# Stocks Vault

[![vault-ci](https://github.com/Ali0600/stocks-vault/actions/workflows/vault-ci.yml/badge.svg)](https://github.com/Ali0600/stocks-vault/actions/workflows/vault-ci.yml)

A stock-research wiki (an Obsidian vault) kept up to date by an LLM. It covers a personal
portfolio plus a watchlist, using a structured schema where every fact cites its source.
Claude Code maintains the notes against the contract in [SCHEMA.md](SCHEMA.md);
[index.md](index.md) is the catalog and [log.md](log.md) is the append-only history.

## Layout
- `Stocks/` — one note per company (Overview · What's Unique + chokepoint · Competitors · Supply Chain · Facts · Contracts Awarded · Dilutions · Speculations · Open Questions · Articles)
- `Sectors/` — sector groupings · `Maps/` — cross-cutting graphs (e.g. the AI supply chain) · `Concepts/` — primers on a technology or mechanism
- `Articles/` — sources that have been pulled in (never edited, except their auto-refreshed price table)
- `scripts/` — the maintenance tools · `.github/workflows/` — CI

## Automation / DevOps
- **`scripts/vault_lint.py`** — a 14-rule integrity checker (sourcing, supply-chain
  symmetry, index drift, broken links, section coverage, snapshot/graph freshness…).
  Pure stdlib. It **exits non-zero on failure**, so it works as a CI and pre-commit gate.
  Unit tests live in `scripts/tests/` (run `pytest scripts/tests`).
- **`scripts/refresh_graph.py`** — reads every note's supplier/customer edges and
  renders an auto-refreshed **Mermaid dependency graph** (nodes colored by chokepoint
  severity) into the AI Supply Chain map, so the picture cannot drift from the notes.
- **`scripts/fetch_earnings.py`** — pulls a company's **official earnings release**
  straight from **SEC EDGAR** (ticker → CIK → the 8-K carrying Item 2.02 → the
  Ex-99.1 exhibit) into `_inbox/` for the `/ingest-earnings` workflow. Pure stdlib,
  no API key. Unit-tested against trimmed real EDGAR payloads. EDGAR requires a
  contact email in the User-Agent, so the script reads `SEC_EDGAR_UA` from a git-ignored
  `.env` (see `.env.example`) and refuses to send a request without one.
- **`scripts/refresh_prices.py`** — pulls the latest closes via `yfinance` and rewrites
  each article's price-impact table. Safe to run repeatedly (idempotent).
- **`scripts/refresh_fundamentals.py`** — pulls market cap, revenue, growth, margin,
  P/E and next-earnings into each note's `## Snapshot` block (idempotent, self-installing).
- **`scripts/daily_maintenance.sh`** + **launchd** (`com.stocksvault.maintenance.plist`)
  — the **one refresher that counts**: every day on the local machine it runs
  refresh → lint → auto-commit/push (rebase, then push; on a conflict it stops cleanly,
  so it never leaves markers or stashes behind), and posts a **macOS notification** if it fails.
- **GitHub Actions** (`.github/workflows/vault-ci.yml`) — **checks only, never commits**:
  runs the unit tests + linter on every push/PR, scans history for secrets (gitleaks), and
  **opens a tracking issue when the gate fails**. Only the local launchd job does refreshes,
  so the two paths cannot diverge.
- A **versioned pre-commit hook** (`scripts/hooks/pre-commit`) runs the linter, so a
  corrupting edit cannot be committed. Turn it on once with `bash scripts/install-hooks.sh`.

To run or troubleshoot the scheduled job (launchctl commands, the Full Disk Access fix),
see [RUNBOOK.md](RUNBOOK.md).

### Run locally
```bash
pip install -r scripts/requirements.txt # pinned deps (yfinance) for the refreshers
cp .env.example .env                    # one-time: your SEC EDGAR contact User-Agent
bash scripts/install-hooks.sh           # one-time: activate the pre-commit linter
pytest scripts/tests                     # unit tests for the linter rules
python scripts/vault_lint.py            # integrity gate (exit 0 = clean)
python scripts/refresh_prices.py        # refresh article price tables
python scripts/refresh_fundamentals.py  # refresh per-note fundamentals snapshots
python scripts/refresh_graph.py         # rebuild the supply-chain Mermaid graph
python3 scripts/fetch_earnings.py MU    # fetch an earnings release from SEC EDGAR
```

## Experience Gained
- Designed a **schema-driven knowledge base** of 80+ linked notes with a strict sourcing
  rule: every dated fact cites an ingested article or a concept primer.
- Built a **CI-style checking pipeline**: a 14-rule integrity linter (exit-code gated,
  **pytest-covered**) wired into a **GitHub Actions** workflow and a versioned
  **git pre-commit hook**, with **gitleaks** secret scanning, **pinned dependencies**,
  and **automatic alerting** (a tracking issue opens when the gate fails).
- Automated the daily **market-data refresh** (yfinance) and integrity lint via
  **launchd** (18:30 every day) as the **single committer** (rebase-then-push, stops on conflict), with
  **CI checking only** — which removed a cron-vs-local-job race that had been corrupting
  the repo — plus a **freshness heartbeat** for a stalled refresh and **macOS notifications** on failure.
- Built a **primary-source data pipeline** on the **SEC EDGAR** REST API: resolve a ticker
  to its CIK, pick the earnings filing by form (8-K) and item code (2.02), extract the
  press-release exhibit, and cross-check the reported figures against an independent
  market-data source before anything is recorded.
- Modeled the **AI hardware supply chain** as a directed dependency graph and
  **auto-generated a Mermaid visualization** from the structured notes (supplier→customer
  edges, chokepoint-colored nodes) to show single points of failure.
