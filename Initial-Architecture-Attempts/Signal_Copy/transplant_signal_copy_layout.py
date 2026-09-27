from __future__ import annotations

import argparse
from pathlib import Path

import torch

from tpcn.signal_copy_distance.checkpoint import load_signal_copy_checkpoint
from tpcn.signal_copy_distance.space import make_contiguous_layout, make_layout_from_indices, parse_index_spec


ROOT = Path(__file__).resolve().parent


def main() -> int:
    p = argparse.ArgumentParser(description="Transplant a trained signal-copy model into a new neuron space/IO arrangement.")
    p.add_argument("--source-ckpt", required=True, help="Path to source checkpoint.")
    p.add_argument("--target-n-neurons", type=int, required=True)
    p.add_argument("--target-input-width", type=int, required=True)
    p.add_argument("--target-output-width", type=int, required=True)
    p.add_argument("--target-virtual-distance", type=int, default=32)
    p.add_argument("--target-local-radius", type=int, default=2)
    p.add_argument("--target-input-indices", type=str, default=None, help="Explicit input neuron indices, e.g. 0,1,8-12")
    p.add_argument("--target-output-indices", type=str, default=None, help="Explicit output neuron indices, e.g. 90,91,120-127")
    p.add_argument("--out", required=True, help="Path to output transplanted checkpoint.")
    p.add_argument("--cpu", action="store_true")
    args = p.parse_args()

    device = torch.device("cpu" if args.cpu or not torch.cuda.is_available() else "cuda")
    model, cfg, payload = load_signal_copy_checkpoint(Path(args.source_ckpt), device)

    target_n_neurons = max(4, int(args.target_n_neurons))
    target_local_radius = max(0, int(args.target_local_radius))
    if args.target_input_indices is not None or args.target_output_indices is not None:
        if args.target_input_indices is None or args.target_output_indices is None:
            raise ValueError("Both --target-input-indices and --target-output-indices must be set together")
        target_layout = make_layout_from_indices(
            n_neurons=target_n_neurons,
            local_radius=target_local_radius,
            input_indices=parse_index_spec(args.target_input_indices),
            output_indices=parse_index_spec(args.target_output_indices),
        )
    else:
        target_layout = make_contiguous_layout(
            n_neurons=target_n_neurons,
            input_width=max(1, int(args.target_input_width)),
            output_width=max(1, int(args.target_output_width)),
            virtual_distance=max(0, int(args.target_virtual_distance)),
            local_radius=target_local_radius,
        )

    transplanted = model.transplant_to_layout(
        target_layout=target_layout,
        signal_dim=int(cfg.signal_dim),
        device=device,
    )

    cfg_out = dict(payload.get("config", {}))
    cfg_out["n_neurons"] = int(target_layout.n_neurons)
    cfg_out["input_width"] = int(target_layout.input_indices.numel())
    cfg_out["output_width"] = int(target_layout.output_indices.numel())
    cfg_out["virtual_distance"] = int(target_layout.effective_distance())
    cfg_out["local_radius"] = int(target_layout.local_radius)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    torch.save(
        {
            "epoch": int(payload.get("epoch", 0)),
            "model_state": transplanted.state_dict(),
            "optimizer_state": None,
            "loss": float(payload.get("loss", float("nan"))),
            "accum_loss": float(payload.get("accum_loss", float("nan"))),
            "mae": float(payload.get("mae", float("nan"))),
            "travel_steps": int(payload.get("travel_steps", 1)),
            "effective_distance": int(target_layout.effective_distance()),
            "recurrent_edges": transplanted.recurrent_edge_count(),
            "recurrent_edge_capacity": transplanted.recurrent_edge_capacity(),
            "config": cfg_out,
            "transplant_meta": {
                "source_checkpoint": str(Path(args.source_ckpt).resolve()),
                "target_layout": {
                    "n_neurons": int(target_layout.n_neurons),
                    "local_radius": int(target_layout.local_radius),
                    "input_indices": target_layout.input_indices.tolist(),
                    "output_indices": target_layout.output_indices.tolist(),
                },
            },
        },
        out_path,
    )

    print(f"Saved transplanted checkpoint: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
