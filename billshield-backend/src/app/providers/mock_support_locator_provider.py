from __future__ import annotations

from copy import deepcopy
from decimal import Decimal

from app.core.constants import OpeningStatus, SupportServiceType
from app.core.security import generate_uuid
from app.data.support_services import MOCK_SUPPORT_SERVICES
from app.providers.support_locator_provider import SupportServiceInfo, SupportLocatorProvider


class MockSupportLocatorProvider(SupportLocatorProvider):
    def find_services(
        self,
        postcode: str,
        filters: list[SupportServiceType],
        radius_miles: float,
    ) -> list[SupportServiceInfo]:
        area = postcode[:2].upper().replace(" ", "")

        wildcard = [deepcopy(s) for s in MOCK_SUPPORT_SERVICES if s["postcode_area"] == "*"]
        area_specific = [deepcopy(s) for s in MOCK_SUPPORT_SERVICES if s["postcode_area"] == area]

        all_raw = area_specific + wildcard

        for s in all_raw:
            s["postcode_area"] = area
            if s["town"] is None:
                s["town"] = f"{area} area"

        results: list[SupportServiceInfo] = []
        for svc in all_raw:
            svc_type = svc["type"]
            if filters and SupportServiceType(svc_type) not in filters:
                continue
            if svc["distance_miles"] > radius_miles:
                continue

            results.append(
                SupportServiceInfo(
                    id=generate_uuid(),
                    name=svc["name"],
                    type=SupportServiceType(svc_type),
                    postcode_area=area,
                    distance_miles=Decimal(str(svc["distance_miles"])),
                    opening_status=OpeningStatus(svc["opening_status"]),
                    short_description=svc["short_description"],
                    address_line1=svc.get("address_line1"),
                    town=svc.get("town"),
                    phone=svc.get("phone"),
                    website=svc.get("website"),
                    latitude=Decimal(str(svc["latitude"])) if svc.get("latitude") else None,
                    longitude=Decimal(str(svc["longitude"])) if svc.get("longitude") else None,
                )
            )

        results.sort(key=lambda x: x.distance_miles)
        return results
