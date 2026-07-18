# Reference: Project Scaffold & Python Grammar

Source of truth for **how a research repo is laid out** and **how the Python
inside it is written**. This single reference fuses three tightly-coupled
standards that are always invoked together whenever a file is created or placed:

- **Lightning-Hydra-Template** — the fixed *directory layout* and MLOps
  tooling (`LHT-*`, STRUCTURE).
- **Hydra configuration** — the *config system* that fills that layout with
  composable, overridable YAML (`HY-*`, CONFIG).
- **Google Python Style Guide** — the *grammar* every `.py` file obeys
  (naming, formatting, typing, docstrings) (`GP-*`, PYSTYLE).

These three are inseparable: a `configs/` directory is meaningless without
Hydra's composition rules, and Hydra `_target_` callables are meaningless
without Google-clean, typed Python. Apply them as one unit when scaffolding
(Scenario A) or placing any file (Scenario B). The `references/coordination.md`
registry shows exactly which `LHT-/HY-/GP-*` code owns each concern.

## 1. Directory layout (STRUCTURE — `LHT-*`)

```
configs/          <- Hydra configs grouped by concern
  callbacks/ data/ debug/ experiment/ extras/
  hparams_search/ hydra/ local/ logger/ model/ paths/ trainer/
  train.yaml eval.yaml            <- main configs (defaults lists)
data/             <- raw / processed data (git-ignored)
logs/             <- hydra + logger outputs, timestamped (git-ignored)
notebooks/        <- numbered, initials, short desc (1.0-jqp-explore.ipynb)
scripts/          <- shell scripts (Makefile targets call these)
src/
  data/ models/ utils/
  train.py eval.py                <- @hydra.main entrypoints
tests/            <- generic smoke tests (pytest)
.env.example      <- template for private env vars (copy to .env)
.gitignore
.pre-commit-config.yaml           <- formatting / lint / security hooks
.project-root                     <- marks project root for rootutils
environment.yaml / requirements.txt
pyproject.toml    <- pytest + coverage + tool config
setup.py          <- install project as package
Makefile          <- `make train/test/format/clean`
README.md
```

### Enforced layout rules (`LHT-*`)

| Code | Rule |
|------|------|
| LHT-01 | Entrypoints at `src/train.py`/`src/eval.py` use `@hydra.main` + configs |
| LHT-02 | `configs/` directory exists, grouped by concern |
| LHT-03 | Root ships `.pre-commit-config.yaml`, `pyproject.toml`/`setup.py`, `requirements.txt`, `.gitignore`, `.env.example`, `.project-root` |
| LHT-04 | `tests/` directory with at least one smoke test |
| LHT-05 | `src/` splits by role: `data/`, `models/`, `utils/` |
| LHT-06 | `data/`, `logs/`, `notebooks/` separated from source (git-ignored where appropriate) |
| LHT-07 | Experiments are configs under `configs/experiment/`, not code branches |
| LHT-BP | Best-practice signals (pre-commit, `.env`, metric `/`, torchmetrics, DVC, package install) present |
| LHT-TOOL | Linters/hooks configured (black/isort/flake8/interrogate) |

### Main ideas (rapid experimentation)

- **CLI overrides**: `python src/train.py trainer.max_epochs=20 model.optimizer.lr=1e-4`;
  add new keys with `+` (`python src/train.py +model.new_param="x"`).
- **Minimal boilerplate**: instantiate pipelines from config `_target_`
  (`hydra.utils.instantiate(cfg.model)`).
- **Main configs** (`configs/train.yaml`, `configs/eval.yaml`) set defaults via a
  `defaults:` list.
- **Experiment configs** (`configs/experiment/*.yaml`) version-control best
  hyperparameters by overriding the main config.
- **Logs**: every run writes a timestamped folder under `logs/<task_name>/runs`
  (or `/multiruns` for sweeps) containing `.hydra/`, `checkpoints/`, `csv/`, `wandb/`.
- **Hyperparameter search**: Optuna/Ax/Nevergrad via `configs/hparams_search/` +
  `python src/train.py -m hparams_search=...`.
- **Tests**: generic smoke tests verifying commands run without exceptions.
- **CI**: GitHub Actions for pytest + pre-commit.

### Best practices (`LHT-BP`)

- **Miniconda** per-project envs; **pre-commit** auto-formats on commit
  (`pre-commit install` → `pre-commit run -a`).
- **Private env vars in `.env`** (git-ignored); reference via `${oc.env:MY_VAR}`. Never commit secrets.
- **Name metrics with `/`** (`self.log("train/loss", ...)`) so loggers group them.
- **torchmetrics** for correct multi-GPU reduction; separate instance per step.
- **Version-control data/models with DVC** (`dvc add data/MNIST`).
- **Install as a package** (`pip install -e .`) so `from src...` works; else rely on `rootutils.setup_root`.
- **Keep local configs out of version control** (`configs/local/default.yaml`, `optional` + git-ignored).
- **Enforce tags** for experiments so runs are filterable in loggers.

### Tooling config (enforced by pre-commit) — `LHT-TOOL`

The template's `.pre-commit-config.yaml` runs, in order: pre-commit-hooks
(trailing-whitespace, end-of-file-fixer, check-docstring-first, check-yaml,
debug-statements, detect-private-key, check-executables-have-shebangs,
check-toml, check-case-conflict, check-added-large-files), **black** (`--line-length 99`),
**isort** (`--profile black`), **pyupgrade** (`--py38-plus`), **docformatter**,
**interrogate** (`--fail-under=80`), **flake8**, **bandit**, **prettier** (YAML),
**shellcheck**, **mdformat**, **codespell**, **nbstripout** + **nbqa**.

`pyproject.toml` configures pytest (`--strict-markers`, `slow` marker,
`--doctest-modules`) and coverage; `Makefile` exposes `train`, `test`,
`test-full`, `format`, `clean`, `sync`.

## 2. Configuration system (CONFIG — `HY-*`)

Principles: compose a hierarchical config from **groups**; override any value
from the **CLI** (`key=value`, add with `+key=value`); keep configs in version
control where *experiments are just config overrides*; never hardcode absolute
paths — resolve from `configs/paths/default.yaml`.

### Entrypoint pattern — `HY-ENTRY`

```python
import hydra
import rootutils
from omegaconf import DictConfig

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

@hydra.main(version_base="1.3", config_path="../configs", config_name="train")
def main(cfg: DictConfig) -> None:
    ...
```

- `setup_root` adds the project root to `PYTHONPATH`, sets `PROJECT_ROOT`, loads `.env` — location-independent.
- Guard with `if __name__ == "__main__": main()`.

### Config structure — `HY-STRUCT`

- Main config starts with a `defaults:` list whose **order defines override precedence** (later wins).
- Each YAML is either a **defaults list** (`@package _global_`) or a **group member**.
- Use `_target_` to point at a callable/class; instantiate via `hydra.utils.instantiate(cfg.x)`.
- Group member example:
  ```yaml
  _target_: src.models.components.MyModel
  lr: 1.0e-3
  optimizer: adam
  ```

### Config groups — `HY-GROUP`

`callbacks/`, `data/`, `debug/`, `experiment/`, `extras/`, `hparams_search/`,
`hydra/`, `local/`, `logger/`, `model/`, `paths/`, `trainer/`. The main config
composes them in order:
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
  - experiment: null      # version-control best hyperparameters
  - hparams_search: null  # hyperparameter search config
  - optional local: default # machine/user specific, git-ignored
  - debug: null           # fast dev runs
```

### Path resolution — `HY-PATH`

`configs/paths/default.yaml` resolves all filesystem roots so runs are location-independent:
```yaml
root_dir: ${oc.env:PROJECT_ROOT}
data_dir: ${paths.root_dir}/data/
log_dir: ${paths.root_dir}/logs/
output_dir: ${hydra:runtime.output_dir}
work_dir: ${hydra:runtime.cwd}
```
Use OmegaConf interpolation (`${...}`), not f-strings. `configs/hydra/default.yaml`
sets the dynamically generated output dir (`${paths.log_dir}/${task_name}/runs/${now:...}`).
Read env vars with `${oc.env:VAR}`.

### Experiments & sweeps — `HY-EXP` / `HY-SWEEP`

- `configs/experiment/*.yaml` override the main config to version-control best hyperparameters; run with `python src/train.py experiment=example`.
- `configs/hparams_search/*.yaml` define Optuna/Ax/Nevergrad sweeps; run with `python src/train.py -m hparams_search=mnist_optuna` (launch fn must `return` the optimized metric).
- `configs/debug/*.yaml` for fast dev (limit batches, overfit, profiler).

### Structured configs — `HY-STRUCTCFG`

Prefer `@dataclass` / `DictConfig` typed schemas over raw dicts so typos and missing keys fail early. Honored by `hydra.main` + `hydra.utils.instantiate`. Pairs with `GP-TYPE`/`GP-ANN`.

### Best practices — `HY-BEST`

- No hardcoded absolute paths; everything flows from `paths`.
- Don't mutate `cfg` in place unexpectedly; prefer structured configs.
- Inspect with `python src/train.py --cfg job`.
- `local/` configs are `optional` and git-ignored.
- Instantiate *every* object (data, model, trainer, callbacks, loggers) from the composed config — never construct imperatively in the entrypoint.

| Code | Meaning | Related code |
|------|---------|--------------|
| HY-ENTRY | `@hydra.main` + `setup_root` entrypoint | LHT-01 |
| HY-STRUCT | defaults list / `_target_` configs | PL-INST |
| HY-GROUP | config groups present & composed | LHT-02 |
| HY-PATH | interpolated, non-hardcoded paths | LHT-03 |
| HY-EXP | experiment configs version-controlled | LHT-07 |
| HY-SWEEP | hparams_search defined for sweeps | LHT-BP |
| HY-STRUCTCFG | structured/typed configs | GP-TYPE |
| HY-BEST | no hardcoded paths; instantiate all | all |

## 3. Python grammar (PYSTYLE — `GP-*`)

Project config (Black line length 99, from the template) overrides the Google
default (80) when present. Each rule maps to a `GP-*` code used by the skill's
`PYSTYLE` findings and `scripts/audit_style.py`.

### Language rules

| Code | Source | Rule |
|------|--------|------|
| GP-LINT | 2.1 | pylint config present; suppress with `# pylint: disable=` + reason |
| GP-IMP / GP-IMPFMT | 2.2 / 3.13 | absolute imports; grouped stdlib→third-party→local, no wildcard `*` |
| GP-PKG | 2.3 | full-path imports; no `sys.path` cwd reliance |
| GP-EXC | 2.4 | never bare `except:`; catch specific; `raise ... from e` |
| GP-GLOB | 2.5 | no mutable module globals (except `Final` constants) |
| GP-COMP/GP-GEN/GP-LAMBDA/GP-COND | 2.7–2.11 | sane comprehensions/lambdas/conditionals |
| GP-DEF | 2.12 | no mutable default args (`=None` then init) |
| GP-PROP/GP-GETSET | 2.13/3.15 | `@property` for cheap access only |
| GP-TRUE | 2.14 | truthiness (`if foo:`, not `== True`) |
| GP-SCOPE/GP-DECO/GP-THREAD/GP-POWER/GP-FUTURE/GP-TYPE | 2.16–2.21 | advanced language rules (lexical scoping, decorators, threading, power features, `__future__`, typing) |
| GP-RES | 3.11 | context managers for files/sockets (`with`) |

### Style rules

| Code | Source | Rule |
|------|--------|------|
| GP-SEMI | 3.1 | no semicolons; one statement per line |
| GP-LEN | 3.2 | ≤80 (Google) / ≤99 (project Black) |
| GP-PAREN | 3.3 | parentheses sparingly |
| GP-INDENT | 3.4 | 4 spaces, no tabs; continuation aligns |
| GP-BLANK | 3.5 | 2 blank lines between top-level, 1 between methods |
| GP-WS | 3.6 | PEP8 spacing; no trailing whitespace |
| GP-SHEBANG | 3.7 | `#!/usr/bin/env python3` on executables only |
| GP-DOC | 3.8 | docstrings on every public module/func/class/method (PEP 257) |
| GP-STR | 3.10 | `"` consistent; f-strings; `logging` not `print` |
| GP-TODO | 3.12 | `TODO(username): what and why` |
| GP-NAME | 3.16 | `lower_snake_case` / `CapWords` / `UPPER_CASE`; no `l`/`I`/`O` singles |
| GP-MAIN | 3.17 | `if __name__ == "__main__":` guard |
| GP-FLEN | 3.18 | keep functions short; extract helpers |
| GP-ANN | 3.19 | annotate all signatures; `Sequence`/`Mapping` for inputs |

### Notes that bind the three layers

- The template's tooling (`LHT-TOOL`) *implements* the `GP-*` rules via black/isort/flake8;
  project line length (99) overrides Google default (80) — read `pyproject.toml` for the override (`GP-LEN`).
- `HY-STRUCTCFG` reinforces `GP-TYPE`/`GP-ANN`: untyped `instantiate` targets and untyped `__init__` are linked findings.
- `GP-NAME` governs config keys and `src/` module names alike; `LHT-05` expects `src/data`, `src/models`, `src/utils`.
