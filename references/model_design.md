# Reference: Model & Component Design

Source of truth for **how models and their parts are structured** in research
code. This single reference fuses three standards that all answer one question —
*"what does a well-shaped model look like?"* — at three levels of abstraction:

- **PyTorch Lightning Style Guide** — the *contract* every model/system obeys
  (`LightningModule` shape, method order, metrics). `PL-*` codes.
- **timm Model Architecture Style** — the *concrete shape* of a vision model:
  named architecture, `models/{layers,blocks,architectures}` tiers. `RC-TIMM-*`.
- **OpenMMLab Engineering Standard** — the *pluggability* pattern that lets
  components be selected by config instead of `if` ladders: Registry +
  `build_from_cfg`. `RC-OPENMMLAB-*`.

They compound: the Lightning contract says "separate model from system"; timm
shows what that separated model should look like; OpenMMLab shows how to make
it selectable from config. Apply them together whenever you write or restructure
a model, a backbone, or a registerable component.

## 1. Lightning contract (LIGHTNING — `PL-*`)

### Systems vs Models — `PL-SYS`

- A **model** is a backbone (resnet18, RNN, ViT): pure `nn.Module`, no training logic.
- A **system** defines how models interact + training/eval logic. It is the
  `LightningModule` that wires models, optimizers, and steps.
- Keep the model separate from the system for modularity, testability, refactorability.
  The template instantiates the backbone separately (`configs/model/<project>.yaml`
  → `src/models/components/<Project>Model`) and feeds it into the `LightningModule`
  (`src/models/<project>_module.py`).

### Self-contained — `PL-SELF`

- "Can someone drop this file into a `Trainer` without knowing internals?"
- Couple the optimizer + scheduler with the model in `configure_optimizers`.
- Store init params so they are saved to the checkpoint and accessible as
  `self.hparams` — call `self.save_hyperparameters(logger=False)` and pass
  `net`/`optimizer`/`scheduler` as `hparams` (instantiated by Hydra). See `PL-HPARAM`.

### Init clarity — `PL-INIT`

- Define sensible typed defaults in `__init__`; never pass opaque `params` objects.
  - Bad: `def __init__(self, params): self.lr = params.lr`
  - Good: `def __init__(self, net: nn.Module, optimizer: ..., scheduler: ..., compile: bool = False)`
- Keep `__init__` free of heavy work; use `setup()` for dynamic building.
- Annotate every argument; document each in the docstring (`:param x:`). Pairs with `GP-ANN`/`GP-NAME`.

### Method order — `PL-ORDER`

Preserve this order in every `LightningModule`:
1. `__init__` (model/system definition + `save_hyperparameters`)
2. `forward` (inference only)
3. `training_step` (+ `on_training_*_end`, `model_step` helper)
4. `validation_step` (+ `on_validation_*_end`)
5. `test_step` (+ `on_test_*_end`)
6. `predict_step`
7. `setup` (per stage; safe place for DDP-aware building)
8. `configure_optimizers`
9. any extra hooks (`on_train_start`, `on_*_epoch_end`, `configure_*`)
Only required: `__init__`, `training_step`, `configure_optimizers`.

### forward vs training_step — `PL-FWD`

- `forward()` = inference/predictions only (used by `torch.compile`, `torch.export`, serving). Must NOT depend on `training_step`.
- `training_step()` = training logic; computes loss, calls `forward`, logs.
- Factor a shared `model_step(batch)` helper called by `training_step`/`validation_step`/`test_step`.

### Data — `PL-DL` / `PL-DM`

- Tune `num_workers` for throughput (config `configs/data/<project>.yaml`); pin memory; `persistent_workers=True` for heavy setups.
- `LightningDataModule` decouples data hooks from the `LightningModule` → dataset-agnostic models. Must document splits, sample counts, transforms (in docstrings). Split: `prepare_data` (download, once, no rank), `setup` (assign to self, per rank), `train/test/predict_dataloader`. Instantiated from config via `_target_` (`PL-INST`).

### Metrics & logging — `PL-METRIC`

- Use **torchmetrics**, not hand-rolled accuracy/loss — correct under multi-GPU. Separate instance per step (`train_acc`, `val_acc`, `test_acc`).
- Name with `/`: `self.log("train/loss", ...)`, `"val/acc"`, `"test/acc_best"`.
- Explicit `on_step`/`on_epoch`: `self.log("train/loss", self.train_loss, on_step=False, on_epoch=True, prog_bar=True)`.
- Best-tracking: `self.log("val/acc_best", self.val_acc_best.compute(), sync_dist=True, prog_bar=True)` in `on_validation_epoch_end`.
- Reset metrics at the right boundary (`on_train_start` resets val metrics).

### Distributed care — `PL-DDP`

- `setup(stage)` runs on every process in DDP — build rank-local models there, not `__init__`.
- Pass `sync_dist=True` when logging a metric that aggregates across ranks.

### configure_optimizers — `PL-OPT`

- Must exist (BLOCKER if missing). Return `Optimizer`, list, or dict:
  ```python
  return {"optimizer": optimizer,
          "lr_scheduler": {"scheduler": scheduler,
                           "monitor": "val/loss",
                           "interval": "epoch", "frequency": 1}}
  ```
- Build from `self.hparams` (instantiated by Hydra): `optimizer = self.hparams.optimizer(params=self.parameters())`.

### Docstrings — `PL-DOC`

- Every public method gets a docstring (`:param x:` / `:return:`). Class docstring lists the key methods. Pairs with `GP-DOC` / `RC-SP-002` / `RC-ENG-001/007`.

| Code | Meaning | Related code |
|------|---------|--------------|
| PL-SYS | model/system separation | LHT-05 (src split) |
| PL-SELF | self-contained, optimizer in configure_optimizers | - |
| PL-INIT | typed, explicit init; no opaque params | GP-ANN/GP-NAME |
| PL-ORDER | method order preserved | - |
| PL-FWD | forward != training_step | - |
| PL-DL | tuned DataLoader workers | - |
| PL-DM | LightningDataModule documented | HY-STRUCT (PL-INST) |
| PL-METRIC | torchmetrics, `/`-named, sync_dist | LHT-BP |
| PL-DDP | DDP-aware setup/build | - |
| PL-OPT | configure_optimizers present & well-formed | - |
| PL-HPARAM | save_hyperparameters for ckpt | LHT-BP |
| PL-INST | `_target_` instantiation from config | HY-STRUCT |
| PL-DOC | docstrings on public methods | GP-DOC |

## 2. timm architecture shape (TIMM — `RC-TIMM-*`)

timm keeps **generic helpers** (layers, blocks) separate from **named
architectures** (the concrete `VisionTransformer`, `ResNet`, ...). A model file
defines exactly one well-named architecture class — never a catch-all `MyModel`.
The class name *is* the architecture; it is referenced by registry and factory,
not by a string branch in a script.

**Forbidden** — generic, content-free names:
```python
class MyModel(nn.Module):          # forbidden
    ...
```
**Required** — name the architecture explicitly:
```python
class VisionTransformer(nn.Module):  # required
    ...
```

### Module layout `models/`

```
models/
├── layers/          # low-level reusable ops (attention, drop_path, mlp, patch embed)
├── blocks/          # composed blocks built from layers (attention block, FFN block)
└── architectures/   # concrete named models (VisionTransformer, DynamicViT, ...)
```
New ViT variants (Dynamic ViT, Sparse Transformer) belong in `architectures/`
and reuse `layers/` + `blocks/` — not a monolithic new file with its own copy
of the attention code.

| Code | Rule | Severity |
|------|------|----------|
| RC-TIMM-001 | Model class named after the architecture (e.g. `VisionTransformer`), not a generic `MyModel`. | MAJOR |
| RC-TIMM-002 | Generic ops in `models/layers/`; compositions in `models/blocks/`; named models in `models/architectures/`. | MAJOR |
| RC-TIMM-003 | New vision-transformer variants reuse existing `layers/`+`blocks/`; no duplicated attention/FFN code. | MINOR |
| RC-TIMM-004 | Architecture registered/exported via the model factory, not referenced by string `if model == "vit"`. | MAJOR |

## 3. OpenMMLab pluggability (OPENMMLAB — `RC-OPENMMLAB-*`)

OpenMMLab components (models, backbones, datasets, schedulers) are declared with
a decorator and built from a config dict — never selected by a string `if/elif`
ladder.

**Required** — register, then build from config:
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
**Forbidden** — string branching that defeats pluggability:
```python
if model == "vit":
    build_vit()
elif model == "tdst":
    build_tdsvit()
else:
    build_resnet()
```

This pattern (1) makes adding `TDSViT` one `@register_module()` line, not a
new `elif`; (2) lets the experiment config select the component while code stays
generic (`build_from_cfg(cfg)`); (3) gives a single source of truth for "what
components exist". It is the concrete realization of `PL-SYS` (config selects the
model) and the adapter that makes `RC-HYDRA-*` configs actually instantiate
objects.

| Code | Rule | Severity |
|------|------|----------|
| RC-OPENMMLAB-001 | Pluggable components registered (`@X.register_module()`), not selected by string `if model == "..."`. | MAJOR |
| RC-OPENMMLAB-002 | Components instantiated via `build_from_cfg(cfg)` / `Registry.build(cfg)`, not hand-built branches. | MAJOR |
| RC-OPENMMLAB-003 | Adding a component requires only a registration + config entry, not edits to a central `if/elif` ladder. | MINOR |

## Synergy summary

- `PL-SYS` (separate model from system) is the *why*; `RC-TIMM-002` (layers/blocks/architectures) is the *how* for the separated model; `RC-OPENMMLAB-*` is the *how to select it*.
- `RC-TIMM-004` (no string model selection) and `RC-OPENMMLAB-001` (register, don't branch) are the same rule at two layers.
- `PL-INST` (`_target_`) and `RC-OPENMMLAB-002` (`build_from_cfg`) both say: instantiate from config, never imperatively — the OpenMMLab Registry is one way to satisfy `PL-INST` inside a non-Hydra codebase.
