"""Tests for fetch_earnings.py — the SEC EDGAR earnings-release fetcher.

Every check here runs against JSON fixtures trimmed from real EDGAR responses
(see scripts/tests/fixtures/), so the suite is hermetic: the autouse fixture
below makes any network call raise, which proves the decision logic is pure.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import fetch_earnings as fe  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def fixture(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """The pure core must never reach the network."""
    def boom(url):
        raise AssertionError("network call in a unit test: %s" % url)
    monkeypatch.setattr(fe, "fetch_bytes", boom)


TICKERS_MAP = {
    "0": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA CORP"},
    "1": {"cik_str": 723125, "ticker": "MU", "title": "MICRON TECHNOLOGY INC"},
}


# --- resolve_cik ------------------------------------------------------------

def test_resolve_cik_finds_ticker():
    assert fe.resolve_cik("MU", TICKERS_MAP) == (723125, "MICRON TECHNOLOGY INC")


def test_resolve_cik_is_case_insensitive():
    assert fe.resolve_cik("mu", TICKERS_MAP)[0] == 723125


def test_resolve_cik_unknown_raises():
    with pytest.raises(fe.TickerNotFound):
        fe.resolve_cik("ZZZZ", TICKERS_MAP)


# --- pick_8k ----------------------------------------------------------------

def test_pick_8k_returns_newest_earnings_filing():
    got = fe.pick_8k(fixture("mu_submissions.json"))
    assert got["accession"] == "0000723125-26-000013"
    assert got["filed"] == "2026-06-24"
    assert got["acc_nodash"] == "000072312526000013"
    assert got["primary_doc"] == "mu-20260624.htm"


def test_pick_8k_skips_newer_non_earnings_8k():
    """A 5.02 (officer change) 8-K filed later must not win — the items filter,
    not just the form, decides."""
    assert fe.pick_8k(fixture("mu_submissions.json"))["filed"] != "2026-06-29"


def test_pick_8k_excludes_8ka_amendments():
    """8-K/A is a different form; a prefix match would wrongly select it."""
    assert fe.pick_8k(fixture("mu_submissions.json"))["accession"] != "0000723125-26-000099"


def test_pick_8k_tolerates_spaces_in_items():
    got = fe.pick_8k(fixture("mu_submissions.json"), date="2026-05-01")
    assert got["accession"] == "0000723125-26-000097"


def test_pick_8k_honours_date():
    got = fe.pick_8k(fixture("mu_submissions.json"), date="2026-03-18")
    assert got["accession"] == "0000723125-26-000004"
    assert got["filed"] == "2026-03-18"


def test_pick_8k_unmatched_date_lists_available_dates():
    with pytest.raises(fe.NoEarnings8K) as exc:
        fe.pick_8k(fixture("mu_submissions.json"), date="2026-01-01")
    assert exc.value.kind == "date"
    assert "2026-06-24" in exc.value.available
    assert "2026-03-18" in exc.value.available
    assert "2026-06-29" not in exc.value.available  # non-earnings 8-K


def test_pick_8k_foreign_private_issuer_names_the_fallback():
    with pytest.raises(fe.NoEarnings8K) as exc:
        fe.pick_8k(fixture("fpi_submissions.json"))
    assert exc.value.kind == "6k"
    msg = str(exc.value)
    assert "6-K" in msg and "_inbox" in msg


def test_pick_8k_no_earnings_filing_at_all():
    with pytest.raises(fe.NoEarnings8K) as exc:
        fe.pick_8k(fixture("no_earnings_submissions.json"))
    assert exc.value.kind == "none"


# --- pick_exhibit -----------------------------------------------------------

def test_pick_exhibit_prefers_ex99():
    got = fe.pick_exhibit(fixture("mu_filing_index.json"), "mu-20260624.htm")
    assert got == "a2026q3ex991-pressrelease.htm"


def test_pick_exhibit_falls_back_to_press_then_largest():
    press = {"directory": {"item": [
        {"name": "wrapper.htm", "size": "9000"},
        {"name": "d123-pressrelease.htm", "size": "50"},
        {"name": "other.htm", "size": "80000"},
    ]}}
    assert fe.pick_exhibit(press, "wrapper.htm") == "d123-pressrelease.htm"

    largest = {"directory": {"item": [
        {"name": "wrapper.htm", "size": "9000"},
        {"name": "small.htm", "size": "1200"},
        {"name": "big.htm", "size": "240000"},
    ]}}
    assert fe.pick_exhibit(largest, "wrapper.htm") == "big.htm"


def test_pick_exhibit_ignores_noise_and_non_html():
    """R*.htm viewer renderings, images and XML are never press releases."""
    noise = {"directory": {"item": [
        {"name": "mu-20260624.htm", "size": "28554"},
        {"name": "R1.htm", "size": "999999"},
        {"name": "chart.jpg", "size": "888888"},
        {"name": "data.xml", "size": "777777"},
    ]}}
    with pytest.raises(fe.NoExhibit) as exc:
        fe.pick_exhibit(noise, "mu-20260624.htm")
    assert "R1.htm" in exc.value.files


# --- html_to_text -----------------------------------------------------------

def test_html_to_text_strips_tags_and_unescapes():
    out = fe.html_to_text(
        "<html><style>b{color:red}</style><script>x=1</script>"
        "<p>Revenue of $41.46&nbsp;billion</p><p>Micron&#8217;s record</p></html>"
    )
    assert "color:red" not in out and "x=1" not in out
    assert "Revenue of $41.46 billion" in out
    assert "’" in out  # entity decoded, not left as &#8217;


def test_html_to_text_keeps_table_rows_on_one_line():
    out = fe.html_to_text(
        "<table><tr><td>Revenue</td><td>41,456</td><td>23,860</td></tr>"
        "<tr><td>Net income</td><td>28,243</td><td>13,785</td></tr></table>"
    )
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines[0] == "Revenue | 41,456 | 23,860"
    assert lines[1] == "Net income | 28,243 | 13,785"


# --- render_note / inbox_path ----------------------------------------------

def test_render_note_header_carries_every_provenance_field():
    meta = {
        "company": "MICRON TECHNOLOGY INC", "ticker": "MU", "cik": 723125,
        "filed": "2026-06-24", "period": "2026-06-24",
        "accession": "0000723125-26-000013",
        "exhibit": "a2026q3ex991-pressrelease.htm",
        "url": "https://www.sec.gov/Archives/edgar/data/723125/000072312526000013/"
               "a2026q3ex991-pressrelease.htm",
        "fetched": "2026-07-31",
    }
    note = fe.render_note(meta, "Revenue of $41.46 billion")
    for key, value in meta.items():
        assert "%s: %s" % (key, value) in note
    assert note.startswith("---\n")
    assert note.count("---\n") >= 2
    assert note.rstrip().endswith("Revenue of $41.46 billion")
    assert "form: 8-K (Item 2.02)" in note


def test_inbox_path_is_stable():
    got = fe.inbox_path("/vault", "MU", "2026-06-24")
    assert got == "/vault/_inbox/MU 2026-06-24 earnings (SEC 8-K).md"


# --- user agent -------------------------------------------------------------

def test_user_agent_requires_a_contact_email(monkeypatch):
    """SEC returns 403 for any User-Agent without contact info, so refuse to
    send one rather than surfacing a confusing HTTP error."""
    monkeypatch.setenv("SEC_EDGAR_UA", "stocks-vault/1.0 (+https://github.com/x/y)")
    with pytest.raises(fe.ConfigError):
        fe.user_agent()


def test_user_agent_accepts_a_contact_email(monkeypatch):
    monkeypatch.setenv("SEC_EDGAR_UA", "Stocks Vault research someone@example.com")
    assert fe.user_agent() == "Stocks Vault research someone@example.com"


def test_user_agent_unset_explains_the_setup(monkeypatch):
    monkeypatch.delenv("SEC_EDGAR_UA", raising=False)
    monkeypatch.setattr(fe, "ENV_FILE", os.path.join(FIXTURES, "does-not-exist.env"))
    with pytest.raises(fe.ConfigError) as exc:
        fe.user_agent()
    assert "SEC_EDGAR_UA" in str(exc.value) and ".env" in str(exc.value)


def test_user_agent_reads_gitignored_env_file(monkeypatch, tmp_path):
    """The contact email is personal, so it lives in a gitignored .env rather
    than in the committed default."""
    env = tmp_path / ".env"
    env.write_text('# comment\nSEC_EDGAR_UA="Stocks Vault research me@example.com"\n')
    monkeypatch.delenv("SEC_EDGAR_UA", raising=False)
    monkeypatch.setattr(fe, "ENV_FILE", str(env))
    assert fe.user_agent() == "Stocks Vault research me@example.com"
