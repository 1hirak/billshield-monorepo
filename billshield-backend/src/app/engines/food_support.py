from __future__ import annotations

from decimal import Decimal

from app.core.constants import (
    INCOME_BAND_MONTHLY_MAP,
    ConfidenceLevel,
    EffortLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.engines.ranking_engine import RecommendationCandidate
from app.models.household import Household


def check_food_support(
    household: Household,
) -> list[RecommendationCandidate]:
    candidates: list[RecommendationCandidate] = []

    estimated_income = INCOME_BAND_MONTHLY_MAP.get(household.income_band, 1650)
    food_pressure_ratio = float(household.monthly_food_cost) / estimated_income if estimated_income > 0 else 0

    high_food_pressure = food_pressure_ratio > 0.15

    if household.has_children:
        candidates.append(
            RecommendationCandidate(
                engine_type="food_support",
                title="Check eligibility for free school meals",
                description="Children in England may qualify for free school meals if you receive certain benefits.",
                what_detected="Your household includes children.",
                why_it_matters="Free school meals can save around £450 per child per year.",
                monthly_saving_pounds=Decimal("37"),
                annual_saving_pounds=Decimal("450"),
                saving_label=SavingLabel.SUPPORT_VALUE,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.ONLY_IF_ELIGIBLE if not household.receives_qualifying_benefits else ConfidenceLevel.MEDIUM,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Check your local council's free school meals page.",
                steps=[
                    "Visit your local council website and search free school meals.",
                    "Check whether your benefits or income level qualifies.",
                    "Apply online — it usually takes a few days.",
                ],
                eligibility_caveat="Eligibility is usually linked to specific benefits. Check your local council rules.",
            )
        )

        candidates.append(
            RecommendationCandidate(
                engine_type="food_support",
                title="Check Healthy Start vouchers",
                description="If you are pregnant or have children under 4, you may qualify for Healthy Start vouchers for milk, fruit, and vegetables.",
                what_detected="Your household includes young children.",
                why_it_matters="Healthy Start provides £4.25 per week per child towards healthy food.",
                monthly_saving_pounds=Decimal("17"),
                annual_saving_pounds=Decimal("204"),
                saving_label=SavingLabel.SUPPORT_VALUE,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.ONLY_IF_ELIGIBLE,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Check the NHS Healthy Start website.",
                steps=[
                    "Visit the NHS Healthy Start website.",
                    "Check if you qualify based on benefits or income.",
                    "Apply online or via your health visitor.",
                ],
                eligibility_caveat="Available for pregnant women or children under 4 in qualifying households.",
            )
        )

    if high_food_pressure or (household.receives_qualifying_benefits and float(household.monthly_food_cost) > 250):
        candidates.append(
            RecommendationCandidate(
                engine_type="food_support",
                title="Local food support options are available",
                description="Your food costs are high relative to income. Local food banks and community pantries can provide immediate help.",
                what_detected="Your monthly food pressure is high.",
                why_it_matters="Food banks and pantries can provide emergency support while you work on longer-term changes.",
                monthly_saving_pounds=Decimal("40"),
                annual_saving_pounds=None,
                saving_label=SavingLabel.SUPPORT_ACCESS,
                effort=EffortLevel.MEDIUM,
                confidence=ConfidenceLevel.MEDIUM,
                urgency=UrgencyLevel.HIGH if high_food_pressure else UrgencyLevel.MEDIUM,
                next_step="Check the support services page for local food banks and community pantries.",
                steps=[
                    "Visit the support services page on your dashboard.",
                    "Find the nearest food bank or community pantry.",
                    "Contact them or check referral requirements.",
                    "You can also contact Citizens Advice for a food bank voucher.",
                ],
                eligibility_caveat="Some food banks require a referral from Citizens Advice, a GP, or social worker.",
            )
        )

    return candidates
