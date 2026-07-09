from __future__ import annotations

from pydantic import Field

from app.core.constants import SavingLabel
from app.schemas.common import CamelModel


class SimulateScenarioRequest(CamelModel):
    household_id: str = Field(alias="householdId")
    bill_id: str | None = Field(default=None, alias="billId")
    heating_reduction_celsius: float = Field(default=0, alias="heatingReductionCelsius")
    appliance_reduction_percent: float = Field(default=0, alias="applianceReductionPercent")
    shift_appliances_to_off_peak: bool = Field(default=False, alias="shiftAppliancesToOffPeak")
    request_direct_debit_review: bool = Field(default=False, alias="requestDirectDebitReview")
    apply_for_council_tax_reduction: bool = Field(default=False, alias="applyForCouncilTaxReduction")
    switch_to_social_broadband_tariff: bool = Field(default=False, alias="switchToSocialBroadbandTariff")
    check_water_meter_or_social_tariff: bool = Field(default=False, alias="checkWaterMeterOrSocialTariff")
    change_payment_date: bool = Field(default=False, alias="changePaymentDate")


class ScenarioBreakdownItem(CamelModel):
    category: str
    monthly_saving: float = Field(alias="monthlySaving")
    confidence: str
    saving_label: str = Field(alias="savingLabel")


class ScenarioSimulationResponse(CamelModel):
    household_id: str = Field(alias="householdId")
    estimated_monthly_saving: float = Field(alias="estimatedMonthlySaving")
    estimated_annual_saving: float = Field(alias="estimatedAnnualSaving")
    confidence: str
    overall_risk: str = Field(alias="overallRisk")
    safety_warning: str | None = Field(default=None, alias="safetyWarning")
    tariff_warning: str | None = Field(default=None, alias="tariffWarning")
    breakdown: list[ScenarioBreakdownItem]
    notes: list[str] = Field(default_factory=list)
