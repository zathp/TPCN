import math

import pytest

from tpcn import (
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
