---
description: Lint the vault — contradictions, stale speculations, orphan articles, index drift
---

Lint the Stocks Vault. Read SCHEMA.md first, then check every note in `Stocks/`,
`Sectors/`, and `Articles/` against these rules and report findings grouped by
severity:

1. **Sourcing** — every Facts / Contracts Awarded / Dilutions / Speculations
   bullet starts `YYYY-MM-DD —` and ends with a source link — an `([[article note]])`
   or a `([[Concept]])` primer — that resolves to a real file in `Articles/` or
   `Concepts/`.
2. **Speculation hygiene** — every speculation carries
   `(status: open|confirmed|busted)`; flag open ones that look resolvable now
   (check against current data via
   `~/Documents/stock-analysis-ui/venv/bin/python` with yfinance).
3. **Orphans & links** — articles not linked from any stock/sector note; stock
   notes missing an article that cites them in `## Articles`; broken [[wikilinks]].
4. **Index drift** — `index.md` sector groupings, counts, and article entries vs
   the actual files on disk.
5. **Conventions** — filenames (`TICKER.md`, exact sector names,
   `YYYY-MM-DD short-slug.md`); required frontmatter present (`ticker`, `sector`,
   `updated` on stocks; full article frontmatter); stock notes carry all schema
   sections (Overview, Snapshot, What's Unique, Competitors, Supply Chain, Facts,
   Contracts Awarded, Dilutions, Speculations, Open Questions, Articles);
   `<!-- prices:start/end -->` and `<!-- snapshot:start/end -->` markers intact.
6. **Contradictions & language** — facts that disagree across notes; any
   buy/sell/hold or position-advice language.
7. **Conflicted copies** — `* 2.md` / iCloud-conflict files: flag in chat only,
   never edit or delete them.
8. **Watchlist sync** — compare notes against the portfolio
   (`sqlite3 -readonly ~/Documents/stock-analysis-ui/data/tracker.db "SELECT
   ticker FROM stocks"`): flag `tracked: false` notes whose ticker is now in the
   portfolio (drop the flag, un-star it in index.md, remove "(watchlist)" in
   sector Members) and portfolio tickers that have no stock note at all. If the
   DB is unreadable, report that and skip this check.
9. **Stock-note sections** — every stock note has non-empty **Overview**,
   **What's Unique** (including a `### Only They Do` sub-section ending with a
   `**Chokepoint:**` rating), and **Competitors**; competitor `[[wikilinks]]`
   resolve to real notes. List competitor tickers/names with no vault note —
   watchlist candidates. Every note also has a **Supply Chain** section
   (`### Suppliers` / `### Customers`, may be empty).
10. **Maps** — every `Maps/` note's wikilinks resolve; flag stocks whose
   Chokepoint rating is Medium+ but which no map references.
11. **Concepts** — every `Concepts/` note's wikilinks resolve; flag concept notes
   not linked from any stock or map (orphans), and concept notes citing hard
   numbers without a `## Sources` footer. Flag a primer's company-specific dated
   finding that isn't reflected on the named holding's Facts.
12. **Supply-chain symmetry** — for every vault member `[[B]]` under A's
   **Suppliers**, B's **Customers** must list `[[A]]` (and vice-versa); flag
   asymmetric vault pairs. External (plain-text) entries are one-sided and exempt.
13. **Snapshot freshness** — each note's machine-maintained `## Snapshot` block
    carries an `_Auto-updated YYYY-MM-DD via yfinance._` line; warn (never fail)
    when that date is older than 7 days — a stale snapshot means the daily refresh
    job (launchd / CI) has stalled and needs attention.

Fix `index.md` drift directly (it is Claude-maintained). For anything that touches
wiki note content, list the proposed fixes and wait for approval. If anything was
changed, bump `updated:` on touched notes and append one line to `log.md`.
