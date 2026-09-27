import pytest

from tpcn import (
    EligibilityActivity,
    EligibilityCapacityError,
    EligibilityLedger,
    Event,
    PredictionError,
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
    result = ledger.apply_signal(signal(3.0, RewardSignal(2.0, prediction_id="p:1")))

    assert result.status == "matched"
    assert result.trace_id == "work"
    assert result.eligibility == pytest.approx(0.3678794412)
    assert result.credit == pytest.approx(0.7357588824)


def test_irregular_timestamp_decay_is_deterministic_and_bounded() -> None:
    first = EligibilityLedger("ledger", max_traces=1, decay_time_constant=2.0, trace_limit=1.0, credit_limit=1.0)
    second = EligibilityLedger("ledger", max_traces=1, decay_time_constant=2.0, trace_limit=1.0, credit_limit=1.0)
    for ledger in (first, second):
        ledger.record_activity(activity(0.5, EligibilityActivity("work", 4.0)))
        ledger.apply_signal(signal(2.75, RewardSignal(4.0, trace_id="work")))

    assert first.traces == second.traces
    assert abs(first.traces[0].value) <= 1.0
    assert abs(first.traces[0].credit) <= 1.0


def test_unmatched_reward_does_not_mutate_local_trace() -> None:
    ledger = EligibilityLedger("ledger", max_traces=2, decay_time_constant=2.0)
    ledger.record_activity(activity(1.0, EligibilityActivity("work", 1.0, "p:1")))
    before = ledger.traces

    result = ledger.apply_signal(signal(2.0, RewardSignal(1.0, prediction_id="other")))

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