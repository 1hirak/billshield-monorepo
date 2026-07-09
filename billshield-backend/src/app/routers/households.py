from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.household import CreateHouseholdRequest, HouseholdResponse, UpdateHouseholdRequest
from app.services.household_service import HouseholdService

router = APIRouter(prefix="/households", tags=["households"])


@router.post("", response_model=HouseholdResponse, status_code=201)
def create_household(data: CreateHouseholdRequest, db: Session = Depends(get_db)):
    service = HouseholdService(db)
    return service.create(data)  # type: ignore[return-value]


@router.get("/{household_id}", response_model=HouseholdResponse)
def get_household(household_id: str, db: Session = Depends(get_db)):
    service = HouseholdService(db)
    return service.get(household_id)  # type: ignore[return-value]


@router.patch("/{household_id}", response_model=HouseholdResponse)
def update_household(household_id: str, data: UpdateHouseholdRequest, db: Session = Depends(get_db)):
    service = HouseholdService(db)
    return service.update(household_id, data)  # type: ignore[return-value]
