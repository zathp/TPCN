from __future__ import annotations

import pytest

from tpcn import (
    E1Config,
    E1Mode,
    Event,
    EventQueue,
    IR2Mode,
    IR2PendingKind,
    IR2_SCHEMA_REVISION,
    MPhase,
    MultiExcursionNeuron,
    TPCNIR2,
    IR2UnsupportedRuntimeError,
    neuron_from_ir2,
    neuron_from_ir2_e2,
    neuron_to_ir2_e2,
)


def config() -> E1Config:
    return E1Config(
        decay_rate=0.001,
        emission_delay=0.01,
        m_emit_delay=0.01,
        m_rearm_delay=0.01,
        delta_x_e=0.5,
    )


def round_trip(neuron: MultiExcursionNeuron) -> MultiExcursionNeuron:
    document = TPCNIR2((neuron_to_ir2_e2(neuron),))
    parsed = TPCNIR2.from_json(document.to_json())
    assert parsed.schema_revision == IR2_SCHEMA_REVISION == 1
    return neuron_from_ir2_e2(parsed.neurons[0])


def drain(neuron: MultiExcursionNeuron, queue: EventQueue[Event]) -> list:
    outputs = []
    while queue:
        next_event = queue.peek()
        assert next_event is not None
        event = queue.pop_ready(next_event.timestamp)
        emission = neuron.receive_event(event, queue)
        if emission is not None:
            outputs.append(emission)
    return outputs


def test_armed_round_trip_restores_one_pending_m_emit_without_duplicate() -> None:
    neuron = MultiExcursionNeuron("n", config=config())
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 8.0, queue=queue)
    record = neuron_to_ir2_e2(neuron)
    assert record.mode == IR2Mode.M_ACTIVE
    assert record.m_phase == MPhase.ARMED
    assert record.pending_internal_event is not None
    assert record.pending_internal_event.kind == IR2PendingKind.M_EMIT

    restored = round_trip(neuron)
    assert restored.mode == E1Mode.M_ACTIVE
    assert restored.m_phase == neuron.m_phase
    assert restored.pending_event == neuron.pending_event
    assert restored.multi_episode_id == neuron.multi_episode_id
    assert restored.process_pending() is not None
    assert restored.m_phase == MPhase.REFRACTORY
    assert restored.pending_event is not None
    assert restored.pending_event.kind.value == "M_REARM"

    with pytest.raises(IR2UnsupportedRuntimeError, match="M_ACTIVE"):
        neuron_from_ir2(record)


def test_refractory_round_trip_continues_after_a_prior_m_emission() -> None:
    original = MultiExcursionNeuron("n", config=config())
    queue: EventQueue[Event] = EventQueue(64)
    original.receive_contribution(0.0, 8.0, queue=queue)
    prior = original.receive_event(queue.pop_ready(0.01), queue)
    assert prior is not None
    assert original.m_phase == MPhase.REFRACTORY

    restored = round_trip(original)
    assert restored.pending_event == original.pending_event
    assert restored.multi_episode_id == prior.episode_id
    assert restored.lineage_id == prior.lineage_id
    restored_queue: EventQueue[Event] = EventQueue(64)
    original_queue: EventQueue[Event] = EventQueue(64)
    actual = drain(restored, restored_queue)
    expected = drain(original, original_queue)

    assert [
        (item.event_id, item.timestamp, item.payload, item.episode_id, item.lineage_id)
        for item in actual
    ] == [
        (item.event_id, item.timestamp, item.payload, item.episode_id, item.lineage_id)
        for item in expected
    ]
    assert len({item.event_id for item in actual}) == len(actual)


def test_e2_adapter_reconstructs_ordinary_state_with_e2_defaults() -> None:
    neuron = MultiExcursionNeuron("n", config=config())
    neuron.receive_contribution(0.0, 1.0)
    restored = neuron_from_ir2_e2(
        TPCNIR2((neuron_to_ir2_e2(neuron),)).neurons[0]
    )
    assert restored.mode == E1Mode.S_PENDING
    assert restored.pending_event is not None
    assert restored.pending_event.kind.value == "S_EMIT"


def test_e2_reconstruction_restores_counters_and_continues_with_unique_ids() -> None:
    neuron = MultiExcursionNeuron("n", config=config())
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 8.0, queue=queue)
    prior = neuron.receive_event(queue.pop_ready(0.01), queue)
    assert prior is not None
    restored = round_trip(neuron)
    assert restored._event_identity == neuron._event_identity
    assert restored._episode_identity == neuron._episode_identity
    assert restored._lineage_identity == neuron._lineage_identity
    assert restored._input_identity == neuron._input_identity

    outputs = drain(restored, EventQueue(64))
    assert all(item.event_id != prior.event_id for item in outputs)
    assert all(item.sequence > prior.sequence for item in outputs)
