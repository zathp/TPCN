import pytest

from tpcn import (
    LocalEnergyModel,
    PredictionError,
    RewardAdjustedUtility,
    RewardMessage,
    UsefulnessObservation,
)


def test_known_activity_reconciles_with_bounded_proxy_counters() -> None:
    meter = LocalEnergyModel("node", max_energy=10.0, max_counter=3)
    meter.observe_activity("events_received", cost=2.5, count=2, timestamp=0.25)
    snapshot = meter.observe_activity("operator_activations", cost=1.0, timestamp=1.75)

    assert snapshot.energy == pytest.approx(6.0)
    assert snapshot.activity == pytest.approx(6.0)
    assert dict(snapshot.counters)["events_received"] == 2
    assert snapshot.timestamp == pytest.approx(1.75)


def test_irregular_meter_updates_do_not_create_a_global_neural_tick() -> None:
    first = LocalEnergyModel("first")
    second = LocalEnergyModel("second")
    first.update(0.25)
    second.update(8.75)

    assert first.clock.timestamp == pytest.approx(0.25)
    assert second.clock.timestamp == pytest.approx(8.75)
    assert first.energy == second.energy == 0.0


def test_idle_update_only_changes_local_measurement_state() -> None:
    meter = LocalEnergyModel("node")
    meter.update(4.0)

    assert meter.energy == 0.0
    assert meter.activity == 0.0
    assert all(value == 0 for _, value in meter.snapshot().counters)


def test_prediction_error_is_consumed_as_causal_local_activity() -> None:
    meter = LocalEnergyModel("node")
    error = PredictionError("p", "predictor", "next", 0.25, 1.0, 0.75, 1.0, 3.5, "observer")
    snapshot = meter.observe_prediction_error(error)

    assert snapshot.energy == pytest.approx(1.75)
    assert dict(snapshot.counters)["prediction_errors"] == 1
    assert snapshot.timestamp == pytest.approx(3.5)


def test_saturating_overflow_is_bounded_and_deterministic() -> None:
    first = LocalEnergyModel("node", max_energy=3.0, max_counter=2)
    second = LocalEnergyModel("node", max_energy=3.0, max_counter=2)
    for meter in (first, second):
        meter.observe_activity("events_emitted", cost=10.0, count=5)

    assert first.snapshot() == second.snapshot()
    assert first.energy == 3.0
    assert dict(first.snapshot().counters)["events_emitted"] == 2


def test_useful_expensive_work_survives_but_unproductive_work_is_suppressed() -> None:
    utility = RewardAdjustedUtility(formula="net", energy_weight=1.0)
    useful = utility.evaluate(8.0, reward=10.0)
    unproductive = utility.evaluate(8.0, reward=1.0)
    idle = utility.evaluate(0.0, reward=0.0)

    assert useful.retain is True
    assert unproductive.retain is False
    assert idle.retain is False


def test_reward_message_and_usefulness_are_explicit_local_inputs() -> None:
    utility = RewardAdjustedUtility(formula="ratio", epsilon=1.0)
    utility.observe_reward(RewardMessage("prediction:p", 6.0, 9.0))
    utility.observe_usefulness(UsefulnessObservation("activity:p", 2.0, 9.0))
    decision = utility.evaluate_last_reward(2.0)

    assert decision.utility == pytest.approx(2.0)
    assert utility.last_reward is not None
    assert utility.last_reward.credit_id == "prediction:p"
    assert utility.usefulness_total == pytest.approx(2.0)