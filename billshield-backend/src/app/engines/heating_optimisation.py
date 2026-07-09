from __future__ import annotations

from decimal import Decimal

from app.core.constants import ConfidenceLevel, EffortLevel, SafetyRiskLevel, SavingLabel, UrgencyLevel
from app.engines.ranking_engine import RecommendationCandidate
from app.models.household import Household


def check_heating_optimisation(
    household: Household,
) -> list[RecommendationCandidate]:
    candidates: list[RecommendationCandidate] = []

    is_vulnerable = any(
        [
            household.has_children,
            household.has_pensioner,
            household.has_health_condition,
            household.has_disability,
        ]
    )

    if is_vulnerable:
        candidates.extend(
            [
                RecommendationCandidate(
                    engine_type="heating_optimisation",
                    title="Close curtains at dusk",
                    description="Closing curtains when it gets dark helps keep warmth in.",
                    what_detected="Simple draught-proofing can reduce heat loss with no cost.",
                    why_it_matters="This is a low-effort, no-cost way to keep your home warmer.",
                    monthly_saving_pounds=Decimal("3"),
                    annual_saving_pounds=Decimal("36"),
                    saving_label=SavingLabel.ESTIMATED_SAVING,
                    effort=EffortLevel.LOW,
                    confidence=ConfidenceLevel.MEDIUM,
                    urgency=UrgencyLevel.LOW,
                    safety_risk=SafetyRiskLevel.NONE,
                    next_step="Make sure curtains and blinds are closed at dusk.",
                    steps=[
                        "Close all curtains or blinds when it gets dark.",
                        "Tuck curtains behind radiators (if safe and not covering vents) to direct heat into the room.",
                    ],
                    safety_caveat="Keep regularly used rooms at a safe temperature, especially for older people, children, or anyone with health conditions.",
                ),
                RecommendationCandidate(
                    engine_type="heating_optimisation",
                    title="Bleed your radiators if rooms heat unevenly",
                    description="If some radiators are cold at the top, bleeding them can improve efficiency.",
                    what_detected="Cold spots on radiators may mean trapped air.",
                    why_it_matters="Bleeding radiators can make your heating system run more efficiently.",
                    monthly_saving_pounds=Decimal("5"),
                    annual_saving_pounds=Decimal("60"),
                    saving_label=SavingLabel.ESTIMATED_SAVING,
                    effort=EffortLevel.LOW,
                    confidence=ConfidenceLevel.MEDIUM,
                    urgency=UrgencyLevel.LOW,
                    safety_risk=SafetyRiskLevel.LOW,
                    safety_caveat="Keep regularly used rooms at a safe temperature, especially for older people, children, or anyone with health conditions.",
                    next_step="Check whether your radiators have cold spots at the top.",
                    steps=[
                        "Turn off your heating and let radiators cool.",
                        "Use a radiator key to open the bleed valve slowly.",
                        "Close the valve when water appears.",
                        "Check boiler pressure afterwards if needed.",
                    ],
                ),
            ]
        )
    else:
        candidates.append(
            RecommendationCandidate(
                engine_type="heating_optimisation",
                title="Use heating timers to match your routine",
                description="Set timers so heating is on when you need it and lower when you are out or asleep.",
                what_detected="Using heating timers can reduce waste.",
                why_it_matters="You may be able to reduce energy use without reducing comfort.",
                monthly_saving_pounds=Decimal("10"),
                annual_saving_pounds=Decimal("120"),
                saving_label=SavingLabel.ESTIMATED_SAVING,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.MEDIUM,
                urgency=UrgencyLevel.LOW,
                safety_risk=SafetyRiskLevel.LOW,
                safety_caveat="Keep regularly used rooms at a safe temperature, especially for older people, children, or anyone with health conditions.",
                next_step="Check your heating timer settings and adjust them to your routine.",
                steps=[
                    "Set heating to come on 30 minutes before waking and turn off 30 minutes before bed.",
                    "Programme different weekend and weekday schedules if your routine changes.",
                    "Keep at least 18°C in regularly used rooms.",
                ],
            )
        )

    candidates.append(
        RecommendationCandidate(
            engine_type="heating_optimisation",
            title="Draught-proof gaps around doors and windows",
            description="Simple draught-proofing can reduce heat loss with low-cost materials.",
            what_detected="Gaps around doors and windows let warm air escape.",
            why_it_matters="Draught-proofing is one of the cheapest and most effective ways to keep warmth in.",
            monthly_saving_pounds=Decimal("4"),
            annual_saving_pounds=Decimal("48"),
            saving_label=SavingLabel.ESTIMATED_SAVING,
            effort=EffortLevel.LOW,
            confidence=ConfidenceLevel.MEDIUM,
            urgency=UrgencyLevel.LOW,
            safety_risk=SafetyRiskLevel.NONE,
            next_step="Check for draughts around doors and windows.",
            steps=[
                "Identify gaps around external doors and windows.",
                "Use low-cost draught strips, brushes, or sealant.",
                "Do not block intentional ventilation (e.g., bathroom or kitchen vents).",
            ],
        )
    )

    return candidates
