from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.plan import ThirtyDayPlan


class PlanRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, plan: ThirtyDayPlan) -> ThirtyDayPlan:
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def get_by_household(self, household_id: str) -> list[ThirtyDayPlan]:
        return (
            self.db.query(ThirtyDayPlan)
            .filter(ThirtyDayPlan.household_id == household_id)
            .order_by(ThirtyDayPlan.created_at.desc())
            .all()
        )

    def get_latest(self, household_id: str) -> ThirtyDayPlan | None:
        return (
            self.db.query(ThirtyDayPlan)
            .filter(ThirtyDayPlan.household_id == household_id)
            .order_by(ThirtyDayPlan.created_at.desc())
            .first()
        )
