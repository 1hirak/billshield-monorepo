from __future__ import annotations

from pydantic import Field

from app.core.constants import ConfidenceLevel, EffortLevel, SavingLabel, UrgencyLevel
from app.schemas.common import CamelModel


class RecommendationResponse(CamelModel):
    id: str
    household_id: str = Field(alias="householdId")
    engine_type: str = Field(alias="engineType")
    rank: int
    title: str
    description: str
    what_detected: str = Field(alias="whatDetected")
    why_it_matters: str = Field(alias="whyItMatters")
    monthly_saving_pounds: float | None = Field(alias="monthlySavingPounds")
    annual_saving_pounds: float | None = Field(alias="annualSavingPounds")
    saving_label: str = Field(alias="savingLabel")
    effort: str
    confidence: str
    urgency: str
    safety_risk: str = Field(alias="safetyRisk")
    eligibility_caveat: str | None = None
    safety_caveat: str | None = None
    next_step: str = Field(alias="nextStep")
    steps: list[str] | None = None
    call_script: str | None = None
    status: str


class RecommendationListResponse(CamelModel):
    household_id: str = Field(alias="householdId")
    recommendations: list[RecommendationResponse]
    top_count: int = Field(alias="topCount")
    total_count: int = Field(alias="totalCount")
