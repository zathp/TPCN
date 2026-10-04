import json

import pytest

from tpcn.cpu_visualization import (
    MAX_METRIC_BYTES,
    ReplaySequence,
    ReplaySequenceError,
    run_cpu_training,
)
from tpcn.visualization import (
    EXCURSION_FORMAT_VERSION,
    MAX_EXPORT_BYTES,
    NeuronRecord,
    VisualizationSnapshot,
    export_snapshot,
)


def test_capture_modes_do_not_change_training_result() -> None:
    disabled, disabled_capture = run_cpu_training(epochs=4, seed=7, examples_per_class=2, snapshot_every=0)
    every, every_capture = run_cpu_training(epochs=4, seed=7, examples_per_class=2, snapshot_every=1)
    frequent, frequent_capture = run_cpu_training(epochs=4, seed=7, examples_per_class=2, snapshot_every=2)

    assert disabled == every == frequent
    assert disabled_capture.snapshots == ()
    assert len(every_capture.snapshots) == 4
    assert len(frequent_capture.snapshots) == 2
    assert every_capture.metrics == frequent_capture.metrics
    assert all(record[4] == EXCURSION_FORMAT_VERSION for record in every_capture.snapshots)
    snapshot = ReplaySequence(every_capture.snapshots).snapshots[0]
    assert snapshot.format_version == EXCURSION_FORMAT_VERSION
    assert all(not hasattr(neuron, "activation") for neuron in snapshot.neurons)


def test_snapshot_sequence_is_deterministic_and_replays_offline(tmp_path) -> None:
    _, first_capture = run_cpu_training(epochs=3, seed=3, examples_per_class=1, snapshot_every=1)
    _, second_capture = run_cpu_training(epochs=3, seed=3, examples_per_class=1, snapshot_every=1)
    first = ReplaySequence(first_capture.snapshots, first_capture.metrics)
    second = ReplaySequence(second_capture.snapshots, second_capture.metrics)

    assert first.records == second.records
    assert first.digest == second.digest
    first.save(tmp_path)
    replayed = ReplaySequence.load(tmp_path)
    assert replayed.digest == first.digest
    assert replayed.inspect(0)["frame"]["neurons"]
    assert replayed.inspect(0)["metrics"]["epoch"] == replayed.snapshots[0].epoch


def test_replay_rejects_missing_malformed_and_over_limit_data(tmp_path) -> None:
    _, capture = run_cpu_training(epochs=2, seed=0, examples_per_class=1, snapshot_every=1)
    sequence = ReplaySequence(capture.snapshots, capture.metrics)
    sequence.save(tmp_path)
    (tmp_path / "snapshot-000001.tpcv").write_bytes(b"truncated")

    with pytest.raises(ReplaySequenceError, match="invalid TPCV record"):
        ReplaySequence.load(tmp_path)

    sequence.save(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    manifest["records"].append("snapshot-000003.tpcv")
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReplaySequenceError, match="bounded limit"):
        ReplaySequence.load(tmp_path, max_snapshots=2)

    sequence.save(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    manifest["records"] = ["missing.tpcv"]
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReplaySequenceError, match="missing"):
        ReplaySequence.load(tmp_path)


def test_replay_rejects_mixed_versions_and_oversized_files(tmp_path) -> None:
    _, capture = run_cpu_training(epochs=1, seed=0, examples_per_class=1, snapshot_every=1)
    legacy = export_snapshot(VisualizationSnapshot(
        0.0, 0, (NeuronRecord("legacy", False, 0.0, 0.0, 0),),
    ))
    with pytest.raises(ReplaySequenceError, match="cannot mix"):
        ReplaySequence((legacy, capture.snapshots[0]))

    sequence = ReplaySequence(capture.snapshots)
    sequence.save(tmp_path)
    (tmp_path / "snapshot-000001.tpcv").write_bytes(b"x" * (MAX_EXPORT_BYTES + 1))
    with pytest.raises(ReplaySequenceError, match="exceeds the bounded size"):
        ReplaySequence.load(tmp_path)

    sequence.save(tmp_path)
    (tmp_path / "manifest.json").write_bytes(b"x" * (MAX_METRIC_BYTES + 1))
    with pytest.raises(ReplaySequenceError, match="manifest exceeds the bounded limit"):
        ReplaySequence.load(tmp_path)