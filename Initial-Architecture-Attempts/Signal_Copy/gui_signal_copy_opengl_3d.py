from __future__ import annotations

import argparse
import math
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


def _jet_color(v: np.ndarray) -> np.ndarray:
    x = np.clip((v + 1.0) * 0.5, 0.0, 1.0)
    r = np.clip(1.5 - np.abs(4.0 * x - 3.0), 0.0, 1.0)
    g = np.clip(1.5 - np.abs(4.0 * x - 2.0), 0.0, 1.0)
    b = np.clip(1.5 - np.abs(4.0 * x - 1.0), 0.0, 1.0)
    return np.stack((r, g, b), axis=1).astype(np.float32)


def _build_neuron_positions(n: int, radius: float = 6.0) -> np.ndarray:
    idx = np.arange(n, dtype=np.float32) + 0.5
    phi = np.arccos(1.0 - 2.0 * idx / max(float(n), 1.0))
    theta = math.pi * (1.0 + 5.0 ** 0.5) * idx
    x = radius * np.cos(theta) * np.sin(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(phi)
    return np.stack((x, y, z), axis=1).astype(np.float32)


def _sample_edges(mask_rec: torch.Tensor, struct_rec: torch.Tensor, w_rec: torch.Tensor, max_edges: int) -> np.ndarray:
    with torch.no_grad():
        active = (mask_rec > 0.5) & (struct_rec > 0.5)
        src, dst = torch.nonzero(active, as_tuple=True)
        if src.numel() == 0:
            return np.zeros((0, 3), dtype=np.float32)

        vals = w_rec[src, dst]
        pairs = torch.stack((src, dst, vals), dim=1)
        if pairs.shape[0] > max_edges:
            sel = torch.randperm(pairs.shape[0], device=pairs.device)[:max_edges]
            pairs = pairs[sel]

        return pairs.detach().cpu().numpy().astype(np.float32)


def _draw_text_2d(pygame_mod, text: str, x: int, y: int, color=(220, 220, 220)) -> None:
    font = pygame_mod.font.SysFont("consolas", 16)
    surf = font.render(text, True, color)
    rgba = pygame_mod.image.tostring(surf, "RGBA", True)
    from OpenGL.GL import glWindowPos2d, glDrawPixels, GL_RGBA, GL_UNSIGNED_BYTE

    glWindowPos2d(x, y)
    glDrawPixels(surf.get_width(), surf.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, rgba)


def run_gui(args: argparse.Namespace) -> int:
    try:
        import pygame  # type: ignore
        from pygame.locals import DOUBLEBUF, OPENGL
    except Exception as ex:
        print("pygame is required. Install with: pip install pygame")
        print(f"Import error: {ex}")
        return 2

    try:
        from OpenGL.GL import (
            glBegin,
            glBlendFunc,
            glClear,
            glClearColor,
            glColor3f,
            glColor4f,
            glDisable,
            glEnable,
            glEnd,
            glLineWidth,
            glLoadIdentity,
            glMatrixMode,
            glPointSize,
            glVertex3f,
            GL_BLEND,
            GL_COLOR_BUFFER_BIT,
            GL_DEPTH_BUFFER_BIT,
            GL_DEPTH_TEST,
            GL_LINES,
            GL_MODELVIEW,
            GL_ONE_MINUS_SRC_ALPHA,
            GL_POINTS,
            GL_PROJECTION,
            GL_SRC_ALPHA,
        )
        from OpenGL.GLU import gluLookAt, gluPerspective
    except Exception as ex:
        print("PyOpenGL is required. Install with: pip install PyOpenGL PyOpenGL_accelerate")
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

    positions = _build_neuron_positions(n_neurons, radius=float(args.radius))
    edge_pairs = _sample_edges(
        model.mask_rec,
        model.struct_mask_rec,
        model.w_rec,
        max_edges=max(0, int(args.max_edges)),
    )

    in_idx = set(torch.nonzero(model.mask_in[0] > 0.5, as_tuple=False).flatten().cpu().tolist())
    out_idx = set(torch.nonzero(model.mask_out[:, 0] > 0.5, as_tuple=False).flatten().cpu().tolist())

    pygame.init()
    pygame.display.set_caption("TPCN OpenGL 3D Neuron Viewer")
    screen = pygame.display.set_mode((int(args.width), int(args.height)), DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.04, 0.04, 0.05, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = max(float(args.width) / max(float(args.height), 1.0), 1e-3)
    gluPerspective(55.0, aspect, 0.1, 200.0)

    yaw = 0.0
    pitch = 0.0
    dist = 18.0
    running = True
    paused = False
    step_idx = 0
    mae_ema = 0.0

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_SPACE:
                    paused = not paused

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            yaw -= 1.2
        if keys[pygame.K_RIGHT]:
            yaw += 1.2
        if keys[pygame.K_UP]:
            pitch = min(89.0, pitch + 1.0)
        if keys[pygame.K_DOWN]:
            pitch = max(-89.0, pitch - 1.0)
        if keys[pygame.K_w]:
            dist = max(5.0, dist - 0.2)
        if keys[pygame.K_s]:
            dist = min(80.0, dist + 0.2)

        if not paused:
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
                step_idx += 1

        h_np = h_state[0].detach().cpu().numpy().astype(np.float32)
        colors = _jet_color(h_np)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        ry = math.radians(yaw)
        rp = math.radians(pitch)
        cx = dist * math.cos(rp) * math.sin(ry)
        cy = dist * math.sin(rp)
        cz = dist * math.cos(rp) * math.cos(ry)
        gluLookAt(cx, cy, cz, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        if edge_pairs.shape[0] > 0:
            w_abs = np.abs(edge_pairs[:, 2])
            w_max = max(float(np.max(w_abs)), 1e-6)

            # Glow pass: thicker, softer lines with alpha proportional to edge weight.
            glLineWidth(3.5)
            glBegin(GL_LINES)
            for src_f, dst_f, w_f in edge_pairs:
                src = int(src_f)
                dst = int(dst_f)
                p0 = positions[src]
                p1 = positions[dst]
                intensity = min(1.0, max(0.0, abs(float(w_f)) / w_max))
                alpha = 0.03 + (0.24 * intensity)
                glColor4f(0.45, 0.65, 1.00, alpha)
                glVertex3f(float(p0[0]), float(p0[1]), float(p0[2]))
                glVertex3f(float(p1[0]), float(p1[1]), float(p1[2]))
            glEnd()

            # Core pass: sharp lines also weighted by magnitude for crisp structure.
            glLineWidth(1.1)
            glBegin(GL_LINES)
            for src_f, dst_f, w_f in edge_pairs:
                src = int(src_f)
                dst = int(dst_f)
                p0 = positions[src]
                p1 = positions[dst]
                intensity = min(1.0, max(0.0, abs(float(w_f)) / w_max))
                c = 0.15 + (0.85 * intensity)
                glColor4f(c, c, c, 0.85)
                glVertex3f(float(p0[0]), float(p0[1]), float(p0[2]))
                glVertex3f(float(p1[0]), float(p1[1]), float(p1[2]))
            glEnd()

        glPointSize(max(2.0, float(args.point_size)))
        glBegin(GL_POINTS)
        for i in range(n_neurons):
            p = positions[i]
            if i in in_idx:
                glColor3f(0.1, 0.9, 0.2)
            elif i in out_idx:
                glColor3f(1.0, 0.4, 0.1)
            else:
                c = colors[i]
                glColor3f(float(c[0]), float(c[1]), float(c[2]))
            glVertex3f(float(p[0]), float(p[1]), float(p[2]))
        glEnd()

        glDisable(GL_DEPTH_TEST)
        _draw_text_2d(pygame, f"step={step_idx} mae_ema={mae_ema:.4f} edges={edge_pairs.shape[0]} paused={paused}", 10, int(args.height) - 24)
        _draw_text_2d(pygame, "Arrows: orbit  W/S: zoom  Space: pause  Esc: exit", 10, int(args.height) - 44)
        glEnable(GL_DEPTH_TEST)

        pygame.display.flip()
        clock.tick(max(1, int(args.fps)))

        if args.steps > 0 and step_idx >= int(args.steps):
            running = False

    pygame.quit()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OpenGL 3D viewer for TPCN neurons and recurrent links.")
    p.add_argument("--ckpt", default=None, help="Checkpoint path (auto-selects best-loss if omitted).")
    p.add_argument("--fps", type=int, default=60)
    p.add_argument("--steps", type=int, default=0, help="Number of simulation steps (0 = until closed).")
    p.add_argument("--stage", type=int, default=2, choices=[0, 1, 2], help="Pattern stage for generated signal input.")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=800)
    p.add_argument("--radius", type=float, default=6.0, help="Radius of neuron sphere layout.")
    p.add_argument("--point-size", type=float, default=7.0)
    p.add_argument("--max-edges", type=int, default=12000, help="Maximum recurrent links rendered.")
    p.add_argument("--cpu", action="store_true", help="Force CPU inference.")
    return p


def main() -> int:
    parser = build_parser()
    return run_gui(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
