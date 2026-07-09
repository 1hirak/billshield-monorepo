import { AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface ErrorBannerProps {
  message: string;
  className?: string;
  onRetry?: () => void;
}

export function ErrorBanner({ message, className, onRetry }: ErrorBannerProps) {
  return (
    <div
      className={cn(
        "flex items-start gap-3 rounded-xl border border-destructive/30 bg-destructive/5 p-4",
        className
      )}
    >
      <AlertCircle className="h-5 w-5 text-destructive shrink-0 mt-0.5" />
      <div className="flex-1">
        <p className="text-sm text-foreground">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="mt-2 text-sm font-medium text-destructive hover:underline"
          >
            Try again
          </button>
        )}
      </div>
    </div>
  );
}
