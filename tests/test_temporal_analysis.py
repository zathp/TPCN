import pytest

from tpcn.cpu_visualization import ReplaySequence, ReplaySequenceError
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


def test_temporal_analysis_classifies_explicit_supplied_metric_trend() -> None:
    replay = ReplaySequence(
        (
            snapshot(1, {0}, (("n0", "n1"),)),
            snapshot(2, {0, 1}, (("n0", "n1"), ("n1", "n2"))),
            snapshot(3, {0, 1}, (("n0", "n1"), ("n1", "n2"))),
        ),
        ({"epoch": 1, "accuracy": 0.4}, {"epoch": 2, "accuracy": 0.6}, {"epoch": 3, "accuracy": 0.7}),
    )
    analysis = analyze_replay(replay)
    assert analysis["classification"] == "changing topology / improving behavior"
    assert analysis["snapshot_metrics"][0]["metric_deltas"] == {}


def test_temporal_analysis_aggregates_explicit_rejection_reasons() -> None:
    replay = ReplaySequence(
        (snapshot(1, {0}, (("n0", "n1"),)),),
        ({"epoch": 1, "accuracy": 0.8, "mutation_rejection_reasons": {"duplicate": 2, "fan_in_full": 1, "accepted": 1}},),
    )
    analysis = analyze_replay(replay)
    assert analysis["mutation_rejections"]["duplicate"] == 2
    assert analysis["mutation_rejections"]["fan_in_full"] == 1
    assert analysis["mutation_rejections"]["accepted"] == 1


def test_compare_replays_reports_raw_deltas_without_causal_claim() -> None:
    left = ReplaySequence((snapshot(1, {0}, (("n0", "n1"),)),), ({"epoch": 1, "accuracy": 0.5, "energy": 1.0},))
    right = ReplaySequence((snapshot(1, {0, 1}, (("n0", "n1"), ("n1", "n2"))),), ({"epoch": 1, "accuracy": 0.7, "energy": 0.8},))
    comparison = compare_replays(left, right)
    assert comparison["metrics"]["accuracy"]["left"] == pytest.approx(0.5)
    assert comparison["metrics"]["accuracy"]["right"] == pytest.approx(0.7)
    assert comparison["metrics"]["accuracy"]["delta_right_minus_left"] == pytest.approx(0.2)
    assert comparison["left_digest"] != comparison["right_digest"]


def test_edge_usage_remains_unavailable_without_event_path_evidence() -> None:
    result = analyze_replay(ReplaySequence((snapshot(1, {0}, (("n0", "n1"),)),), ({"epoch": 1, "accuracy": 1.0},)))
    assert result["edge_statistics"][0]["used_recently"] is None
    assert result["edge_summary"]["edge_use_evidence"] == "unavailable"
    assert "edge-use evidence: unavailable" in summarize_analysis(result)


def test_malformed_replay_is_rejected_before_analysis():
    with pytest.raises(ReplaySequenceError):
        ReplaySequence((b"not-tpcv",), ())
