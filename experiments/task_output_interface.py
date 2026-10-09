"""Truth-blind task output mapping and bounded event-time evaluation.

This module is deliberately downstream of the neural runtime.  It maps only
the existing canonical ``destination`` EXCURSION emission; it does not emit,
schedule, route, or reward anything.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from numbers import Real
from typing import Iterable

from tpcn import EventType, ExcursionEmission


CHANNEL_ID = "target-before-deadline"
SOURCE_ID = "destination"
TARGET_TYPE = "designated-target-event"
SCHEMA_REVISION = 1

# These hard ceilings make the per-trial limits finite even when the caller
# constructs its own TaskWindow.  They are software interface bounds, not
# scientific task values.
MAX_EMISSIONS_PER_TRIAL = 4096
MAX_IDENTITIES_PER_TRIAL = 4096
MAX_IDENTIFIER_BYTES = 256
MAX_TASK_IDENTITY_BYTES = 2048


class TrialStatus(str, Enum):
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE/CENSORED"


class ConfusionCell(str, Enum):
    TP = "TP"
    FN = "FN"
    TN = "TN"
    FP = "FP"


class OutcomeSubtype(str, Enum):
    ON_TIME = "ON-TIME"
    PREMATURE = "PREMATURE"
    LATE = "LATE"
    SILENT_MISSED = "SILENT/MISSED"
    FALSE_POSITIVE = "FALSE-POSITIVE"
    TRUE_NEGATIVE = "TRUE-NEGATIVE"
    CENSORED = "CENSORED"


def _finite_time(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a finite real number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be finite") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _bounded_identifier(value: object, name: str, *, limit: int = MAX_IDENTIFIER_BYTES) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{name} must be a non-empty string")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise ValueError(f"{name} is not valid UTF-8 text") from exc
    if size > limit:
        raise ValueError(f"{name} exceeds the {limit}-byte identifier limit")
    return value


def _positive_integer(value: object, name: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value <= 0 or value > maximum:
        raise ValueError(f"{name} must be between 1 and {maximum}")
    return value


def _encode_component(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii").rstrip("=")


def make_prediction_id(
    trial_id: str,
    evaluation_window_id: str,
    channel_id: str,
    prediction_event_id: str,
) -> str:
    """Return an injective, versioned encoding of the four identity fields."""
    components = (trial_id, evaluation_window_id, channel_id, prediction_event_id)
    for index, component in enumerate(components):
        _bounded_identifier(component, f"identity component {index}")
    result = "taskpred-v1:" + ".".join(
        _encode_component(part) for part in components
    )
    if len(result.encode("utf-8")) > MAX_TASK_IDENTITY_BYTES:
        raise ValueError("prediction identity exceeds the hard byte limit")
    return result


@dataclass(frozen=True, slots=True)
class TaskWindow:
    """Frozen evaluator metadata and finite per-trial storage bounds."""

    trial_id: str
    evaluation_window_id: str
    t_start: float
    t_evidence: float
    t_deadline: float
    t_close: float
    time_unit: str = "logical"
    max_emissions: int = 256
    max_identities: int = 256
    max_identifier_bytes: int = 128
    max_identity_bytes: int = 1024

    def __post_init__(self) -> None:
        _bounded_identifier(self.trial_id, "trial_id", limit=MAX_IDENTIFIER_BYTES)
        _bounded_identifier(
            self.evaluation_window_id,
            "evaluation_window_id",
            limit=MAX_IDENTIFIER_BYTES,
        )
        _bounded_identifier(
            self.time_unit,
            "time_unit",
            limit=MAX_IDENTIFIER_BYTES,
        )
        for name in ("t_start", "t_evidence", "t_deadline", "t_close"):
            _finite_time(getattr(self, name), name)
        if not (
            self.t_start
            <= self.t_evidence
            <= self.t_deadline
            < self.t_close
        ):
            raise ValueError(
                "window order must satisfy t_start <= t_evidence <= "
                "t_deadline < t_close"
            )
        _positive_integer(
            self.max_emissions, "max_emissions", MAX_EMISSIONS_PER_TRIAL
        )
        _positive_integer(
            self.max_identities, "max_identities", MAX_IDENTITIES_PER_TRIAL
        )
        if self.max_identities > self.max_emissions:
            raise ValueError("max_identities cannot exceed max_emissions")
        _positive_integer(
            self.max_identifier_bytes,
            "max_identifier_bytes",
            MAX_IDENTIFIER_BYTES,
        )
        _positive_integer(
            self.max_identity_bytes,
            "max_identity_bytes",
            MAX_TASK_IDENTITY_BYTES,
        )
        for name in ("trial_id", "evaluation_window_id", "time_unit"):
            _bounded_identifier(
                getattr(self, name),
                name,
                limit=self.max_identifier_bytes,
            )


@dataclass(frozen=True, slots=True)
class TaskPrediction:
    """Schema-revision-1 affirmative task record mapped from one emission."""

    trial_id: str
    evaluation_window_id: str
    channel_id: str
    source_id: str
    prediction_event_id: str
    prediction_time: float
    emission_sequence: int
    target_type: str
    predicts_occurrence: bool
    prediction_id: str
    # This opaque digest is solely an identity-integrity check.  It is not
    # available to scoring logic and cannot affect whether an output exists.
    _canonical_content_digest: str = field(repr=False)
    schema_revision: int = SCHEMA_REVISION


def _emission_content_digest(emission: ExcursionEmission) -> str:
    content = (
        emission.event_id,
        emission.sequence,
        emission.source,
        float(emission.timestamp).hex(),
        float(emission.payload).hex(),
        emission.lineage_id,
        emission.episode_id,
        getattr(emission.event_type, "value", str(emission.event_type)),
    )
    encoded = json.dumps(content, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def map_emission(
    emission: ExcursionEmission, window: TaskWindow
) -> TaskPrediction | None:
    """Map an actual designated-source EXCURSION to affirmative prediction.

    Wrong-source and non-EXCURSION emissions return ``None``.  Payload,
    lineage, truth, neural state, and future input never select or suppress an
    affirmative output.  The private digest detects conflicting re-observation
    of a canonical identity without exposing payload to evaluation.
    """
    if not isinstance(emission, ExcursionEmission):
        raise TypeError("emission must be an ExcursionEmission")
    if not isinstance(window, TaskWindow):
        raise TypeError("window must be a TaskWindow")
    if emission.source != SOURCE_ID or emission.event_type != EventType.EXCURSION:
        return None
    event_id = _bounded_identifier(
        emission.event_id, "emission.event_id", limit=window.max_identifier_bytes
    )
    timestamp = _finite_time(emission.timestamp, "emission.timestamp")
    if isinstance(emission.sequence, bool) or not isinstance(emission.sequence, int):
        raise TypeError("emission.sequence must be an integer")
    if emission.sequence <= 0:
        raise ValueError("emission.sequence must be positive")
    prediction_id = make_prediction_id(
        window.trial_id,
        window.evaluation_window_id,
        CHANNEL_ID,
        event_id,
    )
    if len(prediction_id.encode("utf-8")) > window.max_identity_bytes:
        raise ValueError("prediction_id exceeds the declared identity-byte limit")
    return TaskPrediction(
        trial_id=window.trial_id,
        evaluation_window_id=window.evaluation_window_id,
        channel_id=CHANNEL_ID,
        source_id=SOURCE_ID,
        prediction_event_id=event_id,
        prediction_time=emission.timestamp,
        emission_sequence=emission.sequence,
        target_type=TARGET_TYPE,
        predicts_occurrence=True,
        prediction_id=prediction_id,
        _canonical_content_digest=_emission_content_digest(emission),
    )


def _validate_prediction(prediction: TaskPrediction, window: TaskWindow) -> None:
    if not isinstance(prediction, TaskPrediction):
        raise TypeError("prediction must be a TaskPrediction")
    if (
        prediction.trial_id != window.trial_id
        or prediction.evaluation_window_id != window.evaluation_window_id
        or prediction.channel_id != CHANNEL_ID
        or prediction.source_id != SOURCE_ID
        or prediction.target_type != TARGET_TYPE
        or prediction.predicts_occurrence is not True
        or prediction.schema_revision != SCHEMA_REVISION
    ):
        raise ValueError("TaskPrediction metadata does not match its frozen window")
    _bounded_identifier(
        prediction.prediction_event_id,
        "prediction_event_id",
        limit=window.max_identifier_bytes,
    )
    _finite_time(prediction.prediction_time, "prediction_time")
    if (
        isinstance(prediction.emission_sequence, bool)
        or not isinstance(prediction.emission_sequence, int)
        or prediction.emission_sequence <= 0
    ):
        raise ValueError("emission_sequence must be a positive integer")
    expected_id = make_prediction_id(
        prediction.trial_id,
        prediction.evaluation_window_id,
        prediction.channel_id,
        prediction.prediction_event_id,
    )
    if prediction.prediction_id != expected_id:
        raise ValueError("prediction_id does not encode the frozen identity tuple")
    if len(expected_id.encode("utf-8")) > window.max_identity_bytes:
        raise ValueError("prediction_id exceeds the declared identity-byte limit")
    if (
        not isinstance(prediction._canonical_content_digest, str)
        or len(prediction._canonical_content_digest) != 64
    ):
        raise ValueError("canonical emission integrity digest is malformed")


@dataclass(frozen=True, slots=True)
class TrialResult:
    trial_id: str
    evaluation_window_id: str
    status: TrialStatus
    truth_occurred: bool
    observed_through: float
    confusion_cell: ConfusionCell | None
    subtype: OutcomeSubtype
    primary_prediction: TaskPrediction | None
    predictions: tuple[TaskPrediction, ...]
    out_of_window_count: int
    premature_count: int
    late_count: int
    duplicate_count: int
    silent_miss_count: int
    deadline_lead_time: float | None
    signed_deadline_offset: float | None
    target_relative_lead_time: float | None
    signed_target_relative_offset: float | None
    incomplete_reasons: tuple[str, ...]


class TaskEvaluator:
    """Bounded, trial-local event-time evaluator; never feeds labels upstream."""

    def __init__(self, window: TaskWindow) -> None:
        if not isinstance(window, TaskWindow):
            raise TypeError("window must be a TaskWindow")
        self.window = window
        self._predictions: list[TaskPrediction] = []
        self._by_identity: dict[str, TaskPrediction] = {}
        self._sequence_ids: dict[int, str] = {}
        self._last_time: float | None = None
        self._last_sequence: int | None = None
        self._overflow = False
        self._closed = False

    @property
    def buffered_prediction_count(self) -> int:
        return len(self._predictions)

    @property
    def overflowed(self) -> bool:
        return self._overflow

    def observe(self, prediction: TaskPrediction) -> bool:
        """Store a distinct mapped output, or mark finite-capacity censoring.

        Exact re-observation is idempotent and returns ``False``.  Capacity
        exhaustion does not raise into or backpressure neural execution; it
        marks this external trial incomplete and stores nothing further.
        """
        if self._closed:
            raise RuntimeError("trial evaluator is closed; reset before reuse")
        _validate_prediction(prediction, self.window)
        previous = self._by_identity.get(prediction.prediction_id)
        if previous is not None:
            if previous != prediction:
                raise ValueError(
                    "conflicting content for an already observed emission identity"
                )
            return False
        prior_sequence_id = self._sequence_ids.get(prediction.emission_sequence)
        if prior_sequence_id is not None:
            raise ValueError(
                "distinct emission identities cannot share a source sequence"
            )
        timestamp = float(prediction.prediction_time)
        if self._last_time is not None and timestamp < self._last_time:
            raise ValueError("canonical emission timestamps must be nondecreasing")
        if (
            self._last_sequence is not None
            and prediction.emission_sequence <= self._last_sequence
        ):
            raise ValueError("canonical emission sequence must be strictly increasing")
        if len(self._predictions) >= self.window.max_emissions:
            self._overflow = True
            return False
        if len(self._by_identity) >= self.window.max_identities:
            self._overflow = True
            return False
        self._predictions.append(prediction)
        self._by_identity[prediction.prediction_id] = prediction
        self._sequence_ids[prediction.emission_sequence] = prediction.prediction_id
        self._last_time = timestamp
        self._last_sequence = prediction.emission_sequence
        return True

    def finalize(
        self,
        *,
        observed_through: float,
        pending_due_work: bool,
        truncated: bool,
        truth_occurred: bool,
        target_time: float | None = None,
    ) -> TrialResult:
        """Finalize from external completion evidence; no neural tick is used."""
        if self._closed:
            raise RuntimeError("trial evaluator is already closed")
        observed = _finite_time(observed_through, "observed_through")
        if not isinstance(pending_due_work, bool) or not isinstance(truncated, bool):
            raise TypeError("pending_due_work and truncated must be bool")
        if not isinstance(truth_occurred, bool):
            raise TypeError("truth_occurred must be bool")
        if truth_occurred:
            if target_time is not None:
                target = _finite_time(target_time, "target_time")
                if not self.window.t_evidence <= target <= self.window.t_deadline:
                    raise ValueError(
                        "target_time must lie in the evidence/deadline interval"
                    )
        elif target_time is not None:
            raise ValueError("negative truth must not supply a target_time")

        reasons: list[str] = []
        if observed < self.window.t_close:
            reasons.append("observation did not reach t_close")
        if self._predictions and max(
            float(item.prediction_time) for item in self._predictions
        ) > observed:
            reasons.append("observation boundary precedes a recorded emission")
        if pending_due_work:
            reasons.append("pending due work")
        if truncated:
            reasons.append("observation truncated")
        if self._overflow:
            reasons.append("finite observation/identity capacity exhausted")
        complete = not reasons

        ordered = tuple(self._predictions)
        scoring_predictions = tuple(
            item
            for item in ordered
            if self.window.t_start
            <= item.prediction_time
            <= self.window.t_close
        )
        out_of_window_count = len(ordered) - len(scoring_predictions)
        premature_count = sum(
            item.prediction_time < self.window.t_evidence
            for item in scoring_predictions
        )
        late_count = sum(
            item.prediction_time > self.window.t_deadline
            for item in scoring_predictions
        )
        primary = scoring_predictions[0] if scoring_predictions else None
        duplicate_count = max(0, len(scoring_predictions) - 1)

        cell: ConfusionCell | None = None
        subtype = OutcomeSubtype.CENSORED
        silent_miss_count = 0
        if complete:
            if truth_occurred:
                if primary is not None and (
                    self.window.t_evidence
                    <= primary.prediction_time
                    <= self.window.t_deadline
                ):
                    cell = ConfusionCell.TP
                    subtype = OutcomeSubtype.ON_TIME
                else:
                    cell = ConfusionCell.FN
                    if primary is None:
                        subtype = OutcomeSubtype.SILENT_MISSED
                        silent_miss_count = 1
                    elif primary.prediction_time < self.window.t_evidence:
                        subtype = OutcomeSubtype.PREMATURE
                    else:
                        subtype = OutcomeSubtype.LATE
            elif primary is None:
                cell = ConfusionCell.TN
                subtype = OutcomeSubtype.TRUE_NEGATIVE
            else:
                cell = ConfusionCell.FP
                if primary.prediction_time < self.window.t_evidence:
                    subtype = OutcomeSubtype.PREMATURE
                elif primary.prediction_time > self.window.t_deadline:
                    subtype = OutcomeSubtype.LATE
                else:
                    subtype = OutcomeSubtype.FALSE_POSITIVE

        deadline_lead: float | None = None
        signed_deadline_offset: float | None = None
        target_lead: float | None = None
        signed_target_offset: float | None = None
        if primary is not None:
            signed_deadline_offset = primary.prediction_time - self.window.t_deadline
            if signed_deadline_offset <= 0:
                deadline_lead = -signed_deadline_offset
            if truth_occurred and target_time is not None:
                signed_target_offset = target_time - primary.prediction_time
                if signed_target_offset >= 0:
                    target_lead = signed_target_offset

        result = TrialResult(
            trial_id=self.window.trial_id,
            evaluation_window_id=self.window.evaluation_window_id,
            status=TrialStatus.COMPLETE if complete else TrialStatus.INCOMPLETE,
            truth_occurred=truth_occurred,
            observed_through=observed,
            confusion_cell=cell,
            subtype=subtype,
            primary_prediction=primary,
            predictions=ordered,
            out_of_window_count=out_of_window_count,
            premature_count=premature_count,
            late_count=late_count,
            duplicate_count=duplicate_count,
            silent_miss_count=silent_miss_count,
            deadline_lead_time=deadline_lead,
            signed_deadline_offset=signed_deadline_offset,
            target_relative_lead_time=target_lead,
            signed_target_relative_offset=signed_target_offset,
            incomplete_reasons=tuple(reasons),
        )
        self._clear()
        self._closed = True
        return result

    def reset(self, window: TaskWindow) -> None:
        """Start a fresh trial after close, releasing all prior trial storage."""
        if not self._closed:
            raise RuntimeError("reset is allowed only after trial finalization")
        if not isinstance(window, TaskWindow):
            raise TypeError("window must be a TaskWindow")
        if (
            window.trial_id == self.window.trial_id
            and window.evaluation_window_id == self.window.evaluation_window_id
        ):
            raise ValueError("reset requires a new trial/window identity")
        self.window = window
        self._clear()
        self._closed = False

    def _clear(self) -> None:
        self._predictions.clear()
        self._by_identity.clear()
        self._sequence_ids.clear()
        self._last_time = None
        self._last_sequence = None
        self._overflow = False


@dataclass(frozen=True, slots=True)
class AggregateMetrics:
    tp: int
    fn: int
    tn: int
    fp: int
    complete_trials: int
    excluded_incomplete_trials: int
    positive_denominator: int
    negative_denominator: int
    balanced_accuracy: float | None
    tpr: float | None
    fnr: float | None
    fpr: float | None
    premature_count: int
    late_count: int
    silent_miss_count: int
    out_of_window_count: int
    duplicate_count: int
    deadline_lead_time_samples: int
    target_relative_lead_time_samples: int
    signed_deadline_offset_samples: int
    signed_target_relative_offset_samples: int


def aggregate_metrics(results: Iterable[TrialResult]) -> AggregateMetrics:
    """Summarize complete trials only; undefined rates are explicit ``None``."""
    tp = fn = tn = fp = complete = excluded = 0
    premature = late = silent = out_of_window = duplicates = 0
    deadline_samples = target_samples = 0
    signed_deadline_samples = signed_target_samples = 0
    for result in results:
        if not isinstance(result, TrialResult):
            raise TypeError("results must contain TrialResult records")
        if result.status == TrialStatus.INCOMPLETE:
            excluded += 1
            continue
        complete += 1
        if result.confusion_cell == ConfusionCell.TP:
            tp += 1
        elif result.confusion_cell == ConfusionCell.FN:
            fn += 1
        elif result.confusion_cell == ConfusionCell.TN:
            tn += 1
        elif result.confusion_cell == ConfusionCell.FP:
            fp += 1
        else:
            raise ValueError("complete trial lacks exactly one confusion-matrix cell")
        premature += result.premature_count
        late += result.late_count
        silent += result.silent_miss_count
        out_of_window += result.out_of_window_count
        duplicates += result.duplicate_count
        deadline_samples += result.deadline_lead_time is not None
        target_samples += result.target_relative_lead_time is not None
        signed_deadline_samples += result.signed_deadline_offset is not None
        signed_target_samples += result.signed_target_relative_offset is not None

    positive_denominator = tp + fn
    negative_denominator = tn + fp
    tpr = tp / positive_denominator if positive_denominator else None
    fnr = fn / positive_denominator if positive_denominator else None
    fpr = fp / negative_denominator if negative_denominator else None
    balanced = (
        (tpr + tn / negative_denominator) / 2.0
        if positive_denominator and negative_denominator
        else None
    )
    return AggregateMetrics(
        tp=tp,
        fn=fn,
        tn=tn,
        fp=fp,
        complete_trials=complete,
        excluded_incomplete_trials=excluded,
        positive_denominator=positive_denominator,
        negative_denominator=negative_denominator,
        balanced_accuracy=balanced,
        tpr=tpr,
        fnr=fnr,
        fpr=fpr,
        premature_count=premature,
        late_count=late,
        silent_miss_count=silent,
        out_of_window_count=out_of_window,
        duplicate_count=duplicates,
        deadline_lead_time_samples=deadline_samples,
        target_relative_lead_time_samples=target_samples,
        signed_deadline_offset_samples=signed_deadline_samples,
        signed_target_relative_offset_samples=signed_target_samples,
    )
