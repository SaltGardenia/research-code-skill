---
name: research-code-skill
description: >-
  面向 AI 智能体、用于科研（机器学习/深度学习）项目的编码规范执行器。它的核心职责有两点：
  （1）在所有编码工作中保持项目固定的架构不变——绝不破坏或偏离既定结构；
  （2）强制执行代码级规范——命名、格式化、调用方式与配置——使每个文件都保持一致。
   它将十三份权威参考资料融合为四个使用集群，并以机器可执行的 Rule Card（RC-*）形式固化，
   另加一层受 Karpathy 启发的编码纪律（编码前先思考、简洁优先、精准改动、目标驱动执行），
   覆盖于机械卡之上，避免把这些来源堆叠成彼此独立的检查清单。触发场景包括任何代码任务：
  “加一个模型”“写训练脚本”“重构这个模块”“搭建项目骨架”“给函数命名”
  “加一个配置组”“管理数据集元数据”“给实验发布打标签”“这个文件应该用什么结构”。
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
version: 1.2.0
author: research-code-skill
tags:
  - python
  - research
  - machine-learning
  - code-style
  - pytorch-lightning
  - hydra
  - best-practices
  - coding-standards
  - project-structure
compatibility:
  - claude
  - gpt
  - kilo
  - any-model-supporting-skills
---

# Research Code Skill（中文版 · 供开发者阅读）

> 本文件是 `SKILL.md` 的中文对照版，方便开发者阅读。智能体运行时仍应加载英文原版 `SKILL.md`。

本技能充当科研实验室 ML/DL 项目的**编码规范层**。它不在事后审查代码，而是活在智能体的上下文里，
**在每一次代码操作发生的同时就施加约束**。其本质有两点：

1. **项目架构**——保持实验室固定的项目结构不变。当智能体写或修改代码时，架构是稳定基座：
   不要破坏它，不要另起炉灶，保持它清晰一致。
2. **代码级规范**——在该架构之内，每一个符号与调用都遵循统一规则：命名、格式化、导入/调用风格，
   以及配置如何组合。

这两条轴线在两个核心场景（从零搭建、整理已有仓库）中都得到强制执行。智能体在写或改任何项目代码之前
先查阅本技能，因此代码库在构建之初就保持连贯。

本技能将十三份权威参考资料提炼为**四个融合的使用集群**，外加一个协调层，汇成一套共享规范集。
每个集群是智能体随手可取的一个连贯关注点——其中的来源是“化合”而非“堆叠”：

1. **项目骨架与 Python 语法**（`references/scaffold_grammar.md`）
   ——融合 Lightning-Hydra-Template（结构，`LHT-*`）、Hydra 配置（`HY-*`）
   与 Google Python Style（`GP-*`）：承载代码的布局、填充布局的配置系统、书写其中 Python 的语法。
2. **模型与组件设计**（`references/model_design.md`）——融合 PyTorch Lightning Style（`PL-*`，
   模型/系统契约）、timm 架构风格（`RC-TIMM-*`，命名架构 + `models/{layers,blocks,architectures}`）
   与 OpenMMLab Registry（`RC-OPENMMLAB-*`，`@X.register_module()` + `build_from_cfg`）：
   一个形态良好、可插拔的模型应该长什么样。
3. **实验可复现性**（`references/experiment_repro.md`）——融合 Hydra 配置优先（`RC-HYDRA-*`）、
   FAIR 数据（`RC-DATA-*`）、SemVer+Git Flow（`RC-VER-*`）与 Meta Research 理念（`RC-META-*`）：
   让一次运行可重新生成的 config→data→code→experiment 链路。
4. **工程过程与接口纪律**（`references/engineering_process.md`）——融合 Software Engineering at Google
   （`RC-ENG-*`，评审/变更规模/文档）与 Scientific-Python 习惯（`RC-SP-*`，`fit`/`predict`、
   可安装包、CI）：“好的代码”作为工程产物意味着什么。它还拥有**科研代码注释规范**
   （`references/code_comments.md`，`COMMENT-*`）：科研注释记录意图/数学/设计决策/实验约束，
   而非逐行叙述。
5. **references/coordination.md** + **references/rule_cards.md**——把全部来源映射到一套规则码登记表
   （`LHT-/HY-/PL-/GP-*` 加上 `RC-*` Rule Card），使每条规范唯一、不重复、可被机器检查。

## 在工作流中的角色

本技能是项目上下文的**核心组成部分**，而非可选工具。把它当作项目成文的工程章程：

- **架构优先**：既定结构（`configs/`、`src/data`、`src/models`、`src/utils`、入口脚本、根文件）是不变量。
  每一次代码操作都尊重它；绝不绕过或拆解它。
- 在项目初始化时（场景 A），从 `templates/project_skeleton/` 搭建结构。
- 在每一次代码变更（增/改/删文件或符号）前，先查相关 reference 找到适用的规范，再按它写。
- 给任何东西命名时（模块、类、函数、变量、配置键、配置文件），套用适用 reference 中的命名规则。
- 当用户的请求会破坏某条规范时，遵循规范并简要说明你所做的偏离
  （不要默默偏离，也不要默默自创）。

## 两个核心场景

本技能只在两种情况下使用。两者共享同一不变量：**保留项目架构**——它是稳定基座；
代码在它*内部*增添和变更，绝不以破坏或绕过它的方式。在该架构之内，所有代码服从**代码级规范**
（命名、格式、调用）。识别当前属于哪个场景，并按其模式操作。

> **两条监管轴**
> 1. **架构（项目级）**——固定结构：`configs/` 按关注点分组，`src/data` · `src/models` · `src/utils`，
>    入口脚本，根文件。保持清晰；不要拆解或重造它。
> 2. **代码级**——命名、格式化、导入/调用风格，以及配置组合，跨所有文件统一。

### 场景 A — 从零搭建（绿地）

目标为空或尚不存在。用本技能构建整个项目，使其从第一个提交起就符合规范：

- 从 `templates/project_skeleton/`（scaffold 模式）起步，铺下**固定架构**：
  目录结构、根文件、`configs/`、`src/`。
- 在该架构内严格书写每一个新文件：正确的目录、正确的模块形态、正确的配置组合、正确的名称。
- 此模式只向前，没有现成代码需要调和。

### 场景 B — 整理已有仓库

目标是一个已有仓库，其中代码可能未遵循规范。用本技能把它带入**同一架构**而不破坏它：

- 先对照规则码登记表**审计**现状（运行 `scripts/audit_style.py`，或从 reference 推理）以枚举缺口。
- 然后**重构与重写**以贴合固定架构：把文件移入 `src/`、`configs/<group>/`；把硬编码参数转为 Hydra 配置；
  拆分模型与系统；按 `GP-NAME`/`PL-*` 重命名符号；补上缺失的根文件与 `tests/`。
- 在改变形态的同时保留行为；通过**移动/重命名**来重组，且**绝不要任意删除或重写**既有代码。
  若某段代码没有匹配的归属目录，**把它留在项目根目录**而非删除。**绝不用另一种架构替换本架构**。
- 汇报所做的具体改动（每组改动附一条简短的“已应用规范”说明），并重跑一致性校验门确认。

## 何时使用

只要智能体在该科研项目中工作，就应用本技能：

- **场景 A（搭建）**：搭建并书写一个从头就遵循规范的全新科研项。
- **场景 B（整理）**：重组、重命名、重构已有仓库，使其架构、命名与配置符合标准。
- 任一场景内的**持续代码操作**：创建/读取/更新/删除文件或符号，或选择名称——始终按规范。

不要用于：

- 没有 Python/ML 后端的纯前端/纯 Web 项目。
- 非 Python 语言（C++、JS），除非仅适用 Google 命名/文本规则。

## 前置条件

在应用规范前，确认：

1. 提供了目标路径（仓库根、目录或具体文件）。
2. 变更涉及项目内的 Python 代码或 Hydra YAML 配置。
3. 拥有读取权限；仅在操作需要时才 Write/Edit。
4. 若需执行脚本，需有 Python 3.8+ 解释器。

若未给出目标，先向用户询问路径再继续。判定场景：若目标为空或不存在，用**场景 A**
（scaffold，步骤 5）；若已包含代码，用**场景 B**（整理，步骤 5→6）。

## 流程

在工作的同时应用规范。每一步映射到某份 reference 来源；只为当前操作加载对应的那一簇 reference。

> 惰性加载 reference：只为被操作的关注点读取 `references/` 下的**那一个集群文件**。
> 不要一次性全加载——四个文件是融合的，挑拥有该关注点的那一个。
> - 骨架与语法 → `references/scaffold_grammar.md`（布局 `LHT-*`、配置 `HY-*`、Python `GP-*`）
> - 模型与组件 → `references/model_design.md`（`PL-*`、`RC-TIMM-*`、`RC-OPENMMLAB-*`）
> - 实验可复现 → `references/experiment_repro.md`（`RC-HYDRA-*`、`RC-DATA-*`、`RC-VER-*`、`RC-META-*`）
> - 工程过程 → `references/engineering_process.md`（`RC-ENG-*`、`RC-SP-*`、`COMMENT-*`）
> - 跨切面 → `references/coordination.md` + `references/rule_cards.md`
> - 行为纪律 → `references/rule_cards.md`（`RC-KARPATHY-*`）

### 步骤 1 — 项目结构与 Python 语法（集群 1）

加载 `references/scaffold_grammar.md`（融合 Lightning-Hydra-Template 布局、Hydra 配置系统、
Google Python 语法），然后按布局放置代码：

- `configs/` 存放按关注点分组的 Hydra YAML 配置
  （`data/`、`model/`、`trainer/`、`callbacks/`、`logger/`、`experiment/` 等）。
- `src/` 按角色拆分源码：`src/data/`、`src/models/`、`src/utils/`，入口为 `src/train.py`、`src/eval.py`。
- `tests/` 存放通用冒烟测试；`data/`、`logs/`、`notebooks/` 彼此分离。
- 根文件：`.pre-commit-config.yaml`、`pyproject.toml`（或 `setup.py`）、`requirements.txt`、
  `.gitignore`、`.env.example`、`.project-root`。

创建文件时，把它放在匹配目录下（代码 `LHT-01..07`）。

### 步骤 2 — 配置规范（Hydra）

加载 `references/scaffold_grammar.md`（CONFIG 段），然后书写满足以下要求的配置：

- 入口处使用 `@hydra.main(version_base=..., config_path=..., config_name=...)`，
  配合 `rootutils.setup_root` 实现位置无关。
- 按组组合，通过 CLI 与 `@` defaults 列表覆盖。
- 每个对象表达为一个 `_target_` 加原始类型参数。
- 所有路径经 `configs/paths/default.yaml` 解析（无硬编码路径）。
- 把实验作为 `configs/experiment/` 下的配置纳入版本控制。

应用代码 `HY-ENTRY`、`HY-STRUCT`、`HY-GROUP`、`HY-PATH`、`HY-EXP`、`HY-BEST`。

### 步骤 3 — LightningModule / DataModule 规范（集群 2）

加载 `references/model_design.md`（PyTorch Lightning 契约 + timm + OpenMMLab），然后塑造满足以下要求的模块：

- 将**模型**骨干与**系统**（`LightningModule`）分离。
- **自包含**：优化器 + 调度器位于 `configure_optimizers` 中。
- 拥有**显式、带类型的 `__init__`** 并给出合理默认值（不要不透明的 `params`）。
- 遵循**方法顺序**：`__init__` → `forward` → `training_step` → 验证 → `test` →
  `configure_optimizers` → 额外钩子。
- 保持 `forward()` 仅用于推理（绝不放训练逻辑）。
- 用 `LightningDataModule` 处理数据；`torchmetrics`（每个 step 用独立实例）、`/`-命名的指标、
  在 DDP 下用 `sync_dist=True`。

应用代码 `PL-SYS`、`PL-SELF`、`PL-INIT`、`PL-ORDER`、`PL-FWD`、`PL-DM`、`PL-METRIC`、`PL-DDP`、
`PL-OPT`、`PL-HPARAM`。

### 步骤 4 — Python 风格与命名（Google Python Style Guide）

加载 `references/scaffold_grammar.md`（PYSTYLE 段），然后书写满足以下要求的代码：

- 函数/变量用 `snake_case`，类用 `CapWords`，常量用 `UPPER_CASE`；
  避免 `l`、`I`、`O` 单字母名（`GP-NAME`）。
- 行宽 ≤ 80（Google），除非项目设为 99（Black/PL 模板覆盖）（`GP-LEN`）。
- 导入分组：标准库、第三方、本地；禁止通配符导入（`GP-IMP`）。
- 每个公开模块/类/函数都带 docstring（`GP-DOC`）。
- 所有函数签名带类型注解（`GP-ANN`/`GP-TYPE`）。
- 避免分号、裸 `except:`、可变默认参数、用 `print` 做诊断（`GP-SEMI`/`GP-EXC`/`GP-DEF`/`GP-PRINT`）。
- 用 `if __name__ == "__main__":` 守护可执行脚本（`GP-MAIN`）。

用 `scripts/audit_style.py` 作为一致性校验门（它检查这些代码的一个子集）。
完整规则登记表见 `references/coordination.md`。

### 步骤 5 — 从零搭建（场景 A）

目标为空或不存在时使用。加载 `references/scaffold_grammar.md`，然后从 `templates/project_skeleton/`
按其中的 `MANIFEST.md` 生成目录骨架。复制 `configs/` + `src/` 桩与根文件。不要覆盖用户既有文件；
准确汇报创建了什么、跳过了什么。随后在书写每个新文件时继续步骤 1–4，使项目从首个提交起就符合规范。
6. **同步 `.gitignore`**：运行 `python scripts/sync_gitignore.py .`，使忽略列表反映刚创建的布局
   （脚本只维护其自动管理块，绝不触碰手写规则）。

### 步骤 6 — 整理已有仓库（场景 B）

目标已有代码时使用。通过重构而非仅标注缺口来应用规范：

1. **审计**现状对照规则码登记表（运行 `scripts/audit_style.py` 和/或从 reference 推理），
   按类别（STRUCTURE / CONFIG / LIGHTNING / PYSTYLE）枚举偏离。
2. **重构**：把文件移入 `src/data`、`src/models`、`src/utils`、`configs/<group>/`；
   补上缺失的根文件与 `tests/`。
3. **重写为符合规范**：把硬编码参数转为 Hydra `_target_` 配置；拆分模型骨干与 `LightningModule` 系统；
   按 `GP-NAME` / `PL-*` 重命名符号；应用 `torchmetrics` 与 `/`-命名的日志。
4. **保留行为**——优先移动/重命名而非删除；保持输出一致。
5. **确认**：重跑 `scripts/audit_style.py`；剩余的 BLOCKER/MAJOR 项必须先解决，才能宣告仓库整理完成。
6. **同步 `.gitignore`**：运行 `python scripts/sync_gitignore.py .`，使忽略列表跟踪新创建/移动过的目录
   （如 `logs/`、`outputs/`、`wandb/`、`checkpoints/`）。脚本从当前布局在带标记的自动管理块内推导条目；
   手写规则被保留。

### 步骤 7 — 应用并确认（两场景通用）

把代码写成符合规范的样子。当一次变更触及两层（例如一个实例化未类型化模块的配置），
应用最具体的单一代码，并遵循另一份 reference 中的相关代码（见 `references/coordination.md`）。
若有可用的校验脚本，运行它来确认改动成立。

### 步骤 8 — 运行强制质量门（两场景通用）

写完/改完代码后，项目必须在变更被接受前通过标准质量工具。这些是实验室的必检项；
从项目根运行（配置位于 `pyproject.toml` / `.pre-commit-config.yaml`）：

```bash
black .                 # 1. 格式化（默认行宽 99）
isort .                 # 2. 导入排序（black profile）
ruff check .            # 3. 静态 lint + 导入/风格/复杂度检查
mypy src/              # 4. 跨源码包的类型检查
pytest tests/          # 5. 运行测试套件（冒烟 + 单元）
```

规则：

- 按顺序运行全部五项；不要跳过任何一项。修复它们报告的每一个错误。
- `black`/`isort` 可能重写文件——之后重新读取，再运行一次确认干净。
- `mypy src/` 必须零类型错误（`strict` 可选；至少公共签名不能无类型——见 `GP-ANN`）。
- `pytest tests/` 必须全绿；为任何新的 `LightningModule`/`DataModule`/入口新增或扩展冒烟测试。
- 在 CI 中，这一确切序列作为门运行；本地是同一契约。

### 步骤 9 — 应用 Rule Card（跨切面，两场景通用）

除四类核心代码外，本技能还以 **Rule Card**（`RC-*`）形式强制执行七个标准族——它们是抽象、
可被机器检查的规范，而非简单的链接。它们内嵌在四个集群文件中。加载 `references/rule_cards.md`
（索引）加对应关注点的集群文件：

- **集群 3 — 实验可复现性**（`references/experiment_repro.md`）：
  - **Hydra 配置优先** `RC-HYDRA-*`：每个实验变量（lr、batch、seed、路径……）都存在于配置中，
    从 `cfg` 读取；不要像 `lr = 0.001` 那样硬编码字面量。
  - **FAIR 数据** `RC-DATA-*`：数据集有元数据、标识符、固定到 tag 的版本、可运行加载器；
    每次运行记录其数据版本。
  - **版本化 / Git Flow** `RC-VER-*`：每次实验发布是一个遵循 SemVer 的 git tag；
    工作在 `feature/*`/`experiment/*` 上，而非 `main`。
  - **Meta Research 理念** `RC-META-*`：可复现/可配置/有文档/可基准化的实验；
    不要 `train_v2_final.py`，变体即实验配置。
- **集群 2 — 模型与组件设计**（`references/model_design.md`）：
  - **timm 模型设计** `RC-TIMM-*`：为架构命名（如 `VisionTransformer`，而非 `MyModel`）；
    算子放 `models/layers/`、块放 `models/blocks/`、命名模型放 `models/architectures/`；经工厂注册。
  - **OpenMMLab Registry** `RC-OPENMMLAB-*`：用 `@X.register_module()` 注册组件，
    经 `build_from_cfg(cfg)` 构建；绝不用 `if model == "vit"` 分支。
- **集群 4 — 工程过程**（`references/engineering_process.md`）：
  - **工程（Google）** `RC-ENG-*`：小而可评审的变更、有文档的公共 API、测试覆盖、
    合并到 `main` 前评审；接口文档永不漂移（`RC-ENG-007`）。
  - **Scientific Python** `RC-SP-*`：估计器暴露 `fit(X,y)`/`predict(X)`；
    公共符号有文档 + 类型；数值代码有测试；可安装包 + CI。
  - **科研代码注释规范** `COMMENT-*`：注释解释**为什么**（意图、数学、设计决策、实验约束），
    而非逐行叙述；公共 API/docstring 遵循 NumPy/PEP257；数学带公式 + 引文；`TODO(owner): reason`；
     无陈旧注释（`COMMENT-001..017`）。
  - **LLM 编码纪律（Karpathy）** `RC-KARPATHY-*`：位于机械卡之上的行为层——**编码前先思考**
     （暴露假设、权衡、困惑）、**简洁优先**（最小代码、无臆想抽象）、**精准改动**
     （只改被要求的、贴合风格、只清理自己制造的孤儿）、**目标驱动执行**（命令式 →
     可验证目标 + 验证循环）。对抗 LLM 失效模式——错误假设、过度复杂、无关改动、模糊目标——
     偏向谨慎而非速度（琐碎单行改动可自行判断）。


当某条 Rule Card 触及已被 `LHT-/HY-/PL-/GP-*` 覆盖的代码时，应用最具体的单一代码并交叉引用；
绝不在两个代码下重复同一条规则。

## 强制质量工具

这五个工具是受本技能约束的每一个科研项目的**必检项**。它们把规范落地：`black`/`isort` 强制格式化
（`GP-LEN`/`GP-IMP`），`ruff` 强制静态规则（`GP-SEM*`/`GP-EXC`/...），`mypy` 强制类型
（`GP-ANN`/`GP-TYPE`），`pytest` 强制代码确实能跑。它们的配置随 scaffold 模板提供。

| 工具 | 用途 | 调用 |
|------|------|------|
| black | 格式化 | `black .` |
| isort | 导入排序 | `isort .` |
| ruff | 静态分析 / lint | `ruff check .` |
| mypy | 类型检查 | `mypy src/` |
| pytest | 测试 | `pytest tests/` |

## 输出格式

本技能默认不输出审查报告。它**塑造它所写的代码**。当你必须向用户解释某条规范选择时，
返回一段简短、固定的 Markdown 说明：

```markdown
# 已应用规范：<操作> 于 <目标>

## 决策
- <应用了哪种结构/命名/配置模式>

## 规则
- <代码> — <登记表中该规则的一句话>

## 说明
- <可选：刻意偏离或已消除的歧义>
```

代码是 `references/coordination.md` 中的统一登记表：STRUCTURE（`LHT-*`）、CONFIG（`HY-*`）、
LIGHTNING（`PL-*`）、PYSTYLE（`GP-*`）。严重度仅在运行脚本时使用：`BLOCKER`（破坏运行/复现）、
`MAJOR`（核心规则）、`MINOR`（风格瑕疵）。

## 错误处理

- **未找到 Python/配置目标**：向用户询问路径，或从零搭建（场景 A，步骤 5）。
- **校验脚本缺依赖**：打印 `pip install -r requirements.txt`，重试一次；若仍失败，退回到手动规范检查。
- **Write 权限被拒**：停止，说明哪些无法写入，并建议用户授权。
- **文件无法解析**：跳过它，注明原因，继续其余部分。
- **目标非空却请求场景 A**：切换到场景 B（整理）——绝不覆盖；重构并补上缺失文件，汇报冲突。
- **reference 文件缺失/不可读**：加载下一个适用 reference；若都没有，退回到此处内联规则并标记缺口。
- **规则有歧义**：优先采用项目自己的 `pyproject.toml`/`setup.cfg` 配置而非通用默认，并注明应用的覆盖。

## 约束

- **架构是不变量**：项目固定的结构即稳定基座。编码时绝不要破坏、绕过或用别的布局替换它。
  在架构*内部*增添和变更代码；保持它清晰。
- 单一职责：本技能只管科研代码规范（架构、命名、结构、配置）；不要混入无关任务。
- 它是**上下文式执行器**，而非事后审查器：在代码被写/改的同时应用规范，而非之后。
- 仅两条轴：（1）项目级架构，（2）代码级命名/格式/调用。两者都保持统一；不要引入第三、临时的关注点。
- 除非用户明确要求，绝不自动提交或推送变更。
- 绝不臆造配置值或名称；从规范和既有项目模式中推导。
- 尊重项目既有的行宽 / 格式化配置（若存在）。
- 惰性加载 reference 文档：只为被操作的关注点读取 `references/` 文件，而非一次性全读。
- 使用 `references/coordination.md` 中的统一规则码登记表；绝不要发明不在登记表中的代码，
  也绝不要让同一条规则挂在两个代码下。
