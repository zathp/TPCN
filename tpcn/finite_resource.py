"""Luna-13D finite-resource retention, pruning, and capacity experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import platform
import random
import subprocess
import sys
from typing import Any

from .causal_utility import UtilityConfig, _learn
from .canonical_neuron import TPCNNeuron
from .energy_utility import LocalEnergyModel
from .event_runtime import Event, EventQueue, execute_bounded
from .structural_plasticity import CandidateEvidence, MutationResult, StructuralPlasticityController
from .topology import BoundedTopology


EdgeTuple = tuple[str, str, float]
NODES = ("left", "right", "target", "relay", "noise")
USEFUL_EDGE: EdgeTuple = ("right", "target", 1.0)
EXPENSIVE_USEFUL_PATH: tuple[EdgeTuple, EdgeTuple] = (
    ("right", "relay", 0.5),
    ("relay", "target", 0.5),
)
EXPENSIVE_USELESS_PATH: tuple[EdgeTuple, EdgeTuple] = (
    ("left", "noise", 4.0),
    ("noise", "target", 4.0),
)


@dataclass(frozen=True, slots=True)
class FiniteResourceConfig:
    fixture_id: str = "luna-13d-interval-deadline-capacity-v1"
    event_budget: int = 24
    queue_capacity: int = 8
    fan_in_limit: int = 2
    fan_out_limit: int = 2
    edge_capacity: int = 6
    pruning_inactivity_threshold: int = 1
    pruning_utility_threshold: float = 0.1
    non_inferiority_cases: int = 2
    resource_reduction_threshold: float = 0.1
    random_seeds: tuple[int, ...] = (0, 1, 2, 3, 4)

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


class _TrafficObserver:
    def __init__(self) -> None:
        self.traffic: dict[EdgeTuple, int] = {}

    def record_route(self, edge: Any, _event: Event, _routed: Event) -> None:
        key = (edge.source, edge.destination, float(edge.propagation_delay))
        self.traffic[key] = self.traffic.get(key, 0) + 1


def _fingerprint(edges: tuple[EdgeTuple, ...]) -> str:
    return hashlib.sha256(repr(tuple(sorted(edges))).encode("utf-8")).hexdigest()


def _topology(config: FiniteResourceConfig, edges: tuple[EdgeTuple, ...], *, edge_capacity: int | None = None) -> BoundedTopology:
    return BoundedTopology.from_edges(
        NODES,
        edges,
        fan_in_limit=config.fan_in_limit,
        fan_out_limit=config.fan_out_limit,
        edge_capacity=edge_capacity or config.edge_capacity,
        routing_capacity=config.fan_out_limit,
    )


def _evaluate(config: FiniteResourceConfig, edges: tuple[EdgeTuple, ...], capacity_policy: str) -> dict[str, Any]:
    topology = _topology(config, edges)
    examples = (("short-held-out", 1.0, "on_time"), ("long-held-out", 3.0, "late"))
    case_results: list[dict[str, Any]] = []
    traffic_total: dict[EdgeTuple, int] = {}
    total_energy = 0.0
    failed_execution = False

    for example_id, interval, target in examples:
        neurons = {node: TPCNNeuron(node, decay_rate=0.1, input_gain=1.0) for node in NODES}
        queue: EventQueue[Event] = EventQueue(config.queue_capacity)
        queue.push(Event(0.0, "right", "right", "cue", 1.0))
        queue.push(Event(interval, "right", "right", "probe", -1.0))
        observer = _TrafficObserver()
        meter = LocalEnergyModel(f"luna-13d-{example_id}", max_counter=config.event_budget * 4)
        arrivals: list[float] = []

        def handle(event: Event, pending: EventQueue[Event]) -> None:
            meter.observe_event(event)
            neuron = neurons[event.destination]
            neuron.receive_event(event)
            if event.destination == "target":
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
            "fixed_external_target": target,
            "prediction_or_decision": decision,
            "correct": decision == target,
            "target_arrivals": tuple(arrivals),
            "target_latency": second_arrival,
            "events": execution.processed_event_count,
            "completion": asdict(execution),
        })
        for edge, count in observer.traffic.items():
            traffic_total[edge] = traffic_total.get(edge, 0) + count

    accuracy = sum(int(case["correct"]) for case in case_results)
    completion = "budget_exhausted" if failed_execution else "completed"
    return {
        "capacity_policy": capacity_policy,
        "capacity": config.edge_capacity,
        "capacity_used": len(edges),
        "remaining_slots": config.edge_capacity - len(edges),
        "graph_edges": edges,
        "graph_fingerprint": _fingerprint(edges),
        "useful_edge_present": USEFUL_EDGE in edges,
        "task_result": f"{accuracy}/2",
        "task_cases_correct": accuracy,
        "total_events": sum(case["events"] for case in case_results),
        "proxy_energy": total_energy,
        "proxy_energy_unit": "activity-cost-proxy; uncalibrated",
        "latency": tuple(case["target_latency"] for case in case_results),
        "queue_peak": max(case["completion"]["peak_queue_occupancy"] for case in case_results),
        "edge_traffic": {str(edge): count for edge, count in sorted(traffic_total.items())},
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
    neighbors = {source: set(NODES) - {source} for source in NODES}
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
    base = (USEFUL_EDGE,)
    controller = _controller(config, base, edge_capacity=capacity)
    mutations = []
    for evidence in (
        _candidate("left", "noise", 0.1, 4.0, "distractor-left-noise"),
        _candidate("noise", "target", 0.1, 4.0, "distractor-noise-target"),
        _candidate("right", "relay", 1.0, 0.5, "useful-relay-entry"),
        _candidate("relay", "target", 1.0, 0.5, "useful-relay-exit"),
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


def run_experiment(config: FiniteResourceConfig = FiniteResourceConfig()) -> dict[str, Any]:
    learning_config = UtilityConfig(event_budget=max(config.event_budget, 12), queue_capacity=config.queue_capacity)
    learned = _learn(learning_config)
    learned_edge = tuple(learned["admission"]["final_edges"][0])
    if learned_edge != USEFUL_EDGE:
        raise RuntimeError(f"unexpected Luna-13B learned edge: {learned_edge!r}")

    baseline_edges = (USEFUL_EDGE,)
    baseline = _evaluate(config, baseline_edges, "comfortable")
    expensive_useful = _evaluate(config, EXPENSIVE_USEFUL_PATH, "comfortable-expensive-useful")
    distractor_controller = _controller(config, baseline_edges)
    distractor_mutations = []
    for evidence in (
        _candidate("left", "noise", 0.1, 4.0, "unused-distractor"),
        _candidate("noise", "target", 0.1, 4.0, "expensive-useless"),
    ):
        distractor_mutations.append(_mutation_payload(distractor_controller.grow(evidence)))
    distractor_edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in distractor_controller.topology.edges)
    distractor = _evaluate(config, distractor_edges, "distractor-pressure")
    distractor["mutations"] = distractor_mutations

    pressure = tuple(_pressure_result(config, capacity) for capacity in (4, 5, 6))

    pruning_controller = _controller(config, distractor_edges)
    before_pruning = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in pruning_controller.topology.edges)
    scores = {
        (USEFUL_EDGE[0], USEFUL_EDGE[1]): 1.0,
        ("left", "noise"): 0.0,
        ("noise", "target"): 0.0,
    }
    pruned = tuple(_mutation_payload(result) for result in pruning_controller.prune_by_score(scores, maximum=2))
    after_pruning = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in pruning_controller.topology.edges)
    pruning = _evaluate(config, after_pruning, "declared-pruning")
    pruning["mutations"] = pruned
    pruning["graph_before"] = before_pruning
    pruning["capacity_freed"] = len(before_pruning) - len(after_pruning)
    pruning["failure_categories"]["pruning_related_failure"] = pruning["task_cases_correct"] < baseline["task_cases_correct"]

    later_controller = _controller(config, after_pruning)
    later_mutations = [
        later_controller.grow(_candidate("right", "relay", 1.0, 0.5, "later-useful-relay-entry")),
        later_controller.grow(_candidate("relay", "target", 1.0, 0.5, "later-useful-relay-exit")),
    ]
    later_edges = tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in later_controller.topology.edges)
    post_pruning = _evaluate(config, later_edges, "post-pruning-growth")
    post_pruning["mutations"] = tuple(_mutation_payload(result) for result in later_mutations)
    post_pruning["capacity_freed_before_growth"] = len(before_pruning) - len(after_pruning)

    fixed_edges = _evaluate(config, baseline_edges, "fixed-topology")
    random_controls = []
    for seed in config.random_seeds:
        source = random.Random(seed).choice(("left", "right"))
        edge = (source, "target", 1.0)
        result = _evaluate(config, (edge,), f"random-seed-{seed}")
        result["seed"] = seed
        result["policy"] = "equal-budget-random-growth"
        result["selected_edge"] = edge
        random_controls.append(result)

    edge_records = []
    for role, edge, utility, cost, age in (
        ("externally useful", USEFUL_EDGE, "2/2 present; 1/2 targeted removal in Luna-13C", 1.0, 0),
        ("expensive useful", EXPENSIVE_USEFUL_PATH[0], "baseline route contributes target arrivals", 2.0, 0),
        ("expensive useless", EXPENSIVE_USELESS_PATH[0], "no right-source traffic or external contribution", 4.0, 1),
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