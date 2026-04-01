"""
Cross-modal identity fusion layer for CPCN.

PersonHypothesis       — dataclass summarising the fused identity state.
CrossModalFusionLayer  — nn.Module that merges face + voice + context into one
                         running person hypothesis with contradiction detection.

See CPCN design notes for detailed behaviour.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn


# ── Person hypothesis ──────────────────────────────────────────────────────────


@dataclass
class PersonHypothesis:
    """Unified person-state output from one forward call of CrossModalFusionLayer."""

    fused_score: float = 0.0
    face_score: float = 0.0
    voice_score: float = 0.0
    context_score: float = 0.0
    anchor_agreement: float = 0.0
    confidence: float = 0.0         # winning-hypothesis margin
    contradiction: float = 0.0      # |face_winner - voice_winner| when they disagree
    novelty: float = 0.0            # how unexpected this hypothesis is
    best_id: int = -1               # winning identity index (-1 = unknown / insufficient confidence)
    is_contested: bool = False


# ── Fusion layer ───────────────────────────────────────────────────────────────


class CrossModalFusionLayer(nn.Module):
    """
    Confidence-weighted cross-modal fusion of face and voice identity evidence.

    The module maintains a smoothed running hypothesis ``_h`` over all
    candidate identities.  On each forward call it updates ``_h`` in place
    using an EMA then selects the best candidate.

    Args:
        n_identities      : number of known identity slots
        base_w_face       : base weight for face evidence
        base_w_voice      : base weight for voice evidence
        base_w_context    : base weight for contextual expectation
        base_w_anchor     : base weight for anchor agreement
        confidence_threshold : min best-score to report a known identity (best_id)
        margin_threshold  : min margin between top two scores to count as confident
        beta              : EMA rate for running hypothesis (0 = frozen, 1 = instant)
        contest_delta     : margin below which the result is flagged as contested
    """

    def __init__(
        self,
        n_identities: int = 16,
        base_w_face: float = 0.40,
        base_w_voice: float = 0.30,
        base_w_context: float = 0.15,
        base_w_anchor: float = 0.15,
        confidence_threshold: float = 0.35,
        margin_threshold: float = 0.10,
        beta: float = 0.25,
        contest_delta: float = 0.10,
    ) -> None:
        super().__init__()
        self.n_identities = int(n_identities)
        self.base_w_face = float(base_w_face)
        self.base_w_voice = float(base_w_voice)
        self.base_w_context = float(base_w_context)
        self.base_w_anchor = float(base_w_anchor)
        self.confidence_threshold = float(confidence_threshold)
        self.margin_threshold = float(margin_threshold)
        self.beta = float(beta)
        self.contest_delta = float(contest_delta)

        # Smoothed running fused scores: (n_identities,)
        # Registered as a buffer so .to(device) and state_dict() handle it.
        self.register_buffer("_h", torch.zeros(self.n_identities))

    def reset(self) -> None:
        """Reset running person hypothesis to zero."""
        self._h.zero_()

    def _fit_scores(self, scores: torch.Tensor) -> torch.Tensor:
        """Ensure `scores` has length `self.n_identities` by padding or truncating.

        Pads with zeros if shorter, truncates if longer. Returns a tensor
        on the same device as `self._h`.
        """
        if not torch.is_tensor(scores):
            scores = torch.tensor([], device=self._h.device)
        scores = scores.to(self._h.device)
        # Convert scalar tensors to 1-D
        if scores.dim() == 0:
            scores = scores.unsqueeze(0)
        if scores.numel() == 0:
            return torch.zeros(self.n_identities, device=self._h.device)
        n = int(scores.shape[0])
        if n == self.n_identities:
            return scores
        if n < self.n_identities:
            out = torch.zeros(self.n_identities, device=self._h.device)
            out[:n] = scores
            return out
        # n > self.n_identities -> truncate
        return scores[: self.n_identities]

    @torch.no_grad()
    def forward(
        self,
        face_scores: torch.Tensor,      # (n_identities,)
        voice_scores: torch.Tensor,     # (n_identities,)
        context_score: float = 0.0,
        anchor_agreement: float = 0.0,
        face_quality: float = 1.0,
        voice_quality: float = 1.0,
    ) -> PersonHypothesis:
        """
        Fuse face and voice evidence into a smoothed PersonHypothesis.

        All tensors must already be on the same device as the module.
        No gradients flow through this layer (it is a stateful estimator,
        not a differentiable module for backprop).
        """
        # Quality-adapted weights (renormalised so they sum to 1)
        w_f = self.base_w_face * float(face_quality)
        w_v = self.base_w_voice * float(voice_quality)
        w_total = w_f + w_v + self.base_w_context + self.base_w_anchor + 1e-8
        w_f /= w_total
        w_v /= w_total
        w_c = self.base_w_context / w_total
        w_a = self.base_w_anchor / w_total

        # Instantaneous fused score per identity
        # Normalize input score lengths to the fusion vector length
        f_scores = self._fit_scores(face_scores)
        v_scores = self._fit_scores(voice_scores)

        instant_f = (
            w_f * f_scores
            + w_v * v_scores
            + w_c * float(context_score)
            + w_a * float(anchor_agreement)
        )

        # EMA update of running hypothesis
        with torch.no_grad():
            self._h = (1.0 - self.beta) * self._h + self.beta * instant_f

        best_idx = int(torch.argmax(self._h).item())
        best_score = float(self._h[best_idx].item())

        # Confidence = margin between winner and runner-up
        if self.n_identities > 1:
            sorted_h, _ = torch.sort(self._h, descending=True)
            margin = float((sorted_h[0] - sorted_h[1]).item())
        else:
            margin = best_score

        # Contradiction: do face and voice prefer different candidates?
        # Use the normalized score vectors for winner selection and reporting
        face_best = int(torch.argmax(f_scores).item())
        voice_best = int(torch.argmax(v_scores).item())
        if face_best == voice_best:
            contradiction = 0.0
        else:
            contradiction = abs(float(f_scores[face_best].item()) - float(v_scores[voice_best].item()))

        contested = margin < self.contest_delta
        confidence = best_score if margin >= self.margin_threshold else 0.0
        novelty = max(0.0, 1.0 - best_score)

        return PersonHypothesis(
            fused_score=best_score,
            face_score=float(f_scores[best_idx].item()),
            voice_score=float(v_scores[best_idx].item()),
            context_score=float(context_score),
            anchor_agreement=float(anchor_agreement),
            confidence=confidence,
            contradiction=contradiction,
            novelty=novelty,
            best_id=best_idx if confidence >= self.confidence_threshold else -1,
            is_contested=contested,
        )
