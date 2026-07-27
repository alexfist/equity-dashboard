"""SEC EDGAR company-facts client: extracts annual financials + derived metrics.

Caches per-ticker results in memory for 24h to avoid repeated EDGAR calls.

Filers are inconsistent about which us-gaap tag they use for a given concept
from year to year (e.g. AVGO tagged FY2025 net income as `ProfitLoss` instead
of `NetIncomeLoss`). Series extraction therefore merges across a candidate
tag list per fiscal-year-end date rather than picking a single winning tag —
earlier tags in the list take priority when more than one has a value for
the same period, but a later tag can fill a year the earlier tag is missing.
"""

import time
from datetime import date
from typing import Optional

import httpx

from sec_edgar import HEADERS, get_cik

COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

_CACHE_TTL_SECONDS = 24 * 60 * 60
_facts_cache: dict[str, tuple[float, dict]] = {}

# Candidate us-gaap tags per logical field, priority order (first wins on overlap).
REVENUE_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"]
NET_INCOME_TAGS = ["NetIncomeLoss", "ProfitLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]
OPERATING_INCOME_TAGS = ["OperatingIncomeLoss"]
ASSETS_TAGS = ["Assets"]
# CashAndDueFromBanks: the bank-specific cash tag (e.g. JPM) — banks don't use
# CashAndCashEquivalentsAtCarryingValue, so this is a pure fallback, never an
# override, for tickers that report the generic tag.
CASH_TAGS = ["CashAndCashEquivalentsAtCarryingValue", "CashAndDueFromBanks"]
CAPEX_TAGS = ["PaymentsToAcquirePropertyPlantAndEquipment"]
SHARES_TAGS = ["CommonStockSharesOutstanding"]
CURRENT_LIABILITIES_TAGS = ["LiabilitiesCurrent"]
# ROIC's denominator (Assets - CurrentLiabilities) falls back to
# StockholdersEquity for filers that don't tag current liabilities (banks
# don't split their balance sheet into current/noncurrent) — this changes the
# metric to ROE for those filers, which is the number banks are actually
# evaluated on anyway.
STOCKHOLDERS_EQUITY_TAGS = ["StockholdersEquity"]
# Pretax income, used only as an OperatingIncomeLoss fallback: banks don't
# report a GAAP "operating income" line, but NetIncome + IncomeTaxExpense
# reconstructs their pretax income, which is the closest available analog.
INCOME_TAX_EXPENSE_TAGS = ["IncomeTaxExpenseBenefit"]

# Debt: prefer a single combined tag; only sum current+noncurrent as a fallback
# (a company with genuinely no debt, e.g. VRTX, correctly yields None throughout).
# LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities is the tag
# large banks (e.g. JPM) now use in place of the plain LongTermDebt tag.
DEBT_COMBINED_TAGS = [
    "DebtLongtermAndShorttermCombinedAmount",
    "LongTermDebt",
    "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities",
]
DEBT_NONCURRENT_TAGS = ["LongTermDebtNoncurrent"]
DEBT_CURRENT_TAGS = ["LongTermDebtCurrent"]

# Tags used only by get_latest_comp_metrics() for the peer-comps table.
GROSS_PROFIT_TAGS = ["GrossProfit"]
COST_OF_REVENUE_TAGS = ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfServices"]
RD_EXPENSE_TAGS = ["ResearchAndDevelopmentExpense"]


def _fetch_companyfacts(cik: str) -> Optional[dict]:
    now = time.time()
    cached = _facts_cache.get(cik)
    if cached and (now - cached[0]) < _CACHE_TTL_SECONDS:
        return cached[1]

    try:
        resp = httpx.get(COMPANYFACTS_URL.format(cik=cik), headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (httpx.HTTPError, httpx.TimeoutException, ValueError):
        return None

    _facts_cache[cik] = (now, data)
    return data


def _duration_days(start: str, end: str) -> int:
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def _tag_duration_series(gaap: dict, tag: str) -> dict[str, float]:
    """{end_date: value} for one tag's annual (10-K, FY, ~365-day) duration facts.

    Picks the most-recently-filed value for each end date (handles restatements).
    """
    node = gaap.get(tag)
    if not node:
        return {}
    units = node.get("units", {}).get("USD", [])
    by_end: dict[str, tuple[str, float]] = {}  # end -> (filed, val)
    for u in units:
        if u.get("form") != "10-K" or u.get("fp") != "FY":
            continue
        start, end = u.get("start"), u.get("end")
        if not start or not end:
            continue
        if not (350 <= _duration_days(start, end) <= 380):
            continue
        filed = u.get("filed", "")
        existing = by_end.get(end)
        if existing is None or filed > existing[0]:
            by_end[end] = (filed, u["val"])
    return {end: v[1] for end, v in by_end.items()}


def _tag_instant_series(gaap: dict, tag: str) -> dict[str, float]:
    """{end_date: value} for one tag's annual (10-K, FY) instant (balance-sheet) facts."""
    node = gaap.get(tag)
    if not node:
        return {}
    units = node.get("units", {}).get("USD", [])
    if not units:
        # e.g. CommonStockSharesOutstanding is reported in "shares", not "USD"
        units = node.get("units", {}).get("shares", [])
    by_end: dict[str, tuple[str, float]] = {}
    for u in units:
        if u.get("form") != "10-K" or u.get("fp") != "FY":
            continue
        if u.get("start"):
            continue  # instant values carry no "start"
        end = u.get("end")
        if not end:
            continue
        filed = u.get("filed", "")
        existing = by_end.get(end)
        if existing is None or filed > existing[0]:
            by_end[end] = (filed, u["val"])
    return {end: v[1] for end, v in by_end.items()}


def _merge_series(series_list: list[dict[str, float]]) -> dict[str, float]:
    """Merge per-year series across tags: earlier series in the list win on overlap,
    later series fill in years the earlier ones are missing."""
    merged: dict[str, float] = {}
    for series in reversed(series_list):
        merged.update(series)
    return merged


def _annual_duration_series(gaap: dict, tags: list[str]) -> dict[str, float]:
    return _merge_series([_tag_duration_series(gaap, tag) for tag in tags])


def _annual_instant_series(gaap: dict, tags: list[str]) -> dict[str, float]:
    return _merge_series([_tag_instant_series(gaap, tag) for tag in tags])


def _annual_debt_series(gaap: dict) -> dict[str, float]:
    """Total debt: prefer a single combined tag; fall back to summing
    noncurrent + current long-term debt where a combined tag isn't reported."""
    combined = _annual_instant_series(gaap, DEBT_COMBINED_TAGS)
    noncurrent = _annual_instant_series(gaap, DEBT_NONCURRENT_TAGS)
    current = _annual_instant_series(gaap, DEBT_CURRENT_TAGS)

    summed: dict[str, float] = {}
    for end, nc_val in noncurrent.items():
        summed[end] = nc_val + current.get(end, 0)

    # combined tag wins where present; summed fallback fills any remaining gaps
    return _merge_series([combined, summed])


def _safe_div(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None or b is None or b == 0:
        return None
    return a / b


def _pct(x: Optional[float]) -> Optional[float]:
    return None if x is None else round(x * 100, 1)


def _pretax_income_fallback_series(gaap: dict) -> dict[str, float]:
    """NetIncome + IncomeTaxExpense, used only to fill years OPERATING_INCOME_TAGS
    doesn't cover — banks don't report a GAAP operating income line, but this
    reconstructs their pretax income, the closest available analog."""
    net_income = _annual_duration_series(gaap, NET_INCOME_TAGS)
    tax = _annual_duration_series(gaap, INCOME_TAX_EXPENSE_TAGS)
    return {end: net_income[end] + tax[end] for end in net_income if end in tax}


def get_annual_financials(ticker: str, years: int = 5) -> list[dict]:
    """Return up to `years` most recent fiscal years of annual financials + derived metrics.

    Returns an empty list (never raises) if the ticker can't be resolved or
    EDGAR is unreachable.
    """
    cik = get_cik(ticker)
    if cik is None:
        return []

    data = _fetch_companyfacts(cik)
    if data is None:
        return []

    gaap = data.get("facts", {}).get("us-gaap", {})

    revenue = _annual_duration_series(gaap, REVENUE_TAGS)
    net_income = _annual_duration_series(gaap, NET_INCOME_TAGS)
    operating_income = _merge_series(
        [_annual_duration_series(gaap, OPERATING_INCOME_TAGS), _pretax_income_fallback_series(gaap)]
    )
    capex = _annual_duration_series(gaap, CAPEX_TAGS)

    assets = _annual_instant_series(gaap, ASSETS_TAGS)
    debt = _annual_debt_series(gaap)
    cash = _annual_instant_series(gaap, CASH_TAGS)
    shares = _annual_instant_series(gaap, SHARES_TAGS)
    current_liabilities = _annual_instant_series(gaap, CURRENT_LIABILITIES_TAGS)
    stockholders_equity = _annual_instant_series(gaap, STOCKHOLDERS_EQUITY_TAGS)

    fiscal_year_ends = sorted(revenue.keys(), reverse=True)[:years]

    results = []
    for end in fiscal_year_ends:
        rev = revenue.get(end)
        ni = net_income.get(end)
        oi = operating_income.get(end)
        cx = capex.get(end)
        a = assets.get(end)
        d = debt.get(end)
        c = cash.get(end)
        s = shares.get(end)
        cl = current_liabilities.get(end)
        se = stockholders_equity.get(end)

        fcf = (oi - cx) if (oi is not None and cx is not None) else None
        invested_capital = (a - cl) if (a is not None and cl is not None) else se

        results.append(
            {
                "fiscal_year_end": end,
                "fiscal_year": int(end.split("-")[0]),
                "revenue": rev,
                "net_income": ni,
                "operating_income": oi,
                "total_assets": a,
                "total_debt": d,
                "cash": c,
                "capex": cx,
                "shares_outstanding": s,
                "operating_margin": _safe_div(oi, rev),
                "net_margin": _safe_div(ni, rev),
                "fcf": fcf,
                "roic": _safe_div(ni, invested_capital),
            }
        )

    return results


def get_latest_comp_metrics(ticker: str) -> Optional[dict]:
    """Return the most recent fiscal year's derived metrics (whole percents,
    e.g. 32.9 for 32.9%) used to populate the live cells of the peer-comps
    table. Returns None if the ticker can't be resolved or has no revenue
    data on EDGAR, so callers can fall back to a hardcoded value instead.
    """
    cik = get_cik(ticker)
    if cik is None:
        return None

    data = _fetch_companyfacts(cik)
    if data is None:
        return None

    gaap = data.get("facts", {}).get("us-gaap", {})

    revenue = _annual_duration_series(gaap, REVENUE_TAGS)
    if not revenue:
        return None

    net_income = _annual_duration_series(gaap, NET_INCOME_TAGS)
    operating_income = _merge_series(
        [_annual_duration_series(gaap, OPERATING_INCOME_TAGS), _pretax_income_fallback_series(gaap)]
    )
    capex = _annual_duration_series(gaap, CAPEX_TAGS)
    assets = _annual_instant_series(gaap, ASSETS_TAGS)
    current_liabilities = _annual_instant_series(gaap, CURRENT_LIABILITIES_TAGS)
    stockholders_equity = _annual_instant_series(gaap, STOCKHOLDERS_EQUITY_TAGS)
    gross_profit = _annual_duration_series(gaap, GROSS_PROFIT_TAGS)
    cost_of_revenue = _annual_duration_series(gaap, COST_OF_REVENUE_TAGS)
    rd_expense = _annual_duration_series(gaap, RD_EXPENSE_TAGS)

    years_sorted = sorted(revenue.keys(), reverse=True)
    latest = years_sorted[0]
    prior = years_sorted[1] if len(years_sorted) > 1 else None

    rev = revenue.get(latest)
    ni = net_income.get(latest)
    oi = operating_income.get(latest)
    cx = capex.get(latest)
    a = assets.get(latest)
    cl = current_liabilities.get(latest)
    se = stockholders_equity.get(latest)
    gp = gross_profit.get(latest)
    cor = cost_of_revenue.get(latest)
    rd = rd_expense.get(latest)
    prior_rev = revenue.get(prior) if prior else None

    if gp is None and rev is not None and cor is not None:
        gp = rev - cor

    fcf = (oi - cx) if (oi is not None and cx is not None) else None
    invested_capital = (a - cl) if (a is not None and cl is not None) else se
    revenue_growth = (
        _safe_div(rev - prior_rev, prior_rev) if (rev is not None and prior_rev is not None) else None
    )

    return {
        "net_margin": _pct(_safe_div(ni, rev)),
        "operating_margin": _pct(_safe_div(oi, rev)),
        "gross_margin": _pct(_safe_div(gp, rev)),
        "fcf_margin": _pct(_safe_div(fcf, rev)),
        "roic": _pct(_safe_div(ni, invested_capital)),
        "rd_pct_revenue": _pct(_safe_div(rd, rev)),
        "revenue_growth_yoy": _pct(revenue_growth),
    }
