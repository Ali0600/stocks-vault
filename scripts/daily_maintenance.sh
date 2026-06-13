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
    # Rebase onto anything CI pushed while this machine was offline, so the two
    # auto-push paths (launchd + GitHub Actions) can't silently diverge. A
    # conflict aborts cleanly and leaves the commit local for manual resolution.
    if git pull --rebase --autostash -q origin main; then
      git push -q origin main && echo "pushed"
    else
      echo "pull --rebase hit a conflict — commit kept local, push skipped (resolve manually)"
      notify "Stocks Vault ⚠️" "Push conflict — commit kept local; resolve manually"
    fi
  fi
else
  echo "no changes to commit"
fi

exit $LINT_RC
