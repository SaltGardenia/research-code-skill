# 🧪 Research Code Skill

[![Skill](https://img.shields.io/badge/skill-research--code-blue)](https://github.com/SaltGardenia/research-code-skill)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](https://www.python.org)

> Keep research codebases tidy and consistent. The agent applies this standard **as it writes and edits** — not as an after-the-fact review.
> [中文文档→](./README.md)

## ✨ Capabilities

- 🏗️ Project level: a clear, predictable structure — kept that way.
- 💬 High-quality comments: concise, forceful, short-sentence first. Explain why, not what. Formulas carry citations; decisions carry a `Reason:`; `TODO`/`FIXME`/`WARNING` disciplined; paper-core modules get a dedicated doc block.
- 🎨 Python style & naming: snake_case / CapWords / UPPER_CASE. Grouped imports, full docstrings, type hints, unified line length.
- ⚙️ Every experiment parameter lives in config. Code reads `cfg` only — no hardcoded literals.
- 🧩 Models decoupled from systems. Self-contained, fixed method order. LightningModule uses torchmetrics, `/`-named metrics, explicit `configure_optimizers`, DDP-friendly.
- 🏛️ Named architectures & pluggability: timm style (layers/blocks/architectures); OpenMMLab Registry registers-then-builds; no `if model == "..."` branching.
- 🔁 Reproducible experiments: config, data version (FAIR), and code tag (SemVer/Git Flow) bound together. Results regenerate. No `train_v2_final.py`.
- 🚦 Mandatory quality gates: black / isort / ruff / mypy / pytest. A change must pass before it is accepted.
- 📦 Ships as an installable package. CI runs style + type checks. Small reviewable changes; interface docs never drift.
- 🧠 Behavioral discipline (Karpathy): think before coding, simplicity first, surgical changes, goal-driven execution.
- 🔧 Automaintained `.gitignore`: rules sync with the layout, hand-written entries preserved.
- 📂 Run artifacts funnel into `.cache/`; no cache files litter the repo root.
- 🤝 Never deletes or rewrites your code. Only moves or renames — behavior preserved.
- 📏 Rules are machine-checkable. Applied live as work proceeds, not just cited from docs.

## 🎯 Two scenario examples

**A. Build from scratch**
> "Create a new research project here and add a model trained on CIFAR."
> The agent scaffolds from the skeleton, then writes `src/`, `configs/`, and Hydra `_target_` per the standard.

**B. Tidy an existing repo**
> "Tidy this repo: move code into the right dirs, turn training params into config, unify naming."
> The agent audits drift, then refactors/rename into compliance and re-runs the gates.

## 📂 Project structure example

Standard structure produced after the agent scaffolds or tidies:

```
<project>/
├── .github/workflows/         # CI (pytest + pre-commit)
├── configs/                   # Hydra configs grouped by concern
│   ├── callbacks/  data/  debug/  experiment/
│   ├── extras/  hparams_search/  hydra/
│   ├── local/  logger/  model/  paths/  trainer/
│   ├── eval.yaml  train.yaml     # main configs (defaults lists)
├── data/                      # raw / processed data (git-ignored)
├── logs/                      # hydra + logger outputs, timestamped (git-ignored)
├── notebooks/                 # numbered + initials + short desc (e.g. 1.0-jqp-explore.ipynb)
├── scripts/                   # shell scripts (called by Makefile targets)
├── src/
│   ├── data/                  # LightningDataModule
│   ├── models/                # model backbone + LightningModule
│   │   └── components/        # reusable model components
│   ├── utils/                 # utilities and instantiation logic
│   ├── eval.py  train.py      # @hydra.main entrypoints
├── tests/                     # smoke + unit tests (pytest)
├── .env.example               # template for private env vars (copy to .env)
├── .gitignore
├── .pre-commit-config.yaml    # formatting / lint / security hooks
├── .project-root              # rootutils marks the project root
├── environment.yaml           # conda env
├── Makefile                   # make train/test/format/clean
├── pyproject.toml             # pytest + coverage + tool config
├── requirements.txt
├── setup.py                   # install project as a package
└── README.md
```

## 📚 Reference projects

| Concern | Basis |
|------|------|
| Project structure & style | [Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template), [Hydra](https://hydra.cc/), [Google Python Style](https://google.github.io/styleguide/pyguide.html) |
| Model & component design | [PyTorch Lightning Style](https://lightning.ai/docs/pytorch/stable/starter/style_guide.html), [timm](https://github.com/huggingface/pytorch-image-models), [OpenMMLab](https://github.com/open-mmlab) |
| Reproducible experiments | [Hydra](https://hydra.cc/), [FAIR](https://www.go-fair.org/fair-principles/), [SemVer](https://semver.org/), [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/), [Meta Research](https://github.com/facebookresearch) |
| Engineering habits & interfaces | [Software Engineering at Google](https://google.github.io/eng-practices/), [Scientific Python](https://learn.scientific-python.org/development/), research-code commenting standard |

## 🚀 Quick start

Clone to a stable path (don't develop inside this copy); point the agent at `SKILL.md`:

```bash
git clone https://github.com/SaltGardenia/research-code-skill.git ~/ai-skills/research-code-skill
```

Claude Code loads the main file via a subagent:

```bash
mkdir -p ~/.claude/agents
cat > ~/.claude/agents/research-code-skill.md <<'EOF'
---
name: research-code-skill
description: Use to scaffold or tidy research (ML/DL) codebases with a fixed structure and unified rules.
---
When invoked, first read `~/ai-skills/research-code-skill/SKILL.md` and follow it as the governing workflow.
Read supporting files from `~/ai-skills/research-code-skill/` only when needed.
Do not replace this skill with a generic coding response.
EOF
```

Other agents (Kilo, Codex, etc.) keep the full folder too: create a subagent / slash command / custom prompt pointing at the main file. Update with: `cd ~/ai-skills/research-code-skill && git pull`.

Run the checker locally: install first with `python -m pip install -r requirements.txt`, then `python scripts/audit_style.py .`, `python scripts/sync_gitignore.py .`, `bash scripts/run_gate.sh`.
