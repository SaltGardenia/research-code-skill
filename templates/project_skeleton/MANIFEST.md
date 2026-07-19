# Template: project skeleton for scaffold mode

Copy these files into an empty target repo when the user asks to initialize a
clean research project. Replace `<project>` with the project name. Do NOT
overwrite existing user files.

Layout matches Lightning-Hydra-Template exactly:

- .github/workflows/ci.yaml
- configs/train.yaml
- configs/eval.yaml
- configs/callbacks/default.yaml
- configs/data/<project>.yaml
- configs/debug/default.yaml
- configs/experiment/example.yaml
- configs/extras/default.yaml
- configs/hparams_search/mnist_optuna.yaml
- configs/hydra/default.yaml
- configs/local/default.yaml
- configs/logger/wandb.yaml
- configs/model/<project>.yaml
- configs/paths/default.yaml
- configs/trainer/default.yaml
- data/            (git-ignored)
- logs/            (git-ignored)
- notebooks/1.0-jqp-explore.ipynb
- scripts/train.sh
- scripts/test.sh
- src/__init__.py
- src/train.py
- src/eval.py
- src/models/__init__.py
- src/models/components/__init__.py
- src/data/__init__.py
- src/utils/__init__.py
- src/utils/utils.py
- tests/test_configs.py
- .pre-commit-config.yaml
- pyproject.toml
- requirements.txt
- setup.py
- environment.yaml
- Makefile
- README.md
- .gitignore
- .env.example
- .project-root
