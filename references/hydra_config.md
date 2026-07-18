# Reference: Hydra Configuration

Source of truth for *configuration* standards in research code.

## Principles
- Compose a hierarchical config from smaller config **groups**.
- Override any value from the **command line** (`key=value`).
- Keep configs in version control; experiments are just config overrides.

## Entrypoint pattern
```python
import hydra
from omegaconf import DictConfig

@hydra.main(version_base="1.3", config_path="../configs", config_name="train")
def main(cfg: DictConfig) -> None:
    ...
```

## Config structure
- Each YAML is either a **defaults list** (`@package _group_`, `_target_` +
  params) or a **group member** (e.g. `configs/model/mnist.yaml`).
- Use `_target_` to point at a callable/class; instantiate via
  `hydra.utils.instantiate(cfg.x)`.
- Paths resolved from `configs/paths/default.yaml` + `rootutils.setup_root`,
  so runs are location-independent.

## Groups (from Lightning-Hydra-Template)
`callbacks/`, `data/`, `debug/`, `experiment/`, `extras/`, `hparams_search/`,
`hydra/`, `local/`, `logger/`, `model/`, `paths/`, `trainer/`.

## Best practices
- No hardcoded absolute paths.
- `configs/experiment/*.yaml` version-controls hyperparameter sweeps.
- `configs/debug/*.yaml` for fast dev runs (limit batches, overfit, profiler).
- Use `python src/train.py --help` to inspect the composed config.
- Don't mutate `cfg` in place unexpectedly; prefer structured configs (dataclasses).
