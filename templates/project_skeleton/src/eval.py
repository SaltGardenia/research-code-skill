"""Evaluation entrypoint for <project>."""
from __future__ import annotations

import hydra
import rootutils
from omegaconf import DictConfig

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

from src.utils.utils import extras, task_wrapper  # noqa: E402


@hydra.main(version_base="1.3", config_path="../configs", config_name="eval")
def main(cfg: DictConfig) -> None:
    """Evaluate a checkpoint on the test set."""
    extras(cfg)
    with task_wrapper(cfg):
        from src.models.components.<Project>Model import <Project>Model
        from src.data.components.<Project>DataModule import <Project>DataModule
        import pytorch_lightning as pl

        datamodule = hydra.utils.instantiate(cfg.data)
        model = <Project>Model.load_from_checkpoint(cfg.ckpt_path)
        trainer = hydra.utils.instantiate(cfg.trainer)
        trainer.test(model, datamodule=datamodule)


if __name__ == "__main__":
    main()
