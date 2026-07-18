# Research Code Reviewer

> An AI-agent skill that enforces research-grade Python/ML code standards, distilled
> from four authoritative references into one actionable review workflow.

## What it does

`research-code-reviewer` turns an AI agent into a strict but helpful reviewer for
scientific / deep-learning codebases. It checks code and configuration against:

| Reference | Enforced concern |
|-----------|------------------|
| **Lightning-Hydra-Template** | Project directory structure & MLOps layout |
| **PyTorch Lightning Style Guide** | `LightningModule` / `LightningDataModule` design |
| **Google Python Style Guide** | General Python formatting & idioms |
| **Hydra** | Hierarchical, composable, overridable configs |

## Directory layout

```
research-code-reviewer/
├── SKILL.md            # Core entry: triggers, procedure, output format
├── README.md           # This file
├── requirements.txt    # Script dependencies
├── scripts/
│   └── audit_style.py  # Heuristic PYSTYLE/LIGHTNING checker
├── references/
│   ├── lightning_hydra_template.md
│   ├── pytorch_lightning_style.md
│   ├── google_python_style.md
│   └── hydra_config.md
├── templates/
│   └── project_skeleton/   # Files copied in scaffold mode
└── examples/
    ├── review_request.md   # Sample agent invocation
    └── sample_report.md    # Expected output
```

## How to invoke (agent)

Tell the agent one of:

- "Review `<path>` against research code standards."
- "Make this DL repo reproducible / follow best practices."
- "Audit the configs in `configs/` and the `LightningModule` in `src/models/`."
- "Scaffold a clean research project at `<path>`."

The agent loads `SKILL.md` and follows the Procedure, then returns the fixed
Markdown report defined in the skill's Output Format.

## Quickstart for humans

Run the bundled audit on a repo:

```bash
pip install -r requirements.txt
python scripts/audit_style.py path/to/repo
```

This prints the same finding table the skill produces, useful for CI.

## References used

- `lightning-hydra-template` (ashleve) — structure & MLOps conventions.
- PyTorch Lightning official Style Guide.
- Google Python Style Guide (pyguide).
- Hydra (facebookresearch) configuration patterns.
