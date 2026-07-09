import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import userEvent from "@testing-library/user-event";

import LandingPage from "@/pages/LandingPage";
import DashboardPage from "@/pages/DashboardPage";
import OnboardingPage from "@/pages/OnboardingPage";

const originalFetch = globalThis.fetch;

function mockFetchOnce(data: unknown, ok = true, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValueOnce({
    ok,
    status,
    json: async () => data,
  }) as unknown as typeof fetch;
}

function mockFetch(data: unknown, ok = true, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    json: async () => data,
  }) as unknown as typeof fetch;
}

beforeEach(() => {
  localStorage.clear();
});

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe("LandingPage", () => {
  it("renders hero headline", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByText("Understand your bills. Find savings. Get support.")).toBeDefined();
  });

  it("renders Start household check button", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByText("Start household check")).toBeDefined();
  });

  it("renders View demo dashboard button", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByText("View demo dashboard")).toBeDefined();
  });

  it("renders three feature cards", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByText("Scan your energy bill")).toBeDefined();
    expect(screen.getByText("Forecast monthly pressure")).toBeDefined();
    expect(screen.getByText("Find savings and support")).toBeDefined();
  });

  it("calls seed API on demo button click", async () => {
    mockFetchOnce({ householdId: "h-123", billId: "b-456", message: "ok" });
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    const btn = screen.getByText("View demo dashboard");
    await userEvent.click(btn);
    await waitFor(() => {
      expect(globalThis.fetch).toHaveBeenCalled();
    });
  });

  it("renders footer text", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByText("Your data stays private. Delete uploaded bill data at any time.")).toBeDefined();
  });
});

describe("OnboardingPage", () => {
  it("renders step 1 fields", () => {
    render(
      <MemoryRouter>
        <OnboardingPage />
      </MemoryRouter>
    );
    expect(screen.getByText("Set up your household")).toBeDefined();
    expect(screen.getByLabelText("Postcode")).toBeDefined();
    expect(screen.getByLabelText("Energy provider")).toBeDefined();
  });

  it("shows step indicator bar", () => {
    render(
      <MemoryRouter>
        <OnboardingPage />
      </MemoryRouter>
    );
    const indicators = document.querySelectorAll(".flex.items-center.gap-2 > div");
    expect(indicators.length).toBe(3);
  });

  it("validates postcode before allowing next from step 1", async () => {
    render(
      <MemoryRouter>
        <OnboardingPage />
      </MemoryRouter>
    );
    const nextBtn = screen.getByText("Next");
    await userEvent.click(nextBtn);
    await waitFor(() => {
      expect(screen.getByText("Please enter your postcode.")).toBeDefined();
    });
  });

  it("validates invalid postcode format", async () => {
    render(
      <MemoryRouter>
        <OnboardingPage />
      </MemoryRouter>
    );
    await userEvent.type(screen.getByLabelText("Postcode"), "INVALID");
    await userEvent.type(screen.getByLabelText("Energy provider"), "Test Energy");
    const nextBtn = screen.getByText("Next");
    await userEvent.click(nextBtn);
    await waitFor(() => {
      expect(screen.getByText("Please enter a valid UK postcode (e.g. BS1 4ST).")).toBeDefined();
    });
  });

  it("allows advancing to step 2 with valid data", async () => {
    render(
      <MemoryRouter>
        <OnboardingPage />
      </MemoryRouter>
    );
    await userEvent.type(screen.getByLabelText("Postcode"), "BS1 4ST");
    await userEvent.type(screen.getByLabelText("Energy provider"), "BrightSpark");
    await userEvent.click(screen.getByText("Next"));
    await waitFor(() => {
      expect(screen.getByText("Monthly costs")).toBeDefined();
    });
  });

  it("validates cost fields on step 2", async () => {
    render(
      <MemoryRouter>
        <OnboardingPage />
      </MemoryRouter>
    );
    await userEvent.type(screen.getByLabelText("Postcode"), "BS1 4ST");
    await userEvent.type(screen.getByLabelText("Energy provider"), "BrightSpark");
    await userEvent.click(screen.getByText("Next"));
    await waitFor(() => screen.getByText("Monthly costs"));

    const foodInput = screen.getByLabelText("Food (£/month)");
    await userEvent.clear(foodInput);
    await userEvent.type(foodInput, "99999");
    await userEvent.click(screen.getByText("Next"));
    await waitFor(() => {
      expect(screen.getByText("Food seems too high. Please check and try again.")).toBeDefined();
    });
  });
});

describe("DashboardPage", () => {
  beforeEach(() => {
    localStorage.setItem("billshield_household_id", "h-test-123");
  });

  it("shows loading skeleton initially", () => {
    mockFetch(new Promise(() => {}));
    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <DashboardPage />
      </MemoryRouter>
    );
    // DashboardSkeleton renders skeleton placeholders; dashboard heading is not in loading state
    const skeletons = document.querySelectorAll(".animate-pulse");
    expect(skeletons.length).toBeGreaterThan(0);
  });

  it("renders no-bill state when billBreakdown is null", async () => {
    mockFetch({
      householdId: "h-1",
      summary: { monthlyHouseholdPressure: 1742, estimatedDisposableBuffer: 126, energyBillRisk: "medium_high", potentialMonthlySavings: 0 },
      monthlyPressureForecast: [],
      billBreakdown: null,
      topRecommendedActions: [{ id: "upload", rank: 1, engineType: "onboarding", title: "Upload your first energy bill", description: "...", nextStep: "Go to bill upload", ctaLabel: "Upload bill" }],
      otherRecommendedActions: [],
      insights: [],
    });
    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <DashboardPage />
      </MemoryRouter>
    );
    await waitFor(() => {
      const matches = screen.getAllByText("Upload your first energy bill");
      expect(matches.length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders full dashboard with summary cards", async () => {
    mockFetch({
      householdId: "h-1",
      summary: { monthlyHouseholdPressure: 1742, estimatedDisposableBuffer: 126, energyBillRisk: "medium_high", potentialMonthlySavings: 94 },
      monthlyPressureForecast: [],
      billBreakdown: {
        electricityUsageCostMonthly: 66,
        gasUsageCostMonthly: 70,
        standingChargesMonthly: 28,
        monthlyDirectDebit: 142,
        estimatedAnnualCost: 1440,
        currentTariffStatus: "standard_variable",
        standingChargeInsight: "Standing charges are fixed.",
        avoidableCostMonthly: 136,
        unavoidableStandingChargeMonthly: 28,
      },
      topRecommendedActions: [{ id: "r1", rank: 1, engineType: "tariff_check", title: "Check your tariff", description: "...", savingLabel: "potential_saving", effort: "low", confidence: "medium", urgency: "medium", safetyRisk: "none", nextStep: "Compare tariffs" }],
      otherRecommendedActions: [],
      insights: [{ type: "info", title: "Tip", body: "Helpful insight" }],
    });
    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <DashboardPage />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByText("Monthly pressure")).toBeDefined();
      expect(screen.getByText("Bill Breakdown")).toBeDefined();
      expect(screen.getByText("Check your tariff")).toBeDefined();
    });
  });

  it("shows error banner on fetch failure", async () => {
    mockFetch({ error: { message: "Network error" } }, false, 500);
    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <DashboardPage />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByText("Network error")).toBeDefined();
    });
  });
});
