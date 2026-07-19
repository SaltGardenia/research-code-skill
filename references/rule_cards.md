# Rule Cards — machine-executable registry

The user's recommended pattern: instead of only linking documents, we abstract
each standard into a **Rule Card** (`RC-XXX-NNN`) the agent can check and apply
directly. This file is the single index of all rule cards. Rule cards are
cross-cutting: they sit on top of the four core code categories
(`LHT-*` / `HY-*` / `PL-*` / `GP-*`) and cover data, science idiom,
versioning, engineering process, and the model/experiment disciplines.

The 13 source standards are **fused into 4 reference files**, each a natural
usage cluster where the standards compound rather than stack:

1. `scaffold_grammar.md` — **Project Scaffold & Python Grammar**
   (Lightning-Hydra-Template + Hydra config + Google Python Style):
   layout (`LHT-*`), config system (`HY-*`), and the Python grammar (`GP-*`).
2. `model_design.md` — **Model & Component Design**
   (PyTorch Lightning Style + timm + OpenMMLab): the model contract (`PL-*`),
   the concrete architecture shape (`RC-TIMM-*`), and pluggability (`RC-OPENMMLAB-*`).
3. `experiment_repro.md` — **Experiment Reproducibility**
   (Hydra Config-First + FAIR + SemVer/GitFlow + Meta Research): the chain
   config→data→code→experiment (`RC-HYDRA-*`, `RC-DATA-*`, `RC-VER-*`, `RC-META-*`).
4. `engineering_process.md` — **Engineering Process & Interface Discipline**
   (Software Engineering at Google + Scientific Python): review/change discipline
   (`RC-ENG-*`) and the ML code idiom (`RC-SP-*`).

Severity: `BLOCKER` (breaks reproducibility/run), `MAJOR` (violates a core
rule), `MINOR` (should-fix).

## RC-DATA — FAIR data management (`references/experiment_repro.md`)
- RC-DATA-001: every dataset/artifact has metadata (schema, source, license). [MAJOR]
- RC-DATA-002: every dataset/artifact has a unique, resolvable identifier. [MAJOR]
- RC-DATA-003: every dataset declares a version pinned to a git tag / DVC rev. [MAJOR]
- RC-DATA-004: every dataset ships loading instructions (runnable loader). [MAJOR]
- RC-DATA-005: every experiment run records the exact data version used. [BLOCKER]
- RC-DATA-006: data formats/serialization are open & standard. [MINOR]

## RC-SP — Scientific Python ecosystem (`references/engineering_process.md`)
- RC-SP-001: public estimators expose `fit(X, y)` / `predict(X)`. [MAJOR]
- RC-SP-002: public functions/classes carry docstrings + type hints. [MAJOR]
- RC-SP-003: numerical routines include a unit/regression test. [MAJOR]
- RC-SP-004: benchmarkable numeric code ships a benchmark/timing test. [MINOR]
- RC-SP-005: public API changes are small, documented, reviewable. [MINOR]
- RC-SP-006: transformers expose `transform` / `fit_transform`. [MINOR]
- RC-SP-007: project ships as an installable package; CI runs style + type checks. [MINOR]

## RC-VER — Versioning & Git Flow (`references/experiment_repro.md`)
- RC-VER-001: every experiment release maps to a git tag (`vMAJOR.MINOR.PATCH`). [MAJOR]
- RC-VER-002: version follows SemVer `MAJOR.MINOR.PATCH`. [MAJOR]
- RC-VER-003: `main` holds only tagged, stable releases. [MAJOR]
- RC-VER-004: new work lives on `feature/*` / `experiment/*`, not on `main`. [MINOR]
- RC-VER-005: `release/*` prepares MINOR/MAJOR; `hotfix/*` for PATCH. [MINOR]
- RC-VER-006: bump version before tagging a release. [MINOR]

## RC-ENG — Software Engineering at Google (`references/engineering_process.md`)
- RC-ENG-001: every public function/class carries documentation. [MAJOR]
- RC-ENG-002: every change is small, single-purpose, reviewable. [MAJOR]
- RC-ENG-003: every change is covered by a test. [MAJOR]
- RC-ENG-004: every change passes review before merge to `main`. [MAJOR]
- RC-ENG-005: change intent is stated explicitly. [MINOR]
- RC-ENG-006: code stays consistent with surrounding style/structure. [MINOR]
- RC-ENG-007: on every public API change, update its docstring (signature, params, returns, examples) so docs never drift. [MAJOR]

## RC-META — Meta Research repo philosophy (`references/experiment_repro.md`)
- RC-META-001: every experiment is reproducible (seed + pinned data + recorded config). [MAJOR]
- RC-META-002: knobs live in configs, not hardcoded in scripts. [MAJOR]
- RC-META-003: every experiment is documented (how to run + what it means). [MAJOR]
- RC-META-004: every experiment targets a clear, comparable benchmark/metric. [MINOR]
- RC-META-005: forbidden filename pattern `*_v<N>_*final*.py` / `*_new.py` / `*_copy.py` / `*_old.py`; use `train.py` + experiment config. [MAJOR]
- RC-META-006: entrypoint is `trainer.py`/`train.py`; variants are `configs/experiment/*.yaml`, not new scripts. [MINOR]

## RC-HYDRA — Hydra Config-First (`references/experiment_repro.md`)
- RC-HYDRA-001: every experimental variable (lr, batch, seed, depth, paths, scheduler) exists in config and is read from `cfg`. [MAJOR]
- RC-HYDRA-002: no hardcoded experimental literals in code (e.g. `lr = 0.001`); override via CLI/config. [MAJOR]
- RC-HYDRA-003: experiments differ only by config overrides, not by edited code literals. [MINOR]

## RC-TIMM — timm Model Architecture Style (`references/model_design.md`)
- RC-TIMM-001: model class is named after the architecture (e.g. `VisionTransformer`), not a generic `MyModel`. [MAJOR]
- RC-TIMM-002: generic ops live in `models/layers/`; compositions in `models/blocks/`; named models in `models/architectures/`. [MAJOR]
- RC-TIMM-003: new vision-transformer variants reuse existing `layers/`+`blocks/`; no duplicated attention/FFN code. [MINOR]
- RC-TIMM-004: architecture is registered/exported via the model factory, not referenced by string `if model == "vit"`. [MAJOR]

## RC-OPENMMLAB — OpenMMLab Engineering Standard (`references/model_design.md`)
- RC-OPENMMLAB-001: pluggable components are registered (`@X.register_module()`), not selected by string `if model == "..."`. [MAJOR]
- RC-OPENMMLAB-002: components are instantiated via `build_from_cfg(cfg)` / `Registry.build(cfg)`, not hand-built branches. [MAJOR]
- RC-OPENMMLAB-003: adding a component requires only a registration + config entry, not edits to a central `if/elif` ladder. [MINOR]

## COMMENT — Research Code Comment Standard (`references/code_comments.md`)
- COMMENT001: comment explains **why**, not **what** (states assumption/intent). [MAJOR]
- COMMENT002: every public function/class carries a docstring (NumPy/PEP257 style). [MAJOR]
- COMMENT003: core module docstring states function, I/O, and design source/reference. [MAJOR]
- COMMENT004: mathematical algorithms carry the formula + citation as a comment. [MAJOR]
- COMMENT005: complex algorithms carry a staged (Stage 1/2/3) block comment. [MINOR]
- COMMENT006: non-obvious design decisions carry a `Reason:` comment. [MAJOR]
- COMMENT007: `TODO(owner): action + reason` (+ issue link); no bare `TODO`. [MINOR]
- COMMENT008: known problems use `FIXME:` with temporary-solution note. [MINOR]
- COMMENT009: dangerous code uses `WARNING:` explaining the hazard. [MINOR]
- COMMENT010: empirical constraints use `Experiment Note:` (observed delta). [MINOR]
- COMMENT011: no code-restatement comments (`# convolution`). [MINOR]
- COMMENT012: no meaningless comments (`# model`). [MINOR]
- COMMENT013: no stale comments that contradict the code (`# use ResNet` + `ViT()`). [MAJOR]
- COMMENT014: core code comments in English; Chinese only for temp experimental notes. [MINOR]
- COMMENT015: comment density matches code type (util ~10% … paper-core 40%+). [MINOR]
- COMMENT016: every paper-core module has a Purpose/Formula/Reference/IO/Complexity/Design doc block. [MAJOR]
- COMMENT017: on modify, update/remove stale comments and docstring new public APIs. [MAJOR]

## RC-KARPATHY — LLM coding-discipline principles (`references/coordination.md`)
Derived from Andrej Karpathy's observations on LLM coding pitfalls. These are
**behavioral** guardrails that sit above the mechanical RC-* cards: they govern
how the agent reasons and edits, not which specific symbol/format to use. They
directly counter four failure modes: wrong assumptions, overcomplication,
orthogonal edits, and vague/unverifiable goals.

- RC-KARPATHY-001: **Think Before Coding** — state assumptions explicitly; if
  ambiguous, present multiple interpretations and ask rather than silently
  guessing. [MAJOR]
- RC-KARPATHY-002: **Think Before Coding** — push back when a simpler approach
  exists; surface tradeoffs instead of blindly following the literal request. [MINOR]
- RC-KARPATHY-003: **Think Before Coding** — stop and name what is unclear; do
  not hide confusion or run with a wrong assumption. [MAJOR]
- RC-KARPATHY-004: **Simplicity First** — write the minimum code that solves
  the problem; no features, abstractions, configurability, or error handling
  beyond what was requested. [MAJOR]
- RC-KARPATHY-005: **Simplicity First** — if the same work fits in far fewer
  lines (e.g. 200 → 50), rewrite it; a senior engineer should not call it
  overcomplicated. [MINOR]
- RC-KARPATHY-006: **Surgical Changes** — touch only what the request requires;
  do not "improve" adjacent code, comments, or formatting. [MAJOR]
- RC-KARPATHY-007: **Surgical Changes** — match existing style even if you would
  do it differently; do not refactor unbroken code. [MINOR]
- RC-KARPATHY-008: **Surgical Changes** — remove only imports/vars/funcs that
  *your* change made unused; if you spot pre-existing dead code, mention it,
  never delete it unasked. [MINOR]
- RC-KARPATHY-009: **Goal-Driven Execution** — transform imperative asks into
  verifiable goals (e.g. "write a test that reproduces the bug, then make it
  pass"); loop until the success criterion is met. [MAJOR]
- RC-KARPATHY-010: **Goal-Driven Execution** — for multi-step work, state a
  brief plan with a verify step per item before acting. [MINOR]

> Note: these four principles (Think Before Coding, Simplicity First, Surgical
> Changes, Goal-Driven Execution) bias toward **caution over speed**. Use
> judgment on trivial one-liners (typo fixes) — not every change needs full
> rigor. They augment, never replace, the `LHT-/HY-/PL-/GP-*` and other RC-*
> cards.

## How the agent uses Rule Cards

1. Choose the **cluster** for the concern at hand, then load only that one
   `references/*.md` file (lazy loading — do NOT load all at once):
   - layout / config / Python grammar → `scaffold_grammar.md`
   - model / backbone / component design → `model_design.md`
   - experiment run / data / version / naming → `experiment_repro.md`
   - review / change size / API idiom → `engineering_process.md`
2. For the action being performed, check the applicable `RC-*` cards and the
   core `LHT-/HY-/PL-/GP-*` codes (same file, same cluster).
3. Apply them as the code/data is written; do not invent cards outside this
   index. If a card conflicts with an existing project convention, the project
   convention wins and the deviation is noted.
