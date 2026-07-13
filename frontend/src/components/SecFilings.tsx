import type { Filing } from "../types";
import { Badge } from "./Badge";
import { fmtDate } from "../lib/format";

export function SecFilings({ filings }: { filings: Filing[] }) {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-text-dim">
          Recent SEC Filings
        </h3>
        <Badge color="blue">SEC EDGAR · Live</Badge>
      </div>
      {filings.length === 0 ? (
        <p className="py-6 text-center text-sm text-text-dim">No recent filings available</p>
      ) : (
        <ul className="divide-y divide-panel-border/50">
          {filings.map((f, i) => (
            <li key={i} className="flex flex-wrap items-center gap-3 py-3 text-sm">
              <Badge color="blue">{f.form}</Badge>
              <span className="text-text-dim">{fmtDate(f.filing_date)}</span>
              <span className="text-text">{f.description}</span>
              <a
                href={f.url}
                target="_blank"
                rel="noreferrer"
                className="ml-auto font-medium text-accent-blue hover:underline"
              >
                View filing →
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
