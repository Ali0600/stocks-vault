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
- **`scripts/vault_lint.py`** — 14-rule integrity linter (sourcing, supply-chain
  symmetry, index drift, broken links, section coverage, snapshot/graph freshness…).
  Pure stdlib; **exits non-zero on failure** so it works as a CI and pre-commit gate.
  Unit-tested in `scripts/tests/` (run `pytest scripts/tests`).
- **`scripts/refresh_graph.py`** — parses every note's supplier/customer edges and
  renders an auto-refreshed **Mermaid dependency graph** (nodes colored by chokepoint
  severity) into the AI Supply Chain map, so the visual can't drift from the notes.
- **`scripts/refresh_prices.py`** — pulls latest closes via `yfinance` and rewrites
  each article's price-impact table (idempotent).
- **`scripts/refresh_fundamentals.py`** — pulls market cap, revenue, growth, margin,
  P/E and next-earnings into each note's `## Snapshot` block (idempotent, self-installing).
- **`scripts/daily_maintenance.sh`** + **launchd** (`com.stocksvault.maintenance.plist`)
  — runs refresh → lint → auto-commit daily on the local machine, and posts a **macOS
  notification** if the lint gate fails or a push conflicts.
- **GitHub Actions** (`.github/workflows/vault-ci.yml`) — runs the unit tests + linter
  on every push/PR, scans the history for secrets (gitleaks), **opens a tracking issue
  when the gate fails**, and on a weekday schedule refreshes prices/fundamentals/graph
  and commits them back (rebasing first so it can't diverge from the local job).
- A **versioned pre-commit hook** (`scripts/hooks/pre-commit`) runs the linter so a
  corrupting edit can't be committed — activate it once with `bash scripts/install-hooks.sh`.

Operating & troubleshooting the scheduled job (launchctl commands, the Full Disk
Access fix): see [RUNBOOK.md](RUNBOOK.md).

### Run locally
```bash
pip install -r scripts/requirements.txt # pinned deps (yfinance) for the refreshers
bash scripts/install-hooks.sh           # one-time: activate the pre-commit linter
pytest scripts/tests                     # unit tests for the linter rules
python scripts/vault_lint.py            # integrity gate (exit 0 = clean)
python scripts/refresh_prices.py        # refresh article price tables
python scripts/refresh_fundamentals.py  # refresh per-note fundamentals snapshots
python scripts/refresh_graph.py         # rebuild the supply-chain Mermaid graph
```

## Highlights
- Designed a **schema-driven knowledge base** of 50+ interlinked notes with a strict
  sourcing contract (every dated fact cites an ingested article or a concept primer).
- Built a **CI-style validation pipeline**: a 14-rule integrity linter (exit-code
  gated, **pytest-covered**) wired into a **GitHub Actions** workflow and a versioned
  **git pre-commit hook**, with **gitleaks** secret scanning, **pinned dependencies**,
  and **automated alerting** (a tracking issue is opened when the gate fails).
- Automated **market-data refresh** (yfinance) and integrity linting on a daily
  schedule via **launchd**, with rebase-before-push **auto-commit** to a
  version-controlled vault (no divergence between the local and CI push paths), a
  **freshness heartbeat** that flags a stalled refresh job, and **macOS notifications**
  on failure.
- Modeled the **AI hardware supply chain** as a directed dependency graph and
  **auto-generated a Mermaid visualization** from the structured notes (supplier→customer
  edges, chokepoint-colored nodes) to surface single points of failure.
