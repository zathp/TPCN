from __future__ import annotations

import math

import pytest

from tpcn.canonical_neuron import TPCNNeuron
from tpcn.event_runtime import Event, EventQueue, EventType, QueueCapacityError
from tpcn.excursion_neuron import E1Config, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import (
    ExcursionCharacterResult,
    ExcursionCharacterRuntime,
)
from tpcn.experiments import ExperimentConfig, ExperimentRunner, make_synthetic_workload
from tpcn.ir2 import (
    IR2Edge,
    IR2Event,
    IR2Mode,
    IR2Provenance,
    IR2UnsupportedRuntimeError,
    IR2Neuron,
    TPCNIR2,
    neuron_to_ir2_e2,
)
from tpcn.predictive_coding import (
    PREDICTION_ERROR_EVENT,
    Prediction,
    PredictionError,
)
from tpcn.topology import BoundedTopology, Edge


def _runtime(
    *,
    emission_delay: float = 0.5,
    m_emit_delay: float = 1.0,
    queue_capacity: int = 16,
    event_budget: int = 64,
    settling_horizon: float = 4.0,
    nodes: tuple[str, ...] = ("n0", "n1"),
    edges: tuple[Edge | tuple[str, str, float], ...] = (),
) -> ExcursionCharacterRuntime:
    topology = BoundedTopology.from_edges(
        nodes,
        edges,
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=max(4, len(edges)),
        routing_capacity=max(4, len(edges)),
    )
    neurons = tuple(
        MultiExcursionNeuron(
            node,
            config=E1Config(
                emission_delay=emission_delay,
                m_emit_delay=m_emit_delay,
                m_rearm_delay=0.5,
                delta_x_e=1.0,
                event_budget=max(128, event_budget * 4),
            ),
        )
        for node in nodes
    )
    return ExcursionCharacterRuntime(
        neurons,
        topology,
        queue_capacity=queue_capacity,
        event_budget=event_budget,
        settling_horizon=settling_horizon,
        prediction_capacity=32,
        prediction_expiry=4.0,
        max_activity_events=event_budget,
        namespace="test",
    )


def _start(runtime: ExcursionCharacterRuntime, character_id: str = "char") -> None:
    runtime.start_character(
        character_id,
        0,
        timestamp=0.0,
        predictor_source="n0",
        readout_sources=("n0",),
        input_destination="n0",
    )


def _end(runtime: ExcursionCharacterRuntime, last_timestamp: float = 0.0):
    return runtime.end_character(
        last_external_timestamp=last_timestamp,
        reward=0.0,
        reward_delay=0.0,
        reward_message_id="reward:test",
    )


def test_integrated_excursion_silence_routes_nothing() -> None:
    runtime = _runtime(edges=(("n0", "n1", 1.0),))
    _start(runtime)

    runtime.admit_external_batch(((0.0, 0.1),))
    result = _end(runtime)

    assert result.emission_count == 0
    assert result.classifier_result.activity_event_count == 0
    assert not any(row[2] == "n1" for row in result.trace)


def test_integrated_excursion_routes_only_on_emission() -> None:
    runtime = _runtime(edges=(("n0", "n1", 1.0),))
    _start(runtime)

    runtime.admit_external_batch(((0.0, 1.2),))
    assert not any(row[3] == EventType.EXCURSION for row in runtime._trace)
    result = _end(runtime)

    routed = [row for row in result.trace if row[3] == EventType.EXCURSION]
    assert result.emission_count == 1
    assert len(routed) == 1
    assert routed[0][2] == "n1"
    assert routed[0][0] == pytest.approx(1.5)
    assert routed[0][4] == pytest.approx(math.tanh(0.3))
    emission = next(row for row in result.trace if row[3] == "excursion_emission")
    assert emission[5] == routed[0][6]
    assert emission[6] != routed[0][5]
    assert isinstance(emission[7], int) and isinstance(emission[8], int)
    assert result.energy == pytest.approx(sum(value for _, value in result.energy_components))


def test_external_event_precedes_same_time_internal_event() -> None:
    runtime = _runtime(emission_delay=0.5)
    _start(runtime)

    runtime.admit_external_batch(((0.0, 1.2),))
    runtime.admit_external_batch(((0.5, -0.1),))
    same_time = [row for row in runtime._trace if row[0] == 0.5 and row[2] == "n0"]

    assert same_time[0][3] == EventType.INPUT
    assert same_time[1][3] == EventType.INTERNAL


def test_future_internal_event_does_not_jump_over_next_external_input() -> None:
    runtime = _runtime(emission_delay=2.0)
    _start(runtime)

    runtime.admit_external_batch(((0.0, 1.2),))
    pending = runtime.neurons[0].pending_internal_event
    assert pending is not None and pending.timestamp == 2.0
    runtime.admit_external_batch(((1.0, 4.0),))
    admitted = [(row[0], row[3]) for row in runtime._trace]
    assert admitted[:2] == [(0.0, EventType.INPUT), (1.0, EventType.INPUT)]

    result = _end(runtime, last_timestamp=1.0)
    internal_t2 = [
        row for row in result.trace
        if row[0] == 2.0 and row[3] == EventType.INTERNAL
    ]
    assert internal_t2
    assert [row[0] for row in result.trace[:2]] == [0.0, 1.0]
    assert any(
        set(row[8]) == {"char:input:0", "char:input:1"}
        for row in internal_t2
    )


def test_character_queue_is_bounded() -> None:
    runtime = _runtime(queue_capacity=1)
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))

    with pytest.raises(QueueCapacityError):
        runtime.admit_external_batch(((0.0, 0.1),))


def test_integrated_delayed_prediction_error() -> None:
    runtime = _runtime()
    _start(runtime)

    runtime.admit_external_batch(((0.0, 1.2),))
    runtime.admit_external_batch(((1.0, 0.4),))
    result = _end(runtime, last_timestamp=1.0)
    errors = [row[4] for row in result.trace if row[3] == "prediction_error"]

    assert result.matched_predictions == 1
    assert result.prediction_loss > 0.0
    assert len(errors) == 1
    assert errors[0].observation_timestamp == 1.0


def _run_matched_error(
    monkeypatch: pytest.MonkeyPatch,
    *,
    nodes: tuple[str, ...],
    edges: tuple[Edge | tuple[str, str, float], ...],
    queue_capacity: int = 16,
) -> tuple[
    ExcursionCharacterRuntime,
    ExcursionCharacterResult,
    list[Prediction],
    dict[str, list[Event]],
    list[tuple[str, Event]],
]:
    runtime = _runtime(
        nodes=nodes,
        edges=edges,
        queue_capacity=queue_capacity,
        event_budget=128,
    )
    _start(runtime)
    assert runtime._predictor is not None
    predictions: list[Prediction] = []
    create_prediction = runtime._predictor.create_prediction

    def record_prediction(
        target_key: str,
        predicted_value: float,
        *,
        timestamp: float | None = None,
        expected_resolution_at: float | None = None,
        expires_at: float | None = None,
    ) -> Prediction:
        prediction = create_prediction(
            target_key,
            predicted_value,
            timestamp=timestamp,
            expected_resolution_at=expected_resolution_at,
            expires_at=expires_at,
        )
        predictions.append(prediction)
        return prediction

    monkeypatch.setattr(runtime._predictor, "create_prediction", record_prediction)
    applied_errors: dict[str, list[Event]] = {node: [] for node in nodes}
    for node, ledger in runtime._ledgers.items():
        apply_signal = ledger.apply_signal

        def record_error(event, *, node=node, apply_signal=apply_signal):
            if isinstance(event.payload, PredictionError):
                applied_errors[node].append(event)
            return apply_signal(event)

        monkeypatch.setattr(ledger, "apply_signal", record_error)

    neuron_errors: list[tuple[str, Event]] = []
    for neuron in runtime.neurons:
        receive_event = neuron.receive_event

        def record_neuron_event(event, queue, *, node=neuron.neuron_id, receive_event=receive_event):
            if event.event_type == PREDICTION_ERROR_EVENT:
                neuron_errors.append((node, event))
            return receive_event(event, queue)

        monkeypatch.setattr(neuron, "receive_event", record_neuron_event)

    runtime.admit_external_batch(((0.0, 1.2),))
    runtime.admit_external_batch(((1.0, 0.4),))
    result = _end(runtime, last_timestamp=1.0)
    return runtime, result, predictions, applied_errors, neuron_errors


def _prediction_error_rows(result):
    return [row for row in result.trace if row[3] == PREDICTION_ERROR_EVENT]


def test_integrated_prediction_error_routes_one_hop_without_reverse_delivery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, result, predictions, applied, neuron_errors = _run_matched_error(
        monkeypatch,
        nodes=("n0", "n1", "n2"),
        edges=(
            Edge("n0", "n1", 0.25, edge_weight=1.7, divider_strength=0.2, reference=0.9),
            Edge("n2", "n1", 0.1),
        ),
    )

    rows = _prediction_error_rows(result)
    assert len(predictions) == 1
    assert predictions[0].predicted_value == pytest.approx(0.3)
    assert predictions[0].created_at == pytest.approx(0.5)
    assert [(row[1], row[2], row[0]) for row in rows] == [
        ("n0", "n0", 1.0),
        ("n0", "n1", 1.25),
    ]
    assert [len(applied[node]) for node in ("n0", "n1", "n2")] == [1, 1, 0]
    assert not neuron_errors

    local_error = rows[0][4]
    assert isinstance(local_error, PredictionError)
    assert local_error.error == pytest.approx(0.1)
    assert local_error.predicted_value == predictions[0].predicted_value
    assert local_error.observed_value == 0.4
    assert local_error.prediction_timestamp == predictions[0].created_at
    assert local_error.observation_timestamp == 1.0
    for row in rows:
        assert row[4] == local_error
        assert row[6] == predictions[0].prediction_id == local_error.prediction_id
        assert row[7] == rows[0][7]
        assert row[5] >= 0
    assert rows[0][5] != rows[1][5]
    assert rows[0][8] == rows[1][8]
    assert rows[0][11] is rows[1][11] is False


def test_integrated_prediction_error_routes_two_hops_with_cumulative_delay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, result, predictions, applied, neuron_errors = _run_matched_error(
        monkeypatch,
        nodes=("n0", "n1", "n2", "n3"),
        edges=(
            Edge("n0", "n1", 0.25, edge_weight=-1.5, divider_strength=0.1, reference=-0.8),
            Edge("n1", "n2", 0.4, edge_weight=2.0, divider_strength=0.7, reference=0.6),
            Edge("n3", "n1", 0.1),
        ),
    )

    rows = _prediction_error_rows(result)
    assert len(predictions) == 1
    assert [(row[1], row[2], row[0]) for row in rows] == [
        ("n0", "n0", 1.0),
        ("n0", "n1", 1.25),
        ("n1", "n2", 1.65),
    ]
    assert [row[9] for row in rows] == [0, 1, 2]
    assert [row[10] for row in rows] == [
        ("n0",),
        ("n0", "n1"),
        ("n0", "n1", "n2"),
    ]
    assert [len(applied[node]) for node in ("n0", "n1", "n2", "n3")] == [1, 1, 1, 0]
    assert not neuron_errors

    local_error = rows[0][4]
    assert isinstance(local_error, PredictionError)
    assert local_error.prediction_id == predictions[0].prediction_id
    assert local_error.error == pytest.approx(0.1)
    assert local_error.predicted_value == pytest.approx(0.3)
    assert local_error.observed_value == 0.4
    assert local_error.prediction_timestamp == 0.5
    assert local_error.observation_timestamp == 1.0
    assert local_error.observation_source == "char"
    assert all(row[4] == local_error for row in rows)
    assert all(row[6] == local_error.prediction_id for row in rows)
    assert all(row[7] == rows[0][7] for row in rows)
    assert all(row[8] == rows[0][8] for row in rows)
    assert [event.payload for node in ("n0", "n1", "n2") for event in applied[node]] == [
        local_error,
        local_error,
        local_error,
    ]


def test_integrated_prediction_error_convergent_paths_apply_and_forward_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run_once():
        return _run_matched_error(
            monkeypatch,
            nodes=("n0", "n1", "n2", "n3", "n4", "n5"),
            edges=(
                ("n0", "n1", 0.25),
                ("n0", "n2", 0.25),
                ("n1", "n3", 0.4),
                ("n2", "n3", 0.4),
                ("n3", "n4", 0.3),
                ("n5", "n1", 0.2),
            ),
        )

    first_runtime, first_result, _, first_applied, first_neuron_errors = run_once()
    second_runtime, second_result, _, second_applied, second_neuron_errors = run_once()
    first_rows = _prediction_error_rows(first_result)
    second_rows = _prediction_error_rows(second_result)
    transcript = lambda rows: [
        (row[0], row[1], row[2], row[5], row[6], row[7], row[9], row[10])
        for row in rows
    ]

    assert transcript(first_rows) == transcript(second_rows)
    assert [
        (row[1], row[2], row[0], row[10])
        for row in first_rows
    ] == [
        ("n0", "n0", 1.0, ("n0",)),
        ("n0", "n1", 1.25, ("n0", "n1")),
        ("n0", "n2", 1.25, ("n0", "n2")),
        ("n1", "n3", 1.65, ("n0", "n1", "n3")),
        ("n2", "n3", 1.65, ("n0", "n2", "n3")),
        ("n3", "n4", 1.95, ("n0", "n1", "n3", "n4")),
    ]
    assert [len(first_applied[node]) for node in first_runtime.by_id] == [1, 1, 1, 1, 1, 0]
    assert [len(second_applied[node]) for node in second_runtime.by_id] == [1, 1, 1, 1, 1, 0]
    assert not first_neuron_errors
    assert not second_neuron_errors
    assert sum(row[2] == "n3" for row in first_rows) == 2
    assert sum(row[2] == "n4" for row in first_rows) == 1
    assert first_rows[3][10] == ("n0", "n1", "n3")
    assert first_runtime._delivered_errors == second_runtime._delivered_errors == set()


def test_integrated_prediction_error_cycle_terminates_at_duplicate_destination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, result, _, applied, neuron_errors = _run_matched_error(
        monkeypatch,
        nodes=("n0", "n1"),
        edges=(("n0", "n1", 0.25), ("n1", "n0", 0.4)),
    )

    rows = _prediction_error_rows(result)
    assert [(row[1], row[2]) for row in rows] == [
        ("n0", "n0"),
        ("n0", "n1"),
        ("n1", "n0"),
    ]
    assert [len(applied[node]) for node in ("n0", "n1")] == [1, 1]
    assert not neuron_errors
    assert len(rows) == 3


def test_integrated_prediction_error_delivery_guard_resets_between_characters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime, first_result, first_predictions, _, _ = _run_matched_error(
        monkeypatch,
        nodes=("n0", "n1"),
        edges=(("n0", "n1", 0.25),),
    )
    first_error = _prediction_error_rows(first_result)[0][4]
    assert isinstance(first_error, PredictionError)
    assert first_predictions[0].prediction_id == first_error.prediction_id
    assert runtime._delivered_errors == set()

    _start(runtime, "char")
    runtime.admit_external_batch(((0.0, 1.2),))
    runtime.admit_external_batch(((1.0, 0.4),))
    second_result = _end(runtime, last_timestamp=1.0)
    second_rows = _prediction_error_rows(second_result)

    assert [(row[1], row[2]) for row in second_rows] == [("n0", "n0"), ("n0", "n1")]
    assert second_rows[0][4] == first_error
    assert second_rows[1][4] == first_error
    assert runtime._delivered_errors == set()


def test_integrated_prediction_error_fanout_capacity_failure_is_atomic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _runtime(
        nodes=("n0", "n1", "n2"),
        edges=(("n0", "n1", 0.25), ("n0", "n2", 0.4)),
        queue_capacity=2,
        event_budget=128,
    )
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))

    with pytest.raises(QueueCapacityError, match="complete fan-out"):
        runtime.admit_external_batch(((1.0, 0.4),))

    assert runtime.queue is not None
    assert len(runtime.queue) == 1
    assert runtime.queue.peek() is not None
    assert runtime.queue.peek().destination == "n0"
    assert not any(
        row[3] == PREDICTION_ERROR_EVENT and row[1] != "n0"
        for row in runtime._trace
    )


def test_integrated_delayed_credit() -> None:
    runtime = _runtime()
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))
    runtime.admit_external_batch(((1.0, 0.4),))

    result = runtime.end_character(
        last_external_timestamp=1.0,
        reward=1.0,
        reward_delay=0.25,
        reward_message_id="reward:delayed",
    )

    assert result.matched_credit >= 1
    assert result.reward_attribution == "matched"
    assert result.reward_update_latency == 0.25


def test_integrated_readout_uses_excursion_events() -> None:
    runtime = _runtime()
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))
    result = _end(runtime)

    assert result.classifier_result.activity_event_count == result.emission_count
    assert result.feature == pytest.approx(0.3)


def test_integrated_character_settling_is_finite() -> None:
    runtime = _runtime(emission_delay=2.0, settling_horizon=0.25)
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))
    result = _end(runtime)

    assert result.incomplete_settling
    assert result.pending_event_count == 1
    assert result.beyond_deadline_event_count == 1
    assert not result.execution.completed


def test_reset_invalidates_old_pending_work() -> None:
    runtime = _runtime()
    _start(runtime, "old")
    runtime.admit_external_batch(((0.0, 1.2),))
    runtime.reset()
    _start(runtime, "new")
    runtime.admit_external_batch(((0.0, 0.1),))
    result = _end(runtime)

    assert result.emission_count == 0
    assert all("old" not in str(row) for row in result.trace)


def test_identity_high_water_survives_character_reset() -> None:
    runtime = _runtime()
    _start(runtime, "first")
    runtime.admit_external_batch(((0.0, 1.2),))
    first = _end(runtime)
    first_high_water = runtime.neurons[0]._event_identity

    _start(runtime, "second")
    runtime.admit_external_batch(((0.0, 1.2),))
    second = _end(runtime)

    assert first.emission_count == second.emission_count == 1
    assert runtime.neurons[0]._event_identity > first_high_water
    first_id = next(row for row in first.trace if row[3] == "excursion_emission")[5]
    second_id = next(row for row in second.trace if row[3] == "excursion_emission")[5]
    assert first_id != second_id


def test_ir2_quiescent_reconstruction_is_deterministic() -> None:
    source = MultiExcursionNeuron("n0")
    records = (neuron_to_ir2_e2(source), IR2Neuron("n1"))
    document = TPCNIR2(
        records,
        (IR2Edge("n0", "n1", 1.0, 1.0, 0.0, 1.0),),
        nodes=("n0", "n1"),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=4,
        routing_capacity=4,
        event_queue_capacity=16,
    )

    traces = []
    for _ in range(2):
        runtime = ExcursionCharacterRuntime.from_quiescent_ir2(
            TPCNIR2.from_json(document.to_json()),
            queue_capacity=16,
            event_budget=64,
            settling_horizon=4.0,
            prediction_capacity=32,
            prediction_expiry=4.0,
            max_activity_events=64,
            namespace="ir2",
        )
        _start(runtime)
        runtime.admit_external_batch(((0.0, 1.2),))
        traces.append(_end(runtime).trace)

    assert traces[0] == traces[1]


@pytest.mark.parametrize(
    "record_kwargs",
    (
        {"x": 0.25},
        {"x": -0.25},
        {"x": math.nextafter(0.0, 1.0)},
        {"x": math.nextafter(0.0, -1.0)},
        {"unassigned_provenance_count": 1},
        {"unassigned_provenance_truncated": True},
        {"provenance": (IR2Provenance("input:0", 0.0, 0.5, None, None),)},
        {"provenance_truncated": True},
        {
            "provenance": (IR2Provenance("input:0", 0.0, 0.5, None, None),),
            "provenance_truncated": True,
        },
        {
            "provenance": (IR2Provenance("input:0", 0.0, 0.5, None, None),),
            "unassigned_provenance_count": 1,
        },
        {
            "x": math.nextafter(0.0, 1.0),
            "provenance": (IR2Provenance("input:0", 0.0, 0.5, None, None),),
        },
    ),
)
def test_ir2_quiescent_startup_rejects_residual_state_or_provenance(
    record_kwargs: dict[str, object],
) -> None:
    document = TPCNIR2((IR2Neuron("n0", **record_kwargs),), nodes=("n0",))

    with pytest.raises(
        IR2UnsupportedRuntimeError,
        match="residual state or provenance",
    ):
        ExcursionCharacterRuntime.from_quiescent_ir2(
            document,
            queue_capacity=8,
            event_budget=16,
            settling_horizon=2.0,
            prediction_capacity=4,
            prediction_expiry=1.0,
            max_activity_events=16,
            namespace="nonquiescent",
        )


@pytest.mark.parametrize("x", (0.0, -0.0))
def test_ir2_quiescent_startup_accepts_signed_zero(x: float) -> None:
    document = TPCNIR2((IR2Neuron("n0", x=x),), nodes=("n0",))
    restored = TPCNIR2.from_json(document.to_json())

    runtime = ExcursionCharacterRuntime.from_quiescent_ir2(
        restored,
        queue_capacity=8,
        event_budget=16,
        settling_horizon=2.0,
        prediction_capacity=4,
        prediction_expiry=1.0,
        max_activity_events=16,
        namespace="signed-zero",
    )

    assert math.copysign(1.0, restored.neurons[0].x) == math.copysign(1.0, x)
    assert runtime.neurons[0].x == 0.0


def test_ir2_quiescent_startup_preserves_identity_high_water_counters() -> None:
    high_water = {
        "next_event_identity": 7,
        "next_episode_identity": 5,
        "next_lineage_identity": 6,
        "next_input_identity": 8,
    }
    document = TPCNIR2((IR2Neuron("n0", **high_water),), nodes=("n0",))
    runtime = ExcursionCharacterRuntime.from_quiescent_ir2(
        document,
        queue_capacity=8,
        event_budget=16,
        settling_horizon=2.0,
        prediction_capacity=4,
        prediction_expiry=1.0,
        max_activity_events=16,
        namespace="high-water",
    )
    neuron = runtime.neurons[0]

    assert neuron._event_identity == high_water["next_event_identity"]
    assert neuron._episode_identity == high_water["next_episode_identity"]
    assert neuron._lineage_identity == high_water["next_lineage_identity"]
    assert neuron._input_identity == high_water["next_input_identity"]

    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))
    result = _end(runtime)

    assert result.emission_count == 1
    emission = next(row for row in result.trace if row[3] == "excursion_emission")
    assert emission[5] == f"n0:excursion:{high_water['next_event_identity'] + 1}"
    assert emission[6] == high_water["next_event_identity"] + 1
    assert emission[7] > high_water["next_episode_identity"]
    assert emission[8] > high_water["next_lineage_identity"]
    assert neuron._event_identity > high_water["next_event_identity"]
    assert neuron._episode_identity > high_water["next_episode_identity"]
    assert neuron._lineage_identity > high_water["next_lineage_identity"]
    assert neuron._input_identity == high_water["next_input_identity"]


def test_ir2_quiescent_startup_rejects_shared_queued_work() -> None:
    document = TPCNIR2(
        (IR2Neuron("n0"),),
        events=(IR2Event(0.5, "n0", "n0", "signal", {"value": 1.0}),),
        nodes=("n0",),
        event_queue_capacity=2,
    )

    with pytest.raises(IR2UnsupportedRuntimeError, match="empty shared event queue"):
        ExcursionCharacterRuntime.from_quiescent_ir2(
            document,
            queue_capacity=8,
            event_budget=16,
            settling_horizon=2.0,
            prediction_capacity=4,
            prediction_expiry=1.0,
            max_activity_events=16,
            namespace="queued-work",
        )


def test_legacy_mode_is_explicit() -> None:
    runner = ExperimentRunner(ExperimentConfig(neuron_model="TANH_LEGACY"))
    runner.evaluate(make_synthetic_workload(examples_per_class=1))

    assert runner.config.neuron_model == "TANH_LEGACY"
    assert all(isinstance(neuron, TPCNNeuron) for neuron in runner.last_neurons)


def test_no_label_leakage() -> None:
    workload = make_synthetic_workload(examples_per_class=1)
    relabeled = tuple(
        type(example)(example.example_id, example.points, "Z" if example.label == "A" else "A")
        for example in workload
    )

    first = ExperimentRunner().evaluate(workload)
    second = ExperimentRunner().evaluate(relabeled)
    assert first.event_trace == second.event_trace
    assert first.metrics.energy == second.metrics.energy


def test_deterministic_replay() -> None:
    workload = make_synthetic_workload(examples_per_class=2)

    assert ExperimentRunner().evaluate(workload) == ExperimentRunner().evaluate(workload)


def test_no_global_timestep() -> None:
    runtime = _runtime()
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))
    runtime.admit_external_batch(((1.75, 0.1),))
    result = _end(runtime, last_timestamp=1.75)

    external_times = [row[0] for row in result.trace if row[3] == EventType.INPUT]
    assert external_times == [0.0, 1.75]


def test_integrated_multiple_same_time_external_inputs_precede_internal_work() -> None:
    runtime = _runtime(emission_delay=0.5)
    _start(runtime)
    runtime.admit_external_batch(((0.0, 0.6), (0.0, 0.6)))

    at_zero = [row for row in runtime._trace if row[0] == 0.0]
    assert len(at_zero) == 2
    assert all(row[3] == EventType.INPUT for row in at_zero)


def test_stale_canceled_e2_work_is_harmless() -> None:
    runtime = _runtime(emission_delay=2.0)
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))
    old_pending = runtime.neurons[0].pending_internal_event
    assert old_pending is not None
    runtime.admit_external_batch(((1.0, 4.0),))
    current_pending = runtime.neurons[0].pending_internal_event
    assert current_pending is not None
    assert current_pending.queue_sequence != old_pending.queue_sequence
    result = _end(runtime, last_timestamp=1.0)
    assert result.execution.processed_event_count < runtime.event_budget


def test_multiple_m_excursions_are_distinct_readout_events() -> None:
    runtime = _runtime(m_emit_delay=0.1, event_budget=128)
    _start(runtime)
    runtime.admit_external_batch(((0.0, 7.0),))
    result = _end(runtime)

    assert result.emission_count >= 2
    assert result.classifier_result.activity_event_count == result.emission_count


def test_event_budget_exhaustion_is_incomplete() -> None:
    runtime = _runtime(event_budget=1)
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))
    result = _end(runtime)

    assert result.incomplete_settling
    assert result.execution.budget_exhausted
    assert result.pending_event_count > 0


def test_budget_exhaustion_cannot_admit_input_past_pending_work() -> None:
    runtime = _runtime(event_budget=1)
    _start(runtime)
    runtime.admit_external_batch(((0.0, 1.2),))

    with pytest.raises(RuntimeError, match="event budget exhausted before"):
        runtime.admit_external_batch(((1.0, 0.1),))

    assert [row[0] for row in runtime._trace if row[3] == EventType.INPUT] == [0.0]


def test_late_input_fails_explicitly() -> None:
    runtime = _runtime()
    _start(runtime)
    runtime.admit_external_batch(((1.0, 0.1),))

    with pytest.raises(ValueError, match="late external input"):
        runtime.admit_external_batch(((0.5, 0.1),))


def test_mixed_model_network_is_rejected() -> None:
    topology = BoundedTopology(("n0", "n1"), fan_in_limit=1, fan_out_limit=1)

    with pytest.raises(TypeError, match="MultiExcursionNeuron"):
        ExcursionCharacterRuntime(
            (MultiExcursionNeuron("n0"), TPCNNeuron("n1")),
            topology,
            queue_capacity=8,
            event_budget=16,
            settling_horizon=1.0,
            prediction_capacity=4,
            prediction_expiry=1.0,
            max_activity_events=16,
            namespace="mixed",
        )


def test_excursion_experiment_keeps_topology_fixed() -> None:
    with pytest.raises(ValueError, match="structural plasticity is unavailable"):
        ExperimentConfig(neuron_model="EXCURSION_V1", structural_plasticity=True)


@pytest.mark.parametrize(
    ("payload", "process_pending", "expected_mode"),
    (
        (1.2, False, IR2Mode.S_PENDING),
        (1.2, True, IR2Mode.S_RETURN),
        (8.0, False, IR2Mode.M_ACTIVE),
    ),
)
def test_ir2_active_modes_are_rejected(
    payload: float,
    process_pending: bool,
    expected_mode: IR2Mode,
) -> None:
    live = MultiExcursionNeuron(
        "n0",
        config=E1Config(emission_delay=0.5, m_emit_delay=1.0),
    )
    queue = EventQueue(8)
    live.receive_contribution(0.0, payload, queue=queue)
    if process_pending:
        live.receive_event(queue.pop_ready(0.5), queue)
    record = neuron_to_ir2_e2(live)
    assert record.mode is expected_mode
    assert record.pending_internal_event is not None
    document = TPCNIR2((record,), nodes=("n0",))

    with pytest.raises(IR2UnsupportedRuntimeError, match="live-network resume"):
        ExcursionCharacterRuntime.from_quiescent_ir2(
            document,
            queue_capacity=8,
            event_budget=16,
            settling_horizon=2.0,
            prediction_capacity=4,
            prediction_expiry=1.0,
            max_activity_events=16,
            namespace="live",
        )


def test_ir2_model_mixing_is_rejected() -> None:
    document = TPCNIR2(
        (neuron_to_ir2_e2(MultiExcursionNeuron("n0")), IR2Neuron("n1", dynamics_model="TANH_LEGACY")),
        nodes=("n0", "n1"),
    )

    with pytest.raises(IR2UnsupportedRuntimeError, match="uniformly selected"):
        ExcursionCharacterRuntime.from_quiescent_ir2(
            document,
            queue_capacity=8,
            event_budget=16,
            settling_horizon=2.0,
            prediction_capacity=4,
            prediction_expiry=1.0,
            max_activity_events=16,
            namespace="mixed-ir2",
        )
