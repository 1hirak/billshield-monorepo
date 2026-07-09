from __future__ import annotations

from decimal import Decimal

from app.core.constants import SavingLabel
from app.models.bill import Bill


def calculate_standing_charges(
    bill: Bill | None,
) -> dict:
    if not bill or not bill.confirmed_fields_json:
        return {
            "electricityUsageCostMonthly": 66,
            "gasUsageCostMonthly": 70,
            "standingChargesMonthly": 28,
            "monthlyDirectDebit": 142,
            "avoidableCostMonthly": 114,
            "unavoidableStandingChargeMonthly": 28,
            "insight": "Standing charges are fixed daily costs. Even if your usage falls, this part of the bill remains.",
        }

    fields = bill.confirmed_fields_json
    elec_sc = Decimal(str(fields.get("electricityStandingChargePencePerDay", 0)))
    gas_sc = Decimal(str(fields.get("gasStandingChargePencePerDay", 0)))

    monthly_standing = (elec_sc + gas_sc) * 365 / 100 / 12
    monthly_standing = round(float(monthly_standing))

    elec_unit = Decimal(str(fields.get("electricityUnitRatePencePerKwh", 0)))
    gas_unit = Decimal(str(fields.get("gasUnitRatePencePerKwh", 0)))
    elec_usage = int(fields.get("annualElectricityUsageKwh", 0))
    gas_usage = int(fields.get("annualGasUsageKwh", 0))

    elec_monthly = float(Decimal(elec_usage) * elec_unit / 100 / 12)
    gas_monthly = float(Decimal(gas_usage) * gas_unit / 100 / 12)

    monthly_dd = float(fields.get("monthlyDirectDebit", 142))

    avoidable = round(elec_monthly + gas_monthly)
    unavoidable = round(monthly_standing)

    return {
        "electricityUsageCostMonthly": round(elec_monthly),
        "gasUsageCostMonthly": round(gas_monthly),
        "standingChargesMonthly": unavoidable,
        "monthlyDirectDebit": monthly_dd,
        "estimatedAnnualCost": round((elec_monthly + gas_monthly + monthly_standing) * 12),
        "currentTariffStatus": fields.get("tariffType", "standard_variable"),
        "standingChargeInsight": "Standing charges are fixed daily costs. Even if your usage falls, this part of the bill remains.",
        "avoidableCostMonthly": avoidable,
        "unavoidableStandingChargeMonthly": unavoidable,
    }
