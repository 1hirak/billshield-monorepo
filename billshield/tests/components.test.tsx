import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import userEvent from "@testing-library/user-event";
import { SummaryCard } from "@/components/dashboard/SummaryCard";
import { BillBreakdownCard } from "@/components/dashboard/BillBreakdownCard";
import { RecommendationCard } from "@/components/recommendations/RecommendationCard";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import type { BillBreakdown as BillBreakdownType, RecommendedAction } from "@/api/types";

const mockBreakdown: BillBreakdownType = {
  electricityUsageCostMonthly: 66,
  gasUsageCostMonthly: 70,
  standingChargesMonthly: 28,
  monthlyDirectDebit: 142,
  estimatedAnnualCost: 1440,
  currentTariffStatus: "standard_variable",
  standingChargeInsight: "Standing charges are fixed daily costs.",
  avoidableCostMonthly: 136,
  unavoidableStandingChargeMonthly: 28,
  insight: "Standing charges are fixed daily costs.",
};

const mockAction: RecommendedAction = {
  id: "rec-1",
  rank: 1,
  engineType: "direct_debit_health_check",
  title: "Request a Direct Debit review",
  description: "Your Direct Debit appears higher than your forecast usage.",
  whatDetected: "Your monthly Direct Debit is £142.",
  whyItMatters: "You may be building unnecessary credit.",
  monthlySavingPounds: 22,
  annualSavingPounds: 264,
  savingLabel: "cashflow_improvement",
  effort: "low",
  confidence: "high",
  urgency: "medium",
  safetyRisk: "none",
  eligibilityCaveat: null,
  safetyCaveat: null,
  nextStep: "Submit a meter reading, then ask your supplier to review.",
  steps: ["Step one", "Step two", "Step three"],
  callScript: "I want to review my Direct Debit.",
  ctaLabel: "View steps",
};

describe("SummaryCard", () => {
  it("renders title and value", () => {
    render(<SummaryCard title="Monthly Pressure" value="£1,742" />);
    expect(screen.getByText("Monthly Pressure")).toBeDefined();
    expect(screen.getByText("£1,742")).toBeDefined();
  });

  it("renders subtitle when provided", () => {
    render(<SummaryCard title="Test" value="100" subtitle="sub text" />);
    expect(screen.getByText("sub text")).toBeDefined();
  });

  it("does not render subtitle when not provided", () => {
    render(<SummaryCard title="Test" value="100" />);
    expect(screen.queryByText("sub text")).toBeNull();
  });

  it("applies success variant border", () => {
    render(<SummaryCard title="Test" value="100" variant="success" />);
    const el = screen.getByText("Test").parentElement?.parentElement;
    expect(el?.className).toContain("border-emerald");
  });

  it("applies danger variant border", () => {
    render(<SummaryCard title="Test" value="100" variant="danger" />);
    const el = screen.getByText("Test").parentElement?.parentElement;
    expect(el?.className).toContain("border-orange");
  });
});

describe("BillBreakdownCard", () => {
  it("renders all cost line items", () => {
    render(<BillBreakdownCard data={mockBreakdown} />);
    expect(screen.getByText("Bill Breakdown")).toBeDefined();
    expect(screen.getByText("Electricity usage")).toBeDefined();
    expect(screen.getByText("Gas usage")).toBeDefined();
    expect(screen.getByText("Standing charges")).toBeDefined();
    expect(screen.getByText("Monthly Direct Debit")).toBeDefined();
  });

  it("shows tariff status badge", () => {
    render(<BillBreakdownCard data={mockBreakdown} />);
    expect(screen.getByText("standard variable")).toBeDefined();
  });

  it("renders standing charge insight", () => {
    render(<BillBreakdownCard data={mockBreakdown} />);
    expect(screen.getByText("Standing charges are fixed daily costs.")).toBeDefined();
  });

  it("does not render insight when missing", () => {
    render(<BillBreakdownCard data={{ ...mockBreakdown, standingChargeInsight: "", insight: "" }} />);
    expect(screen.queryByText("Standing charges are fixed daily costs.")).toBeNull();
  });
});

describe("RecommendationCard", () => {
  it("renders title and description", () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={mockAction} />
      </MemoryRouter>
    );
    expect(screen.getByText("Request a Direct Debit review")).toBeDefined();
    expect(screen.getByText("Your Direct Debit appears higher than your forecast usage.")).toBeDefined();
  });

  it("shows rank badge when showRank is true", () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={mockAction} showRank={true} />
      </MemoryRouter>
    );
    expect(screen.getByText("1")).toBeDefined();
  });

  it("hides rank badge when showRank is false", () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={mockAction} showRank={false} />
      </MemoryRouter>
    );
    expect(screen.queryByText("1")).toBeNull();
  });

  it("shows saving amount when present", () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={mockAction} />
      </MemoryRouter>
    );
    expect(screen.getByText("/month")).toBeDefined();
  });

  it("shows saving label badge", () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={mockAction} />
      </MemoryRouter>
    );
    expect(screen.getByText("Cashflow improvement")).toBeDefined();
  });

  it("expands steps on click", async () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={mockAction} />
      </MemoryRouter>
    );
    const btn = screen.getByText("View steps");
    await userEvent.click(btn);
    expect(screen.getByText("Step one")).toBeDefined();
    expect(screen.getByText("Step two")).toBeDefined();
    expect(screen.getByText("Hide steps")).toBeDefined();
  });

  it("renders eligibility caveat when present", () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={{ ...mockAction, eligibilityCaveat: "Eligibility depends on council rules." }} />
      </MemoryRouter>
    );
    expect(screen.getByText("Eligibility depends on council rules.")).toBeDefined();
  });

  it("renders safety caveat when present", () => {
    render(
      <MemoryRouter>
        <RecommendationCard action={{ ...mockAction, safetyCaveat: "Keep rooms at a safe temperature." }} />
      </MemoryRouter>
    );
    expect(screen.getByText("Keep rooms at a safe temperature.")).toBeDefined();
  });
});

describe("ErrorBoundary", () => {
  function CrashComponent() {
    throw new Error("Test crash");
  }

  it("renders fallback UI on error", () => {
    render(
      <ErrorBoundary>
        <CrashComponent />
      </ErrorBoundary>
    );
    expect(screen.getByText("Something went wrong")).toBeDefined();
    expect(screen.getByText("Test crash")).toBeDefined();
  });

  it("renders children when no error", () => {
    render(
      <ErrorBoundary>
        <p>Everything is fine</p>
      </ErrorBoundary>
    );
    expect(screen.getByText("Everything is fine")).toBeDefined();
  });
});
