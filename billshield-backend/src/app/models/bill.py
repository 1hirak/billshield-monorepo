from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import BillStatus, BillType
from app.db.base import Base, TimestampMixin, UUIDMixin


class Bill(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "bills"

    household_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[BillStatus] = mapped_column(
        Enum(BillStatus, name="bill_status_enum"), nullable=False, default=BillStatus.UPLOADED
    )
    bill_type: Mapped[BillType] = mapped_column(
        Enum(BillType, name="bill_type_enum"), nullable=False
    )
    extraction_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    confirmed_fields_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    extraction_confidence: Mapped[str | None] = mapped_column(String(20), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    household: Mapped["Household"] = relationship("Household", back_populates="bills")  # noqa: F821
    recommendations: Mapped[list["Recommendation"]] = relationship(  # noqa: F821
        "Recommendation", back_populates="bill", lazy="selectin"
    )
