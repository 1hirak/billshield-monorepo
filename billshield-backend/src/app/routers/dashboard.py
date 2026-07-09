from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/{household_id}")
def get_dashboard(household_id: str, db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.get_dashboard(household_id)
