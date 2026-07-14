import type { CompanyInfo } from "../types";

export function CompanyHeader({
  company,
  intrinsicValue,
  currentPrice,
}: {
  company: CompanyInfo;
  intrinsicValue: number | null;
  currentPrice: number;
}) {
  // Recommendation is derived live from DCF upside/downside once the intrinsic
  // value is available; falls back to the static research recommendation while
  // the DCF model is still loading.
  const upsidePct =
    intrinsicValue !== null ? ((intrinsicValue - currentPrice) / currentPrice) * 100 : null;

  const recommendation =
    upsidePct === null
      ? company.recommendation
      : upsidePct > 20
        ? "BUY"
        : upsidePct < -20
          ? "SELL"
          : "HOLD";

  const badgeClass =
    (
      {
        BUY: "bg-accent-green/15 text-accent-green border border-accent-green/30",
        HOLD: "bg-accent-amber/15 text-accent-amber border border-accent-amber/30",
        SELL: "bg-accent-red/15 text-accent-red border border-accent-red/30",
      } as Record<string, string>
    )[recommendation] ?? "bg-accent-blue/15 text-accent-blue border border-accent-blue/30";

  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-2xl font-bold text-text">{company.ticker}</span>
            <span className={`rounded px-2.5 py-0.5 text-xs font-semibold ${badgeClass}`}>
              {recommendation}
            </span>
          </div>
          <p className="mt-1 text-text-dim">{company.name}</p>
          <p className="mt-0.5 text-sm text-text-dim">
            {company.sector} · {company.exchange} · CIK {company.cik}
          </p>
        </div>
        <div className="text-right">
          <div className="text-xs uppercase tracking-wide text-text-dim">Current Price</div>
          <div className="text-2xl font-semibold text-text">${currentPrice.toFixed(2)}</div>
          {intrinsicValue !== null && (
            <>
              <div className="mt-2 text-xs uppercase tracking-wide text-text-dim">
                DCF Base Case Target
              </div>
              <div className="text-lg font-medium text-accent-blue">
                ${intrinsicValue.toFixed(2)}
              </div>
            </>
          )}
        </div>
      </div>
      <p className="mt-4 text-xs text-text-dim">
        Last updated: {new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}
      </p>
    </div>
  );
}
