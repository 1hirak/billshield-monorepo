from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from app.core.constants import OpeningStatus, SupportServiceType
from app.schemas.common import CamelModel


class SupportServiceResponse(CamelModel):
    id: str
    name: str
    type: str
    distance_miles: float = Field(alias="distanceMiles")
    opening_status: str = Field(alias="openingStatus")
    short_description: str = Field(alias="shortDescription")
    address_line1: str
    town: str
    phone: str | None = None
    website: str | None = None
    directions_label: str | None = Field(default="Get directions", alias="directionsLabel")


class MapPlaceholder(CamelModel):
    center_label: str = Field(alias="centerLabel")
    message: str


class SupportServicesResponse(CamelModel):
    postcode: str
    normalized_postcode: str = Field(alias="normalizedPostcode")
    radius_miles: float = Field(alias="radiusMiles")
    map_placeholder: MapPlaceholder = Field(alias="mapPlaceholder")
    services: list[SupportServiceResponse]
    available_filters: list[str] = Field(alias="availableFilters")
