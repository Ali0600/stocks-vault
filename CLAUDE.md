# Stocks Vault

LLM-maintained stock research wiki. **Read SCHEMA.md before changing anything** —
it is the contract for structure, sourcing rules, and bookkeeping. `index.md` is
the catalog; `log.md` is append-only history.

- `Stocks/`, `Sectors/`, `Maps/`, `Concepts/` — wiki notes (Claude-maintained; the human edits freely)
- `Articles/`, `_inbox/` — raw sources, immutable once ingested
- The tracker app (`~/Documents/stock-analysis-ui`) only **reads** this vault

## Workflows
- `/ingest-article <url-or-inbox-path>` — fetch, verify, file, route takeaways
- `/vault-lint` — consistency check across the vault

## Market data
Fetch prices with yfinance through the tracker's venv:
`~/Documents/stock-analysis-ui/venv/bin/python -c "import yfinance; ..."`

Portfolio source of truth:
`sqlite3 -readonly ~/Documents/stock-analysis-ui/data/tracker.db "SELECT ticker FROM stocks"`
— stock notes with `tracked: false` are watchlist (article-discovered, no position).
The app builds its stock **list** from the `stocks` table (grouped by `sectors`) and only
opens a vault note for a stock already in it — so a vault-only watchlist note does **not**
appear in the app. "Add a stock to the tracker" = INSERT into `stocks` (back up the DB
first), then drop the note's `tracked: false`; sector names must match the `Sectors/*.md`
filenames. lint #8 flags a `tracked: false` note that's actually in the DB.

Never use buy/sell/hold or position-advice language anywhere in the vault.
