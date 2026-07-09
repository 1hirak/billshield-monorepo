import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Loader2, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ErrorBanner } from "@/components/ui/error-banner";
import { DashboardSkeleton } from "@/components/ui/loading-skeleton";
import { getBillExtraction, confirmBillFields } from "@/api/endpoints";
import type { BillExtraction, Confidence } from "@/api/types";
import { cn } from "@/lib/utils";
import { getConfidenceBadge } from "@/utils/badgeStyles";

interface FieldConfig {
  key: string;
  label: string;
  type: "text" | "number" | "date";
  suffix?: string;
}

const FIELDS: FieldConfig[] = [
  { key: "supplier", label: "Supplier", type: "text" },
  { key: "tariffName", label: "Tariff name", type: "text" },
  { key: "monthlyDirectDebit", label: "Monthly Direct Debit", type: "number", suffix: "\u00A3" },
  { key: "electricityUnitRatePencePerKwh", label: "Electricity unit rate", type: "number", suffix: "p/kWh" },
  { key: "electricityStandingChargePencePerDay", label: "Electricity standing charge", type: "number", suffix: "p/day" },
  { key: "gasUnitRatePencePerKwh", label: "Gas unit rate", type: "number", suffix: "p/kWh" },
  { key: "gasStandingChargePencePerDay", label: "Gas standing charge", type: "number", suffix: "p/day" },
  { key: "annualElectricityUsageKwh", label: "Annual electricity usage", type: "number", suffix: "kWh" },
  { key: "annualGasUsageKwh", label: "Annual gas usage", type: "number", suffix: "kWh" },
  { key: "billPeriodStart", label: "Bill period start", type: "date" },
  { key: "billPeriodEnd", label: "Bill period end", type: "date" },
  { key: "paymentMethod", label: "Payment method", type: "text" },
  { key: "tariffType", label: "Tariff type", type: "text" },
  { key: "contractEndDate", label: "Contract end date", type: "date" },
];

export default function BillReviewPage() {
  const { billId } = useParams<{ billId: string }>();
  const navigate = useNavigate();
  const [data, setData] = useState<BillExtraction | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [values, setValues] = useState<Record<string, string | number | null>>({});

  useEffect(() => {
    if (!billId) return;
    getBillExtraction(billId)
      .then((d) => {
        setData(d);
        const initial: Record<string, string | number | null> = {};
        for (const field of FIELDS) {
          const ext = d.extraction[field.key as keyof typeof d.extraction];
          if (ext) initial[field.key] = ext.value;
        }
        setValues(initial);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [billId]);

  const handleConfirm = async () => {
    if (!billId) return;
    setSubmitting(true);
    setError(null);
    try {
      await confirmBillFields(billId, values);
      navigate("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to confirm");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <DashboardSkeleton />;
  if (error && !data) return <ErrorBanner message={error} onRetry={() => window.location.reload()} />;
  if (!data) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Review extracted details</h1>
        <p className="text-sm text-muted-foreground mt-1">
          {data.reviewWarning}
        </p>
      </div>

      {error && <ErrorBanner message={error} />}

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Left: Bill preview placeholder */}
        <div className="lg:col-span-2">
          <div className="rounded-2xl border border-border bg-card p-6 space-y-4 sticky top-20">
            <div className="flex items-center gap-2 text-muted-foreground">
              <FileText className="h-5 w-5" />
              <span className="text-sm font-medium">Bill Preview</span>
            </div>
            <div className="rounded-xl bg-muted/50 p-6 space-y-3">
              <div className="h-4 w-3/4 bg-muted rounded" />
              <div className="h-3 w-full bg-muted rounded" />
              <div className="h-3 w-5/6 bg-muted rounded" />
              <div className="mt-4 space-y-2">
                {["Supplier", "Direct Debit", "Electricity rate", "Gas rate", "Standing charge", "Tariff"].map((tag) => (
                  <span
                    key={tag}
                    className="inline-block mr-2 mb-1 text-xs px-2 py-0.5 rounded bg-primary/10 text-primary font-medium"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <div className="h-3 w-full bg-muted rounded mt-4" />
              <div className="h-3 w-2/3 bg-muted rounded" />
              <div className="h-3 w-4/5 bg-muted rounded" />
            </div>
            <p className="text-xs text-muted-foreground">
              {data.originalFilename}
            </p>
          </div>
        </div>

        {/* Right: Editable fields */}
        <div className="lg:col-span-3 space-y-4">
          {FIELDS.map((field) => {
            const ext = data.extraction[field.key as keyof typeof data.extraction];
            const confidence = ext?.confidence as Confidence | undefined;
            const badge = confidence ? getConfidenceBadge(confidence) : null;
            const needsReview = confidence === "needs_review";

            return (
              <div
                key={field.key}
                className={cn(
                  "rounded-xl border p-4 space-y-2",
                  needsReview
                    ? "border-red-300 bg-red-50/50 dark:border-red-800 dark:bg-red-950/20"
                    : "border-border bg-card"
                )}
              >
                <div className="flex items-center justify-between">
                  <Label htmlFor={field.key} className="text-sm font-medium">
                    {field.label}
                  </Label>
                  {badge && (
                    <span className={cn("text-xs px-2 py-0.5 rounded-md font-medium", badge.className)}>
                      {badge.label}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  {field.suffix && field.type === "number" && (
                    <span className="text-sm text-muted-foreground">{field.suffix === "\u00A3" ? "\u00A3" : ""}</span>
                  )}
                  <Input
                    id={field.key}
                    type={field.type === "date" ? "date" : field.type}
                    value={values[field.key] ?? ""}
                    onChange={(e) =>
                      setValues((prev) => ({
                        ...prev,
                        [field.key]: field.type === "number" ? Number(e.target.value) : e.target.value || null,
                      }))
                    }
                    className={cn(needsReview && "border-red-300 dark:border-red-700")}
                  />
                  {field.suffix && field.suffix !== "\u00A3" && (
                    <span className="text-xs text-muted-foreground whitespace-nowrap">{field.suffix}</span>
                  )}
                </div>
              </div>
            );
          })}

          <div className="flex items-center gap-3 pt-4">
            <Button variant="outline" onClick={() => navigate("/upload")}>
              Back
            </Button>
            <Button onClick={handleConfirm} disabled={submitting} className="flex-1">
              {submitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Confirm and continue to dashboard
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
