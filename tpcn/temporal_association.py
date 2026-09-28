"""Bounded source-local temporal association for structural experiments."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import Iterable, Mapping

from .structural_plasticity import CandidateEvidence


@dataclass(frozen=True, slots=True)
class TemporalAssociationState:
    """Bounded policy state exposed for experiment evidence."""

    observation_count: int
    history_count: int
    candidate_count: int
    candidate_capacity: int
    history_capacity: int
    maximum_score: int
    candidate_rejections: int
    candidate_rejection_reasons: tuple[tuple[str, int], ...]


class TemporalAssociationPolicy:
    """Turn source-local earlier/later observations into bounded candidates."""

    def __init__(
        self,
        nodes: Iterable[str],
        *,
        history_capacity: int = 8,
        candidate_capacity: int = 16,
        association_window: float = 8.0,
        maximum_score: int = 8,
        propagation_delay: float = 1.0,
        local_neighbors: Mapping[str, Iterable[str]] | None = None,
    ) -> None:
        node_list = tuple(nodes)
        if not node_list or any(not isinstance(node, str) or not node for node in node_list):
            raise ValueError("nodes must contain non-empty strings")
        if len(set(node_list)) != len(node_list):
            raise ValueError("nodes must be unique")
        for value, name in ((history_capacity, "history_capacity"),
                            (candidate_capacity, "candidate_capacity"),
                            (maximum_score, "maximum_score")):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for value, name in ((association_window, "association_window"),
                            (propagation_delay, "propagation_delay")):
            if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or float(value) <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        self.nodes = node_list
        self.history_capacity = history_capacity
        self.candidate_capacity = candidate_capacity
        self.association_window = float(association_window)
        self.maximum_score = maximum_score
        self.propagation_delay = float(propagation_delay)
        self._neighbors = self._normalize_neighbors(local_neighbors)
        self._history = {node: deque(maxlen=history_capacity) for node in node_list}
        self._scores: dict[tuple[str, str], int] = {}
        self._observation_count = 0
        self._candidate_rejections = 0
        self._candidate_rejection_reasons: dict[str, int] = {}

    @property
    def state(self) -> TemporalAssociationState:
        return TemporalAssociationState(
            self._observation_count,
            sum(len(items) for items in self._history.values()),
            len(self._scores),
            self.candidate_capacity,
            self.history_capacity,
            self.maximum_score,
            self._candidate_rejections,
            tuple(sorted(self._candidate_rejection_reasons.items())),
        )

    @property
    def candidates(self) -> tuple[CandidateEvidence, ...]:
        """Return all bounded candidates in deterministic score order."""
        return tuple(
            CandidateEvidence(
                source,
                source,
                destination,
                score,
                self.propagation_delay,
                f"temporal-{source}-{destination}-{score}",
            )
            for (source, destination), score in sorted(
                self._scores.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
            )
        )

    @property
    def candidate_rejections(self) -> int:
        return self._candidate_rejections

    @property
    def candidate_rejection_reasons(self) -> tuple[tuple[str, int], ...]:
        return tuple(sorted(self._candidate_rejection_reasons.items()))

    def observe(self, observer: str, node: str, timestamp: Real) -> None:
        """Record one locally available event and update one causal association."""
        self._validate_node(observer)
        self._validate_node(node)
        if isinstance(timestamp, bool) or not isinstance(timestamp, Real) or not isfinite(float(timestamp)):
            raise ValueError("timestamp must be finite")
        current_time = float(timestamp)
        history = self._history[observer]
        if history and current_time < history[-1][1]:
            raise ValueError("local observations must be monotonic")
        previous = next((item for item in reversed(history) if item[0] == observer), None)
        if previous is not None and node != observer:
            elapsed = current_time - previous[1]
            if 0.0 < elapsed <= self.association_window and self._is_local(observer, node):
                key = (observer, node)
                if key in self._scores:
                    self._scores[key] = min(self.maximum_score, self._scores[key] + 1)
                elif len(self._scores) < self.candidate_capacity:
                    self._scores[key] = 1
                else:
                    self._candidate_rejections += 1
                    self._candidate_rejection_reasons["candidate_capacity"] = (
                        self._candidate_rejection_reasons.get("candidate_capacity", 0) + 1
                    )
        history.append((node, current_time))
        self._observation_count += 1

    def reset(self) -> None:
        """Clear sequence-local evidence while preserving the declared policy bounds."""
        for history in self._history.values():
            history.clear()
        self._scores.clear()
        self._observation_count = 0
        self._candidate_rejections = 0
        self._candidate_rejection_reasons.clear()

    def _normalize_neighbors(self, neighbors: Mapping[str, Iterable[str]] | None) -> dict[str, frozenset[str]]:
        if neighbors is None:
            return {source: frozenset(destination for destination in self.nodes if destination != source)
                    for source in self.nodes}
        normalized: dict[str, frozenset[str]] = {}
        for source, destinations in neighbors.items():
            self._validate_node(source)
            destination_set = frozenset(destinations)
            if any(destination not in self.nodes or destination == source for destination in destination_set):
                raise ValueError("local neighbors must be distinct topology nodes")
            normalized[source] = destination_set
        return normalized

    def _is_local(self, source: str, destination: str) -> bool:
        return destination in self._neighbors.get(source, frozenset())

    def _validate_node(self, node: str) -> None:
        if node not in self.nodes:
            raise ValueError(f"unknown node: {node!r}")


__all__ = ["TemporalAssociationPolicy", "TemporalAssociationState"]