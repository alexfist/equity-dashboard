"""SEC EDGAR client: ticker -> CIK resolution and recent 8-K filings.

SEC rejects any automated request that lacks a descriptive User-Agent
(name + contact email) with a 403 — every call here sets one.
"""

import time
from typing import Optional

import httpx

SEC_USER_AGENT = "EquityDashboard research@example.com"
HEADERS = {"User-Agent": SEC_USER_AGENT}

TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
FILING_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_no_dashes}/{doc}"

_cik_cache: Optional[dict[str, str]] = None
_cik_cache_fetched_at: float = 0
_CACHE_TTL_SECONDS = 24 * 60 * 60


def _load_ticker_map() -> dict[str, str]:
    """Fetch and cache the ticker -> 10-digit zero-padded CIK map."""
    global _cik_cache, _cik_cache_fetched_at

    if _cik_cache is not None and (time.time() - _cik_cache_fetched_at) < _CACHE_TTL_SECONDS:
        return _cik_cache

    resp = httpx.get(TICKER_MAP_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    raw = resp.json()

    mapping: dict[str, str] = {}
    for entry in raw.values():
        ticker = entry["ticker"].upper()
        cik = str(entry["cik_str"]).zfill(10)
        mapping[ticker] = cik

    _cik_cache = mapping
    _cik_cache_fetched_at = time.time()
    return mapping


def get_cik(ticker: str) -> Optional[str]:
    """Return the 10-digit zero-padded CIK for a ticker, or None if not found."""
    try:
        mapping = _load_ticker_map()
    except (httpx.HTTPError, httpx.TimeoutException):
        return None
    return mapping.get(ticker.upper())


def get_recent_8k_filings(ticker: str, limit: int = 5) -> list[dict]:
    """Return the `limit` most recent 8-K filings for a ticker.

    Returns an empty list (never raises) if the ticker can't be resolved
    or SEC EDGAR is unreachable.
    """
    cik = get_cik(ticker)
    if cik is None:
        return []

    try:
        resp = httpx.get(SUBMISSIONS_URL.format(cik=cik), headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except (httpx.HTTPError, httpx.TimeoutException, ValueError):
        return []

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accession_numbers = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    primary_docs = recent.get("primaryDocument", [])
    primary_doc_descriptions = recent.get("primaryDocDescription", [])

    cik_int = int(cik)
    filings = []
    for i, form in enumerate(forms):
        if form != "8-K":
            continue
        accession_no_dashes = accession_numbers[i].replace("-", "")
        doc = primary_docs[i] if i < len(primary_docs) else ""
        url = FILING_URL.format(cik_int=cik_int, accession_no_dashes=accession_no_dashes, doc=doc)
        filings.append(
            {
                "form": form,
                "filing_date": filing_dates[i],
                "description": (
                    primary_doc_descriptions[i]
                    if i < len(primary_doc_descriptions) and primary_doc_descriptions[i]
                    else "Current report"
                ),
                "url": url,
            }
        )
        if len(filings) >= limit:
            break

    return filings
