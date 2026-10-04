import hashlib
import struct

import pytest

from tpcn import Event, EventQueue, MultiExcursionNeuron, TPCNNeuron
from tpcn.excursion_neuron import E1Mode
from tpcn.topology import BoundedTopology
from tpcn.visualization import (
    ConnectionRecord,
    EXCURSION_FORMAT_VERSION,
    ExcursionNeuronRecord,
    MAX_EXPORT_BYTES,
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


def test_tpcv1_bytes_match_the_pre_migration_golden_fixture() -> None:
    encoded = export_snapshot(_snapshot())

    assert len(encoded) == 120
    assert hashlib.sha256(encoded).hexdigest() == (
        "0ad558e8e229f1a4598513987b44715a051f43f399540c82e2515137af9b6eb8"
    )
    assert encoded[4] == 1
    assert parse_snapshot(encoded).format_version == 1


def _excursion_snapshot() -> VisualizationSnapshot:
    modes = (
        (E1Mode.N, False, False),
        (E1Mode.S_PENDING, True, True),
        (E1Mode.S_RETURN, True, False),
        (E1Mode.M_ACTIVE, True, False),
    )
    records = tuple(
        ExcursionNeuronRecord(
            f"mode-{index}",
            active,
            mode,
            float(index) / 4,
            pending,
            index + 2,
            (index, -index) if index == 1 else None,
        )
        for index, (mode, active, pending) in enumerate(modes)
    )
    return VisualizationSnapshot(
        2.5, 9, records,
        (ConnectionRecord("mode-0", "mode-1", 0.125),),
        format_version=EXCURSION_FORMAT_VERSION,
    )


def test_tpcv2_round_trip_preserves_excursion_identity_and_observations() -> None:
    snapshot = _excursion_snapshot()
    first = export_snapshot(snapshot)
    second = export_snapshot(snapshot)
    decoded = parse_snapshot(first)

    assert first == second
    assert first[4] == EXCURSION_FORMAT_VERSION
    assert decoded == snapshot
    assert decoded.format_version == EXCURSION_FORMAT_VERSION
    assert [(item.mode, item.active, item.state, item.pending_internal_work, item.processed_events)
            for item in decoded.neurons] == [
        (E1Mode.N, False, 0.0, False, 2),
        (E1Mode.S_PENDING, True, 0.25, True, 3),
        (E1Mode.S_RETURN, True, 0.5, False, 4),
        (E1Mode.M_ACTIVE, True, 0.75, False, 5),
    ]
    assert all(not hasattr(item, "activation") for item in decoded.neurons)
    frame = ReferenceVisualizer((decoded,)).frames()[0]
    assert frame["format_version"] == EXCURSION_FORMAT_VERSION
    assert frame["neurons"][1][3] is None
    assert frame["neurons"][1][4:] == ("S_PENDING", True, 3)


def test_public_excursion_capture_observes_reachable_modes_without_activation() -> None:
    neutral = MultiExcursionNeuron("neutral")
    pending = MultiExcursionNeuron("pending")
    returning = MultiExcursionNeuron("returning")
    active = MultiExcursionNeuron("active")
    pending_queue: EventQueue[Event] = EventQueue(capacity=4)
    return_queue: EventQueue[Event] = EventQueue(capacity=4)
    active_queue: EventQueue[Event] = EventQueue(capacity=4)

    pending.receive_contribution(0.0, 1.0, queue=pending_queue)
    returning.receive_contribution(0.0, 1.0, queue=return_queue)
    returning.process_pending(queue=return_queue)
    active.receive_contribution(0.0, 4.0, queue=active_queue)

    snapshot = VisualizationSnapshot.from_components(
        (neutral, pending, returning, active), epoch=1,
    )

    assert snapshot.format_version == EXCURSION_FORMAT_VERSION
    assert {
        item.neuron_id: (item.mode, item.active, item.pending_internal_work, item.processed_events)
        for item in snapshot.neurons
    } == {
        "neutral": (E1Mode.N, False, False, 0),
        "pending": (E1Mode.S_PENDING, True, True, 1),
        "returning": (E1Mode.S_RETURN, True, True, 2),
        "active": (E1Mode.M_ACTIVE, True, True, 1),
    }


@pytest.mark.parametrize(
    ("offset", "value", "message"),
    [
        (4, 99, "unsupported snapshot version"),
        (34, 0x80, "reserved neuron bits"),
        (35, 4, "invalid excursion mode"),
        (34, 1, "active must equal"),
    ],
)
def test_tpcv2_rejects_invalid_version_mode_and_flags(
    offset: int, value: int, message: str,
) -> None:
    snapshot = VisualizationSnapshot(
        1.0, 0, (ExcursionNeuronRecord("n", False, E1Mode.N, 0.0, False, 0),),
        format_version=EXCURSION_FORMAT_VERSION,
    )
    encoded = bytearray(export_snapshot(snapshot))
    encoded[offset] = value

    with pytest.raises(VisualizationFormatError, match=message):
        parse_snapshot(encoded)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda data: data[:-1],
        lambda data: data + b"x",
        lambda data: data[:33] + b"\xff" + data[34:],
        lambda data: data[:36] + struct.pack(">d", float("inf")) + data[44:],
    ],
)
def test_tpcv2_rejects_truncated_trailing_utf8_and_nonfinite_data(mutate) -> None:
    snapshot = VisualizationSnapshot(
        1.0, 0, (ExcursionNeuronRecord("n", False, E1Mode.N, 0.0, False, 0),),
        format_version=EXCURSION_FORMAT_VERSION,
    )

    with pytest.raises(VisualizationFormatError):
        parse_snapshot(mutate(export_snapshot(snapshot)))


def test_visualizer_rejects_mixed_tpcv_versions() -> None:
    with pytest.raises(ValueError, match="cannot mix"):
        ReferenceVisualizer((_snapshot(), _excursion_snapshot()))


def test_empty_snapshot_is_valid_and_framed() -> None:
    encoded = export_snapshot(VisualizationSnapshot(0.0, 0))

    assert len(encoded) == 32
    assert parse_snapshot(encoded) == VisualizationSnapshot(0.0, 0)


def test_empty_tpcv2_snapshot_retains_version_identity() -> None:
    snapshot = VisualizationSnapshot(
        0.0, 0, format_version=EXCURSION_FORMAT_VERSION,
    )

    assert parse_snapshot(export_snapshot(snapshot)) == snapshot
    assert parse_snapshot(export_snapshot(snapshot)).format_version == EXCURSION_FORMAT_VERSION


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

    oversized_view = memoryview(b"x" * (MAX_EXPORT_BYTES + 1)).cast(
        "B", shape=[1, MAX_EXPORT_BYTES + 1],
    )
    with pytest.raises(VisualizationFormatError, match="bounded parser size"):
        parse_snapshot(oversized_view)


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