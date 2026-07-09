from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    HouseholdType,
    IncomeBand,
    PaymentMethod,
)
from app.db.base import Base, TimestampMixin, UUIDMixin


class Household(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "households"

    postcode: Mapped[str] = mapped_column(String(20), nullable=False)
    normalized_postcode: Mapped[str] = mapped_column(String(20), nullable=False)
    household_type: Mapped[HouseholdType] = mapped_column(
        Enum(HouseholdType, name="household_type_enum"), nullable=False
    )
    income_band: Mapped[IncomeBand] = mapped_column(
        Enum(IncomeBand, name="income_band_enum"), nullable=False
    )
    energy_provider: Mapped[str] = mapped_column(String(200), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method_enum"), nullable=False
    )
    monthly_rent_or_mortgage: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    monthly_food_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    monthly_transport_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    monthly_council_tax: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    monthly_broadband_mobile_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    monthly_water_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    receives_qualifying_benefits: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_children: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_pensioner: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_health_condition: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_disability: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_single_adult: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    occupants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    water_metered: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    bills: Mapped[list["Bill"]] = relationship("Bill", back_populates="household", lazy="selectin")
    recommendations: Mapped[list["Recommendation"]] = relationship(
        "Recommendation", back_populates="household", lazy="selectin"
    )
    plans: Mapped[list["ThirtyDayPlan"]] = relationship(
        "ThirtyDayPlan", back_populates="household", lazy="selectin"
    )
