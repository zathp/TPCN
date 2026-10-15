from __future__ import annotations

import hashlib

import pytest

from tpcn.cpu_visualization import ReplaySequence, ReplaySequenceError
from tpcn.viewer_3d import VisualizationScene
from viz_tpcn_3d import _pick, _project, _slider_index, _transport_button, load_single_replay

from test_viewer_3d import _tpcv2_replay


def test_selected_manifest_load_is_single_read_only_and_identified(tmp_path) -> None:
    replay = _tpcv2_replay()
    run = tmp_path / "one-replay"
    replay.save(run)
    (run / "unlisted-snapshot.tpcv").write_bytes(b"must not be discovered")
    manifest = run / "manifest.json"
    original_manifest = manifest.read_bytes()

    sequence, identity = load_single_replay(manifest)

    assert len(sequence.snapshots) == 3
    assert identity["source_artifact_id"] == "one-replay"
    assert identity["snapshot_count"] == "3"
    assert identity["manifest_sha256"] == hashlib.sha256(original_manifest).hexdigest()
    assert manifest.read_bytes() == original_manifest
    assert sequence.digest == replay.digest


def test_single_manifest_loader_rejects_other_files_missing_records_and_malformed_json(tmp_path) -> None:
    with pytest.raises(ReplaySequenceError, match="manifest.json"):
        load_single_replay(tmp_path / "analysis.json")

    missing = tmp_path / "missing-run"
    missing.mkdir()
    with pytest.raises(ReplaySequenceError, match="manifest is missing"):
        load_single_replay(missing)

    run = tmp_path / "broken-run"
    run.mkdir()
    (run / "manifest.json").write_text("{not-json", encoding="utf-8")
    with pytest.raises(ReplaySequenceError, match="malformed"):
        load_single_replay(run / "manifest.json")

    replay = _tpcv2_replay()
    replay.save(run)
    (run / "snapshot-000002.tpcv").unlink()
    with pytest.raises(ReplaySequenceError, match="missing"):
        load_single_replay(run)


def test_headless_pick_uses_diagnostic_scene_positions_only() -> None:
    scene = VisualizationScene(_tpcv2_replay())
    scene.fit()
    node = next(iter(scene.nodes()))
    projected = _project(scene, node.position, 1280, 800)
    assert projected is not None
    picked = _pick(scene, (round(projected[0]), round(projected[1])), 1280, 800)
    assert picked == ("neuron", node.neuron_id)


def test_timeline_slider_maps_bounds_and_intermediate_snapshots_deterministically() -> None:
    assert _slider_index(0, 1280, 20) == 0
    assert _slider_index(350, 1280, 20) == 0
    assert _slider_index(1280 - 18, 1280, 20) == 19
    assert _slider_index(815, 1280, 20) in (9, 10)
    assert _slider_index(350, 1280, 1) == 0


@pytest.mark.parametrize("height", [480, 900])
def test_transport_buttons_match_drawn_rectangles_in_screen_coordinates(height: int) -> None:
    for index, x in enumerate((40, 100, 175, 250, 310)):
        assert _transport_button(x, height - 55, height) == index
        assert _transport_button(x, height - 42, height) == index
        assert _transport_button(x, height - 72, height) == index
        assert _transport_button(x, height - 30, height) is None
    assert _transport_button(5, height - 55, height) is None
    assert _transport_button(72, height - 55, height) is None


def test_recent_removed_edge_remains_inspectable_beyond_removal_snapshot() -> None:
    replay = _tpcv2_replay()
    extended = ReplaySequence(replay.records + (replay.records[-1],), replay.metrics)
    scene = VisualizationScene(extended)
    scene.seek(3)
    scene.select_edge(("n0", "n1"))
    assert "removed in snapshot diff" in scene.inspect_edge()["status"]
    assert scene.inspect_edge()["propagation_delay"] == 1.0
