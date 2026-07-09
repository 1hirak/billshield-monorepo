import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, FileText, Loader2, AlertCircle, Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ErrorBanner } from "@/components/ui/error-banner";
import { uploadBill, confirmBillFields } from "@/api/endpoints";
import { getHouseholdId, setBillId } from "@/utils/storage";
import { cn } from "@/lib/utils";

const ACCEPTED = ["application/pdf", "image/png", "image/jpeg", "image/jpg"];
const MAX_SIZE = 10 * 1024 * 1024;

function createDemoPdfBlob(): File {
  const header = "%PDF-1.4\n% BillShield MVP — demo bill data\n";
  return new File([header], "billshield-demo-energy-bill.pdf", { type: "application/pdf" });
}

export default function BillUploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [skipping, setSkipping] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const householdId = getHouseholdId();

  if (!householdId) {
    navigate("/onboarding");
    return null;
  }

  const validateFile = (f: File): string | null => {
    if (!ACCEPTED.includes(f.type)) return "Unsupported file type. Please upload PDF, PNG, or JPG.";
    if (f.size > MAX_SIZE) return "File too large. Maximum size is 10 MB.";
    return null;
  };

  const handleFile = (f: File) => {
    const err = validateFile(f);
    if (err) {
      setError(err);
      return;
    }
    setError(null);
    setFile(f);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const result = await uploadBill({
        householdId,
        billType: "energy",
        file,
      });
      setBillId(result.billId);
      navigate(`/review/${result.billId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleSkip = async () => {
    setSkipping(true);
    setError(null);
    try {
      const demoFile = createDemoPdfBlob();
      const uploadResult = await uploadBill({
        householdId,
        billType: "energy",
        file: demoFile,
      });
      setBillId(uploadResult.billId);

      await confirmBillFields(uploadResult.billId, {
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
      });

      navigate("/dashboard");
    } catch {
      navigate("/dashboard");
    } finally {
      setSkipping(false);
    }
  };

  return (
    <div className="space-y-6 max-w-xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Upload your energy bill</h1>
        <p className="text-sm text-muted-foreground mt-1">
          We will extract the key details so you can check for savings.
        </p>
      </div>

      {error && <ErrorBanner message={error} />}

      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={cn(
          "relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-12 transition-colors cursor-pointer",
          dragOver
            ? "border-primary bg-primary/5"
            : "border-border bg-card hover:border-primary/50"
        )}
        onClick={() => document.getElementById("file-input")?.click()}
      >
        <input
          id="file-input"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleFile(f);
          }}
        />
        <Upload className="h-10 w-10 text-muted-foreground mb-4" />
        <p className="text-sm font-medium text-foreground">
          Drag and drop your bill here, or click to browse
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          PDF, PNG, or JPG up to 10 MB
        </p>
      </div>

      {file && (
        <div className="flex items-center gap-3 rounded-xl border border-border bg-card p-4">
          <FileText className="h-8 w-8 text-primary" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-foreground truncate">{file.name}</p>
            <p className="text-xs text-muted-foreground">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
          <Button onClick={handleUpload} disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Scanning...
              </>
            ) : (
              "Scan bill"
            )}
          </Button>
        </div>
      )}

      <div className="flex flex-col items-center gap-3">
        <div className="flex items-start gap-2 rounded-lg bg-blue-50 dark:bg-blue-950/20 p-3 w-full">
          <Info className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
          <p className="text-xs text-blue-800 dark:text-blue-300">
            This is an MVP demo — OCR is simulated. Skip below to use demo bill data and explore the full dashboard immediately.
          </p>
        </div>
        <Button
          variant="outline"
          onClick={handleSkip}
          disabled={skipping}
          className="w-full"
        >
          {skipping && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {skipping ? "Setting up demo bill..." : "Skip for now — explore the dashboard"}
        </Button>
      </div>

      <div className="flex items-start gap-2 rounded-lg bg-muted p-3">
        <AlertCircle className="h-4 w-4 text-muted-foreground shrink-0 mt-0.5" />
        <p className="text-xs text-muted-foreground">
          Your bill is processed securely. You can delete uploaded data at any time from Settings.
        </p>
      </div>
    </div>
  );
}
