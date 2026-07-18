# Template: project skeleton for scaffold mode

Copy these files into an empty target repo when the user asks to initialize a
clean research project. Replace `<project>` with the project name. Do NOT
overwrite existing user files.

Files to create:
- configs/train.yaml
- configs/eval.yaml
- configs/model/<project>.yaml
- configs/data/<project>.yaml
- configs/trainer/default.yaml
- configs/logger/wandb.yaml
- configs/paths/default.yaml
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
- .gitignore
- .env.example
- .project-root
