# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Entries are grouped under `Added`, `Changed`, `Fixed`, or `Security`, with the
newest release at the top. Add an entry under `[Unreleased]` whenever a
user-visible change lands; it moves into a dated release heading at the next
release cut.

## [Unreleased]

### Changed
- DCF sliders (all five year-by-year revenue growth rates, EBITDA margin,
  WACC, and terminal growth rate) now range 0-100% instead of arbitrary
  narrower caps (e.g. WACC was capped at 18%, terminal growth at 5%),
  needed for the model to stay usable on outlier assumptions like JPM's.
  Exit EV/EBITDA Multiple stays 5-40x since it's a multiple, not a percent.

### Added
- Fourth ticker, JPM (JPMorgan Chase & Co., CIK 0000019617). Company info,
  business summary, moat, risks, and C-suite are populated from verified
  FY2025 10-K figures ($4.4T total assets, $182.4B net revenue, 20% ROTCE,
  14.6% CET1 ratio, 52% overhead ratio). Several pieces are left as
  placeholders for manual follow-up, each marked `TODO(user)` in
  `backend/company_data.py`: `current_price` (no live quote source was
  available this session), the DCF assumptions (the app's EBITDA/CapEx
  DCF shape doesn't fit bank economics — flagged for a rework), and most
  of the peer comps table (BAC/WFC/C/GS values are blank; only JPM's own
  verified figures are filled in). The earnings section is intentionally
  empty pending a manually-pasted summary, per this file's own top-of-file
  convention.
- Bank-specific XBRL tag fallbacks in `financials.py` so `/api/financials`
  and the live peer-comps metrics work for bank filers, which don't use the
  same us-gaap tags as operating companies: `CashAndDueFromBanks` (cash),
  `LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities` (total
  debt, since JPM stopped tagging plain `LongTermDebt` after 2013), and a
  reconstructed pretax-income fallback (`NetIncomeLoss +
  IncomeTaxExpenseBenefit`) for the missing `OperatingIncomeLoss` line.
  ROIC's denominator falls back from `Assets - LiabilitiesCurrent` to
  `StockholdersEquity` when a filer doesn't tag current liabilities, which
  turns the metric into ROE for those filers. All are additive fallbacks
  only used when the primary tag is missing, so VRTX/AVGO/COST are
  unaffected. CapEx (and therefore FCF) has no fallback and stays N/A for
  banks — no XBRL tag for it exists in JPM's filings, since bank capex is
  folded into an unbroken-out "other" cash flow line.
- Screenshots section in the root README (`docs/screenshots/dashboard-overview.png`).
- DCF slider inputs (growth rates, EBITDA margin, WACC, terminal growth,
  exit multiple, terminal weight) and the current price field now persist to
  `localStorage` per ticker, so they survive a page reload instead of
  resetting to the default assumptions.
- New "Key Risks" qualitative section (`GET /api/qualitative/{ticker}`
  → `risks`), rendered between Economic Moat and C-Suite Assessment. AVGO's
  three risks (debt-funded acquisitions, AI customer concentration/vertical
  integration, concentrated wafer and materials supply chain) are sourced
  from figures in Broadcom's FY2025 10-K ($67.1B total indebtedness, ~40%
  of net revenue from the top five end customers, ~95% of wafers from
  TSMC, ~17% of net revenue from China shipments). VRTX and COST each get
  three risks grounded in facts already established in their business
  summaries (CF revenue concentration, unproven new franchises, and drug
  pricing pressure for VRTX; thin operating margins, membership renewal
  dependence, and tariff exposure for COST).

### Changed
- CORS allowed origins (backend) and the API base URL (frontend) are now
  configurable via `ALLOWED_ORIGINS` and `VITE_API_BASE_URL` env vars,
  falling back to the local dev ports so `npm run dev` / `uvicorn --reload`
  keep working unchanged. Needed to point a deployed frontend at a deployed
  backend instead of hardcoded localhost URLs.
- Key metrics card label corrected from "Net Cash / (Debt)" to "Net Cash -
  Debt" (the underlying calculation was already cash minus debt).

### Fixed
- TypeScript build error on Vercel: the recommendation badge color map was
  missing the `INVESTIGATE` key, which `company.recommendation` can be
  (AVGO's static fallback value).
- DCF sliders bled across ticker tabs: switching tabs could briefly pass one
  ticker's `dcf`/`company` data alongside another ticker's `ticker` prop
  (the reset-to-null effect hadn't committed yet), which the new
  localStorage persistence would then save under the wrong ticker's key.
  `CompanyTab` now tracks which ticker its loaded data belongs to and only
  renders `DCFModel` once they match, so sliders and current price never
  leak between tabs.

### Content
- AVGO business summary: added a balance sheet paragraph covering goodwill
  ($97.8B, mostly VMware/CA Technologies), rising stock-based compensation
  ($2.2B → $7.6B FY2023-FY2025, mostly VMware retention grants), long-term
  debt (~$62B) with its ~$3B/yr interest expense drag on free cash flow, and
  the offsetting liquidity cushion ($19.6B cash, fully undrawn $7.5B
  revolver). Figures verified against SEC EDGAR XBRL data and the FY2025
  10-K liquidity note.

## [0.1.0] - 2026-07-13

### Added
- Full-stack equity research dashboard for VRTX, AVGO, and COST (React + Vite +
  TypeScript + Tailwind frontend, Python FastAPI backend).
- Company header, key metrics grid, and 5-year revenue/net income chart, all
  sourced from SEC EDGAR company facts.
- Interactive client-side DCF model with per-year revenue growth sliders,
  EBITDA margin, WACC, and terminal growth inputs.
- Terminal value blended from two models (Gordon Growth and Exit EV/EBITDA
  Multiple) with an adjustable weight slider, defaulting to each company's own
  EV/EBITDA from the peer comps table.
- Dynamic BUY/HOLD/SELL recommendation badge, derived live from DCF
  upside/downside vs. current price (20% thresholds), falling back to a
  static research recommendation until the DCF model loads.
- Peer comps table per sector (biotech, semiconductors, retail) with
  best-in-class highlighting; margin/growth/ROIC metrics are pulled live from
  SEC EDGAR and update automatically as new filings are submitted, while
  valuation multiples and retail-specific metrics remain hardcoded research
  estimates.
- Qualitative sections: business overview, economic moat assessment, C-suite
  assessment, latest earnings call summary, recent news (via Finnhub), and
  recent SEC filings (8-K).
- Citation badges throughout distinguishing SEC EDGAR (live), Finnhub, and
  hardcoded research data.

### Changed
- Rewrote all hardcoded qualitative research content (business summaries,
  moat descriptions, C-suite notes, earnings summaries) to avoid dashes as
  sentence punctuation and to use plain language suited to a retail investor
  audience.

### Security
- Removed a real API key that had been accidentally copied into
  `backend/.env.example`; it now contains only a placeholder.

[Unreleased]: https://github.com/alexfist/equity-dashboard/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/alexfist/equity-dashboard/releases/tag/v0.1.0
