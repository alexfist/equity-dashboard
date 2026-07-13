# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Entries are grouped under `Added`, `Changed`, `Fixed`, or `Security`, with the
newest release at the top. Add an entry under `[Unreleased]` whenever a
user-visible change lands; it moves into a dated release heading at the next
release cut.

## [Unreleased]

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
