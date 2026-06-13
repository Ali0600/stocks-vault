"""Unit tests for scripts/vault_lint.py.

Each test builds a minimal *valid* vault in a tmp dir, then mutates one thing to
prove a specific rule fires. Asserting on `fails` (not `warns`) keeps the tests
hermetic — the local watchlist/DB check only ever emits warnings, so it can't
flip a baseline. Run: `pytest scripts/tests`.
"""
import datetime
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import vault_lint  # noqa: E402

TODAY = datetime.date.today().isoformat()


def stock_note(ticker="FOO", sector="Test", overview="A test company.",
               suppliers="", customers="", facts="", speculations="", extra="",
               updated=TODAY):
    """Render a structurally valid stock note (all required sections/markers)."""
    return f"""---
ticker: {ticker}
sector: {sector}
updated: {updated}
---
# {ticker} Inc ({ticker})

## Overview
{overview}{extra}

## Snapshot
<!-- snapshot:start -->
| Mkt cap | Revenue (TTM) | Rev growth | Net margin | P/E | Next earnings |
| --- | --- | --- | --- | --- | --- |
| $1B | $1B | +0% | 0% | n/m | — |

_Auto-updated {updated} via yfinance._
<!-- snapshot:end -->

## What's Unique
Does a unique thing.

### Only They Do
- Some exclusivity
- **Chokepoint:** Low — limited.

## Competitors
- Rival Inc (RVL) — overlaps on widgets

## Supply Chain
### Suppliers
{suppliers}
### Customers
{customers}

## Facts
{facts}

## Contracts Awarded

## Dilutions

## Speculations
{speculations}

## Open Questions

## Articles
"""


def write_vault(tmp_path, notes):
    """notes: {ticker: content}. Returns the vault root as an absolute string."""
    (tmp_path / "Stocks").mkdir()
    for tk, content in notes.items():
        (tmp_path / "Stocks" / f"{tk}.md").write_text(content, encoding="utf-8")
    return str(tmp_path)


def add_concept(tmp_path, name="Test"):
    d = tmp_path / "Concepts"
    d.mkdir(exist_ok=True)
    (d / f"{name}.md").write_text(f"# {name}\n\n## Sources\n- https://example.com\n", encoding="utf-8")


@pytest.fixture(autouse=True)
def restore_cwd():
    """lint() chdir's into the vault root; put the process back afterwards."""
    cwd = os.getcwd()
    yield
    os.chdir(cwd)


# --- baseline -------------------------------------------------------------

def test_clean_vault_passes(tmp_path):
    root = write_vault(tmp_path, {"FOO": stock_note("FOO")})
    fails, _, counts = vault_lint.lint(root)
    assert fails == [], fails
    assert counts[0] == 1  # one stock note


# --- one test per failure rule -------------------------------------------

def test_missing_section_fails(tmp_path):
    note = stock_note("FOO").replace("## Facts\n", "", 1)
    root = write_vault(tmp_path, {"FOO": note})
    fails, _, _ = vault_lint.lint(root)
    assert any("missing section 'Facts'" in f for f in fails), fails


def test_unsourced_dated_bullet_fails(tmp_path):
    note = stock_note("FOO", facts="- 2026-06-13 — a thing happened (no link)")
    root = write_vault(tmp_path, {"FOO": note})
    fails, _, _ = vault_lint.lint(root)
    assert any("unsourced" in f for f in fails), fails


def test_malformed_bullet_fails(tmp_path):
    note = stock_note("FOO", facts="- just a plain bullet with no date")
    root = write_vault(tmp_path, {"FOO": note})
    fails, _, _ = vault_lint.lint(root)
    assert any("malformed bullet" in f for f in fails), fails


def test_speculation_missing_status_fails(tmp_path):
    add_concept(tmp_path)
    note = stock_note("FOO", speculations="- 2026-06-13 — a forecast ([[Test]])")
    root = write_vault(tmp_path, {"FOO": note})
    fails, _, _ = vault_lint.lint(root)
    assert any("speculation missing status" in f for f in fails), fails
    assert not any("unsourced" in f for f in fails), "source [[Test]] should resolve"


def test_broken_wikilink_fails(tmp_path):
    note = stock_note("FOO", extra=" See [[Nonexistent]].")
    root = write_vault(tmp_path, {"FOO": note})
    fails, _, _ = vault_lint.lint(root)
    assert any("broken [[Nonexistent]]" in f for f in fails), fails


def test_supply_chain_asymmetry_fails(tmp_path):
    foo = stock_note("FOO", customers="- [[BAR]] — buys widgets")
    bar = stock_note("BAR")  # BAR's Suppliers does not list FOO
    root = write_vault(tmp_path, {"FOO": foo, "BAR": bar})
    fails, _, _ = vault_lint.lint(root)
    assert any("symmetry" in f and "BAR" in f for f in fails), fails


# --- the map's dependency-graph markers (warn-only) -----------------------

def test_map_missing_graph_markers_warns(tmp_path):
    root = write_vault(tmp_path, {"FOO": stock_note("FOO")})
    (tmp_path / "Maps").mkdir()
    (tmp_path / "Maps" / "AI Supply Chain.md").write_text(
        "# AI Supply Chain\n\n## Key dependencies\n- x\n", encoding="utf-8")
    fails, warns, _ = vault_lint.lint(root)
    assert fails == [], fails
    assert any("dependency-graph markers" in w for w in warns), warns


# --- freshness heartbeat is warn-only, never a failure --------------------

def test_stale_snapshot_warns_but_does_not_fail(tmp_path):
    old = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    note = stock_note("FOO").replace(
        f"_Auto-updated {TODAY} via yfinance._",
        f"_Auto-updated {old} via yfinance._",
    )
    root = write_vault(tmp_path, {"FOO": note})
    fails, warns, _ = vault_lint.lint(root)
    assert fails == [], fails
    assert any("snapshot stale" in w for w in warns), warns
