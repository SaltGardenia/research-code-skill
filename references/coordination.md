# Reference Coordination: how the sources work together

This skill is a **coding-standard layer** distilled from authoritative references
plus a coordination layer. The references are **not independent checklists** —
they reinforce the same pipeline at different layers and, crucially, they
**compound into four usage clusters** (not thirteen separate files). Each
cluster is one coherent concern the agent reaches for, fusing standards that
answer the same question at different levels of abstraction. This file is the
single coordination point; load it when you need to resolve cross-cutting rules
or map a convention to its origin.

## The four clusters (fused sources)

```
1. SCAFFOLD & GRAMMAR   (scaffold_grammar.md)
   Lightning-Hydra-Template  -> directory layout every file lives in   (LHT-*)
   Hydra config              -> the config system that fills it          (HY-*)
   Google Python Style       -> the grammar every .py file obeys       (GP-*)
   Invoked together whenever a file is created or placed.

2. MODEL & COMPONENT      (model_design.md)
   PyTorch Lightning Style   -> the model/system contract                (PL-*)
   timm architecture        -> the concrete named-architecture shape    (RC-TIMM-*)
   OpenMMLab Registry       -> pluggability: select by config, not if  (RC-OPENMMLAB-*)
   Invoked together whenever a model/backbone/component is written.

3. EXPERIMENT REPRO       (experiment_repro.md)
   Hydra Config-First      -> every experimental variable lives in cfg  (RC-HYDRA-*)
   FAIR data               -> the data the run consumes is pinned       (RC-DATA-*)
   SemVer + Git Flow       -> the code the run uses is tagged          (RC-VER-*)
   Meta Research philosophy -> the experiment is a named variant        (RC-META-*)
   Invoked together whenever a run is finished, versioned, or tidied.

4. ENGINEERING PROCESS    (engineering_process.md)
   Software Engineering @Google -> review / change-size / doc discipline (RC-ENG-*)
   Scientific Python          -> the ML code idiom (fit/predict, pkg)    (RC-SP-*)
   Invoked together whenever a public symbol is defined, changed, reviewed.
```

## The pipeline they jointly define

```
configs/  (Hydra: HY-*, RC-HYDRA-*)        -> composes a typed config tree
         |  instantiated via _target_ / registry
         v
src/  (Lightning-Hydra-Template: LHT-*, PL-*) -> train.py builds objects
         |  LightningModule / DataModule (PL-*) + named arch (RC-TIMM-*) + registry (RC-OPENMMLAB-*)
         v
Python sources  (Google: GP-*)               -> every file obeys style/type rules
         |
         v
data/ + experiments (FAIR: RC-DATA-*, SemVer/GitFlow: RC-VER-*, SWE: RC-ENG-*, Meta: RC-META-*)
         |  governed datasets, tagged reproducible releases, reviewed changes
         v
mandatory quality gate (LHT-TOOL)            -> black . / isort . / ruff check .
                                              -> mypy src/ / pytest tests/
                                              -> gates the above before commit/CI
   + Scientific-Python discipline (RC-SP-*): installable package, CI style+type, sklearn fit/predict idiom
```

## Reference responsibilities (single responsibility, no overlap)

| Reference | Owns | Prefix | SKILL category |
|-----------|------|--------|----------------|
| `scaffold_grammar.md` | project directory layout, MLOps files, Hydra config system, Python grammar | `LHT-` `HY-` `GP-` | STRUCTURE / CONFIG / PYSTYLE |
| `model_design.md` | model/system contract, named architecture tiers, component registry | `PL-` `RC-TIMM-` `RC-OPENMMLAB-` | LIGHTNING / TIMM / OPENMMLAB |
| `experiment_repro.md` | config-first runs, FAIR data, SemVer/GitFlow, Meta experiment philosophy | `RC-HYDRA-` `RC-DATA-` `RC-VER-` `RC-META-` | HYDRA-CFG / DATA / VERSION / META |
| `engineering_process.md` | SWE review/change discipline, Scientific-Python idiom, **Research Code Comment Standard** | `RC-ENG-` `RC-SP-` `COMMENT-` | ENGINEERING / SCIENCE / COMMENT |

## Cross-cutting rules (where clusters must agree)

1. **Instantiation chain** — Hydra (`HY-STRUCT`) defines `_target_` configs;
   the Lightning template (`LHT-01`) consumes them in `src/train.py` via
   `hydra.utils.instantiate`; the resulting objects obey PL rules
   (`PL-INST`, `PL-INIT`). A missing `configure_optimizers` is both a
   `PL-OPT` (Lightning) and a `LHT-01` structural smell. The OpenMMLab
   Registry (`RC-OPENMMLAB-002`) is an alternate instantiation path that
   satisfies `PL-INST` inside a non-Hydra codebase.
2. **Typed configs == typed code** — `HY-STRUCTCFG` (structured configs)
   reinforces `GP-TYPE`/`GP-ANN` (annotated signatures). The audit treats
   untyped `instantiate` targets and untyped `__init__` as linked findings.
3. **Paths** — `HY-PATH` forbids hardcoded paths; `LHT-03` requires
   `.project-root` + `.env.example`. Both must hold for reproducibility.
4. **Metrics** — `PL-METRIC` (`/`-named, torchmetrics, `sync_dist`) is the
   concrete realization of the template best practice `LHT-BP`.
5. **Mandatory quality gate** — `LHT-TOOL` *implements* the `GP-*` rules via
   five required tools: `black .` (formatting, line-length 99), `isort .`
   (import order), `ruff check .` (static lint), `mypy src/` (typing), and
   `pytest tests/` (tests). Project line length (99) overrides the Google
   default (80); the audit reads `pyproject.toml` for the override (`GP-LEN`).
   `RC-SP-007` is the Scientific-Python statement of the same gate (installable
   package + CI style+type checks).
6. **Naming** — `GP-NAME` (snake_case/CapWords) governs config keys and
   `src/` module names alike; `LHT-05` expects `src/data`, `src/models`,
   `src/utils`. `RC-TIMM-001` is the model-class-level expression of the same
   naming discipline (name it `VisionTransformer`, not `MyModel`).
7. **Reproducible release loop** — `RC-VER-001` (tag each release) pins the
   data version (`RC-DATA-003`) and the config used (`HY-EXP`); `RC-ENG-004`
   (review before merge) closes the loop. `RC-HYDRA-001` is what makes the
   config self-contained enough to regenerate the run. `RC-META-005/006` forbids
   `train_v2_final.py`, demanding `train.py` + experiment config instead.

## Unified rule-code registry

| Code | Source (cluster) | Category | Meaning |
|------|-------------------|----------|---------|
| LHT-01..07, LHT-BP, LHT-TOOL | scaffold_grammar (template) | STRUCTURE | layout / entrypoints / root files / tests / src split / data-logs / experiments / best-practice / tooling |
| HY-ENTRY..HY-BEST | scaffold_grammar (hydra) | CONFIG | `@hydra.main` / defaults+`_target_` / groups / paths / experiment / sweep / structured / best-practice |
| GP-* (40+ codes) | scaffold_grammar (google) | PYSTYLE | all general Python rules (see scaffold_grammar.md) |
| PL-SYS..PL-DOC | model_design (lightning) | LIGHTNING | system/model split / self-contained / typed init / method order / forward≠train / dataloader / datamodule / metrics / ddp / optimizers / hparams / instantiate / docstrings |
| RC-TIMM-001..004 | model_design (timm) | TIMM | named-architecture / layers-blocks-architectures tiers / reuse / factory-not-string |
| RC-OPENMMLAB-001..003 | model_design (openmmlab) | OPENMMLAB | register_module / build_from_cfg / no-if-ladder |
| RC-HYDRA-001..003 | experiment_repro (hydra rules) | HYDRA-CFG | config-first / no-hardcoded-literal / override-not-edit |
| RC-DATA-001..006 | experiment_repro (FAIR) | DATA | dataset id / metadata / version / loader / run pin / open format |
| RC-VER-001..006 | experiment_repro (semver+gitflow) | VERSION | tag per release / SemVer / main stable / branches / release+hotfix / bump |
| RC-META-001..006 | experiment_repro (meta) | META | reproducible / config-not-hardcode / documented / benchmark / no-final-names / entrypoint+config |
| RC-ENG-001..007 | engineering_process (google swe) | ENGINEERING | docs / small change / tests / review / intent / consistency / interface-doc-never-drift |
| RC-SP-001..007 | engineering_process (scientific-python) | SCIENCE | sklearn idiom / docs+types / tests / benchmark / small API / transform / package+CI |
| COMMENT-001..017 | engineering_process (code_comments) | COMMENT | why-not-what / docstrings / math-formula / design-reason / TODO / FIXME / WARNING / experiment-note / no-stale / english / density / paper-core-block / update-on-modify |

## How to apply as the agent works

1. Pick the **cluster** for the concern you are acting on, and load only that
   one `references/*.md` file (lazy loading; do not load all at once):
   - layout / config / Python grammar → `scaffold_grammar.md`
   - model / backbone / component design → `model_design.md`
   - experiment run / data / version / naming → `experiment_repro.md`
   - review / change size / API idiom → `engineering_process.md`
2. When a code change touches two clusters (e.g. a config that instantiates an
   untyped module), apply the single most specific code and follow the related
   code from the other reference (cross-link in your note).
3. Never apply the same rule under two codes; pick the cluster that owns it
   (table above) and cross-link.
4. The aggregated `RC-*` machine-executable cards live in
   `references/rule_cards.md`; load it as the index when applying the
   cross-cutting standards (DATA/SCIENCE/VERSION/ENGINEERING/TIMM/OPENMMLAB/HYDRA-CFG).
