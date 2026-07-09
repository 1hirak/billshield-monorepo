import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ErrorBanner } from "@/components/ui/error-banner";
import { createHousehold } from "@/api/endpoints";
import { setHouseholdId } from "@/utils/storage";
import { Loader2, ChevronRight, ChevronLeft } from "lucide-react";
import type { HouseholdPayload, HouseholdType, IncomeBand, PaymentMethod } from "@/api/types";

const UK_POSTCODE_RE = /^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$/i;

const ENERGY_PROVIDERS = [
  "British Gas",
  "EDF Energy",
  "E.ON Next",
  "Octopus Energy",
  "OVO Energy",
  "Scottish Power",
  "SSE",
  "Shell Energy",
  "Bulb",
  "Utility Warehouse",
  "Ecotricity",
  "Good Energy",
  "Other (type yours)",
];

const HOUSEHOLD_TYPES: { value: HouseholdType; label: string }[] = [
  { value: "single_adult", label: "Single adult" },
  { value: "couple", label: "Couple" },
  { value: "family_with_children", label: "Family with children" },
  { value: "pensioner_household", label: "Pensioner household" },
  { value: "shared_household", label: "Shared household" },
];

const INCOME_BANDS: { value: IncomeBand; label: string }[] = [
  { value: "under_15k", label: "Under \u00A315k" },
  { value: "15k_25k", label: "\u00A315k\u2013\u00A325k" },
  { value: "25k_40k", label: "\u00A325k\u2013\u00A340k" },
  { value: "40k_60k", label: "\u00A340k\u2013\u00A360k" },
  { value: "60k_plus", label: "\u00A360k+" },
];

const PAYMENT_METHODS: { value: PaymentMethod; label: string }[] = [
  { value: "direct_debit", label: "Direct Debit" },
  { value: "prepayment_meter", label: "Prepayment meter" },
  { value: "standard_credit", label: "Standard credit" },
  { value: "unknown", label: "Unknown" },
];

const COST_FIELDS = [
  { key: "monthlyRentOrMortgage", label: "Rent or mortgage", max: 10000 },
  { key: "monthlyFoodCost", label: "Food", max: 5000 },
  { key: "monthlyTransportCost", label: "Transport", max: 5000 },
  { key: "monthlyCouncilTax", label: "Council tax", max: 2000 },
  { key: "monthlyBroadbandMobileCost", label: "Broadband / mobile", max: 1000 },
  { key: "monthlyWaterCost", label: "Water", max: 1000 },
];

const ELIGIBILITY_FIELDS = [
  { key: "receivesQualifyingBenefits", label: "Receives qualifying benefits" },
  { key: "hasChildren", label: "Has children" },
  { key: "hasPensioner", label: "Has pensioner in household" },
  { key: "hasHealthCondition", label: "Has health condition" },
  { key: "hasDisability", label: "Has disability" },
  { key: "isSingleAdult", label: "Single adult household" },
  { key: "waterMetered", label: "Water metered" },
];

export default function OnboardingPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stepError, setStepError] = useState<string | null>(null);

  const [form, setForm] = useState<HouseholdPayload>({
    postcode: "",
    householdType: "family_with_children",
    incomeBand: "15k_25k",
    energyProvider: "",
    paymentMethod: "direct_debit",
    monthlyRentOrMortgage: 0,
    monthlyFoodCost: 0,
    monthlyTransportCost: 0,
    monthlyCouncilTax: 0,
    monthlyBroadbandMobileCost: 0,
    monthlyWaterCost: 0,
    receivesQualifyingBenefits: false,
    hasChildren: false,
    hasPensioner: false,
    hasHealthCondition: false,
    hasDisability: false,
    isSingleAdult: false,
    bedrooms: 2,
    occupants: 2,
    waterMetered: false,
  });

  const update = (field: string, value: unknown) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setStepError(null);
  };

  const validateStep1 = (): boolean => {
    if (!form.postcode.trim()) {
      setStepError("Please enter your postcode.");
      return false;
    }
    if (!UK_POSTCODE_RE.test(form.postcode.trim())) {
      setStepError("Please enter a valid UK postcode (e.g. BS1 4ST).");
      return false;
    }
    if (!form.energyProvider.trim()) {
      setStepError("Please enter your energy provider.");
      return false;
    }
    return true;
  };

  const validateStep2 = (): boolean => {
    for (const field of COST_FIELDS) {
      const val = form[field.key as keyof HouseholdPayload] as number;
      if (isNaN(val) || val < 0) {
        setStepError(`${field.label} must be a positive number.`);
        return false;
      }
      if (val > field.max) {
        setStepError(`${field.label} seems too high. Please check and try again.`);
        return false;
      }
    }
    return true;
  };

  const handleNext = () => {
    if (step === 1 && !validateStep1()) return;
    if (step === 2 && !validateStep2()) return;
    setStep((s) => s + 1);
  };

  const handleSubmit = async () => {
    if (!validateStep1()) { setStep(1); return; }
    if (!validateStep2()) { setStep(2); return; }

    setLoading(true);
    setError(null);
    try {
      const result = await createHousehold(form);
      setHouseholdId(result.id);
      toast.success("Household profile created!");
      navigate("/upload");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Something went wrong";
      setError(msg);
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Set up your household</h1>
        <p className="text-sm text-muted-foreground mt-1">
          This helps estimate pressure and identify support routes. You can update it later.
        </p>
      </div>

      {/* Step indicators */}
      <div className="flex items-center gap-2">
        {[1, 2, 3].map((s) => (
          <div
            key={s}
            className={`h-2 flex-1 rounded-full transition-colors ${
              s <= step ? "bg-primary" : "bg-muted"
            }`}
          />
        ))}
      </div>

      {stepError && (
        <ErrorBanner message={stepError} />
      )}

      {error && <ErrorBanner message={error} />}

      <div className="rounded-2xl border border-border bg-card p-6 space-y-5">
        {step === 1 && (
          <>
            <h2 className="text-base font-semibold">Household basics</h2>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="postcode">Postcode</Label>
                <Input
                  id="postcode"
                  placeholder="e.g. BS1 4ST"
                  value={form.postcode}
                  onChange={(e) => update("postcode", e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="energyProvider">Energy provider</Label>
                {form.energyProvider === "Other (type yours)" ? (
                  <Input
                    id="energyProvider"
                    placeholder="Enter your provider name"
                    value=""
                    onChange={(e) => update("energyProvider", e.target.value || "Other (type yours)")}
                  />
                ) : (
                  <Select
                    value={form.energyProvider || undefined}
                    onValueChange={(v) => update("energyProvider", v)}
                  >
                    <SelectTrigger id="energyProvider">
                      <SelectValue placeholder="Select your provider..." />
                    </SelectTrigger>
                    <SelectContent>
                      {ENERGY_PROVIDERS.map((p) => (
                        <SelectItem key={p} value={p}>
                          {p}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              </div>
              <div className="space-y-2">
                <Label>Household type</Label>
                <div className="space-y-2">
                  {HOUSEHOLD_TYPES.map((ht) => (
                    <label key={ht.value} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="householdType"
                        checked={form.householdType === ht.value}
                        onChange={() => update("householdType", ht.value)}
                        className="accent-primary"
                      />
                      <span className="text-sm">{ht.label}</span>
                    </label>
                  ))}
                </div>
              </div>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label>Income band</Label>
                  <div className="space-y-2">
                    {INCOME_BANDS.map((ib) => (
                      <label key={ib.value} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="radio"
                          name="incomeBand"
                          checked={form.incomeBand === ib.value}
                          onChange={() => update("incomeBand", ib.value)}
                          className="accent-primary"
                        />
                        <span className="text-sm">{ib.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
                <div className="space-y-2">
                  <Label>Payment method</Label>
                  <div className="space-y-2">
                    {PAYMENT_METHODS.map((pm) => (
                      <label key={pm.value} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="radio"
                          name="paymentMethod"
                          checked={form.paymentMethod === pm.value}
                          onChange={() => update("paymentMethod", pm.value)}
                          className="accent-primary"
                        />
                        <span className="text-sm">{pm.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <h2 className="text-base font-semibold">Monthly costs</h2>
            <div className="grid gap-4 sm:grid-cols-2">
              {COST_FIELDS.map((field) => {
                const rawVal = form[field.key as keyof HouseholdPayload] as number;
                const displayVal = rawVal === 0 ? "" : rawVal;
                return (
                  <div key={field.key} className="space-y-2">
                    <Label htmlFor={field.key}>{field.label} ({"\u00A3"}/month)</Label>
                    <Input
                      id={field.key}
                      type="number"
                      min={0}
                      placeholder="0"
                      value={displayVal}
                      onChange={(e) => {
                        const v = e.target.value;
                        update(field.key, v === "" ? 0 : Math.max(0, Number(v)));
                      }}
                    />
                  </div>
                );
              })}
            </div>
          </>
        )}

        {step === 3 && (
          <>
            <h2 className="text-base font-semibold">Eligibility signals</h2>
            <p className="text-sm text-muted-foreground">
              These help identify benefits and support you may qualify for.
            </p>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-3">
                {ELIGIBILITY_FIELDS.map((field) => (
                  <div key={field.key} className="flex items-center gap-2">
                    <Checkbox
                      id={field.key}
                      checked={form[field.key as keyof HouseholdPayload] as boolean}
                      onCheckedChange={(val) => update(field.key, val)}
                    />
                    <Label htmlFor={field.key} className="text-sm font-normal cursor-pointer">
                      {field.label}
                    </Label>
                  </div>
                ))}
              </div>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="bedrooms">Bedrooms</Label>
                  <Input
                    id="bedrooms"
                    type="number"
                    min={1}
                    max={10}
                    value={form.bedrooms}
                    onChange={(e) => update("bedrooms", Number(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="occupants">Occupants</Label>
                  <Input
                    id="occupants"
                    type="number"
                    min={1}
                    max={20}
                    value={form.occupants}
                    onChange={(e) => update("occupants", Number(e.target.value))}
                  />
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={() => setStep((s) => s - 1)}
          disabled={step === 1}
        >
          <ChevronLeft className="h-4 w-4 mr-1" />
          Back
        </Button>

        {step < 3 ? (
          <Button onClick={handleNext}>
            Next
            <ChevronRight className="h-4 w-4 ml-1" />
          </Button>
        ) : (
          <Button onClick={handleSubmit} disabled={loading}>
            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Continue to bill upload
          </Button>
        )}
      </div>
    </div>
  );
}
