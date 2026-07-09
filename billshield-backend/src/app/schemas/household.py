from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_validator

from app.core.constants import HouseholdType, IncomeBand, PaymentMethod
from app.schemas.common import CamelModel

UK_POSTCODE_PATTERN = re.compile(
    r"^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$", re.IGNORECASE
)


class CreateHouseholdRequest(CamelModel):
    postcode: str
    household_type: HouseholdType = Field(alias="householdType")
    income_band: IncomeBand = Field(alias="incomeBand")
    energy_provider: str = Field(alias="energyProvider")
    payment_method: PaymentMethod = Field(alias="paymentMethod")
    monthly_rent_or_mortgage: Decimal = Field(ge=0, alias="monthlyRentOrMortgage")
    monthly_food_cost: Decimal = Field(ge=0, alias="monthlyFoodCost")
    monthly_transport_cost: Decimal = Field(ge=0, alias="monthlyTransportCost")
    monthly_council_tax: Decimal = Field(ge=0, alias="monthlyCouncilTax")
    monthly_broadband_mobile_cost: Decimal = Field(ge=0, alias="monthlyBroadbandMobileCost")
    monthly_water_cost: Decimal = Field(ge=0, alias="monthlyWaterCost")
    receives_qualifying_benefits: bool | None = Field(default=None, alias="receivesQualifyingBenefits")
    has_children: bool | None = None
    has_pensioner: bool | None = None
    has_health_condition: bool | None = None
    has_disability: bool | None = None
    is_single_adult: bool | None = None
    bedrooms: int | None = Field(default=None, ge=0)
    occupants: int | None = Field(default=None, ge=0)
    water_metered: bool | None = None

    @field_validator("postcode")
    @classmethod
    def validate_postcode(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Postcode is required.")
        cleaned = v.strip().upper().replace(" ", "")
        if not UK_POSTCODE_PATTERN.match(" ".join([cleaned[:-3], cleaned[-3:]])):
            raise ValueError("Please enter a valid UK postcode.")
        return v.strip()

    @field_validator("energy_provider")
    @classmethod
    def validate_energy_provider(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Energy provider cannot be empty.")
        return v.strip()


class UpdateHouseholdRequest(CamelModel):
    postcode: str | None = None
    household_type: HouseholdType | None = None
    income_band: IncomeBand | None = None
    energy_provider: str | None = None
    payment_method: PaymentMethod | None = None
    monthly_rent_or_mortgage: Decimal | None = Field(default=None, ge=0)
    monthly_food_cost: Decimal | None = Field(default=None, ge=0)
    monthly_transport_cost: Decimal | None = Field(default=None, ge=0)
    monthly_council_tax: Decimal | None = Field(default=None, ge=0)
    monthly_broadband_mobile_cost: Decimal | None = Field(default=None, ge=0)
    monthly_water_cost: Decimal | None = Field(default=None, ge=0)
    receives_qualifying_benefits: bool | None = None
    has_children: bool | None = None
    has_pensioner: bool | None = None
    has_health_condition: bool | None = None
    has_disability: bool | None = None
    is_single_adult: bool | None = None
    bedrooms: int | None = Field(default=None, ge=0)
    occupants: int | None = Field(default=None, ge=0)
    water_metered: bool | None = None


class HouseholdResponse(CamelModel):
    id: str
    postcode: str
    normalized_postcode: str = Field(alias="normalizedPostcode")
    household_type: HouseholdType = Field(alias="householdType")
    income_band: IncomeBand = Field(alias="incomeBand")
    energy_provider: str = Field(alias="energyProvider")
    payment_method: PaymentMethod = Field(alias="paymentMethod")
    monthly_rent_or_mortgage: Decimal = Field(alias="monthlyRentOrMortgage")
    monthly_food_cost: Decimal = Field(alias="monthlyFoodCost")
    monthly_transport_cost: Decimal = Field(alias="monthlyTransportCost")
    monthly_council_tax: Decimal = Field(alias="monthlyCouncilTax")
    monthly_broadband_mobile_cost: Decimal = Field(alias="monthlyBroadbandMobileCost")
    monthly_water_cost: Decimal = Field(alias="monthlyWaterCost")
    receives_qualifying_benefits: bool | None = Field(default=None, alias="receivesQualifyingBenefits")
    has_children: bool | None = None
    has_pensioner: bool | None = None
    has_health_condition: bool | None = None
    has_disability: bool | None = None
    is_single_adult: bool | None = None
    bedrooms: int | None = None
    occupants: int | None = None
    water_metered: bool | None = None
    created_at: datetime
