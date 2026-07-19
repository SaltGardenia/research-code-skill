---
name: research-code-skill
description: >-
  Coding-standard enforcer for AI agents working inside a research (ML/DL) lab
  project. Its core job is twofold: (1) keep the project's fixed architecture
  intact across all coding work 鈥?never break or drift from the established
  structure; (2) enforce code-level conventions 鈥?naming, formatting, calling,
  and configuration 鈥?so every file is uniform. It codifies five authoritative
   systems as machine-executable Rule Cards (RC-*). It fuses thirteen
   authoritative references into four usage clusters so the agent never stacks
   them as separate checklists, plus a Karpathy-inspired behavioral discipline
   (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven
   Execution) layered above the mechanical cards: (1) Project Scaffold & Python Grammar
   (Lightning-Hydra-Template structure + Hydra configs + Google Python
   Style); (2) Model & Component Design (PyTorch Lightning Style Guide + timm
   named architectures + OpenMMLab Registry pattern); (3) Experiment
   Reproducibility (Hydra Config-First + FAIR data + SemVer/Git Flow + Meta
   Research philosophy); (4) Engineering Process (Software Engineering at Google
   + Scientific-Python idiom). It operates in two scenarios: build from zero (A)
   or tidy an existing repo (B). It is NOT a post-hoc reviewer: it constrains
   code as it is written. Trigger on any code task: "add a model", "write a
   training script", "refactor this module", "create the project scaffold",
   "name this function", "add a config group", "manage dataset metadata", "tag
   this experiment release", or "what structure should this file use".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
version: 1.3.0
author: research-code-skill
tags:
  - python
  - research
  - machine-learning
  - code-style
  - pytorch-lightning
  - hydra
  - best-practices
  - coding-standards
  - project-structure
compatibility:
  - claude
  - gpt
  - kilo
  - any-model-supporting-skills
---

# Research Code Skill

> **For developers (human readers):** every Markdown file in this skill ships with
> a Chinese companion (`.zh.md`, e.g. `SKILL.zh.md`, `references/*.zh.md`) for
> easier reading. The agent always loads the **English** original; the `.zh.md`
> files are documentation only and are never the source of truth.

A skill that acts as the **coding-standard layer** of a research lab's ML/DL
project. Rather than reviewing code after the fact, it lives in the agent's
context and **constrains every code operation as it happens**. Its essence is
twofold:

1. **Project architecture** 鈥?keep the lab's fixed project structure intact.
   As the agent writes or edits code, the architecture is the stable base: do
   not break it, do not invent a new layout, keep it clear and consistent.
2. **Code-level conventions** 鈥?within that architecture, every symbol and call
   follows uniform rules: naming, formatting, import/call style, and how
   configs compose.

These two axes are enforced in both core scenarios (build from zero, tidy an
existing repo). The agent consults this skill before writing or editing any
project code, so the codebase stays coherent by construction.

It distills thirteen authoritative references into **four fused usage
clusters**, plus a coordination layer, into one shared convention set. Each
cluster is one coherent concern the agent reaches for 鈥?the sources inside it
compound, they do not stack:

1. **Project Scaffold & Python Grammar** (`references/scaffold_grammar.md`)
   鈥?fuses Lightning-Hydra-Template (structure, `LHT-*`), Hydra configs
   (`HY-*`), and Google Python Style (`GP-*`): the layout, the config system
   that fills it, and the grammar that writes the Python in it.
2. **Model & Component Design** (`references/model_design.md`) 鈥?fuses PyTorch
   Lightning Style (`PL-*`, the model/system contract), timm architecture style
   (`RC-TIMM-*`, named architectures + `models/{layers,blocks,architectures}`),
   and OpenMMLab Registry (`RC-OPENMMLAB-*`, `@X.register_module()` +
   `build_from_cfg`): how a well-shaped, pluggable model looks.
3. **Experiment Reproducibility** (`references/experiment_repro.md`) 鈥?fuses
   Hydra Config-First (`RC-HYDRA-*`), FAIR data (`RC-DATA-*`), SemVer+Git Flow
   (`RC-VER-*`), and Meta Research philosophy (`RC-META-*`): the
   config鈫抎ata鈫抍ode鈫抏xperiment chain that makes a run regenerable.
4. **Engineering Process & Interface Discipline**
   (`references/engineering_process.md`) 鈥?fuses Software Engineering at Google
   (`RC-ENG-*`, review/change-size/docs) and Scientific-Python idiom
   (`RC-SP-*`, `fit`/`predict`, installable package, CI): what "good code"
   means as an engineering artifact. It also owns the **Research Code Comment
   Standard** (`references/code_comments.md`, `COMMENT-*`): research
   comments record intent / math / design decision / experiment constraint,
   not a line-by-line narration.
5. **references/coordination.md** + **references/rule_cards.md** 鈥?map all
   sources into one rule-code registry (`LHT-/HY-/PL-/GP-*` plus `RC-*`
   Rule Cards) so every convention is single, non-duplicated, machine-checkable.

## Role in the workflow

This skill is a **core part of the project context**, not an optional utility.
Treat it as the project's written engineering charter:

- **Architecture first**: the established structure (`configs/`, `src/data`,
  `src/models`, `src/utils`, entrypoints, root files) is the invariant. Every
  code operation respects it; never bypass or dismantle it.
- On project init (Scenario A), scaffold the structure from
  `templates/project_skeleton/`.
- On every code change (add / edit / delete a file or symbol), first check the
  relevant reference for the convention that applies, then write to match it.
- When naming anything (module, class, function, variable, config key, config
  file), apply the naming rules from the applicable reference.
- When the user's request would break a convention, follow the convention and
  briefly note the deviation you applied (do not silently diverge, do not
  silently invent).

## Two core scenarios

This skill is used in exactly two situations. Both share the same invariant:
**preserve the project's architecture** 鈥?it is the stable base; code is added
and changed *within* it, never by breaking or bypassing it. Within that
architecture, all code obeys the **code-level conventions** (naming, format,
calling). Identify which scenario applies and follow its mode.

> **Two axes of regulation**
> 1. **Architecture (project level)** 鈥?fixed structure: `configs/` grouped by
>    concern, `src/data` 路 `src/models` 路 `src/utils`, entrypoints, root files.
>    Keep it clear; do not dismantle or reinvent it.
> 2. **Code level** 鈥?naming, formatting, import/call style, and config
>    composition, uniform across every file.

### Scenario A 鈥?Build from zero (greenfield)
The target is empty or does not yet exist. Use this skill to construct the
whole project so it conforms from the first commit:

- Start from `templates/project_skeleton/` (scaffold mode) to lay down the
  **fixed architecture**: directory structure, root files, `configs/`, `src/`.
- Write every new file strictly within that architecture: right directory, right
  module shape, right config composition, right names.
- This mode is forward-only; there is no existing code to reconcile.

### Scenario B 鈥?Tidy an existing repository
The target is an existing repo with code that may not follow the conventions.
Use this skill to bring it into the **same architecture** without breaking it:

- First **audit** the current state against the rule-code registry (run
  `scripts/audit_style.py`, or reason from the references) to enumerate gaps.
- Then **restructure and rewrite** to fit the fixed architecture: relocate
  files into `src/`, `configs/<group>/`; convert hardcoded args into Hydra
  configs; split models from systems; rename symbols per `GP-NAME`/`PL-*`; add
  missing root files and `tests/`.
- Preserve behavior while changing shape; reorganize by **moving/renaming**, and
  **never arbitrarily delete or rewrite** existing code. If a piece of code has
  no matching target folder, **leave it in the project root** rather than
  removing it. **Never replace the architecture with a different one**.
- Report the concrete changes made (a short "Convention applied" note per
  group of changes), and re-run the conformance gate to confirm.

## When to Use

Apply this skill whenever the agent works in the research project:

- **Scenario A (build)**: scaffold and write a brand-new research project that
  follows the conventions from day one.
- **Scenario B (tidy)**: reorganize, rename, and refactor an existing repo so
  its architecture, naming, and configs conform to the standard.
- **Ongoing code ops** within either scenario: create / read / update / delete
  a file or symbol, or choose a name 鈥?always per the conventions.

Do NOT use this skill for:
- Pure frontend / web-only projects without a Python/ML backend.
- Non-Python languages (C++, JS) unless only the Google naming/text rules apply.

## Preconditions

Before applying a convention, verify:
1. A target path is provided (repo root, directory, or specific files).
2. The change concerns Python code or Hydra YAML configs in the project.
3. Read access is available; Write/Edit only when the operation requires it.
4. For script execution, a Python 3.8+ interpreter is available.

If no target is given, ask the user for the path before proceeding.
Decide the scenario: if the target is empty or absent, use **Scenario A**
(scaffold, Procedure Step 5); if it already contains code, use **Scenario B**
(tidy, Procedure Step 5鈫?).

## Procedure

Apply the conventions as you work. Each step maps to a reference source; load
only the reference for the operation at hand.

> Lazy reference loading: read only the **one cluster file** under
> `references/` for the concern being acted on. Do NOT load all at once 鈥?
> the four files are fused, pick the one that owns the concern.
> - SCAFFOLD & GRAMMAR 鈫?`references/scaffold_grammar.md` (layout `LHT-*`, config `HY-*`, Python `GP-*`)
> - MODEL & COMPONENT 鈫?`references/model_design.md` (`PL-*`, `RC-TIMM-*`, `RC-OPENMMLAB-*`)
> - EXPERIMENT REPRO 鈫?`references/experiment_repro.md` (`RC-HYDRA-*`, `RC-DATA-*`, `RC-VER-*`, `RC-META-*`)
> - ENGINEERING PROCESS 鈫?`references/engineering_process.md` (`RC-ENG-*`, `RC-SP-*`, `COMMENT-*`)
> - cross-cutting -> `references/coordination.md` + `references/rule_cards.md`
> - BEHAVIORAL DISCIPLINE -> `references/rule_cards.md` (`RC-KARPATHY-*`)

### Always-on behavioral discipline (Karpathy -- applies to EVERY code action)
These four principles are **summarized here so they stay in context for every
edit**; the full `RC-KARPATHY-*` cards live in `references/rule_cards.md`.
- **Think Before Coding**: state assumptions; if ambiguous, surface
  interpretations and ask instead of silently guessing. Stop and name confusion.
- **Simplicity First**: minimum code that solves the problem; no speculative
  features, abstractions, or error handling beyond the request.
- **Surgical Changes**: touch only what the request requires; match existing
  style; clean up only the orphans *your* change created.
- **Goal-Driven Execution**: turn imperative asks into verifiable goals
  (e.g. "write a test that reproduces the bug, then make it pass") and loop
  until the success criterion holds.
> Caveat: bias toward caution over speed -- trivial one-liners (typo fixes) need
> not invoke full rigor.


### Step 1 鈥?Project structure & Python grammar (Cluster 1)
Load `references/scaffold_grammar.md` (fuses Lightning-Hydra-Template layout,
Hydra config system, and Google Python grammar), then place code per the layout:
- `configs/` holds Hydra YAML configs grouped by concern
  (`data/`, `model/`, `trainer/`, `callbacks/`, `logger/`, `experiment/`, ...).
- `src/` holds source split by role: `src/data/`, `src/models/`,
  `src/utils/`, with entrypoints `src/train.py`, `src/eval.py`.
- `tests/` holds generic smoke tests; `data/`, `logs/`, `notebooks/` are separated.
- Root files: `.pre-commit-config.yaml`, `pyproject.toml` (or `setup.py`),
  `requirements.txt`, `.gitignore`, `.env.example`, `.project-root`.
When creating a file, put it under the matching directory (codes `LHT-01..07`).

### Step 2 鈥?Config conventions (Hydra)
Load `references/scaffold_grammar.md` (CONFIG section), then write configs that:
- Use `@hydra.main(version_base=..., config_path=..., config_name=...)` at
  entrypoints, with `rootutils.setup_root` for location independence.
- Compose by group, override via CLI and `@` defaults lists.
- Express each object as a `_target_` plus primitive params.
- Resolve all paths via `configs/paths/default.yaml` (no hardcoded paths).
- Version-control experiments as configs under `configs/experiment/`.
Apply codes `HY-ENTRY`, `HY-STRUCT`, `HY-GROUP`, `HY-PATH`, `HY-EXP`, `HY-BEST`.

### Step 3 鈥?LightningModule / DataModule conventions (Cluster 2)
Load `references/model_design.md` (PyTorch Lightning contract + timm + OpenMMLab),
then shape modules that:
- Separate **model** backbones from the **system** (`LightningModule`).
- Are **self-contained**: optimizer + scheduler live in `configure_optimizers`.
- Have **explicit typed `__init__`** with sensible defaults (no opaque `params`).
- Follow the **method order**: `__init__` 鈫?`forward` 鈫?`training_step` 鈫?
  validation 鈫?`test` 鈫?`configure_optimizers` 鈫?extra hooks.
- Keep `forward()` for inference only (never training logic).
- Use `LightningDataModule` for data; `torchmetrics` (separate instance per
  step), `/`-named metrics, `sync_dist=True` under DDP.
Apply codes `PL-SYS`, `PL-SELF`, `PL-INIT`, `PL-ORDER`, `PL-FWD`, `PL-DM`,
`PL-METRIC`, `PL-DDP`, `PL-OPT`, `PL-HPARAM`.

### Step 4 鈥?Python style & naming (Google Python Style Guide)
Load `references/scaffold_grammar.md` (PYSTYLE section), then write code that:
- Uses `snake_case` for functions/vars, `CapWords` for classes, `UPPER_CASE`
  for constants; avoids `l`, `I`, `O` single-letter names (`GP-NAME`).
- Respects line length <= 80 (Google) unless the project sets 99
  (Black/PL template override) (`GP-LEN`).
- Groups imports: stdlib, third-party, local; no wildcard imports (`GP-IMP`).
- Carries docstrings on every public module/class/function (`GP-DOC`).
- Carries type annotations on all signatures (`GP-ANN`/`GP-TYPE`).
- Avoids semicolons, bare `except:`, mutable default args, `print` for
  diagnostics (`GP-SEMI`/`GP-EXC`/`GP-DEF`/`GP-PRINT`).
- Guards executables with `if __name__ == "__main__":` (`GP-MAIN`).
Use `scripts/audit_style.py` as a conformance gate (it checks a subset of these
codes). The full rule registry lives in `references/coordination.md`.

### Step 5 鈥?Build from zero (Scenario A)
Used when the target is empty or absent. Load
`references/scaffold_grammar.md`, then generate the directory skeleton
from `templates/project_skeleton/` per its `MANIFEST.md`. Copy `configs/` +
`src/` stubs and root files. Do not overwrite existing user files; report
exactly what was created and what was skipped. Then continue with Steps 1鈥? as
you write each new file, so the project conforms from the first commit.
6. **Sync `.gitignore`**: run `python scripts/sync_gitignore.py .` so the ignore
   list reflects the freshly created layout (the script only maintains its
   auto-managed block and never touches hand-written rules).

### Step 6 鈥?Tidy existing repo (Scenario B)
Used when the target already has code. Apply the conventions by restructuring,
not just noting gaps:
1. **Audit** current state against the rule-code registry (run
   `scripts/audit_style.py` and/or reason from the references) to enumerate
   deviations per category (STRUCTURE / CONFIG / LIGHTNING / PYSTYLE).
2. **Restructure**: relocate files into `src/data`, `src/models`,
   `src/utils`, `configs/<group>/`; add missing root files and `tests/`.
3. **Rewrite to conform**: convert hardcoded args into Hydra `_target_`
   configs; split model backbones from `LightningModule` systems; rename symbols
   per `GP-NAME` / `PL-*`; apply `torchmetrics` and `/`-named logging.
4. **Preserve behavior** 鈥?prefer moving/renaming over deleting; keep outputs
   identical.
 5. **Confirm**: re-run `scripts/audit_style.py`; remaining BLOCKER/MAJOR items
    must be resolved before declaring the repo tidy.
 6. **Sync `.gitignore`**: run `python scripts/sync_gitignore.py .` so the ignore
    list tracks the new/relocated directories (e.g. `logs/`, `outputs/`,
    `wandb/`, `checkpoints/`). The script derives entries from the current
    layout inside a marked auto-managed block; hand-written rules are preserved.

### Step 7 鈥?Apply & confirm (both scenarios)
Write the code to match the convention. When a change touches two layers (e.g.
a config that instantiates an untyped module), apply the single most specific
code and follow the related code from the other reference
(see `references/coordination.md`). If a conformance script is available, run it
to confirm the change holds.

### Step 8 鈥?Run the mandatory quality gate (both scenarios)
After writing/editing code, the project MUST pass the standard quality tools
before the change is accepted. These are the lab's required checks; run them
from the project root (configs live in `pyproject.toml` / `.pre-commit-config.yaml`):

```bash
black .                 # 1. Formatting (line-length 99 by default)
isort .                 # 2. Import ordering (black profile)
ruff check .            # 3. Static lint + import/style/complexity checks
mypy src/              # 4. Type checking across the source package
pytest tests/          # 5. Run the test suite (smoke + unit)
```

Rules:
- Run all five in order; do not skip any. Fix every error they report.
- `black`/`isort` may rewrite files 鈥?re-read them after, then re-run to
  confirm clean.

### Caches are aggregated, not scattered
Tool caches and run artifacts that have **no direct relation to the project
code** are swept into a single `.cache/` folder at the repo root so the tree
stays clean. This covers only caches (`.mypy_cache/`, `.pytest_cache/`,
`.ruff_cache/`, `.coverage`, `htmlcov/`) 鈥?**not** Hydra run outputs, which
stay at the root (`logs/`, `outputs/`, `wandb/`) as real experiment artifacts.
- Redirect caches with the provided helper: `scripts/run_gate.sh` (bash) or
  `scripts/run_gate.ps1` (PowerShell). It sets `MYPY_CACHE_DIR`,
  `PYTEST_DEBUG_TEMPROOT`, `COVERAGE_FILE` and `ruff --cache-dir`, then runs
  the five tools; with `SWEEP_ONLY=1` it only moves loose caches into `.cache/`.
- All `.cache/` contents are already covered by `.gitignore`, so they are
  never committed. See `.cache/README.md`.
- `mypy src/` must reach zero type errors (`strict` optional; at minimum no
  untyped public signatures 鈥?see `GP-ANN`).
- `pytest tests/` must be green; add/extend a smoke test for any new
  `LightningModule`/`DataModule`/entrypoint.
- In CI this exact sequence runs as the gate; locally it is the same contract.

### Step 9 鈥?Apply the Rule Cards (cross-cutting, both scenarios)
Beyond the four core code categories, the skill enforces seven standard
families as **Rule Cards** (`RC-*`) 鈥?abstracted, machine-checkable rules
rather than mere links. They live inside the four cluster files. Load
`references/rule_cards.md` (index) plus the cluster file for the concern:

- **Cluster 3 鈥?Experiment Reproducibility** (`references/experiment_repro.md`):
  - **Hydra Config-First** `RC-HYDRA-*`: every experimental variable
    (lr, batch, seed, paths, ...) exists in config, read from `cfg`; no
    hardcoded literals like `lr = 0.001`.
  - **FAIR data** `RC-DATA-*`: datasets have metadata, identifier, version
    pinned to a tag, a runnable loader; every run records its data version.
  - **Versioning / Git Flow** `RC-VER-*`: every experiment release is a git
    tag following SemVer; work stays on `feature/*`/`experiment/*`, not `main`.
  - **Meta Research philosophy** `RC-META-*`: reproducible/configurable/
    documented/benchmarkable experiments; no `train_v2_final.py`, variants as
    experiment configs.
- **Cluster 2 鈥?Model & Component Design** (`references/model_design.md`):
  - **timm model design** `RC-TIMM-*`: name the architecture (e.g.
    `VisionTransformer`, not `MyModel`); ops in `models/layers/`, blocks in
    `models/blocks/`, named models in `models/architectures/`; register via factory.
  - **OpenMMLab Registry** `RC-OPENMMLAB-*`: register components with
    `@X.register_module()`; build via `build_from_cfg(cfg)`; never `if model == "vit"` branching.
- **Cluster 4 鈥?Engineering Process** (`references/engineering_process.md`):
  - **Engineering (Google)** `RC-ENG-*`: small reviewable changes, documented
    public API, test coverage, review before merge to `main`; interface docs
    never drift (`RC-ENG-007`).
  - **Scientific Python** `RC-SP-*`: estimators expose `fit(X,y)`/`predict(X)`;
    public symbols documented + typed; numeric code tested; installable package + CI.
  - **Research Code Comment Standard** `COMMENT-*`: comments explain **why**
    (intent, math, design decision, experiment constraint), not a line-by-line
    narration; public APIs/docstrings follow NumPy/PEP257; math carries the
    formula + citation; `TODO(owner): reason`; no stale comments (`COMMENT-001..017`).
  - **LLM Coding-Discipline (Karpathy) `RC-KARPATHY-*`**: a behavioral layer
    over the mechanical cards 鈥?**Think Before Coding** (surface assumptions,
    tradeoffs, confusion), **Simplicity First** (minimum code, no speculative
    abstraction), **Surgical Changes** (touch only what is asked, match style,
    clean only your own orphans), **Goal-Driven Execution** (imperative 鈫?
    verifiable goal + verify loop). It counters LLM failure modes 鈥?wrong
    assumptions, overcomplication, orthogonal edits, vague goals 鈥?and biases
    toward caution over speed (use judgment on trivial one-liners).

When a Rule Card touches code already covered by `LHT-/HY-/PL-/GP-*`, apply the
single most specific code and cross-link; never duplicate a rule under two
codes.

## Mandatory quality tools

These five tools are **required** for every research project governed by this
skill. They operationalize the conventions: `black`/`isort` enforce formatting
(`GP-LEN`/`GP-IMP`), `ruff` enforces static rules (`GP-SEM*`/`GP-EXC`/...),
`mypy` enforces typing (`GP-ANN`/`GP-TYPE`), and `pytest` enforces that the
code actually runs. Their configs ship with the scaffold template.

| Tool | Purpose | Invocation |
|------|---------|------------|
| black | Formatting | `black .` |
| isort | Import ordering | `isort .` |
| ruff | Static analysis / lint | `ruff check .` |
| mypy | Type checking | `mypy src/` |
| pytest | Tests | `pytest tests/` |

## Output Format

This skill does not emit a review report by default. It **shapes the code it
writes**. When you must explain a convention choice to the user, return a short
fixed Markdown note:

```markdown
# Convention applied: <operation> in <target>

## Decision
- <what structure/naming/config pattern was applied>

## Rule
- <code> 鈥?<one-line rule from the registry>

## Note
- <optional: deliberate deviation or ambiguity resolved>
```

Codes are the unified registry in `references/coordination.md`: STRUCTURE
(`LHT-*`), CONFIG (`HY-*`), LIGHTNING (`PL-*`), PYSTYLE (`GP-*`). Severity is
used only when a script is run: `BLOCKER` (breaks run/repro), `MAJOR` (core
rule), `MINOR` (style nit).

## Error Handling

- **No Python/config target found**: ask the user for the path, or build from
  zero (Scenario A, Step 5).
- **Conformance script missing deps**: print `pip install -r requirements.txt`,
  retry once; if still failing, fall back to manual convention checks.
- **Permission denied on Write**: stop, explain what could not be written, and
  suggest the user grant access.
- **Unparseable file**: skip it, note the reason, and continue the rest.
- **Target not empty but Scenario A requested**: switch to Scenario B (tidy) 鈥?
  never overwrite; restructure and add missing files, reporting conflicts.
- **Reference file missing/unreadable**: load the next applicable reference; if
  none, fall back to the inlined rules here and flag the gap.
- **Ambiguous rule**: prefer the project's own `pyproject.toml`/`setup.cfg`
  config over the generic default, and note the override applied.

## Constraints

- **Architecture is invariant**: the project's fixed structure is the stable
  base. Never break it, bypass it, or replace it with a different layout while
  coding. Add and change code *within* the architecture; keep it clear.
- Single responsibility: this skill ONLY governs research-code standards
  (architecture, naming, structure, configs); do not mix in unrelated tasks.
- It is a **contextual enforcer**, not a post-hoc reviewer: apply conventions
  as code is written/edited, not after.
- Two axes only: (1) project-level architecture, (2) code-level naming/format/
  calling. Keep both uniform; do not introduce a third, ad-hoc concern.
- Never auto-commit or push changes unless the user explicitly asks.
- Never invent config values or names; derive them from the conventions and
  existing project patterns.
- Respect the project's existing line-length / formatter config if present.
- Load reference docs lazily: read `references/` files only for the concern
  being acted on, not all at once.
- Use the unified rule-code registry in `references/coordination.md`; never
  invent a code not in the registry, and never apply one rule under two codes.

