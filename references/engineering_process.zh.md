# 参考：工程过程与接口纪律（中文版 · 供开发者阅读）

> 本文件是 `references/engineering_process.md` 的中文对照版。智能体运行时仍应加载英文原版。

本参考是 **“好的代码”作为工程产物意味着什么** 的事实来源——跨其他参考产出的每一个文件。
两个标准在此融合，因为它们在同一张桌子上从两个座位回答同一个问题：

- **Software Engineering at Google** —— *过程*：小而可评审的变更、清晰意图、测试、代码评审、
  以及永不漂移的接口文档（`RC-ENG-*`）。
- **Scientific Python 生态** —— *代码级习惯*：NumPy/SciPy/sklearn 约定、`fit`/`predict` 估计器 API、
  docstring + 类型、作为可安装包交付并配 CI（`RC-SP-*`）。

它们化合：Google 说“文档化并测试公共 API”；Scientific-Python 说“这是该 API 的具体形态
（`fit`/`predict`、可安装包、CI 风格+类型检查）”。每当你定义、变更或评审一个公共符号时应用两者。

## 1. 工程过程（ENGINEERING —— `RC-ENG-*`）

提炼自 *Software Engineering at Google* 与 Google Engineering Practices / Code Review 指南。

**原则**

- **小而可评审的变更**——一个 CL/PR 一个逻辑变更；易于推理与回退。
- **清晰意图**——每次变更陈述其目的；不静默蔓延范围。
- **可测试**——被测试覆盖；行为可验证。
- **可维护**——简单、有文档、与周围代码一致。
- **代码评审**——每次变更都评审；评审者检查正确性、测试、清晰度、约定。

**评审者检查什么**（每个维度）：设计 · 功能 · 复杂度 · 测试 · 命名 · 注释 · 风格 · 文档。

### Rule Card

| 代码 | 规则 | 严重度 |
|------|------|--------|
| RC-ENG-001 | 每个公共函数/类都带文档（docstring）。 | MAJOR |
| RC-ENG-002 | 每次变更都小、单一目的、可评审。 | MAJOR |
| RC-ENG-003 | 每次变更都被测试覆盖（或说明为何不）。 | MAJOR |
| RC-ENG-004 | 每次变更在合并到 `main` 前通过评审。 | MAJOR |
| RC-ENG-005 | 变更意图被显式陈述（清晰目的，无范围蔓延）。 | MINOR |
| RC-ENG-006 | 代码与周围风格/结构保持一致。 | MINOR |
| RC-ENG-007 | 每次公共函数/类变更都更新其接口文档（签名、参数、返回、示例），文档永不漂移。 | MAJOR |

### 接口文档（自维护）—— `RC-ENG-007`

接口文档是一个*活产物*，而非一次性说明。本技能不自动生成独立的 API 文件；而是智能体在编辑时
让每个公共符号上的 docstring 与代码保持同步：

- **位置**：函数/类自身的 docstring（对于 scaffold，即 `src/` 下逐模块 docstring）。
  由 `GP-DOC` / `PL-DOC` / `RC-SP-002` 强制。
- **记录什么**：签名、参数（`:param x:`）、返回（`:return:`）、抛出的异常，以及有用的可运行示例（doctest）。
  与变更平行——重命名的参数、新的返回字段、或改变的默认值，都在同一处编辑中更新文档。
- **漂移是 MAJOR 坏味道**：公共 API 的 docstring 不再匹配其签名即违反 `RC-ENG-007`。
  智能体在改代码的同一遍中修复文档，使生成的 API 页面始终反映当前接口。
- 可选：若项目保留独立的 `docs/api.md`，变更时更新对应条目。

## 2. Scientific-Python 习惯（SCIENCE —— `RC-SP-*`）

提炼自 Scientific Python Developer Guide 与 NumPy / SciPy / scikit-learn 生态。

**它们强制什么**

- **API 设计**——小、一致、可组合接口；合理默认值。
- **文档**——每个公共符号有文档；有用处放 doctest。
- **测试**——单元 + 回归测试；数值例程的基准。
- **贡献流**——小而可评审的变更；清晰意图。
- **打包**——作为可安装包交付（setuptools / hatchling / meson-python）；
  保持源码可导入（`pip install -e .` 或 `rootutils.setup_root`）。
- **风格检查**——CI 中的自动化格式化/linter（black / isort / ruff / flake8），不靠人手争风格。
- **静态类型**——CI 中用 mypy/pyright 检查类型注解。
- **持续集成**——每次变更跑 pytest + pre-commit + 类型检查；
  `scientific-python/cookie` 模板生成带九个构建后端和 Nox 测试 CI 的仓库。
- **仓库评审**——`sp-repo-review` 按指南的检验项审计仓库。

### 估计器 API（scikit-learn 习惯）

此处对 ML 代码最重要的单一约定：

```python
model.fit(X, y)        # 从数据学习
model.predict(X)       # 在新数据上推断
```
而非 `model.train_magic()` 这类临时名字。任何暴露给用户的模型都应遵循 `fit` / `predict`
（transformer 加 `transform` / `fit_transform`，评估器加 `score`）。
这使实验室的模型可互换、熟悉。

### Rule Card

| 代码 | 规则 | 严重度 |
|------|------|--------|
| RC-SP-001 | 公共估计器暴露 `fit(X, y)` / `predict(X)`（sklearn 习惯）。 | MAJOR |
| RC-SP-002 | 公共函数/类带 docstring + 类型提示（API 设计）。 | MAJOR |
| RC-SP-003 | 数值例程包含单元/回归测试。 | MAJOR |
| RC-SP-004 | 可基准化的数值代码附带基准/计时测试。 | MINOR |
| RC-SP-005 | 公共 API 变更小而可文档化、可评审。 | MINOR |
| RC-SP-006 | transformer 暴露 `transform` / `fit_transform`。 | MINOR |
| RC-SP-007 | 项目作为可安装包交付；CI 运行风格 + 类型检查。 | MINOR |

## 协同与交叉引用

- `RC-ENG-001`（每个公共符号有文档）与 `GP-DOC` / `PL-DOC` 重叠——应用最具体的代码
  （当关乎“保持文档同步”的过程时用 `RC-ENG-*`；当关乎机械存在性时用 `GP-DOC`/`PL-DOC`）。
- `RC-ENG-003`（测试）强化 `pytest tests/` 质量门。
- `RC-ENG-002`/`RC-SP-005` 是过程侧与习惯侧同一“小而可评审、有文档的变更”思想。
- `RC-SP-007`（可安装包 + CI 风格/类型）是让 `RC-ENG-*` 在实践中可评审的原因——
  CI 运行 black/isort/ruff/mypy/pytest，风格不靠人手争。
- 评审流与 `RC-VER-*`（被打 tag、基于分支的发布）相连。

## 权威链接

- SWE at Google（书）：https://abseil.io/resources/swe-book
- Google Eng Practices：https://google.github.io/eng-practices/
- Scientific Python Dev Guide：https://learn.scientific-python.org/development/
- sp-repo-review：https://github.com/scientific-python/repo-review
- cookie 模板：https://github.com/scientific-python/cookie
