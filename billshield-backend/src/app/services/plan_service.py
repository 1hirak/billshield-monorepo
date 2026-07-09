from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.core.errors import HouseholdNotFoundError
from app.core.security import generate_uuid
from app.models.plan import ThirtyDayPlan
from app.providers.mock_plan_generator_provider import MockPlanGeneratorProvider
from app.providers.plan_generator_provider import PlanGeneratorProvider
from app.repositories.household_repository import HouseholdRepository
from app.repositories.plan_repository import PlanRepository
from app.repositories.recommendation_repository import RecommendationRepository


class PlanService:
    def __init__(self, db: Session, plan_provider: PlanGeneratorProvider | None = None) -> None:
        self.db = db
        self.household_repo = HouseholdRepository(db)
        self.plan_repo = PlanRepository(db)
        self.rec_repo = RecommendationRepository(db)
        self.plan_provider = plan_provider or MockPlanGeneratorProvider()

    def generate_plan(self, household_id: str, tone: str = "supportive_practical") -> dict[str, Any]:
        household = self.household_repo.get_by_id(household_id)
        if not household:
            raise HouseholdNotFoundError(household_id)

        recommendations = self.rec_repo.get_by_household(household_id)

        generated = self.plan_provider.generate_plan(household, recommendations)

        plan = ThirtyDayPlan(
            id=generate_uuid(),
            household_id=household_id,
            generated_from_recommendation_ids={"recommendationIds": [str(r.id) for r in recommendations]},
            this_week_json=generated.this_week,
            next_two_weeks_json=generated.next_two_weeks,
            by_day_thirty_json=generated.by_day_thirty,
            tone=tone,
        )
        self.plan_repo.create(plan)

        return {
            "planId": str(plan.id),
            "householdId": household_id,
            "generatedAt": plan.created_at.isoformat() if plan.created_at else "",
            "title": generated.title,
            "intro": generated.intro,
            "thisWeek": generated.this_week,
            "nextTwoWeeks": generated.next_two_weeks,
            "byDayThirty": generated.by_day_thirty,
            "actions": {
                "downloadAvailable": True,
                "copyAvailable": True,
                "regenerateAvailable": True,
            },
            "reassurance": generated.reassurance,
        }

    def get_latest_plan(self, household_id: str) -> dict[str, Any] | None:
        plan = self.plan_repo.get_latest(household_id)
        if not plan:
            return None

        return {
            "planId": str(plan.id),
            "householdId": str(plan.household_id),
            "generatedAt": plan.created_at.isoformat() if plan.created_at else "",
            "title": "Your 30-day bill survival plan",
            "thisWeek": plan.this_week_json,
            "nextTwoWeeks": plan.next_two_weeks_json,
            "byDayThirty": plan.by_day_thirty_json,
            "actions": {
                "downloadAvailable": True,
                "copyAvailable": True,
                "regenerateAvailable": True,
            },
            "reassurance": "You do not have to do everything at once. Start with the first low-effort action and return when you are ready.",
        }
