import { describe, it, expect } from "vitest";
import { formatCurrency, formatPence, formatKwh, capitalize, formatEnumLabel, formatRiskLabel } from "@/utils/formatters";

describe("formatCurrency", () => {
  it("formats whole pounds", () => {
    expect(formatCurrency(1742)).toBe("£1,742");
  });

  it("formats small numbers", () => {
    expect(formatCurrency(0)).toBe("£0");
  });

  it("formats decimals", () => {
    expect(formatCurrency(142.50)).toBe("£142.5");
  });

  it("formats large numbers", () => {
    expect(formatCurrency(10000)).toBe("£10,000");
  });

  it("formats negative", () => {
    expect(formatCurrency(-50)).toBe("£-50");
  });
});

describe("formatPence", () => {
  it("formats pence", () => {
    expect(formatPence(27.34)).toBe("27.34p");
  });

  it("formats zero", () => {
    expect(formatPence(0)).toBe("0.00p");
  });

  it("formats with rounding", () => {
    expect(formatPence(60.123)).toBe("60.12p");
  });
});

describe("formatKwh", () => {
  it("formats kWh", () => {
    expect(formatKwh(2900)).toBe("2,900 kWh");
  });

  it("formats small value", () => {
    expect(formatKwh(0)).toBe("0 kWh");
  });

  it("formats large value", () => {
    expect(formatKwh(11000)).toBe("11,000 kWh");
  });
});

describe("capitalize", () => {
  it("capitalizes lowercase", () => {
    expect(capitalize("hello")).toBe("Hello");
  });

  it("handles single char", () => {
    expect(capitalize("a")).toBe("A");
  });

  it("handles empty string", () => {
    expect(capitalize("")).toBe("");
  });
});

describe("formatEnumLabel", () => {
  it("converts snake_case", () => {
    expect(formatEnumLabel("medium_high")).toBe("Medium High");
  });

  it("handles single word", () => {
    expect(formatEnumLabel("low")).toBe("Low");
  });

  it("handles multi_underscore", () => {
    expect(formatEnumLabel("council_tax_reduction_checker")).toBe("Council Tax Reduction Checker");
  });
});

describe("formatRiskLabel", () => {
  it("returns Low", () => expect(formatRiskLabel("low")).toBe("Low"));
  it("returns Medium", () => expect(formatRiskLabel("medium")).toBe("Medium"));
  it("returns Medium-High", () => expect(formatRiskLabel("medium_high")).toBe("Medium-High"));
  it("returns High", () => expect(formatRiskLabel("high")).toBe("High"));
  it("falls back to capitalize for unknown", () => expect(formatRiskLabel("unknown_risk")).toBe("Unknown_risk"));
});
