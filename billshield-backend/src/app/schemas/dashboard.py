from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from app.core.constants import ConfidenceLevel, EffortLevel, SafetyRiskLevel, SavingLabel, UrgencyLevel
from app.schemas.common import CamelModel


class DashboardSummary(CamelModel):
    monthly_household_pressure: float = Field(alias="monthlyHouseholdPressure")
    estimated_disposable_buffer: float = Field(alias="estimatedDisposableBuffer")
    energy_bill_risk: str = Field(alias="energyBillRisk")
    potential_monthly_savings: float = Field(alias="potentialMonthlySavings")


class MonthlyPressurePoint(CamelModel):
    month: str
    energy: float
    rent: float
    food: float
    transport: float
    council_tax: float = Field(alias="councilTax")
    water: float
    broadband_mobile: float = Field(alias="broadbandMobile")


class BillBreakdown(CamelModel):
    electricity_usage_cost_monthly: float = Field(alias="electricityUsageCostMonthly")
    gas_usage_cost_monthly: float = Field(alias="gasUsageCostMonthly")
    standing_charges_monthly: float = Field(alias="standingChargesMonthly")
    monthly_direct_debit: float = Field(alias="monthlyDirectDebit")
    estimated_annual_cost: float = Field(alias="estimatedAnnualCost")
    current_tariff_status: str = Field(alias="currentTariffStatus")
    standing_charge_insight: str = Field(alias="standingChargeInsight")
    avoidable_cost_monthly: float = Field(alias="avoidableCostMonthly")
    unavoidable_standing_charge_monthly: float = Field(alias="unavoidableStandingChargeMonthly")


class DashboardRecommendation(CamelModel):
    id: str
    rank: int
    engine_type: str = Field(alias="engineType")
    title: str
    description: str
    what_detected: str | None = Field(default=None, alias="whatDetected")
    why_it_matters: str | None = Field(default=None, alias="whyItMatters")
    monthly_saving_pounds: float | None = Field(default=None, alias="monthlySavingPounds")
    annual_saving_pounds: float | None = Field(default=None, alias="annualSavingPounds")
    saving_label: str | None = Field(default=None, alias="savingLabel")
    effort: str | None = None
    confidence: str | None = None
    urgency: str | None = None
    safety_risk: str | None = Field(default=None, alias="safetyRisk")
    eligibility_caveat: str | None = Field(default=None, alias="eligibilityCaveat")
    safety_caveat: str | None = Field(default=None, alias="safetyCaveat")
    next_step: str | None = Field(default=None, alias="nextStep")
    steps: list[str] | None = None
    cta_label: str | None = Field(default="View steps", alias="ctaLabel")


class DashboardInsight(CamelModel):
    type: str
    title: str
    body: str


class DashboardResponse(CamelModel):
    household_id: str = Field(alias="householdId")
    summary: DashboardSummary
    monthly_pressure_forecast: list[MonthlyPressurePoint] = Field(alias="monthlyPressureForecast")
    bill_breakdown: BillBreakdown | None = Field(default=None, alias="billBreakdown")
    top_recommended_actions: list[DashboardRecommendation] = Field(alias="topRecommendedActions")
    other_recommended_actions: list[DashboardRecommendation] = Field(
        default_factory=list, alias="otherRecommendedActions"
    )
    insights: list[DashboardInsight] = Field(default_factory=list)
