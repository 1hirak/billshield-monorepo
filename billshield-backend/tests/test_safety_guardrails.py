from __future__ import annotations

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
from app.engines.heating_optimisation import check_heating_optimisation
from app.engines.ranking_engine import RecommendationCandidate, rank_recommendations
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
        "has_children": False,
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


class TestHeatingSafetyGuardrails:
    def test_pensioner_household_avoids_aggressive_heating_rec(self):
        household = _make_household(has_pensioner=True)
        candidates = check_heating_optimisation(household)
        for c in candidates:
            assert "reduce" not in c.title.lower() or c.safety_risk != SafetyRiskLevel.NONE

    def test_children_household_gets_safe_only(self):
        household = _make_household(has_children=True)
        candidates = check_heating_optimisation(household)
        for c in candidates:
            assert c.safety_caveat is not None or c.safety_risk == SafetyRiskLevel.NONE

    def test_health_condition_household_gets_guarded_recommendations(self):
        household = _make_household(has_health_condition=True, has_disability=True)
        candidates = check_heating_optimisation(household)
        assert len(candidates) > 0

    def test_unmarked_heating_candidate_has_safety_after_ranking(self):
        candidate = RecommendationCandidate(
            engine_type="heating_optimisation",
            title="Reduce heating by 2°C",
            description="Lower your thermostat",
            what_detected="Detected heating waste",
            why_it_matters="Could save money",
            monthly_saving_pounds=Decimal("15"),
            saving_label=SavingLabel.ESTIMATED_SAVING,
            effort=EffortLevel.LOW,
            confidence=ConfidenceLevel.MEDIUM,
            urgency=UrgencyLevel.MEDIUM,
            safety_risk=SafetyRiskLevel.NONE,
            next_step="Lower thermostat",
        )
        household = _make_household(has_children=True)
        ranked = rank_recommendations([candidate], household)
        assert len(ranked) == 1
        assert ranked[0].safety_risk == SafetyRiskLevel.MEDIUM
        assert ranked[0].safety_caveat is not None


class TestEligibilityLabelling:
    def test_council_tax_labels_as_potential(self):
        from app.engines.council_tax_checker import check_council_tax_reduction
        household = _make_household(income_band=IncomeBand.UNDER_15K)
        candidates = check_council_tax_reduction(household)
        for c in candidates:
            assert c.saving_label == SavingLabel.POTENTIAL_SAVING

    def test_broadband_social_tariff_labels_as_potential(self):
        from app.engines.broadband_social_tariff import check_broadband_social_tariff
        household = _make_household(receives_qualifying_benefits=True, monthly_broadband_mobile_cost=Decimal("50"))
        candidates = check_broadband_social_tariff(household)
        for c in candidates:
            assert c.saving_label == SavingLabel.POTENTIAL_SAVING

    def test_direct_debit_review_labels_as_cashflow(self):
        from app.engines.direct_debit_health import check_direct_debit_health
        from app.models.bill import Bill
        bill = Bill(
            original_filename="bill.pdf",
            content_type="application/pdf",
            file_size_bytes=1000,
            confirmed_fields_json={
                "monthlyDirectDebit": 160,
                "electricityUnitRatePencePerKwh": 27.34,
                "gasUnitRatePencePerKwh": 7.62,
                "electricityStandingChargePencePerDay": 60.12,
                "gasStandingChargePencePerDay": 31.44,
                "annualElectricityUsageKwh": 2900,
                "annualGasUsageKwh": 11000,
            },
        )
        candidates = check_direct_debit_health(bill)
        for c in candidates:
            assert c.saving_label == SavingLabel.CASHFLOW_IMPROVEMENT
