"""
WEMA Dual-Track prediction and self-generated error for CPCN.

DualTrackOutput  — dataclass capturing all track outputs and error components.
WEMADualTrack    — runs Track A (anchor/self prediction) and Track B (world
                   prediction) in parallel and computes a global error signal
                   that drives Open reservoir adaptation.

From architecture docs:
    Track A: predicts your next state (high inertia, α=0.70, β=0.95)
    Track B: predicts world state     (more plastic,  α=0.30, β=0.85)

    global_error = mean|track_A - track_B|
                 + duplication_error          # ||anchor_A_out - anchor_B_out||
                 + contradiction_error        # cross-modal face/voice mismatch
                 + boundary_uncertainty       # 1 - smoothed_self_score
"""

from __future__ import annotations

from dataclasses import dataclass

import torch

from .wema_filter import WEMAFilter


# ── Output container ───────────────────────────────────────────────────────────

@dataclass
class DualTrackOutput:
    """All outputs from one step of the dual-track WEMA system."""

    track_a: torch.Tensor               # WEMA_A output (anchor / self)
    track_b: torch.Tensor               # WEMA_B output (world)
    prediction_error: torch.Tensor      # element-wise |track_a - track_b|
    duplication_error: float            # ||anchor_A_out - anchor_B_out|| / dim
    contradiction_error: float          # cross-modal face/voice contradiction
    boundary_uncertainty: float         # 1 - smoothed_self_score
    global_error: float                 # scalar sum of all error components


# ── Dual-track layer ───────────────────────────────────────────────────────────

class WEMADualTrack:
    """
    Dual-track WEMA prediction system.

    Track A runs on the anchor reservoir output — high inertia, conservative.
    Track B runs on the open reservoir output  — more plastic, world-facing.

    ``global_error`` is the scalar error signal used to gate learning and
    route back into the Open reservoir for online adaptation.

    This class is intentionally not an nn.Module because it holds no
    trainable parameters — it is a stateful filter.
    """

    def __init__(
        self,
        alpha_a: float = 0.70,
        alpha_b: float = 0.30,
        beta_a: float = 0.95,
        beta_b: float = 0.85,
        eps: float = 1e-6,
    ) -> None:
        self._alpha_a = float(alpha_a)
        self._alpha_b = float(alpha_b)
        self._beta_a = float(beta_a)
        self._beta_b = float(beta_b)

        self._wema_a = WEMAFilter(eps=eps)
        self._wema_b = WEMAFilter(eps=eps)

    def reset(self) -> None:
        self._wema_a.reset()
        self._wema_b.reset()

    def step(
        self,
        anchor_output: torch.Tensor,
        world_output: torch.Tensor,
        duplication_error: float = 0.0,
        contradiction_error: float = 0.0,
        boundary_uncertainty: float = 0.0,
    ) -> DualTrackOutput:
        """
        Advance both tracks by one timestep and compute global error.

        Args:
            anchor_output        : output from AnchorReadout_A, shape (output_dim,)
            world_output         : output from OpenReadout, shape (output_dim,)
            duplication_error    : ||anchor_A_out - anchor_B_out|| / dim
            contradiction_error  : face/voice cross-modal contradiction score
            boundary_uncertainty : 1 - smoothed_self_score from BoundaryInference

        Returns:
            DualTrackOutput with all fields populated.
        """
        device = anchor_output.device
        dtype = anchor_output.dtype

        alpha_a = torch.tensor(self._alpha_a, device=device, dtype=dtype)
        alpha_b = torch.tensor(self._alpha_b, device=device, dtype=dtype)
        beta_a = torch.tensor(self._beta_a, device=device, dtype=dtype)
        beta_b = torch.tensor(self._beta_b, device=device, dtype=dtype)

        y_a = self._wema_a.step(x=anchor_output, alpha=alpha_a, beta=beta_a)
        y_b = self._wema_b.step(x=world_output,  alpha=alpha_b, beta=beta_b)

        prediction_error = torch.abs(y_a - y_b)
        pred_err_mean = float(prediction_error.mean().item())

        global_error = (
            pred_err_mean
            + float(duplication_error)
            + float(contradiction_error)
            + float(boundary_uncertainty)
        )

        return DualTrackOutput(
            track_a=y_a,
            track_b=y_b,
            prediction_error=prediction_error,
            duplication_error=float(duplication_error),
            contradiction_error=float(contradiction_error),
            boundary_uncertainty=float(boundary_uncertainty),
            global_error=global_error,
        )
