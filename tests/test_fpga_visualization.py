import pytest

from tpcn.visualization import ConnectionRecord, NeuronRecord, VisualizationSnapshot
from tpcn.fpga_visualization import (
    FLAG_RESET,
    DiagnosticStream,
    TraceDecodeError,
    decode_hex_trace,
    decode_snapshot_trace,
    encode_hex_trace,
    encode_snapshot_trace,
)


def _known_snapshot() -> VisualizationSnapshot:
    return VisualizationSnapshot(
        timestamp=7.0,
        epoch=4,
        neurons=(
            NeuronRecord("n-2", True, 0.25, 0.5, 2),
            NeuronRecord("n-1", False, -0.5, 0.0, 1),
        ),
        connections=(ConnectionRecord("n-1", "n-2", 1.0),),
    )


def test_known_topology_activity_round_trips_through_modelsim_hex() -> None:
    text = encode_hex_trace(encode_snapshot_trace(_known_snapshot(), sequence=9, reset=True))

    frame, decoded = decode_snapshot_trace(text)

    assert frame.sequence == 9
    assert frame.flags & FLAG_RESET
    assert decoded == _known_snapshot()
    assert decoded.connections == (ConnectionRecord("n-1", "n-2", 1.0),)
    assert decoded.neurons[1].active is True


def test_trace_words_are_deterministic_and_big_endian() -> None:
    words = encode_snapshot_trace(_known_snapshot(), sequence=1)
    assert encode_hex_trace(words) == encode_hex_trace(words)
    assert encode_hex_trace(words).splitlines()[0] == "54524331"


def test_unknown_hdl_values_are_explicitly_rejected() -> None:
    text = encode_hex_trace(encode_snapshot_trace(_known_snapshot(), sequence=2))
    unknown_text = text.replace(text.splitlines()[4], "0000000X", 1)

    with pytest.raises(TraceDecodeError, match="X/Z/unknown"):
        decode_hex_trace(unknown_text)


def test_truncated_trace_frame_is_rejected() -> None:
    text = encode_hex_trace(encode_snapshot_trace(_known_snapshot(), sequence=2))

    with pytest.raises(TraceDecodeError, match="framing length"):
        decode_hex_trace("\n".join(text.splitlines()[:-1]))


def test_reset_and_snapshot_boundaries_are_independent_of_core_state() -> None:
    reset_words = (0x54524331, (1 << 16) | FLAG_RESET, 3, 0, 0)
    frame = decode_hex_trace(encode_hex_trace(reset_words))
    assert frame.is_reset
    assert not frame.is_snapshot
    assert frame.payload == b""


def test_diagnostic_stream_drops_without_backpressure_and_reports_loss() -> None:
    stream = DiagnosticStream(capacity=1)
    frame = decode_hex_trace(encode_hex_trace(encode_snapshot_trace(_known_snapshot(), sequence=1)))

    assert stream.offer(frame)
    assert not stream.offer(frame)
    assert stream.dropped == 1
    assert stream.overflow
    assert stream.pop() == frame
    assert stream.pop() is None