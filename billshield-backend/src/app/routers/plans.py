from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.plan import GeneratePlanRequest, ThirtyDayPlanResponse
from app.services.plan_service import PlanService

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/30-day", response_model=ThirtyDayPlanResponse)
def generate_plan(data: GeneratePlanRequest, db: Session = Depends(get_db)):
    service = PlanService(db)
    return service.generate_plan(data.household_id, data.tone)  # type: ignore[return-value]
