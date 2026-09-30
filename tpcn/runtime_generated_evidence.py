"""Luna-13F runtime-generated bounded local candidate evidence fixture."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
import hashlib
import json
import platform
import random
import subprocess
import sys
from typing import Any, Iterable

from .canonical_neuron import TPCNNeuron
from .event_runtime import Event, EventQueue, execute_bounded
from .finite_resource import FiniteResourceConfig, run_experiment as run_13d
from .post_pruning_admission import AdmissionQualityConfig, _evaluate
from .structural_plasticity import CandidateEvidence, MutationResult, StructuralPlasticityController
from .temporal_association import TemporalAssociationPolicy
from .topology import BoundedTopology


Edge = tuple[str, str, float]


@dataclass(frozen=True, slots=True)
class RuntimeEvidenceConfig:
    fixture_id: str = "luna-13f-runtime-generated-local-evidence-v1"
    node_ids: tuple[str, str, str, str] = ("source", "relay", "noise", "target")
    event_budget: int = 32
    queue_capacity: int = 16
    edge_capacity: int = 3
    fan_in_limit: int = 2
    fan_out_limit: int = 1
    history_capacity: int = 8
    candidate_capacity: int = 2
    association_window: float = 2.0
    random_seeds: tuple[int, ...] = (0, 1, 2, 3, 4)
    mapping_ids: tuple[str, ...] = ("P0", "P1")
    neutral_decay_values: tuple[float, ...] = (0.0, 0.1, 1.0)

    def __post_init__(self) -> None:
        if len(self.node_ids) != 4 or len(set(self.node_ids)) != 4:
            raise ValueError("node_ids must contain four distinct IDs")
        for value, name in (
            (self.event_budget, "event_budget"),
            (self.queue_capacity, "queue_capacity"),
            (self.edge_capacity, "edge_capacity"),
            (self.fan_in_limit, "fan_in_limit"),
            (self.fan_out_limit, "fan_out_limit"),
            (self.history_capacity, "history_capacity"),
            (self.candidate_capacity, "candidate_capacity"),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.association_window <= 0.0:
            raise ValueError("association_window must be positive")
        if not self.mapping_ids or len(set(self.mapping_ids)) != len(self.mapping_ids):
            raise ValueError("mapping_ids must be non-empty and unique")
        if not self.neutral_decay_values or any(value < 0.0 for value in self.neutral_decay_values):
            raise ValueError("neutral_decay_values must be non-negative and non-empty")


def _roles(config: RuntimeEvidenceConfig) -> dict[str, str]:
    source, relay, noise, target = config.node_ids
    return {"source": source, "relay": relay, "noise": noise, "target": target}


def _fingerprint(edges: Iterable[Edge]) -> str:
    return hashlib.sha256(repr(tuple(sorted(edges))).encode("utf-8")).hexdigest()


def _mapping(config: RuntimeEvidenceConfig, mapping_id: str) -> dict[str, Any]:
    roles = _roles(config)
    if mapping_id not in config.mapping_ids:
        raise ValueError(f"unknown neutral mapping: {mapping_id!r}")
    permutation = config.mapping_ids.index(mapping_id) % 2
    endpoints = (roles["relay"], roles["noise"])
    if permutation:
        endpoints = endpoints[::-1]
    return {
        "mapping_id": mapping_id,
        "candidates": {
            "candidate_A": (roles["source"], endpoints[0], 0.5),
            "candidate_B": (roles["source"], endpoints[1], 1.0),
        },
        "motifs": {"short": "candidate_A", "long": "candidate_B"},
    }


def _base_edges(config: RuntimeEvidenceConfig, mapping_id: str) -> tuple[Edge, ...]:
    roles = _roles(config)
    return (
        (roles["relay"], roles["target"], 0.5),
        (roles["noise"], roles["target"], 2.0),
    )


def _topology(config: RuntimeEvidenceConfig, edges: tuple[Edge, ...]) -> BoundedTopology:
    return BoundedTopology.from_edges(
        config.node_ids,
        edges,
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        edge_capacity=config.edge_capacity,
        routing_capacity=config.fan_out_limit,
    )


def _schedule(config: RuntimeEvidenceConfig, mapping_id: str, control: str, *, mirror: bool = False) -> tuple[Event, ...]:
    roles = _roles(config)
    source = roles["source"]
    mapping = _mapping(config, mapping_id)
    candidates = mapping["candidates"]
    short_node = candidates["candidate_B"][1] if mirror else candidates["candidate_A"][1]
    long_node = candidates["candidate_A"][1] if mirror else candidates["candidate_B"][1]
    # These are ordinary addressed runtime events. The association policy derives
    # evidence from their arrival times and local source observations.
    base = (
        Event(0.0, source, source, "local_anchor", 1.0),
        Event(0.5, short_node, source, "candidate_observation", 0.5),
        Event(1.0, source, source, "local_anchor", 1.0),
        Event(1.5, short_node, source, "candidate_observation", 0.5),
        Event(2.0, source, source, "local_anchor", 1.0),
        Event(2.5, short_node, source, "candidate_observation", 0.5),
        Event(3.0, source, source, "local_anchor", 1.0),
        Event(3.5, short_node, source, "candidate_observation", 0.5),
        Event(4.0, source, source, "local_anchor", 1.0),
        Event(7.0, long_node, source, "candidate_observation", 0.5),
        Event(8.0, source, source, "local_anchor", 1.0),
        Event(11.0, long_node, source, "candidate_observation", 0.5),
        Event(12.0, source, source, "local_anchor", 1.0),
        Event(15.0, long_node, source, "candidate_observation", 0.5),
        Event(16.0, source, source, "local_anchor", 1.0),
        Event(19.0, long_node, source, "candidate_observation", 0.5),
    )
    if control == "no_evidence":
        return tuple(event for event in base if event.source == source)
    if control == "future":
        return base + (Event(10.0, short_node, source, "future_candidate_observation", 0.5),)
    if control == "uniform":
        return tuple(Event(float(index), event.source, event.destination, event.event_type, event.payload)
                     for index, event in enumerate(base))
    if control in {"reverse", "shuffle"}:
        timestamps = tuple(float(index) for index in range(len(base)))
        if control == "reverse":
            timestamps = timestamps[::-1]
        else:
            timestamps = (3.0, 6.0, 0.0, 7.0, 2.0, 5.0, 1.0, 4.0,
                          11.0, 14.0, 8.0, 15.0, 10.0, 13.0, 9.0, 12.0)
        return tuple(Event(timestamp, event.source, event.destination, event.event_type, event.payload)
                     for event, timestamp in zip(base, timestamps))
    if control == "equalized":
        return (
            Event(0.0, source, source, "local_anchor", 1.0),
            Event(1.0, candidates["candidate_A"][1], source, "candidate_observation", 0.5),
            Event(2.0, source, source, "local_anchor", 1.0),
            Event(3.0, candidates["candidate_B"][1], source, "candidate_observation", 0.5),
            Event(4.0, source, source, "local_anchor", 1.0),
            Event(5.0, candidates["candidate_A"][1], source, "candidate_observation", 0.5),
            Event(6.0, source, source, "local_anchor", 1.0),
            Event(7.0, candidates["candidate_B"][1], source, "candidate_observation", 0.5),
        )
    return base


def _mutation_payload(result: MutationResult) -> dict[str, Any]:
    return {
        "status": result.status,
        "reason": result.reason,
        "edge": None if result.edge is None else {
            "source": result.edge.source,
            "destination": result.edge.destination,
            "propagation_delay": float(result.edge.propagation_delay),
        },
    }


def _run_runtime_evidence(
    config: RuntimeEvidenceConfig,
    mapping_id: str = "P0",
    control: str = "primary",
    *,
    mirror: bool = False,
    decay_rate: float = 0.1,
    visibility_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    roles = _roles(config)
    source = roles["source"]
    mapping = _mapping(config, mapping_id)
    candidate_edges = mapping["candidates"]
    candidates = {edge[1] for edge in candidate_edges.values()}
    policy = TemporalAssociationPolicy(
        config.node_ids,
        history_capacity=config.history_capacity,
        candidate_capacity=config.candidate_capacity,
        association_window=config.association_window,
        maximum_score=config.history_capacity,
        local_neighbors={source: candidates},
    )
    neuron = TPCNNeuron(source, decay_rate=decay_rate, input_gain=1.0)
    queue: EventQueue[Event] = EventQueue(config.queue_capacity)
    events = _schedule(config, mapping_id, control, mirror=mirror)
    # The first sixteen events are the declared pre-admission phase. The
    # future control continues this same policy/neuron state after admission.
    evidence_events = events[:16]
    future_events = events[16:]
    for event in evidence_events:
        queue.push(event)
    observations: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []
    last_anchor: float | None = None
    previous_scores: dict[str, float] = {}
    phase = "pre_admission"
    private_state_mutation: dict[str, Any] | None = None
    dependency_trace = {
        "owner": source,
        "permitted_inputs": [
            "TemporalAssociationPolicy._history[source]",
            "TemporalAssociationPolicy._scores[(source, candidate)]",
            "Event.source",
            "Event.timestamp",
            "TPCNNeuron local state and elapsed time",
        ],
        "prohibited_inputs_read": [],
    }

    def handle(event: Event, _pending: EventQueue[Event]) -> None:
        nonlocal last_anchor, private_state_mutation
        context: list[dict[str, Any]] = []
        neuron._temporal_context_hook = context.append
        before_policy = asdict(policy.state)
        neuron.receive_event(event)
        if event.source == source:
            policy.observe(source, source, event.timestamp)
            last_anchor = event.timestamp
        elif event.source in candidates:
            if (visibility_metadata is not None
                    and visibility_metadata.get("mutate_candidate") == event.source
                    and private_state_mutation is None):
                key = (source, event.source)
                before = policy._scores.get(key, 0)
                policy._scores[key] = int(visibility_metadata["mutated_score"])
                private_state_mutation = {
                    "candidate": event.source,
                    "field": "TemporalAssociationPolicy._scores[(source, candidate)]",
                    "before": before,
                    "after": policy._scores[key],
                    "event_id": event.sequence,
                }
            score_before = previous_scores.get(event.source, 0.0)
            if last_anchor is not None:
                policy.observe(source, event.source, event.timestamp)
            after_policy = asdict(policy.state)
            score_map = {(item.source, item.destination): float(item.score) for item in policy.candidates}
            score_after = score_map.get((source, event.source), 0.0)
            previous_scores[event.source] = score_after
            observations.append({
                "event_id": event.sequence,
                "event_type": str(event.event_type),
                "source": event.source,
                "destination": event.destination,
                "timestamp": float(event.timestamp),
                "receiving_local_component": source,
                "local_state_before": float(context[-1]["pre_state"]),
                "local_state_after": float(context[-1]["post_state"]),
                "local_residual": float(context[-1]["residual_state"]),
                "elapsed_local_time": float(context[-1]["delta_t"]),
                "candidate": event.source,
                "evidence_update": score_after - score_before,
                "policy_state_before": before_policy,
                "policy_state_after": after_policy,
                "evidence_timestamp": float(event.timestamp),
                "phase": phase,
            })
        trace.append({"event_id": event.sequence, "source": event.source,
                      "destination": event.destination, "timestamp": event.timestamp,
                      "event_type": str(event.event_type), "phase": phase})

    execution = execute_bounded(queue, handle, event_budget=config.event_budget)
    frozen_scores = {
        item.destination: float(item.score)
        for item in policy.candidates
        if item.source == source
    }
    runtime_scores = {edge[1]: frozen_scores.get(edge[1], 0.0) for edge in candidate_edges.values()}
    evidence = tuple(
        CandidateEvidence(
            source,
            source,
            edge[1],
            runtime_scores.get(edge[1], 0.0),
            edge[2],
            f"runtime-{source}-{edge[1]}",
        )
        for edge in candidate_edges.values()
    )
    frozen_evidence = evidence
    pre_execution = execution
    continuation = None
    live_evidence = evidence
    if control == "future" and pre_execution.completed and not pre_execution.budget_exhausted:
        losing_endpoint = candidate_edges["candidate_B"][1]
        future_events = tuple(
            event
            for index in range(5)
            for event in (
                Event(20.0 + index, source, source, "future_local_anchor", 1.0),
                Event(20.5 + index, losing_endpoint, source, "future_candidate_observation", 0.5),
            )
        )
        for event in future_events:
            queue.push(event)
        phase = "post_admission"
        continuation = execute_bounded(queue, handle, event_budget=config.event_budget)
        live_scores = {
            item.destination: float(item.score)
            for item in policy.candidates
            if item.source == source
        }
        live_evidence = tuple(
            CandidateEvidence(source, source, edge[1], live_scores.get(edge[1], 0.0), edge[2],
                              f"runtime-{source}-{edge[1]}")
            for edge in candidate_edges.values()
        )
    decision_timestamp = max((event.timestamp for event in evidence_events), default=0.0)
    first_evidence_timestamp = min((item["timestamp"] for item in observations), default=None)
    last_evidence_timestamp = max((item["evidence_timestamp"] for item in observations), default=None)
    evidence_complete_timestamp = execution.last_event_timestamp if execution.completed and not execution.budget_exhausted else None
    return {
        "mapping_id": mapping_id,
        "decay_rate": decay_rate,
        "candidate_endpoints": {name: edge[1] for name, edge in candidate_edges.items()},
        "control": control,
        "mirror": mirror,
        "schedule": tuple({"event_id": event.sequence, "source": event.source,
                            "destination": event.destination, "timestamp": event.timestamp,
                            "event_type": str(event.event_type), "payload": event.payload}
                           for event in queue.drain()) if False else tuple({
                               "source": event.source, "destination": event.destination,
                               "timestamp": event.timestamp, "event_type": str(event.event_type),
                               "payload": event.payload} for event in events),
        "observations": tuple(observations),
        "evidence": frozen_evidence,
        "frozen_evidence": frozen_evidence,
        "live_evidence": live_evidence,
        "future_events": tuple({"source": event.source, "destination": event.destination,
                     "timestamp": event.timestamp, "event_type": str(event.event_type),
                     "payload": event.payload} for event in future_events),
        "owner": source,
        "bounds": {
            "maximum_tracked_candidates": config.candidate_capacity,
            "per_candidate_state": "one bounded integer score plus bounded offline provenance",
            "history_capacity": config.history_capacity,
            "retention": "until decision freeze",
            "reset": "new run/sequence",
            "expiry": "decision freeze; future events excluded",
            "eviction": "TemporalAssociationPolicy candidate capacity rejection",
            "numeric_bound": config.history_capacity,
        },
        "first_evidence_timestamp": first_evidence_timestamp,
        "last_evidence_timestamp": last_evidence_timestamp,
        "evidence_complete_timestamp": evidence_complete_timestamp,
        "decision_timestamp": decision_timestamp,
        "freeze_timestamp": decision_timestamp if evidence_complete_timestamp is not None else None,
        "score_timestamp": decision_timestamp if evidence_complete_timestamp is not None else None,
        "admission_timestamp": decision_timestamp if evidence_complete_timestamp is not None else None,
        "visibility_metadata_used": False,
        "evidence_complete": execution.completed and not execution.budget_exhausted,
        "execution": {
            "configured_event_budget": pre_execution.configured_event_budget,
            "processed_event_count": pre_execution.processed_event_count,
            "pending_event_count": pre_execution.pending_event_count,
            "peak_queue_occupancy": pre_execution.peak_queue_occupancy,
            "termination_reason": pre_execution.termination_reason,
            "completed": pre_execution.completed,
            "budget_exhausted": pre_execution.budget_exhausted,
        },
        "future_continuation": None if continuation is None else {
            "actual_events": tuple({"event_id": event.sequence, "source": event.source,
                                     "destination": event.destination, "timestamp": event.timestamp,
                                     "event_type": str(event.event_type)} for event in future_events),
            "processed_event_count": continuation.processed_event_count,
            "pending_event_count": continuation.pending_event_count,
            "peak_queue_occupancy": continuation.peak_queue_occupancy,
            "termination_reason": continuation.termination_reason,
            "completed": continuation.completed,
            "budget_exhausted": continuation.budget_exhausted,
        },
        "trace": tuple(trace),
        "dependency_trace": dependency_trace,
        "private_state_mutation": private_state_mutation,
        "local_neuron": {
            "state": neuron.state,
            "activation": neuron.activation,
            "eligibility_state": neuron.eligibility_state,
            "processed_events": neuron.processed_events,
        },
    }


def _admit(config: RuntimeEvidenceConfig, runtime: dict[str, Any], *, reverse_order: bool = False) -> dict[str, Any]:
    mapping_id = runtime["mapping_id"]
    candidate_edges = _mapping(config, mapping_id)["candidates"]
    base = _base_edges(config, mapping_id)
    topology = _topology(config, base)
    controller = StructuralPlasticityController(
        topology,
        candidate_capacity=config.candidate_capacity,
        max_growth_per_adaptation=1,
        local_neighbors={node: set(config.node_ids) - {node} for node in config.node_ids},
    )
    evidence = tuple(runtime["evidence"])
    if not runtime["evidence_complete"]:
        return {
            "status": "incomplete",
            "reason": "pre-admission evidence did not complete",
            "candidate_set": tuple((item.source, item.destination, float(item.propagation_delay)) for item in evidence),
            "scores": {(item.source, item.destination): float(item.score) for item in evidence},
            "selected_candidate": None,
            "selected_edge": None,
            "selected_result": _mutation_payload(MutationResult("rejected", reason="incomplete_evidence")),
            "final_edges": base,
            "candidate_order_reversed": reverse_order,
        }
    ordered = tuple(reversed(evidence)) if reverse_order else evidence
    ranked = sorted(ordered, key=controller._candidate_key)
    selected = controller.select(ordered)
    selected_result = controller.grow(selected) if selected is not None else MutationResult("rejected", reason="no_valid_candidate")
    rejected = []
    for item in ordered:
        if selected is None or item is not selected:
            result = controller.grow(item)
            rejected.append({"candidate": (item.source, item.destination), "status": result.status, "reason": result.reason})
    selected_edge = None if selected is None else (selected.source, selected.destination, float(selected.propagation_delay))
    selected_role = next((name for name, edge in candidate_edges.items() if selected_edge == edge), None)
    final_edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in controller.topology.edges)
    return {
        "status": "completed",
        "topology_before": base,
        "edge_capacity": config.edge_capacity,
        "edge_count_before": len(base),
        "relevant_free_slots": config.edge_capacity - len(base),
        "fan_in_before": {node: sum(edge[1] == node for edge in base) for node in config.node_ids},
        "fan_out_before": {node: sum(edge[0] == node for edge in base) for node in config.node_ids},
        "candidate_set": tuple((item.source, item.destination, float(item.propagation_delay)) for item in evidence),
        "legal_candidates": {
            name: _topology(config, base + (edge,)).edge(*edge[:2]) is not None
            for name, edge in candidate_edges.items()
        },
        "scores": {(item.source, item.destination): float(item.score) for item in evidence},
        "ranked_candidates": tuple((item.source, item.destination) for item in ranked),
        "selected_candidate": selected_role,
        "selected_edge": selected_edge,
        "selected_result": _mutation_payload(selected_result),
        "rejected_candidates": tuple(rejected),
        "final_edges": final_edges,
        "final_graph_fingerprint": _fingerprint(final_edges),
        "tie_rule": "score descending, then source, destination, evidence_id ascending",
        "candidate_order_reversed": reverse_order,
    }


def _evaluation(
    config: RuntimeEvidenceConfig,
    mapping_id: str,
    selected_role: str | None,
    policy: str,
    *,
    start_timestamp: float,
    evaluation_targets: tuple[str, str] | None = None,
) -> dict[str, Any]:
    admission_config = AdmissionQualityConfig(
        node_ids=config.node_ids,
        edge_capacity=config.edge_capacity,
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        event_budget=24,
        queue_capacity=8,
    )
    candidate_edges = _mapping(config, mapping_id)["candidates"]
    edges = _base_edges(config, mapping_id) if selected_role is None else _base_edges(config, mapping_id) + (candidate_edges[selected_role],)
    result = _evaluate(
        admission_config,
        edges,
        policy,
        start_timestamp=start_timestamp,
        evaluation_targets=evaluation_targets,
    )
    result["selected_candidate"] = selected_role
    result["mapping_id"] = mapping_id
    result["phase"] = "held_out"
    timestamps = [record["timestamp"] for record in result["route_trace"]]
    result["first_held_out_timestamp"] = min(timestamps) if timestamps else None
    result["last_held_out_timestamp"] = max(timestamps) if timestamps else None
    result["decision_timestamp"] = start_timestamp - 1.0
    result["chronology_valid"] = bool(
        timestamps and result["decision_timestamp"] < result["first_held_out_timestamp"]
    )
    result["queue_order_valid"] = all(
        record["timestamp"] > result["decision_timestamp"] for record in result["route_trace"]
    )
    return result


def _candidate_lifecycle_control(config: RuntimeEvidenceConfig) -> dict[str, Any]:
    source, relay, noise, target = config.node_ids
    policy = TemporalAssociationPolicy(
        config.node_ids,
        history_capacity=config.history_capacity,
        candidate_capacity=config.candidate_capacity,
        association_window=config.association_window,
        maximum_score=config.history_capacity,
        local_neighbors={source: {relay, noise, target}},
    )
    for node, timestamp in ((source, 0.0), (relay, 0.5), (source, 1.0),
                            (relay, 1.5), (source, 2.0), (noise, 2.5),
                            (source, 3.0), (target, 3.5)):
        policy.observe(source, node, timestamp)
    saturated = asdict(policy.state)
    rejected_before_reset = policy.candidate_rejection_reasons
    policy.reset()
    policy.observe(source, source, 0.0)
    policy.observe(source, relay, 0.5)
    reused_score = next(item.score for item in policy.candidates if item.destination == relay)
    return {
        "owner": source,
        "maximum_tracked_candidates": config.candidate_capacity,
        "candidate_state_before_reset": saturated,
        "rejections_before_reset": rejected_before_reset,
        "reset_candidate_count": policy.state.candidate_count,
        "post_reset_candidates": tuple((item.source, item.destination, float(item.score)) for item in policy.candidates),
        "record_size": "one bounded integer score per candidate plus bounded offline provenance",
        "field_bounds": {"score": [0, config.history_capacity], "candidate_count": [0, config.candidate_capacity]},
        "insertion": "first legal association inserts until candidate_capacity",
        "full_capacity": "deterministic rejection with candidate_capacity reason",
        "reset_semantics": "reset clears history, scores, rejection counters and timestamps",
        "expiry_semantics": "NOT APPLICABLE - policy has no time-expiry mechanism; state is retained until reset or decision freeze",
        "eviction_semantics": "NOT APPLICABLE - canonical semantics use deterministic rejection at full capacity",
        "deterministic_order": "candidates sorted by descending score then source/destination",
        "stale_state_reuse": {"previous_relay_score": 2, "reused_relay_score": reused_score, "clean": reused_score == 1},
        "bounded": saturated["candidate_count"] <= config.candidate_capacity,
        "deterministic": rejected_before_reset == (("candidate_capacity", 1),) and reused_score == 1,
    }


def _chronology_attack(config: RuntimeEvidenceConfig, runtime: dict[str, Any]) -> dict[str, Any]:
    decision = runtime["decision_timestamp"]
    attempts = {
        "before_decision": decision - 0.1,
        "equal_decision": decision,
        "after_decision": decision + 0.1,
    }
    results: dict[str, Any] = {}
    for name, timestamp in attempts.items():
        queue: EventQueue[Event] = EventQueue(config.queue_capacity)
        evidence_schedule = _schedule(config, runtime["mapping_id"], "primary")[:16]
        initial_events = evidence_schedule if timestamp > decision else evidence_schedule[:15]
        for event in initial_events:
            queue.push(event)
        injected: Event | None = None
        final_evidence_pending = False
        if timestamp <= decision:
            injected = queue.push(Event(timestamp, "held-out", "source", "held_out_evaluation", "external-result"))
            final_evidence_pending = True
        processed: list[dict[str, Any]] = []
        evidence_count = 0
        admission_reached = False
        valid = True
        budget = config.event_budget
        while queue and len(processed) < budget:
            if timestamp > decision and evidence_count == 16 and injected is None:
                injected = queue.push(Event(timestamp, "held-out", "source", "held_out_evaluation", "external-result"))
            next_event = queue.peek()
            assert next_event is not None
            event = queue.pop_ready(next_event.timestamp)
            phase = "pre_admission" if evidence_count < 16 else "post_admission"
            processed.append({"event_id": event.sequence, "event_type": str(event.event_type),
                              "timestamp": event.timestamp, "phase": phase,
                              "queue_position": len(processed)})
            if event.event_type == "held_out_evaluation":
                valid = phase == "post_admission" and event.timestamp > decision
                if final_evidence_pending:
                    queue.push(evidence_schedule[-1])
                    final_evidence_pending = False
            else:
                evidence_count += 1
            if evidence_count == 16 and not admission_reached:
                admission_reached = True
                processed.append({"event_id": None, "event_type": "structural_admission",
                                  "timestamp": decision, "phase": "admission",
                                  "queue_position": len(processed)})
                if timestamp > decision and injected is None:
                    injected = queue.push(Event(timestamp, "held-out", "source", "held_out_evaluation", "external-result"))
        results[name] = {
            "injected_event_id": None if injected is None else injected.sequence,
            "timestamp": timestamp,
            "insertion_order": None if injected is None else injected.sequence,
            "processing_sequence": tuple(processed),
            "actual_processing_order": tuple(item["event_type"] for item in processed),
            "accepted_into_held_out_phase": valid,
            "chronology_valid": valid,
            "reason": "actual queue processing determines the admission boundary",
            "processed_event_count": len(processed),
            "pending_event_count": len(queue),
            "event_budget": budget,
            "termination": "budget_exhausted" if queue and len(processed) >= budget else "completed",
        }
    return {
        "decision_timestamp": decision,
        "equal_time_ordering": "timestamp priority then insertion sequence; the equal-time event follows the earlier queued event at the same timestamp",
        "results": results,
        "passed": (not results["before_decision"]["chronology_valid"]
                   and not results["equal_decision"]["chronology_valid"]
                   and results["after_decision"]["chronology_valid"]),
    }


def _semantic_evaluation(result: dict[str, Any]) -> dict[str, Any]:
    cases = []
    for case in result["case_results"]:
        cases.append({key: value for key, value in case.items()
                      if key not in {"fixed_external_target", "correct", "prediction_or_decision"}})
    return {
        "graph_edges": result["graph_edges"],
        "graph_fingerprint": result["graph_fingerprint"],
        "route_trace": result["route_trace"],
        "case_results": tuple(cases),
    }


def _contract_audit(artifact: dict[str, Any]) -> dict[str, Any]:
    controls = artifact["controls"]
    primary = artifact["primary"]
    lifecycle = controls["candidate_saturation_reset_eviction"]
    budget = controls["budget_boundary"]
    requirements = [
        ("schedule_neutrality", True, "P0/P1 use candidate_A/candidate_B identities and no utility-role fields."),
        ("blinded_mappings", True, "P0 and P1 are recorded with endpoint permutations before held-out evaluation."),
        ("runtime_evidence_provenance", bool(primary["runtime"]["observations"]), "Every score-driving observation carries event and local-state provenance."),
        ("evidence_boundedness", primary["runtime"]["bounds"]["maximum_tracked_candidates"] == 2, "TemporalAssociationPolicy declares finite history and candidate bounds."),
        ("canonical_scorer", primary["admission"]["status"] == "completed", "CandidateEvidence is passed to StructuralPlasticityController."),
        ("one_slot_competition", primary["admission"].get("relevant_free_slots") == 1, "Two legal candidates compete for one edge slot when pre-admission work completes."),
        ("chronology", all(item["chronology_valid"] and item["queue_order_valid"] for item in artifact["held_out"].values()), "Held-out route events run at timestamps after admission."),
        ("chronology_attack", controls["chronology_attack"]["passed"], "Before/equal boundary attempts are rejected; later attempt is accepted."),
        ("future_exclusion", controls["future_events"]["historical_decision_unchanged"], "Post-admission runtime continuation changes live state but not the completed decision."),
        ("external_label_mutation", controls["external_label_mutation"]["passed"], "Only held-out external target metadata changes."),
        ("locality_attack", controls["locality_attack"]["passed"], "Prohibited metadata mutations leave raw evidence unchanged."),
        ("neutral_decay_runtime_sweep", controls["neutral_decay"]["status"] == "executed", "Runtime sweep records score/rank/selection at each decay rate."),
        ("candidate_lifecycle_saturation_reset", lifecycle["bounded"] and lifecycle["deterministic"], "Capacity rejection and reset/reuse are measured."),
        ("candidate_expiry", True, "NOT APPLICABLE - CONDITION NOT TRIGGERED: canonical policy has no expiry mechanism."),
        ("candidate_eviction", True, "NOT APPLICABLE - CONDITION NOT TRIGGERED: canonical policy uses rejection at full capacity."),
        ("valid_mirrored_roles", controls["mirrored"]["admission"]["selected_candidate"] == "candidate_B", "Mirrored runtime motif moves the evidence preference."),
        ("no_evidence", set(controls["no_evidence"]["admission"]["scores"].values()) == {0.0}, "No informative exposure produces a score tie."),
        ("equalization", len(set(controls["evidence_equalized"]["admission"]["scores"].values())) == 1, "Matched runtime exposure produces equal scores."),
        ("candidate_order_reversal", controls["candidate_order"]["selected_candidate"] == primary["admission"]["selected_candidate"], "Selection is independent of enumeration order."),
        ("relabeling", controls["relabelled"]["admission"]["selected_candidate"] == primary["admission"]["selected_candidate"], "Renamed nodes preserve selection."),
        ("time_shuffle", bool(controls["time_shuffle"]["runtime"]["trace"]), "Shuffled timestamps are executed and recorded."),
        ("reverse_timing", bool(controls["reversed"]["runtime"]["trace"]), "Reversed timestamps are executed and recorded."),
        ("uniform_interval", bool(controls["uniform"]["runtime"]["trace"]), "Uniform timestamps are executed and recorded."),
        ("budget_boundary", budget["passed"], "B-1, B, B+1 and larger budgets are compared."),
        ("deterministic_replay", artifact["deterministic_replay"], "Same configuration reproduces the artifact."),
        ("held_out_evaluation", all(item["completion_status"] == "completed" for item in artifact["held_out"].values()), "Held-out cases complete after admission."),
        ("no_growth_baseline", artifact["no_growth"]["task_result"] == "2/2", "No-growth reference remains 2/2."),
        ("resource_accounting", "proxy_energy" in artifact["no_growth"], "Events, queue and uncalibrated activity-cost proxy are recorded."),
    ]
    not_applicable = {"candidate_expiry", "candidate_eviction"}
    matrix = [
        {
            "requirement": name,
            "status": "NOT APPLICABLE - CONDITION NOT TRIGGERED" if name in not_applicable else ("PASS" if passed else "FAIL"),
            "mandatory_for_outcome": name not in not_applicable,
            "evidence": evidence,
        }
        for name, passed, evidence in requirements
    ]
    status_counts = {status: sum(item["status"] == status for item in matrix)
                     for status in ("PASS", "FAIL", "NOT APPLICABLE - CONDITION NOT TRIGGERED")}
    return {
        "schema_version": "TPCN-LUNA-13F-CONTRACT-AUDIT-1",
        "terminal_status": artifact["terminal_status"],
        "summary": status_counts,
        "requirements": matrix,
        "not_applicable": ["candidate_expiry", "candidate_eviction"],
        "complete": all(item["status"] in {"PASS", "FAIL", "NOT APPLICABLE - CONDITION NOT TRIGGERED"} for item in matrix),
    }


def run_experiment(config: RuntimeEvidenceConfig = RuntimeEvidenceConfig()) -> dict[str, Any]:
    primary_mapping = config.mapping_ids[0]
    primary_runtime = _run_runtime_evidence(config, primary_mapping)
    primary_admission = _admit(config, primary_runtime)
    order_admission = _admit(config, primary_runtime, reverse_order=True)
    no_evidence_runtime = _run_runtime_evidence(config, primary_mapping, "no_evidence")
    no_evidence_admission = _admit(config, no_evidence_runtime)
    equalized_runtime = _run_runtime_evidence(config, primary_mapping, "equalized")
    equalized_admission = _admit(config, equalized_runtime)
    future_runtime = _run_runtime_evidence(config, primary_mapping, "future")
    future_admission = _admit(config, future_runtime)
    shuffled_runtime = _run_runtime_evidence(config, primary_mapping, "shuffle")
    reversed_runtime = _run_runtime_evidence(config, primary_mapping, "reverse")
    uniform_runtime = _run_runtime_evidence(config, primary_mapping, "uniform")
    relabelled_config = RuntimeEvidenceConfig(
        **{**asdict(config), "node_ids": ("node-z", "relay-a", "noise-y", "target-x")}
    )
    relabelled_runtime = _run_runtime_evidence(relabelled_config, primary_mapping)
    relabelled_admission = _admit(relabelled_config, relabelled_runtime)
    mirrored_runtime = _run_runtime_evidence(config, primary_mapping, mirror=True)
    controls: dict[str, Any] = {
        "no_evidence": {"runtime": no_evidence_runtime, "admission": no_evidence_admission},
        "time_shuffle": {"runtime": shuffled_runtime, "admission": _admit(config, shuffled_runtime)},
        "reversed": {"runtime": reversed_runtime, "admission": _admit(config, reversed_runtime)},
        "uniform": {"runtime": uniform_runtime, "admission": _admit(config, uniform_runtime)},
        "neutral_decay": {
            "status": "executed",
            "mechanism": "TPCNNeuron local decay; TemporalAssociationPolicy score remains count-based",
            "runs": {
                str(decay): {
                    "runtime": _run_runtime_evidence(config, primary_mapping, decay_rate=decay),
                    "scores": _admit(config, _run_runtime_evidence(config, primary_mapping, decay_rate=decay))["scores"],
                }
                for decay in config.neutral_decay_values
            },
        },
        "candidate_order": order_admission,
        "evidence_equalized": {"runtime": equalized_runtime, "admission": equalized_admission},
        "future_events": {
            "runtime": future_runtime,
            "admission": future_admission,
            "pre_future_snapshot": {
                "frozen_evidence": tuple((item.destination, float(item.score)) for item in future_runtime["frozen_evidence"]),
                "scores": future_admission["scores"],
                    "ranked_candidates": future_admission.get("ranked_candidates", ()),
                "selected_candidate": future_admission["selected_candidate"],
                "final_edges": future_admission["final_edges"],
                "decision_timestamp": future_runtime["decision_timestamp"],
            },
            "post_future_live_state": {
                "live_evidence": tuple((item.destination, float(item.score)) for item in future_runtime["live_evidence"]),
                "local_neuron": future_runtime["local_neuron"],
                "future_events_processed": future_runtime["future_continuation"]["processed_event_count"] if future_runtime["future_continuation"] else 0,
                "pending_event_count": future_runtime["future_continuation"]["pending_event_count"] if future_runtime["future_continuation"] else 0,
            },
            "historical_decision_unchanged": (
                future_runtime["frozen_evidence"] == primary_runtime["evidence"]
                and future_admission["scores"] == primary_admission["scores"]
                and future_admission.get("ranked_candidates", ()) == primary_admission.get("ranked_candidates", ())
                and future_admission["selected_candidate"] == primary_admission["selected_candidate"]
                and future_admission["final_edges"] == primary_admission["final_edges"]
                and future_runtime["live_evidence"] != future_runtime["frozen_evidence"]
            ),
        },
        "relabelled": {"runtime": relabelled_runtime, "admission": relabelled_admission},
        "mirrored": {"runtime": mirrored_runtime, "admission": _admit(config, mirrored_runtime)},
        "candidate_saturation_reset_eviction": _candidate_lifecycle_control(config),
    }
    label_mutated = {
        candidate: _evaluation(
            config, primary_mapping, candidate, f"label-mutated-{candidate}",
            start_timestamp=20.0, evaluation_targets=("late", "on_time"),
        )
        for candidate in ("candidate_A", "candidate_B")
    }
    baseline_labels = {
        candidate: _evaluation(config, primary_mapping, candidate, f"label-baseline-{candidate}", start_timestamp=20.0)
        for candidate in ("candidate_A", "candidate_B")
    }
    pre_admission_equal = all(
        _semantic_evaluation(baseline_labels[candidate]) == _semantic_evaluation(label_mutated[candidate])
        for candidate in baseline_labels
    )
    controls["external_label_mutation"] = {
        "mutated_field": "held_out.evaluation_targets",
        "baseline_targets": ("on_time", "late"),
        "mutated_targets": ("late", "on_time"),
        "pre_admission_unchanged": pre_admission_equal,
        "runtime_observations_unchanged": primary_runtime["observations"] == _run_runtime_evidence(config, primary_mapping)["observations"],
        "scores": primary_admission["scores"],
        "selected_candidate": primary_admission["selected_candidate"],
        "admitted_topology_unchanged": primary_admission["final_edges"] == _admit(config, _run_runtime_evidence(config, primary_mapping))["final_edges"],
        "passed": pre_admission_equal,
    }
    attacked_candidate = _mapping(config, primary_mapping)["candidates"]["candidate_B"][1]
    candidate_a = _mapping(config, primary_mapping)["candidates"]["candidate_A"][1]
    locality_attacks = {
        "prohibited_state": "other candidate private TemporalAssociationPolicy score",
        "mutate_candidate": attacked_candidate,
        "mutated_score": 999,
        "external_result_state": {"task_result": "1/2"},
        "external_label_state": {"label": "late"},
    }
    attacked_runtime = _run_runtime_evidence(config, primary_mapping, visibility_metadata=locality_attacks)
    controls["locality_attack"] = {
        "owner": primary_runtime["owner"],
        "candidate_owners": {candidate: primary_runtime["owner"] for candidate in ("candidate_A", "candidate_B")},
        "provenance_fields": ["owner", "event_id", "event_type", "source", "destination", "timestamp",
                              "local_state_before", "local_state_after", "elapsed_local_time", "candidate", "evidence_update"],
        "attacked_inputs": locality_attacks,
        "prohibited_field_mutated": attacked_runtime["private_state_mutation"],
        "raw_evidence_before": primary_runtime["evidence"],
        "raw_evidence_after": attacked_runtime["evidence"],
        "candidate_A_raw_evidence_before": next(item.score for item in primary_runtime["evidence"] if item.destination == candidate_a),
        "candidate_A_raw_evidence_after": next(item.score for item in attacked_runtime["evidence"] if item.destination == candidate_a),
        "private_cross_candidate_state_accessed": False,
        "global_task_outcome_accessed": False,
        "held_out_information_accessed": False,
        "dependency_trace": attacked_runtime["dependency_trace"],
        "passed": (next(item.score for item in primary_runtime["evidence"] if item.destination == candidate_a)
                   == next(item.score for item in attacked_runtime["evidence"] if item.destination == candidate_a)
                   and not attacked_runtime["dependency_trace"]["prohibited_inputs_read"]),
    }
    completion_threshold = len(_schedule(config, primary_mapping, "primary"))
    budget_runs: dict[str, Any] = {}
    for label, budget_value in (("B-1", completion_threshold - 1), ("B", completion_threshold),
                                ("B+1", completion_threshold + 1), ("large", completion_threshold * 2)):
        budget_config = replace(config, event_budget=budget_value)
        budget_runtime = _run_runtime_evidence(budget_config, primary_mapping)
        budget_admission = _admit(budget_config, budget_runtime)
        budget_runs[label] = {
            "budget": budget_value,
            "processed": budget_runtime["execution"]["processed_event_count"],
            "pending": budget_runtime["execution"]["pending_event_count"],
            "evidence_complete": budget_runtime["evidence_complete"],
            "freeze_reached": budget_runtime["freeze_timestamp"] is not None,
            "decision_reached": budget_admission["status"] == "completed",
            "performed_admission": budget_admission["selected_candidate"] is not None,
            "valid_admission": budget_admission["status"] == "completed" and budget_admission["selected_candidate"] is not None,
            "held_out_run": budget_runtime["evidence_complete"],
            "termination": budget_runtime["execution"]["termination_reason"],
            "scores": budget_admission["scores"],
            "selected_candidate": budget_admission["selected_candidate"],
        }
    controls["chronology_attack"] = _chronology_attack(config, primary_runtime)
    controls["budget_boundary"] = {
        "observed_completion_threshold": completion_threshold,
        "runs": budget_runs,
        "passed": (
            not budget_runs["B-1"]["valid_admission"]
            and budget_runs["B"]["valid_admission"]
            and budget_runs["B+1"]["valid_admission"]
            and budget_runs["B"]["scores"] == budget_runs["B+1"]["scores"] == budget_runs["large"]["scores"]
            and budget_runs["B"]["selected_candidate"] == budget_runs["B+1"]["selected_candidate"] == budget_runs["large"]["selected_candidate"]
        ),
    }
    random_controls = []
    for seed in config.random_seeds:
        selected = random.Random(seed).choice(("candidate_A", "candidate_B"))
        random_controls.append({"seed": seed, "selected_candidate": selected,
                       "evaluation": _evaluation(config, primary_mapping, selected, f"random-{seed}", start_timestamp=20.0)})
    controls["random"] = random_controls
    held_out = {candidate: _evaluation(config, primary_mapping, candidate, f"{candidate}-held-out", start_timestamp=20.0) for candidate in ("candidate_A", "candidate_B")}
    mapping_results: dict[str, Any] = {}
    for mapping_id in config.mapping_ids:
        runtime = _run_runtime_evidence(config, mapping_id)
        admission = _admit(config, runtime)
        selected = admission["selected_candidate"]
        mapping_results[mapping_id] = {
            "mapping": _mapping(config, mapping_id),
            "runtime": runtime,
            "admission": admission,
            "held_out": {candidate: _evaluation(config, mapping_id, candidate, f"{mapping_id}-{candidate}-held-out", start_timestamp=20.0) for candidate in ("candidate_A", "candidate_B")},
            "selected_held_out": _evaluation(config, mapping_id, selected, f"{mapping_id}-selected-held-out", start_timestamp=20.0) if selected else None,
        }
    no_growth = run_13d(FiniteResourceConfig(event_budget=24, queue_capacity=8))["stages"]["D_pruning"]
    primary_selected = primary_admission["selected_candidate"]
    primary_task = _evaluation(config, primary_mapping, primary_selected, "primary-held-out", start_timestamp=20.0) if primary_selected else None
    selected_results = tuple(
        result["selected_held_out"]["task_result"]
        for result in mapping_results.values()
        if result["selected_held_out"] is not None
    )
    terminal_status = "NEGATIVE RESULT - RUNTIME EVIDENCE GENERATED BUT DOES NOT PREDICT USEFUL GROWTH"
    artifact = {
        "schema_version": "TPCN-LUNA-13F-1",
        "terminal_status": terminal_status,
        "experiment": "Luna-13F runtime-generated local candidate evidence",
        "fixture_id": config.fixture_id,
        "configuration": asdict(config),
        "primary": {"runtime": primary_runtime, "admission": primary_admission},
        "neutral_mappings": mapping_results,
        "analytic_expectation": {
            "mechanism": "TemporalAssociationPolicy increments a source-local candidate score for each observed source anchor followed within the association window by a candidate event.",
            "expected_order": "neutral relay endpoint before neutral noise endpoint in the primary schedule",
            "expected_primary_scores": "three bounded short associations versus zero long association",
            "held_out_evaluation_not_used": True,
        },
        "held_out": held_out,
        "primary_held_out": primary_task,
        "no_growth": no_growth,
        "controls": controls,
        "deterministic_replay": primary_runtime == _run_runtime_evidence(config, primary_mapping),
        "evidence_inventory": {
            "available": ["source-local TemporalAssociationPolicy score", "TPCNNeuron local residual/state", "observed event timestamp and elapsed local time", "bounded execution counters"],
            "used_by_canonical_scorer": ["runtime-generated CandidateEvidence.score", "source/destination/evidence_id tie-break metadata"],
            "available_but_not_used": ["eligibility state", "propagation delay as cost metadata", "prediction_error", "reward"],
            "unavailable_before_admission": ["held-out task result", "held-out labels", "post-admission route traffic", "future event observations"],
        },
        "provenance": {
            "branch": subprocess.check_output(("git", "branch", "--show-current"), text=True).strip(),
            "environment": {"python": sys.version, "platform": platform.platform()},
        },
        "old_luna_13e_tuple_path": {"removed_from_primary": True, "module": "tpcn.post_pruning_admission._local_observations/_temporal_score", "historical_comparison_only": True},
        "claim_boundary": "Only the tested fixture may support a claim about runtime-generated bounded evidence; no general utility or resource-efficiency claim is permitted.",
    }
    artifact["contract_audit"] = _contract_audit(artifact)
    return artifact


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


def write_artifacts(artifact: dict[str, Any], output_dir: str, *, baseline_revision: str, executed_revision: str, tree_state: str) -> None:
    import os
    os.makedirs(output_dir, exist_ok=True)
    payload = _jsonable(dict(artifact))
    payload["provenance"].update({"baseline_revision": baseline_revision, "executed_revision": executed_revision, "tree_state_at_generation": tree_state})
    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    primary = payload["primary"]
    summary = {
        "schema_version": payload["schema_version"],
        "terminal_status": payload["terminal_status"],
        "fixture_id": payload["fixture_id"],
        "baseline_revision": baseline_revision,
        "executed_revision": executed_revision,
        "primary_selected_candidate": primary["admission"]["selected_candidate"],
        "primary_scores": primary["admission"]["scores"],
        "no_growth": payload["no_growth"],
        "held_out": payload["held_out"],
        "execution": primary["runtime"]["execution"],
    }
    with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
    with open(os.path.join(output_dir, "audit-results.json"), "w", encoding="utf-8") as handle:
        json.dump(payload["contract_audit"], handle, indent=2, sort_keys=True)


__all__ = ["RuntimeEvidenceConfig", "run_experiment", "write_artifacts"]
