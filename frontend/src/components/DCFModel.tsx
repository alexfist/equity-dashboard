import { useEffect, useMemo, useState } from "react";
import type { DCFAssumptions } from "../types";
import { computeDCF, defaultInputsFrom, type DCFInputs } from "../lib/dcf";
import { fmtBillions } from "../lib/format";

function Slider({
  label,
  value,
  min,
  max,
  step,
  onChange,
  suffix = "%",
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
  suffix?: string;
}) {
  return (
    <div>
      <div className="mb-1 flex justify-between text-xs text-text-dim">
        <span>{label}</span>
        <span className="font-medium text-text">
          {value}
          {suffix}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full accent-[#58a6ff]"
      />
    </div>
  );
}

function storageKey(ticker: string) {
  return `dcf-inputs-${ticker}`;
}

function loadSaved(ticker: string): { inputs: DCFInputs; priceText: string } | null {
  try {
    const raw = localStorage.getItem(storageKey(ticker));
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || !parsed.inputs || !parsed.priceText) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function DCFModel({
  ticker,
  assumptions,
  initialPrice,
  onIntrinsicValueChange,
  onCurrentPriceChange,
}: {
  ticker: string;
  assumptions: DCFAssumptions;
  initialPrice: number;
  onIntrinsicValueChange?: (value: number) => void;
  onCurrentPriceChange?: (value: number) => void;
}) {
  const [inputs, setInputs] = useState<DCFInputs>(
    () => loadSaved(ticker)?.inputs ?? defaultInputsFrom(assumptions)
  );
  // Raw text, not a number: an empty string is a valid in-progress state while
  // typing, so the field never snaps back to "0" and blocks editing.
  const [priceText, setPriceText] = useState<string>(
    () => loadSaved(ticker)?.priceText ?? initialPrice.toFixed(2)
  );

  // No reset-on-ticker-change effect here: CompanyTab mounts this component
  // with `key={ticker}`, so switching companies fully remounts it and the
  // lazy useState initializers above run fresh with the new ticker. A reset
  // effect here would race the persist effect below (it would fire on the
  // same render, before the reset's setState is applied, and re-persist the
  // previous ticker's values under the new ticker's storage key).

  // Persist sliders and price per ticker so they survive a page reload.
  useEffect(() => {
    localStorage.setItem(storageKey(ticker), JSON.stringify({ inputs, priceText }));
  }, [ticker, inputs, priceText]);

  const currentPrice = parseFloat(priceText) || 0;

  const result = useMemo(
    () => computeDCF(assumptions, inputs, currentPrice),
    [assumptions, inputs, currentPrice]
  );

  useEffect(() => {
    onIntrinsicValueChange?.(result.intrinsicValuePerShare);
  }, [result.intrinsicValuePerShare, onIntrinsicValueChange]);

  useEffect(() => {
    onCurrentPriceChange?.(currentPrice);
  }, [currentPrice, onCurrentPriceChange]);

  const setGrowth = (i: number, v: number) => {
    setInputs((prev) => {
      const growthRates = [...prev.growthRates];
      growthRates[i] = v;
      return { ...prev, growthRates };
    });
  };

  const upsideColor = result.upsidePct >= 0 ? "text-accent-green" : "text-accent-red";

  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-text-dim">
        Interactive DCF Model
      </h3>
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        {/* Assumptions panel */}
        <div className="space-y-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-text-dim">
            Assumptions
          </div>
          {inputs.growthRates.map((rate, i) => (
            <Slider
              key={i}
              label={`Year ${i + 1} Revenue Growth`}
              value={rate}
              min={0}
              max={100}
              step={1}
              onChange={(v) => setGrowth(i, v)}
            />
          ))}
          <Slider
            label="EBITDA Margin"
            value={inputs.ebitdaMargin}
            min={0}
            max={100}
            step={1}
            onChange={(v) => setInputs((p) => ({ ...p, ebitdaMargin: v }))}
          />
          <Slider
            label="WACC"
            value={inputs.wacc}
            min={0}
            max={100}
            step={0.5}
            onChange={(v) => setInputs((p) => ({ ...p, wacc: v }))}
          />
          <Slider
            label="Terminal Growth Rate"
            value={inputs.terminalGrowth}
            min={0}
            max={100}
            step={0.5}
            onChange={(v) => setInputs((p) => ({ ...p, terminalGrowth: v }))}
          />
          <div className="border-t border-panel-border pt-4">
            <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-text-dim">
              Terminal Value Blend
            </div>
            <Slider
              label="Exit EV/EBITDA Multiple"
              value={inputs.exitMultiple}
              min={5}
              max={40}
              step={0.5}
              suffix="x"
              onChange={(v) => setInputs((p) => ({ ...p, exitMultiple: v }))}
            />
            <Slider
              label="Weight: Gordon Growth vs. Exit Multiple"
              value={inputs.terminalWeight}
              min={0}
              max={100}
              step={5}
              onChange={(v) => setInputs((p) => ({ ...p, terminalWeight: v }))}
            />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Current Price ($)</label>
            <input
              type="text"
              inputMode="decimal"
              value={priceText}
              onChange={(e) => {
                const v = e.target.value;
                // Allow only characters that can appear while typing a decimal number
                if (v === "" || /^\d*\.?\d*$/.test(v)) {
                  setPriceText(v);
                }
              }}
              onBlur={() => {
                if (priceText === "" || isNaN(parseFloat(priceText))) {
                  setPriceText("0.00");
                }
              }}
              className="w-full rounded border border-panel-border bg-bg px-3 py-1.5 text-sm text-text"
            />
          </div>
        </div>

        {/* Output panel */}
        <div>
          <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-text-dim">
            Projections
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="text-text-dim">
                  <th className="pb-1 text-left font-medium">Year</th>
                  <th className="pb-1 text-right font-medium">Revenue</th>
                  <th className="pb-1 text-right font-medium">FCF</th>
                  <th className="pb-1 text-right font-medium">PV(FCF)</th>
                </tr>
              </thead>
              <tbody>
                {result.years.map((y) => (
                  <tr key={y.year} className="border-t border-panel-border/50">
                    <td className="py-1 text-text-dim">Y{y.year}</td>
                    <td className="py-1 text-right text-text">{fmtBillions(y.revenue)}</td>
                    <td className="py-1 text-right text-text">{fmtBillions(y.fcf)}</td>
                    <td className="py-1 text-right text-text">{fmtBillions(y.pvFcf)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-4 space-y-1.5 border-t border-panel-border pt-3 text-sm">
            <Row label="PV of FCFs" value={fmtBillions(result.pvOfFcfSum)} />
            <Row
              label={`Terminal Value (Gordon, ${inputs.terminalWeight}% wt)`}
              value={fmtBillions(result.gordonTerminalValue)}
              dim
            />
            <Row
              label={`Terminal Value (Exit Multiple, ${100 - inputs.terminalWeight}% wt)`}
              value={fmtBillions(result.exitMultipleTerminalValue)}
              dim
            />
            <Row label="PV of Terminal Value (blended)" value={fmtBillions(result.pvOfTerminalValue)} />
            <Row label="Enterprise Value" value={fmtBillions(result.enterpriseValue)} bold />
            <Row
              label={assumptions.is_net_debt ? "Less: Net Debt" : "Plus: Net Cash"}
              value={fmtBillions(result.netCashOrDebtAdjustment)}
            />
            <Row label="Equity Value" value={fmtBillions(result.equityValue)} bold />
          </div>

          <div className="mt-5 rounded-lg bg-white/5 p-4 text-center">
            <div className="text-xs uppercase tracking-wide text-text-dim">
              Intrinsic Value / Share
            </div>
            <div className="text-3xl font-bold text-text">
              ${result.intrinsicValuePerShare.toFixed(2)}
            </div>
            {currentPrice > 0 && (
              <div className={`mt-1 text-sm font-medium ${upsideColor}`}>
                {result.upsidePct >= 0 ? "+" : ""}
                {result.upsidePct.toFixed(1)}% vs current price
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function Row({
  label,
  value,
  bold = false,
  dim = false,
}: {
  label: string;
  value: string;
  bold?: boolean;
  dim?: boolean;
}) {
  return (
    <div
      className={`flex justify-between ${bold ? "font-semibold text-text" : "text-text-dim"} ${dim ? "text-xs opacity-70" : ""}`}
    >
      <span>{label}</span>
      <span className={bold ? "text-text" : ""}>{value}</span>
    </div>
  );
}
