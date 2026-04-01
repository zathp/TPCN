from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class NeuronSpaceLayout:
    """Defines a neuron space and where IO endpoints live inside it."""

    n_neurons: int
    local_radius: int
    input_indices: torch.Tensor
    output_indices: torch.Tensor

    def effective_distance(self) -> int:
        if self.input_indices.numel() == 0 or self.output_indices.numel() == 0:
            return 0
        return max(0, int(self.output_indices[0].item() - self.input_indices[-1].item()))


def parse_index_spec(spec: str) -> list[int]:
    """Parses comma-separated integers and ranges like 1,3,8-12."""
    out: list[int] = []
    for part in spec.split(","):
        p = part.strip()
        if not p:
            continue
        if "-" in p:
            left, right = p.split("-", 1)
            start = int(left.strip())
            end = int(right.strip())
            step = 1 if end >= start else -1
            out.extend(list(range(start, end + step, step)))
            continue
        out.append(int(p))
    return out


def make_layout_from_indices(
    n_neurons: int,
    local_radius: int,
    input_indices: list[int] | torch.Tensor,
    output_indices: list[int] | torch.Tensor,
) -> NeuronSpaceLayout:
    in_idx = torch.as_tensor(input_indices, dtype=torch.long).flatten()
    out_idx = torch.as_tensor(output_indices, dtype=torch.long).flatten()

    if in_idx.numel() == 0:
        raise ValueError("input_indices cannot be empty")
    if out_idx.numel() == 0:
        raise ValueError("output_indices cannot be empty")

    if torch.any(in_idx < 0) or torch.any(in_idx >= n_neurons):
        raise ValueError("input_indices contains values out of [0, n_neurons)")
    if torch.any(out_idx < 0) or torch.any(out_idx >= n_neurons):
        raise ValueError("output_indices contains values out of [0, n_neurons)")

    if torch.unique(in_idx).numel() != in_idx.numel():
        raise ValueError("input_indices contains duplicates")
    if torch.unique(out_idx).numel() != out_idx.numel():
        raise ValueError("output_indices contains duplicates")

    in_idx = torch.sort(in_idx).values
    out_idx = torch.sort(out_idx).values

    return NeuronSpaceLayout(
        n_neurons=int(n_neurons),
        local_radius=max(0, int(local_radius)),
        input_indices=in_idx,
        output_indices=out_idx,
    )


def make_contiguous_layout(
    n_neurons: int,
    input_width: int,
    output_width: int,
    virtual_distance: int,
    local_radius: int,
) -> NeuronSpaceLayout:
    input_start = 0
    input_end = min(n_neurons, max(input_width, 1))

    requested_start = input_end + max(virtual_distance, 0)
    max_start = max(n_neurons - max(output_width, 1), 0)
    output_start = min(max(requested_start, 0), max_start)
    output_end = min(n_neurons, output_start + max(output_width, 1))

    input_idx = torch.arange(input_start, input_end, dtype=torch.long)
    output_idx = torch.arange(output_start, output_end, dtype=torch.long)
    if input_idx.numel() == 0 or output_idx.numel() == 0:
        raise ValueError("Could not create valid input/output neuron regions. Increase n-neurons or widths.")

    return NeuronSpaceLayout(
        n_neurons=int(n_neurons),
        local_radius=max(0, int(local_radius)),
        input_indices=input_idx,
        output_indices=output_idx,
    )


def build_local_recurrent_mask(n_neurons: int, local_radius: int, device: torch.device) -> torch.Tensor:
    idx = torch.arange(n_neurons, device=device)
    dist = torch.abs(idx[:, None] - idx[None, :])
    return (dist <= max(0, int(local_radius))).to(torch.float32)


def build_masks_for_layout(
    layout: NeuronSpaceLayout,
    signal_dim: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    mask_rec = build_local_recurrent_mask(layout.n_neurons, layout.local_radius, device)

    mask_in = torch.zeros((signal_dim, layout.n_neurons), device=device, dtype=torch.float32)
    mask_in[:, layout.input_indices.to(device)] = 1.0

    mask_out = torch.zeros((layout.n_neurons, signal_dim), device=device, dtype=torch.float32)
    mask_out[layout.output_indices.to(device), :] = 1.0

    return mask_rec, mask_in, mask_out


def linear_neuron_map(source_n: int, target_n: int, device: torch.device) -> torch.Tensor:
    """Maps each target neuron to the nearest source neuron index in linear space."""
    if target_n <= 0 or source_n <= 0:
        raise ValueError("source_n and target_n must both be positive")
    return torch.linspace(0, source_n - 1, target_n, device=device).round().long()