#!/usr/bin/env python3
"""audit_style.py - conformance checker for research-code-skill.

Used as a gate to confirm a research project's code/config still obeys the
conventions this skill enforces (STRUCTURE / CONFIG / LIGHTNING / PYSTYLE),
using the unified rule-code registry in references/coordination.md. It is a
lightweight static check that complements (not replaces) the agent applying
the conventions as it writes and edits code.

Usage:
    python scripts/audit_style.py path/to/repo [--max-line-length 80]

Exit code 0 = no BLOCKER, 1 = at least one BLOCKER.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
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
            Finding("PYSTYLE", "MINOR", f"{path}:0", "READ",
                     f"Skipped: {exc}")
        )
        return

    text = "".join(lines)
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        loc = f"{path}:{i}"

        # GP-LEN: line length
        if len(line) > max_len:
            out.append(Finding("PYSTYLE", "MINOR", loc, "GP-LEN",
                               f"Line {len(line)}>{max_len} chars; wrap it."))

        # GP-SEMI: semicolons (not in strings/comments)
        if _has_semicolon(line):
            out.append(Finding("PYSTYLE", "MINOR", loc, "GP-SEMI",
                               "Avoid semicolons; one statement per line."))

        # GP-EXC: bare except
        if re.search(r"^\s*except\s*:", line):
            out.append(Finding("PYSTYLE", "MAJOR", loc, "GP-EXC",
                               "Use `except SpecificError:` not bare `except:`."))

        # GP-DEF: mutable default arg
        if re.search(r"def\s+\w+\([^)]*=\s*(\[\]|\{\}|set\(\))", line):
            out.append(Finding("PYSTYLE", "MAJOR", loc, "GP-DEF",
                               "Avoid mutable default arg; use `= None`."))

        # GP-PRINT: print for diagnostics
        if re.match(r"^\s*print\(", line):
            out.append(Finding("PYSTYLE", "MINOR", loc, "GP-PRINT",
                               "Prefer logging over print for diagnostics."))

        # GP-NAME: single-char l/I/O variable names
        if re.search(r"\b[llOIO]\s*=", line) and "=" in line:
            out.append(Finding("PYSTYLE", "MINOR", loc, "GP-NAME",
                               "Avoid single-char names l/I/O (confusable)."))

    # GP-IMP: wildcard imports (real statement, not inside strings)
    if re.search(r"^\s*from\s+\S+\s+import\s+\*", text, flags=re.M):
        out.append(Finding("PYSTYLE", "MAJOR", f"{path}:0", "GP-IMP",
                           "No wildcard `from x import *`."))

    # PL checks
    if "LightningModule" in text:
        if "configure_optimizers" not in text:
            out.append(Finding("LIGHTNING", "BLOCKER", f"{path}:0", "PL-OPT",
                               "LightningModule missing configure_optimizers."))
        if re.search(r"def\s+__init__\s*\(\s*self\s*,\s*params[\s,)]", text):
            out.append(Finding("LIGHTNING", "MAJOR", f"{path}:0", "PL-INIT",
                               "Avoid opaque `params` in __init__; use typed defaults."))
        if "save_hyperparameters" not in text and "hparams" not in text:
            out.append(Finding("LIGHTNING", "MINOR", f"{path}:0", "PL-HPARAM",
                               "Call self.save_hyperparameters() to persist init args."))
        # PL-METRIC: hand-rolled accuracy vs torchmetrics
        if re.search(r"\.argmax\(.*\)\.sum\(\)", text) and "torchmetrics" not in text:
            out.append(Finding("LIGHTNING", "MINOR", f"{path}:0", "PL-METRIC",
                               "Use torchmetrics instead of hand-rolled accuracy."))
        # PL-FWD: training logic inside forward
        if re.search(r"def forward\(self.*\):", text) and \
           re.search(r"self\.log\(|loss\.backward|training_step", text):
            out.append(Finding("LIGHTNING", "MAJOR", f"{path}:0", "PL-FWD",
                               "Keep training logic in training_step, not forward()."))


def check_repo(root: str, max_len: int, out: List[Finding]) -> None:
    has_configs = os.path.isdir(os.path.join(root, "configs"))
    has_src = os.path.isdir(os.path.join(root, "src"))
    has_tests = os.path.isdir(os.path.join(root, "tests"))
    py_files: List[str] = []

    for dirpath, _dirs, files in os.walk(root):
        norm = dirpath.replace(os.sep, "/")
        if ".git" in norm or "/logs/" in norm or "/data/" in norm:
            continue
        for fn in files:
            full = os.path.join(dirpath, fn)
            if fn.endswith(".py"):
                py_files.append(full)
            # LHT-01: entrypoint without hydra decorator
            if fn in ("train.py", "eval.py") and not has_configs:
                out.append(Finding("STRUCTURE", "MAJOR", full, "LHT-01",
                                   "Entrypoint without configs/; adopt Hydra configs."))

    if not has_configs:
        out.append(Finding("STRUCTURE", "MAJOR", root, "LHT-02",
                           "Missing configs/ directory (Hydra layout)."))
    if not has_src:
        out.append(Finding("STRUCTURE", "MINOR", root, "LHT-05",
                           "Missing src/ directory (data/models/utils split)."))
    if not has_tests:
        out.append(Finding("STRUCTURE", "MINOR", root, "LHT-04",
                           "Missing tests/ directory."))

    # LHT-03: required root files
    for fname, code in [
        (".pre-commit-config.yaml", "LHT-TOOL"),
        ("pyproject.toml", "LHT-03"),
        ("requirements.txt", "LHT-03"),
        (".gitignore", "LHT-03"),
        (".env.example", "LHT-03"),
        (".project-root", "LHT-03"),
    ]:
        if not os.path.exists(os.path.join(root, fname)):
            out.append(Finding("STRUCTURE", "MINOR", root, code,
                               f"Missing root file {fname}."))

    # CONFIG: train.py should use @hydra.main
    for fp in py_files:
        if os.path.basename(fp) in ("train.py", "eval.py"):
            try:
                with open(fp, "r", encoding="utf-8") as fh:
                    content = fh.read()
            except (OSError, UnicodeDecodeError):
                continue
            if "@hydra.main" not in content:
                out.append(Finding("CONFIG", "MAJOR", fp, "HY-ENTRY",
                                   "Entrypoint missing @hydra.main decorator."))

    for fp in py_files:
        check_python_file(fp, max_len, out)


# ---- report --------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="Research code style auditor.")
    ap.add_argument("path", help="Repo root to scan")
    ap.add_argument("--max-line-length", type=int, default=80)
    args = ap.parse_args()

    if not os.path.isdir(args.path):
        sys.stdout.write(f"BLOCKER: path not found: {args.path}\n")
        return 1

    findings: List[Finding] = []
    check_repo(args.path, args.max_line_length, findings)

    blockers = sum(1 for f in findings if f.severity == "BLOCKER")
    majors = sum(1 for f in findings if f.severity == "MAJOR")
    minors = sum(1 for f in findings if f.severity == "MINOR")

    out = sys.stdout
    out.write(f"# Research Code Conformance: {args.path}\n\n")
    out.write("## Summary\n")
    out.write(f"- Findings recorded: {len(findings)}\n")
    out.write(f"- Findings: {len(findings)} "
              f"(BLOCKER: {blockers}, MAJOR: {majors}, MINOR: {minors})\n\n")
    out.write("## Findings\n")
    out.write("| ID | Category | Severity | File:Line | Rule | Suggestion |\n")
    out.write("|----|----------|----------|-----------|------|------------|\n")
    for idx, f in enumerate(findings, start=1):
        out.write(f.as_row(f"F{idx}") + "\n")

    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
