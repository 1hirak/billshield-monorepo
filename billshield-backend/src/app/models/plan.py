from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class ThirtyDayPlan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "thirty_day_plans"

    household_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True
    )
    generated_from_recommendation_ids: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True
    )
    this_week_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    next_two_weeks_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    by_day_thirty_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    tone: Mapped[str] = mapped_column(String(50), nullable=False)

    household: Mapped["Household"] = relationship("Household", back_populates="plans")  # noqa: F821
