import type {
  CompanyInfo,
  CompsResponse,
  DCFAssumptions,
  FilingsResponse,
  FinancialsResponse,
  NewsResponse,
  QualitativeResponse,
  Ticker,
} from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    throw new Error(`${path} failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  company: (ticker: Ticker) => get<CompanyInfo>(`/api/company/${ticker}`),
  financials: (ticker: Ticker) => get<FinancialsResponse>(`/api/financials/${ticker}`),
  dcf: (ticker: Ticker) => get<DCFAssumptions>(`/api/dcf/${ticker}`),
  comps: (ticker: Ticker) => get<CompsResponse>(`/api/comps/${ticker}`),
  news: (ticker: Ticker) => get<NewsResponse>(`/api/news/${ticker}`),
  filings: (ticker: Ticker) => get<FilingsResponse>(`/api/filings/${ticker}`),
  qualitative: (ticker: Ticker) => get<QualitativeResponse>(`/api/qualitative/${ticker}`),
};
