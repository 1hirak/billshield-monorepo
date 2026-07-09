from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, Protocol


@dataclass
class BillExtraction:
    supplier: str = ""
    tariff_name: str = ""
    monthly_direct_debit: Decimal | None = None
    electricity_unit_rate_pence_per_kwh: Decimal | None = None
    electricity_standing_charge_pence_per_day: Decimal | None = None
    gas_unit_rate_pence_per_kwh: Decimal | None = None
    gas_standing_charge_pence_per_day: Decimal | None = None
    annual_electricity_usage_kwh: int | None = None
    annual_gas_usage_kwh: int | None = None
    bill_period_start: date | None = None
    bill_period_end: date | None = None
    payment_method: str = "direct_debit"
    tariff_type: str = "standard_variable"
    contract_end_date: date | None = None
    overall_confidence: str = "medium"
    needs_review_fields: list[str] = field(default_factory=list)


class OcrProvider(Protocol):
    def extract_energy_bill(self, file_path: str) -> BillExtraction: ...
