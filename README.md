# Equity Research Dashboard

A full-stack equity research dashboard covering VRTX (Vertex Pharmaceuticals), AVGO (Broadcom), and COST (Costco). Quantitative financials are pulled live from SEC EDGAR; peer comps and DCF assumptions are hardcoded research inputs; the interactive DCF model runs entirely client-side.

## Screenshots

![VRTX dashboard: company header, key metrics, revenue chart, interactive DCF model, peer comps, and qualitative research sections](docs/screenshots/dashboard-overview.png)

## Prerequisites

- Python 3.10+
- Node.js 18+

## Setup

### 1. Backend

```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your Finnhub API key to `backend/.env` before starting the server (news will gracefully return empty results without one, but nothing will crash):

```sh
cp .env.example .env
# then edit .env and set FINNHUB_KEY=<your key>
```

Start the backend:

```sh
uvicorn main:app --reload --port 8000
```

The API is now live at `http://localhost:8000`. Quick check:

```sh
curl http://localhost:8000/api/financials/VRTX
```

### 2. Frontend

In a separate terminal:

```sh
cd frontend
npm install
npm run dev
```

The dashboard is now live at `http://localhost:5173`.

## Project structure

```
equity-dashboard/
├── backend/
│   ├── main.py              FastAPI app, CORS, route wiring
│   ├── company_data.py      Hardcoded company info, DCF assumptions, peer comps
│   ├── financials.py        SEC EDGAR company-facts fetch + 24h cache + metric derivation
│   ├── sec_edgar.py         Ticker→CIK resolution + recent 8-K filings (live EDGAR)
│   ├── finnhub_client.py    Recent company news (live Finnhub)
│   ├── requirements.txt
│   ├── .env / .env.example
│   └── venv/                 (created locally, gitignored)
├── frontend/
│   ├── src/
│   │   ├── api.ts            Backend fetch client
│   │   ├── types.ts          Shared TS types mirroring backend response shapes
│   │   ├── lib/dcf.ts         Pure client-side DCF calculation
│   │   ├── lib/format.ts      Number/date formatting helpers
│   │   └── components/        Nav, CompanyHeader, MetricsGrid, RevenueChart, DCFModel, CompsTable, CompanyTab
│   └── vite.config.ts
└── README.md
```

## Backend endpoints

| Endpoint | Source |
|---|---|
| `GET /api/company/{ticker}` | Hardcoded |
| `GET /api/financials/{ticker}` | Live SEC EDGAR (`data.sec.gov/api/xbrl/companyfacts`), cached 24h |
| `GET /api/dcf/{ticker}` | Hardcoded DCF assumptions |
| `GET /api/comps/{ticker}` | Hardcoded peer comps (research estimates) |
| `GET /api/news/{ticker}` | Live Finnhub (`company-news`) |
| `GET /api/filings/{ticker}` | Live SEC EDGAR (`data.sec.gov/submissions`) |

Tickers: `VRTX`, `AVGO`, `COST`.

## Notes

- SEC EDGAR requires a descriptive `User-Agent` header on every request — this is set in `backend/sec_edgar.py` and reused by `financials.py`.
- All EDGAR/Finnhub calls fail gracefully (empty list / null fields), never crash the request.
- The DCF model's sliders (growth rates, EBITDA margin, WACC, terminal growth) recompute the full projection client-side in `frontend/src/lib/dcf.ts` — no backend round-trip.
