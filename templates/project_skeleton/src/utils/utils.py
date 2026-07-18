"""Utility helpers for <project> (config extras, logging, task wrapper)."""
from __future__ import annotations

import logging
from contextlib import contextmanager
from functools import wraps
from typing import Callable

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)


def extras(cfg: DictConfig) -> None:
    """Apply extra utilities from config (e.g. debug flags)."""
    log.info("Applying config extras: %s", cfg.get("extras", {}))


@contextmanager
def task_wrapper(cfg: DictConfig):
    """Wrap a task with logging of start/end and the composed config."""
    log.info("Starting task: %s", cfg.get("task_name", "task"))
    yield
    log.info("Task finished.")


def task_wrapper_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(cfg: DictConfig, *args, **kwargs):
        with task_wrapper(cfg):
            return func(cfg, *args, **kwargs)

    return wrapper
