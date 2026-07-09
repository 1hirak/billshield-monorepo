from __future__ import annotations

from decimal import Decimal

from app.core.constants import ConfidenceLevel, EffortLevel, SavingLabel, UrgencyLevel
from app.engines.ranking_engine import RecommendationCandidate
from app.models.household import Household


def check_broadband_social_tariff(
    household: Household,
) -> list[RecommendationCandidate]:
    candidates: list[RecommendationCandidate] = []

    broadband_cost = float(household.monthly_broadband_mobile_cost)
    if broadband_cost < 25:
        return candidates

    if household.receives_qualifying_benefits or broadband_cost > 35:
        amount = min(broadband_cost - 15, 25)
        candidates.append(
            RecommendationCandidate(
                engine_type="broadband_social_tariff_checker",
                title="Check broadband social tariff",
                description="Some households on qualifying benefits can access cheaper broadband packages.",
                what_detected=f"Your broadband and mobile cost is £{round(broadband_cost)}/month, and your profile suggests you may be eligible for support.",
                why_it_matters="Social tariffs are normal broadband packages at lower prices for eligible low-income households.",
                monthly_saving_pounds=Decimal(str(round(amount))),
                annual_saving_pounds=Decimal(str(round(amount * 12))),
                saving_label=SavingLabel.POTENTIAL_SAVING,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.MEDIUM if household.receives_qualifying_benefits else ConfidenceLevel.ONLY_IF_ELIGIBLE,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Check whether your current provider offers a social tariff.",
                steps=[
                    "Check if anyone in the household receives a qualifying benefit.",
                    "Search your provider's social tariff page.",
                    "Ask to switch without exit fees if eligible.",
                ],
                eligibility_caveat="Usually requires Universal Credit, Pension Credit, or another qualifying benefit.",
            )
        )

    return candidates
