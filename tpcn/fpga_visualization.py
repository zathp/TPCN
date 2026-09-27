"""ModelSim and FPGA diagnostic adapters for the canonical TPCV payload.

The adapter is downstream-only: it frames bytes exported by
``tpcn.visualization`` and never receives or emits TPCN events.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import struct
import zlib
from typing import Iterable

from .visualization import VisualizationSnapshot, export_snapshot, parse_snapshot


TRACE_MAGIC = 0x54524331  # ASCII "TRC1"
TRACE_VERSION = 1
WORD_BYTES = 4
FLAG_RESET = 0x0001
FLAG_SNAPSHOT_START = 0x0002
FLAG_SNAPSHOT_END = 0x0004
FLAG_INCOMPLETE = 0x0008
FLAG_UNKNOWN = 0x0010
_HEX_WORD = re.compile(r"^[0-9a-fA-FxXzZ]{8}$")


class TraceDecodeError(ValueError):
    """Raised when a ModelSim trace is malformed or contains unknown data."""


@dataclass(frozen=True, slots=True)
class TraceFrame:
    """One framed diagnostic record, with a lossless TPCV byte payload."""

    sequence: int
    flags: int
    payload: bytes
    unknown_words: int = 0

    @property
    def is_reset(self) -> bool:
        return bool(self.flags & FLAG_RESET)

    @property
    def is_snapshot(self) -> bool:
        return bool(self.flags & (FLAG_SNAPSHOT_START | FLAG_SNAPSHOT_END))


def _uint(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xFFFFFFFF:
        raise ValueError(f"{name} must be an unsigned 32-bit integer")
    return value


def encode_trace_frame(payload: bytes = b"", *, sequence: int = 0, flags: int = 0) -> tuple[int, ...]:
    """Encode a frame as big-endian 32-bit words.

    Word 0 is ``TRC1``. Word 1 packs version in bits 31..16 and flags in
    bits 15..0. Words 2 and 3 are sequence and payload byte length. The
    payload is padded with zero bytes to a word boundary and followed by a
    CRC-32 over the unpadded payload. No byte order depends on host endian.
    """
    if not isinstance(payload, bytes):
        raise TypeError("payload must be bytes")
    _uint(sequence, "sequence")
    if isinstance(flags, bool) or not isinstance(flags, int) or not 0 <= flags <= 0xFFFF:
        raise ValueError("flags must be an unsigned 16-bit integer")
    if len(payload) > 0xFFFFFFFF:
        raise OverflowError("trace payload is too large")
    padded = payload + b"\0" * (-len(payload) % WORD_BYTES)
    words = [TRACE_MAGIC, (TRACE_VERSION << 16) | flags, sequence, len(payload)]
    words.extend(struct.unpack(f">{len(padded) // WORD_BYTES}I", padded) if padded else ())
    words.append(zlib.crc32(payload) & 0xFFFFFFFF)
    return tuple(words)


def encode_snapshot_trace(
    snapshot: VisualizationSnapshot,
    *,
    sequence: int,
    reset: bool = False,
) -> tuple[int, ...]:
    """Frame one canonical snapshot with explicit snapshot/reset boundaries."""
    flags = FLAG_SNAPSHOT_START | FLAG_SNAPSHOT_END
    if snapshot.incomplete:
        flags |= FLAG_INCOMPLETE
    if reset:
        flags |= FLAG_RESET
    return encode_trace_frame(export_snapshot(snapshot), sequence=sequence, flags=flags)


def encode_hex_trace(words: Iterable[int]) -> str:
    """Render one word per line, matching ModelSim ``%08h`` output."""
    checked = tuple(_uint(word, "word") for word in words)
    return "".join(f"{word:08X}\n" for word in checked)


def _parse_hex_words(text: str) -> tuple[tuple[int, ...], int]:
    words: list[int] = []
    unknown_words = 0
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        token = raw_line.strip()
        if not token or token.startswith("#"):
            continue
        if not _HEX_WORD.fullmatch(token):
            raise TraceDecodeError(f"invalid 32-bit hex word at line {line_number}")
        if any(character in token.lower() for character in "xz"):
            unknown_words += 1
            words.append(0)
        else:
            words.append(int(token, 16))
    return tuple(words), unknown_words


def decode_hex_trace(text: str, *, allow_unknown: bool = False) -> TraceFrame:
    """Decode one deterministic word stream and validate its framing/CRC.

    HDL X/Z words are surfaced through ``unknown_words`` and the UNKNOWN flag.
    They are replaced by zero only to keep framing inspectable; canonical
    snapshot decoding remains blocked unless ``allow_unknown`` is requested.
    """
    words, unknown_words = _parse_hex_words(text)
    if len(words) < 5 or words[0] != TRACE_MAGIC:
        raise TraceDecodeError("trace header is truncated or has invalid magic")
    version = words[1] >> 16
    flags = words[1] & 0xFFFF
    if version != TRACE_VERSION:
        raise TraceDecodeError(f"unsupported trace version: {version}")
    sequence = words[2]
    payload_length = words[3]
    payload_words = (payload_length + WORD_BYTES - 1) // WORD_BYTES
    expected_words = 4 + payload_words + 1
    if len(words) != expected_words:
        raise TraceDecodeError("trace framing length does not match payload")
    if unknown_words and not allow_unknown:
        raise TraceDecodeError("trace contains HDL X/Z/unknown values")
    payload_start = 4
    payload_end = payload_start + payload_words
    padded = b"".join(struct.pack(">I", word) for word in words[payload_start:payload_end])
    payload = padded[:payload_length]
    if zlib.crc32(payload) & 0xFFFFFFFF != words[-1]:
        raise TraceDecodeError("trace payload CRC mismatch")
    if unknown_words:
        flags |= FLAG_UNKNOWN
    return TraceFrame(sequence, flags, payload, unknown_words)


def decode_snapshot_trace(text: str, *, allow_unknown: bool = False) -> tuple[TraceFrame, VisualizationSnapshot]:
    frame = decode_hex_trace(text, allow_unknown=allow_unknown)
    if not frame.is_snapshot:
        raise TraceDecodeError("trace frame is not a snapshot boundary")
    try:
        snapshot = parse_snapshot(frame.payload)
    except (TypeError, ValueError) as error:
        raise TraceDecodeError("trace payload is not a valid TPCV snapshot") from error
    return frame, snapshot


class DiagnosticStream:
    """Bounded downstream FIFO model whose producer is never backpressured."""

    def __init__(self, *, capacity: int = 64) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self._frames: list[TraceFrame] = []
        self.dropped = 0
        self.overflow = False

    @property
    def pending(self) -> tuple[TraceFrame, ...]:
        return tuple(self._frames)

    def reset(self) -> None:
        self._frames.clear()
        self.dropped = 0
        self.overflow = False

    def offer(self, frame: TraceFrame) -> bool:
        if not isinstance(frame, TraceFrame):
            raise TypeError("frame must be a TraceFrame")
        if len(self._frames) >= self.capacity:
            self.dropped += 1
            self.overflow = True
            return False
        self._frames.append(frame)
        return True

    def pop(self) -> TraceFrame | None:
        return self._frames.pop(0) if self._frames else None


__all__ = [
    "DiagnosticStream", "FLAG_INCOMPLETE", "FLAG_RESET", "FLAG_SNAPSHOT_END",
    "FLAG_SNAPSHOT_START", "FLAG_UNKNOWN", "TRACE_MAGIC", "TRACE_VERSION",
    "TraceDecodeError", "TraceFrame", "WORD_BYTES", "decode_hex_trace",
    "decode_snapshot_trace", "encode_hex_trace", "encode_snapshot_trace",
    "encode_trace_frame",
]