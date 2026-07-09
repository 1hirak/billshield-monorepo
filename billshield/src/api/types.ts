export type HouseholdType =
  | "single_adult"
  | "couple"
  | "family_with_children"
  | "pensioner_household"
  | "shared_household";

export type IncomeBand =
  | "under_15k"
  | "15k_25k"
  | "25k_40k"
  | "40k_60k"
  | "60k_plus";

export type PaymentMethod =
  | "direct_debit"
  | "prepayment_meter"
  | "standard_credit"
  | "unknown";

export type Confidence =
  | "high"
  | "medium"
  | "low"
  | "needs_review"
  | "only_if_eligible"
  | "only_if_tariff_eligible";

export type Effort = "low" | "medium" | "high";
export type Urgency = "low" | "medium" | "high";
export type SafetyRisk = "none" | "low" | "medium" | "high";

export type SavingLabel =
  | "estimated_saving"
  | "potential_saving"
  | "cashflow_improvement"
  | "support_value"
  | "green_only"
  | "no_direct_saving"
  | "billing_accuracy"
  | "risk_reduction"
  | "support_access"
  | "planning";

export type EnergyBillRisk = "low" | "medium" | "medium_high" | "high";

export type SupportServiceType =
  | "warm_space"
  | "food_bank"
  | "citizens_advice"
  | "library"
  | "council_emergency_support"
  | "debt_advice"
  | "energy_help";

export type OpeningStatus =
  | "open_now"
  | "closed_now"
  | "opens_today"
  | "appointment_only";

export interface HouseholdPayload {
  postcode: string;
  householdType: HouseholdType;
  incomeBand: IncomeBand;
  energyProvider: string;
  paymentMethod: PaymentMethod;
  monthlyRentOrMortgage: number;
  monthlyFoodCost: number;
  monthlyTransportCost: number;
  monthlyCouncilTax: number;
  monthlyBroadbandMobileCost: number;
  monthlyWaterCost: number;
  receivesQualifyingBenefits?: boolean;
  hasChildren?: boolean;
  hasPensioner?: boolean;
  hasHealthCondition?: boolean;
  hasDisability?: boolean;
  isSingleAdult?: boolean;
  bedrooms?: number;
  occupants?: number;
  waterMetered?: boolean;
}

export interface Household extends HouseholdPayload {
  id: string;
  normalizedPostcode: string;
  createdAt: string;
}

export interface ExtractionField<T = string | number | null> {
  value: T;
  confidence: Confidence;
}

export interface BillExtraction {
  billId: string;
  householdId: string;
  status: string;
  billType: string;
  originalFilename: string;
  uploadedAt: string;
  extraction: {
    supplier: ExtractionField<string>;
    tariffName: ExtractionField<string>;
    monthlyDirectDebit: ExtractionField<number>;
    electricityUnitRatePencePerKwh: ExtractionField<number>;
    electricityStandingChargePencePerDay: ExtractionField<number>;
    gasUnitRatePencePerKwh: ExtractionField<number>;
    gasStandingChargePencePerDay: ExtractionField<number>;
    annualElectricityUsageKwh: ExtractionField<number>;
    annualGasUsageKwh: ExtractionField<number>;
    billPeriodStart: ExtractionField<string>;
    billPeriodEnd: ExtractionField<string>;
    paymentMethod: ExtractionField<string>;
    tariffType: ExtractionField<string>;
    contractEndDate: ExtractionField<string | null>;
  };
  reviewWarning: string;
}

export interface BillUploadResponse {
  billId: string;
  householdId: string;
  status: string;
  message: string;
  extractionSummary: {
    supplier: string;
    tariffName: string;
    monthlyDirectDebit: number;
    overallConfidence: Confidence;
    needsReviewFields: string[];
  };
}

export interface BillConfirmResponse {
  billId: string;
  householdId: string;
  status: string;
  confirmedFields: Record<string, unknown>;
  message: string;
}

export interface RecommendedAction {
  id: string;
  rank: number;
  engineType: string;
  title: string;
  description: string;
  whatDetected?: string;
  whyItMatters?: string;
  monthlySavingPounds?: number;
  annualSavingPounds?: number;
  savingLabel?: SavingLabel;
  effort?: Effort;
  confidence?: Confidence;
  urgency?: Urgency;
  safetyRisk?: SafetyRisk;
  eligibilityCaveat?: string | null;
  safetyCaveat?: string | null;
  nextStep?: string;
  steps?: string[];
  ctaLabel?: string;
  callScript?: string | null;
}

export interface DashboardInsight {
  type: "info" | "caution";
  title: string;
  body: string;
}

export interface MonthlyPressureForecast {
  month: string;
  energy: number;
  rent: number;
  food: number;
  transport: number;
  councilTax: number;
  water: number;
  broadbandMobile: number;
}

export interface BillBreakdown {
  electricityUsageCostMonthly: number;
  gasUsageCostMonthly: number;
  standingChargesMonthly: number;
  monthlyDirectDebit: number;
  estimatedAnnualCost?: number;
  currentTariffStatus?: string;
  standingChargeInsight?: string;
  insight?: string;
  avoidableCostMonthly: number;
  unavoidableStandingChargeMonthly: number;
}

export interface DashboardData {
  householdId: string;
  summary: {
    monthlyHouseholdPressure: number;
    estimatedDisposableBuffer: number;
    energyBillRisk: EnergyBillRisk;
    potentialMonthlySavings: number;
  };
  monthlyPressureForecast: MonthlyPressureForecast[];
  billBreakdown: BillBreakdown | null;
  topRecommendedActions: RecommendedAction[];
  otherRecommendedActions: RecommendedAction[];
  insights: DashboardInsight[];
}

export interface ScenarioPayload {
  householdId: string;
  billId?: string | null;
  heatingReductionCelsius: number;
  applianceReductionPercent: number;
  shiftAppliancesToOffPeak: boolean;
  requestDirectDebitReview: boolean;
  applyForCouncilTaxReduction: boolean;
  switchToSocialBroadbandTariff: boolean;
  checkWaterMeterOrSocialTariff: boolean;
  changePaymentDate: boolean;
}

export interface ScenarioBreakdown {
  category: string;
  monthlySaving: number;
  confidence: Confidence;
  savingLabel: SavingLabel;
}

export interface ScenarioResult {
  householdId: string;
  estimatedMonthlySaving: number;
  estimatedAnnualSaving: number;
  confidence: Confidence;
  overallRisk: SafetyRisk;
  safetyWarning: string | null;
  tariffWarning: string | null;
  breakdown: ScenarioBreakdown[];
  notes: string[];
}

export interface SupportService {
  id: string;
  name: string;
  type: SupportServiceType;
  distanceMiles: number;
  openingStatus: OpeningStatus;
  shortDescription: string;
  addressLine1: string;
  town: string;
  phone: string | null;
  website: string | null;
  directionsLabel: string;
}

export interface SupportServicesResponse {
  postcode: string;
  normalizedPostcode: string;
  radiusMiles: number;
  mapPlaceholder: {
    centerLabel: string;
    message: string;
  };
  services: SupportService[];
  availableFilters: string[];
}

export interface PlanItem {
  id: string;
  title: string;
  description: string;
  estimatedSavingPounds: number | null;
  savingLabel: SavingLabel;
  effort: Effort;
  done: boolean;
  callScript: string | null;
}

export interface PlanSection {
  title: string;
  items: PlanItem[];
}

export interface ThirtyDayPlan {
  planId: string;
  householdId: string;
  generatedAt: string;
  title: string;
  intro: string;
  thisWeek: PlanSection;
  nextTwoWeeks: PlanSection;
  byDayThirty: PlanSection;
  actions: {
    downloadAvailable: boolean;
    copyAvailable: boolean;
    regenerateAvailable: boolean;
  };
  reassurance: string;
}

export interface SeedResponse {
  householdId: string;
  billId?: string;
  message: string;
}

export interface HealthResponse {
  status: string;
  appName: string;
  version: string;
  environment: string;
  mockMode: boolean;
}
