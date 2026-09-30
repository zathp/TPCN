"""Luna-13F runtime-generated bounded local candidate evidence fixture."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
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
from .post_pruning_admission import AdmissionQualityConfig, _base_edges, _candidate_edges, _evaluate
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
    beneficial_role: str = "relay"
    harmful_role: str = "noise"

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
        if {self.beneficial_role, self.harmful_role} != {"relay", "noise"}:
            raise ValueError("beneficial_role and harmful_role must be relay/noise")
        if self.association_window <= 0.0:
            raise ValueError("association_window must be positive")


def _roles(config: RuntimeEvidenceConfig) -> dict[str, str]:
    source, relay, noise, target = config.node_ids
    return {"source": source, "relay": relay, "noise": noise, "target": target}


def _fingerprint(edges: Iterable[Edge]) -> str:
    return hashlib.sha256(repr(tuple(sorted(edges))).encode("utf-8")).hexdigest()


def _candidate_edges(config: RuntimeEvidenceConfig) -> dict[str, Edge]:
    roles = _roles(config)
    return {
        "G": (roles["source"], roles[config.beneficial_role], 0.5),
        "H": (roles["source"], roles[config.harmful_role], 1.0),
    }


def _base_edges(config: RuntimeEvidenceConfig) -> tuple[Edge, ...]:
    roles = _roles(config)
    return (
        (roles[config.beneficial_role], roles["target"], 0.5),
        (roles[config.harmful_role], roles["target"], 2.0),
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


def _schedule(config: RuntimeEvidenceConfig, control: str, *, mirror: bool = False) -> tuple[Event, ...]:
    roles = _roles(config)
    source = roles["source"]
    short_role = config.beneficial_role if not mirror else config.harmful_role
    long_role = config.harmful_role if not mirror else config.beneficial_role
    short_node = roles[short_role]
    long_node = roles[long_role]
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
        Event(6.0, long_node, source, "candidate_observation", 0.5),
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
            timestamps = (3.0, 6.0, 0.0, 7.0, 2.0, 5.0, 1.0, 4.0)
        return tuple(Event(timestamp, event.source, event.destination, event.event_type, event.payload)
                     for event, timestamp in zip(base, timestamps))
    if control == "equalized":
        return (
            Event(0.0, source, source, "local_anchor", 1.0),
            Event(1.0, short_node, source, "candidate_observation", 0.5),
            Event(2.0, source, source, "local_anchor", 1.0),
            Event(3.0, short_node, source, "candidate_observation", 0.5),
            Event(4.0, source, source, "local_anchor", 1.0),
            Event(5.0, long_node, source, "candidate_observation", 0.5),
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


def _run_runtime_evidence(config: RuntimeEvidenceConfig, control: str = "primary", *, mirror: bool = False) -> dict[str, Any]:
    roles = _roles(config)
    source = roles["source"]
    candidates = {roles["relay"], roles["noise"]}
    policy = TemporalAssociationPolicy(
        config.node_ids,
        history_capacity=config.history_capacity,
        candidate_capacity=config.candidate_capacity,
        association_window=config.association_window,
        maximum_score=config.history_capacity,
        local_neighbors={source: candidates},
    )
    neuron = TPCNNeuron(source, decay_rate=0.1, input_gain=1.0)
    queue: EventQueue[Event] = EventQueue(config.queue_capacity)
    events = _schedule(config, control, mirror=mirror)
    for event in events:
        queue.push(event)
    observations: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []
    last_anchor: float | None = None

    def handle(event: Event, _pending: EventQueue[Event]) -> None:
        nonlocal last_anchor
        context: list[dict[str, Any]] = []
        neuron._temporal_context_hook = context.append
        before_policy = asdict(policy.state)
        neuron.receive_event(event)
        if event.source == source:
            policy.observe(source, source, event.timestamp)
            last_anchor = event.timestamp
        elif event.source in candidates:
            if last_anchor is not None:
                policy.observe(source, event.source, event.timestamp)
            after_policy = asdict(policy.state)
            score_map = {(item.source, item.destination): float(item.score) for item in policy.candidates}
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
                "evidence_update": score_map.get((source, event.source), 0.0),
                "policy_state_before": before_policy,
                "policy_state_after": after_policy,
                "evidence_timestamp": float(event.timestamp),
            })
        trace.append({"event_id": event.sequence, "source": event.source,
                      "destination": event.destination, "timestamp": event.timestamp,
                      "event_type": str(event.event_type)})

    execution = execute_bounded(queue, handle, event_budget=config.event_budget)
    runtime_scores = {
        item.destination: float(item.score)
        for item in policy.candidates
        if item.source == source
    }
    evidence = tuple(
        CandidateEvidence(
            source,
            source,
            edge[1],
            runtime_scores.get(edge[1], 0.0),
            edge[2],
            f"runtime-{source}-{edge[1]}",
        )
        for edge in _candidate_edges(config).values()
    )
    if control == "no_evidence":
        evidence = ()
    decision_timestamp = max((item["evidence_timestamp"] for item in observations), default=0.0)
    return {
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
        "evidence": evidence,
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
        "decision_timestamp": decision_timestamp,
        "execution": {
            "configured_event_budget": execution.configured_event_budget,
            "processed_event_count": execution.processed_event_count,
            "pending_event_count": execution.pending_event_count,
            "peak_queue_occupancy": execution.peak_queue_occupancy,
            "termination_reason": execution.termination_reason,
            "completed": execution.completed,
            "budget_exhausted": execution.budget_exhausted,
        },
        "trace": tuple(trace),
        "local_neuron": {
            "state": neuron.state,
            "activation": neuron.activation,
            "eligibility_state": neuron.eligibility_state,
            "processed_events": neuron.processed_events,
        },
    }


def _admit(config: RuntimeEvidenceConfig, runtime: dict[str, Any], *, reverse_order: bool = False) -> dict[str, Any]:
    base = _base_edges(config)
    topology = _topology(config, base)
    controller = StructuralPlasticityController(
        topology,
        candidate_capacity=config.candidate_capacity,
        max_growth_per_adaptation=1,
        local_neighbors={rolesource: set(config.node_ids) - {rolesource} for rolesource in config.node_ids},
    )
    evidence = tuple(runtime["evidence"])
    ordered = tuple(reversed(evidence)) if reverse_order else evidence
    ranked = sorted(ordered, key=controller._candidate_key)
    selected = controller.select(ordered)
    selected_result = controller.grow(selected) if selected is not None else MutationResult("rejected", reason="no_valid_candidate")
    rejected = []
    for item in ordered:
        if selected is None or item is not selected:
            result = controller.grow(item)
            rejected.append({"candidate": (item.source, item.destination), "status": result.status, "reason": result.reason})
    candidate_edges = _candidate_edges(config)
    selected_edge = None if selected is None else (selected.source, selected.destination, float(selected.propagation_delay))
    selected_role = next((name for name, edge in candidate_edges.items() if selected_edge == edge), None)
    final_edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in controller.topology.edges)
    return {
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


def _evaluation(config: RuntimeEvidenceConfig, selected_role: str | None, policy: str) -> dict[str, Any]:
    admission_config = AdmissionQualityConfig(
        node_ids=config.node_ids,
        edge_capacity=config.edge_capacity,
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        event_budget=24,
        queue_capacity=8,
        beneficial_role=config.beneficial_role,
        harmful_role=config.harmful_role,
    )
    edges = _base_edges(config) if selected_role is None else _base_edges(config) + (_candidate_edges(config)[selected_role],)
    result = _evaluate(admission_config, edges, policy)
    result["selected_candidate"] = selected_role
    return result


def run_experiment(config: RuntimeEvidenceConfig = RuntimeEvidenceConfig()) -> dict[str, Any]:
    primary_runtime = _run_runtime_evidence(config)
    primary_admission = _admit(config, primary_runtime)
    order_admission = _admit(config, primary_runtime, reverse_order=True)
    no_evidence_runtime = _run_runtime_evidence(config, "no_evidence")
    no_evidence_admission = _admit(config, no_evidence_runtime)
    equalized_runtime = _run_runtime_evidence(config, "equalized")
    equalized_admission = _admit(config, equalized_runtime)
    future_runtime = _run_runtime_evidence(config, "future")
    future_admission = _admit(config, future_runtime)
    shuffled_runtime = _run_runtime_evidence(config, "shuffle")
    reversed_runtime = _run_runtime_evidence(config, "reverse")
    uniform_runtime = _run_runtime_evidence(config, "uniform")
    relabelled_config = RuntimeEvidenceConfig(
        **{**asdict(config), "node_ids": ("node-z", "relay-a", "noise-y", "target-x")}
    )
    relabelled_runtime = _run_runtime_evidence(relabelled_config)
    relabelled_admission = _admit(relabelled_config, relabelled_runtime)
    mirrored_runtime = _run_runtime_evidence(config, mirror=True)
    controls: dict[str, Any] = {
        "no_evidence": {"runtime": no_evidence_runtime, "admission": no_evidence_admission},
        "time_shuffle": {"runtime": shuffled_runtime, "admission": _admit(config, shuffled_runtime)},
        "reversed": {"runtime": reversed_runtime, "admission": _admit(config, reversed_runtime)},
        "uniform": {"runtime": uniform_runtime, "admission": _admit(config, uniform_runtime)},
        "neutral_decay": {"status": "not_applicable", "reason": "canonical TemporalAssociationPolicy uses bounded counts, not a decay parameter"},
        "candidate_order": order_admission,
        "evidence_equalized": {"runtime": equalized_runtime, "admission": equalized_admission},
        "future_events": {"runtime": future_runtime, "admission": future_admission},
        "relabelled": {"runtime": relabelled_runtime, "admission": relabelled_admission},
        "mirrored": {"runtime": mirrored_runtime, "admission": _admit(config, mirrored_runtime)},
    }
    random_controls = []
    for seed in config.random_seeds:
        selected = random.Random(seed).choice(("G", "H"))
        random_controls.append({"seed": seed, "selected_candidate": selected,
                               "evaluation": _evaluation(config, selected, f"random-{seed}")})
    controls["random"] = random_controls
    held_out = {candidate: _evaluation(config, candidate, f"{candidate}-held-out") for candidate in ("G", "H")}
    no_growth = run_13d(FiniteResourceConfig(event_budget=24, queue_capacity=8))["stages"]["D_pruning"]
    return {
        "schema_version": "TPCN-LUNA-13F-1",
        "terminal_status": "BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION",
        "experiment": "Luna-13F runtime-generated local candidate evidence",
        "fixture_id": config.fixture_id,
        "configuration": asdict(config),
        "primary": {"runtime": primary_runtime, "admission": primary_admission},
        "analytic_expectation": {
            "mechanism": "TemporalAssociationPolicy increments a source-local candidate score for each observed source anchor followed within the association window by a candidate event.",
            "expected_order": "beneficial-role endpoint before harmful-role endpoint in the primary schedule",
            "expected_primary_scores": "three bounded short associations versus zero long association",
            "held_out_evaluation_not_used": True,
        },
        "held_out": held_out,
        "no_growth": no_growth,
        "controls": controls,
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


__all__ = ["RuntimeEvidenceConfig", "run_experiment", "write_artifacts"]
