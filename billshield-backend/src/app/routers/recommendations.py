from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/{household_id}")
def get_recommendations(household_id: str, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.get_for_household(household_id)
