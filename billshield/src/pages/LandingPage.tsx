import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Shield, ScanLine, TrendingDown, HeartHandshake, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { createHousehold, uploadBill, confirmBillFields } from "@/api/endpoints";
import { setHouseholdId, setBillId } from "@/utils/storage";
import { useState } from "react";

const DEMO_HOUSEHOLD = {
  postcode: "BS1 4ST",
  householdType: "family_with_children" as const,
  incomeBand: "15k_25k" as const,
  energyProvider: "BrightSpark Energy",
  paymentMethod: "direct_debit" as const,
  monthlyRentOrMortgage: 850,
  monthlyFoodCost: 360,
  monthlyTransportCost: 155,
  monthlyCouncilTax: 168,
  monthlyBroadbandMobileCost: 52,
  monthlyWaterCost: 39,
  receivesQualifyingBenefits: true,
  hasChildren: true,
};

const DEMO_BILL_FIELDS = {
  supplier: "BrightSpark Energy",
  tariffName: "Standard Variable Direct",
  monthlyDirectDebit: 142,
  electricityUnitRatePencePerKwh: 27.34,
  electricityStandingChargePencePerDay: 60.12,
  gasUnitRatePencePerKwh: 7.62,
  gasStandingChargePencePerDay: 31.44,
  annualElectricityUsageKwh: 2900,
  annualGasUsageKwh: 11000,
  paymentMethod: "direct_debit",
  tariffType: "standard_variable",
};

export default function LandingPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleDemo = async () => {
    setLoading(true);
    try {
      const household = await createHousehold(DEMO_HOUSEHOLD);
      setHouseholdId(household.id);

      const pdfBlob = new File(
        ["%PDF-1.4\n% Demo bill for BillShield UK\n"],
        "demo-energy-bill.pdf",
        { type: "application/pdf" }
      );

      const uploadResult = await uploadBill({
        householdId: household.id,
        billType: "energy",
        file: pdfBlob,
      });
      setBillId(uploadResult.billId);

      await confirmBillFields(uploadResult.billId, DEMO_BILL_FIELDS);

      navigate("/dashboard");
    } catch {
      setLoading(false);
      toast.error("Demo setup failed — try 'Start household check' instead.");
    }
  };

  return (
    <div className="min-h-svh flex flex-col bg-background">
      <header className="flex items-center justify-between px-6 py-4 max-w-5xl mx-auto w-full">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6 text-primary" />
          <span className="font-semibold text-lg tracking-tight">BillShield UK</span>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-4 pb-16">
        <div className="max-w-2xl text-center space-y-6">
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-foreground text-balance">
            Understand your bills. Find savings. Get support.
          </h1>
          <p className="text-lg text-muted-foreground max-w-lg mx-auto">
            BillShield helps turn confusing household bills into clear monthly actions. No shame, no hype, just practical steps.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <Button
              size="lg"
              onClick={() => navigate("/onboarding")}
              className="w-full sm:w-auto"
            >
              Start household check
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={handleDemo}
              disabled={loading}
              className="w-full sm:w-auto"
            >
              {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              View demo dashboard
            </Button>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl w-full">
          <FeatureCard
            icon={<ScanLine className="h-6 w-6" />}
            title="Scan your energy bill"
            description="Upload a bill and we extract the key details for you to check."
          />
          <FeatureCard
            icon={<TrendingDown className="h-6 w-6" />}
            title="Forecast monthly pressure"
            description="See your full household costs and where pressure is building."
          />
          <FeatureCard
            icon={<HeartHandshake className="h-6 w-6" />}
            title="Find savings and support"
            description="Get ranked actions and local services tailored to your situation."
          />
        </div>
      </main>

      <footer className="py-6 text-center text-xs text-muted-foreground">
        Your data stays private. Delete uploaded bill data at any time.
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-border bg-card p-6 text-center space-y-3">
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-primary/5 text-primary">
        {icon}
      </div>
      <h3 className="text-sm font-semibold text-foreground">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}
