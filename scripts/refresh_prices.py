#!/usr/bin/env python3
"""Refresh the price table inside each Articles/*.md from yfinance latest closes.

The article's `prices:` frontmatter map is the immutable at-publication baseline;
this script only rewrites the table between the <!-- prices:start/end --> markers
and the "_Prices refreshed_" line. Safe to run repeatedly (idempotent).
"""
import re, glob, os, datetime
import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def latest_close(ticker):
    try:
        h = yf.Ticker(ticker).history(period="5d")["Close"]
        if len(h):
            return round(float(h.iloc[-1]), 2), h.index[-1].date()
    except Exception:
        pass
    return None, None

today = datetime.date.today().isoformat()
changed = []

for f in glob.glob("Articles/*.md"):
    txt = open(f, encoding="utf-8").read()
    fmm = re.search(r'^---\n(.*?)\n---', txt, re.S)
    if not fmm:
        continue
    pm = re.search(r'\n\s*prices:\s*\n((?:\s+[A-Z.]+:\s*[\d.]+\n)+)', fmm.group(1) + "\n")
    if not pm:
        continue
    pub = {}
    for line in pm.group(1).strip().split("\n"):
        k, v = line.split(":")
        pub[k.strip()] = float(v)

    rows, asof = [], None
    for tkr in sorted(pub):
        now, d = latest_close(tkr)
        if now is None:
            now = pub[tkr]
        if d:
            asof = d
        since = (now / pub[tkr] - 1) * 100
        rows.append(f"| {tkr} | ${pub[tkr]:.2f} | ${now:.2f} | {since:+.2f}% |")

    table = ("| Ticker | At publication | Now | Since |\n"
             "| --- | --- | --- | --- |\n" + "\n".join(rows))
    asof_s = f" (latest close {asof})" if asof else ""
    block = (f"<!-- prices:start -->\n{table}\n\n"
             f"_Prices refreshed {today}{asof_s}._\n<!-- prices:end -->")
    new = re.sub(r'<!-- prices:start -->.*?<!-- prices:end -->', lambda m: block, txt, flags=re.S)
    if new != txt:
        open(f, "w", encoding="utf-8").write(new)
        changed.append(os.path.basename(f))

print("refreshed:", ", ".join(changed) if changed else "no changes")
