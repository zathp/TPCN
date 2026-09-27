from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import torch

from tpcn.signal_copy_distance.checkpoint import load_signal_copy_checkpoint
from tpcn.signal_copy_distance.data import generate_visual_pattern, make_visual_grids


ROOT = Path(__file__).resolve().parent


def _all_signal_copy_ckpts() -> list[Path]:
    return sorted(
        (ROOT / "checkpoints").glob("tpcn_signal_copy_distance_epoch_*.pt"),
        key=lambda p: p.stat().st_mtime,
    )


def _best_checkpoint(override: str | None) -> Path:
    if override:
        return Path(override)
    ckpts = _all_signal_copy_ckpts()
    if not ckpts:
        raise FileNotFoundError("No signal_copy checkpoints found in checkpoints/")

    best, best_loss = None, float("inf")
    for p in ckpts:
        try:
            d = torch.load(p, map_location="cpu", weights_only=False)
            l = float(d.get("loss", float("inf")))
            if l < best_loss:
                best_loss, best = l, p
        except Exception:
            continue

    if best is None:
        best = ckpts[-1]
    print(f"Using checkpoint: {best.name} (loss={best_loss:.6f})")
    return best


def _to_rgb_heat(img: np.ndarray, vmin: float, vmax: float) -> np.ndarray:
    x = (img - vmin) / max(vmax - vmin, 1e-8)
    x = np.clip(x, 0.0, 1.0)
    r = np.clip(2.0 * x - 0.2, 0.0, 1.0)
    b = np.clip(1.2 - 2.0 * x, 0.0, 1.0)
    g = np.clip(1.0 - np.abs(2.0 * x - 1.0), 0.0, 1.0)
    rgb = np.stack((r, g, b), axis=-1)
    return (rgb * 255.0).astype(np.uint8)


def _blit_image(
    pygame_mod,
    surface,
    img: np.ndarray,
    x: int,
    y: int,
    width: int,
    height: int,
    vmin: float,
    vmax: float,
) -> None:
    rgb = _to_rgb_heat(img, vmin=vmin, vmax=vmax)
    rgb_swapped = np.transpose(rgb, (1, 0, 2))
    surf = pygame_mod.surfarray.make_surface(rgb_swapped)
    surf = pygame_mod.transform.scale(surf, (width, height))
    surface.blit(surf, (x, y))


def _render_text(pygame_mod, surface, font, text: str, x: int, y: int, color=(220, 220, 220)) -> None:
    t = font.render(text, True, color)
    surface.blit(t, (x, y))


def run_gui(args: argparse.Namespace) -> int:
    try:
        import pygame  # type: ignore
    except Exception as ex:
        print("pygame is required for this GUI. Install with: pip install pygame")
        print(f"Import error: {ex}")
        return 2

    device = torch.device("cpu" if args.cpu or not torch.cuda.is_available() else "cuda")
    ckpt = _best_checkpoint(args.ckpt)
    model, cfg, payload = load_signal_copy_checkpoint(ckpt, device)

    height = int(cfg.visual_height)
    width = int(cfg.visual_width)
    travel = int(payload.get("travel_steps", 12))
    tonic_strength = float(cfg.tonic_strength)
    tonic_vacancy_scale = float(cfg.tonic_vacancy_scale)
    tonic = model.compute_tonic(tonic_strength, tonic_vacancy_scale).unsqueeze(0) if tonic_strength > 0 else None

    n_neurons = int(model.n_neurons)
    gx, gy = make_visual_grids(height, width, device)

    h_state = torch.zeros(1, n_neurons, device=device)
    history = torch.zeros(travel + 1, height * width, device=device)
    ptr = 0

    panel_scale = max(8, int(args.scale))
    panel_w = width * panel_scale
    panel_h = height * panel_scale

    neu_cols = int(math.ceil(math.sqrt(n_neurons)))
    neu_rows = int(math.ceil(n_neurons / max(neu_cols, 1)))
    neu_cell = max(4, panel_scale // 2)
    neu_w = neu_cols * neu_cell
    neu_h = neu_rows * neu_cell

    margin = 16
    top_h = 36
    gap = 12

    win_w = (margin * 2) + (panel_w * 3) + (gap * 2)
    win_w = max(win_w, (margin * 2) + neu_w)
    win_h = top_h + margin + panel_h + gap + neu_h + margin

    pygame.init()
    pygame.display.set_caption("TPCN Signal-Copy Neuron GUI")
    screen = pygame.display.set_mode((win_w, win_h))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)
    small = pygame.font.SysFont("consolas", 14)

    running = True
    step_idx = 0
    mae_ema = 0.0

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False

        with torch.no_grad():
            x_t = generate_visual_pattern(
                step_idx=step_idx,
                stage=int(args.stage),
                height=height,
                width=width,
                grid_x=gx,
                grid_y=gy,
                device=device,
            ).unsqueeze(0)

            history[ptr] = x_t[0]
            target = history[(ptr + 1) % history.shape[0]]
            ptr = (ptr + 1) % history.shape[0]

            h_state, y_t = model.step(x_t, h_state, tonic)
            h_state = h_state.detach()

            err = (y_t[0] - target).abs()
            mae = float(err.mean().item())
            mae_ema = (0.95 * mae_ema) + (0.05 * mae)

        x_img = x_t[0].detach().cpu().numpy().reshape(height, width)
        y_img = y_t[0].detach().cpu().numpy().reshape(height, width)
        e_img = err.detach().cpu().numpy().reshape(height, width)
        h_np = h_state[0].detach().cpu().numpy()

        screen.fill((12, 12, 14))

        _render_text(pygame, screen, font, f"TPCN Signal-Copy | step={step_idx} | MAE={mae:.4f} | EMA={mae_ema:.4f}", margin, 8)

        p1x = margin
        p2x = p1x + panel_w + gap
        p3x = p2x + panel_w + gap
        py = top_h

        _blit_image(pygame, screen, x_img, p1x, py, panel_w, panel_h, vmin=-1.0, vmax=1.0)
        _blit_image(pygame, screen, y_img, p2x, py, panel_w, panel_h, vmin=-1.0, vmax=1.0)
        _blit_image(pygame, screen, e_img, p3x, py, panel_w, panel_h, vmin=0.0, vmax=2.0)

        _render_text(pygame, screen, small, "Input", p1x, py - 18)
        _render_text(pygame, screen, small, "Output", p2x, py - 18)
        _render_text(pygame, screen, small, "Abs Error", p3x, py - 18)

        ny = py + panel_h + gap
        _render_text(pygame, screen, small, f"Neuron Activity ({n_neurons})", margin, ny - 18)

        for i in range(n_neurons):
            r = i // neu_cols
            c = i % neu_cols
            v = float(h_np[i])
            color = _to_rgb_heat(np.array([[v]], dtype=np.float32), vmin=-1.0, vmax=1.0)[0, 0]
            rect = pygame.Rect(margin + c * neu_cell, ny + r * neu_cell, neu_cell - 1, neu_cell - 1)
            pygame.draw.rect(screen, (int(color[0]), int(color[1]), int(color[2])), rect)

        pygame.display.flip()
        clock.tick(max(1, int(args.fps)))

        step_idx += 1
        if args.steps > 0 and step_idx >= int(args.steps):
            running = False

    pygame.quit()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Realtime pygame GUI for TPCN signal-copy checkpoints.")
    p.add_argument("--ckpt", default=None, help="Checkpoint path (auto-selects best-loss if omitted).")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--steps", type=int, default=0, help="Number of steps to run (0 = run until closed).")
    p.add_argument("--scale", type=int, default=24, help="Pixels per signal cell in input/output/error panels.")
    p.add_argument("--stage", type=int, default=2, choices=[0, 1, 2], help="Pattern stage for generated signal input.")
    p.add_argument("--cpu", action="store_true", help="Force CPU inference.")
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run_gui(args)


if __name__ == "__main__":
    raise SystemExit(main())
