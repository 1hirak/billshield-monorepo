from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from app.core.constants import (
    ConfidenceLevel,
    EffortLevel,
    SafetyRiskLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.models.household import Household


@dataclass
class RecommendationCandidate:
    engine_type: str
    title: str
    description: str
    what_detected: str
    why_it_matters: str
    monthly_saving_pounds: Decimal | None = None
    annual_saving_pounds: Decimal | None = None
    saving_label: SavingLabel = SavingLabel.ESTIMATED_SAVING
    effort: EffortLevel = EffortLevel.MEDIUM
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    safety_risk: SafetyRiskLevel = SafetyRiskLevel.NONE
    eligibility_caveat: str | None = None
    safety_caveat: str | None = None
    next_step: str = ""
    steps: list[str] = field(default_factory=list)
    call_script: str | None = None
    raw_score_inputs: dict | None = None


def _urgency_score(urgency: UrgencyLevel) -> float:
    return {UrgencyLevel.HIGH: 30, UrgencyLevel.MEDIUM: 15, UrgencyLevel.LOW: 5}.get(urgency, 5)


def _confidence_score(confidence: ConfidenceLevel) -> float:
    return {
        ConfidenceLevel.HIGH: 20,
        ConfidenceLevel.MEDIUM: 10,
        ConfidenceLevel.LOW: 3,
        ConfidenceLevel.NEEDS_REVIEW: 0,
        ConfidenceLevel.ONLY_IF_ELIGIBLE: 5,
        ConfidenceLevel.ONLY_IF_TARIFF_ELIGIBLE: 5,
    }.get(confidence, 5)


def _effort_penalty(effort: EffortLevel) -> float:
    return {EffortLevel.LOW: 0, EffortLevel.MEDIUM: 8, EffortLevel.HIGH: 18}.get(effort, 8)


def _safety_penalty(safety: SafetyRiskLevel) -> float:
    return {
        SafetyRiskLevel.NONE: 0,
        SafetyRiskLevel.LOW: 5,
        SafetyRiskLevel.MEDIUM: 25,
        SafetyRiskLevel.HIGH: 999,
    }.get(safety, 0)


def _saving_score(monthly_saving: Decimal | None) -> float:
    if monthly_saving is None:
        return 0
    return min(float(monthly_saving), 100)


def _vulnerability_boost(household: Household) -> int:
    boost = 0
    if household.has_children:
        boost += 2
    if household.has_pensioner:
        boost += 2
    if household.has_health_condition:
        boost += 3
    if household.has_disability:
        boost += 3
    if household.receives_qualifying_benefits:
        boost += 2
    return boost


def _is_unsafe_heating(candidate: RecommendationCandidate, household: Household) -> bool:
    if candidate.engine_type not in (
        "heating_optimisation",
        "appliance_time_shifting",
    ):
        return False

    if household.has_children:
        return True
    if household.has_pensioner:
        return True
    if household.has_health_condition:
        return True
    if household.has_disability:
        return True
    return False


def rank_recommendations(
    candidates: list[RecommendationCandidate],
    household: Household,
) -> list[RecommendationCandidate]:
    scored: list[tuple[float, RecommendationCandidate]] = []

    for c in candidates:
        if c.safety_risk == SafetyRiskLevel.HIGH:
            continue

        if _is_unsafe_heating(c, household):
            c.safety_risk = SafetyRiskLevel.MEDIUM
            c.safety_caveat = (
                "Keep regularly used rooms at a safe temperature, especially for older people, "
                "children, or anyone with health conditions."
            )

        saving = _saving_score(c.monthly_saving_pounds)
        urgency = _urgency_score(c.urgency)
        confidence = _confidence_score(c.confidence)
        effort_p = _effort_penalty(c.effort)
        safety_p = _safety_penalty(c.safety_risk)
        vuln_b = _vulnerability_boost(household)

        score = saving + urgency + confidence - effort_p - safety_p + vuln_b

        if c.saving_label == SavingLabel.GREEN_ONLY and saving < 10:
            score -= 20

        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    ranked: list[RecommendationCandidate] = []
    for rank_idx, (_, candidate) in enumerate(scored, start=1):
        ranked.append(candidate)

    return ranked


def select_top_actions(
    ranked: list[RecommendationCandidate],
    top_count: int = 3,
) -> tuple[list[RecommendationCandidate], list[RecommendationCandidate]]:
    top: list[RecommendationCandidate] = []
    other: list[RecommendationCandidate] = []

    for c in ranked:
        if len(top) < top_count and c.saving_label != SavingLabel.GREEN_ONLY:
            top.append(c)
        else:
            other.append(c)

    if len(top) < top_count:
        extra_needed = top_count - len(top)
        for c in ranked:
            if c not in top and extra_needed > 0:
                top.append(c)
                extra_needed -= 1

    return top, other
