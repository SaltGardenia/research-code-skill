# 参考：实验可复现性（中文版 · 供开发者阅读）

> 本文件是 `references/experiment_repro.md` 的中文对照版。智能体运行时仍应加载英文原版。

本参考是 **让一次运行可重新生成** 的事实来源。四个标准在此汇聚，因为只有当四件事对齐时结果才可被复现——
其中任一处断裂都会破坏整条链：

- **Hydra 配置优先**（`hydra_rules`）——每个*实验变量*都存在于配置中，从 `cfg` 读取。`RC-HYDRA-*`。
- **FAIR 数据原则**（`data_management`）——运行所消费的*数据*被标识、版本化、可加载。`RC-DATA-*`。
- **Semantic Versioning + Git Flow**（`version_control`）——运行所用*代码*被打 tag、走分支。`RC-VER-*`。
- **Meta Research 仓库理念**（`meta_research`）——*实验本身*可复现/可配置/有文档/可基准化，
  表达为配置变体，而非 `train_v2_final.py`。`RC-META-*`。

把它们读作一条链：**配置（HYDRA）选择 → 数据（FAIR）被固定 → 代码（VER）被打 tag → 实验（META）是一个命名变体**。
每当你收尾、版本化或整理一个实验时，应用全部四个。

## 1. 配置优先（HYDRA-CFG —— `RC-HYDRA-*`）

**任何实验变量必须存在于配置中。** 一次训练运行完全由其组合配置（defaults 树 + 覆盖）描述；
代码从 `cfg` 读取值，而非凭空发明。

**禁止**——硬编码实验值：
```python
def train():
    lr = 0.001            # 禁止
    ...
```
**要求**——变量位于配置中，从 `cfg` 读取：
```yaml
# conf/optimizer.yaml
optimizer:
  lr: 0.001
```
```python
def train(cfg):
    lr = cfg.optimizer.lr     # 要求
    ...
```
batch size、seed、模型深度、数据集路径、调度器亦然——凡是 sweep 会触碰的旋钮。
运行时用 `python train.py optimizer.lr=0.0005` 覆盖，绝不要编辑字面量。

## 2. FAIR 数据（DATA —— `RC-DATA-*`）

一个科研代码库只有在数据可复现时才是可复现的。把数据集、checkpoint、产物当作一等、受治理的对象——
而非 `data/` 里的散落文件。提炼自 FAIR Guiding Principles（Wilkinson 等，*Scientific Data*，2016）。

**可发现（Findable）**——唯一持久标识符（VCS 下路径、DOI、内容哈希）+ 丰富元数据，可注册/可搜索。
**可访问（Accessible）**——经标准协议可检索（开放或鉴权）；即便数据退役，元数据仍可用。
**可互操作（Interoperable）**——标准、开放的格式与共享词汇，使其能与其他工具结合。
**可复用（Reusable）**——清晰许可证、来源、社区标准元数据。

每个数据集/产物都要求：一个**唯一标识符**；**元数据**（schema、来源、许可证）；固定到 git tag / DVC rev 的
**版本**；**加载说明**（一个 `LightningDataModule`、`get_dataset()` 或 DVC pull）；以及**每次运行记录的确切数据版本**
（配置 + tag），以便结果重生。

## 3. 版本化与 Git Flow（VERSION —— `RC-VER-*`）

提炼自 Semantic Versioning 2.0.0 与 Git Flow（Vincent Driessen）。版本 = `MAJOR.MINOR.PATCH`：
- `MAJOR` 破坏性/不兼容（如 `1.0.0` 论文发布）
- `MINOR` 新的向后兼容功能（`0.2.0` 新算法）
- `PATCH` 向后兼容修复（`0.1.1` 数据加载器修复）

允许预发布（`1.0.0-rc.1`）与构建元数据（`1.0.0+build.5`）扩展。每次实验发布**必须映射到 git tag**，
以便确切的代码 + 配置可检索。

分支：`main`（被打 tag 的稳定版）、`develop`（集成）、`feature/*`、`release/*`、`hotfix/*`。
科研友好的变体：`main` 配 `experiment/v1`、`feature/new-model`、`fix/data-loader`。
注意：Git Flow 适合版本化产物（论文、已发布库），而非持续交付的 Web 应用。

## 4. Meta Research 理念（META —— `RC-META-*`）

每个实验都应**可复现**（固定 seed + 固定数据 + 记录配置）、**可配置**（旋钮在配置中，而非脚本）、
**有文档**（如何运行 + 含义）、**可基准化**（清晰可比较的指标，而非 notebook 里的一个数）。

**禁止**暗示漂移的版本化/final 文件名：`train_v2_final.py`、`model_new.py`、`exp_copy.py`、
`test_old.py`、`run_FIXED.py`。**允许**意图清晰的、配置驱动的入口：`trainer.py`/`train.py` +
`configs/experiment/<name>.yaml`。若忍不住想写 `train_v2_final.py`，保留 `train.py` 并把变体表达为实验配置。

## Rule Card（机器可执行）

| 代码 | 规则 | 严重度 |
|------|------|--------|
| RC-HYDRA-001 | 每个实验变量（lr、batch、seed、深度、路径、调度器）都存在于配置中并从 `cfg` 读取。 | MAJOR |
| RC-HYDRA-002 | 代码中无硬编码实验字面量（如 `lr = 0.001`）；经 CLI/配置覆盖。 | MAJOR |
| RC-HYDRA-003 | 实验仅通过配置覆盖区分，而非通过被编辑的代码字面量。 | MINOR |
| RC-DATA-001 | 每个数据集/产物都有元数据（schema、来源、许可证）。 | MAJOR |
| RC-DATA-002 | 每个数据集/产物都有唯一的、可解析的标识符。 | MAJOR |
| RC-DATA-003 | 每个数据集声明一个固定到 git tag / DVC rev 的版本。 | MAJOR |
| RC-DATA-004 | 每个数据集都随附加载说明（可运行的加载器）。 | MAJOR |
| RC-DATA-005 | 每次实验运行都记录所用的确切数据版本。 | BLOCKER |
| RC-DATA-006 | 数据格式/序列化是开放且标准的。 | MINOR |
| RC-VER-001 | 每次实验发布映射到 git tag（`vMAJOR.MINOR.PATCH`）。 | MAJOR |
| RC-VER-002 | 版本遵循 SemVer `MAJOR.MINOR.PATCH`（+ 可选预发布）。 | MAJOR |
| RC-VER-003 | `main` 只持有被打 tag 的稳定发布。 | MAJOR |
| RC-VER-004 | 新工作位于 `feature/*` / `experiment/*`，而非直接在 `main`。 | MINOR |
| RC-VER-005 | `release/*` 准备每个 MINOR/MAJOR；`hotfix/*` 用于 PATCH。 | MINOR |
| RC-VER-006 | 打 tag 发布前先升版本（不静默发布）。 | MINOR |
| RC-META-001 | 每个实验都可复现（seed + 固定数据 + 记录配置）。 | MAJOR |
| RC-META-002 | 旋钮位于配置中，而非硬编码在脚本里。 | MAJOR |
| RC-META-003 | 每个实验都有文档（如何运行 + 含义）。 | MAJOR |
| RC-META-004 | 每个实验瞄准清晰、可比较的基准/指标。 | MINOR |
| RC-META-005 | 禁止文件名模式 `*_v<N>_*final*.py` / `*_new.py` / `*_copy.py` / `*_old.py`；
  使用 `train.py` + 实验配置。 | MAJOR |
| RC-META-006 | 入口是 `trainer.py`/`train.py`；变体是 `configs/experiment/*.yaml`，而非新脚本。 | MINOR |

## 如何应用这条链

- **搭建（A）**：从一开始写 `train.py` + `configs/experiment/`；`data/` 配 `data/README.md`
  （或 `.dvc.yaml`）描述每个资产；初始化 `main` + `develop` 并记录分支模型。
- **整理（B）**：把硬编码字面量提升为配置（`RC-HYDRA-*`）；重命名 `train_v2_final.py` →
  把其 diff 折进 `train.py` + 一个实验配置（`RC-META-005/006`）；固定数据版本（`RC-DATA-003/005`）；
  给结果打 tag（`RC-VER-001`）。
- **闭环**：打 tag（`RC-VER-001`）固定数据版本（`RC-DATA-003`）与所用配置（`HY-EXP`）；
  `RC-ENG-004`（合并前评审）收尾。结果从一个 tag 重生。

## 权威链接

- Hydra: https://hydra.cc/ · FAIR: https://www.go-fair.org/fair-principles/
- SemVer: https://semver.org/ · Git Flow: https://nvie.com/posts/a-successful-git-branching-model/
- Meta Research: https://github.com/facebookresearch
- FAIR 论文：Wilkinson 等，*Scientific Data*（2016），https://doi.org/10.1038/sdata.2016.18
