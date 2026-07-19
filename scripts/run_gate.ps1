#!/usr/bin/env pwsh
# PowerShell counterpart of scripts/run_gate.sh
# Sweep loose tool caches from the repo root into .cache/, then optionally run the gate.
param(
  [switch]$SweepOnly
)

$ROOT = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$CACHE = Join-Path $ROOT '.cache'
New-Item -ItemType Directory -Force -Path $CACHE\mypy, $CACHE\pytest, $CACHE\ruff, $CACHE\coverage | Out-Null

$env:MYPY_CACHE_DIR = Join-Path $CACHE 'mypy'
$env:PYTEST_DEBUG_TEMPROOT = Join-Path $CACHE 'pytest'
$env:COVERAGE_FILE = Join-Path $CACHE 'coverage\.coverage'
$RUFF_CACHE = Join-Path $CACHE 'ruff'

function Move-IfExists($src, $dst) {
  if (Test-Path $src) {
    New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
    Move-Item -Force $src $dst
    Write-Host "moved: $src -> $dst"
  }
}
Move-IfExists (Join-Path $ROOT '.mypy_cache') (Join-Path $CACHE 'mypy\cache')
Move-IfExists (Join-Path $ROOT '.pytest_cache') (Join-Path $CACHE 'pytest\cache')
Move-IfExists (Join-Path $ROOT '.ruff_cache') (Join-Path $CACHE 'ruff\cache')
Move-IfExists (Join-Path $ROOT '.coverage') (Join-Path $CACHE 'coverage\.coverage')
Move-IfExists (Join-Path $ROOT 'htmlcov') (Join-Path $CACHE 'coverage\htmlcov')

if ($SweepOnly) {
  Write-Host "Sweep done. Caches live under .cache/."
  exit 0
}

black .
isort .
ruff --cache-dir $RUFF_CACHE check .
mypy --cache-dir (Join-Path $CACHE 'mypy') src/
pytest --rootdir=$ROOT tests/
