from __future__ import annotations

from dataclasses import asdict, replace

import pytest

from tpcn.event_runtime import EventType
from tpcn.cpu_visualization import CPUTrainingCapture
from tpcn.excursion_neuron import E1Config, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.experiments import (
    ExperimentConfig,
    ExperimentRunner,
    SyntheticExample,
)
from tpcn.stroke_dataset import StrokePoint
from tpcn.structural_observation import (
    StructuralEmissionObservation,
    StructuralObservationPlane,
    StructuralObservationSnapshot,
)
from tpcn.structural_plasticity import CandidateEvidence, StructuralPlasticityController
from tpcn.topology import BoundedTopology, Edge
from tpcn.visualization import EXCURSION_FORMAT_VERSION, parse_snapshot


def _plane(
    neighbors: dict[str, tuple[str, ...]] | None = None,
    *,
    nodes: tuple[str, ...] = ("s", "d"),
    history_capacity: int = 8,
    candidate_capacity: int = 8,
    maximum_score: int = 8,
    neighborhood_limit: int = 2,
    reverse_observer_limit: int = 2,
) -> StructuralObservationPlane:
    normalized = (
        {"s": ("d",), "d": ()}
        if neighbors is None and nodes == ("s", "d")
        else neighbors
    )
    assert normalized is not None
    return StructuralObservationPlane(
        nodes,
        normalized,
        neighborhood_limit=neighborhood_limit,
        reverse_observer_limit=reverse_observer_limit,
        history_capacity=history_capacity,
        candidate_capacity=candidate_capacity,
        association_window=2.0,
        maximum_score=maximum_score,
        propagation_delay=0.4,
    )


def _runtime(
    *,
    callback=None,
    nodes: tuple[str, ...] = ("n0", "n1"),
    edges: tuple[Edge, ...] = (),
    payload: float = 1.2,
    topology: BoundedTopology | None = None,
) -> tuple[ExcursionCharacterRuntime, object]:
    if topology is None:
        topology = BoundedTopology.from_edges(
            nodes,
            edges,
            fan_in_limit=2,
            fan_out_limit=2,
            edge_capacity=8,
            routing_capacity=8,
        )
    neurons = tuple(
        MultiExcursionNeuron(
            node,
            config=E1Config(
                emission_delay=0.1,
                m_emit_delay=0.2,
                m_rearm_delay=0.1,
                delta_x_e=0.1,
                event_budget=2048,
            ),
        )
        for node in nodes
    )
    runtime = ExcursionCharacterRuntime(
        neurons,
        topology,
        queue_capacity=128,
        event_budget=1024,
        settling_horizon=4.0,
        prediction_capacity=32,
        prediction_expiry=4.0,
        max_activity_events=1024,
        namespace="luna28-test",
        emission_observer=callback,
    )
    runtime.start_character(
        "character",
        0,
        timestamp=0.0,
        predictor_source=nodes[0],
        readout_sources=nodes,
        input_destination=nodes[0],
    )
    runtime.admit_external_batch(((0.0, payload),))
    result = runtime.end_character(
        last_external_timestamp=0.0,
        reward=0.0,
        reward_delay=0.0,
        reward_message_id="character:reward",
    )
    return runtime, result


def _runner_config(
    neighbors: dict[str, tuple[str, ...]],
    *,
    growth: bool = True,
    **overrides: object,
) -> ExperimentConfig:
    values: dict[str, object] = {
        "epochs": 1,
        "max_points": 4,
        "structural_observation": True,
        "structural_plasticity": growth,
        "structural_policy": "e2_local_temporal" if growth else "baseline",
        "structural_neighbors": neighbors,
        "structural_neighborhood_limit": 2,
        "structural_reverse_observer_limit": 2,
        "structural_association_window": 4.0,
        "structural_history_capacity": 8,
        "structural_candidate_capacity": 4,
        "structural_maximum_score": 3,
        "structural_growth_delay": 0.4,
        "structural_growth_attempt_budget": 4,
        "topology_node_count": len(neighbors),
        "topology_initial_edges": 0,
        "topology_fan_in": 2,
        "topology_fan_out": 2,
        "topology_edge_capacity": 8,
        "queue_capacity": 128,
        "event_budget": 1024,
        "settling_horizon": 4.0,
        "reward_mode": "neutral",
    }
    values.update(overrides)
    return ExperimentConfig(**values)


def _example(label: str = "A", *, example_id: str = "character") -> SyntheticExample:
    return SyntheticExample(
        example_id,
        (StrokePoint(0.6, 0.6, timestamp=0.0),),
        label,
    )


def _runner(
    neighbors: dict[str, tuple[str, ...]],
    *,
    growth: bool = True,
    **overrides: object,
) -> tuple[ExperimentRunner, SyntheticExample]:
    config = _runner_config(neighbors, growth=growth, **overrides)
    runner = ExperimentRunner(config)
    example = _example()
    runner._ensure_topology((example,))
    return runner, example


def _growth_runner(
    label: str = "A",
    **config_overrides: object,
) -> tuple[ExperimentRunner, SyntheticExample]:
    nodes = ("neuron-0", "neuron-1", "neuron-2")
    neighbors = {"neuron-0": ("neuron-2",), "neuron-1": (), "neuron-2": ()}
    example = SyntheticExample(
        "causal-character",
        tuple(StrokePoint(3.5, 3.5, timestamp=float(index)) for index in range(4)),
        label,
    )
    runner = ExperimentRunner(
        _runner_config(
            neighbors,
            growth=True,
            max_points=4,
            settling_horizon=8.0,
            topology_edge_capacity=4,
            **config_overrides,
        )
    )
    runner._ensure_topology((example,))
    topology = BoundedTopology.from_edges(
        nodes,
        (
            Edge("neuron-0", "neuron-1", 0.2, divider_strength=0.0, reference=1.0),
            Edge("neuron-1", "neuron-2", 0.2, divider_strength=0.0, reference=1.0),
        ),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=4,
        routing_capacity=4,
    )
    runner._topology = topology
    runner.plasticity.topology = topology
    runner._network.set_topology(topology)
    return runner, example


def _snapshot(*candidates: CandidateEvidence) -> StructuralObservationSnapshot:
    return StructuralObservationSnapshot(candidates, (), 0, 0, 0, ())


def _candidate(source: str, destination: str, *, score: int = 1, delay: float = 0.4) -> CandidateEvidence:
    return CandidateEvidence(source, source, destination, score, delay, f"{source}-{destination}-{score}")


def _signature(topology: BoundedTopology) -> tuple[tuple[str, str, float], ...]:
    return tuple(
        (edge.source, edge.destination, float(edge.propagation_delay))
        for edge in topology.edges
    )


def _causal_character(
    topology: BoundedTopology,
    *,
    callback=None,
) -> tuple[ExcursionCharacterRuntime, object]:
    return _runtime(
        callback=callback,
        nodes=topology.nodes,
        payload=7.0,
        topology=topology,
    )


def _chain_topology() -> BoundedTopology:
    return BoundedTopology.from_edges(
        ("n0", "n1", "n2"),
        (
            Edge("n0", "n1", 0.2, divider_strength=0.0, reference=1.0),
            Edge("n1", "n2", 0.2, divider_strength=0.0, reference=1.0),
        ),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=4,
        routing_capacity=4,
    )


def test_e2_structural_observer_sees_only_actual_excursions() -> None:
    plane = _plane({"n0": ("n1",), "n1": ()}, nodes=("n0", "n1"))
    runtime, result = _runtime(callback=plane.observe_emission)

    snapshot = plane.freeze()
    assert result.emission_count > 0
    assert snapshot.observation_count == result.emission_count
    assert {item.event_id for item in snapshot.observations} == {
        emission.event_id for emission in runtime._emissions
    }
    assert all(isinstance(item, StructuralEmissionObservation) for item in snapshot.observations)
    assert all(not hasattr(item, "payload") for item in snapshot.observations)


def test_e2_silence_creates_no_structural_observation() -> None:
    plane = _plane({"n0": ("n1",), "n1": ()}, nodes=("n0", "n1"))
    _, result = _runtime(callback=plane.observe_emission, payload=0.01)

    snapshot = plane.freeze()
    assert result.emission_count == 0
    assert snapshot.observation_count == 0
    assert snapshot.observations == ()
    assert snapshot.candidates == ()


def test_structural_observation_does_not_change_character_result() -> None:
    topology_a = _chain_topology()
    topology_b = _chain_topology()
    plane = _plane(
        {"n0": ("n2",), "n1": (), "n2": ()},
        nodes=("n0", "n1", "n2"),
    )
    runtime_with_observation, result_with_observation = _causal_character(
        topology_a,
        callback=plane.observe_emission,
    )
    runtime_without_observation, result_without_observation = _causal_character(topology_b)

    assert result_with_observation == result_without_observation
    assert _signature(topology_a) == _signature(topology_b)
    assert runtime_with_observation._active is False
    assert runtime_without_observation._active is False
    assert plane.freeze().observation_count == result_with_observation.emission_count


def test_non_neighbor_emission_is_not_structurally_visible() -> None:
    plane = _plane(
        {"s": ("d",), "d": (), "other": ()},
        nodes=("s", "d", "other"),
    )
    plane.observe_emission("s", "s-1", 0.0)
    plane.observe_emission("other", "other-1", 0.5)
    snapshot = plane.freeze()

    assert not any(item.observer == "s" and item.emitter_id == "other" for item in snapshot.observations)
    assert snapshot.candidates == ()


def test_equal_time_emissions_do_not_form_temporal_candidate() -> None:
    plane = _plane()
    plane.observe_emission("s", "s-1", 1.0)
    plane.observe_emission("d", "d-1", 1.0)

    assert plane.freeze().candidates == ()


def test_source_before_neighbor_forms_bounded_candidate() -> None:
    plane = _plane()
    plane.observe_emission("s", "s-1", 1.0)
    plane.observe_emission("d", "d-1", 1.5)
    candidates = plane.freeze().candidates

    assert len(candidates) == 1
    assert (candidates[0].observer, candidates[0].source, candidates[0].destination) == ("s", "s", "d")
    assert candidates[0].score == 1
    assert candidates[0].propagation_delay == 0.4


def test_candidate_score_saturates_at_declared_maximum() -> None:
    plane = _plane(maximum_score=2)
    for index in range(4):
        plane.observe_emission("s", f"s-{index}", float(index * 2))
        plane.observe_emission("d", f"d-{index}", float(index * 2 + 1))

    assert plane.freeze().candidates[0].score == 2


def test_candidate_capacity_is_bounded_and_reported() -> None:
    plane = _plane(
        {"s": ("a", "b"), "a": (), "b": ()},
        nodes=("s", "a", "b"),
        candidate_capacity=1,
    )
    plane.observe_emission("s", "s-1", 0.0)
    plane.observe_emission("a", "a-1", 0.5)
    plane.observe_emission("s", "s-2", 1.0)
    plane.observe_emission("b", "b-1", 1.5)
    snapshot = plane.freeze()

    assert len(snapshot.candidates) == 1
    assert snapshot.candidate_rejections == 1
    assert snapshot.candidate_rejection_reasons == (("candidate_capacity", 1),)


def test_incomplete_character_produces_no_growth() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors)
    before = _signature(runner.topology)

    decision, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=False,
        update=True,
    )

    assert decision.status == "discarded"
    assert decision.reason == "incomplete_settling"
    assert not decision.growth_attempted
    assert decision.evidence.candidates == ()
    assert decision.evidence.observations == ()
    assert runner._structural_growth_attempts == 0
    assert _signature(runner.topology) == before


def test_budget_exhausted_character_produces_no_growth() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors, structural_growth_attempt_budget=1)
    snapshot = _snapshot(_candidate("neuron-0", "neuron-1"))
    first, _ = runner._attempt_e2_growth(snapshot, successful_settling=True, update=True)
    before_second = _signature(runner.topology)
    second, exhausted = runner._attempt_e2_growth(
        snapshot,
        successful_settling=True,
        update=True,
    )

    assert first.status == "grown"
    assert second.status == "budget_exhausted"
    assert exhausted
    assert not second.growth_attempted
    assert second.evidence.candidates == ()
    assert second.evidence.observations == ()
    assert _signature(runner.topology) == before_second


def test_growth_attempt_budget_is_finite_and_reported() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, example = _runner(neighbors, structural_growth_attempt_budget=1)
    first, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=True,
        update=True,
    )
    second, exhausted = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=True,
        update=True,
    )
    assert first.growth_attempted
    assert not second.growth_attempted
    assert exhausted
    assert runner._structural_growth_attempts == 1
    assert runner.config.structural_growth_attempt_budget == 1
    assert example.label == "A"

    exhausted_runner, exhausted_example = _growth_runner(
        structural_growth_attempt_budget=1
    )
    exhausted_runner._structural_growth_attempts = 1
    exhausted = exhausted_runner._execute((exhausted_example,), 0, update=True)
    assert exhausted.metrics.structural_growth_attempts == 0
    assert exhausted.metrics.structural_growth_budget_exhausted
    assert exhausted.metrics.structural_growth_budget_remaining == 0
    assert exhausted.metrics.structural_candidate_count == 0
    assert exhausted_runner.structural_decisions[-1].status == "budget_exhausted"


def test_no_mutation_occurs_while_character_runtime_is_active() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors)
    assert runner._network is not None
    runtime = ExcursionCharacterRuntime(
        runner._network.neurons,
        runner.topology,
        queue_capacity=16,
        event_budget=16,
        settling_horizon=1.0,
        prediction_capacity=4,
        prediction_expiry=1.0,
        max_activity_events=16,
        namespace="active-test",
    )
    runtime.start_character(
        "active",
        0,
        timestamp=0.0,
        predictor_source="neuron-0",
        readout_sources=("neuron-0",),
        input_destination="neuron-0",
    )
    runner._active_runtime = runtime
    before = _signature(runner.topology)
    try:
        with pytest.raises(RuntimeError, match="runtime is active"):
            runner._attempt_e2_growth(
                _snapshot(_candidate("neuron-0", "neuron-1")),
                successful_settling=True,
                update=True,
            )
        assert _signature(runner.topology) == before
    finally:
        runtime.reset()
        runner._active_runtime = None


def test_character_evidence_is_consumed_and_reset() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, example = _runner(neighbors, growth=False)

    runner._run_excursion_example(example, 0, update=True)
    first = runner._last_structural_snapshot
    runner._run_excursion_example(example, 0, update=True)
    second = runner._last_structural_snapshot

    assert first is not None and second is not None and first is not second
    assert first.observation_count == second.observation_count
    assert first.candidates == second.candidates
    assert tuple(
        (item.observer, item.emitter_id, item.timestamp) for item in first.observations
    ) == tuple(
        (item.observer, item.emitter_id, item.timestamp) for item in second.observations
    )


def test_topology_persists_after_growth() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors)
    decision, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=True,
        update=True,
    )

    assert decision.status == "grown"
    assert runner.topology is runner.plasticity.topology
    assert runner.topology is runner._network.topology


def test_experiment_reset_destroys_structural_state() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors)
    runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=True,
        update=True,
    )
    assert runner.structural_decisions

    runner.reset()

    assert runner.topology is None
    assert runner.plasticity is None
    assert runner.structural_decisions == ()
    assert runner._structural_growth_attempts == 0
    assert runner._last_structural_snapshot is None


def test_growth_uses_same_topology_as_future_e2_routing() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors)
    runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=True,
        update=True,
    )

    assert runner.topology is runner.plasticity.topology
    assert runner.topology is runner._network.topology
    assert runner.topology.edge("neuron-0", "neuron-1").propagation_delay == 0.4


def test_admitted_growth_changes_later_real_e2_route() -> None:
    topology = _chain_topology()
    neighbors = {"n0": ("n2",), "n1": (), "n2": ()}
    plane = _plane(
        neighbors,
        nodes=("n0", "n1", "n2"),
        neighborhood_limit=1,
        reverse_observer_limit=1,
    )
    first_runtime, first_result = _causal_character(topology, callback=plane.observe_emission)
    frozen = plane.freeze()
    candidate = next(item for item in frozen.candidates if item.source == "n0")
    assert candidate.destination == "n2"
    assert ("n0", "n2", 0.4) not in _signature(topology)

    controller = StructuralPlasticityController(
        topology,
        candidate_capacity=3,
        local_neighbors=neighbors,
    )
    selected = controller.select(frozen.candidates)
    assert selected == candidate
    mutation = controller.grow(selected)
    assert mutation.status == "grown"
    grown_topology = controller.topology
    assert grown_topology is not topology
    assert grown_topology.edge("n0", "n2").propagation_delay == 0.4

    baseline = _chain_topology()
    baseline_runtime, baseline_result = _causal_character(baseline)
    later_runtime, later_result = _causal_character(grown_topology)
    direct_routes = [
        row
        for row in later_result.trace
        if row[1] == "n0" and row[2] == "n2" and row[3] == EventType.EXCURSION
    ]
    assert direct_routes
    source_emission = next(
        emission for emission in later_runtime._emissions if emission.source == "n0"
    )
    assert direct_routes[0][0] == pytest.approx(source_emission.timestamp + 0.4)
    assert direct_routes[0][9] == 1
    assert later_result.execution.processed_event_count > baseline_result.execution.processed_event_count
    assert later_result.max_route_depth >= baseline_result.max_route_depth
    assert dict(later_result.energy_components)["edge_transfer"] > dict(
        baseline_result.energy_components
    )["edge_transfer"]
    assert first_result.emission_count > 0
    assert first_runtime._active is False
    assert baseline_runtime._active is False
    assert later_runtime._active is False


def test_experiment_growth_uses_frozen_actual_emission_evidence() -> None:
    runner, example = _growth_runner()
    before = _signature(runner.topology)

    first = runner._run_excursion_example(example, 0, update=True)
    decision = first.structural_decision

    assert decision is not None
    assert decision.status == "grown"
    assert decision.growth_attempted
    assert decision.candidate_rank == 1
    assert decision.selected_candidate is not None
    assert decision.selected_candidate.source == "neuron-0"
    assert decision.selected_candidate.destination == "neuron-2"
    assert decision.selected_candidate.score == 1
    assert decision.selected_candidate.propagation_delay == 0.4
    assert any(item.emitter_id == "neuron-0" for item in decision.evidence.observations)
    assert any(item.emitter_id == "neuron-2" for item in decision.evidence.observations)
    assert decision.topology_before == before
    assert ("neuron-0", "neuron-2", 0.4) in decision.topology_after
    assert runner._active_runtime is None
    assert runner.topology is runner.plasticity.topology is runner._network.topology

    later = runner._run_excursion_example(example, 0, update=False)
    direct_routes = [
        row
        for row in later.trace
        if row[1] == "neuron-0"
        and row[2] == "neuron-2"
        and row[3] == EventType.EXCURSION
    ]
    source_time = next(
        row[0]
        for row in later.trace
        if row[1] == "neuron-0" and row[3] == "excursion_emission"
    )
    assert direct_routes
    assert direct_routes[0][0] == pytest.approx(source_time + 0.4)
    assert later.execution.processed_event_count > first.execution.processed_event_count
    assert dict(later.energy_components)["edge_transfer"] > dict(first.energy_components)[
        "edge_transfer"
    ]


def test_growth_does_not_change_already_completed_character() -> None:
    topology = _chain_topology()
    neighbors = {"n0": ("n2",), "n1": (), "n2": ()}
    plane = _plane(
        neighbors,
        nodes=("n0", "n1", "n2"),
        neighborhood_limit=1,
        reverse_observer_limit=1,
    )
    runtime, completed = _causal_character(topology, callback=plane.observe_emission)
    original_trace = completed.trace
    controller = StructuralPlasticityController(
        topology,
        candidate_capacity=3,
        local_neighbors=neighbors,
    )
    selected = controller.select(plane.freeze().candidates)
    assert selected is not None
    assert controller.grow(selected).status == "grown"

    assert completed.trace == original_trace
    assert runtime._active is False


def test_label_mutation_does_not_change_structural_decision() -> None:
    runner_a, example_a = _growth_runner()
    runner_b, _ = _growth_runner()
    relabeled = replace(example_a, label="Z")

    runner_a._run_excursion_example(example_a, 0, update=True)
    runner_b._run_excursion_example(relabeled, 0, update=True)

    assert runner_a.structural_decisions == runner_b.structural_decisions
    assert _signature(runner_a.topology) == _signature(runner_b.topology)


def test_future_suffix_does_not_change_prior_structural_decision() -> None:
    first, example = _growth_runner()
    second, _ = _growth_runner()
    first._run_excursion_example(example, 0, update=True)
    prior = first.structural_decisions[-1]
    suffix = replace(example, example_id="future", label="Z")
    second._execute((example, suffix), 0, update=True)
    suffix_prior = second.structural_decisions[0]

    assert prior == suffix_prior


def test_fixed_topology_control_remains_available() -> None:
    runner = ExperimentRunner(ExperimentConfig(topology_initial_edges=0))
    example = _example()
    result = runner.evaluate((example,))

    assert result.metrics.structural_growth_attempts == 0
    assert result.metrics.structural_decisions == ()
    assert result.metrics.pruned_connections == 0
    assert runner.topology is not None
    assert len(runner.topology) == 0


def test_structural_mode_is_explicit() -> None:
    with pytest.raises(ValueError, match="structural observation is enabled"):
        ExperimentConfig(structural_plasticity=True)
    with pytest.raises(ValueError, match="explicitly set"):
        ExperimentConfig(structural_observation=True)


@pytest.mark.parametrize("policy", ("fixed", "baseline", "random", "temporal", "reversed"))
def test_legacy_e2_unsupported_structural_policies_fail_explicitly(policy: str) -> None:
    with pytest.raises(ValueError, match="e2_local_temporal"):
        _runner_config(
            {"neuron-0": ("neuron-1",), "neuron-1": ()},
            growth=True,
            structural_policy=policy,
        )


def test_growth_respects_edge_capacity() -> None:
    neighbors = {
        "neuron-0": ("neuron-2",),
        "neuron-1": (),
        "neuron-2": (),
    }
    runner, _ = _runner(
        neighbors,
        topology_edge_capacity=1,
        topology_fan_in=2,
        topology_fan_out=2,
    )
    runner.topology.connect("neuron-1", "neuron-2", 0.2)
    before = _signature(runner.topology)
    decision, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-2")),
        successful_settling=True,
        update=True,
    )

    assert decision.status == "full_capacity"
    assert decision.reason == "edge_capacity"
    assert _signature(runner.topology) == before


def test_growth_respects_fan_in_limit() -> None:
    neighbors = {
        "neuron-0": ("neuron-2",),
        "neuron-1": ("neuron-2",),
        "neuron-2": (),
    }
    runner, _ = _runner(neighbors, topology_fan_in=1)
    runner.topology.connect("neuron-1", "neuron-2", 0.2)
    before = _signature(runner.topology)
    decision, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-2")),
        successful_settling=True,
        update=True,
    )

    assert decision.status == "full_capacity"
    assert decision.reason == "fan_in_full"
    assert _signature(runner.topology) == before


def test_growth_respects_fan_out_limit() -> None:
    neighbors = {
        "neuron-0": ("neuron-1", "neuron-2"),
        "neuron-1": (),
        "neuron-2": (),
    }
    runner, _ = _runner(neighbors, topology_fan_out=1)
    runner.topology.connect("neuron-0", "neuron-1", 0.2)
    before = _signature(runner.topology)
    decision, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-2")),
        successful_settling=True,
        update=True,
    )

    assert decision.status == "full_capacity"
    assert decision.reason == "fan_out_full"
    assert _signature(runner.topology) == before


def test_growth_is_atomic_on_rejection() -> None:
    neighbors = {
        "neuron-0": ("neuron-2",),
        "neuron-1": (),
        "neuron-2": (),
    }
    runner, _ = _runner(neighbors, topology_fan_in=1)
    runner.topology.connect("neuron-1", "neuron-2", 0.2)
    before = _signature(runner.topology)
    decision, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-2")),
        successful_settling=True,
        update=True,
    )

    assert decision.status == "full_capacity"
    assert decision.topology_before == decision.topology_after == before
    assert runner._mutation_history[-1][0] == "full_capacity"


def test_structural_repeat_is_deterministic() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    snapshot = _snapshot(_candidate("neuron-0", "neuron-1", score=2))
    first, _ = _runner(neighbors)
    second, _ = _runner(neighbors)
    first_decision, _ = first._attempt_e2_growth(
        snapshot,
        successful_settling=True,
        update=True,
    )
    second_decision, _ = second._attempt_e2_growth(
        snapshot,
        successful_settling=True,
        update=True,
    )

    assert first_decision == second_decision
    assert _signature(first.topology) == _signature(second.topology)


def test_capture_on_off_does_not_change_structural_decisions() -> None:
    uncaptured, example = _growth_runner()
    captured, _ = _growth_runner()
    workload = (example,)
    capture = CPUTrainingCapture(snapshot_every=1)

    uncaptured_result = uncaptured.train(workload)
    captured_result = captured.train(
        workload,
        observer=lambda epoch, neurons, metrics: capture.observe(
            epoch,
            neurons,
            metrics,
            captured.topology,
        ),
    )

    assert uncaptured.structural_decisions == captured.structural_decisions
    assert uncaptured_result.history == captured_result.history
    assert len(capture.snapshots) == 1
    assert capture.metrics[0] == asdict(captured_result.history[0])
    assert parse_snapshot(capture.snapshots[0]).format_version == EXCURSION_FORMAT_VERSION


def test_pruning_remains_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors)
    assert runner.plasticity is not None

    def forbidden(*_args, **_kwargs):
        raise AssertionError("pruning must remain disabled")

    monkeypatch.setattr(runner.plasticity, "prune", forbidden)
    monkeypatch.setattr(runner.plasticity, "prune_by_score", forbidden)
    runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=True,
        update=True,
    )


def test_no_n3_parameter_learning() -> None:
    neighbors = {"neuron-0": ("neuron-1",), "neuron-1": ()}
    runner, _ = _runner(neighbors)
    nodes = ("neuron-0", "neuron-1")
    topology = BoundedTopology.from_edges(
        nodes,
        (Edge("neuron-1", "neuron-0", 0.7, edge_weight=0.3, divider_strength=0.4, reference=0.2),),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=4,
        routing_capacity=4,
    )
    runner._topology = topology
    runner.plasticity.topology = topology
    runner._network.set_topology(topology)
    before = tuple(
        (edge.source, edge.destination, edge.edge_weight, edge.divider_strength, edge.reference)
        for edge in topology.edges
    )
    runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-1")),
        successful_settling=True,
        update=True,
    )
    after = tuple(
        (edge.source, edge.destination, edge.edge_weight, edge.divider_strength, edge.reference)
        for edge in runner.topology.edges
    )

    assert before == after[: len(before)]
    assert all(
        edge.edge_weight == 1.0 and edge.divider_strength == 1.0 and edge.reference == 0.0
        for edge in runner.topology.edges[len(before) :]
    )


def test_structural_observation_work_is_bounded() -> None:
    neighbors = {"s": ("d",), "d": ("s",), "x": ("d",)}
    plane = _plane(
        neighbors,
        nodes=("s", "d", "x"),
        history_capacity=2,
        candidate_capacity=1,
        neighborhood_limit=1,
        reverse_observer_limit=2,
    )
    for index in range(10):
        plane.observe_emission(("s", "d", "x")[index % 3], f"event-{index}", float(index))
    snapshot = plane.freeze()

    assert snapshot.observation_work <= snapshot.observation_count * (1 + plane.reverse_observer_limit)
    assert len(snapshot.observations) <= len(plane.nodes) * plane.history_capacity
    assert len(snapshot.candidates) <= len(plane.nodes) * plane.candidate_capacity


def test_convergent_fan_in_capacity_remains_available() -> None:
    neighbors = {
        "neuron-0": ("neuron-2",),
        "neuron-1": ("neuron-2",),
        "neuron-2": (),
    }
    runner, _ = _runner(
        neighbors,
        structural_growth_attempt_budget=2,
        topology_fan_in=2,
        topology_edge_capacity=2,
    )
    first, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-0", "neuron-2")),
        successful_settling=True,
        update=True,
    )
    second, _ = runner._attempt_e2_growth(
        _snapshot(_candidate("neuron-1", "neuron-2")),
        successful_settling=True,
        update=True,
    )

    assert first.status == second.status == "grown"
    assert len(runner.topology.incoming("neuron-2")) == 2
    assert len(runner.topology) == runner.topology.edge_capacity == 2


@pytest.mark.parametrize(
    ("nodes", "neighbors", "message"),
    (
        (("s", "d"), {"s": ("d",)}, "every topology node"),
        (("s", "d"), {"s": ("x",), "d": ()}, "topology nodes"),
        (("s", "d"), {"s": ("s",), "d": ()}, "non-self"),
        (("s", "d"), {"s": ("d", "d"), "d": ()}, "unique"),
        (
            ("s", "d", "x"),
            {"s": ("d", "x"), "d": (), "x": ()},
            "neighborhood limit",
        ),
    ),
)
def test_structural_neighborhood_is_explicit_and_bounded(
    nodes: tuple[str, ...],
    neighbors: dict[str, tuple[str, ...]],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        _plane(
            neighbors,
            nodes=nodes,
            neighborhood_limit=1 if message == "neighborhood limit" else 2,
        )


def test_reverse_observer_capacity_is_enforced() -> None:
    with pytest.raises(ValueError, match="reverse-observer limit"):
        _plane(
            {"s": ("d",), "x": ("d",), "d": ()},
            nodes=("s", "x", "d"),
            neighborhood_limit=1,
            reverse_observer_limit=1,
        )
