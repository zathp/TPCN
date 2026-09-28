"""Controlled Luna-12J efficacy and causal-intervention fixture.

The fixture is intentionally small: it isolates temporal fan-in formation while
using the same bounded topology, mutation controller, event queue and neuron
path as the CPU reference. Labels are evaluation metadata only.
"""

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
NODES = ("a", "b", "target", "d1", "d2")
SOURCE_NODES = ("a", "b")
TARGET_NODE = "target"


@dataclass(frozen=True, slots=True)
class TemporalEfficacyConfig:
    fan_in_limit: int = 2
    fan_out_limit: int = 2
    edge_capacity: int = 4
    candidate_capacity: int = 8
    history_capacity: int = 8
    maximum_score: int = 8
    propagation_delay: float = 1.0
    max_growth_attempts: int = 2
    queue_capacity: int = 16
    max_events: int = 16

    def __post_init__(self) -> None:
        for name in ("fan_in_limit", "fan_out_limit", "edge_capacity", "candidate_capacity",
                     "history_capacity", "maximum_score", "max_growth_attempts",
                     "queue_capacity", "max_events"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if isinstance(self.propagation_delay, bool) or not isinstance(self.propagation_delay, (int, float)):
            raise TypeError("propagation_delay must be a real number")
        if self.propagation_delay <= 0.0:
            raise ValueError("propagation_delay must be positive")


@dataclass(frozen=True, slots=True)
class CausalIntervention:
    edge: tuple[str, str]
    present_event_count: int
    removed_event_count: int
    present_target_state: float
    removed_target_state: float
    changed: bool


@dataclass(frozen=True, slots=True)
class TemporalEfficacyMetrics:
    policy: PolicyName
    seed: int
    accuracy: float
    class_separation: float
    prediction_loss: float
    prediction_error_count: int
    event_count: int
    activation_count: int
    energy: float
    energy_unit: str
    utility: float
    edge_count: int
    edge_capacity: int
    accepted_additions: int
    removed_edges: int
    rejected_mutations: int
    rejection_reasons: tuple[tuple[str, int], ...]
    candidate_count: int
    candidate_proposals: int
    candidate_space_size: int
    duplicate_proposals: int
    fan_in_distribution: tuple[tuple[str, int], ...]
    fan_out_distribution: tuple[tuple[str, int], ...]
    convergent_fan_in_motifs: int
    active_edge_count: int
    active_edge_utilization: float
    mean_path_length: float
    mean_path_delay: float
    shortest_target_delay: float | None
    path_shortening: float
    topology_stabilized: bool
    topology_edges: tuple[tuple[str, str, float], ...]
    mutation_statuses: tuple[str, ...]
    target_states: tuple[tuple[str, float], ...]
    replay_digest: str


@dataclass(frozen=True, slots=True)
class TemporalEfficacyResult:
    metrics: TemporalEfficacyMetrics
    causal_intervention: CausalIntervention | None


@dataclass(frozen=True, slots=True)
class _Example:
    example_id: str
    label: str
    inputs: tuple[tuple[str, float, float], ...]


@dataclass(frozen=True, slots=True)
class _Replay:
    accuracy: float
    class_separation: float
    prediction_loss: float
    prediction_error_count: int
    event_count: int
    activation_count: int
    energy: float
    utility: float
    active_edges: frozenset[tuple[str, str]]
    path_lengths: tuple[int, ...]
    path_delays: tuple[float, ...]
    target_states: tuple[tuple[str, float], ...]
    trace: tuple[tuple[object, ...], ...]
    digest: str


def _examples() -> tuple[_Example, ...]:
    return (
        _Example("a-first", "a-first", (("a", 0.0, 1.0), ("b", 0.5, -1.0))),
        _Example("b-first", "b-first", (("b", 0.0, -1.0), ("a", 0.5, 1.0))),
    )


def _candidate_pool(config: TemporalEfficacyConfig) -> tuple[CandidateEvidence, ...]:
    destinations = ("d1", "d2", TARGET_NODE)
    return tuple(
        CandidateEvidence(source, source, destination, 1.0, config.propagation_delay,
                          f"baseline-{source}-{destination}")
        for source in SOURCE_NODES
        for destination in destinations
    )


def _temporal_candidates(config: TemporalEfficacyConfig, *, reversed_order: bool = False) -> tuple[CandidateEvidence, ...]:
    policy = TemporalAssociationPolicy(
        NODES,
        history_capacity=config.history_capacity,
        candidate_capacity=config.candidate_capacity,
        maximum_score=config.maximum_score,
        propagation_delay=config.propagation_delay,
        local_neighbors={"a": (TARGET_NODE,), "b": (TARGET_NODE,)},
    )
    for source in SOURCE_NODES:
        observations = ((source, TARGET_NODE, 0.0), (source, source, 1.0)) if reversed_order else (
            (source, source, 0.0), (source, TARGET_NODE, 1.0)
        )
        for observer, node, timestamp in observations:
            policy.observe(observer, node, timestamp)
    return policy.candidates


def _controller(config: TemporalEfficacyConfig) -> StructuralPlasticityController:
    topology = BoundedTopology(
        NODES,
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        edge_capacity=config.edge_capacity,
    )
    local_neighbors = {
        source: tuple(destination for destination in NODES if destination != source)
        for source in SOURCE_NODES
    }
    return StructuralPlasticityController(
        topology,
        candidate_capacity=config.candidate_capacity,
        max_growth_per_adaptation=config.max_growth_attempts,
        local_neighbors=local_neighbors,
    )


def _grow(
    controller: StructuralPlasticityController,
    candidates: tuple[CandidateEvidence, ...],
    config: TemporalEfficacyConfig,
) -> tuple[tuple[str, ...], dict[str, int], int]:
    pending = list(candidates)
    statuses: list[str] = []
    rejection_reasons: dict[str, int] = {}
    duplicate_proposals = 0
    for _ in range(config.max_growth_attempts):
        selected = controller.select(pending)
        if selected is None:
            break
        pending.remove(selected)
        result = controller.grow(selected)
        statuses.append(result.status)
        if result.status == "duplicate":
            duplicate_proposals += 1
        if result.status != "grown":
            reason = result.reason or result.status
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
    return tuple(statuses), rejection_reasons, duplicate_proposals


def _replay(topology: BoundedTopology, config: TemporalEfficacyConfig) -> _Replay:
    neurons = {node: TPCNNeuron(node, decay_rate=0.5, input_gain=1.0) for node in NODES}
    target_states: list[tuple[str, float]] = []
    trace: list[tuple[object, ...]] = []
    active_edges: set[tuple[str, str]] = set()
    path_lengths: list[int] = []
    path_delays: list[float] = []
    prediction_loss = 0.0
    prediction_error_count = 0
    total_energy = 0.0
    correct = 0
    for example in _examples():
        for neuron in neurons.values():
            neuron.reset()
        meter = LocalEnergyModel("luna-12j-meter", max_counter=config.max_events)
        predictor = LocalPredictor("luna-12j-predictor", max_outstanding=1, error_destination="prediction-errors")
        queue: EventQueue[Event] = EventQueue(config.queue_capacity)
        paths: dict[int, tuple[str, ...]] = {}
        for source, timestamp, payload in example.inputs:
            queued = queue.push(Event(timestamp, source, source, "signal", payload))
            paths[queued.sequence] = (source,)
        target = neurons[TARGET_NODE]
        while queue and len(trace) < config.max_events * len(_examples()):
            pending = queue.peek()
            assert pending is not None
            event = queue.pop_ready(pending.timestamp)
            path = paths.pop(event.sequence)
            neuron = neurons[event.destination]
            activation = neuron.receive_event(event)
            meter.observe_event(event, cost=abs(activation))
            trace.append((example.example_id, event.timestamp, event.source, event.destination, event.payload))
            if event.destination in SOURCE_NODES and predictor.outstanding_count == 0:
                predictor.create_prediction("target", target.activation, timestamp=event.timestamp, expires_at=event.timestamp + 4.0)
            if event.destination == TARGET_NODE:
                resolution = predictor.process_observation(
                    Event(event.timestamp, TARGET_NODE, "predictor", "observation", Observation("target", target.activation)),
                    EventQueue(config.queue_capacity),
                )
                if resolution.error is not None:
                    prediction_loss += abs(resolution.error.error)
                    prediction_error_count += 1
                path_lengths.append(len(path) - 1)
                path_delays.append(event.timestamp - next(item[1] for item in example.inputs if item[0] == path[0]))
            if event.destination in topology.nodes and len(path) < len(NODES) and event.destination not in path[1:]:
                emitted = Event(event.timestamp, event.destination, event.destination, event.event_type, activation)
                for routed in topology.route(emitted, queue):
                    paths[routed.sequence] = path + (routed.destination,)
                    active_edges.add((routed.source, routed.destination))
        target_states.append((example.example_id, target.state))
        total_energy += meter.energy
        predicted = "a-first" if target.state < 0.0 else "b-first"
        correct += int(predicted == example.label)
    states = dict(target_states)
    separation = abs(states["a-first"] - states["b-first"])
    reward = float(correct)
    utility = RewardAdjustedUtility(energy_weight=1.0).evaluate(total_energy, reward).utility
    digest = hashlib.sha256(repr((tuple(trace), tuple(target_states), topology.edges)).encode()).hexdigest()
    return _Replay(
        correct / len(_examples()), separation, prediction_loss, prediction_error_count,
        len(trace), len(trace), total_energy, utility, frozenset(active_edges),
        tuple(path_lengths), tuple(path_delays), tuple(target_states), tuple(trace),
            digest,
    )


def run_temporal_efficacy(
    policy: PolicyName,
    *,
    seed: int = 0,
    config: TemporalEfficacyConfig | None = None,
    causal_intervention: bool = True,
) -> TemporalEfficacyResult:
    """Run one deterministic condition through the real bounded route."""
    if policy not in ("fixed", "baseline", "random", "temporal", "reversed"):
        raise ValueError("unknown policy")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    config = TemporalEfficacyConfig() if config is None else config
    controller = _controller(config)
    candidate_pool = _candidate_pool(config)
    if policy == "fixed":
        candidates = ()
    elif policy == "baseline":
        candidates = candidate_pool
    elif policy == "random":
        candidates = tuple(random.Random(seed).sample(candidate_pool, config.max_growth_attempts))
    else:
        candidates = _temporal_candidates(config, reversed_order=policy == "reversed")
    statuses, rejection_reasons, duplicate_proposals = _grow(controller, candidates, config)
    replay = _replay(controller.topology, config)
    topology = controller.topology
    fan_in = tuple((node, len(topology.incoming(node))) for node in topology.nodes)
    fan_out = tuple((node, len(topology.outgoing(node))) for node in topology.nodes)
    active_edges = len(replay.active_edges)
    path_delay = sum(replay.path_delays) / len(replay.path_delays) if replay.path_delays else 0.0
    path_length = sum(replay.path_lengths) / len(replay.path_lengths) if replay.path_lengths else 0.0
    shortest = min((edge.propagation_delay for edge in topology.incoming(TARGET_NODE)), default=None)
    motifs = sum(len(topology.incoming(node)) >= 2 for node in topology.nodes)
    metrics = TemporalEfficacyMetrics(
        policy, seed, replay.accuracy, replay.class_separation, replay.prediction_loss,
        replay.prediction_error_count, replay.event_count, replay.activation_count,
        replay.energy, "activity-cost-proxy", replay.utility, len(topology), topology.edge_capacity,
        statuses.count("grown"), 0, sum(rejection_reasons.values()), tuple(sorted(rejection_reasons.items())),
        len(candidates), len(candidates), len(candidate_pool), duplicate_proposals, fan_in, fan_out, motifs,
        active_edges, active_edges / max(1, len(topology)), path_length, path_delay, shortest,
        0.0 if shortest is None else max(0.0, config.propagation_delay - shortest),
        not rejection_reasons, tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in topology.edges),
        statuses, replay.target_states, replay.digest,
    )
    intervention = None
    if causal_intervention and policy == "temporal" and ("a", TARGET_NODE) in {(edge.source, edge.destination) for edge in topology.edges}:
        present_count = replay.event_count
        present_state = dict(replay.target_states)["a-first"]
        assert controller.prune("a", TARGET_NODE).status == "pruned"
        removed = _replay(controller.topology, config)
        removed_state = dict(removed.target_states)["a-first"]
        intervention = CausalIntervention(
            ("a", TARGET_NODE), present_count, removed.event_count,
            present_state, removed_state, present_count != removed.event_count or present_state != removed_state,
        )
    return TemporalEfficacyResult(metrics, intervention)


def run_temporal_efficacy_suite(
    *,
    seeds: tuple[int, ...] = (0, 1, 2, 3, 4),
    config: TemporalEfficacyConfig | None = None,
) -> tuple[TemporalEfficacyResult, ...]:
    """Run all declared conditions for every supplied seed without filtering."""
    results = []
    for seed in seeds:
        for policy in ("fixed", "baseline", "random", "temporal", "reversed"):
            results.append(run_temporal_efficacy(policy, seed=seed, config=config))
    return tuple(results)


__all__ = [
    "CausalIntervention", "PolicyName", "TemporalEfficacyConfig", "TemporalEfficacyMetrics",
    "TemporalEfficacyResult", "run_temporal_efficacy", "run_temporal_efficacy_suite",
]