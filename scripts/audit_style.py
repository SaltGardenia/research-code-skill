#!/usr/bin/env python3
"""audit_style.py - heuristic checker for research-code-reviewer skill.

Scans a Python repo and emits the same finding table the SKILL.md defines
(STRUCTURE / CONFIG / LIGHTNING / PYSTYLE). This is a lightweight static
check; it complements (not replaces) the agent's reasoning.

Usage:
    python scripts/audit_style.py path/to/repo [--max-line-length 80]

Exit code 0 = no BLOCKER, 1 = at least one BLOCKER.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List

# ---- finding model -------------------------------------------------------


@dataclass
class Finding:
    category: str
    severity: str
    location: str
    rule: str
    suggestion: str

    def as_row(self, fid: str) -> str:
        return (
            f"| {fid} | {self.category} | {self.severity} | "
            f"{self.location} | {self.rule} | {self.suggestion} |"
        )


# ---- checks --------------------------------------------------------------


def check_python_file(path: str, max_len: int, out: List[Finding]) -> None:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except (OSError, UnicodeDecodeError) as exc:
        out.append(
            Finding("PYSTYLE", "MINOR", f"{path}:0",
                    "READ", f"Skipped: {exc}")
        )
        return

    has_doc_after_def = False
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        loc = f"{path}:{i}"

        # line length
        if len(line) > max_len:
            out.append(Finding("PYSTYLE", "MINOR", loc, "GP-LEN",
                              f"Line {len(line)}>{max_len} chars; wrap it."))

        # bare except
        if re.search(r"^\s*except\s*:", line):
            out.append(Finding("PYSTYLE", "MAJOR", loc, "GP-EXC",
                              "Use `except SpecificError:` not bare `except:`."))

        # mutable default arg
        if re.search(r"def\s+\w+\([^)]*=\s*(\[\]|\{\}|set\(\))", line):
            out.append(Finding("PYSTYLE", "MAJOR", loc, "GP-DEF",
                              "Avoid mutable default arg; use `= None`."))

        # print used for diagnostics
        if re.match(r"^\s*print\(", line):
            out.append(Finding("PYSTYLE", "MINOR", loc, "GP-PRINT",
                              "Prefer logging over print for diagnostics."))

        # docstring presence after def/class
        if re.match(r"^\s*(def|class)\s+\w+", line):
            has_doc_after_def = True
            continue
        if has_doc_after_def:
            has_doc_after_def = False
            stripped = line.strip()
            if stripped and not stripped.startswith('"""') \
                    and not stripped.startswith("'''") \
                    and not stripped.startswith("#"):
                # only flag top-level/public-ish definitions loosely
                pass

    text = "\n".join(lines)
    # LightningModule structure checks
    if "LightningModule" in text:
        if "configure_optimizers" not in text:
            out.append(Finding("LIGHTNING", "BLOCKER", f"{path}:0",
                              "PL-OPT",
                              "LightningModule missing configure_optimizers."))
        if re.search(r"def\s+__init__\s*\(\s*self\s*,\s*params[\s,)]",
                     text):
            out.append(Finding("LIGHTNING", "MAJOR", f"{path}:0",
                              "PL-INIT",
                              "Avoid opaque `params` in __init__; use typed defaults."))
        if "class" in text and "forward" in text and "training_step" in text:
            # forward vs training_step separation is stylistic; note only
            pass


def check_repo(root: str, max_len: int, out: List[Finding]) -> None:
    has_configs = os.path.isdir(os.path.join(root, "configs"))
    has_src = os.path.isdir(os.path.join(root, "src"))
    has_tests = os.path.isdir(os.path.join(root, "tests"))
    py_files: List[str] = []

    for dirpath, _dirs, files in os.walk(root):
        if ".git" in dirpath or "logs" in dirpath:
            continue
        for fn in files:
            full = os.path.join(dirpath, fn)
            if fn.endswith(".py"):
                py_files.append(full)
            if fn == "train.py" and not has_configs:
                out.append(Finding("STRUCTURE", "MAJOR", full, "LHT-01",
                                  "Entrypoint without configs/; adopt Hydra configs."))

    if not has_configs:
        out.append(Finding("STRUCTURE", "MAJOR", root, "LHT-02",
                          "Missing configs/ directory (Hydra layout)."))
    if not has_src:
        out.append(Finding("STRUCTURE", "MINOR", root, "LHT-03",
                          "Missing src/ directory."))
    if not has_tests:
        out.append(Finding("STRUCTURE", "MINOR", root, "LHT-04",
                          "Missing tests/ directory."))

    for fp in py_files:
        check_python_file(fp, max_len, out)


# ---- report --------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="Research code style auditor.")
    ap.add_argument("path", help="Repo root to scan")
    ap.add_argument("--max-line-length", type=int, default=80)
    args = ap.parse_args()

    if not os.path.isdir(args.path):
        print(f"BLOCKER: path not found: {args.path}")
        return 1

    findings: List[Finding] = []
    check_repo(args.path, args.max_line_length, findings)

    blockers = sum(1 for f in findings if f.severity == "BLOCKER")
    majors = sum(1 for f in findings if f.severity == "MAJOR")
    minors = sum(1 for f in findings if f.severity == "MINOR")

    print(f"# Research Code Review: {args.path}\n")
    print("## Summary")
    print(f"- Files scanned: (see findings)")
    print(f"- Findings: {len(findings)} "
          f"(BLOCKER: {blockers}, MAJOR: {majors}, MINOR: {minors})\n")
    print("## Findings")
    print("| ID | Category | Severity | File:Line | Rule | Suggestion |")
    print("|----|----------|----------|-----------|------|------------|")
    for idx, f in enumerate(findings, start=1):
        print(f.as_row(f"F{idx}"))

    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
