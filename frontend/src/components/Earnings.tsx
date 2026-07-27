import type { EarningsEntry } from "../types";
import { Badge } from "./Badge";

export function Earnings({ earnings }: { earnings: EarningsEntry[] }) {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-text-dim">
        Latest Earnings
      </h3>
      {earnings.length === 0 && (
        <p className="py-6 text-center text-sm text-text-dim">
          No earnings summary added yet
        </p>
      )}
      {earnings.map((e) => (
        <div key={e.period}>
          <div className="mb-3 flex items-baseline gap-2">
            <span className="text-lg font-semibold text-text">{e.period}</span>
            <span className="text-sm text-text-dim">{e.date}</span>
          </div>

          <p className="mb-4 text-sm leading-relaxed text-text">{e.summary}</p>

          <div className="mb-4 space-y-3">
            {e.key_quotes.map((q, i) => (
              <blockquote
                key={i}
                className="border-l-2 border-accent-blue/50 py-1 pl-4 text-sm italic text-text"
              >
                "{q.quote}"
                <footer className="mt-1 text-xs not-italic text-text-dim">
                  — {q.speaker}, {q.role}
                </footer>
              </blockquote>
            ))}
          </div>

          <div className="mb-4 grid grid-cols-3 gap-3 rounded-lg bg-white/5 p-3 text-center">
            <div>
              <div className="text-xs uppercase text-text-dim">Revenue Guide</div>
              <div className="text-sm font-medium text-text">{e.guidance.revenue}</div>
            </div>
            <div>
              <div className="text-xs uppercase text-text-dim">Growth</div>
              <div className="text-sm font-medium text-text">{e.guidance.growth}</div>
            </div>
            <div>
              <div className="text-xs uppercase text-text-dim">Margin</div>
              <div className="text-sm font-medium text-text">{e.guidance.margin}</div>
            </div>
          </div>

          <div className="mb-4">
            <div className="mb-1.5 text-xs uppercase text-text-dim">Risks Flagged</div>
            <ul className="space-y-1">
              {e.risks_flagged.map((r, i) => (
                <li key={i} className="flex gap-2 text-sm text-text">
                  <Badge color="amber">Risk</Badge>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>

          <a
            href={e.source_url}
            target="_blank"
            rel="noreferrer"
            className="text-sm font-medium text-accent-blue hover:underline"
          >
            {e.source_label} →
          </a>
        </div>
      ))}
    </div>
  );
}
