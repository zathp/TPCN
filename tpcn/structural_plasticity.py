"""Bounded, local structural adaptation over :mod:`tpcn.topology`."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import Iterable, Mapping

from .topology import BoundedTopology, Edge, TopologyCapacityError, TopologyError


@dataclass(frozen=True, slots=True)
class CandidateEvidence:
    """One locally observed proposal for a directed connection."""

    observer: str
    source: str
    destination: str
    score: Real
    propagation_delay: Real
    evidence_id: str = ""

    def __post_init__(self) -> None:
        if not all(isinstance(value, str) and value for value in (self.observer, self.source, self.destination)):
            raise ValueError("candidate nodes must be non-empty strings")
        if self.source == self.destination:
            raise ValueError("candidate connections must be directed between distinct nodes")
        if not isinstance(self.evidence_id, str):
            raise TypeError("evidence_id must be a string")
        for value, name in ((self.score, "score"), (self.propagation_delay, "propagation_delay")):
            if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
                raise ValueError(f"{name} must be finite")
        if float(self.propagation_delay) <= 0.0:
            raise ValueError("propagation_delay must be positive")


@dataclass(frozen=True, slots=True)
class MutationResult:
    """Inspectable outcome of a single structural mutation."""

    status: str
    edge: Edge | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class PlasticityState:
    """Bounded state exposed for replay and resource inspection."""

    edge_count: int
    edge_capacity: int
    routing_capacity: int
    candidate_count: int
    candidate_capacity: int
    fan_in_limit: int
    fan_out_limit: int
    max_growth_per_adaptation: int
    minimum_edge_count: int


class StructuralPlasticityController:
    """Apply source-local candidate evidence to a finite public topology."""

    def __init__(
        self,
        topology: BoundedTopology,
        *,
        candidate_capacity: int = 32,
        max_growth_per_adaptation: int = 1,
        minimum_edge_count: int = 0,
        local_neighbors: Mapping[str, Iterable[str]] | None = None,
        observer: object | None = None,
    ) -> None:
        if not isinstance(topology, BoundedTopology):
            raise TypeError("topology must be a BoundedTopology")
        if isinstance(candidate_capacity, bool) or not isinstance(candidate_capacity, int) or candidate_capacity <= 0:
            raise ValueError("candidate_capacity must be a positive integer")
        if isinstance(max_growth_per_adaptation, bool) or not isinstance(max_growth_per_adaptation, int) or max_growth_per_adaptation <= 0:
            raise ValueError("max_growth_per_adaptation must be a positive integer")
        if isinstance(minimum_edge_count, bool) or not isinstance(minimum_edge_count, int) or minimum_edge_count < 0:
            raise ValueError("minimum_edge_count must be a nonnegative integer")
        if minimum_edge_count > len(topology):
            raise ValueError("minimum_edge_count cannot exceed the initial edge count")
        self.topology = topology
        self.candidate_capacity = candidate_capacity
        self.max_growth_per_adaptation = max_growth_per_adaptation
        self.minimum_edge_count = minimum_edge_count
        self._local_neighbors = self._normalize_neighbors(local_neighbors)
        self._candidates: dict[tuple[str, str], CandidateEvidence] = {}
        self.observer = observer
        if observer is not None:
            for edge in topology.edges:
                observer.register_edge(edge)

    @property
    def state(self) -> PlasticityState:
        return PlasticityState(
            edge_count=len(self.topology),
            edge_capacity=self.topology.edge_capacity,
            routing_capacity=self.topology.routing_capacity,
            candidate_count=len(self._candidates),
            candidate_capacity=self.candidate_capacity,
            fan_in_limit=self.topology.fan_in_limit,
            fan_out_limit=self.topology.fan_out_limit,
            max_growth_per_adaptation=self.max_growth_per_adaptation,
            minimum_edge_count=self.minimum_edge_count,
        )

    @property
    def candidates(self) -> tuple[CandidateEvidence, ...]:
        """Return the bounded pending evidence in deterministic order."""
        return tuple(self._candidates[key] for key in sorted(self._candidates))

    def submit(self, evidence: CandidateEvidence) -> MutationResult:
        """Record one bounded proposal after checking its local provenance."""
        self._validate_evidence(evidence)
        if self.observer is not None:
            self.observer.record_candidate_proposed(evidence)
        if not self._is_local(evidence):
            if self.observer is not None:
                self.observer.candidate(evidence, status="rejected", reason="nonlocal")
            return MutationResult("rejected", reason="nonlocal")
        key = (evidence.source, evidence.destination)
        if key in self._candidates:
            if self.observer is not None:
                self.observer.candidate(evidence, status="rejected", reason="duplicate")
            return MutationResult("duplicate")
        if key in {(edge.source, edge.destination) for edge in self.topology.edges}:
            if self.observer is not None:
                self.observer.candidate(evidence, status="rejected", reason="duplicate")
            return MutationResult("duplicate", self.topology.edge(*key))
        if len(self._candidates) >= self.candidate_capacity:
            if self.observer is not None:
                self.observer.candidate(evidence, status="rejected", reason="candidate_capacity")
            return MutationResult("full_capacity", reason="candidate_capacity")
        self._candidates[key] = evidence
        if self.observer is not None:
            self.observer.candidate(evidence, status="considered")
        return MutationResult("accepted")

    def select(self, candidates: Iterable[CandidateEvidence]) -> CandidateEvidence | None:
        """Select one candidate without searching topology-wide alternatives."""
        bounded = tuple(candidates)
        if len(bounded) > self.candidate_capacity:
            raise ValueError("candidate batch exceeds candidate_capacity")
        for evidence in bounded:
            self._validate_evidence(evidence)
        local = tuple(evidence for evidence in bounded if self._is_local(evidence))
        return min(local, key=self._candidate_key) if local else None

    def grow(self, evidence: CandidateEvidence) -> MutationResult:
        """Admit and apply one candidate using only public topology operations."""
        result = self.submit(evidence)
        if result.status != "accepted":
            return result
        result = self._commit_growth((evidence,))
        self._candidates.pop((evidence.source, evidence.destination), None)
        if self.observer is not None:
            self.observer.mutation(result, edge=result.edge, reason=result.reason, evidence=evidence)
        return result

    def adapt(self, candidates: Iterable[CandidateEvidence]) -> MutationResult:
        """Select and grow at most one locally evidenced connection."""
        selected = self.select(candidates)
        return MutationResult("rejected", reason="no_valid_candidate") if selected is None else self.grow(selected)

    def adapt_many(
        self,
        candidates: Iterable[CandidateEvidence],
        *,
        maximum: int | None = None,
    ) -> tuple[MutationResult, ...]:
        """Atomically grow a deterministic, bounded set of local candidates."""
        bounded = tuple(candidates)
        if len(bounded) > self.candidate_capacity:
            raise ValueError("candidate batch exceeds candidate_capacity")
        for evidence in bounded:
            self._validate_evidence(evidence)
        unique: dict[tuple[str, str], CandidateEvidence] = {}
        for item in bounded:
            if not self._is_local(item):
                continue
            key = (item.source, item.destination)
            current = unique.get(key)
            if current is None or self._candidate_key(item) < self._candidate_key(current):
                unique[key] = item
        limit = self.max_growth_per_adaptation if maximum is None else maximum
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError("maximum must be a positive integer")
        selected = tuple(sorted(unique.values(), key=self._candidate_key)[:limit])
        if not selected:
            return ()
        result = self._commit_growth(selected)
        if result.status != "grown":
            if self.observer is not None:
                for evidence in selected:
                    self.observer.mutation(result, reason=result.reason, evidence=evidence)
            return tuple(MutationResult(result.status) for _ in selected)
        selected_keys = {(item.source, item.destination) for item in selected}
        grown = tuple(MutationResult("grown", edge) for edge in self.topology.edges
                       if (edge.source, edge.destination) in selected_keys)
        if self.observer is not None:
            for mutation in grown:
                self.observer.mutation(mutation, edge=mutation.edge, reason="growth")
        return grown

    def prune(self, source: str, destination: str) -> MutationResult:
        """Remove an edge while leaving already queued in-flight events untouched."""
        if len(self.topology) <= self.minimum_edge_count:
            return MutationResult("retention_limit")
        try:
            removed = self.topology.edge(source, destination)
        except TopologyError:
            return MutationResult("rejected")
        remaining = tuple(
            (edge.source, edge.destination, edge.propagation_delay)
            for edge in self.topology.edges
            if (edge.source, edge.destination) != (source, destination)
        )
        self.topology = BoundedTopology.from_edges(
            self.topology.nodes,
            remaining,
            fan_in_limit=self.topology.fan_in_limit,
            fan_out_limit=self.topology.fan_out_limit,
            edge_capacity=self.topology.edge_capacity,
            routing_capacity=self.topology.routing_capacity,
        )
        self._candidates.pop((source, destination), None)
        if self.observer is not None:
            self.observer.mutation(MutationResult("pruned", removed), edge=removed)
        return MutationResult("pruned", removed)

    def prune_by_score(
        self,
        scores: Mapping[tuple[str, str], Real],
        *,
        maximum: int = 1,
    ) -> tuple[MutationResult, ...]:
        """Prune the lowest locally supplied edge scores with stable ties."""
        if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
            raise ValueError("maximum must be a positive integer")
        eligible = []
        for edge in self.topology.edges:
            score = scores.get((edge.source, edge.destination))
            if score is None or isinstance(score, bool) or not isinstance(score, Real) or not isfinite(float(score)):
                continue
            eligible.append((float(score), edge.source, edge.destination))
        eligible.sort()
        results = []
        for _, source, destination in eligible[:maximum]:
            result = self.prune(source, destination)
            if result.status == "pruned":
                results.append(result)
        return tuple(results)

    def _validate_evidence(self, evidence: CandidateEvidence) -> None:
        if not isinstance(evidence, CandidateEvidence):
            raise TypeError("evidence must be CandidateEvidence")
        if evidence.observer != evidence.source:
            raise ValueError("candidate evidence must be observed at its source")
        if evidence.source not in self.topology.nodes or evidence.destination not in self.topology.nodes:
            raise TopologyError("candidate endpoints must belong to the topology")

    def _normalize_neighbors(self, neighbors: Mapping[str, Iterable[str]] | None) -> dict[str, frozenset[str]]:
        if neighbors is None:
            return {}
        normalized = {}
        for source, destinations in neighbors.items():
            if source not in self.topology.nodes:
                raise TopologyError("locality source must belong to the topology")
            destination_set = frozenset(destinations)
            if any(destination not in self.topology.nodes for destination in destination_set):
                raise TopologyError("locality destination must belong to the topology")
            normalized[source] = destination_set
        return normalized

    def _is_local(self, evidence: CandidateEvidence) -> bool:
        return not self._local_neighbors or evidence.destination in self._local_neighbors.get(evidence.source, frozenset())

    @staticmethod
    def _candidate_key(evidence: CandidateEvidence) -> tuple[float, str, str, str]:
        return (-float(evidence.score), evidence.source, evidence.destination, evidence.evidence_id)

    def _commit_growth(self, evidence: tuple[CandidateEvidence, ...]) -> MutationResult:
        existing = {(edge.source, edge.destination) for edge in self.topology.edges}
        if any((item.source, item.destination) in existing for item in evidence):
            return MutationResult("duplicate", reason="duplicate")
        if len(self.topology) + len(evidence) > self.topology.edge_capacity:
            return MutationResult("full_capacity", reason="edge_capacity")
        try:
            replacement = BoundedTopology.from_edges(
                self.topology.nodes,
                tuple((edge.source, edge.destination, edge.propagation_delay) for edge in self.topology.edges)
                + tuple((item.source, item.destination, item.propagation_delay) for item in evidence),
                fan_in_limit=self.topology.fan_in_limit,
                fan_out_limit=self.topology.fan_out_limit,
                edge_capacity=self.topology.edge_capacity,
                routing_capacity=self.topology.routing_capacity,
            )
        except TopologyCapacityError:
            if len(self.topology) + len(evidence) > self.topology.edge_capacity:
                reason = "edge_capacity"
            elif any(sum(edge.destination == item.destination for edge in self.topology.edges) >= self.topology.fan_in_limit
                     for item in evidence):
                reason = "fan_in_full"
            elif any(sum(edge.source == item.source for edge in self.topology.edges) >= self.topology.fan_out_limit
                     for item in evidence):
                reason = "fan_out_full"
            else:
                reason = "capacity"
            return MutationResult("full_capacity", reason=reason)
        except TopologyError:
            return MutationResult("rejected", reason="invalid_candidate")
        self.topology = replacement
        return MutationResult("grown", replacement.edge(evidence[0].source, evidence[0].destination))


__all__ = ["CandidateEvidence", "MutationResult", "PlasticityState", "StructuralPlasticityController"]