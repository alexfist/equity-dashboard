import type { BusinessSummary, Moat } from "../types";
import { Badge } from "./Badge";

export function BusinessOverview({ businessSummary }: { businessSummary: BusinessSummary }) {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-text-dim">
          Business Overview
        </h3>
        <Badge color="gray">{businessSummary.source}</Badge>
      </div>
      <div className="space-y-3 text-sm leading-relaxed text-text">
        {businessSummary.paragraphs.map((p, i) => (
          <p key={i}>{p}</p>
        ))}
      </div>
    </div>
  );
}

export function MoatAssessment({ moat }: { moat: Moat }) {
  const strengthColor = moat.strength === "WIDE" ? "green" : "amber";
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-text-dim">
          Economic Moat
        </h3>
        <Badge color="gray">{moat.source}</Badge>
      </div>
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <Badge color="blue">{moat.type}</Badge>
        <Badge color={strengthColor}>{moat.strength}</Badge>
      </div>
      <p className="text-sm leading-relaxed text-text">{moat.description}</p>
    </div>
  );
}
