# 参考：模型与组件设计（中文版 · 供开发者阅读）

> 本文件是 `references/model_design.md` 的中文对照版。智能体运行时仍应加载英文原版。

本参考是科研代码中 **模型及其组成部分如何结构化** 的事实来源。它把三个都在回答同一问题——
*“一个形态良好的模型长什么样？”*——的标准，在三个抽象层级上融合：

- **PyTorch Lightning Style Guide** —— 每个模型/系统遵守的*契约*
  （`LightningModule` 形态、方法顺序、指标）。`PL-*` 代码。
- **timm 模型架构风格** —— 视觉模型的*具体形态*：命名架构、
  `models/{layers,blocks,architectures}` 分层。`RC-TIMM-*`。
- **OpenMMLab 工程标准** —— 让组件按配置而非 `if` 阶梯选择的*可插拔*模式：
  Registry + `build_from_cfg`。`RC-OPENMMLAB-*`。

它们化合：Lightning 契约说“把模型与系统分离”；timm 展示这个被分离的模型应该长什么样；
OpenMMLab 展示如何让它能从配置中被选择。在你写或重构一个模型、骨干或可注册组件时把它们一起应用。

## 1. Lightning 契约（LIGHTNING —— `PL-*`）

### 系统 vs 模型 —— `PL-SYS`

- **模型**是骨干（resnet18、RNN、ViT）：纯 `nn.Module`，不含训练逻辑。
- **系统**定义模型如何交互 + 训练/评估逻辑。它是把模型、优化器、step 串起来的 `LightningModule`。
- 为了模块化、可测、可重构，把模型与系统分离。模板分别实例化骨干
  （`configs/model/<project>.yaml` → `src/models/components/<Project>Model`）并喂给
  `LightningModule`（`src/models/<project>_module.py`）。

### 自包含 —— `PL-SELF`

- “有人能否在不了解内部的情况下把这个文件丢进 `Trainer`？”
- 在 `configure_optimizers` 中把优化器 + 调度器与模型耦合。
- 保存 init 参数使其写入 checkpoint 并可经 `self.hparams` 访问——
  调用 `self.save_hyperparameters(logger=False)` 并传入 `net`/`optimizer`/`scheduler`
  作为被 Hydra 实例化的 `hparams`。见 `PL-HPARAM`。

### Init 清晰 —— `PL-INIT`

- 在 `__init__` 中定义合理的带类型默认值；绝不传入不透明的 `params` 对象。
  - 坏：`def __init__(self, params): self.lr = params.lr`
  - 好：`def __init__(self, net: nn.Module, optimizer: ..., scheduler: ..., compile: bool = False)`
- 让 `__init__` 免于重活；用 `setup()` 做动态构建。
- 注解每个参数；在 docstring（`:param x:`）中记录。与 `GP-ANN`/`GP-NAME` 配对。

### 方法顺序 —— `PL-ORDER`

在每个 `LightningModule` 中保持此顺序：

1. `__init__`（模型/系统定义 + `save_hyperparameters`）
2. `forward`（仅推理）
3. `training_step`（+ `on_training_*_end`、`model_step` 辅助）
4. `validation_step`（+ `on_validation_*_end`）
5. `test_step`（+ `on_test_*_end`）
6. `predict_step`
7. `setup`（按 stage；做 DDP 感知构建的安全之处）
8. `configure_optimizers`
9. 任何额外钩子（`on_train_start`、`on_*_epoch_end`、`configure_*`）

仅必需：`__init__`、`training_step`、`configure_optimizers`。

### forward vs training_step —— `PL-FWD`

- `forward()` = 仅推理/预测（被 `torch.compile`、`torch.export`、serving 使用）。绝不能依赖 `training_step`。
- `training_step()` = 训练逻辑；计算 loss、调用 `forward`、记录日志。
- 抽取一个共享的 `model_step(batch)` 辅助，由 `training_step`/`validation_step`/`test_step` 调用。

### 数据 —— `PL-DL` / `PL-DM`

- 调优 `num_workers` 提升吞吐（配置 `configs/data/<project>.yaml`）；pin memory；
  重负载用 `persistent_workers=True`。
- `LightningDataModule` 把数据钩子与 `LightningModule` 解耦 → 数据集无关的模型。
  必须在 docstring 中记录切分、样本数、transforms。切分：`prepare_data`（下载，一次，无 rank）、
  `setup`（赋给 self，按 rank）、`train/test/predict_dataloader`。
  经 `_target_` 从配置实例化（`PL-INST`）。

### 指标与日志 —— `PL-METRIC`

- 用 **torchmetrics** 而非手写的 accuracy/loss——多 GPU 下正确。每个 step 用独立实例
  （`train_acc`、`val_acc`、`test_acc`）。
- 用 `/` 命名：`self.log("train/loss", ...)`、`"val/acc"`、`"test/acc_best"`。
- 显式 `on_step`/`on_epoch`：`self.log("train/loss", self.train_loss, on_step=False, on_epoch=True, prog_bar=True)`。
- 最佳跟踪：在 `on_validation_epoch_end` 中
  `self.log("val/acc_best", self.val_acc_best.compute(), sync_dist=True, prog_bar=True)`。
- 在正确边界重置指标（`on_train_start` 重置 val 指标）。

### 分布式注意 —— `PL-DDP`

- `setup(stage)` 在 DDP 的每个进程上运行——在那里构建 rank 本地的模型，而非 `__init__`。
- 记录跨 rank 聚合的指标时传入 `sync_dist=True`。

### configure_optimizers —— `PL-OPT`

- 必须存在（缺失即 BLOCKER）。返回 `Optimizer`、列表或字典：
  ```python
  return {"optimizer": optimizer,
          "lr_scheduler": {"scheduler": scheduler,
                           "monitor": "val/loss",
                           "interval": "epoch", "frequency": 1}}
  ```
- 从 `self.hparams`（由 Hydra 实例化）构建：`optimizer = self.hparams.optimizer(params=self.parameters())`。

### Docstring —— `PL-DOC`

- 每个公共方法带 docstring（`:param x:` / `:return:`）。类 docstring 列出关键方法。
  与 `GP-DOC` / `RC-SP-002` / `RC-ENG-001/007` 配对。

| 代码 | 含义 | 相关代码 |
|------|------|----------|
| PL-SYS | 模型/系统分离 | LHT-05（src 拆分） |
| PL-SELF | 自包含，优化器在 configure_optimizers | - |
| PL-INIT | 带类型、显式的 init；无不透明 params | GP-ANN/GP-NAME |
| PL-ORDER | 方法顺序保持 | - |
| PL-FWD | forward ≠ training_step | - |
| PL-DL | 调优的 DataLoader workers | - |
| PL-DM | LightningDataModule 有文档 | HY-STRUCT（PL-INST） |
| PL-METRIC | torchmetrics、`/`-命名、sync_dist | LHT-BP |
| PL-DDP | DDP 感知的 setup/build | - |
| PL-OPT | configure_optimizers 存在且形式良好 | - |
| PL-HPARAM | 为 ckpt 保存 save_hyperparameters | LHT-BP |
| PL-INST | 从配置 `_target_` 实例化 | HY-STRUCT |
| PL-DOC | 公共方法 docstring | GP-DOC |

## 2. timm 架构形态（TIMM —— `RC-TIMM-*`）

timm 把**通用辅助件**（layers、blocks）与**命名架构**（具体的 `VisionTransformer`、`ResNet`……）
分开。一个模型文件恰好定义一个命名良好的架构类——绝不一个包揽一切的 `MyModel`。
类名*就是*架构；它由 registry 与工厂引用，而非脚本中的字符串分支。

**禁止**——通用、无内容的名字：
```python
class MyModel(nn.Module):          # 禁止
    ...
```
**要求**——显式命名架构：
```python
class VisionTransformer(nn.Module):  # 要求
    ...
```

### 模块布局 `models/`

```
models/
├── layers/          # 低层可复用算子（attention、drop_path、mlp、patch embed）
├── blocks/          # 由 layers 组合的块（attention block、FFN block）
└── architectures/   # 具体命名模型（VisionTransformer、DynamicViT……）
```
新的 ViT 变体（Dynamic ViT、Sparse Transformer）属于 `architectures/`
并复用 `layers/` + `blocks/`——而非一个带着自己一份 attention 代码的庞大新文件。

| 代码 | 规则 | 严重度 |
|------|------|--------|
| RC-TIMM-001 | 模型类以架构命名（如 `VisionTransformer`），而非泛化的 `MyModel`。 | MAJOR |
| RC-TIMM-002 | 通用算子位于 `models/layers/`；组合位于 `models/blocks/`；命名模型位于 `models/architectures/`。 | MAJOR |
| RC-TIMM-003 | 新的 vision-transformer 变体复用既有 `layers/`+`blocks/`；不重复 attention/FFN 代码。 | MINOR |
| RC-TIMM-004 | 架构经模型工厂注册/导出，而非经字符串 `if model == "vit"` 引用。 | MAJOR |

## 3. OpenMMLab 可插拔（OPENMMLAB —— `RC-OPENMMLAB-*`）

OpenMMLab 的组件（模型、骨干、数据集、调度器）用装饰器声明，并从配置 dict 构建——
绝不通过字符串 `if/elif` 阶梯选择。

**要求**——注册，再从配置构建：
```python
from mmcv.utils import Registry
MODELS = Registry('models')

@MODELS.register_module()
class TDSViT:
    ...
```
```python
model = MODELS.build(cfg['model'])   # == build_from_cfg(cfg['model'], MODELS)
```
**禁止**——破坏可插拔性的字符串分支：
```python
if model == "vit":
    build_vit()
elif model == "tdst":
    build_tdsvit()
else:
    build_resnet()
```

此模式（1）让添加 `TDSViT` 只需一行 `@register_module()`，而非新 `elif`；
（2）让实验配置选择组件，而代码保持通用（`build_from_cfg(cfg)`）；
（3）为“存在哪些组件”提供单一事实来源。它是 `PL-SYS`（配置选择模型）的具体实现，
也是让 `RC-HYDRA-*` 配置真正实例化对象的适配器。

| 代码 | 规则 | 严重度 |
|------|------|--------|
| RC-OPENMMLAB-001 | 可插拔组件被注册（`@X.register_module()`），而非经字符串 `if model == "..."` 选择。 | MAJOR |
| RC-OPENMMLAB-002 | 组件经 `build_from_cfg(cfg)` / `Registry.build(cfg)` 实例化，而非手工分支构建。 | MAJOR |
| RC-OPENMMLAB-003 | 新增组件只需一次注册 + 一条配置项，无需编辑中央 `if/elif` 阶梯。 | MINOR |

## 协同小结

- `PL-SYS`（模型与系统分离）是*为什么*；`RC-TIMM-002`（layers/blocks/architectures）是被分离模型的*怎么做*；
  `RC-OPENMMLAB-*` 是*怎么选择它*。
- `RC-TIMM-004`（无字符串模型选择）与 `RC-OPENMMLAB-001`（注册而非分支）是同一规则在两个层级上的体现。
- `PL-INST`（`_target_`）与 `RC-OPENMMLAB-002`（`build_from_cfg`）都说：从配置实例化，绝不命令式——
  OpenMMLab Registry 是在非 Hydra 代码库中满足 `PL-INST` 的一种方式。
