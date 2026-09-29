"""Bounded, deterministic experiments over the public TPCN interfaces.

Labels are external metadata. They are consulted only after a label-free
canonical event stream has produced a readout, then may update this runner's
bounded outer-loop readout through reward and eligibility signals.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import random
from typing import Callable, Literal

from .canonical_neuron import TPCNNeuron
from .eligibility import EligibilityActivity, EligibilityLedger, RewardSignal
from .energy_utility import LocalEnergyModel, RewardAdjustedUtility, RewardMessage
from .event_runtime import BoundedExecutionResult, Event, EventQueue, execute_bounded
from .predictive_coding import LocalPredictor, Observation
from .streaming_classifier import ACTIVITY_EVENT, StreamingCharacterClassifier
from .stroke_dataset import CharacterBoundary, END_CHARACTER, START_CHARACTER, StrokePoint
from .structural_plasticity import CandidateEvidence, StructuralPlasticityController
from .topology import BoundedTopology

ActivationMode = Literal["event_only", "utility"]
RewardMode = Literal["dense", "sparse", "neutral"]
StructuralPolicy = Literal["fixed", "baseline", "random", "temporal", "reversed"]


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
    structural_plasticity: bool = False
    structural_policy: StructuralPolicy = "baseline"
    topology_fan_in: int = 2
    topology_fan_out: int = 2
    topology_edge_capacity: int = 8
    topology_initial_edges: int = 1
    topology_node_count: int | None = None
    mutation_history_limit: int = 32
    candidate_capacity: int = 16
    max_growth_per_epoch: int = 1

    def __post_init__(self) -> None:
        for name in ("epochs", "history_limit", "max_points", "prediction_capacity", "max_classes"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for name in ("topology_fan_in", "topology_fan_out", "topology_edge_capacity", "mutation_history_limit",
                     "candidate_capacity", "max_growth_per_epoch"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if isinstance(self.topology_initial_edges, bool) or not isinstance(self.topology_initial_edges, int) or self.topology_initial_edges < 0:
            raise ValueError("topology_initial_edges must be a nonnegative integer")
        if not isinstance(self.structural_plasticity, bool):
            raise TypeError("structural_plasticity must be a boolean")
        if self.structural_policy not in ("fixed", "baseline", "random", "temporal", "reversed"):
            raise ValueError("structural_policy must be a supported policy")
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
        if self.topology_node_count is not None and (
            isinstance(self.topology_node_count, bool)
            or not isinstance(self.topology_node_count, int)
            or self.topology_node_count <= 0
        ):
            raise ValueError("topology_node_count must be a positive integer or None")


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
    utility: float = 0.0
    active_neuron_count: int = 0
    receiving_neuron_count: int = 0
    emitting_neuron_count: int = 0
    never_activated_fraction: float = 1.0
    connection_count: int = 0
    connection_capacity: int = 0
    fan_in_utilization: float = 0.0
    fan_out_utilization: float = 0.0
    mutation_count: int = 0
    accepted_additions: int = 0
    pruned_connections: int = 0
    rejected_mutations: int = 0
    topology_edges: tuple[tuple[str, str, float], ...] = ()
    mutation_history: tuple[tuple[str, str, str, str], ...] = ()
    mutation_rejection_reasons: tuple[tuple[str, int], ...] = ()
    per_class_accuracy: tuple[tuple[str, float], ...] = ()
    represented_classes: tuple[str, ...] = ()
    missing_classes: tuple[str, ...] = ()
    prototype_count: int = 0
    starvation_count: int = 0
    mean_margin: float = 0.0
    readout_diagnostics: tuple[ReadoutDiagnostic, ...] = ()
    prediction_error_count: int = 0
    execution_completed: bool = True
    execution_budget_exhausted: bool = False
    configured_event_budget: int = 0
    processed_event_count: int = 0
    pending_event_count: int = 0
    termination_reason: str = "completed"


@dataclass(frozen=True, slots=True)
class ReadoutDiagnostic:
    """Bounded external-readout evidence for one labeled example."""

    example_id: str
    external_label: str
    network_feature: float
    raw_prediction: str
    prediction: str
    reward: float
    readout_updated: bool
    class_representations: tuple[tuple[str, float, int], ...]
    class_distances: tuple[tuple[str, float], ...]
    nearest_class: str
    winning_distance: float
    runner_up_distance: float
    margin: float
    confidence: float


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    metrics: ExperimentMetrics
    predictions: tuple[str, ...]
    event_trace: tuple[tuple[object, ...], ...]
    converged: bool
    readout_diagnostics: tuple[ReadoutDiagnostic, ...] = ()


@dataclass(frozen=True, slots=True)
class TrainingResult:
    history: tuple[ExperimentMetrics, ...]
    evaluation: EvaluationResult
    parameter_updates: int
    replay_digest: str
    before: EvaluationResult | None = None
    after: EvaluationResult | None = None


TrainingObserver = Callable[[int, tuple[TPCNNeuron, ...], ExperimentMetrics], None]


class _ComputationalNetwork:
    """Persistent neurons and bounded causal routing for one experiment."""

    def __init__(self, nodes: tuple[str, ...], topology: BoundedTopology, queue_capacity: int) -> None:
        self.neurons = tuple(TPCNNeuron(node, input_gain=0.5) for node in nodes)
        self._by_id = {neuron.neuron_id: neuron for neuron in self.neurons}
        self.topology = topology
        self.queue_capacity = queue_capacity

    def set_topology(self, topology: BoundedTopology) -> None:
        self.topology = topology

    def reset_character(self) -> None:
        for neuron in self.neurons:
            neuron.reset()

    def process(
        self,
        source: str,
        timestamp: float,
        payload: float,
        *,
        max_events: int,
    ) -> tuple[tuple[tuple[object, ...], ...], tuple[float, ...], BoundedExecutionResult]:
        queue: EventQueue[Event] = EventQueue(capacity=self.queue_capacity)
        initial = queue.push(Event(timestamp, source, source, "signal", payload))
        depths = {initial.sequence: 0}
        paths = {initial.sequence: (source,)}
        trace: list[tuple[object, ...]] = []
        activations: list[float] = []
        def handle(event: Event, pending_queue: EventQueue[Event]) -> None:
            depth = depths.pop(event.sequence)
            path = paths.pop(event.sequence)
            neuron = self._by_id[event.destination]
            activation = neuron.receive_event(event)
            trace.append((event.timestamp, event.source, event.destination, event.event_type, event.payload))
            activations.append(activation)
            if depth < len(self.neurons) and neuron.neuron_id not in path[1:]:
                emitted = Event(event.timestamp, neuron.neuron_id, neuron.neuron_id, event.event_type, activation)
                for routed in self.topology.route(emitted, pending_queue):
                    depths[routed.sequence] = depth + 1
                    paths[routed.sequence] = path + (routed.destination,)
        execution = execute_bounded(queue, handle, event_budget=max_events)
        return tuple(trace), tuple(activations), execution


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
    example_id: str
    external_label: str
    classifier_prediction: str
    raw_prediction: str
    feature: float
    confidence: float
    loss: float
    energy: float
    events: int
    activations: int
    retained: int
    trace: tuple[tuple[object, ...], ...]
    execution: BoundedExecutionResult
    reward: float
    latency: float
    utility: float
    neuron: TPCNNeuron
    routed_events: int
    propagated_activity: float
    readout_updated: bool
    class_representations: tuple[tuple[str, float, int], ...]
    class_distances: tuple[tuple[str, float], ...]
    nearest_class: str
    winning_distance: float
    runner_up_distance: float
    margin: float


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
        self._topology: BoundedTopology | None = None
        self._plasticity: StructuralPlasticityController | None = None
        self._mutation_history: list[tuple[str, str, str, str]] = []
        self._mutation_rejection_reasons: dict[str, int] = {}
        self._last_mutation_rejection_reasons: dict[str, int] = {}
        self._network: _ComputationalNetwork | None = None

    @property
    def history(self) -> tuple[ExperimentMetrics, ...]:
        return tuple(self._history)

    @property
    def updates(self) -> int:
        return self._updates

    @property
    def prototypes(self) -> tuple[tuple[str, float, int], ...]:
        """Return deterministic bounded external readout state."""
        return tuple((label, value, count) for label, (value, count) in sorted(self._prototypes.items()))

    @property
    def last_neurons(self) -> tuple[TPCNNeuron, ...]:
        """Publicly observable neurons from the most recent workload pass."""
        return self._last_neurons

    @property
    def topology(self) -> BoundedTopology | None:
        return self._topology

    @property
    def plasticity(self) -> StructuralPlasticityController | None:
        return self._plasticity

    def _ensure_topology(self, workload: tuple[SyntheticExample, ...]) -> None:
        node_count = self.config.topology_node_count or len(workload)
        nodes = tuple(f"neuron-{index}" for index in range(node_count))
        if self._topology is not None and self._topology.nodes == nodes:
            return
        possible_edges = len(nodes) * max(0, len(nodes) - 1)
        initial_edges = min(self.config.topology_initial_edges, self.config.topology_edge_capacity, possible_edges)
        self._topology = BoundedTopology(
            nodes, fan_in_limit=self.config.topology_fan_in, fan_out_limit=self.config.topology_fan_out,
            edge_capacity=self.config.topology_edge_capacity)
        candidates = [(source, destination) for source in sorted(nodes) for destination in sorted(nodes)
                      if source != destination]
        random.Random(self.config.seed).shuffle(candidates)
        for source, destination in candidates:
            if len(self._topology) >= initial_edges:
                break
            self._topology.connect(source, destination, 1.0)
        neighbors = {node: tuple(candidate for candidate in nodes if candidate != node)
                 for node in nodes if len(nodes) > 1}
        self._plasticity = StructuralPlasticityController(
            self._topology, candidate_capacity=self.config.candidate_capacity,
            max_growth_per_adaptation=self.config.max_growth_per_epoch,
            minimum_edge_count=0, local_neighbors=neighbors)
        self._network = _ComputationalNetwork(nodes, self._topology, self.config.max_points * 8)
        self._mutation_history = []
        self._mutation_rejection_reasons = {}
        self._last_mutation_rejection_reasons = {}

    def _topology_metrics(self, mutations: tuple[tuple[str, str, str, str], ...]) -> dict[str, object]:
        topology = self._topology
        if topology is None:
            return {}
        edge_count = len(topology)
        denominator = max(1, len(topology.nodes))
        return {
            "connection_count": edge_count,
            "connection_capacity": topology.edge_capacity,
            "fan_in_utilization": edge_count / (denominator * topology.fan_in_limit),
            "fan_out_utilization": edge_count / (denominator * topology.fan_out_limit),
            "topology_edges": tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in topology.edges),
            "mutation_history": tuple(self._mutation_history),
            "mutation_count": len(mutations),
            "accepted_additions": sum(item[0] == "grown" for item in mutations),
            "pruned_connections": sum(item[0] == "pruned" for item in mutations),
            "rejected_mutations": sum(item[0] not in ("grown", "pruned") for item in mutations),
            "mutation_rejection_reasons": tuple(sorted(self._last_mutation_rejection_reasons.items())),
        }

    def _adapt_topology(self, runs: list[_ExampleRun], epoch: int) -> tuple[tuple[str, str, str, str], ...]:
        if not self.config.structural_plasticity or self._plasticity is None or len(runs) < 2:
            return ()
        self._last_mutation_rejection_reasons = {}
        mutations: list[tuple[str, str, str, str]] = []
        nodes = self._topology.nodes
        for index, run in enumerate(runs):
            source = nodes[index % len(nodes)]
            if self.config.structural_policy == "reversed":
                destination = nodes[(index - 1) % len(nodes)]
            elif self.config.structural_policy == "temporal":
                destination = nodes[(index + 2) % len(nodes)]
            elif self.config.structural_policy == "random":
                candidates = [node for node in nodes if node != source]
                destination = random.Random(self.config.seed + epoch + index).choice(candidates)
            else:
                destination = nodes[(index + 1) % len(nodes)]
            evidence = CandidateEvidence(source, source, destination, abs(run.feature) + run.loss,
                                         1.0, f"epoch-{epoch}-neuron-{index}")
            result = self._plasticity.grow(evidence)
            mutations.append((result.status, source, destination, "local_activity_prediction_error"))
            if result.status not in ("grown", "pruned"):
                reason = result.reason or ("duplicate" if result.status == "duplicate" else result.status)
                self._mutation_rejection_reasons[reason] = self._mutation_rejection_reasons.get(reason, 0) + 1
                self._last_mutation_rejection_reasons[reason] = self._last_mutation_rejection_reasons.get(reason, 0) + 1
            if result.status == "grown":
                break
        if epoch % 2 == 1 and self._topology is not None and len(self._topology) > 1:
            scores = {(edge.source, edge.destination): abs(runs[index % len(runs)].feature)
                      for index, edge in enumerate(self._topology.edges)}
            for result in self._plasticity.prune_by_score(scores, maximum=1):
                assert result.edge is not None
                mutations.append((result.status, result.edge.source, result.edge.destination, "local_activity_retention"))
        self._topology = self._plasticity.topology
        assert self._network is not None
        self._network.set_topology(self._topology)
        self._mutation_history.extend(mutations)
        del self._mutation_history[:-self.config.mutation_history_limit]
        return tuple(mutations)

    def _learned_prediction(self, feature: float, fallback: str) -> tuple[str, float]:
        if not self._prototypes:
            return fallback, 0.0
        label, (value, count) = min(self._prototypes.items(), key=lambda item: (abs(feature - item[1][0] / item[1][1]), item[0]))
        distance = abs(feature - value / count)
        return label, 1.0 / (1.0 + distance)

    def _readout_evidence(self, feature: float, fallback: str) -> tuple[str, float, tuple[tuple[str, float], ...], float, float, float]:
        if not self._prototypes:
            return fallback, 0.0, (), 0.0, 0.0, 0.0
        distances = tuple(sorted(
            (label, abs(feature - value / count)) for label, (value, count) in self._prototypes.items()))
        ordered = sorted(distances, key=lambda item: (item[1], item[0]))
        winning = ordered[0][1]
        runner_up = ordered[1][1] if len(ordered) > 1 else winning
        return ordered[0][0], 1.0 / (1.0 + winning), distances, winning, runner_up, runner_up - winning

    def _run_example(self, example: SyntheticExample, index: int, *, update: bool) -> _ExampleRun:
        config = self.config
        assert self._network is not None
        self._network.reset_character()
        classifier = StreamingCharacterClassifier(max_activity_events=config.max_points)
        neuron = self._network.neurons[index % len(self._network.neurons)]
        meter = LocalEnergyModel(f"meter-{index}", max_counter=config.max_points * 8)
        utility = RewardAdjustedUtility(energy_weight=config.energy_weight)
        ledger = EligibilityLedger(f"ledger-{index}", max_traces=config.prediction_capacity, decay_time_constant=4.0)
        predictor = LocalPredictor(f"predictor-{index}", max_outstanding=1, error_destination="errors")
        classifier.ingest_event(Event(0.0, example.example_id, "readout", START_CHARACTER, CharacterBoundary(index)))
        trace: list[tuple[object, ...]] = []
        feature = 0.0
        prediction_loss = 0.0
        for point_index, point in enumerate(example.points):
            timestamp = point.timestamp if point.timestamp is not None else float(point_index)
            routed_trace, activations, execution = self._network.process(
                neuron.neuron_id, timestamp, point.x + point.y, max_events=config.max_points * 8)
            activation = activations[-1]
            for routed_index, item in enumerate(routed_trace):
                meter.observe_event(Event(item[0], item[1], item[2], item[3], item[4]), cost=abs(activations[routed_index]))
            feature += sum(activations)
            trace.extend(routed_trace)
            if point_index:
                resolution = predictor.process_observation(
                    Event(timestamp, example.example_id, "predictor", "observation", Observation("next", activation)),
                    EventQueue(capacity=config.max_points * 8))
                if resolution.error is not None:
                    prediction_loss += abs(resolution.error.error)
            prediction = predictor.create_prediction("next", activation, timestamp=timestamp, expires_at=timestamp + 2.0)
            ledger.record_activity(Event(timestamp, neuron.neuron_id, ledger.ledger_id, "eligibility_activity",
                                         EligibilityActivity(f"{example.example_id}:{point_index}", abs(activation), prediction.prediction_id)))
            classifier.ingest_event(Event(timestamp, neuron.neuron_id, "readout", ACTIVITY_EVENT, sum(activations)))
        end_timestamp = max(float(len(example.points)),
                    float(example.points[-1].timestamp or len(example.points)))
        result = classifier.ingest_event(Event(end_timestamp, example.example_id, "readout",
                               END_CHARACTER, CharacterBoundary(index)))
        assert result is not None
        raw_prediction = result.label
        network_feature = feature / len(example.points)
        classifier_prediction = raw_prediction
        learned_prediction, learned_confidence, distances, winning_distance, runner_up_distance, margin = self._readout_evidence(
            network_feature, raw_prediction)
        prediction = learned_prediction if self._prototypes else raw_prediction
        confidence = learned_confidence if self._prototypes else result.confidence
        correct = prediction == example.label
        reward = 0.0 if config.reward_mode == "neutral" else (config.correct_reward if correct else config.incorrect_reward)
        if config.reward_mode == "sparse" and not correct:
            reward = 0.0
        message_timestamp = end_timestamp + config.reward_delay
        message = RewardMessage(f"{example.example_id}:result", reward, message_timestamp)
        utility.observe_reward(message)
        attribution = ledger.apply_signal(Event(message.timestamp, "utility", ledger.ledger_id, "reward",
                            RewardSignal(reward, trace_id=f"{example.example_id}:0")))
        readout_updated = False
        if update and config.learning_enabled:
            if example.label not in self._prototypes and len(self._prototypes) >= config.max_classes:
                raise BufferError("readout max_classes capacity reached")
            old_value, old_count = self._prototypes.get(example.label, (0.0, 0))
            self._prototypes[example.label] = (old_value + network_feature, old_count + 1)
            self._updates += 1
            readout_updated = True
        retained = 1 if config.activation_mode == "event_only" or utility.evaluate(meter.energy, reward).retain else 0
        routed_events = len(trace)
        representations = self.prototypes
        return _ExampleRun(example.example_id, example.label, classifier_prediction, prediction, network_feature, confidence, prediction_loss,
               meter.energy, routed_events, routed_events, retained, tuple(trace), execution, reward,
                           message.timestamp - end_timestamp if attribution.status == "matched" else 0.0,
                           utility.evaluate(meter.energy, reward).utility,
               neuron, routed_events - len(example.points), network_feature, readout_updated,
               representations, distances, learned_prediction, winning_distance, runner_up_distance, margin)

    def _execute(self, workload: tuple[SyntheticExample, ...], epoch: int, *, update: bool) -> EvaluationResult:
        runs = [self._run_example(example, index, update=update) for index, example in enumerate(workload)]
        self._last_neurons = tuple(run.neuron for run in runs)
        mutations = self._adapt_topology(runs, epoch) if update else ()
        counts: dict[str, int] = {}
        confusion: dict[tuple[str, str], int] = {}
        correct = 0
        per_class_correct: dict[str, int] = {}
        diagnostics: list[ReadoutDiagnostic] = []
        for example, run in zip(workload, runs):
            counts[example.label] = counts.get(example.label, 0) + 1
            confusion[(example.label, run.raw_prediction)] = confusion.get((example.label, run.raw_prediction), 0) + 1
            correct += int(run.raw_prediction == example.label)
            per_class_correct[example.label] = per_class_correct.get(example.label, 0) + int(run.raw_prediction == example.label)
            diagnostics.append(ReadoutDiagnostic(
                run.example_id, run.external_label, run.feature, run.classifier_prediction,
                run.raw_prediction, run.reward, run.readout_updated, run.class_representations,
                run.class_distances, run.nearest_class, run.winning_distance,
                run.runner_up_distance, run.margin, run.confidence))
        total = len(runs)
        represented = tuple(label for label, _, _ in self.prototypes)
        declared = tuple(sorted(counts))
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
            sum(run.confidence for run in runs) / total, sum(run.latency for run in runs) / total,
            sum(run.utility for run in runs),
            sum(run.neuron.activation != 0.0 for run in runs),
            sum(run.neuron.processed_events > 0 for run in runs),
            sum(run.neuron.activation != 0.0 for run in runs),
            sum(run.neuron.activation == 0.0 for run in runs) / total,
            **self._topology_metrics(mutations),
            per_class_accuracy=tuple(
                (label, per_class_correct.get(label, 0) / count)
                for label, count in sorted(counts.items())
            ),
            represented_classes=represented,
            missing_classes=tuple(label for label in declared if label not in represented),
            prototype_count=len(represented),
            starvation_count=sum(label not in represented for label in declared),
            mean_margin=sum(run.margin for run in runs) / total,
            readout_diagnostics=tuple(diagnostics),
            prediction_error_count=sum(run.loss > 0.0 for run in runs),
            execution_completed=all(run.execution.completed for run in runs),
            execution_budget_exhausted=any(run.execution.budget_exhausted for run in runs),
            configured_event_budget=sum(run.execution.configured_event_budget for run in runs),
            processed_event_count=sum(run.execution.processed_event_count for run in runs),
            pending_event_count=sum(run.execution.pending_event_count for run in runs),
            termination_reason=("budget_exhausted" if any(run.execution.budget_exhausted for run in runs) else "completed"),
        )
        predictions = tuple(run.raw_prediction for run in runs)
        trace = tuple(item for run in runs for item in run.trace)
        converged = len(self._history) > 0 and metrics == self._history[-1]
        return EvaluationResult(metrics, predictions, trace, converged, tuple(diagnostics))

    def evaluate(self, workload: tuple[SyntheticExample, ...]) -> EvaluationResult:
        _validate_workload(workload, self.config)
        self._ensure_topology(workload)
        return self._execute(workload, 0, update=False)

    def train(self, workload: tuple[SyntheticExample, ...], *, observer: TrainingObserver | None = None) -> TrainingResult:
        _validate_workload(workload, self.config)
        self._ensure_topology(workload)
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
    "EvaluationResult", "ExperimentConfig", "ExperimentMetrics", "ExperimentRunner", "ReadoutDiagnostic",
    "SyntheticExample", "TrainingObserver", "TrainingResult", "evaluate", "make_synthetic_workload", "train",
]