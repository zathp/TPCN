from __future__ import annotations

import pytest

from tpcn.cpu_visualization import ReplaySequence
from tpcn.excursion_neuron import E1Mode
from tpcn.viewer_3d import VisualizationScene
from tpcn.visualization import (
    EXCURSION_FORMAT_VERSION,
    ConnectionRecord,
    ExcursionNeuronRecord,
    NeuronRecord,
    VisualizationSnapshot,
    export_snapshot,
)


def _tpcv1_replay() -> ReplaySequence:
    baseline = VisualizationSnapshot(
        0.0,
        0,
        (
            NeuronRecord("n0", True, 0.5, 0.8, 5),
            NeuronRecord("n1", False, -0.25, 0.0, 2),
        ),
        (ConnectionRecord("n0", "n1", 0.7),),
        format_version=1,
    )
    advanced = VisualizationSnapshot(
        1.0,
        1,
        (
            NeuronRecord("n0", True, 0.7, 0.9, 7),
            NeuronRecord("n1", True, 0.1, 0.4, 4),
        ),
        (ConnectionRecord("n0", "n1", 0.7),),
        format_version=1,
    )
    metrics = ({"epoch": 0, "accuracy": 0.50, "energy": 1.0}, {"epoch": 1, "accuracy": 0.75, "energy": 0.8})
    return ReplaySequence((export_snapshot(baseline), export_snapshot(advanced)), metrics)


def _tpcv2_replay() -> ReplaySequence:
    baseline = VisualizationSnapshot(
        0.0,
        0,
        (
            ExcursionNeuronRecord("n0", True, E1Mode.M_ACTIVE, 0.25, False, 4),
            ExcursionNeuronRecord("n1", False, E1Mode.N, -0.25, False, 2),
            ExcursionNeuronRecord("n2", True, E1Mode.S_PENDING, 0.85, True, 9),
        ),
        (ConnectionRecord("n0", "n1", 1.0),),
        format_version=EXCURSION_FORMAT_VERSION,
    )
    added = VisualizationSnapshot(
        1.0,
        1,
        (
            ExcursionNeuronRecord("n0", True, E1Mode.M_ACTIVE, 0.30, False, 5),
            ExcursionNeuronRecord("n1", False, E1Mode.N, -0.15, False, 3),
            ExcursionNeuronRecord("n2", True, E1Mode.S_PENDING, 0.90, True, 10),
        ),
        (ConnectionRecord("n0", "n1", 1.0), ConnectionRecord("n1", "n2", 1.5)),
        format_version=EXCURSION_FORMAT_VERSION,
    )
    # Synthetic detached replay evidence: the edge disappears in the final snapshot,
    # but this display-only removal is not proof of an E2 pruning event.
    removed = VisualizationSnapshot(
        2.0,
        2,
        (
            ExcursionNeuronRecord("n0", True, E1Mode.M_ACTIVE, 0.40, False, 6),
            ExcursionNeuronRecord("n1", False, E1Mode.N, -0.10, False, 4),
            ExcursionNeuronRecord("n2", True, E1Mode.S_PENDING, 0.95, True, 11),
        ),
        (ConnectionRecord("n1", "n2", 1.5),),
        format_version=EXCURSION_FORMAT_VERSION,
    )
    metrics = (
        {"epoch": 0, "accuracy": 0.50, "energy": 1.0},
        {"epoch": 1, "accuracy": 0.60, "energy": 0.9},
        {"epoch": 2, "accuracy": 0.70, "energy": 0.8},
    )
    return ReplaySequence((export_snapshot(baseline), export_snapshot(added), export_snapshot(removed)), metrics)


def test_tpcv2_scene_nodes_do_not_require_scalar_activation() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    nodes = scene.nodes()
    assert len(nodes) == 3
    assert all(node.activation is None for node in nodes)
    assert all(node.state == pytest.approx(record.state) for node, record in zip(nodes, scene.snapshot.neurons))


def test_tpcv2_nodeview_activation_is_absent_or_none() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    node = next(node for node in scene.nodes() if node.neuron_id == "n0")
    assert node.activation is None
    assert node.active is True


def test_tpcv2_inspect_activation_is_absent_or_none() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    inspection = scene.inspect("n0")
    assert inspection is not None
    assert inspection["activation"] is None
    assert inspection["state"] == pytest.approx(0.25)
    assert inspection["active"] is True
    assert inspection["processed_events"] == 4


def test_tpcv1_viewer_preserves_scalar_activation() -> None:
    scene = VisualizationScene(_tpcv1_replay())
    node = next(node for node in scene.nodes() if node.neuron_id == "n0")
    assert node.activation == pytest.approx(0.8)
    assert scene.inspect("n0")["activation"] == pytest.approx(0.8)
    scene.seek(1)
    assert scene.inspect("n1")["activation"] == pytest.approx(0.4)


def test_tpcv2_active_filter_uses_active_field() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    scene.filters.active_only = True
    active = scene.nodes()
    assert all(node.active for node in active)
    assert {node.neuron_id for node in active} == {"n0", "n2"}


def test_tpcv2_layout_is_deterministic() -> None:
    first = VisualizationScene(_tpcv2_replay())
    second = VisualizationScene(_tpcv2_replay())
    assert first.coordinate_source == "diagnostic"
    assert first.positions == second.positions
    assert first.nodes() == second.nodes()
    assert first.replay.digest == second.replay.digest


def test_tpcv2_selection_and_neighborhood_work() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    scene.select("n1")
    scene.set_mode("neighborhood")
    neighborhood = scene.neighborhood()
    assert "n1" in neighborhood
    assert "n0" in neighborhood or "n2" in neighborhood
    assert scene.inspect("n1")["fan_in"] >= 0
    assert scene.inspect("n1")["fan_out"] >= 0


def test_tpcv2_metrics_remain_synchronized() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    assert scene.metrics["epoch"] == scene.snapshot.epoch
    scene.seek(1)
    assert scene.metrics["epoch"] == scene.snapshot.epoch
    scene.playing = True
    scene.playback_speed = 2.0
    scene.tick(0.6)
    assert scene.snapshot_index == 2


def test_tpcv2_topology_addition_is_displayed() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    scene.seek(1)
    assert any(edge.kind == "added" for edge in scene.edges())
    assert ("n1", "n2") in scene.diff.added_edges


def test_generic_replay_removal_is_highlighted() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    scene.seek(2)
    assert scene.diff.removed_edges
    assert any(edge.kind == "pruned" for edge in scene.edges())


def test_generic_removal_does_not_claim_e2_pruning() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    scene.seek(2)
    summary = scene.summary()
    assert summary["removed"] >= 1
    assert "e2" not in summary["analysis_classification"].lower()
    assert "prune" not in summary["analysis_classification"].lower()


def test_tpcv2_adversarial_active_record_keeps_activation_none() -> None:
    snapshot = VisualizationSnapshot(
        3.0,
        3,
        (
            ExcursionNeuronRecord("n0", True, E1Mode.S_PENDING, 1.25, True, 12),
            ExcursionNeuronRecord("n1", True, E1Mode.M_ACTIVE, -0.75, False, 8),
        ),
        (ConnectionRecord("n0", "n1", 0.5),),
        format_version=EXCURSION_FORMAT_VERSION,
    )
    scene = VisualizationScene(ReplaySequence((export_snapshot(snapshot),), ({"epoch": 3, "accuracy": 0.9, "energy": 0.7},)))
    node = scene.nodes()[0]
    inspection = scene.inspect("n0")
    assert node.activation is None
    assert inspection["activation"] is None
    assert node.active is True
    assert inspection["active"] is True


def test_tpcv2_layout_is_deterministic_and_scene_controls_work() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    scene.select("n0")
    scene.orbit(10.0, 5.0)
    scene.pan(1.0, 2.0)
    scene.zoom(-1.0)
    scene.fit()
    assert scene.camera.distance > 0.0
    assert scene.snapshot_index == 0
