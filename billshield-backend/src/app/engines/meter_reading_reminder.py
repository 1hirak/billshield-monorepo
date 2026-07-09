from __future__ import annotations

from datetime import date, timedelta

from app.core.constants import (
    CAP_CHANGE_WINDOW_AFTER_DAYS,
    CAP_CHANGE_WINDOW_BEFORE_DAYS,
    ENERGY_CAP_CHANGE_DATES,
    ConfidenceLevel,
    EffortLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.engines.ranking_engine import RecommendationCandidate


def check_meter_reading_needed(
    current_date: date | None = None,
) -> list[RecommendationCandidate]:
    today = current_date or date.today()

    for cap_date in ENERGY_CAP_CHANGE_DATES:
        start_window = cap_date - timedelta(days=CAP_CHANGE_WINDOW_BEFORE_DAYS)
        end_window = cap_date + timedelta(days=CAP_CHANGE_WINDOW_AFTER_DAYS)

        if start_window <= today <= end_window:
            return [
                RecommendationCandidate(
                    engine_type="meter_reading_reminder",
                    title="Submit a meter reading around the price-cap change",
                    description="A quarterly energy price-cap change is approaching. Submit readings to avoid estimated billing at the wrong rate.",
                    what_detected=f"The energy price cap changes around {cap_date.strftime('%d %B %Y')}.",
                    why_it_matters="Submitting a meter reading before and after the price-cap change helps ensure you are billed correctly for your actual usage.",
                    monthly_saving_pounds=None,
                    annual_saving_pounds=None,
                    saving_label=SavingLabel.BILLING_ACCURACY,
                    effort=EffortLevel.LOW,
                    confidence=ConfidenceLevel.HIGH,
                    urgency=UrgencyLevel.MEDIUM,
                    next_step="Submit your gas and electricity meter readings to your supplier.",
                    steps=[
                        "Take a photo or note both gas and electricity meter readings.",
                        "Submit them via your supplier's app, website, or phone line.",
                        "Keep a copy for your records.",
                    ],
                ),
            ]

    return []
