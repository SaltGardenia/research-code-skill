# 模板：scaffold 模式的工程骨架

当用户要求初始化一个干净的科研项目时，将这些文件复制进空目标仓库。把
`<project>` 替换为项目名称。不要覆盖用户已有的文件。

布局与 Lightning-Hydra-Template 完全一致：

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
- data/            （git 忽略）
- logs/            （git 忽略）
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
- .gitignore
- .env.example
- .project-root
