import struct

import pytest

from tpcn import Event, EventQueue, TPCNNeuron
from tpcn.topology import BoundedTopology
from tpcn.visualization import (
    ConnectionRecord,
    MAX_RECORDS,
    NeuronRecord,
    ReferenceVisualizer,
    SnapshotCollector,
    VisualizationFormatError,
    VisualizationSnapshot,
    export_snapshot,
    parse_snapshot,
)


def _snapshot() -> VisualizationSnapshot:
    return VisualizationSnapshot(
        timestamp=4.0,
        epoch=3,
        neurons=(
            NeuronRecord("node-2", False, -0.25, -0.24, 2),
            NeuronRecord("node-1", True, 0.5, 0.46, 7, (8, -2)),
        ),
        connections=(ConnectionRecord("node-1", "node-2", 1.25),),
    )


def test_export_is_deterministic_and_parser_round_trips_sorted_records() -> None:
    first = export_snapshot(_snapshot())
    second = export_snapshot(_snapshot())

    assert first == second
    assert parse_snapshot(first) == _snapshot()
    assert parse_snapshot(first).neurons[0].neuron_id == "node-1"


def test_empty_snapshot_is_valid_and_framed() -> None:
    encoded = export_snapshot(VisualizationSnapshot(0.0, 0))

    assert len(encoded) == 32
    assert parse_snapshot(encoded) == VisualizationSnapshot(0.0, 0)


@pytest.mark.parametrize("bad", [b"", b"TPCV", b"not-a-snapshot"])
def test_malformed_snapshot_is_rejected(bad: bytes) -> None:
    with pytest.raises(VisualizationFormatError):
        parse_snapshot(bad)


def test_unsupported_version_and_trailing_data_are_rejected() -> None:
    encoded = bytearray(export_snapshot(_snapshot()))
    encoded[4] = 99
    with pytest.raises(VisualizationFormatError, match="unsupported snapshot version"):
        parse_snapshot(encoded)

    with pytest.raises(VisualizationFormatError, match="framing length"):
        parse_snapshot(export_snapshot(_snapshot()) + b"x")


def test_export_and_parser_have_bounded_record_behavior() -> None:
    records = tuple(NeuronRecord(f"n-{index}", False, 0.0, 0.0, 0) for index in range(MAX_RECORDS + 1))
    with pytest.raises(ValueError, match="at most"):
        VisualizationSnapshot(0.0, 0, records)

    with pytest.raises(OverflowError):
        export_snapshot(_snapshot(), max_bytes=31)


def test_incomplete_capture_is_explicit() -> None:
    snapshot = VisualizationSnapshot(2.0, 5, incomplete=True)

    assert parse_snapshot(export_snapshot(snapshot)).incomplete is True


def test_reference_visualizer_enumerates_structure_and_changes() -> None:
    first = _snapshot()
    second = VisualizationSnapshot(
        5.0, 4,
        (NeuronRecord("node-1", True, 0.75, 0.63, 8, (8, -2)),),
        (ConnectionRecord("node-1", "node-3", 2.0),),
    )
    visualizer = ReferenceVisualizer.load((export_snapshot(first), export_snapshot(second)))

    assert visualizer.frames()[0]["connections"] == (("node-1", "node-2", 1.25),)
    assert visualizer.changes() == ({
        "from_epoch": 3,
        "to_epoch": 4,
        "changed_neurons": ("node-1",),
        "added_neurons": (),
        "removed_neurons": ("node-2",),
        "added_connections": (("node-1", "node-3"),),
        "removed_connections": (("node-1", "node-2"),),
    },)


def _run(capture: str) -> tuple[tuple[object, ...], tuple[bytes, ...]]:
    first = TPCNNeuron("n-1", input_gain=0.5)
    second = TPCNNeuron("n-2", input_gain=0.25)
    topology = BoundedTopology.from_edges(("n-1", "n-2"), (("n-1", "n-2", 1.0),), fan_in_limit=1, fan_out_limit=1)
    queue: EventQueue[Event] = EventQueue(capacity=8)
    collector = SnapshotCollector(enabled=capture != "disabled", capacity=8)
    snapshots: list[bytes] = []
    for index, value in enumerate((1.0, -0.5, 0.25)):
        event = Event(float(index), "input", "n-1", "signal", value)
        queue.push(event)
        first.receive_event(queue.pop_ready(float(index)))
        topology.route(Event(float(index), "n-1", "ignored", "signal", value), queue)
        second.receive_event(queue.pop_ready(float(index + 1)))
        should_capture = capture == "every" or (capture == "intermittent" and index == 1)
        if should_capture:
            snapshots.append(collector.capture(VisualizationSnapshot.from_components(
                (first, second), topology=topology, timestamp=float(index), epoch=index
            )))
    state = tuple((neuron.state, neuron.activation, neuron.processed_events, neuron.clock.timestamp)
                  for neuron in (first, second)) + (tuple(queue.drain()), tuple(topology.edges))
    return state, tuple(snapshots)


def test_capture_mode_cannot_change_functional_workload_state() -> None:
    disabled, disabled_records = _run("disabled")
    every, every_records = _run("every")
    intermittent, intermittent_records = _run("intermittent")

    assert disabled == every == intermittent
    assert disabled_records == ()
    assert len(every_records) == 3
    assert len(intermittent_records) == 1
    assert parse_snapshot(every_records[1]).epoch == 1


def test_disabled_collector_does_not_store_or_consume_snapshots() -> None:
    collector = SnapshotCollector(enabled=False)

    assert collector.capture(_snapshot()) is None
    assert collector.snapshots == ()


def test_maximum_identifier_and_numeric_values_are_supported() -> None:
    identifier = "x" * 255
    snapshot = VisualizationSnapshot(
        1.0, 0xFFFFFFFF,
        (NeuronRecord(identifier, True, 1.0, -1.0, 0xFFFFFFFF, (-0x80000000, 0x7FFFFFFF)),),
    )

    assert parse_snapshot(export_snapshot(snapshot)) == snapshot


def test_header_body_length_corruption_is_rejected() -> None:
    encoded = bytearray(export_snapshot(_snapshot()))
    encoded[28:32] = struct.pack(">I", 0)

    with pytest.raises(VisualizationFormatError, match="framing length"):
        parse_snapshot(encoded)