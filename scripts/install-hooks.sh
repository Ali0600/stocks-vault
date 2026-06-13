#!/bin/bash
# One-time setup: point git at the versioned hooks dir so the pre-commit
# linter runs on every commit. Idempotent.
set -e
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath scripts/hooks
echo "core.hooksPath → scripts/hooks (pre-commit linter active)"
