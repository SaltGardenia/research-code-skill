---
name: research-code-reviewer
description: >-
  Enforces scientific/research Python code standards for AI agents. Use when
  reviewing, auditing, scaffolding, or refactoring ML/DL research codebases so
  they follow the Lightning-Hydra template, PyTorch Lightning Style Guide,
  Google Python Style Guide, and Hydra configuration best practices. Trigger on
  tasks like "check code style", "make this research repo reproducible",
  "review training script", "apply best practices to my DL project",
  "audit configs", or "set up a clean research project structure".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
version: 1.0.0
author: research-code-skill
tags:
  - python
  - research
  - machine-learning
  - code-style
  - pytorch-lightning
  - hydra
  - best-practices
  - code-review
compatibility:
  - claude
  - gpt
  - kilo
  - any-model-supporting-skills
---

# Research Code Reviewer

A skill that makes an AI agent enforce research-grade Python code standards.
It distills four authoritative references into one actionable workflow:

1. **Lightning-Hydra-Template** — clean, reproducible DL project structure.
2. **PyTorch Lightning Style Guide** — `LightningModule`/`DataModule` structure.
3. **Google Python Style Guide** — general Python formatting and idioms.
4. **Hydra** — hierarchical, composable, overridable configuration.

## When to Use

Invoke this skill when the user asks to:
- Review or audit an existing research/ML codebase for standard violations.
- Scaffold a new research project that follows best practices from day one.
- Refactor messy experimental code into a modular, reproducible layout.
- Validate that configs, entrypoints, modules, and tests conform to the standards.
- Generate or fix code so it passes the bundled linter/audit script.

Do NOT use this skill for:
- Pure frontend / web-only projects without a Python/ML backend.
- Non-Python languages (C++, JS) unless only the Google naming/text rules apply.

## Preconditions

Before running the Procedure, verify:
1. A target path is provided (a repo root, a directory, or specific files).
2. The target contains or will contain Python code (`.py`).
3. Read access is available; Write/Edit only when the user requested changes.
4. For script execution, a Python 3.8+ interpreter is available.

If no target is given, ask the user for the path before proceeding.
If the target is empty, switch to "scaffold" mode (see Procedure step 5).

## Procedure

Execute the steps in order. Each step maps to a reference source.

### Step 1 — Project structure check (Lightning-Hydra-Template)
Verify the repo matches the recommended layout:
- `configs/` holds Hydra YAML configs grouped by concern
  (`data/`, `model/`, `trainer/`, `callbacks/`, `logger/`, `experiment/`, ...).
- `src/` holds source code split by role: `src/data/`, `src/models/`,
  `src/utils/`, with entrypoints `src/train.py`, `src/eval.py`.
- `tests/` holds generic smoke tests; `data/`, `logs/`, `notebooks/` are separated.
- Root files: `.pre-commit-config.yaml`, `pyproject.toml` (or `setup.py`),
  `requirements.txt`, `.gitignore`, `.env.example`, `.project-root`.
Flag any deviation as a `STRUCTURE` finding.

### Step 2 — Config standards check (Hydra)
Verify Hydra usage:
- Entrypoints use `@hydra.main(version_base=..., config_path=..., config_name=...)`.
- Compose configs by group, override via CLI and `@` defaults lists.
- Each config is a `_target_` dataclass/object plus primitive params.
- No hardcoded paths; use `configs/paths/default.yaml` + `rootutils.setup_root`.
- Experiments are version-controlled configs under `configs/experiment/`.
Flag violations as `CONFIG` findings.

### Step 3 — LightningModule / DataModule check (PL Style Guide)
Verify module design:
- **Systems vs Models**: model backbones separated from the system
  (`LightningModule`) that wires them together.
- **Self-contained**: a `Trainer` can run it without knowing internals;
  optimizer + scheduler live in `configure_optimizers`.
- **Init clarity**: explicit typed args with sensible defaults, no opaque
  `params` objects passed in.
- **Method order**: `__init__` → `forward` → `training_step` → validation →
  test → `configure_optimizers` → extra hooks.
- **forward vs training_step**: `forward()` for inference only.
- **DataModules**: `LightningDataModule` decouples data splits, transforms,
  and DataLoaders; tuned `num_workers`.
Flag violations as `LIGHTNING` findings.

### Step 4 — Python style check (Google Python Style Guide)
Verify general Python hygiene:
- Line length <= 80 (Google) unless project sets 99 (Black/PL template).
- `snake_case` for functions/vars, `CapWords` for classes, `UPPER_CASE` for
  constants; no `l`, `I`, `O` single-letter names.
- Imports grouped: stdlib, third-party, local; no wildcard imports.
- Docstrings on every public module/class/function (PEP 257).
- Type annotations on all function signatures.
- No semicolons, no bare `except:`, no mutable default args.
- Logging via `logging`/`log`, never `print` for diagnostics.
- `if __name__ == "__main__":` guard for executable scripts.
- Use the bundled `scripts/audit_style.py` to auto-detect these.
Flag violations as `PYSTYLE` findings.

### Step 5 — Scaffold mode (only when target is empty or user asks to init)
If scaffolding, generate the directory skeleton from `templates/project_skeleton/`
and copy `configs/` + `src/` stubs. Do not overwrite existing user files;
report what was created.

### Step 6 — Report & apply
Produce the standardized report (Output Format). If the user asked to fix,
apply minimal edits per finding, then re-run the audit script to confirm.

## Output Format

Always return a fixed Markdown report:

```markdown
# Research Code Review: <target>

## Summary
- Files scanned: <n>
- Findings: <total> (BLOCKER: <b>, MAJOR: <m>, MINOR: <i>)

## Findings
| ID | Category | Severity | File:Line | Rule | Suggestion |
|----|----------|----------|-----------|------|------------|
| F1 | STRUCTURE | MAJOR | src/train.py:12 | LHT-01 | Move entrypoint configs to configs/ |

## Next Steps
- <actionable bullet, one per top issue>
```

Severity levels: `BLOCKER` (breaks reproducibility/run), `MAJOR` (violates a
core rule), `MINOR` (style nit). Categories are exactly: STRUCTURE, CONFIG,
LIGHTNING, PYSTYLE.

## Error Handling

- **No Python files found**: report `BLOCKER` with empty Findings and instruct
  the user to provide a Python repo or switch to scaffold mode.
- **Audit script missing deps**: print the `pip install -r requirements.txt`
  command and fall back to static heuristic checks without failing.
- **Permission denied on Write**: stop, return the report as suggestions only,
  and note files were not modified.
- **Unparseable Python file**: skip it, list it under "Skipped" with the reason,
  continue the rest.
- **Ambiguous rule**: prefer the project's own `pyproject.toml`/`setup.cfg`
  config over the generic default, and note the override in the report.

## Constraints

- Single responsibility: this skill ONLY reviews/enforces research code
  standards; do not mix in unrelated tasks (e.g. data labeling, web design).
- Never auto-commit or push changes unless the user explicitly asks.
- Never invent config values; only suggest based on existing patterns.
- Respect the project's existing line-length / formatter config if present.
- Load reference docs lazily: read `references/` files only for the category
  currently being checked, not all at once.
- Keep each finding actionable and tied to a concrete file:line.
