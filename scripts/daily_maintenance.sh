#!/bin/bash
# Daily Stocks Vault maintenance: refresh prices, lint, commit if anything changed.
# Wired to launchd (see scripts/com.stocksvault.maintenance.plist).
set -uo pipefail

VAULT="/Users/ah/Documents/Stocks Vault"
PY="$HOME/Documents/stock-analysis-ui/venv/bin/python"

cd "$VAULT" || exit 1
echo "=== vault maintenance $(date) ==="

"$PY" scripts/refresh_prices.py
"$PY" scripts/refresh_fundamentals.py
"$PY" scripts/vault_lint.py
LINT_RC=$?

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "chore: daily refresh (prices + fundamentals) + lint ($(date +%F))"
  git remote get-url origin >/dev/null 2>&1 && git push -q && echo "pushed"
  echo "committed changes"
else
  echo "no changes to commit"
fi

exit $LINT_RC
