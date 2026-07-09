import type { BillBreakdown as BillBreakdownType } from "@/api/types";
import { formatCurrency } from "@/utils/formatters";
import { Info } from "lucide-react";

interface BillBreakdownCardProps {
  data: BillBreakdownType;
}

export function BillBreakdownCard({ data }: BillBreakdownCardProps) {
  const rows = [
    { label: "Electricity usage", value: data.electricityUsageCostMonthly },
    { label: "Gas usage", value: data.gasUsageCostMonthly },
    { label: "Standing charges", value: data.standingChargesMonthly },
    { label: "Monthly Direct Debit", value: data.monthlyDirectDebit, bold: true },
    ...(data.estimatedAnnualCost ? [{ label: "Estimated annual cost", value: data.estimatedAnnualCost }] : []),
    { label: "Avoidable cost (monthly)", value: data.avoidableCostMonthly },
    { label: "Unavoidable standing charge", value: data.unavoidableStandingChargeMonthly },
  ];

  const insightText = data.standingChargeInsight || data.insight;

  return (
    <div className="rounded-2xl border border-border bg-card p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-semibold text-foreground">Bill Breakdown</h3>
        {data.currentTariffStatus && (
          <span className="text-xs px-2 py-1 rounded-md bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400">
            {data.currentTariffStatus.replace(/_/g, " ")}
          </span>
        )}
      </div>

      <div className="divide-y divide-border">
        {rows.map((row) => (
          <div
            key={row.label}
            className="flex items-center justify-between py-2.5"
          >
            <span className="text-sm text-muted-foreground">{row.label}</span>
            <span className={`text-sm ${row.bold ? "font-semibold text-foreground" : "text-foreground"}`}>
              {formatCurrency(row.value)}
            </span>
          </div>
        ))}
      </div>

      {insightText && (
        <div className="flex items-start gap-2 rounded-lg bg-blue-50 dark:bg-blue-950/20 p-3">
          <Info className="h-4 w-4 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
          <p className="text-xs text-blue-800 dark:text-blue-300">
            {insightText}
          </p>
        </div>
      )}
    </div>
  );
}
