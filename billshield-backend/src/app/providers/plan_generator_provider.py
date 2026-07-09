from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from app.models.household import Household
from app.models.recommendation import Recommendation


@dataclass
class GeneratedPlan:
    title: str
    intro: str
    this_week: dict[str, Any]
    next_two_weeks: dict[str, Any]
    by_day_thirty: dict[str, Any]
    tone: str
    reassurance: str


class PlanGeneratorProvider(Protocol):
    def generate_plan(
        self,
        household: Household,
        recommendations: list[Recommendation],
    ) -> GeneratedPlan: ...
