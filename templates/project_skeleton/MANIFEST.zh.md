# 模板：用于 scaffold 模式的项骨架

> 本文件是 `templates/project_skeleton/MANIFEST.md` 的中文对照版。智能体运行时仍应加载英文原版。

当用户要求初始化一个干净的科研项目时，把这些文件复制到一个空的目仓库中。把 `<project>` 换成项目名。
**不要覆盖用户既有文件**。

要创建的文件：

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
