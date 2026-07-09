from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.core.constants import EffortLevel, SavingLabel
from app.schemas.common import CamelModel


class PlanItem(CamelModel):
    id: str
    title: str
    description: str
    estimated_saving_pounds: float | None = Field(default=None, alias="estimatedSavingPounds")
    saving_label: str | None = Field(default=None, alias="savingLabel")
    effort: str | None = None
    done: bool = False
    call_script: str | None = Field(default=None, alias="callScript")


class PlanSection(CamelModel):
    title: str
    items: list[PlanItem]


class PlanActions(CamelModel):
    download_available: bool = Field(default=True, alias="downloadAvailable")
    copy_available: bool = Field(default=True, alias="copyAvailable")
    regenerate_available: bool = Field(default=True, alias="regenerateAvailable")


class GeneratePlanRequest(CamelModel):
    household_id: str = Field(alias="householdId")
    include_completed_actions: bool = Field(default=False, alias="includeCompletedActions")
    tone: str = "supportive_practical"


class ThirtyDayPlanResponse(CamelModel):
    plan_id: str = Field(alias="planId")
    household_id: str = Field(alias="householdId")
    generated_at: datetime = Field(alias="generatedAt")
    title: str
    intro: str
    this_week: PlanSection = Field(alias="thisWeek")
    next_two_weeks: PlanSection = Field(alias="nextTwoWeeks")
    by_day_thirty: PlanSection = Field(alias="byDayThirty")
    actions: PlanActions
    reassurance: str
