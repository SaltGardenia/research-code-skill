# 🧪 科研代码 Skill

[![Skill](https://img.shields.io/badge/skill-research--code-blue)](https://github.com/SaltGardenia/research-code-skill)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](https://www.python.org)

> 让科研（ML/DL）代码库保持整洁、一致。Agent 在**编写和修改代码的过程中**就应用这套标准，而非事后审查。
> [English →](./README.en.md)

## ✨ 能力列表

- 🏗️ 项目层面：建立清晰、可预期的结构，并长期保持。
- 💬 代码层面：高质量注释，简洁有力、高度概括、短句优先、拆分长句；API 设计合理；模块化完善。
- ⚙️ 实验参数一律走配置，代码只从配置读取，杜绝硬编码。
- 🧩 模型与系统分离，模型自包含，遵循固定方法顺序。
- 🔁 实验可复现：配置、数据版本、代码 tag 三者绑定，结果可重生。
- 🚦 强制质量门（black / isort / ruff / mypy / pytest），变更接受前必须通过。
- 🔧 自动维护的 `.gitignore`：随目录结构变化同步忽略规则，不破坏手写规则。
- 📦 运行产物收口到 `.cache/`，仓库根不散落缓存文件。
- 🤝 关键原则：Agent 不会随意删除或重写你的代码，只移动、重命名以保持行为不变。
- 📏 每条规范编码为可检查的规则，随工作实时应用与校验，而非仅引用文档。

## 🎯 两个场景示例

**A. 从零搭建**
> “在这里新建一个科研项目，并添加一个在 CIFAR 上训练的模型。”
> Agent 从骨架搭建结构，再按规范写 `src/`、`configs/`、Hydra `_target_`。

**B. 整理已有仓库**
> “整理这个仓库：把代码归入正确目录，把训练参数改成配置，并保持命名统一。”
> Agent 先审计偏离，再重构重命名至合规，重跑校验门确认。

## 📂 项目结构示例

Agent 搭建或整理后产出的标准结构：

```
<project>/
├── .github/workflows/         # CI（pytest + pre-commit）
├── configs/                   # Hydra 配置，按关注点分组
│   ├── callbacks/  data/  debug/  experiment/
│   ├── extras/  hparams_search/  hydra/
│   ├── local/  logger/  model/  paths/  trainer/
│   ├── eval.yaml  train.yaml     # 主配置（defaults 列表）
├── data/                      # 原始 / 处理后的数据（git 忽略）
├── logs/                      # hydra + logger 输出，带时间戳（git 忽略）
├── notebooks/                 # 编号 + 缩写 + 简述（如 1.0-jqp-explore.ipynb）
├── scripts/                   # shell 脚本（Makefile 目标调用）
├── src/
│   ├── data/                  # LightningDataModule
│   ├── models/                # 模型骨干 + LightningModule
│   │   └── components/        # 可复用的模型组件
│   ├── utils/                 # 工具与实例化逻辑
│   ├── eval.py  train.py      # @hydra.main 入口
├── tests/                     # 冒烟 + 单元测试（pytest）
├── .env.example               # 私有环境变量模板（复制为 .env）
├── .gitignore
├── .pre-commit-config.yaml    # 格式化 / lint / 安全 hooks
├── .project-root              # rootutils 标记项目根
├── environment.yaml           # conda 环境
├── Makefile                   # make train/test/format/clean
├── pyproject.toml             # pytest + coverage + 工具配置
├── requirements.txt
├── setup.py                   # 以包形式安装项目
└── README.md
```

## 📚 参考项目

| 关注领域 | 依据 |
|------|------|
| 项目结构与写法 | [Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template)、[Hydra](https://hydra.cc/)、[Google Python Style](https://google.github.io/styleguide/pyguide.html) |
| 模型与组件设计 | [PyTorch Lightning Style](https://lightning.ai/docs/pytorch/stable/starter/style_guide.html)、[timm](https://github.com/huggingface/pytorch-image-models)、[OpenMMLab](https://github.com/open-mmlab) |
| 可复现实验 | [Hydra](https://hydra.cc/)、[FAIR](https://www.go-fair.org/fair-principles/)、[SemVer](https://semver.org/)、[Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)、[Meta Research](https://github.com/facebookresearch) |
| 工程习惯与接口 | [Software Engineering at Google](https://google.github.io/eng-practices/)、[Scientific Python](https://learn.scientific-python.org/development/)、科研代码注释规范 |

## 🚀 快速开始

克隆到稳定路径（不要在此副本内开发），让 Agent 指向 `SKILL.md`：

```bash
git clone https://github.com/SaltGardenia/research-code-skill.git ~/ai-skills/research-code-skill
```

Claude Code 用 subagent 加载主文件：

```bash
mkdir -p ~/.claude/agents
cat > ~/.claude/agents/research-code-skill.md <<'EOF'
---
name: research-code-skill
description: 用于以固定结构、统一规范搭建或整理科研（ML/DL）代码库。
---
When invoked, first read `~/ai-skills/research-code-skill/SKILL.md` and follow it as the governing workflow.
Read supporting files from `~/ai-skills/research-code-skill/` only when needed.
Do not replace this skill with a generic coding response.
EOF
```

其他 Agent（Kilo、Codex 等）同样保留完整文件夹，创建指向主文件的 subagent / slash command / 自定义 prompt。更新：`cd ~/ai-skills/research-code-skill && git pull`。

本地运行检查器：`python -m pip install -r requirements.txt`，然后 `python scripts/audit_style.py .`、`python scripts/sync_gitignore.py .`、`bash scripts/run_gate.sh`。
