import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Gauge,
  PiggyBank,
  TrendingDown,
  AlertTriangle,
  Info,
  Upload,
} from "lucide-react";
import { getDashboard } from "@/api/endpoints";
import { getHouseholdId } from "@/utils/storage";
import { formatCurrency, formatRiskLabel } from "@/utils/formatters";
import type { DashboardData } from "@/api/types";
import { SummaryCard } from "@/components/dashboard/SummaryCard";
import { PressureChart } from "@/components/dashboard/PressureChart";
import { BillBreakdownCard } from "@/components/dashboard/BillBreakdownCard";
import { RecommendationCard } from "@/components/recommendations/RecommendationCard";
import { DashboardSkeleton } from "@/components/ui/loading-skeleton";
import { ErrorBanner } from "@/components/ui/error-banner";
import { EmptyState } from "@/components/ui/empty-state";
import { cn } from "@/lib/utils";

export default function DashboardPage() {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const householdId = getHouseholdId();

  useEffect(() => {
    if (!householdId) {
      navigate("/onboarding");
      return;
    }
    getDashboard(householdId)
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [householdId, navigate]);

  if (!householdId) return null;
  if (loading) return <DashboardSkeleton />;
  if (error) return <ErrorBanner message={error} onRetry={() => window.location.reload()} />;
  if (!data) return null;

  const { summary, billBreakdown, monthlyPressureForecast, topRecommendedActions, insights } = data;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">Dashboard</h1>

      {/* Summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <SummaryCard
          title="Monthly pressure"
          value={formatCurrency(summary.monthlyHouseholdPressure)}
          subtitle="Total household outgoings"
          icon={<Gauge className="h-5 w-5" />}
        />
        <SummaryCard
          title="Disposable buffer"
          value={formatCurrency(summary.estimatedDisposableBuffer)}
          subtitle="After essential bills"
          icon={<PiggyBank className="h-5 w-5" />}
          variant={summary.estimatedDisposableBuffer < 100 ? "warning" : "default"}
        />
        <SummaryCard
          title="Energy bill risk"
          value={formatRiskLabel(summary.energyBillRisk)}
          subtitle="As % of estimated income"
          icon={<AlertTriangle className="h-5 w-5" />}
          variant={summary.energyBillRisk === "high" ? "danger" : summary.energyBillRisk === "medium_high" ? "warning" : "default"}
        />
        <SummaryCard
          title="Potential savings"
          value={formatCurrency(summary.potentialMonthlySavings)}
          subtitle="Per month if actioned"
          icon={<TrendingDown className="h-5 w-5" />}
          variant={summary.potentialMonthlySavings > 0 ? "success" : "default"}
        />
      </div>

      {/* Bill not uploaded state */}
      {!billBreakdown && (
        <EmptyState
          title="Upload your first energy bill"
          description="Upload an energy bill to get personalised savings recommendations."
          actionLabel="Upload bill"
          onAction={() => navigate("/upload")}
          icon={<Upload className="h-10 w-10" />}
        />
      )}

      {/* Pressure chart */}
      {monthlyPressureForecast.length > 0 && (
        <PressureChart data={monthlyPressureForecast} />
      )}

      {/* Bill breakdown */}
      {billBreakdown && <BillBreakdownCard data={billBreakdown} />}

      {/* Top recommended actions */}
      {topRecommendedActions.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-foreground">
            Top actions this month
          </h2>
          <div className="space-y-4">
            {topRecommendedActions.map((action) => (
              <RecommendationCard key={action.id} action={action} />
            ))}
          </div>
        </div>
      )}

      {/* Insights */}
      {insights.length > 0 && (
        <div className="space-y-3">
          <h2 className="text-lg font-semibold text-foreground">Insights</h2>
          {insights.map((insight, i) => (
            <div
              key={i}
              className={cn(
                "flex items-start gap-3 rounded-xl border p-4",
                insight.type === "caution"
                  ? "border-amber-200 bg-amber-50/50 dark:border-amber-800 dark:bg-amber-950/20"
                  : "border-blue-200 bg-blue-50/50 dark:border-blue-800 dark:bg-blue-950/20"
              )}
            >
              <Info className={cn("h-4 w-4 shrink-0 mt-0.5", insight.type === "caution" ? "text-amber-600" : "text-blue-600")} />
              <div>
                <p className="text-sm font-medium text-foreground">{insight.title}</p>
                <p className="text-sm text-muted-foreground mt-0.5">{insight.body}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
