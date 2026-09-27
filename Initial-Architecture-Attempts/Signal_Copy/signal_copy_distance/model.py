from __future__ import annotations

import torch
from torch import nn

from .config import SignalCopyConfig
from .space import (
    NeuronSpaceLayout,
    build_local_recurrent_mask as build_local_recurrent_mask_from_space,
    build_masks_for_layout,
    linear_neuron_map,
    make_contiguous_layout,
)


def build_input_output_indices(cfg: SignalCopyConfig) -> tuple[torch.Tensor, torch.Tensor, int]:
    layout = make_contiguous_layout(
        n_neurons=cfg.n_neurons,
        input_width=cfg.input_width,
        output_width=cfg.output_width,
        virtual_distance=cfg.virtual_distance,
        local_radius=cfg.local_radius,
    )
    return layout.input_indices, layout.output_indices, layout.effective_distance()


def build_local_recurrent_mask(n_neurons: int, local_radius: int, device: torch.device) -> torch.Tensor:
    return build_local_recurrent_mask_from_space(n_neurons=n_neurons, local_radius=local_radius, device=device)


class DistanceSignalCopyNet(nn.Module):
    """Local recurrent field with region-constrained IO endpoints."""

    def __init__(
        self,
        signal_dim: int,
        n_neurons: int,
        alpha: float,
        mask_rec: torch.Tensor,
        mask_in: torch.Tensor,
        mask_out: torch.Tensor,
        struct_mask_rec: torch.Tensor,
    ) -> None:
        super().__init__()
        self.signal_dim = int(signal_dim)
        self.n_neurons = int(n_neurons)
        self.alpha = float(alpha)

        self.w_in = nn.Parameter(torch.empty(self.signal_dim, self.n_neurons))
        self.w_rec = nn.Parameter(torch.empty(self.n_neurons, self.n_neurons))
        self.w_out = nn.Parameter(torch.empty(self.n_neurons, self.signal_dim))

        param_device = self.w_in.device

        self.register_buffer("mask_rec", mask_rec.to(device=param_device, dtype=torch.float32))
        self.register_buffer("mask_in", mask_in.to(device=param_device, dtype=torch.float32))
        self.register_buffer("mask_out", mask_out.to(device=param_device, dtype=torch.float32))
        self.register_buffer("struct_mask_rec", struct_mask_rec.to(device=param_device, dtype=torch.float32))

        self.reset_parameters()

    def reset_parameters(self) -> None:
        nn.init.xavier_uniform_(self.w_in)
        nn.init.xavier_uniform_(self.w_rec)
        nn.init.xavier_uniform_(self.w_out)
        with torch.no_grad():
            self.w_in.mul_(self.mask_in)
            self.w_rec.mul_(self.mask_rec * self.struct_mask_rec)
            self.w_out.mul_(self.mask_out)

    def enforce_masks_(self) -> None:
        with torch.no_grad():
            self.w_in.mul_(self.mask_in)
            self.w_rec.mul_(self.mask_rec * self.struct_mask_rec)
            self.w_out.mul_(self.mask_out)

    def recurrent_edge_count(self) -> int:
        return int((self.struct_mask_rec > 0.5).sum().item())

    def recurrent_edge_capacity(self) -> int:
        return int((self.mask_rec > 0.5).sum().item())

    def grow_recurrent_edges_from_lagcorr(
        self,
        h_means: torch.Tensor,
        growth_rate: float,
        max_new_edges: int,
        candidate_multiplier: int,
        min_corr_for_growth: float,
        local_radius: int,
    ) -> int:
        if max_new_edges <= 0:
            return 0
        if h_means.ndim != 2 or h_means.shape[0] < 3:
            return 0

        with torch.no_grad():
            n = int(self.n_neurons)
            k = int(max_new_edges * max(1, candidate_multiplier))
            if k <= 0:
                return 0

            i = torch.randint(0, n, size=(k,), device=h_means.device)
            offsets = torch.randint(-max(0, local_radius), max(0, local_radius) + 1, size=(k,), device=h_means.device)
            j = i + offsets
            valid = (j >= 0) & (j < n)

            if not torch.any(valid):
                return 0

            i = i[valid]
            j = j[valid]
            lin = i * n + j
            lin = torch.unique(lin)
            i = lin // n
            j = lin % n

            allowed = self.mask_rec[i, j] > 0.5
            absent = self.struct_mask_rec[i, j] < 0.5
            valid = allowed & absent
            if not torch.any(valid):
                return 0

            i = i[valid]
            j = j[valid]

            x = h_means[:-1, i]
            y = h_means[1:, j]
            x = x - x.mean(dim=0, keepdim=True)
            y = y - y.mean(dim=0, keepdim=True)
            x_std = torch.sqrt((x * x).mean(dim=0) + 1e-8)
            y_std = torch.sqrt((y * y).mean(dim=0) + 1e-8)
            corr = (x * y).mean(dim=0) / (x_std * y_std + 1e-8)

            corr_pos = torch.clamp(corr, min=0.0)
            if min_corr_for_growth > 0.0:
                corr_pos = torch.where(corr_pos >= float(min_corr_for_growth), corr_pos, torch.zeros_like(corr_pos))

            if not torch.any(corr_pos > 0):
                return 0

            in_degree = self.struct_mask_rec.sum(dim=0)
            max_in = in_degree.max().clamp(min=1.0)
            vacancy_all = 1.0 - (in_degree / max_in)
            vacancy_j = vacancy_all[j]

            p = torch.clamp(float(growth_rate) * corr_pos * (0.5 + 0.5 * vacancy_j), min=0.0, max=1.0)
            grow = torch.rand_like(p) < p
            if not torch.any(grow):
                return 0

            i_sel = i[grow]
            j_sel = j[grow]
            c_sel = corr_pos[grow]
            v_sel = vacancy_j[grow]
            score_sel = c_sel * (0.5 + 0.5 * v_sel)

            if i_sel.numel() > max_new_edges:
                top_idx = torch.topk(score_sel, k=max_new_edges, largest=True).indices
                i_sel = i_sel[top_idx]
                j_sel = j_sel[top_idx]
                c_sel = c_sel[top_idx]

            self.struct_mask_rec[i_sel, j_sel] = 1.0
            self.w_rec[i_sel, j_sel] = 0.02 * c_sel
            return int(i_sel.numel())

    def compute_tonic(self, tonic_strength: float, tonic_vacancy_scale: float) -> torch.Tensor:
        in_degree = self.struct_mask_rec.sum(dim=0)
        max_deg = in_degree.max().clamp(min=1.0)
        vacancy = 1.0 - (in_degree / max_deg)
        tonic = tonic_strength * (1.0 + tonic_vacancy_scale * vacancy)
        return tonic

    def step(
        self,
        x_t: torch.Tensor,
        h_prev: torch.Tensor,
        tonic: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        pre = x_t @ self.w_in + h_prev @ self.w_rec
        if tonic is not None:
            pre = pre + tonic
        h_t = torch.tanh((1.0 - self.alpha) * h_prev + self.alpha * pre)
        y_t = h_t @ self.w_out
        return h_t, y_t

    @classmethod
    def from_layout(
        cls,
        signal_dim: int,
        alpha: float,
        layout: NeuronSpaceLayout,
        device: torch.device,
        structural_density: float = 1.0,
    ) -> "DistanceSignalCopyNet":
        mask_rec, mask_in, mask_out = build_masks_for_layout(layout=layout, signal_dim=signal_dim, device=device)
        if structural_density >= 1.0:
            struct_mask_rec = (mask_rec > 0.5).to(torch.float32)
        else:
            p = min(1.0, max(0.0, float(structural_density)))
            struct_mask_rec = ((torch.rand_like(mask_rec) < p) & (mask_rec > 0.5)).to(torch.float32)

        return cls(
            signal_dim=signal_dim,
            n_neurons=layout.n_neurons,
            alpha=alpha,
            mask_rec=mask_rec,
            mask_in=mask_in,
            mask_out=mask_out,
            struct_mask_rec=struct_mask_rec,
        )

    def transplant_to_layout(
        self,
        target_layout: NeuronSpaceLayout,
        signal_dim: int | None = None,
        device: torch.device | None = None,
        neuron_index_map: torch.Tensor | None = None,
    ) -> "DistanceSignalCopyNet":
        """Copy learned neuron patterns into a new space with a new IO arrangement."""
        target_device = device or self.w_in.device
        out_signal_dim = int(self.signal_dim if signal_dim is None else signal_dim)
        target = DistanceSignalCopyNet.from_layout(
            signal_dim=out_signal_dim,
            alpha=self.alpha,
            layout=target_layout,
            device=target_device,
            structural_density=1.0,
        )

        src_n = int(self.n_neurons)
        dst_n = int(target_layout.n_neurons)
        if neuron_index_map is None:
            neuron_index_map = linear_neuron_map(source_n=src_n, target_n=dst_n, device=target_device)
        else:
            neuron_index_map = neuron_index_map.to(device=target_device, dtype=torch.long)
            if neuron_index_map.numel() != dst_n:
                raise ValueError("neuron_index_map must have length equal to target_layout.n_neurons")
        neuron_index_map = neuron_index_map.clamp(min=0, max=max(src_n - 1, 0))

        src_w_in = self.w_in.detach().to(target_device)
        src_w_rec = self.w_rec.detach().to(target_device)
        src_w_out = self.w_out.detach().to(target_device)
        src_struct = self.struct_mask_rec.detach().to(target_device)

        with torch.no_grad():
            target.w_in.zero_()
            target.w_rec.zero_()
            target.w_out.zero_()
            target.struct_mask_rec.zero_()

            common_in_dim = min(src_w_in.shape[0], out_signal_dim)
            target.w_in[:common_in_dim, :] = src_w_in[:common_in_dim, neuron_index_map]

            rec_cols = src_w_rec[neuron_index_map, :]
            target.w_rec[:, :] = rec_cols[:, neuron_index_map]
            struct_cols = src_struct[neuron_index_map, :]
            target.struct_mask_rec[:, :] = struct_cols[:, neuron_index_map]

            common_out_dim = min(src_w_out.shape[1], out_signal_dim)
            target.w_out[:, :common_out_dim] = src_w_out[neuron_index_map, :common_out_dim]

            target.enforce_masks_()

        return target