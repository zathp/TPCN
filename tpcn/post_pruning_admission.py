"""Luna-13E bounded post-pruning admission discrimination fixture."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import platform
import random
import subprocess
import sys
from typing import Any

from .canonical_neuron import TPCNNeuron
from .event_runtime import Event, EventQueue, execute_bounded
from .finite_resource import FiniteResourceConfig, run_experiment as run_13d
from .structural_plasticity import CandidateEvidence, MutationResult, StructuralPlasticityController
from .topology import BoundedTopology


Edge = tuple[str, str, float]


@dataclass(frozen=True, slots=True)
class AdmissionQualityConfig:
    fixture_id: str = "luna-13e-post-pruning-admission-v1"
    event_budget: int = 24
    queue_capacity: int = 8
    edge_capacity: int = 3
    fan_in_limit: int = 2
    fan_out_limit: int = 1
    task_source_role: str = "source"
    node_ids: tuple[str, str, str, str] = ("source", "relay", "noise", "target")
    beneficial_role: str = "relay"
    harmful_role: str = "noise"
    random_seeds: tuple[int, ...] = (0, 1, 2, 3, 4)

    def __post_init__(self) -> None:
        for value, name in (
            (self.event_budget, "event_budget"),
            (self.queue_capacity, "queue_capacity"),
            (self.edge_capacity, "edge_capacity"),
            (self.fan_in_limit, "fan_in_limit"),
            (self.fan_out_limit, "fan_out_limit"),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if len(self.node_ids) != 4 or len(set(self.node_ids)) != 4:
            raise ValueError("node_ids must contain four distinct IDs")
        if self.beneficial_role == self.harmful_role or self.beneficial_role not in {"relay", "noise"} or self.harmful_role not in {"relay", "noise"}:
            raise ValueError("beneficial and harmful roles must be relay/noise and distinct")


def _roles(config: AdmissionQualityConfig) -> dict[str, str]:
    source, relay, noise, target = config.node_ids
    return {"source": source, "relay": relay, "noise": noise, "target": target}


def _fingerprint(edges: tuple[Edge, ...]) -> str:
    return hashlib.sha256(repr(tuple(sorted(edges))).encode("utf-8")).hexdigest()


def _base_edges(config: AdmissionQualityConfig) -> tuple[Edge, ...]:
    roles = _roles(config)
    return (
        (roles[config.beneficial_role], roles["target"], 0.5),
        (roles[config.harmful_role], roles["target"], 2.0),
    )


def _candidate_edges(config: AdmissionQualityConfig) -> dict[str, Edge]:
    roles = _roles(config)
    return {
        "G": (roles["source"], roles[config.beneficial_role], 0.5),
        "H": (roles["source"], roles[config.harmful_role], 1.0),
    }


def _topology(config: AdmissionQualityConfig, edges: tuple[Edge, ...]) -> BoundedTopology:
    return BoundedTopology.from_edges(
        config.node_ids,
        edges,
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        edge_capacity=config.edge_capacity,
        routing_capacity=config.fan_out_limit,
    )


def _local_observations(candidate: str, *, include_future: bool = False) -> tuple[dict[str, Any], ...]:
    observations = {
        "G": ((0.0, 0.5), (1.0, 1.5), (2.0, 2.5)),
        "H": ((0.0, 3.0),),
    }[candidate]
    records = tuple(
        {"candidate": candidate, "source_time": source, "related_time": related, "elapsed": related - source}
        for source, related in observations
    )
    if include_future:
        return records + ({"candidate": candidate, "source_time": 10.0, "related_time": 10.5, "elapsed": 0.5, "future": True},)
    return records


def _temporal_score(candidate: str, *, include_future: bool = False) -> float:
    records = _local_observations(candidate, include_future=include_future)
    return float(sum(record["elapsed"] <= 1.0 for record in records if not record.get("future")))


def _candidate(
    config: AdmissionQualityConfig,
    candidate: str,
    *,
    score_override: float | None = None,
    include_future: bool = False,
) -> tuple[CandidateEvidence, dict[str, Any]]:
    edge = _candidate_edges(config)[candidate]
    score = _temporal_score(candidate, include_future=include_future) if score_override is None else score_override
    evidence = CandidateEvidence(edge[0], edge[0], edge[1], score, edge[2], f"local-observation-{candidate.lower()}")
    provenance = {
        "candidate": candidate,
        "field": "temporal_score",
        "value": score,
        "source_owner": "source-local bounded observation buffer",
        "observation_records": _local_observations(candidate, include_future=include_future),
        "available_time": 2.5 if candidate == "G" else 3.0,
        "decision_time": 4.0,
        "local": True,
        "bounded": True,
        "pre_admission": True,
        "future_dependent": False,
        "label_dependent": False,
        "endpoint_identity_dependent": False,
        "used_in_canonical_score": True,
        "cost_evidence": {
            "propagation_delay": edge[2],
            "predicted_total_path_delay": None,
            "available_before_decision": True,
            "used_in_canonical_score": False,
        },
        "future_records_delivered_after_decision": include_future,
        "future_records_used_in_score": False,
    }
    return evidence, provenance


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


def _evaluate(config: AdmissionQualityConfig, edges: tuple[Edge, ...], policy: str) -> dict[str, Any]:
    topology = _topology(config, edges)
    roles = _roles(config)
    source = roles[config.task_source_role]
    target = roles["target"]
    examples = (("short-held-out", 1.0, "on_time"), ("long-held-out", 3.0, "late"))
    cases: list[dict[str, Any]] = []
    route_trace: list[dict[str, Any]] = []
    total_events = 0
    total_energy = 0.0
    queue_peak = 0
    for example_id, interval, expected in examples:
        neurons = {node: TPCNNeuron(node, decay_rate=0.1, input_gain=1.0) for node in config.node_ids}
        queue: EventQueue[Event] = EventQueue(config.queue_capacity)
        queue.push(Event(0.0, source, source, "cue", 1.0))
        queue.push(Event(interval, source, source, "probe", -1.0))
        arrivals: list[float] = []
        processed_energy = 0.0

        def handle(event: Event, pending: EventQueue[Event]) -> None:
            nonlocal processed_energy
            processed_energy += 1.0
            neurons[event.destination].receive_event(event)
            if event.destination == target:
                arrivals.append(float(event.timestamp))
                route_trace.append({"example_id": example_id, "kind": "target_arrival", "timestamp": event.timestamp, "source": event.source, "destination": event.destination, "event_type": str(event.event_type)})
                return
            before = len(pending)
            forwarded = Event(event.timestamp, event.destination, event.destination, event.event_type, event.payload)
            routed = topology.route(forwarded, pending)
            route_trace.append({"example_id": example_id, "kind": "route", "timestamp": event.timestamp, "source": event.destination, "routed_count": len(routed), "queue_before": before, "queue_after": len(pending)})

        execution = execute_bounded(queue, handle, event_budget=config.event_budget)
        second_arrival = arrivals[1] if len(arrivals) >= 2 else None
        decision = "on_time" if second_arrival is not None and second_arrival <= 3.0 else "late"
        total_events += execution.processed_event_count
        total_energy += processed_energy
        queue_peak = max(queue_peak, execution.peak_queue_occupancy)
        cases.append({
            "example_id": example_id,
            "interval": interval,
            "fixed_external_target": expected,
            "prediction_or_decision": decision,
            "correct": decision == expected,
            "target_arrivals": tuple(arrivals),
            "target_state": neurons[target].state,
            "target_latency": second_arrival,
            "events": execution.processed_event_count,
            "completion": {
                "configured_event_budget": execution.configured_event_budget,
                "processed_event_count": execution.processed_event_count,
                "pending_event_count": execution.pending_event_count,
                "peak_queue_occupancy": execution.peak_queue_occupancy,
                "termination_reason": execution.termination_reason,
                "completed": execution.completed,
                "budget_exhausted": execution.budget_exhausted,
            },
        })
    correct = sum(int(case["correct"]) for case in cases)
    return {
        "policy": policy,
        "graph_edges": edges,
        "graph_fingerprint": _fingerprint(edges),
        "task_result": f"{correct}/2",
        "task_cases_correct": correct,
        "total_events": total_events,
        "proxy_energy": total_energy,
        "proxy_energy_unit": "activity-cost-proxy; uncalibrated",
        "latency": tuple(case["target_latency"] for case in cases),
        "queue_peak": queue_peak,
        "case_results": tuple(cases),
        "route_trace": tuple(route_trace),
        "prediction_error_records": (),
        "completion_status": "budget_exhausted" if any(not case["completion"]["completed"] for case in cases) else "completed",
    }


def _competition(
    config: AdmissionQualityConfig,
    *,
    score_override: dict[str, float] | None = None,
    include_future: bool = False,
) -> dict[str, Any]:
    base = _base_edges(config)
    candidates: list[CandidateEvidence] = []
    provenance: list[dict[str, Any]] = []
    for candidate in ("G", "H"):
        evidence, record = _candidate(config, candidate, score_override=None if score_override is None else score_override[candidate], include_future=include_future)
        candidates.append(evidence)
        provenance.append(record)
    controller = StructuralPlasticityController(
        _topology(config, base),
        candidate_capacity=8,
        max_growth_per_adaptation=1,
        local_neighbors={node: set(config.node_ids) - {node} for node in config.node_ids},
    )
    ranked = sorted(zip(("G", "H"), candidates), key=lambda item: controller._candidate_key(item[1]))
    selected = controller.select(candidates)
    mutation = controller.grow(selected) if selected is not None else MutationResult("rejected", reason="no_valid_candidate")
    chosen = next((candidate for candidate in ("G", "H") if selected and selected.destination == _candidate_edges(config)[candidate][1]), None)
    final_edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in controller.topology.edges)
    return {
        "topology_before": base,
        "capacity_before": config.edge_capacity,
        "capacity_used_before": len(base),
        "relevant_free_slots": config.edge_capacity - len(base),
        "fan_in_before": {node: sum(edge[1] == node for edge in base) for node in config.node_ids},
        "fan_out_before": {node: sum(edge[0] == node for edge in base) for node in config.node_ids},
        "candidate_set": tuple((candidate.source, candidate.destination, float(candidate.propagation_delay)) for candidate in candidates),
        "candidate_evidence": tuple(provenance),
        "scores": {candidate: float(item.score) for candidate, item in zip(("G", "H"), candidates)},
        "ranks": {candidate: index + 1 for index, (candidate, _evidence) in enumerate(ranked)},
        "chosen_candidate": chosen,
        "rejected_candidate": "H" if chosen == "G" else "G" if chosen == "H" else None,
        "rejection_reason": "lost_one_slot_rank_competition" if chosen else "no_valid_candidate",
        "mutation": _mutation_payload(mutation),
        "final_edges": final_edges,
        "final_graph_fingerprint": _fingerprint(final_edges),
        "evaluation": _evaluate(config, final_edges, "current-policy"),
    }


def _mutate_external_labels(competition: dict[str, Any]) -> dict[str, Any]:
    evaluation = dict(competition["evaluation"])
    mutated_cases = []
    for case in evaluation["case_results"]:
        mutated = dict(case)
        mutated["fixed_external_target"] = "late" if case["fixed_external_target"] == "on_time" else "on_time"
        mutated_cases.append(mutated)
    evaluation["case_results"] = tuple(mutated_cases)
    result = dict(competition)
    result["evaluation"] = evaluation
    result["mutated_external_targets"] = tuple(case["fixed_external_target"] for case in mutated_cases)
    result["runtime_input_unchanged"] = True
    return result


def _threshold_and_abstention(config: AdmissionQualityConfig) -> dict[str, Any]:
    base = _base_edges(config)
    controller = StructuralPlasticityController(_topology(config, base), max_growth_per_adaptation=1)
    evidence, _ = _candidate(config, "H", score_override=-1.0)
    result = controller.grow(evidence)
    return {
        "score_threshold": None,
        "confidence_threshold": None,
        "abstention_supported": False,
        "negative_score_growth": _mutation_payload(result),
        "forced_growth_when_selected": result.status == "grown",
    }


def run_experiment(config: AdmissionQualityConfig = AdmissionQualityConfig()) -> dict[str, Any]:
    reference = run_13d(FiniteResourceConfig(event_budget=24, queue_capacity=8))
    stage_a = {
        "fixture_id": reference["fixture_id"],
        "baseline_post_pruning": reference["stages"]["D_pruning"],
        "harmful_post_growth": reference["stages"]["E_post_pruning_growth"],
        "diagnostic_trace": {
            "baseline_post_pruning": reference["stages"]["D_pruning"]["case_results"],
            "harmful_post_growth": reference["stages"]["E_post_pruning_growth"]["case_results"],
            "prediction_error_records": (),
        },
        "mechanism": "duplicate direct/relay target arrivals make the long case on_time; the fixed target is late",
    }
    current = _competition(config)
    candidate_evaluations = {
        candidate: _evaluate(config, _base_edges(config) + (_candidate_edges(config)[candidate],), f"{candidate}-held-out")
        for candidate in ("G", "H")
    }
    equalized = _competition(config, score_override={"G": 1.0, "H": 1.0})
    future = _competition(config, include_future=True)
    relabeled = _competition(AdmissionQualityConfig(**{**asdict(config), "node_ids": ("node-z", "relay-a", "noise-y", "target-x")}))
    mirrored_config = AdmissionQualityConfig(**{**asdict(config), "node_ids": ("source-z", "noise-a", "relay-y", "target-x"), "beneficial_role": "noise", "harmful_role": "relay"})
    mirrored = _competition(mirrored_config)
    label_mutated = _mutate_external_labels(current)
    random_controls = []
    for seed in config.random_seeds:
        selected = random.Random(seed).choice(("G", "H"))
        graph = _base_edges(config) + (_candidate_edges(config)[selected],)
        evaluation = _evaluate(config, graph, f"random-seed-{seed}")
        random_controls.append({"seed": seed, "selected_candidate": selected, "graph": graph, "evaluation": evaluation})
    ablations = {
        "temporal_evidence_only": current,
        "score_removed": _competition(config, score_override={"G": 0.0, "H": 0.0}),
        "cost_evidence_removed": current,
        "residual_state_removed": {"available": False, "reason": "not exposed by current admission interface"},
        "prediction_error_removed": {"available": False, "reason": "no prediction/error term is exposed by current fixture admission"},
        "utility_reward_removed": {"available": False, "reason": "no reward/utility term is exposed before admission"},
    }
    return {
        "schema_version": "TPCN-LUNA-13E-1",
        "experiment": "Luna-13E post-pruning admission quality and harmful-growth discrimination",
        "fixture_id": config.fixture_id,
        "configuration": asdict(config),
        "provenance": {
            "branch": subprocess.check_output(("git", "branch", "--show-current"), text=True).strip(),
            "environment": {"python": sys.version, "platform": platform.platform()},
        },
        "frozen_ground_truth": {
            "G": "source -> beneficial-role intermediate at 0.5, then 0.5 to target; expected held-out task 2/2",
            "H": "source -> harmful-role intermediate at 1.0, then 2.0 to target; expected held-out task 0/2",
            "external_only": True,
            "frozen_before_policy_comparison": True,
            "task": "Luna-13C interval-deadline task: short interval target on_time, long interval target late",
        },
        "stage_A_harmful_growth_reproduction": stage_a,
        "competition": current,
        "candidate_evaluations": candidate_evaluations,
        "controls": {
            "fixed_no_growth": _evaluate(config, _base_edges(config), "fixed-no-growth"),
            "random": random_controls,
            "relabelled": relabeled,
            "mirrored": mirrored,
            "evidence_equalized": equalized,
            "future_events_after_decision": future,
            "label_mutated": label_mutated,
        },
        "ablations": ablations,
        "threshold_and_abstention": _threshold_and_abstention(config),
        "evidence_inventory": {
            "available": ["CandidateEvidence.score", "observer/source locality", "propagation_delay", "candidate endpoint metadata", "evidence_id tie-break metadata"],
            "used_by_canonical_scorer": ["score", "source", "destination", "evidence_id only for deterministic tie-break"],
            "available_but_not_used": ["propagation_delay; no predicted total path cost"],
            "unavailable_before_admission": ["task result", "held-out label", "post-admission traffic", "candidate utility memory", "predicted total path cost", "prediction/error state", "prior reward/eligibility in this fixture"],
        },
        "claim_boundary": "A score-driven preference follows bounded temporal evidence in this fixture; no general utility prediction is claimed.",
        "evidence_labels": {
            "OBSERVED": ["controller score/rank/admission", "held-out task outcomes", "route traces", "bounded execution metrics"],
            "INFERRED": ["duplicate direct/relay arrivals cause the Luna-13D long-case regression"],
            "HYPOTHESIZED": ["richer authorized pre-admission evidence may be needed outside this fixture"],
        },
    }


def _jsonable(value: Any) -> Any:
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
    controls = payload["controls"]
    rows = [("current-policy", payload["competition"]), ("fixed-no-growth", controls["fixed_no_growth"]), ("evidence-equalized", controls["evidence_equalized"])]
    rows.extend((f"random-{item['seed']}", item) for item in controls["random"])
    summary = {
        "schema_version": payload["schema_version"],
        "fixture_id": payload["fixture_id"],
        "baseline_revision": baseline_revision,
        "executed_revision": executed_revision,
        "runs": [{"policy": name, "chosen_candidate": stage.get("chosen_candidate", stage.get("selected_candidate")), "task_result": stage.get("evaluation", stage).get("task_result"), "events": stage.get("evaluation", stage).get("total_events"), "proxy_energy": stage.get("evaluation", stage).get("proxy_energy"), "completion": stage.get("evaluation", stage).get("completion_status")} for name, stage in rows],
    }
    with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)


__all__ = ["AdmissionQualityConfig", "run_experiment", "write_artifacts"]
