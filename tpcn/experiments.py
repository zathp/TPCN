"""Bounded, deterministic experiments over the public TPCN interfaces.

Labels are external metadata. They are consulted only after a label-free
canonical event stream has produced a readout, then may update this runner's
bounded outer-loop readout through reward and eligibility signals.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Callable, Literal

from .canonical_neuron import TPCNNeuron
from .eligibility import EligibilityActivity, EligibilityLedger, RewardSignal
from .energy_utility import LocalEnergyModel, RewardAdjustedUtility, RewardMessage
from .event_runtime import Event, EventQueue
from .predictive_coding import LocalPredictor, Observation
from .streaming_classifier import ACTIVITY_EVENT, StreamingCharacterClassifier
from .stroke_dataset import CharacterBoundary, END_CHARACTER, START_CHARACTER, StrokePoint

ActivationMode = Literal["event_only", "utility"]
RewardMode = Literal["dense", "sparse", "neutral"]


@dataclass(frozen=True, slots=True)
class SyntheticExample:
    example_id: str
    points: tuple[StrokePoint, ...]
    label: str


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    epochs: int = 3
    history_limit: int = 16
    max_points: int = 8
    prediction_capacity: int = 8
    activation_mode: ActivationMode = "event_only"
    energy_weight: float = 1.0
    seed: int = 0
    learning_enabled: bool = True
    reward_mode: RewardMode = "dense"
    reward_delay: float = 0.0
    correct_reward: float = 1.0
    incorrect_reward: float = -1.0
    max_classes: int = 26

    def __post_init__(self) -> None:
        for name in ("epochs", "history_limit", "max_points", "prediction_capacity", "max_classes"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.activation_mode not in ("event_only", "utility"):
            raise ValueError("activation_mode must be 'event_only' or 'utility'")
        if self.reward_mode not in ("dense", "sparse", "neutral"):
            raise ValueError("reward_mode must be 'dense', 'sparse', or 'neutral'")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise TypeError("seed must be an integer")
        if not isinstance(self.learning_enabled, bool):
            raise TypeError("learning_enabled must be a boolean")
        for name in ("energy_weight", "reward_delay", "correct_reward", "incorrect_reward"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be a real number")
            if not math.isfinite(float(value)):
                raise ValueError(f"{name} must be finite")
        if self.energy_weight < 0.0 or self.reward_delay < 0.0:
            raise ValueError("energy_weight and reward_delay must be nonnegative")


@dataclass(frozen=True, slots=True)
class ExperimentMetrics:
    epoch: int
    accuracy: float
    prediction_loss: float
    reward: float
    energy: float
    event_count: int
    activation_count: int
    retained_count: int
    average_reward: float = 0.0
    cumulative_reward: float = 0.0
    update_count: int = 0
    per_class_counts: tuple[tuple[str, int], ...] = ()
    confusion: tuple[tuple[str, str, int], ...] = ()
    mean_confidence: float = 0.0
    reward_update_latency: float = 0.0


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    metrics: ExperimentMetrics
    predictions: tuple[str, ...]
    event_trace: tuple[tuple[object, ...], ...]
    converged: bool


@dataclass(frozen=True, slots=True)
class TrainingResult:
    history: tuple[ExperimentMetrics, ...]
    evaluation: EvaluationResult
    parameter_updates: int
    replay_digest: str
    before: EvaluationResult | None = None
    after: EvaluationResult | None = None


TrainingObserver = Callable[[int, tuple[TPCNNeuron, ...], ExperimentMetrics], None]


def make_synthetic_workload(*, examples_per_class: int = 2, seed: int = 0,
                            points_per_example: int = 3,
                            labels: tuple[str, ...] = ("A", "Z"),
                            strokes_per_example: int = 1) -> tuple[SyntheticExample, ...]:
    """Build a deterministic finite workload with external-only labels."""
    if isinstance(examples_per_class, bool) or not isinstance(examples_per_class, int) or examples_per_class <= 0:
        raise ValueError("examples_per_class must be a positive integer")
    if isinstance(points_per_example, bool) or not isinstance(points_per_example, int) or points_per_example <= 0:
        raise ValueError("points_per_example must be a positive integer")
    if isinstance(strokes_per_example, bool) or not isinstance(strokes_per_example, int) or strokes_per_example <= 0:
        raise ValueError("strokes_per_example must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    if not labels or len(set(labels)) != len(labels) or any(not isinstance(label, str) or not label for label in labels):
        raise ValueError("labels must be unique non-empty strings")
    examples: list[SyntheticExample] = []
    for class_index, label in enumerate(labels):
        sign = -1.0 if class_index % 2 == 0 else 1.0
        for index in range(examples_per_class):
            wobble = ((seed + index * 3 + class_index) % 3) * 0.05
            points = tuple(
                StrokePoint(sign * (1.0 + wobble + point_index * 0.01),
                            sign * (0.5 + wobble),
                            timestamp=float(point_index),
                            stroke_boundary=(strokes_per_example > 1 and point_index % points_per_example == points_per_example - 1))
                for point_index in range(points_per_example * strokes_per_example)
            )
            examples.append(SyntheticExample(f"{label.lower()}-{index}", points, label))
    return tuple(examples)


def _validate_workload(workload: tuple[SyntheticExample, ...], config: ExperimentConfig) -> None:
    if not workload:
        raise ValueError("workload must not be empty")
    if len({example.label for example in workload}) > config.max_classes:
        raise BufferError("workload exceeds max_classes")
    for example in workload:
        if not isinstance(example, SyntheticExample) or not example.points:
            raise ValueError("workload entries must contain points")
        if len(example.points) > config.max_points:
            raise BufferError("workload exceeds max_points")


@dataclass(frozen=True, slots=True)
class _ExampleRun:
    raw_prediction: str
    feature: float
    confidence: float
    loss: float
    energy: float
    events: int
    activations: int
    retained: int
    trace: tuple[tuple[object, ...], ...]
    reward: float
    latency: float
    neuron: TPCNNeuron


class ExperimentRunner:
    """One independent experiment with bounded, resettable learned state."""

    def __init__(self, config: ExperimentConfig | None = None) -> None:
        self.config = ExperimentConfig() if config is None else config
        self.reset()

    def reset(self) -> None:
        self._prototypes: dict[str, tuple[float, int]] = {}
        self._updates = 0
        self._cumulative_reward = 0.0
        self._history: list[ExperimentMetrics] = []
        self._last_neurons: tuple[TPCNNeuron, ...] = ()

    @property
    def history(self) -> tuple[ExperimentMetrics, ...]:
        return tuple(self._history)

    @property
    def updates(self) -> int:
        return self._updates

    @property
    def last_neurons(self) -> tuple[TPCNNeuron, ...]:
        """Publicly observable neurons from the most recent workload pass."""
        return self._last_neurons

    def _learned_prediction(self, feature: float, fallback: str) -> tuple[str, float]:
        if not self._prototypes:
            return fallback, 0.0
        label, (value, count) = min(self._prototypes.items(), key=lambda item: (abs(feature - item[1][0] / item[1][1]), item[0]))
        distance = abs(feature - value / count)
        return label, 1.0 / (1.0 + distance)

    def _run_example(self, example: SyntheticExample, index: int, *, update: bool) -> _ExampleRun:
        config = self.config
        classifier = StreamingCharacterClassifier(max_activity_events=config.max_points)
        neuron = TPCNNeuron(f"neuron-{index}", input_gain=0.5)
        meter = LocalEnergyModel(f"meter-{index}", max_counter=config.max_points * 8)
        utility = RewardAdjustedUtility(energy_weight=config.energy_weight)
        ledger = EligibilityLedger(f"ledger-{index}", max_traces=config.prediction_capacity, decay_time_constant=4.0)
        predictor = LocalPredictor(f"predictor-{index}", max_outstanding=1, error_destination="errors")
        queue: EventQueue[Event] = EventQueue(capacity=config.max_points * 8)
        classifier.ingest_event(Event(0.0, example.example_id, "readout", START_CHARACTER, CharacterBoundary(index)))
        trace: list[tuple[object, ...]] = []
        feature = 0.0
        prediction_loss = 0.0
        for point_index, point in enumerate(example.points):
            timestamp = point.timestamp if point.timestamp is not None else float(point_index)
            event = Event(timestamp, example.example_id, neuron.neuron_id, "signal", point.x + point.y)
            delivered = queue.pop_ready(queue.push(event).timestamp)
            activation = neuron.receive_event(delivered)
            meter.observe_event(delivered, cost=abs(activation))
            feature += activation
            trace.append((delivered.timestamp, delivered.source, delivered.event_type, delivered.payload))
            if point_index:
                resolution = predictor.process_observation(
                    Event(timestamp, example.example_id, "predictor", "observation", Observation("next", activation)), queue)
                if resolution.error is not None:
                    prediction_loss += abs(resolution.error.error)
                    error_event = queue.pop_ready(timestamp)
                    ledger.apply_signal(Event(error_event.timestamp, error_event.source, ledger.ledger_id,
                                              "prediction_error", error_event.payload))
            prediction = predictor.create_prediction("next", activation, timestamp=timestamp, expires_at=timestamp + 2.0)
            ledger.record_activity(Event(timestamp, neuron.neuron_id, ledger.ledger_id, "eligibility_activity",
                                         EligibilityActivity(f"{example.example_id}:{point_index}", abs(activation), prediction.prediction_id)))
            classifier.ingest_event(Event(timestamp, neuron.neuron_id, "readout", ACTIVITY_EVENT, activation))
        result = classifier.ingest_event(Event(float(len(example.points)), example.example_id, "readout",
                                               END_CHARACTER, CharacterBoundary(index)))
        assert result is not None
        raw_prediction = result.label
        learned_prediction, learned_confidence = self._learned_prediction(feature / len(example.points), raw_prediction)
        prediction = learned_prediction if self._prototypes else raw_prediction
        confidence = learned_confidence if self._prototypes else result.confidence
        correct = prediction == example.label
        reward = 0.0 if config.reward_mode == "neutral" else (config.correct_reward if correct else config.incorrect_reward)
        if config.reward_mode == "sparse" and not correct:
            reward = 0.0
        message_timestamp = float(len(example.points)) + config.reward_delay
        message = RewardMessage(f"{example.example_id}:result", reward, message_timestamp)
        utility.observe_reward(message)
        attribution = ledger.apply_signal(Event(message.timestamp, "utility", ledger.ledger_id, "reward",
                            RewardSignal(reward, trace_id=f"{example.example_id}:0")))
        if update and config.learning_enabled and reward > 0.0:
            old_value, old_count = self._prototypes.get(example.label, (0.0, 0))
            self._prototypes[example.label] = (old_value + feature / len(example.points), old_count + 1)
            self._updates += 1
        retained = 1 if config.activation_mode == "event_only" or utility.evaluate(meter.energy, reward).retain else 0
        return _ExampleRun(prediction, feature / len(example.points), confidence, prediction_loss,
                           meter.energy, len(example.points), len(example.points), retained, tuple(trace), reward,
                           message.timestamp - float(len(example.points)) if attribution.status == "matched" else 0.0,
                           neuron)

    def _execute(self, workload: tuple[SyntheticExample, ...], epoch: int, *, update: bool) -> EvaluationResult:
        runs = [self._run_example(example, index, update=update) for index, example in enumerate(workload)]
        self._last_neurons = tuple(run.neuron for run in runs)
        counts: dict[str, int] = {}
        confusion: dict[tuple[str, str], int] = {}
        correct = 0
        for example, run in zip(workload, runs):
            counts[example.label] = counts.get(example.label, 0) + 1
            confusion[(example.label, run.raw_prediction)] = confusion.get((example.label, run.raw_prediction), 0) + 1
            correct += int(run.raw_prediction == example.label)
        total = len(runs)
        reward = sum(run.reward for run in runs)
        cumulative_reward = self._cumulative_reward + reward
        if update:
            self._cumulative_reward = cumulative_reward
        metrics = ExperimentMetrics(
            epoch, correct / total, sum(run.loss for run in runs) / total, reward,
            sum(run.energy for run in runs), sum(run.events for run in runs),
            sum(run.activations for run in runs), sum(run.retained for run in runs),
            reward / total, cumulative_reward, self._updates,
            tuple(sorted(counts.items())), tuple((key[0], key[1], value) for key, value in sorted(confusion.items())),
            sum(run.confidence for run in runs) / total, sum(run.latency for run in runs) / total)
        predictions = tuple(run.raw_prediction for run in runs)
        trace = tuple(item for run in runs for item in run.trace)
        converged = len(self._history) > 0 and metrics == self._history[-1]
        return EvaluationResult(metrics, predictions, trace, converged)

    def evaluate(self, workload: tuple[SyntheticExample, ...]) -> EvaluationResult:
        _validate_workload(workload, self.config)
        return self._execute(workload, 0, update=False)

    def train(self, workload: tuple[SyntheticExample, ...], *, observer: TrainingObserver | None = None) -> TrainingResult:
        _validate_workload(workload, self.config)
        if observer is not None and not callable(observer):
            raise TypeError("observer must be callable")
        before = self.evaluate(workload)
        for epoch in range(self.config.epochs):
            result = self._execute(workload, epoch, update=True)
            self._history.append(result.metrics)
            del self._history[:-self.config.history_limit]
            if observer is not None:
                observer(epoch + 1, self.last_neurons, result.metrics)
        after = self.evaluate(workload)
        digest = hashlib.sha256(repr((self.config, tuple(self._history), after, self._prototypes)).encode()).hexdigest()
        return TrainingResult(tuple(self._history), after, self._updates, digest, before, after)


def evaluate(workload: tuple[SyntheticExample, ...], *, config: ExperimentConfig | None = None) -> EvaluationResult:
    return ExperimentRunner(config).evaluate(workload)


def train(workload: tuple[SyntheticExample, ...], *, config: ExperimentConfig | None = None) -> TrainingResult:
    return ExperimentRunner(config).train(workload)


__all__ = [
    "EvaluationResult", "ExperimentConfig", "ExperimentMetrics", "ExperimentRunner",
    "SyntheticExample", "TrainingObserver", "TrainingResult", "evaluate", "make_synthetic_workload", "train",
]