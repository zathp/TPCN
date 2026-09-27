"""Downstream PyTorch adapter for the canonical TPCV-1 snapshot format."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from .visualization import ConnectionRecord, NeuronRecord, VisualizationSnapshot, export_snapshot


class TorchSnapshotExporter:
    """Pull detached tensor observables without entering the computational path."""

    def __init__(self, *, enabled: bool = True, interval: int = 1) -> None:
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be a boolean")
        if isinstance(interval, bool) or not isinstance(interval, int) or interval <= 0:
            raise ValueError("interval must be a positive integer")
        self.enabled = enabled
        self.interval = interval

    def capture(
        self,
        state: object,
        activation: object,
        *,
        neuron_ids: Sequence[str],
        connections: Iterable[ConnectionRecord] = (),
        timestamp: float,
        epoch: int,
        processed_events: Sequence[int] | None = None,
    ) -> bytes | None:
        if not self.enabled or epoch % self.interval:
            return None
        state_values = _detached_values(state)
        activation_values = _detached_values(activation)
        if len(state_values) != len(neuron_ids) or len(activation_values) != len(neuron_ids):
            raise ValueError("tensor values and neuron_ids must have equal lengths")
        event_values = (0,) * len(neuron_ids) if processed_events is None else tuple(processed_events)
        if len(event_values) != len(neuron_ids):
            raise ValueError("processed_events and neuron_ids must have equal lengths")
        neurons = tuple(
            NeuronRecord(identifier, float(active) != 0.0, float(value), float(active), int(event_count))
            for identifier, value, active, event_count in zip(
                neuron_ids, state_values, activation_values, event_values
            )
        )
        snapshot = VisualizationSnapshot(
            timestamp=timestamp,
            epoch=epoch,
            neurons=neurons,
            connections=tuple(connections),
        )
        return export_snapshot(snapshot)


def _detached_values(value: object) -> tuple[float, ...]:
    """Read a tensor-like value through the standard detached CPU pull path."""
    detach = getattr(value, "detach", None)
    if detach is None:
        raise TypeError("state and activation must be tensor-like")
    cpu_values = detach().cpu().reshape(-1).tolist()
    return tuple(float(item) for item in cpu_values)


__all__ = ["TorchSnapshotExporter"]