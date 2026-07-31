#!/usr/bin/env python3
"""Fetch a company's earnings press release from SEC EDGAR into _inbox/.

EDGAR is the free, official, key-less source for US filers: an earnings release
is Exhibit 99.1 of an 8-K carrying Item 2.02 ("Results of Operations and
Financial Condition"). This walks

    company_tickers.json -> submissions/CIK##########.json -> <filing>/index.json -> Ex-99.1

and writes the extracted text to `_inbox/<TICKER> <filed> earnings (SEC 8-K).md`
for /ingest-earnings to verify and route. It never edits the vault itself.

Two SEC facts the code depends on:
  * Every request must carry a User-Agent with contact info. A User-Agent
    without an email is answered 403 (measured), so we refuse to send one --
    a clear setup error beats a confusing HTTP failure.
  * Fair-access allows 10 requests/second; a run makes four, sequentially.

Foreign private issuers (TSM, NOK, ARM, ASML, CCJ...) file 6-K instead, with no
item codes to identify earnings by. Rather than guess among hundreds of
undifferentiated 6-Ks, this exits non-zero and tells the caller to clip the
company's own IR release into _inbox/.

Layout mirrors vault_lint.py: the decision logic is pure functions returning
data (unit-tested against trimmed real fixtures, no network), and main() owns
the network, the file write, and the exit codes.
"""
import argparse
import datetime
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT, ".env")

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{name}"
EARNINGS_ITEM = "2.02"
TIMEOUT = 30

EXIT_TICKER, EXIT_NO_8K, EXIT_NO_EXHIBIT, EXIT_HTTP, EXIT_CONFIG = 2, 3, 4, 5, 6


class TickerNotFound(Exception):
    pass


class NoEarnings8K(Exception):
    def __init__(self, message, kind, available=None):
        super().__init__(message)
        self.kind = kind                      # "6k" | "date" | "none"
        self.available = available or []


class NoExhibit(Exception):
    def __init__(self, message, files):
        super().__init__(message)
        self.files = files


class FetchError(Exception):
    pass


class ConfigError(Exception):
    pass


# --- configuration ----------------------------------------------------------

def user_agent():
    """The SEC User-Agent, which must carry a contact email.

    Read from $SEC_EDGAR_UA, falling back to a gitignored .env in the vault
    root -- the contact address is personal and this repo is public.
    """
    ua = os.environ.get("SEC_EDGAR_UA") or _env_file_value("SEC_EDGAR_UA")
    if not ua:
        raise ConfigError(
            "SEC_EDGAR_UA is not set. SEC requires a User-Agent with contact info.\n"
            "  Add it to %s (gitignored):\n"
            '    SEC_EDGAR_UA="Your Name your@email.com"' % ENV_FILE
        )
    if "@" not in ua:
        raise ConfigError(
            "SEC_EDGAR_UA must contain a contact email -- SEC answers 403 without one.\n"
            '  Got: %s\n  Expected shape: "Your Name your@email.com"' % ua
        )
    return ua


def _env_file_value(key):
    try:
        with open(ENV_FILE, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError:
        return None
    for line in lines:
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        if name.strip() == key:
            return value.strip().strip('"').strip("'")
    return None


# --- pure core (unit-tested against fixtures) --------------------------------

def resolve_cik(ticker, tickers_map):
    """Map a ticker to (cik, company name) using SEC's company_tickers.json."""
    want = ticker.strip().upper()
    for entry in tickers_map.values():
        if entry.get("ticker", "").upper() == want:
            return int(entry["cik_str"]), entry["title"]
    raise TickerNotFound(
        "%s is not in SEC's ticker list (foreign listing, delisted, or a typo?)" % want
    )


def pick_8k(submissions, date=None):
    """Select the earnings 8-K from a submissions payload.

    An earnings filing is form "8-K" exactly (8-K/A amendments are a different
    form) carrying Item 2.02. Items are compared per-code, not as a substring.
    Without `date` the newest wins; EDGAR serves filings.recent newest-first.
    """
    recent = submissions.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    matches = []
    for i, form in enumerate(forms):
        if form != "8-K":
            continue
        items = [c.strip() for c in (recent.get("items") or [""] * len(forms))[i].split(",")]
        if EARNINGS_ITEM not in items:
            continue
        matches.append({
            "accession": recent["accessionNumber"][i],
            "acc_nodash": recent["accessionNumber"][i].replace("-", ""),
            "filed": recent["filingDate"][i],
            "period": (recent.get("reportDate") or [""] * len(forms))[i],
            "primary_doc": (recent.get("primaryDocument") or [""] * len(forms))[i],
            "items": (recent.get("items") or [""] * len(forms))[i],
        })

    if date:
        for m in matches:
            if m["filed"] == date:
                return m
        raise NoEarnings8K(
            "no earnings 8-K filed on %s. Available: %s"
            % (date, ", ".join(m["filed"] for m in matches) or "none"),
            kind="date", available=[m["filed"] for m in matches],
        )
    if matches:
        return matches[0]

    if any(f == "6-K" for f in forms):
        raise NoEarnings8K(
            "%s files 6-K (foreign private issuer) -- earnings are not filed as an "
            "8-K Item 2.02 on EDGAR, and 6-Ks carry no item codes to identify them by.\n"
            "  Clip the company's own IR press release into _inbox/ and ingest that instead."
            % submissions.get("name", "this filer"),
            kind="6k",
        )
    raise NoEarnings8K(
        "no 8-K with Item %s found in the filer's recent filings" % EARNINGS_ITEM,
        kind="none",
    )


def pick_exhibit(index_json, primary_doc):
    """Find the press-release exhibit among a filing's files.

    Tiers: a name containing "ex99", else one containing "press", else the
    largest HTML file. The 8-K wrapper itself and EDGAR's generated R*.htm
    viewer renderings are never the release.
    """
    candidates = []
    skipped = []
    for item in index_json.get("directory", {}).get("item", []):
        name = item.get("name", "")
        if not name.lower().endswith((".htm", ".html")):
            skipped.append(name)
            continue
        if name == primary_doc or re.match(r"^R\d+\.htm", name, re.I):
            skipped.append(name)
            continue
        try:
            size = int(item.get("size") or 0)
        except (TypeError, ValueError):
            size = 0
        candidates.append((name, size))

    if not candidates:
        files = [n for n, _ in candidates] + skipped
        raise NoExhibit(
            "no press-release exhibit found; filing contains: %s" % ", ".join(files),
            files=files,
        )
    for needle in ("ex99", "press"):
        hits = [c for c in candidates if needle in c[0].lower()]
        if hits:
            return max(hits, key=lambda c: c[1])[0]
    return max(candidates, key=lambda c: c[1])[0]


def html_to_text(raw):
    """Flatten filing HTML to readable text, keeping table rows on one line."""
    text = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"</t[dh]>", " | ", text, flags=re.I)
    text = re.sub(r"</(tr|p|div|li|h[1-6]|table|section)>", "\n", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text).replace("\xa0", " ")

    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        line = line.strip("|").strip()
        lines.append(line)
    out = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def render_note(meta, text):
    """Render the _inbox/ note: a provenance header plus the release text."""
    fields = [
        ("company", meta["company"]), ("ticker", meta["ticker"]), ("cik", meta["cik"]),
        ("form", "8-K (Item %s)" % EARNINGS_ITEM), ("filed", meta["filed"]),
        ("period", meta["period"]), ("accession", meta["accession"]),
        ("exhibit", meta["exhibit"]), ("url", meta["url"]), ("fetched", meta["fetched"]),
    ]
    header = "\n".join("%s: %s" % (k, v) for k, v in fields)
    return "---\n%s\n---\n\n%s\n" % (header, text)


def inbox_path(root, ticker, filed):
    return os.path.join(root, "_inbox", "%s %s earnings (SEC 8-K).md" % (ticker.upper(), filed))


# --- network ----------------------------------------------------------------

def fetch_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": user_agent(),
                                               "Accept-Encoding": "identity"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        hint = " (SEC rejects a User-Agent without contact info)" if exc.code == 403 else ""
        raise FetchError("HTTP %s for %s%s" % (exc.code, url, hint))
    except urllib.error.URLError as exc:
        raise FetchError("could not reach %s: %s" % (url, exc.reason))


def fetch_json(url):
    return json.loads(fetch_bytes(url).decode("utf-8", "replace"))


# --- entry point ------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ticker", help="ticker symbol, e.g. MU")
    parser.add_argument("--date", metavar="YYYY-MM-DD",
                        help="filing date of a specific earnings 8-K (default: newest)")
    args = parser.parse_args(argv)

    try:
        user_agent()  # fail before any request if the contact email is missing
        cik, company = resolve_cik(args.ticker, fetch_json(TICKERS_URL))
        filing = pick_8k(fetch_json(SUBMISSIONS_URL.format(cik=cik)), args.date)

        dest = inbox_path(ROOT, args.ticker, filing["filed"])
        if os.path.exists(dest):
            print("already fetched: %s" % dest)
            return 0

        base = ARCHIVE_URL.format(cik=cik, acc=filing["acc_nodash"], name="index.json")
        exhibit = pick_exhibit(fetch_json(base), filing["primary_doc"])
        url = ARCHIVE_URL.format(cik=cik, acc=filing["acc_nodash"], name=exhibit)
        text = html_to_text(fetch_bytes(url).decode("utf-8", "replace"))
    except ConfigError as exc:
        print("config: %s" % exc, file=sys.stderr)
        return EXIT_CONFIG
    except TickerNotFound as exc:
        print("ticker: %s" % exc, file=sys.stderr)
        return EXIT_TICKER
    except NoEarnings8K as exc:
        print("no earnings filing: %s" % exc, file=sys.stderr)
        return EXIT_NO_8K
    except NoExhibit as exc:
        print("no exhibit: %s" % exc, file=sys.stderr)
        return EXIT_NO_EXHIBIT
    except FetchError as exc:
        print("fetch failed: %s" % exc, file=sys.stderr)
        return EXIT_HTTP

    meta = {
        "company": company, "ticker": args.ticker.upper(), "cik": cik,
        "filed": filing["filed"], "period": filing["period"],
        "accession": filing["accession"], "exhibit": exhibit, "url": url,
        "fetched": datetime.date.today().isoformat(),
    }
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(render_note(meta, text))

    print("%s %s -- %s chars from %s" % (meta["ticker"], filing["filed"], len(text), exhibit),
          file=sys.stderr)
    print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
