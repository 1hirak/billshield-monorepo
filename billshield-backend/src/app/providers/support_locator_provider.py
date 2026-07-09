from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from app.core.constants import OpeningStatus, SupportServiceType


@dataclass
class SupportServiceInfo:
    id: str
    name: str
    type: SupportServiceType
    postcode_area: str
    distance_miles: Decimal
    opening_status: OpeningStatus
    short_description: str
    address_line1: str | None = None
    town: str | None = None
    phone: str | None = None
    website: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class SupportLocatorProvider(Protocol):
    def find_services(
        self,
        postcode: str,
        filters: list[SupportServiceType],
        radius_miles: float,
    ) -> list[SupportServiceInfo]: ...
