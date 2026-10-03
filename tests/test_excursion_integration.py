from __future__ import annotations

import math

import pytest

from tpcn.canonical_neuron import TPCNNeuron
from tpcn.event_runtime import EventType, QueueCapacityError
from tpcn.excursion_neuron import E1Config, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.experiments import ExperimentConfig, ExperimentRunner, make_synthetic_workload
from tpcn.ir2 import (
    IR2Edge,
    IR2UnsupportedRuntimeError,
    IR2Neuron,
    TPCNIR2,
    neuron_to_ir2_e2,
)
from tpcn.topology import BoundedTopology


def _runtime(
    *,
    emission_delay: float = 0.5,
    m_emit_delay: float = 1.0,
    queue_capacity: int = 16,
    event_budget: int = 64,
    settling_horizon: float = 4.0,
    edges: tuple[tuple[str, str, float], ...] = (),
) -> ExcursionCharacterRuntime:
    nodes = ("n0", "n1")
    topology = BoundedTopology.from_edges(
        nodes,
        edges,
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=4,
        routing_capacity=4,
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
        {"unassigned_provenance_count": 1},
        {"unassigned_provenance_truncated": True},
    ),
)
def test_ir2_quiescent_startup_rejects_residual_or_unassigned_provenance(
    record_kwargs: dict[str, object],
) -> None:
    document = TPCNIR2((IR2Neuron("n0", **record_kwargs),), nodes=("n0",))

    with pytest.raises(
        IR2UnsupportedRuntimeError,
        match="residual state or unassigned provenance",
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


def test_ir2_live_network_resume_is_rejected() -> None:
    live = MultiExcursionNeuron("n0", config=E1Config(emission_delay=1.0))
    from tpcn.event_runtime import EventQueue

    live.receive_contribution(0.0, 1.2, queue=EventQueue(8))
    document = TPCNIR2((neuron_to_ir2_e2(live),), nodes=("n0",))

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
