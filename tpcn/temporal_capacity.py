"""Luna-12K bounded capacity and causal path-shortening fixture."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random
from typing import Literal

from .canonical_neuron import TPCNNeuron
from .energy_utility import LocalEnergyModel, RewardAdjustedUtility
from .event_runtime import Event, EventQueue
from .predictive_coding import LocalPredictor, Observation
from .structural_plasticity import CandidateEvidence, StructuralPlasticityController
from .temporal_association import TemporalAssociationPolicy
from .topology import BoundedTopology


PolicyName = Literal["fixed", "baseline", "random", "temporal", "reversed"]
NODES = ("source", "n1", "n2", "target", "decoy", "zalternate", "zzsource")
TARGET_NODE = "target"
LONG_PATH = (("source", "n1"), ("n1", "n2"), ("n2", "target"))
CANDIDATE_ENDPOINTS = (
    ("source", "decoy"),
    ("source", "target"),
    ("zalternate", "target"),
    ("zzsource", "target"),
)


@dataclass(frozen=True, slots=True)
class CapacityPressureConfig:
    fan_in_limit: int = 2
    fan_out_limit: int = 2
    edge_capacity: int = 6
    routing_capacity: int = 6
    candidate_capacity: int = 8
    history_capacity: int = 8
    maximum_score: int = 8
    association_window: float = 1.0
    long_delay: float = 1.0
    shortcut_delay: float = 0.75
    max_growth_attempts: int = 3
    queue_capacity: int = 16
    max_events: int = 16
    temporal_observation_count: int = 6

    def __post_init__(self) -> None:
        for name in (
            "fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity",
            "candidate_capacity", "history_capacity", "maximum_score",
            "max_growth_attempts", "queue_capacity", "max_events",
            "temporal_observation_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for name in ("association_window", "long_delay", "shortcut_delay"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0.0:
                raise ValueError(f"{name} must be positive")
        if self.shortcut_delay >= self.long_delay * 3:
            raise ValueError("shortcut_delay must be shorter than the initial path")


@dataclass(frozen=True, slots=True)
class ReplayMetrics:
    event_count: int
    routed_event_count: int
    activation_count: int
    energy: float
    utility: float
    prediction_loss: float
    prediction_error_count: int
    accuracy: float
    class_separation: float
    active_edges: tuple[tuple[str, str], ...]
    path_hops: tuple[int, ...]
    path_delays: tuple[float, ...]
    target_arrivals: tuple[tuple[str, float, int, float], ...]
    target_states: tuple[tuple[str, float], ...]
    trace: tuple[tuple[object, ...], ...]
    digest: str


@dataclass(frozen=True, slots=True)
class CausalPathIntervention:
    edge: tuple[str, str]
    present: ReplayMetrics
    removed: ReplayMetrics
    changed: bool


@dataclass(frozen=True, slots=True)
class CapacityPressureMetrics:
    policy: PolicyName
    seed: int
    candidate_set: tuple[tuple[str, str], ...]
    candidates_exposed: int
    candidates_considered: int
    candidates_selected: int
    growth_attempts: int
    selected_candidates: tuple[tuple[str, str], ...]
    mutation_statuses: tuple[str, ...]
    accepted_additions: int
    rejected_mutations: int
    rejection_reasons: tuple[tuple[str, int], ...]
    duplicate_proposals: int
    edge_churn: int
    replacement_count: int
    candidate_scores: tuple[tuple[tuple[str, str], float], ...]
    observation_count: int
    observation_history_count: int
    edge_count: int
    edge_capacity: int
    fan_in_limit: int
    fan_out_limit: int
    fan_in_distribution: tuple[tuple[str, int], ...]
    fan_out_distribution: tuple[tuple[str, int], ...]
    fan_in_saturation: float
    fan_out_saturation: float
    global_edge_utilization: float
    active_edge_utilization: float
    convergent_fan_in_motifs: int
    pruned_edges: int
    topology_stabilized: bool
    topology_before: tuple[tuple[str, str, float], ...]
    topology_after: tuple[tuple[str, str, float], ...]
    before: ReplayMetrics
    after: ReplayMetrics
    shortest_path_hops_before: int | None
    shortest_path_hops_after: int | None
    shortest_path_delay_before: float | None
    shortest_path_delay_after: float | None
    path_shortening: float
    shortcut_selected: bool
    shortcut_used: bool
    temporal_preference: bool


@dataclass(frozen=True, slots=True)
class CapacityPressureResult:
    metrics: CapacityPressureMetrics
    causal_intervention: CausalPathIntervention | None


def _initial_topology(config: CapacityPressureConfig) -> BoundedTopology:
    return BoundedTopology.from_edges(
        NODES,
        tuple((source, destination, config.long_delay) for source, destination in LONG_PATH),
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        edge_capacity=config.edge_capacity,
        routing_capacity=config.routing_capacity,
    )


def _local_neighbors() -> dict[str, tuple[str, ...]]:
    return {
        "source": ("decoy", "target"),
        "zalternate": ("target",),
        "zzsource": ("target",),
    }


def _candidate_scores(policy: PolicyName, seed: int, config: CapacityPressureConfig) -> tuple[float, ...]:
    if policy == "baseline":
        return (3.0, 2.0, 1.0, 0.5)
    if policy == "random":
        generator = random.Random(seed)
        scores = list(range(1, len(CANDIDATE_ENDPOINTS) + 1))
        generator.shuffle(scores)
        return tuple(float(score) for score in scores)
    if policy == "temporal":
        temporal = _temporal_policy(config, reversed_order=False)
        scores = {(candidate.source, candidate.destination): float(candidate.score)
                  for candidate in temporal.candidates}
        return tuple(scores.get(endpoint, 0.0) for endpoint in CANDIDATE_ENDPOINTS)
    return (0.0,) * len(CANDIDATE_ENDPOINTS)


def _temporal_policy(config: CapacityPressureConfig, *, reversed_order: bool) -> TemporalAssociationPolicy:
    policy = TemporalAssociationPolicy(
        NODES,
        history_capacity=config.history_capacity,
        candidate_capacity=config.candidate_capacity,
        association_window=config.association_window,
        maximum_score=config.maximum_score,
        propagation_delay=config.shortcut_delay,
        local_neighbors=_local_neighbors(),
    )
    if reversed_order:
        observations = (
            ("target", 0.0), ("target", 0.5), ("target", 1.0),
            ("source", 1.5), ("source", 2.0), ("source", 2.5),
        )
    else:
        observations = (
            ("source", 0.0), ("target", 0.5),
            ("source", 1.0), ("target", 1.5),
            ("source", 2.0), ("target", 2.5),
        )
    for node, timestamp in observations:
        policy.observe("source", node, timestamp)
    return policy


def _candidates(policy: PolicyName, seed: int, config: CapacityPressureConfig) -> tuple[CandidateEvidence, ...]:
    scores = _candidate_scores(policy, seed, config)
    delay_by_endpoint = {("source", "target"): config.shortcut_delay}
    return tuple(
        CandidateEvidence(
            source, source, destination, score,
            delay_by_endpoint.get((source, destination), config.long_delay),
            f"{policy}-{source}-{destination}",
        )
        for (source, destination), score in zip(CANDIDATE_ENDPOINTS, scores)
    )


def _controller(config: CapacityPressureConfig) -> StructuralPlasticityController:
    return StructuralPlasticityController(
        _initial_topology(config),
        candidate_capacity=config.candidate_capacity,
        max_growth_per_adaptation=config.max_growth_attempts,
        local_neighbors=_local_neighbors(),
    )


def _grow(
    controller: StructuralPlasticityController,
    candidates: tuple[CandidateEvidence, ...],
    config: CapacityPressureConfig,
) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...], dict[str, int], int, int, int]:
    pending = list(candidates)
    statuses: list[str] = []
    selected_edges: list[tuple[str, str]] = []
    rejection_reasons: dict[str, int] = {}
    considered = 0
    duplicate_proposals = 0
    for _ in range(config.max_growth_attempts):
        if not pending:
            break
        considered += len(pending)
        selected = controller.select(tuple(pending))
        if selected is None:
            break
        pending.remove(selected)
        selected_edges.append((selected.source, selected.destination))
        result = controller.grow(selected)
        statuses.append(result.status)
        if result.status == "duplicate":
            duplicate_proposals += 1
        if result.status != "grown":
            reason = result.reason or result.status
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
    return (
        tuple(statuses), tuple(selected_edges), rejection_reasons,
        duplicate_proposals, considered, len(statuses),
    )


def _edge_records(topology: BoundedTopology) -> tuple[tuple[str, str, float], ...]:
    return tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in topology.edges)


def _replay(topology: BoundedTopology, config: CapacityPressureConfig) -> ReplayMetrics:
    examples = (("positive", 1.0), ("negative", -1.0))
    neurons = {node: TPCNNeuron(node, decay_rate=0.5, input_gain=1.0) for node in NODES}
    trace: list[tuple[object, ...]] = []
    active_edges: set[tuple[str, str]] = set()
    path_hops: list[int] = []
    path_delays: list[float] = []
    target_arrivals: list[tuple[str, float, int, float]] = []
    target_states: list[tuple[str, float]] = []
    total_energy = 0.0
    routed_event_count = 0
    prediction_loss = 0.0
    prediction_error_count = 0
    correct = 0
    for example_id, payload in examples:
        for neuron in neurons.values():
            neuron.reset()
        meter = LocalEnergyModel("luna-12k-meter", max_counter=config.max_events)
        predictor = LocalPredictor("luna-12k-predictor", max_outstanding=1, error_destination="prediction-errors")
        queue: EventQueue[Event] = EventQueue(config.queue_capacity)
        paths: dict[int, tuple[str, ...]] = {}
        queued = queue.push(Event(0.0, "source", "source", "signal", payload))
        paths[queued.sequence] = ("source",)
        processed = 0
        while queue and processed < config.max_events:
            pending = queue.peek()
            assert pending is not None
            event = queue.pop_ready(pending.timestamp)
            path = paths.pop(event.sequence)
            neuron = neurons[event.destination]
            activation = neuron.receive_event(event)
            meter.observe_event(event, cost=abs(activation))
            processed += 1
            trace.append((example_id, event.timestamp, event.source, event.destination, event.payload, path))
            if event.destination == "source":
                predictor.create_prediction(
                    "target", neurons[TARGET_NODE].activation,
                    timestamp=event.timestamp, expires_at=event.timestamp + 8.0,
                )
            if event.destination == TARGET_NODE:
                resolution = predictor.process_observation(
                    Event(event.timestamp, TARGET_NODE, "predictor", "observation",
                          Observation("target", neurons[TARGET_NODE].activation)),
                    EventQueue(config.queue_capacity),
                )
                if resolution.error is not None:
                    prediction_loss += abs(resolution.error.error)
                    prediction_error_count += 1
                    meter.observe_prediction_error(resolution.error)
                path_hops.append(len(path) - 1)
                path_delays.append(event.timestamp)
                target_arrivals.append((example_id, event.timestamp, len(path) - 1, activation))
            if event.destination in topology.nodes and len(path) < len(NODES) and event.destination not in path[:-1]:
                emitted = Event(event.timestamp, event.destination, event.destination, event.event_type, activation)
                routed = topology.route(emitted, queue)
                routed_event_count += len(routed)
                for routed_event in routed:
                    paths[routed_event.sequence] = path + (routed_event.destination,)
                    active_edges.add((routed_event.source, routed_event.destination))
        state = neurons[TARGET_NODE].state
        target_states.append((example_id, state))
        total_energy += meter.energy
        correct += int((state >= 0.0) == (payload >= 0.0))
    states = dict(target_states)
    separation = abs(states["positive"] - states["negative"])
    utility = RewardAdjustedUtility(energy_weight=1.0).evaluate(total_energy, float(correct)).utility
    digest = hashlib.sha256(repr((tuple(trace), tuple(target_states), topology.edges)).encode()).hexdigest()
    return ReplayMetrics(
        len(trace), routed_event_count, len(trace), total_energy, utility,
        prediction_loss, prediction_error_count, correct / len(examples), separation,
        tuple(sorted(active_edges)), tuple(path_hops), tuple(path_delays),
        tuple(target_arrivals), tuple(target_states), tuple(trace), digest,
    )


def _shortest_target_path(topology: BoundedTopology) -> tuple[int | None, float | None]:
    frontier = [("source", 0, 0.0)]
    visited: dict[str, tuple[int, float]] = {}
    while frontier:
        node, hops, delay = frontier.pop(0)
        prior = visited.get(node)
        if prior is not None and prior <= (hops, delay):
            continue
        visited[node] = (hops, delay)
        if node == TARGET_NODE:
            return hops, delay
        for edge in topology.outgoing(node):
            frontier.append((edge.destination, hops + 1, delay + float(edge.propagation_delay)))
    return None, None


def run_temporal_capacity(
    policy: PolicyName,
    *,
    seed: int = 0,
    config: CapacityPressureConfig | None = None,
    causal_intervention: bool = True,
) -> CapacityPressureResult:
    """Run one 12K policy with equal candidate exposure and bounded pressure."""
    if policy not in ("fixed", "baseline", "random", "temporal", "reversed"):
        raise ValueError("unknown policy")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    config = CapacityPressureConfig() if config is None else config
    controller = _controller(config)
    topology_before = _edge_records(controller.topology)
    before = _replay(controller.topology, config)
    candidates = _candidates("reversed" if policy == "reversed" else policy, seed, config)
    if policy == "fixed":
        statuses: tuple[str, ...] = ()
        selected_edges: tuple[tuple[str, str], ...] = ()
        rejection_reasons: dict[str, int] = {}
        duplicates = 0
        considered = len(candidates)
        attempts = 0
    else:
        statuses, selected_edges, rejection_reasons, duplicates, considered, attempts = _grow(
            controller, candidates, config
        )
    after = _replay(controller.topology, config)
    topology_after = _edge_records(controller.topology)
    fan_in = tuple((node, len(controller.topology.incoming(node))) for node in NODES)
    fan_out = tuple((node, len(controller.topology.outgoing(node))) for node in NODES)
    shortest_before_hops, shortest_before_delay = _shortest_target_path(_initial_topology(config))
    shortest_after_hops, shortest_after_delay = _shortest_target_path(controller.topology)
    shortcut = ("source", TARGET_NODE)
    shortcut_selected = shortcut in selected_edges and shortcut in {(edge[0], edge[1]) for edge in topology_after}
    edge_count = len(controller.topology)
    fan_in_saturation = max(value for _, value in fan_in) / config.fan_in_limit
    fan_out_saturation = max(value for _, value in fan_out) / config.fan_out_limit
    global_edge_utilization = edge_count / config.edge_capacity
    intervention = None
    if causal_intervention and shortcut_selected:
        assert controller.prune(*shortcut).status == "pruned"
        removed = _replay(controller.topology, config)
        intervention = CausalPathIntervention(shortcut, after, removed, after != removed)
    metrics = CapacityPressureMetrics(
        policy, seed, CANDIDATE_ENDPOINTS, len(candidates), considered, len(selected_edges), attempts,
        selected_edges, statuses, statuses.count("grown"), sum(rejection_reasons.values()),
        tuple(sorted(rejection_reasons.items())), duplicates, len(topology_before) + len(topology_after) - 2 * len(set(topology_before) & set(topology_after)),
        0, tuple((endpoint, score) for endpoint, score in zip(CANDIDATE_ENDPOINTS, _candidate_scores(policy if policy != "reversed" else "reversed", seed, config))),
        config.temporal_observation_count if policy in ("temporal", "reversed") else 0,
        config.temporal_observation_count if policy in ("temporal", "reversed") else 0,
        edge_count, config.edge_capacity, config.fan_in_limit, config.fan_out_limit,
        fan_in, fan_out,
        fan_in_saturation, fan_out_saturation, global_edge_utilization,
        len(after.active_edges) / max(1, edge_count),
        sum(value >= 2 for _, value in fan_in),
        1 if intervention is not None else 0,
        not rejection_reasons,
        topology_before, topology_after, before, after,
        shortest_before_hops, shortest_after_hops, shortest_before_delay, shortest_after_delay,
        0.0 if shortest_after_delay is None or shortest_before_delay is None else max(0.0, shortest_before_delay - shortest_after_delay),
        shortcut_selected, shortcut_selected and shortcut in set(after.active_edges),
        policy == "temporal" and shortcut_selected,
    )
    return CapacityPressureResult(metrics, intervention)


def run_temporal_capacity_suite(
    *, seeds: tuple[int, ...] = (0, 1, 2, 3, 4), config: CapacityPressureConfig | None = None,
) -> tuple[CapacityPressureResult, ...]:
    results = []
    for seed in seeds:
        for policy in ("fixed", "baseline", "random", "temporal", "reversed"):
            results.append(run_temporal_capacity(policy, seed=seed, config=config))
    return tuple(results)


__all__ = [
    "CANDIDATE_ENDPOINTS", "CapacityPressureConfig", "CapacityPressureMetrics",
    "CapacityPressureResult", "CausalPathIntervention", "LONG_PATH", "NODES",
    "PolicyName", "ReplayMetrics", "run_temporal_capacity", "run_temporal_capacity_suite",
]