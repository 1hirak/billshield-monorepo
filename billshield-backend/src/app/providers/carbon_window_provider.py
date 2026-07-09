from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class CarbonWindow:
    start: datetime
    end: datetime
    carbon_intensity: str  # low, moderate, high
    forecast_value: int


class CarbonWindowProvider(Protocol):
    def get_low_carbon_windows(self, postcode: str) -> list[CarbonWindow]: ...
