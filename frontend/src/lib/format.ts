export function fmtUsdB(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined) return "N/A";
  return `$${(value / 1e9).toFixed(digits)}B`;
}

/** Format a value that is already expressed in $B units (not raw dollars). */
export function fmtBillions(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined) return "N/A";
  return `$${value.toFixed(digits)}B`;
}

export function fmtUsd(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined) return "N/A";
  return `$${value.toLocaleString(undefined, {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })}`;
}

export function fmtPct(value: number | null | undefined, digits = 1): string {
  if (value === null || value === undefined) return "N/A";
  return `${(value * 100).toFixed(digits)}%`;
}

export function fmtPctRaw(value: number | null | undefined, digits = 1): string {
  // value already expressed as a whole percent (e.g. 32.9, not 0.329)
  if (value === null || value === undefined) return "N/A";
  return `${value.toFixed(digits)}%`;
}

export function fmtShares(value: number | null | undefined): string {
  if (value === null || value === undefined) return "N/A";
  return `${(value / 1e9).toFixed(3)}B`;
}

export function fmtDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
}

export function fmtUnixDate(unixSeconds: number | null): string {
  if (!unixSeconds) return "N/A";
  return new Date(unixSeconds * 1000).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}
