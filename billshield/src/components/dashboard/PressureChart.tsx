import { useMemo } from "react";
import {
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Line,
  ComposedChart,
  LabelList,
} from "recharts";
import type { MonthlyPressureForecast } from "@/api/types";

interface PressureChartProps {
  data: MonthlyPressureForecast[];
}

const COLORS: Record<string, string> = {
  energy: "#f59e0b",
  rent: "#6366f1",
  food: "#10b981",
  transport: "#3b82f6",
  councilTax: "#8b5cf6",
  water: "#06b6d4",
  broadbandMobile: "#ec4899",
};

const KEYS = [
  { dataKey: "energy", name: "Energy", color: COLORS.energy },
  { dataKey: "rent", name: "Rent", color: COLORS.rent },
  { dataKey: "food", name: "Food", color: COLORS.food },
  { dataKey: "transport", name: "Transport", color: COLORS.transport },
  { dataKey: "councilTax", name: "Council Tax", color: COLORS.councilTax },
  { dataKey: "water", name: "Water", color: COLORS.water },
  { dataKey: "broadbandMobile", name: "Broadband", color: COLORS.broadbandMobile },
] as const;

export function PressureChart({ data }: PressureChartProps) {
  const chartData = useMemo(() => {
    return data.map((d) => ({
      ...d,
      total: KEYS.reduce((sum, k) => sum + (Number(d[k.dataKey]) || 0), 0),
    }));
  }, [data]);

  if (chartData.length === 0) {
    return (
      <div className="rounded-2xl border border-border bg-card p-6">
        <h3 className="text-base font-semibold text-foreground mb-4">Monthly Household Pressure</h3>
        <p className="text-sm text-muted-foreground">No forecast data available yet. Upload a bill to see projections.</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-border bg-card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-foreground">Monthly Household Pressure</h3>
        <span className="text-xs text-muted-foreground">
          Total: {KEYS.length} cost categories stacked
        </span>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 25, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
            <XAxis
              dataKey="month"
              tick={{ fontSize: 13, fontWeight: 500 }}
              className="text-muted-foreground"
            />
            <YAxis
              tick={{ fontSize: 12 }}
              tickFormatter={(v) => `£${v}`}
              width={50}
              className="text-muted-foreground"
            />
            <Tooltip
              formatter={(value, name) => [`£${Number(value).toLocaleString()}`, name]}
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "0.75rem",
                padding: "0.75rem",
              }}
              labelStyle={{ fontWeight: 600, marginBottom: "0.25rem" }}
            />
            <Legend
              wrapperStyle={{ fontSize: "0.75rem" }}
            />
            {KEYS.map((k, i) => (
              <Bar
                key={k.dataKey}
                dataKey={k.dataKey}
                stackId="a"
                fill={k.color}
                name={k.name}
                radius={
                  i === KEYS.length - 1 ? [6, 6, 0, 0] : [0, 0, 0, 0]
                }
              >
                {i === KEYS.length - 1 && (
                  <LabelList
                    dataKey="total"
                    position="top"
                    formatter={(v: unknown) => `£${Number(v).toLocaleString()}`}
                    style={{ fontSize: "0.7rem", fontWeight: 600, fill: "hsl(var(--foreground))" }}
                  />
                )}
              </Bar>
            ))}
            <Line
              type="monotone"
              dataKey="total"
              stroke="hsl(var(--foreground))"
              strokeWidth={2}
              strokeDasharray="6 3"
              dot={{ r: 4, fill: "hsl(var(--foreground))" }}
              name="Total"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
