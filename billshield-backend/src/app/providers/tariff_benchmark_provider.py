from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from app.core.constants import PaymentMethod


@dataclass
class TariffBenchmark:
    period: str
    payment_method: PaymentMethod
    electricity_unit_rate_pence_per_kwh: Decimal
    gas_unit_rate_pence_per_kwh: Decimal
    electricity_standing_charge_pence_per_day: Decimal
    gas_standing_charge_pence_per_day: Decimal
    typical_annual_dual_fuel_pounds: int
    disclaimer: str


class TariffBenchmarkProvider(Protocol):
    def get_benchmark(
        self, postcode: str, payment_method: PaymentMethod
    ) -> TariffBenchmark: ...
