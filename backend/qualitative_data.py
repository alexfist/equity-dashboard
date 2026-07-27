# Update earnings summaries manually.
# Generate new summaries in Claude at claude.ai and paste them here.

QUALITATIVE_DATA = {
    "VRTX": {
        "business_summary": {
            "paragraphs": [
                "Vertex Pharmaceuticals holds a near-monopoly in cystic fibrosis (CF) treatment "
                "through its CFTR modulator drugs, Trikafta and the newer once-daily Alyftrek "
                "(approved December 2024). These drugs cover about 90% of eligible CF patients "
                "globally. Fiscal year 2025 revenue reached $12.0 billion at a 33% net margin, and "
                "the company holds $12.3 billion in net cash with effectively no debt, making it "
                "one of the strongest balance sheets in large-cap biotech.",
                "Vertex is using its CF cash flow to fund three new treatment areas at once. In "
                "pain, Journavx was approved by the FDA in January 2025 as the first non-opioid "
                "pill for acute pain. In kidney disease, povetacicept has an application filed with "
                "the FDA as of Q1 2026 and has been granted Breakthrough Therapy status for a "
                "condition called IgA nephropathy. In blood disorders, Casgevy is a gene-editing "
                "therapy, using CRISPR technology, approved in 2023 for sickle cell disease and "
                "beta-thalassemia. Management is trying to repeat the CF playbook in each new area: "
                "strong science, careful clinical execution, and premium pricing that comes with "
                "limited competition.",
                "The key question for investors is whether Vertex's edge in CF treatment carries "
                "over to these new disease areas. Journavx and povetacicept rely on similar types "
                "of drug science that Vertex already knows well. Casgevy and the company's stem "
                "cell program for type 1 diabetes are a bigger stretch, since they use technology "
                "Vertex has not worked with as extensively. Casgevy's slow sales ramp so far is an "
                "early sign that these newer bets may face challenges the company cannot fully "
                "control.",
            ],
            "source": "Research · July 2026",
        },
        "moat": {
            "type": "Intangible Assets + Efficient Scale",
            "strength": "WIDE",
            "description": (
                "Vertex has spent more than 20 years building deep scientific knowledge of the "
                "CFTR protein that competitors cannot easily copy. This is not just about patents, "
                "it is accumulated expertise that is hard to replicate. No competitor has "
                "successfully challenged Vertex's dominance in CF treatment in two decades despite "
                "real attempts. The CF patient population is large enough to support Vertex's "
                "business but not large enough to justify a rival spending 20 years catching up, "
                "which is a classic case of a market too small for two winners. The newer programs "
                "in pain and kidney disease draw on Vertex's chemistry expertise but have not yet "
                "built the same kind of structural advantage."
            ),
            "source": "Research · July 2026",
        },
        "risks": {
            "items": [
                {
                    "title": "Revenue is still concentrated in one franchise",
                    "description": (
                        "Nearly all of Vertex's current revenue comes from its cystic fibrosis "
                        "drugs, Trikafta and Alyftrek. A diversified pharma company can absorb a "
                        "setback in one drug because others carry the business. Vertex cannot yet "
                        "do that. A new competing therapy, a patent challenge, or a manufacturing "
                        "problem affecting the CF franchise would hit the company's results much "
                        "harder than it would a more diversified peer."
                    ),
                },
                {
                    "title": "The new franchises are still unproven commercially",
                    "description": (
                        "Journavx, Casgevy, and povetacicept are all early in their commercial "
                        "lives, and povetacicept's approval was still pending as of Q1 2026. Each "
                        "depends on physicians prescribing it, insurers agreeing to cover it, and "
                        "in povetacicept's case, regulators approving it, none of which Vertex "
                        "fully controls. Casgevy's slow sales ramp since its 2023 approval is a "
                        "real example of how a scientifically strong drug can still be commercially "
                        "slow."
                    ),
                },
                {
                    "title": "Government drug pricing pressure",
                    "description": (
                        "Vertex's CF drugs are priced at a premium, which is the main reason the "
                        "company earns such high margins. Growing political pressure for "
                        "pharmaceutical price controls, including Medicare price negotiation in the "
                        "United States and reference pricing used by governments abroad, is a "
                        "direct threat to that pricing power, and Vertex has limited ability to "
                        "control how those policies develop."
                    ),
                },
            ],
            "source": "Research · July 2026",
        },
        "csuite": [
            {
                "name": "Reshma Kewalramani",
                "role": "CEO & President",
                "tenure": "Since April 2020",
                "strengths": [
                    "Trained as a nephrologist (kidney specialist), directly relevant to the "
                    "povetacicept kidney disease program",
                    "Personally bought 10,000 shares at about $390 in August 2025, a meaningful "
                    "signal of insider confidence",
                    "92.4% of her compensation is tied to stock performance",
                    "Ended the VX-264 type 1 diabetes device program in 2025 when the data was not "
                    "compelling, showing discipline rather than sticking with a program for its "
                    "own sake",
                ],
                "watch": [
                    "As a trained nephrologist who championed the $4.6 billion Alpine acquisition "
                    "that brought in povetacicept, she has a personal connection to the kidney "
                    "disease program. That could bias capital allocation decisions if commercial "
                    "signals turn negative",
                    "She is managing three commercial launches at once (Journavx, Casgevy, and "
                    "Alyftrek), four late-stage trials, and two C-suite leadership transitions at "
                    "the same time",
                ],
            },
            {
                "name": "Charlie Wagner",
                "role": "CFO + COO (dual role)",
                "tenure": "CFO since 2019, added COO mid-2025",
                "strengths": [
                    "Guided revenue growth from $3B to $13B since joining",
                    "Has a track record of scaling multiple healthcare companies",
                    "Describes himself as energized by complexity and operational challenges",
                ],
                "watch": [
                    "Now holds both the CFO and COO roles at the company's most operationally "
                    "complex moment, which raises bandwidth concerns",
                    "At most large pharma companies, these are two separate jobs for a reason",
                ],
            },
            {
                "name": "Mark Bunnage",
                "role": "CSO (incoming, effective Feb 2026)",
                "tenure": "SVP Global Research since 2016",
                "strengths": [
                    "A 10-year Vertex insider deeply embedded in the company's clinical research "
                    "culture",
                    "Led the due diligence team that evaluated the Alpine acquisition, which "
                    "brought povetacicept, one of the pipeline's most promising assets, to Vertex",
                    "Multiple programs advanced to clinical trials under his research leadership, "
                    "including Casgevy, Journavx, and other next-generation molecules",
                ],
                "watch": [
                    "He is stepping into the role held by David Altshuler, who built the company's "
                    "entire commercial portfolio over 13 years",
                    "He is unproven as chief scientific officer at this scale. He has been a "
                    "strong second-in-command in research, but it is unclear if he can originate "
                    "future programs at the same rate",
                ],
            },
        ],
        "earnings": [
            {
                "period": "Q1 2026",
                "date": "April 2026",
                "summary": (
                    "CEO Kewalramani highlighted continued strength in the CF franchise, with "
                    "Alyftrek adoption ramping faster than expected. The rolling application for "
                    "povetacicept remains on track, and management expressed high confidence in "
                    "FDA approval by Q4 2026. Journavx prescription volume tripled compared to the "
                    "2025 pace, though insurance coverage is still expanding and remains the main "
                    "factor limiting sales growth. The leadership transition from Altshuler to "
                    "Bunnage in the chief scientific officer role is described as proceeding "
                    "smoothly, though analysts pressed management on the risk to pipeline "
                    "continuity."
                ),
                "key_quotes": [
                    {
                        "quote": (
                            "Alyftrek is converting faster than we modeled. The once-daily "
                            "profile is resonating with both patients and physicians."
                        ),
                        "speaker": "Reshma Kewalramani",
                        "role": "CEO",
                    },
                    {
                        "quote": (
                            "The rolling BLA for povetacicept is on track. We remain highly "
                            "confident in the strength of the RAINIER data and the pathway to "
                            "approval."
                        ),
                        "speaker": "Reshma Kewalramani",
                        "role": "CEO",
                    },
                ],
                "guidance": {
                    "revenue": "$12.95 to $13.1 billion",
                    "growth": "About 8 to 9% year over year",
                    "margin": "Non-GAAP operating margin about 43 to 44%",
                },
                "risks_flagged": [
                    "Insurance coverage for Journavx is still expanding, and that remains the "
                    "main factor limiting sales growth",
                    "Analysts flagged continuity risk from the chief scientific officer "
                    "transition",
                    "Two-year kidney function data needed to confirm povetacicept's results is "
                    "still pending",
                ],
                "source_url": "https://investors.vrtx.com",
                "source_label": "Vertex Investor Relations · Q1 2026",
            }
        ],
    },
    "AVGO": {
        "business_summary": {
            "paragraphs": [
                "Broadcom runs two business segments with different but complementary strengths. "
                "Semiconductor Solutions, about 61% of fiscal 2025 revenue, designs custom AI "
                "chips in close partnership with Google, Meta, and Apple. It also dominates the "
                "networking chips that connect AI data center hardware together, through its "
                "Tomahawk and Jericho product lines. Infrastructure Software, about 39% of "
                "revenue, includes VMware, a virtualization platform used by enterprise IT "
                "departments (acquired in November 2023 for $69 billion), and CA Technologies "
                "mainframe software. Both software businesses benefit from customers who find it "
                "costly and disruptive to switch providers.",
                "Fiscal 2025 results: revenue of $63.9 billion, free cash flow of $26.9 billion, "
                "and EBITDA margins above 65%. AI chip revenue reached about $20 billion in fiscal "
                "2025, growing more than 100% year over year, driven by rising demand from large "
                "cloud computing customers. Management has guided to a fiscal 2027 AI market "
                "opportunity of $60 to 90 billion from just five large customers, three existing "
                "and two new ones starting in fiscal 2026. Guidance for Q1 fiscal 2026 AI chip "
                "revenue of $8.2 billion represents roughly 100% year over year growth continuing.",
                "The balance sheet is worth a closer look, mainly because of what the VMware deal "
                "added to it. Goodwill, the amount paid above the tangible value of acquired "
                "companies, stood at $97.8 billion at the end of fiscal 2025, mostly from the "
                "VMware and CA Technologies deals. That goodwill is only worth what the company "
                "says it is worth if VMware and CA keep generating the cash flow that justified "
                "the price paid, and a future write-down would hit reported earnings even though "
                "no cash would actually leave the business. Stock based compensation has also "
                "grown quickly, from $2.2 billion in fiscal 2023 to $7.6 billion in fiscal 2025. "
                "Most of that increase is retention grants, new stock awards given to key VMware "
                "employees to keep them from leaving during the integration, a standard practice "
                "in large acquisitions. It is a real cost that dilutes existing shareholders over "
                "time, even though no cash changes hands. Long-term debt was about $62 billion at "
                "the end of fiscal 2025, taken on to fund the VMware deal, with annual interest "
                "expense of roughly $3 billion coming out of free cash flow before any of it can "
                "go toward dividends, buybacks, or further acquisitions. That said, the company is "
                "not stretched thin day to day: it held $19.6 billion in cash as of its most recent "
                "quarter, plus a $7.5 billion revolving credit facility that was entirely undrawn "
                "as of fiscal 2025 year end, giving it a real cushion on top of its $26.9 billion "
                "in annual free cash flow.",
                "The core debate for investors: Broadcom's chip business has a genuine structural "
                "advantage because designing custom chips with a customer creates deep, sticky "
                "partnerships that are hard to displace. The software business has similarly "
                "strong customer lock-in, but it also carries real regulatory risk from the EU and "
                "litigation from enterprise customers over VMware's pricing changes. The stock "
                "trades at 19.8 times forward earnings versus a semiconductor sector median of "
                "36.3 times. That discount reflects two specific investor concerns: possible EU "
                "regulatory action on VMware, and the unresolved question of who succeeds CEO "
                "Hock Tan, who is over 73.",
            ],
            "source": "Research · July 2026",
        },
        "moat": {
            "type": "Switching Costs (dual: semiconductor + software)",
            "strength": "WIDE",
            "description": (
                "Broadcom's custom chip partnerships with Google, Meta, and Apple would take a "
                "competitor an estimated three to five years to replicate, because these are "
                "multi-year engineering collaborations rather than simple vendor contracts. The "
                "Tomahawk and Jericho networking chips carry similar lock-in within AI data "
                "centers. On the software side, VMware and CA mainframe software are embedded so "
                "deeply in enterprise IT systems that switching realistically takes years. A "
                "lawsuit filed by UnitedHealthcare explicitly stated that moving to alternative "
                "mainframe software would take years, which is exactly the kind of switching cost "
                "this moat depends on."
            ),
            "source": "Research · July 2026",
        },
        "risks": {
            "items": [
                {
                    "title": "The rollup strategy runs on debt",
                    "description": (
                        "Broadcom has built itself into a $1.5 trillion company largely by "
                        "borrowing to fund acquisitions, most recently the $69 billion VMware "
                        "deal. Total indebtedness stood at $67.1 billion at the end of fiscal "
                        "2025. That debt has funded real, cash-generating businesses so far, but "
                        "it also means Broadcom carries meaningfully more leverage than most "
                        "large-cap tech peers. A misjudged future acquisition, a sustained rise in "
                        "interest rates, or a slowdown in the cash flow the debt was supposed to "
                        "be serviced by would all be harder to absorb than they would be for a "
                        "company with a cleaner balance sheet."
                    ),
                },
                {
                    "title": "AI customers could bring chip design in-house",
                    "description": (
                        "Broadcom's own 2025 annual report discloses that aggregate sales to its "
                        "top five end customers, through all channels, accounted for approximately "
                        "40% of net revenue, and that one customer alone, a distributor, accounted "
                        "for 32%. Several of Broadcom's largest AI chip customers are the same "
                        "hyperscalers, Google, Meta, and others, that have both the engineering "
                        "talent and the balance sheets to design more of their own AI silicon "
                        "in-house over time. Broadcom explicitly lists customers' internal chip "
                        "development as a risk factor in its own filings. Given how concentrated "
                        "revenue already is among a handful of these customers, even one of them "
                        "materially reducing its purchases in favor of in-house chips would be a "
                        "significant hit to Broadcom's revenue, not a marginal one."
                    ),
                },
                {
                    "title": "Manufacturing depends on a concentrated, fragile supply chain",
                    "description": (
                        "Broadcom does not own the fabs that make its chips. About 95% of the "
                        "wafers made by its contract manufacturers in fiscal 2025 came from a "
                        "single company, TSMC, which also makes chips for Broadcom's competitors "
                        "and could choose, or be required, to prioritize their capacity over "
                        "Broadcom's. On top of that, Broadcom bought roughly two thirds of its raw "
                        "manufacturing materials, things like specialized wafers, precious metals, "
                        "and chemicals, from just five suppliers in fiscal 2025, some of them the "
                        "only available source for that material. Broadcom does not generally sign "
                        "long-term contracts with these suppliers, buying instead on a "
                        "purchase-order basis, so pricing and availability can shift with little "
                        "warning. Layered on top of that is geopolitical exposure: 17% of "
                        "Broadcom's fiscal 2025 net revenue came from shipments to China, a region "
                        "where trade policy and export controls remain unsettled. Any disruption "
                        "across this chain, whether from TSMC allocating capacity elsewhere, a "
                        "single-source supplier running short, or new China trade restrictions, "
                        "could raise Broadcom's costs or limit how much it can actually ship."
                    ),
                },
            ],
            "source": "Research · July 2026",
        },
        "csuite": [
            {
                "name": "Hock Tan",
                "role": "President & CEO",
                "tenure": "Since 2006",
                "strengths": [
                    "Built a $5 billion company (Avago) into a $1.5 trillion company (Broadcom) "
                    "through disciplined acquisitions over 19 years",
                    "Shows extreme capital discipline. He walked away from the Qualcomm deal when "
                    "regulatory conditions turned unfavorable rather than overpaying to get it "
                    "done",
                    "Has consistently delivered on every financial commitment made publicly, "
                    "which is rare among large-cap tech companies",
                    "Focused on free cash flow as an operator. EBITDA margins expanded from 55% "
                    "to over 65% under his leadership",
                    "Recently joined Meta's board, a sign of his continued relevance in the AI "
                    "industry",
                ],
                "watch": [
                    "He is over 73 years old, and no public succession plan has been identified "
                    "anywhere in analyst coverage. This is one of the most underweighted risks by "
                    "the market",
                    "VMware's pricing strategy, which raised prices 800 to 1,500% for some "
                    "customers, triggered lawsuits from AT&T and UnitedHealthcare and an EU "
                    "regulatory inquiry. It is controversial but intentional, and the cash flow "
                    "results support the strategy so far",
                    "The hostile Qualcomm bid in 2017 to 2018 was blocked by the Trump "
                    "administration on national security grounds. Since then, Broadcom has stuck "
                    "to negotiated deals only",
                    "The company has been shaped almost entirely by Tan's personal acquisition "
                    "strategy, which makes succession risk existential rather than just "
                    "operational",
                ],
            },
            {
                "name": "Kirsten Spears",
                "role": "CFO",
                "tenure": "Since 2016",
                "strengths": [
                    "Communicates consistently and clearly about free cash flow",
                    "Strong operational execution across several large acquisitions, including "
                    "the VMware integration",
                    "Has a clear and disciplined track record on guidance",
                ],
                "watch": [
                    "Has a lower public profile than Tan outside of financial reporting, so her "
                    "strategic vision is less visible"
                ],
            },
        ],
        "earnings": [
            {
                "period": "Q3 FY2025",
                "date": "September 2025",
                "summary": (
                    "Record quarterly revenue was driven by continued acceleration in AI chip "
                    "demand and progress integrating VMware. CEO Tan guided Q4 AI chip revenue to "
                    "$6.2 billion, marking eleven consecutive quarters of AI revenue growth. "
                    "VMware software revenue growth is accelerating as enterprise customers move "
                    "to subscription bundles. EBITDA margins continue to expand to new records. "
                    "Analysts pressed management on EU regulatory risk around VMware. Management "
                    "pointed to 87% of its top 10,000 customers signing up for the new bundles as "
                    "evidence that the pricing model is holding up."
                ),
                "key_quotes": [
                    {
                        "quote": (
                            "Q3 AI revenue growth accelerated to 63% year-over-year to $5.2 "
                            "billion. We expect growth in AI semiconductor revenue to accelerate "
                            "to $6.2 billion in Q4, delivering eleven consecutive quarters of "
                            "growth."
                        ),
                        "speaker": "Hock Tan",
                        "role": "CEO",
                    },
                    {
                        "quote": (
                            "Consolidated revenue grew 22% year-over-year to a record $16.0 "
                            "billion."
                        ),
                        "speaker": "Hock Tan",
                        "role": "CEO",
                    },
                ],
                "guidance": {
                    "revenue": "$19.1 billion for Q1 fiscal 2026",
                    "growth": "About 22% year over year, consolidated",
                    "margin": "67% adjusted EBITDA margin guided for Q1 fiscal 2026",
                },
                "risks_flagged": [
                    "Possible EU regulatory action on VMware pricing, including inquiry risk "
                    "from the European Commission",
                    "Third-party analysts have flagged the risk that AI capital spending by "
                    "customers could peak in the second half of 2026",
                    "AI chip revenue is concentrated among a small number of large cloud "
                    "computing customers",
                ],
                "source_url": "https://investors.broadcom.com",
                "source_label": "Broadcom Investor Relations · Q3 FY2025",
            }
        ],
    },
    "COST": {
        "business_summary": {
            "paragraphs": [
                "Costco runs a membership warehouse retail model built on deliberate limits and "
                "scale. Carrying only about 5,000 products, compared to over 30,000 at a typical "
                "supermarket, gives Costco extraordinary purchasing power and fast inventory "
                "turnover. Its Kirkland Signature private label matches or beats national brands "
                "in quality at 15 to 20% lower prices. This deepens member loyalty and compresses "
                "gross margin in a way that actually strengthens the moat, because it makes "
                "Costco's value proposition impossible for traditional retailers to match without "
                "hurting their own profits.",
                "The membership fee is the financial engine of the business. Annual membership "
                "fees, $5.32 billion in fiscal 2025, flow almost entirely to the bottom line and "
                "represent about 50% of total operating income despite being less than 2% of "
                "total revenue. The 89.8% renewal rate is not just a satisfaction metric. It "
                "reflects real switching costs built into the membership relationship. Fiscal "
                "2025 total revenue reached $280.4 billion, a 10-year revenue growth rate of "
                "about 9.2% per year. The September 2024 membership fee increase, from $60 to $65 "
                "for standard members and $110 to $130 for executive members, was absorbed with "
                "minimal member loss.",
                "Fiscal 2026 headwinds are real but manageable given Costco's cost structure. "
                "Tariff uncertainty is being addressed through Kirkland Signature expansion and "
                "diversifying suppliers across more countries. Wage pressure, with the top pay "
                "scale now at $31.90 per hour, flows through operating expenses but is partly "
                "offset by the efficiency of the warehouse format. Internationally, 35 new "
                "warehouses are planned for fiscal 2026, and e-commerce sales grew 22.6% in Q2 "
                "fiscal 2026.",
            ],
            "source": "Research · July 2026",
        },
        "moat": {
            "type": "Cost Advantage + Switching Costs",
            "strength": "WIDE",
            "description": (
                "The 5,000-product discipline and warehouse format create a structural cost "
                "advantage that traditional retailers cannot match even with unlimited capital, "
                "because matching it would require abandoning how conventional retail operates. "
                "The membership fee also creates a psychological switching cost. Members who have "
                "paid $65 to $130 for annual access are motivated to keep shopping at Costco to "
                "get their money's worth, which creates loyalty that goes beyond rational price "
                "comparison. The treasure hunt shopping experience and Kirkland Signature quality "
                "are both genuinely difficult for competitors to replicate at scale."
            ),
            "source": "Research · July 2026",
        },
        "risks": {
            "items": [
                {
                    "title": "Operating margins leave almost no room for error",
                    "description": (
                        "Costco runs on an operating margin of roughly 3.5 to 3.7%, deliberately "
                        "thin because the strategy is to pass savings to members rather than "
                        "maximize retail markup. That is a strength when things go right, but it "
                        "also means there is very little buffer. A cost increase Costco cannot "
                        "pass through to members or offset with scale, whether from tariffs, wages, "
                        "or freight, falls almost straight through to profit."
                    ),
                },
                {
                    "title": "The business depends on members renewing",
                    "description": (
                        "Membership fees are less than 2% of revenue but represent about half of "
                        "total operating income. The entire model depends on keeping the renewal "
                        "rate near its current 89.8%. A meaningful drop in renewals, or member "
                        "pushback the next time fees are raised, would hurt profitability far more "
                        "than the equivalent drop in warehouse sales would."
                    ),
                },
                {
                    "title": "Tariffs and import exposure",
                    "description": (
                        "A meaningful share of Costco's merchandise, including much of the "
                        "Kirkland Signature private label, is imported or built from imported "
                        "components. New or higher tariffs raise Costco's costs faster than it can "
                        "renegotiate with suppliers or shift sourcing to other countries, and "
                        "management has said the eventual size of the fiscal 2026 tariff impact is "
                        "still unclear."
                    ),
                },
            ],
            "source": "Research · July 2026",
        },
        "csuite": [
            {
                "name": "Ron Vachris",
                "role": "President & CEO",
                "tenure": "Since January 2024",
                "strengths": [
                    "A 40-year company veteran who started as a teenage forklift driver, giving "
                    "him about as deep a connection to Costco's culture as anyone could have",
                    "Only the third CEO in Costco's history, providing continuity with the "
                    "company's founding philosophy",
                    "$10.6M of his $12.2M total compensation is tied to pre-tax income "
                    "performance goals, showing strong alignment with shareholders",
                    "Maintained the company's diversity commitments under shareholder pressure, "
                    "with 98% shareholder support on the pay vote",
                ],
                "watch": [
                    "This is his first CEO tenure navigating a genuinely complex macro "
                    "environment, with tariffs, energy costs tied to conflict in the Middle East, "
                    "and wage inflation all happening at once",
                    "He communicates less publicly than peer CEOs, and his style is more "
                    "operational than visionary",
                    "Navigating tariffs will test him in ways his predecessor, Craig Jelinek, "
                    "never had to face",
                ],
            },
            {
                "name": "Gary Millerchip",
                "role": "CFO",
                "tenure": "Since 2018",
                "strengths": [
                    "Proactively discloses headwinds, including flagging wage costs and Middle "
                    "East energy risk directly on earnings calls",
                    "A clear communicator on cost structure and membership economics",
                ],
                "watch": [
                    "The company's tariff pass-through strategy is still being worked out and has "
                    "not yet been fully explained to investors"
                ],
            },
        ],
        "earnings": [
            {
                "period": "Q3 FY2026",
                "date": "June 2026",
                "summary": (
                    "CEO Vachris highlighted tariff headwinds being actively managed through "
                    "Kirkland Signature expansion, with more than 30 new items added in Q4, and "
                    "supplier diversification across more countries. The membership renewal rate "
                    "held steady at 89.8%, even after the September 2024 fee increase fully "
                    "cycled through. E-commerce sales grew 22.6% in Q2, accelerating from prior "
                    "quarters. Wage costs, with the top pay scale raised to $31.90 per hour, were "
                    "explicitly flagged as an ongoing expense pressure. International expansion "
                    "remains on track, with 35 new warehouses planned for the full fiscal year."
                ),
                "key_quotes": [
                    {
                        "quote": (
                            "Our members continue to show remarkable loyalty. The renewal rate "
                            "holding at 89.8% after the fee increase tells you everything about "
                            "the value proposition we deliver."
                        ),
                        "speaker": "Ron Vachris",
                        "role": "CEO",
                    },
                    {
                        "quote": (
                            "The future impact of tariffs remains extremely fluid. What I can "
                            "tell you is that our buying team and Kirkland Signature capabilities "
                            "give us tools most retailers simply do not have."
                        ),
                        "speaker": "Ron Vachris",
                        "role": "CEO",
                    },
                ],
                "guidance": {
                    "revenue": "$295 to $305 billion estimated for fiscal 2026",
                    "growth": "About 7 to 8% year over year",
                    "margin": "Operating margin of about 3.5 to 3.7%",
                },
                "risks_flagged": [
                    "The impact of tariffs on merchandise costs remains fluid and difficult to "
                    "quantify precisely",
                    "Wage inflation, with the top pay scale at $31.90 per hour, is an ongoing "
                    "expense pressure",
                    "CFO Millerchip flagged energy cost risk tied to conflict in the Middle East",
                ],
                "source_url": "https://investor.costco.com",
                "source_label": "Costco Investor Relations · Q3 FY2026",
            }
        ],
    },
    "JPM": {
        "business_summary": {
            "paragraphs": [
                "JPMorgan Chase is the largest bank in the United States by assets, with $4.4 "
                "trillion in total assets at the end of fiscal year 2025. It operates through "
                "three main segments: Consumer and Community Banking, which covers branches, "
                "credit cards, and home and auto lending for individual customers, Commercial "
                "and Investment Bank, which covers trading, investment banking, and lending for "
                "large corporations and institutions, and Asset and Wealth Management, which "
                "manages money for institutions and wealthy individuals. Fiscal year 2025 net "
                "revenue was $182.4 billion, up modestly from $177.6 billion the year before, "
                "while net income was $57.0 billion, down slightly from $58.5 billion in fiscal "
                "year 2024.",
                "JPMorgan's own leadership describes its approach as running a fortress balance "
                "sheet, meaning the company deliberately holds more capital and liquidity than "
                "regulators require so it can keep lending and absorb losses through a downturn "
                "rather than pull back the way many smaller banks have to. At the end of fiscal "
                "year 2025, its core capital ratio, a measure of how much high-quality capital "
                "it holds against its loans and investments, stood at 14.6%, well above the "
                "11.5% regulatory minimum that applies to it. Return on tangible common equity, "
                "a key profitability measure for banks, was 20% for fiscal year 2025, down from "
                "22% the year before but still among the strongest in the industry, and tangible "
                "book value per share grew to $107.56 from $97.30.",
                "The core debate for investors is really about the economic cycle rather than "
                "the company itself. JPMorgan's scale, its mix of consumer and institutional "
                "banking, and its conservative capital position have let it consistently "
                "outperform smaller banks through past downturns, including the 2008 financial "
                "crisis and the 2023 regional bank stress. The tradeoff is that a bank this size "
                "is deeply tied to the health of the overall economy. Loan losses, deposit "
                "costs, and trading and deal-making revenue all move with interest rates, "
                "credit conditions, and market volatility in ways that are largely outside "
                "management's control.",
            ],
            "source": "Research · July 2026",
        },
        "moat": {
            "type": "Scale + Switching Costs",
            "strength": "WIDE",
            "description": (
                "JPMorgan's advantage starts with sheer scale. With $4.4 trillion in assets, it "
                "can spread technology, compliance, and risk management costs across a base "
                "that no regional or mid-size bank can match, which shows up directly in its 52% "
                "overhead ratio, a measure of costs as a share of revenue that runs well below "
                "many peers. On top of that, both consumer and business banking relationships "
                "come with real switching costs. Moving a business's cash management, credit "
                "lines, and payment processing to a new bank, or moving a household's checking "
                "account, mortgage, and credit cards, all take real effort, so customers tend to "
                "stay once they are set up. This combination of low-cost scale and sticky "
                "relationships is difficult for smaller banks and non-bank fintech challengers "
                "to replicate at the same time."
            ),
            "source": "Research · July 2026",
        },
        "risks": {
            "items": [
                {
                    "title": "Results move with the credit cycle",
                    "description": (
                        "JPMorgan's results are directly tied to the health of the broader "
                        "economy. A recession or a sharp rise in unemployment would increase "
                        "loan defaults across its consumer and commercial loan books, forcing "
                        "the company to set aside more money for expected losses, which reduces "
                        "reported profit at exactly the point the economy is already struggling."
                    ),
                },
                {
                    "title": "Interest rates and market activity swing revenue",
                    "description": (
                        "A large share of JPMorgan's revenue, net interest income from loans and "
                        "deposits, and trading and investment banking fees, depends on interest "
                        "rates and market conditions the company does not control. Falling rates "
                        "can compress the spread it earns on loans, while a quiet market for "
                        "trading and dealmaking can slow the revenue its Commercial and "
                        "Investment Bank segment depends on."
                    ),
                },
                {
                    "title": "Regulatory and capital requirements can tighten",
                    "description": (
                        "As the largest and most systemically important U.S. bank, JPMorgan "
                        "faces the strictest capital, stress testing, and regulatory "
                        "requirements in the industry, and those requirements can tighten "
                        "further after any period of financial stress. A higher required capital "
                        "ratio would force the company to hold more capital against the same "
                        "amount of business, directly limiting how much it can return to "
                        "shareholders through dividends and buybacks."
                    ),
                },
            ],
            "source": "Research · July 2026",
        },
        "csuite": [
            {
                "name": "Jamie Dimon",
                "role": "Chairman & CEO",
                "tenure": "CEO since 2005",
                "strengths": [
                    "Led the firm through the 2008 financial crisis without needing the kind of "
                    "government rescue several competitors required",
                    "The longest-tenured CEO among the largest U.S. banks, giving him unusual "
                    "continuity in setting long-term strategy",
                    "Built and consistently maintained the firm's fortress balance sheet "
                    "philosophy, which has repeatedly let JPMorgan play offense (acquiring "
                    "distressed assets and market share) during downturns that hurt competitors",
                ],
                "watch": [
                    "CEO succession is one of the most closely watched questions on Wall Street. "
                    "Several internal executives hold senior roles that position them as "
                    "possible successors, but Dimon has not committed to a firm retirement date",
                    "A leadership change at a company this closely identified with one person "
                    "carries real transition risk, regardless of how strong the bench is",
                ],
            },
            {
                "name": "Jeremy Barnum",
                "role": "CFO",
                "tenure": "Since 2021",
                "strengths": [
                    "Came into the CFO role after running JPMorgan's Global Markets trading "
                    "business, giving him direct operating experience rather than a purely "
                    "financial background",
                    "Communicates clearly and directly on quarterly earnings calls about drivers "
                    "of net interest income and credit costs",
                ],
                "watch": [
                    "Considerably shorter tenure than Dimon's, and has had less time in the seat "
                    "relative to CFOs at some peer banks",
                ],
            },
        ],
        # TODO(user): no earnings call summary yet. Update earnings summaries
        # manually, generate a new one in Claude at claude.ai and paste it
        # here in the same shape as the other tickers' `earnings` entries.
        "earnings": [],
    },
}
