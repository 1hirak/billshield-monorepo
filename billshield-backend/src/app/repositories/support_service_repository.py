from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.constants import SupportServiceType
from app.models.support_service import SupportService


class SupportServiceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_area(
        self,
        postcode_area: str,
        service_types: list[SupportServiceType] | None = None,
        max_distance: float | None = None,
    ) -> list[SupportService]:
        query = self.db.query(SupportService).filter(
            SupportService.postcode_area == postcode_area
        )
        if service_types:
            query = query.filter(SupportService.type.in_(service_types))
        if max_distance:
            query = query.filter(SupportService.distance_miles <= max_distance)
        return query.order_by(SupportService.distance_miles.asc()).all()

    def create_many(self, services: list[SupportService]) -> list[SupportService]:
        self.db.add_all(services)
        self.db.commit()
        for svc in services:
            self.db.refresh(svc)
        return services
