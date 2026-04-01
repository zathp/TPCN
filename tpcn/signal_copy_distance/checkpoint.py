from __future__ import annotations

from pathlib import Path

import torch

from .config import SignalCopyConfig
from .model import DistanceSignalCopyNet


def load_signal_copy_checkpoint(ckpt_path: Path | str, device: torch.device) -> tuple[DistanceSignalCopyNet, SignalCopyConfig, dict]:
    d = torch.load(Path(ckpt_path), map_location="cpu", weights_only=False)
    cfg_raw = dict(d["config"])
    cfg = SignalCopyConfig(**cfg_raw)
    ms = d["model_state"]

    model = DistanceSignalCopyNet(
        signal_dim=int(cfg.signal_dim),
        n_neurons=int(cfg.n_neurons),
        alpha=float(cfg.alpha),
        mask_rec=ms["mask_rec"],
        mask_in=ms["mask_in"],
        mask_out=ms["mask_out"],
        struct_mask_rec=ms["struct_mask_rec"],
    )
    model.load_state_dict(ms, strict=True)
    model.to(device)
    model.eval()
    return model, cfg, d