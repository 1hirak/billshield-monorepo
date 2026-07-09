import type { Confidence, Effort, EnergyBillRisk, SafetyRisk, SavingLabel, Urgency } from "@/api/types";

export function getConfidenceBadge(confidence: Confidence) {
  switch (confidence) {
    case "high":
      return { label: "High confidence", className: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400" };
    case "medium":
      return { label: "Medium confidence", className: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400" };
    case "low":
      return { label: "Low confidence", className: "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400" };
    case "needs_review":
      return { label: "Needs review", className: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400" };
    case "only_if_eligible":
      return { label: "If eligible", className: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400" };
    case "only_if_tariff_eligible":
      return { label: "If tariff eligible", className: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400" };
    default:
      return { label: String(confidence), className: "bg-muted text-muted-foreground" };
  }
}

export function getEffortBadge(effort: Effort) {
  switch (effort) {
    case "low":
      return { label: "Low effort", className: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400" };
    case "medium":
      return { label: "Medium effort", className: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400" };
    case "high":
      return { label: "High effort", className: "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400" };
  }
}

export function getUrgencyBadge(urgency: Urgency) {
  switch (urgency) {
    case "low":
      return { label: "Low urgency", className: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300" };
    case "medium":
      return { label: "Medium urgency", className: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400" };
    case "high":
      return { label: "Urgent", className: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400" };
  }
}

export function getSafetyRiskBadge(risk: SafetyRisk) {
  switch (risk) {
    case "none":
      return { label: "No risk", className: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400" };
    case "low":
      return { label: "Low risk", className: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300" };
    case "medium":
      return { label: "Medium risk", className: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400" };
    case "high":
      return { label: "High risk", className: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400" };
  }
}

export function getEnergyRiskStyle(risk: EnergyBillRisk) {
  switch (risk) {
    case "low":
      return { label: "Low", className: "text-emerald-700 dark:text-emerald-400", bg: "bg-emerald-100 dark:bg-emerald-900/30" };
    case "medium":
      return { label: "Medium", className: "text-amber-700 dark:text-amber-400", bg: "bg-amber-100 dark:bg-amber-900/30" };
    case "medium_high":
      return { label: "Medium-High", className: "text-orange-700 dark:text-orange-400", bg: "bg-orange-100 dark:bg-orange-900/30" };
    case "high":
      return { label: "High", className: "text-red-700 dark:text-red-400", bg: "bg-red-100 dark:bg-red-900/30" };
  }
}

export function getSavingLabelBadge(label: SavingLabel) {
  switch (label) {
    case "estimated_saving":
      return { label: "Estimated saving", className: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400", icon: "pound-sterling" };
    case "potential_saving":
      return { label: "Potential saving", className: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400", icon: "pound-sterling" };
    case "cashflow_improvement":
      return { label: "Cashflow improvement", className: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400", icon: "arrow-up-down" };
    case "support_value":
      return { label: "Support value", className: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400", icon: "heart" };
    case "green_only":
      return { label: "Greener action", className: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400", icon: "leaf" };
    case "no_direct_saving":
      return { label: "No direct saving", className: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400", icon: "minus" };
    case "billing_accuracy":
      return { label: "Billing accuracy", className: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400", icon: "check-circle" };
    case "risk_reduction":
      return { label: "Risk reduction", className: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400", icon: "shield" };
    case "support_access":
      return { label: "Support access", className: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400", icon: "door-open" };
    case "planning":
      return { label: "Planning", className: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400", icon: "clipboard" };
  }
}
