import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2, Trash2, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { ErrorBanner } from "@/components/ui/error-banner";
import { getHousehold, updateHousehold, deleteBillData } from "@/api/endpoints";
import { getHouseholdId, getBillId, removeBillId } from "@/utils/storage";
import type { Household } from "@/api/types";
import { DashboardSkeleton } from "@/components/ui/loading-skeleton";

export default function SettingsPage() {
  const navigate = useNavigate();
  const householdId = getHouseholdId();
  const billId = getBillId();

  const [household, setHousehold] = useState<Household | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [deleteSuccess, setDeleteSuccess] = useState(false);

  const [notifications, setNotifications] = useState({
    billReminders: true,
    weeklyTips: false,
    supportAlerts: true,
  });

  useEffect(() => {
    if (!householdId) {
      navigate("/onboarding");
      return;
    }
    getHousehold(householdId)
      .then(setHousehold)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [householdId, navigate]);

  const handleSave = async () => {
    if (!householdId || !household) return;
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const updated = await updateHousehold(householdId, {
        energyProvider: household.energyProvider,
        paymentMethod: household.paymentMethod,
        monthlyRentOrMortgage: household.monthlyRentOrMortgage,
        monthlyFoodCost: household.monthlyFoodCost,
        monthlyTransportCost: household.monthlyTransportCost,
        monthlyCouncilTax: household.monthlyCouncilTax,
        monthlyBroadbandMobileCost: household.monthlyBroadbandMobileCost,
        monthlyWaterCost: household.monthlyWaterCost,
      });
      setHousehold(updated);
      setSuccess("Settings saved.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteBill = async () => {
    if (!billId) return;
    setDeleting(true);
    setError(null);
    try {
      await deleteBillData(billId);
      removeBillId();
      setDeleteSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  if (!householdId) return null;
  if (loading) return <DashboardSkeleton />;

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">Settings</h1>

      {error && <ErrorBanner message={error} />}
      {success && (
        <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50/50 dark:border-emerald-800 dark:bg-emerald-950/20 p-4">
          <Check className="h-4 w-4 text-emerald-600" />
          <p className="text-sm text-emerald-800 dark:text-emerald-300">{success}</p>
        </div>
      )}

      {/* Household profile */}
      {household && (
        <div className="rounded-2xl border border-border bg-card p-6 space-y-5">
          <h2 className="text-base font-semibold">Household profile</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label>Energy provider</Label>
              <Input
                value={household.energyProvider}
                onChange={(e) => setHousehold({ ...household, energyProvider: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Payment method</Label>
              <Input value={household.paymentMethod.replace(/_/g, " ")} disabled />
            </div>
            {[
              { key: "monthlyRentOrMortgage", label: "Rent / mortgage (\u00A3/month)" },
              { key: "monthlyFoodCost", label: "Food (\u00A3/month)" },
              { key: "monthlyTransportCost", label: "Transport (\u00A3/month)" },
              { key: "monthlyCouncilTax", label: "Council tax (\u00A3/month)" },
              { key: "monthlyBroadbandMobileCost", label: "Broadband / mobile (\u00A3/month)" },
              { key: "monthlyWaterCost", label: "Water (\u00A3/month)" },
            ].map((field) => (
              <div key={field.key} className="space-y-2">
                <Label>{field.label}</Label>
                <Input
                  type="number"
                  value={household[field.key as keyof Household] as number}
                  onChange={(e) =>
                    setHousehold({ ...household, [field.key]: Number(e.target.value) })
                  }
                />
              </div>
            ))}
          </div>
          <Button onClick={handleSave} disabled={saving}>
            {saving && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Save changes
          </Button>
        </div>
      )}

      {/* Notifications */}
      <div className="rounded-2xl border border-border bg-card p-6 space-y-4">
        <h2 className="text-base font-semibold">Notification preferences</h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <Label className="text-sm">Bill reminders</Label>
            <Switch
              checked={notifications.billReminders}
              onCheckedChange={(v) => setNotifications({ ...notifications, billReminders: v })}
            />
          </div>
          <div className="flex items-center justify-between">
            <Label className="text-sm">Weekly tips</Label>
            <Switch
              checked={notifications.weeklyTips}
              onCheckedChange={(v) => setNotifications({ ...notifications, weeklyTips: v })}
            />
          </div>
          <div className="flex items-center justify-between">
            <Label className="text-sm">Support alerts</Label>
            <Switch
              checked={notifications.supportAlerts}
              onCheckedChange={(v) => setNotifications({ ...notifications, supportAlerts: v })}
            />
          </div>
        </div>
      </div>

      {/* Data privacy */}
      <div className="rounded-2xl border border-border bg-card p-6 space-y-4">
        <h2 className="text-base font-semibold">Data and privacy</h2>
        <p className="text-sm text-muted-foreground">
          Your bill data is used to calculate your household support recommendations. You can delete uploaded bill data at any time.
        </p>

        {deleteSuccess ? (
          <div className="flex items-center gap-2 text-sm text-emerald-700 dark:text-emerald-400">
            <Check className="h-4 w-4" />
            Bill data deleted successfully.
          </div>
        ) : billId ? (
          <Button
            variant="destructive"
            onClick={handleDeleteBill}
            disabled={deleting}
          >
            {deleting ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Trash2 className="mr-2 h-4 w-4" />
            )}
            Delete uploaded bill data
          </Button>
        ) : (
          <p className="text-sm text-muted-foreground italic">No bill data uploaded.</p>
        )}
      </div>
    </div>
  );
}
