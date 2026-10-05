"""Run the corrected, bounded Luna-33 ACP-0007 efficacy experiment."""

from __future__ import annotations

from dataclasses import fields, is_dataclass, replace
from enum import Enum
import hashlib
import json
import platform
import random
import sys
import traceback
from pathlib import Path
from typing import Any

from tpcn.event_runtime import EventType
from tpcn.experiments import ExperimentConfig, ExperimentRunner, SyntheticExample
from tpcn.spiral_benchmark import SpiralConfig, SpiralDataset, SpiralExample, make_spiral_dataset
from tpcn.stroke_dataset import StrokePoint
from tpcn.topology import TopologyCapacityError


AUTHORIZATION_REVISION = "89f05f3d7c7ce18646d8b4302b74c66e90ee0895"
CODE_BASELINE = "cc66e6a4affb044bf726d92510bcfd214c1f698f"
SEEDS = tuple(range(5))
CONDITIONS = ("A", "B", "C", "D")
LABELS = (
    "spiral-left-outward",
    "spiral-right-outward",
    "spiral-left-inward",
    "spiral-right-inward",
)
NODES = tuple(f"neuron-{index}" for index in range(8))
RING_NEIGHBORS = {
    node: (NODES[(index + 1) % len(NODES)],)
    for index, node in enumerate(NODES)
}
INITIAL_TOPOLOGIES = {
    0: (("neuron-7", "neuron-4", 1.0), ("neuron-6", "neuron-2", 1.0)),
    1: (("neuron-3", "neuron-5", 1.0), ("neuron-7", "neuron-6", 1.0)),
    2: (("neuron-2", "neuron-1", 1.0), ("neuron-4", "neuron-1", 1.0)),
    3: (("neuron-2", "neuron-4", 1.0), ("neuron-6", "neuron-4", 1.0)),
    4: (("neuron-3", "neuron-4", 1.0), ("neuron-4", "neuron-0", 1.0)),
}
OBSERVER_ONLY_METRICS = frozenset(
    {
        "structural_emission_count",
        "structural_observation_work",
        "structural_candidate_count",
        "structural_candidate_rejections",
        "structural_growth_attempts",
        "structural_growth_attempt_budget",
        "structural_growth_budget_remaining",
        "structural_growth_budget_exhausted",
        "structural_decisions",
    }
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _jsonable(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict) or hasattr(value, "items"):
        return {str(key): _jsonable(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"cannot serialize value of type {type(value).__name__}")


def _canonical_json(value: Any) -> str:
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _example_record(example: SpiralExample) -> dict[str, Any]:
    return {
        "example_id": example.example_id,
        "label": example.label,
        "points": [_jsonable(point) for point in example.points],
        "metadata": _jsonable(example.metadata),
        "sequence_digest": example.sequence_digest,
    }


def _ordered_examples(examples: tuple[SpiralExample, ...], seed: int) -> tuple[SpiralExample, ...]:
    result = list(examples)
    random.Random(seed).shuffle(result)
    return tuple(result)


def _destroy_coordinate_time_order(
    examples: tuple[SpiralExample, ...],
    seed: int,
) -> tuple[SpiralExample, ...]:
    seed_stream = random.Random(seed)
    transformed: list[SpiralExample] = []
    for example in examples:
        coordinates = [(point.x, point.y) for point in example.points]
        random.Random(seed_stream.getrandbits(32)).shuffle(coordinates)
        points = tuple(
            replace(point, x=x, y=y)
            for point, (x, y) in zip(example.points, coordinates, strict=True)
        )
        transformed.append(
            replace(
                example,
                points=points,
                sequence_digest=_digest([(point.x, point.y, point.timestamp, point.stroke_boundary) for point in points]),
            )
        )
    return tuple(transformed)


def build_dataset(
    seed: int,
) -> tuple[
    SpiralDataset,
    tuple[SpiralExample, ...],
    tuple[SpiralExample, ...],
    tuple[SpiralExample, ...],
]:
    generated = make_spiral_dataset(
        examples_per_class=16,
        train_seed=12007 + seed,
        evaluation_seed=22017 + seed,
        config=SpiralConfig(),
    )
    canonical_train = _ordered_examples(generated.train, 330000 + seed)
    canonical_evaluation = _ordered_examples(generated.evaluation, 330001 + seed)
    destroyed_train = _destroy_coordinate_time_order(canonical_train, 330002 + seed)
    return generated, canonical_train, canonical_evaluation, destroyed_train


def build_config(seed: int, condition: str) -> ExperimentConfig:
    if condition not in CONDITIONS:
        raise ValueError(f"unknown Luna-33 condition: {condition!r}")
    observing = condition != "A"
    growing = condition in ("C", "D")
    return ExperimentConfig(
        epochs=1,
        history_limit=16,
        max_points=20,
        prediction_capacity=8,
        activation_mode="event_only",
        energy_weight=1.0,
        seed=seed,
        learning_enabled=True,
        reward_mode="neutral",
        reward_delay=0.0,
        correct_reward=1.0,
        incorrect_reward=-1.0,
        max_classes=4,
        structural_plasticity=growing,
        structural_policy="e2_local_temporal",
        structural_observation=observing,
        structural_neighbors=RING_NEIGHBORS,
        structural_neighborhood_limit=2,
        structural_reverse_observer_limit=2,
        structural_association_window=4.0,
        structural_history_capacity=8,
        structural_candidate_capacity=4,
        structural_maximum_score=3,
        structural_growth_delay=0.4,
        structural_growth_attempt_budget=16,
        topology_fan_in=2,
        topology_fan_out=2,
        topology_edge_capacity=16,
        topology_initial_edges=2,
        topology_node_count=8,
        mutation_history_limit=64,
        candidate_capacity=16,
        max_growth_per_epoch=1,
        neuron_model="EXCURSION_V1",
        queue_capacity=128,
        event_budget=1024,
        settling_horizon=4.0,
        prediction_expiry=4.0,
    )


def _topology_signature(runner: ExperimentRunner) -> tuple[tuple[str, str, float], ...]:
    if runner.topology is None:
        raise RuntimeError("public runner topology was not initialized")
    return tuple(
        sorted((edge.source, edge.destination, float(edge.propagation_delay)) for edge in runner.topology.edges)
    )


def verify_topology_profile() -> dict[str, Any]:
    """Preflight all paired configs using only a one-point topology probe."""
    probe = (
        SyntheticExample(
            "luna33-topology-preflight",
            (StrokePoint(0.1, 0.2, timestamp=0.0),),
            LABELS[0],
        ),
    )
    observed: dict[str, Any] = {}
    for seed in SEEDS:
        expected = tuple(sorted(INITIAL_TOPOLOGIES[seed]))
        paired: dict[str, tuple[tuple[str, str, float], ...]] = {}
        for condition in CONDITIONS:
            runner = ExperimentRunner(build_config(seed, condition))
            runner.evaluate(probe)
            signature = _topology_signature(runner)
            if signature != expected:
                raise TopologyCapacityError(
                    f"seed {seed} condition {condition} initialized {signature!r}, expected {expected!r}"
                )
            paired[condition] = signature
        if len(set(paired.values())) != 1:
            raise RuntimeError(f"seed {seed} conditions do not share identical initial topology")
        observed[str(seed)] = {condition: _jsonable(paired[condition]) for condition in CONDITIONS}
    return observed


def _metric_projection(metrics: Any) -> dict[str, Any]:
    return {
        field.name: _jsonable(getattr(metrics, field.name))
        for field in fields(metrics)
        if field.name not in OBSERVER_ONLY_METRICS
    }


def _evaluation_projection(result: Any) -> dict[str, Any]:
    return {
        "predictions": _jsonable(result.predictions),
        "event_trace_sha256": _digest(result.event_trace),
        "event_trace_count": len(result.event_trace),
        "readout_diagnostics": _jsonable(result.readout_diagnostics),
        "metrics": _metric_projection(result.metrics),
    }


def _valid_metrics(metrics: tuple[Any, ...]) -> bool:
    return all(
        item.execution_completed
        and not item.execution_budget_exhausted
        and item.pending_event_count == 0
        and item.incomplete_settling_count == 0
        for item in metrics
    )


def _admitted_edges(decisions: tuple[Any, ...]) -> list[dict[str, Any]]:
    admitted: list[dict[str, Any]] = []
    for decision in decisions:
        if decision.status != "grown":
            continue
        before = {(source, destination, delay) for source, destination, delay in decision.topology_before}
        additions = [
            (source, destination, delay)
            for source, destination, delay in decision.topology_after
            if (source, destination, delay) not in before
        ]
        for source, destination, delay in additions:
            admitted.append(
                {
                    "source": source,
                    "destination": destination,
                    "delay": delay,
                    "decision_rank": decision.candidate_rank,
                    "score": None if decision.selected_candidate is None else decision.selected_candidate.score,
                    "status": decision.status,
                    "reason": decision.reason,
                }
            )
    return admitted


def _route_uses(edges: list[dict[str, Any]], event_trace: tuple[tuple[Any, ...], ...]) -> list[dict[str, Any]]:
    uses: list[dict[str, Any]] = []
    for edge in edges:
        pair = (edge["source"], edge["destination"])
        matching = []
        for event in event_trace:
            if len(event) < 12 or event[3] != EventType.EXCURSION:
                continue
            route_path = tuple(event[10])
            if any(current == pair for current in zip(route_path, route_path[1:])):
                matching.append(
                    {
                        "timestamp": event[0],
                        "source": event[1],
                        "destination": event[2],
                        "event_id": event[6],
                        "route_path": route_path,
                    }
                )
        if matching:
            uses.append({"edge": pair, "events": matching})
    return uses


def _condition_record(
    seed: int,
    condition: str,
    train: tuple[SpiralExample, ...],
    evaluation: tuple[SpiralExample, ...],
) -> dict[str, Any]:
    config = build_config(seed, condition)
    runner = ExperimentRunner(config)
    training_result = runner.train(tuple(example.as_synthetic() for example in train))
    if training_result.before is None:
        raise RuntimeError("ExperimentRunner.train() did not expose TrainingResult.before")
    initial = tuple(sorted(training_result.before.metrics.topology_edges))
    expected = tuple(sorted(INITIAL_TOPOLOGIES[seed]))
    if initial != expected:
        raise TopologyCapacityError(
            f"seed {seed} condition {condition} pre-training topology {initial!r} differs from expected {expected!r}"
        )
    decisions = tuple(
        decision
        for metrics in training_result.history
        for decision in metrics.structural_decisions
    )
    if condition in ("C", "D") and len(decisions) != len(train):
        raise RuntimeError(
            f"seed {seed} condition {condition} exposed {len(decisions)} training decisions for {len(train)} examples"
        )
    before_eval_topology = _topology_signature(runner)
    before_eval_prototypes = runner.prototypes
    eval_result = runner.evaluate(tuple(example.as_synthetic() for example in evaluation))
    after_eval_topology = _topology_signature(runner)
    after_eval_prototypes = runner.prototypes
    eval_nonmutation = (
        before_eval_topology == after_eval_topology
        and before_eval_prototypes == after_eval_prototypes
    )
    admitted = _admitted_edges(decisions)
    used = _route_uses(admitted, eval_result.event_trace)
    history_metrics = (
        training_result.before.metrics,
        *training_result.history,
        training_result.evaluation.metrics,
        eval_result.metrics,
    )
    training_metrics = tuple(training_result.history)
    final_metric = eval_result.metrics
    after_training_topology = before_eval_topology
    after_training_prototypes = before_eval_prototypes
    candidate_rejection_reasons: dict[str, int] = {}
    growth_rejection_reasons: dict[str, int] = {}
    for decision in decisions:
        for reason, count in decision.evidence.candidate_rejection_reasons:
            candidate_rejection_reasons[reason] = candidate_rejection_reasons.get(reason, 0) + count
        if decision.status not in ("grown", "no_candidate", "observation_only", "evaluation_only"):
            reason = decision.reason or decision.status
            growth_rejection_reasons[reason] = growth_rejection_reasons.get(reason, 0) + 1
    return {
        "status": "completed",
        "seed": seed,
        "condition": condition,
        "config": _jsonable(config),
        "initial_topology": _jsonable(initial),
        "training": {
            "before": _evaluation_projection(training_result.before),
            "history": _jsonable(training_result.history),
            "after": _evaluation_projection(training_result.evaluation),
            "parameter_updates": training_result.parameter_updates,
            "replay_digest": training_result.replay_digest,
            "prototypes": _jsonable(after_training_prototypes),
        },
        "heldout": _evaluation_projection(eval_result),
        "topology_after_training": _jsonable(after_training_topology),
        "prototypes_before_heldout_evaluation": _jsonable(before_eval_prototypes),
        "topology_before_heldout_evaluation": _jsonable(before_eval_topology),
        "evaluation_nonmutation_passed": eval_nonmutation,
        "valid_execution": _valid_metrics(history_metrics),
        "training_classes_represented": (
            not training_result.history[-1].missing_classes
            and set(training_result.history[-1].represented_classes) == set(LABELS)
        ),
        "all_classes_represented": not final_metric.missing_classes and set(final_metric.represented_classes) == set(LABELS),
        "structural": {
            "decisions": _jsonable(decisions),
            "candidate_pair_opportunities": sum(
                len(decision.evidence.candidates) + decision.evidence.candidate_rejections
                for decision in decisions
            ),
            "observed_emissions": sum(decision.evidence.observation_count for decision in decisions),
            "observation_work": sum(decision.evidence.observation_work for decision in decisions),
            "retained_candidates": sum(len(decision.evidence.candidates) for decision in decisions),
            "candidate_capacity_rejections": sum(
                decision.evidence.candidate_rejections for decision in decisions
            ),
            "growth_attempts": sum(decision.growth_attempted for decision in decisions),
            "admissions": sum(decision.status == "grown" for decision in decisions),
            "rejections": sum(
                decision.status not in ("grown", "no_candidate", "observation_only", "evaluation_only")
                for decision in decisions
            ),
            "candidate_rejection_reasons": candidate_rejection_reasons,
            "growth_rejection_reasons": growth_rejection_reasons,
            "saturation_rejections": sum(
                any(
                    marker in (decision.reason or "").lower()
                    for marker in ("capacity", "fan_in", "fan-out", "saturat")
                )
                for decision in decisions
            ),
            "budget_exhaustions": sum(decision.status == "budget_exhausted" for decision in decisions),
            "incomplete_settling_decisions": sum(decision.reason == "incomplete_settling" for decision in decisions),
            "admitted_edges": admitted,
            "admitted_edges_later_used": used,
        },
    }


def _summary_results(results: dict[str, Any]) -> dict[str, Any]:
    conditions = results["conditions"]
    accuracy: dict[int, dict[str, float | None]] = {seed: {} for seed in SEEDS}
    for seed in SEEDS:
        for condition in CONDITIONS:
            row = conditions[str(seed)][condition]
            accuracy[seed][condition] = (
                row["heldout"]["metrics"]["accuracy"] if row["status"] == "completed" else None
            )
    paired_ca: dict[str, float | None] = {}
    paired_cd: dict[str, float | None] = {}
    for seed in SEEDS:
        values = accuracy[seed]
        paired_ca[str(seed)] = (
            values["C"] - values["A"]
            if values["C"] is not None and values["A"] is not None
            else None
        )
        paired_cd[str(seed)] = (
            values["C"] - values["D"]
            if values["C"] is not None and values["D"] is not None
            else None
        )
    complete_pairs = all(value is not None for value in (*paired_ca.values(), *paired_cd.values()))
    mean_ca = sum(paired_ca.values()) / len(SEEDS) if complete_pairs else None
    mean_cd = sum(paired_cd.values()) / len(SEEDS) if complete_pairs else None
    positive_ca = sum(value is not None and value > 0 for value in paired_ca.values())
    positive_cd = sum(value is not None and value > 0 for value in paired_cd.values())
    complete_conditions = all(
        conditions[str(seed)][condition]["status"] == "completed"
        for seed in SEEDS
        for condition in CONDITIONS
    )
    valid_execution = complete_conditions and all(
        conditions[str(seed)][condition].get("valid_execution", False)
        and conditions[str(seed)][condition].get("training_classes_represented", False)
        and conditions[str(seed)][condition].get("all_classes_represented", False)
        for seed in SEEDS
        for condition in CONDITIONS
        if conditions[str(seed)][condition]["status"] == "completed"
    )
    heldout_nonmutation = all(
        conditions[str(seed)][condition].get("evaluation_nonmutation_passed", False)
        for seed in SEEDS
        for condition in CONDITIONS
        if conditions[str(seed)][condition]["status"] == "completed"
    ) and complete_conditions
    noninterference: dict[str, bool] = {}
    for seed in SEEDS:
        a = conditions[str(seed)]["A"]
        b = conditions[str(seed)]["B"]
        if a["status"] != "completed" or b["status"] != "completed":
            noninterference[str(seed)] = False
            continue
        noninterference[str(seed)] = (
            a["initial_topology"] == b["initial_topology"]
            and a["topology_after_training"] == b["topology_after_training"]
            and a["training"]["prototypes"] == b["training"]["prototypes"]
            and _evaluation_projection_from_record(a["training"]["before"])
            == _evaluation_projection_from_record(b["training"]["before"])
            and _evaluation_projection_from_record(a["training"]["after"])
            == _evaluation_projection_from_record(b["training"]["after"])
            and [
                _metric_record_projection(metric)
                for metric in a["training"]["history"]
            ]
            == [
                _metric_record_projection(metric)
                for metric in b["training"]["history"]
            ]
            and _evaluation_projection_from_record(a["heldout"])
            == _evaluation_projection_from_record(b["heldout"])
        )
    route_use_by_seed = {
        str(seed): bool(
            conditions[str(seed)]["C"]["status"] == "completed"
            and conditions[str(seed)]["C"]["structural"]["admitted_edges_later_used"]
        )
        for seed in SEEDS
    }
    route_engagement_count = sum(route_use_by_seed.values())
    runtime_exceptions = [
        conditions[str(seed)][condition].get("error")
        for seed in SEEDS
        for condition in CONDITIONS
        if conditions[str(seed)][condition]["status"] != "completed"
    ]
    if not all(noninterference.values()) or not heldout_nonmutation or runtime_exceptions:
        verdict = "BLOCKED — EXPERIMENT CONTRACT/RUNTIME DEFECT"
    elif not valid_execution:
        verdict = "INCONCLUSIVE"
    elif mean_ca is None or mean_cd is None:
        verdict = "INCONCLUSIVE"
    elif mean_ca <= 0 or mean_cd <= 0:
        verdict = "NOT SUPPORTED IN THIS SETUP"
    elif positive_ca >= 4 and positive_cd >= 4 and route_engagement_count >= 4:
        verdict = "SUPPORTED ONLY IN THIS DECLARED SETUP"
    else:
        verdict = "INCONCLUSIVE"
    return {
        "scientific_efficacy_verdict": verdict,
        "accuracy_by_seed_condition": {str(seed): accuracy[seed] for seed in SEEDS},
        "paired_c_minus_a": paired_ca,
        "paired_c_minus_d": paired_cd,
        "mean_c_minus_a": mean_ca,
        "mean_c_minus_d": mean_cd,
        "positive_c_minus_a_seed_count": positive_ca,
        "positive_c_minus_d_seed_count": positive_cd,
        "valid_execution_gate": valid_execution,
        "heldout_evaluation_nonmutation_gate": heldout_nonmutation,
        "ab_noninterference_by_seed": noninterference,
        "ab_noninterference_gate": all(noninterference.values()),
        "c_route_use_by_seed": route_use_by_seed,
        "c_route_engagement_seed_count": route_engagement_count,
        "c_route_engagement_gate": route_engagement_count >= 4,
        "runtime_exceptions": runtime_exceptions,
        "prediction_benefit_verdict": "NOT ESTABLISHED",
        "resource_benefit_verdict": "NOT ESTABLISHED",
        "hardware_equivalence_verdict": "NOT ESTABLISHED",
    }


def _evaluation_projection_from_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "predictions": record["predictions"],
        "event_trace_sha256": record["event_trace_sha256"],
        "event_trace_count": record["event_trace_count"],
        "readout_diagnostics": record["readout_diagnostics"],
        "metrics": {
            key: value for key, value in record["metrics"].items()
            if key not in OBSERVER_ONLY_METRICS
        },
    }


def _metric_record_projection(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in OBSERVER_ONLY_METRICS}


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(_jsonable(value), indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def run_experiment(output_dir: Path) -> dict[str, Any]:
    preflight = verify_topology_profile()
    datasets: dict[str, Any] = {}
    conditions: dict[str, Any] = {}
    for seed in SEEDS:
        generated, canonical_train, canonical_evaluation, destroyed_train = build_dataset(seed)
        datasets[str(seed)] = {
            "train_count": len(canonical_train),
            "evaluation_count": len(canonical_evaluation),
            "class_counts_train": {label: sum(item.label == label for item in canonical_train) for label in LABELS},
            "class_counts_evaluation": {label: sum(item.label == label for item in canonical_evaluation) for label in LABELS},
            "generated_train_metadata_digest": generated.train_digest,
            "generated_evaluation_metadata_digest": generated.evaluation_digest,
            "ordered_train_digest": _digest([_example_record(item) for item in canonical_train]),
            "ordered_evaluation_digest": _digest([_example_record(item) for item in canonical_evaluation]),
            "destroyed_train_digest": _digest([_example_record(item) for item in destroyed_train]),
        }
        seed_conditions: dict[str, Any] = {}
        conditions[str(seed)] = seed_conditions
        for condition in CONDITIONS:
            train = destroyed_train if condition == "D" else canonical_train
            try:
                seed_conditions[condition] = _condition_record(
                    seed,
                    condition,
                    train,
                    canonical_evaluation,
                )
            except Exception as error:
                seed_conditions[condition] = {
                    "status": "failed",
                    "seed": seed,
                    "condition": condition,
                    "error": {
                        "type": type(error).__name__,
                        "message": str(error),
                        "traceback": traceback.format_exc(),
                    },
                }
    results = {
        "schema": "LUNA33_RESULTS_V1",
        "authorization_revision": AUTHORIZATION_REVISION,
        "code_baseline": CODE_BASELINE,
        "seeds": list(SEEDS),
        "conditions": conditions,
        "datasets": datasets,
        "topology_preflight": preflight,
    }
    summary = _summary_results(results)
    output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "schema": "LUNA33_CONFIG_V1",
        "authorization_revision": AUTHORIZATION_REVISION,
        "code_baseline": CODE_BASELINE,
        "original_invalid_topology_initial_edges": 8,
        "topology_initial_edges": 2,
        "topology_correction_reason": "pre-outcome public-initializer feasibility",
        "no_efficacy_preview_before_correction": True,
        "topology_profile": {
            "node_count": 8,
            "edge_capacity": 16,
            "fan_in": 2,
            "fan_out": 2,
            "observation_neighbors": RING_NEIGHBORS,
            "neighborhood_limit": 2,
            "reverse_observer_limit": 2,
            "preflight_initial_topologies": preflight,
        },
        "shared_experiment_config": _jsonable(build_config(0, "C")),
        "condition_identity": {
            "A": {"structural_observation": False, "structural_plasticity": False, "training_order": "canonical"},
            "B": {"structural_observation": True, "structural_plasticity": False, "training_order": "canonical"},
            "C": {"structural_observation": True, "structural_plasticity": True, "training_order": "canonical"},
            "D": {"structural_observation": True, "structural_plasticity": True, "training_order": "coordinate-time-destroyed"},
        },
        "dataset": {
            "generator": "make_spiral_dataset",
            "examples_per_class": 16,
            "train_seed": "12007 + seed",
            "evaluation_seed": "22017 + seed",
            "training_order_seed": "330000 + seed",
            "evaluation_order_seed": "330001 + seed",
            "point_shuffle_seed_stream": "330002 + seed; getrandbits(32) per training example",
            "classes": LABELS,
            "points_per_example_bounds": [12, 20],
            "disjoint_split_generation": True,
            "digests": datasets,
        },
        "experiment_support_rule": {
            "means": ["C-A > 0", "C-D > 0"],
            "positive_seed_count_minimum": 4,
            "c_seeds_with_admitted_edge_later_route_used_minimum": 4,
            "ab_noninterference_required": True,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
        },
    }
    _write_json(output_dir / "config.json", config)
    _write_json(output_dir / "results.json", results)
    _write_json(output_dir / "summary.json", summary)
    return summary


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/acp0007-luna33-four-class-efficacy"),
    )
    args = parser.parse_args()
    summary = run_experiment(args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
