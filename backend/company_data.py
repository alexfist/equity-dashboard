"""Static/hardcoded company metadata, DCF default assumptions, and peer comps.

Peer comp figures are illustrative research estimates (no live data source
was specified for them) — clearly labeled as such in the API response and
in the frontend footnote per the user's own requirement.
"""

TICKERS = ["VRTX", "AVGO", "COST", "JPM"]

COMPANY_INFO = {
    "VRTX": {
        "ticker": "VRTX",
        "name": "Vertex Pharmaceuticals Incorporated",
        "sector": "Biotechnology",
        "exchange": "NASDAQ",
        "cik": "0000875320",
        "recommendation": "HOLD",
        "current_price": 490.00,
    },
    "AVGO": {
        "ticker": "AVGO",
        "name": "Broadcom Inc.",
        "sector": "Semiconductors",
        "exchange": "NASDAQ",
        "cik": "0001730168",
        "recommendation": "INVESTIGATE",
        "current_price": 250.00,
    },
    "COST": {
        "ticker": "COST",
        "name": "Costco Wholesale Corporation",
        "sector": "Retail - Consumer Staples",
        "exchange": "NASDAQ",
        "cik": "0000909832",
        "recommendation": "HOLD",
        "current_price": 920.00,
    },
    "JPM": {
        "ticker": "JPM",
        "name": "JPMorgan Chase & Co.",
        "sector": "Banking / Financial Services",
        "exchange": "NYSE",
        "cik": "0000019617",
        "recommendation": "HOLD",
        # TODO(user): placeholder only, no live price source was available for
        # this session — replace with the actual current price.
        "current_price": 300.00,
    },
}

# All revenue/debt/cash figures in $B; growthRates as whole percents (e.g. 9 == 9%).
DCF_ASSUMPTIONS = {
    "VRTX": {
        "base_revenue": 12.0,
        "growth_rates": [9, 13, 11, 9, 8],
        "ebitda_margin": 43,
        "da": 0.6,
        "capex": 0.45,
        "tax_rate": 25,
        "wacc": 8.5,
        "terminal_growth": 3.0,
        "net_cash": 12.3,
        "net_debt": None,
        "shares": 0.254,
        "is_net_debt": False,
        "exit_ebitda_multiple": 15.9,
    },
    "AVGO": {
        "base_revenue": 63.9,
        "growth_rates": [20, 18, 14, 12, 8],
        "ebitda_margin": 65,
        "da": 5.5,
        "capex": 0.7,
        "tax_rate": 15,
        "wacc": 9.5,
        "terminal_growth": 3.0,
        "net_cash": None,
        "net_debt": 51.0,
        "shares": 4.83,
        "is_net_debt": True,
        "exit_ebitda_multiple": 17.2,
    },
    "COST": {
        "base_revenue": 280.4,
        "growth_rates": [8, 7, 7, 6, 6],
        "ebitda_margin": 4.2,
        "da": 2.8,
        "capex": 4.5,
        "tax_rate": 25,
        "wacc": 7.2,
        "terminal_growth": 2.5,
        "net_cash": None,
        "net_debt": 1.2,
        "shares": 0.444,
        "is_net_debt": True,
        "exit_ebitda_multiple": 24.8,
    },
    # TODO(user): this EBITDA/CapEx-driven DCF shape was built for
    # operating companies and doesn't really fit a bank's economics — a bank
    # doesn't have a meaningful "EBITDA" or "CapEx" line, its value drivers
    # are net interest margin, loan growth, and credit losses, and analysts
    # more commonly value banks off a dividend discount or excess-return-on-
    # tangible-equity model instead. These are rough placeholders sized to
    # produce a plausible-looking output, not a real bank valuation model —
    # replace before trusting the JPM DCF numbers. base_revenue is FY2025
    # total net revenue ($182.4B) and shares is FY2025 shares outstanding
    # (2.696B), both pulled from the FY2025 10-K; ebitda_margin uses
    # pretax margin as a rough EBITDA proxy.
    "JPM": {
        "base_revenue": 182.4,
        "growth_rates": [4, 4, 4, 4, 4],
        "ebitda_margin": 40,
        "da": 2.0,
        "capex": 3.5,
        "tax_rate": 23,
        "wacc": 9.0,
        "terminal_growth": 3.0,
        "net_cash": None,
        "net_debt": None,
        "shares": 2.696,
        "is_net_debt": True,
        "exit_ebitda_multiple": 10.0,
    },
}

COMPS_FOOTNOTE = (
    "Margin, growth, and ROIC metrics are pulled live from SEC EDGAR and update "
    "automatically as new filings are submitted. Valuation multiples and "
    "retail-specific metrics (marked Research estimate) are hardcoded, since "
    "they require live market prices, forward analyst estimates, or figures "
    "SEC filings do not report in structured form."
)

# Metric labels computed live from SEC EDGAR (see financials.get_latest_comp_metrics)
# rather than served from the hardcoded values below. Key is the dict key that
# function returns; the hardcoded COMPS_DATA values below still serve as a
# fallback if a peer's live fetch fails.
LIVE_COMPS_METRICS = {
    "Net Margin": "net_margin",
    "ROIC": "roic",
    "Gross Margin": "gross_margin",
    "FCF Margin": "fcf_margin",
    "Revenue Growth YoY": "revenue_growth_yoy",
    "R&D as % of Revenue": "rd_pct_revenue",
    "Operating Margin": "operating_margin",
}

# best_in_class marks, per metric, which ticker (subject or peer) has the best value.
# "higher_is_better" controls the color-quartile direction the frontend applies.
COMPS_DATA = {
    "VRTX": {
        "peers": ["VRTX", "REGN", "ABBV", "BMY", "LLY"],
        "metrics": [
            {
                "label": "Fwd P/E",
                "higher_is_better": False,
                "values": {"VRTX": 21.4, "REGN": 16.8, "ABBV": 15.2, "BMY": 8.1, "LLY": 33.6},
                "best_in_class": "BMY",
            },
            {
                "label": "EV/EBITDA",
                "higher_is_better": False,
                "values": {"VRTX": 15.9, "REGN": 11.2, "ABBV": 12.4, "BMY": 7.8, "LLY": 24.1},
                "best_in_class": "BMY",
            },
            {
                "label": "EV/Revenue",
                "higher_is_better": False,
                "values": {"VRTX": 7.0, "REGN": 5.4, "ABBV": 5.9, "BMY": 2.6, "LLY": 12.8},
                "best_in_class": "BMY",
            },
            {
                "label": "R&D as % of Revenue",
                "higher_is_better": True,
                "values": {"VRTX": 33.5, "REGN": 26.1, "ABBV": 13.8, "BMY": 21.4, "LLY": 24.9},
                "best_in_class": "VRTX",
            },
            {
                "label": "Net Margin",
                "higher_is_better": True,
                "values": {"VRTX": 32.9, "REGN": 27.3, "ABBV": 14.1, "BMY": 9.6, "LLY": 21.7},
                "best_in_class": "VRTX",
            },
            {
                "label": "ROIC",
                "higher_is_better": True,
                "values": {"VRTX": 18.1, "REGN": 15.6, "ABBV": 12.9, "BMY": 6.2, "LLY": 19.8},
                "best_in_class": "LLY",
            },
        ],
    },
    "AVGO": {
        "peers": ["AVGO", "NVDA", "AMD", "QCOM", "MRVL"],
        "metrics": [
            {
                "label": "Fwd P/E",
                "higher_is_better": False,
                "values": {"AVGO": 19.8, "NVDA": 32.4, "AMD": 24.9, "QCOM": 13.6, "MRVL": 28.3},
                "best_in_class": "QCOM",
            },
            {
                "label": "EV/EBITDA",
                "higher_is_better": False,
                "values": {"AVGO": 17.2, "NVDA": 26.8, "AMD": 21.5, "QCOM": 10.4, "MRVL": 22.9},
                "best_in_class": "QCOM",
            },
            {
                "label": "EV/FCF",
                "higher_is_better": False,
                "values": {"AVGO": 24.1, "NVDA": 34.6, "AMD": 41.2, "QCOM": 15.8, "MRVL": 38.7},
                "best_in_class": "QCOM",
            },
            {
                "label": "Gross Margin",
                "higher_is_better": True,
                "values": {"AVGO": 68.5, "NVDA": 74.2, "AMD": 51.8, "QCOM": 56.3, "MRVL": 60.1},
                "best_in_class": "NVDA",
            },
            {
                "label": "FCF Margin",
                "higher_is_better": True,
                "values": {"AVGO": 38.9, "NVDA": 44.1, "AMD": 18.6, "QCOM": 29.4, "MRVL": 12.7},
                "best_in_class": "NVDA",
            },
            {
                "label": "ROIC",
                "higher_is_better": True,
                "values": {"AVGO": 15.2, "NVDA": 62.3, "AMD": 11.8, "QCOM": 24.6, "MRVL": 6.4},
                "best_in_class": "NVDA",
            },
            {
                "label": "Revenue Growth YoY",
                "higher_is_better": True,
                "values": {"AVGO": 22.0, "NVDA": 62.5, "AMD": 28.4, "QCOM": 11.2, "MRVL": 34.7},
                "best_in_class": "NVDA",
            },
        ],
    },
    "COST": {
        "peers": ["COST", "WMT", "TGT", "BJ", "AMZN"],
        "metrics": [
            {
                "label": "Fwd P/E",
                "higher_is_better": False,
                "values": {"COST": 46.2, "WMT": 32.1, "TGT": 12.4, "BJ": 21.6, "AMZN": 34.8},
                "best_in_class": "TGT",
            },
            {
                "label": "EV/EBITDA",
                "higher_is_better": False,
                "values": {"COST": 24.8, "WMT": 16.9, "TGT": 7.8, "BJ": 11.3, "AMZN": 18.2},
                "best_in_class": "TGT",
            },
            {
                "label": "Revenue per Square Foot",
                "higher_is_better": True,
                "values": {"COST": 1245, "WMT": 620, "TGT": 340, "BJ": 890, "AMZN": None},
                "best_in_class": "COST",
            },
            {
                "label": "Inventory Turnover",
                "higher_is_better": True,
                "values": {"COST": 12.8, "WMT": 8.9, "TGT": 6.1, "BJ": 10.2, "AMZN": 9.4},
                "best_in_class": "COST",
            },
            {
                "label": "Same-Store Sales Growth",
                "higher_is_better": True,
                "values": {"COST": 6.4, "WMT": 4.6, "TGT": 1.2, "BJ": 3.8, "AMZN": None},
                "best_in_class": "COST",
            },
            {
                "label": "Membership Renewal Rate",
                "higher_is_better": True,
                "values": {"COST": 89.8, "WMT": None, "TGT": None, "BJ": 87.5, "AMZN": None},
                "best_in_class": "COST",
            },
            {
                "label": "Operating Margin",
                "higher_is_better": True,
                "values": {"COST": 3.8, "WMT": 4.3, "TGT": 5.5, "BJ": 3.5, "AMZN": 6.2},
                "best_in_class": "AMZN",
            },
        ],
    },
    # TODO(user): none of these bank-native metrics (ROTCE, overhead ratio,
    # CET1, NIM, P/TBV) map onto LIVE_COMPS_METRICS, so all values here stay
    # hardcoded "Research estimate" rather than being live-overlaid like the
    # other three tickers. JPM's own figures (ROTCE 20%, overhead ratio 52%,
    # CET1 14.6%) are verified against the FY2025 10-K. Peer figures (BAC,
    # WFC, C, GS) are left as None placeholders — fill in from each bank's
    # own most recent 10-K/earnings release.
    "JPM": {
        "peers": ["JPM", "BAC", "WFC", "C", "GS"],
        "metrics": [
            {
                "label": "Fwd P/E",
                "higher_is_better": False,
                "values": {"JPM": None, "BAC": None, "WFC": None, "C": None, "GS": None},
                "best_in_class": None,
            },
            {
                "label": "Price / Tangible Book",
                "higher_is_better": False,
                "values": {"JPM": None, "BAC": None, "WFC": None, "C": None, "GS": None},
                "best_in_class": None,
            },
            {
                "label": "ROTCE",
                "higher_is_better": True,
                "values": {"JPM": 20.0, "BAC": None, "WFC": None, "C": None, "GS": None},
                "best_in_class": "JPM",
            },
            {
                "label": "Overhead (Efficiency) Ratio",
                "higher_is_better": False,
                "values": {"JPM": 52.0, "BAC": None, "WFC": None, "C": None, "GS": None},
                "best_in_class": "JPM",
            },
            {
                "label": "Net Interest Margin",
                "higher_is_better": True,
                "values": {"JPM": None, "BAC": None, "WFC": None, "C": None, "GS": None},
                "best_in_class": None,
            },
            {
                "label": "CET1 Capital Ratio",
                "higher_is_better": True,
                "values": {"JPM": 14.6, "BAC": None, "WFC": None, "C": None, "GS": None},
                "best_in_class": "JPM",
            },
        ],
    },
}
