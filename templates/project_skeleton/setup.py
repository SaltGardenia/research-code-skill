from setuptools import find_packages, setup

setup(
    name="<project>",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.10",
    install_requires=[
        "pytorch-lightning",
        "hydra-core",
        "rootutils",
        "omegaconf",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "ruff",
            "mypy",
            "pytest",
            "pre-commit",
        ],
    },
)
