from __future__ import annotations

import argparse
import os
import random
import socket
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch import nn


ROOT = Path(__file__).resolve().parent


@dataclass
class ReservoirConfig:
    nx: int = 20
    ny: int = 16
    nz: int = 16
    n_probes: int = 128
    drive_dim: int = 32
    dt: float = 0.08
    input_gain: float = 0.15
    base_eddy: float = 1.0
    damping: float = 0.02
    include_global_moments: bool = True
    use_updated_variant: bool = True


@dataclass
class TPCNInspiredConfig:
    input_dim: int
    hidden_dim: int = 256
    delay_steps: int = 4
    locality_radius_in: int = 8
    locality_radius_out: int = 8


@dataclass
class PCStepOutput:
    loss: float
    delayed_out_norm: float
    delayed_hid_norm: float
    prediction_error_mean: float


@dataclass
class TrainArgs:
    genetic_epochs: int
    env_steps: int
    batch_size: int
    hidden_dim: int
    delay_steps: int
    locality_radius_in: int
    locality_radius_out: int
    lr: float
    seed: int
    multi_gpu: bool
    save_every: int
    res_cfg: ReservoirConfig


class SpatialNeuronField:
    """Spatially indexed neuron dynamics without Euclidean-reservoir mechanics."""

    def __init__(self, cfg: ReservoirConfig, batch_size: int, device: torch.device, seed: int) -> None:
        self.device = device
        self.float_dtype = torch.float32
        self.B = int(batch_size)
        self.NX = int(cfg.nx)
        self.NY = int(cfg.ny)
        self.NZ = int(cfg.nz)
        self.drive_dim = int(cfg.drive_dim)
        self.damping = float(cfg.damping)
        self.base_eddy = float(cfg.base_eddy)
        self._generator = torch.Generator(device=device)
        self._generator.manual_seed(int(seed))

        self._prev_probe_state = torch.empty(0, device=device, dtype=self.float_dtype)
        self._proj_w = torch.empty(0, device=device, dtype=self.float_dtype)
        self._coord_basis = torch.empty(0, device=device, dtype=self.float_dtype)
        self._n_probes = 0

    def _ensure_probe_layout(self, probe_idx: torch.Tensor) -> None:
        n_probes = int(probe_idx.shape[0])
        if n_probes == self._n_probes:
            return

        self._n_probes = n_probes
        scale = 1.0 / max(self.NX, self.NY, self.NZ, 1)
        self._proj_w = torch.randn(
            self.drive_dim,
            n_probes,
            generator=self._generator,
            device=self.device,
            dtype=self.float_dtype,
        ) * scale

        coords = probe_idx.to(device=self.device, dtype=self.float_dtype)
        denom = torch.tensor(
            [max(self.NZ - 1, 1), max(self.NY - 1, 1), max(self.NX - 1, 1)],
            device=self.device,
            dtype=self.float_dtype,
        )
        c = (2.0 * (coords / denom)) - 1.0
        z, y, x = c[:, 0], c[:, 1], c[:, 2]
        self._coord_basis = torch.stack(
            (
                x,
                y,
                z,
                x * y,
                y * z,
            ),
            dim=1,
        )
        self._prev_probe_state = torch.zeros(
            self.B,
            n_probes,
            5,
            device=self.device,
            dtype=self.float_dtype,
        )

    def get_reservoir_state_size(self, probe_idx=None, include_particles=False, include_global_moments=True):
        if probe_idx is None:
            n = self.NZ * self.NY * self.NX
        else:
            n = int(torch.as_tensor(probe_idx).shape[0])
        extra = 8 if include_global_moments else 0
        return int(n * 5 + extra)

    def reset_reservoir_state(self, seed=None):
        if seed is not None:
            self._generator.manual_seed(int(seed))
        if self._prev_probe_state.numel() > 0:
            self._prev_probe_state.zero_()

    def reservoir_step(
        self,
        input_vector,
        dt=0.1,
        input_gain=1.0,
        probe_idx=None,
        include_particles=False,
        include_global_moments=True,
        return_numpy=False,
    ):
        if input_vector is None:
            raise ValueError("input_vector is required")
        if probe_idx is None:
            raise ValueError("probe_idx is required for spatial field mode")

        idx = torch.as_tensor(probe_idx, device=self.device, dtype=torch.int32)
        self._ensure_probe_layout(idx)

        u = torch.as_tensor(input_vector, device=self.device, dtype=self.float_dtype)
        if u.ndim == 1:
            u = u.unsqueeze(0)
        if u.ndim != 2:
            raise ValueError(f"Expected input_vector rank 1 or 2, got shape {tuple(u.shape)}")
        if u.shape[0] != self.B:
            if u.shape[0] == 1:
                u = u.expand(self.B, -1)
            else:
                raise ValueError(f"Expected batch size {self.B}, got {u.shape[0]}")

        dt = float(dt)
        damping = max(0.0, min(0.95, self.damping))

        drive = torch.tanh(u @ self._proj_w).unsqueeze(-1)
        drive = drive * float(input_gain)

        ring_prev = self._prev_probe_state.roll(1, dims=1)
        ring_next = self._prev_probe_state.roll(-1, dims=1)
        ring_mix = 0.5 * (ring_prev + ring_next)

        intrinsic = self._coord_basis.unsqueeze(0) * self.base_eddy
        target = 0.65 * drive + 0.25 * ring_mix + 0.10 * intrinsic

        self._prev_probe_state = (1.0 - dt * (1.0 + damping)) * self._prev_probe_state + dt * target

        features = self._prev_probe_state.reshape(self.B, -1)
        if include_global_moments:
            mean = self._prev_probe_state.mean(dim=(1, 2), keepdim=False)
            std = self._prev_probe_state.std(dim=(1, 2), keepdim=False)
            l1 = self._prev_probe_state.abs().mean(dim=(1, 2), keepdim=False)
            l2 = torch.sqrt((self._prev_probe_state * self._prev_probe_state).mean(dim=(1, 2), keepdim=False) + 1e-6)
            per_feat_mean = self._prev_probe_state.mean(dim=1)
            per_feat_var = self._prev_probe_state.var(dim=1, unbiased=False)
            global_moments = torch.stack(
                (
                    mean,
                    std,
                    l1,
                    l2,
                    per_feat_mean[:, 0],
                    per_feat_mean[:, 1],
                    per_feat_var[:, 0],
                    per_feat_var[:, 1],
                ),
                dim=1,
            )
            out = torch.cat((features, global_moments), dim=1)
        else:
            out = features

        if return_numpy:
            return out.detach().cpu().numpy()
        return out


def make_reservoir_backend(cfg: ReservoirConfig, batch_size: int, device: torch.device, seed: int):
    return SpatialNeuronField(cfg=cfg, batch_size=batch_size, device=device, seed=seed)


class LocalPredictiveCodingNet(nn.Module):
    """Local predictive coding model with per-neuron delayed error buffers."""

    def __init__(
        self,
        cfg: TPCNInspiredConfig,
        mask_in: Optional[torch.Tensor] = None,
        mask_out: Optional[torch.Tensor] = None,
    ) -> None:
        super().__init__()
        self.cfg = cfg
        self.input_dim = int(cfg.input_dim)
        self.hidden_dim = int(cfg.hidden_dim)
        self.delay_steps = max(1, int(cfg.delay_steps))

        self.w_in = nn.Parameter(torch.empty(self.input_dim, self.hidden_dim))
        self.w_out = nn.Parameter(torch.empty(self.hidden_dim, self.input_dim))
        param_device = self.w_in.device
        if mask_in is None:
            mask_in = self._build_local_mask(self.input_dim, self.hidden_dim, cfg.locality_radius_in)
        if mask_out is None:
            mask_out = self._build_local_mask(self.hidden_dim, self.input_dim, cfg.locality_radius_out)
        self.register_buffer("mask_in", mask_in.to(device=param_device, dtype=torch.float32))
        self.register_buffer("mask_out", mask_out.to(device=param_device, dtype=torch.float32))
        self.reset_parameters()

        self.register_buffer("err_buf_out", torch.zeros(self.delay_steps, self.input_dim, device=param_device))
        self.register_buffer("err_buf_hid", torch.zeros(self.delay_steps, self.hidden_dim, device=param_device))
        self.delay_idx = 0

    def reset_parameters(self) -> None:
        nn.init.xavier_uniform_(self.w_in)
        nn.init.xavier_uniform_(self.w_out)
        with torch.no_grad():
            self.w_in.mul_(self.mask_in)
            self.w_out.mul_(self.mask_out)

    @staticmethod
    def _build_local_mask(pre_dim: int, post_dim: int, radius: int) -> torch.Tensor:
        r = max(0, int(radius))
        pre_idx = torch.arange(pre_dim, dtype=torch.long).view(pre_dim, 1)
        centers = torch.linspace(0, pre_dim - 1, post_dim).round().long().view(1, post_dim)
        dist = torch.abs(pre_idx - centers)
        circ = torch.minimum(dist, pre_dim - dist)
        return (circ <= r).to(torch.float32)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        h = torch.tanh(x @ self.w_in)
        y_hat = torch.tanh(h @ self.w_out)
        return h, y_hat

    def step(self, x: torch.Tensor, y: torch.Tensor, lr: float, world_size: int, distributed: bool) -> PCStepOutput:
        with torch.no_grad():
            h, y_hat = self.forward(x)

            err_out = y_hat - y
            err_hid = (err_out @ self.w_out.t()) * (1.0 - h * h)

            mean_err_out = err_out.mean(dim=0)
            mean_err_hid = err_hid.mean(dim=0)

            delayed_err_out = self.err_buf_out[self.delay_idx].clone()
            delayed_err_hid = self.err_buf_hid[self.delay_idx].clone()

            self.err_buf_out[self.delay_idx] = mean_err_out
            self.err_buf_hid[self.delay_idx] = mean_err_hid
            self.delay_idx = (self.delay_idx + 1) % self.delay_steps

            mean_h = h.mean(dim=0)
            mean_x = x.mean(dim=0)

            # Strictly local Hebbian-like update weighted by delayed local error.
            d_w_out = -torch.outer(mean_h, delayed_err_out)
            d_w_in = -torch.outer(mean_x, delayed_err_hid)

            # Enforce strict locality: only neighborhood-connected synapses update.
            d_w_in *= self.mask_in
            d_w_out *= self.mask_out

            if distributed:
                dist.all_reduce(d_w_out, op=dist.ReduceOp.SUM)
                dist.all_reduce(d_w_in, op=dist.ReduceOp.SUM)
                d_w_out /= float(world_size)
                d_w_in /= float(world_size)

            self.w_out += lr * d_w_out
            self.w_in += lr * d_w_in

            loss = torch.mean(err_out * err_out)
            delayed_out_norm = torch.mean(torch.abs(delayed_err_out))
            delayed_hid_norm = torch.mean(torch.abs(delayed_err_hid))
            prediction_error_mean = torch.mean(torch.abs(err_out))

        return PCStepOutput(
            loss=float(loss.item()),
            delayed_out_norm=float(delayed_out_norm.item()),
            delayed_hid_norm=float(delayed_hid_norm.item()),
            prediction_error_mean=float(prediction_error_mean.item()),
        )


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def setup_dist(rank: int, world_size: int, master_port: int) -> None:
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = str(master_port)
    backend = "nccl" if torch.cuda.is_available() else "gloo"
    dist.init_process_group(backend=backend, rank=rank, world_size=world_size)


def cleanup_dist() -> None:
    if dist.is_initialized():
        dist.destroy_process_group()


def seed_everything(seed: int, rank: int) -> None:
    base = seed + rank
    random.seed(base)
    torch.manual_seed(base)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(base)


def make_probe_idx(world, n_probes: int) -> torch.Tensor:
    total = world.NZ * world.NY * world.NX
    n = max(1, min(int(n_probes), int(total)))
    flat = torch.linspace(0, total - 1, n, device=world.device).long()
    yz = world.NY * world.NX
    iz = flat // yz
    rem = flat % yz
    iy = rem // world.NX
    ix = rem % world.NX
    return torch.stack((iz.int(), iy.int(), ix.int()), dim=1)


def build_spatial_locality_masks(
    probe_idx: torch.Tensor,
    input_dim: int,
    hidden_dim: int,
    locality_radius_in: int,
    locality_radius_out: int,
    include_global_moments: bool,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Create locality masks from physical probe coordinates.

    State layout from WorldStep is [probe_features(5 each), optional global moments(8)].
    We localize probe features by 3D distance in probe-index space and keep
    global-moment dimensions disconnected for strict locality.
    """
    n_probes = int(probe_idx.shape[0])
    probe_feature_dims = n_probes * 5
    global_dims = 8 if include_global_moments else 0

    if probe_feature_dims + global_dims != input_dim:
        raise ValueError(
            f"State dimension mismatch: expected {probe_feature_dims + global_dims}, got {input_dim}"
        )

    probe_pos = probe_idx.to(device=device, dtype=torch.float32)

    input_probe_id = torch.full((input_dim,), -1, device=device, dtype=torch.long)
    if probe_feature_dims > 0:
        input_probe_id[:probe_feature_dims] = torch.arange(probe_feature_dims, device=device, dtype=torch.long) // 5

    hidden_probe_id = torch.linspace(0, n_probes - 1, hidden_dim, device=device).round().long()
    hidden_probe_pos = probe_pos[hidden_probe_id]

    mask_in = torch.zeros((input_dim, hidden_dim), device=device, dtype=torch.float32)
    mask_out = torch.zeros((hidden_dim, input_dim), device=device, dtype=torch.float32)

    valid_in = input_probe_id >= 0
    if torch.any(valid_in):
        in_probe_pos = probe_pos[input_probe_id[valid_in]]
        dist_in = torch.cdist(in_probe_pos, hidden_probe_pos)
        mask_in_valid = (dist_in <= float(max(0, locality_radius_in))).to(torch.float32)
        mask_in[valid_in] = mask_in_valid

        dist_out = torch.cdist(hidden_probe_pos, in_probe_pos)
        mask_out_valid = (dist_out <= float(max(0, locality_radius_out))).to(torch.float32)
        mask_out[:, valid_in] = mask_out_valid

    return mask_in, mask_out


def build_reservoir_transition_batch(
    world,
    probe_idx: torch.Tensor,
    batch_size: int,
    drive_dim: int,
    dt: float,
    input_gain: float,
    include_global_moments: bool,
) -> tuple[torch.Tensor, torch.Tensor]:
    b = int(getattr(world, "B", batch_size))
    u_t = torch.randn(b, drive_dim, device=world.device, dtype=world.float_dtype)
    u_tp1 = 0.8 * u_t + 0.2 * torch.randn_like(u_t)

    s_t = world.reservoir_step(
        input_vector=u_t,
        dt=dt,
        input_gain=input_gain,
        probe_idx=probe_idx,
        include_particles=False,
        include_global_moments=include_global_moments,
        return_numpy=False,
    )
    s_tp1 = world.reservoir_step(
        input_vector=u_tp1,
        dt=dt,
        input_gain=input_gain,
        probe_idx=probe_idx,
        include_particles=False,
        include_global_moments=include_global_moments,
        return_numpy=False,
    )
    return s_t, s_tp1


def train_worker(rank: int, world_size: int, cfg: TrainArgs, master_port: int) -> None:
    distributed = world_size > 1
    if distributed:
        setup_dist(rank, world_size, master_port)

    seed_everything(cfg.seed, rank)

    if torch.cuda.is_available():
        device = torch.device(f"cuda:{rank}")
        torch.cuda.set_device(device)
    else:
        device = torch.device("cpu")

    world = make_reservoir_backend(
        cfg=cfg.res_cfg,
        batch_size=cfg.batch_size,
        device=device,
        seed=cfg.seed + rank,
    )
    probe_idx = make_probe_idx(world, cfg.res_cfg.n_probes)

    state_dim = world.get_reservoir_state_size(
        probe_idx=probe_idx,
        include_particles=False,
        include_global_moments=cfg.res_cfg.include_global_moments,
    )
    model_cfg = TPCNInspiredConfig(
        input_dim=state_dim,
        hidden_dim=cfg.hidden_dim,
        delay_steps=cfg.delay_steps,
        locality_radius_in=cfg.locality_radius_in,
        locality_radius_out=cfg.locality_radius_out,
    )
    spatial_mask_in, spatial_mask_out = build_spatial_locality_masks(
        probe_idx=probe_idx,
        input_dim=state_dim,
        hidden_dim=cfg.hidden_dim,
        locality_radius_in=cfg.locality_radius_in,
        locality_radius_out=cfg.locality_radius_out,
        include_global_moments=cfg.res_cfg.include_global_moments,
        device=device,
    )
    model = LocalPredictiveCodingNet(
        cfg=model_cfg,
        mask_in=spatial_mask_in,
        mask_out=spatial_mask_out,
    ).to(device)

    if distributed:
        dist.broadcast(model.w_in.data, src=0)
        dist.broadcast(model.w_out.data, src=0)
        dist.broadcast(model.err_buf_out.data, src=0)
        dist.broadcast(model.err_buf_hid.data, src=0)

    ckpt_dir = ROOT / "checkpoints"
    if rank == 0:
        ckpt_dir.mkdir(exist_ok=True)
        print(f"spatial_state_dim={state_dim} probes={cfg.res_cfg.n_probes} drive_dim={cfg.res_cfg.drive_dim}")
        print(
            f"locality_radius_in={cfg.locality_radius_in} locality_radius_out={cfg.locality_radius_out} "
            f"spatial_backend=non_euclidean_field"
        )
        print(f"spatial_backend_class={type(world).__name__}")
        in_density = float(model.mask_in.mean().item())
        out_density = float(model.mask_out.mean().item())
        print(f"locality_mode=spatial_probe_geometry mask_in_density={in_density:.4f} mask_out_density={out_density:.4f}")

    for epoch in range(1, cfg.genetic_epochs + 1):
        world.reset_reservoir_state(seed=cfg.seed + rank + epoch)

        epoch_loss = 0.0
        epoch_delayed_out = 0.0
        epoch_delayed_hid = 0.0
        epoch_pred_err = 0.0

        t0 = time.perf_counter()

        # Environmental loop over spatial field interactions.
        for _ in range(cfg.env_steps):
            x, y = build_reservoir_transition_batch(
                world=world,
                probe_idx=probe_idx,
                batch_size=cfg.batch_size,
                drive_dim=cfg.res_cfg.drive_dim,
                dt=cfg.res_cfg.dt,
                input_gain=cfg.res_cfg.input_gain,
                include_global_moments=cfg.res_cfg.include_global_moments,
            )

            step_out = model.step(
                x=x,
                y=y,
                lr=cfg.lr,
                world_size=world_size,
                distributed=distributed,
            )
            epoch_loss += step_out.loss
            epoch_delayed_out += step_out.delayed_out_norm
            epoch_delayed_hid += step_out.delayed_hid_norm
            epoch_pred_err += step_out.prediction_error_mean

        avg_loss = epoch_loss / max(cfg.env_steps, 1)
        avg_delayed_out = epoch_delayed_out / max(cfg.env_steps, 1)
        avg_delayed_hid = epoch_delayed_hid / max(cfg.env_steps, 1)
        avg_pred_err = epoch_pred_err / max(cfg.env_steps, 1)

        if distributed:
            t = torch.tensor([avg_loss, avg_delayed_out, avg_delayed_hid, avg_pred_err], dtype=torch.float32, device=device)
            dist.all_reduce(t, op=dist.ReduceOp.SUM)
            t /= float(world_size)
            avg_loss = float(t[0].item())
            avg_delayed_out = float(t[1].item())
            avg_delayed_hid = float(t[2].item())
            avg_pred_err = float(t[3].item())

        if rank == 0:
            dt_epoch = time.perf_counter() - t0
            print(
                f"genetic_epoch={epoch:04d} loss={avg_loss:.6f} pred_err={avg_pred_err:.6f} "
                f"delayed_out={avg_delayed_out:.6f} delayed_hid={avg_delayed_hid:.6f} sec={dt_epoch:.2f}"
            )
            if epoch % cfg.save_every == 0 or epoch == cfg.genetic_epochs:
                ckpt_path = ckpt_dir / f"tpcn_spatial_pc_epoch_{epoch}.pt"
                torch.save(
                    {
                        "genetic_epoch": epoch,
                        "model_state": model.state_dict(),
                        "loss": avg_loss,
                        "prediction_error": avg_pred_err,
                        "delayed_out": avg_delayed_out,
                        "delayed_hid": avg_delayed_hid,
                        "config": {
                            "train": asdict(cfg),
                            "spatial": asdict(cfg.res_cfg),
                            "model": asdict(model_cfg),
                        },
                    },
                    ckpt_path,
                )

    cleanup_dist()


def parse_args() -> TrainArgs:
    p = argparse.ArgumentParser(
        description=(
            "Spatial predictive coding trainer without Euclidean reservoir dynamics. "
            "Uses spatially indexed neuron state transitions and neuron-local delayed error updates."
        )
    )
    p.add_argument("--epochs", type=int, default=20, help="Outer genetic-loop epochs.")
    p.add_argument("--env-steps", type=int, default=32, help="Inner environmental-loop steps per epoch.")
    p.add_argument("--batch-size", type=int, default=64, help="Spatial transitions per env step.")
    p.add_argument("--hidden-dim", type=int, default=256)
    p.add_argument("--delay-steps", type=int, default=4, help="Per-neuron delayed-error buffer depth.")
    p.add_argument("--locality-radius-in", type=int, default=8, help="Input-to-hidden local neighborhood radius.")
    p.add_argument("--locality-radius-out", type=int, default=8, help="Hidden-to-output local neighborhood radius.")
    p.add_argument("--lr", type=float, default=5e-3)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--single-gpu", action="store_true", help="Disable multi-GPU even if available.")
    p.add_argument("--save-every", type=int, default=5)

    p.add_argument("--res-nx", type=int, default=20)
    p.add_argument("--res-ny", type=int, default=16)
    p.add_argument("--res-nz", type=int, default=16)
    p.add_argument("--res-probes", type=int, default=128)
    p.add_argument("--res-drive-dim", type=int, default=32)
    p.add_argument("--res-dt", type=float, default=0.08)
    p.add_argument("--res-input-gain", type=float, default=0.15)
    p.add_argument("--res-base-eddy", type=float, default=1.0)
    p.add_argument("--res-damping", type=float, default=0.02)
    p.add_argument("--res-no-global-moments", action="store_true")
    p.add_argument("--res-legacy-variant", action="store_true", help="Deprecated compatibility flag; ignored in spatial mode.")

    a = p.parse_args()

    res_cfg = ReservoirConfig(
        nx=a.res_nx,
        ny=a.res_ny,
        nz=a.res_nz,
        n_probes=a.res_probes,
        drive_dim=a.res_drive_dim,
        dt=a.res_dt,
        input_gain=a.res_input_gain,
        base_eddy=a.res_base_eddy,
        damping=a.res_damping,
        include_global_moments=(not a.res_no_global_moments),
        use_updated_variant=(not a.res_legacy_variant),
    )

    return TrainArgs(
        genetic_epochs=a.epochs,
        env_steps=max(1, a.env_steps),
        batch_size=max(1, a.batch_size),
        hidden_dim=max(2, a.hidden_dim),
        delay_steps=max(1, a.delay_steps),
        locality_radius_in=max(0, a.locality_radius_in),
        locality_radius_out=max(0, a.locality_radius_out),
        lr=float(a.lr),
        seed=int(a.seed),
        multi_gpu=(not a.single_gpu),
        save_every=max(1, a.save_every),
        res_cfg=res_cfg,
    )


def main() -> int:
    cfg = parse_args()

    n_cuda = torch.cuda.device_count() if torch.cuda.is_available() else 0
    use_multi = cfg.multi_gpu and n_cuda > 1

    if use_multi:
        world_size = n_cuda
        master_port = find_free_port()
        print(f"Launching multi-GPU training on {world_size} GPUs.")
        mp.spawn(train_worker, args=(world_size, cfg, master_port), nprocs=world_size, join=True)
    else:
        if n_cuda > 0:
            print("Launching single-GPU training.")
        else:
            print("CUDA not available; launching CPU training.")
        train_worker(rank=0, world_size=1, cfg=cfg, master_port=0)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
