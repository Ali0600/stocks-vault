#!/usr/bin/env python3
"""Refresh the machine-maintained `## Snapshot` fundamentals block in each Stocks/*.md.

Pulls market cap, TTM revenue, revenue growth, net margin, P/E and next-earnings
date from yfinance and rewrites the block between <!-- snapshot:start/end -->.
Self-installing: if a note has no Snapshot section yet, it inserts one right after
Overview (before What's Unique). Idempotent; safe to run repeatedly.

This is auto-maintained market data (like the article price table) — not a curated
fact, and exempt from the dated-citation rule. It does NOT touch frontmatter.
"""
import re, glob, os, datetime
import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = datetime.date.today().isoformat()


def cap(v):
    if not v: return "—"
    if v >= 1e12: return f"${v/1e12:.2f}T"
    if v >= 1e9:  return f"${v/1e9:.0f}B"
    if v >= 1e6:  return f"${v/1e6:.0f}M"
    return f"${v:.0f}"


def rev(v):
    if not v: return "—"
    return f"${v/1e9:.1f}B" if v >= 1e9 else f"${v/1e6:.0f}M"


def pe(trailing, forward):
    if trailing and trailing > 0: return f"{trailing:.1f}"
    if forward and forward > 0:   return f"{forward:.1f}f"
    return "n/m"


def next_earnings(tk):
    try:
        cal = tk.calendar
        if isinstance(cal, dict):
            ed = cal.get("Earnings Date")
            if ed:
                return str(ed[0] if isinstance(ed, list) else ed)
    except Exception:
        pass
    return "—"


def snapshot_row(ticker):
    tk = yf.Ticker(ticker); i = tk.info
    has_rev = bool(i.get("totalRevenue"))
    return {
        "cap": cap(i.get("marketCap")),
        "rev": rev(i.get("totalRevenue")),
        "growth": f"{i['revenueGrowth']*100:+.0f}%" if has_rev and i.get("revenueGrowth") is not None else "—",
        "margin": f"{i['profitMargins']*100:.0f}%" if has_rev and i.get("profitMargins") is not None else "—",
        "pe": pe(i.get("trailingPE"), i.get("forwardPE")),
        "earn": next_earnings(tk),
    }


def block(r):
    return ("<!-- snapshot:start -->\n"
            "| Mkt cap | Revenue (TTM) | Rev growth | Net margin | P/E | Next earnings |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            f"| {r['cap']} | {r['rev']} | {r['growth']} | {r['margin']} | {r['pe']} | {r['earn']} |\n\n"
            f"_Auto-updated {TODAY} via yfinance._\n"
            "<!-- snapshot:end -->")


updated = []
for f in sorted(glob.glob("Stocks/*.md")):
    ticker = os.path.splitext(os.path.basename(f))[0]
    txt = open(f, encoding="utf-8").read()
    try:
        blk = block(snapshot_row(ticker))
    except Exception as e:
        print(f"  ! {ticker}: fetch failed ({e}); left unchanged")
        continue
    if "<!-- snapshot:start -->" in txt:
        new = re.sub(r'<!-- snapshot:start -->.*?<!-- snapshot:end -->', lambda m: blk, txt, flags=re.S)
    else:
        new = txt.replace("## What's Unique", f"## Snapshot\n{blk}\n\n## What's Unique", 1)
    if new != txt:
        open(f, "w", encoding="utf-8").write(new)
        updated.append(ticker)

print(f"snapshot refreshed: {len(updated)} note(s)")
