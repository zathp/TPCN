"""Bounded structural observations of canonical excursion emissions."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import Iterable, Mapping

from .structural_plasticity import CandidateEvidence
from .temporal_association import TemporalAssociationPolicy


@dataclass(frozen=True, slots=True)
class StructuralEmissionObservation:
    observer: str
    emitter_id: str
    event_id: str | int
    timestamp: float


@dataclass(frozen=True, slots=True)
class StructuralObservationSnapshot:
    candidates: tuple[CandidateEvidence, ...]
    observations: tuple[StructuralEmissionObservation, ...]
    observation_count: int
    observation_work: int
    candidate_rejections: int
    candidate_rejection_reasons: tuple[tuple[str, int], ...]


class StructuralObservationPlane:
    """Dispatch actual emissions over a finite, explicitly declared fabric."""

    def __init__(
        self,
        nodes: Iterable[str],
        neighbors: Mapping[str, Iterable[str]],
        *,
        neighborhood_limit: int,
        reverse_observer_limit: int,
        history_capacity: int,
        candidate_capacity: int,
        association_window: float,
        maximum_score: int,
        propagation_delay: float,
    ) -> None:
        self.nodes = tuple(nodes)
        if not self.nodes or any(not isinstance(node, str) or not node for node in self.nodes):
            raise ValueError("nodes must contain non-empty strings")
        if len(set(self.nodes)) != len(self.nodes):
            raise ValueError("nodes must be unique")
        for value, name in (
            (neighborhood_limit, "neighborhood_limit"),
            (reverse_observer_limit, "reverse_observer_limit"),
            (history_capacity, "history_capacity"),
            (candidate_capacity, "candidate_capacity"),
            (maximum_score, "maximum_score"),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for value, name in (
            (association_window, "association_window"),
            (propagation_delay, "propagation_delay"),
        ):
            if (
                isinstance(value, bool)
                or not isinstance(value, Real)
                or not isfinite(float(value))
                or float(value) <= 0.0
            ):
                raise ValueError(f"{name} must be finite and positive")
        self.neighborhood_limit = neighborhood_limit
        self.reverse_observer_limit = reverse_observer_limit
        self.history_capacity = history_capacity
        self.candidate_capacity = candidate_capacity
        self.maximum_score = maximum_score
        self.association_window = float(association_window)
        self.propagation_delay = float(propagation_delay)
        self.neighbors = self._normalize_neighbors(neighbors)

        reverse: dict[str, list[str]] = {node: [] for node in self.nodes}
        for source in self.nodes:
            for emitter in self.neighbors[source]:
                reverse[emitter].append(source)
        self._reverse_observers = {
            emitter: tuple(sorted(sources)) for emitter, sources in reverse.items()
        }
        self._policies = {
            source: TemporalAssociationPolicy(
                (source, *self.neighbors[source]),
                history_capacity=history_capacity,
                candidate_capacity=candidate_capacity,
                association_window=self.association_window,
                maximum_score=maximum_score,
                propagation_delay=self.propagation_delay,
                local_neighbors={source: self.neighbors[source]},
            )
            for source in self.nodes
        }
        self._observations = {
            source: deque(maxlen=history_capacity) for source in self.nodes
        }
        self._observation_count = 0
        self._observation_work = 0
        self._frozen = False

    def observe_emission(
        self,
        emitter_id: str,
        event_id: str | int,
        timestamp: Real,
    ) -> None:
        if self._frozen:
            raise RuntimeError("structural evidence is frozen")
        if emitter_id not in self._policies:
            raise ValueError(f"unknown emission node: {emitter_id!r}")
        if isinstance(event_id, bool) or not isinstance(event_id, (str, int)):
            raise ValueError("event_id must be a string or integer")
        if isinstance(event_id, str) and not event_id:
            raise ValueError("event_id must be non-empty")
        if isinstance(timestamp, bool) or not isinstance(timestamp, Real) or not isfinite(float(timestamp)):
            raise ValueError("timestamp must be finite")
        observed_at = float(timestamp)
        recipients = (emitter_id, *self._reverse_observers[emitter_id])
        for observer in recipients:
            self._policies[observer].observe(observer, emitter_id, observed_at)
            self._observations[observer].append(
                StructuralEmissionObservation(observer, emitter_id, event_id, observed_at)
            )
        self._observation_count += 1
        self._observation_work += len(recipients)

    def freeze(self) -> StructuralObservationSnapshot:
        if self._frozen:
            raise RuntimeError("structural evidence is already frozen")
        self._frozen = True
        candidates = tuple(
            sorted(
                (
                    candidate
                    for policy in self._policies.values()
                    for candidate in policy.candidates
                ),
                key=lambda item: (
                    -float(item.score),
                    item.source,
                    item.destination,
                    item.evidence_id,
                ),
            )
        )
        rejection_reasons: dict[str, int] = {}
        candidate_rejections = 0
        observations = []
        for source in self.nodes:
            policy = self._policies[source]
            candidate_rejections += policy.candidate_rejections
            for reason, count in policy.candidate_rejection_reasons:
                rejection_reasons[reason] = rejection_reasons.get(reason, 0) + count
            observations.extend(self._observations[source])
        return StructuralObservationSnapshot(
            candidates,
            tuple(observations),
            self._observation_count,
            self._observation_work,
            candidate_rejections,
            tuple(sorted(rejection_reasons.items())),
        )

    def _normalize_neighbors(
        self,
        neighbors: Mapping[str, Iterable[str]],
    ) -> dict[str, tuple[str, ...]]:
        if not isinstance(neighbors, Mapping):
            raise TypeError("neighbors must be an explicit mapping")
        if set(neighbors) != set(self.nodes):
            raise ValueError("neighbors must explicitly declare every topology node")
        normalized: dict[str, tuple[str, ...]] = {}
        reverse_counts = {node: 0 for node in self.nodes}
        for source in self.nodes:
            entries = neighbors[source]
            if isinstance(entries, (str, bytes)):
                raise ValueError("neighbor lists must contain node IDs, not strings")
            destinations = tuple(entries)
            if len(destinations) != len(set(destinations)):
                raise ValueError(f"neighbors for {source!r} must be unique")
            if len(destinations) > self.neighborhood_limit:
                raise ValueError(f"neighborhood limit exceeded for {source!r}")
            if any(
                not isinstance(destination, str)
                or destination not in self.nodes
                or destination == source
                for destination in destinations
            ):
                raise ValueError("neighbors must be distinct non-self topology nodes")
            normalized[source] = tuple(sorted(destinations))
            for destination in destinations:
                reverse_counts[destination] += 1
                if reverse_counts[destination] > self.reverse_observer_limit:
                    raise ValueError(f"reverse-observer limit exceeded for {destination!r}")
        return normalized


__all__ = [
    "StructuralEmissionObservation",
    "StructuralObservationPlane",
    "StructuralObservationSnapshot",
]
