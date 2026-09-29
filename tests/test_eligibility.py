import pytest

from tpcn import (
    EligibilityActivity,
    EligibilityCapacityError,
    EligibilityLedger,
    Event,
    PredictionError,
    RewardMessage,
    RewardSignal,
)


def activity(timestamp: float, payload: EligibilityActivity) -> Event:
    return Event(timestamp, "neuron", "ledger", "eligibility_activity", payload)


def signal(timestamp: float, payload: RewardSignal | PredictionError) -> Event:
    return Event(timestamp, "signal-source", "ledger", "reward", payload)


def test_delayed_reward_credits_local_activity_after_causal_arrival() -> None:
    ledger = EligibilityLedger("ledger", max_traces=2, decay_time_constant=2.0, credit_limit=10.0)
    ledger.record_activity(activity(1.0, EligibilityActivity("work", 1.0, "p:1")))

    assert ledger.traces[0].credit == 0.0
    result = ledger.apply_signal(signal(3.0, RewardSignal(2.0, message_id="r:1", prediction_id="p:1")))

    assert result.status == "matched"
    assert result.trace_id == "work"
    assert result.eligibility == pytest.approx(0.3678794412)
    assert result.credit == pytest.approx(0.7357588824)


def test_irregular_timestamp_decay_is_deterministic_and_bounded() -> None:
    first = EligibilityLedger("ledger", max_traces=1, decay_time_constant=2.0, trace_limit=1.0, credit_limit=1.0)
    second = EligibilityLedger("ledger", max_traces=1, decay_time_constant=2.0, trace_limit=1.0, credit_limit=1.0)
    for ledger in (first, second):
        ledger.record_activity(activity(0.5, EligibilityActivity("work", 4.0)))
        ledger.apply_signal(signal(2.75, RewardSignal(4.0, message_id="r:decay", trace_id="work")))

    assert first.traces == second.traces
    assert abs(first.traces[0].value) <= 1.0
    assert abs(first.traces[0].credit) <= 1.0


def test_unmatched_reward_does_not_mutate_local_trace() -> None:
    ledger = EligibilityLedger("ledger", max_traces=2, decay_time_constant=2.0)
    ledger.record_activity(activity(1.0, EligibilityActivity("work", 1.0, "p:1")))
    before = ledger.traces

    result = ledger.apply_signal(signal(2.0, RewardSignal(1.0, message_id="r:unknown", prediction_id="other")))

    assert result.status == "unmatched"
    assert ledger.traces == before


def test_prediction_error_is_a_causal_local_signal() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=1.0, credit_limit=4.0)
    ledger.record_activity(activity(2.0, EligibilityActivity("work", 1.0, "predictor:prediction:0")))
    error = PredictionError("predictor:prediction:0", "predictor", "next", 0.0, 0.5, 0.5, 2.0, 5.0, "observer")

    result = ledger.apply_signal(signal(5.0, error))

    assert result.status == "matched"
    assert result.credit == pytest.approx(0.0248935342)


def test_trace_capacity_has_deterministic_overflow() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=1.0)
    ledger.record_activity(activity(0.0, EligibilityActivity("first", 1.0)))

    with pytest.raises(EligibilityCapacityError):
        ledger.record_activity(activity(1.0, EligibilityActivity("second", 1.0)))

    assert tuple(trace.trace_id for trace in ledger.traces) == ("first",)


def test_reward_duplicate_is_a_no_op_without_clock_or_credit_mutation() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
    ledger.record_activity(activity(0.0, EligibilityActivity("work", 1.0, "p")))
    first = ledger.apply_signal(signal(1.0, RewardSignal(2.0, message_id="A", prediction_id="p")))
    before_duplicate = (ledger.clock.timestamp, ledger.traces, ledger.retained_reward_identities)

    duplicate = ledger.apply_signal(signal(0.5, RewardSignal(2.0, message_id="A", prediction_id="p")))

    assert first.status == "matched"
    assert duplicate.status == "duplicate"
    assert (ledger.clock.timestamp, ledger.traces, ledger.retained_reward_identities) == before_duplicate


def test_many_duplicate_deliveries_remain_idempotent() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
    ledger.record_activity(activity(0.0, EligibilityActivity("work", 1.0, "p")))
    accepted = ledger.apply_signal(signal(1.0, RewardMessage("p", 2.0, 1.0, message_id="A").to_reward_signal()))

    duplicates = [ledger.apply_signal(signal(1.0 + index, RewardMessage(
        "p", 2.0, 1.0 + index, message_id="A").to_reward_signal())) for index in range(1, 33)]

    assert accepted.status == "matched"
    assert all(result.status == "duplicate" and result.credit == 0.0 for result in duplicates)
    assert ledger.traces[0].credit == accepted.credit


def test_equal_valued_distinct_reward_ids_apply_independently() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
    ledger.record_activity(activity(0.0, EligibilityActivity("work", 1.0, "p")))

    first = ledger.apply_signal(signal(1.0, RewardSignal(2.0, message_id="A", prediction_id="p")))
    second = ledger.apply_signal(signal(2.0, RewardSignal(2.0, message_id="B", prediction_id="p")))
    replay = ledger.apply_signal(signal(3.0, RewardSignal(2.0, message_id="A", prediction_id="p")))

    assert first.status == second.status == "matched"
    assert second.credit > first.credit
    assert replay.status == "duplicate"
    assert replay.credit == 0.0


def test_reward_identity_retention_is_fifo_bounded_and_eviction_reopens_identity() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=100.0, credit_limit=10.0,
                               max_reward_identities=2)
    ledger.record_activity(activity(0.0, EligibilityActivity("work", 1.0, "p")))
    for timestamp, message_id in enumerate(("A", "B", "C"), start=1):
        assert ledger.apply_signal(signal(float(timestamp), RewardSignal(1.0, message_id=message_id,
                                                                         prediction_id="p"))).status == "matched"

    assert ledger.retained_reward_identities == ("B", "C")
    replayed = ledger.apply_signal(signal(4.0, RewardSignal(1.0, message_id="A", prediction_id="p")))

    assert replayed.status == "matched"
    assert ledger.retained_reward_identities == ("C", "A")
    assert len(ledger.retained_reward_identities) == 2


def test_reward_identity_reset_clears_duplicate_scope() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
    ledger.record_activity(activity(0.0, EligibilityActivity("work", 1.0, "p")))
    ledger.apply_signal(signal(1.0, RewardSignal(1.0, message_id="A", prediction_id="p")))
    ledger.reset()
    ledger.record_activity(activity(0.0, EligibilityActivity("next-work", 1.0, "p")))

    result = ledger.apply_signal(signal(1.0, RewardSignal(1.0, message_id="A", prediction_id="p")))

    assert result.status == "matched"
    assert ledger.retained_reward_identities == ("A",)


def test_expired_trace_does_not_consume_reward_identity() -> None:
    ledger = EligibilityLedger("ledger", max_traces=1, decay_time_constant=1.0, expiry=1.0)
    ledger.record_activity(activity(0.0, EligibilityActivity("work", 1.0, "p")))
    expired = ledger.apply_signal(signal(2.0, RewardSignal(1.0, message_id="A", prediction_id="p")))
    ledger.record_activity(activity(2.0, EligibilityActivity("replacement", 1.0, "p")))
    accepted = ledger.apply_signal(signal(2.0, RewardSignal(1.0, message_id="A", prediction_id="p")))

    assert expired.status == "expired"
    assert accepted.status == "matched"


def test_reward_replay_is_deterministic_across_ledgers() -> None:
    events = (
        (1.0, RewardSignal(2.0, message_id="A", prediction_id="p")),
        (2.0, RewardSignal(2.0, message_id="B", prediction_id="p")),
        (3.0, RewardSignal(2.0, message_id="A", prediction_id="p")),
    )
    ledgers = [EligibilityLedger("ledger", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
               for _ in range(2)]
    for ledger in ledgers:
        ledger.record_activity(activity(0.0, EligibilityActivity("work", 1.0, "p")))
    results = [
        tuple(ledger.apply_signal(signal(timestamp, payload)) for timestamp, payload in events)
        for ledger in ledgers
    ]

    assert results[0] == results[1]
    assert ledgers[0].traces == ledgers[1].traces


def test_reward_observation_on_and_off_do_not_change_learning() -> None:
    events = (
        (1.0, RewardSignal(2.0, message_id="A", prediction_id="p")),
        (2.0, RewardSignal(2.0, message_id="A", prediction_id="p")),
        (3.0, RewardSignal(2.0, message_id="B", prediction_id="p")),
    )
    plain = EligibilityLedger("plain", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
    observed = EligibilityLedger("observed", max_traces=1, decay_time_constant=10.0, credit_limit=10.0)
    for ledger in (plain, observed):
        ledger.record_activity(Event(0.0, "neuron", ledger.ledger_id, "eligibility_activity",
                                     EligibilityActivity("work", 1.0, "p")))
        telemetry = []
    for timestamp, payload in events:
            plain.apply_signal(Event(timestamp, "signal-source", plain.ledger_id, "reward", payload))
            telemetry.append(observed.apply_signal(
                Event(timestamp, "signal-source", observed.ledger_id, "reward", payload)
            ).status)

    assert telemetry == ["matched", "duplicate", "matched"]
    assert plain.traces == observed.traces
    assert plain.retained_reward_identities == observed.retained_reward_identities