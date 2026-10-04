from __future__ import annotations

import math

import pytest

from tpcn.cpu_visualization import CPUTrainingCapture, ReplaySequence, run_cpu_training
from tpcn.experiments import ExperimentConfig, ExperimentRunner, SyntheticExample, make_synthetic_workload
from tpcn.stroke_dataset import StrokePoint
from tpcn.topology import BoundedTopology, Edge
from tpcn.visualization import EXCURSION_FORMAT_VERSION, VisualizationSnapshot, export_snapshot

NODES = ("neuron-0", "neuron-1", "neuron-2")
NEIGHBORS = {"neuron-0": ("neuron-2",), "neuron-1": (), "neuron-2": ()}


def _e2_config(**overrides: object) -> ExperimentConfig:
    values: dict[str, object] = {
        "epochs": 1,
        "max_points": 4,
        "structural_observation": True,
        "structural_plasticity": True,
        "structural_policy": "e2_local_temporal",
        "structural_neighbors": NEIGHBORS,
        "structural_neighborhood_limit": 2,
        "structural_reverse_observer_limit": 2,
        "structural_association_window": 4.0,
        "structural_history_capacity": 8,
        "structural_candidate_capacity": 4,
        "structural_maximum_score": 3,
        "structural_growth_delay": 0.4,
        "structural_growth_attempt_budget": 4,
        "topology_node_count": 3,
        "topology_initial_edges": 0,
        "topology_fan_in": 2,
        "topology_fan_out": 2,
        "topology_edge_capacity": 4,
        "queue_capacity": 128,
        "event_budget": 1024,
        "settling_horizon": 8.0,
        "reward_mode": "neutral",
        "energy_weight": 1.0,
    }
    values.update(overrides)
    return ExperimentConfig(**values)


def _initial_topology() -> BoundedTopology:
    return BoundedTopology.from_edges(
        NODES,
        (
            Edge("neuron-0", "neuron-1", 0.2, divider_strength=0.0, reference=1.0),
            Edge("neuron-1", "neuron-2", 0.2, divider_strength=0.0, reference=1.0),
        ),
        fan_in_limit=2, fan_out_limit=2, edge_capacity=4, routing_capacity=4,
    )


def _example(label: str = "A") -> SyntheticExample:
    return SyntheticExample(
        "causal-character",
        tuple(StrokePoint(3.5, 3.5, timestamp=float(index)) for index in range(4)),
        label,
    )


def _runner(config: ExperimentConfig | None = None, example: SyntheticExample | None = None):
    # The explicit chain topology is installed exactly as in the Luna-28 growth fixture.
    example = example or _example()
    runner = ExperimentRunner(config or _e2_config())
    runner._ensure_topology((example,))
    topology = _initial_topology()
    runner._topology = topology
    runner.plasticity.topology = topology
    runner._network.set_topology(topology)
    return runner, example


def _signature(topology: BoundedTopology) -> tuple[tuple[str, str, float], ...]:
    return tuple((e.source, e.destination, float(e.propagation_delay)) for e in topology.edges)


def _train_captured(snapshot_every: int, label: str = "A"):
    runner, example = _runner(example=_example(label))
    capture = CPUTrainingCapture(snapshot_every=snapshot_every)
    result = runner.train(
        (example,),
        observer=lambda epoch, neurons, metrics: capture.observe(epoch, neurons, metrics, runner.topology),
    )
    return runner, result, capture


def test_helper_accepts_explicit_config_and_uses_its_seed_and_settings() -> None:
    config = _e2_config(epochs=2, seed=11, structural_plasticity=False, structural_policy="baseline")
    result, capture = run_cpu_training(config=config, examples_per_class=1, snapshot_every=1)
    expected = ExperimentRunner(config).train(make_synthetic_workload(examples_per_class=1, seed=11))

    assert result == expected
    assert len(result.history) == 2
    assert len(capture.snapshots) == 2
    # Equal scalar duplicates are not conflicts.
    same, _ = run_cpu_training(config=config, examples_per_class=1, epochs=2, seed=11, learning_enabled=True)
    assert same == result


@pytest.mark.parametrize(
    "scalar", [{"epochs": 5}, {"seed": 1}, {"structural_plasticity": True}, {"learning_enabled": False}]
)
def test_helper_rejects_conflicting_runner_values(scalar: dict[str, object]) -> None:
    config = _e2_config(structural_plasticity=False, structural_policy="baseline")
    with pytest.raises(ValueError, match="conflicts with the supplied ExperimentConfig"):
        run_cpu_training(config=config, examples_per_class=1, **scalar)
    with pytest.raises(TypeError, match="ExperimentConfig"):
        run_cpu_training(config={"epochs": 1})  # type: ignore[arg-type]


def test_default_route_is_fixed_and_legacy_boolean_requires_explicit_e2_configuration() -> None:
    result, capture = run_cpu_training(epochs=2, seed=3, examples_per_class=1, snapshot_every=1)
    explicit, _ = run_cpu_training(
        config=ExperimentConfig(epochs=2, seed=3), examples_per_class=1, snapshot_every=1
    )

    assert result == explicit
    assert all(m.mutation_count == 0 and m.pruned_connections == 0 for m in result.history)
    assert len({m.connection_count for m in result.history}) == 1
    assert len(capture.snapshots) == 2
    with pytest.raises(ValueError, match="structural observation"):
        run_cpu_training(epochs=2, seed=3, examples_per_class=1, structural_plasticity=True)


def test_structural_run_is_deterministic_and_has_real_bounded_mutations() -> None:
    first_runner, first, first_capture = _train_captured(1)
    second_runner, second, second_capture = _train_captured(1)

    assert first == second
    assert first_capture.snapshots == second_capture.snapshots
    assert first_runner.structural_decisions == second_runner.structural_decisions
    metric = first.history[-1]
    decision = first_runner.structural_decisions[0]
    assert decision.status == "grown"
    assert decision.growth_attempted
    assert decision.candidate_rank == 1
    assert (decision.selected_candidate.source, decision.selected_candidate.destination) == ("neuron-0", "neuron-2")
    assert ("neuron-0", "neuron-2", 0.4) in decision.topology_after
    assert ("neuron-0", "neuron-2", 0.4) not in decision.topology_before
    assert metric.structural_growth_attempts == 1
    assert metric.mutation_count == metric.accepted_additions == 1
    assert metric.rejected_mutations == 0
    assert metric.pruned_connections == 0
    assert metric.connection_count == 3 <= metric.connection_capacity == 4
    assert math.isfinite(metric.fan_in_utilization) and 0.0 < metric.fan_in_utilization <= 1.0
    assert math.isfinite(metric.fan_out_utilization) and 0.0 < metric.fan_out_utilization <= 1.0
    assert len(metric.mutation_history) <= 32
    assert metric.structural_growth_attempts <= metric.structural_growth_attempt_budget
    assert len(first_runner.topology.edges) == 3


def test_added_edge_is_visible_in_tpcv2_replay() -> None:
    runner, result, capture = _train_captured(1)
    neurons = runner.last_neurons
    before = VisualizationSnapshot.from_components(neurons, topology=_initial_topology(), timestamp=0.0, epoch=0)
    replay = ReplaySequence((export_snapshot(before), *capture.snapshots), capture.metrics)

    assert all(s.format_version == EXCURSION_FORMAT_VERSION for s in replay.snapshots)
    timeline = replay.connection_timeline()
    added = [item for item in timeline if item["added_connections"]]
    assert len(added) == 1
    assert added[0]["added_connections"] == (("neuron-0", "neuron-2"),)
    assert added[0]["unchanged_connections"] == (("neuron-0", "neuron-1"), ("neuron-1", "neuron-2"))
    assert not any(item["recently_pruned_connections"] for item in timeline)
    assert result.history[0].connection_count == len(replay.snapshots[-1].connections)


def test_capture_is_downstream_only_for_structural_decisions() -> None:
    off_runner, off, off_capture = _train_captured(0)
    on_runner, on, on_capture = _train_captured(1)

    assert off == on
    assert off_runner.structural_decisions == on_runner.structural_decisions
    assert _signature(off_runner.topology) == _signature(on_runner.topology)
    assert off_capture.snapshots == ()
    assert len(on_capture.snapshots) == 1


def test_controls_report_behavior_and_topology_without_assuming_benefit() -> None:
    fixed, _ = run_cpu_training(config=_e2_config(epochs=3, seed=5, structural_plasticity=False,
                                                  structural_policy="baseline"), examples_per_class=1)
    grown, _ = run_cpu_training(config=_e2_config(epochs=3, seed=5), examples_per_class=1)
    control, _ = run_cpu_training(config=_e2_config(epochs=3, seed=5, learning_enabled=False,
                                                    structural_plasticity=False, structural_policy="baseline"),
                                  examples_per_class=1)
    legacy_fixed = run_cpu_training(config=ExperimentConfig(epochs=3, seed=5), examples_per_class=1)[0]

    assert control.parameter_updates == 0
    for result in (fixed, grown, control, legacy_fixed):
        assert all(m.pruned_connections == 0 for m in result.history)
        assert all(m.mutation_count == m.accepted_additions + m.rejected_mutations for m in result.history)
        metrics = result.evaluation.metrics
        assert metrics.event_count == metrics.processed_event_count
        assert metrics.activation_count == metrics.excursion_count
        assert metrics.energy >= 0.0
    for result in (fixed, grown, control):
        metrics = result.evaluation.metrics
        assert metrics.utility == metrics.reward - metrics.energy
    assert len({m.connection_count for m in fixed.history}) == 1


def test_structural_evidence_is_label_isolated() -> None:
    first_runner, _, _ = _train_captured(1, "A")
    second_runner, _, _ = _train_captured(1, "Z")
    first, = first_runner.structural_decisions
    second, = second_runner.structural_decisions

    assert first.evidence.observations == second.evidence.observations
    assert first.evidence.candidates == second.evidence.candidates
    assert first.selected_candidate == second.selected_candidate
    assert (first.candidate_rank, first.status) == (second.candidate_rank, second.status)
    assert first.topology_before == second.topology_before
    assert first.topology_after == second.topology_after
    assert _signature(first_runner.topology) == _signature(second_runner.topology)
    assert first.evidence.observations and first.evidence.candidates


def test_e2_never_prunes_even_across_epochs() -> None:
    runner, example = _runner(_e2_config(epochs=3))
    result = runner.train((example,))

    assert all(m.pruned_connections == 0 for m in result.history)
    assert all(not d.topology_before or set(d.topology_before) <= set(d.topology_after)
               for d in runner.structural_decisions)


def test_explicit_tanh_legacy_retains_historical_growth_and_pruning() -> None:
    config = ExperimentConfig(epochs=4, seed=7, structural_plasticity=True, neuron_model="TANH_LEGACY")
    first, first_capture = run_cpu_training(config=config, examples_per_class=1, snapshot_every=1)
    second, second_capture = run_cpu_training(config=config, examples_per_class=1, snapshot_every=1)
    off, off_capture = run_cpu_training(config=config, examples_per_class=1, snapshot_every=0)

    assert first == second == off
    assert first_capture.snapshots == second_capture.snapshots
    assert off_capture.snapshots == ()
    assert any(m.accepted_additions for m in first.history)
    assert any(m.pruned_connections for m in first.history)
    assert all(m.connection_count <= m.connection_capacity for m in first.history)
    assert all(len(m.mutation_history) <= 32 for m in first.history)
    timeline = ReplaySequence(first_capture.snapshots, first_capture.metrics).connection_timeline()
    assert any(item["added_connections"] for item in timeline)
    assert any(item["recently_pruned_connections"] for item in timeline)
