"""Live side-by-side visualisation of the best signal-copy model.

Finds the checkpoint with the lowest recorded loss under checkpoints/,
reconstructs the model, and displays a matplotlib window with:
  - Left:   input pattern  (H x W grid)
  - Centre: output pattern (H x W grid)
  - Right:  absolute error (H x W grid)
  - Bottom: running MAE trace

Run:
    python viz_signal_copy.py [--ckpt PATH] [--fps N] [--steps N] [--cpu]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

from tpcn.signal_copy_distance.checkpoint import load_signal_copy_checkpoint
from tpcn.signal_copy_distance.data import generate_visual_pattern, make_visual_grids

ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def _all_signal_copy_ckpts():
    return sorted(
        (ROOT / "checkpoints").glob("tpcn_signal_copy_distance_epoch_*.pt"),
        key=lambda p: p.stat().st_mtime,
    )


def _best_checkpoint(override: str | None):
    if override:
        return Path(override)
    ckpts = _all_signal_copy_ckpts()
    if not ckpts:
        print("No signal_copy checkpoints found in checkpoints/", file=sys.stderr)
        sys.exit(1)
    best, best_loss = None, float("inf")
    for p in ckpts:
        try:
            d = torch.load(p, map_location="cpu", weights_only=False)
            l = float(d.get("loss", float("inf")))
            if l < best_loss:
                best_loss, best = l, p
        except Exception:
            pass
    if best is None:
        best = ckpts[-1]
    print(f"Using checkpoint: {best.name}  (loss={best_loss:.6f})")
    return best


# ---------------------------------------------------------------------------
# Main visualiser loop
# ---------------------------------------------------------------------------

def run_viz(args):
    device = torch.device("cpu" if args.cpu or not torch.cuda.is_available() else "cuda")
    ckpt   = _best_checkpoint(args.ckpt)
    model, cfg, d = load_signal_copy_checkpoint(ckpt, device)

    height = int(cfg.visual_height)
    width  = int(cfg.visual_width)
    travel = int(d.get("travel_steps", 12))
    ts     = float(cfg.tonic_strength)
    tvs    = float(cfg.tonic_vacancy_scale)

    tonic = model.compute_tonic(ts, tvs).unsqueeze(0) if ts > 0 else None

    gx, gy = make_visual_grids(height, width, device)
    n_neurons = model.n_neurons

    h       = torch.zeros(1, n_neurons, device=device)
    history = torch.zeros(travel + 1, height * width, device=device)
    ptr     = 0
    mae_trace: list[float] = []

    # -----------------------------------------------------------------------
    # Build figure
    # -----------------------------------------------------------------------
    matplotlib.use("TkAgg" if "tkinter" in sys.modules else "Qt5Agg")
    fig = plt.figure(figsize=(12, 6), facecolor="#0e0e0e")
    gs  = gridspec.GridSpec(
        2, 4, figure=fig,
        height_ratios=[3, 1],
        hspace=0.35, wspace=0.30,
        left=0.06, right=0.97, top=0.90, bottom=0.08,
    )

    ax_in  = fig.add_subplot(gs[0, 0])
    ax_out = fig.add_subplot(gs[0, 1])
    ax_err = fig.add_subplot(gs[0, 2])
    ax_net = fig.add_subplot(gs[0, 3])
    ax_mae = fig.add_subplot(gs[1, :])

    for ax in (ax_in, ax_out, ax_err, ax_net):
        ax.set_xticks([])
        ax.set_yticks([])

    vkw = dict(vmin=-1.0, vmax=1.0, cmap="RdBu_r", interpolation="nearest", aspect="auto")
    im_in  = ax_in.imshow(np.zeros((height, width)), **vkw)
    im_out = ax_out.imshow(np.zeros((height, width)), **vkw)
    im_err = ax_err.imshow(np.zeros((height, width)), vmin=0.0, vmax=2.0,
                            cmap="hot", interpolation="nearest", aspect="auto")

    # neuron activity strip (1-D spatial layout, no 2-D shape assumed)
    strip_w = min(n_neurons, 256)
    im_net = ax_net.imshow(np.zeros((1, strip_w)), vmin=-1.0, vmax=1.0,
                            cmap="seismic", interpolation="nearest", aspect="auto")

    ax_in.set_title("INPUT",  color="white", fontsize=9)
    ax_out.set_title("OUTPUT (predicted)", color="white", fontsize=9)
    ax_err.set_title("|ERROR|", color="white", fontsize=9)
    ax_net.set_title("NEURON ACTIVITY", color="white", fontsize=9)

    (line_mae,) = ax_mae.plot([], [], color="#00e5ff", lw=1.0)
    ax_mae.set_facecolor("#141414")
    ax_mae.tick_params(colors="grey")
    ax_mae.set_ylabel("MAE", color="grey", fontsize=8)
    ax_mae.set_xlabel("step", color="grey", fontsize=8)
    ax_mae.set_xlim(0, max(args.steps, 1))
    ax_mae.set_ylim(0, 2.0)
    for ax in (ax_in, ax_out, ax_err, ax_net):
        ax.set_facecolor("#1a1a1a")
    fig.patch.set_facecolor("#0e0e0e")

    epoch_tag = ckpt.stem.split("_epoch_")[-1] if "_epoch_" in ckpt.stem else "?"
    fig.suptitle(
        f"Signal Copy Model  |  epoch={epoch_tag}  |  "
        f"neurons={n_neurons}  travel_steps={travel}",
        color="white", fontsize=10,
    )

    plt.ion()
    plt.show(block=False)

    stage = 2  # Show hardest patterns in viz

    n_total = args.steps if args.steps > 0 else 10_000_000

    for step_idx in range(n_total):
        x_t = generate_visual_pattern(step_idx, stage, height, width, gx, gy, device).unsqueeze(0)
        history[ptr] = x_t[0]
        target = history[(ptr + 1) % history.shape[0]]
        ptr = (ptr + 1) % history.shape[0]

        h, y_t = model.step(x_t, h, tonic)
        h = h.detach()

        residual = (y_t[0] - target).abs()
        mae = float(residual.mean().item())
        mae_trace.append(mae)

        x_np   = x_t[0].cpu().numpy().reshape(height, width)
        y_np   = y_t[0].cpu().numpy().reshape(height, width)
        err_np = residual.cpu().numpy().reshape(height, width)

        # neuron strip (subsample)
        h_np   = h[0].cpu().numpy()
        step_s = max(1, n_neurons // strip_w)
        strip  = h_np[::step_s][:strip_w].reshape(1, -1)

        im_in.set_data(x_np)
        im_out.set_data(y_np)
        im_err.set_data(err_np)
        im_net.set_data(strip)

        xs = list(range(len(mae_trace)))
        line_mae.set_data(xs, mae_trace)
        if len(mae_trace) > 200:
            ax_mae.set_xlim(len(mae_trace) - 200, len(mae_trace))
        cur_max = max(max(mae_trace[-200:], default=0.1) * 1.1, 0.05)
        ax_mae.set_ylim(0, cur_max)
        ax_mae.set_title(f"MAE={mae:.4f}", color="grey", fontsize=8)

        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        time.sleep(max(0.0, 1.0 / max(args.fps, 1)))

        if not plt.fignum_exists(fig.number):
            break

    plt.ioff()
    plt.show()


def main():
    p = argparse.ArgumentParser(description="Live side-by-side visualisation of best signal-copy model.")
    p.add_argument("--ckpt",  default=None, help="Explicit checkpoint path (auto-selects lowest loss if omitted).")
    p.add_argument("--fps",   type=int,   default=10,  help="Target frame rate.")
    p.add_argument("--steps", type=int,   default=0,   help="Number of steps to run (0 = run until window closed).")
    p.add_argument("--cpu",   action="store_true", help="Force CPU inference.")
    run_viz(p.parse_args())


if __name__ == "__main__":
    main()
