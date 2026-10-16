from __future__ import annotations

from threading import Condition
from typing import Any


class PairEventGate:
    """Synchronize paired event-loop boundaries and release both sides on stop."""

    def __init__(self) -> None:
        self._condition = Condition()
        self._ready: set[str] = set()
        self._event_identities: dict[str, Any] = {}
        self._completed: set[str] = set()
        self._finished: set[str] = set()
        self._exposure_ids: dict[str, str] = {}
        self._exposure_done: set[str] = set()
        self._stopped = False
        self._stop_reason: str | None = None
        self._trigger_side: str | None = None
        self._trigger_anchor: dict[str, str] | None = None

    def begin_exposure(self, side: str, exposure_id: str) -> None:
        if side not in {"original", "instrumented"} or not isinstance(exposure_id, str) or not exposure_id:
            raise ValueError("invalid paired exposure identity")
        with self._condition:
            if self._stopped:
                raise RuntimeError("paired execution has stopped")
            if side in self._exposure_ids:
                raise RuntimeError(f"{side} started a new exposure before pair alignment")
            self._exposure_ids[side] = exposure_id
            peer = "instrumented" if side == "original" else "original"
            if peer in self._exposure_ids and self._exposure_ids[peer] != exposure_id:
                self._stopped = True
                self._stop_reason = "paired exposure identity mismatch"
                self._trigger_side = side
                self._condition.notify_all()
                raise RuntimeError("paired exposure identities differ")
            self._condition.notify_all()

    def before_event(self, side: str, exposure_id: str, event_identity: Any = None) -> bool:
        if side not in {"original", "instrumented"}:
            raise ValueError("invalid paired side")
        peer = "instrumented" if side == "original" else "original"
        with self._condition:
            if self._stopped:
                return False
            if event_identity is None:
                self.stop(side, "next event identity unavailable", None)
                return False
            if self._exposure_ids.get(side) != exposure_id:
                raise RuntimeError("event-loop exposure differs from its capture identity")
            while (not self._stopped and peer not in self._finished
                   and peer not in self._exposure_done and peer not in self._exposure_ids):
                self._condition.wait()
            if self._stopped:
                return False
            if peer in self._finished or peer in self._exposure_done:
                self.stop(side, "unmatched next event after peer completion", None)
                return False
            if self._exposure_ids[peer] != exposure_id:
                self._stopped = True
                self._stop_reason = "paired exposure identity mismatch"
                self._trigger_side = side
                self._condition.notify_all()
                return False
            self._ready.add(side)
            self._event_identities[side] = event_identity
            if self._ready == {"original", "instrumented"}:
                if self._event_identities[side] != self._event_identities[peer]:
                    self.stop(side, "paired next event identity mismatch", None)
                    return False
                self._ready.clear()
                self._event_identities.clear()
                self._condition.notify_all()
                return True
            while not self._stopped and peer not in self._finished and side in self._ready:
                self._condition.wait()
            if peer in self._finished or peer in self._exposure_done:
                self.stop(side, "unmatched next event after peer completion", None)
            return not self._stopped

    def after_event(self, side: str) -> None:
        peer = "instrumented" if side == "original" else "original"
        with self._condition:
            if self._stopped:
                return
            if peer in self._finished or peer in self._exposure_done:
                self.stop(side, "unmatched completed event after peer completion", None)
                return
            self._completed.add(side)
            if self._completed == {"original", "instrumented"}:
                self._completed.clear()
                self._condition.notify_all()
                return
            while (not self._stopped and peer not in self._finished
                   and peer not in self._exposure_done and side in self._completed):
                self._condition.wait()

    def finish_exposure(self, side: str) -> None:
        peer = "instrumented" if side == "original" else "original"
        with self._condition:
            self._exposure_done.add(side)
            if peer in self._ready or peer in self._completed:
                self.stop(side, "peer has unmatched next event", None)
            self._ready.discard(side)
            self._completed.discard(side)
            self._condition.notify_all()
            if peer in self._exposure_done:
                if self._exposure_ids.get(side) != self._exposure_ids.get(peer):
                    self._stopped = True
                    self._stop_reason = "paired exposure identity mismatch"
                    self._trigger_side = side
                    self._condition.notify_all()
                    return
                self._exposure_ids.clear()
                self._exposure_done.clear()
                self._ready.clear()
                self._completed.clear()
                self._condition.notify_all()
                return
            while not self._stopped and peer not in self._finished and side in self._exposure_done:
                self._condition.wait()

    def finish(self, side: str) -> None:
        peer = "instrumented" if side == "original" else "original"
        with self._condition:
            self._finished.add(side)
            if peer in self._ready or peer in self._completed:
                self.stop(side, "peer finished at unmatched event boundary", None)
            self._exposure_done.add(side)
            self._ready.discard(side)
            self._completed.discard(side)
            self._condition.notify_all()

    def stop(self, side: str, reason: str, anchor: dict[str, str] | None) -> None:
        with self._condition:
            if not self._stopped:
                self._stopped = True
                self._stop_reason = reason
                self._trigger_side = side
                self._trigger_anchor = anchor
            self._condition.notify_all()

    @property
    def stopped(self) -> bool:
        with self._condition:
            return self._stopped

    @property
    def stop_evidence(self) -> dict[str, Any]:
        with self._condition:
            return {"reason": self._stop_reason, "trigger_side": self._trigger_side,
                    "anchor": self._trigger_anchor}
