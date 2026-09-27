from tpcn.cpu_visualization import ReplaySequence, run_cpu_training
from tpcn.viewer_3d import VisualizationScene


def _scene() -> VisualizationScene:
    _, capture = run_cpu_training(epochs=4, seed=7, examples_per_class=1,
                                  snapshot_every=1, structural_plasticity=True)
    return VisualizationScene(ReplaySequence(capture.snapshots, capture.metrics), history_limit=2)


def test_layout_and_scene_generation_are_deterministic_and_diagnostic() -> None:
    first = _scene()
    second = _scene()
    assert first.coordinate_source == "diagnostic"
    assert first.positions == second.positions
    assert first.nodes() == second.nodes()
    assert first.replay.digest == second.replay.digest


def test_topology_deltas_and_bounded_prune_highlights() -> None:
    scene = _scene()
    observed_addition = False
    observed_prune = False
    for index in range(len(scene.replay.snapshots)):
        scene.seek(index)
        observed_addition |= bool(scene.diff.added_edges)
        observed_prune |= any(edge.kind == "pruned" for edge in scene.edges())
    assert observed_addition
    assert observed_prune
    scene.seek(len(scene.replay.snapshots) - 1)
    assert len(scene._history) <= 2


def test_playback_filters_selection_neighborhood_and_metrics() -> None:
    scene = _scene()
    scene.select("neuron-0")
    scene.set_mode("neighborhood")
    assert "neuron-0" in scene.neighborhood()
    assert scene.inspect()["fan_in"] >= 0
    assert scene.metrics["epoch"] == scene.snapshot.epoch
    scene.filters.active_only = True
    assert all(node.active for node in scene.nodes())
    scene.playing = True
    scene.playback_speed = 2.0
    scene.tick(0.6)
    assert scene.snapshot_index == 1
    scene.first()
    scene.orbit(10, 10)
    scene.pan(1, 2)
    scene.zoom(-2)
    scene.fit()
    assert scene.camera.distance > 0