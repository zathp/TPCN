from __future__ import annotations

import random
import time
from dataclasses import asdict
from pathlib import Path

import torch
from torch.nn import functional as F

from .config import SignalCopyConfig
from .data import compute_loss_drop_pct, make_visual_grids, sample_curriculum_visual_batch
from .model import DistanceSignalCopyNet
from .space import make_contiguous_layout, make_layout_from_indices


def seed_everything(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _print_run_header(
    cfg: SignalCopyConfig,
    model: DistanceSignalCopyNet,
    device: torch.device,
    input_idx: torch.Tensor,
    output_idx: torch.Tensor,
    effective_distance: int,
    travel_steps: int,
) -> None:
    print(f"device={device}")
    print(
        f"n_neurons={cfg.n_neurons} input_width={len(input_idx)} output_width={len(output_idx)} "
        f"effective_distance={effective_distance} local_radius={cfg.local_radius}"
    )
    print(f"propagation_speed={cfg.propagation_speed:.4f} travel_steps={travel_steps}")
    if cfg.enable_pain_onset_gate:
        print(f"pain_onset_gate=enabled warmup_steps={travel_steps}")
    else:
        print("pain_onset_gate=disabled warmup_steps=0")
    print(
        f"error_accumulation=enabled decay={cfg.error_accum_decay:.4f} "
        f"accum_loss_weight={cfg.accum_loss_weight:.2f}"
    )
    if cfg.enable_structural_plasticity:
        cap = model.recurrent_edge_capacity()
        cur = model.recurrent_edge_count()
        dens = (100.0 * cur / max(cap, 1))
        print(
            f"structural_plasticity=enabled rec_init_density={cfg.rec_init_density:.2f} "
            f"growth_rate={cfg.growth_rate:.3f} max_new_edges_per_epoch={cfg.max_new_edges_per_epoch} "
            f"min_corr_for_growth={cfg.min_corr_for_growth:.3f} edge_density={dens:.2f}%"
        )
    else:
        print("structural_plasticity=disabled")
    print(
        f"tonic_energy=enabled strength={cfg.tonic_strength:.4f} "
        f"vacancy_scale={cfg.tonic_vacancy_scale:.2f}"
    )
    if cfg.curriculum_mode:
        print(
            f"curriculum_mode=enabled visual_shape=({cfg.visual_height},{cfg.visual_width}) "
            "stages=[flash_all,line_patterns,function_patterns]"
        )
        print(
            f"curriculum_schedule=min_stage_epochs={cfg.min_stage_epochs} "
            f"min_loss_drop_pct={cfg.min_loss_drop_pct:.2f} "
            f"post_advance_hold_epochs={cfg.post_advance_hold_epochs}"
        )
    else:
        print("curriculum_mode=disabled input_distribution=gaussian")


def train_signal_copy_distance(
    cfg: SignalCopyConfig,
    checkpoint_dir: Path,
    checkpoint_prefix: str = "tpcn_signal_copy_distance",
    device: torch.device | None = None,
) -> int:
    seed_everything(cfg.seed)

    run_device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint_dir.mkdir(exist_ok=True)

    if cfg.input_indices is not None or cfg.output_indices is not None:
        if cfg.input_indices is None or cfg.output_indices is None:
            raise ValueError("Both cfg.input_indices and cfg.output_indices must be set together")
        layout = make_layout_from_indices(
            n_neurons=cfg.n_neurons,
            local_radius=cfg.local_radius,
            input_indices=cfg.input_indices,
            output_indices=cfg.output_indices,
        )
    else:
        layout = make_contiguous_layout(
            n_neurons=cfg.n_neurons,
            input_width=cfg.input_width,
            output_width=cfg.output_width,
            virtual_distance=cfg.virtual_distance,
            local_radius=cfg.local_radius,
        )
    input_idx = layout.input_indices
    output_idx = layout.output_indices
    effective_distance = layout.effective_distance()
    travel_steps = max(1, int(round(effective_distance / cfg.propagation_speed)))

    structural_density = cfg.rec_init_density if cfg.enable_structural_plasticity else 1.0
    model = DistanceSignalCopyNet.from_layout(
        signal_dim=cfg.signal_dim,
        alpha=cfg.alpha,
        layout=layout,
        device=run_device,
        structural_density=structural_density,
    ).to(run_device)

    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    _print_run_header(cfg, model, run_device, input_idx, output_idx, effective_distance, travel_steps)

    grid_x = torch.empty(0, device=run_device)
    grid_y = torch.empty(0, device=run_device)
    if cfg.curriculum_mode:
        grid_x, grid_y = make_visual_grids(cfg.visual_height, cfg.visual_width, run_device)

    stage = 0
    stage_baseline_loss: float | None = None
    stage_start_epoch = 1
    next_allowed_advance_epoch = 1

    for epoch in range(1, cfg.epochs + 1):
        t0 = time.perf_counter()
        advanced_this_epoch = False

        h = torch.zeros(cfg.batch_size, cfg.n_neurons, device=run_device)
        history = torch.zeros(travel_steps + 1, cfg.batch_size, cfg.signal_dim, device=run_device)
        ptr = 0

        total_loss = 0.0
        total_mae = 0.0
        total_accum_loss = 0.0
        active_steps = 0
        err_memory = torch.zeros(cfg.batch_size, cfg.signal_dim, device=run_device)
        h_mean_trace: list[torch.Tensor] = []
        tonic = model.compute_tonic(cfg.tonic_strength, cfg.tonic_vacancy_scale)

        for step_idx in range(cfg.steps_per_epoch):
            h = h.detach()
            if cfg.curriculum_mode:
                x_t = sample_curriculum_visual_batch(
                    stage=stage,
                    step_idx=ptr,
                    batch_size=cfg.batch_size,
                    height=cfg.visual_height,
                    width=cfg.visual_width,
                    grid_x=grid_x,
                    grid_y=grid_y,
                    device=run_device,
                )
            else:
                x_t = torch.randn(cfg.batch_size, cfg.signal_dim, device=run_device)
            history[ptr] = x_t
            target = history[(ptr + 1) % history.shape[0]]

            h, y_t = model.step(x_t, h, tonic=tonic)
            h_mean_trace.append(h.mean(dim=0).detach())

            residual = y_t - target
            accum_residual = (cfg.error_accum_decay * err_memory) + residual
            instant_loss = F.mse_loss(residual, torch.zeros_like(residual))
            accum_loss = F.mse_loss(accum_residual, torch.zeros_like(accum_residual))
            loss = ((1.0 - cfg.accum_loss_weight) * instant_loss) + (cfg.accum_loss_weight * accum_loss)
            err_memory = accum_residual.detach()

            pain_active = (not cfg.enable_pain_onset_gate) or (step_idx >= travel_steps)
            if pain_active:
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                optimizer.step()
                model.enforce_masks_()

                total_loss += float(loss.item())
                total_accum_loss += float(accum_loss.item())
                total_mae += float((y_t - target).abs().mean().item())
                active_steps += 1

            ptr = (ptr + 1) % history.shape[0]

        tonic = model.compute_tonic(cfg.tonic_strength, cfg.tonic_vacancy_scale)

        grown_edges = 0
        if cfg.enable_structural_plasticity and len(h_mean_trace) >= 3:
            h_means = torch.stack(h_mean_trace, dim=0)
            grown_edges = model.grow_recurrent_edges_from_lagcorr(
                h_means=h_means,
                growth_rate=cfg.growth_rate,
                max_new_edges=cfg.max_new_edges_per_epoch,
                candidate_multiplier=cfg.candidate_multiplier,
                min_corr_for_growth=cfg.min_corr_for_growth,
                local_radius=cfg.local_radius,
            )
            model.enforce_masks_()

        denom = max(active_steps, 1)
        avg_loss = total_loss / denom
        avg_accum_loss = total_accum_loss / denom
        avg_mae = total_mae / denom
        dt_epoch = time.perf_counter() - t0

        loss_drop_pct = 0.0
        if cfg.curriculum_mode:
            if stage_baseline_loss is None:
                stage_baseline_loss = avg_loss
            loss_drop_pct = compute_loss_drop_pct(stage_baseline_loss, avg_loss)

            stage_age = epoch - stage_start_epoch + 1
            can_advance = (
                stage < 2
                and epoch >= next_allowed_advance_epoch
                and stage_age >= cfg.min_stage_epochs
                and loss_drop_pct >= cfg.min_loss_drop_pct
            )
            if can_advance:
                stage += 1
                advanced_this_epoch = True
                stage_start_epoch = epoch + 1
                stage_baseline_loss = None
                next_allowed_advance_epoch = epoch + 1 + cfg.post_advance_hold_epochs

        if cfg.curriculum_mode:
            advance_tag = " stage_advance=1" if advanced_this_epoch else " stage_advance=0"
            edge_tag = ""
            if cfg.enable_structural_plasticity:
                cap = model.recurrent_edge_capacity()
                cur = model.recurrent_edge_count()
                edge_tag = f" grown_edges={grown_edges} rec_edges={cur}/{cap}"
            print(
                f"epoch={epoch:04d} loss={avg_loss:.6f} accum_loss={avg_accum_loss:.6f} mae={avg_mae:.6f} "
                f"travel_steps={travel_steps} stage={stage} loss_drop_pct={loss_drop_pct:.2f} "
                f"next_advance_epoch={next_allowed_advance_epoch} active_steps={active_steps}/{cfg.steps_per_epoch} "
                f"sec={dt_epoch:.2f}{advance_tag}{edge_tag}"
            )
        else:
            edge_tag = ""
            if cfg.enable_structural_plasticity:
                cap = model.recurrent_edge_capacity()
                cur = model.recurrent_edge_count()
                edge_tag = f" grown_edges={grown_edges} rec_edges={cur}/{cap}"
            print(
                f"epoch={epoch:04d} loss={avg_loss:.6f} accum_loss={avg_accum_loss:.6f} mae={avg_mae:.6f} "
                f"travel_steps={travel_steps} active_steps={active_steps}/{cfg.steps_per_epoch} sec={dt_epoch:.2f}{edge_tag}"
            )

        if epoch % cfg.save_every == 0 or epoch == cfg.epochs:
            ckpt_path = checkpoint_dir / f"{checkpoint_prefix}_epoch_{epoch}.pt"
            torch.save(
                {
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "optimizer_state": optimizer.state_dict(),
                    "loss": avg_loss,
                    "accum_loss": avg_accum_loss,
                    "mae": avg_mae,
                    "travel_steps": travel_steps,
                    "effective_distance": effective_distance,
                    "recurrent_edges": model.recurrent_edge_count(),
                    "recurrent_edge_capacity": model.recurrent_edge_capacity(),
                    "config": asdict(cfg),
                },
                ckpt_path,
            )

    return 0