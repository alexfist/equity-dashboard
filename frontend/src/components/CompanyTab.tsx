import { useEffect, useState } from "react";
import { api } from "../api";
import type {
  CompanyInfo,
  CompsResponse,
  DCFAssumptions,
  FilingsResponse,
  FinancialsResponse,
  NewsResponse,
  QualitativeResponse,
  Ticker,
} from "../types";
import { CompanyHeader } from "./CompanyHeader";
import { MetricsGrid } from "./MetricsGrid";
import { RevenueChart, RevenueChartSkeleton } from "./RevenueChart";
import { DCFModel } from "./DCFModel";
import { CompsTable } from "./CompsTable";
import { BusinessOverview, MoatAssessment } from "./BusinessOverview";
import { CSuite } from "./CSuite";
import { Earnings } from "./Earnings";
import { NewsFeed } from "./NewsFeed";
import { SecFilings } from "./SecFilings";

export function CompanyTab({ ticker }: { ticker: Ticker }) {
  const [company, setCompany] = useState<CompanyInfo | null>(null);
  const [financials, setFinancials] = useState<FinancialsResponse | null>(null);
  const [dcf, setDcf] = useState<DCFAssumptions | null>(null);
  const [comps, setComps] = useState<CompsResponse | null>(null);
  const [intrinsicValue, setIntrinsicValue] = useState<number | null>(null);
  const [currentPrice, setCurrentPrice] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Qualitative sections (Part 3) — fetched independently so a failure here
  // never blanks the quantitative sections above (Part 1/2 are untouched).
  const [qualitative, setQualitative] = useState<QualitativeResponse | null>(null);
  const [news, setNews] = useState<NewsResponse | null>(null);
  const [filings, setFilings] = useState<FilingsResponse | null>(null);

  useEffect(() => {
    let cancelled = false;
    setCompany(null);
    setFinancials(null);
    setDcf(null);
    setComps(null);
    setIntrinsicValue(null);
    setCurrentPrice(null);
    setError(null);

    Promise.all([
      api.company(ticker),
      api.financials(ticker),
      api.dcf(ticker),
      api.comps(ticker),
    ])
      .then(([c, f, d, cp]) => {
        if (cancelled) return;
        setCompany(c);
        setFinancials(f);
        setDcf(d);
        setComps(cp);
      })
      .catch((err) => {
        if (!cancelled) setError(String(err));
      });

    return () => {
      cancelled = true;
    };
  }, [ticker]);

  useEffect(() => {
    let cancelled = false;
    setQualitative(null);
    setNews(null);
    setFilings(null);

    api.qualitative(ticker).then((q) => !cancelled && setQualitative(q)).catch(() => {});
    api.news(ticker).then((n) => !cancelled && setNews(n)).catch(() => {});
    api.filings(ticker).then((fl) => !cancelled && setFilings(fl)).catch(() => {});

    return () => {
      cancelled = true;
    };
  }, [ticker]);

  if (error) {
    return (
      <div className="rounded-lg border border-accent-red/30 bg-accent-red/10 p-6 text-accent-red">
        Failed to load data for {ticker}: {error}. Is the backend running on port 8000?
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {company ? (
        <CompanyHeader
          company={company}
          intrinsicValue={intrinsicValue}
          currentPrice={currentPrice ?? company.current_price}
        />
      ) : (
        <div className="h-32 animate-pulse rounded-lg bg-white/5" />
      )}

      {financials ? (
        <MetricsGrid annual={financials.annual} />
      ) : (
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-20 animate-pulse rounded-lg bg-white/5" />
          ))}
        </div>
      )}

      {financials ? <RevenueChart annual={financials.annual} /> : <RevenueChartSkeleton />}

      {dcf && company ? (
        <DCFModel
          assumptions={dcf}
          initialPrice={company.current_price}
          onIntrinsicValueChange={setIntrinsicValue}
          onCurrentPriceChange={setCurrentPrice}
        />
      ) : (
        <div className="h-96 animate-pulse rounded-lg bg-white/5" />
      )}

      {comps ? (
        <CompsTable ticker={ticker} comps={comps} />
      ) : (
        <div className="h-64 animate-pulse rounded-lg bg-white/5" />
      )}

      {/* --- Qualitative sections (Part 3) --- */}
      {qualitative && <BusinessOverview businessSummary={qualitative.business_summary} />}
      {qualitative && <MoatAssessment moat={qualitative.moat} />}
      {qualitative && <CSuite csuite={qualitative.csuite} />}
      {qualitative && <Earnings earnings={qualitative.earnings} />}
      {news && <NewsFeed articles={news.articles} />}
      {filings && <SecFilings filings={filings.filings} />}
    </div>
  );
}
