# 🧪 Research Code Skill

[![Skill](https://img.shields.io/badge/skill-research--code-blue)](https://github.com/SaltGardenia/research-code-skill)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](https://www.python.org)

> Keep research (ML/DL) codebases tidy and consistent. The agent applies this standard **while writing and editing code**, not as an after-the-fact review.
> [中文文档（默认）→](./README.md)

## ✨ Capabilities

- 🏗️ Project level: establish a clear, predictable structure and keep it that way.
- 💬 Code level: high-quality comments — concise and forceful, highly summarized, short sentences first, long sentences split. Sound API design and clean modularization.
- ⚙️ All experiment parameters live in config; code only reads from config — no hardcoding.
- 🧩 Models are decoupled from systems, self-contained, and follow a fixed method order.
- 🔁 Reproducible experiments: config, data version, and code tag are bound together so results can be regenerated.
- 🚦 Mandatory quality gates (black / isort / ruff / mypy / pytest) must pass before a change is accepted.
- 🔧 Auto-maintained `.gitignore`: ignore rules stay in sync as the layout changes, without clobbering hand-written rules.
- 📦 Run artifacts are funneled into `.cache/`, so no cache files litter the repo root.
- 🤝 Key principle: the agent never deletes or rewrites your code on a whim — it only moves or renames to preserve behavior.
- 📏 Every rule is encoded as a checkable rule, applied and verified live as work proceeds — not just referenced from docs.

## 🎯 Two scenario examples

**A. Build from scratch**
> "Create a new research project here and add a model trained on CIFAR."
> The agent scaffolds the structure from the skeleton, then writes `src/`, `configs/`, and Hydra `_target_` per the standard.

**B. Tidy an existing repo**
> "Tidy this repo: move code into the right directories, turn training params into config, and unify naming."
> The agent audits drift first, then refactors/rename into compliance and re-runs the gates to confirm.

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

Run the checker locally: `python -m pip install -r requirements.txt`, then `python scripts/audit_style.py .`, `python scripts/sync_gitignore.py .`, `bash scripts/run_gate.sh`.
