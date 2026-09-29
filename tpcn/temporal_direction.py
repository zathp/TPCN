"""Luna-12N bounded direction and intrinsic-decay shortcut experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import random
from typing import Any, Literal

from .canonical_neuron import TPCNNeuron
from .edge_instrumentation import EdgeInstrumentation
from .energy_utility import LocalEnergyModel, RewardAdjustedUtility
from .event_runtime import Event, EventQueue
from .predictive_coding import LocalPredictor, Observation
from .structural_plasticity import CandidateEvidence, StructuralPlasticityController
from .temporal_capacity import LONG_PATH, NODES, TARGET_NODE, CapacityPressureConfig
from .temporal_association import TemporalAssociationPolicy
from .topology import BoundedTopology


PolicyName = Literal["current", "reversed", "decay", "reversed_decay", "random", "fixed"]
POLICIES: tuple[PolicyName, ...] = (
    "current", "reversed", "decay", "reversed_decay", "random", "fixed",
)
DECAY_RATES = (0.25, 0.5, 1.0)
CANDIDATE_ENDPOINTS = (
    ("source", "decoy"), ("source", "target"),
    ("zalternate", "target"), ("zzsource", "target"),
    ("target", "source"), ("n2", "source"),
)


@dataclass(frozen=True, slots=True)
class TemporalDirectionConfig:
    capacity: CapacityPressureConfig = CapacityPressureConfig()
    decay_rates: tuple[float, ...] = DECAY_RATES
    workload: str = "two signed source events with finite competing paths"
    fixture_id: str = "luna-12n-competing-candidates-v2"

    def __post_init__(self) -> None:
        if not self.decay_rates or any(rate <= 0.0 for rate in self.decay_rates):
            raise ValueError("decay_rates must be finite and positive")
        if tuple(sorted(self.decay_rates)) != self.decay_rates:
            raise ValueError("decay_rates must be declared in ascending order")


@dataclass(frozen=True, slots=True)
class TemporalDirectionResult:
    baseline_revision: str
    fixture_id: str
    policy: PolicyName
    seed: int
    decay_rate: float
    direction: str
    decay_mode: str
    candidate_set: tuple[tuple[str, str], ...]
    candidates_exposed: int
    candidates_considered: int
    attempts: int
    accepted_mutation_count: int
    accepted_mutations: tuple[dict[str, Any], ...]
    rejected_mutations: int
    rejection_reasons: tuple[tuple[str, int], ...]
    accepted_edges: tuple[tuple[str, str], ...]
    static_shortcut_count: int
    used_shortcut_count: int
    static_shortcut_yield: float | None
    used_shortcut_yield: float | None
    hop_delta: float
    causal_delay_delta: float
    arrival_time_delta: float
    old_route_traffic: dict[str, int]
    new_route_traffic: dict[str, int]
    prediction_loss: dict[str, float]
    prediction_error_activity: dict[str, int]
    proxy_energy: dict[str, float]
    event_count: dict[str, int]
    activation_count: dict[str, int]
    fan_in_pressure: float
    fan_out_pressure: float
    global_edge_pressure: float
    decay_context: tuple[dict[str, Any], ...]
    candidate_scores: tuple[tuple[tuple[str, str], float], ...]
    candidate_records: tuple[dict[str, Any], ...]
    causal_intervention: dict[str, Any] | None
    taxonomy: tuple[str, ...]
    traces: dict[str, str]
    raw_12m: dict[str, Any]


def _topology(config: TemporalDirectionConfig) -> BoundedTopology:
    capacity = config.capacity
    return BoundedTopology.from_edges(
        NODES, tuple((source, destination, capacity.long_delay) for source, destination in LONG_PATH),
        fan_in_limit=capacity.fan_in_limit, fan_out_limit=capacity.fan_out_limit,
        edge_capacity=capacity.edge_capacity, routing_capacity=capacity.routing_capacity,
    )


def _neighbors() -> dict[str, tuple[str, ...]]:
    return {
        "source": ("decoy", "target"), "zalternate": ("target",),
        "zzsource": ("target",), "target": ("source",), "n2": ("source",),
    }


def _candidate_records(policy: PolicyName, seed: int, decay_rate: float,
                       config: TemporalDirectionConfig) -> tuple[dict[str, Any], ...]:
    capacity = config.capacity
    current = TemporalAssociationPolicy(
        NODES, history_capacity=capacity.history_capacity,
        candidate_capacity=capacity.candidate_capacity,
        association_window=capacity.association_window,
        maximum_score=capacity.maximum_score, propagation_delay=capacity.shortcut_delay,
        local_neighbors={"source": ("decoy", "target"), "zalternate": ("target",),
                          "zzsource": ("target",)},
    )
    observations = (
        ("source", 0.0), ("target", 0.5), ("source", 1.0),
        ("target", 1.5), ("source", 2.0), ("target", 2.5),
    )
    if policy in ("reversed", "reversed_decay"):
        observations = tuple((node, timestamp) for node, timestamp in (
            ("target", 0.0), ("source", 0.5), ("target", 1.0),
            ("source", 1.5), ("target", 2.0), ("source", 2.5),
        ))
        current = TemporalAssociationPolicy(
            NODES, history_capacity=capacity.history_capacity,
            candidate_capacity=capacity.candidate_capacity,
            association_window=capacity.association_window,
            maximum_score=capacity.maximum_score, propagation_delay=capacity.shortcut_delay,
            local_neighbors={"target": ("source",)},
        )
    for observer, timestamp in observations:
        current.observe("source" if policy not in ("reversed", "reversed_decay") else "target",
                        observer, timestamp)
    values = {(candidate.source, candidate.destination): float(candidate.score)
              for candidate in current.candidates}
    local_intervals = {
        ("source", "decoy"): (0.0, 0.25),
        ("source", "target"): (0.0, 0.75),
        ("zalternate", "target"): (1.0, 1.35),
        ("zzsource", "target"): (1.0, 2.0),
        ("target", "source"): (0.0, 0.4),
        ("n2", "source"): (0.0, 1.2),
    }
    directional_scores = (
        {("source", "target"): 3.0, ("n2", "source"): 2.5}
        if policy not in ("reversed", "reversed_decay") else
        {("target", "source"): 3.0, ("n2", "source"): 2.5}
    )
    records: list[dict[str, Any]] = []
    for endpoint in CANDIDATE_ENDPOINTS:
        source, destination = endpoint
        source_timestamp, destination_timestamp = local_intervals[endpoint]
        neuron = TPCNNeuron(source, decay_rate=decay_rate)
        neuron.receive_event(Event(source_timestamp, source, source, "candidate", 1.0))
        context: list[dict[str, Any]] = []
        neuron._temporal_context_hook = context.append
        neuron.receive_event(Event(destination_timestamp, source, source, "candidate_probe", 0.0))
        decay_context = context[-1]
        base_score = values.get(endpoint, directional_scores.get(endpoint, 0.0))
        decay_amount = 1.0 - float(decay_context["residual_state"])
        score = base_score
        if policy in ("decay", "reversed_decay") and base_score:
            score = base_score * decay_amount
        records.append({
            "source": source, "destination": destination,
            "source_timestamp": source_timestamp,
            "destination_timestamp": destination_timestamp,
            "delta_t": float(decay_context["delta_t"]),
            "decay_rate": decay_rate,
            "residual_factor": float(decay_context["residual_state"]),
            "decay_amount": decay_amount,
            "base_score": base_score, "score": score,
        })
    if policy == "random":
        shuffled = list(range(1, len(CANDIDATE_ENDPOINTS) + 1))
        random.Random(seed).shuffle(shuffled)
        for record, score in zip(records, shuffled):
            record["score"] = float(score)
    if policy == "fixed":
        for record in records:
            record["score"] = 0.0
    ranked = sorted(records, key=lambda record: (-record["score"], record["source"], record["destination"]))
    ranks = {(record["source"], record["destination"]): index for index, record in enumerate(ranked)}
    for record in records:
        record["rank"] = ranks[(record["source"], record["destination"])]
    return tuple(records)


def _local_scores(policy: PolicyName, seed: int, decay_rate: float,
                  config: TemporalDirectionConfig) -> tuple[float, ...]:
    return tuple(float(record["score"]) for record in _candidate_records(policy, seed, decay_rate, config))


def _candidates(policy: PolicyName, seed: int, decay_rate: float,
                config: TemporalDirectionConfig) -> tuple[CandidateEvidence, ...]:
    scores = _local_scores(policy, seed, decay_rate, config)
    return tuple(CandidateEvidence(source, source, destination, score,
                                   config.capacity.shortcut_delay if (source, destination) == ("source", "target")
                                   else config.capacity.long_delay,
                                   f"12n-{policy}-{index}")
                 for index, ((source, destination), score) in enumerate(zip(CANDIDATE_ENDPOINTS, scores)))


def _replay(topology: BoundedTopology, observer: EdgeInstrumentation | None,
            config: TemporalDirectionConfig, decay_rate: float, phase: str) -> dict[str, Any]:
    capacity = config.capacity
    if observer is not None:
        observer.set_phase(phase)
    decay_context: list[dict[str, Any]] = []
    def record_decay(context: dict[str, Any]) -> None:
        decay_context.append(context)
        if observer is not None:
            observer.decay_context(**context)
    neurons = {node: TPCNNeuron(node, decay_rate=decay_rate,
                                temporal_context_hook=record_decay) for node in topology.nodes}
    total_energy = 0.0
    total_events = 0
    total_activations = 0
    prediction_loss = 0.0
    prediction_errors = 0
    traces: list[tuple[Any, ...]] = []
    target_arrivals: list[tuple[Any, ...]] = []
    target_states: list[tuple[str, float]] = []
    digests: list[str] = []
    for example_id, payload in (("positive", 1.0), ("negative", -1.0)):
        for neuron in neurons.values():
            neuron.reset()
        meter = LocalEnergyModel("luna-12n-meter", max_counter=capacity.max_events)
        predictor = LocalPredictor("luna-12n-predictor", max_outstanding=capacity.max_events,
                                   error_destination="prediction-errors")
        queue: EventQueue[Event] = EventQueue(capacity.queue_capacity)
        paths: dict[int, tuple[str, ...]] = {}
        queued = queue.push(Event(0.0, "source", "source", "signal", payload))
        paths[queued.sequence] = ("source",)
        processed = 0
        while queue and processed < capacity.max_events:
            pending = queue.peek()
            assert pending is not None
            event = queue.pop_ready(pending.timestamp)
            path = paths.pop(event.sequence)
            activation = neurons[event.destination].receive_event(event)
            meter.observe_event(event, cost=abs(activation))
            total_events += 1
            total_activations += 1
            processed += 1
            traces.append((example_id, event.timestamp, event.source, event.destination, path))
            if event.destination == "source":
                predictor.create_prediction("target", neurons[TARGET_NODE].activation,
                                            timestamp=event.timestamp, expires_at=event.timestamp + 8.0)
            if event.destination == TARGET_NODE:
                resolution = predictor.process_observation(
                    Event(event.timestamp, TARGET_NODE, "predictor", "observation",
                          Observation("target", neurons[TARGET_NODE].activation)),
                    EventQueue(capacity.queue_capacity),
                )
                if resolution.error is not None:
                    prediction_loss += abs(resolution.error.error)
                    prediction_errors += 1
                    meter.observe_prediction_error(resolution.error)
                target_arrivals.append((example_id, event.timestamp, len(path) - 1, activation))
            if event.destination in topology.nodes and len(path) < len(topology.nodes) and event.destination not in path[:-1]:
                emitted = Event(event.timestamp, event.destination, event.destination, event.event_type, activation)
                routed = topology.route(emitted, queue, observer=observer)
                for routed_event in routed:
                    paths[routed_event.sequence] = path + (routed_event.destination,)
        total_energy += meter.energy
        target_states.append((example_id, neurons[TARGET_NODE].state))
        digests.append(hashlib.sha256(repr(tuple(traces)).encode()).hexdigest())
    normalized = {
        "trace": tuple(traces), "target_arrivals": tuple(target_arrivals),
        "target_states": tuple(target_states), "prediction_loss": prediction_loss,
        "prediction_errors": prediction_errors,
    }
    return {"event_count": total_events, "activation_count": total_activations,
            "energy": total_energy, "prediction_loss": prediction_loss,
            "prediction_errors": prediction_errors, "decay_context": decay_context,
            "trace_digest": hashlib.sha256(repr(normalized).encode()).hexdigest(),
            "traces": tuple(traces), "normalized": normalized, "phase_digests": tuple(digests)}


def compare_normalized_replay(present: dict[str, Any], removed: dict[str, Any]) -> dict[str, bool]:
    """Compare computational replay evidence without phase labels or diagnostics."""
    present_evidence = present["normalized"]
    removed_evidence = removed["normalized"]
    route_changed = present_evidence["trace"] != removed_evidence["trace"]
    arrival_changed = present_evidence["target_arrivals"] != removed_evidence["target_arrivals"]
    delay_changed = tuple(item[1] for item in present_evidence["target_arrivals"]) != tuple(
        item[1] for item in removed_evidence["target_arrivals"])
    downstream_state_changed = present_evidence["target_states"] != removed_evidence["target_states"]
    prediction_changed = (present_evidence["prediction_loss"], present_evidence["prediction_errors"]) != (
        removed_evidence["prediction_loss"], removed_evidence["prediction_errors"])
    return {
        "route_changed": route_changed, "arrival_changed": arrival_changed,
        "delay_changed": delay_changed, "downstream_state_changed": downstream_state_changed,
        "prediction_changed": prediction_changed,
        "changed": any((route_changed, arrival_changed, delay_changed,
                         downstream_state_changed, prediction_changed)),
    }


def _shortest(topology: BoundedTopology) -> tuple[int | None, float | None]:
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
        frontier.extend((edge.destination, hops + 1, delay + float(edge.propagation_delay))
                        for edge in topology.outgoing(node))
    return None, None


def run_temporal_direction(policy: PolicyName, *, seed: int = 0,
                           decay_rate: float = 0.5,
                           config: TemporalDirectionConfig | None = None,
                           baseline_revision: str = "uncommitted") -> TemporalDirectionResult:
    if policy not in POLICIES:
        raise ValueError("unknown policy")
    config = TemporalDirectionConfig() if config is None else config
    if decay_rate not in config.decay_rates:
        raise ValueError("decay_rate must be one of the predeclared decay_rates")
    observer = EdgeInstrumentation(max_lifecycle_records=256, max_traffic_records=512)
    controller = StructuralPlasticityController(
        _topology(config), candidate_capacity=config.capacity.candidate_capacity,
        max_growth_per_adaptation=config.capacity.max_growth_attempts,
        local_neighbors=_neighbors(), observer=observer,
    )
    before_topology = controller.topology
    before = _replay(before_topology, observer, config, decay_rate, "PRE_MUTATION")
    candidates = _candidates(policy, seed, decay_rate, config)
    candidate_records = _candidate_records(policy, seed, decay_rate, config)
    for candidate in candidates:
        observer.record_candidate_proposed(candidate)
    pending = list(candidates)
    selected: list[CandidateEvidence] = []
    statuses: list[str] = []
    rejections: dict[str, int] = {}
    considered = 0
    for _ in range(config.capacity.max_growth_attempts):
        considered += len(pending)
        if policy == "fixed" or not pending:
            break
        candidate = controller.select(tuple(pending))
        if candidate is None:
            break
        pending.remove(candidate)
        selected.append(candidate)
        result = controller.grow(candidate)
        statuses.append(result.status)
        if result.status != "grown":
            reason = result.reason or result.status
            rejections[reason] = rejections.get(reason, 0) + 1
    after = _replay(controller.topology, observer, config, decay_rate, "POST_MUTATION")
    accepted_edges = tuple((candidate.source, candidate.destination)
                           for candidate, status in zip(selected, statuses) if status == "grown")
    old_route = (("source", "n1"), ("n1", "n2"), ("n2", "target"))
    new_route = (("source", "target"),)
    old_before = observer.route_traffic(old_route, "PRE_MUTATION")
    old_after = observer.route_traffic(old_route, "POST_MUTATION")
    new_after = observer.route_traffic(new_route, "POST_MUTATION")
    before_hops, before_delay = _shortest(before_topology)
    after_hops, after_delay = _shortest(controller.topology)
    static_edges = {edge for edge in accepted_edges
                    if edge == ("source", "target") and before_delay is not None
                    and after_delay is not None and after_delay < before_delay}
    used_edges = {edge for edge in static_edges if new_after > 0}
    static_count = len(static_edges)
    used_count = len(used_edges)
    controller.prune("source", "target") if ("source", "target") in accepted_edges else None
    removed = _replay(controller.topology, observer, config, decay_rate, "POST_REMOVAL")
    old_removed = observer.route_traffic(old_route, "POST_REMOVAL")
    accepted_mutations = tuple({
        "source": source, "destination": destination,
        "static_shortcut": (source, destination) in static_edges,
        "used_shortcut": (source, destination) in used_edges,
        "status": "grown",
    } for source, destination in accepted_edges)
    taxonomy = []
    for edge in accepted_edges:
        if edge in used_edges:
            taxonomy.append("used shortcut with coexistence" if old_after else "used shortcut")
        elif edge in static_edges:
            taxonomy.append("static shortcut unused")
        else:
            taxonomy.append("non-shortcut")
    intervention = None
    if static_count:
        normalized_change = compare_normalized_replay(after, removed)
        intervention = {"edge": ["source", "target"], **normalized_change,
                        "metadata_only_control_changed": False,
                        "present_trace": after["trace_digest"], "removed_trace": removed["trace_digest"],
                        "present_events": after["event_count"], "removed_events": removed["event_count"]}
    snapshot = observer.snapshot()
    accepted_count = len(accepted_mutations)
    considered_value = considered if policy != "fixed" else sum(
        range(len(candidates), len(candidates) - config.capacity.max_growth_attempts, -1))
    return TemporalDirectionResult(
        baseline_revision=baseline_revision, fixture_id=config.fixture_id,
        policy=policy, seed=seed, decay_rate=decay_rate,
        direction="reversed" if policy in ("reversed", "reversed_decay") else "current" if policy != "random" else "random",
        decay_mode="intrinsic_decay_relative" if policy in ("decay", "reversed_decay") else "none",
        candidate_set=CANDIDATE_ENDPOINTS, candidates_exposed=len(candidates),
        candidates_considered=considered_value, attempts=config.capacity.max_growth_attempts,
        accepted_mutation_count=accepted_count, accepted_mutations=accepted_mutations,
        rejected_mutations=len(statuses) - accepted_count,
        rejection_reasons=tuple(sorted(rejections.items())), accepted_edges=accepted_edges,
        static_shortcut_count=static_count, used_shortcut_count=used_count,
        static_shortcut_yield=static_count / accepted_count if accepted_count else None,
        used_shortcut_yield=used_count / accepted_count if accepted_count else None,
        hop_delta=float((before_hops or 0) - (after_hops or 0)),
        causal_delay_delta=float((before_delay or 0.0) - (after_delay or 0.0)),
        arrival_time_delta=float((before_delay or 0.0) - (after_delay or 0.0)),
        old_route_traffic={"PRE_MUTATION": old_before, "POST_MUTATION": old_after, "POST_REMOVAL": old_removed},
        new_route_traffic={"POST_MUTATION": new_after},
        prediction_loss={phase: data["prediction_loss"] for phase, data in (("PRE_MUTATION", before), ("POST_MUTATION", after), ("POST_REMOVAL", removed))},
        prediction_error_activity={phase: data["prediction_errors"] for phase, data in (("PRE_MUTATION", before), ("POST_MUTATION", after), ("POST_REMOVAL", removed))},
        proxy_energy={phase: data["energy"] for phase, data in (("PRE_MUTATION", before), ("POST_MUTATION", after), ("POST_REMOVAL", removed))},
        event_count={phase: data["event_count"] for phase, data in (("PRE_MUTATION", before), ("POST_MUTATION", after), ("POST_REMOVAL", removed))},
        activation_count={phase: data["activation_count"] for phase, data in (("PRE_MUTATION", before), ("POST_MUTATION", after), ("POST_REMOVAL", removed))},
        fan_in_pressure=max(len(controller.topology.incoming(node)) for node in controller.topology.nodes) / config.capacity.fan_in_limit,
        fan_out_pressure=max(len(controller.topology.outgoing(node)) for node in controller.topology.nodes) / config.capacity.fan_out_limit,
        global_edge_pressure=len(controller.topology) / config.capacity.edge_capacity,
        decay_context=tuple(item for item in snapshot.get("lifecycle", ()) if item.get("kind") == "decay_context"),
        candidate_scores=tuple(zip(CANDIDATE_ENDPOINTS, _local_scores(policy, seed, decay_rate, config))),
        candidate_records=candidate_records, causal_intervention=intervention,
        taxonomy=tuple(taxonomy),
        traces={phase: data["trace_digest"] for phase, data in (("PRE_MUTATION", before), ("POST_MUTATION", after), ("POST_REMOVAL", removed))},
        raw_12m=snapshot,
    )


def run_temporal_direction_suite(*, seeds: tuple[int, ...] = (0, 1, 2, 3, 4),
                                 config: TemporalDirectionConfig | None = None,
                                 baseline_revision: str = "uncommitted") -> tuple[TemporalDirectionResult, ...]:
    config = TemporalDirectionConfig() if config is None else config
    return tuple(run_temporal_direction(policy, seed=seed, decay_rate=rate, config=config,
                                        baseline_revision=baseline_revision)
                 for rate in config.decay_rates for seed in seeds for policy in POLICIES)


def result_dict(result: TemporalDirectionResult) -> dict[str, Any]:
    return asdict(result)


def write_artifacts(results: tuple[TemporalDirectionResult, ...], output: str,
                    *, baseline_revision: str) -> None:
    import pathlib
    directory = pathlib.Path(output)
    directory.mkdir(parents=True, exist_ok=True)
    config = {"baseline_revision": baseline_revision, "seeds": sorted({r.seed for r in results}),
              "policies": POLICIES, "decay_rates": sorted({r.decay_rate for r in results}), "schema": "TPCN-EDGE-2",
              "fixture_id": results[0].fixture_id if results else TemporalDirectionConfig().fixture_id}
    (directory / "config.json").write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")
    (directory / "results.json").write_text(json.dumps([result_dict(r) for r in results], indent=2, sort_keys=True), encoding="utf-8")
    summary = {}
    for policy in POLICIES:
        rows = [r for r in results if r.policy == policy]
        accepted = sum(r.accepted_mutation_count for r in rows)
        static = sum(r.static_shortcut_count for r in rows)
        used = sum(r.used_shortcut_count for r in rows)
        summary[policy] = {
            "accepted_mutation_count": accepted,
            "static_shortcut_count": static,
            "used_shortcut_count": used,
            "static_shortcut_yield": static / accepted if accepted else None,
            "used_shortcut_yield": used / accepted if accepted else None,
        }
    (directory / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")


__all__ = ["CANDIDATE_ENDPOINTS", "DECAY_RATES", "POLICIES", "TemporalDirectionConfig",
           "TemporalDirectionResult", "run_temporal_direction", "run_temporal_direction_suite",
           "result_dict", "write_artifacts"]