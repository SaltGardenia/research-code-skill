# Template: project skeleton for scaffold mode

Copy these files into an empty target repo when the user asks to initialize a
clean research project. Replace `<project>` with the project name. Do NOT
overwrite existing user files.

The layout below is the **frozen structural skeleton** (identical to the tree in
`references/scaffold_grammar.md` section 1). The directories and fixed-name
files are required and must be present. Config-group entries named `project`
(e.g. `configs/model/project.yaml`) are **group placeholders**: they require the
group directory to contain *at least one* config file — you should add your own
named configs (e.g. `configs/model/resnet.yaml`) and may keep or drop the
literal `project.yaml`. Additional files and configs beyond the skeleton are
permitted (extra models, experiments, data configs, etc.).

- .github/workflows/                 (Github Actions workflows)
- configs/callbacks/default.yaml
- configs/data/project.yaml
- configs/debug/default.yaml
- configs/experiment/example.yaml
- configs/extras/default.yaml
- configs/hparams_search/mnist_optuna.yaml
- configs/hydra/default.yaml
- configs/local/default.yaml
- configs/logger/wandb.yaml
- configs/model/project.yaml
- configs/paths/default.yaml
- configs/trainer/default.yaml
- configs/eval.yaml
- configs/train.yaml
- data/                             (git-ignored)
- logs/                             (git-ignored)
- notebooks/1.0-jqp-explore.ipynb
- scripts/train.sh
- scripts/test.sh
- src/__init__.py
- src/train.py
- src/eval.py
- src/data/__init__.py
- src/data/components/__init__.py
- src/models/__init__.py
- src/models/components/__init__.py
- src/utils/__init__.py
- src/utils/utils.py
- tests/test_configs.py
- .env.example
- .gitignore
- .pre-commit-config.yaml
- .project-root
- environment.yaml
- Makefile
- pyproject.toml
- requirements.txt
- setup.py
- README.md
