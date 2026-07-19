# <project>

A research (ML/DL) project scaffolded with the research-code-skill standard,
following the Lightning-Hydra-Template layout.

## Structure

- `configs/` — Hydra configs grouped by concern
- `src/` — `data/`, `models/`, `utils/` plus `train.py` / `eval.py` entrypoints
- `data/`, `logs/`, `notebooks/` — data, run outputs, exploration (git-ignored where appropriate)
- `scripts/`, `tests/` — launch scripts and smoke/unit tests

## Quick start

```bash
pip install -e .
python src/train.py
```
