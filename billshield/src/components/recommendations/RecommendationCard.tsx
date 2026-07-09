import { useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import type { RecommendedAction } from "@/api/types";
import { formatCurrency } from "@/utils/formatters";
import {
  getConfidenceBadge,
  getEffortBadge,
  getUrgencyBadge,
  getSafetyRiskBadge,
  getSavingLabelBadge,
} from "@/utils/badgeStyles";

interface RecommendationCardProps {
  action: RecommendedAction;
  showRank?: boolean;
}

export function RecommendationCard({ action, showRank = true }: RecommendationCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopyScript = async () => {
    if (action.callScript) {
      await navigator.clipboard.writeText(action.callScript);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const savingBadge = action.savingLabel ? getSavingLabelBadge(action.savingLabel) : null;

  return (
    <div className="rounded-2xl border border-border bg-card p-5 space-y-4">
      <div className="flex items-start gap-3">
        {showRank && (
          <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-bold">
            {action.rank}
          </div>
        )}
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-foreground leading-tight">
            {action.title}
          </h4>
          <p className="mt-1 text-sm text-muted-foreground">{action.description}</p>
        </div>
        {action.monthlySavingPounds != null && action.monthlySavingPounds > 0 && (
          <div className="text-right shrink-0">
            <p className="text-lg font-bold text-emerald-700 dark:text-emerald-400">
              {formatCurrency(action.monthlySavingPounds)}
            </p>
            <p className="text-xs text-muted-foreground">/month</p>
          </div>
        )}
      </div>

      {/* Badges */}
      <div className="flex flex-wrap gap-1.5">
        {savingBadge && (
          <span className={cn("inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium", savingBadge.className)}>
            {savingBadge.label}
          </span>
        )}
        {action.effort && (
          <span className={cn("inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium", getEffortBadge(action.effort).className)}>
            {getEffortBadge(action.effort).label}
          </span>
        )}
        {action.confidence && (
          <span className={cn("inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium", getConfidenceBadge(action.confidence).className)}>
            {getConfidenceBadge(action.confidence).label}
          </span>
        )}
        {action.urgency && (
          <span className={cn("inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium", getUrgencyBadge(action.urgency).className)}>
            {getUrgencyBadge(action.urgency).label}
          </span>
        )}
        {action.safetyRisk && action.safetyRisk !== "none" && (
          <span className={cn("inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium", getSafetyRiskBadge(action.safetyRisk).className)}>
            {getSafetyRiskBadge(action.safetyRisk).label}
          </span>
        )}
      </div>

      {/* What detected / Why it matters */}
      {(action.whatDetected || action.whyItMatters) && (
        <div className="space-y-2 text-sm">
          {action.whatDetected && (
            <div>
              <p className="font-medium text-foreground text-xs uppercase tracking-wide mb-0.5">What we detected</p>
              <p className="text-muted-foreground">{action.whatDetected}</p>
            </div>
          )}
          {action.whyItMatters && (
            <div>
              <p className="font-medium text-foreground text-xs uppercase tracking-wide mb-0.5">Why it matters</p>
              <p className="text-muted-foreground">{action.whyItMatters}</p>
            </div>
          )}
        </div>
      )}

      {/* Caveats */}
      {action.eligibilityCaveat && (
        <div className="rounded-lg bg-purple-50 dark:bg-purple-950/20 p-3">
          <p className="text-xs text-purple-800 dark:text-purple-300">
            {action.eligibilityCaveat}
          </p>
        </div>
      )}
      {action.safetyCaveat && (
        <div className="rounded-lg bg-amber-50 dark:bg-amber-950/20 p-3">
          <p className="text-xs text-amber-800 dark:text-amber-300">
            {action.safetyCaveat}
          </p>
        </div>
      )}

      {/* Next step */}
      {action.nextStep && (
        <div className="rounded-lg bg-muted p-3">
          <p className="text-xs font-medium text-foreground mb-0.5">Next step</p>
          <p className="text-sm text-muted-foreground">{action.nextStep}</p>
        </div>
      )}

      {/* Expandable steps */}
      {action.steps && action.steps.length > 0 && (
        <div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setExpanded(!expanded)}
            className="text-sm gap-1.5"
          >
            {expanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
            {expanded ? "Hide steps" : action.ctaLabel || "View steps"}
          </Button>
          {expanded && (
            <ol className="mt-3 space-y-2 pl-4">
              {action.steps.map((step, i) => (
                <li key={i} className="flex gap-2 text-sm text-muted-foreground">
                  <span className="shrink-0 font-medium text-foreground">{i + 1}.</span>
                  {step}
                </li>
              ))}
            </ol>
          )}
        </div>
      )}

      {/* Call script */}
      {action.callScript && (
        <div className="rounded-lg border border-border bg-muted/50 p-4">
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs font-medium text-foreground">Suggested call script</p>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCopyScript}
              className="h-7 text-xs gap-1"
            >
              {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
              {copied ? "Copied" : "Copy"}
            </Button>
          </div>
          <blockquote className="text-sm italic text-muted-foreground border-l-2 border-primary/30 pl-3">
            {action.callScript}
          </blockquote>
        </div>
      )}
    </div>
  );
}
