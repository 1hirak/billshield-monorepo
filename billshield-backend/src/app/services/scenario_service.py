from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.core.constants import ConfidenceLevel, SavingLabel
from app.core.errors import BillNotFoundError, HouseholdNotFoundError, InvalidScenarioError
from app.core.logging import get_logger
from app.models.household import Household
from app.repositories.bill_repository import BillRepository
from app.repositories.household_repository import HouseholdRepository
from app.schemas.scenario import SimulateScenarioRequest

logger = get_logger(__name__)


class ScenarioService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.household_repo = HouseholdRepository(db)
        self.bill_repo = BillRepository(db)

    def simulate(self, data: SimulateScenarioRequest) -> dict[str, Any]:
        household = self.household_repo.get_by_id(data.household_id)
        if not household:
            raise HouseholdNotFoundError(data.household_id)

        bill = None
        if data.bill_id:
            bill = self.bill_repo.get_by_id(data.bill_id)
            if not bill:
                raise BillNotFoundError(data.bill_id)

        is_vulnerable = any([
            household.has_children,
            household.has_pensioner,
            household.has_health_condition,
            household.has_disability,
        ])

        breakdown: list[dict] = []
        safety_warnings: list[str] = []
        tariff_warnings: list[str] = []
        total_monthly = Decimal("0")

        if data.request_direct_debit_review:
            saving = Decimal("22")
            total_monthly += saving
            breakdown.append({
                "category": "Direct Debit review",
                "monthlySaving": float(saving),
                "confidence": "high",
                "savingLabel": "cashflow_improvement",
            })

        if data.apply_for_council_tax_reduction:
            saving = Decimal("35")
            total_monthly += saving
            breakdown.append({
                "category": "Council tax support",
                "monthlySaving": float(saving),
                "confidence": "medium",
                "savingLabel": "potential_saving",
            })

        if data.switch_to_social_broadband_tariff:
            saving = Decimal("18")
            total_monthly += saving
            breakdown.append({
                "category": "Broadband social tariff",
                "monthlySaving": float(saving),
                "confidence": "medium",
                "savingLabel": "potential_saving",
            })

        if data.shift_appliances_to_off_peak:
            tariff_type = "standard_variable"
            if bill and bill.confirmed_fields_json:
                tariff_type = bill.confirmed_fields_json.get("tariffType", "standard_variable")

            if tariff_type in ("fixed", "standard_variable", "prepayment", "other"):
                tariff_warnings.append(
                    "On flat tariffs, off-peak appliance use may be greener but not cheaper. "
                    "Off-peak scheduling usually saves money only on Economy 7, time-of-use, EV, battery, or smart off-peak tariffs."
                )
                breakdown.append({
                    "category": "Appliance changes",
                    "monthlySaving": 0,
                    "confidence": "high",
                    "savingLabel": "green_only",
                })
            else:
                saving = Decimal("7")
                total_monthly += saving
                breakdown.append({
                    "category": "Appliance changes",
                    "monthlySaving": float(saving),
                    "confidence": "only_if_tariff_eligible",
                    "savingLabel": "potential_saving",
                })

        if data.check_water_meter_or_social_tariff:
            saving = Decimal("8")
            total_monthly += saving
            breakdown.append({
                "category": "Water support",
                "monthlySaving": float(saving),
                "confidence": "only_if_eligible",
                "savingLabel": "potential_saving",
            })

        if data.heating_reduction_celsius > 0:
            if is_vulnerable:
                safety_warnings.append(
                    "BillShield will not recommend unsafe under-heating. "
                    "Keep regularly used rooms at a safe temperature, especially for older people, children, or anyone with health conditions."
                )
            else:
                saving = Decimal(str(round(data.heating_reduction_celsius * 5)))
                total_monthly += saving
                breakdown.append({
                    "category": "Heating reduction",
                    "monthlySaving": float(saving),
                    "confidence": "medium",
                    "savingLabel": "estimated_saving",
                })

        notes = [
            "Potential support savings depend on eligibility and local rules.",
            "Direct Debit changes improve cashflow but may not reduce annual energy use.",
            "Heating changes should only be made where the home remains safe and warm enough.",
        ]

        overall_confidence = "medium"
        overall_risk = "low"
        if is_vulnerable:
            overall_risk = "medium"
        if total_monthly < 30:
            overall_confidence = "low"

        return {
            "householdId": data.household_id,
            "estimatedMonthlySaving": round(float(total_monthly)),
            "estimatedAnnualSaving": round(float(total_monthly * 12)),
            "confidence": overall_confidence,
            "overallRisk": overall_risk,
            "safetyWarning": safety_warnings[0] if safety_warnings else None,
            "tariffWarning": tariff_warnings[0] if tariff_warnings else None,
            "breakdown": breakdown,
            "notes": notes,
        }
