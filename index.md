# Stocks Vault — Index

Read this first. Maintained by Claude after every change.

## Sectors
Watchlist tickers (no portfolio position) are marked *.
- [[AI Infrastructure]] (4+3*): [[APLD]]* · [[CRWV]]* · [[DELL]]* · [[HPE]] · [[IREN]] · [[NBIS]] · [[SMCI]]
- [[Biotech]] (3): [[ARTV]] · [[IKT]] · [[PRQR]]
- [[Cannabis]] (2): [[CGC]] · [[TLRY]]
- [[Consumer & Fintech]] (3+1*): [[BYND]] · [[HOOD]] · [[SOFI]]* · [[TTWO]]
- [[Materials]] (1): [[MP]]
- [[Networking & Optical]] (3+7*): [[AAOI]] · [[ALAB]]* · [[ANET]]* · [[CIEN]]* · [[COHR]]* · [[CRDO]]* · [[FN]]* · [[LITE]]* · [[NOK]] · [[POET]]
- [[Nuclear]] (5): [[CCJ]] · [[LEU]] · [[NNE]] · [[OKLO]] · [[SMR]]
- [[Power & Infrastructure]] (0+4*): [[DY]]* · [[ETN]]* · [[GEV]]* · [[VRT]]*
- [[Quantum]] (4): [[IONQ]] · [[QBTS]] · [[QUBT]] · [[RGTI]]
- [[Semiconductors]] (5+10*): [[AMAT]] · [[AMD]]* · [[ARM]]* · [[ASML]]* · [[AVGO]]* · [[CDNS]]* · [[INTC]] · [[KLAC]]* · [[LRCX]]* · [[MPWR]]* · [[MRVL]] · [[MU]]* · [[NVDA]] · [[SNPS]]* · [[TSM]]
- [[Software & Cloud]] (3+2*): [[GOOGL]]* · [[IBM]] · [[MSFT]] · [[NOW]] · [[ORCL]]*
- [[Space]] (4): [[ASTS]] · [[GSAT]] · [[PL]] · [[RKLB]]

## Maps
- [[AI Supply Chain]] — sand→tokens chain across the portfolio, chokepoints rated

## Concepts
- [[HBM]] — stacked memory on the GPU; the AI bandwidth bottleneck
- [[CoWoS]] — TSMC packaging that bonds GPU die + HBM; tightest link in the stack
- [[CUDA]] — NVIDIA's software lock-in
- [[Foundry process nodes]] — leading-edge (2nm / GAA); why few fabs gate the top chips
- [[Rare-earth magnets]] — NdFeB magnets, China dominance, the strategic-source angle
- [[Optical interconnect]] — transceivers (800G→1.6T) that wire GPUs into clusters
- [[GPU interconnect]] — NVLink scale-up vs Ethernet/InfiniBand scale-out
- [[Custom AI silicon]] — merchant GPU vs hyperscaler ASIC (TPU, Trainium); the MRVL/Broadcom co-design duopoly
- [[Datacenter power]] — rack densities, grid queues; the rising binding constraint
- [[Liquid cooling]] — why air fails at GB200 densities
- [[Neocloud economics]] — GPU-as-a-service and the GPU-backed debt model
- [[Wafer-fab equipment]] — the five-vendor WFE oligopoly; ASML's EUV monopoly
- [[EDA & chip IP]] — the Synopsys/Cadence design-tool duopoly + Arm IP; gates every chip before fab
- [[AI cluster networking]] — scale-up vs scale-out fabrics; the switching/retimer/AEC layer that wires GPU clusters

## Articles
- 2026-07-29 · [[2026-07-29 msft-fq4-26-earnings]] — MSFT FQ4-26 (SEC 8-K): revenue $90.0B +18%, EPS $4.81 verified; commercial RPO +84% to $678B, Azure +43% and past $100B/yr, 30M Copilot seats; new non-GAAP measure excluding the OpenAI investment
- 2026-07-29 · [[2026-07-29 hood-q2-26-earnings]] — HOOD Q2-26 (SEC 8-K): record revenue $1.31B +32%, EPS $0.62 verified; event contracts +10x to $156M while crypto -38%, 13 lines over $100M annualized; $129M one-time RVI deconsolidation gain inside net income
- 2026-07-23 · [[2026-07-23 intc-q2-26-earnings]] — INTC Q2-26 (SEC 8-K): revenue $16.1B +25% (best in 15 yrs), DCAI +59%, Foundry +31%, Xeon 6+ on 18A; the $11B GAAP loss is a $12.5B non-cash mark-to-market on CHIPS Act Escrowed Shares, not operations
- 2026-07-22 · [[2026-07-22 now-q2-26-earnings]] — NOW Q2-26 (SEC 8-K): revenue $3.99B +24% verified, RPO $29B; ServiceNow AI crossed $1B ACV; AI delivery runs on hyperscaler partnerships; Q2 beat partly a US Federal pull-forward from Q3
- 2026-07-22 · [[2026-07-22 ibm-q2-26-earnings]] — IBM Q2-26 (SEC 8-K): revenue $17.16B, EPS $2.27 verified; IBM Z -42% against Distributed Infrastructure +37% with a ~$500M Power/Storage backlog; FY constant-currency growth guided 4-5%
- 2026-06-24 · [[2026-06-24 mu-fq3-26-earnings]] — MU FQ3-26 (SEC 8-K): revenue $41.46B, 84.6% GM, EPS $24.67 all verified; HBM4 in high-volume shipment, HBM4E for CY2027; multi-year Strategic Customer Agreements (terms undisclosed) → Contracts Awarded; FQ4 guide $50B open
- 2026-06-16 · [[2026-06-16 mrvl-record-highs-valuation]] — MRVL FQ1 FY27 $2.42B +28% verified, ~59% GM, $11.5B/$16.5B FY guide, Celestial AI photonics buy, ~$1B supplier prepayments, ~915M shares; valuation/rating not routed
- 2026-06-16 · [[2026-06-16 sofi-golden-opportunity]] — SOFI Q1 record net rev $1.1B +43% verified, EBITDA $340M +62%, members 14.7M +35%, Q2 guide +30%; valuation/rating not routed
- 2026-06-14 · [[2026-06-14 alphabet-incredible]] — Alphabet bull case; created GOOGL* watchlist note (Software & Cloud), wired NVDA→GOOGL + AVGO→GOOGL (TPU); Cloud +63%, >$100B/qtr verified; price-run/target not routed
- 2026-06-14 · [[2026-06-14 sofi-selloff-wall-street]] — SOFI selloff roundup (+ bundled HOOD/SpaceX piece); created SOFI* watchlist note; routed SOFI Q1 tech-segment decline + SpaceX IPO access (SOFI & HOOD); targets/ratings not routed
- 2026-06-13 · [[2026-06-13 nebius-revenue-684-growth]] — NBIS Q1 revenue +684% verified ($399M vs $50.9M); ≥100MW sites 1→7, run-rate $1.25B→$1.9B→$7–9B guide; "+135%" price claim corrected to +170% (not routed)
- 2026-06-13 · [[2026-06-13 intel-bofa-double-upgrade]] — BofA two-notch upgrade of INTC (PT $135); +238% YTD verified, ">100x fwd" corrected to ~81x
- 2026-06-12 · [[2026-06-12 oracle-q4-ai-demand]] — ORCL FQ4: $638B RPO backlog, OCI +93%, $67B AI contracts signed, BYOH model; ~$40B FY27 raise + capex > revenue (dilution/capex routed); created ORCL* watchlist note, wired NVDA→ORCL; targets/rating not routed
- 2026-06-12 · [[2026-06-12 datacenter-strong-buy-trio]] — created watchlist notes APLD* (AI Infra), GEV*/DY* (new Power & Infrastructure sector); routed APLD 15-yr hyperscaler leases (1.4 GW / $86B) + DY's $1.95B Power Solutions buy; targets/upside not routed
- 2026-06-12 · [[2026-06-12 marvell-briley-pt-raise]] — MRVL CFO change (Dan Durn), expanded NVIDIA/Computex collaboration (NVLink Fusion + optics), S&P 500 inclusion (eff. 06-22); thesis routed, PT/rating/+227% YTD not routed
- 2026-06-11 · [[2026-06-11 smci-wolfe-risks]] — Wolfe initiates SMCI (neutral); DOJ/Liaw indictment, Q3 FY26 $10.2B +123% verified, ~$40B FY guide, >$13B Blackwell backlog, CRWV/xAI concentration; HPE/DELL margin notes routed
- 2026-06-11 · [[2026-06-11 situational-awareness-neocloud-stakes]] — Aschenbrenner fund's neocloud stakes; 38.89% claim corrected (NBIS, NVDA, CRWV*)
- 2026-06-10 · [[2026-06-10 optics-stocks-ai-rally]] — optics rally on AI boom (AAOI, NVDA, COHR*, LITE*)
- 2026-03-18 · [[2026-03-18 mu-fq2-26-earnings]] — MU FQ2-26 (SEC 8-K): revenue $23.86B vs a $18.70B guide, 74.4% GM, EPS $12.07 verified; margin expansion in all four business units on "tight industry supply"; dividend +30%
- 2025-12-17 · [[2025-12-17 mu-fq1-26-earnings]] — MU FQ1-26 (SEC 8-K): revenue $13.64B, 56.0% GM, EPS $4.60 verified; Cloud Memory $5.28B at 66% GM; first company-sourced confirmation of the HBM thesis
