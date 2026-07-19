# 参考：项目骨架与 Python 语法（中文版 · 供开发者阅读）

> 本文件是 `references/scaffold_grammar.md` 的中文对照版。智能体运行时仍应加载英文原版。

本参考是 **科研仓库如何布局** 以及 **其中 Python 如何书写** 的事实来源。它把三个始终一起被调用的紧密耦合标准融合进单一参考——每当创建或放置文件时：

- **Lightning-Hydra-Template** —— 固定的*目录布局*与 MLOps 工具（`LHT-*`，STRUCTURE）。
- **Hydra 配置** —— 用可组合、可覆盖的 YAML 填充布局的*配置系统*（`HY-*`，CONFIG）。
- **Google Python Style Guide** —— 每个 `.py` 文件遵守的*语法*（命名、格式化、类型、docstring）
  （`GP-*`，PYSTYLE）。

三者不可分：`configs/` 目录没有 Hydra 的组合规则就毫无意义，而 Hydra 的 `_target_` 可调用对象
没有 Google 式的干净、带类型 Python 也毫无意义。在搭建（场景 A）或放置任何文件（场景 B）时把它们作为一个整体应用。
`references/coordination.md` 登记表精确展示了哪个 `LHT-/HY-/GP-*` 代码拥有哪个关注点。

## 1. 目录布局（STRUCTURE —— `LHT-*`）

```
configs/          <- 按关注点分组的 Hydra 配置
  callbacks/ data/ debug/ experiment/ extras/
  hparams_search/ hydra/ local/ logger/ model/ paths/ trainer/
  train.yaml eval.yaml            <- 主配置（defaults 列表）
data/             <- 原始 / 处理后数据（git 忽略）
logs/             <- hydra + logger 输出，带时间戳（git 忽略）
notebooks/        <- 编号、首字母、简短描述（1.0-jqp-explore.ipynb）
scripts/          <- shell 脚本（Makefile 目标调用它们）
src/
  data/ models/ utils/
  train.py eval.py                <- @hydra.main 入口
tests/            <- 通用冒烟测试（pytest）
.env.example      <- 私有环境变量的模板（复制到 .env）
.gitignore
.pre-commit-config.yaml           <- 格式化 / lint / 安全钩子
.project-root                     <- 为 rootutils 标记项目根
environment.yaml / requirements.txt
pyproject.toml    <- pytest + coverage + 工具配置
setup.py          <- 把项目安装为包
Makefile          <- `make train/test/format/clean`
README.md
```

### 强制布局规则（`LHT-*`）

| 代码 | 规则 |
|------|------|
| LHT-01 | 入口位于 `src/train.py`/`src/eval.py`，使用 `@hydra.main` + 配置 |
| LHT-02 | 存在 `configs/` 目录，按关注点分组 |
| LHT-03 | 根目录提供 `.pre-commit-config.yaml`、`pyproject.toml`/`setup.py`、`requirements.txt`、`.gitignore`、`.env.example`、`.project-root` |
| LHT-04 | `tests/` 目录至少含一个冒烟测试 |
| LHT-05 | `src/` 按角色拆分：`data/`、`models/`、`utils/` |
| LHT-06 | `data/`、`logs/`、`notebooks/` 与源码分离（适当时 git 忽略） |
| LHT-07 | 实验是 `configs/experiment/` 下的配置，而非代码分支 |
| LHT-BP | 最佳实践信号（pre-commit、`.env`、`/` 指标、torchmetrics、DVC、包安装）存在 |
| LHT-TOOL | 已配置 linter/钩子（black/isort/flake8/interrogate） |

### 核心思想（快速实验）

- **CLI 覆盖**：`python src/train.py trainer.max_epochs=20 model.optimizer.lr=1e-4`；
  用 `+` 添加新键（`python src/train.py +model.new_param="x"`）。
- **最小样板**：从配置 `_target_` 实例化流水线（`hydra.utils.instantiate(cfg.model)`）。
- **主配置**（`configs/train.yaml`、`configs/eval.yaml`）通过 `defaults:` 列表设默认值。
- **实验配置**（`configs/experiment/*.yaml`）通过覆盖主配置来版本化最佳超参。
- **日志**：每次运行在 `logs/<task_name>/runs`（sweep 为 `/multiruns`）下写一个带时间戳的文件夹，
  内含 `.hydra/`、`checkpoints/`、`csv/`、`wandb/`。
- **超参搜索**：通过 `configs/hparams_search/` + `python src/train.py -m hparams_search=...` 用 Optuna/Ax/Nevergrad。
- **测试**：验证命令无异常运行的通用冒烟测试。
- **CI**：GitHub Actions 跑 pytest + pre-commit。

### 最佳实践（`LHT-BP`）

- **Miniconda** 每项目环境；**pre-commit** 在提交时自动格式化
  （`pre-commit install` → `pre-commit run -a`）。
- **私有环境变量放 `.env`**（git 忽略）；经 `${oc.env:MY_VAR}` 引用。绝不提交密钥。
- **指标用 `/` 命名**（`self.log("train/loss", ...)`）以便 logger 分组。
- **torchmetrics** 用于正确的多 GPU 规约；每个 step 用独立实例。
- **用 DVC 做数据/模型版本控制**（`dvc add data/MNIST`）。
- **作为包安装**（`pip install -e .`）使 `from src...` 可用；否则依赖 `rootutils.setup_root`。
- **本地配置不进版本控制**（`configs/local/default.yaml`，`optional` + git 忽略）。
- **强制 tag** 以区分实验，便于在 logger 中过滤。

### 工具配置（pre-commit 强制执行）—— `LHT-TOOL`

模板的 `.pre-commit-config.yaml` 按顺序运行：pre-commit-hooks
（trailing-whitespace、end-of-file-fixer、check-docstring-first、check-yaml、
debug-statements、detect-private-key、check-executables-have-shebangs、
check-toml、check-case-conflict、check-added-large-files）、**black**（`--line-length 99`）、
**isort**（`--profile black`）、**pyupgrade**（`--py38-plus`）、**docformatter**、
**interrogate**（`--fail-under=80`）、**flake8**、**bandit**、**prettier**（YAML）、
**shellcheck**、**mdformat**、**codespell**、**nbstripout** + **nbqa**。

`pyproject.toml` 配置 pytest（`--strict-markers`、`slow` marker、`--doctest-modules`）与 coverage；
`Makefile` 暴露 `train`、`test`、`test-full`、`format`、`clean`、`sync`。

## 2. 配置系统（CONFIG —— `HY-*`）

原则：从**组**组合出分层配置；从 **CLI**（`key=value`，用 `+key=value` 添加）覆盖任意值；
把配置纳入版本控制，其中*实验只是配置覆盖*；绝不硬编码绝对路径——从 `configs/paths/default.yaml` 解析。

### 入口模式 —— `HY-ENTRY`

```python
import hydra
import rootutils
from omegaconf import DictConfig

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

@hydra.main(version_base="1.3", config_path="../configs", config_name="train")
def main(cfg: DictConfig) -> None:
    ...
```

- `setup_root` 把项目根加入 `PYTHONPATH`、设置 `PROJECT_ROOT`、加载 `.env`——位置无关。
- 用 `if __name__ == "__main__": main()` 守护。

### 配置结构 —— `HY-STRUCT`

- 主配置以 `defaults:` 列表开头，其**顺序决定覆盖优先级**（后者胜）。
- 每个 YAML 要么是**defaults 列表**（`@package _global_`）要么是**组成员**。
- 用 `_target_` 指向可调用对象/类；经 `hydra.utils.instantiate(cfg.x)` 实例化。
- 组成员示例：
  ```yaml
  _target_: src.models.components.MyModel
  lr: 1.0e-3
  optimizer: adam
  ```

### 配置组 —— `HY-GROUP`

`callbacks/`、`data/`、`debug/`、`experiment/`、`extras/`、`hparams_search/`、
`hydra/`、`local/`、`logger/`、`model/`、`paths/`、`trainer/`。主配置按顺序组合它们：
```yaml
defaults:
  - _self_
  - data: mnist
  - model: mnist
  - callbacks: default
  - logger: null
  - trainer: default
  - paths: default
  - extras: default
  - hydra: default
  - experiment: null      # 版本化最佳超参
  - hparams_search: null  # 超参搜索配置
  - optional local: default # 机器/用户特定，git 忽略
  - debug: null           # 快速开发运行
```

### 路径解析 —— `HY-PATH`

`configs/paths/default.yaml` 解析所有文件系统根，使运行位置无关：
```yaml
root_dir: ${oc.env:PROJECT_ROOT}
data_dir: ${paths.root_dir}/data/
log_dir: ${paths.root_dir}/logs/
output_dir: ${hydra:runtime.output_dir}
work_dir: ${hydra:runtime.cwd}
```
使用 OmegaConf 插值（`${...}`），而非 f-string。`configs/hydra/default.yaml`
设置动态生成的输出目录（`${paths.log_dir}/${task_name}/runs/${now:...}`）。
用 `${oc.env:VAR}` 读取环境变量。

### 实验与搜索 —— `HY-EXP` / `HY-SWEEP`

- `configs/experiment/*.yaml` 覆盖主配置以版本化最佳超参；运行 `python src/train.py experiment=example`。
- `configs/hparams_search/*.yaml` 定义 Optuna/Ax/Nevergrad 搜索；
  运行 `python src/train.py -m hparams_search=mnist_optuna`（启动函数必须 `return` 被优化指标）。
- `configs/debug/*.yaml` 用于快速开发（限制 batch、过拟合、profiler）。

### 结构化配置 —— `HY-STRUCTCFG`

优先用 `@dataclass` / `DictConfig` 带类型 schema 而非原始 dict，使拼写错误与缺键尽早失败。
由 `hydra.main` + `hydra.utils.instantiate` 支持。与 `GP-TYPE`/`GP-ANN` 配对。

### 最佳实践 —— `HY-BEST`

- 无硬编码绝对路径；一切都从 `paths` 流出。
- 不要意外就地修改 `cfg`；优先结构化配置。
- 用 `python src/train.py --cfg job` 检视。
- `local/` 配置是 `optional` 且 git 忽略。
- 从组合配置实例化*每一个*对象（数据、模型、trainer、callbacks、loggers）——绝不在入口中命令式构造。

| 代码 | 含义 | 相关代码 |
|------|------|----------|
| HY-ENTRY | `@hydra.main` + `setup_root` 入口 | LHT-01 |
| HY-STRUCT | defaults 列表 / `_target_` 配置 | PL-INST |
| HY-GROUP | 配置组存在且被组合 | LHT-02 |
| HY-PATH | 插值、非硬编码路径 | LHT-03 |
| HY-EXP | 实验配置纳入版本控制 | LHT-07 |
| HY-SWEEP | 为搜索定义 hparams_search | LHT-BP |
| HY-STRUCTCFG | 结构化/带类型配置 | GP-TYPE |
| HY-BEST | 无硬编码路径；全部实例化 | 全部 |

## 3. Python 语法（PYSTYLE —— `GP-*`）

项目配置（模板的 Black 行宽 99）存在时覆盖 Google 默认（80）。每条规则映射到技能
`PYSTYLE` 发现与 `scripts/audit_style.py` 使用的 `GP-*` 代码。

### 语言规则

| 代码 | 来源 | 规则 |
|------|------|------|
| GP-LINT | 2.1 | 存在 pylint 配置；用 `# pylint: disable=` + 理由抑制 |
| GP-IMP / GP-IMPFMT | 2.2 / 3.13 | 绝对导入；分组 标准库→第三方→本地，无通配符 `*` |
| GP-PKG | 2.3 | 全路径导入；不依赖 `sys.path` 的 cwd |
| GP-EXC | 2.4 | 绝不裸 `except:`；捕获具体异常；`raise ... from e` |
| GP-GLOB | 2.5 | 无可变模块全局（除 `Final` 常量） |
| GP-COMP/GP-GEN/GP-LAMBDA/GP-COND | 2.7–2.11 | 合理的推导式/lambda/条件式 |
| GP-DEF | 2.12 | 无可变默认参数（用 `=None` 再初始化） |
| GP-PROP/GP-GETSET | 2.13/3.15 | `@property` 仅用于廉价访问 |
| GP-TRUE | 2.14 | 真值判断（`if foo:`，而非 `== True`） |
| GP-SCOPE/GP-DECO/GP-THREAD/GP-POWER/GP-FUTURE/GP-TYPE | 2.16–2.21 | 高级语言规则（词法作用域、装饰器、线程、强力特性、`__future__`、类型） |
| GP-RES | 3.11 | 文件/套接字用上下文管理器（`with`） |

### 风格规则

| 代码 | 来源 | 规则 |
|------|------|------|
| GP-SEMI | 3.1 | 无分号；每行一条语句 |
| GP-LEN | 3.2 | ≤80（Google）/ ≤99（项目 Black） |
| GP-PAREN | 3.3 | 节制使用括号 |
| GP-INDENT | 3.4 | 4 空格，无 tab；续行对齐 |
| GP-BLANK | 3.5 | 顶层之间 2 空行，方法之间 1 空行 |
| GP-WS | 3.6 | PEP8 间距；无尾随空格 |
| GP-SHEBANG | 3.7 | 仅可执行文件用 `#!/usr/bin/env python3` |
| GP-DOC | 3.8 | 每个公共模块/函数/类/方法带 docstring（PEP 257） |
| GP-STR | 3.10 | 一致使用 `"`；f-string；用 `logging` 而非 `print` |
| GP-TODO | 3.12 | `TODO(username): 做什么及为什么` |
| GP-NAME | 3.16 | `lower_snake_case` / `CapWords` / `UPPER_CASE`；不用 `l`/`I`/`O` 单字母 |
| GP-MAIN | 3.17 | `if __name__ == "__main__":` 守护 |
| GP-FLEN | 3.18 | 函数保持简短；抽取辅助函数 |
| GP-ANN | 3.19 | 注解所有签名；输入用 `Sequence`/`Mapping` |

### 把三层绑在一起的注记

- 模板的工具（`LHT-TOOL`）通过 black/isort/flake8 *实现* `GP-*` 规则；
  项目行宽（99）覆盖 Google 默认（80）——从 `pyproject.toml` 读取覆盖值（`GP-LEN`）。
- `HY-STRUCTCFG` 强化 `GP-TYPE`/`GP-ANN`：未类型化的 `instantiate` 目标与未类型化的 `__init__` 是关联发现。
- `GP-NAME` 同时约束配置键与 `src/` 模块名；`LHT-05` 期望 `src/data`、`src/models`、`src/utils`。
