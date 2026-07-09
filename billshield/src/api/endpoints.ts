import { request, uploadRequest } from "./client";
import type {
  BillConfirmResponse,
  BillExtraction,
  BillUploadResponse,
  DashboardData,
  HealthResponse,
  Household,
  HouseholdPayload,
  ScenarioPayload,
  ScenarioResult,
  SeedResponse,
  SupportServicesResponse,
  ThirtyDayPlan,
} from "./types";

export function healthCheck() {
  return request<HealthResponse>("/health");
}

export function seedDemoData() {
  return request<SeedResponse>("/dev/seed", { method: "POST" });
}

export function resetDemoData() {
  return request<{ message: string }>("/dev/reset", { method: "POST" });
}

export function createHousehold(payload: HouseholdPayload) {
  return request<Household>("/households", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getHousehold(householdId: string) {
  return request<Household>(`/households/${householdId}`);
}

export function updateHousehold(householdId: string, payload: Partial<HouseholdPayload>) {
  return request<Household>(`/households/${householdId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function uploadBill({
  householdId,
  billType,
  file,
}: {
  householdId: string;
  billType: string;
  file: File;
}) {
  const formData = new FormData();
  formData.append("householdId", householdId);
  formData.append("billType", billType);
  formData.append("file", file);
  return uploadRequest<BillUploadResponse>("/bills/upload", formData);
}

export function getBillExtraction(billId: string) {
  return request<BillExtraction>(`/bills/${billId}`);
}

export function confirmBillFields(billId: string, payload: Record<string, unknown>) {
  return request<BillConfirmResponse>(`/bills/${billId}/confirm`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function getDashboard(householdId: string) {
  return request<DashboardData>(`/dashboard/${householdId}`);
}

export function getRecommendations(householdId: string) {
  return request<{ recommendations: DashboardData["topRecommendedActions"] }>(
    `/recommendations/${householdId}`
  );
}

export function simulateScenario(payload: ScenarioPayload) {
  return request<ScenarioResult>("/scenarios/simulate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getSupportServices({
  postcode,
  filters,
  radiusMiles = 5,
}: {
  postcode: string;
  filters?: string[];
  radiusMiles?: number;
}) {
  const params = new URLSearchParams();
  params.set("postcode", postcode);
  if (filters && filters.length > 0) {
    params.set("filters", filters.join(","));
  }
  params.set("radiusMiles", String(radiusMiles));
  return request<SupportServicesResponse>(`/support-services?${params.toString()}`);
}

export function generateThirtyDayPlan(payload: {
  householdId: string;
  includeCompletedActions?: boolean;
  tone?: string;
}) {
  return request<ThirtyDayPlan>("/plans/30-day", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function deleteBillData(billId: string) {
  return request<{ billId: string; status: string; message: string }>(
    `/bills/${billId}/data`,
    { method: "DELETE" }
  );
}
