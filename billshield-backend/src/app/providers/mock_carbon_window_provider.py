from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.providers.carbon_window_provider import CarbonWindow, CarbonWindowProvider


class MockCarbonWindowProvider(CarbonWindowProvider):
    def get_low_carbon_windows(self, postcode: str) -> list[CarbonWindow]:
        now = datetime.now(tz=timezone.utc)
        tonight_start = now.replace(hour=22, minute=0, second=0, microsecond=0)
        return [
            CarbonWindow(
                start=tonight_start,
                end=tonight_start + timedelta(hours=8),
                carbon_intensity="low",
                forecast_value=120,
            ),
        ]
