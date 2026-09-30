"""Luna-13D finite-resource retention, pruning, and capacity experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import platform
import random
import subprocess
import sys
from typing import Any, Iterable

from .causal_utility import UtilityConfig, _learn
from .canonical_neuron import TPCNNeuron
from .energy_utility import LocalEnergyModel
from .event_runtime import Event, EventQueue, execute_bounded
from .structural_plasticity import CandidateEvidence, MutationResult, StructuralPlasticityController
from .topology import BoundedTopology


EdgeTuple = tuple[str, str, float]
OBSERVATION_HORIZON = 4.0


@dataclass(frozen=True, slots=True)
class FiniteResourceConfig:
    fixture_id: str = "luna-13d-interval-deadline-capacity-v1"
    event_budget: int = 24
    queue_capacity: int = 8
    fan_in_limit: int = 2
    fan_out_limit: int = 2
    edge_capacity: int = 6
    pruning_inactivity_threshold: int = 2
    pruning_utility_threshold: float = 0.1
    non_inferiority_cases: int = 2
    resource_reduction_threshold: float = 0.1
    random_seeds: tuple[int, ...] = (0, 1, 2, 3, 4)
    node_ids: tuple[str, str, str, str, str] = ("left", "right", "target", "relay", "noise")
    task_source_role: str = "right"

    def __post_init__(self) -> None:
        for value, name in (
            (self.event_budget, "event_budget"),
            (self.queue_capacity, "queue_capacity"),
            (self.fan_in_limit, "fan_in_limit"),
            (self.fan_out_limit, "fan_out_limit"),
            (self.edge_capacity, "edge_capacity"),
            (self.pruning_inactivity_threshold, "pruning_inactivity_threshold"),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.pruning_utility_threshold < 0.0 or self.resource_reduction_threshold < 0.0:
            raise ValueError("thresholds must be nonnegative")
        if not self.random_seeds:
            raise ValueError("random_seeds must not be empty")
        if len(self.node_ids) != 5 or len(set(self.node_ids)) != 5 or any(not node for node in self.node_ids):
            raise ValueError("node_ids must contain five distinct non-empty IDs")
        if self.task_source_role not in {"left", "right"}:
            raise ValueError("task_source_role must be left or right")


def _roles(config: FiniteResourceConfig) -> dict[str, str]:
    left, right, target, relay, noise = config.node_ids
    return {"left": left, "right": right, "target": target, "relay": relay, "noise": noise}


def _nodes(config: FiniteResourceConfig) -> tuple[str, ...]:
    return config.node_ids


def _useful_edge(config: FiniteResourceConfig) -> EdgeTuple:
    roles = _roles(config)
    return (roles[config.task_source_role], roles["target"], 1.0)


def _expensive_useful_path(config: FiniteResourceConfig) -> tuple[EdgeTuple, EdgeTuple]:
    roles = _roles(config)
    return (
        (roles[config.task_source_role], roles["relay"], 0.5),
        (roles["relay"], roles["target"], 0.5),
    )


def _expensive_useless_path(config: FiniteResourceConfig) -> tuple[EdgeTuple, EdgeTuple]:
    roles = _roles(config)
    unused_role = "left" if config.task_source_role == "right" else "right"
    return (
        (roles[unused_role], roles["noise"], 4.0),
        (roles["noise"], roles["target"], 4.0),
    )


class _TrafficObserver:
    def __init__(self) -> None:
        self.traffic: dict[EdgeTuple, int] = {}
        self.timestamps: dict[EdgeTuple, list[float]] = {}

    def record_route(self, edge: Any, _event: Event, _routed: Event) -> None:
        key = (edge.source, edge.destination, float(edge.propagation_delay))
        self.traffic[key] = self.traffic.get(key, 0) + 1
        self.timestamps.setdefault(key, []).append(float(_event.timestamp))


def _fingerprint(edges: tuple[EdgeTuple, ...]) -> str:
    return hashlib.sha256(repr(tuple(sorted(edges))).encode("utf-8")).hexdigest()


def _topology(config: FiniteResourceConfig, edges: tuple[EdgeTuple, ...], *, edge_capacity: int | None = None) -> BoundedTopology:
    return BoundedTopology.from_edges(
        _nodes(config),
        edges,
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        edge_capacity=edge_capacity or config.edge_capacity,
        routing_capacity=config.fan_out_limit,
    )


def _evaluate(config: FiniteResourceConfig, edges: tuple[EdgeTuple, ...], capacity_policy: str) -> dict[str, Any]:
    topology = _topology(config, edges)
    roles = _roles(config)
    task_source = roles[config.task_source_role]
    target = roles["target"]
    examples = (("short-held-out", 1.0, "on_time"), ("long-held-out", 3.0, "late"))
    case_results: list[dict[str, Any]] = []
    traffic_total: dict[EdgeTuple, int] = {}
    timestamp_total: dict[EdgeTuple, list[float]] = {}
    total_energy = 0.0
    failed_execution = False

    for example_id, interval, expected_target in examples:
        neurons = {node: TPCNNeuron(node, decay_rate=0.1, input_gain=1.0) for node in _nodes(config)}
        queue: EventQueue[Event] = EventQueue(config.queue_capacity)
        queue.push(Event(0.0, task_source, task_source, "cue", 1.0))
        queue.push(Event(interval, task_source, task_source, "probe", -1.0))
        observer = _TrafficObserver()
        meter = LocalEnergyModel(f"luna-13d-{example_id}", max_counter=config.event_budget * 4)
        arrivals: list[float] = []

        def handle(event: Event, pending: EventQueue[Event]) -> None:
            meter.observe_event(event)
            neuron = neurons[event.destination]
            neuron.receive_event(event)
            if event.destination == target:
                arrivals.append(float(event.timestamp))
            else:
                forwarded = Event(
                    event.timestamp,
                    event.destination,
                    event.destination,
                    event.event_type,
                    event.payload,
                )
                topology.route(forwarded, pending, observer=observer)

        execution = execute_bounded(queue, handle, event_budget=config.event_budget)
        total_energy += meter.energy
        failed_execution = failed_execution or execution.budget_exhausted
        second_arrival = arrivals[1] if len(arrivals) >= 2 else None
        decision = "on_time" if second_arrival is not None and second_arrival <= 3.0 else "late"
        case_results.append({
            "example_id": example_id,
            "interval": interval,
            "fixed_external_target": expected_target,
            "prediction_or_decision": decision,
            "correct": decision == expected_target,
            "target_arrivals": tuple(arrivals),
            "target_latency": second_arrival,
            "events": execution.processed_event_count,
            "completion": asdict(execution),
            "edge_timestamps": {str(edge): tuple(times) for edge, times in observer.timestamps.items()},
        })
        for edge, count in observer.traffic.items():
            traffic_total[edge] = traffic_total.get(edge, 0) + count
        for edge, times in observer.timestamps.items():
            timestamp_total.setdefault(edge, []).extend(times)

    edge_evidence = []
    observation_horizon = OBSERVATION_HORIZON
    for edge in topology.edges:
        key = (edge.source, edge.destination, float(edge.propagation_delay))
        use_count = traffic_total.get(key, 0)
        edge_timestamps = timestamp_total.get(key, [])
        last_use = None
        if edge_timestamps:
            last_use = max(edge_timestamps)
        age = observation_horizon if last_use is None else observation_horizon - last_use
        edge_evidence.append({
            "edge": key,
            "creation_time": 0.0,
            "use_count": use_count,
            "last_use_timestamp": last_use,
            "inactivity_age": age,
            "observed_utility": float(use_count),
            "observed_cost": float(use_count) * float(edge.propagation_delay),
            "pruning_score": float(use_count),
        })

    accuracy = sum(int(case["correct"]) for case in case_results)
    completion = "budget_exhausted" if failed_execution else "completed"
    return {
        "capacity_policy": capacity_policy,
        "capacity": config.edge_capacity,
        "capacity_used": len(edges),
        "remaining_slots": config.edge_capacity - len(edges),
        "graph_edges": edges,
        "graph_fingerprint": _fingerprint(edges),
        "useful_edge_present": _useful_edge(config) in edges,
        "task_result": f"{accuracy}/2",
        "task_cases_correct": accuracy,
        "total_events": sum(case["events"] for case in case_results),
        "proxy_energy": total_energy,
        "proxy_energy_unit": "activity-cost-proxy; uncalibrated",
        "latency": tuple(case["target_latency"] for case in case_results),
        "queue_peak": max(case["completion"]["peak_queue_occupancy"] for case in case_results),
        "edge_traffic": {str(edge): count for edge, count in sorted(traffic_total.items())},
        "edge_evidence": tuple(edge_evidence),
        "case_results": tuple(case_results),
        "completion_status": completion,
        "failure_categories": {
            "task_failure": accuracy < 2,
            "queue_rejection": False,
            "budget_exhaustion": failed_execution,
            "capacity_failure": False,
            "pruning_related_failure": False,
        },
    }


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


def _controller(config: FiniteResourceConfig, edges: tuple[EdgeTuple, ...], *, edge_capacity: int | None = None) -> StructuralPlasticityController:
    topology = _topology(config, edges, edge_capacity=edge_capacity)
    neighbors = {source: set(_nodes(config)) - {source} for source in _nodes(config)}
    return StructuralPlasticityController(
        topology,
        candidate_capacity=8,
        max_growth_per_adaptation=1,
        minimum_edge_count=1,
        local_neighbors=neighbors,
    )


def _candidate(source: str, destination: str, score: float, delay: float, evidence_id: str) -> CandidateEvidence:
    return CandidateEvidence(source, source, destination, score, delay, evidence_id)


def _pressure_result(config: FiniteResourceConfig, capacity: int) -> dict[str, Any]:
    roles = _roles(config)
    unused_role = "left" if config.task_source_role == "right" else "right"
    base = (_useful_edge(config),)
    controller = _controller(config, base, edge_capacity=capacity)
    mutations = []
    for evidence in (
        _candidate(roles[unused_role], roles["noise"], 0.1, 4.0, "distractor-unused-noise"),
        _candidate(roles["noise"], roles["target"], 0.1, 4.0, "distractor-noise-target"),
        _candidate(roles[config.task_source_role], roles["relay"], 1.0, 0.5, "useful-relay-entry"),
        _candidate(roles["relay"], roles["target"], 1.0, 0.5, "useful-relay-exit"),
    ):
        result = controller.grow(evidence)
        mutations.append(_mutation_payload(result))
    edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in controller.topology.edges)
    evaluation = _evaluate(config, edges, f"capacity-{capacity}")
    evaluation["capacity"] = capacity
    evaluation["capacity_used"] = len(edges)
    evaluation["remaining_slots"] = capacity - len(edges)
    evaluation["mutations"] = mutations
    evaluation["failure_categories"]["capacity_failure"] = any(item["status"] == "full_capacity" for item in mutations)
    return evaluation


def _pruning_eligibility(evidence: dict[str, Any], config: FiniteResourceConfig) -> tuple[bool, str]:
    inactive = float(evidence["inactivity_age"]) >= float(config.pruning_inactivity_threshold)
    low_utility = float(evidence["observed_utility"]) < float(config.pruning_utility_threshold)
    if inactive and low_utility:
        return True, "inactivity_and_utility"
    if inactive:
        return True, "inactivity"
    if low_utility:
        return True, "utility"
    return False, "retained"


def run_experiment(config: FiniteResourceConfig = FiniteResourceConfig(), *, _include_identity_controls: bool = True) -> dict[str, Any]:
    roles = _roles(config)
    unused_role = "left" if config.task_source_role == "right" else "right"
    learning_config = UtilityConfig(event_budget=max(config.event_budget, 12), queue_capacity=config.queue_capacity)
    learned = _learn(learning_config)
    learned_edge = tuple(learned["admission"]["final_edges"][0])
    if learned_edge != ("right", "target", 1.0):
        raise RuntimeError(f"unexpected Luna-13B learned edge: {learned_edge!r}")
    useful_edge = _useful_edge(config)

    baseline_edges = (useful_edge,)
    baseline = _evaluate(config, baseline_edges, "comfortable")
    expensive_useful = _evaluate(config, _expensive_useful_path(config), "comfortable-expensive-useful")
    distractor_controller = _controller(config, baseline_edges)
    distractor_mutations = []
    for evidence in (
        _candidate(roles[unused_role], roles["noise"], 0.1, 4.0, "unused-distractor"),
        _candidate(roles["noise"], roles["target"], 0.1, 4.0, "expensive-useless"),
    ):
        distractor_mutations.append(_mutation_payload(distractor_controller.grow(evidence)))
    distractor_edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in distractor_controller.topology.edges)
    distractor = _evaluate(config, distractor_edges, "distractor-pressure")
    distractor["mutations"] = distractor_mutations

    pressure = tuple(_pressure_result(config, capacity) for capacity in (4, 5, 6))

    pruning_controller = _controller(config, distractor_edges)
    before_pruning = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in pruning_controller.topology.edges)
    pruning_observation = _evaluate(config, distractor_edges, "pruning-observation")
    observed_by_edge = {tuple(item["edge"]): item for item in pruning_observation["edge_evidence"]}
    eligible: dict[EdgeTuple, str] = {}
    scores: dict[tuple[str, str], float] = {}
    for edge, evidence in observed_by_edge.items():
        is_eligible, reason = _pruning_eligibility(evidence, config)
        evidence["eligible"] = is_eligible
        evidence["eligibility_reason"] = reason
        if is_eligible:
            eligible[edge] = reason
            scores[(edge[0], edge[1])] = evidence["pruning_score"]
    pruned_results = pruning_controller.prune_by_score(scores, maximum=2)
    pruned = []
    for result in pruned_results:
        payload = _mutation_payload(result)
        edge_key = (payload["edge"]["source"], payload["edge"]["destination"], payload["edge"]["propagation_delay"])
        payload["reason"] = eligible.get(edge_key, "eligible")
        pruned.append(payload)
    pruned = tuple(pruned)
    after_pruning = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in pruning_controller.topology.edges)
    pruning = _evaluate(config, after_pruning, "declared-pruning")
    pruning["mutations"] = pruned
    pruning["graph_before"] = before_pruning
    pruning["capacity_freed"] = len(before_pruning) - len(after_pruning)
    pruning["pruning_evidence"] = tuple(observed_by_edge.values())
    pruning["failure_categories"]["pruning_related_failure"] = pruning["task_cases_correct"] < baseline["task_cases_correct"]

    later_controller = _controller(config, after_pruning)
    later_mutations = [
        later_controller.grow(_candidate(roles[config.task_source_role], roles["relay"], 1.0, 0.5, "later-useful-relay-entry")),
        later_controller.grow(_candidate(roles["relay"], roles["target"], 1.0, 0.5, "later-useful-relay-exit")),
    ]
    later_edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in later_controller.topology.edges)
    post_pruning = _evaluate(config, later_edges, "post-pruning-growth")
    post_pruning["mutations"] = tuple(_mutation_payload(result) for result in later_mutations)
    post_pruning["capacity_freed_before_growth"] = len(before_pruning) - len(after_pruning)

    fixed_edges = _evaluate(config, baseline_edges, "fixed-topology")
    random_controls = []
    for seed in config.random_seeds:
        source_role = random.Random(seed).choice(("left", "right"))
        edge = (roles[source_role], roles["target"], 1.0)
        result = _evaluate(config, (edge,), f"random-seed-{seed}")
        result["seed"] = seed
        result["policy"] = "equal-budget-random-growth"
        result["selected_edge"] = edge
        random_controls.append(result)

    edge_records = []
    for role, edge, utility, cost, age in (
        ("externally useful", useful_edge, "2/2 present; 1/2 targeted removal in Luna-13C", 1.0, 0),
        ("expensive useful", _expensive_useful_path(config)[0], "isolated path task result", 2.0, 0),
        ("expensive useless", _expensive_useless_path(config)[0], "no route traffic", 4.0, 1),
    ):
        edge_records.append({
            "edge_role": role,
            "edge": edge,
            "uses": baseline["edge_traffic"].get(str(edge), 0),
            "reward_utility_evidence": utility,
            "cost": cost,
            "age": age,
            "pruned": any(item.get("edge", {}).get("source") == edge[0] and item.get("edge", {}).get("destination") == edge[1] for item in pruned if item.get("edge")),
            "reason": "lowest declared utility score" if role == "expensive useless" else "retained or not eligible under declared score",
        })

    threshold_validation = []
    for age, expected in ((1.0, False), (2.0, True), (3.0, True)):
        evidence = {"inactivity_age": age, "observed_utility": 1.0}
        actual, reason = _pruning_eligibility(evidence, replace(config, pruning_inactivity_threshold=2, pruning_utility_threshold=0.0))
        threshold_validation.append({"metric": "inactivity", "observed_evidence": evidence, "threshold": 2, "expected_eligible": expected, "actual_eligible": actual, "reason": reason})
    for threshold, expected in ((0.0, False), (0.1, True)):
        evidence = {"inactivity_age": 0.0, "observed_utility": 0.0}
        actual, reason = _pruning_eligibility(evidence, replace(config, pruning_inactivity_threshold=10, pruning_utility_threshold=threshold))
        threshold_validation.append({"metric": "utility", "observed_evidence": evidence, "threshold": threshold, "expected_eligible": expected, "actual_eligible": actual, "reason": reason})

    identity_controls = {}
    if _include_identity_controls:
        for label, identity_config in (
            ("relabeled", replace(config, node_ids=("u-left", "u-right", "u-target", "u-relay", "u-noise"))),
            ("mirrored", replace(config, node_ids=("m-left", "m-right", "m-target", "m-relay", "m-noise"), task_source_role="left")),
        ):
            identity_artifact = run_experiment(identity_config, _include_identity_controls=False)
            identity_controls[label] = {
                "node_ids": identity_config.node_ids,
                "task_source_role": identity_config.task_source_role,
                "pruning_evidence": identity_artifact["stages"]["D_pruning"]["pruning_evidence"],
                "pruned_edges": identity_artifact["stages"]["D_pruning"]["mutations"],
                "capacity_freed": identity_artifact["stages"]["D_pruning"]["capacity_freed"],
                "task_result": identity_artifact["stages"]["D_pruning"]["task_result"],
            }

    return {
        "schema_version": "TPCN-LUNA-13D-1",
        "experiment": "Luna-13D finite-resource utility, retention, and capacity pressure",
        "fixture_id": config.fixture_id,
        "configuration": asdict(config),
        "provenance": {
            "environment": {"python": sys.version, "platform": platform.platform()},
            "branch": subprocess.check_output(("git", "branch", "--show-current"), text=True).strip(),
        },
        "task": {
            "source": "Luna-13C fixed external interval-deadline task",
            "external_target": "on_time for short interval and late for long interval",
            "decision_rule": "second target arrival at or before 3.0 is on_time; otherwise late",
            "target_independent_of_topology": True,
            "label_boundary": "labels affect evaluation only; no labels enter events, routing, evidence, utility or pruning",
        },
        "structural_learning": {
            "mechanism": "Luna-13B run_condition(decay_low)",
            "learned_edge": learned_edge,
            "candidate_records": learned["records"],
            "useful_edge_provenance": "Luna-13C corrective external effect, present 2/2 and targeted removal 1/2",
        },
        "thresholds_frozen_before_evaluation": {
            "inactivity": config.pruning_inactivity_threshold,
            "utility": config.pruning_utility_threshold,
            "matched_utility_cases": config.non_inferiority_cases,
            "resource_reduction": config.resource_reduction_threshold,
        },
        "pruning_semantics": {
            "evidence_fields": ["use_count", "last_use_timestamp", "inactivity_age", "observed_utility", "observed_cost", "pruning_score"],
            "score": "observed_utility = route use count",
            "eligibility": "prune when inactivity_age >= inactivity_threshold OR observed_utility < utility_threshold",
            "equality": "inactivity equality prunes; utility equality is retained",
            "selection": "among eligible edges, lowest observed pruning_score first, bounded maximum 2",
            "labels_or_endpoint_identity_used": False,
        },
        "threshold_validation": threshold_validation,
        "identity_controls": identity_controls,
        "stages": {
            "A_baseline": {"reference": baseline, "expensive_useful_path": expensive_useful},
            "B_distractor": distractor,
            "C_capacity_pressure": pressure,
            "D_pruning": pruning,
            "E_post_pruning_growth": post_pruning,
        },
        "controls": {"fixed_topology": fixed_edges, "random_growth": random_controls},
        "edge_records": edge_records,
        "checkpoint": {"implemented": False, "limitation": "Uses bounded deterministic rebuild/reset; no serialized neuron/queue/eligibility/random-state clone was added."},
        "evidence_labels": {
            "OBSERVED": ["learned edge provenance", "task/resource matrices", "mutation statuses", "traffic and completion counters"],
            "INFERRED": ["direct right-to-target traffic mediates the fixed task result"],
            "HYPOTHESIZED": ["declared utility score should distinguish useful and low-value edges under pressure"],
        },
        "interpretation": {
            "replacement_authorized": False,
            "resource_efficiency_claim": False,
            "note": "Resource comparisons remain Pareto-style; lower events with lower task utility are not efficiency evidence.",
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
    payload = dict(artifact)
    payload["provenance"] = {
        **payload["provenance"],
        "baseline_revision": baseline_revision,
        "executed_revision": executed_revision,
        "tree_state_at_generation": tree_state,
    }
    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as handle:
        json.dump(_jsonable(payload), handle, indent=2, sort_keys=True)
    stages = payload["stages"]
    run_rows = [("A_baseline", stages["A_baseline"]["reference"]),
                ("A_expensive_useful", stages["A_baseline"]["expensive_useful_path"]),
                ("B_distractor", stages["B_distractor"])]
    run_rows.extend((f"C_capacity_{stage['capacity']}", stage) for stage in stages["C_capacity_pressure"])
    run_rows.extend((name, stages[name]) for name in ("D_pruning", "E_post_pruning_growth"))
    run_rows.append(("fixed_topology", payload["controls"]["fixed_topology"]))
    run_rows.extend((f"random_seed_{stage['seed']}", stage) for stage in payload["controls"]["random_growth"])
    summary = {
        "schema_version": payload["schema_version"],
        "fixture_id": payload["fixture_id"],
        "baseline_revision": baseline_revision,
        "executed_revision": executed_revision,
        "runs": [{
            "run": name,
            "capacity_policy": stage.get("capacity_policy"),
            "useful_edge_present": stage.get("useful_edge_present"),
            "task_result": stage.get("task_result"),
            "events": stage.get("total_events"),
            "proxy_energy": stage.get("proxy_energy"),
            "latency": stage.get("latency"),
            "completion": stage.get("completion_status"),
        } for name, stage in run_rows],
    }
    with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(_jsonable(summary), handle, indent=2, sort_keys=True)


__all__ = ["FiniteResourceConfig", "run_experiment", "write_artifacts"]