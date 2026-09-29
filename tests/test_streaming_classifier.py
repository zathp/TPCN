import pytest

from tpcn import (
    ACTIVITY_EVENT,
    CharacterBoundary,
    END_CHARACTER,
    END_STROKE,
    Event,
    START_CHARACTER,
    StreamingCharacterClassifier,
    TPCNNeuron,
)


def boundary(event_type: str, timestamp: float, index: int, sequence: int) -> Event:
    return Event(timestamp, "stream", "readout", event_type,
                 CharacterBoundary(index), sequence)


def activity(timestamp: float, value: float, sequence: int) -> Event:
    return Event(timestamp, "neuron-0", "readout", ACTIVITY_EVENT, value, sequence)


def run_stream(label: str | None) -> tuple[tuple[float, ...], str, tuple[float, ...]]:
    classifier = StreamingCharacterClassifier()
    events = (
        boundary(START_CHARACTER, 0.0, 2, 0),
        activity(0.0, 0.5, 1),
        activity(0.5, -0.25, 2),
        boundary(END_CHARACTER, 1.0, 2, 3),
    )
    evidence = []
    for event in events[:-1]:
        result = classifier.ingest_event(event)
        if result is not None and hasattr(result, "probabilities"):
            evidence.append(result.probabilities)
    result = classifier.ingest_event(events[-1])
    assert result is not None
    assert label in (None, "A", "Z")
    return evidence[0], result.label, result.scores


def test_classifier_exposes_exactly_26_a_to_z_outputs() -> None:
    classifier = StreamingCharacterClassifier()

    assert classifier.class_labels == tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert len(classifier.class_labels) == 26


def test_no_authoritative_result_before_end_character() -> None:
    classifier = StreamingCharacterClassifier()

    assert classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 0)) is None
    assert classifier.ingest_event(activity(0.0, 1.0, 1)) is not None
    assert classifier.authoritative_result is None


def test_end_stroke_is_not_character_finalization() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 0))

    evidence = classifier.ingest_event(Event(0.5, "stream", "readout", END_STROKE, None, 1))

    assert evidence is not None
    assert classifier.is_active
    assert classifier.authoritative_result is None


def test_completed_character_emits_exactly_one_result_with_identity_and_time() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 2.0, 7, 11))
    classifier.ingest_event(activity(2.5, 1.0, 12))

    result = classifier.ingest_event(boundary(END_CHARACTER, 3.0, 7, 13))

    assert result is not None
    assert result.character_index == 7
    assert len(result.probabilities) == 26
    assert (result.start_timestamp, result.end_timestamp) == (2.0, 3.0)
    assert (result.start_sequence, result.end_sequence) == (11, 13)
    assert classifier.authoritative_result == result


def test_stale_direct_finalization_is_atomic_and_does_not_poison_time() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 3, 0))
    classifier.ingest_event(activity(8.0, 1.0, 1))
    before = (
        classifier.local_timestamp,
        classifier.is_active,
        classifier.evidence().scores,
        classifier.authoritative_result,
        classifier.activity_event_count,
        classifier._character_index,
        classifier._start_event,
    )

    with pytest.raises(ValueError, match="nondecreasing"):
        classifier.finalize_character(boundary(END_CHARACTER, 5.0, 3, 2))

    after = (
        classifier.local_timestamp,
        classifier.is_active,
        classifier.evidence().scores,
        classifier.authoritative_result,
        classifier.activity_event_count,
        classifier._character_index,
        classifier._start_event,
    )
    assert after == before

    with pytest.raises(ValueError, match="nondecreasing"):
        classifier.ingest_event(boundary(START_CHARACTER, 6.0, 4, 3))


def test_equal_time_direct_and_dispatched_finalization_follow_queue_order() -> None:
    direct = StreamingCharacterClassifier()
    dispatched = StreamingCharacterClassifier()
    start = boundary(START_CHARACTER, 0.0, 5, 0)
    end = boundary(END_CHARACTER, 0.0, 5, 1)
    direct.ingest_event(start)
    dispatched.ingest_event(start)

    direct_result = direct.finalize_character(end)
    dispatched_result = dispatched.ingest_event(end)

    assert dispatched_result == direct_result
    assert direct.local_timestamp == dispatched.local_timestamp == 0.0
    assert not direct.is_active and not dispatched.is_active


def test_future_direct_finalization_remains_supported() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 6, 0))
    classifier.ingest_event(activity(8.0, 1.0, 1))

    result = classifier.finalize_character(boundary(END_CHARACTER, 9.0, 6, 2))

    assert result.character_index == 6
    assert classifier.local_timestamp == 9.0
    assert classifier.authoritative_result == result


def test_multiple_characters_reset_activity_and_do_not_leak_state() -> None:
    classifier = StreamingCharacterClassifier()
    for index, value in enumerate((1.0, -1.0)):
        classifier.ingest_event(boundary(START_CHARACTER, index * 2.0, index, index * 3))
        classifier.ingest_event(activity(index * 2.0, value, index * 3 + 1))
        result = classifier.ingest_event(
            boundary(END_CHARACTER, index * 2.0 + 1.0, index, index * 3 + 2)
        )
        assert result is not None
        assert result.activity_event_count == 1
        assert classifier.activity_event_count == 1


def test_empty_character_is_valid_and_has_bounded_default_evidence() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 0))

    result = classifier.ingest_event(boundary(END_CHARACTER, 0.0, 0, 1))

    assert result is not None
    assert result.activity_event_count == 0
    assert len(result.scores) == 26


def test_evidence_inspection_is_side_effect_free() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 0))
    classifier.ingest_event(activity(0.25, 1.0, 1))
    before = (classifier.activity_event_count, classifier.authoritative_result, classifier.is_active)

    first = classifier.evidence()
    second = classifier.evidence()

    assert first == second
    assert (classifier.activity_event_count, classifier.authoritative_result, classifier.is_active) == before


def test_deterministic_replay_and_label_independent_inference() -> None:
    with_label_a = run_stream("A")
    with_label_z = run_stream("Z")
    without_label = run_stream(None)

    assert with_label_a == with_label_z == without_label


def test_long_stream_has_bounded_classifier_state() -> None:
    classifier = StreamingCharacterClassifier(max_activity_events=3)
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 0))
    for sequence in range(3):
        classifier.ingest_event(activity(float(sequence), 100.0, sequence + 1))

    assert classifier.activity_event_count == 3
    assert len(classifier.evidence().scores) == 26


def test_activity_capacity_is_explicit_backpressure() -> None:
    classifier = StreamingCharacterClassifier(max_activity_events=1)
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 0))
    classifier.ingest_event(activity(0.0, 1.0, 1))

    try:
        classifier.ingest_event(activity(1.0, 1.0, 2))
    except BufferError:
        pass
    else:
        raise AssertionError("activity capacity must remain bounded")


def test_boundaries_and_activity_are_rejected_outside_their_protocol() -> None:
    classifier = StreamingCharacterClassifier()

    with pytest.raises(ValueError):
        classifier.ingest_event(Event(0.0, "stream", "readout", END_STROKE, None, 0))

    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 1))
    with pytest.raises(ValueError):
        classifier.ingest_event(Event(0.1, "neuron-0", "readout", "signal", 1.0, 2))


def test_canonical_neuron_activity_can_feed_the_readout() -> None:
    neuron = TPCNNeuron("neuron-0")
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0, 0))

    activation = neuron.receive_event(Event(0.25, "input", "neuron-0", "signal", 1.0, 1))
    classifier.ingest_event(activity(0.25, activation, 2))

    assert classifier.activity_event_count == 1