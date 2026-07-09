from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Enum, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import OpeningStatus, SupportServiceType
from app.db.base import Base, TimestampMixin, UUIDMixin


class SupportService(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "support_services"

    name: Mapped[str] = mapped_column(String(300), nullable=False)
    type: Mapped[SupportServiceType] = mapped_column(
        Enum(SupportServiceType, name="support_service_type_enum"), nullable=False
    )
    postcode_area: Mapped[str] = mapped_column(String(10), nullable=False)
    distance_miles: Mapped[Decimal] = mapped_column(Numeric(5, 1), nullable=False)
    opening_status: Mapped[OpeningStatus] = mapped_column(
        Enum(OpeningStatus, name="opening_status_enum"), nullable=False
    )
    short_description: Mapped[str] = mapped_column(Text, nullable=False)
    address_line1: Mapped[str | None] = mapped_column(String(300), nullable=True)
    town: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
