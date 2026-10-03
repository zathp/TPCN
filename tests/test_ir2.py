import pytest

from tpcn import (
    EXCURSION_V1,
    EXECUTION_ORDER_POLICY,
    E1Config,
    IR2DowngradeError,
    IR2Mode,
    IR2Neuron,
    IR2PendingInternal,
    IR2PendingKind,
    IR2Event,
    IR2_TPCV_SEPARATION,
    IR2UnsupportedRuntimeError,
    MPhase,
    SingleExcursionNeuron,
    TANH_LEGACY,
    TPCNIR2,
    downgrade_ir2_to_ir1,
    ir2_from_ir1,
    neuron_from_ir2,
    neuron_from_ir2_e2,
    neuron_to_ir2,
)
from tpcn.execution_ir import ExecutionIR, IREdge, IREvent, IRNeuron


def test_e1_pending_round_trip_is_deterministic_and_continuable() -> None:
    neuron = SingleExcursionNeuron("n", config=E1Config(emission_delay=0.75))
    neuron.receive_contribution(0.0, 1.0)
    record = neuron_to_ir2(neuron)
    document = TPCNIR2((record,))

    restored_document = TPCNIR2.from_json(document.to_json())
    restored = neuron_from_ir2(restored_document.neurons[0])
    assert restored_document.to_json() == document.to_json()
    assert restored.pending_event == neuron.pending_event
    assert restored.process_pending() is not None
    assert restored.last_emission is not None


def test_non_default_config_and_truncated_provenance_are_preserved() -> None:
    neuron = SingleExcursionNeuron("n", config=E1Config(provenance_capacity=2, x_max=9.0))
    for index in range(3):
        neuron.receive_contribution(float(index), 0.1, event_id=f"input-{index}")
    record = neuron_to_ir2(neuron)
    assert record.provenance_truncated is True
    assert [entry.causal_event_id for entry in record.provenance] == ["input-1", "input-2"]
    restored = neuron_from_ir2(record)
    assert restored.provenance == neuron.provenance
    assert restored.provenance_truncated is True


def test_identity_counters_continue_after_reconstruction_and_reset() -> None:
    neuron = SingleExcursionNeuron("n")
    neuron.receive_contribution(0.0, 1.0)
    first = neuron_to_ir2(neuron)
    restored = neuron_from_ir2(first)
    restored.process_pending()
    restored.reset(timestamp=2.0)
    restored.receive_contribution(2.0, 1.0)
    restored.process_pending()
    assert restored.last_emission is not None
    assert restored.last_emission.event_id.endswith(":2")


def test_unknown_and_impossible_records_are_rejected() -> None:
    neuron = SingleExcursionNeuron("n")
    record = neuron_to_ir2(neuron).to_dict()
    record["dynamics_model"] = "UNKNOWN"
    with pytest.raises(ValueError, match="unsupported"):
        IR2Neuron.from_dict(record)
    record = neuron_to_ir2(neuron).to_dict()
    record["ir_version"] = "TPCN-IR-999"
    with pytest.raises(ValueError, match="unsupported"):
        TPCNIR2.from_dict(record)


def test_m_is_schema_valid_but_not_supported_by_e1_runtime() -> None:
    pending = IR2PendingInternal("n", IR2PendingKind.M_EMIT, 1.0, 1, 1)
    record = IR2Neuron(
        "n", mode=IR2Mode.M_ACTIVE, m_phase=MPhase.ARMED, multi_episode_id=1,
        lineage_id=1, next_episode_identity=1, next_lineage_identity=1,
        pending_internal_event=pending, generation_token=1,
    )
    encoded = TPCNIR2((record,)).to_json()
    restored = TPCNIR2.from_json(encoded).neurons[0]
    with pytest.raises(IR2UnsupportedRuntimeError, match="M_ACTIVE"):
        neuron_from_ir2(restored)


@pytest.mark.parametrize(
    ("phase", "kind"),
    ((MPhase.ARMED, IR2PendingKind.M_REARM), (MPhase.REFRACTORY, IR2PendingKind.M_EMIT)),
)
def test_m_phase_and_pending_kind_must_agree(phase: MPhase, kind: IR2PendingKind) -> None:
    with pytest.raises(ValueError, match="inconsistent"):
        IR2Neuron(
            "n", mode=IR2Mode.M_ACTIVE, m_phase=phase, multi_episode_id=1,
            lineage_id=1, next_episode_identity=1, next_lineage_identity=1,
            generation_token=1,
            pending_internal_event=IR2PendingInternal("n", kind, 1.0, 1, 1),
        )


def test_m_pending_episode_must_match_multi_episode() -> None:
    with pytest.raises(ValueError, match="ownership"):
        IR2Neuron(
            "n", mode=IR2Mode.M_ACTIVE, m_phase=MPhase.ARMED, multi_episode_id=2,
            lineage_id=1, next_episode_identity=2, next_lineage_identity=1,
            generation_token=1,
            pending_internal_event=IR2PendingInternal("n", IR2PendingKind.M_EMIT, 1.0, 1, 1),
        )


def test_pending_internal_event_must_be_strictly_future_for_e2_configuration() -> None:
    with pytest.raises(ValueError, match="strictly future"):
        IR2Neuron(
            "n",
            x=1.0,
            local_last_update_time=0.5,
            mode=IR2Mode.S_PENDING,
            ordinary_episode_id=1,
            lineage_id=1,
            captured_polarity=1,
            next_episode_identity=1,
            next_lineage_identity=1,
            generation_token=1,
            pending_internal_event=IR2PendingInternal(
                "n", IR2PendingKind.S_EMIT, 0.5, 1, 1
            ),
        )


def test_m_active_identity_high_water_and_counter_budget_are_validated() -> None:
    pending = IR2PendingInternal("n", IR2PendingKind.M_EMIT, 1.0, 1, 1)
    with pytest.raises(ValueError, match="high-water"):
        IR2Neuron(
            "n",
            mode=IR2Mode.M_ACTIVE,
            m_phase=MPhase.ARMED,
            multi_episode_id=1,
            lineage_id=1,
            pending_internal_event=pending,
            generation_token=1,
        )
    with pytest.raises(ValueError, match="event budget"):
        IR2Neuron(
            "n",
            mode=IR2Mode.M_ACTIVE,
            m_phase=MPhase.ARMED,
            multi_episode_id=1,
            lineage_id=1,
            next_episode_identity=1,
            next_lineage_identity=1,
            next_event_identity=2,
            pending_internal_event=pending,
            generation_token=1,
            event_budget=1,
        )


def _valid_ir2_mode_record(
    mode: IR2Mode,
    *,
    event_budget: int = 5,
) -> IR2Neuron:
    generation = 1
    pending_kind = {
        IR2Mode.S_PENDING: IR2PendingKind.S_EMIT,
        IR2Mode.S_RETURN: None,
        IR2Mode.M_ACTIVE: IR2PendingKind.M_EMIT,
        IR2Mode.N: None,
    }[mode]
    pending = (
        None
        if pending_kind is None
        else IR2PendingInternal("n", pending_kind, 1.0, 1, generation)
    )
    return IR2Neuron(
        neuron_id="n",
        mode=mode,
        x=1.0,
        ordinary_episode_id=1 if mode in (IR2Mode.S_PENDING, IR2Mode.S_RETURN) else None,
        lineage_id=1 if mode != IR2Mode.N else None,
        captured_polarity=1 if mode == IR2Mode.S_PENDING else None,
        m_phase=MPhase.ARMED if mode == IR2Mode.M_ACTIVE else None,
        multi_episode_id=1 if mode == IR2Mode.M_ACTIVE else None,
        pending_internal_event=pending,
        event_budget=event_budget,
        generation_token=generation,
        next_episode_identity=1 if mode != IR2Mode.N else 0,
        next_lineage_identity=1 if mode != IR2Mode.N else 0,
    )


@pytest.mark.parametrize(
    ("mode", "identity_field", "counter_field"),
    (
        (IR2Mode.S_PENDING, "ordinary_episode_id", "next_episode_identity"),
        (IR2Mode.S_PENDING, "lineage_id", "next_lineage_identity"),
        (IR2Mode.S_RETURN, "ordinary_episode_id", "next_episode_identity"),
        (IR2Mode.S_RETURN, "lineage_id", "next_lineage_identity"),
        (IR2Mode.M_ACTIVE, "multi_episode_id", "next_episode_identity"),
        (IR2Mode.M_ACTIVE, "lineage_id", "next_lineage_identity"),
    ),
)
def test_active_identity_ahead_of_high_water_is_rejected(
    mode: IR2Mode,
    identity_field: str,
    counter_field: str,
) -> None:
    record = _valid_ir2_mode_record(mode)
    values = record.to_dict()
    values[identity_field] = 2
    values[counter_field] = 1

    with pytest.raises(ValueError, match="high-water"):
        IR2Neuron.from_dict(values)


@pytest.mark.parametrize("mode", tuple(IR2Mode))
def test_active_identity_equal_to_high_water_is_valid(mode: IR2Mode) -> None:
    record = _valid_ir2_mode_record(mode)
    assert IR2Neuron.from_dict(record.to_dict()) == record


def test_valid_s_pending_high_water_allocates_new_m_identity() -> None:
    record = _valid_ir2_mode_record(IR2Mode.S_PENDING)
    restored = neuron_from_ir2_e2(record)
    prior_ordinary_id = restored.ordinary_episode_id
    prior_lineage_id = restored.lineage_id

    restored.receive_contribution(0.01, 3.1)

    assert prior_ordinary_id == record.next_episode_identity
    assert restored.multi_episode_id is not None
    assert restored.multi_episode_id > prior_ordinary_id
    assert restored._episode_identity == restored.multi_episode_id
    assert restored.lineage_id == prior_lineage_id
    assert restored._lineage_identity == record.next_lineage_identity


@pytest.mark.parametrize("mode", tuple(IR2Mode))
@pytest.mark.parametrize(
    "counter_name",
    (
        "generation_token",
        "next_event_identity",
        "next_episode_identity",
        "next_lineage_identity",
        "next_input_identity",
        "processed_event_count",
        "input_contribution_count",
    ),
)
@pytest.mark.parametrize(("offset", "valid"), ((-1, True), (0, True), (1, False)))
def test_every_mode_validates_all_execution_counters_against_budget(
    mode: IR2Mode,
    counter_name: str,
    offset: int,
    valid: bool,
) -> None:
    values = _valid_ir2_mode_record(mode, event_budget=5).to_dict()
    values[counter_name] = 5 + offset
    if counter_name == "generation_token" and values["pending_internal_event"] is not None:
        values["pending_internal_event"]["generation"] = 5 + offset

    if valid:
        record = IR2Neuron.from_dict(values)
        assert record.event_budget == 5
    else:
        with pytest.raises(ValueError, match="event budget"):
            IR2Neuron.from_dict(values)


@pytest.mark.parametrize(
    ("pending_time", "e2_valid"),
    ((-0.1, False), (0.0, False), (0.1, True)),
)
def test_e2_reconstruction_requires_strictly_future_ordinary_pending_event(
    pending_time: float,
    e2_valid: bool,
) -> None:
    values = _valid_ir2_mode_record(IR2Mode.S_PENDING, event_budget=5).to_dict()
    values["local_last_update_time"] = 0.0
    values["delta_t_m_emit"] = None
    values["delta_t_m_rearm"] = None
    values["delta_x_e"] = None
    values["pending_internal_event"]["timestamp"] = pending_time

    if pending_time < 0.0:
        with pytest.raises(ValueError, match="wrong owner or timestamp"):
            IR2Neuron.from_dict(values)
        return

    record = IR2Neuron.from_dict(values)
    if e2_valid:
        assert neuron_from_ir2_e2(record).pending_event.timestamp == pending_time
    else:
        with pytest.raises(ValueError, match="strictly after local time"):
            neuron_from_ir2_e2(record)


def test_equal_time_pending_remains_supported_by_historical_e1_adapter() -> None:
    values = _valid_ir2_mode_record(IR2Mode.S_PENDING).to_dict()
    values["pending_internal_event"]["timestamp"] = 0.0
    values["delta_t_m_emit"] = None
    values["delta_t_m_rearm"] = None
    values["delta_x_e"] = None
    record = IR2Neuron.from_dict(values)

    restored = neuron_from_ir2(record)

    assert restored.process_pending() is not None
    assert restored.last_emission is not None
    assert restored.last_emission.timestamp == record.local_last_update_time


def test_ir1_upgrade_is_explicit_and_excursion_downgrade_is_rejected() -> None:
    ir1 = ExecutionIR(
        (IREdge("a", "b", -1.0, 0.5, 0.25, 2.0),),
        (IRNeuron("a", 0.0, 2.0, 1.0), IRNeuron("b", 0.5, 3.0, 1.7)),
        (IREvent(1.0, "a", "b", "signal", 0.5, sequence=4),),
        nodes=("a", "b"),
        fan_in_limit=3, fan_out_limit=4, edge_capacity=2, routing_capacity=5,
        event_queue_capacity=6, event_budget=7,
    )
    upgraded = ir2_from_ir1(ir1)
    assert all(record.dynamics_model == TANH_LEGACY for record in upgraded.neurons)
    assert upgraded.neurons[1].neuron_gain == 1.7
    assert upgraded.edges[0].propagation_delay == 2.0
    assert upgraded.events == (IR2Event(1.0, "a", "b", "signal", 0.5, 4),)
    assert upgraded.fan_in_limit == 3
    assert upgraded.fan_out_limit == 4
    assert upgraded.edge_capacity == 2
    assert upgraded.routing_capacity == 5
    assert upgraded.event_queue_capacity == 6
    assert upgraded.event_budget == 7
    assert upgraded.execution_order_policy == EXECUTION_ORDER_POLICY
    with pytest.raises(IR2DowngradeError):
        downgrade_ir2_to_ir1(TPCNIR2((neuron_to_ir2(SingleExcursionNeuron("n")),)))


def test_schema_does_not_claim_visualization_or_backend_state() -> None:
    assert "TPCV-1" in IR2_TPCV_SEPARATION
    assert EXCURSION_V1 != TANH_LEGACY
