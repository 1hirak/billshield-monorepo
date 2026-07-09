from __future__ import annotations

from decimal import Decimal

from app.core.constants import (
    INCOME_BAND_MONTHLY_MAP,
    ConfidenceLevel,
    EffortLevel,
    HouseholdType,
    IncomeBand,
    SavingLabel,
    UrgencyLevel,
)
from app.engines.ranking_engine import RecommendationCandidate
from app.models.household import Household


def check_council_tax_reduction(
    household: Household,
) -> list[RecommendationCandidate]:
    candidates: list[RecommendationCandidate] = []

    pressure_ratio = float(household.monthly_council_tax) / INCOME_BAND_MONTHLY_MAP.get(
        household.income_band, 1650
    )

    if household.income_band in (IncomeBand.UNDER_15K, IncomeBand.FIFTEEN_TO_25K) or (
        pressure_ratio > 0.08 and household.income_band == IncomeBand.TWENTYFIVE_TO_40K
    ):
        amount = 35 if household.income_band == IncomeBand.UNDER_15K else 25
        candidates.append(
            RecommendationCandidate(
                engine_type="council_tax_reduction_checker",
                title="Check Council Tax Reduction",
                description="Your income band and household profile may qualify for a reduction in council tax.",
                what_detected="Your council tax is high relative to your income band.",
                why_it_matters="Council Tax Reduction can reduce monthly pressure for eligible households.",
                monthly_saving_pounds=Decimal(str(amount)),
                annual_saving_pounds=Decimal(str(amount * 12)),
                saving_label=SavingLabel.POTENTIAL_SAVING,
                effort=EffortLevel.MEDIUM,
                confidence=ConfidenceLevel.MEDIUM,
                urgency=UrgencyLevel.HIGH,
                next_step="Check your local council's Council Tax Reduction application page.",
                steps=[
                    "Find your local council using your postcode.",
                    "Check the Council Tax Reduction eligibility rules.",
                    "Prepare income, savings, rent, and household details.",
                    "Apply online or contact the council if you need help.",
                ],
                eligibility_caveat="Eligibility depends on your local council, income, savings, and household circumstances.",
            )
        )

    if household.household_type == HouseholdType.SINGLE_ADULT:
        candidates.append(
            RecommendationCandidate(
                engine_type="council_tax_reduction_checker",
                title="Check single-person council tax discount",
                description="You may be entitled to a 25% single-person discount on your council tax.",
                what_detected="You are the only adult in your household.",
                why_it_matters="Single-person discount is a straightforward 25% reduction.",
                monthly_saving_pounds=Decimal(str(round(float(household.monthly_council_tax) * 0.25))),
                annual_saving_pounds=Decimal(str(round(float(household.monthly_council_tax) * 0.25 * 12))),
                saving_label=SavingLabel.POTENTIAL_SAVING,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Apply for the single-person discount on your local council website.",
                steps=[
                    "Visit your local council website.",
                    "Apply for the single-person council tax discount.",
                    "This is usually applied quickly once confirmed.",
                ],
                eligibility_caveat="You must be the only person over 18 living in the property.",
            )
        )

    return candidates
