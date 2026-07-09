import { useEffect, useState, useCallback, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Loader2, AlertTriangle, Info } from "lucide-react";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { ErrorBanner } from "@/components/ui/error-banner";
import { simulateScenario } from "@/api/endpoints";
import { getHouseholdId, getBillId } from "@/utils/storage";
import { formatCurrency } from "@/utils/formatters";
import { getSavingLabelBadge, getConfidenceBadge } from "@/utils/badgeStyles";
import type { ScenarioBreakdown, ScenarioResult } from "@/api/types";
import { cn } from "@/lib/utils";

export default function ScenarioSimulatorPage() {
  const navigate = useNavigate();
  const householdId = getHouseholdId();
  const billId = getBillId();

  const [heating, setHeating] = useState(0);
  const [appliance, setAppliance] = useState(0);
  const [offPeak, setOffPeak] = useState(false);
  const [ddReview, setDdReview] = useState(true);
  const [councilTax, setCouncilTax] = useState(true);
  const [broadband, setBroadband] = useState(false);
  const [water, setWater] = useState(false);
  const [paymentDate, setPaymentDate] = useState(false);

  const [result, setResult] = useState<ScenarioResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!householdId) navigate("/onboarding");
  }, [householdId, navigate]);

  const simulate = useCallback(async () => {
    if (!householdId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await simulateScenario({
        householdId,
        billId,
        heatingReductionCelsius: heating,
        applianceReductionPercent: 0,
        shiftAppliancesToOffPeak: offPeak,
        requestDirectDebitReview: ddReview,
        applyForCouncilTaxReduction: councilTax,
        switchToSocialBroadbandTariff: broadband,
        checkWaterMeterOrSocialTariff: water,
        changePaymentDate: paymentDate,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Simulation failed");
    } finally {
      setLoading(false);
    }
  }, [householdId, billId, heating, offPeak, ddReview, councilTax, broadband, water, paymentDate]);

  useEffect(() => {
    const timeout = setTimeout(simulate, 500);
    return () => clearTimeout(timeout);
  }, [simulate]);

  const applianceSaving = Math.round(appliance * 0.1);

  const displayResult = useMemo<ScenarioResult | null>(() => {
    if (!result) return null;
    const extraBreakdown: ScenarioBreakdown[] =
      appliance > 0
        ? [
            {
              category: "Appliance reduction",
              monthlySaving: applianceSaving,
              confidence: "medium",
              savingLabel: "estimated_saving",
            },
          ]
        : [];
    return {
      ...result,
      estimatedMonthlySaving: result.estimatedMonthlySaving + applianceSaving,
      estimatedAnnualSaving: result.estimatedMonthlySaving * 12 + applianceSaving * 12,
      breakdown: [...result.breakdown, ...extraBreakdown],
    };
  }, [result, appliance, applianceSaving]);

  if (!householdId) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Scenario Simulator</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Explore what-if scenarios to understand how changes could reduce your monthly pressure.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Controls */}
        <div className="rounded-2xl border border-border bg-card p-6 space-y-6">
          <h2 className="text-base font-semibold">Adjustments</h2>

          <div className="space-y-5">
            <div className="space-y-3">
              <Label className="text-sm">Lower heating by {heating}{"\u00B0"}C</Label>
              <Slider
                value={[heating]}
                onValueChange={([v]) => setHeating(v)}
                min={0}
                max={2}
                step={0.5}
              />
              <p className="text-xs text-muted-foreground">0{"\u00B0"}C to 2{"\u00B0"}C reduction</p>
              <div className="flex items-start gap-2 rounded-lg bg-blue-50 dark:bg-blue-950/20 p-3">
                <Info className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
                <p className="text-xs text-blue-800 dark:text-blue-300">
                  For households with children, older residents, or health conditions, we focus on non-temperature actions like draught-proofing. Heating savings may not apply to your profile.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <Label className="text-sm">
                Reduce appliance use by {appliance}% —
                <span className="font-medium text-emerald-700 dark:text-emerald-400 ml-1">
                  {formatCurrency(applianceSaving)}/mo
                </span>
              </Label>
              <Slider
                value={[appliance]}
                onValueChange={([v]) => setAppliance(v)}
                min={0}
                max={30}
                step={5}
              />
            </div>

            <ToggleRow label="Shift appliances to off-peak" checked={offPeak} onChange={setOffPeak} />
            <ToggleRow label="Request Direct Debit review" checked={ddReview} onChange={setDdReview} />
            <ToggleRow label="Apply for Council Tax Reduction" checked={councilTax} onChange={setCouncilTax} />
            <ToggleRow label="Switch to social broadband tariff" checked={broadband} onChange={setBroadband} />
            <ToggleRow label="Check water meter / social tariff" checked={water} onChange={setWater} />
            <ToggleRow label="Change payment date" checked={paymentDate} onChange={setPaymentDate} />
          </div>

          <div className="flex items-start gap-2 rounded-lg bg-amber-50 dark:bg-amber-950/20 p-3">
            <AlertTriangle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
            <p className="text-xs text-amber-800 dark:text-amber-300">
              BillShield will not recommend unsafe under-heating. Keep regularly used rooms at a safe temperature, especially for older people, children, or anyone with health conditions.
            </p>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-4">
          {error && <ErrorBanner message={error} />}

          {loading && !result && (
            <div className="rounded-2xl border border-border bg-card p-6 flex items-center justify-center h-48">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          )}

          {displayResult && (
            <>
              {/* Summary */}
              <div className="rounded-2xl border border-border bg-card p-6 space-y-4">
                <h2 className="text-base font-semibold">Estimated Impact</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Monthly saving</p>
                    <p className="text-2xl font-bold text-emerald-700 dark:text-emerald-400">
                      {formatCurrency(displayResult.estimatedMonthlySaving)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Annual saving</p>
                    <p className="text-2xl font-bold text-emerald-700 dark:text-emerald-400">
                      {formatCurrency(displayResult.estimatedAnnualSaving)}
                    </p>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <span className={cn("text-xs px-2 py-0.5 rounded-md font-medium", getConfidenceBadge(displayResult.confidence).className)}>
                    {getConfidenceBadge(displayResult.confidence).label}
                  </span>
                </div>
              </div>

              {displayResult.safetyWarning && (
                <div className="flex items-start gap-2 rounded-xl border border-red-200 bg-red-50/50 dark:border-red-800 dark:bg-red-950/20 p-4">
                  <AlertTriangle className="h-4 w-4 text-red-600 shrink-0 mt-0.5" />
                  <p className="text-sm text-red-800 dark:text-red-300">{displayResult.safetyWarning}</p>
                </div>
              )}
              {displayResult.tariffWarning && (
                <div className="flex items-start gap-2 rounded-xl border border-amber-200 bg-amber-50/50 dark:border-amber-800 dark:bg-amber-950/20 p-4">
                  <Info className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
                  <p className="text-sm text-amber-800 dark:text-amber-300">{displayResult.tariffWarning}</p>
                </div>
              )}

              {displayResult.breakdown.length > 0 && (
                <div className="rounded-2xl border border-border bg-card p-6 space-y-4">
                  <h3 className="text-base font-semibold">Savings Breakdown</h3>
                  <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={displayResult.breakdown} layout="vertical" margin={{ left: 20, right: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
                        <XAxis type="number" tickFormatter={(v) => `\u00A3${v}`} />
                        <YAxis type="category" dataKey="category" width={140} tick={{ fontSize: 12 }} />
                        <Tooltip formatter={(value) => [`\u00A3${value}/month`]} />
                        <Bar dataKey="monthlySaving" fill="#10b981" radius={[0, 4, 4, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  <div className="space-y-2">
                    {displayResult.breakdown.map((item, i) => {
                      const badge = getSavingLabelBadge(item.savingLabel);
                      return (
                        <div key={i} className="flex items-center justify-between text-sm">
                          <div className="flex items-center gap-2">
                            <span className="text-foreground">{item.category}</span>
                            <span className={cn("text-xs px-1.5 py-0.5 rounded font-medium", badge.className)}>
                              {badge.label}
                            </span>
                          </div>
                          <span className="font-medium text-emerald-700 dark:text-emerald-400">
                            {formatCurrency(item.monthlySaving)}/mo
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {displayResult.notes.length > 0 && (
                <div className="rounded-2xl border border-border bg-card p-6 space-y-2">
                  <h3 className="text-sm font-semibold text-foreground">Notes</h3>
                  <ul className="space-y-1">
                    {displayResult.notes.map((note, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                        <span className="shrink-0 mt-1.5 h-1.5 w-1.5 rounded-full bg-muted-foreground" />
                        {note}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {offPeak && (
                <div className="flex items-start gap-2 rounded-lg bg-blue-50 dark:bg-blue-950/20 p-3">
                  <Info className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
                  <p className="text-xs text-blue-800 dark:text-blue-300">
                    On flat tariffs, off-peak appliance use may be greener but not cheaper. On Economy 7, time-of-use, EV, battery, or smart tariffs, off-peak scheduling may reduce bills.
                  </p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function ToggleRow({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between">
      <Label className="text-sm">{label}</Label>
      <Switch checked={checked} onCheckedChange={onChange} />
    </div>
  );
}
