import pytest

from tpcn import (
    BoundedTopology,
    Event,
    EventQueue,
    LocalPredictor,
    Observation,
    PREDICTION_EVENT,
    PREDICTION_ERROR_EVENT,
    PredictionCapacityError,
    TPCNNeuron,
)


def observation(timestamp: float, key: str, value: float) -> Event:
    return Event(timestamp, "observer", "predictor", "observation", Observation(key, value))


def test_prediction_creation_is_local_bounded_and_deterministic() -> None:
    first = LocalPredictor("node", max_outstanding=2, error_destination="errors")
    second = LocalPredictor("node", max_outstanding=2, error_destination="errors")

    first_prediction = first.create_prediction("next", 0.75, timestamp=0.25, expected_resolution_at=2.0)
    second_prediction = second.create_prediction("next", 0.75, timestamp=0.25, expected_resolution_at=2.0)

    assert first_prediction == second_prediction
    assert first.outstanding_count == 1
    assert second.clock.timestamp == pytest.approx(0.25)


def test_prediction_can_be_created_from_canonical_neuron_local_state() -> None:
    neuron = TPCNNeuron("node")
    neuron.receive_event(Event(1.5, "input", "node", "signal", 0.5))
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="errors")

    prediction = predictor.create_prediction_from_neuron(neuron, "next")

    assert prediction.created_at == pytest.approx(1.5)
    assert prediction.predicted_value == pytest.approx(neuron.activation)


def test_delayed_observation_matches_and_computes_signed_error() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="errors")
    prediction = predictor.create_prediction("next", 0.25, timestamp=1.0)

    result = predictor.observe(observation(7.5, "next", 0.75))

    assert result.status == "matched"
    assert result.prediction == prediction
    assert result.error is not None
    assert result.error.error == pytest.approx(0.5)
    assert result.error.observation_timestamp == pytest.approx(7.5)
    assert predictor.outstanding_count == 0


def test_prediction_emission_then_delayed_observation_forms_causal_sequence() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="errors")
    queue = EventQueue(capacity=4)
    prediction = predictor.create_prediction("next", 0.5, timestamp=1.0)

    emitted = predictor.emit_prediction(prediction, queue, "observer", delay=1.5)

    assert emitted.event_type == PREDICTION_EVENT
    assert emitted.timestamp == pytest.approx(2.5)
    with pytest.raises(IndexError):
        queue.pop_ready(2.49)
    assert queue.pop_ready(2.5).payload == prediction
    assert predictor.observe(observation(4.0, "next", 1.0)).error is not None


def test_error_event_is_queued_and_finitely_propagated_through_topology() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="error_sink")
    topology = BoundedTopology.from_edges(
        ("predictor", "error_sink", "downstream"),
        (("predictor", "error_sink", 1.25),),
        fan_in_limit=2,
        fan_out_limit=2,
    )
    queue = EventQueue(capacity=4)
    predictor.create_prediction("next", 0.0, timestamp=1.0)

    result = predictor.process_observation(observation(2.0, "next", 1.0), queue, topology)

    assert result.error is not None
    assert len(queue) == 1
    queued = queue.peek()
    assert queued is not None
    assert queued.event_type == PREDICTION_ERROR_EVENT
    assert queued.timestamp == pytest.approx(3.25)
    with pytest.raises(IndexError):
        queue.pop_ready(3.24)
    assert queue.pop_ready(3.25).payload == result.error


def test_unmatched_duplicate_and_unknown_observations_are_explicit() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="errors")
    predictor.create_prediction("next", 1.0)

    matched = predictor.observe(observation(1.0, "next", 1.0))
    duplicate = predictor.observe(observation(2.0, "next", 1.0))
    unknown = predictor.observe(observation(3.0, "other", 1.0))

    assert matched.status == "matched"
    assert duplicate.status == "unmatched"
    assert unknown.status == "unmatched"
    assert predictor.unmatched_observation_count == 2


def test_expired_predictions_are_removed_and_not_resolved_later() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="errors")
    prediction = predictor.create_prediction("next", 1.0, expires_at=2.0)

    expired = predictor.expire(2.1)
    result = predictor.observe(observation(3.0, "next", 1.0))

    assert expired == (prediction,)
    assert result.status == "unmatched"
    assert predictor.expired_count == 1


def test_unresolved_predictions_remain_bounded_pending_without_global_progress() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=1, error_destination="errors")
    prediction = predictor.create_prediction("never_seen", 1.0, timestamp=4.0)

    assert predictor.outstanding_predictions == (prediction,)
    assert predictor.outstanding_count == 1
    assert predictor.clock.timestamp == pytest.approx(4.0)


def test_multiple_predictions_match_fifo_and_capacity_is_bounded() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="errors")
    first = predictor.create_prediction("next", 1.0, timestamp=1.0)
    second = predictor.create_prediction("next", 2.0, timestamp=1.0)

    with pytest.raises(PredictionCapacityError):
        predictor.create_prediction("next", 3.0)

    assert predictor.observe(observation(2.0, "next", 4.0)).prediction == first
    assert predictor.observe(observation(3.0, "next", 4.0)).prediction == second


def test_equal_time_prediction_identity_breaks_matching_ties_deterministically() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=3, error_destination="errors")
    first = predictor.create_prediction("next", 1.0, timestamp=2.0)
    second = predictor.create_prediction("next", 2.0, timestamp=2.0)

    assert predictor.observe(observation(4.0, "next", 0.0)).prediction == first
    assert predictor.observe(observation(5.0, "next", 0.0)).prediction == second


def test_observation_at_expiry_is_valid_but_later_observation_is_not() -> None:
    predictor = LocalPredictor("predictor", max_outstanding=2, error_destination="errors")
    predictor.create_prediction("at", 1.0, expires_at=2.0)
    predictor.create_prediction("after", 1.0, expires_at=2.0)

    at_expiry = predictor.observe(observation(2.0, "at", 1.0))
    after_expiry = predictor.observe(observation(2.1, "after", 1.0))

    assert at_expiry.status == "matched"
    assert after_expiry.status == "unmatched"
    assert predictor.expired_count == 1


def test_irregular_times_have_no_global_prediction_timestep() -> None:
    first = LocalPredictor("first", max_outstanding=2, error_destination="errors")
    second = LocalPredictor("second", max_outstanding=2, error_destination="errors")
    first.create_prediction("next", 0.0, timestamp=0.25)
    second.create_prediction("next", 0.0, timestamp=8.75)

    assert first.clock.timestamp == pytest.approx(0.25)
    assert second.clock.timestamp == pytest.approx(8.75)