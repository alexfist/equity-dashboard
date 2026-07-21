export type Ticker = "VRTX" | "AVGO" | "COST";

export interface CompanyInfo {
  ticker: Ticker;
  name: string;
  sector: string;
  exchange: string;
  cik: string;
  recommendation: "HOLD" | "INVESTIGATE";
  current_price: number;
}

export interface AnnualFinancials {
  fiscal_year_end: string;
  fiscal_year: number;
  revenue: number | null;
  net_income: number | null;
  operating_income: number | null;
  total_assets: number | null;
  total_debt: number | null;
  cash: number | null;
  capex: number | null;
  shares_outstanding: number | null;
  operating_margin: number | null;
  net_margin: number | null;
  fcf: number | null;
  roic: number | null;
}

export interface FinancialsResponse {
  ticker: Ticker;
  annual: AnnualFinancials[];
}

export interface DCFAssumptions {
  base_revenue: number;
  growth_rates: number[];
  ebitda_margin: number;
  da: number;
  capex: number;
  tax_rate: number;
  wacc: number;
  terminal_growth: number;
  net_cash: number | null;
  net_debt: number | null;
  shares: number;
  is_net_debt: boolean;
  exit_ebitda_multiple: number;
}

export interface CompsMetric {
  label: string;
  higher_is_better: boolean;
  values: Record<string, number | null>;
  best_in_class: string;
  source: string;
}

export interface CompsResponse {
  peers: string[];
  metrics: CompsMetric[];
  footnote: string;
}

export interface NewsArticle {
  headline: string;
  summary: string;
  source: string;
  url: string;
  datetime: number | null;
}

export interface NewsResponse {
  ticker: Ticker;
  articles: NewsArticle[];
}

export interface Filing {
  form: string;
  filing_date: string;
  description: string;
  url: string;
}

export interface FilingsResponse {
  ticker: Ticker;
  filings: Filing[];
}

export interface BusinessSummary {
  paragraphs: string[];
  source: string;
}

export interface Moat {
  type: string;
  strength: "WIDE" | "NARROW";
  description: string;
  source: string;
}

export interface CSuiteMember {
  name: string;
  role: string;
  tenure: string;
  strengths: string[];
  watch: string[];
}

export interface KeyQuote {
  quote: string;
  speaker: string;
  role: string;
}

export interface EarningsGuidance {
  revenue: string;
  growth: string;
  margin: string;
}

export interface EarningsEntry {
  period: string;
  date: string;
  summary: string;
  key_quotes: KeyQuote[];
  guidance: EarningsGuidance;
  risks_flagged: string[];
  source_url: string;
  source_label: string;
}

export interface RiskItem {
  title: string;
  description: string;
}

export interface Risks {
  items: RiskItem[];
  source: string;
}

export interface QualitativeResponse {
  business_summary: BusinessSummary;
  moat: Moat;
  risks: Risks;
  csuite: CSuiteMember[];
  earnings: EarningsEntry[];
}
