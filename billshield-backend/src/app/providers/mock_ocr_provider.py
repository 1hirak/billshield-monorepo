from __future__ import annotations

import random

from app.providers.ocr_provider import BillExtraction, OcrProvider


class MockOcrProvider(OcrProvider):
    def extract_energy_bill(self, file_path: str) -> BillExtraction:
        return BillExtraction(
            supplier="BrightSpark Energy",
            tariff_name="Standard Variable Direct",
            monthly_direct_debit=random.choice([139, 142, 145, 152]),
            electricity_unit_rate_pence_per_kwh=27.34,
            electricity_standing_charge_pence_per_day=60.12,
            gas_unit_rate_pence_per_kwh=7.62,
            gas_standing_charge_pence_per_day=31.44,
            annual_electricity_usage_kwh=2900,
            annual_gas_usage_kwh=11000,
            overall_confidence="medium",
            needs_review_fields=["gasStandingChargePencePerDay", "tariffName"],
        )
