# Design decisions

Forks with real alternatives, recorded as they're made. Rejected options are kept
because the thinking behind them is worth more than the choice itself.

## Backlog — alternatives worth trying later

- **Robinhood MCP for earnings discovery** (from "Where do official earnings come
  from?") — a market-wide earnings calendar and consensus-estimate feed that EDGAR
  has no equivalent of. Worth using interactively to decide *what* to ingest and to
  add a beat/miss-vs-estimate line, without becoming a pipeline dependency.

---

## 2026-07-31 — Where do official earnings come from?

**The fork:** the vault could only ingest secondary coverage (`/ingest-article`),
which left stock notes without the companies' own reported numbers.

- **SEC EDGAR 8-K Item 2.02 → Ex-99.1** — the primary document, free, no key, no
  account. Full narrative: results tables, guidance, segments, contracts, dividends.
  Costs: needs a contact email in the User-Agent (403 otherwise), and foreign
  private issuers file 6-K with no item codes, so they need a manual fallback.
- **Robinhood MCP (`get_earnings_results` / `get_earnings_calendar`)** — instantly
  available in-session, and uniquely carries *consensus estimates* plus a
  market-wide calendar. But it returns numbers only, no narrative — no contract
  wins, no product milestones, nothing routable to Contracts Awarded — and it is
  session-tied, so a scheduled or headless run can't reach it.
- **yfinance only** (already a vault dependency) — `quarterly_income_stmt` has the
  audited figures with zero new infrastructure, but again numbers without narrative,
  and no guidance.

**Chosen: SEC EDGAR as the primary text, yfinance as the verification layer.**
The narrative is the point — Facts, Contracts Awarded and Speculations all need
prose that a numbers feed structurally cannot provide. Verifying EDGAR's figures
against yfinance also keeps the vault's existing "every claim gets a verdict"
contract intact, with two independent sources.

**Status of the rejected options:**
- Robinhood MCP as the *primary* source — `rejected` (session-tied; a pipeline
  can't depend on it; no narrative). As a *discovery/estimates* aid —
  `deferred — worth trying`; it already earned its keep during planning by
  identifying which tracked tickers reported in July.
- yfinance-only — `rejected` (no narrative, no guidance; it is already the
  verification layer, which is the right role for it).

**Revisit hook:** `scripts/fetch_earnings.py` isolates all sourcing behind
`main()`; adding a beat/miss line would mean enriching step 5 of
`.claude/commands/ingest-earnings.md` with an estimates lookup, leaving the
fetcher untouched.

---

## 2026-07-31 — How does the SEC contact email stay out of a public repo?

**The fork:** EDGAR requires a contact email in the User-Agent, but this repo is
public and personal values must not be committed.

- **Committed neutral default (repo URL)** — no personal data, but 403s on every
  request: a feature that looks built and never works.
- **Gitignored `.env` + committed `.env.example`, validated at startup** — one-time
  setup, and a missing/invalid value fails immediately with the exact fix.
- **Prompt for it interactively** — no setup file, but unusable from a scheduled or
  headless run.

**Chosen: gitignored `.env` with fail-fast validation.** It matches the
"personal values belong in `.env` from day one" rule and converts an opaque HTTP
403 into a one-line setup instruction.

**Status of the rejected options:** committed default — `rejected` (a default that
always fails is worse than no default). Interactive prompt — `rejected` (breaks
unattended use, which is the direction this repo's automation moves in).

**Revisit hook:** `user_agent()` in `scripts/fetch_earnings.py` is the single
place config is resolved; a secret manager or keychain lookup would slot in there.
