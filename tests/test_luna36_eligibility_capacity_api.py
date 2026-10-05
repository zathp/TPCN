from __future__ import annotations

import pytest

from tpcn.eligibility import EligibilityCapacityError
from tpcn.excursion_neuron import E1Config, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.ir2 import IR2Edge, IR2Neuron, TPCNIR2, neuron_to_ir2_e2
from tpcn.topology import BoundedTopology


def _runtime(nodes=("n0", "n1"), **kwargs) -> ExcursionCharacterRuntime:
    topology = BoundedTopology.from_edges(
        nodes, (), fan_in_limit=2, fan_out_limit=2, edge_capacity=4, routing_capacity=4
    )
    neurons = tuple(
        MultiExcursionNeuron(
            node, config=E1Config(emission_delay=0.5, m_emit_delay=1.0, m_rearm_delay=0.5,
                                  delta_x_e=1.0, event_budget=256)
        )
        for node in nodes
    )
    return ExcursionCharacterRuntime(
        neurons, topology, queue_capacity=16, event_budget=64, settling_horizon=4.0,
        prediction_capacity=kwargs.pop("prediction_capacity", 8), prediction_expiry=4.0,
        max_activity_events=64, namespace="t", **kwargs,
    )


def _start(runtime: ExcursionCharacterRuntime) -> None:
    runtime.start_character(
        "c", 0, timestamp=0.0, predictor_source="n0", readout_sources=("n0",), input_destination="n0"
    )


def _ledger_capacities(runtime: ExcursionCharacterRuntime) -> dict[str, int]:
    return {node: ledger.max_traces for node, ledger in runtime._ledgers.items()}


@pytest.mark.parametrize("nodes", (("n0",), ("n0", "n1")))
def test_default_preserves_legacy_formula(nodes) -> None:
    runtime = _runtime(nodes)
    expected = 8 * len(nodes)
    assert runtime.eligibility_capacity == expected
    _start(runtime)
    assert _ledger_capacities(runtime) == {node: expected for node in nodes}


def test_explicit_capacity_is_per_ledger_and_leaves_prediction_capacity() -> None:
    runtime = _runtime(eligibility_capacity=3)
    assert runtime.eligibility_capacity == 3
    assert runtime.prediction_capacity == 8
    _start(runtime)
    assert _ledger_capacities(runtime) == {"n0": 3, "n1": 3}
    assert runtime._predictor.max_outstanding == 8


@pytest.mark.parametrize("value", (True, False, 1.0, "2", 0, -1))
def test_invalid_capacity_is_rejected(value) -> None:
    with pytest.raises(ValueError, match="eligibility_capacity"):
        _runtime(eligibility_capacity=value)


def test_property_is_read_only() -> None:
    runtime = _runtime()
    with pytest.raises(AttributeError):
        runtime.eligibility_capacity = 5  # type: ignore[misc]


def test_too_small_capacity_still_raises_bounded_error() -> None:
    runtime = _runtime(eligibility_capacity=1)
    _start(runtime)
    with pytest.raises(EligibilityCapacityError):
        for timestamp in (0.0, 5.0, 10.0):
            runtime.admit_external_batch(((timestamp, 1.2),))


def _document() -> TPCNIR2:
    return TPCNIR2(
        (neuron_to_ir2_e2(MultiExcursionNeuron("n0")), IR2Neuron("n1")),
        (IR2Edge("n0", "n1", 1.0, 1.0, 0.0, 1.0),),
        nodes=("n0", "n1"), fan_in_limit=2, fan_out_limit=2,
        edge_capacity=4, routing_capacity=4, event_queue_capacity=16,
    )


def _from_ir2(**kwargs) -> ExcursionCharacterRuntime:
    return ExcursionCharacterRuntime.from_quiescent_ir2(
        TPCNIR2.from_json(_document().to_json()), queue_capacity=16, event_budget=64,
        settling_horizon=4.0, prediction_capacity=8, prediction_expiry=4.0,
        max_activity_events=64, namespace="ir2", **kwargs,
    )


def test_from_quiescent_ir2_default_and_forwarding() -> None:
    assert _from_ir2().eligibility_capacity == 16
    runtime = _from_ir2(eligibility_capacity=5)
    assert runtime.eligibility_capacity == 5
    _start(runtime)
    assert _ledger_capacities(runtime) == {"n0": 5, "n1": 5}
    with pytest.raises(ValueError, match="eligibility_capacity"):
        _from_ir2(eligibility_capacity=0)


def test_default_replay_is_deterministic_and_serialization_unchanged() -> None:
    traces = []
    for _ in range(2):
        runtime = _runtime()
        _start(runtime)
        runtime.admit_external_batch(((0.0, 1.2),))
        traces.append(runtime.end_character(
            last_external_timestamp=0.0, reward=0.0, reward_delay=0.0, reward_message_id="r").trace)
    assert traces[0] == traces[1]
    assert "eligibility_capacity" not in _document().to_json()
