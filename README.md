# Research Code Skill

[![Skill](https://img.shields.io/badge/skill-research--code-blue)](https://github.com/SaltGardenia/research-code-skill)
[![Clusters](https://img.shields.io/badge/clusters-4%20fused-brightgreen)](https://github.com/SaltGardenia/research-code-skill)
[![Conformance](https://img.shields.io/badge/conformance-checked-informational)](https://github.com/SaltGardenia/research-code-skill)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](https://www.python.org)

> Keep your research (ML/DL) codebase clean and consistent.
> The Agent applies these standards **as it writes and edits code** — not as a
> post-hoc review.
>
> [中文文档 →](./README.zh.md)
>
> **Developer note:** every Markdown file in this skill has a Chinese companion
> (`.zh.md`) for human readers — e.g. `SKILL.zh.md`, `references/*.zh.md`,
> `examples/*.zh.md`. Agents load the **English** originals; the `.zh.md` files
> are documentation only.

## What it does

The skill enforces two standards whenever the Agent works on your code:

1. **Project-level standard.** The Agent establishes one clear, predictable
   structure for the project and maintains it — so the structure stays stable and
   consistent as the code grows.
2. **Code-level standard.** Within that structure, the code stays healthy:
   **comments that explain the reasoning, sensible API design, and thorough
   modularization** — so the code is easy to read, reuse, and extend.

Every guideline is encoded as a concrete, checkable rule, so the skill applies
and verifies the standard during work rather than merely referencing documents.

## Secondary practices

The two standards above are reinforced by well-established practices:

- **Reproducible experiments** — settings are recorded and data is identified and
  version-locked, so a result can be reproduced later.
- **Clean composition** — adding a model or option is a small, self-contained
  addition rather than another special case; names describe what things are.
- **Automatic consistency** — basic formatting and checks run before code is
  accepted, so uniformity is enforced by the process.

### Comments

As part of the code-level standard, comments in a research project capture
what is easy to lose: **research intent, reasoning, design decisions, and
experimental constraints** — so the code conveys the thinking, not just the
steps. The skill ensures comments explain **why, not merely what**, document
what others will rely on, record the relevant math and its source, and are
updated or removed when they become stale.

### Comparison with an unorganized repo

A research repo that grows without structure accumulates recurring problems. The
skill's fixed structure addresses them:

| Unorganized repo | Repo shaped by this skill | Benefit |
|-------------------|-----------------------------|---------------|
| Experiment settings scattered and hardcoded in code | All settings gathered in one organized place | Trying alternatives and reproducing runs is straightforward |
| Near-duplicate files accumulate as work evolves | One clear home for reusable pieces | Reuse instead of copy; shared logic written once |
| A growing list of special-case branches to pick behavior | New options slot in cleanly | Adding an option touches one place, not a fragile central list |
| Data dropped in a folder with no version or notes | Data that is identified, described, and version-locked | Every run records exactly which data it used |
| "Which version?" answered by a chat message | Clear release versions tied to a snapshot of the code | Results map back to exact code and settings |
| Descriptions rot as the code changes | Descriptions updated in the same change | What you read always matches what the code does |
| Checks run occasionally, by hand, if at all | Checks run automatically as a required step | Consistency is enforced, not left to chance |

## Two main scenarios

**A. Build from zero.** Start a new project that follows the standard from the
first commit.

> Tell the Agent:
> "Start a new research project here and add a model that trains on CIFAR."

**B. Tidy an existing repo.** Bring a messy repo into the standard structure.

> Tell the Agent:
> "Organize this repo: move code into the right folders, turn the training
> flags into configs, and keep the naming consistent."

## Key principle when tidying a repo

The Agent **never arbitrarily deletes or rewrites your code**. It reorganizes by
moving and renaming, preserving behavior. If a piece of code has no matching
target folder, it is **left in the project root** rather than removed.

## The structure it builds

When starting from zero, the Agent sets up one consistent, predictable project
structure and then works inside it. In concrete terms, that means separate,
clear homes for:

- **Settings** — everything that controls an experiment, organized by purpose
  so a run is fully described by its settings.
- **Code** — separate places for data handling, models, and shared helpers.
- **Entry points** — clear ways to start training or evaluation.
- **Tests** — quick checks that the project still holds together.
- **Project files** — the standard supporting files a healthy project keeps at
  its root.

Each part has a clear owner in the standard, so there is never ambiguity
about where something belongs. This structure is the **invariant**: the Agent
writes and rearranges code *inside* it and never swaps it for a different one.

## What it's built on

The two standards draw on widely-trusted, authoritative practices, listed
here by area of focus:

| Area of focus | Grounded in |
|------|-------------|
| **Project layout & writing style** | [Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template), [Hydra](https://hydra.cc/), [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) |
| **Model & component design** | [PyTorch Lightning Style Guide](https://lightning.ai/docs/pytorch/stable/starter/style_guide.html), [timm](https://github.com/huggingface/pytorch-image-models), [OpenMMLab](https://github.com/open-mmlab) |
| **Reproducible experiments** | [Hydra](https://hydra.cc/), [FAIR Data Principles](https://www.go-fair.org/fair-principles/), [Semantic Versioning](https://semver.org/), [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/), [Meta Research](https://github.com/facebookresearch) |
| **Engineering habits & clear interfaces** | [Software Engineering at Google](https://google.github.io/eng-practices/), [Scientific Python](https://learn.scientific-python.org/development/), Research Code Comment Standard |

## How to use it

Ask the Agent to work on your research code (build, add, refactor, name,
organize). It loads this skill automatically and applies the standard as it
works — including running the quality checks for you.

## What's in the box (tooling)

The skill ships with scripts that keep the repo clean and the standard enforced.
Run them yourself if you want the same result the Agent produces.

| Script | Purpose |
|--------|---------|
| `scripts/audit_style.py <path>` | Conformance probe (subset of `LHT-/HY-/PL-/GP-*`): emits the fixed findings table. |
| `scripts/sync_gitignore.py [path]` | Auto-maintains `.gitignore` from the current directory layout. Derives ignore entries inside a marked auto-managed block; hand-written rules are preserved. Use `--check` in CI. |
| `scripts/run_gate.sh` / `scripts/run_gate.ps1` | Runs the mandatory quality gate (`black`/`isort`/`ruff`/`mypy`/`pytest`) with all tool caches redirected into `.cache/`. |

### Caches are aggregated, not scattered

Tool caches and run artifacts that have **no direct relation to the project
code** are swept into a single `.cache/` folder at the repo root
(`.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/`).
Hydra run outputs (`logs/`, `outputs/`, `wandb/`) stay at the root as real
experiment artifacts. Everything under `.cache/` is already covered by
`.gitignore` and never committed — see `.cache/README.md`.

### Auto-maintained .gitignore

After scaffolding (Scenario A) or tidying (Scenario B), the Agent runs
`python scripts/sync_gitignore.py .` so the ignore list always tracks the
current layout — new product directories (`logs/`, `wandb/`, `checkpoints/`, …)
are ignored automatically without hand-editing.

## Installation

This skill is a single installable unit. Keep a stable copy of the repo, then
point your agent at the skill's main file. The whole folder must accompany it,
since the skill requires the supporting files to function.

### Claude Code

First clone to a stable path (do not develop inside this clone):

```bash
npm install -g @anthropic-ai/claude-code
claude
mkdir -p ~/ai-skills
git clone https://github.com/SaltGardenia/research-code-skill.git ~/ai-skills/research-code-skill
```

Recommended: a subagent wrapper that loads the skill's main file:

```bash
mkdir -p ~/.claude/agents
cat > ~/.claude/agents/research-code-skill.md <<'EOF'
---
name: research-code-skill
description: Use for building or tidying a research (ML/DL) codebase with a fixed structure and uniform conventions.
---

When invoked, first read `~/ai-skills/research-code-skill/SKILL.md` and follow it as the governing workflow.
Read supporting files from `~/ai-skills/research-code-skill/` only when needed.
Do not replace this skill with a generic coding response.
EOF
```

Then start a new Claude Code session and ask the subagent to work on your code.
Prefer a subagent (or a slash command) over copying the folder into
`~/.claude/skills/`, so the directory structure stays intact.

To update later:

```bash
cd ~/ai-skills/research-code-skill
git pull
```

### Other agents (Kilo, Codex, OpenClaw, OpenCode, Hermes)

Keep a stable copy, then create a lightweight subagent, slash command, or
custom-prompt wrapper that points at the skill's main file. For Codex you can
also just paste the repo link and ask it to read that file and follow it. Example
prompt:

> Install this skill from https://github.com/SaltGardenia/research-code-skill.git
> and follow its main file. Keep the full folder, not just that one file.

### Python dependency (only if you run the checker yourself)

The quality gate is run automatically by the Agent. If you want to run
the checker locally, install the project's Python tools:

```bash
python -m pip install -r requirements.txt
```

Then run the conformance probe and the auto-`.gitignore` sync:

```bash
python scripts/audit_style.py .            # conformance findings table
python scripts/sync_gitignore.py .         # keep .gitignore in sync with layout
bash scripts/run_gate.sh                   # full quality gate, caches -> .cache/
```
