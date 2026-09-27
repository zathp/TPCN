import pytest

from tpcn.cpu_visualization import ReplaySequence, ReplaySequenceError, run_cpu_training
from tpcn.temporal_analysis import analyze_replay, compare_replays, summarize_analysis
from tpcn.visualization import ConnectionRecord, NeuronRecord, VisualizationSnapshot, export_snapshot


def snapshot(epoch, active, edges=()):
    neurons = tuple(NeuronRecord(f"n{index}", index in active, float(index), float(index in active), index)
                    for index in range(3))
    return export_snapshot(VisualizationSnapshot(0.0, epoch, neurons,
        tuple(ConnectionRecord(source, destination, 1.0) for source, destination in edges)))


def test_node_and_edge_lifetimes_are_deterministic():
    replay = ReplaySequence((snapshot(1, {0}, (("n0", "n1"),)),
                             snapshot(2, {0, 1}, (("n0", "n1"), ("n1", "n2"))),
                             snapshot(3, set(), ())),
                            ({"epoch": 1, "accuracy": 0.5}, {"epoch": 2, "accuracy": 0.5}, {"epoch": 3, "accuracy": 0.5}))
    result = analyze_replay(replay)
    nodes = {item["neuron_id"]: item for item in result["node_statistics"]}
    edges = {(item["source"], item["destination"]): item for item in result["edge_statistics"]}
    assert nodes["n2"]["permanently_inactive"]
    assert nodes["n0"]["active_snapshot_count"] == 2
    assert edges[("n0", "n1")]["lifetime_snapshots"] == 2
    assert edges[("n0", "n1")]["persisted_to_final_snapshot"] is False
    assert result["edge_summary"]["total_removals"] == 2
    assert result["edge_summary"]["churn_rate"] == pytest.approx(3 / 2)


def test_flat_metrics_and_changing_topology_are_reported():
    _, capture = run_cpu_training(epochs=4, seed=7, examples_per_class=1,
                                  snapshot_every=1, structural_plasticity=True)
    result = analyze_replay(ReplaySequence(capture.snapshots, capture.metrics))
    assert result["flat_metrics"]["prediction_loss"]["flat"] is True
    assert result["topology_changes_with_flat_functional_metrics"]
    assert result["classification"] == "persistent churn / no functional response"
    assert "metric_deltas" in result["snapshot_metrics"][0]


def test_rejection_reason_aggregation_preserves_observed_reasons():
    _, capture = run_cpu_training(epochs=4, seed=7, examples_per_class=1,
                                  snapshot_every=1, structural_plasticity=True)
    reasons = analyze_replay(ReplaySequence(capture.snapshots, capture.metrics))["mutation_rejections"]
    assert reasons["duplicate"] >= 1
    assert reasons["accepted"] >= 1
    assert reasons["growth_attempts"] >= reasons["accepted"]


def test_edge_use_is_not_inferred_from_existence_and_summary_is_concise():
    result = analyze_replay(ReplaySequence((snapshot(1, {0}, (("n0", "n1"),)),),
                                            ({"epoch": 1, "accuracy": 1.0},)))
    assert result["edge_statistics"][0]["used_recently"] is None
    assert result["edge_summary"]["edge_use_evidence"] == "unavailable"
    assert "edge-use evidence: unavailable" in summarize_analysis(result)


def test_compare_runs_reports_raw_metric_deltas_without_claiming_causation():
    left, left_capture = run_cpu_training(epochs=2, seed=3, examples_per_class=1,
                                          snapshot_every=1, structural_plasticity=False)
    right, right_capture = run_cpu_training(epochs=2, seed=3, examples_per_class=1,
                                            snapshot_every=1, structural_plasticity=True)
    comparison = compare_replays(ReplaySequence(left_capture.snapshots, left_capture.metrics),
                                 ReplaySequence(right_capture.snapshots, right_capture.metrics))
    assert comparison["metrics"]["accuracy"]["left"] is not None
    assert "delta_right_minus_left" in comparison["metrics"]["energy"]
    assert comparison["left_digest"] != ""


def test_malformed_replay_is_rejected_before_analysis():
    with pytest.raises(ReplaySequenceError):
        ReplaySequence((b"not-tpcv",), ())
