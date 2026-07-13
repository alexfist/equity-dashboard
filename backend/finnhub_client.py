"""Finnhub client: recent company news."""

import os
from datetime import date, timedelta

import httpx

FINNHUB_BASE_URL = "https://finnhub.io/api/v1/company-news"


def get_company_news(ticker: str, limit: int = 10) -> list[dict]:
    """Return the `limit` most recent news articles for a ticker.

    Returns an empty list (never raises) on a missing/invalid API key,
    a non-200 response, or any network error.
    """
    api_key = os.environ.get("FINNHUB_KEY")
    if not api_key or api_key == "your_key_here":
        return []

    today = date.today()
    thirty_days_ago = today - timedelta(days=30)

    params = {
        "symbol": ticker.upper(),
        "from": thirty_days_ago.isoformat(),
        "to": today.isoformat(),
        "token": api_key,
    }

    try:
        resp = httpx.get(FINNHUB_BASE_URL, params=params, timeout=10)
        if resp.status_code != 200:
            return []
        raw = resp.json()
    except (httpx.HTTPError, httpx.TimeoutException, ValueError):
        return []

    if not isinstance(raw, list):
        return []

    articles = []
    for item in raw[:limit]:
        articles.append(
            {
                "headline": item.get("headline", ""),
                "summary": item.get("summary", ""),
                "source": item.get("source", ""),
                "url": item.get("url", ""),
                "datetime": item.get("datetime"),
            }
        )
    return articles
