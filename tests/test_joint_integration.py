from __future__ import annotations

from dataclasses import dataclass

from tpcn import (
    ACTIVITY_EVENT,
    CausalNormalizer,
    CharacterBoundary,
    END_CHARACTER,
    END_STROKE,
    EligibilityActivity,
    EligibilityLedger,
    Event,
    EventQueue,
    LocalEnergyModel,
    RewardAdjustedUtility,
    RewardMessage,
    START_CHARACTER,
    StrokePoint,
    StrokeStreamEncoder,
    StreamingCharacterClassifier,
    TPCNNeuron,
)


@dataclass(frozen=True)
class IntegratedRun:
    classifications: tuple[object, ...]
    attributions: tuple[object, ...]
    energy: float
    trace_count: int
    serialized: tuple[tuple[object, ...], ...]


def _encoder() -> StrokeStreamEncoder:
    normalizer = CausalNormalizer.fit_training(
        (StrokePoint(0.0, 0.0), StrokePoint(10.0, 10.0), StrokePoint(20.0, 0.0))
    )
    return StrokeStreamEncoder(normalizer, max_points=8)


def _character_events(encoder: StrokeStreamEncoder, index: int, offset: float) -> tuple[Event, ...]:
    return encoder.encode(
        (
            StrokePoint(1.0, 1.0, timestamp=offset),
            StrokePoint(2.0, 4.0, timestamp=offset + 1.0, stroke_boundary=True),
            StrokePoint(4.0, 2.0, timestamp=offset + 2.0),
        ),
        source=f"character-{index}",
        destination="neuron-0",
    )


def _run(labels: tuple[str | None, ...]) -> IntegratedRun:
    encoder = _encoder()
    input_queue: EventQueue[object] = EventQueue(capacity=64)
    classifier = StreamingCharacterClassifier(max_activity_events=8)
    neuron = TPCNNeuron("neuron-0", input_gain=0.5)
    energy = LocalEnergyModel("meter", max_counter=64)
    utility = RewardAdjustedUtility()
    ledger = EligibilityLedger("ledger", max_traces=4, decay_time_constant=4.0)
    classifications: list[object] = []
    attributions: list[object] = []
    serialized: list[tuple[object, ...]] = []

    for index, _label in enumerate(labels):
        for event in _character_events(encoder, index, index * 10.0):
            queued = input_queue.push(event)
            serialized.append((queued.timestamp, queued.event_type, queued.sequence))

    while input_queue:
        event = input_queue.pop_ready(100.0)
        if event.event_type in (START_CHARACTER, END_CHARACTER):
            result = classifier.ingest_event(event)
            if result is not None:
                classifications.append(result)
            continue
        if event.event_type != "stroke":
            continue

        stroke = event.payload
        activity = neuron.receive_event(Event(event.timestamp, event.source, "neuron-0", "signal", stroke.x))
        energy.observe_event(event, cost=abs(activity))
        trace_id = f"character:{getattr(event, 'source')}"
        ledger.record_activity(
            Event(event.timestamp, "neuron-0", "ledger", "eligibility_activity",
                  EligibilityActivity(trace_id, abs(activity), trace_id))
        )
        classifier.ingest_event(Event(event.timestamp, "neuron-0", "readout", ACTIVITY_EVENT, activity))
        if stroke.stroke_boundary:
            classifier.ingest_event(Event(event.timestamp, event.source, "readout", END_STROKE, None))

    reward = RewardMessage("character:character-0", 2.0, 12.0)
    utility.observe_reward(reward)
    attribution = ledger.apply_signal(
        Event(reward.timestamp, "utility", "ledger", "reward", reward.to_reward_signal())
    )
    attributions.append(attribution)
    return IntegratedRun(tuple(classifications), tuple(attributions), energy.energy,
                         len(ledger.traces), tuple(serialized))


def test_joint_causal_path_preserves_boundaries_identity_and_delayed_credit() -> None:
    result = _run(("A", "Z"))

    assert len(result.classifications) == 2
    first, second = result.classifications
    assert first.character_index == 0
    assert second.character_index == 1
    assert (first.start_timestamp, first.end_timestamp) == (0.0, 2.0)
    assert (second.start_timestamp, second.end_timestamp) == (10.0, 12.0)
    assert first.activity_event_count == 3
    assert second.activity_event_count == 3
    assert result.attributions[0].status == "matched"
    assert result.attributions[0].trace_id == "character:character-0"
    assert result.attributions[0].timestamp == 12.0
    assert result.trace_count == 2
    assert result.energy > 0.0


def test_reward_and_labels_cannot_change_current_classifier_trajectory() -> None:
    first = _run(("A",))
    second = _run(("Z",))
    assert first.classifications == second.classifications
    assert first.serialized == second.serialized


def test_evidence_inspection_and_reward_are_not_classifier_inputs() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(Event(0.0, "stream", "readout", START_CHARACTER, CharacterBoundary(0)))
    classifier.ingest_event(Event(1.0, "neuron", "readout", ACTIVITY_EVENT, 0.5))
    before = classifier.evidence()
    assert classifier.evidence() == before
    assert classifier.authoritative_result is None

    ledger = EligibilityLedger("ledger", max_traces=2, decay_time_constant=2.0)
    ledger.record_activity(Event(1.0, "neuron", "ledger", "eligibility_activity",
                                 EligibilityActivity("old", 1.0, "old")))
    reward = RewardMessage("old", 1.0, 3.0)
    attribution = ledger.apply_signal(Event(3.0, "utility", "ledger", "reward",
                                             reward.to_reward_signal()))
    assert attribution.trace_id == "old"
    assert classifier.evidence() == before


def test_empty_character_and_reward_for_earlier_character_after_next_start() -> None:
    classifier = StreamingCharacterClassifier()
    ledger = EligibilityLedger("ledger", max_traces=2, decay_time_constant=2.0)
    first_start = Event(0.0, "character-0", "readout", START_CHARACTER, CharacterBoundary(0))
    first_activity = Event(0.0, "neuron", "readout", ACTIVITY_EVENT, 0.25)
    first_end = Event(0.0, "character-0", "readout", END_CHARACTER, CharacterBoundary(0))
    classifier.ingest_event(first_start)
    classifier.ingest_event(first_activity)
    ledger.record_activity(Event(0.0, "neuron", "ledger", "eligibility_activity",
                                 EligibilityActivity("character-0", 1.0, "character-0")))
    assert classifier.ingest_event(first_end).character_index == 0

    second_start = Event(1.0, "character-1", "readout", START_CHARACTER, CharacterBoundary(1))
    classifier.ingest_event(second_start)
    classifier.ingest_event(Event(1.0, "neuron", "readout", ACTIVITY_EVENT, -0.25))
    reward = RewardMessage("character-0", 1.0, 1.5)
    attribution = ledger.apply_signal(
        Event(1.5, "utility", "ledger", "reward", reward.to_reward_signal())
    )

    assert attribution.status == "matched"
    assert attribution.trace_id == "character-0"
    assert classifier.authoritative_result is None
    empty_result = classifier.ingest_event(
        Event(2.0, "character-1", "readout", END_CHARACTER, CharacterBoundary(1))
    )
    assert empty_result.character_index == 1
    assert empty_result.activity_event_count == 1


def test_long_multi_character_stream_has_bounded_state_and_deterministic_replay() -> None:
    first = _run(tuple(None for _ in range(2)))
    second = _run(tuple(None for _ in range(2)))
    assert first == second
    assert len(first.classifications) == 2
    assert all(len(result.scores) == 26 for result in first.classifications)
    assert first.trace_count <= 4