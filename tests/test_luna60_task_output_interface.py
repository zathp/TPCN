from __future__ import annotations

from dataclasses import replace

import pytest

from experiments.task_output_interface import (
    CHANNEL_ID,
    SOURCE_ID,
    AggregateMetrics,
    ConfusionCell,
    OutcomeSubtype,
    TaskEvaluator,
    TaskPrediction,
    TaskWindow,
    TrialStatus,
    aggregate_metrics,
    map_emission,
    make_prediction_id,
)
from tpcn import (
    E1Config,
    Event,
    EventQueue,
    EventType,
    ExcursionEmission,
    MultiExcursionNeuron,
)


def make_window(
    *,
    trial: str = "trial-1",
    window: str = "window-1",
    start: float = 0.0,
    evidence: float = 2.0,
    deadline: float = 5.0,
    close: float = 8.0,
    max_emissions: int = 16,
    max_identities: int = 16,
    max_identifier_bytes: int = 128,
    max_identity_bytes: int = 1024,
) -> TaskWindow:
    return TaskWindow(
        trial,
        window,
        start,
        evidence,
        deadline,
        close,
        max_emissions=max_emissions,
        max_identities=max_identities,
        max_identifier_bytes=max_identifier_bytes,
        max_identity_bytes=max_identity_bytes,
    )


def emission(
    timestamp: float,
    sequence: int,
    *,
    event_id: str | None = None,
    source: str = SOURCE_ID,
    payload: float = 0.5,
    event_type: EventType = EventType.EXCURSION,
) -> ExcursionEmission:
    return ExcursionEmission(
        event_id=event_id or f"{source}:excursion:{sequence}",
        sequence=sequence,
        source=source,
        timestamp=timestamp,
        payload=payload,
        lineage_id=7,
        episode_id=sequence,
        event_type=event_type,
    )


def prediction(
    time: float,
    sequence: int,
    window: TaskWindow,
    *,
    payload: float = 0.5,
    event_id: str | None = None,
) -> TaskPrediction:
    mapped = map_emission(
        emission(
            time,
            sequence,
            event_id=event_id,
            payload=payload,
        ),
        window,
    )
    assert mapped is not None
    return mapped


def score(
    predictions: tuple[TaskPrediction, ...],
    *,
    truth: bool,
    target_time: float | None = None,
    window: TaskWindow | None = None,
):
    trial_window = window or make_window()
    evaluator = TaskEvaluator(trial_window)
    for item in predictions:
        assert evaluator.observe(item)
    return evaluator.finalize(
        observed_through=max(
            [trial_window.t_close]
            + [float(item.prediction_time) for item in predictions]
        ),
        pending_due_work=False,
        truncated=False,
        truth_occurred=truth,
        target_time=target_time,
    )


def _run_canonical_delayed_path(*, adapter_enabled: bool):
    """Fixture driver uses the real delayed neuron event queue, no classifier."""
    window = make_window()
    neuron = MultiExcursionNeuron(
        SOURCE_ID,
        config=E1Config(
            emission_delay=0.1,
            event_budget=64,
            provenance_capacity=16,
        ),
    )
    queue: EventQueue[Event] = EventQueue(16)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    mapped = []
    emissions = []
    while queue:
        next_event = queue.peek()
        assert next_event is not None
        event = queue.pop_ready(next_event.timestamp)
        result = neuron.receive_event(event, queue)
        if result is not None:
            emissions.append(result)
            if adapter_enabled:
                task_record = map_emission(result, window)
                if task_record is not None:
                    mapped.append(task_record)
    final_state = (
        neuron.x,
        neuron.integration_state,
        neuron.mode,
        neuron.pending_internal_event,
        tuple(neuron.emissions),
        neuron.processed_event_count,
        len(queue),
    )
    return tuple(emissions), tuple(mapped), final_state


def test_real_delayed_canonical_emission_maps_without_neural_interference() -> None:
    disabled = _run_canonical_delayed_path(adapter_enabled=False)
    enabled = _run_canonical_delayed_path(adapter_enabled=True)
    enabled_repeat = _run_canonical_delayed_path(adapter_enabled=True)

    assert len(disabled[0]) == 1
    canonical = disabled[0][0]
    assert canonical.source == SOURCE_ID
    assert canonical.event_type is EventType.EXCURSION
    assert canonical.timestamp > 0.0  # Delayed S_EMIT was actually processed.
    assert disabled[0] == enabled[0]
    assert enabled == enabled_repeat
    assert disabled[2] == enabled[2]
    assert disabled[1] == ()
    assert len(enabled[1]) == 1
    record = enabled[1][0]
    assert record.prediction_event_id == canonical.event_id
    assert record.prediction_time == canonical.timestamp
    assert record.emission_sequence == canonical.sequence
    assert record.predicts_occurrence is True
    # Routing and native prediction/error/eligibility/reward were not exercised.


def test_maps_only_destination_excursion_and_ignores_payload_sign() -> None:
    window = make_window()
    negative = map_emission(emission(3.0, 1, payload=-9.0), window)
    positive = map_emission(emission(3.0, 1, payload=+0.001), window)
    assert negative is not None and positive is not None
    assert negative.prediction_id == positive.prediction_id
    assert negative.prediction_event_id == positive.prediction_event_id
    assert negative.prediction_time == positive.prediction_time
    assert negative.emission_sequence == positive.emission_sequence
    assert negative.predicts_occurrence is positive.predicts_occurrence is True
    assert map_emission(emission(3.0, 1, source="relay"), window) is None
    assert (
        map_emission(
            emission(3.0, 1, event_type=EventType.SIGNAL),
            window,
        )
        is None
    )


@pytest.mark.parametrize(
    ("timestamp", "expected_subtype"),
    (
        (2.0, OutcomeSubtype.ON_TIME),  # evidence equality
        (5.0, OutcomeSubtype.ON_TIME),  # deadline equality
    ),
)
def test_positive_inclusive_evidence_and_deadline_boundaries(
    timestamp: float, expected_subtype: OutcomeSubtype
) -> None:
    window = make_window()
    result = score(
        (prediction(timestamp, 1, window),),
        truth=True,
        target_time=4.0,
        window=window,
    )
    assert result.status is TrialStatus.COMPLETE
    assert result.confusion_cell is ConfusionCell.TP
    assert result.subtype is expected_subtype


def test_close_equality_is_scored_and_outside_window_is_diagnostic_only() -> None:
    window = make_window()
    at_close = score(
        (prediction(window.t_close, 1, window),),
        truth=False,
        window=window,
    )
    assert at_close.confusion_cell is ConfusionCell.FP
    assert at_close.primary_prediction is not None
    assert at_close.primary_prediction.prediction_time == window.t_close
    assert at_close.subtype is OutcomeSubtype.LATE

    records = (
        prediction(-1.0, 1, window),
        prediction(3.0, 2, window),
        prediction(window.t_close + 1.0, 3, window),
    )
    result = score(records, truth=False, window=window)
    assert result.confusion_cell is ConfusionCell.FP
    assert result.primary_prediction == records[1]
    assert result.out_of_window_count == 2
    assert result.duplicate_count == 0


def test_first_premature_output_is_primary_and_on_time_later_output_is_duplicate() -> None:
    window = make_window()
    early = prediction(1.5, 1, window)
    later = prediction(3.0, 2, window)
    result = score((early, later), truth=True, target_time=4.0, window=window)
    assert result.confusion_cell is ConfusionCell.FN
    assert result.subtype is OutcomeSubtype.PREMATURE
    assert result.primary_prediction == early
    assert result.premature_count == 1
    assert result.duplicate_count == 1
    assert result.deadline_lead_time == 3.5
    assert result.target_relative_lead_time == 2.5


def test_first_late_output_is_not_rescued_and_chronological_order_is_enforced() -> None:
    window = make_window()
    late = prediction(5.5, 1, window)
    later_late_duplicate = prediction(6.0, 2, window)
    result = score(
        (late, later_late_duplicate),
        truth=True,
        target_time=4.0,
        window=window,
    )
    assert result.confusion_cell is ConfusionCell.FN
    assert result.subtype is OutcomeSubtype.LATE
    assert result.primary_prediction == late
    assert result.late_count == 2
    assert result.duplicate_count == 1
    assert result.deadline_lead_time is None
    assert result.signed_deadline_offset == 0.5
    assert result.target_relative_lead_time is None
    assert result.signed_target_relative_offset == -1.5

    # A chronologically later canonical output cannot have an earlier on-time
    # timestamp. The contradictory "late then on-time duplicate" sequence is
    # therefore rejected rather than silently reordered or used to rescue.
    evaluator = TaskEvaluator(window)
    evaluator.observe(late)
    with pytest.raises(ValueError, match="timestamps must be nondecreasing"):
        evaluator.observe(prediction(4.5, 2, window))


def test_negative_emission_is_false_positive_and_negative_silence_is_tn_only_at_close() -> None:
    window = make_window()
    false_positive = score(
        (prediction(3.0, 1, window),),
        truth=False,
        window=window,
    )
    assert false_positive.confusion_cell is ConfusionCell.FP
    assert false_positive.subtype is OutcomeSubtype.FALSE_POSITIVE

    evaluator = TaskEvaluator(window)
    censored = evaluator.finalize(
        observed_through=window.t_close - 0.01,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert censored.status is TrialStatus.INCOMPLETE
    assert censored.confusion_cell is None
    assert censored.subtype is OutcomeSubtype.CENSORED
    assert censored.silent_miss_count == 0

    complete = TaskEvaluator(window).finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert complete.status is TrialStatus.COMPLETE
    assert complete.confusion_cell is ConfusionCell.TN
    assert complete.subtype is OutcomeSubtype.TRUE_NEGATIVE


def test_positive_silence_is_fn_only_after_complete_close() -> None:
    window = make_window()
    censored = TaskEvaluator(window).finalize(
        observed_through=window.t_deadline,
        pending_due_work=True,
        truncated=True,
        truth_occurred=True,
        target_time=4.0,
    )
    assert censored.status is TrialStatus.INCOMPLETE
    assert censored.confusion_cell is None
    assert censored.silent_miss_count == 0

    complete = TaskEvaluator(window).finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=True,
        target_time=4.0,
    )
    assert complete.confusion_cell is ConfusionCell.FN
    assert complete.subtype is OutcomeSubtype.SILENT_MISSED
    assert complete.silent_miss_count == 1


def test_completion_boundary_must_cover_every_observed_emission_time() -> None:
    window = make_window()
    evaluator = TaskEvaluator(window)
    evaluator.observe(prediction(window.t_close + 1.0, 1, window))
    result = evaluator.finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert result.status is TrialStatus.INCOMPLETE
    assert result.confusion_cell is None
    assert any(
        "precedes a recorded emission" in reason
        for reason in result.incomplete_reasons
    )


def test_truth_is_evaluator_only_and_target_time_must_match_truth_window() -> None:
    window = make_window()
    evaluator = TaskEvaluator(window)
    with pytest.raises(ValueError, match="evidence/deadline"):
        evaluator.finalize(
            observed_through=window.t_close,
            pending_due_work=False,
            truncated=False,
            truth_occurred=True,
            target_time=window.t_close,
        )
    with pytest.raises(ValueError, match="must not supply"):
        TaskEvaluator(window).finalize(
            observed_through=window.t_close,
            pending_due_work=False,
            truncated=False,
            truth_occurred=False,
            target_time=3.0,
        )


def test_positive_truth_without_target_time_scores_and_omits_target_lead() -> None:
    window = make_window()
    result = score(
        (prediction(3.0, 1, window),),
        truth=True,
        target_time=None,
        window=window,
    )

    assert result.status is TrialStatus.COMPLETE
    assert result.confusion_cell is ConfusionCell.TP
    assert result.subtype is OutcomeSubtype.ON_TIME
    assert result.deadline_lead_time == 2.0
    assert result.signed_deadline_offset == -2.0
    assert result.target_relative_lead_time is None
    assert result.signed_target_relative_offset is None


def test_ambiguous_prefix_outputs_are_truth_blind_and_prefix_silence_waits_for_close() -> None:
    window = make_window()
    prefix = (prediction(1.0, 1, window),)
    positive_prefix = score(prefix, truth=True, target_time=4.0, window=window)
    negative_prefix = score(prefix, truth=False, window=window)
    assert positive_prefix.predictions == negative_prefix.predictions == prefix
    assert positive_prefix.confusion_cell is ConfusionCell.FN
    assert positive_prefix.subtype is OutcomeSubtype.PREMATURE
    assert negative_prefix.confusion_cell is ConfusionCell.FP
    assert negative_prefix.subtype is OutcomeSubtype.PREMATURE

    continued_silence = TaskEvaluator(window).finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert continued_silence.confusion_cell is ConfusionCell.TN


def test_identical_input_truth_swap_changes_scores_never_mapped_outputs() -> None:
    window = make_window()
    inputs = (emission(3.0, 1), emission(4.0, 2, payload=-2.0))
    mapped = tuple(map_emission(item, window) for item in inputs)
    assert all(item is not None for item in mapped)
    affirmative = tuple(item for item in mapped if item is not None)

    positive_eval = TaskEvaluator(window)
    negative_eval = TaskEvaluator(window)
    for item in affirmative:
        positive_eval.observe(item)
        negative_eval.observe(item)
    positive = positive_eval.finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=True,
        target_time=4.5,
    )
    negative = negative_eval.finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert positive.predictions == negative.predictions == affirmative
    assert positive.confusion_cell is ConfusionCell.TP
    assert negative.confusion_cell is ConfusionCell.FP
    assert positive.primary_prediction == negative.primary_prediction


def test_exact_reobservation_is_idempotent_but_conflicting_content_fails() -> None:
    window = make_window()
    original_emission = emission(3.0, 1, payload=0.25)
    original = map_emission(original_emission, window)
    assert original is not None
    evaluator = TaskEvaluator(window)
    assert evaluator.observe(original) is True
    assert evaluator.observe(original) is False
    assert evaluator.buffered_prediction_count == 1

    changed_emission = replace(original_emission, payload=-0.25)
    conflicting = map_emission(changed_emission, window)
    assert conflicting is not None
    with pytest.raises(ValueError, match="conflicting content"):
        evaluator.observe(conflicting)


def test_prediction_identity_is_injective_and_trial_window_namespaced() -> None:
    # Delimiters in components cannot alias because each component is encoded.
    first = make_prediction_id("a/b", "c", CHANNEL_ID, "d")
    second = make_prediction_id("a", "b/c", CHANNEL_ID, "d")
    assert first != second
    assert first != make_prediction_id("a/b", "c2", CHANNEL_ID, "d")

    first_window = make_window(trial="trial-A", window="window")
    second_window = make_window(trial="trial-B", window="window")
    first_prediction = prediction(3.0, 1, first_window, event_id="same-event")
    second_prediction = prediction(3.0, 1, second_window, event_id="same-event")
    assert first_prediction.prediction_id != second_prediction.prediction_id


def test_canonical_order_and_equal_time_sequence_tie_break_are_validated() -> None:
    window = make_window()
    earlier_sequence = prediction(3.0, 1, window, event_id="dest:excursion:1")
    later_sequence = prediction(3.0, 2, window, event_id="dest:excursion:2")
    evaluator = TaskEvaluator(window)
    assert evaluator.observe(earlier_sequence)
    assert evaluator.observe(later_sequence)
    result = evaluator.finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert result.primary_prediction == earlier_sequence
    assert result.predictions == (earlier_sequence, later_sequence)
    assert result.duplicate_count == 1

    out_of_order = TaskEvaluator(window)
    out_of_order.observe(later_sequence)
    with pytest.raises(ValueError, match="sequence must be strictly increasing"):
        out_of_order.observe(earlier_sequence)

    duplicate_sequence = TaskEvaluator(window)
    duplicate_sequence.observe(earlier_sequence)
    with pytest.raises(ValueError, match="share a source sequence"):
        duplicate_sequence.observe(
            prediction(3.5, 1, window, event_id="different-event")
        )


def test_reset_releases_trial_state_and_requires_new_trial_window() -> None:
    first_window = make_window()
    evaluator = TaskEvaluator(first_window)
    evaluator.observe(prediction(3.0, 1, first_window))
    evaluator.finalize(
        observed_through=first_window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert evaluator.buffered_prediction_count == 0
    with pytest.raises(RuntimeError, match="closed"):
        evaluator.observe(prediction(3.0, 1, first_window))
    with pytest.raises(ValueError, match="new trial/window identity"):
        evaluator.reset(first_window)

    second_window = make_window(trial="trial-2", window="window-2")
    evaluator.reset(second_window)
    assert evaluator.buffered_prediction_count == 0
    assert evaluator.observe(prediction(3.0, 1, second_window))


def test_capacity_overflow_is_bounded_and_marks_trial_incomplete() -> None:
    window = make_window(max_emissions=1, max_identities=1)
    evaluator = TaskEvaluator(window)
    assert evaluator.observe(prediction(3.0, 1, window))
    assert evaluator.observe(prediction(3.5, 2, window)) is False
    assert evaluator.overflowed
    assert evaluator.buffered_prediction_count == 1
    result = evaluator.finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert result.status is TrialStatus.INCOMPLETE
    assert result.confusion_cell is None
    assert "capacity exhausted" in result.incomplete_reasons[-1]


def test_identity_capacity_exhaustion_is_distinct_and_censors_trial() -> None:
    window = make_window(max_emissions=3, max_identities=1)
    evaluator = TaskEvaluator(window)
    assert evaluator.observe(prediction(3.0, 1, window))
    assert evaluator.observe(prediction(3.5, 2, window)) is False
    assert evaluator.overflowed
    assert evaluator.buffered_prediction_count == 1
    result = evaluator.finalize(
        observed_through=window.t_close,
        pending_due_work=False,
        truncated=False,
        truth_occurred=False,
    )
    assert result.status is TrialStatus.INCOMPLETE
    assert result.confusion_cell is None


def test_task_prediction_window_mismatch_and_identity_byte_limit_reject() -> None:
    first_window = make_window()
    second_window = make_window(trial="trial-other")
    mapped = prediction(3.0, 1, first_window)
    with pytest.raises(ValueError, match="metadata"):
        TaskEvaluator(second_window).observe(mapped)

    small_identity_window = make_window(max_identity_bytes=32)
    with pytest.raises(ValueError, match="identity-byte limit"):
        map_emission(emission(3.0, 1), small_identity_window)


@pytest.mark.parametrize(
    "kwargs",
    (
        {"start": 3.0, "evidence": 2.0, "deadline": 5.0, "close": 8.0},
        {"start": 0.0, "evidence": 6.0, "deadline": 5.0, "close": 8.0},
        {"start": 0.0, "evidence": 2.0, "deadline": 8.0, "close": 8.0},
        {"start": float("nan")},
        {"deadline": float("inf")},
        {"max_emissions": 0},
        {"max_emissions": 1, "max_identities": 2},
        {"max_identifier_bytes": 257},
    ),
)
def test_window_metadata_order_finiteness_and_capacity_rejection(kwargs) -> None:
    with pytest.raises((TypeError, ValueError)):
        make_window(**kwargs)


def test_extreme_finite_numeric_type_that_overflows_float_is_rejected() -> None:
    with pytest.raises(ValueError, match="must be finite"):
        make_window(start=10**400)


def test_identifier_length_and_invalid_emission_time_are_rejected() -> None:
    window = make_window(max_identifier_bytes=16, max_identity_bytes=256)
    with pytest.raises(ValueError, match="identifier limit"):
        map_emission(emission(3.0, 1, event_id="x" * 17), window)
    with pytest.raises(ValueError, match="timestamp must be finite"):
        map_emission(emission(float("nan"), 1), make_window())


def test_metrics_use_one_cell_per_complete_trial_and_n_a_zero_denominators() -> None:
    window = make_window()
    outcomes = (
        score((prediction(3.0, 1, window),), truth=True, target_time=4.0, window=window),
        score((), truth=True, target_time=4.0, window=window),
        score((), truth=False, window=window),
        score((prediction(3.5, 1, window),), truth=False, window=window),
    )
    censored = TaskEvaluator(window).finalize(
        observed_through=window.t_close - 1,
        pending_due_work=True,
        truncated=False,
        truth_occurred=False,
    )
    metrics = aggregate_metrics((*outcomes, censored))
    assert isinstance(metrics, AggregateMetrics)
    assert (metrics.tp, metrics.fn, metrics.tn, metrics.fp) == (1, 1, 1, 1)
    assert metrics.complete_trials == 4
    assert metrics.excluded_incomplete_trials == 1
    assert metrics.positive_denominator == 2
    assert metrics.negative_denominator == 2
    assert metrics.balanced_accuracy == 0.5
    assert metrics.tpr == 0.5
    assert metrics.fnr == 0.5
    assert metrics.fpr == 0.5

    only_positives = aggregate_metrics(outcomes[:2])
    assert only_positives.negative_denominator == 0
    assert only_positives.fpr is None
    assert only_positives.balanced_accuracy is None
    assert only_positives.tpr == 0.5
    assert only_positives.fnr == 0.5
    assert aggregate_metrics(()).balanced_accuracy is None
    assert aggregate_metrics(()).tpr is None
    assert aggregate_metrics(()).fpr is None
