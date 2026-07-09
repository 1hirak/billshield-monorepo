from __future__ import annotations

import pytest
from decimal import Decimal

from app.core.constants import (
    ConfidenceLevel,
    EffortLevel,
    HouseholdType,
    IncomeBand,
    PaymentMethod,
    SafetyRiskLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.engines.appliance_time_shifting import check_appliance_time_shifting
from app.engines.broadband_social_tariff import check_broadband_social_tariff
from app.engines.council_tax_checker import check_council_tax_reduction
from app.engines.direct_debit_health import check_direct_debit_health
from app.engines.heating_optimisation import check_heating_optimisation
from app.engines.ranking_engine import (
    RecommendationCandidate,
    rank_recommendations,
    select_top_actions,
)
from app.engines.standing_charge_awareness import calculate_standing_charges
from app.models.bill import Bill
from app.models.household import Household


def _make_household(**overrides) -> Household:
    defaults = {
        "postcode": "BS1 4ST",
        "normalized_postcode": "BS14ST",
        "household_type": HouseholdType.FAMILY_WITH_CHILDREN,
        "income_band": IncomeBand.FIFTEEN_TO_25K,
        "energy_provider": "BrightSpark Energy",
        "payment_method": PaymentMethod.DIRECT_DEBIT,
        "monthly_rent_or_mortgage": Decimal("850"),
        "monthly_food_cost": Decimal("360"),
        "monthly_transport_cost": Decimal("155"),
        "monthly_council_tax": Decimal("168"),
        "monthly_broadband_mobile_cost": Decimal("52"),
        "monthly_water_cost": Decimal("39"),
        "receives_qualifying_benefits": True,
        "has_children": True,
        "has_pensioner": False,
        "has_health_condition": False,
        "has_disability": False,
        "is_single_adult": False,
        "bedrooms": 3,
        "occupants": 4,
        "water_metered": False,
    }
    defaults.update(overrides)
    return Household(**defaults)


def _make_bill(**fields) -> Bill:
    defaults = {
        "original_filename": "bill.pdf",
        "content_type": "application/pdf",
        "file_size_bytes": 1000,
        "confirmed_fields_json": {
            "supplier": "BrightSpark Energy",
            "tariffName": "Standard Variable Direct",
            "monthlyDirectDebit": 142,
            "electricityUnitRatePencePerKwh": 27.34,
            "electricityStandingChargePencePerDay": 60.12,
            "gasUnitRatePencePerKwh": 7.62,
            "gasStandingChargePencePerDay": 31.44,
            "annualElectricityUsageKwh": 2900,
            "annualGasUsageKwh": 11000,
            "paymentMethod": "direct_debit",
            "tariffType": "standard_variable",
        },
    }
    defaults.update(fields)
    return Bill(**defaults)


class TestDirectDebitHealth:
    def test_dd_too_high_creates_review(self):
        bill = _make_bill(confirmed_fields_json={
            "monthlyDirectDebit": 180,
            "electricityUnitRatePencePerKwh": 27.34,
            "gasUnitRatePencePerKwh": 7.62,
            "electricityStandingChargePencePerDay": 60.12,
            "gasStandingChargePencePerDay": 31.44,
            "annualElectricityUsageKwh": 2900,
            "annualGasUsageKwh": 11000,
        })
        candidates = check_direct_debit_health(bill)
        assert len(candidates) > 0
        rec = candidates[0]
        assert rec.saving_label == SavingLabel.CASHFLOW_IMPROVEMENT
        assert rec.monthly_saving_pounds is not None

    def test_dd_too_low_creates_risk(self):
        bill = _make_bill(confirmed_fields_json={
            "monthlyDirectDebit": 50,
            "electricityUnitRatePencePerKwh": 27.34,
            "gasUnitRatePencePerKwh": 7.62,
            "electricityStandingChargePencePerDay": 60.12,
            "gasStandingChargePencePerDay": 31.44,
            "annualElectricityUsageKwh": 2900,
            "annualGasUsageKwh": 11000,
        })
        candidates = check_direct_debit_health(bill)
        assert len(candidates) > 0
        rec = candidates[0]
        assert rec.saving_label == SavingLabel.RISK_REDUCTION

    def test_dd_healthy_returns_empty(self):
        bill = _make_bill(confirmed_fields_json={
            "monthlyDirectDebit": 120,
            "electricityUnitRatePencePerKwh": 27.34,
            "gasUnitRatePencePerKwh": 7.62,
            "electricityStandingChargePencePerDay": 60.12,
            "gasStandingChargePencePerDay": 31.44,
            "annualElectricityUsageKwh": 2000,
            "annualGasUsageKwh": 7000,
        })
        candidates = check_direct_debit_health(bill)
        assert len(candidates) == 0

    def test_no_confirmed_bill_returns_generic(self):
        bill_no_confirmed = _make_bill()
        bill_no_confirmed.confirmed_fields_json = None
        candidates = check_direct_debit_health(bill_no_confirmed)
        assert len(candidates) > 0
        assert candidates[0].confidence == ConfidenceLevel.NEEDS_REVIEW


class TestCouncilTaxChecker:
    def test_low_income_creates_council_tax_rec(self):
        household = _make_household(income_band=IncomeBand.UNDER_15K)
        candidates = check_council_tax_reduction(household)
        assert len(candidates) > 0
        rec = candidates[0]
        assert rec.saving_label == SavingLabel.POTENTIAL_SAVING
        assert "may qualify" in rec.title.lower() or "check" in rec.title.lower()

    def test_high_income_no_rec(self):
        household = _make_household(income_band=IncomeBand.SIXTY_PLUS)
        candidates = check_council_tax_reduction(household)
        assert len(candidates) == 0


class TestBroadbandChecker:
    def test_qualifying_benefits_creates_rec(self):
        household = _make_household(receives_qualifying_benefits=True, monthly_broadband_mobile_cost=Decimal("52"))
        candidates = check_broadband_social_tariff(household)
        assert len(candidates) > 0
        assert candidates[0].saving_label == SavingLabel.POTENTIAL_SAVING

    def test_low_cost_no_rec(self):
        household = _make_household(monthly_broadband_mobile_cost=Decimal("20"))
        candidates = check_broadband_social_tariff(household)
        assert len(candidates) == 0


class TestApplianceShifting:
    def test_flat_tariff_returns_green_only(self):
        bill = _make_bill(confirmed_fields_json={"tariffType": "standard_variable"})
        candidates = check_appliance_time_shifting(bill)
        assert len(candidates) > 0
        assert candidates[0].saving_label == SavingLabel.GREEN_ONLY

    def test_economy7_tariff_returns_potential_saving(self):
        bill = _make_bill(confirmed_fields_json={"tariffType": "economy_7"})
        candidates = check_appliance_time_shifting(bill)
        assert len(candidates) > 0
        assert candidates[0].saving_label == SavingLabel.POTENTIAL_SAVING


class TestHeatingSafety:
    def test_vulnerable_household_gets_safe_advice(self):
        household = _make_household(has_pensioner=True)
        candidates = check_heating_optimisation(household)
        assert len(candidates) > 0
        for c in candidates:
            assert c.safety_caveat is not None or c.safety_risk != SafetyRiskLevel.MEDIUM

    def test_non_vulnerable_gets_timer_advice(self):
        household = _make_household(has_children=False, has_pensioner=False, has_health_condition=False, has_disability=False)
        candidates = check_heating_optimisation(household)
        titles = [c.title.lower() for c in candidates]
        assert any("timer" in t for t in titles)


class TestStandingChargeInsight:
    def test_calculates_fixed_costs(self):
        bill = _make_bill()
        breakdown = calculate_standing_charges(bill)
        assert "standingChargesMonthly" in breakdown
        assert breakdown["standingChargesMonthly"] > 0
        assert breakdown["avoidableCostMonthly"] > 0


class TestRankingEngine:
    def test_returns_top_three(self):
        candidates = [
            RecommendationCandidate(
                engine_type="direct_debit_health_check",
                title="DD too high",
                description="",
                what_detected="",
                why_it_matters="",
                monthly_saving_pounds=Decimal("22"),
                saving_label=SavingLabel.CASHFLOW_IMPROVEMENT,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Submit reading",
            ),
            RecommendationCandidate(
                engine_type="council_tax_reduction_checker",
                title="Council tax help",
                description="",
                what_detected="",
                why_it_matters="",
                monthly_saving_pounds=Decimal("35"),
                saving_label=SavingLabel.POTENTIAL_SAVING,
                effort=EffortLevel.MEDIUM,
                confidence=ConfidenceLevel.MEDIUM,
                urgency=UrgencyLevel.HIGH,
                next_step="Apply",
            ),
            RecommendationCandidate(
                engine_type="broadband_social_tariff_checker",
                title="Broadband social tariff",
                description="",
                what_detected="",
                why_it_matters="",
                monthly_saving_pounds=Decimal("18"),
                saving_label=SavingLabel.POTENTIAL_SAVING,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.MEDIUM,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Check",
            ),
            RecommendationCandidate(
                engine_type="appliance_time_shifting",
                title="Off-peak appliances",
                description="",
                what_detected="",
                why_it_matters="",
                monthly_saving_pounds=Decimal("0"),
                saving_label=SavingLabel.GREEN_ONLY,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.LOW,
                next_step="Check tariff",
            ),
        ]
        household = _make_household()
        ranked = rank_recommendations(candidates, household)
        top, other = select_top_actions(ranked, top_count=3)
        assert len(top) == 3

    def test_high_safety_risk_excluded_from_top(self):
        candidates = [
            RecommendationCandidate(
                engine_type="heating_optimisation",
                title="Unsafe lowering",
                description="",
                what_detected="",
                why_it_matters="",
                monthly_saving_pounds=Decimal("50"),
                saving_label=SavingLabel.ESTIMATED_SAVING,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.HIGH,
                safety_risk=SafetyRiskLevel.HIGH,
                next_step="Lower",
            ),
            RecommendationCandidate(
                engine_type="direct_debit_health_check",
                title="Safe action",
                description="",
                what_detected="",
                why_it_matters="",
                monthly_saving_pounds=Decimal("10"),
                saving_label=SavingLabel.CASHFLOW_IMPROVEMENT,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.LOW,
                next_step="Review",
            ),
        ]
        household = _make_household()
        ranked = rank_recommendations(candidates, household)
        high_safety = [c for c in ranked if c.safety_risk == SafetyRiskLevel.HIGH]
        assert len(high_safety) == 0
