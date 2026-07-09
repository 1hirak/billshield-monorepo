from __future__ import annotations

from decimal import Decimal

from app.core.constants import ConfidenceLevel, EffortLevel, SavingLabel, UrgencyLevel
from app.engines.ranking_engine import RecommendationCandidate
from app.models.household import Household


def scan_eligibility(
    household: Household,
) -> list[RecommendationCandidate]:
    candidates: list[RecommendationCandidate] = []

    if household.has_disability or household.has_health_condition or household.has_pensioner:
        candidates.append(
            RecommendationCandidate(
                engine_type="eligibility_scanner",
                title="Check Priority Services Register eligibility",
                description="You may be able to join your energy supplier's Priority Services Register for extra support.",
                what_detected="Your household profile indicates you or someone in your home may be eligible.",
                why_it_matters="The Priority Services Register provides free extra services such as advance notice of power cuts, priority reconnection, and accessible billing.",
                monthly_saving_pounds=None,
                annual_saving_pounds=None,
                saving_label=SavingLabel.SUPPORT_VALUE,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.MEDIUM,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Contact your energy supplier and ask to join the Priority Services Register.",
                steps=[
                    "Call your energy supplier or check their website.",
                    "Ask to be added to the Priority Services Register.",
                    "No charge — it is a free service.",
                ],
            )
        )

    if household.receives_qualifying_benefits:
        candidates.append(
            RecommendationCandidate(
                engine_type="eligibility_scanner",
                title="You may qualify for the Warm Home Discount",
                description="The Warm Home Discount provides a one-off reduction on electricity bills for eligible households.",
                what_detected="Your profile indicates you receive qualifying benefits.",
                why_it_matters="This is a government scheme that reduces your bill — it does not need to be repaid.",
                monthly_saving_pounds=Decimal("12"),
                annual_saving_pounds=Decimal("150"),
                saving_label=SavingLabel.SUPPORT_VALUE,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.ONLY_IF_ELIGIBLE,
                urgency=UrgencyLevel.HIGH,
                next_step="Check with your electricity supplier whether you are eligible.",
                steps=[
                    "Check whether your supplier is part of the scheme.",
                    "Most eligible households receive it automatically if they claim certain benefits.",
                    "Contact your supplier to confirm.",
                ],
                eligibility_caveat="Eligibility depends on your specific benefits, supplier, and the scheme year rules.",
            )
        )

        candidates.append(
            RecommendationCandidate(
                engine_type="eligibility_scanner",
                title="Check if your supplier offers a hardship grant",
                description="Some energy suppliers provide grants to customers struggling with bills.",
                what_detected="Your profile suggests you may be under financial pressure.",
                why_it_matters="Supplier hardship grants can reduce arrears and do not need to be repaid.",
                monthly_saving_pounds=Decimal("25"),
                annual_saving_pounds=None,
                saving_label=SavingLabel.SUPPORT_VALUE,
                effort=EffortLevel.MEDIUM,
                confidence=ConfidenceLevel.ONLY_IF_ELIGIBLE,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Ask your energy supplier whether they offer a hardship or support fund.",
                steps=[
                    "Contact your supplier's customer support.",
                    "Ask about their hardship fund or support grant.",
                    "You may need to provide income and household details.",
                ],
                eligibility_caveat="Grants vary by supplier and are usually for customers in arrears or at risk.",
                call_script="I'm struggling to pay my energy bill. Do you have a hardship grant or support fund I could apply for?",
            )
        )

    return candidates
