# Stocks Vault — Schema & Conventions

An LLM-maintained wiki (Karpathy pattern) for stocks and market sectors.
Claude reads this file before touching the vault.

## Layers
1. **Raw sources** — `Articles/` and `_inbox/`. Immutable once ingested (only
   the auto-refreshed price table inside an article note may change).
2. **Wiki** — `Stocks/`, `Sectors/`, `Maps/`, and `Concepts/` notes. Maintained by
   Claude; the human edits anything at will in Obsidian. Maps are cross-cutting
   notes (e.g. supply chains) that wire stock notes together with wikilinks;
   Concepts are short technology/mechanism primers, wikilinked from the stocks and
   maps that touch them.
3. **Schema** — this file.

`index.md` is the catalog (read it first). `log.md` is an append-only
chronological record of every change.

## Division of labor
- **Human**: curates sources (URLs or files in `_inbox/`), asks questions,
  reviews and edits notes.
- **Claude**: all bookkeeping — summarizing, fact-checking, routing takeaways,
  cross-linking, maintaining `index.md` and `log.md`.
- **The tracker app** (`~/Documents/stock-analysis-ui`) only READS this vault;
  it renders stock/sector notes and article price impact in its detail views.

## Rules
- Every dated-event bullet (**Facts**, **Contracts Awarded**, **Dilutions**,
  **Speculations**): `- YYYY-MM-DD — <statement> (<source>)`, where `<source>` is
  an `[[article note]]` **or** a `[[Concept]]` primer whose `## Sources` back the
  claim. No unsourced claims in wiki notes. Article-sourced facts use the
  event/publish date; concept-sourced facts use the **recording date** (the
  statement carries any historical timing, e.g. "entered volume production in Q4
  2025").
- **Fact** = verified against market data or corroborated reporting. Route durable
  signal the tracker app can't give — supply-chain moves, contracts,
  competitive/exclusivity shifts, product/tech milestones, regulation, catalysts,
  business fundamentals (revenue, segment splits, margins, backlog). Do **not**
  route stock-price performance (closes, YTD %, period/day returns): the
  `## Snapshot` block and the tracker app already cover price/returns — verify a
  cited price figure for accuracy, then drop it. (Business metric "revenue +51% YoY"
  stays; stock metric "+402% YTD" does not.)
  **Speculation** = forecast or unverified claim; ends with `(status: open)`.
  When later evidence lands, flip to `confirmed`/`busted` with the new date and
  source rather than deleting.
- Stock notes carry two descriptive sections after **Overview**: **What's Unique**
  (1–2 sentences on the genuine differentiator or moat) and **Competitors**
  (bullets — `[[TICKER]]` for a rival that has a vault note, `Name (TICKER)`
  otherwise, each with a short overlap phrase). Like Overview, these are durable
  prose, exempt from the dated-citation rule above. Competitor tickers without a
  vault note are watchlist candidates.
- Inside **What's Unique**, a `### Only They Do` sub-section: bullets for genuine
  exclusivity — sole-supplier positions, proprietary process/patents, regulatory
  or IP exclusivities (mark company-claimed ones as such) — ending with a
  `**Chokepoint:**` line (None/Low/Medium/High/Extreme — why), rating whether that
  exclusivity gates the AI build-out or the company's own niche. Keep honest:
  "Low" is a fine answer; never inflate exclusivity to justify a rating.
- Stock notes also track two dated/sourced event streams (same bullet format and
  Fact/Speculation verification labels as above): **Contracts Awarded** — customer
  wins, government/defense awards, offtake or purchase commitments, named
  partnerships with disclosed scope — and **Dilutions** — equity raises (ATM,
  secondary, PIPE), convertible notes, warrant/option overhang, and share-count
  changes like reverse/forward splits. Route an event to its most specific section
  (a contract → Contracts Awarded, not Facts); don't duplicate. Both may be empty.
- Stock notes carry a **Supply Chain** section (after Competitors) with
  `### Suppliers` and `### Customers` sub-lists — who the company buys critical
  inputs from and who buys from it. Bullets: `[[TICKER]]` for vault members,
  `Name (external)` otherwise, + what flows + a criticality flag (sole-source
  and/or the supplier's chokepoint rating) so bottlenecks pop. Durable prose like
  Competitors (exempt from the dated-citation rule; specific dated supply *deals*
  still go to Contracts Awarded). **Bidirectional:** when both ends are vault
  members the edge appears on both notes (A's Suppliers `[[B]]` ⇔ B's Customers
  `[[A]]`); external names appear one-sided. May be empty.
- Stock notes carry a machine-maintained **Snapshot** block (after Overview,
  between `<!-- snapshot:start/end -->`) — market cap, TTM revenue, revenue growth,
  net margin, P/E, next-earnings date — auto-refreshed by
  `scripts/refresh_fundamentals.py` via yfinance. Like the article price table it's
  a mutable exception, exempt from the dated-citation rule; don't hand-edit, and the
  refresh does not bump `updated:`. It is data, never advice.
- The `Maps/AI Supply Chain` note carries a machine-generated **dependency graph**
  (Mermaid) between `<!-- graph:start/end -->`, rebuilt by `scripts/refresh_graph.py`
  from every stock note's Supply Chain edges and colored by each note's
  `**Chokepoint:**` rating. Like the Snapshot block it's a mutable, auto-maintained
  exception — don't hand-edit it, and the rebuild doesn't bump `updated:`. The curated
  prose around it (chain layers, ranked chokepoints, fan-in/fan-out reading) stays
  human/Claude-maintained.
- Never use buy/sell/hold or position-advice language anywhere in the vault.
- Article frontmatter `prices:` = close on the publish date (prior close on
  non-trading days; ingestion-day price if the publish date is unknown — note it).
- Filenames: stocks `TICKER.md` · sectors exactly the sector name ·
  articles `YYYY-MM-DD short-slug.md` · concepts the concept name (`Concepts/HBM.md`).
- Stock notes are portfolio holdings by default. Article-discovered tickers get
  **watchlist** notes — `tracked: false` in frontmatter, `*` after the ticker in
  `index.md`, "(watchlist)" in sector Members — when coverage has routable
  claims; passing mentions stay article-only. Portfolio source of truth: the
  `stocks` table in `~/Documents/stock-analysis-ui/data/tracker.db`; drop the
  flag when a ticker joins the portfolio.
- Stock-note sections, in order: Overview · Snapshot · What's Unique (with its
  `### Only They Do` sub-section) · Competitors · Supply Chain (`### Suppliers` /
  `### Customers`) · Facts · Contracts Awarded · Dilutions · Speculations ·
  Open Questions · Articles.
- **Concept notes** (`Concepts/<Name>.md`, e.g. `[[HBM]]`): short "simple but
  technical" primers on a mechanism, technology, or market structure — 1–2
  paragraphs, then an `## In this vault` link list and a `## Sources` footer (web
  links; required when the note cites hard numbers). Durable prose, exempt from the
  dated-citation rule; not company-scoped — they explain the shared mechanism that
  per-company `### Only They Do` sections reference. Link them from the natural
  first mention in the stocks/maps that touch them (aliased, e.g.
  `[[Optical interconnect|transceivers]]`). When a primer documents a
  company-specific dated finding about a holding, also record it on that holding's
  Facts citing the primer (market-wide structure may stay in the primer, or go to
  the relevant Sector note) — don't leave routable research stranded in prose.
- After any change: bump `updated:` on touched notes, refresh `index.md`,
  append one line to `log.md`. Never rewrite `log.md` history.
- Ignore Obsidian/iCloud conflicted copies (`NVDA 2.md`) — flag them in chat.

## Workflows
- **Ingest** an article: `/ingest-article <url-or-inbox-path>` in Claude Code.
- **Lint** the vault: `/vault-lint` — contradictions, stale speculations,
  orphan articles, missing links.
- **Synthesis**: when the tracker's AI analyses are regenerated, they must be
  grounded in each stock's vault Facts/Speculations.

*Vault created 2026-06-11.*
