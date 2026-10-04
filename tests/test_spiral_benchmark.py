"""HISTORICAL COMPATIBILITY EXPERIMENT; NOT CURRENT EXCURSION_V1 / ACP-0007 EFFICACY EVIDENCE."""

from dataclasses import replace
from typing import Literal

import pytest
from tpcn.experiments import ExperimentConfig, evaluate
import tpcn.spiral_benchmark as spiral_benchmark
from tpcn.spiral_benchmark import (
    ControlResult,
    SpiralConfig,
    SpiralExample,
    generate_matched_pair,
    generate_spiral,
    make_spiral_dataset,
    run_controls,
    transform_points,
)


def test_spiral_generation_is_deterministic_and_starts_at_translated_center() -> None:
    first = generate_spiral(41, "spiral-left")
    second = generate_spiral(41, "spiral-left")

    assert first == second
    assert first.points[0].x == first.metadata.offset_x
    assert first.points[0].y == first.metadata.offset_y
    assert first.metadata.sample_count == len(first.points)
    assert first.metadata.label == "spiral-left"
    assert "left" not in first.example_id and "right" not in first.example_id


def test_matched_pair_shares_nuisance_and_inverts_only_handedness() -> None:
    left, right = generate_matched_pair(9)

    assert left.metadata.nuisance_tuple == right.metadata.nuisance_tuple
    assert left.metadata.handedness == -right.metadata.handedness
    assert left.points[0] == right.points[0]
    assert tuple(point.timestamp for point in left.points) == tuple(point.timestamp for point in right.points)
    assert any(left_point != right_point for left_point, right_point in zip(left.points[1:], right.points[1:]))


def test_split_is_disjoint_balanced_and_nuisance_distributions_are_class_symmetric() -> None:
    dataset = make_spiral_dataset(examples_per_class=8, train_seed=100, evaluation_seed=200)
    train_ids = {item.example_id for item in dataset.train}
    evaluation_ids = {item.example_id for item in dataset.evaluation}
    train_sequences = {item.sequence_digest for item in dataset.train}
    evaluation_sequences = {item.sequence_digest for item in dataset.evaluation}

    assert not train_ids & evaluation_ids
    assert not train_sequences & evaluation_sequences
    expected_labels = {
        "spiral-left-outward", "spiral-right-outward",
        "spiral-left-inward", "spiral-right-inward",
    }
    assert {item.label for item in dataset.train} == expected_labels
    assert {item.label for item in dataset.evaluation} == expected_labels
    assert all(item.metadata.nuisance_tuple[9] >= 12 for item in dataset.train + dataset.evaluation)
    assert all(item.metadata.nuisance_tuple[9] <= 20 for item in dataset.train + dataset.evaluation)


def test_order_controls_preserve_points_but_reassign_causal_time() -> None:
    example = generate_spiral(12, "spiral-right")
    shuffled = transform_points(example, "shuffle", seed=3)
    reversed_example = transform_points(example, "reverse")

    assert sorted((point.x, point.y) for point in shuffled.points) == sorted((point.x, point.y) for point in example.points)
    assert sorted((point.x, point.y) for point in reversed_example.points) == sorted((point.x, point.y) for point in example.points)
    assert tuple(point.timestamp for point in shuffled.points) == tuple(point.timestamp for point in reversed_example.points)
    assert shuffled.label == reversed_example.label == example.label


def test_labels_do_not_change_neural_trace_for_identical_spiral_streams() -> None:
    example = generate_spiral(23, "spiral-left")
    relabeled = replace(example, label="spiral-right")
    config = ExperimentConfig(max_points=len(example.points), prediction_capacity=len(example.points), seed=23)

    first = evaluate((example.as_synthetic(),), config=config)
    second = evaluate((relabeled.as_synthetic(),), config=config)

    assert first.event_trace == second.event_trace
    assert first.metrics.energy == second.metrics.energy
    assert first.metrics.prediction_loss == second.metrics.prediction_loss


def test_control_results_are_deterministic_and_include_required_order_controls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = SpiralConfig(min_points=6, max_points=6, min_duration=60.0, max_duration=60.0)
    dataset = make_spiral_dataset(examples_per_class=2, train_seed=300, evaluation_seed=400, config=config)

    captured: list[tuple[str, ExperimentConfig]] = []
    original_control = spiral_benchmark._control

    def record_config(
        name: str,
        examples: tuple[SpiralExample, ...],
        experiment_config: ExperimentConfig,
        *,
        train: tuple[SpiralExample, ...] = (),
        transform: Literal["ordered", "shuffle", "reverse"] = "ordered",
    ) -> ControlResult:
        captured.append((name, experiment_config))
        return original_control(
            name, examples, experiment_config, train=train, transform=transform
        )

    monkeypatch.setattr(spiral_benchmark, "_control", record_config)
    first = run_controls(dataset, epochs=1)
    second = run_controls(dataset, epochs=1)

    assert first == second
    assert {result.name for result in first} == {
        "no-learning", "fixed-topology", "structural-plasticity",
        "shuffled-order (shuffle)", "time-reversal (reverse)",
        "rotation-invariance", "scale-translation", "noise-robustness",
        "same-class-nuisance-pair", "opposite-handed-matched-pair",
    }
    assert all(0.0 <= result.accuracy <= 1.0 for result in first)
    assert len(captured) == 2 * len(first)
    assert all(config.neuron_model == "TANH_LEGACY" for _, config in captured)
    assert {name for name, _ in captured[:len(first)]} == {result.name.split(" (")[0] for result in first}
    assert all(
        first_config == second_config
        for (_, first_config), (_, second_config) in zip(captured[:len(first)], captured[len(first):])
    )
