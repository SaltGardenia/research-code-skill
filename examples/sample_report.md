# Example: conformance report (gate output)

When `scripts/audit_style.py` is run as a confirmation gate (not as the skill's
primary purpose), it emits the fixed Markdown table from SKILL.md. This is the
expected result of the trigger in `examples/review_request.md` after the agent
has written conforming code into `./my_project`.

```markdown
# Research Code Conformance: ./my_project

## Summary
- Files scanned: 14
- Findings: 1 (BLOCKER: 0, MAJOR: 0, MINOR: 1)

## Findings
| ID | Category | Severity | File:Line | Rule | Suggestion |
|----|----------|----------|-----------|------|------------|
| F1 | PYSTYLE | MINOR | src/models/cifar_module.py:88 | GP-LEN | Line 84>80 chars; wrap it (or set 99 in pyproject). |

## Next Steps
- Either wrap the long line or set the project line-length override to 99.
```

## How to reproduce

```bash
pip install -r requirements.txt
python scripts/audit_style.py ./my_project
```

Exit code `0` means no BLOCKER (conventions hold well enough to proceed);
`1` means at least one BLOCKER must be fixed before the change is accepted.
