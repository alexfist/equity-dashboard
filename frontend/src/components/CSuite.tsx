import type { CSuiteMember } from "../types";

export function CSuite({ csuite }: { csuite: CSuiteMember[] }) {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-text-dim">
        C-Suite Assessment
      </h3>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {csuite.map((exec) => (
          <div key={exec.name} className="rounded-lg border border-panel-border/60 p-4">
            <div className="mb-3">
              <div className="font-semibold text-text">{exec.name}</div>
              <div className="text-sm text-text-dim">{exec.role}</div>
              <div className="text-xs text-text-dim">{exec.tenure}</div>
            </div>
            <ul className="mb-3 space-y-1.5">
              {exec.strengths.map((s, i) => (
                <li key={i} className="flex gap-2 text-sm text-text">
                  <span className="mt-0.5 shrink-0 text-accent-green">✓</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
            <ul className="space-y-1.5">
              {exec.watch.map((w, i) => (
                <li key={i} className="flex gap-2 text-sm text-text">
                  <span className="mt-0.5 shrink-0 text-accent-amber">⚠</span>
                  <span>{w}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
