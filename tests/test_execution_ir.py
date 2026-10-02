import math

import pytest

from tpcn import (
    ApproximationContract,
    BackendCapabilities,
    BackendIdentity,
    EqualTimePolicy,
    EquivalenceLevel,
    Edge,
    Event,
    EventQueue,
    ExecutionIR,
    IREdge,
    IREvent,
    IRNeuron,
    IR_EXCLUDED_RUNTIME_STATE,
    IR_SCOPE_DESCRIPTION,
    SUPPORTED_ACTIVATION_MODELS,
    StatisticalRequirement,
    TPCNNeuron,
    BoundedTopology,
    edge_to_ir,
    reference_from_ir,
    topology_to_ir,
)


def test_ir_preserves_non_default_model_b_and_neuron_parameters() -> None:
    edge = IREdge("a", "b", -1.5, 0.25, 0.5, 2.5, routing_cost=3, legacy_identity=False)
    neuron = IRNeuron("b", 0.3, 1.5, 1.25, state=0.4, local_timestamp=2.0)
    ir = ExecutionIR((edge,), (neuron,), nodes=("a", "b",), fan_in_limit=2,
                     fan_out_limit=2, edge_capacity=4, routing_capacity=3,
                     event_queue_capacity=8, event_budget=20)

    restored = reference_from_ir(ir)
    assert restored.topology.edge("a", "b").edge_weight == -1.5
    assert restored.topology.edge("a", "b").divider_strength == 0.25
    assert restored.topology.edge("a", "b").reference == 0.5
    assert restored.topology.edge("a", "b").propagation_delay == 2.5
    assert restored.topology.edge("a", "b").routing_cost == 3
    assert restored.neurons["b"].decay_rate == 0.3
    assert restored.neurons["b"].neuron_gain == 1.25
    assert restored.neurons["b"].state == 0.4
    assert restored.neurons["b"].clock.timestamp == 2.0


def test_canonical_conversion_round_trips_deterministically() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b"), ((Edge("a", "b", 1.25,
        edge_weight=-0.75, divider_strength=0.6, reference=-0.2)),),
        fan_in_limit=2, fan_out_limit=2, edge_capacity=3, routing_capacity=2,
    )
    neurons = {"a": TPCNNeuron("a", decay_rate=0.2, neuron_gain=0.8),
               "b": TPCNNeuron("b", decay_rate=0.4, neuron_gain=1.2)}
    queue = EventQueue(4)
    queued = queue.push(Event(0.0, "a", "b", "signal", 0.25))
    ir = topology_to_ir(topology, neurons, (queued,), event_queue_capacity=4, event_budget=10)

    encoded = ir.to_json()
    assert encoded == ir.to_json()
    decoded = ExecutionIR.from_json(encoded)
    assert decoded == ir
    restored = reference_from_ir(decoded)
    assert tuple(restored.topology.edges) == tuple(topology.edges)
    assert restored.neurons["b"].neuron_gain == 1.2
    assert restored.events[0].sequence == 0


def test_ir_rejects_unsupported_versions_and_invalid_bounds() -> None:
    with pytest.raises(ValueError, match="unsupported"):
        ExecutionIR.from_dict({"version": "TPCN-IR-999"})
    with pytest.raises(ValueError):
        IREdge("a", "b", 1.0, 1.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        IRNeuron("a", 0.0, 1.0, 1.0, state=2.0)
    with pytest.raises(ValueError):
        IREvent(0.0, "a", "b", "signal", None, sequence=-2)


def test_ir_accepts_only_the_canonical_tanh_activation_model() -> None:
    assert SUPPORTED_ACTIVATION_MODELS == frozenset({"tanh"})
    assert IRNeuron("a", 0.0, 1.0, 1.0, activation_model="tanh").activation_model == "tanh"
    with pytest.raises(ValueError, match="unsupported activation_model"):
        IRNeuron("a", 0.0, 1.0, 1.0, activation_model="relu")
    with pytest.raises(ValueError):
        IRNeuron("a", 0.0, 1.0, 1.0, activation_model="")


def test_reference_reconstruction_defends_against_activation_semantic_loss() -> None:
    neuron = IRNeuron("a", 0.0, 1.0, 1.0)
    object.__setattr__(neuron, "activation_model", "custom")
    ir = ExecutionIR((), (neuron,), nodes=("a",))
    with pytest.raises(ValueError, match="unsupported activation_model"):
        reference_from_ir(ir)


def test_event_sequence_identities_are_unique_across_the_pending_set() -> None:
    events = (
        IREvent(1.0, "a", "b", "signal", "first", sequence=4),
        IREvent(2.0, "a", "b", "signal", "second", sequence=4),
    )
    with pytest.raises(ValueError, match="unique sequence"):
        ExecutionIR((), (), events, nodes=("a", "b"), event_queue_capacity=2)


def test_equal_time_event_order_survives_serialization_and_reconstruction() -> None:
    events = (
        IREvent(1.0, "a", "b", "signal", "later", sequence=8),
        IREvent(1.0, "a", "b", "signal", "first", sequence=3),
    )
    ir = ExecutionIR((), (), events, nodes=("a", "b"), event_queue_capacity=2)
    decoded = ExecutionIR.from_json(ir.to_json())
    restored = reference_from_ir(decoded)
    assert [event.sequence for event in decoded.events] == [8, 3]
    assert [event.sequence for event in restored.events] == [3, 8]
    assert [event.payload for event in restored.events] == ["first", "later"]


def test_approximation_contract_declares_ir_tolerances_statistics_and_boundary() -> None:
    contract = ApproximationContract(
        BackendIdentity.GPU_FPGA_APPROXIMATION,
        frozenset(EquivalenceLevel),
        EqualTimePolicy.COINCIDENT_WINDOW,
        supported_ir_version="TPCN-IR-1",
        numeric_tolerance=0.0,
        timing_tolerance=0.25,
        statistical_requirement=StatisticalRequirement.REQUIRED,
        approximation_boundary=frozenset({"quantized arithmetic", "coincident equal-time fan-in"}),
    )
    assert contract.supported_ir_version == "TPCN-IR-1"
    assert contract.numeric_tolerance == 0.0
    assert contract.timing_tolerance == 0.25
    assert contract.statistical_requirement is StatisticalRequirement.REQUIRED
    assert contract.approximation_boundary == frozenset(
        {"quantized arithmetic", "coincident equal-time fan-in"}
    )
    assert contract.equivalence_levels == frozenset(EquivalenceLevel)


@pytest.mark.parametrize("field", ("numeric_tolerance", "timing_tolerance"))
@pytest.mark.parametrize("value", (-1.0, float("nan"), float("inf")))
def test_approximation_contract_rejects_invalid_tolerances(field: str, value: float) -> None:
    with pytest.raises(ValueError):
        ApproximationContract(
            BackendIdentity.GPU_NATIVE,
            frozenset({EquivalenceLevel.E0_SEMANTIC}),
            EqualTimePolicy.SEQUENTIAL_DETERMINISTIC,
            **{field: value},
        )


def test_approximation_contract_rejects_unknown_ir_and_preserves_optional_none() -> None:
    with pytest.raises(ValueError, match="supported canonical IR"):
        ApproximationContract(
            BackendIdentity.GPU_NATIVE,
            frozenset(),
            EqualTimePolicy.SEQUENTIAL_DETERMINISTIC,
            supported_ir_version="TPCN-IR-999",
        )
    contract = ApproximationContract(
        BackendIdentity.GPU_NATIVE,
        frozenset({EquivalenceLevel.E0_SEMANTIC}),
        EqualTimePolicy.SEQUENTIAL_DETERMINISTIC,
    )
    assert contract.numeric_tolerance is None
    assert contract.timing_tolerance is None
    assert contract.statistical_requirement is StatisticalRequirement.NONE
    assert contract.approximation_boundary == frozenset()
    assert contract == ApproximationContract(
        BackendIdentity.GPU_NATIVE,
        frozenset({EquivalenceLevel.E0_SEMANTIC}),
        EqualTimePolicy.SEQUENTIAL_DETERMINISTIC,
    )


def test_ir_scope_excludes_full_live_runtime_checkpoint_state() -> None:
    assert "not a full live-runtime checkpoint" in IR_SCOPE_DESCRIPTION
    assert "eligibility state" in IR_EXCLUDED_RUNTIME_STATE


def test_backend_contract_names_capabilities_without_claiming_implementation() -> None:
    capabilities = BackendCapabilities(
        BackendIdentity.GPU_FPAA_APPROXIMATION,
        equivalence_levels=frozenset({EquivalenceLevel.E0_SEMANTIC, EquivalenceLevel.E2_EVENT}),
        equal_time_policies=frozenset({EqualTimePolicy.COINCIDENT_WINDOW}),
    )
    assert capabilities.implemented is False
    assert EqualTimePolicy.SEQUENTIAL_DETERMINISTIC.value == "sequential_deterministic"
    assert EqualTimePolicy.COINCIDENT_WINDOW in capabilities.equal_time_policies
    assert "window" not in ExecutionIR((), (), nodes=("a",)).to_json()


def test_ir_does_not_depend_on_tpcv_records() -> None:
    ir = ExecutionIR((), (IRNeuron("a", 0.0, 1.0, 1.0),), nodes=("a",))
    assert "TPCV" not in ir.to_json()
    assert "cuda" not in ir.to_json().lower()
    assert math.isfinite(IRNeuron("a", 0.0, 1.0, 1.0).state)
