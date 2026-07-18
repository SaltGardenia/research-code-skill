# Example: agent invocation (enforcing conventions in context)

This file shows how an agent uses `research-code-skill` as a **contextual coding
standard enforcer** — applying conventions as it builds or tidies a project,
not reviewing after the fact. The skill has two core scenarios (see SKILL.md).

## Scenario A — Build from zero (greenfield)

```
Scaffold a new research project at ./new_project so it follows the lab's
coding standard from day one, then add a ResNet backbone and a LightningModule
that trains it on CIFAR (right src/ dirs, Google/PL names, Hydra _target_).
```

The agent scaffolds from `templates/project_skeleton/` and writes every new
file to the conventions (`LHT-*`, `HY-*`, `PL-*`, `GP-*`).

## Scenario B — Tidy an existing repository

```
Refactor ./legacy_exp so it follows the standard: move code into src/data,
src/models, src/utils and configs/<group>/, convert the argparse flags in
train.py into Hydra configs, split the model from the LightningModule, and
rename symbols per the naming rules. Preserve training behavior.
```

The agent audits with `scripts/audit_style.py`, then restructures/renames to
conformance, then re-runs the gate.

## What the agent does (instead of reviewing)

1. Loads the matching `references/` file for the concern (e.g. `PL-*` for a
   module, `HY-*` for a config, `GP-*` for naming).
2. Writes/moves the code to match the convention (correct directory, class
   shape, `_target_` config, `snake_case`/`CapWords` names).
3. Runs `python scripts/audit_style.py <target>` as a confirmation gate.
4. Runs the mandatory quality gate from the project root:
   `black . && isort . && ruff check . && mypy src/ && pytest tests/`.
5. Briefly notes any deliberate deviation using the fixed "Convention applied"
   format from SKILL.md.

## Minimal target the example below was run against

Assume the agent is adding `src/models/components/resnet.py` and
`src/models/cifar_module.py` to `./my_project` (which already has the scaffold
structure). The generated files obey `PL-SYS`, `PL-ORDER`, `PL-METRIC`,
`GP-NAME`, `GP-ANN`. Running `python scripts/audit_style.py ./my_project`
produces the conformance report in `examples/sample_report.md`.
