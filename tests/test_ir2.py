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
    IR2_TPCV_SEPARATION,
    IR2UnsupportedRuntimeError,
    MPhase,
    SingleExcursionNeuron,
    TANH_LEGACY,
    TPCNIR2,
    downgrade_ir2_to_ir1,
    ir2_from_ir1,
    neuron_from_ir2,
    neuron_to_ir2,
)
from tpcn.execution_ir import ExecutionIR, IREdge, IRNeuron


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
        pending_internal_event=pending, generation_token=1,
    )
    encoded = TPCNIR2((record,)).to_json()
    restored = TPCNIR2.from_json(encoded).neurons[0]
    with pytest.raises(IR2UnsupportedRuntimeError, match="M_ACTIVE"):
        neuron_from_ir2(restored)


def test_ir1_upgrade_is_explicit_and_excursion_downgrade_is_rejected() -> None:
    ir1 = ExecutionIR(
        (IREdge("a", "b", -1.0, 0.5, 0.25, 2.0),),
        (IRNeuron("a", 0.0, 2.0, 1.0), IRNeuron("b", 0.5, 3.0, 1.0)),
        nodes=("a", "b"),
        edge_capacity=2,
    )
    upgraded = ir2_from_ir1(ir1)
    assert all(record.dynamics_model == TANH_LEGACY for record in upgraded.neurons)
    assert upgraded.edges[0].propagation_delay == 2.0
    assert upgraded.execution_order_policy == EXECUTION_ORDER_POLICY
    with pytest.raises(IR2DowngradeError):
        downgrade_ir2_to_ir1(TPCNIR2((neuron_to_ir2(SingleExcursionNeuron("n")),)))


def test_schema_does_not_claim_visualization_or_backend_state() -> None:
    assert "TPCV-1" in IR2_TPCV_SEPARATION
    assert EXCURSION_V1 != TANH_LEGACY
