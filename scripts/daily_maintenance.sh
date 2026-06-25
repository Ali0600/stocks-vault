#!/bin/bash
# Daily Stocks Vault maintenance: refresh prices/fundamentals/graph, lint,
# commit if anything changed, and alert (macOS notification) on any failure.
# Wired to launchd (see scripts/com.stocksvault.maintenance.plist).
set -uo pipefail

VAULT="/Users/ah/Documents/Stocks Vault"
PY="$HOME/Documents/stock-analysis-ui/venv/bin/python"

# Post a macOS notification (best-effort; never fail the run if it can't).
notify() { /usr/bin/osascript -e "display notification \"$2\" with title \"$1\"" >/dev/null 2>&1 || true; }

cd "$VAULT" || exit 1
echo "=== vault maintenance $(date) ==="

# Safety: never run on a tree left in a conflicted/marker state by a prior failure
# (otherwise the refresh would commit marker-laden files and cascade).
if grep -rlq '^<<<<<<< ' Stocks/ Articles/ Maps/ index.md 2>/dev/null; then
  echo "conflict markers present — aborting; resolve the vault first"
  notify "Stocks Vault ⚠️" "Conflict markers in vault — daily run aborted"
  exit 1
fi

"$PY" scripts/refresh_prices.py
"$PY" scripts/refresh_fundamentals.py
"$PY" scripts/refresh_graph.py
"$PY" scripts/vault_lint.py
LINT_RC=$?
if [[ $LINT_RC -ne 0 ]]; then
  notify "Stocks Vault ⚠️" "Daily lint FAILED — commit gated. See .maintenance.log"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "chore: daily refresh (prices + fundamentals + graph) + lint ($(date +%F))"
  echo "committed changes"
  if git remote get-url origin >/dev/null 2>&1; then
    # This machine is the authoritative refresher (CI no longer commits). Rebase
    # onto any commits already on origin (e.g. curated pushes), then push. On
    # conflict, ABORT the rebase so the tree is never left with markers/stashes —
    # the commit stays local and the next run retries cleanly.
    if git pull --rebase -q origin main; then
      git push -q origin main && echo "pushed" || echo "push failed — will retry next run"
    else
      git rebase --abort 2>/dev/null || true
      echo "rebase conflict — aborted to keep the tree clean; commit kept local"
      notify "Stocks Vault ⚠️" "Refresh rebase conflict — commit kept local; tree clean"
    fi
  fi
else
  echo "no changes to commit"
fi

exit $LINT_RC
