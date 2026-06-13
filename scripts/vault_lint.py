#!/usr/bin/env python3
"""Stocks Vault integrity lint.

Structural checks over the wiki. Pure stdlib so it runs anywhere (incl. CI).
Exits non-zero on any FAILURE (the CI / pre-commit gate); warnings don't fail.
The DB-backed watchlist check runs only when the tracker DB is present (local).
"""
import re, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def read(f): return open(f, encoding="utf-8").read()

def fm(t):
    m = re.match(r'^---\n(.*?)\n---', t, re.S); d = {}
    if m:
        for line in m.group(1).split("\n"):
            if ':' in line:
                k, v = line.split(':', 1); d[k.strip()] = v.strip()
    return d

def sections(t):
    o = {}; cur = None
    for ln in t.split("\n"):
        h = re.match(r'^## (.+)$', ln)
        if h: cur = h.group(1); o[cur] = []; continue
        if cur is not None: o[cur].append(ln)
    return {k: "\n".join(v) for k, v in o.items()}

def links(s): return [m.split('|')[0].strip() for m in re.findall(r'\[\[([^\]]+)\]\]', s)]

stock_files = sorted(glob.glob("Stocks/*.md"))
tickers = {os.path.splitext(os.path.basename(f))[0] for f in stock_files}
def exists(n): return any(os.path.isfile(f"{d}/{n}.md") for d in ("Stocks", "Sectors", "Maps", "Concepts", "Articles"))

fails, warns = [], []
F = fails.append
W = warns.append

EXPECTED = ["Overview", "What's Unique", "Competitors", "Supply Chain", "Facts",
            "Contracts Awarded", "Dilutions", "Speculations", "Open Questions", "Articles"]
DATED = ("Facts", "Contracts Awarded", "Dilutions", "Speculations")

sup, cus = {}, {}
for f in stock_files:
    t = os.path.splitext(os.path.basename(f))[0]; txt = read(f); S = sections(txt); d = fm(txt)
    for k in ("ticker", "sector", "updated"):
        if k not in d: F(f"{t}: missing frontmatter '{k}'")
    for s in EXPECTED:
        if s not in S: F(f"{t}: missing section '{s}'")
    for s in ("Overview", "What's Unique", "Competitors"):
        if not S.get(s, "").strip(): F(f"{t}: empty '{s}'")
    if "### Only They Do" not in txt: F(f"{t}: missing '### Only They Do'")
    if "**Chokepoint:**" not in txt: F(f"{t}: missing '**Chokepoint:**'")
    if "### Suppliers" not in txt or "### Customers" not in txt: F(f"{t}: missing Supply Chain sub-headers")
    for sec in DATED:
        for ln in S.get(sec, "").split("\n"):
            if ln.strip().startswith("- "):
                if not re.match(r'^- \d{4}-\d{2}-\d{2} —', ln):
                    F(f"{t}[{sec}]: malformed bullet: {ln.strip()[:48]}")
                else:
                    lk = links(ln)
                    if not lk or not (os.path.isfile(f"Articles/{lk[-1]}.md") or os.path.isfile(f"Concepts/{lk[-1]}.md")):
                        F(f"{t}[{sec}]: unsourced: {ln.strip()[:48]}")
                    if sec == "Speculations" and not re.search(r'\(status: (open|confirmed|busted)\)', ln):
                        F(f"{t}: speculation missing status: {ln.strip()[:48]}")
    sc = S.get("Supply Chain", "")
    sm = re.search(r'### Suppliers\n(.*?)(?:\n### Customers|\Z)', sc, re.S)
    cm = re.search(r'### Customers\n(.*)', sc, re.S)
    sup[t] = {x for x in links(sm.group(1)) if x in tickers} if sm else set()
    cus[t] = {x for x in links(cm.group(1)) if x in tickers} if cm else set()

# supply-chain symmetry
for a in tickers:
    for b in cus[a]:
        if a not in sup.get(b, set()): F(f"symmetry: {a}->{b} but {b} Suppliers missing {a}")
    for b in sup[a]:
        if a not in cus.get(b, set()): F(f"symmetry: {b}->{a} but {b} Customers missing {a}")

# broken wikilinks everywhere
scan = glob.glob("Stocks/*.md") + glob.glob("Sectors/*.md") + glob.glob("Maps/*.md") + glob.glob("Concepts/*.md")
if os.path.isfile("index.md"): scan.append("index.md")
for f in scan:
    for n in links(read(f)):
        if not exists(n): F(f"{os.path.basename(f)}: broken [[{n}]]")

# articles: markers, frontmatter, orphans
linked = set()
for f in scan:
    linked |= set(links(read(f)))
for f in glob.glob("Articles/*.md"):
    t = read(f); b = os.path.basename(f)[:-3]
    if "<!-- prices:start -->" not in t or "<!-- prices:end -->" not in t: F(f"article {b}: missing price markers")
    for k in ("title", "url", "source", "published", "tickers", "prices"):
        if k not in fm(t): F(f"article {b}: missing frontmatter '{k}'")
    if b not in linked: W(f"orphan article (unlinked): {b}")

# concepts: sources footer
for f in glob.glob("Concepts/*.md"):
    if "## Sources" not in read(f): W(f"concept {os.path.basename(f)[:-3]}: no '## Sources' footer")

# index drift (sectors)
if os.path.isfile("index.md"):
    idx = read("index.md"); act = {}
    for f in stock_files:
        d = fm(read(f)); s = d.get("sector", "?"); w = d.get("tracked", "").lower() == "false"
        act.setdefault(s, {"h": set(), "w": set()})
        (act[s]["w"] if w else act[s]["h"]).add(os.path.splitext(os.path.basename(f))[0])
    for s, g in act.items():
        lab = f"({len(g['h'])}+{len(g['w'])}*)" if g["w"] else f"({len(g['h'])})"
        line = next((l for l in idx.split("\n") if f"[[{s}]]" in l and "(" in l), "")
        if lab not in line: F(f"index drift: {s} expected {lab} — '{line.strip()[:55]}'")
        mi = set(re.findall(r'\[\[([A-Z]{1,5})\]\]', line.split(':', 1)[1] if ':' in line else ""))
        if mi != g["h"] | g["w"]: F(f"index drift: {s} members {sorted(mi)} != disk {sorted(g['h'] | g['w'])}")

# conflicted copies (warn only)
for f in glob.glob("**/* [0-9].md", recursive=True): W(f"iCloud conflicted copy: {f}")

# watchlist sync (local only)
db = os.path.expanduser("~/Documents/stock-analysis-ui/data/tracker.db")
if os.path.isfile(db):
    import sqlite3
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        port = {r[0] for r in con.execute("SELECT ticker FROM stocks")}; con.close()
        for f in stock_files:
            t = os.path.splitext(os.path.basename(f))[0]; d = fm(read(f)); wl = d.get("tracked", "").lower() == "false"
            if wl and t in port: W(f"watchlist: {t} is tracked:false but IS in portfolio — promote")
            if not wl and t not in port: W(f"watchlist: {t} is a holding note but NOT in portfolio")
        for t in sorted(port - tickers): W(f"watchlist: {t} in portfolio but has no note")
    except Exception as e:
        W(f"watchlist check skipped: {e}")
else:
    W("watchlist check skipped (tracker DB not present)")

print(f"Stocks Vault lint — {len(stock_files)} stock notes, {len(glob.glob('Concepts/*.md'))} concepts, {len(glob.glob('Articles/*.md'))} articles")
if warns:
    print(f"\n{len(warns)} warning(s):")
    for w in warns: print("  - " + w)
if fails:
    print(f"\n{len(fails)} FAILURE(s):")
    for x in fails: print("  - " + x)
    print("\nLINT FAILED")
    sys.exit(1)
print("\nLINT PASSED — all structural checks clean")
sys.exit(0)
