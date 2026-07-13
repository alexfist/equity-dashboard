import type { Ticker } from "../types";

const TABS: Ticker[] = ["VRTX", "AVGO", "COST"];

export function Nav({
  active,
  onSelect,
}: {
  active: Ticker;
  onSelect: (t: Ticker) => void;
}) {
  return (
    <nav className="border-b border-panel-border bg-panel">
      <div className="mx-auto flex max-w-6xl items-center gap-8 px-6 py-4">
        <h1 className="text-lg font-semibold tracking-tight text-text">
          Equity Research Dashboard
        </h1>
        <div className="flex gap-1">
          {TABS.map((t) => (
            <button
              key={t}
              onClick={() => onSelect(t)}
              className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
                active === t
                  ? "bg-accent-blue/15 text-accent-blue"
                  : "text-text-dim hover:bg-white/5 hover:text-text"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}
