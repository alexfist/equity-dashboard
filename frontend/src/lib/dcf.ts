import type { DCFAssumptions } from "../types";

/** The subset of DCF assumptions the sliders let the user adjust. */
export interface DCFInputs {
  growthRates: number[]; // 5 years, whole percents
  ebitdaMargin: number; // whole percent
  wacc: number; // whole percent
  terminalGrowth: number; // whole percent
  exitMultiple: number; // EV/EBITDA multiple applied to year-5 EBITDA
  terminalWeight: number; // 0-100, weight on Gordon Growth vs. (100 - this) on Exit Multiple
}

export interface DCFYearProjection {
  year: number;
  revenue: number; // $B
  ebitda: number; // $B
  ebit: number; // $B
  nopat: number; // $B
  da: number; // $B
  capex: number; // $B
  fcf: number; // $B (unlevered)
  discountFactor: number;
  pvFcf: number; // $B
}

export interface DCFResult {
  years: DCFYearProjection[];
  pvOfFcfSum: number; // $B
  gordonTerminalValue: number; // $B (undiscounted, at year 5)
  exitMultipleTerminalValue: number; // $B (undiscounted, at year 5)
  terminalValue: number; // $B (undiscounted, at year 5) — blended by terminalWeight
  pvOfTerminalValue: number; // $B
  enterpriseValue: number; // $B
  netCashOrDebtAdjustment: number; // $B, positive = added to EV, negative = subtracted
  equityValue: number; // $B
  intrinsicValuePerShare: number; // $
  upsidePct: number; // % vs currentPrice
}

/** Default slider inputs derived from a company's baseline DCF assumptions. */
export function defaultInputsFrom(assumptions: DCFAssumptions): DCFInputs {
  return {
    growthRates: [...assumptions.growth_rates],
    ebitdaMargin: assumptions.ebitda_margin,
    wacc: assumptions.wacc,
    terminalGrowth: assumptions.terminal_growth,
    exitMultiple: assumptions.exit_ebitda_multiple,
    terminalWeight: 50,
  };
}

/**
 * Unlevered FCF DCF. D&A and CapEx are held at their base-year ratio to
 * revenue (from `assumptions`) and scaled with projected revenue each year,
 * rather than held flat in dollar terms, since revenue can grow 30%+ over
 * the projection window.
 */
export function computeDCF(
  assumptions: DCFAssumptions,
  inputs: DCFInputs,
  currentPrice: number
): DCFResult {
  const { base_revenue, da, capex, tax_rate, net_cash, net_debt, shares, is_net_debt } =
    assumptions;

  const daRatio = da / base_revenue;
  const capexRatio = capex / base_revenue;

  const years: DCFYearProjection[] = [];
  let revenue = base_revenue;
  const waccDecimal = inputs.wacc / 100;

  for (let i = 0; i < 5; i++) {
    const year = i + 1;
    const growthRate = inputs.growthRates[i] ?? 0;
    revenue = revenue * (1 + growthRate / 100);

    const ebitda = revenue * (inputs.ebitdaMargin / 100);
    const yearDa = revenue * daRatio;
    const yearCapex = revenue * capexRatio;
    const ebit = ebitda - yearDa;
    const nopat = ebit * (1 - tax_rate / 100);
    const fcf = nopat + yearDa - yearCapex;

    const discountFactor = 1 / Math.pow(1 + waccDecimal, year);
    const pvFcf = fcf * discountFactor;

    years.push({
      year,
      revenue,
      ebitda,
      ebit,
      nopat,
      da: yearDa,
      capex: yearCapex,
      fcf,
      discountFactor,
      pvFcf,
    });
  }

  const pvOfFcfSum = years.reduce((sum, y) => sum + y.pvFcf, 0);

  const finalYear = years[years.length - 1];
  const terminalGrowthDecimal = inputs.terminalGrowth / 100;
  const gordonTerminalValue =
    (finalYear.fcf * (1 + terminalGrowthDecimal)) / (waccDecimal - terminalGrowthDecimal);
  const exitMultipleTerminalValue = finalYear.ebitda * inputs.exitMultiple;

  const gordonWeight = inputs.terminalWeight / 100;
  const terminalValue =
    gordonTerminalValue * gordonWeight + exitMultipleTerminalValue * (1 - gordonWeight);
  const pvOfTerminalValue = terminalValue * finalYear.discountFactor;

  const enterpriseValue = pvOfFcfSum + pvOfTerminalValue;

  const netCashOrDebtAdjustment = is_net_debt ? -(net_debt ?? 0) : net_cash ?? 0;
  const equityValue = enterpriseValue + netCashOrDebtAdjustment;

  const intrinsicValuePerShare = equityValue / shares;
  const upsidePct =
    currentPrice > 0 ? ((intrinsicValuePerShare - currentPrice) / currentPrice) * 100 : 0;

  return {
    years,
    pvOfFcfSum,
    gordonTerminalValue,
    exitMultipleTerminalValue,
    terminalValue,
    pvOfTerminalValue,
    enterpriseValue,
    netCashOrDebtAdjustment,
    equityValue,
    intrinsicValuePerShare,
    upsidePct,
  };
}
