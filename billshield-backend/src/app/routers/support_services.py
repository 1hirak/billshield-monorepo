from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.support_service import SupportServiceService

router = APIRouter(prefix="/support-services", tags=["support-services"])


@router.get("")
def get_support_services(
    postcode: str = Query(..., description="UK postcode to search near"),
    filters: str | None = Query(default=None, description="Comma-separated service types"),
    radius_miles: float = Query(default=5, ge=0.1, le=20, alias="radiusMiles"),
    db: Session = Depends(get_db),
):
    filter_list = [f.strip() for f in filters.split(",")] if filters else None
    service = SupportServiceService(db)
    return service.get_services(postcode, filter_list, radius_miles)
