# Rule Card（中文版 · 供开发者阅读）

> 本文件是 `references/rule_cards.md` 的中文对照版。智能体运行时仍应加载英文原版。

建议的模式：与其仅链接文档，不如把每条标准抽象成一张 **Rule Card**（`RC-XXX-NNN`），
让智能体能直接检查并应用。本文件是所有 Rule Card 的单一索引。Rule Card 是跨切面的：
它们位于四个核心代码类别（`LHT-*` / `HY-*` / `PL-*` / `GP-*`）之上，覆盖数据、科学习惯、
版本化、工程过程，以及模型/实验纪律。

十三份来源标准被**融合进 4 个 reference 文件**，每个都是标准化合的天然使用集群（标准在其中化合而非堆叠）：

1. `scaffold_grammar.md` ——**项目骨架与 Python 语法**
   （Lightning-Hydra-Template + Hydra 配置 + Google Python Style）：布局（`LHT-*`）、
   配置系统（`HY-*`）、Python 语法（`GP-*`）。
2. `model_design.md` ——**模型与组件设计**
   （PyTorch Lightning Style + timm + OpenMMLab）：模型契约（`PL-*`）、具体架构形态（`RC-TIMM-*`）、
   可插拔（`RC-OPENMMLAB-*`）。
3. `experiment_repro.md` ——**实验可复现性**
   （Hydra 配置优先 + FAIR + SemVer/GitFlow + Meta Research）：config→data→code→experiment 链路
   （`RC-HYDRA-*`、`RC-DATA-*`、`RC-VER-*`、`RC-META-*`）。
4. `engineering_process.md` ——**工程过程与接口纪律**
   （Software Engineering at Google + Scientific Python）：评审/变更纪律（`RC-ENG-*`）与 ML 代码习惯
   （`RC-SP-*`）。

严重度：`BLOCKER`（破坏可复现性/运行）、`MAJOR`（违反核心规则）、`MINOR`（应修）。

## RC-DATA —— FAIR 数据管理（`references/experiment_repro.md`）
- RC-DATA-001：每个数据集/产物都有元数据（schema、来源、许可证）。[MAJOR]
- RC-DATA-002：每个数据集/产物都有唯一的、可解析的标识符。[MAJOR]
- RC-DATA-003：每个数据集声明一个固定到 git tag / DVC rev 的版本。[MAJOR]
- RC-DATA-004：每个数据集都随附加载说明（可运行的加载器）。[MAJOR]
- RC-DATA-005：每次实验运行都记录所用的确切数据版本。[BLOCKER]
- RC-DATA-006：数据格式/序列化是开放且标准的。[MINOR]

## RC-SP —— Scientific Python 生态（`references/engineering_process.md`）
- RC-SP-001：公共估计器暴露 `fit(X, y)` / `predict(X)`。[MAJOR]
- RC-SP-002：公共函数/类带有 docstring + 类型提示。[MAJOR]
- RC-SP-003：数值例程包含单元/回归测试。[MAJOR]
- RC-SP-004：可基准化的数值代码附带基准/计时测试。[MINOR]
- RC-SP-005：公共 API 变更小而可文档化、可评审。[MINOR]
- RC-SP-006：transformer 暴露 `transform` / `fit_transform`。[MINOR]
- RC-SP-007：项目作为可安装包发布；CI 运行风格 + 类型检查。[MINOR]

## RC-VER —— 版本化与 Git Flow（`references/experiment_repro.md`）
- RC-VER-001：每次实验发布映射到 git tag（`vMAJOR.MINOR.PATCH`）。[MAJOR]
- RC-VER-002：版本遵循 SemVer `MAJOR.MINOR.PATCH`。[MAJOR]
- RC-VER-003：`main` 只持有被打 tag 的稳定发布。[MAJOR]
- RC-VER-004：新工作位于 `feature/*` / `experiment/*`，而非直接位于 `main`。[MINOR]
- RC-VER-005：`release/*` 准备 MINOR/MAJOR；`hotfix/*` 用于 PATCH。[MINOR]
- RC-VER-006：打 tag 发布前先升版本（不静默发布）。[MINOR]

## RC-ENG —— Software Engineering at Google（`references/engineering_process.md`）
- RC-ENG-001：每个公共函数/类都带文档。[MAJOR]
- RC-ENG-002：每次变更都小、单一目的、可评审。[MAJOR]
- RC-ENG-003：每次变更都有测试覆盖。[MAJOR]
- RC-ENG-004：每次变更在合并到 `main` 前通过评审。[MAJOR]
- RC-ENG-005：变更意图被显式说明。[MINOR]
- RC-ENG-006：代码与周围风格/结构保持一致。[MINOR]
- RC-ENG-007：每次公共 API 变更都更新其 docstring（签名、参数、返回、示例），文档永不漂移。[MAJOR]

## RC-META —— Meta Research 仓库理念（`references/experiment_repro.md`）
- RC-META-001：每个实验都可复现（seed + 固定数据 + 记录配置）。[MAJOR]
- RC-META-002：旋钮位于配置中，而非硬编码在脚本里。[MAJOR]
- RC-META-003：每个实验都有文档（如何运行 + 含义）。[MAJOR]
- RC-META-004：每个实验瞄准清晰、可比较的基准/指标。[MINOR]
- RC-META-005：禁止文件名模式 `*_v<N>_*final*.py` / `*_new.py` / `*_copy.py` / `*_old.py`；
  使用 `train.py` + 实验配置。[MAJOR]
- RC-META-006：入口是 `trainer.py`/`train.py`；变体是 `configs/experiment/*.yaml`，而非新脚本。[MINOR]

## RC-HYDRA —— Hydra 配置优先（`references/experiment_repro.md`）
- RC-HYDRA-001：每个实验变量（lr、batch、seed、深度、路径、调度器）都存在于配置中并从 `cfg` 读取。[MAJOR]
- RC-HYDRA-002：代码中无硬编码实验字面量（如 `lr = 0.001`）；经 CLI/配置覆盖。[MAJOR]
- RC-HYDRA-003：实验仅通过配置覆盖区分，而非通过被编辑的代码字面量。[MINOR]

## RC-TIMM —— timm 模型架构风格（`references/model_design.md`）
- RC-TIMM-001：模型类以架构命名（如 `VisionTransformer`），而非泛化的 `MyModel`。[MAJOR]
- RC-TIMM-002：通用算子位于 `models/layers/`；组合位于 `models/blocks/`；命名模型位于 `models/architectures/`。[MAJOR]
- RC-TIMM-003：新的 vision-transformer 变体复用既有 `layers/`+`blocks/`；不重复 attention/FFN 代码。[MINOR]
- RC-TIMM-004：架构经模型工厂注册/导出，而非经字符串 `if model == "vit"` 引用。[MAJOR]

## RC-OPENMMLAB —— OpenMMLab 工程标准（`references/model_design.md`）
- RC-OPENMMLAB-001：可插拔组件被注册（`@X.register_module()`），而非经字符串 `if model == "..."` 选择。[MAJOR]
- RC-OPENMMLAB-002：组件经 `build_from_cfg(cfg)` / `Registry.build(cfg)` 实例化，而非手工分支构建。[MAJOR]
- RC-OPENMMLAB-003：新增组件只需一次注册 + 一条配置项，无需编辑中央 `if/elif` 阶梯。[MINOR]

## COMMENT —— 科研代码注释规范（`references/code_comments.md`）
- COMMENT001：注释解释**为什么**，而非**什么**（说明假设/意图）。[MAJOR]
- COMMENT002：每个公共函数/类带有 docstring（NumPy/PEP257 风格）。[MAJOR]
- COMMENT003：核心模块 docstring 说明功能、I/O、设计来源/参考。[MAJOR]
- COMMENT004：数学算法以注释形式带公式 + 引文。[MAJOR]
- COMMENT005：复杂算法带阶段性（Stage 1/2/3）块注释。[MINOR]
- COMMENT006：非显然的设计决策带 `Reason:` 注释。[MAJOR]
- COMMENT007：`TODO(owner): action + reason`（+ issue 链接）；不要裸 `TODO`。[MINOR]
- COMMENT008：已知问题用 `FIXME:` 并附临时解决方案说明。[MINOR]
- COMMENT009：危险代码用 `WARNING:` 说明危害。[MINOR]
- COMMENT010：经验约束用 `Experiment Note:`（观测到的差异）。[MINOR]
- COMMENT011：不要代码重述注释（`# convolution`）。[MINOR]
- COMMENT012：不要无意义注释（`# model`）。[MINOR]
- COMMENT013：不要与代码矛盾的陈旧注释（`# use ResNet` + `ViT()`）。[MAJOR]
- COMMENT014：核心代码注释用英文；中文仅用于临时实验笔记。[MINOR]
- COMMENT015：注释密度匹配代码类型（工具 ~10% —— 论文核心 40%+）。[MINOR]
- COMMENT016：每个论文核心模块都有 Purpose/Formula/Reference/IO/Complexity/Design 文档块。[MAJOR]
- COMMENT017：修改时更新/删除陈旧注释，并为新公共 API 写 docstring。[MAJOR]

## RC-KARPATHY —— LLM 编码纪律原则（`references/coordination.md`）
源自 Andrej Karpathy 对 LLM 编码失误的观察。这是一层**行为**护栏，位于
机械式 `RC-*` 卡之上：它约束智能体如何思考与编辑，而非具体用哪个符号/格式。
它直接对抗四种失效模式：错误假设、过度复杂、无关改动、目标模糊不可验证。

- RC-KARPATHY-001：**编码前先思考**——显式陈述假设；若存在歧义，列出多种
  解读并提问，而非默默猜测。[MAJOR]
- RC-KARPATHY-002：**编码前先思考**——存在更简单方案时要提出反对，陈述
  权衡取舍，而非盲目照字面执行。[MINOR]
- RC-KARPATHY-003：**编码前先思考**——停下来指认不清之处；不要隐藏困惑，
  也不要带着错误假设一路跑下去。[MAJOR]
- RC-KARPATHY-004：**简洁优先**——写出解决问题的最小代码；不写超出请求的功能、
  抽象、可配置性，或不必要的错误处理。[MAJOR]
- RC-KARPATHY-005：**简洁优先**——同样的工作若能大幅精简（如 200 → 50 行），
  就重写；资深工程师不应认为它过度复杂。[MINOR]
- RC-KARPATHY-006：**精准改动**——只触碰请求所要求的部分；不要"顺手改进"
  相邻代码、注释或格式。[MAJOR]
- RC-KARPATHY-007：**精准改动**——即便你有不同做法也要贴合现有风格；不要重构
  没坏的代码。[MINOR]
- RC-KARPATHY-008：**精准改动**——只删除*你的*改动所制造的未用导入/变量/函数；
  若发现既有的死代码，指出它，绝不在未获许可时删除。[MINOR]
- RC-KARPATHY-009：**目标驱动执行**——把命令式要求转化为可验证目标（如"先写
  一个能复现该 bug 的测试，再让它通过"）；循环执行直到满足成功标准。[MAJOR]
- RC-KARPATHY-010：**目标驱动执行**——多步工作前，先列出每项带 verify 步骤
  的简要计划。[MINOR]

> 注：这四条原则（编码前先思考、简洁优先、精准改动、目标驱动执行）偏向
> **谨慎而非速度**。对琐碎的单行改动（如改错别字）可自行判断——并非每次
> 改动都需要完整 rigor。它补充而非取代 `LHT-/HY-/PL-/GP-*` 及其他 `RC-*` 卡。

## 智能体如何使用 Rule Card

1. 为当前关注点挑选**集群**，然后只加载那一个 `references/*.md` 文件
   （惰性加载——不要一次性全加载）：
   - 布局 / 配置 / Python 语法 → `scaffold_grammar.md`
   - 模型 / 骨干 / 组件设计 → `model_design.md`
   - 实验运行 / 数据 / 版本 / 命名 → `experiment_repro.md`
    - 评审 / 变更规模 / API 习惯 → `engineering_process.md`
    - 行为纪律（Karpathy）→ `rule_cards.md`（`RC-KARPATHY-*`）
2. 对正在执行的操作，检查适用的 `RC-*` 卡与核心 `LHT-/HY-/PL-/GP-*` 代码（同文件、同集群）。
3. 在写代码/数据时应用它们；不要在本索引之外臆造卡。若某张卡与既有项目约定冲突，
   以项目约定为准，并注明偏离。
