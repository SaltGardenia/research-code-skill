#!/usr/bin/env python3
"""sync_gitignore.py - auto-maintain .gitignore from the project layout.

Part of the research-code-skill. Run it after scaffolding (Scenario A) or
tidying (Scenario B) so that `.gitignore` always reflects the current
directory structure. It is a *conformance* helper, not a review gate.

What it does
------------
1. Scans the target repo for directories / artifacts that should be ignored.
2. Writes only the derived entries inside a clearly marked auto-managed block,
   leaving any hand-written rules outside that block untouched.

Markers (do not edit by hand):
    # >>> research-code-skill:auto-gitignore >>>
    ... derived entries ...
    # <<< research-code-skill:auto-gitignore <<<

Usage:
    python scripts/sync_gitignore.py [path]      # default: repo root
    python scripts/sync_gitignore.py --check     # exit 1 if drift detected
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import List

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("sync_gitignore")

# --- Fixed rules that are always correct, regardless of layout -------------
ALWAYS = [
    "__pycache__/",
    "*.py[cod]",
    "*.egg-info/",
    ".env",
    ".env.*",
    "!.env.example",
    "*.log",
]

# --- Directory-based rules: present in .gitignore only if the dir exists ---
# (dir_name, gitignore_entry)
DIR_RULES = [
    ("data", "data/"),
    ("logs", "logs/"),
    ("outputs", "outputs/"),
    ("wandb", "wandb/"),
    ("checkpoints", "checkpoints/"),
    ("notebooks", "notebooks/"),
    ("runs", "runs/"),
    ("mlruns", "mlruns/"),
    ("lightning_logs", "lightning_logs/"),
    ("dvc", ".dvc/cache/"),
    ("assets", "assets/"),  # generated/large assets, keep optional
]

# --- Cache aggregation (skill convention: everything lands in .cache/) ------
CACHE_RULES = [
    ".cache/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".coverage",
    ".coverage.*",
    "htmlcov/",
    "coverage.xml",
]

MARK_START = "# >>> research-code-skill:auto-gitignore >>>"
MARK_END = "# <<< research-code-skill:auto-gitignore <<<"

# Directories that are part of the skill content itself, never ignored.
SKILL_DIRS = {"references", "templates", "scripts", "examples", "docs", "assets"}


def derive_entries(root: str) -> List[str]:
    entries: List[str] = []
    entries += ALWAYS
    for dir_name, rule in DIR_RULES:
        if os.path.isdir(os.path.join(root, dir_name)) and dir_name not in SKILL_DIRS:
            entries.append(rule)
    entries += CACHE_RULES
    # de-dup while preserving order
    seen, out = set(), []
    for e in entries:
        if e not in seen:
            seen.add(e)
            out.append(e)
    return out


def render_block(entries: List[str]) -> str:
    lines = [MARK_START, "# Auto-managed by research-code-skill sync_gitignore.py",
             "# Edit rules outside this block to add project-specific ignores."]
    lines += entries
    lines.append(MARK_END)
    return "\n".join(lines)


def current_block(text: str) -> str | None:
    if MARK_START in text and MARK_END in text:
        start = text.index(MARK_START)
        end = text.index(MARK_END) + len(MARK_END)
        return text[start:end]
    return None


def sync(root: str) -> bool:
    gi_path = os.path.join(root, ".gitignore")
    new_block = render_block(derive_entries(root))
    if os.path.exists(gi_path):
        with open(gi_path, "r", encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = ""

    old_block = current_block(text)
    if old_block == new_block:
        logger.info(f"[sync_gitignore] {gi_path} already up to date.")
        return False

    # Strip any previous auto block, then append the fresh one.
    if old_block is not None:
        text = text.replace(old_block, "").strip() + "\n"
    text = text.rstrip() + "\n\n" + new_block + "\n"
    with open(gi_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    logger.info(f"[sync_gitignore] updated {gi_path}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Auto-maintain .gitignore.")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if .gitignore would change (CI mode)")
    args = ap.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        logger.error(f"error: path not found: {root}")
        return 2

    gi_path = os.path.join(root, ".gitignore")
    new_block = render_block(derive_entries(root))
    if os.path.exists(gi_path):
        with open(gi_path, "r", encoding="utf-8") as fh:
            old_block = current_block(fh.read())
    else:
        old_block = None

    if args.check:
        if old_block != new_block:
            logger.warning("[sync_gitignore] DRIFT: .gitignore is out of date. "
                           "Run scripts/sync_gitignore.py to fix.")
            return 1
        logger.info("[sync_gitignore] OK: .gitignore is in sync.")
        return 0

    sync(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
