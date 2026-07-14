"""Equity Research Dashboard — FastAPI backend."""

import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import company_data
import financials
import finnhub_client
import qualitative_data
import sec_edgar

app = FastAPI(title="Equity Research Dashboard API")

# Comma-separated list of allowed frontend origins, e.g.
# "http://localhost:5173,https://equity-dashboard.vercel.app". Falls back to
# the local Vite dev server when unset so `uvicorn main:app --reload` keeps
# working out of the box.
_allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _allowed_origins.split(",") if o.strip()],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _validate_ticker(ticker: str) -> str:
    ticker = ticker.upper()
    if ticker not in company_data.TICKERS:
        raise HTTPException(status_code=404, detail=f"Unknown ticker: {ticker}")
    return ticker


@app.get("/api/company/{ticker}")
def get_company(ticker: str):
    ticker = _validate_ticker(ticker)
    return company_data.COMPANY_INFO[ticker]


@app.get("/api/financials/{ticker}")
def get_financials(ticker: str):
    ticker = _validate_ticker(ticker)
    return {"ticker": ticker, "annual": financials.get_annual_financials(ticker, years=5)}


@app.get("/api/dcf/{ticker}")
def get_dcf_assumptions(ticker: str):
    ticker = _validate_ticker(ticker)
    return company_data.DCF_ASSUMPTIONS[ticker]


@app.get("/api/comps/{ticker}")
def get_comps(ticker: str):
    ticker = _validate_ticker(ticker)
    base = company_data.COMPS_DATA[ticker]
    peers = base["peers"]

    metrics = []
    for m in base["metrics"]:
        metric = dict(m)
        live_key = company_data.LIVE_COMPS_METRICS.get(m["label"])

        if live_key is None:
            metric["source"] = "Research estimate"
            metrics.append(metric)
            continue

        values = dict(m["values"])
        for peer in peers:
            live = financials.get_latest_comp_metrics(peer)
            if live and live.get(live_key) is not None:
                values[peer] = live[live_key]
        metric["values"] = values
        metric["source"] = "SEC EDGAR · Live"

        candidates = {p: v for p, v in values.items() if v is not None}
        if candidates:
            metric["best_in_class"] = (
                max(candidates, key=candidates.get)
                if m["higher_is_better"]
                else min(candidates, key=candidates.get)
            )
        metrics.append(metric)

    return {"peers": peers, "metrics": metrics, "footnote": company_data.COMPS_FOOTNOTE}


@app.get("/api/news/{ticker}")
def get_news(ticker: str):
    ticker = _validate_ticker(ticker)
    return {"ticker": ticker, "articles": finnhub_client.get_company_news(ticker, limit=10)}


@app.get("/api/filings/{ticker}")
def get_filings(ticker: str):
    ticker = _validate_ticker(ticker)
    return {"ticker": ticker, "filings": sec_edgar.get_recent_8k_filings(ticker, limit=5)}


@app.get("/api/qualitative/{ticker}")
def get_qualitative(ticker: str):
    ticker = _validate_ticker(ticker)
    return qualitative_data.QUALITATIVE_DATA[ticker]
