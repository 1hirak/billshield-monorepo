import { describe, it, expect } from "vitest";
import {
  getConfidenceBadge,
  getEffortBadge,
  getUrgencyBadge,
  getSafetyRiskBadge,
  getEnergyRiskStyle,
  getSavingLabelBadge,
} from "@/utils/badgeStyles";

describe("getConfidenceBadge", () => {
  it("returns emerald for high", () => {
    const b = getConfidenceBadge("high");
    expect(b.label).toBe("High confidence");
    expect(b.className).toContain("emerald");
  });
  it("returns amber for medium", () => {
    const b = getConfidenceBadge("medium");
    expect(b.label).toBe("Medium confidence");
    expect(b.className).toContain("amber");
  });
  it("returns orange for low", () => {
    const b = getConfidenceBadge("low");
    expect(b.label).toBe("Low confidence");
    expect(b.className).toContain("orange");
  });
  it("returns red for needs_review", () => {
    const b = getConfidenceBadge("needs_review");
    expect(b.label).toBe("Needs review");
    expect(b.className).toContain("red");
  });
  it("returns purple for only_if_eligible", () => {
    const b = getConfidenceBadge("only_if_eligible");
    expect(b.label).toBe("If eligible");
    expect(b.className).toContain("purple");
  });
  it("returns purple for only_if_tariff_eligible", () => {
    const b = getConfidenceBadge("only_if_tariff_eligible");
    expect(b.label).toBe("If tariff eligible");
    expect(b.className).toContain("purple");
  });
});

describe("getEffortBadge", () => {
  it("returns emerald for low", () => {
    const b = getEffortBadge("low");
    expect(b.label).toBe("Low effort");
    expect(b.className).toContain("emerald");
  });
  it("returns amber for medium", () => {
    const b = getEffortBadge("medium");
    expect(b.label).toBe("Medium effort");
  });
  it("returns orange for high", () => {
    const b = getEffortBadge("high");
    expect(b.label).toBe("High effort");
  });
});

describe("getUrgencyBadge", () => {
  it("returns slate for low", () => {
    expect(getUrgencyBadge("low").label).toBe("Low urgency");
  });
  it("returns amber for medium", () => {
    expect(getUrgencyBadge("medium").label).toBe("Medium urgency");
  });
  it("returns Urgent for high", () => {
    expect(getUrgencyBadge("high").label).toBe("Urgent");
  });
});

describe("getSafetyRiskBadge", () => {
  it("returns No risk for none", () => {
    expect(getSafetyRiskBadge("none").label).toBe("No risk");
  });
  it("returns Low risk for low", () => {
    expect(getSafetyRiskBadge("low").label).toBe("Low risk");
  });
  it("returns Medium risk for medium", () => {
    expect(getSafetyRiskBadge("medium").label).toBe("Medium risk");
  });
  it("returns High risk for high", () => {
    expect(getSafetyRiskBadge("high").label).toBe("High risk");
  });
});

describe("getEnergyRiskStyle", () => {
  it("returns emerald for low", () => {
    expect(getEnergyRiskStyle("low").label).toBe("Low");
    expect(getEnergyRiskStyle("low").className).toContain("emerald");
  });
  it("returns amber for medium", () => {
    expect(getEnergyRiskStyle("medium").label).toBe("Medium");
  });
  it("returns orange for medium_high", () => {
    expect(getEnergyRiskStyle("medium_high").label).toBe("Medium-High");
  });
  it("returns red for high", () => {
    expect(getEnergyRiskStyle("high").label).toBe("High");
  });
});

describe("getSavingLabelBadge", () => {
  it("returns Estimated saving for estimated_saving", () => {
    expect(getSavingLabelBadge("estimated_saving").label).toBe("Estimated saving");
  });
  it("returns Potential saving for potential_saving", () => {
    expect(getSavingLabelBadge("potential_saving").label).toBe("Potential saving");
  });
  it("returns Cashflow improvement for cashflow_improvement", () => {
    expect(getSavingLabelBadge("cashflow_improvement").label).toBe("Cashflow improvement");
  });
  it("returns Support value for support_value", () => {
    expect(getSavingLabelBadge("support_value").label).toBe("Support value");
  });
  it("returns Greener action for green_only", () => {
    expect(getSavingLabelBadge("green_only").label).toBe("Greener action");
  });
  it("returns No direct saving for no_direct_saving", () => {
    expect(getSavingLabelBadge("no_direct_saving").label).toBe("No direct saving");
  });
  it("returns Billing accuracy for billing_accuracy", () => {
    expect(getSavingLabelBadge("billing_accuracy").label).toBe("Billing accuracy");
  });
  it("returns Risk reduction for risk_reduction", () => {
    expect(getSavingLabelBadge("risk_reduction").label).toBe("Risk reduction");
  });
  it("returns Support access for support_access", () => {
    expect(getSavingLabelBadge("support_access").label).toBe("Support access");
  });
  it("returns Planning for planning", () => {
    expect(getSavingLabelBadge("planning").label).toBe("Planning");
  });
});
