export function formatCurrency(amount: number): string {
  return `\u00A3${amount.toLocaleString("en-GB")}`;
}

export function formatPence(amount: number): string {
  return `${amount.toFixed(2)}p`;
}

export function formatKwh(amount: number): string {
  return `${amount.toLocaleString("en-GB")} kWh`;
}

export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function formatEnumLabel(value: string): string {
  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function formatRiskLabel(risk: string): string {
  switch (risk) {
    case "low":
      return "Low";
    case "medium":
      return "Medium";
    case "medium_high":
      return "Medium-High";
    case "high":
      return "High";
    default:
      return capitalize(risk);
  }
}
