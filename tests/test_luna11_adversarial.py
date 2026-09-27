from __future__ import annotations

import pytest

from tpcn import (
    ACTIVITY_EVENT,
    CharacterBoundary,
    END_CHARACTER,
    END_STROKE,
    EligibilityActivity,
    EligibilityLedger,
    Event,
    EventQueue,
    QueueCapacityError,
    RewardMessage,
    START_CHARACTER,
    StreamingCharacterClassifier,
)
from tpcn.energy_utility import LocalEnergyModel
from tpcn.topology import BoundedTopology


def boundary(event_type: str, timestamp: float, index: int) -> Event:
    return Event(timestamp, "stream", "readout", event_type, CharacterBoundary(index))


def activity(timestamp: float, value: float) -> Event:
    return Event(timestamp, "neuron", "readout", ACTIVITY_EVENT, value)


def test_character_boundaries_and_read_only_inspection_are_causal() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0))
    classifier.ingest_event(activity(0.5, 1.0))
    before_stroke = classifier.evidence()

    assert classifier.ingest_event(Event(0.75, "stream", "readout", END_STROKE, None)) == before_stroke
    assert classifier.authoritative_result is None
    assert classifier.evidence() == before_stroke

    result = classifier.ingest_event(boundary(END_CHARACTER, 1.0, 0))
    assert result is not None
    assert classifier.authoritative_result == result
    with pytest.raises(ValueError):
        classifier.ingest_event(boundary(END_CHARACTER, 1.0, 0))


def test_delayed_reward_keeps_old_character_identity_while_next_is_active() -> None:
    ledger = EligibilityLedger("ledger", max_traces=2, decay_time_constant=10.0)
    ledger.record_activity(Event(1.0, "neuron", "ledger", "eligibility_activity",
                                 EligibilityActivity("character-0", 1.0, "character-0")))
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 2.0, 1))
    classifier.ingest_event(activity(2.0, -1.0))

    reward = RewardMessage("character-0", 1.0, 3.0)
    attribution = ledger.apply_signal(
        Event(reward.timestamp, "utility", "ledger", "reward", reward.to_reward_signal())
    )

    assert attribution.trace_id == "character-0"
    assert classifier.authoritative_result is None
    assert classifier.activity_event_count == 1


def test_interleaved_instances_do_not_share_classifier_state() -> None:
    first = StreamingCharacterClassifier()
    second = StreamingCharacterClassifier()
    first.ingest_event(boundary(START_CHARACTER, 0.0, 0))
    second.ingest_event(boundary(START_CHARACTER, 0.0, 0))
    first.ingest_event(activity(1.0, 1.0))

    assert first.activity_event_count == 1
    assert second.activity_event_count == 0
    assert second.evidence().event_count == 0


def test_fanout_rejection_is_atomic_and_finite() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (("a", "b", 1.0), ("a", "c", 2.0)),
        fan_in_limit=2, fan_out_limit=2,
    )
    queue = EventQueue(capacity=1)
    event = Event(0.0, "a", "ignored", "signal", None)

    with pytest.raises(QueueCapacityError):
        topology.route(event, queue)
    assert len(queue) == 0


def test_batch_and_eventwise_delivery_have_identical_order() -> None:
    def run(batch: bool) -> list[tuple[str, float]]:
        topology = BoundedTopology.from_edges(
            ("a", "b", "c"), (("a", "b", 1.0), ("a", "c", 1.0)),
            fan_in_limit=2, fan_out_limit=2,
        )
        queue = EventQueue(capacity=4)
        topology.route(Event(0.0, "a", "ignored", "signal", None), queue)
        result: list[tuple[str, float]] = []
        while queue:
            ready = queue.pop_ready_batch(1.0) if batch else [queue.pop_ready(1.0)]
            result.extend((item.destination, item.timestamp) for item in ready)
        return result

    assert run(False) == run(True)


def test_propagation_is_queued_until_positive_arrival_time() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b"), (("a", "b", 2.0),), fan_in_limit=1, fan_out_limit=1,
    )
    queue = EventQueue(capacity=1)
    topology.route(Event(3.0, "a", "ignored", "signal", None), queue)

    with pytest.raises(IndexError):
        queue.pop_ready(4.99)
    assert queue.pop_ready(5.0).destination == "b"


def test_long_workload_keeps_classifier_and_energy_state_bounded() -> None:
    classifier = StreamingCharacterClassifier(max_activity_events=2)
    energy = LocalEnergyModel("meter", max_energy=3.0, max_counter=4)
    for index in range(100):
        timestamp = float(index * 3)
        classifier.ingest_event(boundary(START_CHARACTER, timestamp, index))
        classifier.ingest_event(activity(timestamp, 1.0))
        energy.observe_activity("events_received", cost=1.0, timestamp=timestamp)
        result = classifier.ingest_event(boundary(END_CHARACTER, timestamp + 1.0, index))
        assert result is not None

    snapshot = energy.snapshot()
    assert len(snapshot.counters) == 7
    assert snapshot.energy <= 3.0
    assert snapshot.activity <= 3.0
    assert len(classifier.evidence().scores) == 26


def test_reward_replay_is_not_silently_idempotent_without_a_message_identity() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
    ledger.record_activity(Event(0.0, "neuron", "ledger", "eligibility_activity",
                                 EligibilityActivity("work", 1.0, "credit")))
    signal = RewardMessage("credit", 2.0, 1.0).to_reward_signal()
    first = ledger.apply_signal(Event(1.0, "utility", "ledger", "reward", signal))
    second = ledger.apply_signal(Event(2.0, "utility", "ledger", "reward", signal))

    assert first.status == second.status == "matched"
    assert second.credit > first.credit


@pytest.mark.xfail(strict=True, reason="Luna-7: rejected event advances classifier local timestamp")
def test_rejected_classifier_event_can_be_retried_without_poisoning_order() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0))
    with pytest.raises(ValueError):
        classifier.ingest_event(Event(1.0, "neuron", "readout", "signal", 1.0))

    classifier.ingest_event(activity(0.5, 1.0))
    assert classifier.activity_event_count == 1


@pytest.mark.xfail(strict=True, reason="Luna-7: direct finalization does not commit local timestamp")
def test_direct_finalization_rejects_earlier_next_character() -> None:
    classifier = StreamingCharacterClassifier()
    classifier.ingest_event(boundary(START_CHARACTER, 0.0, 0))
    classifier.finalize_character(boundary(END_CHARACTER, 10.0, 0))

    with pytest.raises(ValueError):
        classifier.ingest_event(boundary(START_CHARACTER, 5.0, 1))