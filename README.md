# Stocks Vault

[![vault-ci](https://github.com/Ali0600/stocks-vault/actions/workflows/vault-ci.yml/badge.svg)](https://github.com/Ali0600/stocks-vault/actions/workflows/vault-ci.yml)

An LLM-maintained stock-research wiki (Obsidian vault) covering a personal
portfolio plus a watchlist, with a structured, source-cited schema. Notes are
maintained by Claude Code against the contract in [SCHEMA.md](SCHEMA.md);
[index.md](index.md) is the catalog and [log.md](log.md) is the append-only history.

## Layout
- `Stocks/` — one note per company (Overview · What's Unique + chokepoint · Competitors · Supply Chain · Facts · Contracts Awarded · Dilutions · Speculations · Open Questions · Articles)
- `Sectors/` — sector groupings · `Maps/` — cross-cutting graphs (e.g. the AI supply chain) · `Concepts/` — technology/mechanism primers
- `Articles/` — ingested sources (immutable except their auto-refreshed price table)
- `scripts/` — the maintenance toolchain · `.github/workflows/` — CI

## Automation / DevOps
- **`scripts/vault_lint.py`** — 12-rule integrity linter (sourcing, supply-chain
  symmetry, index drift, broken links, section coverage…). Pure stdlib; **exits
  non-zero on failure** so it works as a CI and pre-commit gate.
- **`scripts/refresh_prices.py`** — pulls latest closes via `yfinance` and rewrites
  each article's price-impact table (idempotent).
- **`scripts/refresh_fundamentals.py`** — pulls market cap, revenue, growth, margin,
  P/E and next-earnings into each note's `## Snapshot` block (idempotent, self-installing).
- **`scripts/daily_maintenance.sh`** + **launchd** (`com.stocksvault.maintenance.plist`)
  — runs refresh → lint → auto-commit daily on the local machine.
- **GitHub Actions** (`.github/workflows/vault-ci.yml`) — lints on every push/PR and,
  on a weekday schedule, refreshes prices and commits them back.
- A **pre-commit hook** runs the linter so a corrupting edit can't be committed.

Operating & troubleshooting the scheduled job (launchctl commands, the Full Disk
Access fix): see [RUNBOOK.md](RUNBOOK.md).

### Run locally
```bash
python scripts/vault_lint.py            # integrity gate (exit 0 = clean)
python scripts/refresh_prices.py        # refresh article price tables
python scripts/refresh_fundamentals.py  # refresh per-note fundamentals snapshots
```

## Highlights
- Designed a **schema-driven knowledge base** of 50+ interlinked notes with a strict
  sourcing contract (every dated fact cites an ingested article or a concept primer).
- Built a **CI-style validation pipeline**: a 12-rule integrity linter (exit-code
  gated) wired into a **GitHub Actions** workflow and a **git pre-commit hook**.
- Automated **market-data refresh** (yfinance) and integrity linting on a daily
  schedule via **launchd**, with auto-commit to a version-controlled vault.
- Modeled the **AI hardware supply chain** as a directed dependency graph
  (supplier↔customer edges, chokepoint severity ratings) to surface single points
  of failure.
