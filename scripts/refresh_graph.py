#!/usr/bin/env python3
"""Generate the supply-chain dependency graph (Mermaid) into the AI Supply Chain map.

Parses every Stocks/*.md note's `## Supply Chain` → `### Suppliers` / `### Customers`
sub-lists, builds the directed supplier→customer edge set across vault members, and
renders a Mermaid `graph LR` with nodes colored by each note's `**Chokepoint:**`
rating so bottlenecks pop visually. Writes between <!-- graph:start/end --> in
`Maps/AI Supply Chain.md` (self-installing). Pure stdlib, deterministic, idempotent.

Like the per-note Snapshot block this is machine-maintained market structure derived
from the notes — exempt from the dated-citation rule, and it does not bump `updated:`.
"""
import re, glob, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = datetime.date.today().isoformat()
MAP = "Maps/AI Supply Chain.md"


def section(txt, name):
    m = re.search(rf'^## {re.escape(name)}\n(.*?)(?=^## |\Z)', txt, re.S | re.M)
    return m.group(1) if m else ""


def sub(txt, name):
    m = re.search(rf'### {re.escape(name)}\n(.*?)(?=\n### |\Z)', txt, re.S)
    return m.group(1) if m else ""


def links(s):
    return [m.split('|')[0].strip() for m in re.findall(r'\[\[([^\]]+)\]\]', s)]


def choke_class(txt):
    # Read only the rating token, up to the em-dash separator — the explanation
    # after it often names other tiers ("...so not Extreme") and must not match.
    m = re.search(r'\*\*Chokepoint:\*\*\s*([^\n—]+)', txt)
    s = (m.group(1) if m else "").lower()
    for k in ("extreme", "high", "medium", "low"):
        if k in s:
            return k
    return "none"


stock_files = sorted(glob.glob("Stocks/*.md"))
tickers = {os.path.splitext(os.path.basename(f))[0] for f in stock_files}
choke, edges = {}, set()
for f in stock_files:
    t = os.path.splitext(os.path.basename(f))[0]
    txt = open(f, encoding="utf-8").read()
    choke[t] = choke_class(txt)
    sc = section(txt, "Supply Chain")
    for x in links(sub(sc, "Suppliers")):
        if x in tickers:
            edges.add((x, t))          # supplier x → this note
    for y in links(sub(sc, "Customers")):
        if y in tickers:
            edges.add((t, y))          # this note → customer y

nodes = sorted({n for e in edges for n in e})

CLASSDEF = [
    "  classDef extreme fill:#b91c1c,color:#fff,stroke:#7f1d1d,stroke-width:2px;",
    "  classDef high fill:#ea580c,color:#fff,stroke:#9a3412;",
    "  classDef medium fill:#ca8a04,color:#fff,stroke:#713f12;",
    "  classDef low fill:#3f3f46,color:#fff,stroke:#18181b;",
    "  classDef none fill:#52525b,color:#fff,stroke:#27272a;",
]

lines = ["graph LR"] + CLASSDEF
lines += [f"  {n}[{n}]:::{choke.get(n, 'none')}" for n in nodes]
lines += [f"  {a} --> {b}" for a, b in sorted(edges)]
mermaid = "\n".join(lines)

block = (
    "<!-- graph:start -->\n"
    "```mermaid\n" + mermaid + "\n```\n\n"
    f"_Nodes colored by chokepoint severity (Extreme/High = red/orange, Medium = "
    f"amber, Low = grey). {len(nodes)} nodes, {len(edges)} edges. Auto-generated "
    f"{TODAY} from each note's Supply Chain section._\n"
    "<!-- graph:end -->"
)

txt = open(MAP, encoding="utf-8").read()
if "<!-- graph:start -->" in txt:
    new = re.sub(r'<!-- graph:start -->.*?<!-- graph:end -->', lambda m: block, txt, flags=re.S)
else:
    section_md = f"## Dependency graph\n{block}\n\n"
    if "## Key dependencies" in txt:
        new = txt.replace("## Key dependencies", section_md + "## Key dependencies", 1)
    elif "## Related" in txt:
        new = txt.replace("## Related", section_md + "## Related", 1)
    else:
        new = txt.rstrip() + "\n\n" + section_md

if new != txt:
    open(MAP, "w", encoding="utf-8").write(new)
    print(f"graph refreshed: {len(nodes)} nodes, {len(edges)} edges")
else:
    print("graph unchanged")
