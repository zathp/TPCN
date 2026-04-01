from dataclasses import dataclass


@dataclass
class PersonHypothesis:
    fused_score: float = 0.0
    face_score: float = 0.0
    voice_score: float = 0.0
    context_score: float = 0.0
    anchor_agreement: float = 0.0
    confidence: float = 0.0
    contradiction: float = 0.0
    novelty: float = 0.0
    best_id: int = -1
    is_contested: bool = False
