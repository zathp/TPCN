"""CPU training capture and offline replay for the downstream TPCV-1 path."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .experiments import ExperimentConfig, ExperimentMetrics, ExperimentRunner, TrainingResult, make_synthetic_workload
from .visualization import (
    ReferenceVisualizer,
    SnapshotCollector,
    VisualizationFormatError,
    VisualizationSnapshot,
    export_snapshot,
    parse_snapshot,
)


SEQUENCE_VERSION = 1
MANIFEST_NAME = "manifest.json"
MAX_METRIC_BYTES = 1_048_576


class ReplaySequenceError(ValueError):
    """Raised when a saved CPU replay sequence is missing or invalid."""


class CPUTrainingCapture:
    """Bounded epoch observer that never participates in experiment execution."""

    def __init__(self, *, snapshot_every: int = 0, max_snapshots: int = 64) -> None:
        if isinstance(snapshot_every, bool) or not isinstance(snapshot_every, int) or snapshot_every < 0:
            raise ValueError("snapshot_every must be a nonnegative integer")
        self.snapshot_every = snapshot_every
        self.collector = SnapshotCollector(enabled=snapshot_every > 0, capacity=max_snapshots)
        self.metrics: list[dict[str, object]] = []

    def observe(self, epoch: int, neurons: tuple[object, ...], metrics: ExperimentMetrics) -> None:
        self.metrics.append(asdict(metrics))
        if self.snapshot_every and epoch % self.snapshot_every == 0:
            snapshot = VisualizationSnapshot.from_components(
                neurons,
                timestamp=max((neuron.clock.timestamp for neuron in neurons), default=0.0),
                epoch=metrics.epoch,
            )
            self.collector.capture(snapshot)

    @property
    def snapshots(self) -> tuple[bytes, ...]:
        return tuple(export_snapshot(snapshot) for snapshot in self.collector.snapshots)


class ReplaySequence:
    """A detached, validated snapshot sequence and its metric timeline."""

    def __init__(self, records: Iterable[bytes], metrics: Iterable[dict[str, object]] = ()) -> None:
        self.records = tuple(bytes(record) for record in records)
        try:
            self.snapshots = tuple(parse_snapshot(record) for record in self.records)
        except VisualizationFormatError as error:
            raise ReplaySequenceError("replay contains an invalid TPCV-1 record") from error
        self.metrics = tuple(dict(item) for item in metrics)
        metric_bytes = json.dumps(self.metrics, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if len(metric_bytes) > MAX_METRIC_BYTES:
            raise ReplaySequenceError("metric timeline exceeds the bounded limit")

    @property
    def digest(self) -> str:
        digest = hashlib.sha256()
        for record in self.records:
            digest.update(len(record).to_bytes(4, "big"))
            digest.update(record)
        return digest.hexdigest()

    def frames(self) -> tuple[dict[str, object], ...]:
        return ReferenceVisualizer(self.snapshots).frames()

    def changes(self) -> tuple[dict[str, object], ...]:
        return ReferenceVisualizer(self.snapshots).changes()

    def inspect(self, index: int) -> dict[str, object]:
        if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(self.snapshots):
            raise IndexError("snapshot index is out of range")
        snapshot = self.snapshots[index]
        metrics = next((item for item in self.metrics if item.get("epoch") == snapshot.epoch), None)
        return {"frame": self.frames()[index], "metrics": metrics}

    def save(self, directory: str | Path) -> Path:
        target = Path(directory)
        target.mkdir(parents=True, exist_ok=True)
        names = []
        for index, record in enumerate(self.records, start=1):
            name = f"snapshot-{index:06d}.tpcv"
            (target / name).write_bytes(record)
            names.append(name)
        manifest = {"sequence_version": SEQUENCE_VERSION, "records": names, "metrics": self.metrics, "digest": self.digest}
        encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if len(encoded) > MAX_METRIC_BYTES:
            raise OverflowError("replay manifest exceeds the bounded limit")
        (target / MANIFEST_NAME).write_bytes(encoded)
        return target

    @classmethod
    def load(cls, directory: str | Path, *, max_snapshots: int = 64) -> "ReplaySequence":
        if isinstance(max_snapshots, bool) or not isinstance(max_snapshots, int) or max_snapshots <= 0:
            raise ValueError("max_snapshots must be a positive integer")
        target = Path(directory)
        manifest_path = target / MANIFEST_NAME
        if not manifest_path.is_file():
            raise ReplaySequenceError("replay manifest is missing")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ReplaySequenceError("replay manifest is malformed") from error
        if not isinstance(manifest, dict) or manifest.get("sequence_version") != SEQUENCE_VERSION:
            raise ReplaySequenceError("unsupported replay sequence version")
        names = manifest.get("records")
        metrics = manifest.get("metrics", [])
        if not isinstance(names, list) or not isinstance(metrics, list) or len(names) > max_snapshots:
            raise ReplaySequenceError("replay sequence exceeds the bounded limit")
        records = []
        for name in names:
            if not isinstance(name, str) or Path(name).name != name or not name.endswith(".tpcv"):
                raise ReplaySequenceError("invalid replay record name")
            record_path = target / name
            if not record_path.is_file():
                raise ReplaySequenceError(f"replay record is missing: {name}")
            try:
                records.append(record_path.read_bytes())
            except OSError as error:
                raise ReplaySequenceError(f"replay record cannot be read: {name}") from error
        sequence = cls(records, metrics)
        if manifest.get("digest") != sequence.digest:
            raise ReplaySequenceError("replay digest does not match manifest")
        return sequence


def run_cpu_training(
    *,
    epochs: int = 3,
    seed: int = 0,
    examples_per_class: int = 2,
    snapshot_every: int = 0,
    max_snapshots: int = 64,
) -> tuple[TrainingResult, CPUTrainingCapture]:
    config = ExperimentConfig(epochs=epochs, seed=seed)
    workload = make_synthetic_workload(examples_per_class=examples_per_class, seed=seed)
    capture = CPUTrainingCapture(snapshot_every=snapshot_every, max_snapshots=max_snapshots)
    result = ExperimentRunner(config).train(workload, observer=capture.observe)
    return result, capture


__all__ = ["CPUTrainingCapture", "ReplaySequence", "ReplaySequenceError", "run_cpu_training"]