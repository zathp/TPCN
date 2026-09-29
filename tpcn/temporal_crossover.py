"""Luna-13B causal local temporal structural crossover fixture."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import platform
import sys
from typing import Any, Literal

from .canonical_neuron import TPCNNeuron
from .event_runtime import Event, EventQueue, execute_bounded
from .structural_plasticity import CandidateEvidence, StructuralPlasticityController
from .topology import BoundedTopology


Condition = Literal[
    "decay_low",
    "decay_high",
    "decay_near",
    "ordinary",
    "reversed",
    "shuffled",
    "random",
    "score_shuffled",
    "fixed",
    "uniform",
    "neutral",
]


@dataclass(frozen=True, slots=True)
class CrossoverConfig:
    fixture_id: str = "luna-13b-runtime-local-crossover-v1"
    candidate_roles: tuple[str, str] = ("left", "right")
    candidate_ids: tuple[str, str] = ("left", "right")
    target_id: str = "target"
    stimulus_id: str = "stimulus"
    amplitudes: tuple[float, float] = (0.7, 1.0)
    observation_intervals: tuple[float, float] = (1.0, 3.0)
    stimulus_delay: float = 0.25
    execution_decay: float = 0.1
    scoring_decay_low: float = 0.0
    scoring_decay_high: float = 0.2
    event_budget: int = 12
    queue_capacity: int = 16
    candidate_propagation_delay: float = 1.0

    def __post_init__(self) -> None:
        if len(self.candidate_roles) != 2 or len(self.candidate_ids) != 2:
            raise ValueError("exactly two candidate roles and IDs are required")
        if len(set(self.candidate_ids)) != 2:
            raise ValueError("candidate IDs must be distinct")
        for value, name in zip(self.amplitudes, ("left_amplitude", "right_amplitude")):
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        for value, name in zip(self.observation_intervals, ("left_interval", "right_interval")):
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        for value, name in ((self.stimulus_delay, "stimulus_delay"),
                            (self.execution_decay, "execution_decay"),
                            (self.scoring_decay_low, "scoring_decay_low"),
                            (self.scoring_decay_high, "scoring_decay_high"),
                            (self.candidate_propagation_delay, "candidate_propagation_delay")):
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.event_budget <= 0 or self.queue_capacity <= 0:
            raise ValueError("event_budget and queue_capacity must be positive")


def frozen_crossover(config: CrossoverConfig = CrossoverConfig()) -> dict[str, float]:
    """Derive the equality point from the implemented score equation."""
    residuals = tuple(
        amplitude * math.exp(-config.execution_decay * interval)
        for amplitude, interval in zip(config.amplitudes, config.observation_intervals)
    )
    interval_delta = config.observation_intervals[1] - config.observation_intervals[0]
    if interval_delta == 0.0 or residuals[0] <= 0.0 or residuals[1] <= 0.0:
        raise ValueError("crossover requires distinct positive intervals and residuals")
    crossover = math.log(residuals[1] / residuals[0]) / interval_delta
    return {
        "left_residual_at_execution_decay": residuals[0],
        "right_residual_at_execution_decay": residuals[1],
        "interval_delta": interval_delta,
        "scoring_decay_crossover": crossover,
        "equation": "score = abs(local_residual) * exp(-scoring_decay * elapsed)",
        "equality": "r_left * exp(-mu * dt_left) = r_right * exp(-mu * dt_right)",
    }


def _role_map(config: CrossoverConfig, mirror: bool) -> dict[str, str]:
    roles = config.candidate_roles[::-1] if mirror else config.candidate_roles
    return dict(zip(roles, config.candidate_ids))


def _observation_topology(config: CrossoverConfig, condition: Condition,
                          role_to_id: dict[str, str]) -> BoundedTopology:
    target_delays_by_role = dict(zip(config.candidate_roles, config.observation_intervals))
    if condition == "uniform":
        target_delays_by_role = {role: config.observation_intervals[0] for role in config.candidate_roles}
    left_id, right_id = config.candidate_ids
    id_to_role = {candidate_id: role for role, candidate_id in role_to_id.items()}
    left_stimulus = f"{config.stimulus_id}-{left_id}"
    right_stimulus = f"{config.stimulus_id}-{right_id}"
    edges = (
        (left_stimulus, left_id, config.stimulus_delay),
        (right_stimulus, right_id, config.stimulus_delay),
        (config.target_id, left_id, config.stimulus_delay + target_delays_by_role[id_to_role[left_id]]),
        (config.target_id, right_id, config.stimulus_delay + target_delays_by_role[id_to_role[right_id]]),
    )
    return BoundedTopology.from_edges(
        (left_stimulus, right_stimulus, config.target_id, left_id, right_id), edges,
        fan_in_limit=2, fan_out_limit=2, edge_capacity=4, routing_capacity=4,
    )


def _score_for_condition(condition: Condition, residual: float, elapsed: float,
                         scoring_decay: float) -> tuple[float, str]:
    if condition == "ordinary":
        return 1.0, "ordinary_temporal_association"
    if condition == "neutral":
        scoring_decay = 0.0
    if condition in {"decay_low", "decay_high", "decay_near", "uniform", "neutral"}:
        return abs(residual) * math.exp(-scoring_decay * elapsed), "runtime_local_decay_score"
    if condition in {"reversed", "shuffled"}:
        return 0.0, "no_ordered_local_association"
    return abs(residual) * math.exp(-scoring_decay * elapsed), "runtime_local_decay_score"


def _run_observations(
    config: CrossoverConfig,
    condition: Condition,
    scoring_decay: float,
    *,
    mirror: bool,
    future_probe: bool,
) -> tuple[tuple[dict[str, Any], ...], dict[str, Any]]:
    role_to_id = _role_map(config, mirror)
    id_to_role = {candidate_id: role for role, candidate_id in role_to_id.items()}
    topology = _observation_topology(config, condition, role_to_id)
    queue: EventQueue[Event] = EventQueue(config.queue_capacity)
    seed_time = 4.0 if condition in {"reversed", "shuffled"} else 0.0
    source_nodes = {f"{config.stimulus_id}-{candidate_id}" for candidate_id in config.candidate_ids}
    for candidate_id in config.candidate_ids:
        role = id_to_role[candidate_id]
        amplitude = config.amplitudes[config.candidate_roles.index(role)]
        source_node = f"{config.stimulus_id}-{candidate_id}"
        queue.push(Event(seed_time, source_node, source_node, "seed", amplitude))
    queue.push(Event(0.0, config.target_id, config.target_id, "seed", 0.0))
    if future_probe:
        queue.push(Event(10.0, config.target_id, config.target_id, "future_probe", 0.0))
    neurons = {
        candidate_id: TPCNNeuron(candidate_id, decay_rate=config.execution_decay)
        for candidate_id in config.candidate_ids
    }
    first_observations: dict[str, dict[str, Any]] = {}
    records: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []

    def handle(event: Event, pending: EventQueue[Event]) -> None:
        if event.destination in source_nodes | {config.target_id}:
            topology.route(event, pending)
            trace.append({"kind": "route_seed", "source": event.source,
                          "timestamp": event.timestamp, "sequence": event.sequence})
            return
        candidate_id = event.destination
        context: list[dict[str, Any]] = []
        neuron = neurons[candidate_id]
        neuron._temporal_context_hook = context.append
        neuron.receive_event(Event(event.timestamp, event.source, candidate_id,
                                   "local_observation", event.payload))
        trace.append({"kind": "local_observation", "source": event.source,
                      "destination": candidate_id, "timestamp": event.timestamp,
                      "sequence": event.sequence, "payload": event.payload})
        if event.source in source_nodes:
            first_observations[candidate_id] = {
                "event_source": event.source,
                "event_sequence": event.sequence,
                "timestamp": event.timestamp,
                "payload": float(event.payload),
            }
            return
        if (event.source != config.target_id or candidate_id not in first_observations
            or any(record["candidate_id"] == candidate_id for record in records)):
            return
        local = context[-1]
        first = first_observations[candidate_id]
        elapsed = event.timestamp - first["timestamp"]
        score, score_source = _score_for_condition(
            condition, float(local["residual_state"]), elapsed, scoring_decay,
        )
        records.append({
            "candidate_id": candidate_id,
            "candidate_role": id_to_role[candidate_id],
            "evidence_source": score_source,
            "originating_observation": {
                "source": first["event_source"], "timestamp": first["timestamp"],
                "sequence": first["event_sequence"], "payload": first["payload"],
            },
            "followup_observation": {
                "source": event.source, "timestamp": event.timestamp,
                "sequence": event.sequence, "payload": float(event.payload),
            },
            "observation_timestamp": first["timestamp"],
            "decision_observation_timestamp": event.timestamp,
            "elapsed_interval": elapsed,
            "local_pre_state": float(local["pre_state"]),
            "local_residual_state": float(local["residual_state"]),
            "execution_decay": config.execution_decay,
            "scoring_decay": scoring_decay,
            "score_components": {
                "local_residual_magnitude": abs(float(local["residual_state"])),
                "elapsed_decay_factor": math.exp(-scoring_decay * elapsed),
            },
            "score": score,
            "decision_timestamp": event.timestamp,
        })

    execution = execute_bounded(queue, handle, event_budget=config.event_budget)
    records.sort(key=lambda item: item["candidate_id"])
    ranked = sorted(records, key=lambda item: (-item["score"], item["candidate_id"]))
    ranks = {item["candidate_id"]: index for index, item in enumerate(ranked, start=1)}
    for record in records:
        record["rank"] = ranks[record["candidate_id"]]
    return tuple(records), {
        "trace": tuple(trace),
        "execution": {
            "configured_event_budget": execution.configured_event_budget,
            "processed_event_count": execution.processed_event_count,
            "pending_event_count": execution.pending_event_count,
            "peak_queue_occupancy": execution.peak_queue_occupancy,
            "termination_reason": execution.termination_reason,
            "completed": execution.completed,
            "budget_exhausted": execution.budget_exhausted,
        },
        "observation_topology": tuple(
            (edge.source, edge.destination, float(edge.propagation_delay))
            for edge in topology.edges
        ),
    }


def _admit(config: CrossoverConfig, condition: Condition,
           records: tuple[dict[str, Any], ...], seed: int) -> dict[str, Any]:
    topology = BoundedTopology(
        config.candidate_ids + (config.target_id,), fan_in_limit=2, fan_out_limit=1,
        edge_capacity=1, routing_capacity=1,
    )
    local_neighbors = {candidate_id: (config.target_id,) for candidate_id in config.candidate_ids}
    controller = StructuralPlasticityController(
        topology, candidate_capacity=2, max_growth_per_adaptation=1,
        local_neighbors=local_neighbors,
    )
    by_id = {record["candidate_id"]: record for record in records}
    evidence = tuple(
        CandidateEvidence(
            record["candidate_id"], record["candidate_id"], config.target_id,
            record["admission_score"], config.candidate_propagation_delay,
            f"13b-{condition}-{record['candidate_id']}",
        )
        for record in records
    )
    candidate_set = tuple((item.source, item.destination) for item in evidence)
    if condition == "fixed":
        selected = None
        selected_result = {"status": "not_attempted", "reason": "fixed_topology"}
        rejected = tuple({"candidate": candidate, "status": "not_attempted",
                          "reason": "fixed_topology"} for candidate in candidate_set)
    else:
        selection_pool = list(evidence)
        if condition == "score_shuffled":
            shuffled_scores = [item.score for item in selection_pool]
            import random
            random.Random(seed).shuffle(shuffled_scores)
            selection_pool = [CandidateEvidence(item.observer, item.source, item.destination,
                                                score, item.propagation_delay, item.evidence_id)
                              for item, score in zip(selection_pool, shuffled_scores)]
        if condition == "random":
            import random
            selected = random.Random(seed).choice(selection_pool)
        else:
            selected = controller.select(selection_pool)
        selected_result_obj = controller.grow(selected) if selected is not None else None
        selected_result = {
            "status": selected_result_obj.status if selected_result_obj else "rejected",
            "reason": selected_result_obj.reason if selected_result_obj else "no_valid_candidate",
            "edge": (selected_result_obj.edge.source, selected_result_obj.edge.destination)
            if selected_result_obj and selected_result_obj.edge else None,
        }
        rejected_items = [item for item in evidence if selected is None or item.source != selected.source]
        rejected = []
        for item in rejected_items:
            result = controller.grow(item)
            rejected.append({"candidate": (item.source, item.destination),
                             "status": result.status, "reason": result.reason})
        rejected = tuple(rejected)
    selected_id = selected.source if condition != "fixed" and selected is not None else None
    selected_role = by_id[selected_id]["candidate_role"] if selected_id is not None else None
    for record in by_id.values():
        record["admitted"] = record["candidate_id"] == selected_id and selected_result["status"] == "grown"
    return {
        "candidate_set": candidate_set,
        "capacity_before": {"edge_count": 0, "edge_capacity": 1, "remaining_slots": 1,
                             "fan_in_target": 0, "fan_in_limit": 2,
                             "fan_out_by_candidate": {candidate_id: 0 for candidate_id in config.candidate_ids},
                             "fan_out_limit": 1},
        "projected_capacity": {"edge_count": 1, "edge_capacity": 1},
        "selected_candidate": selected_id,
        "selected_role": selected_role,
        "selected_result": selected_result,
        "rejected_candidates": rejected,
        "final_edges": tuple((edge.source, edge.destination, float(edge.propagation_delay)) for edge in controller.topology.edges),
        "graph_fingerprint": hashlib.sha256(repr(tuple(controller.topology.edges)).encode()).hexdigest(),
        "tie_rule": "score descending, then candidate identifier ascending",
    }


def run_condition(
    condition: Condition,
    *,
    config: CrossoverConfig = CrossoverConfig(),
    scoring_decay: float | None = None,
    seed: int = 0,
    mirror: bool = False,
    future_probe: bool = False,
) -> dict[str, Any]:
    """Run one bounded condition and return reconstructable evidence."""
    crossover = frozen_crossover(config)
    if scoring_decay is None:
        scoring_decay = {
            "decay_low": config.scoring_decay_low,
            "decay_high": config.scoring_decay_high,
            "decay_near": crossover["scoring_decay_crossover"],
            "ordinary": 0.0, "uniform": config.scoring_decay_high,
            "neutral": 0.0, "reversed": config.scoring_decay_high,
            "shuffled": config.scoring_decay_high, "random": config.scoring_decay_high,
            "score_shuffled": config.scoring_decay_high, "fixed": config.scoring_decay_high,
        }[condition]
    records, runtime = _run_observations(
        config, condition, scoring_decay, mirror=mirror, future_probe=future_probe,
    )
    for record in records:
        record["admission_score"] = record["score"]
    admission = _admit(config, condition, records, seed)
    ranked = sorted(records, key=lambda item: (-item["score"], item["candidate_id"]))
    return {
        "condition": condition,
        "seed": seed,
        "mirror": mirror,
        "fixture_id": config.fixture_id,
        "scoring_decay": scoring_decay,
        "execution_decay": config.execution_decay,
        "records": records,
        "candidate_scores": tuple((record["candidate_id"], record["score"]) for record in records),
        "ranked_candidates": tuple(record["candidate_id"] for record in ranked),
        "decision_timestamp": max((record["decision_timestamp"] for record in records), default=None),
        "runtime": runtime,
        "admission": admission,
        "crossover": crossover,
        "complete": runtime["execution"]["completed"],
        "future_probe": future_probe,
    }


def run_suite(*, config: CrossoverConfig = CrossoverConfig(), seed: int = 0) -> tuple[dict[str, Any], ...]:
    crossover = frozen_crossover(config)
    conditions: tuple[tuple[Condition, float | None], ...] = (
        ("decay_low", config.scoring_decay_low),
        ("decay_high", config.scoring_decay_high),
        ("decay_near", crossover["scoring_decay_crossover"]),
        ("ordinary", 0.0), ("reversed", config.scoring_decay_high),
        ("shuffled", config.scoring_decay_high), ("random", config.scoring_decay_high),
        ("score_shuffled", config.scoring_decay_high), ("fixed", config.scoring_decay_high),
        ("uniform", config.scoring_decay_high), ("neutral", 0.0),
    )
    results = [run_condition(condition, config=config, scoring_decay=decay, seed=seed)
               for condition, decay in conditions]
    results.extend((
        run_condition("decay_low", config=config, scoring_decay=config.scoring_decay_low,
                      seed=seed, mirror=False),
        run_condition("decay_low", config=config, scoring_decay=config.scoring_decay_low,
                      seed=seed, mirror=True),
    ))
    return tuple(results)


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


def write_artifacts(results: tuple[dict[str, Any], ...], output_dir: str, *,
                    baseline_revision: str, executed_revision: str,
                    config: CrossoverConfig = CrossoverConfig(),
                    tree_state: str = "clean before artifact generation") -> None:
    import os
    os.makedirs(output_dir, exist_ok=True)
    config = results[0]["crossover"]
    artifact = {
        "schema_version": "TPCN-LUNA-13B-1",
        "baseline_revision": baseline_revision,
        "executed_revision": executed_revision,
        "tree_state_at_execution": tree_state,
        "experiment": "Luna-13B causal local temporal structural crossover",
        "fixture_id": results[0]["fixture_id"],
        "configuration": asdict(config),
        "environment": {"python": sys.version, "platform": platform.platform()},
        "frozen_crossover": config,
        "deterministic_repetitions": True,
        "results": _jsonable(results),
    }
    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as handle:
        json.dump(artifact, handle, indent=2, sort_keys=True)
    summary = {
        result["condition"] + ("_mirror" if result["mirror"] else ""): {
            "ranked_candidates": result["ranked_candidates"],
            "selected_candidate": result["admission"]["selected_candidate"],
            "final_edges": result["admission"]["final_edges"],
            "completed": result["complete"],
        }
        for result in results
    }
    with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(_jsonable(summary), handle, indent=2, sort_keys=True)


__all__ = ["Condition", "CrossoverConfig", "frozen_crossover", "run_condition", "run_suite", "write_artifacts"]