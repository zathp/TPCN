"""Reproducible Luna-25 UCI Character Trajectories CPU benchmark."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
from typing import Any, Iterable

import numpy as np
from scipy.io import loadmat
import scipy

from tpcn.excursion_neuron import E1Config
from tpcn.experiments import (
    EvaluationResult,
    ExperimentConfig,
    ExperimentMetrics,
    ExperimentRunner,
    ReadoutDiagnostic,
    SyntheticExample,
)
from tpcn.stroke_dataset import StrokePoint


DOI = "10.24432/C58G7V"
SOURCE_URL = "https://archive.ics.uci.edu/static/public/175/character+trajectories.zip"
SOURCE_FILENAME = "mixoutALL_shifted.mat"
SPLIT_VERSION = "luna25-v1"
SPLIT_SEED = 20261003
EXAMPLES_PER_CLASS = 8
TRAIN_PER_CLASS = 4
VALIDATION_PER_CLASS = 2
TEST_PER_CLASS = 2
SAMPLE_INTERVAL_SECONDS = 0.005


@dataclass(frozen=True, slots=True)
class TrajectoryRecord:
    example_id: str
    source_index: int
    class_code: int
    label: str
    velocities: tuple[tuple[float, float], ...]


@dataclass(frozen=True, slots=True)
class SplitAssignment:
    split: str
    rank: int
    record: TrajectoryRecord


def _matlab_text(value: Any) -> str:
    array = np.asarray(value)
    if array.dtype.kind in ("U", "S"):
        return "".join(str(item) for item in array.reshape(-1).tolist())
    if array.size == 1:
        return _matlab_text(array.reshape(-1)[0])
    raise ValueError("UCI class key must contain one text label per entry")


def _single_matlab_struct(value: Any) -> Any:
    array = np.asarray(value)
    if array.size != 1:
        raise ValueError("UCI consts must contain exactly one MATLAB struct")
    return array.reshape(-1)[0]


def parse_matlab_dataset(raw: dict[str, Any]) -> tuple[TrajectoryRecord, ...]:
    """Parse the observed UCI mixout/consts schema without transforming time order."""
    if "mixout" not in raw or "consts" not in raw:
        raise ValueError("UCI MATLAB file must contain mixout and consts")
    constants = _single_matlab_struct(raw["consts"])
    try:
        class_codes = np.asarray(constants.charlabels).reshape(-1, order="F")
        class_keys = tuple(_matlab_text(item) for item in np.asarray(constants.key).reshape(-1, order="F"))
    except AttributeError as error:
        raise ValueError("UCI consts must contain charlabels and key") from error
    if not class_keys or len(set(class_keys)) != len(class_keys):
        raise ValueError("UCI class keys must be non-empty and unique")
    if not np.issubdtype(class_codes.dtype, np.integer):
        raise ValueError("UCI character labels must be integer class codes")
    trajectories = np.asarray(raw["mixout"]).reshape(-1, order="F")
    if len(trajectories) != len(class_codes):
        raise ValueError("UCI trajectory and label counts differ")
    if not len(trajectories):
        raise ValueError("UCI dataset contains no trajectories")

    records: list[TrajectoryRecord] = []
    for source_index, (trajectory, raw_code) in enumerate(zip(trajectories, class_codes)):
        code = int(raw_code)
        if code < 1 or code > len(class_keys):
            raise ValueError(f"UCI class code {code} is outside the class-key mapping")
        values = np.asarray(trajectory, dtype=np.float64)
        if values.ndim != 2 or values.shape[0] != 3 or values.shape[1] == 0:
            raise ValueError("each UCI trajectory must have shape 3-by-T with T > 0")
        if not np.isfinite(values).all():
            raise ValueError("UCI trajectory contains a non-finite value")
        velocities = tuple(
            (float(x_velocity), float(y_velocity))
            for x_velocity, y_velocity in zip(values[0], values[1])
        )
        records.append(
            TrajectoryRecord(
                f"{SOURCE_FILENAME}:mixout[{source_index:04d}]",
                source_index,
                code,
                class_keys[code - 1],
                velocities,
            )
        )
    return tuple(records)


def load_uci_dataset(path: Path) -> tuple[TrajectoryRecord, ...]:
    """Load and validate one downloaded UCI MATLAB source file."""
    if path.name != SOURCE_FILENAME:
        raise ValueError(f"expected UCI source filename {SOURCE_FILENAME!r}")
    if not path.is_file():
        raise FileNotFoundError(path)
    return parse_matlab_dataset(loadmat(path, struct_as_record=False, squeeze_me=False))


def make_split(
    records: Iterable[TrajectoryRecord],
    *,
    seed: int = SPLIT_SEED,
    examples_per_class: int = EXAMPLES_PER_CLASS,
    train_per_class: int = TRAIN_PER_CLASS,
    validation_per_class: int = VALIDATION_PER_CLASS,
    test_per_class: int = TEST_PER_CLASS,
) -> dict[str, tuple[SplitAssignment, ...]]:
    """Select class members and partitions by a versioned SHA-256 rank."""
    if (examples_per_class != train_per_class + validation_per_class + test_per_class
            or min(train_per_class, validation_per_class, test_per_class) <= 0):
        raise ValueError("split quotas must be positive and sum to examples_per_class")
    grouped: dict[str, list[TrajectoryRecord]] = {}
    for record in records:
        grouped.setdefault(record.label, []).append(record)
    if not grouped:
        raise ValueError("cannot split an empty dataset")

    split_lists: dict[str, list[SplitAssignment]] = {
        "train": [],
        "validation": [],
        "test": [],
    }
    quotas = (
        ("train", train_per_class),
        ("validation", validation_per_class),
        ("test", test_per_class),
    )
    for label in sorted(grouped):
        members = grouped[label]
        if len(members) < examples_per_class:
            raise ValueError(
                f"class {label!r} has {len(members)} examples; "
                f"{examples_per_class} are required"
            )
        ranked = sorted(
            members,
            key=lambda record: (
                hashlib.sha256(
                    f"{SPLIT_VERSION}\0{seed}\0{label}\0{record.example_id}".encode("utf-8")
                ).hexdigest(),
                record.example_id,
            ),
        )[:examples_per_class]
        offset = 0
        for split_name, quota in quotas:
            for rank, record in enumerate(ranked[offset:offset + quota], start=offset):
                split_lists[split_name].append(SplitAssignment(split_name, rank, record))
            offset += quota
    return {
        split_name: tuple(assignments)
        for split_name, assignments in split_lists.items()
    }


def as_workload(assignments: Iterable[SplitAssignment]) -> tuple[SyntheticExample, ...]:
    """Map only current-point vx+vy scalars to the existing sequential runner."""
    workload = []
    for assignment in assignments:
        points = tuple(
            StrokePoint(
                x=x_velocity + y_velocity,
                y=0.0,
                timestamp=point_index * SAMPLE_INTERVAL_SECONDS,
            )
            for point_index, (x_velocity, y_velocity) in enumerate(
                assignment.record.velocities
            )
        )
        workload.append(
            SyntheticExample(
                assignment.record.example_id,
                points,
                assignment.record.label,
            )
        )
    return tuple(workload)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("cannot serialize a non-finite benchmark value")
    if hasattr(value, "value") and isinstance(value.value, (str, int, float)):
        return value.value
    return value


def _canonical_digest(value: Any) -> str:
    serialized = json.dumps(
        _jsonable(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def _diagnostic_report(
    diagnostics: Iterable[ReadoutDiagnostic],
    class_labels: tuple[str, ...],
) -> tuple[dict[str, Any], ...]:
    grouped: dict[str, list[ReadoutDiagnostic]] = {label: [] for label in class_labels}
    for diagnostic in diagnostics:
        grouped.setdefault(diagnostic.external_label, []).append(diagnostic)
    rows = []
    for label in class_labels:
        examples = grouped.get(label, [])
        correct = sum(item.prediction == item.external_label for item in examples)
        rows.append(
            {
                "class": label,
                "count": len(examples),
                "correct": correct,
                "accuracy": correct / len(examples) if examples else None,
                "predictions": [
                    {
                        "example_id": item.example_id,
                        "predicted_label": item.prediction,
                        "raw_classifier_prediction": item.raw_prediction,
                        "reward": item.reward,
                        "confidence": item.confidence,
                    }
                    for item in examples
                ],
            }
        )
    return tuple(rows)


def _training_history_report(history: Iterable[ExperimentMetrics]) -> list[dict[str, Any]]:
    reports = []
    for metrics in history:
        summary = _jsonable(metrics)
        summary.pop("readout_diagnostics", None)
        reports.append(summary)
    return reports


def _classification_summary(
    diagnostics: Iterable[ReadoutDiagnostic],
    labels: tuple[str, ...],
) -> dict[str, Any]:
    examples = tuple(diagnostics)
    confusion = {actual: {predicted: 0 for predicted in labels} for actual in labels}
    for item in examples:
        if item.prediction not in confusion[item.external_label]:
            raise ValueError(f"prediction {item.prediction!r} is outside the declared class set")
        confusion[item.external_label][item.prediction] += 1
    per_class = []
    for label in labels:
        tp = confusion[label][label]
        fp = sum(confusion[actual][label] for actual in labels if actual != label)
        fn = sum(confusion[label][predicted] for predicted in labels if predicted != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        class_count = sum(confusion[label].values())
        per_class.append(
            {
                "class": label,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "support": class_count,
            }
        )
    correct = sum(confusion[label][label] for label in labels)
    count = len(examples)
    return {
        "count": count,
        "accuracy": correct / count if count else None,
        "macro_precision": sum(item["precision"] for item in per_class) / len(labels),
        "macro_recall": sum(item["recall"] for item in per_class) / len(labels),
        "macro_f1": sum(item["f1"] for item in per_class) / len(labels),
        "per_class": per_class,
        "confusion_matrix": {
            actual: {predicted: confusion[actual][predicted] for predicted in labels}
            for actual in labels
        },
    }


def _result_report(
    result: EvaluationResult,
    assignments: tuple[SplitAssignment, ...],
    labels: tuple[str, ...],
    queue_capacity: int,
    edge_capacity: int,
) -> dict[str, Any]:
    metrics = result.metrics
    metrics_summary = _jsonable(metrics)
    metrics_summary.pop("readout_diagnostics", None)
    return {
        "classification": _classification_summary(result.readout_diagnostics, labels),
        "metrics": metrics_summary,
        "per_class": _diagnostic_report(result.readout_diagnostics, labels),
        "sample_ids": [item.record.example_id for item in assignments],
        "event_trace_sha256": _canonical_digest(result.event_trace),
        "predictions_sha256": _canonical_digest(result.predictions),
        "resource_utilization": {
            "peak_queue_occupancy": metrics.peak_queue_occupancy,
            "queue_capacity": queue_capacity,
            "peak_queue_utilization": metrics.peak_queue_occupancy / queue_capacity,
            "connections": metrics.connection_count,
            "connection_capacity": metrics.connection_capacity,
            "edge_capacity_configured": edge_capacity,
            "connection_utilization": (
                metrics.connection_count / metrics.connection_capacity
                if metrics.connection_capacity
                else 0.0
            ),
            "fan_in_utilization": metrics.fan_in_utilization,
            "fan_out_utilization": metrics.fan_out_utilization,
        },
        "settling": {
            "completed": metrics.execution_completed,
            "incomplete_characters": metrics.incomplete_settling_count,
            "budget_exhausted": metrics.execution_budget_exhausted,
            "pending_events": metrics.pending_event_count,
            "beyond_deadline_events": metrics.beyond_deadline_event_count,
        },
        "prediction_and_credit": {
            "prediction_targets_observed": sum(
                len(item.record.velocities) for item in assignments
            ),
            "matched_predictions": metrics.matched_prediction_count,
            "unmatched_predictions": metrics.unmatched_prediction_count,
            "expired_predictions": metrics.expired_prediction_count,
            "prediction_errors": metrics.prediction_error_count,
            "prediction_loss": metrics.prediction_loss,
            "matched_delayed_credit": metrics.matched_credit_count,
            "unmatched_delayed_credit": metrics.unmatched_credit_count,
        },
        "activity": {
            "processed_events": metrics.processed_event_count,
            "emissions": metrics.excursion_count,
            "silent_events": metrics.silent_event_count,
            "max_route_depth": metrics.maximum_route_depth,
            "provenance_truncated_characters": metrics.provenance_truncated_count,
        },
        "energy_proxy": {
            "units": (
                "activity-cost proxy units; not joules and not calibrated "
                "physical energy"
            ),
            "event_processing": metrics.event_processing_proxy,
            "emitted_amplitude": metrics.emitted_amplitude_proxy,
            "edge_transfer": metrics.edge_transfer_proxy,
            "prediction_error": metrics.prediction_error_proxy,
            "total": metrics.energy,
        },
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fresh_run(
    config: ExperimentConfig,
    split: dict[str, tuple[SplitAssignment, ...]],
    labels: tuple[str, ...],
) -> dict[str, Any]:
    runner = ExperimentRunner(config)
    train_result = runner.train(as_workload(split["train"]))
    validation = runner.evaluate(as_workload(split["validation"]))
    test = runner.evaluate(as_workload(split["test"]))
    training_history = _training_history_report(train_result.history)
    reports = {
        "train": _result_report(
            train_result.evaluation, split["train"], labels,
            config.queue_capacity, config.topology_edge_capacity,
        ),
        "validation": _result_report(
            validation, split["validation"], labels,
            config.queue_capacity, config.topology_edge_capacity,
        ),
        "test": _result_report(
            test, split["test"], labels,
            config.queue_capacity, config.topology_edge_capacity,
        ),
    }
    stable = {
        "training_history": training_history,
        "training_replay_digest": train_result.replay_digest,
        "splits": reports,
    }
    return {
        "stable_output_sha256": _canonical_digest(stable),
        "training_replay_digest": train_result.replay_digest,
        "training_history": training_history,
        "split_reports": reports,
    }


def _sample_manifest(
    split: dict[str, tuple[SplitAssignment, ...]],
) -> dict[str, Any]:
    return {
        "split_version": SPLIT_VERSION,
        "seed": SPLIT_SEED,
        "algorithm": (
            "For each class, rank source records by SHA-256 of the UTF-8 bytes "
            "of `luna25-v1\\0{seed}\\0{class_label}\\0{example_id}`; break ties "
            "by example_id; take the first eight. Ranks 0-3 are train, 4-5 "
            "validation, and 6-7 test."
        ),
        "records": [
            {
                "split": assignment.split,
                "rank_within_class": assignment.rank,
                "example_id": assignment.record.example_id,
                "source_index_zero_based": assignment.record.source_index,
                "class_code_one_based": assignment.record.class_code,
                "class_label": assignment.record.label,
            }
            for split_name in ("train", "validation", "test")
            for assignment in split[split_name]
        ],
    }


def run_benchmark(data_path: Path, output_dir: Path, repetitions: int = 2) -> dict[str, Any]:
    if repetitions != 2:
        raise ValueError("Luna-25 requires exactly two fresh-state repetitions")
    records = load_uci_dataset(data_path)
    source_labels = tuple(sorted({record.label for record in records}))
    source_counts = {
        label: sum(record.label == label for record in records)
        for label in source_labels
    }
    split = make_split(records)
    if len(source_labels) != 20 or len(records) != 2858:
        raise ValueError(
            f"validated source count changed: {len(records)} examples, "
            f"{len(source_labels)} classes"
        )
    if any(count < EXAMPLES_PER_CLASS for count in source_counts.values()):
        raise ValueError("source does not satisfy the declared per-class sample quota")
    max_source_length = max(len(record.velocities) for record in records)
    if max_source_length > 256:
        raise ValueError("source trajectory length exceeds the declared 256-point cap")
    data = loadmat(data_path, struct_as_record=False, squeeze_me=False)
    constants = _single_matlab_struct(data["consts"])
    interval = float(np.asarray(constants.dt).reshape(-1)[0])
    if not math.isclose(interval, SAMPLE_INTERVAL_SECONDS, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"source sample interval {interval} differs from 0.005 seconds")
    classes_by_code = {
        str(code): label
        for code, label in enumerate(
            tuple(_matlab_text(item) for item in np.asarray(constants.key).reshape(-1, order="F")),
            start=1,
        )
    }

    config = ExperimentConfig(
        epochs=3,
        history_limit=16,
        max_points=256,
        prediction_capacity=8,
        activation_mode="event_only",
        energy_weight=1.0,
        seed=SPLIT_SEED,
        learning_enabled=True,
        reward_mode="dense",
        reward_delay=0.0,
        correct_reward=1.0,
        incorrect_reward=-1.0,
        max_classes=len(source_labels),
        structural_plasticity=False,
        structural_policy="fixed",
        topology_fan_in=2,
        topology_fan_out=2,
        topology_edge_capacity=8,
        topology_initial_edges=1,
        topology_node_count=80,
        mutation_history_limit=32,
        candidate_capacity=16,
        max_growth_per_epoch=1,
        neuron_model="EXCURSION_V1",
        queue_capacity=512,
        event_budget=4096,
        settling_horizon=10.0,
        prediction_expiry=4.0,
    )
    neuron_config = E1Config(event_budget=config.queue_capacity * 16)

    runs = [_fresh_run(config, split, source_labels) for _ in range(repetitions)]
    stable_hashes = [run["stable_output_sha256"] for run in runs]
    repeated_match = stable_hashes[0] == stable_hashes[1]
    split_manifest = _sample_manifest(split)
    split_manifest_digest = _canonical_digest(split_manifest)
    split_manifest_bytes = (
        json.dumps(split_manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    report_directory = output_dir.resolve()
    report_directory.mkdir(parents=True, exist_ok=True)
    run_manifest = {
        "benchmark": "Luna-25 UCI Character Trajectories sequential CPU evaluation",
        "benchmark_protocol": SPLIT_VERSION,
        "baseline": SPLIT_VERSION,
        "historical_split_reconstructable": False,
        "historical_result_reproduced": False,
        "baseline_is_reconstruction_of_luna22": False,
        "historical_split_reconstruction": (
            "Not possible: retained evidence does not identify record membership "
            "or the original loader/preprocessing implementation."
        ),
        "status": (
            "completed" if all(
                report["settling"]["completed"]
                for run in runs
                for report in run["split_reports"].values()
            ) else "incomplete"
        ),
        "dataset": {
            "name": "UCI Character Trajectories",
            "doi": DOI,
            "repository_url": "https://archive.ics.uci.edu/dataset/175/character+trajectories",
            "download_url": SOURCE_URL,
            "retrieved_utc_date": datetime.now(timezone.utc).date().isoformat(),
            "retrieval_details": (
                "Downloaded the UCI dataset 175 archive by HTTP GET from the "
                "recorded URL; verified archive and extracted source SHA-256."
            ),
            "archive_filename": "character-trajectories.zip",
            "source_filename": data_path.name,
            "source_sha256": _sha256(data_path),
            "archive_sha256": "5d2db017ef0d8cf0e65ed060c9e90399f78eb9f1e3cb63e22ca8c3ef4ba67d52",
            "license": "CC BY 4.0 (as identified on the UCI dataset page)",
            "raw_dataset_committed": False,
            "usable_examples": len(records),
            "class_count": len(source_labels),
            "classes": list(source_labels),
            "class_mapping_one_based": classes_by_code,
            "examples_per_class": source_counts,
            "trajectory_rows": {
                "0": "x_velocity",
                "1": "y_velocity",
                "2": "pen tip force (validated in source schema; ignored by benchmark)",
            },
            "source_schema_note": (
                "UCI documents three retained dimensions (x, y, pen-tip force), "
                "numerical differentiation and Gaussian smoothing; consts.dt "
                "confirms the 200 Hz sample interval."
            ),
            "matlab_sample_interval_seconds": interval,
            "observed_trajectory_length_min": min(len(record.velocities) for record in records),
            "observed_trajectory_length_max": max_source_length,
        },
        "parser": {
            "source_schema": "mixout cell array (3-by-T per example) and consts.charlabels/key/dt",
            "preserves_source_temporal_order": True,
            "feature": "current-point x_velocity + y_velocity only",
            "future_point_normalization": False,
            "whole_character_normalization": False,
            "scipy_version": scipy.__version__,
        },
        "split": {
            "version": SPLIT_VERSION,
            "seed": SPLIT_SEED,
            "selection": "SHA-256 rank; no Python or library RNG",
            "examples_per_class": EXAMPLES_PER_CLASS,
            "train_per_class": TRAIN_PER_CLASS,
            "validation_per_class": VALIDATION_PER_CLASS,
            "test_per_class": TEST_PER_CLASS,
            "sizes": {name: len(assignments) for name, assignments in split.items()},
            "class_counts": {
                name: {
                    label: sum(item.record.label == label for item in assignments)
                    for label in source_labels
                }
                for name, assignments in split.items()
            },
        },
        "experiment": {
            "runtime": "existing ExperimentRunner sequential EXCURSION_V1 CPU path",
            "config": _jsonable(config),
            "multi_excursion_neuron_config": _jsonable(neuron_config),
            "logical_time_unit": "seconds",
            "input_timestamps": "point_index * 0.005 seconds, reset per character",
            "event_point_boundary": (
                "The outer runner admits each available point at its timestamp; "
                "only that current scalar contributes to the admitted numeric input."
            ),
            "label_boundary": (
                "Class label is retained only on the outer SyntheticExample for "
                "post-readout reward/prototype orchestration and evaluation. It is "
                "not included in StrokePoint, Event payload, prediction target, or topology."
            ),
            "topology_node_count": 80,
            "topology_initial_edges": 1,
            "structural_plasticity": False,
            "queue_capacity": config.queue_capacity,
            "event_budget_per_character": config.event_budget,
            "settling_horizon_seconds": config.settling_horizon,
            "prediction_capacity_per_character": config.prediction_capacity,
            "prediction_expiry_seconds": config.prediction_expiry,
            "max_points_per_character": config.max_points,
            "derived_runtime_limits": {
                "classifier_activity_events_per_character": config.event_budget,
                "eligibility_traces_per_neuron": (
                    config.prediction_capacity * config.topology_node_count
                    if config.topology_node_count is not None
                    else None
                ),
                "eligibility_decay_time_constant_seconds": 4.0,
                "eligibility_trace_limit": 1.0,
                "eligibility_credit_limit": 1.0,
                "eligibility_max_reward_identities": 64,
                "energy_meter_max_counter": config.event_budget * 8,
                "energy_meter_max_energy": 1_000_000.0,
                "utility_formula": "net",
                "utility_energy_weight": config.energy_weight,
                "utility_threshold": 0.0,
                "utility_epsilon": 1e-9,
                "utility_max_messages": 1024,
            },
            "energy_units": (
                "activity-cost proxy units; not joules and not calibrated "
                "physical energy"
            ),
        },
        "repetitions": [
            {
                "index": index + 1,
                "fresh_runner_state": True,
                "stable_output_sha256": run["stable_output_sha256"],
                "training_replay_digest": run["training_replay_digest"],
            }
            for index, run in enumerate(runs)
        ],
        "repeated_run_stable_outputs_match": repeated_match,
        "split_manifest_sha256": split_manifest_digest,
        "split_manifest_sha256_format": (
            "SHA-256 of canonical UTF-8 JSON (sorted keys, compact separators, "
            "ASCII escaping, no trailing newline)"
        ),
        "prediction_interpretation": (
            "No predictions matched the observed targets and no prediction "
            "errors were generated; predictive efficacy is not established."
        ),
        "credit_interpretation": (
            "Runtime credit accounting executed, but no matched delayed-credit "
            "outcome occurred; useful delayed-credit learning is not demonstrated."
        ),
        "training_history": runs[0]["training_history"],
        "splits": runs[0]["split_reports"],
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "reproduction_command": (
            f'"{sys.executable}" -m scripts.benchmark_uci_character_trajectories '
            f'--data "{data_path.resolve()}" '
            f'--output-dir "{report_directory}" --repetitions 2'
        ),
    }

    per_class_report = {
        split_name: {
            "class_order": list(source_labels),
            "classes": report["per_class"],
            "classification": report["classification"],
        }
        for split_name, report in runs[0]["split_reports"].items()
    }
    (report_directory / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (report_directory / "split_manifest.json").write_bytes(
        split_manifest_bytes
    )
    (report_directory / "per_class_report.json").write_text(
        json.dumps(per_class_report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if not repeated_match:
        raise RuntimeError("fresh-state repeated runs produced different stable outputs")
    return run_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="path to mixoutALL_shifted.mat")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/luna-25-uci-character-trajectories"),
    )
    parser.add_argument("--repetitions", type=int, default=2)
    arguments = parser.parse_args(argv)
    report = run_benchmark(arguments.data, arguments.output_dir, arguments.repetitions)
    print(json.dumps({
        "status": report["status"],
        "dataset": report["dataset"]["usable_examples"],
        "classes": report["dataset"]["class_count"],
        "split_sizes": report["split"]["sizes"],
        "repeated_run_stable_outputs_match": report["repeated_run_stable_outputs_match"],
        "output_dir": str(arguments.output_dir.resolve()),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
