from __future__ import annotations

from decimal import Decimal

from app.core.constants import PaymentMethod
from app.providers.tariff_benchmark_provider import TariffBenchmark, TariffBenchmarkProvider


class MockTariffBenchmarkProvider(TariffBenchmarkProvider):
    def get_benchmark(
        self, postcode: str, payment_method: PaymentMethod
    ) -> TariffBenchmark:
        return TariffBenchmark(
            period="2026-Q3",
            payment_method=payment_method,
            electricity_unit_rate_pence_per_kwh=Decimal("26.11"),
            gas_unit_rate_pence_per_kwh=Decimal("7.33"),
            electricity_standing_charge_pence_per_day=Decimal("57.19"),
            gas_standing_charge_pence_per_day=Decimal("29.04"),
            typical_annual_dual_fuel_pounds=1862,
            disclaimer="Mock benchmark for MVP. Actual rates vary by region, meter type, and payment method.",
        )
