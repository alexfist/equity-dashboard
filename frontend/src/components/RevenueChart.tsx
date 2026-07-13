import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { AnnualFinancials } from "../types";

export function RevenueChartSkeleton() {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <div className="mb-4 h-4 w-40 animate-pulse rounded bg-white/10" />
      <div className="h-64 animate-pulse rounded bg-white/5" />
    </div>
  );
}

export function RevenueChart({ annual }: { annual: AnnualFinancials[] }) {
  const data = [...annual]
    .sort((a, b) => a.fiscal_year - b.fiscal_year)
    .map((y) => ({
      year: y.fiscal_year,
      Revenue: y.revenue !== null ? y.revenue / 1e9 : null,
      "Net Income": y.net_income !== null ? y.net_income / 1e9 : null,
    }));

  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-text-dim">
        Revenue &amp; Net Income ($B)
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
          <XAxis dataKey="year" stroke="#8b949e" fontSize={12} />
          <YAxis stroke="#8b949e" fontSize={12} />
          <Tooltip
            contentStyle={{ background: "#161b22", border: "1px solid #30363d", borderRadius: 6 }}
            labelStyle={{ color: "#e6edf3" }}
          />
          <Legend />
          <Bar dataKey="Revenue" fill="#58a6ff" radius={[4, 4, 0, 0]} />
          <Bar dataKey="Net Income" fill="#3fb950" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
