"""Deterministic Luna-12G spiral benchmark and diagnostic controls.

The generator owns only external workload data. Labels and generator metadata
never enter the canonical event stream; callers pass ``points`` to the
existing experiment runner and use ``label`` only for readout supervision.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import random
from typing import Any, Literal

from .experiments import ExperimentConfig, ExperimentRunner, SyntheticExample
from .stroke_dataset import StrokePoint

SpiralLabel = Literal[
    "spiral-left-outward", "spiral-right-outward",
    "spiral-left-inward", "spiral-right-inward",
    "spiral-left", "spiral-right",
]


@dataclass(frozen=True, slots=True)
class SpiralConfig:
    min_points: int = 12
    max_points: int = 20
    min_duration: float = 240.0
    max_duration: float = 320.0
    min_scale: float = 0.8
    max_scale: float = 1.2
    min_angular_speed: float = 1.7
    max_angular_speed: float = 2.5
    min_radial_growth: float = 0.7
    max_radial_growth: float = 1.1
    max_rotation: float = 2.0 * math.pi
    max_translation: float = 1.0
    max_timing_jitter: float = 0.08
    max_coordinate_noise: float = 0.025
    max_radial_jitter: float = 0.04

    def __post_init__(self) -> None:
        if not (1 <= self.min_points <= self.max_points):
            raise ValueError("point bounds are invalid")
        for name in ("min_duration", "max_duration", "min_scale", "max_scale",
                     "min_angular_speed", "max_angular_speed", "min_radial_growth",
                     "max_radial_growth"):
            if not math.isfinite(float(getattr(self, name))):
                raise ValueError(f"{name} must be finite")
        if self.min_duration <= 0.0 or self.max_duration < self.min_duration:
            raise ValueError("duration bounds are invalid")
        if self.min_scale <= 0.0 or self.max_scale < self.min_scale:
            raise ValueError("scale bounds are invalid")


@dataclass(frozen=True, slots=True)
class SpiralMetadata:
    seed: int
    label: SpiralLabel
    handedness: int
    rotation: float
    scale: float
    offset_x: float
    offset_y: float
    angular_speed: float
    radial_growth: float
    timing_jitter: float
    coordinate_noise: float
    radial_jitter: float
    sample_count: int
    duration: float
    path_length: float
    traversal: str = "outward"

    @property
    def nuisance_tuple(self) -> tuple[float | int, ...]:
        return (self.rotation, self.scale, self.offset_x, self.offset_y,
                self.angular_speed, self.radial_growth, self.timing_jitter,
                self.coordinate_noise, self.radial_jitter, self.sample_count,
                self.duration)


@dataclass(frozen=True, slots=True)
class SpiralExample:
    example_id: str
    points: tuple[StrokePoint, ...]
    label: SpiralLabel
    metadata: SpiralMetadata
    sequence_digest: str

    def as_synthetic(self) -> SyntheticExample:
        return SyntheticExample(self.example_id, self.points, self.label)


@dataclass(frozen=True, slots=True)
class SpiralDataset:
    train: tuple[SpiralExample, ...]
    evaluation: tuple[SpiralExample, ...]
    train_digest: str
    evaluation_digest: str


@dataclass(frozen=True, slots=True)
class ControlResult:
    name: str
    sample_count: int
    accuracy: float
    per_class_accuracy: tuple[tuple[str, float], ...]
    confusion: tuple[tuple[str, str, int], ...]
    confidence: float
    margin: float
    prediction_loss: float
    reward: float
    energy: float
    utility: float
    event_count: int
    active_neuron_count: int
    connection_count: int
    mutation_count: int
    accepted_additions: int
    pruned_connections: int
    represented_classes: tuple[str, ...]
    activation_count: int = 0
    prediction_error_count: int = 0


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _sequence_digest(points: tuple[StrokePoint, ...]) -> str:
    return _digest([(point.x, point.y, point.timestamp, point.stroke_boundary) for point in points])


def _sample_nuisance(seed: int, config: SpiralConfig) -> dict[str, float | int]:
    rng = random.Random(seed)
    return {
        "rotation": rng.uniform(0.0, config.max_rotation),
        "scale": rng.uniform(config.min_scale, config.max_scale),
        "offset_x": rng.uniform(-config.max_translation, config.max_translation),
        "offset_y": rng.uniform(-config.max_translation, config.max_translation),
        "angular_speed": rng.uniform(config.min_angular_speed, config.max_angular_speed),
        "radial_growth": rng.uniform(config.min_radial_growth, config.max_radial_growth),
        "timing_jitter": rng.uniform(0.0, config.max_timing_jitter),
        "coordinate_noise": rng.uniform(0.0, config.max_coordinate_noise),
        "radial_jitter": rng.uniform(0.0, config.max_radial_jitter),
        "sample_count": rng.randint(config.min_points, config.max_points),
        "duration": rng.uniform(config.min_duration, config.max_duration),
    }


def _make_example(seed: int, label: SpiralLabel, config: SpiralConfig,
                  nuisance: dict[str, float | int] | None = None) -> SpiralExample:
    if label not in ("spiral-left", "spiral-right", "spiral-left-outward", "spiral-right-outward",
                     "spiral-left-inward", "spiral-right-inward"):
        raise ValueError("label must identify a supported spiral class")
    values = _sample_nuisance(seed, config) if nuisance is None else nuisance
    base_label = label.replace("-outward", "").replace("-inward", "")
    handedness = 1 if base_label == "spiral-left" else -1
    traversal = "inward" if label.endswith("-inward") else "outward"
    rng = random.Random(seed ^ 0x5EED5EED)
    count = int(values["sample_count"])
    duration = float(values["duration"])
    timestamps: list[float] = [0.0]
    for index in range(1, count):
        base = duration * index / (count - 1)
        timestamps.append(max(timestamps[-1] + duration / (count * 4.0),
                              base + rng.uniform(-float(values["timing_jitter"]), float(values["timing_jitter"]))))
    timestamps[-1] = duration
    cos_rotation, sin_rotation = math.cos(float(values["rotation"])), math.sin(float(values["rotation"]))
    points: list[StrokePoint] = []
    path_length = 0.0
    previous: tuple[float, float] | None = None
    fractions = tuple(index / (count - 1) for index in range(count))
    for index, timestamp in enumerate(timestamps):
        fraction = fractions[index]
        radial = float(values["radial_growth"]) * fraction
        if index:
            radial += rng.uniform(-float(values["radial_jitter"]), float(values["radial_jitter"]))
        theta = float(values["angular_speed"]) * fraction * 2.0 * math.pi
        local_x = float(values["scale"]) * radial * math.cos(theta)
        local_y = handedness * float(values["scale"]) * radial * math.sin(theta)
        rotated_x = cos_rotation * local_x - sin_rotation * local_y
        rotated_y = sin_rotation * local_x + cos_rotation * local_y
        if index:
            rotated_x += rng.gauss(0.0, float(values["coordinate_noise"]))
            rotated_y += rng.gauss(0.0, float(values["coordinate_noise"]))
        x = float(values["offset_x"]) + rotated_x
        y = float(values["offset_y"]) + rotated_y
        if previous is not None:
            path_length += math.hypot(x - previous[0], y - previous[1])
        previous = (x, y)
        points.append(StrokePoint(x, y, timestamp=timestamp))
    if traversal == "inward":
        timestamps = tuple(point.timestamp for point in points)
        points = [StrokePoint(point.x, point.y, timestamp)
                  for point, timestamp in zip(reversed(points), timestamps)]
    metadata = SpiralMetadata(seed, label, handedness, float(values["rotation"]), float(values["scale"]),
                              float(values["offset_x"]), float(values["offset_y"]), float(values["angular_speed"]),
                              float(values["radial_growth"]), float(values["timing_jitter"]),
                              float(values["coordinate_noise"]), float(values["radial_jitter"]),
                              count, duration, path_length, traversal)
    return SpiralExample(f"spiral-{seed}", tuple(points), label, metadata, _sequence_digest(tuple(points)))


def generate_spiral(seed: int, label: SpiralLabel, *, config: SpiralConfig | None = None) -> SpiralExample:
    """Generate one deterministic center-outward spiral."""
    return _make_example(seed, label, config or SpiralConfig())


def generate_matched_pair(seed: int, *, config: SpiralConfig | None = None) -> tuple[SpiralExample, SpiralExample]:
    """Generate opposite handedness with exactly shared nuisance parameters."""
    selected = config or SpiralConfig()
    nuisance = _sample_nuisance(seed, selected)
    return (_make_example(seed, "spiral-left-outward", selected, nuisance),
            _make_example(seed, "spiral-right-outward", selected, nuisance))


def generate_traversal_pair(seed: int, *, handedness: str = "left",
                            config: SpiralConfig | None = None) -> tuple[SpiralExample, SpiralExample]:
    """Generate matched outward/inward streams over the same geometric path."""
    if handedness not in ("left", "right"):
        raise ValueError("handedness must be left or right")
    selected = config or SpiralConfig()
    nuisance = _sample_nuisance(seed, selected)
    prefix = f"spiral-{handedness}"
    return (_make_example(seed, f"{prefix}-outward", selected, nuisance),
            _make_example(seed, f"{prefix}-inward", selected, nuisance))


def make_spiral_dataset(*, examples_per_class: int = 32, train_seed: int = 12007,
                        evaluation_seed: int = 12017, config: SpiralConfig | None = None) -> SpiralDataset:
    selected = config or SpiralConfig()
    if examples_per_class <= 0:
        raise ValueError("examples_per_class must be positive")
    def stream(seed: int, split: str) -> tuple[SpiralExample, ...]:
        examples = []
        for index in range(examples_per_class):
            labels = ("spiral-left-outward", "spiral-right-outward",
                      "spiral-left-inward", "spiral-right-inward")
            for label_index, label in enumerate(labels):
                example_seed = seed * 1_000_000 + index * len(labels) + label_index
                example = _make_example(example_seed, label, selected)
                examples.append(SpiralExample(f"{split}-{example.example_id}", example.points,
                                               example.label, example.metadata, example.sequence_digest))
        return tuple(examples)
    train = stream(train_seed, "train")
    evaluation = stream(evaluation_seed, "eval")
    train_keys = {example.sequence_digest for example in train}
    eval_keys = {example.sequence_digest for example in evaluation}
    if train_keys & eval_keys:
        raise AssertionError("train/evaluation sequence reuse detected")
    return SpiralDataset(train, evaluation, _digest([asdict(item.metadata) for item in train]),
                         _digest([asdict(item.metadata) for item in evaluation]))


def transform_points(example: SpiralExample, transform: Literal["shuffle", "reverse"] , *, seed: int = 0) -> SpiralExample:
    """Apply a declared order control while preserving the spatial samples."""
    if transform == "shuffle":
        points = list(example.points)
        random.Random(seed).shuffle(points)
    elif transform == "reverse":
        points = list(reversed(example.points))
    else:
        raise ValueError("transform must be shuffle or reverse")
    duration = example.metadata.duration
    points = [StrokePoint(point.x, point.y, duration * index / max(1, len(points) - 1))
              for index, point in enumerate(points)]
    return SpiralExample(f"{example.example_id}-{transform}", tuple(points), example.label,
                         example.metadata, _sequence_digest(tuple(points)))


def generate_variant(example: SpiralExample, *, rotation: float | None = None,
                     scale: float | None = None, coordinate_noise: float | None = None,
                     offset_x: float | None = None, offset_y: float | None = None) -> SpiralExample:
    """Regenerate one example while changing only declared nuisance values."""
    metadata = asdict(example.metadata)
    metadata.pop("label")
    metadata.pop("handedness")
    metadata.pop("path_length")
    metadata["rotation"] = example.metadata.rotation if rotation is None else rotation
    metadata["scale"] = example.metadata.scale if scale is None else scale
    metadata["coordinate_noise"] = (example.metadata.coordinate_noise
                                      if coordinate_noise is None else coordinate_noise)
    metadata["offset_x"] = example.metadata.offset_x if offset_x is None else offset_x
    metadata["offset_y"] = example.metadata.offset_y if offset_y is None else offset_y
    return _make_example(example.metadata.seed, example.label, SpiralConfig(
        min_points=example.metadata.sample_count, max_points=example.metadata.sample_count,
        min_duration=example.metadata.duration, max_duration=example.metadata.duration), metadata)


def _control(name: str, examples: tuple[SpiralExample, ...], config: ExperimentConfig,
             *, train: tuple[SpiralExample, ...] = (), transform: str = "ordered") -> ControlResult:
    runner = ExperimentRunner(config)
    if train:
        runner.train(tuple(item.as_synthetic() for item in train))
    result = runner.evaluate(tuple(item.as_synthetic() for item in examples))
    mutation_count = sum(item.mutation_count for item in runner.history) if train else result.metrics.mutation_count
    accepted_additions = sum(item.accepted_additions for item in runner.history) if train else result.metrics.accepted_additions
    pruned_connections = sum(item.pruned_connections for item in runner.history) if train else result.metrics.pruned_connections
    diagnostics = result.readout_diagnostics
    predictions = tuple(item.prediction for item in diagnostics)
    labels = tuple(item.external_label for item in diagnostics)
    correct = sum(prediction == label for prediction, label in zip(predictions, labels))
    class_counts: dict[str, list[int]] = {}
    confusion: dict[tuple[str, str], int] = {}
    for label, prediction in zip(labels, predictions):
        class_counts.setdefault(label, [0, 0])[1] += 1
        class_counts[label][0] += int(label == prediction)
        confusion[(label, prediction)] = confusion.get((label, prediction), 0) + 1
    return ControlResult(name + (f" ({transform})" if transform != "ordered" else ""), len(examples),
                         correct / len(examples), tuple((label, values[0] / values[1]) for label, values in sorted(class_counts.items())),
                         tuple((left, right, count) for (left, right), count in sorted(confusion.items())),
                         sum(item.confidence for item in diagnostics) / len(diagnostics),
                         sum(item.margin for item in diagnostics) / len(diagnostics), result.metrics.prediction_loss,
                         result.metrics.reward, result.metrics.energy, result.metrics.utility, result.metrics.event_count,
                         result.metrics.active_neuron_count, result.metrics.connection_count,
                         mutation_count, accepted_additions, pruned_connections,
                         result.metrics.represented_classes, result.metrics.activation_count,
                         result.metrics.prediction_error_count)


def run_controls(dataset: SpiralDataset, *, epochs: int = 20, max_points: int | None = None) -> tuple[ControlResult, ...]:
    point_limit = max_points or max(len(item.points) for item in dataset.train + dataset.evaluation)
    base = dict(epochs=epochs, max_points=point_limit, prediction_capacity=point_limit,
                max_classes=4, seed=17)
    no_learning = _control("no-learning", dataset.evaluation, ExperimentConfig(**base, learning_enabled=False))
    fixed = _control("fixed-topology", dataset.evaluation, ExperimentConfig(**base), train=dataset.train)
    plastic = _control("structural-plasticity", dataset.evaluation,
                       ExperimentConfig(**base, structural_plasticity=True), train=dataset.train)
    shuffled = tuple(transform_points(item, "shuffle", seed=17 + index) for index, item in enumerate(dataset.evaluation))
    reversed_examples = tuple(transform_points(item, "reverse") for item in dataset.evaluation)
    rotations = tuple(generate_variant(item, rotation=angle)
                      for item in dataset.evaluation
                      for angle in (0.0, math.pi / 4.0, math.pi / 2.0, math.pi))
    scaled_translated = tuple(generate_variant(item, scale=0.65 + 0.15 * (index % 4),
                                               offset_x=-0.8 + 0.5 * (index % 4),
                                               offset_y=0.8 - 0.5 * (index % 4))
                              for index, item in enumerate(dataset.evaluation))
    noisy = tuple(generate_variant(item, coordinate_noise=level)
                  for item in dataset.evaluation for level in (0.0, 0.01, 0.025))
    same_class = (dataset.evaluation[0], generate_variant(dataset.evaluation[0], rotation=math.pi / 3.0,
                                                           scale=1.1, offset_x=-0.4, offset_y=0.4))
    pair_config = SpiralConfig(min_points=point_limit, max_points=point_limit,
                               min_duration=240.0, max_duration=240.0)
    opposite_pair = generate_matched_pair(91007, config=pair_config)
    return (no_learning, fixed, plastic,
            _control("shuffled-order", shuffled, ExperimentConfig(**base), train=dataset.train, transform="shuffle"),
            _control("time-reversal", reversed_examples, ExperimentConfig(**base), train=dataset.train, transform="reverse"),
            _control("rotation-invariance", rotations, ExperimentConfig(**base), train=dataset.train),
            _control("scale-translation", scaled_translated, ExperimentConfig(**base), train=dataset.train),
            _control("noise-robustness", noisy, ExperimentConfig(**base), train=dataset.train),
            _control("same-class-nuisance-pair", same_class, ExperimentConfig(**base), train=dataset.train),
            _control("opposite-handed-matched-pair", opposite_pair, ExperimentConfig(**base), train=dataset.train))


def run_policy_control(dataset: SpiralDataset, *, policy: str, config: ExperimentConfig,
                       order_transform: Literal["ordered", "reverse"] = "ordered") -> ControlResult:
    """Run one explicitly named policy through the classifier experiment."""
    if policy not in ("fixed", "baseline", "random", "temporal", "reversed"):
        raise ValueError("policy must be a supported structural policy")
    if order_transform == "reverse":
        train = tuple(transform_points(item, "reverse") for item in dataset.train)
        evaluation = tuple(transform_points(item, "reverse") for item in dataset.evaluation)
    elif order_transform == "ordered":
        train, evaluation = dataset.train, dataset.evaluation
    else:
        raise ValueError("order_transform must be ordered or reverse")
    return _control(policy, evaluation, config, train=train, transform=order_transform)


def metadata_json(dataset: SpiralDataset, controls: tuple[ControlResult, ...]) -> str:
    return json.dumps({"train_digest": dataset.train_digest, "evaluation_digest": dataset.evaluation_digest,
                       "train": [asdict(item.metadata) for item in dataset.train],
                       "evaluation": [asdict(item.metadata) for item in dataset.evaluation],
                       "controls": [asdict(control) for control in controls]}, indent=2, sort_keys=True)


__all__ = ["ControlResult", "SpiralConfig", "SpiralDataset", "SpiralExample", "SpiralMetadata",
           "generate_matched_pair", "generate_spiral", "generate_traversal_pair", "generate_variant", "make_spiral_dataset",
           "metadata_json", "run_controls", "run_policy_control", "transform_points"]