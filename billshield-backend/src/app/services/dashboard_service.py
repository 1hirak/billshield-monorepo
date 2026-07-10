from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.core.constants import (
    DEFAULT_ENERGY_COST_FALLBACK,
    INCOME_BAND_MONTHLY_MAP,
    ConfidenceLevel,
    EffortLevel,
    RecommendationEngineType,
    SafetyRiskLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.core.errors import HouseholdNotFoundError
from app.engines.appliance_time_shifting import check_appliance_time_shifting
from app.engines.broadband_social_tariff import check_broadband_social_tariff
from app.engines.council_tax_checker import check_council_tax_reduction
from app.engines.debt_arrears_triage import triage_debt_arrears
from app.engines.direct_debit_health import check_direct_debit_health
from app.engines.eligibility_scanner import scan_eligibility
from app.engines.food_support import check_food_support
from app.engines.heating_optimisation import check_heating_optimisation
from app.engines.meter_reading_reminder import check_meter_reading_needed
from app.engines.ranking_engine import RecommendationCandidate, rank_recommendations, select_top_actions
from app.engines.standing_charge_awareness import calculate_standing_charges
from app.engines.tariff_checker import check_tariff
from app.engines.water_bill_optimiser import check_water_bill_optimisation
from app.models.household import Household
from app.models.recommendation import Recommendation
from app.repositories.bill_repository import BillRepository
from app.repositories.household_repository import HouseholdRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.household_service import HouseholdService


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.household_repo = HouseholdRepository(db)
        self.bill_repo = BillRepository(db)
        self.rec_repo = RecommendationRepository(db)

    def get_dashboard(self, household_id: str) -> dict[str, Any]:
        household = self.household_repo.get_by_id(household_id)
        if not household:
            raise HouseholdNotFoundError(household_id)

        bills = self.bill_repo.get_by_household(household_id)
        latest_bill = bills[0] if bills else None

        if not bills or (latest_bill and latest_bill.status.value not in ("extracted", "confirmed")):
            return self._build_dashboard_no_bill(household)

        self.rec_repo.delete_by_household(household_id)

        candidates = self._run_all_engines(household, latest_bill)
        ranked = rank_recommendations(candidates, household)
        top, other = select_top_actions(ranked, top_count=3)

        recommendations = self._persist_recommendations(household_id, latest_bill.id if latest_bill else None, ranked)

        summary = self._build_summary(household, latest_bill, top)
        forecast = self._build_forecast(household, latest_bill)
        breakdown = calculate_standing_charges(latest_bill)

        top_count = len(top)
        all_formatted = self._format_recommendations(recommendations)
        top_actions = all_formatted[:top_count]
        other_actions = all_formatted[top_count:]

        insights = self._build_insights(latest_bill)

        return {
            "householdId": household_id,
            "summary": summary,
            "monthlyPressureForecast": forecast,
            "billBreakdown": breakdown,
            "topRecommendedActions": top_actions,
            "otherRecommendedActions": other_actions,
            "insights": insights,
        }

    def _build_dashboard_no_bill(self, household: Household) -> dict[str, Any]:
        income = INCOME_BAND_MONTHLY_MAP.get(household.income_band, 1650)
        pressure = (
            float(household.monthly_rent_or_mortgage)
            + float(household.monthly_food_cost)
            + float(household.monthly_transport_cost)
            + float(household.monthly_council_tax)
            + float(household.monthly_broadband_mobile_cost)
            + float(household.monthly_water_cost)
            + DEFAULT_ENERGY_COST_FALLBACK
        )
        buffer = income - pressure
        energy_ratio = DEFAULT_ENERGY_COST_FALLBACK / income if income > 0 else 0.5
        risk = self._energy_risk_label(energy_ratio)

        return {
            "householdId": str(household.id),
            "summary": {
                "monthlyHouseholdPressure": round(pressure),
                "estimatedDisposableBuffer": round(buffer),
                "energyBillRisk": risk,
                "potentialMonthlySavings": 0,
            },
            "monthlyPressureForecast": [],
            "billBreakdown": None,
            "topRecommendedActions": [{
                "id": "upload_first_bill",
                "rank": 1,
                "engineType": "onboarding",
                "title": "Upload your first energy bill",
                "description": "Upload an energy bill to get personalised savings recommendations.",
                "nextStep": "Go to the bill upload page and upload a recent energy bill.",
                "ctaLabel": "Upload bill",
            }],
            "otherRecommendedActions": [],
            "insights": [],
        }

    def _run_all_engines(self, household: Household, bill) -> list[RecommendationCandidate]:
        candidates: list[RecommendationCandidate] = []
        candidates.extend(check_tariff(household, bill))
        candidates.extend(check_direct_debit_health(bill))
        candidates.extend(check_meter_reading_needed())
        candidates.extend(check_heating_optimisation(household))
        candidates.extend(check_appliance_time_shifting(bill))
        candidates.extend(scan_eligibility(household))
        candidates.extend(check_council_tax_reduction(household))
        candidates.extend(check_broadband_social_tariff(household))
        candidates.extend(check_water_bill_optimisation(household))
        candidates.extend(check_food_support(household))
        candidates.extend(triage_debt_arrears(household))
        return candidates

    def _persist_recommendations(
        self,
        household_id: str,
        bill_id: str | None,
        ranked: list[RecommendationCandidate],
    ) -> list[Recommendation]:
        records: list[Recommendation] = []
        for rank_idx, candidate in enumerate(ranked, start=1):
            engine_type = candidate.engine_type
            try:
                engine_enum = RecommendationEngineType(engine_type)
            except ValueError:
                engine_enum = RecommendationEngineType.TARIFF_CHECK

            rec = Recommendation(
                household_id=household_id,
                bill_id=bill_id,
                engine_type=engine_enum,
                rank=rank_idx,
                title=candidate.title,
                description=candidate.description,
                what_detected=candidate.what_detected,
                why_it_matters=candidate.why_it_matters,
                monthly_saving_pounds=candidate.monthly_saving_pounds,
                annual_saving_pounds=candidate.annual_saving_pounds,
                saving_label=candidate.saving_label,
                effort=candidate.effort,
                confidence=candidate.confidence,
                urgency=candidate.urgency,
                safety_risk=candidate.safety_risk,
                eligibility_caveat=candidate.eligibility_caveat,
                safety_caveat=candidate.safety_caveat,
                next_step=candidate.next_step,
                steps_json={"steps": candidate.steps} if candidate.steps else None,
                call_script=candidate.call_script,
            )
            records.append(rec)

        return self.rec_repo.create_many(records)

    def _build_summary(self, household: Household, bill, top) -> dict[str, Any]:
        income = INCOME_BAND_MONTHLY_MAP.get(household.income_band, 1650)
        energy_cost = self._get_energy_cost(bill)
        pressure = (
            float(household.monthly_rent_or_mortgage)
            + float(household.monthly_food_cost)
            + float(household.monthly_transport_cost)
            + float(household.monthly_council_tax)
            + float(household.monthly_broadband_mobile_cost)
            + float(household.monthly_water_cost)
            + energy_cost
        )
        buffer = income - pressure
        energy_ratio = energy_cost / income if income > 0 else 0.5
        risk = self._energy_risk_label(energy_ratio)

        potential_savings = sum(
            float(c.monthly_saving_pounds or 0) for c in top
            if c.saving_label not in (SavingLabel.GREEN_ONLY, SavingLabel.NO_DIRECT_SAVING)
        )

        return {
            "monthlyHouseholdPressure": round(pressure),
            "estimatedDisposableBuffer": round(buffer),
            "energyBillRisk": risk,
            "potentialMonthlySavings": round(potential_savings),
        }

    def _get_energy_cost(self, bill) -> float:
        if not bill or not bill.confirmed_fields_json:
            return DEFAULT_ENERGY_COST_FALLBACK
        monthly_dd = bill.confirmed_fields_json.get("monthlyDirectDebit")
        if monthly_dd:
            return float(monthly_dd)
        return DEFAULT_ENERGY_COST_FALLBACK

    @staticmethod
    def _energy_risk_label(ratio: float) -> str:
        if ratio < 0.08:
            return "low"
        elif ratio < 0.12:
            return "medium"
        elif ratio < 0.18:
            return "medium_high"
        return "high"

    def _build_forecast(self, household: Household, bill) -> list[dict]:
        energy_base = self._get_energy_cost(bill)
        months = [
            ("Jul", 1.00),
            ("Aug", 0.97),
            ("Sep", 1.03),
            ("Oct", 1.11),
        ]
        return [
            {
                "month": m,
                "energy": round(energy_base * factor),
                "rent": float(household.monthly_rent_or_mortgage),
                "food": round(float(household.monthly_food_cost) * (1 + i * 0.01)),
                "transport": float(household.monthly_transport_cost),
                "councilTax": float(household.monthly_council_tax),
                "water": float(household.monthly_water_cost),
                "broadbandMobile": float(household.monthly_broadband_mobile_cost),
            }
            for i, (m, factor) in enumerate(months)
        ]

    def _format_recommendations(self, recommendations: list[Recommendation]) -> list[dict]:
        formatted = []
        for rec in recommendations:
            steps = []
            if rec.steps_json and isinstance(rec.steps_json, dict):
                steps = rec.steps_json.get("steps", [])

            formatted.append({
                "id": str(rec.id),
                "rank": rec.rank,
                "engineType": rec.engine_type.value,
                "title": rec.title,
                "description": rec.description,
                "whatDetected": rec.what_detected,
                "whyItMatters": rec.why_it_matters,
                "monthlySavingPounds": float(rec.monthly_saving_pounds) if rec.monthly_saving_pounds else None,
                "annualSavingPounds": float(rec.annual_saving_pounds) if rec.annual_saving_pounds else None,
                "savingLabel": rec.saving_label.value,
                "effort": rec.effort.value,
                "confidence": rec.confidence.value,
                "urgency": rec.urgency.value,
                "safetyRisk": rec.safety_risk.value,
                "eligibilityCaveat": rec.eligibility_caveat,
                "safetyCaveat": rec.safety_caveat,
                "nextStep": rec.next_step,
                "steps": steps,
                "ctaLabel": "View steps",
                "callScript": rec.call_script,
            })
        return formatted

    def _build_insights(self, bill) -> list[dict]:
        insights = [
            {
                "type": "info",
                "title": "Standing charges still apply",
                "body": "Even if you used no energy this month, standing charges would still be on your bill.",
            },
        ]

        if bill and bill.confirmed_fields_json:
            if bill.confirmed_fields_json.get("tariffType") == "standard_variable":
                insights.append({
                    "type": "caution",
                    "title": "Submit readings around price changes",
                    "body": "Submitting meter readings near quarterly price-cap changes can reduce estimated billing errors.",
                })

        return insights
