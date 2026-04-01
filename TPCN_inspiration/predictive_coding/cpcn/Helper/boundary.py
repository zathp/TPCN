"""
Self/Other Boundary Inference layer for CPCN.

BoundaryState      — enum of five possible boundary classifications.
BoundaryScores     — dataclass holding all raw scores plus chosen state.
BoundaryInference  — stateful layer that computes and smooths boundary scores.

Score model (from architecture docs §30):

    B_self = w_I * identity_confidence
           + w_A * anchor_agreement
           + w_P * perspective_score
           - w_E * global_error

Smoothed with EMA at rate rho to prevent flickering.

State selection:
    CONTESTED       — top two scores are within `contest_margin`
    SELF            — B_self >= self_threshold AND margin > margin_threshold
    PROBABLE_SELF   — B_self >= probable_self_threshold
    FAMILIAR_OTHER  — familiar_score >= familiar_threshold
    UNKNOWN_OTHER   — default
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


# ── Boundary state enum ────────────────────────────────────────────────────────

class BoundaryState(Enum):
    SELF = auto()
    PROBABLE_SELF = auto()
    FAMILIAR_OTHER = auto()
    UNKNOWN_OTHER = auto()
    CONTESTED = auto()


# ── Score container ────────────────────────────────────────────────────────────

@dataclass
class BoundaryScores:
    """All boundary scores produced by one forward call."""

    self_score: float = 0.0
    familiar_other_score: float = 0.0
    unknown_other_score: float = 0.0
    contested: bool = False
    boundary_state: BoundaryState = BoundaryState.UNKNOWN_OTHER
    smoothed_self_score: float = 0.0

    @property
    def update_permitted(self) -> bool:
        """Memory updates should be blocked when boundary is contested."""
        return not self.contested and self.boundary_state != BoundaryState.CONTESTED


# ── Inference layer ────────────────────────────────────────────────────────────

class BoundaryInference:
    """
    Stateful self/other boundary inference.

    Call ``step()`` once per timestep with the current evidence bundle.
    The returned ``BoundaryScores`` contains both raw and smoothed scores
    plus the selected ``BoundaryState``.

    The layer maintains a smoothed self-score (EMA at rate `rho`) so that
    downstream consumers (e.g. growth valve gate, memory update gate) see
    a stable signal rather than frame-level noise.
    """

    def __init__(
        self,
        w_identity: float = 0.35,
        w_anchor: float = 0.40,
        w_perspective: float = 0.15,
        w_error: float = 0.10,
        self_threshold: float = 0.70,
        probable_self_threshold: float = 0.50,
        familiar_threshold: float = 0.55,
        margin_threshold: float = 0.15,
        contest_margin: float = 0.10,
        rho: float = 0.20,
    ) -> None:
        self.w_identity = float(w_identity)
        self.w_anchor = float(w_anchor)
        self.w_perspective = float(w_perspective)
        self.w_error = float(w_error)

        self.self_threshold = float(self_threshold)
        self.probable_self_threshold = float(probable_self_threshold)
        self.familiar_threshold = float(familiar_threshold)
        self.margin_threshold = float(margin_threshold)
        self.contest_margin = float(contest_margin)
        self.rho = float(rho)

        self._smoothed_self: float = 0.0

    def reset(self) -> None:
        self._smoothed_self = 0.0

    def step(
        self,
        identity_confidence: float,
        anchor_agreement: float,
        familiar_score: float,
        perspective_score: float,
        global_error: float,
    ) -> BoundaryScores:
        """
        Compute boundary scores and select a boundary state.

        Args:
            identity_confidence : fused identity confidence in [0, 1]
            anchor_agreement    : how strongly anchor memory agrees in [0, 1]
            familiar_score      : best-match familiar-other similarity in [0, 1]
            perspective_score   : perspective-consistency cue in [0, 1]
            global_error        : global error signal in [0, 1]
        """
        b_self = (
            self.w_identity * identity_confidence
            + self.w_anchor * anchor_agreement
            + self.w_perspective * perspective_score
            - self.w_error * global_error
        )
        b_familiar = familiar_score
        b_unknown = 1.0 - (identity_confidence + anchor_agreement) / 2.0

        # Smooth self score
        self._smoothed_self = (
            self.rho * b_self + (1 - self.rho) * self._smoothed_self
        )

        # Margin for contest
        scores = [b_self, b_familiar, b_unknown]
        sorted_scores = sorted(scores, reverse=True)
        margin = sorted_scores[0] - sorted_scores[1]
        contested = margin < self.contest_margin

        # State selection
        if contested:
            state = BoundaryState.CONTESTED
        elif b_self >= self.self_threshold and margin > self.margin_threshold:
            state = BoundaryState.SELF
        elif b_self >= self.probable_self_threshold:
            state = BoundaryState.PROBABLE_SELF
        elif b_familiar >= self.familiar_threshold:
            state = BoundaryState.FAMILIAR_OTHER
        else:
            state = BoundaryState.UNKNOWN_OTHER

        return BoundaryScores(
            self_score=b_self,
            familiar_other_score=b_familiar,
            unknown_other_score=b_unknown,
            contested=contested,
            boundary_state=state,
            smoothed_self_score=self._smoothed_self,
        )