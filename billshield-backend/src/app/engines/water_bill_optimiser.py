from __future__ import annotations

from decimal import Decimal

from app.core.constants import ConfidenceLevel, EffortLevel, SavingLabel, UrgencyLevel
from app.engines.ranking_engine import RecommendationCandidate
from app.models.household import Household


def check_water_bill_optimisation(
    household: Household,
) -> list[RecommendationCandidate]:
    candidates: list[RecommendationCandidate] = []

    if household.water_metered is False and household.occupants and household.bedrooms:
        if household.occupants < household.bedrooms:
            potential = Decimal("12")
            candidates.append(
                RecommendationCandidate(
                    engine_type="water_bill_optimiser",
                    title="Check whether a water meter could save money",
                    description=f"You have {household.occupants} people in a {household.bedrooms}-bedroom home and are not metered. A water meter may reduce your bill.",
                    what_detected="Your property is unmetered with more bedrooms than occupants.",
                    why_it_matters="Water meters charge for what you use, which often saves money for smaller households in larger homes.",
                    monthly_saving_pounds=potential,
                    annual_saving_pounds=potential * 12,
                    saving_label=SavingLabel.POTENTIAL_SAVING,
                    effort=EffortLevel.MEDIUM,
                    confidence=ConfidenceLevel.MEDIUM,
                    urgency=UrgencyLevel.LOW,
                    next_step="Use a water meter calculator or contact your water company.",
                    steps=[
                        "Check your water company website for a meter calculator.",
                        "Estimate whether a meter would save you money.",
                        "Apply for a meter — most companies install them free.",
                    ],
                    eligibility_caveat="Water meter savings depend on your actual usage. If you use a lot of water, a meter could cost more.",
                )
            )

    if household.receives_qualifying_benefits and float(household.monthly_water_cost) > 25:
        candidates.append(
            RecommendationCandidate(
                engine_type="water_bill_optimiser",
                title="Check water company social tariff",
                description="Some water companies offer reduced bills for low-income households.",
                what_detected="Your water bill is relatively high and you receive qualifying benefits.",
                why_it_matters="Water social tariffs can cap or reduce your annual water bill.",
                monthly_saving_pounds=Decimal("8"),
                annual_saving_pounds=Decimal("96"),
                saving_label=SavingLabel.POTENTIAL_SAVING,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.ONLY_IF_ELIGIBLE,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Check your water company's website for social tariff or WaterSure eligibility.",
                steps=[
                    "Search your water company's social tariff page.",
                    "Check whether you meet the eligibility criteria.",
                    "Apply if you qualify.",
                ],
                eligibility_caveat="Eligibility varies by water company and usually requires specific benefits or medical conditions.",
            )
        )

    return candidates
