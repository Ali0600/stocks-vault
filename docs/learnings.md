# Learnings

Transferable concepts that came up while building this vault. Newest first.

## SEC EDGAR as the free, official earnings source

Every US-listed company's earnings press release is public, free, and key-less on
EDGAR. The chain is: `company_tickers.json` maps ticker → CIK ·
`data.sec.gov/submissions/CIK##########.json` lists recent filings · an earnings
release is form **8-K** carrying **Item 2.02** ("Results of Operations and
Financial Condition") · the filing's `index.json` lists its files, and the release
itself is **Exhibit 99.1**. There is no rate-limit key — just a User-Agent and a
10 requests/second ceiling.

**Why it came up:** MU's note had empty Facts and Contracts Awarded because the
vault's only ingestion path was `/ingest-article`, which depends on secondary
coverage. The primary document was free the whole time.

**Takeaway:** before wiring an ingestion pipeline to a paid API or to a
publisher's coverage, check whether the regulator already publishes the primary
document — it's the same data, earlier, without a middleman's framing.

## Two things EDGAR will surprise you with

1. **A User-Agent without a contact email is answered 403.** Not rate-limited —
   rejected outright. The failure is confusing because the same request succeeds
   the moment an email appears in the header, and a repo-URL "neutral default"
   looks perfectly reasonable in code review while failing 100% of the time.
2. **Foreign private issuers don't file 8-Ks.** TSM, NOK, ARM, ASML and CCJ file
   **6-K**, which carries *no item codes at all* — TSM alone has 744 of them, all
   with an empty `items` field. There is no way to identify the earnings one by
   metadata, so the fetcher exits non-zero and asks for a manual clip instead of
   guessing.

**Takeaway:** an API's *shape* being uniform doesn't mean its *semantics* are.
Probe the exact call you plan to depend on, with the exact headers you plan to
send, before designing around it — and when a whole class of entity can't be
served, fail loudly and name the fallback rather than returning nothing.

## A default that always fails is indistinguishable from a broken feature

The original design shipped `SEC_EDGAR_UA` with a committed repo-URL default so
no personal email would land in a public repo. That default 403s on every request,
so the feature would have appeared "built but broken" forever. The fix keeps the
privacy property *and* the loud failure: the value is read from a gitignored
`.env` (with a committed `.env.example`), and the script validates that the
User-Agent contains an email *before* making any request — so a missing setup
produces a one-line setup instruction instead of an opaque HTTP error.

**Takeaway:** when a required credential can't be committed, don't paper over it
with a placeholder that technically runs. Validate the config at the boundary and
fail with the exact fix.

## Verifying a source against an independent one

The MU release reports GAAP diluted EPS of $24.67 and non-GAAP $25.11. yfinance's
`quarterly_income_stmt` independently reports $24.67 — matching the GAAP figure
and confirming that the non-GAAP number is the company's own adjusted measure, not
a discrepancy. Two sources that agree on the audited figure and differ on the
adjusted one tell you *which* number is which.

**Takeaway:** cross-check a primary source against an independent one not to catch
lies, but to learn which of its numbers are standardized and which are the
issuer's own construction — the disagreement is the information.
