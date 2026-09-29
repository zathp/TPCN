"""Luna-13C useful causal effect fixture built on the Luna-13B mechanism."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import platform
import random
import subprocess
import sys
from typing import Any, Literal

from .canonical_neuron import TPCNNeuron
from .event_runtime import Event, EventQueue, execute_bounded
from .temporal_crossover import CrossoverConfig, run_condition
from .topology import BoundedTopology


Condition = Literal[
    "learned_present",
    "targeted_removed",
    "restored",
    "sham",
    "irrelevant_removed",
    "fixed_useful",
    "fixed_topology",
    "random_growth",
]


@dataclass(frozen=True, slots=True)
class UtilityConfig:
    fixture_id: str = "luna-13c-interval-deadline-v1"
    source_ids: tuple[str, str] = ("left", "right")
    target_id: str = "target"
    propagation_delay: float = 1.0
    short_interval: float = 1.0
    long_interval: float = 3.0
    response_deadline: float = 3.0
    event_budget: int = 12
    queue_capacity: int = 8
    random_seed: int = 0

    def __post_init__(self) -> None:
        if len(self.source_ids) != 2 or len(set(self.source_ids)) != 2:
            raise ValueError("exactly two distinct source IDs are required")
        if not self.target_id or self.target_id in self.source_ids:
            raise ValueError("target_id must be distinct and non-empty")
        for value, name in (
            (self.propagation_delay, "propagation_delay"),
            (self.short_interval, "short_interval"),
            (self.long_interval, "long_interval"),
            (self.response_deadline, "response_deadline"),
        ):
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")
        if self.short_interval >= self.long_interval:
            raise ValueError("short_interval must be less than long_interval")
        if self.event_budget <= 0 or self.queue_capacity <= 0:
            raise ValueError("event_budget and queue_capacity must be positive")


@dataclass(frozen=True, slots=True)
class TaskExample:
    example_id: str
    interval: float
    target: str


def _examples(
    config: UtilityConfig,
    evaluation_targets: tuple[str, str] | None = None,
) -> tuple[TaskExample, ...]:
    targets = evaluation_targets or ("on_time", "late")
    if len(targets) != 2 or any(not isinstance(target, str) or not target for target in targets):
        raise ValueError("evaluation_targets must contain two non-empty strings")
    return (
        TaskExample("short-held-out", config.short_interval, targets[0]),
        TaskExample("long-held-out", config.long_interval, targets[1]),
    )


def _edge_tuple(source: str, destination: str, delay: float) -> tuple[str, str, float]:
    return (source, destination, float(delay))


def _fingerprint(edges: tuple[tuple[str, str, float], ...]) -> str:
    canonical = tuple(sorted(edges))
    return hashlib.sha256(repr(canonical).encode("utf-8")).hexdigest()


def _state_fingerprint(config: UtilityConfig, learned_result: dict[str, Any]) -> str:
    payload = {
        "config": asdict(config),
        "learned_edge": learned_result["admission"]["final_edges"],
        "candidate_records": learned_result["records"],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _learn(config: UtilityConfig) -> dict[str, Any]:
    crossover = CrossoverConfig(
        candidate_ids=config.source_ids,
        candidate_roles=config.source_ids,
        target_id=config.target_id,
        candidate_propagation_delay=config.propagation_delay,
        event_budget=config.event_budget,
        queue_capacity=16,
    )
    result = run_condition("decay_low", config=crossover, seed=config.random_seed)
    if not result["complete"] or result["admission"]["selected_candidate"] is None:
        raise RuntimeError("Luna-13B training fixture did not complete with an edge")
    if len(result["admission"]["final_edges"]) != 1:
        raise RuntimeError("Luna-13B training fixture did not produce one learned edge")
    return result


def _topology(config: UtilityConfig, edges: tuple[tuple[str, str, float], ...]) -> BoundedTopology:
    return BoundedTopology.from_edges(
        config.source_ids + (config.target_id,),
        edges,
        fan_in_limit=2,
        fan_out_limit=1,
        edge_capacity=2,
        routing_capacity=2,
    )


def _apply_intervention(
    config: UtilityConfig,
    base_edges: tuple[tuple[str, str, float], ...],
    action: str,
    target_edge: tuple[str, str, float] | None = None,
) -> tuple[tuple[str, str, float], ...]:
    """Apply every graph intervention through the same bounded rebuild path."""
    source_graph = _topology(config, base_edges)
    current_edges = tuple(
        (edge.source, edge.destination, float(edge.propagation_delay))
        for edge in source_graph.edges
    )
    if action == "sham_rebuild":
        next_edges = current_edges
    elif action == "remove_edge":
        if target_edge is None:
            raise ValueError("remove_edge requires target_edge")
        next_edges = tuple(edge for edge in current_edges if edge != target_edge)
    elif action == "restore_graph":
        next_edges = current_edges
    else:
        raise ValueError(f"unsupported intervention action: {action}")
    rebuilt_graph = _topology(config, next_edges)
    return tuple(
        (edge.source, edge.destination, float(edge.propagation_delay))
        for edge in rebuilt_graph.edges
    )


def _evaluate(
    config: UtilityConfig,
    condition: Condition,
    edges: tuple[tuple[str, str, float], ...],
    checkpoint_fingerprint: str,
    examples: tuple[TaskExample, ...],
    intervention: str,
) -> dict[str, Any]:
    topology = _topology(config, edges)
    neurons = {
        node: TPCNNeuron(node, decay_rate=0.1, input_gain=1.0)
        for node in config.source_ids + (config.target_id,)
    }
    trace: list[dict[str, Any]] = []
    case_results: list[dict[str, Any]] = []

    for example in examples:
        for neuron in neurons.values():
            neuron.reset()
        queue: EventQueue[Event] = EventQueue(config.queue_capacity)
        queue.push(Event(0.0, config.source_ids[1], config.source_ids[1], "cue", 1.0))
        queue.push(Event(example.interval, config.source_ids[1], config.source_ids[1], "probe", -1.0))
        arrivals: list[float] = []

        def handle(event: Event, pending: EventQueue[Event]) -> None:
            if event.destination in config.source_ids:
                neurons[event.destination].receive_event(event)
                topology.route(event, pending)
                trace.append({
                    "example_id": example.example_id,
                    "kind": "source",
                    "timestamp": event.timestamp,
                    "source": event.source,
                    "destination": event.destination,
                    "payload": event.payload,
                })
                return
            neuron = neurons[config.target_id]
            neuron.receive_event(event)
            arrivals.append(event.timestamp)
            trace.append({
                "example_id": example.example_id,
                "kind": "target_arrival",
                "timestamp": event.timestamp,
                "source": event.source,
                "destination": event.destination,
                "payload": event.payload,
            })

        execution = execute_bounded(queue, handle, event_budget=config.event_budget)
        second_arrival = arrivals[1] if len(arrivals) >= 2 else None
        decision = "on_time" if second_arrival is not None and second_arrival <= config.response_deadline else "late"
        case_results.append({
            "example_id": example.example_id,
            "interval": example.interval,
            "fixed_external_target": example.target,
            "prediction_or_decision": decision,
            "correct": decision == example.target,
            "target_arrivals": tuple(arrivals),
            "target_state": neurons[config.target_id].state,
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

    accuracy = sum(int(case["correct"]) for case in case_results) / len(case_results)
    return {
        "condition": condition,
        "intervention": intervention,
        "checkpoint_fingerprint": checkpoint_fingerprint,
        "graph_edges": edges,
        "graph_fingerprint": _fingerprint(edges),
        "primary_metric": "accuracy",
        "primary_metric_value": accuracy,
        "case_results": tuple(case_results),
        "trace": tuple(trace),
        "all_completed": all(case["completion"]["completed"] for case in case_results),
        "total_events": sum(case["events"] for case in case_results),
        "target_arrival_count": sum(len(case["target_arrivals"]) for case in case_results),
    }


def run_experiment(
    *,
    config: UtilityConfig = UtilityConfig(),
    evaluation_targets: tuple[str, str] | None = None,
) -> dict[str, Any]:
    learned = _learn(config)
    learned_edge = tuple(learned["admission"]["final_edges"][0])
    irrelevant_edge = _edge_tuple(config.source_ids[0], config.target_id, config.propagation_delay)
    positive_control_edge = _edge_tuple(config.source_ids[1], config.target_id, 0.5)
    learned_only = (learned_edge,)
    frozen_graph = tuple(sorted((learned_edge, irrelevant_edge)))
    checkpoint = _state_fingerprint(config, learned)
    random_source = random.Random(config.random_seed).choice(config.source_ids)
    random_edge = _edge_tuple(random_source, config.target_id, config.propagation_delay)
    interventions: dict[Condition, tuple[str, tuple[tuple[str, str, float], ...], tuple[str, str, float] | None]] = {
        "learned_present": ("restore_graph", frozen_graph, None),
        "targeted_removed": ("remove_edge", frozen_graph, learned_edge),
        "restored": ("restore_graph", frozen_graph, None),
        "sham": ("sham_rebuild", frozen_graph, None),
        "irrelevant_removed": ("remove_edge", frozen_graph, irrelevant_edge),
        "fixed_useful": ("restore_graph", (positive_control_edge,), None),
        "fixed_topology": ("restore_graph", (), None),
        "random_growth": ("restore_graph", (random_edge,), None),
    }
    examples = _examples(config, evaluation_targets)
    results = {
        condition: _evaluate(
            config,
            condition,
            _apply_intervention(config, base_edges, action, target_edge),
            checkpoint,
            examples,
            action,
        )
        for condition, (action, base_edges, target_edge) in interventions.items()
    }
    label_isolation = None
    if evaluation_targets is None:
        relabeled = run_experiment(config=config, evaluation_targets=("late", "on_time"))
        label_isolation = {
            "mutated_targets": ["late", "on_time"],
            "structural_state_unchanged": relabeled["structural_learning"] == {
                "mechanism": "Luna-13B run_condition(decay_low)",
                "learned_edge": learned_edge,
                "candidate_records": learned["records"],
                "training_runtime": learned["runtime"],
                "training_graph_fingerprint": _fingerprint(learned_only),
                "frozen_checkpoint_fingerprint": checkpoint,
                "frozen_graph_edges": frozen_graph,
                "irrelevant_edge": irrelevant_edge,
                "positive_control_edge": positive_control_edge,
            },
            "pre_output_computation_unchanged": all(
                results[condition]["trace"] == relabeled["results"][condition]["trace"]
                and results[condition]["graph_edges"] == relabeled["results"][condition]["graph_edges"]
                and results[condition]["total_events"] == relabeled["results"][condition]["total_events"]
                for condition in results
            ),
        }
    return {
        "schema_version": "TPCN-LUNA-13C-1",
        "experiment": "Luna-13C useful causal effect of learned temporal structure",
        "fixture_id": config.fixture_id,
        "configuration": asdict(config),
        "task": {
            "definition": "The same cue/probe payloads are sent with short or long elapsed interval.",
            "external_target": "on_time for the short interval and late for the long interval",
            "target_independent_of_topology": True,
            "examples": [asdict(example) for example in examples],
            "split": "structural training uses the Luna-13B fixture; both task cases are frozen held-out evaluation cases",
            "decision_rule": f"second target arrival at or before {config.response_deadline} is on_time; otherwise late",
            "primary_metric": "per-case accuracy",
            "practical_effect_threshold": 0.5,
        },
        "structural_learning": {
            "mechanism": "Luna-13B run_condition(decay_low)",
            "learned_edge": learned_edge,
            "candidate_records": learned["records"],
            "training_runtime": learned["runtime"],
            "training_graph_fingerprint": _fingerprint(learned_only),
            "frozen_checkpoint_fingerprint": checkpoint,
            "frozen_graph_edges": frozen_graph,
            "irrelevant_edge": irrelevant_edge,
            "positive_control_edge": positive_control_edge,
        },
        "results": results,
        "label_isolation_attack": label_isolation,
        "controls": {
            "random_seed": config.random_seed,
            "random_selection": "random.Random(seed).choice(source_ids)",
            "random_candidate_opportunity": list(config.source_ids),
            "same_event_payloads": [1.0, -1.0],
            "same_event_budget": config.event_budget,
            "same_queue_capacity": config.queue_capacity,
        },
        "evidence_labels": {
            "OBSERVED": ["runtime-local learned edge", "paired target decisions", "completion counters"],
            "INFERRED": ["target arrival through the learned edge mediates the task decision"],
            "HYPOTHESIZED": ["the narrow causal utility claim pending gate evaluation"],
        },
    }


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


def write_artifacts(
    artifact: dict[str, Any],
    output_dir: str,
    *,
    baseline_revision: str,
    executed_revision: str,
    tree_state: str,
) -> None:
    import os

    os.makedirs(output_dir, exist_ok=True)
    artifact = dict(artifact)
    artifact["provenance"] = {
        "baseline_revision": baseline_revision,
        "executed_revision": executed_revision,
        "tree_state_at_generation": tree_state,
        "branch": subprocess.check_output(("git", "branch", "--show-current"), text=True).strip(),
        "environment": {"python": sys.version, "platform": platform.platform()},
    }
    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as handle:
        json.dump(_jsonable(artifact), handle, indent=2, sort_keys=True)
    summary = {
        condition: {
            "primary_metric_value": result["primary_metric_value"],
            "graph_fingerprint": result["graph_fingerprint"],
            "all_completed": result["all_completed"],
            "total_events": result["total_events"],
        }
        for condition, result in artifact["results"].items()
    }
    with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(_jsonable(summary), handle, indent=2, sort_keys=True)


__all__ = ["Condition", "TaskExample", "UtilityConfig", "run_experiment", "write_artifacts"]