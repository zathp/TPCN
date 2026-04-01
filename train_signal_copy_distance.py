from __future__ import annotations

from pathlib import Path

from tpcn.signal_copy_distance.config import build_arg_parser, config_from_args
from tpcn.signal_copy_distance.trainer import train_signal_copy_distance


ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    cfg = config_from_args(args)

    ckpt_dir = ROOT / "checkpoints"
    return train_signal_copy_distance(
        cfg=cfg,
        checkpoint_dir=ckpt_dir,
        checkpoint_prefix="tpcn_signal_copy_distance",
    )


if __name__ == "__main__":
    raise SystemExit(main())
