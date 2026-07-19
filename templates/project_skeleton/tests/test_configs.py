"""Smoke test: composed configs instantiate without error."""
from __future__ import annotations

import os

import hydra
from omegaconf import DictConfig

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "configs")


def test_train_config_compose() -> None:
    """Composing the train config must not raise."""
    with hydra.initialize_config_dir(config_dir=CONFIG_DIR, version_base="1.3"):
        cfg = hydra.compose(config_name="train")
    assert cfg is not None
