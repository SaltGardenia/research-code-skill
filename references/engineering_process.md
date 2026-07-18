# Reference: Engineering Process & Interface Discipline

Source of truth for **what "good code" means as an engineering artifact** —
across every file the other references produce. Two standards fuse here because
they answer the same question from two seats at the same table:

- **Software Engineering at Google** — the *process*: small reviewable changes,
  clear intent, tests, code review, and interface docs that never drift
  (`RC-ENG-*`).
- **Scientific Python ecosystem** — the *code-level idiom*: NumPy/SciPy/sklearn
  conventions, the `fit`/`predict` Estimator API, docstrings + types,
  shipped as an installable package with CI (`RC-SP-*`).

They compound: Google says "document and test the public API"; Scientific-Python
says "here is the concrete shape of that API (`fit`/`predict`, installable
package, CI style+type checks)". Apply both whenever you define, change, or
review a public symbol.

## 1. Engineering process (ENGINEERING — `RC-ENG-*`)

Distilled from *Software Engineering at Google* and the Google Engineering
Practices / Code Review guidelines.

**Principles**
- **Small, reviewable changes** — one logical change per CL/PR; easy to reason about and revert.
- **Clear intent** — every change states its purpose; no silent scope creep.
- **Testable** — covered by tests; behavior verifiable.
- **Maintainable** — simple, documented, consistent with surrounding code.
- **Code review** — every change reviewed; reviewers check correctness, tests, clarity, convention.

**What reviewers check** (each dimension): Design · Functionality · Complexity ·
Tests · Naming · Comments · Style · Documentation.

### Rule cards

| Code | Rule | Severity |
|------|------|----------|
| RC-ENG-001 | Every public function/class carries documentation (docstring). | MAJOR |
| RC-ENG-002 | Every change is small, single-purpose, and reviewable. | MAJOR |
| RC-ENG-003 | Every change is covered by a test (or justifies why not). | MAJOR |
| RC-ENG-004 | Every change passes review before merge to `main`. | MAJOR |
| RC-ENG-005 | Change intent is stated explicitly (clear purpose, no scope creep). | MINOR |
| RC-ENG-006 | Code stays consistent with surrounding style/structure. | MINOR |
| RC-ENG-007 | On every change to a public function/class, update its interface doc (signature, params, returns, examples) so docs never drift. | MAJOR |

### Interface documentation (self-maintained) — `RC-ENG-007`

Interface docs are a *live artifact*, not a one-off writeup. The skill does not
auto-generate a separate API file; instead the Agent keeps the docstring on
every public symbol in sync with the code as it edits:

- **Where it lives**: the docstring on the function/class itself (and, for the
  scaffold, per-module docstrings in `src/`). Enforced by `GP-DOC` / `PL-DOC` / `RC-SP-002`.
- **What to record**: signature, params (`:param x:`), returns (`:return:`),
  raises, and a runnable example (doctest) where useful. Keep parallel to the
  change — a renamed arg, new return field, or changed default all update the
  doc in the same edit.
- **Drift is a MAJOR smell**: a public API whose docstring no longer matches
  its signature fails `RC-ENG-007`. The Agent fixes the doc in the same pass as
  the code, so a generated API page always reflects the current interface.
- Optional: if the project keeps a standalone `docs/api.md`, update the matching entry on change.

## 2. Scientific-Python idiom (SCIENCE — `RC-SP-*`)

Distilled from the Scientific Python Developer Guide and the NumPy / SciPy /
scikit-learn ecosystem.

**What they enforce**
- **API design** — small, consistent, composable interfaces; sensible defaults.
- **Documentation** — every public symbol documented; doctests where useful.
- **Testing** — unit + regression tests; benchmarks for numerical routines.
- **Contribution flow** — small, reviewable changes; clear intent.
- **Packaging** — ship as an installable package (setuptools / hatchling /
  meson-python); keep source importable (`pip install -e .` or `rootutils.setup_root`).
- **Style checking** — automated formatters/linters (black / isort / ruff /
  flake8) in CI so style is not argued by hand.
- **Static typing** — type annotations checked with mypy/pyright in CI.
- **Continuous Integration** — pytest + pre-commit + type checks on every
  change; the `scientific-python/cookie` template generates a repo with nine
  build backends and Nox-tested CI.
- **Repo review** — `sp-repo-review` audits a repo against the guide's checks.

### The Estimator API (scikit-learn idiom)

The single most important convention for ML code here:

```python
model.fit(X, y)        # learn from data
model.predict(X)        # infer on new data
```
NOT ad-hoc names like `model.train_magic()`. Any model exposed to users should
follow `fit` / `predict` (plus `transform` / `fit_transform` for transformers,
`score` for evaluators). This keeps the lab's models interchangeable and familiar.

### Rule cards

| Code | Rule | Severity |
|------|------|----------|
| RC-SP-001 | Public estimators expose `fit(X, y)` / `predict(X)` (sklearn idiom). | MAJOR |
| RC-SP-002 | Public functions/classes carry docstrings + type hints (API design). | MAJOR |
| RC-SP-003 | Numerical routines include a unit/regression test. | MAJOR |
| RC-SP-004 | Benchmarkable numeric code ships a benchmark or timing test. | MINOR |
| RC-SP-005 | Public API changes are small, documented, reviewable. | MINOR |
| RC-SP-006 | Transformers expose `transform` / `fit_transform`. | MINOR |
| RC-SP-007 | Project ships as an installable package; CI runs style + type checks. | MINOR |

## Synergy & cross-links

- `RC-ENG-001` (doc on every public symbol) overlaps `GP-DOC` / `PL-DOC` —
  apply the most specific code (the `RC-ENG-*` when it is about the *process*
  of keeping docs in sync; `GP-DOC`/`PL-DOC` for the mechanical presence).
- `RC-ENG-003` (tests) reinforces the `pytest tests/` quality gate.
- `RC-ENG-002`/`RC-SP-005` are the same "small, reviewable, documented change"
  idea from the process and the idiom sides.
- `RC-SP-007` (installable package + CI style/type) is what makes `RC-ENG-*`
  reviewable in practice — CI runs black/isort/ruff/mypy/pytest so style is not
  argued by hand.
- Review flow ties to `RC-VER-*` (tagged, branch-based releases).

## Authoritative links

- SWE at Google (book): https://abseil.io/resources/swe-book
- Google Eng Practices: https://google.github.io/eng-practices/
- Scientific Python Dev Guide: https://learn.scientific-python.org/development/
- sp-repo-review: https://github.com/scientific-python/repo-review
- cookie template: https://github.com/scientific-python/cookie
