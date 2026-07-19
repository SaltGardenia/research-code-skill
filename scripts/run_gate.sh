#!/usr/bin/env bash
# Sweep loose tool caches from the repo root into the .cache/ aggregation folder,
# and run the mandatory quality gate with all caches redirected there.
#
# Usage:
#   bash scripts/run_gate.sh            # sweep + run black/isort/ruff/mypy/pytest
#   SWEEP_ONLY=1 bash scripts/run_gate.sh   # only move caches into .cache/

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="$ROOT/.cache"
mkdir -p "$CACHE"/{mypy,pytest,ruff,coverage}

# --- Redirect tool caches into .cache/ ---
export MYPY_CACHE_DIR="$CACHE/mypy"
export PYTEST_DEBUG_TEMPROOT="$CACHE/pytest"
export COVERAGE_FILE="$CACHE/coverage/.coverage"
RUFF_CACHE="$CACHE/ruff"

# --- Sweep any loose caches already at the root into .cache/ ---
move_if_exists() {
  local src="$1" dst="$2"
  if [ -e "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    mv "$src" "$dst"
    echo "moved: $src -> $dst"
  fi
}
move_if_exists "$ROOT/.mypy_cache"    "$CACHE/mypy/cache"
move_if_exists "$ROOT/.pytest_cache"  "$CACHE/pytest/cache"
move_if_exists "$ROOT/.ruff_cache"    "$CACHE/ruff/cache"
move_if_exists "$ROOT/.coverage"      "$CACHE/coverage/.coverage"
move_if_exists "$ROOT/htmlcov"        "$CACHE/coverage/htmlcov"

if [ "${SWEEP_ONLY:-0}" = "1" ]; then
  echo "Sweep done. Caches live under .cache/."
  exit 0
fi

# --- Mandatory quality gate (Step 8 of SKILL.md) ---
black .
isort .
ruff --cache-dir "$RUFF_CACHE" check .
mypy --cache-dir "$CACHE/mypy" src/
pytest --rootdir="$ROOT" tests/
