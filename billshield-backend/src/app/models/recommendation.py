from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import JSON, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    ConfidenceLevel,
    EffortLevel,
    RecommendationEngineType,
    RecommendationStatus,
    SafetyRiskLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.db.base import Base, TimestampMixin, UUIDMixin


class Recommendation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "recommendations"

    household_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True
    )
    bill_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("bills.id", ondelete="SET NULL"), nullable=True
    )
    engine_type: Mapped[RecommendationEngineType] = mapped_column(
        Enum(RecommendationEngineType, name="rec_engine_type_enum"), nullable=False
    )
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    what_detected: Mapped[str] = mapped_column(Text, nullable=False)
    why_it_matters: Mapped[str] = mapped_column(Text, nullable=False)
    monthly_saving_pounds: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    annual_saving_pounds: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    saving_label: Mapped[SavingLabel] = mapped_column(
        Enum(SavingLabel, name="saving_label_enum"), nullable=False
    )
    effort: Mapped[EffortLevel] = mapped_column(
        Enum(EffortLevel, name="effort_level_enum"), nullable=False
    )
    confidence: Mapped[ConfidenceLevel] = mapped_column(
        Enum(ConfidenceLevel, name="confidence_level_enum"), nullable=False
    )
    urgency: Mapped[UrgencyLevel] = mapped_column(
        Enum(UrgencyLevel, name="urgency_level_enum"), nullable=False
    )
    safety_risk: Mapped[SafetyRiskLevel] = mapped_column(
        Enum(SafetyRiskLevel, name="safety_risk_enum"), nullable=False, default=SafetyRiskLevel.NONE
    )
    eligibility_caveat: Mapped[str | None] = mapped_column(Text, nullable=True)
    safety_caveat: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_step: Mapped[str] = mapped_column(Text, nullable=False)
    steps_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    call_script: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(RecommendationStatus, name="rec_status_enum"),
        nullable=False,
        default=RecommendationStatus.ACTIVE,
    )

    household: Mapped["Household"] = relationship("Household", back_populates="recommendations")  # noqa: F821
    bill: Mapped["Bill | None"] = relationship("Bill", back_populates="recommendations")  # noqa: F821
