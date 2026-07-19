# 参考：协调层——各来源如何协同（中文版 · 供开发者阅读）

> 本文件是 `references/coordination.md` 的中文对照版。智能体运行时仍应加载英文原版。

本技能是一个**编码规范层**，由权威参考资料加一个协调层提炼而来。这些参考资料**不是相互独立的检查清单**——
它们在不同的层上强化同一条流水线，并且关键地，它们**化合为四个使用集群**（而非十三份独立文件）。
每个集群是智能体随手可取的一个连贯关注点，把在不同抽象层级回答同一问题的标准融合在一起。
本文件是唯一的协调点；当你需要解决跨切面规则或将某条规范映射到其来源时加载它。

## 四个集群（融合的来源）

```text
1. 骨架与语法   (scaffold_grammar.md)
   Lightning-Hydra-Template  -> 每个文件所处的目录布局   (LHT-*)
   Hydra 配置              -> 填充布局的配置系统          (HY-*)
   Google Python Style     -> 每个 .py 文件遵守的语法      (GP-*)
   每当创建或放置一个文件时一起调用。

2. 模型与组件   (model_design.md)
   PyTorch Lightning Style  -> 模型/系统契约               (PL-*)
   timm 架构             -> 具体的命名架构形态          (RC-TIMM-*)
   OpenMMLab Registry      -> 可插拔：按配置选择，而非 if (RC-OPENMMLAB-*)
   每当写一个模型/骨干/组件时一起调用。

3. 实验可复现    (experiment_repro.md)
   Hydra 配置优先     -> 每个实验变量都存在于 cfg    (RC-HYDRA-*)
   FAIR 数据          -> 运行所消费的数据被固定         (RC-DATA-*)
   SemVer + Git Flow  -> 运行所用代码被打 tag           (RC-VER-*)
   Meta Research 理念  -> 实验是一个命名变体             (RC-META-*)
   每当一次运行被收尾、版本化或整理时一起调用。

4. 工程过程       (engineering_process.md)
   Software Engineering @Google -> 评审/变更规模/文档纪律 (RC-ENG-*)
   Scientific Python          -> ML 代码习惯 (fit/predict, 包) (RC-SP-*)
   每当定义、变更、评审一个公共符号时一起调用。
```

## 它们共同定义的流水线

```text
configs/  (Hydra: HY-*, RC-HYDRA-*)        -> 组合出一棵带类型的配置树
       | 经 _target_ / registry 实例化
       v
src/  (Lightning-Hydra-Template: LHT-*, PL-*) -> train.py 构建对象
       | LightningModule / DataModule (PL-*) + 命名架构 (RC-TIMM-*) + registry (RC-OPENMMLAB-*)
       v
Python 源码  (Google: GP-*)               -> 每个文件遵守风格/类型规则
       |
       v
data/ + 实验 (FAIR: RC-DATA-*, SemVer/GitFlow: RC-VER-*, SWE: RC-ENG-*, Meta: RC-META-*)
       | 受治理的数据集、被打 tag 的可复现发布、被评审的变更
       v
强制质量门 (LHT-TOOL)                     -> black . / isort . / ruff check .
                                            -> mypy src/ / pytest tests/
                                            -> 在提交/CI 前把关上述一切
   + Scientific-Python 纪律 (RC-SP-*)：可安装包、CI 风格+类型、sklearn fit/predict 习惯
```

## 各 reference 的职责（单一职责，不重叠）

| Reference | 拥有 | 前缀 | SKILL 类别 |
|-----------|------|--------|------------|
| `scaffold_grammar.md` | 项目目录布局、MLOps 文件、Hydra 配置系统、Python 语法 | `LHT-` `HY-` `GP-` | STRUCTURE / CONFIG / PYSTYLE |
| `model_design.md` | 模型/系统契约、命名架构分层、组件注册表 | `PL-` `RC-TIMM-` `RC-OPENMMLAB-` | LIGHTNING / TIMM / OPENMMLAB |
| `experiment_repro.md` | 配置优先运行、FAIR 数据、SemVer/GitFlow、Meta 实验理念 | `RC-HYDRA-` `RC-DATA-` `RC-VER-` `RC-META-` | HYDRA-CFG / DATA / VERSION / META |
| `engineering_process.md` | SWE 评审/变更纪律、Scientific-Python 习惯、**科研代码注释规范** | `RC-ENG-` `RC-SP-` `COMMENT-` | ENGINEERING / SCIENCE / COMMENT |

## 跨切面规则（集群必须达成一致之处）

1. **实例化链**——Hydra（`HY-STRUCT`）定义 `_target_` 配置；Lightning 模板（`LHT-01`）
   在 `src/train.py` 中经 `hydra.utils.instantiate` 消费；生成的对象遵守 PL 规则
   （`PL-INST`、`PL-INIT`）。缺 `configure_optimizers` 既是 `PL-OPT`（Lightning）也是
   `LHT-01` 结构性坏味道。OpenMMLab Registry（`RC-OPENMMLAB-002`）是另一条实例化路径，
   在非 Hydra 代码库中满足 `PL-INST`。
2. **带类型配置 == 带类型代码**——`HY-STRUCTCFG`（结构化配置）强化 `GP-TYPE`/`GP-ANN`
   （带注解的签名）。审计把未类型化的 `instantiate` 目标与未类型化的 `__init__` 视为关联发现。
3. **路径**——`HY-PATH` 禁止硬编码路径；`LHT-03` 要求 `.project-root` + `.env.example`。
   两者都必须成立以保证可复现。
4. **指标**——`PL-METRIC`（`/`-命名、torchmetrics、`sync_dist`）是模板最佳实践 `LHT-BP` 的具体实现。
5. **强制质量门**——`LHT-TOOL` 通过五个必检工具*实现* `GP-*` 规则：`black .`（格式化，行宽 99）、
   `isort .`（导入排序）、`ruff check .`（静态 lint）、`mypy src/`（类型）、`pytest tests/`（测试）。
   项目行宽（99）覆盖 Google 默认（80）；审计读取 `pyproject.toml` 获取覆盖值（`GP-LEN`）。
   `RC-SP-007` 是同一门的 Scientific-Python 表述（可安装包 + CI 风格+类型检查）。
6. **命名**——`GP-NAME`（snake_case/CapWords）同时约束配置键与 `src/` 模块名；
   `LHT-05` 期望 `src/data`、`src/models`、`src/utils`。`RC-TIMM-001` 是同一命名纪律在模型类层级的表达
   （命名为 `VisionTransformer`，而非 `MyModel`）。
7. **可复现发布闭环**——`RC-VER-001`（每个发布打 tag）固定数据版本（`RC-DATA-003`）和所用配置
   （`HY-EXP`）；`RC-ENG-004`（合并前评审）收尾。`RC-HYDRA-001` 使配置自包含到足以重生运行。
   `RC-META-005/006` 禁止 `train_v2_final.py`，要求 `train.py` + 实验配置。

## 统一规则码登记表

| 代码 | 来源（集群） | 类别 | 含义 |
|------|--------------|------|------|
| LHT-01..07, LHT-BP, LHT-TOOL | scaffold_grammar (template) | STRUCTURE | 布局/入口/根文件/测试/src 拆分/data-logs/实验/最佳实践/工具 |
| HY-ENTRY..HY-BEST | scaffold_grammar (hydra) | CONFIG | `@hydra.main` / defaults+`_target_` / 分组 / 路径 / 实验 / sweep / 结构化 / 最佳实践 |
| GP-*（40+ 代码） | scaffold_grammar (google) | PYSTYLE | 全部通用 Python 规则（见 scaffold_grammar.md） |
| PL-SYS..PL-DOC | model_design (lightning) | LIGHTNING | 系统/模型拆分 / 自包含 / 带类型 init / 方法顺序 / forward≠train / dataloader / datamodule / 指标 / ddp / 优化器 / hparams / 实例化 / docstring |
| RC-TIMM-001..004 | model_design (timm) | TIMM | 命名架构 / layers-blocks-architectures 分层 / 复用 / 工厂而非字符串 |
| RC-OPENMMLAB-001..003 | model_design (openmmlab) | OPENMMLAB | register_module / build_from_cfg / 无 if 阶梯 |
| RC-HYDRA-001..003 | experiment_repro (hydra rules) | HYDRA-CFG | 配置优先 / 无硬编码字面量 / 覆盖而非编辑 |
| RC-DATA-001..006 | experiment_repro (FAIR) | DATA | 数据集 id / 元数据 / 版本 / 加载器 / 运行固定 / 开放格式 |
| RC-VER-001..006 | experiment_repro (semver+gitflow) | VERSION | 每次发布打 tag / SemVer / main 稳定 / 分支 / release+hotfix / 升级 |
| RC-META-001..006 | experiment_repro (meta) | META | 可复现 / 配置而非硬编码 / 有文档 / 可基准 / 无 final 文件名 / 入口+配置 |
| RC-ENG-001..007 | engineering_process (google swe) | ENGINEERING | 文档 / 小变更 / 测试 / 评审 / 意图 / 一致性 / 接口文档永不漂移 |
| RC-SP-001..007 | engineering_process (scientific-python) | SCIENCE | sklearn 习惯 / 文档+类型 / 测试 / 基准 / 小 API / transform / 包+CI |
| COMMENT-001..017 | engineering_process (code_comments) | COMMENT | 为什么而非什么 / docstring / 数学公式 / 设计理由 / TODO / FIXME / WARNING / 实验注记 / 无陈旧 / 英文 / 密度 / 论文核心块 / 修改时更新 |

## 智能体如何随工作应用

1. 为当前关注点挑选**集群**，并只加载那一个 `references/*.md` 文件（惰性加载；不要一次性全加载）：
   - 布局 / 配置 / Python 语法 → `scaffold_grammar.md`
   - 模型 / 骨干 / 组件设计 → `model_design.md`
   - 实验运行 / 数据 / 版本 / 命名 → `experiment_repro.md`
   - 评审 / 变更规模 / API 习惯 → `engineering_process.md`
2. 当一次代码变更触及两个集群（例如一个实例化未类型化模块的配置），应用最具体的单一代码，
   并遵循另一份 reference 中的相关代码（在你的说明中交叉引用）。
3. 绝不让同一条规则挂在两个代码下；挑选拥有它的集群（上表）并交叉引用。
4. 聚合的 `RC-*` 机器可执行卡位于 `references/rule_cards.md`；应用跨切面标准
   （DATA/SCIENCE/VERSION/ENGINEERING/TIMM/OPENMMLAB/HYDRA-CFG）时把它作为索引加载。
