import type { CompsResponse, Ticker } from "../types";

function quartileClass(
  value: number | null,
  allValues: (number | null)[],
  higherIsBetter: boolean
): string {
  if (value === null) return "text-text-dim";
  const sorted = [...allValues].filter((v): v is number => v !== null).sort((a, b) => a - b);
  const rank = sorted.indexOf(value) / Math.max(sorted.length - 1, 1); // 0 (worst) -> 1 (best) after orientation below
  const normalizedRank = higherIsBetter ? rank : 1 - rank;
  if (normalizedRank >= 0.75) return "text-accent-green";
  if (normalizedRank >= 0.25) return "text-accent-amber";
  return "text-accent-red";
}

export function CompsTable({ ticker, comps }: { ticker: Ticker; comps: CompsResponse }) {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-text-dim">
        Peer Comparison
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-panel-border text-text-dim">
              <th className="py-2 text-left font-medium">Metric</th>
              {comps.peers.map((p) => (
                <th
                  key={p}
                  className={`py-2 text-right font-medium ${
                    p === ticker ? "text-accent-blue" : ""
                  }`}
                >
                  {p}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {comps.metrics.map((m) => {
              const allValues = comps.peers.map((p) => m.values[p] ?? null);
              const isLive = m.source.startsWith("SEC EDGAR");
              return (
                <tr key={m.label} className="border-b border-panel-border/50">
                  <td className="py-2 text-text-dim">
                    <div className="flex items-center gap-1.5">
                      <span>{m.label}</span>
                      <span
                        title={m.source}
                        className={`rounded px-1.5 py-0.5 text-[10px] font-medium ${
                          isLive
                            ? "bg-accent-blue/15 text-accent-blue"
                            : "bg-white/5 text-text-dim"
                        }`}
                      >
                        {isLive ? "Live" : "Est."}
                      </span>
                    </div>
                  </td>
                  {comps.peers.map((p) => {
                    const v = m.values[p] ?? null;
                    const isSubject = p === ticker;
                    const isBest = p === m.best_in_class;
                    return (
                      <td
                        key={p}
                        className={`py-2 text-right ${
                          isSubject ? "bg-accent-blue/10 font-semibold" : ""
                        } ${quartileClass(v, allValues, m.higher_is_better)}`}
                      >
                        {v === null ? "N/A" : v.toLocaleString()}
                        {isBest && <span title="Best in class"> ★</span>}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="mt-4 text-xs text-text-dim">{comps.footnote}</p>
    </div>
  );
}
