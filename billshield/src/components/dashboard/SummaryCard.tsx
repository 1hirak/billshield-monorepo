import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface SummaryCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon?: ReactNode;
  variant?: "default" | "success" | "warning" | "danger";
  className?: string;
}

export function SummaryCard({
  title,
  value,
  subtitle,
  icon,
  variant = "default",
  className,
}: SummaryCardProps) {
  const variantStyles = {
    default: "border-border",
    success: "border-emerald-200 dark:border-emerald-800",
    warning: "border-amber-200 dark:border-amber-800",
    danger: "border-orange-200 dark:border-orange-800",
  };

  return (
    <div
      className={cn(
        "rounded-2xl border bg-card p-5 space-y-2",
        variantStyles[variant],
        className
      )}
    >
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        {icon && <div className="text-muted-foreground">{icon}</div>}
      </div>
      <p className="text-2xl font-bold tracking-tight text-foreground">{value}</p>
      {subtitle && (
        <p className="text-xs text-muted-foreground">{subtitle}</p>
      )}
    </div>
  );
}
