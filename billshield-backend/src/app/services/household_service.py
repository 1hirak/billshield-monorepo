from __future__ import annotations

import re

from sqlalchemy.orm import Session

from app.core.constants import HouseholdType
from app.core.errors import HouseholdNotFoundError
from app.core.security import generate_uuid
from app.models.household import Household
from app.repositories.household_repository import HouseholdRepository
from app.schemas.household import CreateHouseholdRequest, UpdateHouseholdRequest


class HouseholdService:
    def __init__(self, db: Session) -> None:
        self.repository = HouseholdRepository(db)

    def create(self, data: CreateHouseholdRequest) -> Household:
        normalized = self._normalize_postcode(data.postcode)
        household = Household(
            id=generate_uuid(),
            **data.model_dump(by_alias=False),
            normalized_postcode=normalized,
        )
        if data.household_type == HouseholdType.PENSIONER_HOUSEHOLD and data.has_pensioner is None:
            household.has_pensioner = True
        if data.household_type == HouseholdType.SINGLE_ADULT and data.is_single_adult is None:
            household.is_single_adult = True
        return self.repository.create(household)

    def get(self, household_id: str) -> Household:
        household = self.repository.get_by_id(household_id)
        if not household:
            raise HouseholdNotFoundError(household_id)
        return household

    def update(self, household_id: str, data: UpdateHouseholdRequest) -> Household:
        household = self.get(household_id)
        update_data = {k: v for k, v in data.model_dump(by_alias=False).items() if v is not None}
        if "postcode" in update_data:
            update_data["normalized_postcode"] = self._normalize_postcode(update_data["postcode"])
        return self.repository.update(household, **update_data)

    @staticmethod
    def _normalize_postcode(postcode: str) -> str:
        return re.sub(r"\s+", "", postcode).upper()
