from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.constants import (
    BillStatus,
    BillType,
    HouseholdType,
    IncomeBand,
    PaymentMethod,
)
from app.db.init_db import init_db
from app.models.bill import Bill
from app.models.household import Household
from app.core.security import generate_uuid

MOCK_HOUSEHOLD_DATA = {
    "postcode": "BS1 4ST",
    "normalized_postcode": "BS14ST",
    "household_type": HouseholdType.FAMILY_WITH_CHILDREN,
    "income_band": IncomeBand.FIFTEEN_TO_25K,
    "energy_provider": "BrightSpark Energy",
    "payment_method": PaymentMethod.DIRECT_DEBIT,
    "monthly_rent_or_mortgage": Decimal("850"),
    "monthly_food_cost": Decimal("360"),
    "monthly_transport_cost": Decimal("155"),
    "monthly_council_tax": Decimal("168"),
    "monthly_broadband_mobile_cost": Decimal("52"),
    "monthly_water_cost": Decimal("39"),
    "receives_qualifying_benefits": True,
    "has_children": True,
    "has_pensioner": False,
    "has_health_condition": False,
    "has_disability": False,
    "is_single_adult": False,
    "bedrooms": 3,
    "occupants": 4,
    "water_metered": False,
}

MOCK_EXTRACTION_JSON = {
    "supplier": {"value": "BrightSpark Energy", "confidence": "high"},
    "tariffName": {"value": "Standard Variable Direct", "confidence": "medium"},
    "monthlyDirectDebit": {"value": 142, "confidence": "high"},
    "electricityUnitRatePencePerKwh": {"value": 27.34, "confidence": "high"},
    "electricityStandingChargePencePerDay": {"value": 60.12, "confidence": "medium"},
    "gasUnitRatePencePerKwh": {"value": 7.62, "confidence": "high"},
    "gasStandingChargePencePerDay": {"value": 31.44, "confidence": "needs_review"},
    "annualElectricityUsageKwh": {"value": 2900, "confidence": "high"},
    "annualGasUsageKwh": {"value": 11000, "confidence": "medium"},
    "billPeriodStart": {"value": "2026-04-01", "confidence": "high"},
    "billPeriodEnd": {"value": "2026-06-30", "confidence": "high"},
    "paymentMethod": {"value": "direct_debit", "confidence": "high"},
    "tariffType": {"value": "standard_variable", "confidence": "medium"},
    "contractEndDate": {"value": None, "confidence": "needs_review"},
}


def seed_demo_data(db: Session) -> dict[str, str]:
    existing = db.query(Household).first()
    if existing:
        return {"householdId": str(existing.id), "message": "Data already seeded."}

    household = Household(**MOCK_HOUSEHOLD_DATA)
    household.id = generate_uuid()
    db.add(household)
    db.flush()

    bill = Bill(
        household_id=household.id,
        original_filename="energy-bill-demo.pdf",
        content_type="application/pdf",
        file_size_bytes=1024 * 100,
        storage_path=None,
        status=BillStatus.EXTRACTED,
        bill_type=BillType.ENERGY,
        extraction_json=MOCK_EXTRACTION_JSON,
        extraction_confidence="medium",
    )
    db.add(bill)
    db.commit()

    return {
        "householdId": str(household.id),
        "billId": str(bill.id),
        "message": "Demo data seeded successfully.",
    }


def reset_demo_data(db: Session) -> dict[str, str]:
    db.query(Bill).delete()
    db.query(Household).delete()
    db.commit()
    return {"message": "All demo data has been reset."}
