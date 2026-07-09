from __future__ import annotations

from decimal import Decimal

TARIFF_BENCHMARKS: dict[str, dict] = {
    "default_direct_debit": {
        "period": "2026-Q3",
        "paymentMethod": "direct_debit",
        "electricityUnitRatePencePerKwh": 26.11,
        "gasUnitRatePencePerKwh": 7.33,
        "electricityStandingChargePencePerDay": 57.19,
        "gasStandingChargePencePerDay": 29.04,
        "typicalAnnualDualFuelPounds": 1862,
        "disclaimer": "Mock benchmark for MVP. Actual rates vary by region, meter type, and payment method.",
    },
    "default_prepayment": {
        "period": "2026-Q3",
        "paymentMethod": "prepayment_meter",
        "electricityUnitRatePencePerKwh": 26.65,
        "gasUnitRatePencePerKwh": 7.28,
        "electricityStandingChargePencePerDay": 57.30,
        "gasStandingChargePencePerDay": 29.11,
        "typicalAnnualDualFuelPounds": 1887,
        "disclaimer": "Mock benchmark for MVP. Actual rates vary by region, meter type, and payment method.",
    },
    "default_standard_credit": {
        "period": "2026-Q3",
        "paymentMethod": "standard_credit",
        "electricityUnitRatePencePerKwh": 27.90,
        "gasUnitRatePencePerKwh": 7.84,
        "electricityStandingChargePencePerDay": 61.39,
        "gasStandingChargePencePerDay": 31.22,
        "typicalAnnualDualFuelPounds": 1990,
        "disclaimer": "Mock benchmark for MVP. Actual rates vary by region, meter type, and payment method.",
    },
}
