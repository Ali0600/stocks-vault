---
title: "TSMC Second Quarter 2026 Results"
url: https://investor.tsmc.com/english/quarterly-results/2026/q2
source: TSMC Investor Relations — Q2 2026 quarterly results (foreign private issuer; no SEC 8-K)
published: 2026-07-16
ingested: 2026-07-31
tickers: TSM
prices:
  TSM: 409.74
---

# TSMC Q2 2026 — 67.7% gross margin, and a guide to ~$45B

## Summary
[[TSM]]'s Q2 2026 revenue was US$40.20B (NT$1,270.4B at 31.60), with a gross margin
of 67.7% and an operating margin of 60.3%. Net income was NT$706.6B and diluted EPS
NT$136.23. The company guided Q3 2026 revenue to US$44.6–45.8B at a 65–67% gross
margin and 56–58% operating margin.

For the vault, the significant number is the margin. A 67.7% gross margin at a
pure-play foundry is the clearest available measure of how much pricing power the
leading-edge bottleneck confers — TSMC is the single hardest node to route around
in the [[AI Supply Chain]], and it is currently converting that position into
margins normally seen in software, not manufacturing. The Q3 guide implies revenue
growing another ~11–14% sequentially while margin compresses slightly.

**Sourcing note:** TSMC is a foreign private issuer and files 6-K, not 8-K, so
there is no Item 2.02 earnings filing on EDGAR to fetch —
`scripts/fetch_earnings.py TSM` exits with that message by design. This note is
built from TSMC's own investor-relations quarterly results page, cross-checked
against yfinance. The revenue-by-node and revenue-by-platform breakdowns, which
live in the separate earnings-release document, were **not retrieved** and are not
recorded here.

## Claims & Verification
- Q2 2026 revenue US$40.20B at a 31.60 USD/NTD rate — **verified**: yfinance
  reports NT$1,270.381B for the period ending 2026-06-30, and 40.20 × 31.60 =
  NT$1,270.3B.
- Gross margin 67.7% — **verified** (yfinance gross profit NT$860.311B on
  NT$1,270.381B revenue = 67.72%).
- Operating margin 60.3% — **verified** (yfinance operating income NT$766.603B =
  60.35%).
- Net income NT$706.562B, diluted EPS NT$136.23 — **verified** (yfinance).
- Q3 2026 guidance: revenue US$44.6–45.8B, gross margin 65.0–67.0%, operating
  margin 56.0–58.0%, at an assumed 32.0 USD/NTD — **company guidance**.
- Revenue by technology node and by platform — **not retrieved** (see sourcing
  note); nothing routed on those.

## Takeaways Routed
- [[TSM]] ← Facts: Q2-26 revenue, gross and operating margin, and EPS.
- [[TSM]] ← Speculations: the Q3-26 revenue and margin guide (status: open).
- The share price was checked but **not routed**.

## Price Since Publication
<!-- prices:start -->
| Ticker | At publication | Now | Since |
| --- | --- | --- | --- |
| TSM | $409.74 | $406.68 | -0.75% |

_Prices refreshed 2026-07-31 (latest close 2026-07-31)._
<!-- prices:end -->
