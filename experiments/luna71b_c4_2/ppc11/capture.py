from __future__ import annotations

from typing import Any

from .schema import RECORDS, encode_payload
from .trace import TraceWriter


class SourceCapture:
    """Passive sink bound to exactly one source execution and exposure."""

    def __init__(self, writer: TraceWriter, *, pair_gate: Any = None) -> None:
        self.writer = writer
        self.pair_gate = pair_gate
        self.side = writer.identity["side"]
        if self.pair_gate is not None:
            self.pair_gate.begin_exposure(self.side, writer.identity["exposure_id"])
        self._queue_order = 0
        self._process_order = 0
        self._feedback_order = 0
        self._parameter_order = 0
        self._last_operation = "before_first_event"
        self._last_timestamp: Any = None
        self._branches_recorded: set[str] = set()
        self._terminal_recorded = False

    def emit(self, record_type: str, **payload: Any) -> None:
        if record_type not in RECORDS:
            raise ValueError(f"unsupported PPC-11 record type: {record_type}")
        comparison_id, _ = RECORDS[record_type]
        encoded = encode_payload(payload)
        self.writer.record(comparison_id, record_type, encoded)
        if record_type == "branch_state":
            self._branches_recorded.add(payload["branch_name"])

    def gap(self, requirement_id: str, field_path: str, source_point: str, reason: str) -> None:
        self.emit("capture_gap", requirement_id=requirement_id, field_path=field_path,
                  source_point=source_point, reason=reason)

    def parameter_transition(self, parameter_id: str, parameter_kind: str, old_value: Any,
                             new_value: Any, cause: str, timestamp: float) -> None:
        self.emit("parameter_transition", parameter_id=parameter_id,
                  parameter_kind=parameter_kind, old_value=old_value, new_value=new_value,
                  cause=cause, transition_order=self._parameter_order, timestamp=timestamp)
        self._parameter_order += 1

    def prediction_created(self, prediction: Any) -> None:
        self.emit("prediction_create", prediction_id=prediction.prediction_id,
                  expected_symbol=str(prediction.predicted_value), created_at=prediction.created_at,
                  due_at=prediction.expected_resolution_at, expires_at=prediction.expires_at)

    def prediction_matched(self, prediction_id: str, observed_symbol: str, timestamp: float) -> None:
        self.emit("prediction_match", prediction_id=prediction_id,
                  observed_symbol=observed_symbol, matched_at=timestamp, outcome="matched")

    def feedback_applied(self, feedback_id: str, origin_id: str, timestamp: float,
                         sign: int | tuple[int, ...], magnitude: float, due_at: float) -> None:
        self.emit("feedback_apply", feedback_id=feedback_id, origin_id=origin_id,
                  due_at=due_at, applied_at=timestamp, application_order=self._feedback_order,
                  sign=sign, magnitude=magnitude)
        self._feedback_order += 1

    def unavailable_branches(self) -> None:
        for name in (
            "queue_overflow_drop_failure", "duplicate_feedback", "rejected_feedback",
            "prediction_expiration", "prediction_settlement", "omission_resolution",
            "score_tie", "eligibility_expiration", "eligibility_consumption",
        ):
            if name not in self._branches_recorded:
                self.emit("branch_state", branch_name=name, evidence_state="EVIDENCE_UNAVAILABLE",
                          occurrence_count=None, occurrences=None)

    @staticmethod
    def _anchor(exposure_id: str, event: Any) -> dict[str, str] | None:
        event_id = getattr(event, "event_id", None)
        event_type = getattr(event, "event_type", None)
        event_type = getattr(event_type, "value", event_type)
        fields = {
            "exposure_id": exposure_id,
            "event_id": event_id,
            "source": getattr(event, "source", None),
            "destination": getattr(event, "destination", None),
            "event_type": event_type,
        }
        if any(not isinstance(value, str) or not value for value in fields.values()):
            return None
        return fields

    @staticmethod
    def _event_payload(event: Any) -> dict[str, Any]:
        event_type = getattr(event, "event_type", None)
        event_type = getattr(event_type, "value", event_type)
        return {
            "event_type": str(event_type),
            "payload": getattr(event, "payload", None),
            "timestamp": getattr(event, "timestamp", None),
            "queue_sequence": getattr(event, "sequence", None),
            "priority_key": [getattr(event, "timestamp", None), getattr(event, "sequence", None)],
        }

    @staticmethod
    def _pending_rows(pending: list[Any]) -> list[dict[str, Any]]:
        return [{"event_id": getattr(item, "event_id", None),
                 "source": getattr(item, "source", None),
                 "destination": getattr(item, "destination", None),
                 "event_type": getattr(getattr(item, "event_type", None), "value", getattr(item, "event_type", None)),
                 "timestamp": getattr(item, "timestamp", None),
                 "queue_sequence": getattr(item, "sequence", None)} for item in pending]

    def _terminal(self, queue: Any) -> None:
        self._terminal_snapshot(len(queue), queue.capacity, queue._snapshot())

    def before_next_event(self, queue: Any) -> bool:
        if self.pair_gate is None:
            return True
        event = queue.peek()
        anchor = self._anchor(self.writer.identity["exposure_id"], event)
        identity = None if anchor is None else encode_payload({
            "anchor": anchor, **self._event_payload(event)})
        if self.pair_gate.before_event(self.side, self.writer.identity["exposure_id"], identity):
            return True
        self._terminal(queue)
        self.unavailable_branches()
        return False

    def after_event(self) -> None:
        if self.pair_gate is not None:
            self.pair_gate.after_event(self.side)

    def finish(self, *, queue: Any) -> bool:
        if self.pair_gate is not None:
            self.pair_gate.finish_exposure(self.side)
            if self.pair_gate.stopped:
                self._terminal(queue)
                self.unavailable_branches()
                return False
        return True

    def execution_failed(self, queue: Any) -> None:
        if self.pair_gate is not None:
            self.pair_gate.stop(self.side, "event handler/runtime failure", None)
        self._terminal(queue)
        self.unavailable_branches()

    def queue_transition(self, operation: str, *, event: Any, occupancy_before: int,
                         occupancy_after: int, capacity: int, pending: list[Any],
                         queue_sequence: int | None = None, reason: str | None = None,
                         tie_break_cause: str | None = None) -> None:
        identity = self.writer.identity
        anchor = self._anchor(identity["exposure_id"], event)
        if operation == "queue_failure" and self.pair_gate is not None:
            self.pair_gate.stop(self.side, reason or "P11 queue failure", anchor)
        payload = self._event_payload(event)
        if operation == "enqueue":
            if anchor is None:
                self.gap("P02", "payload.anchor", "EventQueue.push", "event lacks a complete non-empty five-field P02 anchor")
            else:
                data = {"anchor": anchor, **payload, "enqueue_order": self._queue_order,
                        "queue_sequence": queue_sequence, "admission_outcome": "ADMITTED",
                        "occupancy_before": occupancy_before, "occupancy_after": occupancy_after}
                self.emit("enqueue", **data)
                self.emit("schedule", anchor=anchor, event_type=payload["event_type"],
                          payload=payload["payload"], timestamp=payload["timestamp"],
                          queue_sequence=queue_sequence, priority_key=payload["priority_key"],
                          tie_break_cause=None)
                self.emit("admission_decision", anchor=anchor, admission_outcome="ADMITTED",
                          occupancy_before=occupancy_before, occupancy_after=occupancy_after,
                          queue_sequence=queue_sequence)
            self._queue_order += 1
        elif operation == "queue_failure":
            admission_outcome = ("REJECTED_CAPACITY" if reason == "QueueCapacityError" else
                                 "REJECTED_INVALID" if reason == "ValueError" else "OTHER_FAILURE")
            if anchor is None:
                self.gap("P11", "payload.anchor", "EventQueue.push", f"failed event cannot be aligned: {reason}")
            else:
                rejected = {"anchor": anchor, "event_type": payload["event_type"],
                            "payload": payload["payload"], "timestamp": payload["timestamp"],
                            "enqueue_order": self._queue_order,
                            "queue_sequence": getattr(event, "sequence", None),
                            "priority_key": payload["priority_key"],
                            "admission_outcome": admission_outcome,
                            "occupancy_before": occupancy_before,
                            "occupancy_after": occupancy_after}
                self.emit("enqueue", **rejected)
                self.emit("admission_decision", anchor=anchor,
                          admission_outcome=admission_outcome,
                          occupancy_before=occupancy_before,
                          occupancy_after=occupancy_after, queue_sequence=getattr(event, "sequence", None))
                self.emit("queue_failure", anchor=anchor, occupancy=occupancy_before,
                          capacity=capacity, reason=reason or "unspecified")
                self.emit("branch_state", branch_name="queue_overflow_drop_failure",
                          evidence_state="MEASURED_POSITIVE", occurrence_count=1,
                          occurrences=[{"anchor": anchor, "reason": reason or "unspecified",
                                        "occupancy": occupancy_before, "capacity": capacity}])
                self._queue_order += 1
        elif operation == "dequeue":
            if anchor is None:
                self.gap("P02", "payload.anchor", "EventQueue.pop_ready", "dequeued event lacks a complete alignment anchor")
            else:
                self.emit("dequeue", anchor=anchor, event_type=payload["event_type"],
                          payload=payload["payload"], timestamp=payload["timestamp"],
                          queue_sequence=queue_sequence, priority_key=payload["priority_key"],
                          dequeue_order=self._queue_order,
                          tie_break_cause=tie_break_cause)
            self._queue_order += 1
        elif operation == "process":
            if anchor is None:
                self.gap("P02", "payload.anchor", "execute_bounded", "processed event lacks a complete alignment anchor")
            else:
                self.emit("process", anchor=anchor, event_type=payload["event_type"],
                          payload=payload["payload"], timestamp=payload["timestamp"],
                          queue_sequence=queue_sequence, process_order=self._process_order)
            self.emit("event_processed", event_id=getattr(event, "event_id", None),
                      processed_at=getattr(event, "timestamp", None),
                      process_order=self._process_order, processed_count=self._process_order + 1)
            self._process_order += 1
        if operation in {"enqueue", "dequeue", "process"}:
            self._last_operation = operation
        if operation in {"dequeue", "process"}:
            self._last_timestamp = getattr(event, "timestamp", self._last_timestamp)
        self.emit("queue_state", occupancy=occupancy_after, capacity=capacity,
                  pending=self._pending_rows(pending))
        if operation == "queue_failure":
            self._terminal_snapshot(occupancy_after, capacity, pending)
            self.unavailable_branches()
            if self.pair_gate is not None:
                self.pair_gate.stop(self.side, reason or "P11 queue failure", anchor)

    def _terminal_snapshot(self, occupancy: int, capacity: int, pending: list[Any]) -> None:
        if self._terminal_recorded:
            return
        self.emit("terminal_state", last_operation=self._last_operation,
                  timestamp=self._last_timestamp, occupancy=occupancy,
                  capacity=capacity, pending=self._pending_rows(pending))
        self._terminal_recorded = True
