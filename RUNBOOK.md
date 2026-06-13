# Runbook — Stocks Vault automation

Operating and troubleshooting the maintenance pipeline (lint, price/fundamentals
refresh, scheduled runs). See [README.md](README.md) for what each piece *is*.

## The scheduled job (launchd)
- Agent: `com.stocksvault.maintenance` — a macOS **LaunchAgent** (runs as you, while logged in)
- Plist: `~/Library/LaunchAgents/com.stocksvault.maintenance.plist`
  (versioned source: `scripts/com.stocksvault.maintenance.plist`)
- Schedule: daily **18:30** local · runs `scripts/daily_maintenance.sh` · logs to `.maintenance.log`

## launchctl cheat-sheet
```bash
# is it loaded?  (columns: PID  last-exit-code  label)
launchctl list | grep stocksvault

# run it NOW (don't wait for 18:30)
launchctl kickstart -k gui/$(id -u)/com.stocksvault.maintenance

# what did the last run do?
cat ~/Documents/Stocks\ Vault/.maintenance.log

# stop / disable
launchctl bootout gui/$(id -u)/com.stocksvault.maintenance

# (re)enable — after editing the plist, or after disabling
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.stocksvault.maintenance.plist

# change the time:   edit Hour/Minute in the plist, then bootout + bootstrap
# remove entirely:   bootout, then  rm ~/Library/LaunchAgents/com.stocksvault.maintenance.plist
```
If the Mac is asleep at the scheduled time, launchd runs the job at the next wake.
There is no GUI for launchd — manage it here, or with a third-party app (LaunchControl / Lingon).

## Known issue: "Operation not permitted" (exit code 126)
macOS blocks background launchd agents from reading `~/Documents`, `~/Desktop`,
`~/Downloads` (privacy / TCC) unless granted **Full Disk Access**. Symptom in
`.maintenance.log`:
```
/bin/bash: …/daily_maintenance.sh: Operation not permitted
```
**Fix (one-time):** System Settings → Privacy & Security → **Full Disk Access** →
**+** → press **⌘⇧G** → type `/bin/bash` → Add → toggle it **on**. Then re-run with
`launchctl kickstart -k …`. (The script runs fine from Terminal because Terminal
already has that permission; launchd does not.)

## Run anything manually (no launchd, no Full Disk Access needed)
```bash
cd ~/Documents/Stocks\ Vault
PY=~/Documents/stock-analysis-ui/venv/bin/python
$PY scripts/vault_lint.py            # integrity gate (exit 0 = clean)
$PY scripts/refresh_prices.py        # article price tables
$PY scripts/refresh_fundamentals.py  # per-note Snapshot blocks
bash scripts/daily_maintenance.sh    # all of the above + commit + push
```

## Cloud fallback (GitHub Actions)
The CI workflow (`.github/workflows/vault-ci.yml`) lints on every push and, on a
weekday cron, refreshes + commits in the cloud — no TCC issue. If the local agent
is disabled, `git pull` to sync your local copy. `gh run list` shows recent runs.
