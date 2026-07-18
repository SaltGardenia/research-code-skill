"""Training entrypoint for <project>.

Instantiates config objects with Hydra and runs a PyTorch Lightning Trainer.
"""
from __future__ import annotations

import hydra
import rootutils
from omegaconf import DictConfig

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

from src.utils.utils import extras, task_wrapper  # noqa: E402


@hydra.main(version_base="1.3", config_path="../configs", config_name="train")
def main(cfg: DictConfig) -> None:
    """Run the training pipeline defined by the composed config."""
    extras(cfg)
    with task_wrapper(cfg):
        from src.models.components.<Project>Model import <Project>Model
        from src.data.components.<Project>DataModule import <Project>DataModule
        import pytorch_lightning as pl

        datamodule = hydra.utils.instantiate(cfg.data)
        model = hydra.utils.instantiate(cfg.model)
        trainer = hydra.utils.instantiate(cfg.trainer)
        trainer.fit(model, datamodule=datamodule, ckpt_path=cfg.ckpt_path)
        if cfg.get("test"):
            trainer.test(model, datamodule=datamodule)


if __name__ == "__main__":
    main()
