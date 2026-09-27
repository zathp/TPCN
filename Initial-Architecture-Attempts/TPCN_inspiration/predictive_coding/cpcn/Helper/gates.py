"""
GrowthValve — governs how open the system is to external influence.

Implements a smooth valve that increases openness over time, never resets.

"""

class GrowthValve:
    def __init__(self, initial_openness=0.1, max_openness=0.8, rate=0.01):
        self.openness = initial_openness
        self.max_openness = max_openness
        self.rate = rate

    def step(self):
        if self.openness < self.max_openness:
            self.openness += self.rate
            if self.openness > self.max_openness:
                self.openness = self.max_openness
        return self.openness

    def record_interaction(self) -> None:
        """Compatibility shim: increment interaction count and slowly increase openness.

        This mirrors the behaviour expected elsewhere in the codebase where
        `record_interaction()` is called after successful identity confirmations.
        """
        # Simple heuristic: every 100 interactions increase openness by 0.05
        if not hasattr(self, "_interaction_count"):
            self._interaction_count = 0
        if not hasattr(self, "step_size"):
            self.step_size = 0.05
        if not hasattr(self, "interactions_per_step"):
            self.interactions_per_step = 100
        self._interaction_count += 1
        if self._interaction_count % self.interactions_per_step == 0:
            self.openness = min(self.max_openness, self.openness + self.step_size)

    @property
    def world_weight(self) -> float:
        return float(self.openness)

    @property
    def self_weight(self) -> float:
        return float(1.0 - self.openness)

    @property
    def interaction_count(self) -> int:
        return int(getattr(self, "_interaction_count", 0))

    def reset(self) -> None:
        """Reset interaction count only; openness intentionally preserved."""
        if hasattr(self, "_interaction_count"):
            self._interaction_count = 0
