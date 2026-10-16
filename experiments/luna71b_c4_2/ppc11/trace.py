from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterator

from .schema import ENVELOPE_FIELDS, SCHEMA_VERSION, validate_record

MAX_LINE_BYTES = 1_048_576
MAX_TRACE_BYTES = 8 * 1024 * 1024
MAX_RECORDS = 10_000


def _canonical(row: dict[str, Any]) -> bytes:
    return (json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


class TraceWriter:
    """Create-once bounded JSONL writer; partial files remain visibly incomplete."""

    def __init__(self, path: str | Path, *, identity: dict[str, Any], max_bytes: int = MAX_TRACE_BYTES) -> None:
        if max_bytes <= 0 or max_bytes > MAX_TRACE_BYTES:
            raise ValueError("invalid PPC-11 trace byte bound")
        required = {"side", "run_id", "source_revision", "runtime_manifest_sha256", "seed", "arm", "split", "example_id", "exposure_id"}
        if set(identity) != required:
            raise ValueError("trace identity has missing or unknown fields")
        self.identity = dict(identity)
        self.path = Path(path)
        if self.path.with_suffix(self.path.suffix + ".complete.json").exists():
            raise FileExistsError("PPC-11 completion marker already exists")
        self._stream = self.path.open("xb")
        self._max_bytes = max_bytes
        self._bytes = 0
        self._index = 0
        self._seen: set[tuple[Any, ...]] = set()
        self._digest = hashlib.sha256()
        self._closed = False
        self._failed = False

    def record(self, comparison_id: str, record_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return self._record(comparison_id, record_type, payload)
        except BaseException:
            self._failed = True
            raise

    def _record(self, comparison_id: str, record_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self._closed:
            raise ValueError("trace writer is closed")
        if self._index >= MAX_RECORDS:
            raise ValueError("PPC-11 record budget exceeded")
        row = {"schema_version": SCHEMA_VERSION, **self.identity, "record_index": self._index,
               "comparison_id": comparison_id, "record_type": record_type, "payload": payload}
        validate_record(row, expected_side=self.identity["side"])
        identity = (row["side"], row["run_id"], row["arm"], row["split"], row["example_id"], row["record_index"])
        if identity in self._seen:
            raise ValueError("duplicate record identity")
        self._seen.add(identity)
        raw = _canonical(row)
        if len(raw) > MAX_LINE_BYTES or self._bytes + len(raw) > self._max_bytes:
            raise ValueError("PPC-11 trace byte budget exceeded")
        written = self._stream.write(raw)
        if written != len(raw):
            raise OSError("short PPC-11 trace write")
        self._digest.update(raw)
        self._bytes += written
        self._index += 1
        return row

    def close(self, *, completed: bool = True) -> None:
        if self._closed:
            return
        self._stream.flush()
        self._stream.close()
        self._closed = True
        if completed and not self._failed and self._index:
            marker = {"format": "ppc11-file-completion-1", "sha256": self.sha256,
                      "byte_size": self._bytes, "record_count": self._index,
                      "identity": self.identity}
            raw_marker = _canonical(marker)
            if len(raw_marker) > MAX_LINE_BYTES:
                raise ValueError("PPC-11 completion marker byte budget exceeded")
            with self.path.with_suffix(self.path.suffix + ".complete.json").open("xb") as stream:
                written = stream.write(raw_marker)
                if written != len(raw_marker):
                    raise OSError("short PPC-11 completion marker write")

    @property
    def sha256(self) -> str:
        return self._digest.hexdigest()

    @property
    def byte_size(self) -> int:
        return self._bytes

    def __enter__(self) -> "TraceWriter":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close(completed=exc_type is None)


def read_trace(path: str | Path, *, expected_side: str | None = None) -> tuple[list[dict[str, Any]], str, int]:
    records: list[dict[str, Any]] = []
    digest = hashlib.sha256()
    size = 0
    seen: set[tuple[Any, ...]] = set()
    with Path(path).open("rb") as stream:
        while True:
            raw = stream.readline(MAX_LINE_BYTES + 1)
            if not raw:
                break
            if len(raw) > MAX_LINE_BYTES or not raw.endswith(b"\n"):
                raise ValueError("oversized or truncated PPC-11 record")
            size += len(raw)
            if size > MAX_TRACE_BYTES:
                raise ValueError("PPC-11 trace byte budget exceeded")
            try:
                row = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ValueError("invalid UTF-8 JSONL record") from error
            if not isinstance(row, dict) or _canonical(row) != raw:
                raise ValueError("noncanonical PPC-11 JSON encoding")
            validate_record(row, expected_side=expected_side)
            expected_index = len(records)
            if row["record_index"] != expected_index:
                raise ValueError("record_index must be contiguous from zero")
            key = (row["side"], row["run_id"], row["arm"], row["split"], row["example_id"], row["record_index"])
            if key in seen:
                raise ValueError("duplicate record identity")
            seen.add(key)
            if records:
                first = records[0]
                for field in ("schema_version", "side", "run_id", "source_revision", "runtime_manifest_sha256", "seed", "arm", "split", "example_id", "exposure_id"):
                    if row[field] != first[field]:
                        raise ValueError(f"trace identity changed at record {expected_index}: {field}")
            digest.update(raw)
            records.append(row)
            if len(records) > MAX_RECORDS:
                raise ValueError("PPC-11 record budget exceeded")
    if not records:
        raise ValueError("empty PPC-11 trace")
    marker_path = Path(path).with_suffix(Path(path).suffix + ".complete.json")
    try:
        with marker_path.open("rb") as stream:
            raw_marker = stream.read(MAX_LINE_BYTES + 1)
        marker = json.loads(raw_marker)
    except (OSError, ValueError) as error:
        raise ValueError("missing or invalid PPC-11 completion marker") from error
    expected_marker = {
        "format": "ppc11-file-completion-1", "sha256": digest.hexdigest(),
        "byte_size": size, "record_count": len(records),
        "identity": {key: records[0][key] for key in records[0]
                     if key not in {"schema_version", "record_index", "comparison_id", "record_type", "payload"}},
    }
    if len(raw_marker) > MAX_LINE_BYTES or _canonical(expected_marker) != raw_marker:
        raise ValueError("altered PPC-11 completion marker or truncated trace")
    return records, digest.hexdigest(), size


def iter_trace(path: str | Path, *, expected_side: str | None = None) -> Iterator[dict[str, Any]]:
    records, _, _ = read_trace(path, expected_side=expected_side)
    yield from records
