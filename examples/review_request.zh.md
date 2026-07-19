# 示例：智能体调用（在上下文中强制执行规范）

> 本文件是 `examples/review_request.md` 的中文对照版。智能体运行时仍应加载英文原版。

本文件展示智能体如何把 `research-code-skill` 当作一个**上下文式编码标准执行器**——
在构建或整理项目的同时应用规范，而非事后审查。本技能有两个核心场景（见 SKILL.md）。

## 场景 A — 从零搭建（绿地）

```
在 ./new_project 搭建一个新的科研项目，使其从第一天起就遵循实验室的编码标准，
然后加一个 ResNet 骨干和一个在 CIFAR 上训练它的 LightningModule
（正确的 src/ 目录、Google/PL 命名、Hydra _target_）。
```

智能体从 `templates/project_skeleton/` 搭建，并把每个新文件写成符合规范的样子
（`LHT-*`、`HY-*`、`PL-*`、`GP-*`）。

## 场景 B — 整理已有仓库

```
重构 ./legacy_exp 使其遵循标准：把代码移入 src/data、src/models、src/utils
和 configs/<group>/，把 train.py 中的 argparse flags 转为 Hydra 配置，
拆分模型与 LightningModule，并按命名规则重命名符号。保留训练行为。
```

智能体用 `scripts/audit_style.py` 审计，然后重构/重命名至合规，再重跑校验门。

## 智能体做什么（而非审查）

1. 为关注点加载匹配的 `references/` 文件（例如模块用 `PL-*`、配置用 `HY-*`、命名用 `GP-*`）。
2. 把代码写/移到符合规范（正确的目录、类形态、`_target_` 配置、`snake_case`/`CapWords` 命名）。
3. 运行 `python scripts/audit_style.py <target>` 作为确认门。
4. 从项目根运行强制质量门：
   `black . && isort . && ruff check . && mypy src/ && pytest tests/`。
5. 用 SKILL.md 中固定的“已应用规范”格式简要说明任何刻意偏离。

## 下方示例所针对的最小目标

假设智能体正向 `./my_project`（已有 scaffold 结构）添加
`src/models/components/resnet.py` 与 `src/models/cifar_module.py`。
生成的文件遵守 `PL-SYS`、`PL-ORDER`、`PL-METRIC`、`GP-NAME`、`GP-ANN`。
运行 `python scripts/audit_style.py ./my_project` 产生 `examples/sample_report.md` 中的合规报告。
