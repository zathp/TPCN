"""Bounded, deterministic experiments over the public TPCN interfaces.

Labels are external metadata. They are consulted only after a label-free
canonical event stream has produced a readout, then may update this runner's
bounded outer-loop readout through reward and eligibility signals.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import math
import random
from types import MappingProxyType
from typing import Callable, Literal

from .canonical_neuron import TPCNNeuron
from .eligibility import EligibilityActivity, EligibilityLedger, RewardSignal
from .energy_utility import LocalEnergyModel, RewardAdjustedUtility, RewardMessage
from .event_runtime import BoundedExecutionResult, Event, EventQueue, execute_bounded
from .excursion_neuron import E1Config, MultiExcursionNeuron
from .experiment_excursion_runtime import ExcursionCharacterRuntime
from .predictive_coding import LocalPredictor, Observation
from .streaming_classifier import ACTIVITY_EVENT, StreamingCharacterClassifier
from .stroke_dataset import CharacterBoundary, END_CHARACTER, START_CHARACTER, StrokePoint
from .structural_plasticity import CandidateEvidence, StructuralPlasticityController
from .structural_observation import StructuralObservationPlane, StructuralObservationSnapshot
from .topology import BoundedTopology

ActivationMode = Literal["event_only", "utility"]
RewardMode = Literal["dense", "sparse", "neutral"]
StructuralPolicy = Literal["fixed", "baseline", "random", "temporal", "reversed", "e2_local_temporal"]
NeuronModel = Literal["EXCURSION_V1", "TANH_LEGACY"]


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
    structural_observation: bool = False
    structural_neighbors: Mapping[str, tuple[str, ...]] | None = None
    structural_neighborhood_limit: int | None = None
    structural_reverse_observer_limit: int | None = None
    structural_association_window: float | None = None
    structural_history_capacity: int | None = None
    structural_candidate_capacity: int | None = None
    structural_maximum_score: int | None = None
    structural_growth_delay: float | None = None
    structural_growth_attempt_budget: int | None = None
    topology_fan_in: int = 2
    topology_fan_out: int = 2
    topology_edge_capacity: int = 8
    topology_initial_edges: int = 1
    topology_node_count: int | None = None
    mutation_history_limit: int = 32
    candidate_capacity: int = 16
    max_growth_per_epoch: int = 1
    neuron_model: NeuronModel = "EXCURSION_V1"
    queue_capacity: int = 128
    event_budget: int = 4096
    settling_horizon: float = 4.0
    prediction_expiry: float = 4.0

    def __post_init__(self) -> None:
        for name in ("epochs", "history_limit", "max_points", "prediction_capacity", "max_classes",
                     "queue_capacity", "event_budget"):
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
        if not isinstance(self.structural_observation, bool):
            raise TypeError("structural_observation must be a boolean")
        if self.structural_policy not in ("fixed", "baseline", "random", "temporal", "reversed", "e2_local_temporal"):
            raise ValueError("structural_policy must be a supported policy")
        if self.activation_mode not in ("event_only", "utility"):
            raise ValueError("activation_mode must be 'event_only' or 'utility'")
        if self.reward_mode not in ("dense", "sparse", "neutral"):
            raise ValueError("reward_mode must be 'dense', 'sparse', or 'neutral'")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise TypeError("seed must be an integer")
        if not isinstance(self.learning_enabled, bool):
            raise TypeError("learning_enabled must be a boolean")
        if self.neuron_model not in ("EXCURSION_V1", "TANH_LEGACY"):
            raise ValueError("neuron_model must be 'EXCURSION_V1' or 'TANH_LEGACY'")
        if self.structural_neighbors is not None:
            if not isinstance(self.structural_neighbors, Mapping):
                raise TypeError("structural_neighbors must be a mapping")
            normalized_neighbors: dict[str, tuple[str, ...]] = {}
            for source, destinations in self.structural_neighbors.items():
                if not isinstance(source, str) or not source:
                    raise ValueError("structural neighbor sources must be non-empty strings")
                if isinstance(destinations, (str, bytes)):
                    raise ValueError("structural neighbor values must be node collections")
                try:
                    neighbors = tuple(destinations)
                except TypeError as error:
                    raise ValueError("structural neighbor values must be iterable") from error
                if any(not isinstance(node, str) or not node for node in neighbors):
                    raise ValueError("structural neighbor IDs must be non-empty strings")
                if len(neighbors) != len(set(neighbors)):
                    raise ValueError(f"structural neighbors for {source!r} must be unique")
                if source in neighbors:
                    raise ValueError("structural neighbors cannot contain the source")
                normalized_neighbors[source] = tuple(sorted(neighbors))
            object.__setattr__(
                self,
                "structural_neighbors",
                MappingProxyType(dict(sorted(normalized_neighbors.items()))),
            )
        if self.structural_observation and self.neuron_model != "EXCURSION_V1":
            raise ValueError("structural observation requires EXCURSION_V1 emissions")
        if self.neuron_model == "EXCURSION_V1" and self.structural_plasticity:
            if not self.structural_observation:
                raise ValueError(
                    "structural plasticity is unavailable unless structural observation is enabled"
                )
            if self.structural_policy != "e2_local_temporal":
                raise ValueError(
                    "EXCURSION_V1 growth requires structural_policy='e2_local_temporal'; "
                    "legacy structural policies are unsupported"
                )
        if self.neuron_model == "EXCURSION_V1" and self.structural_observation:
            integer_bounds = (
                ("structural_neighborhood_limit", self.structural_neighborhood_limit),
                ("structural_reverse_observer_limit", self.structural_reverse_observer_limit),
                ("structural_history_capacity", self.structural_history_capacity),
                ("structural_candidate_capacity", self.structural_candidate_capacity),
                ("structural_maximum_score", self.structural_maximum_score),
                ("structural_growth_attempt_budget", self.structural_growth_attempt_budget),
            )
            for name, value in integer_bounds:
                if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                    raise ValueError(f"{name} must be explicitly set to a positive integer")
            for name, value in (
                ("structural_association_window", self.structural_association_window),
                ("structural_growth_delay", self.structural_growth_delay),
            ):
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(float(value))
                    or float(value) <= 0.0
                ):
                    raise ValueError(f"{name} must be explicitly set to a finite positive number")
            if self.structural_neighbors is None:
                raise ValueError("structural_neighbors must be explicitly provided")
        for name in ("energy_weight", "reward_delay", "correct_reward", "incorrect_reward",
                     "settling_horizon", "prediction_expiry"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be a real number")
            if not math.isfinite(float(value)):
                raise ValueError(f"{name} must be finite")
        if min(self.energy_weight, self.reward_delay, self.settling_horizon, self.prediction_expiry) < 0.0:
            raise ValueError("energy, delay, settling horizon and prediction expiry must be nonnegative")
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
    peak_queue_occupancy: int = 0
    beyond_deadline_event_count: int = 0
    incomplete_settling_count: int = 0
    excursion_count: int = 0
    silent_event_count: int = 0
    matched_prediction_count: int = 0
    unmatched_prediction_count: int = 0
    expired_prediction_count: int = 0
    matched_credit_count: int = 0
    unmatched_credit_count: int = 0
    event_processing_proxy: float = 0.0
    emitted_amplitude_proxy: float = 0.0
    edge_transfer_proxy: float = 0.0
    prediction_error_proxy: float = 0.0
    maximum_route_depth: int = 0
    provenance_truncated_count: int = 0
    structural_emission_count: int = 0
    structural_observation_work: int = 0
    structural_candidate_count: int = 0
    structural_candidate_rejections: int = 0
    structural_growth_attempts: int = 0
    structural_growth_attempt_budget: int = 0
    structural_growth_budget_remaining: int = 0
    structural_growth_budget_exhausted: bool = False
    structural_decisions: tuple[StructuralDecision, ...] = ()


@dataclass(frozen=True, slots=True)
class StructuralDecision:
    """One bounded post-character evidence and growth decision."""

    evidence: StructuralObservationSnapshot
    selected_candidate: CandidateEvidence | None
    candidate_rank: int | None
    status: str
    reason: str | None
    growth_attempted: bool
    topology_before: tuple[tuple[str, str, float], ...]
    topology_after: tuple[tuple[str, str, float], ...]


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


TrainingObserver = Callable[[int, tuple[TPCNNeuron | MultiExcursionNeuron, ...], ExperimentMetrics], None]


class _ComputationalNetwork:
    """Persistent neurons and bounded causal routing for one experiment."""

    def __init__(
        self,
        nodes: tuple[str, ...],
        topology: BoundedTopology,
        queue_capacity: int,
        neuron_model: NeuronModel,
    ) -> None:
        if neuron_model == "TANH_LEGACY":
            self.neurons: tuple[TPCNNeuron | MultiExcursionNeuron, ...] = tuple(
                TPCNNeuron(node, input_gain=0.5) for node in nodes
            )
        else:
            self.neurons = tuple(
                MultiExcursionNeuron(node, config=E1Config(event_budget=queue_capacity * 16))
                for node in nodes
            )
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
    neuron: TPCNNeuron | MultiExcursionNeuron
    routed_events: int
    propagated_activity: float
    readout_updated: bool
    class_representations: tuple[tuple[str, float, int], ...]
    class_distances: tuple[tuple[str, float], ...]
    nearest_class: str
    winning_distance: float
    runner_up_distance: float
    margin: float
    excursion_count: int = 0
    silent_event_count: int = 0
    peak_queue_occupancy: int = 0
    beyond_deadline_event_count: int = 0
    incomplete_settling: bool = False
    matched_prediction_count: int = 0
    unmatched_prediction_count: int = 0
    expired_prediction_count: int = 0
    matched_credit_count: int = 0
    unmatched_credit_count: int = 0
    energy_components: tuple[tuple[str, float], ...] = ()
    maximum_route_depth: int = 0
    provenance_truncated: bool = False
    active_network_neuron_count: int = 0
    receiving_network_neuron_count: int = 0
    emitting_network_neuron_count: int = 0
    structural_decision: StructuralDecision | None = None
    structural_budget_exhausted: bool = False


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
        self._last_neurons: tuple[TPCNNeuron | MultiExcursionNeuron, ...] = ()
        self._topology: BoundedTopology | None = None
        self._plasticity: StructuralPlasticityController | None = None
        self._mutation_history: list[tuple[str, str, str, str]] = []
        self._mutation_rejection_reasons: dict[str, int] = {}
        self._last_mutation_rejection_reasons: dict[str, int] = {}
        self._network: _ComputationalNetwork | None = None
        self._structural_growth_attempts = 0
        self._structural_budget_exhaustions = 0
        self._structural_pass_attempts = 0
        self._structural_pass_admissions = 0
        self._structural_pass_rejections = 0
        self._structural_decision_history: deque[StructuralDecision] = deque(
            maxlen=self.config.mutation_history_limit
        )
        self._structural_pass_decisions: deque[StructuralDecision] | None = None
        self._last_structural_snapshot: StructuralObservationSnapshot | None = None
        self._active_runtime: ExcursionCharacterRuntime | None = None

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
    def last_neurons(self) -> tuple[TPCNNeuron | MultiExcursionNeuron, ...]:
        """Publicly observable neurons from the most recent workload pass."""
        return self._last_neurons

    @property
    def topology(self) -> BoundedTopology | None:
        return self._topology

    @property
    def plasticity(self) -> StructuralPlasticityController | None:
        return self._plasticity

    @property
    def structural_decisions(self) -> tuple[StructuralDecision, ...]:
        return tuple(self._structural_decision_history)

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
        if self.config.neuron_model == "EXCURSION_V1" and self.config.structural_observation:
            assert self.config.structural_neighbors is not None
            assert self.config.structural_neighborhood_limit is not None
            assert self.config.structural_reverse_observer_limit is not None
            assert self.config.structural_history_capacity is not None
            assert self.config.structural_candidate_capacity is not None
            assert self.config.structural_association_window is not None
            assert self.config.structural_maximum_score is not None
            assert self.config.structural_growth_delay is not None
            locality = self.config.structural_neighbors
            StructuralObservationPlane(
                nodes,
                locality,
                neighborhood_limit=self.config.structural_neighborhood_limit,
                reverse_observer_limit=self.config.structural_reverse_observer_limit,
                history_capacity=self.config.structural_history_capacity,
                candidate_capacity=self.config.structural_candidate_capacity,
                association_window=self.config.structural_association_window,
                maximum_score=self.config.structural_maximum_score,
                propagation_delay=self.config.structural_growth_delay,
            )
        else:
            locality = {
                node: tuple(candidate for candidate in nodes if candidate != node)
                for node in nodes
            }
        controller_candidate_capacity = (
            len(nodes) * self.config.structural_candidate_capacity
            if self.config.neuron_model == "EXCURSION_V1" and self.config.structural_observation
            else self.config.candidate_capacity
        )
        self._plasticity = StructuralPlasticityController(
            self._topology, candidate_capacity=controller_candidate_capacity,
            max_growth_per_adaptation=self.config.max_growth_per_epoch,
            minimum_edge_count=0, local_neighbors=locality)
        self._network = _ComputationalNetwork(
            nodes,
            self._topology,
            self.config.queue_capacity,
            self.config.neuron_model,
        )
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

    def _record_structural_decision(self, decision: StructuralDecision) -> None:
        self._structural_decision_history.append(decision)
        if self._structural_pass_decisions is not None:
            self._structural_pass_decisions.append(decision)

    def _attempt_e2_growth(
        self,
        evidence: StructuralObservationSnapshot,
        *,
        successful_settling: bool,
        update: bool,
    ) -> tuple[StructuralDecision, bool]:
        assert self._topology is not None
        before = tuple(
            (edge.source, edge.destination, float(edge.propagation_delay))
            for edge in self._topology.edges
        )
        selected: CandidateEvidence | None = None
        rank: int | None = None
        attempted = False
        budget_exhausted = False
        retained_evidence = evidence
        status = "observation_only" if not self.config.structural_plasticity else "no_candidate"
        reason: str | None = None
        if not successful_settling:
            status = "discarded"
            reason = "incomplete_settling"
            retained_evidence = StructuralObservationSnapshot((), (), 0, 0, 0, ())
        elif not update:
            status = "evaluation_only"
            reason = "topology_mutation_disabled_for_evaluation"
        elif not self.config.structural_plasticity:
            status = "observation_only"
        elif evidence.candidates:
            budget = self.config.structural_growth_attempt_budget
            assert budget is not None
            if self._structural_growth_attempts >= budget:
                status = "budget_exhausted"
                reason = "growth_attempt_budget"
                self._structural_budget_exhaustions += 1
                budget_exhausted = True
                retained_evidence = StructuralObservationSnapshot((), (), 0, 0, 0, ())
            else:
                if self._active_runtime is not None:
                    raise RuntimeError("structural growth cannot run while an E2 runtime is active")
                assert self._plasticity is not None
                selected = self._plasticity.select(evidence.candidates)
                if selected is None:
                    status = "candidate_unavailable"
                    reason = "no_valid_candidate"
                else:
                    rank = evidence.candidates.index(selected) + 1
                    self._structural_growth_attempts += 1
                    attempted = True
                    mutation = self._plasticity.grow(selected)
                    status = mutation.status
                    reason = mutation.reason
                    self._structural_pass_attempts += 1
                    self._topology = self._plasticity.topology
                    assert self._network is not None
                    self._network.set_topology(self._topology)
                    source = selected.source
                    destination = selected.destination
                    mutation_reason = reason or "e2_local_temporal"
                    self._mutation_history.append(
                        (status, source, destination, mutation_reason)
                    )
                    del self._mutation_history[:-self.config.mutation_history_limit]
                    if status not in ("grown", "pruned"):
                        self._structural_pass_rejections += 1
                        rejection = reason or status
                        self._mutation_rejection_reasons[rejection] = (
                            self._mutation_rejection_reasons.get(rejection, 0) + 1
                        )
                        self._last_mutation_rejection_reasons[rejection] = (
                            self._last_mutation_rejection_reasons.get(rejection, 0) + 1
                        )
                    elif status == "grown":
                        self._structural_pass_admissions += 1
        after = tuple(
            (edge.source, edge.destination, float(edge.propagation_delay))
            for edge in self._topology.edges
        )
        decision = StructuralDecision(
            retained_evidence,
            selected,
            rank,
            status,
            reason,
            attempted,
            before,
            after,
        )
        if update:
            self._record_structural_decision(decision)
        return decision, budget_exhausted

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
        if self.config.neuron_model == "TANH_LEGACY":
            return self._run_legacy_example(example, index, update=update)
        return self._run_excursion_example(example, index, update=update)

    def _run_legacy_example(self, example: SyntheticExample, index: int, *, update: bool) -> _ExampleRun:
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
                            RewardSignal(reward, message_id=f"{example.example_id}:reward",
                                         trace_id=f"{example.example_id}:0")))
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

    def _run_excursion_example(self, example: SyntheticExample, index: int, *, update: bool) -> _ExampleRun:
        config = self.config
        assert self._network is not None
        plane: StructuralObservationPlane | None = None
        if config.structural_observation:
            assert config.structural_neighbors is not None
            assert config.structural_neighborhood_limit is not None
            assert config.structural_reverse_observer_limit is not None
            assert config.structural_history_capacity is not None
            assert config.structural_candidate_capacity is not None
            assert config.structural_association_window is not None
            assert config.structural_maximum_score is not None
            assert config.structural_growth_delay is not None
            plane = StructuralObservationPlane(
                self._network.topology.nodes,
                config.structural_neighbors,
                neighborhood_limit=config.structural_neighborhood_limit,
                reverse_observer_limit=config.structural_reverse_observer_limit,
                history_capacity=config.structural_history_capacity,
                candidate_capacity=config.structural_candidate_capacity,
                association_window=config.structural_association_window,
                maximum_score=config.structural_maximum_score,
                propagation_delay=config.structural_growth_delay,
            )
        self._last_structural_snapshot = None
        neurons = self._network.neurons
        if not all(isinstance(neuron, MultiExcursionNeuron) for neuron in neurons):
            raise RuntimeError("EXCURSION_V1 network contains a non-E2 neuron")
        self._network.reset_character()
        input_neuron = neurons[index % len(neurons)]
        assert isinstance(input_neuron, MultiExcursionNeuron)
        runtime = ExcursionCharacterRuntime(
            neurons,
            self._topology,
            queue_capacity=config.queue_capacity,
            event_budget=config.event_budget,
            settling_horizon=config.settling_horizon,
            prediction_capacity=config.prediction_capacity,
            prediction_expiry=config.prediction_expiry,
            max_activity_events=config.event_budget,
            namespace=f"experiment-{config.seed}",
            emission_observer=None if plane is None else plane.observe_emission,
        )
        first_timestamp = (
            example.points[0].timestamp
            if example.points[0].timestamp is not None
            else 0.0
        )
        runtime.start_character(
            example.example_id,
            index,
            timestamp=first_timestamp,
            predictor_source=input_neuron.neuron_id,
            readout_sources=(neuron.neuron_id for neuron in neurons),
            input_destination=input_neuron.neuron_id,
        )
        point_index = 0
        while point_index < len(example.points):
            point = example.points[point_index]
            timestamp = point.timestamp if point.timestamp is not None else float(point_index)
            batch: list[tuple[float, float]] = []
            while point_index < len(example.points):
                current = example.points[point_index]
                current_timestamp = (
                    current.timestamp if current.timestamp is not None else float(point_index)
                )
                if current_timestamp != timestamp:
                    break
                batch.append((timestamp, current.x + current.y))
                point_index += 1
            runtime.admit_external_batch(batch)
        last_point = example.points[-1]
        last_timestamp = (
            last_point.timestamp
            if last_point.timestamp is not None
            else float(len(example.points) - 1)
        )
        selected: dict[str, object] = {}

        def resolve_reward(result: object, feature: float) -> float:
            label_free = result
            raw_prediction = getattr(label_free, "label")
            classifier_prediction = raw_prediction
            learned_prediction, learned_confidence, distances, winning, runner_up, margin = (
                self._readout_evidence(feature, raw_prediction)
            )
            prediction = learned_prediction if self._prototypes else raw_prediction
            confidence = learned_confidence if self._prototypes else getattr(label_free, "confidence")
            reward = (
                0.0
                if config.reward_mode == "neutral"
                else (config.correct_reward if prediction == example.label else config.incorrect_reward)
            )
            if config.reward_mode == "sparse" and prediction != example.label:
                reward = 0.0
            selected.update(
                classifier_prediction=classifier_prediction,
                raw_prediction=prediction,
                confidence=confidence,
                learned_prediction=learned_prediction,
                distances=distances,
                winning=winning,
                runner_up=runner_up,
                margin=margin,
            )
            return reward

        self._active_runtime = runtime
        try:
            result = runtime.end_character(
                last_external_timestamp=last_timestamp,
                reward=resolve_reward,
                reward_delay=config.reward_delay,
                reward_message_id=f"{example.example_id}:reward",
            )
        finally:
            runtime.reset()
            self._active_runtime = None
        structural_decision: StructuralDecision | None = None
        structural_budget_exhausted = False
        if plane is not None:
            frozen_evidence = plane.freeze()
            structural_decision, structural_budget_exhausted = self._attempt_e2_growth(
                frozen_evidence,
                successful_settling=(
                    not result.incomplete_settling
                    and result.execution.completed
                    and not result.execution.budget_exhausted
                ),
                update=update,
            )
            self._last_structural_snapshot = structural_decision.evidence
        network_feature = result.feature
        prediction = str(selected["raw_prediction"])
        raw_classifier_prediction = str(selected["classifier_prediction"])
        confidence = float(selected["confidence"])
        readout_updated = False
        if update and config.learning_enabled:
            if example.label not in self._prototypes and len(self._prototypes) >= config.max_classes:
                raise BufferError("readout max_classes capacity reached")
            old_value, old_count = self._prototypes.get(example.label, (0.0, 0))
            self._prototypes[example.label] = (old_value + network_feature, old_count + 1)
            self._updates += 1
            readout_updated = True
        utility = result.utility
        retained = 1 if config.activation_mode == "event_only" or utility > 0.0 else 0
        distances = selected["distances"]
        representations = self.prototypes
        return _ExampleRun(
            example_id=example.example_id,
            external_label=example.label,
            classifier_prediction=raw_classifier_prediction,
            raw_prediction=prediction,
            feature=network_feature,
            confidence=confidence,
            loss=result.prediction_loss,
            energy=result.energy,
            events=result.execution.processed_event_count,
            activations=result.emission_count,
            retained=retained,
            trace=result.trace,
            execution=result.execution,
            reward=result.reward,
            latency=result.reward_update_latency,
            utility=utility,
            neuron=input_neuron,
            routed_events=result.execution.processed_event_count,
            propagated_activity=network_feature,
            readout_updated=readout_updated,
            class_representations=representations,
            class_distances=distances,
            nearest_class=str(selected["learned_prediction"]),
            winning_distance=float(selected["winning"]),
            runner_up_distance=float(selected["runner_up"]),
            margin=float(selected["margin"]),
            excursion_count=result.emission_count,
            silent_event_count=result.silent_event_count,
            peak_queue_occupancy=result.peak_queue_occupancy,
            beyond_deadline_event_count=result.beyond_deadline_event_count,
            incomplete_settling=result.incomplete_settling,
            matched_prediction_count=result.matched_predictions,
            unmatched_prediction_count=result.unmatched_predictions,
            expired_prediction_count=result.expired_predictions,
            matched_credit_count=result.matched_credit,
            unmatched_credit_count=result.unmatched_credit,
            energy_components=result.energy_components,
            maximum_route_depth=result.max_route_depth,
            provenance_truncated=result.provenance_truncated,
            active_network_neuron_count=result.active_neuron_count,
            receiving_network_neuron_count=result.receiving_neuron_count,
            emitting_network_neuron_count=result.emitting_neuron_count,
            structural_decision=structural_decision,
            structural_budget_exhausted=structural_budget_exhausted,
        )

    def _execute(self, workload: tuple[SyntheticExample, ...], epoch: int, *, update: bool) -> EvaluationResult:
        self._structural_pass_decisions = deque(maxlen=self.config.mutation_history_limit)
        self._structural_pass_attempts = 0
        self._structural_pass_admissions = 0
        self._structural_pass_rejections = 0
        if self.config.neuron_model == "EXCURSION_V1":
            self._last_mutation_rejection_reasons = {}
        try:
            runs = [
                self._run_example(example, index, update=update)
                for index, example in enumerate(workload)
            ]
        finally:
            pass_decisions = tuple(self._structural_pass_decisions)
            self._structural_pass_decisions = None
        self._last_neurons = tuple(run.neuron for run in runs)
        if update and self.config.neuron_model == "TANH_LEGACY":
            mutations = self._adapt_topology(runs, epoch)
        else:
            mutations = tuple(
                (
                    decision.status,
                    decision.selected_candidate.source,
                    decision.selected_candidate.destination,
                    decision.reason or "e2_local_temporal",
                )
                for decision in pass_decisions
                if decision.growth_attempted and decision.selected_candidate is not None
            )
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
        topology_metrics = self._topology_metrics(mutations)
        if self.config.neuron_model == "EXCURSION_V1":
            topology_metrics.update(
                mutation_count=self._structural_pass_attempts,
                accepted_additions=self._structural_pass_admissions,
                pruned_connections=0,
                rejected_mutations=self._structural_pass_rejections,
            )
        metrics = ExperimentMetrics(
            epoch, correct / total, sum(run.loss for run in runs) / total, reward,
            sum(run.energy for run in runs), sum(run.events for run in runs),
            sum(run.activations for run in runs), sum(run.retained for run in runs),
            reward / total, cumulative_reward, self._updates,
            tuple(sorted(counts.items())), tuple((key[0], key[1], value) for key, value in sorted(confusion.items())),
            sum(run.confidence for run in runs) / total, sum(run.latency for run in runs) / total,
            sum(run.utility for run in runs),
            sum(
                run.active_network_neuron_count
                if isinstance(run.neuron, MultiExcursionNeuron)
                else int(run.neuron.activation != 0.0)
                for run in runs
            ),
            sum(
                run.receiving_network_neuron_count
                if isinstance(run.neuron, MultiExcursionNeuron)
                else int(run.neuron.processed_events > 0)
                for run in runs
            ),
            sum(
                run.emitting_network_neuron_count
                if isinstance(run.neuron, MultiExcursionNeuron)
                else int(run.neuron.activation != 0.0)
                for run in runs
            ),
            sum(
                1.0 - run.emitting_network_neuron_count / max(1, len(self._last_neurons))
                if isinstance(run.neuron, MultiExcursionNeuron)
                else float(run.neuron.activation == 0.0)
                for run in runs
            ) / total,
            **topology_metrics,
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
            prediction_error_count=sum(run.matched_prediction_count for run in runs),
            execution_completed=all(run.execution.completed for run in runs),
            execution_budget_exhausted=any(run.execution.budget_exhausted for run in runs),
            configured_event_budget=sum(run.execution.configured_event_budget for run in runs),
            processed_event_count=sum(run.execution.processed_event_count for run in runs),
            pending_event_count=sum(run.execution.pending_event_count for run in runs),
            termination_reason=("budget_exhausted" if any(run.execution.budget_exhausted for run in runs) else "completed"),
            peak_queue_occupancy=max((run.peak_queue_occupancy for run in runs), default=0),
            beyond_deadline_event_count=sum(run.beyond_deadline_event_count for run in runs),
            incomplete_settling_count=sum(run.incomplete_settling for run in runs),
            excursion_count=sum(run.excursion_count for run in runs),
            silent_event_count=sum(run.silent_event_count for run in runs),
            matched_prediction_count=sum(run.matched_prediction_count for run in runs),
            unmatched_prediction_count=sum(run.unmatched_prediction_count for run in runs),
            expired_prediction_count=sum(run.expired_prediction_count for run in runs),
            matched_credit_count=sum(run.matched_credit_count for run in runs),
            unmatched_credit_count=sum(run.unmatched_credit_count for run in runs),
            event_processing_proxy=sum(
                dict(run.energy_components).get("event_processing", 0.0) for run in runs
            ),
            emitted_amplitude_proxy=sum(
                dict(run.energy_components).get("emitted_amplitude", 0.0) for run in runs
            ),
            edge_transfer_proxy=sum(
                dict(run.energy_components).get("edge_transfer", 0.0) for run in runs
            ),
            prediction_error_proxy=sum(
                dict(run.energy_components).get("prediction_error", 0.0) for run in runs
            ),
            maximum_route_depth=max((run.maximum_route_depth for run in runs), default=0),
            provenance_truncated_count=sum(run.provenance_truncated for run in runs),
            structural_emission_count=sum(
                run.structural_decision.evidence.observation_count
                for run in runs
                if run.structural_decision is not None
            ),
            structural_observation_work=sum(
                run.structural_decision.evidence.observation_work
                for run in runs
                if run.structural_decision is not None
            ),
            structural_candidate_count=sum(
                len(run.structural_decision.evidence.candidates)
                for run in runs
                if run.structural_decision is not None
            ),
            structural_candidate_rejections=sum(
                run.structural_decision.evidence.candidate_rejections
                for run in runs
                if run.structural_decision is not None
            ),
            structural_growth_attempts=sum(
                run.structural_decision.growth_attempted
                for run in runs
                if run.structural_decision is not None
            ),
            structural_growth_attempt_budget=(
                self.config.structural_growth_attempt_budget or 0
            ),
            structural_growth_budget_remaining=(
                max(
                    0,
                    self.config.structural_growth_attempt_budget
                    - self._structural_growth_attempts,
                )
                if self.config.structural_growth_attempt_budget is not None
                else 0
            ),
            structural_growth_budget_exhausted=any(
                run.structural_budget_exhausted for run in runs
            ),
            structural_decisions=pass_decisions,
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
    "StructuralDecision",
    "SyntheticExample", "TrainingObserver", "TrainingResult", "evaluate", "make_synthetic_workload", "train",
]