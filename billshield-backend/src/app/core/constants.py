from __future__ import annotations

from datetime import date
from enum import Enum


class HouseholdType(str, Enum):
    SINGLE_ADULT = "single_adult"
    COUPLE = "couple"
    FAMILY_WITH_CHILDREN = "family_with_children"
    PENSIONER_HOUSEHOLD = "pensioner_household"
    SHARED_HOUSEHOLD = "shared_household"


class IncomeBand(str, Enum):
    UNDER_15K = "under_15k"
    FIFTEEN_TO_25K = "15k_25k"
    TWENTYFIVE_TO_40K = "25k_40k"
    FORTY_TO_60K = "40k_60k"
    SIXTY_PLUS = "60k_plus"


class PaymentMethod(str, Enum):
    DIRECT_DEBIT = "direct_debit"
    PREPAYMENT_METER = "prepayment_meter"
    STANDARD_CREDIT = "standard_credit"
    UNKNOWN = "unknown"


class BillStatus(str, Enum):
    UPLOADED = "uploaded"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    DELETED = "deleted"


class BillType(str, Enum):
    ENERGY = "energy"
    COUNCIL_TAX = "council_tax"
    WATER = "water"
    BROADBAND = "broadband"
    OTHER = "other"


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEEDS_REVIEW = "needs_review"
    ONLY_IF_ELIGIBLE = "only_if_eligible"
    ONLY_IF_TARIFF_ELIGIBLE = "only_if_tariff_eligible"


class EffortLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SafetyRiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SavingLabel(str, Enum):
    ESTIMATED_SAVING = "estimated_saving"
    POTENTIAL_SAVING = "potential_saving"
    CASHFLOW_IMPROVEMENT = "cashflow_improvement"
    SUPPORT_VALUE = "support_value"
    GREEN_ONLY = "green_only"
    NO_DIRECT_SAVING = "no_direct_saving"
    BILLING_ACCURACY = "billing_accuracy"
    RISK_REDUCTION = "risk_reduction"
    SUPPORT_ACCESS = "support_access"
    PLANNING = "planning"


class RecommendationEngineType(str, Enum):
    TARIFF_CHECK = "tariff_check"
    DIRECT_DEBIT_HEALTH = "direct_debit_health_check"
    METER_READING_REMINDER = "meter_reading_reminder"
    HEATING_OPTIMISATION = "heating_optimisation"
    APPLIANCE_TIME_SHIFTING = "appliance_time_shifting"
    STANDING_CHARGE_AWARENESS = "standing_charge_awareness"
    ELIGIBILITY_SCANNER = "eligibility_scanner"
    COUNCIL_TAX_REDUCTION = "council_tax_reduction_checker"
    BROADBAND_SOCIAL_TARIFF = "broadband_social_tariff_checker"
    WATER_BILL_OPTIMISER = "water_bill_optimiser"
    FOOD_SUPPORT = "food_support"
    DEBT_ARREARS_TRIAGE = "debt_arrears_triage"


class SupportServiceType(str, Enum):
    WARM_SPACE = "warm_space"
    FOOD_BANK = "food_bank"
    CITIZENS_ADVICE = "citizens_advice"
    LIBRARY = "library"
    COUNCIL_EMERGENCY_SUPPORT = "council_emergency_support"
    DEBT_ADVICE = "debt_advice"
    ENERGY_HELP = "energy_help"


class OpeningStatus(str, Enum):
    OPEN_NOW = "open_now"
    CLOSED_NOW = "closed_now"
    OPENS_TODAY = "opens_today"
    APPOINTMENT_ONLY = "appointment_only"


class RecommendationStatus(str, Enum):
    ACTIVE = "active"
    DISMISSED = "dismissed"
    COMPLETED = "completed"


class TariffType(str, Enum):
    STANDARD_VARIABLE = "standard_variable"
    FIXED = "fixed"
    ECONOMY_7 = "economy_7"
    TIME_OF_USE = "time_of_use"
    DYNAMIC = "dynamic"
    EV = "ev"
    PREPAYMENT = "prepayment"
    OTHER = "other"


INCOME_BAND_MONTHLY_MAP: dict[IncomeBand, int] = {
    IncomeBand.UNDER_15K: 1050,
    IncomeBand.FIFTEEN_TO_25K: 1650,
    IncomeBand.TWENTYFIVE_TO_40K: 2500,
    IncomeBand.FORTY_TO_60K: 3700,
    IncomeBand.SIXTY_PLUS: 5000,
}

ENERGY_CAP_CHANGE_DATES: list[date] = [
    date(2026, 1, 1),
    date(2026, 4, 1),
    date(2026, 7, 1),
    date(2026, 10, 1),
]

CAP_CHANGE_WINDOW_BEFORE_DAYS = 7
CAP_CHANGE_WINDOW_AFTER_DAYS = 5

ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_UPLOAD_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
}

BENCHMARK_TARIFF_THRESHOLD_PCT = 5
TARIFF_HIGH_THRESHOLD_PCT = 10

DIRECT_DEBIT_HEALTHY_MAX_DIFF = 10.0

HEATING_SAFETY_HOUSEHOLD_TYPES: set[HouseholdType] = {
    HouseholdType.PENSIONER_HOUSEHOLD,
}

DEFAULT_ENERGY_COST_FALLBACK = 142
