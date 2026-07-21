import type { AnnualFinancials } from "../types";
import { fmtPct, fmtShares, fmtUsdB } from "../lib/format";

interface MetricDef {
  label: string;
  get: (y: AnnualFinancials) => number | null;
  fmt: (v: number | null) => string;
  higherIsBetter: boolean;
}

const METRICS: MetricDef[] = [
  { label: "Revenue", get: (y) => y.revenue, fmt: fmtUsdB, higherIsBetter: true },
  { label: "Net Income", get: (y) => y.net_income, fmt: fmtUsdB, higherIsBetter: true },
  { label: "FCF", get: (y) => y.fcf, fmt: fmtUsdB, higherIsBetter: true },
  { label: "Operating Margin", get: (y) => y.operating_margin, fmt: fmtPct, higherIsBetter: true },
  { label: "Net Margin", get: (y) => y.net_margin, fmt: fmtPct, higherIsBetter: true },
  { label: "ROIC", get: (y) => y.roic, fmt: fmtPct, higherIsBetter: true },
  {
    label: "Net Cash - Debt",
    get: (y) => (y.cash ?? 0) - (y.total_debt ?? 0),
    fmt: fmtUsdB,
    higherIsBetter: true,
  },
  {
    label: "Shares Outstanding",
    get: (y) => y.shares_outstanding,
    fmt: fmtShares,
    higherIsBetter: false,
  },
];

function Delta({ current, prior, higherIsBetter }: { current: number | null; prior: number | null; higherIsBetter: boolean }) {
  if (current === null || prior === null || prior === 0) return null;
  const isUp = current >= prior;
  const isGood = higherIsBetter ? isUp : !isUp;
  const arrow = (
    <span className={`text-xs font-medium ${isGood ? "text-accent-green" : "text-accent-red"}`}>
      {isUp ? "▲" : "▼"}
    </span>
  );

  // A sign flip (e.g. net income swinging from negative to positive) makes a
  // percent change meaningless — show direction only, not a misleading magnitude.
  if (current * prior < 0) {
    return (
      <span className="text-xs font-medium">
        {arrow} <span className="text-text-dim">N/M</span>
      </span>
    );
  }

  const pctChange = ((current - prior) / Math.abs(prior)) * 100;
  return (
    <span className={`text-xs font-medium ${isGood ? "text-accent-green" : "text-accent-red"}`}>
      {isUp ? "▲" : "▼"} {Math.abs(pctChange).toFixed(1)}%
    </span>
  );
}

export function MetricsGrid({ annual }: { annual: AnnualFinancials[] }) {
  if (annual.length === 0) {
    return (
      <div className="rounded-lg border border-panel-border bg-panel p-6 text-text-dim">
        No financial data available.
      </div>
    );
  }

  const latest = annual[0];
  const prior = annual[1];

  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
      {METRICS.map((m) => (
        <div key={m.label} className="rounded-lg border border-panel-border bg-panel p-4">
          <div className="text-xs uppercase tracking-wide text-text-dim">{m.label}</div>
          <div className="mt-1 text-xl font-semibold text-text">{m.fmt(m.get(latest))}</div>
          {prior && (
            <div className="mt-1">
              <Delta current={m.get(latest)} prior={m.get(prior)} higherIsBetter={m.higherIsBetter} />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
