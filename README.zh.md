# 科研代码 Skill

[![Skill](https://img.shields.io/badge/skill-research--code-blue)](https://github.com/SaltGardenia/research-code-skill)
[![Clusters](https://img.shields.io/badge/clusters-4%20fused-brightgreen)](https://github.com/SaltGardenia/research-code-skill)
[![Conformance](https://img.shields.io/badge/conformance-checked-informational)](https://github.com/SaltGardenia/research-code-skill)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](https://www.python.org)

> 让科研（机器学习 / 深度学习）代码库保持整洁、统一。
> Agent 在**编写和修改代码的过程中**就应用这套标准，而不是事后审查。
>
> [English →](./README.md)

## 它做什么

该 Skill 在 Agent 处理代码时强制执行两项规范：

1. **项目层面的规范。** Agent 为项目建立一套清晰、可预期的结构并长期保持——代码结构随代码增长保持稳定、一致。
2. **代码层面的规范。** 在该结构内部，代码保持健康：**注释讲清思路、API 设计合理、模块化完善**——代码因而易读、易复用、易扩展。

每条指导都编码为具体、可核对的规则，Skill 在工作过程中**应用并核验**标准，而非仅引用文档。

## 辅助性实践

上述两项规范由下列成熟实践予以支撑：

- **实验可复现** —— 设置被记录、数据被标识并锁定版本，结果日后可重跑。
- **干净组合** —— 新增模型或选项为独立小块，而非又一份特例；命名直接说明其含义。
- **一致性自动保证** —— 基础格式与检查在代码被接受前自动运行，一致性由流程保障。

### 注释如何被处理

作为代码层面规范的一部分，科研项目的注释应捕捉那些最容易丢失的东西：**研究意图、推理过程、设计决策、实验约束**——让代码承载*思路*，而不只是步骤。本 Skill 会确保注释解释**为什么，而不只是是什么**，说明别人会依赖的东西，必要时记录数学及其出处，并在注释过时或被删时同步更新。

### 它相较未整理仓库有何优势

一个自然生长、未经整理的科研仓库往往会积累同样的老问题。下面是它稳定的结构消除的几条：

| 未整理的仓库 | 经本 Skill 加工的仓库 | 为什么有帮助 |
|------------|--------------------|-----------|
| 实验设置到处散落，还被直接写进代码里 | 所有设置集中在一个有组织的地方 | 尝试不同做法与重现运行都变得轻松 |
| 随着工作推进，近乎重复的文件副本越堆越多 | 可复用的部件只有一个清晰归处 | 东西被复用而非复制 |
| 用一长串特例分支来选择行为 | 新选项干净地插入 | 新增一个选项只动一处，而非一份脆弱的中央清单 |
| 数据随手丢进某个文件夹，没有版本也没有说明 | 被清楚标识、有描述、锁定版本的数据 | 每次运行都记录了它到底用了哪份数据 |
| “哪个版本？”靠一条聊天消息回答 | 清晰的发布版本，对应一份可取回的代码快照 | 结果能对应回确切的代码与设置 |
| 说明随代码改动而失修 | 说明在同一次改动里更新 | 文档与代码行为始终保持一致 |
| 检查偶尔手动跑一下，甚至根本不跑 | 检查作为必经步骤自动运行 | 一致性由流程强制保障，而非偶然 |

## 两个主要场景

**A. 从零开始。** 新建一个从第一次提交起就符合标准的项目。

> 你可以这样对 Agent 说：
> “在这里新建一个科研项目，并添加一个在 CIFAR 上训练的模型。”

**B. 整理已有仓库。** 把杂乱的仓库整理成标准结构。

> 你可以这样对 Agent 说：
> “整理这个仓库：把代码归入正确的文件夹，把训练参数改成配置，
> 并保持命名统一。”

## 整理仓库时的关键原则

Agent **不会随意删除或重写你的代码**。它通过移动和重命名来整理，保持原有行为
不变。如果某段代码没有对应的目标文件夹，就**保留在项目根目录**，而不是删掉。

## 它搭建出的项目结构

从零开始时，Agent 会建立一套一致、可预期的项目结构，并始终在其中工作。具体而言，即为以下各项各设一个清晰、独立的归处：

- **各项设置** —— 一切控制实验的东西，按用途组织，让一次运行由它的设置完整描述。
- **代码本身** —— 处理数据、模型、以及共享辅助逻辑各有各的地方。
- **清晰的入口** —— 有显而易见的方式来开始训练或评估。
- **测试** —— 快速核验项目是否仍然完好。
- **项目日常维护** —— 一个健康项目在根目录会保留的那些标准配套文件。

每一部分在标准里都有清晰的归属，于是任何东西该放哪儿都不会含糊。这套结构就是**不变式**：Agent 只在它*内部*编写和重排代码，绝不会用另一套结构替换它。

## 它站在哪些实践之上

上面的两项规范，汲取自广受信赖的权威实践，按关注领域分列如下：

| 关注领域 | 依据 |
|------|------|
| **项目结构与写法风格** | [Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template)、[Hydra](https://hydra.cc/)、[Google Python 风格指南](https://google.github.io/styleguide/pyguide.html) |
| **模型与组件设计** | [PyTorch Lightning 风格指南](https://lightning.ai/docs/pytorch/stable/starter/style_guide.html)、[timm](https://github.com/huggingface/pytorch-image-models)、[OpenMMLab](https://github.com/open-mmlab) |
| **可复现的实验** | [Hydra](https://hydra.cc/)、[FAIR 数据原则](https://www.go-fair.org/fair-principles/)、[语义化版本](https://semver.org/)、[Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)、[Meta Research](https://github.com/facebookresearch) |
| **工程习惯与清晰接口** | [谷歌软件工程实践](https://google.github.io/eng-practices/)、[Scientific Python](https://learn.scientific-python.org/development/)、科研代码注释规范 |

## 如何使用

只需让 Agent 处理你的科研代码（搭建、添加、重构、命名、整理）。它会自动加载
本 Skill，并在工作过程中应用这套标准 —— 包括替你运行质量检查。

## 安装

本 Skill 是一个独立可安装的单元。请保留一份稳定的仓库副本，再让你的 agent
指向它的主文件——整个文件夹都要一起带上，因为 Skill 需要这些配套文件才能正常工作。

### Claude Code

先把仓库 clone 到稳定路径：

```bash
npm install -g @anthropic-ai/claude-code
claude
mkdir -p ~/ai-skills
git clone https://github.com/SaltGardenia/research-code-skill.git ~/ai-skills/research-code-skill
```

推荐做法：用一个 subagent wrapper 来加载 Skill 的主文件：

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

然后开启新的 Claude Code 会话，让这个 subagent 处理你的代码。比起把文件夹复制进
`~/.claude/skills/`，更推荐用 subagent（或 slash command），这样目录结构不会被破坏。

后续更新只需：

```bash
cd ~/ai-skills/research-code-skill
git pull
```

### 其他 agent（Kilo、Codex、OpenClaw、OpenCode、Hermes）

保留一份稳定的副本，再创建轻量的 subagent、slash command 或自定义 prompt
wrapper，指向 Skill 的主文件。Codex 也可以直接把仓库链接贴给它，让它读取
该文件并照此执行。示例提示词：

> 从这个仓库安装 skill：https://github.com/SaltGardenia/research-code-skill.git
> 并遵循它的主文件。请保留完整的文件夹，而不只是那一个文件。

### Python 依赖（仅当你自己运行检查器时）

质量闸门由 Agent 自动运行。如果你想在本地运行检查器，安装
项目里的 Python 工具即可：

```bash
python -m pip install -r requirements.txt
```
