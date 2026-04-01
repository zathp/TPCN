"""
CPCN — Complex Predictive Coding Network.

Full layered architecture (bottom → top):

  1. Adaptive baseline perception
      FaceIdentityModule, VoiceIdentityModule, FacialStateModule
      → slow-updating prototype banks with multi-gate update condition

  2. Cross-modal fusion
      CrossModalFusionLayer
      → smoothed PersonHypothesis with contradiction and novelty signals

  3. Self/other boundary inference
      BoundaryInference
      → BoundaryScores with smoothed self-score and BoundaryState

  4. Personal Anchor — two identical copies A and B (~800 nodes each)
      TorchWorldStep  (nx=10, ny=10, nz=8)
      AnchorReadout   (frozen, not trained online)
      → anchor_output_a, anchor_output_b

  5. Open reservoir — world-facing, more plastic (~5 k nodes)
      TorchWorldStep  (nx=20, ny=16, nz=16)
      OpenReadout     (trained online against next-step predictive objective)
      → world_output, alpha

  6. Self-duplication error + WEMA dual-track
      anchor_duplication_error  — ||output_A - output_B|| / dim
      WEMADualTrack             — Track A (self) vs Track B (world)
      → global_error

  7. Growth valve
      GrowthValve  — openness 10% → 80% over interactions, never resets

Online training (when `train=True`):
  Only the OpenReadout is optimised.
  Loss: MSE(prev_world_output, current_anchor_output_a)
  i.e. the open layer must predict the next anchor state one step ahead.
  Gradient clipping at max_norm=1.0 for stability.

Usage::

    from CPCN import CPCN, CPCNConfig

    net = CPCN()

    # Offline: inspect behaviour
    out = net.step(
        face_features=torch.randn(128),
        voice_features=torch.randn(64),
    )
    print(out.global_error, out.openness)

    # Online: run and train simultaneously
    out = net.step(face_features=..., voice_features=..., train=True)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn
import torch.optim as optim

from .Helper import (
    TorchWorldStep,
    OpenReadout,
    FaceIdentityModule,
    VoiceIdentityModule,
    FacialStateModule,
    CrossModalFusionLayer,
    PersonHypothesis,
    BoundaryInference,
    BoundaryScores,
    GrowthValve,
    WEMADualTrack,
    DualTrackOutput,
)
# Import the correct AnchorReadout and anchor_duplication_error from CPCN/Helper/anchor.py
import sys
sys.path.append(r'CPCN/Helper')
from anchor import AnchorReadout, anchor_duplication_error
# Import the correct AnchorReadout from CPCN/Helper/anchor.py
import sys
sys.path.append(r'CPCN/Helper')
from anchor import AnchorReadout


# ── Configuration ──────────────────────────────────────────────────────────────

@dataclass
class CPCNConfig:
    """
    All hyperparameters for a CPCN instance.

    Reservoir geometry:
        Anchor: 28 × 28 × 18 = 14 112 nodes per copy × 2 copies
        Open:   36 × 36 × 36 = 46 656 nodes

    These are deliberate — Anchor is small and conservative;
    Open is large enough to model world dynamics.
    """

    # ── Anchor reservoir (two copies, identical geometry) ──────────────────
    anchor_nx: int = 28
    anchor_ny: int = 28
    anchor_nz: int = 18          # 28 × 28 × 18 = 14 112 nodes
    anchor_damping: float = 0.05
    anchor_base_eddy: float = 0.95
    n_anchor_probes: int = 64

    # ── Open reservoir ─────────────────────────────────────────────────────
    open_nx: int = 36
    open_ny: int = 36
    open_nz: int = 36           # 36 × 36 × 36 = 46 656 nodes
    open_damping: float = 0.02
    open_base_eddy: float = 1.1
    n_open_probes: int = 128

    # ── Readout head dimensions ────────────────────────────────────────────
    anchor_output_dim: int = 64
    open_output_dim: int = 64

    # ── Adaptive baseline dimensions ───────────────────────────────────────
    face_input_dim: int = 128
    voice_input_dim: int = 64
    facial_state_input_dim: int = 64
    n_identities: int = 16

    # ── Fusion ────────────────────────────────────────────────────────────
    fusion_n_identities: int = 16

    # ── WEMA dual-track ───────────────────────────────────────────────────
    wema_alpha_a: float = 0.70
    wema_alpha_b: float = 0.30

    # ── Growth valve ──────────────────────────────────────────────────────
    initial_openness: float = 0.10

    # ── Online optimiser ──────────────────────────────────────────────────
    lr: float = 1e-3

    # ── Reservoir seed ────────────────────────────────────────────────────
    seed: int = 0


# ── Output container ───────────────────────────────────────────────────────────

@dataclass
class CPCNOutput:
    """All state and error outputs from one CPCN step."""

    person_hypothesis: PersonHypothesis
    boundary_scores: BoundaryScores
    anchor_output_a: torch.Tensor
    anchor_output_b: torch.Tensor
    open_output: torch.Tensor
    alpha: torch.Tensor             # gain hint from OpenReadout α head
    dual_track: DualTrackOutput
    global_error: float
    openness: float
    gate_open_face: bool
    gate_open_voice: bool
    gate_open_state: bool


# ── Main network ───────────────────────────────────────────────────────────────

class CPCN(nn.Module):
    """
    Complex Predictive Coding Network.

    See module docstring for full architecture summary and usage examples.
    """

    def __init__(
        self,
        cfg: Optional[CPCNConfig] = None,
        device: Optional[torch.device] = None,
    ) -> None:
        super().__init__()

        if cfg is None:
            cfg = CPCNConfig()
        self.cfg = cfg
        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # ── Layer 1: Adaptive baselines ────────────────────────────────────
        self.face_module = FaceIdentityModule(
            input_dim=cfg.face_input_dim,
            embed_dim=cfg.face_input_dim // 2,
            n_identities=cfg.n_identities,
        )
        self.voice_module = VoiceIdentityModule(
            input_dim=cfg.voice_input_dim,
            embed_dim=cfg.voice_input_dim // 2,
            n_identities=cfg.n_identities,
        )
        self.state_module = FacialStateModule(
            input_dim=cfg.facial_state_input_dim,
            embed_dim=cfg.facial_state_input_dim // 2,
            n_emotions=8,
        )

        # ── Layer 2: Cross-modal fusion ────────────────────────────────────
        self.fusion = CrossModalFusionLayer(
            n_identities=cfg.fusion_n_identities,
        )

        # ── Layer 3: Boundary inference (stateful, not nn.Module) ─────────
        self.boundary = BoundaryInference()

        # ── Layer 4: Anchor reservoirs A and B ────────────────────────────
        # Identical geometry, different seeds so they start in distinct states.
        self._anchor_a = TorchWorldStep(
            nx=cfg.anchor_nx,
            ny=cfg.anchor_ny,
            nz=cfg.anchor_nz,
            damping=cfg.anchor_damping,
            base_eddy=cfg.anchor_base_eddy,
            enable_particles=False,
            seed=cfg.seed,
            device=self.device,
        )
        self._anchor_b = TorchWorldStep(
            nx=cfg.anchor_nx,
            ny=cfg.anchor_ny,
            nz=cfg.anchor_nz,
            damping=cfg.anchor_damping,
            base_eddy=cfg.anchor_base_eddy,
            enable_particles=False,
            seed=cfg.seed + 1,
            device=self.device,
        )

        # ── Layer 5: Open reservoir ────────────────────────────────────────
        self._open = TorchWorldStep(
            nx=cfg.open_nx,
            ny=cfg.open_ny,
            nz=cfg.open_nz,
            damping=cfg.open_damping,
            base_eddy=cfg.open_base_eddy,
            enable_particles=False,
            seed=cfg.seed + 42,
            device=self.device,
        )

        # Build deterministic probe-index grids once
        self._anchor_probes = self._make_probe_idx(self._anchor_a, cfg.n_anchor_probes)
        self._open_probes   = self._make_probe_idx(self._open,    cfg.n_open_probes)

        anchor_state_dim = self._anchor_a.get_reservoir_state_size(
            probe_idx=self._anchor_probes,
            include_particles=False,
            include_global_moments=True,
        )
        open_state_dim = self._open.get_reservoir_state_size(
            probe_idx=self._open_probes,
            include_particles=False,
            include_global_moments=True,
        )

        # ── Readout heads ──────────────────────────────────────────────────
        # Both anchor readouts are frozen (conservative self-model).
        self.anchor_readout_a = AnchorReadout(anchor_state_dim, cfg.anchor_output_dim)
        self.anchor_readout_b = AnchorReadout(anchor_state_dim, cfg.anchor_output_dim)
        # Open readout is the only trained component.
        # Ensure OpenReadout output_dim matches AnchorReadout for WEMA compatibility
        self.open_readout = OpenReadout(open_state_dim, cfg.anchor_output_dim)

        # ── Layer 6: Dual-track WEMA ───────────────────────────────────────
        self.dual_track = WEMADualTrack(
            alpha_a=cfg.wema_alpha_a,
            alpha_b=cfg.wema_alpha_b,
        )

        # ── Layer 7: Growth valve ──────────────────────────────────────────
        self.growth_valve = GrowthValve(initial_openness=cfg.initial_openness)

        # ── Online optimiser (Open readout only) ───────────────────────────
        self._optimizer = optim.Adam(
            self.open_readout.parameters(),
            lr=cfg.lr,
        )
        # Store previous open reservoir state for next-step prediction loss.
        # We store the *state* (detached) and re-forward through open_readout
        # at loss time so the computation graph always uses current weights.
        self._prev_open_state: Optional[torch.Tensor] = None

        # Move all nn.Module components to target device
        self.to(self.device)

    # ── Internal helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _make_probe_idx(world: TorchWorldStep, n_probes: int) -> torch.Tensor:
        """Build evenly-spaced probe indices over (z, y, x) grid."""
        total = world.NZ * world.NY * world.NX
        n = max(1, min(int(n_probes), int(total)))
        flat = torch.linspace(0, total - 1, n, device=world.device).long()
        yz = world.NY * world.NX
        iz = flat // yz
        rem = flat % yz
        iy = rem // world.NX
        ix = rem % world.NX
        return torch.stack((iz.int(), iy.int(), ix.int()), dim=1)

    def _prior_global_error(self) -> float:
        """Return the last known global error for gate checks, defaulting to 0."""
        s = self.dual_track._wema_a.state
        if s is None:
            return 0.0
        return float(s.abs().mean().item())

    # Compatibility wrapper for identity modules whose forward() signatures
    # changed over time. Accepts a module and feature vector and always
    # returns a tuple: (state, scores, gate_open).
    def _call_identity_module(self, module, features: Optional[torch.Tensor], **kwargs):
        if features is None:
            n_ids = getattr(module, 'n_identities', None)
            if n_ids is None:
                # fallback: empty tensor
                return None, torch.tensor([], device=self.device), False
            return None, torch.zeros(int(n_ids), device=self.device), False

        feat = features.to(self.device)
        # Try calling with expected keyword args first
        try:
            out = module(feat, **kwargs)
        except TypeError as exc:
            # Fallback: try calling with only the feature vector
            try:
                out = module(feat)
            except Exception:
                raise

        # Normalize outputs into (state, scores, gate)
        if isinstance(out, tuple):
            if len(out) == 3:
                return out[0], out[1], bool(out[2])
            if len(out) == 2:
                # older API: (state, score) -> expand score to one-hot-like vector
                state, score = out
                # If score is scalar, return as single-element scores tensor
                if not torch.is_tensor(score):
                    score = torch.tensor([float(score)], device=self.device)
                return state, score, False
        # If module returned a single tensor, treat as scores
        if torch.is_tensor(out):
            scores = out
            return None, scores, False
        # Unknown return shape
        return None, torch.tensor([], device=self.device), False

    # ── Main step ──────────────────────────────────────────────────────────────

    def step(
        self,
        face_features: Optional[torch.Tensor] = None,
        voice_features: Optional[torch.Tensor] = None,
        facial_state_features: Optional[torch.Tensor] = None,
        face_quality: float = 1.0,
        voice_quality: float = 1.0,
        perspective_score: float = 0.5,
        train: bool = False,
        dt: float = 0.1,
    ) -> CPCNOutput:
        """
        Run one complete forward step through all CPCN layers.

        Args:
            face_features          : (face_input_dim,) feature vector or None
            voice_features         : (voice_input_dim,) feature vector or None
            facial_state_features  : (facial_state_input_dim,) feature vector or None
            face_quality           : sensory quality of face signal in [0, 1]
            voice_quality          : sensory quality of voice signal in [0, 1]
            perspective_score      : self-perspective consistency cue in [0, 1]
            train                  : if True, run an online optimiser step on
                                     the Open readout head
            dt                     : reservoir integration timestep

        Returns:
            CPCNOutput containing all intermediate outputs.
        """
        prior_error = self._prior_global_error()

        # ── 1. Adaptive baselines ──────────────────────────────────────────
        _, face_scores, gate_face = self._call_identity_module(
            self.face_module,
            face_features,
            quality=face_quality,
            anchor_agreement=0.5,
            global_error=prior_error,
        )

        _, voice_scores, gate_voice = self._call_identity_module(
            self.voice_module,
            voice_features,
            quality=voice_quality,
            anchor_agreement=0.5,
            global_error=prior_error,
        )

        _, state_scores, gate_state = self._call_identity_module(
            self.state_module,
            facial_state_features,
            quality=1.0,
            anchor_agreement=0.5,
            global_error=prior_error,
        )

        # ── 2. Cross-modal fusion ──────────────────────────────────────────
        hypothesis = self.fusion(
            face_scores=face_scores,
            voice_scores=voice_scores,
            context_score=0.0,
            anchor_agreement=0.5,
            face_quality=face_quality,
            voice_quality=voice_quality,
        )

        # ── 3. Boundary inference ──────────────────────────────────────────
        boundary_scores = self.boundary.step(
            identity_confidence=hypothesis.confidence,
            anchor_agreement=hypothesis.anchor_agreement,
            familiar_score=hypothesis.fused_score,
            perspective_score=perspective_score,
            global_error=prior_error,
        )
        boundary_uncertainty = 1.0 - boundary_scores.smoothed_self_score

        # ── 4. Build reservoir input vector ───────────────────────────────
        # Concatenate face and voice scores as a compact summary of the
        # current perceptual state. Ensure both score vectors are resized
        # to the fusion module's expected identity length so concatenation
        # produces a fixed-size input vector for the reservoirs.
        f_scores = self.fusion._fit_scores(face_scores)
        v_scores = self.fusion._fit_scores(voice_scores)
        raw_input = torch.cat([f_scores, v_scores], dim=0)  # (2 * fusion.n_identities,)
        input_gain = max(0.01, float(hypothesis.fused_score) * 0.10)

        # ── 5. Step Anchor-A and Anchor-B ─────────────────────────────────
        state_a = self._anchor_a.reservoir_step(
            input_vector=raw_input,
            dt=dt,
            input_gain=input_gain,
            probe_idx=self._anchor_probes,
            include_particles=False,
            include_global_moments=True,
            return_numpy=False,
        )
        state_b = self._anchor_b.reservoir_step(
            input_vector=raw_input,
            dt=dt,
            input_gain=input_gain,
            probe_idx=self._anchor_probes,
            include_particles=False,
            include_global_moments=True,
            return_numpy=False,
        )

        # ── 6. Step Open reservoir ─────────────────────────────────────────
        # Open reservoir receives a weighted version of the same input.
        # World weight = openness; anchor weight = 1 - openness.
        open_gain = input_gain * self.growth_valve.world_weight
        open_state = self._open.reservoir_step(
            input_vector=raw_input,
            dt=dt,
            input_gain=open_gain,
            probe_idx=self._open_probes,
            include_particles=False,
            include_global_moments=True,
            return_numpy=False,
        )

        # ── 7. Readout heads ───────────────────────────────────────────────
        with torch.set_grad_enabled(train):
            anchor_out_a = self.anchor_readout_a(state_a)
            anchor_out_b = self.anchor_readout_b(state_b)
            world_out, alpha = self.open_readout(open_state)

        # ── 8. Self-duplication error ──────────────────────────────────────
        dup_error = anchor_duplication_error(anchor_out_a, anchor_out_b)

        # ── 9. WEMA dual-track ─────────────────────────────────────────────
        dual = self.dual_track.step(
            anchor_output=anchor_out_a.detach(),
            world_output=world_out.detach(),
            duplication_error=dup_error,
            contradiction_error=hypothesis.contradiction,
            boundary_uncertainty=boundary_uncertainty,
        )

        # ── 10. Online training: Open readout next-step prediction ─────────
        if train and self._prev_open_state is not None:
            # Re-forward the previous reservoir state through open_readout
            # using the CURRENT weights so the computation graph is fresh.
            prev_world_out, _ = self.open_readout(self._prev_open_state)
            target = anchor_out_a.detach()
            train_loss = nn.functional.mse_loss(prev_world_out, target)
            self._optimizer.zero_grad()
            train_loss.backward()
            nn.utils.clip_grad_norm_(self.open_readout.parameters(), max_norm=1.0)
            self._optimizer.step()

        # Store open reservoir state (detached) for next step's training
        self._prev_open_state = open_state.detach().clone() if train else None

        # ── 11. Growth valve ───────────────────────────────────────────────
        # Count the interaction only when a known identity was confirmed
        # and the boundary is not contested.
        if hypothesis.best_id >= 0 and boundary_scores.update_permitted:
            self.growth_valve.record_interaction()

        return CPCNOutput(
            person_hypothesis=hypothesis,
            boundary_scores=boundary_scores,
            anchor_output_a=anchor_out_a.detach(),
            anchor_output_b=anchor_out_b.detach(),
            open_output=world_out.detach(),
            alpha=alpha.detach(),
            dual_track=dual,
            global_error=dual.global_error,
            openness=self.growth_valve.openness,
            gate_open_face=gate_face,
            gate_open_voice=gate_voice,
            gate_open_state=gate_state,
        )

    # ── Reset ──────────────────────────────────────────────────────────────────

    def reset(self, reset_reservoirs: bool = True) -> None:
        """
        Reset all stateful components.

        ``reset_reservoirs=True`` re-initialises the field dynamics of all
        three TorchWorldStep instances.  The growth valve's maturity counter
        is intentionally NOT reset — use a new CPCN instance for that.
        """
        if reset_reservoirs:
            self._anchor_a.reset_reservoir_state()
            self._anchor_b.reset_reservoir_state()
            self._open.reset_reservoir_state()
        self.face_module.reset()
        self.voice_module.reset()
        self.state_module.reset()
        self.fusion.reset()
        self.boundary.reset()
        self.dual_track.reset()
        self._prev_open_state = None

    # ── Convenience properties ─────────────────────────────────────────────────

    @property
    def openness(self) -> float:
        """Current world-openness in [0.10, 0.80]."""
        return self.growth_valve.openness

    @property
    def interaction_count(self) -> int:
        """Number of confirmed external interactions recorded so far."""
        return self.growth_valve.interaction_count
