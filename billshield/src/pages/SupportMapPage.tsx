import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { MapPin, Phone, ExternalLink, Clock, Navigation } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { ErrorBanner } from "@/components/ui/error-banner";
import { EmptyState } from "@/components/ui/empty-state";
import { CardSkeleton } from "@/components/ui/loading-skeleton";
import { getSupportServices, getHousehold } from "@/api/endpoints";
import { getHouseholdId } from "@/utils/storage";
import type { SupportServicesResponse, SupportService } from "@/api/types";
import { cn } from "@/lib/utils";

const FILTER_OPTIONS = [
  { value: "warm_space", label: "Warm spaces" },
  { value: "food_bank", label: "Food support" },
  { value: "citizens_advice", label: "Citizens Advice" },
  { value: "library", label: "Libraries" },
  { value: "council_emergency_support", label: "Council support" },
  { value: "debt_advice", label: "Debt advice" },
  { value: "energy_help", label: "Energy help" },
];

const STATUS_STYLES: Record<string, { label: string; className: string }> = {
  open_now: { label: "Open now", className: "text-emerald-700 dark:text-emerald-400" },
  closed_now: { label: "Closed", className: "text-red-600 dark:text-red-400" },
  opens_today: { label: "Opens today", className: "text-amber-700 dark:text-amber-400" },
  appointment_only: { label: "Appointment only", className: "text-blue-700 dark:text-blue-400" },
};

export default function SupportMapPage() {
  const navigate = useNavigate();
  const householdId = getHouseholdId();
  const [postcode, setPostcode] = useState("");
  const [filters, setFilters] = useState<string[]>([]);
  const [data, setData] = useState<SupportServicesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!householdId) {
      navigate("/onboarding");
      return;
    }
    getHousehold(householdId)
      .then((h) => setPostcode(h.postcode))
      .catch(() => {});
  }, [householdId, navigate]);

  useEffect(() => {
    if (!postcode) return;
    setLoading(true);
    setError(null);
    getSupportServices({ postcode, filters: filters.length > 0 ? filters : undefined })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [postcode, filters]);

  if (!householdId) return null;

  const toggleFilter = (value: string) => {
    setFilters((prev) =>
      prev.includes(value) ? prev.filter((f) => f !== value) : [...prev, value]
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Local Support</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Find practical support services near you.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Filters */}
        <div className="space-y-4">
          <div className="rounded-2xl border border-border bg-card p-5 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="postcode">Postcode</Label>
              <Input
                id="postcode"
                value={postcode}
                onChange={(e) => setPostcode(e.target.value)}
                placeholder="e.g. BS1 4ST"
              />
            </div>

            <div className="space-y-3">
              <Label className="text-sm font-medium">Filter services</Label>
              {FILTER_OPTIONS.map((opt) => (
                <div key={opt.value} className="flex items-center gap-2">
                  <Checkbox
                    id={opt.value}
                    checked={filters.includes(opt.value)}
                    onCheckedChange={() => toggleFilter(opt.value)}
                  />
                  <Label htmlFor={opt.value} className="text-sm font-normal cursor-pointer">
                    {opt.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>

          {/* Service pin grid */}
          {data && data.services.length > 0 && (
            <div className="rounded-2xl border border-border bg-card p-5 space-y-3">
              <div className="flex items-center gap-2 text-muted-foreground">
                <MapPin className="h-4 w-4" />
                <span className="text-sm font-medium">{data.mapPlaceholder.centerLabel}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 max-h-64 overflow-y-auto">
                {data.services.map((s) => (
                  <div
                    key={s.id}
                    className="flex items-start gap-2 rounded-lg bg-muted/50 p-2.5 cursor-pointer hover:bg-muted transition-colors"
                    onClick={() => {
                      const el = document.getElementById(`service-${s.id}`);
                      el?.scrollIntoView({ behavior: "smooth" });
                      el?.classList.add("ring-2", "ring-primary");
                      setTimeout(() => el?.classList.remove("ring-2", "ring-primary"), 2000);
                    }}
                  >
                    <MapPin className="h-3.5 w-3.5 text-primary shrink-0 mt-0.5" />
                    <div className="min-w-0">
                      <p className="text-xs font-medium text-foreground truncate">{s.name}</p>
                      <p className="text-xs text-muted-foreground">{s.distanceMiles}mi</p>
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-xs text-muted-foreground text-center">
                Click a pin to scroll to its details
              </p>
            </div>
          )}
        </div>

        {/* Right: Results */}
        <div className="lg:col-span-2 space-y-4">
          {error && <ErrorBanner message={error} />}
          {loading && (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <CardSkeleton key={i} />
              ))}
            </div>
          )}
          {!loading && data && data.services.length === 0 && (
            <EmptyState
              title="No services found"
              description="None found in your area with the current filters. Try broadening your search."
            />
          )}
          {!loading &&
            data &&
            data.services.map((service) => (
              <ServiceCard key={service.id} service={service} />
            ))}
          {!loading && data && data.services.length > 0 && (
            <p className="text-xs text-muted-foreground text-center pt-4 border-t border-border">
              Mock data — 20+ illustrative services. Real addresses and locations will be available in a future release.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

function ServiceCard({ service }: { service: SupportService }) {
  const statusStyle = STATUS_STYLES[service.openingStatus] || {
    label: service.openingStatus,
    className: "text-muted-foreground",
  };

  const address = [service.addressLine1, service.town].filter(Boolean).join(", ");
  const mapsUrl = address
    ? `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(address)}`
    : "#";

  return (
    <div
      id={`service-${service.id}`}
      className="rounded-2xl border border-border bg-card p-5 space-y-3 scroll-mt-20 transition-shadow"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="text-sm font-semibold text-foreground">{service.name}</h3>
          <p className="text-xs text-muted-foreground capitalize">
            {service.type.replace(/_/g, " ")}
          </p>
        </div>
        <div className="text-right shrink-0">
          <p className="text-sm font-medium text-foreground">{service.distanceMiles} miles</p>
          <p
            className={cn(
              "text-xs font-medium flex items-center gap-1 justify-end",
              statusStyle.className
            )}
          >
            <Clock className="h-3 w-3" />
            {statusStyle.label}
          </p>
        </div>
      </div>

      <p className="text-sm text-muted-foreground">{service.shortDescription}</p>

      <div className="flex items-start gap-2 rounded-lg bg-blue-50 dark:bg-blue-950/20 p-3">
        <MapPin className="h-4 w-4 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
        <div className="min-w-0">
          <p className="text-sm font-medium text-blue-900 dark:text-blue-200">{address}</p>
          {service.phone && (
            <p className="text-xs text-blue-700 dark:text-blue-300 flex items-center gap-1 mt-0.5">
              <Phone className="h-3 w-3" />
              {service.phone}
            </p>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2 pt-1">
        {service.website && (
          <Button variant="outline" size="sm" asChild>
            <a href={service.website} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="h-3.5 w-3.5 mr-1" />
              Website
            </a>
          </Button>
        )}
        <Button variant="outline" size="sm" asChild>
          <a href={mapsUrl} target="_blank" rel="noopener noreferrer">
            <Navigation className="h-3.5 w-3.5 mr-1" />
            Get directions
          </a>
        </Button>
      </div>
    </div>
  );
}
