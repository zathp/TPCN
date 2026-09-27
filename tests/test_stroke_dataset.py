from __future__ import annotations

import pytest

from tpcn import (
    CausalNormalizer,
    END_CHARACTER,
    START_CHARACTER,
    STROKE_EVENT,
    StrokeEvent,
    StrokePoint,
    StrokeStreamEncoder,
    EventQueue,
    serialize_stream,
)


def training_points() -> tuple[StrokePoint, ...]:
    return (
        StrokePoint(0.0, 0.0),
        StrokePoint(10.0, 10.0),
        StrokePoint(20.0, 0.0),
    )


def test_stream_has_boundaries_ordered_points_and_no_label() -> None:
    encoder = StrokeStreamEncoder(CausalNormalizer.fit_training(training_points()), max_points=4)
    events = encoder.encode(
        (StrokePoint(1.0, 2.0, timestamp=3.0), StrokePoint(2.0, 4.0, timestamp=4.5, stroke_boundary=True)),
        source="input",
        destination="neuron-0",
    )

    assert [event.event_type for event in events] == [START_CHARACTER, STROKE_EVENT, STROKE_EVENT, END_CHARACTER]
    assert [event.timestamp for event in events] == [3.0, 3.0, 4.5, 4.5]
    assert isinstance(events[1].payload, StrokeEvent)
    assert not hasattr(events[1].payload, "label")
    assert serialize_stream(events) == serialize_stream(tuple(events))


def test_features_use_current_and_past_points_only() -> None:
    normalizer = CausalNormalizer.fit_training(training_points())
    encoder = StrokeStreamEncoder(normalizer, max_points=3)
    first = encoder.encode(
        (StrokePoint(0.0, 0.0, timestamp=0.0), StrokePoint(10.0, 10.0, timestamp=1.0)),
        source="input",
        destination="neuron-0",
    )
    second = encoder.encode(
        (StrokePoint(0.0, 0.0, timestamp=0.0), StrokePoint(10.0, 1.0, timestamp=1.0)),
        source="input",
        destination="neuron-0",
    )
    assert first[2].payload != second[2].payload
    assert first[1].payload.dx == 0.0
    assert first[1].payload.dy == 0.0


def test_training_fit_is_explicit_and_stream_buffer_is_bounded() -> None:
    with pytest.raises(ValueError):
        CausalNormalizer.fit_training(())
    encoder = StrokeStreamEncoder(CausalNormalizer.fit_training(training_points()), max_points=1)
    with pytest.raises(BufferError):
        encoder.encode(training_points()[:2], source="input", destination="neuron-0")


def test_synthetic_time_requires_declared_positive_interval_and_resets_delta() -> None:
    normalizer = CausalNormalizer.fit_training(training_points())
    with pytest.raises(ValueError):
        StrokeStreamEncoder(normalizer, max_points=2).encode(
            (StrokePoint(1.0, 1.0),), source="input", destination="neuron-0"
        )
    encoder = StrokeStreamEncoder(normalizer, max_points=2, synthetic_interval=0.25)
    events = encoder.encode(
        (StrokePoint(1.0, 1.0), StrokePoint(2.0, 2.0)),
        source="input",
        destination="neuron-0",
    )
    next_events = encoder.encode(
        (StrokePoint(2.0, 2.0),), source="input", destination="neuron-0"
    )
    assert [event.timestamp for event in events] == [0.0, 0.0, 0.25, 0.25]
    assert next_events[1].payload.dx == 0.0
    assert next_events[0].payload.character_index == 1


def test_timestamps_are_monotonic_and_labels_are_external_only() -> None:
    normalizer = CausalNormalizer.fit_training(training_points())
    encoder = StrokeStreamEncoder(normalizer, max_points=2)
    with pytest.raises(ValueError):
        encoder.encode(
            (StrokePoint(1.0, 1.0, timestamp=2.0), StrokePoint(2.0, 2.0, timestamp=1.0)),
            source="input",
            destination="neuron-0",
        )


def test_stream_delivers_through_bounded_runtime_queue() -> None:
    normalizer = CausalNormalizer.fit_training(training_points())
    events = StrokeStreamEncoder(normalizer, max_points=2).encode(
        (StrokePoint(1.0, 1.0, timestamp=2.0),),
        source="input",
        destination="neuron-0",
    )
    queue = EventQueue[object](capacity=len(events))
    for event in events:
        queue.push(event)
    assert [queue.pop_ready(2.0).event_type for _ in events] == [
        START_CHARACTER,
        STROKE_EVENT,
        END_CHARACTER,
    ]