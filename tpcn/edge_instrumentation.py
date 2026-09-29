"""Bounded downstream instrumentation for edge lifecycle and routed traffic."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math
from typing import Any


@dataclass(frozen=True, slots=True)
class EdgeIdentity:
    source: str
    destination: str
    generation: int


class EdgeInstrumentation:
    """Record bounded edge facts without participating in execution decisions."""

    schema_version = "TPCN-EDGE-2"

    def __init__(self, *, max_lifecycle_records: int = 256,
                 max_traffic_records: int = 512, counter_limit: int = 2**31 - 1) -> None:
        for value, name in ((max_lifecycle_records, "max_lifecycle_records"),
                            (max_traffic_records, "max_traffic_records"),
                            (counter_limit, "counter_limit")):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        self.max_lifecycle_records = max_lifecycle_records
        self.max_traffic_records = max_traffic_records
        self.counter_limit = counter_limit
        self._generations: dict[tuple[str, str], int] = {}
        self._active: dict[tuple[str, str], EdgeIdentity] = {}
        self._stats: dict[EdgeIdentity, dict[str, Any]] = {}
        self._lifecycle: deque[dict[str, Any]] = deque(maxlen=max_lifecycle_records)
        self._traffic: deque[dict[str, Any]] = deque(maxlen=max_traffic_records)
        self._phase = "UNSCOPED"

    def set_phase(self, phase: str) -> None:
        if not isinstance(phase, str) or not phase:
            raise ValueError("phase must be a non-empty string")
        self._phase = phase

    def register_edge(self, edge: Any, *, timestamp: float | None = None,
                      reason: str = "existing") -> EdgeIdentity:
        key = (edge.source, edge.destination)
        if key in self._active:
            return self._active[key]
        generation = self._generations.get(key, -1) + 1
        identity = EdgeIdentity(edge.source, edge.destination, generation)
        self._generations[key] = generation
        self._active[key] = identity
        self._stats.setdefault(identity, {
            "identity": self._identity(identity), "delay": float(edge.propagation_delay),
            "routing_cost": int(edge.routing_cost), "created_at": None if timestamp is None else float(timestamp),
            "created_at_domain": "unavailable" if timestamp is None else "event_timestamp",
            "first_use": None, "last_use": None, "traffic_count": 0,
            "traffic_by_phase": {},
        })
        self._lifecycle.append({"kind": "edge_created", "timestamp": None if timestamp is None else float(timestamp),
                                "timestamp_domain": "unavailable" if timestamp is None else "event_timestamp",
                                "identity": self._identity(identity), "reason": reason})
        return identity

    def candidate(self, evidence: Any, *, timestamp: float | None = None, status: str = "proposed",
                  reason: str | None = None) -> None:
        self._lifecycle.append({"kind": f"candidate_{status}",
                                "timestamp": None if timestamp is None else float(timestamp),
                                "timestamp_domain": "unavailable" if timestamp is None else "event_timestamp",
                                "phase": self._phase, "source": getattr(evidence, "source", None),
                                "destination": getattr(evidence, "destination", None),
                                "delay": None if evidence is None else float(evidence.propagation_delay),
                                "reason": reason})

    def record_candidate_proposed(self, evidence: Any, *, timestamp: float | None = None) -> None:
        self.candidate(evidence, timestamp=timestamp, status="proposed")

    def mutation(self, result: Any, *, timestamp: float | None = None, edge: Any = None,
                 reason: str | None = None, evidence: Any = None) -> None:
        if result.status == "grown" and edge is not None:
            self.register_edge(edge, timestamp=timestamp, reason=reason or "growth")
        elif result.status == "pruned" and edge is not None:
            identity = self._active.pop((edge.source, edge.destination), None)
            if identity is not None:
                self._lifecycle.append({"kind": "edge_pruned", "timestamp": None if timestamp is None else float(timestamp),
                                        "timestamp_domain": "unavailable" if timestamp is None else "event_timestamp",
                                        "identity": self._identity(identity), "reason": reason or "pruned"})
        elif result.status != "grown":
            self.candidate(evidence, timestamp=timestamp, status="rejected",
                           reason=reason or getattr(result, "reason", None) or result.status)

    def record_route(self, edge: Any, event: Any, routed_event: Any) -> EdgeIdentity:
        identity = self.register_edge(edge, timestamp=event.timestamp)
        stats = self._stats[identity]
        if stats["traffic_count"] < self.counter_limit:
            stats["traffic_count"] += 1
        phase_counts = stats["traffic_by_phase"]
        phase_counts[self._phase] = min(self.counter_limit, phase_counts.get(self._phase, 0) + 1)
        if stats["first_use"] is None:
            stats["first_use"] = float(event.timestamp)
        stats["last_use"] = float(event.timestamp)
        self._traffic.append({"identity": self._identity(identity), "phase": self._phase,
                      "event_type": str(event.event_type),
                              "emission_timestamp": float(event.timestamp),
                              "arrival_timestamp": float(routed_event.timestamp)})
        return identity

    def route_traffic(self, route: tuple[tuple[str, str], ...], phase: str) -> int:
        return self.measured_route_traffic(self._traffic, route, phase)

    @staticmethod
    def measured_route_traffic(traffic: Any, route: tuple[tuple[str, str], ...], phase: str) -> int:
        counts = []
        for source, destination in route:
            counts.append(sum(1 for record in traffic
                              if record.get("phase") == phase
                              and record["identity"]["source"] == source
                              and record["identity"]["destination"] == destination))
        return min(counts) if counts else 0

    def decay_context(self, *, neuron: str, timestamp: float, delta_t: float,
                      decay_rate: float, pre_state: float, residual_state: float,
                      post_state: float) -> None:
        self._lifecycle.append({"kind": "decay_context", "neuron": neuron,
                                "timestamp": float(timestamp), "delta_t": float(delta_t),
                                "decay_rate": float(decay_rate), "pre_state": float(pre_state),
                                "residual_state": float(residual_state), "post_state": float(post_state),
                                "decay_factor": math.exp(-float(decay_rate) * float(delta_t))})

    def snapshot(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version,
                "edges": [dict(value) for value in self._stats.values()],
                "lifecycle": list(self._lifecycle), "traffic": list(self._traffic),
                "bounds": {"max_lifecycle_records": self.max_lifecycle_records,
                            "max_traffic_records": self.max_traffic_records,
                            "counter_limit": self.counter_limit,
                            "overflow": "counter saturates; records use bounded ring buffers"},
                "audit": {"persistent_edge_strength": "not present",
                          "persistent_edge_utility": "not present",
                          "persistent_edge_eligibility": "not present",
                          "usage_score": "derived diagnostic: traffic_count"}}

    @staticmethod
    def _identity(identity: EdgeIdentity) -> dict[str, Any]:
        return {"source": identity.source, "destination": identity.destination,
                "generation": identity.generation}


def run_competing_path_fixture(*, instrument: bool = True, seed: int = 12) -> dict[str, Any]:
    """Run a deterministic old-route/shortcut lifecycle fixture."""
    from .canonical_neuron import TPCNNeuron
    from .event_runtime import Event, EventQueue
    from .structural_plasticity import CandidateEvidence, StructuralPlasticityController
    from .topology import BoundedTopology

    observer = EdgeInstrumentation(max_lifecycle_records=64, max_traffic_records=128,
                                   counter_limit=31) if instrument else None
    topology = BoundedTopology.from_edges(
        ("source", "mid", "target"),
        (("source", "mid", 1.0), ("mid", "target", 1.0)),
        fan_in_limit=2, fan_out_limit=2, edge_capacity=3, routing_capacity=3,
    )
    controller = StructuralPlasticityController(
        topology, candidate_capacity=2, max_growth_per_adaptation=1,
        local_neighbors={"source": ("target",)}, observer=observer,
    )
    decay_records: list[dict[str, float | str]] = []

    def record_decay(context: dict[str, float | str]) -> None:
        decay_records.append(context)
        if observer is not None:
            observer.decay_context(**context)

    neurons = {node: TPCNNeuron(node, decay_rate=0.5, temporal_context_hook=record_decay)
               for node in topology.nodes}

    def replay(label: str) -> tuple[tuple[str, ...], str]:
        if observer is not None:
            observer.set_phase({"before": "PRE_SHORTCUT", "after": "POST_SHORTCUT",
                                "removed": "POST_REMOVAL"}[label])
        for neuron in neurons.values():
            neuron.reset()
        queue: EventQueue[Event] = EventQueue(16)
        paths: dict[int, tuple[str, ...]] = {}
        trace: list[str] = []
        queued = queue.push(Event(0.0, "source", "source", "signal", 1.0))
        paths[queued.sequence] = ("source",)
        while queue:
            pending = queue.peek()
            assert pending is not None
            event = queue.pop_ready(pending.timestamp)
            path = paths.pop(event.sequence)
            neurons[event.destination].receive_event(event)
            trace.append(f"{label}:{event.timestamp}:{event.source}>{event.destination}")
            current_topology = controller.topology
            if event.destination in current_topology.nodes and event.destination not in path[:-1]:
                emitted = Event(event.timestamp, event.destination, event.destination, event.event_type,
                                neurons[event.destination].activation)
                routed = current_topology.route(emitted, queue, observer=observer)
                for routed_event in routed:
                    paths[routed_event.sequence] = path + (routed_event.destination,)
        return tuple(trace), __import__("hashlib").sha256(repr(trace).encode()).hexdigest()

    before_trace, before_digest = replay("before")
    shortcut = CandidateEvidence("source", "source", "target", 2.0, 0.5, f"fixture-{seed}")
    rejected = CandidateEvidence("source", "source", "mid", 1.0, 1.0, f"reject-{seed}")
    accepted = controller.grow(shortcut)
    duplicate_result = controller.grow(
        CandidateEvidence("source", "source", "target", 2.0, 0.5, f"duplicate-{seed}")
    )
    rejected_result = controller.grow(rejected)
    after_trace, after_digest = replay("after")
    pruned = controller.prune("source", "target")
    removed_trace, removed_digest = replay("removed")

    rejection_results: dict[str, str | None] = {
        "duplicate": duplicate_result.reason or duplicate_result.status,
    }
    if observer is not None:
        fan_topology = BoundedTopology.from_edges(
            ("fan_source", "fan_left", "fan_right", "fan_target"),
            (("fan_source", "fan_left", 1.0), ("fan_right", "fan_target", 1.0)),
            fan_in_limit=1, fan_out_limit=1, edge_capacity=3, routing_capacity=3,
        )
        fan_controller = StructuralPlasticityController(
            fan_topology,
            local_neighbors={"fan_source": ("fan_right",), "fan_left": ("fan_target",)},
            observer=observer,
        )
        fan_out_result = fan_controller.grow(
            CandidateEvidence("fan_source", "fan_source", "fan_right", 1.0, 1.0, f"fan-out-{seed}")
        )
        fan_in_result = fan_controller.grow(
            CandidateEvidence("fan_left", "fan_left", "fan_target", 1.0, 1.0, f"fan-in-{seed}")
        )
        rejection_results.update({
            "fan_in_full": fan_in_result.reason or fan_in_result.status,
            "fan_out_full": fan_out_result.reason or fan_out_result.status,
        })

        capacity_topology = BoundedTopology.from_edges(
            ("capacity_source", "capacity_existing", "capacity_target"),
            (("capacity_source", "capacity_existing", 1.0),),
            fan_in_limit=2, fan_out_limit=2, edge_capacity=1, routing_capacity=2,
        )
        capacity_controller = StructuralPlasticityController(
            capacity_topology,
            local_neighbors={"capacity_source": ("capacity_target",)},
            observer=observer,
        )
        capacity_result = capacity_controller.grow(
            CandidateEvidence("capacity_source", "capacity_source", "capacity_target", 1.0, 1.0, f"capacity-{seed}")
        )
        rejection_results["edge_capacity"] = capacity_result.reason or capacity_result.status

        candidate_topology = BoundedTopology(
            ("candidate_source", "candidate_left", "candidate_right"),
            fan_in_limit=2, fan_out_limit=2, edge_capacity=3, routing_capacity=2,
        )
        candidate_controller = StructuralPlasticityController(
            candidate_topology, candidate_capacity=1,
            local_neighbors={"candidate_source": ("candidate_left", "candidate_right")},
            observer=observer,
        )
        candidate_controller.submit(CandidateEvidence(
            "candidate_source", "candidate_source", "candidate_left", 1.0, 1.0, f"candidate-a-{seed}"
        ))
        candidate_result = candidate_controller.grow(CandidateEvidence(
            "candidate_source", "candidate_source", "candidate_right", 1.0, 1.0, f"candidate-b-{seed}"
        ))
        rejection_results["candidate_capacity"] = candidate_result.reason or candidate_result.status
    artifact = observer.snapshot() if observer is not None else {"schema_version": "disabled"}
    artifact.update({"run": {"seed": seed, "instrumentation": instrument},
                     "traces": {"before": before_trace, "after": after_trace, "removed": removed_trace},
                     "digests": {"before": before_digest, "after": after_digest, "removed": removed_digest},
                     "mutations": {"accepted": accepted.status, "rejected": rejected_result.reason,
                                    "pruned": pruned.status},
                     "rejection_results": rejection_results,
                     "decay_context": decay_records,
                     "phases": ["PRE_SHORTCUT", "POST_SHORTCUT", "POST_REMOVAL"],
                     "analysis": {"old_route_before": observer.route_traffic(
                                      (("source", "mid"), ("mid", "target")), "PRE_SHORTCUT") if observer else None,
                                  "old_route_after": observer.route_traffic(
                                      (("source", "mid"), ("mid", "target")), "POST_SHORTCUT") if observer else None,
                                  "shortcut_after": observer.route_traffic(
                                      (("source", "target"),), "POST_SHORTCUT") if observer else None,
                                  "old_route_after_removal": observer.route_traffic(
                                      (("source", "mid"), ("mid", "target")), "POST_REMOVAL") if observer else None,
                                  "shortcut_used": after_digest != before_digest,
                                  "persistent_edge_strength": "not available in current architecture",
                                  "persistent_edge_utility": "not available in current architecture"}})
    return artifact


__all__ = ["EdgeIdentity", "EdgeInstrumentation", "run_competing_path_fixture"]