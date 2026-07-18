# Reference: Experiment Reproducibility

Source of truth for **making a run regenerable**. Four standards converge
here because a result is reproducible only when four things align — and a breach
in any one breaks the whole chain:

- **Hydra Config-First** (`hydra_rules`) — every *experimental variable*
  lives in config, read from `cfg`. `RC-HYDRA-*`.
- **FAIR Data Principles** (`data_management`) — the *data* the run consumes
  is identified, versioned, loadable. `RC-DATA-*`.
- **Semantic Versioning + Git Flow** (`version_control`) — the *code* the run
  uses is tagged and branched. `RC-VER-*`.
- **Meta Research repo philosophy** (`meta_research`) — the *experiment itself*
  is reproducible/configurable/documented/benchmarkable, expressed as config
  variants, never `train_v2_final.py`. `RC-META-*`.

Read them as one chain: **config (HYDRA) selects → data (FAIR) is pinned →
code (VER) is tagged → experiment (META) is a named variant**. Apply all four
whenever you finish, version, or tidy an experiment.

## 1. Config-First (HYDRA-CFG — `RC-HYDRA-*`)

**Any experimental variable must exist in config.** A training run is described
entirely by its composed config (defaults tree + overrides); code reads values
from `cfg`, it does not invent them.

**Forbidden** — hardcoded experimental values:
```python
def train():
    lr = 0.001            # forbidden
    ...
```
**Required** — variable lives in config, read from `cfg`:
```yaml
# conf/optimizer.yaml
optimizer:
  lr: 0.001
```
```python
def train(cfg):
    lr = cfg.optimizer.lr     # required
    ...
```
Same for batch size, seed, model depth, dataset path, scheduler — every knob a
sweep would touch. Override at runtime with `python train.py optimizer.lr=0.0005`,
never by editing a literal.

## 2. FAIR data (DATA — `RC-DATA-*`)

A research codebase is only reproducible if its data is. Treat datasets,
checkpoints, and artifacts as first-class, governed objects — not loose files in
`data/`. Distilled from the FAIR Guiding Principles (Wilkinson et al., *Scientific
Data*, 2016).

**Findable** — unique persistent identifier (path under VCS, DOI, content hash) + rich metadata, registered/searchable.
**Accessible** — retrievable via a standard protocol (open or auth'd); metadata stays accessible even if data is retired.
**Interoperable** — standard, open formats and shared vocabularies so it combines with other tools.
**Reusable** — clear license, provenance, community-standard metadata.

Required for every dataset/artifact: a **unique identifier**; **metadata**
(schema, source, license); a **version** pinned to a git tag / DVC rev;
**loading instructions** (a `LightningDataModule`, `get_dataset()`, or DVC pull);
and the **exact data version recorded per run** (config + tag) so the result
regenerates.

## 3. Versioning & Git Flow (VERSION — `RC-VER-*`)

Distilled from Semantic Versioning 2.0.0 and Git Flow (Vincent Driessen).
Version = `MAJOR.MINOR.PATCH`:
- `MAJOR` breaking/incompatible (e.g. `1.0.0` paper release)
- `MINOR` new backward-compatible functionality (`0.2.0` new algorithm)
- `PATCH` backward-compatible fix (`0.1.1` data-loader fix)

Pre-release (`1.0.0-rc.1`) and build-metadata (`1.0.0+build.5`) extensions
allowed. Every experiment release **must map to a git tag** so the exact
code + config is retrievable.

Branches: `main` (tagged stable), `develop` (integration), `feature/*`,
`release/*`, `hotfix/*`. Research-friendly variant: `main` with
`experiment/v1`, `feature/new-model`, `fix/data-loader`. Caveat: Git Flow fits
versioned artifacts (paper, published lib), not continuously-delivered web apps.

## 4. Meta Research philosophy (META — `RC-META-*`)

Every experiment should be **reproducible** (fixed seed + pinned data + recorded
config), **configurable** (knobs in configs, not scripts), **documented** (how
to run + what it means), and **benchmarkable** (clear comparable metric, not a
notebook number).

**Forbidden** versioned/final filenames that signal drift: `train_v2_final.py`,
`model_new.py`, `exp_copy.py`, `test_old.py`, `run_FIXED.py`.
**Allowed** intent-revealing, config-driven entrypoints: `trainer.py`/`train.py`
+ `configs/experiment/<name>.yaml`. If tempted by `train_v2_final.py`, keep
`train.py` and express the variant as an experiment config.

## Rule cards (machine-executable)

| Code | Rule | Severity |
|------|------|----------|
| RC-HYDRA-001 | Every experimental variable (lr, batch, seed, depth, paths, scheduler) exists in config and is read from `cfg`. | MAJOR |
| RC-HYDRA-002 | No hardcoded experimental literals in code (e.g. `lr = 0.001`); override via CLI/config. | MAJOR |
| RC-HYDRA-003 | Experiments differ only by config overrides, not by edited code literals. | MINOR |
| RC-DATA-001 | Every dataset/artifact has metadata (schema, source, license). | MAJOR |
| RC-DATA-002 | Every dataset/artifact has a unique, resolvable identifier. | MAJOR |
| RC-DATA-003 | Every dataset declares a version pinned to a git tag / DVC rev. | MAJOR |
| RC-DATA-004 | Every dataset ships loading instructions (runnable loader). | MAJOR |
| RC-DATA-005 | Every experiment run records the exact data version used. | BLOCKER |
| RC-DATA-006 | Data formats/serialization are open & standard. | MINOR |
| RC-VER-001 | Every experiment release maps to a git tag (`vMAJOR.MINOR.PATCH`). | MAJOR |
| RC-VER-002 | Version follows SemVer `MAJOR.MINOR.PATCH` (+ optional pre-release). | MAJOR |
| RC-VER-003 | `main` holds only tagged, stable releases. | MAJOR |
| RC-VER-004 | New work lives on `feature/*` / `experiment/*`, not directly on `main`. | MINOR |
| RC-VER-005 | A `release/*` branch prepares each MINOR/MAJOR; `hotfix/*` for PATCH. | MINOR |
| RC-VER-006 | Bump the version before tagging a release (no silent releases). | MINOR |
| RC-META-001 | Every experiment is reproducible (seed + pinned data + recorded config). | MAJOR |
| RC-META-002 | Knobs live in configs, not hardcoded in scripts. | MAJOR |
| RC-META-003 | Every experiment is documented (how to run + what it means). | MAJOR |
| RC-META-004 | Every experiment targets a clear, comparable benchmark/metric. | MINOR |
| RC-META-005 | Forbidden filename pattern `*_v<N>_*final*.py` / `*_new.py` / `*_copy.py` / `*_old.py`; use `train.py` + experiment config. | MAJOR |
| RC-META-006 | Entrypoint is `trainer.py`/`train.py`; variants are `configs/experiment/*.yaml`, not new scripts. | MINOR |

## How to apply the chain

- **Scaffold (A)**: write `train.py` + `configs/experiment/` from the start;
  `data/` with a `data/README.md` (or `.dvc.yaml`) describing each asset;
  initialize `main` + `develop` and document the branch model.
- **Tidy (B)**: lift hardcoded literals into config (`RC-HYDRA-*`); rename
  `train_v2_final.py` → fold its diff into `train.py` + an experiment config
  (`RC-META-005/006`); pin data versions (`RC-DATA-003/005`); tag the result
  (`RC-VER-001`).
- **Close the loop**: tagging (`RC-VER-001`) pins the data version
  (`RC-DATA-003`) and the config used (`HY-EXP`); `RC-ENG-004` (review before
  merge) seals it. A result regenerates from a single tag.

## Authoritative links

- Hydra: https://hydra.cc/  ·  FAIR: https://www.go-fair.org/fair-principles/
- SemVer: https://semver.org/  ·  Git Flow: https://nvie.com/posts/a-successful-git-branching-model/
- Meta Research: https://github.com/facebookresearch
- FAIR paper: Wilkinson et al., *Scientific Data* (2016), https://doi.org/10.1038/sdata.2016.18
