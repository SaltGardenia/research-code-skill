# Reference: Google Python Style Guide (pyguide)

General Python hygiene enforced by this skill. Project config (e.g. Black line
length 99) overrides the Google default (80) when present.

## Language rules
- **Lint**: comply with `pylint`/`flake8` via `pyproject.toml`.
- **Imports**: absolute imports preferred; no wildcard `from x import *`.
- **Packages**: use explicit relative imports within a package.
- **Exceptions**: never use bare `except:`; catch specific exceptions; re-raise
  with `raise ... from e` when wrapping.
- **Mutable global state**: avoid module-level mutable globals.
- **Comprehensions**: okay for simple cases; avoid complex nested ones.
- **Default iterators/operators**: use them (e.g. `for x in seq`, not `range(len)`).
- **Lambda**: one-liners only; prefer `def` for anything nontrivial.
- **Default args**: never use mutable defaults (`def f(x=[])`); use `None`.
- **Properties**: use for computed attrs; avoid heavy work in getters.
- **True/False**: use truthiness; `if foo:` not `if foo == True:`.
- **Decorators**: use sparingly; `@property`, `@classmethod` are fine.
- **Threading**: guard shared state; prefer queues.
- **Type-annotated code**: annotate all signatures (PEP 484).

## Style rules
- **Semicolons**: none.
- **Line length**: <= 80 (or project setting, commonly 99 with Black).
- **Parentheses**: minimize; for line continuation use parentheses, not `\`.
- **Indentation**: 4 spaces; trailing commas allowed in multiline collections.
- **Blank lines**: 2 between top-level defs/classes; 1 between methods.
- **Whitespace**: PEP 8 spacing around operators; no trailing whitespace.
- **Shebang**: `#!/usr/bin/env python3` on executable scripts.
- **Comments/Docstrings**: PEP 257; docstring every public module/class/func.
- **Strings**: use `"` consistently; prefer f-strings; `logging` not `print` for diagnostics.
- **Files/sockets**: close via `with` / context managers.
- **TODO**: `TODO(username): description` format.
- **Imports formatting**: stdlib, third-party, local; alphabetical within group.
- **Statements**: one per line.
- **Naming**: `snake_case` funcs/vars, `CapWords` classes, `UPPER_CASE` constants;
  avoid `l`, `I`, `O`.
- **Main**: guard with `if __name__ == "__main__":`.
- **Function length**: keep short; extract helpers.
