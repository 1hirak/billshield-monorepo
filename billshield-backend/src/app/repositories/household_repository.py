from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.household import Household


class HouseholdRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, household: Household) -> Household:
        self.db.add(household)
        self.db.commit()
        self.db.refresh(household)
        return household

    def get_by_id(self, household_id: str) -> Household | None:
        return self.db.query(Household).filter(Household.id == household_id).first()

    def update(self, household: Household, **kwargs) -> Household:
        for key, value in kwargs.items():
            if value is not None and hasattr(household, key):
                setattr(household, key, value)
        self.db.commit()
        self.db.refresh(household)
        return household
