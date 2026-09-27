from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class SignalCopyConfig:
    epochs: int
    steps_per_epoch: int
    batch_size: int
    signal_dim: int
    n_neurons: int
    input_width: int
    output_width: int
    virtual_distance: int
    local_radius: int
    propagation_speed: float
    alpha: float
    lr: float
    weight_decay: float
    seed: int
    save_every: int
    curriculum_mode: bool
    visual_height: int
    visual_width: int
    min_stage_epochs: int
    min_loss_drop_pct: float
    post_advance_hold_epochs: int
    enable_pain_onset_gate: bool
    error_accum_decay: float
    accum_loss_weight: float
    enable_structural_plasticity: bool
    rec_init_density: float
    growth_rate: float
    max_new_edges_per_epoch: int
    candidate_multiplier: int
    min_corr_for_growth: float
    tonic_strength: float
    tonic_vacancy_scale: float
    input_indices: list[int] | None = None
    output_indices: list[int] | None = None


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Distance-constrained signal copy trainer with local recurrent propagation."
        )
    )
    p.add_argument("--epochs", type=int, default=40)
    p.add_argument("--steps-per-epoch", type=int, default=200)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--signal-dim", type=int, default=4)
    p.add_argument("--n-neurons", type=int, default=96)
    p.add_argument("--input-width", type=int, default=8)
    p.add_argument("--output-width", type=int, default=8)
    p.add_argument("--virtual-distance", type=int, default=48)
    p.add_argument("--input-indices", type=str, default=None, help="Explicit input neuron indices, e.g. 0,1,4-7")
    p.add_argument("--output-indices", type=str, default=None, help="Explicit output neuron indices, e.g. 40,41,60-63")
    p.add_argument("--local-radius", type=int, default=2)
    p.add_argument("--propagation-speed", type=float, default=2.0)
    p.add_argument("--alpha", type=float, default=0.35, help="State update blend factor in [0,1].")
    p.add_argument("--lr", type=float, default=2e-3)
    p.add_argument("--weight-decay", type=float, default=1e-5)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--save-every", type=int, default=10)
    p.add_argument("--curriculum-mode", action="store_true", help="Use 2D visual curriculum patterns instead of Gaussian signals.")
    p.add_argument("--visual-height", type=int, default=8, help="Height of 2D visual input/output pattern in curriculum mode.")
    p.add_argument("--visual-width", type=int, default=8, help="Width of 2D visual input/output pattern in curriculum mode.")
    p.add_argument("--min-stage-epochs", type=int, default=4, help="Minimum epochs to stay in each curriculum stage.")
    p.add_argument("--min-loss-drop-pct", type=float, default=8.0, help="Required percent loss decrease from stage baseline before stage advance.")
    p.add_argument("--post-advance-hold-epochs", type=int, default=2, help="Extra epochs to hold after stage advance before another advance is allowed.")
    p.add_argument("--disable-pain-onset-gate", action="store_true", help="If set, computes error immediately instead of waiting for delay-buffer warmup.")
    p.add_argument("--error-accum-decay", type=float, default=0.95, help="Temporal decay for accumulated error trace in [0, 1).")
    p.add_argument("--accum-loss-weight", type=float, default=0.7, help="Weight of accumulated-error loss term in [0, 1].")
    p.add_argument("--structural-plasticity", action="store_true", help="Enable growth of new recurrent edges from lag-1 activity correlation.")
    p.add_argument("--rec-init-density", type=float, default=0.125, help="Initial fraction of allowed recurrent edges that exist.")
    p.add_argument("--growth-rate", type=float, default=0.30, help="Edge growth probability scale.")
    p.add_argument("--max-new-edges-per-epoch", type=int, default=512, help="Maximum new recurrent edges to add per epoch.")
    p.add_argument("--candidate-multiplier", type=int, default=12, help="Sampled growth candidates per allowed edge budget.")
    p.add_argument("--min-corr-for-growth", type=float, default=0.05, help="Minimum positive lag-correlation required for growth.")
    p.add_argument("--tonic-strength", type=float, default=0.05, help="Base tonic excitation into each neuron pre-activation each step.")
    p.add_argument("--tonic-vacancy-scale", type=float, default=2.0, help="Extra tonic multiplier for low in-degree neurons.")
    return p


def config_from_args(args: argparse.Namespace) -> SignalCopyConfig:
    visual_height = max(2, int(args.visual_height))
    visual_width = max(2, int(args.visual_width))
    curriculum_mode = bool(args.curriculum_mode)
    signal_dim = max(1, int(args.signal_dim))
    if curriculum_mode:
        signal_dim = visual_height * visual_width

    explicit_input_indices: list[int] | None = None
    explicit_output_indices: list[int] | None = None
    if args.input_indices is not None or args.output_indices is not None:
        from .space import parse_index_spec

        if args.input_indices is None or args.output_indices is None:
            raise ValueError("Both --input-indices and --output-indices must be provided together")
        explicit_input_indices = parse_index_spec(args.input_indices)
        explicit_output_indices = parse_index_spec(args.output_indices)

    return SignalCopyConfig(
        epochs=max(1, int(args.epochs)),
        steps_per_epoch=max(1, int(args.steps_per_epoch)),
        batch_size=max(1, int(args.batch_size)),
        signal_dim=signal_dim,
        n_neurons=max(4, int(args.n_neurons)),
        input_width=max(1, int(args.input_width)),
        output_width=max(1, int(args.output_width)),
        virtual_distance=max(0, int(args.virtual_distance)),
        local_radius=max(0, int(args.local_radius)),
        propagation_speed=max(1e-3, float(args.propagation_speed)),
        alpha=min(1.0, max(0.0, float(args.alpha))),
        lr=max(1e-6, float(args.lr)),
        weight_decay=max(0.0, float(args.weight_decay)),
        seed=int(args.seed),
        save_every=max(1, int(args.save_every)),
        curriculum_mode=curriculum_mode,
        visual_height=visual_height,
        visual_width=visual_width,
        min_stage_epochs=max(1, int(args.min_stage_epochs)),
        min_loss_drop_pct=max(0.0, float(args.min_loss_drop_pct)),
        post_advance_hold_epochs=max(0, int(args.post_advance_hold_epochs)),
        enable_pain_onset_gate=(not bool(args.disable_pain_onset_gate)),
        error_accum_decay=min(0.9999, max(0.0, float(args.error_accum_decay))),
        accum_loss_weight=min(1.0, max(0.0, float(args.accum_loss_weight))),
        enable_structural_plasticity=bool(args.structural_plasticity),
        rec_init_density=min(1.0, max(0.0, float(args.rec_init_density))),
        growth_rate=max(0.0, float(args.growth_rate)),
        max_new_edges_per_epoch=max(0, int(args.max_new_edges_per_epoch)),
        candidate_multiplier=max(1, int(args.candidate_multiplier)),
        min_corr_for_growth=max(0.0, float(args.min_corr_for_growth)),
        tonic_strength=max(0.0, float(args.tonic_strength)),
        tonic_vacancy_scale=max(0.0, float(args.tonic_vacancy_scale)),
        input_indices=explicit_input_indices,
        output_indices=explicit_output_indices,
    )