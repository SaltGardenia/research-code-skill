# Reference: PyTorch Lightning Style Guide

Goal: improve **readability** and **reproducibility** — any `LightningModule`
should be structured the same way across repos.

## LightningModule

### Systems vs Models
- A **model** is a backbone (resnet18, RNN, ...).
- A **system** defines how models interact + training/eval logic (GAN, Seq2Seq, BERT).
- Keep the model separate from the system for modularity, testability, refactorability.

### Self-contained
- "Can someone drop this file into a Trainer without knowing internals?"
- Couple the optimizer + scheduler with the model in `configure_optimizers`.

### Init clarity
- Define sensible typed defaults in `__init__`; never pass opaque `params` objects.
  - Bad: `def __init__(self, params): self.lr = params.lr`
  - Good: `def __init__(self, encoder: nn.Module, coef_x: float = 0.2, lr: float = 1e-3)`

### Method order
1. `__init__` (model/system definition)
2. `forward` (inference only)
3. `training_step` + `on_train_*_end`
4. `validation_step` + `on_validation_*_end`
5. `test_step` + `on_test_*_end`
6. `predict_step`
7. `configure_optimizers`
8. any extra hooks

Only required: `__init__`, `training_step`, `configure_optimizers`.

### forward vs training_step
- `forward()` = inference/predictions only.
- `training_step()` = training logic; should NOT depend on `forward()`.

## Data

### DataLoaders
- Tune `num_workers` for throughput.

### LightningDataModule
- Decouples data hooks from the `LightningModule` → dataset-agnostic models.
- Must document: which splits, sample counts per split, transforms used.

## Docstrings
- Every public method gets a docstring stating what it does and returns.
