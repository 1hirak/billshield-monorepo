import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Download,
  Copy,
  RefreshCw,
  Check,
  CheckCircle2,
  Circle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ErrorBanner } from "@/components/ui/error-banner";
import { DashboardSkeleton } from "@/components/ui/loading-skeleton";
import { generateThirtyDayPlan } from "@/api/endpoints";
import { getHouseholdId } from "@/utils/storage";
import { formatCurrency } from "@/utils/formatters";
import { getEffortBadge, getSavingLabelBadge } from "@/utils/badgeStyles";
import type { ThirtyDayPlan, PlanItem, PlanSection } from "@/api/types";
import { cn } from "@/lib/utils";

export default function ThirtyDayPlanPage() {
  const navigate = useNavigate();
  const householdId = getHouseholdId();
  const [plan, setPlan] = useState<ThirtyDayPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [completedIds, setCompletedIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (!householdId) {
      navigate("/onboarding");
      return;
    }
    loadPlan();
  }, [householdId, navigate]);

  const loadPlan = async () => {
    if (!householdId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await generateThirtyDayPlan({
        householdId,
        includeCompletedActions: false,
        tone: "supportive_practical",
      });
      setPlan(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate plan");
    } finally {
      setLoading(false);
    }
  };

  const toggleComplete = (id: string) => {
    setCompletedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const getPlanText = (): string => {
    if (!plan) return "";
    const sections = [plan.thisWeek, plan.nextTwoWeeks, plan.byDayThirty];
    let text = `${plan.title}\n\n${plan.intro}\n\n`;
    for (const section of sections) {
      if (section.items.length === 0) continue;
      text += `--- ${section.title} ---\n`;
      for (const item of section.items) {
        const done = completedIds.has(item.id) ? "[x]" : "[ ]";
        text += `${done} ${item.title}: ${item.description}\n`;
      }
      text += "\n";
    }
    text += plan.reassurance;
    return text;
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(getPlanText());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([getPlanText()], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "billshield-30-day-plan.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!householdId) return null;
  if (loading) return <DashboardSkeleton />;
  if (error) return <ErrorBanner message={error} onRetry={loadPlan} />;
  if (!plan) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">{plan.title}</h1>
          <p className="text-sm text-muted-foreground mt-1">{plan.intro}</p>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex flex-wrap gap-2">
        {plan.actions.downloadAvailable && (
          <Button variant="outline" size="sm" onClick={handleDownload}>
            <Download className="h-3.5 w-3.5 mr-1.5" />
            Download plan
          </Button>
        )}
        {plan.actions.copyAvailable && (
          <Button variant="outline" size="sm" onClick={handleCopy}>
            {copied ? <Check className="h-3.5 w-3.5 mr-1.5" /> : <Copy className="h-3.5 w-3.5 mr-1.5" />}
            {copied ? "Copied" : "Copy plan"}
          </Button>
        )}
        {plan.actions.regenerateAvailable && (
          <Button variant="outline" size="sm" onClick={loadPlan}>
            <RefreshCw className="h-3.5 w-3.5 mr-1.5" />
            Regenerate
          </Button>
        )}
      </div>

      {/* Plan sections */}
      {[plan.thisWeek, plan.nextTwoWeeks, plan.byDayThirty].map((section) => (
        section.items.length > 0 && (
          <PlanSectionComponent
            key={section.title}
            section={section}
            completedIds={completedIds}
            onToggle={toggleComplete}
          />
        )
      ))}

      {/* Reassurance */}
      <div className="rounded-2xl border border-border bg-card p-5">
        <p className="text-sm text-muted-foreground italic">{plan.reassurance}</p>
      </div>
    </div>
  );
}

function PlanSectionComponent({
  section,
  completedIds,
  onToggle,
}: {
  section: PlanSection;
  completedIds: Set<string>;
  onToggle: (id: string) => void;
}) {
  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold text-foreground">{section.title}</h2>
      <div className="space-y-3">
        {section.items.map((item) => (
          <PlanItemCard
            key={item.id}
            item={item}
            completed={completedIds.has(item.id)}
            onToggle={() => onToggle(item.id)}
          />
        ))}
      </div>
    </div>
  );
}

function PlanItemCard({
  item,
  completed,
  onToggle,
}: {
  item: PlanItem;
  completed: boolean;
  onToggle: () => void;
}) {
  const [scriptCopied, setScriptCopied] = useState(false);
  const effortBadge = getEffortBadge(item.effort);
  const savingBadge = getSavingLabelBadge(item.savingLabel);

  const handleCopyScript = async () => {
    if (item.callScript) {
      await navigator.clipboard.writeText(item.callScript);
      setScriptCopied(true);
      setTimeout(() => setScriptCopied(false), 2000);
    }
  };

  return (
    <div
      className={cn(
        "rounded-xl border bg-card p-4 space-y-3 transition-opacity",
        completed ? "border-emerald-200 dark:border-emerald-800 opacity-75" : "border-border"
      )}
    >
      <div className="flex items-start gap-3">
        <button onClick={onToggle} className="mt-0.5 shrink-0">
          {completed ? (
            <CheckCircle2 className="h-5 w-5 text-emerald-600" />
          ) : (
            <Circle className="h-5 w-5 text-muted-foreground" />
          )}
        </button>
        <div className="flex-1 min-w-0">
          <p className={cn("text-sm font-medium", completed && "line-through text-muted-foreground")}>
            {item.title}
          </p>
          <p className="text-sm text-muted-foreground mt-0.5">{item.description}</p>
        </div>
        {item.estimatedSavingPounds != null && (
          <span className="text-sm font-semibold text-emerald-700 dark:text-emerald-400 shrink-0">
            {formatCurrency(item.estimatedSavingPounds)}
          </span>
        )}
      </div>

      <div className="flex flex-wrap gap-1.5 pl-8">
        <span className={cn("text-xs px-1.5 py-0.5 rounded font-medium", savingBadge.className)}>
          {savingBadge.label}
        </span>
        <span className={cn("text-xs px-1.5 py-0.5 rounded font-medium", effortBadge.className)}>
          {effortBadge.label}
        </span>
      </div>

      {item.callScript && (
        <div className="ml-8 rounded-lg border border-border bg-muted/50 p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-medium text-foreground">Call script</span>
            <Button variant="ghost" size="sm" onClick={handleCopyScript} className="h-6 text-xs">
              {scriptCopied ? "Copied" : "Copy"}
            </Button>
          </div>
          <blockquote className="text-sm italic text-muted-foreground border-l-2 border-primary/30 pl-3">
            {item.callScript}
          </blockquote>
        </div>
      )}
    </div>
  );
}
