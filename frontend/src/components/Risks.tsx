import type { Risks } from "../types";
import { Badge } from "./Badge";

export function RisksSection({ risks }: { risks: Risks }) {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-text-dim">
          Key Risks
        </h3>
        <Badge color="gray">{risks.source}</Badge>
      </div>
      <div className="space-y-4">
        {risks.items.map((item, i) => (
          <div key={i} className="flex gap-3">
            <Badge color="amber">Risk</Badge>
            <div>
              <div className="text-sm font-semibold text-text">{item.title}</div>
              <p className="mt-1 text-sm leading-relaxed text-text-dim">{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
