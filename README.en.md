# 🧪 Research Code Skill

[![Skill](https://img.shields.io/badge/skill-research--code-blue)](https://github.com/SaltGardenia/research-code-skill)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](https://www.python.org)

> Keep research codebases tidy and consistent. The agent applies this standard **as it writes and edits** — not as an after-the-fact review.
> [中文文档→](./README.md)

## ✨ Capabilities

- Project level: establish a clear, predictable structure and keep it that way.
- Models are decoupled from systems, self-contained, following a fixed method order.
- All experiment parameters live in config files; code only reads from config, no hardcoding.
- Reproducible experiments: config, data version, and code tag bound together, so results regenerate.
- Mandatory quality gates (black / isort / ruff / mypy / pytest) must pass before a change is accepted.
- Code level: comments explain the thinking, sensible API design, clean modularization.
- Named architectures & pluggability: timm tiers, OpenMMLab register-then-build, no `if model == "..."` branching.
- Ships as an installable package; CI runs style + type checks; small reviewable changes, interface docs never drift.
- Behavioral discipline: think before coding, simplicity first, surgical changes, goal-driven execution.
- Automaintained `.gitignore`: ignore rules sync with the layout, without clobbering hand-written rules.
- Run artifacts funnel into `.cache/`; no cache files litter the repo root.
- Key principle: the agent never deletes or rewrites your code on a whim — it only moves or renames to preserve behavior.
- Every rule is encoded as a checkable rule, applied and verified live as work proceeds — not just referenced from docs.

## 🎯 Two scenario examples

**A. Build from scratch**

> "Create a new research project here and add a model trained on CIFAR."
> The agent scaffolds from the skeleton, then writes `src/`, `configs/`, and Hydra `_target_` per the standard.

**B. Tidy an existing repo**

> "Tidy this repo: move code into the right dirs, turn training params into config, unify naming."
> The agent audits drift, then refactors/rename into compliance and re-runs the gates.

## 📚 Reference projects

| Concern                         | Basis                                                                                                                                                                                                                                   |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project structure & style       | [Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template), [Hydra](https://hydra.cc/), [Google Python Style](https://google.github.io/styleguide/pyguide.html)                                                    |
| Model & component design        | [PyTorch Lightning Style](https://lightning.ai/docs/pytorch/stable/starter/style_guide.html), [timm](https://github.com/huggingface/pytorch-image-models), [OpenMMLab](https://github.com/open-mmlab)                                   |
| Reproducible experiments        | [Hydra](https://hydra.cc/), [FAIR](https://www.go-fair.org/fair-principles/), [SemVer](https://semver.org/), [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/), [Meta Research](https://github.com/facebookresearch) |
| Engineering habits & interfaces | [Software Engineering at Google](https://google.github.io/eng-practices/), [Scientific Python](https://learn.scientific-python.org/development/), research-code commenting standard                                                     |
| LLM coding discipline           | [Karpathy Skills](https://github.com/multica-ai/andrej-karpathy-skills)                                                                                                                                                                 |

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
