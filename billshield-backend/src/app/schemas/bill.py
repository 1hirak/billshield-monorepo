from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from app.core.constants import BillStatus, BillType
from app.schemas.common import CamelModel


class ExtractedField(CamelModel):
    value: Any | None = None
    confidence: str | None = None


class BillExtractionData(CamelModel):
    supplier: ExtractedField | None = None
    tariff_name: ExtractedField | None = None
    monthly_direct_debit: ExtractedField | None = None
    electricity_unit_rate_pence_per_kwh: ExtractedField | None = None
    electricity_standing_charge_pence_per_day: ExtractedField | None = None
    gas_unit_rate_pence_per_kwh: ExtractedField | None = None
    gas_standing_charge_pence_per_day: ExtractedField | None = None
    annual_electricity_usage_kwh: ExtractedField | None = None
    annual_gas_usage_kwh: ExtractedField | None = None
    bill_period_start: ExtractedField | None = None
    bill_period_end: ExtractedField | None = None
    payment_method: ExtractedField | None = None
    tariff_type: ExtractedField | None = None
    contract_end_date: ExtractedField | None = None


class ExtractionSummary(CamelModel):
    supplier: str
    tariff_name: str = Field(alias="tariffName")
    monthly_direct_debit: float = Field(alias="monthlyDirectDebit")
    overall_confidence: str = Field(alias="overallConfidence")
    needs_review_fields: list[str] = Field(default_factory=list, alias="needsReviewFields")


class BillUploadResponse(CamelModel):
    bill_id: str = Field(alias="billId")
    household_id: str = Field(alias="householdId")
    status: BillStatus
    message: str
    extraction_summary: ExtractionSummary | None = Field(default=None, alias="extractionSummary")


class ConfirmBillFieldsRequest(CamelModel):
    supplier: str | None = None
    tariff_name: str | None = None
    monthly_direct_debit: float | None = None
    electricity_unit_rate_pence_per_kwh: float | None = None
    electricity_standing_charge_pence_per_day: float | None = None
    gas_unit_rate_pence_per_kwh: float | None = None
    gas_standing_charge_pence_per_day: float | None = None
    annual_electricity_usage_kwh: float | None = None
    annual_gas_usage_kwh: float | None = None
    bill_period_start: str | None = None
    bill_period_end: str | None = None
    payment_method: str | None = None
    tariff_type: str | None = None
    contract_end_date: str | None = None


class BillExtractionResponse(CamelModel):
    bill_id: str = Field(alias="billId")
    household_id: str = Field(alias="householdId")
    status: BillStatus
    bill_type: BillType = Field(alias="billType")
    original_filename: str = Field(alias="originalFilename")
    uploaded_at: datetime = Field(alias="uploadedAt")
    extraction: BillExtractionData | None = None
    review_warning: str | None = Field(default=None, alias="reviewWarning")


class ConfirmBillResponse(CamelModel):
    bill_id: str = Field(alias="billId")
    household_id: str = Field(alias="householdId")
    status: BillStatus
    confirmed_fields: dict[str, Any] | None = Field(default=None, alias="confirmedFields")
    message: str
