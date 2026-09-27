"""Downstream PyTorch snapshot adapter for the canonical TPCV format."""

from __future__ import annotations

from collections.abc import Sequence

import torch

from ..visualization import (
    ConnectionRecord,
    NeuronRecord,
    VisualizationSnapshot,
    export_snapshot,
)


class TorchSnapshotExporter:
    """Capture a detached GPU model view using the Luna-12 record format.

    The adapter performs no model mutation and has no execution-side state. A
    capture synchronizes only the requested tensors while exporting; disabled
    capture returns without touching them.
    """

    def __init__(
        self,
        *,
        enabled: bool = True,
        interval: int = 1,
        neuron_ids: Sequence[str] | None = None,
        propagation_delay: float = 1.0,
    ) -> None:
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be a boolean")
        if isinstance(interval, bool) or not isinstance(interval, int) or interval <= 0:
            raise ValueError("interval must be a positive integer")
        if propagation_delay < 0.0:
            raise ValueError("propagation_delay must be nonnegative")
        self.enabled = enabled
        self.interval = interval
        self.neuron_ids = tuple(neuron_ids) if neuron_ids is not None else None
        self.propagation_delay = float(propagation_delay)

    def capture(
        self,
        model: object,
        hidden_state: torch.Tensor,
        *,
        timestamp: float,
        epoch: int,
        processed_events: Sequence[int] | None = None,
        positions: Sequence[tuple[int, int] | None] | None = None,
        incomplete: bool = False,
    ) -> bytes | None:
        """Return one canonical record, or ``None`` outside a capture boundary."""
        if not self.enabled or epoch % self.interval:
            return None
        snapshot = self.snapshot(
            model,
            hidden_state,
            timestamp=timestamp,
            epoch=epoch,
            processed_events=processed_events,
            positions=positions,
            incomplete=incomplete,
        )
        return export_snapshot(snapshot)

    def snapshot(
        self,
        model: object,
        hidden_state: torch.Tensor,
        *,
        timestamp: float,
        epoch: int,
        processed_events: Sequence[int] | None = None,
        positions: Sequence[tuple[int, int] | None] | None = None,
        incomplete: bool = False,
    ) -> VisualizationSnapshot:
        if not isinstance(hidden_state, torch.Tensor) or hidden_state.ndim not in (1, 2):
            raise ValueError("hidden_state must be a one- or two-dimensional tensor")
        state = hidden_state.detach()[0] if hidden_state.ndim == 2 else hidden_state.detach()
        state = state.to(device="cpu", dtype=torch.float64)
        count = int(state.numel())
        ids = self.neuron_ids or tuple(f"n-{index}" for index in range(count))
        if len(ids) != count:
            raise ValueError("neuron_ids must match the hidden-state width")
        events = tuple(processed_events) if processed_events is not None else (0,) * count
        if len(events) != count:
            raise ValueError("processed_events must match the hidden-state width")
        coords = tuple(positions) if positions is not None else (None,) * count
        if len(coords) != count:
            raise ValueError("positions must match the hidden-state width")

        values = state.tolist()
        neurons = tuple(
            NeuronRecord(identifier, value != 0.0, value, value, int(event_count), position)
            for identifier, value, event_count, position in zip(ids, values, events, coords)
        )
        mask = getattr(model, "struct_mask_rec", None)
        if not isinstance(mask, torch.Tensor) or mask.ndim != 2 or mask.shape != (count, count):
            raise ValueError("model.struct_mask_rec must match the hidden-state width")
        edge_indices = (mask.detach() > 0.5).nonzero(as_tuple=False).to(device="cpu").tolist()
        connections = tuple(
            ConnectionRecord(ids[source], ids[destination], self.propagation_delay)
            for source, destination in edge_indices
        )
        return VisualizationSnapshot(timestamp, epoch, neurons, connections, incomplete)


__all__ = ["TorchSnapshotExporter"]