from tpcn.cpu_visualization import ReplaySequence, run_cpu_training
from tpcn.experiments import ExperimentConfig, ExperimentRunner, make_synthetic_workload


def test_structural_run_is_deterministic_and_has_real_bounded_mutations() -> None:
    first, first_capture = run_cpu_training(
        epochs=4, seed=7, examples_per_class=1, snapshot_every=1, structural_plasticity=True
    )
    second, second_capture = run_cpu_training(
        epochs=4, seed=7, examples_per_class=1, snapshot_every=1, structural_plasticity=True
    )

    assert first == second
    assert first_capture.snapshots == second_capture.snapshots
    assert any(metric.accepted_additions for metric in first.history)
    assert any(metric.pruned_connections for metric in first.history)
    assert all(metric.connection_count <= metric.connection_capacity for metric in first.history)
    assert all(metric.fan_in_utilization <= 1.0 and metric.fan_out_utilization <= 1.0 for metric in first.history)
    assert all(len(metric.mutation_history) <= 32 for metric in first.history)


def test_capture_is_downstream_only_for_structural_decisions() -> None:
    disabled, disabled_capture = run_cpu_training(
        epochs=4, seed=3, examples_per_class=1, snapshot_every=0, structural_plasticity=True
    )
    enabled, enabled_capture = run_cpu_training(
        epochs=4, seed=3, examples_per_class=1, snapshot_every=1, structural_plasticity=True
    )

    assert disabled == enabled
    assert disabled_capture.snapshots == ()
    replay = ReplaySequence(enabled_capture.snapshots, enabled_capture.metrics)
    timeline = replay.connection_timeline()
    assert any(item["added_connections"] for item in timeline)
    assert any(item["recently_pruned_connections"] for item in timeline)


def test_controls_report_behavior_and_topology_without_assuming_benefit() -> None:
    workload = make_synthetic_workload(examples_per_class=1, seed=5)
    fixed = ExperimentRunner(ExperimentConfig(epochs=4, seed=5)).train(workload)
    structural = ExperimentRunner(ExperimentConfig(epochs=4, seed=5, structural_plasticity=True)).train(workload)
    control = ExperimentRunner(ExperimentConfig(epochs=4, seed=5, learning_enabled=False)).train(workload)

    assert fixed.history[-1].connection_count == fixed.history[0].connection_count
    assert any(metric.mutation_count for metric in structural.history)
    assert control.parameter_updates == 0
    for result in (fixed, structural, control):
        metrics = result.evaluation.metrics
        assert metrics.event_count == metrics.activation_count
        assert metrics.energy >= 0.0
        assert metrics.utility == metrics.reward - metrics.energy


def test_structural_evidence_is_label_isolated() -> None:
    workload = make_synthetic_workload(examples_per_class=1, seed=2)
    relabeled = tuple(type(example)(example.example_id, example.points, "Z" if example.label == "A" else "A")
                      for example in workload)
    config = ExperimentConfig(epochs=3, seed=2, structural_plasticity=True)
    first = ExperimentRunner(config).train(workload)
    second = ExperimentRunner(config).train(relabeled)

    assert tuple(metric.mutation_history for metric in first.history) == tuple(
        metric.mutation_history for metric in second.history
    )
