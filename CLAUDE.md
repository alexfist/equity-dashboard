Build a full-stack equity research dashboard.

TECH STACK:
- Frontend: React with Vite, TypeScript, Tailwind CSS, Recharts
- Backend: Python with FastAPI
- Data: SEC EDGAR API (https://data.sec.gov) for all quantitative 
  financial data — free, no API key, works globally

COMPANIES:
- VRTX (Vertex Pharmaceuticals, CIK 0000875320)
- AVGO (Broadcom, CIK 0001730168)
- COST (Costco, CIK 0000909832)

CHANGELOG:
- The project is version-controlled on GitHub with a manual CHANGELOG.md
  at the repo root, in Keep a Changelog format.
- Whenever a notable user-visible change is made, add an entry under the
  `[Unreleased]` heading at the top of CHANGELOG.md (grouped under Added /
  Changed / Fixed / Security as appropriate) before considering the change
  done.

PROJECT STRUCTURE:
- Root folder: equity-dashboard/
- frontend/ folder: React + Vite + TypeScript + Tailwind + Recharts
- backend/ folder: Python FastAPI
  - Create virtual environment: python -m venv venv
  - Activate it and install ALL dependencies inside venv only
  - Never install anything into global Python environment
  - Include requirements.txt
  - Include .env file with: FINNHUB_KEY=your_key_here
  - Include .env.example with same structure
  - Install python-dotenv so backend loads .env automatically
- Include README.md at root with step-by-step instructions to:
  - Activate the venv (source backend/venv/bin/activate)
  - Install backend dependencies (pip install -r requirements.txt)
  - Start the backend (uvicorn main:app --reload on port 8000)
  - Install frontend dependencies (npm install)
  - Start the frontend (npm run dev on port 5173)
- Include CORS configuration so frontend can talk to backend

BACKEND ENDPOINTS — all quantitative, all from SEC EDGAR:

1. GET /api/company/{ticker}
   - Return basic company info: name, sector, exchange, 
     CIK number, recommendation (hardcode: VRTX=HOLD, 
     AVGO=INVESTIGATE, COST=HOLD), current price estimate 
     (hardcode: VRTX=$490, AVGO=$250, COST=$920)

2. GET /api/financials/{ticker}
   - Fetch from SEC EDGAR company facts endpoint:
     https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json
   - Extract and return last 5 years of annual data:
     - Revenue (us-gaap/Revenues or 
       us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax)
     - Net Income (us-gaap/NetIncomeLoss)
     - Operating Income (us-gaap/OperatingIncomeLoss)
     - Total Assets (us-gaap/Assets)
     - Total Debt (us-gaap/LongTermDebt)
     - Cash (us-gaap/CashAndCashEquivalentsAtCarryingValue)
     - CapEx (us-gaap/PaymentsToAcquirePropertyPlantAndEquipment)
     - Shares Outstanding (us-gaap/CommonStockSharesOutstanding)
   - Calculate and return derived metrics:
     - Operating Margin = Operating Income / Revenue
     - Net Margin = Net Income / Revenue
     - FCF = Operating Income - CapEx (approximation)
     - ROIC = Net Income / (Total Assets - Current Liabilities)
   - Cache results for 24 hours to avoid hitting EDGAR repeatedly

3. GET /api/dcf/{ticker}
   - Return default DCF assumptions for each company:
     VRTX: baseRevenue=12.0, growthRates=[9,13,11,9,8], 
       ebitdaMargin=43, da=0.6, capex=0.45, taxRate=25, 
       wacc=8.5, terminalGrowth=3.0, netCash=12.3, 
       shares=0.254, isNetDebt=false, exitEbitdaMultiple=15.9
     AVGO: baseRevenue=63.9, growthRates=[20,18,14,12,8], 
       ebitdaMargin=65, da=5.5, capex=0.7, taxRate=15, 
       wacc=9.5, terminalGrowth=3.0, netDebt=51.0, 
       shares=4.83, isNetDebt=true, exitEbitdaMultiple=17.2
     COST: baseRevenue=280.4, growthRates=[8,7,7,6,6], 
       ebitdaMargin=4.2, da=2.8, capex=4.5, taxRate=25, 
       wacc=7.2, terminalGrowth=2.5, netDebt=1.2, 
       shares=0.444, isNetDebt=true, exitEbitdaMultiple=24.8
   - exitEbitdaMultiple defaults to each company's own current
     EV/EBITDA from the /api/comps/{ticker} peer table — used
     as the default Exit Multiple terminal value input in the
     frontend DCF model (Section 4)

4. GET /api/comps/{ticker}
   - Return sector-specific peer comparison data (hardcoded):

   VRTX peers (Biotech/Pharma) — REGN, ABBV, BMY, LLY:
   Metrics: Fwd P/E, EV/EBITDA, EV/Revenue, 
   R&D as % of Revenue, Net Margin, ROIC

   AVGO peers (Semiconductors) — NVDA, AMD, QCOM, MRVL:
   Metrics: Fwd P/E, EV/EBITDA, EV/FCF, 
   Gross Margin, FCF Margin, ROIC, Revenue Growth YoY

   COST peers (Retail) — WMT, TGT, BJ, AMZN:
   Metrics: Fwd P/E, EV/EBITDA, Revenue per Square Foot,
   Inventory Turnover, Same-Store Sales Growth, 
   Membership Renewal Rate (COST and BJ only), 
   Operating Margin

   Include a note field on each metric flagging which 
   company is best-in-class for that metric.

5. GET /api/news/{ticker}
   - Use Finnhub API to fetch 10 most recent news articles:
     https://finnhub.io/api/v1/company-news?symbol={ticker}&from={30_days_ago}&to={today}&token={FINNHUB_KEY}
   - Load FINNHUB_KEY from .env file using python-dotenv
   - Return: headline, summary, source, url, datetime
   - If Finnhub fails or returns empty, return empty array 
     gracefully without crashing

6. GET /api/filings/{ticker}
   - Fetch 5 most recent 8-K filings from SEC EDGAR:
     https://efts.sec.gov/LATEST/search-index?q=%22earnings%22&forms=8-K&entity={company_name}
   - Return: form type, filing date, description, 
     direct URL to filing on SEC EDGAR

FRONTEND PAGES AND COMPONENTS:

Layout:
- Dark theme throughout (background #0D1117, matching the 
  Bloomberg terminal aesthetic)
- Top navigation bar with app title "Equity Research Dashboard"
  and company selector tabs: VRTX | AVGO | COST
- Each company tab loads all sections below for that company

Section 1 — Company header:
- Ticker, company name, sector, exchange
- Recommendation badge, derived live from DCF upside/downside
  rather than the static hardcoded value:
  upside % = (intrinsicValue - currentPrice) / currentPrice
  - upside > +20% → BUY (green)
  - upside < -20% → SELL (red)
  - otherwise → HOLD (amber)
  - Falls back to the static /api/company/{ticker}
    `recommendation` field only while the DCF model/intrinsic
    value hasn't loaded yet
  - Recomputes in real time as the DCF sliders move, since
    intrinsicValue and currentPrice are already lifted into
    CompanyTab state
- Estimated current price and DCF base case target price
- Last updated timestamp

Section 2 — Key metrics cards (2x4 grid):
- Revenue, Net Income, FCF, Operating Margin, 
  Net Margin, ROIC, Net Cash/Debt, Shares Outstanding
- Pull from /api/financials/{ticker} — most recent year
- Each card shows current value and YoY change with 
  up/down arrow and color coding (green = good, red = bad)

Section 3 — Revenue and net income chart:
- Grouped bar chart, last 5 years
- Revenue bars in blue, net income bars in green
- X axis = fiscal year, Y axis = $B
- Pull from /api/financials/{ticker}
- Show a loading skeleton while data fetches

Section 4 — Interactive DCF model:
- Fetch default assumptions from /api/dcf/{ticker}
- Left panel: sliders for each assumption
  - Year 1-5 revenue growth rates (individual sliders, 
    0-40% range)
  - EBITDA margin (10-80%)
  - WACC (5-18%, step 0.5)
  - Terminal growth rate (1-5%, step 0.5)
  - Terminal Value Blend group:
    - Exit EV/EBITDA multiple (5-40x, step 0.5) — defaults
      to the subject company's own EV/EBITDA from
      /api/comps/{ticker} (VRTX 15.9x, AVGO 17.2x, COST 24.8x),
      served from /api/dcf/{ticker} as `exit_ebitda_multiple`
    - Weight: Gordon Growth vs. Exit Multiple (0-100%,
      step 5, defaults to 50%) — controls how the two
      terminal value models are blended
- Terminal value is computed from two models and blended
  by the weight slider rather than from Gordon Growth alone:
  - Gordon Growth: FCF_year5 * (1 + terminalGrowth) / (WACC - terminalGrowth)
  - Exit Multiple: EBITDA_year5 * exitMultiple
  - blendedTV = gordonTV * (weight/100) + exitMultipleTV * (1 - weight/100)
  - weight=100 reduces to pure Gordon Growth; weight=0 reduces
    to pure Exit Multiple
- Right panel: live output table showing
  - Year by year revenue and FCF projections
  - PV of FCFs
  - Terminal value breakdown: Gordon Growth component and
    Exit Multiple component (both shown at their current
    weights), plus the blended PV of terminal value
  - Enterprise value
  - Plus/minus net cash or net debt
  - Equity value
  - Intrinsic value per share (large, prominent)
  - Upside/downside % vs current price 
    (green if upside, red if downside)
- All calculations happen client-side in React for 
  instant response — do not call backend for DCF math
- Include an editable current price input field

Section 5 — Peer comps table:
- Pull from /api/comps/{ticker}
- Highlight the subject company row in a distinct color
- Color code each metric cell: 
  green = top quartile, amber = middle, red = bottom
- Show best-in-class indicator on the winning cell 
  for each metric column
- Include a footnote: "Source: Research estimates, 
  July 2026. Peer data hardcoded."

Get everything running locally. Make sure:
- Backend starts without errors on port 8000
- Frontend starts without errors on port 5173  
- /api/financials/VRTX returns real data from SEC EDGAR
- The DCF sliders update the intrinsic value in real time
- The revenue chart renders with real data

Dev servers are launched via .claude/launch.json ("frontend"
and "backend" configs). Both ports are pinned with
autoPort: false — port 5173 is required because the backend's
CORS `allow_origins` is hardcoded to http://localhost:5173,
and port 8000 is required because the frontend's API client
is hardcoded to call http://localhost:8000. Free those ports
(kill any stray process) rather than letting either server
auto-select a different one.

Add the following qualitative sections to the existing 
equity research dashboard. Do not modify any existing 
quantitative functionality — only add new sections.

BACKEND — new endpoint:

GET /api/qualitative/{ticker}
- Hardcode all data in a separate qualitative_data.py file
- Add a comment at the top: 
  "Update earnings summaries manually. 
   Generate new summaries in Claude at claude.ai 
   and paste them here."
- Return structured JSON with these fields:
  business_summary, moat, csuite, earnings, 
  each structured as described below

QUALITATIVE DATA — hardcode exactly as follows:

Style: no dashes as sentence punctuation anywhere in this
qualitative content (hyphens in compound words like
"10-year" or "non-opioid" are fine). Write for an average
retail investor: explain acronyms and jargon in plain
language on first use, spell out numbers where it reads
more naturally.

─── VRTX ───────────────────────────────────────────

business_summary:
  paragraphs: [
    "Vertex Pharmaceuticals holds a near-monopoly in 
     cystic fibrosis (CF) treatment through its CFTR 
     modulator drugs, Trikafta and the newer once-daily 
     Alyftrek (approved December 2024). These drugs cover 
     about 90% of eligible CF patients globally. Fiscal 
     year 2025 revenue reached $12.0 billion at a 33% net 
     margin, and the company holds $12.3 billion in net 
     cash with effectively no debt, making it one of the 
     strongest balance sheets in large-cap biotech.",
    "Vertex is using its CF cash flow to fund three new 
     treatment areas at once. In pain, Journavx was 
     approved by the FDA in January 2025 as the first 
     non-opioid pill for acute pain. In kidney disease, 
     povetacicept has an application filed with the FDA 
     as of Q1 2026 and has been granted Breakthrough 
     Therapy status for a condition called IgA nephropathy. 
     In blood disorders, Casgevy is a gene-editing therapy, 
     using CRISPR technology, approved in 2023 for sickle 
     cell disease and beta-thalassemia. Management is 
     trying to repeat the CF playbook in each new area: 
     strong science, careful clinical execution, and 
     premium pricing that comes with limited competition.",
    "The key question for investors is whether Vertex's 
     edge in CF treatment carries over to these new disease 
     areas. Journavx and povetacicept rely on similar types 
     of drug science that Vertex already knows well. Casgevy 
     and the company's stem cell program for type 1 diabetes 
     are a bigger stretch, since they use technology Vertex 
     has not worked with as extensively. Casgevy's slow 
     sales ramp so far is an early sign that these newer 
     bets may face challenges the company cannot fully 
     control."
  ]
  source: "Research · July 2026"

moat:
  type: "Intangible Assets + Efficient Scale"
  strength: "WIDE"
  description: "Vertex has spent more than 20 years 
    building deep scientific knowledge of the CFTR protein 
    that competitors cannot easily copy. This is not just 
    about patents, it is accumulated expertise that is hard 
    to replicate. No competitor has successfully challenged 
    Vertex's dominance in CF treatment in two decades 
    despite real attempts. The CF patient population is 
    large enough to support Vertex's business but not large 
    enough to justify a rival spending 20 years catching 
    up, which is a classic case of a market too small for 
    two winners. The newer programs in pain and kidney 
    disease draw on Vertex's chemistry expertise but have 
    not yet built the same kind of structural advantage."
  source: "Research · July 2026"

csuite: [
  {
    name: "Reshma Kewalramani",
    role: "CEO & President",
    tenure: "Since April 2020",
    strengths: [
      "Trained as a nephrologist (kidney specialist), 
       directly relevant to the povetacicept kidney 
       disease program",
      "Personally bought 10,000 shares at about $390 in 
       August 2025, a meaningful signal of insider 
       confidence",
      "92.4% of her compensation is tied to stock 
       performance",
      "Ended the VX-264 type 1 diabetes device program in 
       2025 when the data was not compelling, showing 
       discipline rather than sticking with a program for 
       its own sake"
    ],
    watch: [
      "As a trained nephrologist who championed the $4.6 
       billion Alpine acquisition that brought in 
       povetacicept, she has a personal connection to the 
       kidney disease program. That could bias capital 
       allocation decisions if commercial signals turn 
       negative",
      "She is managing three commercial launches at once 
       (Journavx, Casgevy, and Alyftrek), four late-stage 
       trials, and two C-suite leadership transitions at 
       the same time"
    ]
  },
  {
    name: "Charlie Wagner",
    role: "CFO + COO (dual role)",
    tenure: "CFO since 2019, added COO mid-2025",
    strengths: [
      "Guided revenue growth from $3B to $13B since 
       joining",
      "Has a track record of scaling multiple healthcare 
       companies",
      "Describes himself as energized by complexity and 
       operational challenges"
    ],
    watch: [
      "Now holds both the CFO and COO roles at the 
       company's most operationally complex moment, which 
       raises bandwidth concerns",
      "At most large pharma companies, these are two 
       separate jobs for a reason"
    ]
  },
  {
    name: "Mark Bunnage",
    role: "CSO (incoming, effective Feb 2026)",
    tenure: "SVP Global Research since 2016",
    strengths: [
      "A 10-year Vertex insider deeply embedded in the 
       company's clinical research culture",
      "Led the due diligence team that evaluated the 
       Alpine acquisition, which brought povetacicept, one 
       of the pipeline's most promising assets, to Vertex",
      "Multiple programs advanced to clinical trials under 
       his research leadership, including Casgevy, 
       Journavx, and other next-generation molecules"
    ],
    watch: [
      "He is stepping into the role held by David 
       Altshuler, who built the company's entire 
       commercial portfolio over 13 years",
      "He is unproven as chief scientific officer at this 
       scale. He has been a strong second-in-command in 
       research, but it is unclear if he can originate 
       future programs at the same rate"
    ]
  }
]

earnings: [
  {
    period: "Q1 2026",
    date: "April 2026",
    summary: "CEO Kewalramani highlighted continued 
      strength in the CF franchise, with Alyftrek adoption 
      ramping faster than expected. The rolling application 
      for povetacicept remains on track, and management 
      expressed high confidence in FDA approval by Q4 2026. 
      Journavx prescription volume tripled compared to the 
      2025 pace, though insurance coverage is still 
      expanding and remains the main factor limiting sales 
      growth. The leadership transition from Altshuler to 
      Bunnage in the chief scientific officer role is 
      described as proceeding smoothly, though analysts 
      pressed management on the risk to pipeline 
      continuity.",
    key_quotes: [
      {
        quote: "Alyftrek is converting faster than we 
          modeled. The once-daily profile is resonating 
          with both patients and physicians.",
        speaker: "Reshma Kewalramani",
        role: "CEO"
      },
      {
        quote: "The rolling BLA for povetacicept is on 
          track. We remain highly confident in the 
          strength of the RAINIER data and the pathway 
          to approval.",
        speaker: "Reshma Kewalramani",
        role: "CEO"
      }
    ],
    guidance: {
      revenue: "$12.95 to $13.1 billion",
      growth: "About 8 to 9% year over year",
      margin: "Non-GAAP operating margin about 43 to 44%"
    },
    risks_flagged: [
      "Insurance coverage for Journavx is still expanding, 
       and that remains the main factor limiting sales 
       growth",
      "Analysts flagged continuity risk from the chief 
       scientific officer transition",
      "Two-year kidney function data needed to confirm 
       povetacicept's results is still pending"
    ],
    source_url: "https://investors.vrtx.com",
    source_label: "Vertex Investor Relations · Q1 2026"
  }
]

─── AVGO ───────────────────────────────────────────

business_summary:
  paragraphs: [
    "Broadcom runs two business segments with different 
     but complementary strengths. Semiconductor Solutions, 
     about 61% of fiscal 2025 revenue, designs custom AI 
     chips in close partnership with Google, Meta, and 
     Apple. It also dominates the networking chips that 
     connect AI data center hardware together, through its 
     Tomahawk and Jericho product lines. Infrastructure 
     Software, about 39% of revenue, includes VMware, a 
     virtualization platform used by enterprise IT 
     departments (acquired in November 2023 for $69 
     billion), and CA Technologies mainframe software. 
     Both software businesses benefit from customers who 
     find it costly and disruptive to switch providers.",
    "Fiscal 2025 results: revenue of $63.9 billion, free 
     cash flow of $26.9 billion, and EBITDA margins above 
     65%. AI chip revenue reached about $20 billion in 
     fiscal 2025, growing more than 100% year over year, 
     driven by rising demand from large cloud computing 
     customers. Management has guided to a fiscal 2027 AI 
     market opportunity of $60 to 90 billion from just five 
     large customers, three existing and two new ones 
     starting in fiscal 2026. Guidance for Q1 fiscal 2026 
     AI chip revenue of $8.2 billion represents roughly 
     100% year over year growth continuing.",
    "The core debate for investors: Broadcom's chip 
     business has a genuine structural advantage because 
     designing custom chips with a customer creates deep, 
     sticky partnerships that are hard to displace. The 
     software business has similarly strong customer 
     lock-in, but it also carries real regulatory risk from 
     the EU and litigation from enterprise customers over 
     VMware's pricing changes. The stock trades at 19.8 
     times forward earnings versus a semiconductor sector 
     median of 36.3 times. That discount reflects two 
     specific investor concerns: possible EU regulatory 
     action on VMware, and the unresolved question of who 
     succeeds CEO Hock Tan, who is over 73."
  ]
  source: "Research · July 2026"

moat:
  type: "Switching Costs (dual: semiconductor + software)"
  strength: "WIDE"
  description: "Broadcom's custom chip partnerships with 
    Google, Meta, and Apple would take a competitor an 
    estimated three to five years to replicate, because 
    these are multi-year engineering collaborations rather 
    than simple vendor contracts. The Tomahawk and Jericho 
    networking chips carry similar lock-in within AI data 
    centers. On the software side, VMware and CA mainframe 
    software are embedded so deeply in enterprise IT 
    systems that switching realistically takes years. A 
    lawsuit filed by UnitedHealthcare explicitly stated 
    that moving to alternative mainframe software would 
    take years, which is exactly the kind of switching 
    cost this moat depends on."
  source: "Research · July 2026"

csuite: [
  {
    name: "Hock Tan",
    role: "President & CEO",
    tenure: "Since 2006",
    strengths: [
      "Built a $5 billion company (Avago) into a $1.5 
       trillion company (Broadcom) through disciplined 
       acquisitions over 19 years",
      "Shows extreme capital discipline. He walked away 
       from the Qualcomm deal when regulatory conditions 
       turned unfavorable rather than overpaying to get it 
       done",
      "Has consistently delivered on every financial 
       commitment made publicly, which is rare among 
       large-cap tech companies",
      "Focused on free cash flow as an operator. EBITDA 
       margins expanded from 55% to over 65% under his 
       leadership",
      "Recently joined Meta's board, a sign of his 
       continued relevance in the AI industry"
    ],
    watch: [
      "He is over 73 years old, and no public succession 
       plan has been identified anywhere in analyst 
       coverage. This is one of the most underweighted 
       risks by the market",
      "VMware's pricing strategy, which raised prices 800 
       to 1,500% for some customers, triggered lawsuits 
       from AT&T and UnitedHealthcare and an EU regulatory 
       inquiry. It is controversial but intentional, and 
       the cash flow results support the strategy so far",
      "The hostile Qualcomm bid in 2017 to 2018 was 
       blocked by the Trump administration on national 
       security grounds. Since then, Broadcom has stuck to 
       negotiated deals only",
      "The company has been shaped almost entirely by 
       Tan's personal acquisition strategy, which makes 
       succession risk existential rather than just 
       operational"
    ]
  },
  {
    name: "Kirsten Spears",
    role: "CFO",
    tenure: "Since 2016",
    strengths: [
      "Communicates consistently and clearly about free 
       cash flow",
      "Strong operational execution across several large 
       acquisitions, including the VMware integration",
      "Has a clear and disciplined track record on 
       guidance"
    ],
    watch: [
      "Has a lower public profile than Tan outside of 
       financial reporting, so her strategic vision is 
       less visible"
    ]
  }
]

earnings: [
  {
    period: "Q3 FY2025",
    date: "September 2025",
    summary: "Record quarterly revenue was driven by 
      continued acceleration in AI chip demand and 
      progress integrating VMware. CEO Tan guided Q4 AI 
      chip revenue to $6.2 billion, marking eleven 
      consecutive quarters of AI revenue growth. VMware 
      software revenue growth is accelerating as 
      enterprise customers move to subscription bundles. 
      EBITDA margins continue to expand to new records. 
      Analysts pressed management on EU regulatory risk 
      around VMware. Management pointed to 87% of its top 
      10,000 customers signing up for the new bundles as 
      evidence that the pricing model is holding up.",
    key_quotes: [
      {
        quote: "Q3 AI revenue growth accelerated to 63% 
          year-over-year to $5.2 billion. We expect 
          growth in AI semiconductor revenue to 
          accelerate to $6.2 billion in Q4, delivering 
          eleven consecutive quarters of growth.",
        speaker: "Hock Tan",
        role: "CEO"
      },
      {
        quote: "Consolidated revenue grew 22% 
          year-over-year to a record $16.0 billion.",
        speaker: "Hock Tan",
        role: "CEO"
      }
    ],
    guidance: {
      revenue: "$19.1 billion for Q1 fiscal 2026",
      growth: "About 22% year over year, consolidated",
      margin: "67% adjusted EBITDA margin guided for Q1 
        fiscal 2026"
    },
    risks_flagged: [
      "Possible EU regulatory action on VMware pricing, 
       including inquiry risk from the European Commission",
      "Third-party analysts have flagged the risk that AI 
       capital spending by customers could peak in the 
       second half of 2026",
      "AI chip revenue is concentrated among a small 
       number of large cloud computing customers"
    ],
    source_url: "https://investors.broadcom.com",
    source_label: "Broadcom Investor Relations · Q3 FY2025"
  }
]

─── COST ───────────────────────────────────────────

business_summary:
  paragraphs: [
    "Costco runs a membership warehouse retail model built 
     on deliberate limits and scale. Carrying only about 
     5,000 products, compared to over 30,000 at a typical 
     supermarket, gives Costco extraordinary purchasing 
     power and fast inventory turnover. Its Kirkland 
     Signature private label matches or beats national 
     brands in quality at 15 to 20% lower prices. This 
     deepens member loyalty and compresses gross margin in 
     a way that actually strengthens the moat, because it 
     makes Costco's value proposition impossible for 
     traditional retailers to match without hurting their 
     own profits.",
    "The membership fee is the financial engine of the 
     business. Annual membership fees, $5.32 billion in 
     fiscal 2025, flow almost entirely to the bottom line 
     and represent about 50% of total operating income 
     despite being less than 2% of total revenue. The 
     89.8% renewal rate is not just a satisfaction metric. 
     It reflects real switching costs built into the 
     membership relationship. Fiscal 2025 total revenue 
     reached $280.4 billion, a 10-year revenue growth rate 
     of about 9.2% per year. The September 2024 membership 
     fee increase, from $60 to $65 for standard members and 
     $110 to $130 for executive members, was absorbed with 
     minimal member loss.",
    "Fiscal 2026 headwinds are real but manageable given 
     Costco's cost structure. Tariff uncertainty is being 
     addressed through Kirkland Signature expansion and 
     diversifying suppliers across more countries. Wage 
     pressure, with the top pay scale now at $31.90 per 
     hour, flows through operating expenses but is partly 
     offset by the efficiency of the warehouse format. 
     Internationally, 35 new warehouses are planned for 
     fiscal 2026, and e-commerce sales grew 22.6% in Q2 
     fiscal 2026."
  ]
  source: "Research · July 2026"

moat:
  type: "Cost Advantage + Switching Costs"
  strength: "WIDE"
  description: "The 5,000-product discipline and warehouse 
    format create a structural cost advantage that 
    traditional retailers cannot match even with unlimited 
    capital, because matching it would require abandoning 
    how conventional retail operates. The membership fee 
    also creates a psychological switching cost. Members 
    who have paid $65 to $130 for annual access are 
    motivated to keep shopping at Costco to get their 
    money's worth, which creates loyalty that goes beyond 
    rational price comparison. The treasure hunt shopping 
    experience and Kirkland Signature quality are both 
    genuinely difficult for competitors to replicate at 
    scale."
  source: "Research · July 2026"

csuite: [
  {
    name: "Ron Vachris",
    role: "President & CEO",
    tenure: "Since January 2024",
    strengths: [
      "A 40-year company veteran who started as a teenage 
       forklift driver, giving him about as deep a 
       connection to Costco's culture as anyone could have",
      "Only the third CEO in Costco's history, providing 
       continuity with the company's founding philosophy",
      "$10.6M of his $12.2M total compensation is tied to 
       pre-tax income performance goals, showing strong 
       alignment with shareholders",
      "Maintained the company's diversity commitments 
       under shareholder pressure, with 98% shareholder 
       support on the pay vote"
    ],
    watch: [
      "This is his first CEO tenure navigating a genuinely 
       complex macro environment, with tariffs, energy 
       costs tied to conflict in the Middle East, and wage 
       inflation all happening at once",
      "He communicates less publicly than peer CEOs, and 
       his style is more operational than visionary",
      "Navigating tariffs will test him in ways his 
       predecessor, Craig Jelinek, never had to face"
    ]
  },
  {
    name: "Gary Millerchip",
    role: "CFO",
    tenure: "Since 2018",
    strengths: [
      "Proactively discloses headwinds, including flagging 
       wage costs and Middle East energy risk directly on 
       earnings calls",
      "A clear communicator on cost structure and 
       membership economics"
    ],
    watch: [
      "The company's tariff pass-through strategy is still 
       being worked out and has not yet been fully 
       explained to investors"
    ]
  }
]

earnings: [
  {
    period: "Q3 FY2026",
    date: "June 2026",
    summary: "CEO Vachris highlighted tariff headwinds 
      being actively managed through Kirkland Signature 
      expansion, with more than 30 new items added in Q4, 
      and supplier diversification across more countries. 
      The membership renewal rate held steady at 89.8%, 
      even after the September 2024 fee increase fully 
      cycled through. E-commerce sales grew 22.6% in Q2, 
      accelerating from prior quarters. Wage costs, with 
      the top pay scale raised to $31.90 per hour, were 
      explicitly flagged as an ongoing expense pressure. 
      International expansion remains on track, with 35 
      new warehouses planned for the full fiscal year.",
    key_quotes: [
      {
        quote: "Our members continue to show remarkable 
          loyalty. The renewal rate holding at 89.8% 
          after the fee increase tells you everything 
          about the value proposition we deliver.",
        speaker: "Ron Vachris",
        role: "CEO"
      },
      {
        quote: "The future impact of tariffs remains 
          extremely fluid. What I can tell you is that 
          our buying team and Kirkland Signature 
          capabilities give us tools most retailers 
          simply do not have.",
        speaker: "Ron Vachris",
        role: "CEO"
      }
    ],
    guidance: {
      revenue: "$295 to $305 billion estimated for fiscal 
        2026",
      growth: "About 7 to 8% year over year",
      margin: "Operating margin of about 3.5 to 3.7%"
    },
    risks_flagged: [
      "The impact of tariffs on merchandise costs remains 
       fluid and difficult to quantify precisely",
      "Wage inflation, with the top pay scale at $31.90 
       per hour, is an ongoing expense pressure",
      "CFO Millerchip flagged energy cost risk tied to 
       conflict in the Middle East"
    ],
    source_url: "https://investor.costco.com",
    source_label: "Costco Investor Relations · Q3 FY2026"
  }
]

─── FRONTEND — qualitative sections ────────────────

Add the following sections to each company tab, 
below the existing quantitative sections. Pull all 
data from GET /api/qualitative/{ticker}.

Section 6 — Business summary:
- Display as 3 paragraphs in a clean card
- Citation badge: "Research · July 2026" in gray
- Section header: "Business Overview"

Section 7 — Moat assessment:
- Display moat type and strength rating as badges 
  (WIDE = green, NARROW = amber)
- Display description paragraph below
- Citation badge in gray
- Section header: "Economic Moat"

Section 8 — C-suite assessment:
- One card per executive
- Show name, role, tenure
- Strengths as a bulleted green list with checkmark icons
- Watch items as a bulleted amber list with 
  warning icons
- Section header: "C-Suite Assessment"

Section 9 — Latest earnings call:
- Show period and date as header
- Summary paragraph in a card
- Key quotes displayed as styled pull-quote blocks 
  with speaker name and role beneath each quote
- Guidance numbers in a small 3-column metrics row
- Risks flagged as a list with red warning badges
- Source link at bottom: 
  "[source_label] →" linking to source_url
- Section header: "Latest Earnings"

Section 10 — Recent news (from Finnhub):
- Fetch from /api/news/{ticker}
- Display as 5 article cards showing:
  headline (bold), 2-sentence summary, source name 
  (green badge), date, "Read full article →" link
- If no news: clean empty state message
- Section header: "Recent News"
- Subtle "Via Finnhub" attribution in section header

Section 11 — Recent SEC filings:
- Fetch from /api/filings/{ticker}
- Display as a simple list: 
  form type badge | date | description | "View →" link
- Source badge: "SEC EDGAR · Live" in blue
- Section header: "Recent SEC Filings"

CITATION RULES throughout qualitative sections:
- SEC EDGAR quantitative data: blue badge "SEC EDGAR"
- Finnhub news: green badge "Via Finnhub"
- Hardcoded research data: gray badge "Research · July 2026"
- Earnings summaries: gray badge with last-updated date
- Every section must have at least one visible 
  source attribution

Do not modify any existing quantitative functionality. 
Only add new sections below existing ones.