from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.core.constants import SupportServiceType
from app.providers.mock_support_locator_provider import MockSupportLocatorProvider
from app.providers.support_locator_provider import SupportLocatorProvider


class SupportServiceService:
    def __init__(
        self,
        db: Session,
        support_provider: SupportLocatorProvider | None = None,
    ) -> None:
        self.db = db
        self.support_provider = support_provider or MockSupportLocatorProvider()

    def get_services(
        self,
        postcode: str,
        filters: list[str] | None = None,
        radius_miles: float = 5,
    ) -> dict[str, Any]:
        area = postcode[:2].upper().replace(" ", "")

        service_types: list[SupportServiceType] = []
        if filters:
            for f in filters:
                try:
                    service_types.append(SupportServiceType(f))
                except ValueError:
                    pass

        services = self.support_provider.find_services(postcode, service_types, radius_miles)

        return {
            "postcode": postcode,
            "normalizedPostcode": area,
            "radiusMiles": radius_miles,
            "mapPlaceholder": {
                "centerLabel": f"{area} area",
                "message": "Map data is mocked for the MVP. Real map and directions integrations can be connected later.",
            },
            "services": [
                {
                    "id": s.id,
                    "name": s.name,
                    "type": s.type.value,
                    "distanceMiles": float(s.distance_miles),
                    "openingStatus": s.opening_status.value,
                    "shortDescription": s.short_description,
                    "addressLine1": s.address_line1,
                    "town": s.town,
                    "phone": s.phone,
                    "website": s.website,
                    "directionsLabel": "Get directions",
                }
                for s in services
            ],
            "availableFilters": [t.value for t in SupportServiceType],
        }
