from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import (
    ALLOWED_UPLOAD_EXTENSIONS,
    ALLOWED_UPLOAD_MIME_TYPES,
    BillStatus,
    BillType,
)
from app.core.errors import (
    BillAlreadyDeletedError,
    BillNotFoundError,
    UnsupportedFileTypeError,
    UploadTooLargeError,
)
from app.core.security import generate_safe_filename, generate_uuid, sanitize_path
from app.models.bill import Bill
from app.providers.mock_ocr_provider import MockOcrProvider
from app.providers.ocr_provider import BillExtraction, OcrProvider
from app.repositories.bill_repository import BillRepository
from app.schemas.bill import ConfirmBillFieldsRequest


class BillService:
    def __init__(self, db: Session, ocr_provider: OcrProvider | None = None) -> None:
        self.repository = BillRepository(db)
        self.ocr_provider = ocr_provider or MockOcrProvider()

    def upload(
        self, household_id: str, file: UploadFile, bill_type: BillType = BillType.ENERGY
    ) -> dict[str, Any]:
        if not file.filename:
            raise UnsupportedFileTypeError("empty")

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_UPLOAD_EXTENSIONS:
            raise UnsupportedFileTypeError(ext)

        if file.content_type and file.content_type not in ALLOWED_UPLOAD_MIME_TYPES:
            raise UnsupportedFileTypeError(file.content_type or "unknown")

        safe_filename = generate_safe_filename(file.filename)
        upload_dir = Path(settings.UPLOAD_DIR).resolve()
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = sanitize_path(upload_dir, safe_filename)

        contents = file.file.read()
        file_size = len(contents)

        if file_size > settings.max_upload_bytes:
            raise UploadTooLargeError(file_size, settings.max_upload_bytes)

        if file_size == 0:
            raise UnsupportedFileTypeError("empty")

        with open(file_path, "wb") as f:
            f.write(contents)

        bill = Bill(
            id=generate_uuid(),
            household_id=household_id,
            original_filename=safe_filename,
            content_type=file.content_type or "application/octet-stream",
            file_size_bytes=file_size,
            storage_path=str(file_path),
            status=BillStatus.EXTRACTING,
            bill_type=bill_type,
        )
        self.repository.create(bill)

        extraction = self.ocr_provider.extract_energy_bill(str(file_path))
        extraction_json = self._extraction_to_dict(extraction)
        self.repository.update(
            bill,
            extraction_json=extraction_json,
            extraction_confidence=extraction.overall_confidence,
            status=BillStatus.EXTRACTED,
        )

        return {
            "billId": str(bill.id),
            "householdId": household_id,
            "status": BillStatus.EXTRACTED.value,
            "message": "Bill uploaded and mock extraction completed.",
            "extractionSummary": {
                "supplier": extraction.supplier,
                "tariffName": extraction.tariff_name,
                "monthlyDirectDebit": float(extraction.monthly_direct_debit or 0),
                "overallConfidence": extraction.overall_confidence,
                "needsReviewFields": extraction.needs_review_fields,
            },
        }

    def get_extraction(self, bill_id: str) -> dict[str, Any]:
        bill = self._get_active_bill(bill_id)

        extraction = {}
        if bill.extraction_json:
            fields = bill.extraction_json
            extraction = {
                "supplier": {"value": fields.get("supplier", {}).get("value"), "confidence": fields.get("supplier", {}).get("confidence")},
                "tariffName": {"value": fields.get("tariffName", {}).get("value"), "confidence": fields.get("tariffName", {}).get("confidence")},
                "monthlyDirectDebit": {"value": fields.get("monthlyDirectDebit", {}).get("value"), "confidence": fields.get("monthlyDirectDebit", {}).get("confidence")},
                "electricityUnitRatePencePerKwh": {"value": fields.get("electricityUnitRatePencePerKwh", {}).get("value"), "confidence": fields.get("electricityUnitRatePencePerKwh", {}).get("confidence")},
                "electricityStandingChargePencePerDay": {"value": fields.get("electricityStandingChargePencePerDay", {}).get("value"), "confidence": fields.get("electricityStandingChargePencePerDay", {}).get("confidence")},
                "gasUnitRatePencePerKwh": {"value": fields.get("gasUnitRatePencePerKwh", {}).get("value"), "confidence": fields.get("gasUnitRatePencePerKwh", {}).get("confidence")},
                "gasStandingChargePencePerDay": {"value": fields.get("gasStandingChargePencePerDay", {}).get("value"), "confidence": fields.get("gasStandingChargePencePerDay", {}).get("confidence")},
                "annualElectricityUsageKwh": {"value": fields.get("annualElectricityUsageKwh", {}).get("value"), "confidence": fields.get("annualElectricityUsageKwh", {}).get("confidence")},
                "annualGasUsageKwh": {"value": fields.get("annualGasUsageKwh", {}).get("value"), "confidence": fields.get("annualGasUsageKwh", {}).get("confidence")},
                "billPeriodStart": {"value": fields.get("billPeriodStart", {}).get("value"), "confidence": fields.get("billPeriodStart", {}).get("confidence")},
                "billPeriodEnd": {"value": fields.get("billPeriodEnd", {}).get("value"), "confidence": fields.get("billPeriodEnd", {}).get("confidence")},
                "paymentMethod": {"value": fields.get("paymentMethod", {}).get("value"), "confidence": fields.get("paymentMethod", {}).get("confidence")},
                "tariffType": {"value": fields.get("tariffType", {}).get("value"), "confidence": fields.get("tariffType", {}).get("confidence")},
                "contractEndDate": {"value": fields.get("contractEndDate", {}).get("value"), "confidence": fields.get("contractEndDate", {}).get("confidence")},
            }

        return {
            "billId": str(bill.id),
            "householdId": str(bill.household_id),
            "status": bill.status.value if hasattr(bill.status, "value") else str(bill.status),
            "billType": bill.bill_type.value if hasattr(bill.bill_type, "value") else str(bill.bill_type),
            "originalFilename": bill.original_filename,
            "uploadedAt": bill.created_at.isoformat() if bill.created_at else None,
            "extraction": extraction,
            "reviewWarning": "Please check these details before we calculate savings.",
        }

    def confirm_fields(self, bill_id: str, data: ConfirmBillFieldsRequest) -> dict[str, Any]:
        bill = self._get_active_bill(bill_id)

        confirmed = data.model_dump(by_alias=False, exclude_unset=True)
        self.repository.update(
            bill,
            confirmed_fields_json=confirmed,
            status=BillStatus.CONFIRMED,
        )

        return {
            "billId": str(bill.id),
            "householdId": str(bill.household_id),
            "status": BillStatus.CONFIRMED.value,
            "confirmedFields": confirmed,
            "message": "Bill details confirmed. Dashboard calculations are ready.",
        }

    def delete_data(self, bill_id: str) -> dict[str, Any]:
        bill = self._get_active_bill(bill_id)

        if bill.storage_path:
            try:
                os.remove(bill.storage_path)
            except FileNotFoundError:
                pass

        self.repository.update(bill, extraction_json=None)
        self.repository.soft_delete(bill)

        return {
            "billId": str(bill.id),
            "status": BillStatus.DELETED.value,
            "message": "Bill data has been deleted.",
        }

    def _get_active_bill(self, bill_id: str) -> Bill:
        bill = self.repository.get_by_id(bill_id)
        if not bill:
            raise BillNotFoundError(bill_id)
        if bill.deleted_at:
            raise BillAlreadyDeletedError(bill_id)
        return bill

    @staticmethod
    def _extraction_to_dict(extraction: BillExtraction) -> dict[str, Any]:
        return {
            "supplier": {"value": extraction.supplier, "confidence": "high"},
            "tariffName": {"value": extraction.tariff_name, "confidence": "medium"},
            "monthlyDirectDebit": {"value": float(extraction.monthly_direct_debit or 0), "confidence": "high"},
            "electricityUnitRatePencePerKwh": {"value": float(extraction.electricity_unit_rate_pence_per_kwh or 0), "confidence": "high"},
            "electricityStandingChargePencePerDay": {"value": float(extraction.electricity_standing_charge_pence_per_day or 0), "confidence": "medium"},
            "gasUnitRatePencePerKwh": {"value": float(extraction.gas_unit_rate_pence_per_kwh or 0), "confidence": "high"},
            "gasStandingChargePencePerDay": {"value": float(extraction.gas_standing_charge_pence_per_day or 0), "confidence": "needs_review"},
            "annualElectricityUsageKwh": {"value": extraction.annual_electricity_usage_kwh or 0, "confidence": "high"},
            "annualGasUsageKwh": {"value": extraction.annual_gas_usage_kwh or 0, "confidence": "medium"},
            "billPeriodStart": {"value": "2026-04-01", "confidence": "high"},
            "billPeriodEnd": {"value": "2026-06-30", "confidence": "high"},
            "paymentMethod": {"value": extraction.payment_method, "confidence": "high"},
            "tariffType": {"value": extraction.tariff_type, "confidence": "medium"},
            "contractEndDate": {"value": None, "confidence": "needs_review"},
        }
