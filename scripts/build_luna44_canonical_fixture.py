"""Build the label-free Luna-44 canonical point-stream fixture.

Run once before any neural execution:
    python scripts/build_luna44_canonical_fixture.py

This script invokes only the authorized Luna-34 training-point-sequence
generator. It never calls a scientific runner or reads labels or metadata.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import struct
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SOURCE_REVISION = "a79494cd66be28fd291ed11eddd62d342f457cfd"
EXPECTED_GENERATOR_SHA256 = "17e581cf702fae1f56889472a967d2e8e5fec37cc041edba8247da14a0a8b5db"
EXPECTED_SPIRAL_BENCHMARK_SHA256 = "2ffb1b5ebb23f016436043118bc675eddaa14bfd923129359fe61a12df94d9f0"
SEEDS = tuple(range(5))
SEQUENCES_PER_SEED = 64
ARTIFACT_DIRECTORY = ROOT / "artifacts" / "luna44-canonical-fixture"
FIXTURE_PATH = ARTIFACT_DIRECTORY / "fixture.json"
PROVENANCE_PATH = ARTIFACT_DIRECTORY / "provenance.json"


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _fixture_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode("utf-8")


def _binary64_be_hex(value: float) -> str:
    return struct.pack(">d", value).hex()


def _float_record(value: float) -> dict[str, str]:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("fixture values must be finite binary64 values")
    return {"decimal": repr(value), "hex": value.hex()}


def batch_ordinals(points: Iterable[Any]) -> tuple[int, ...]:
    """Return production-ordered same-time batch ordinals for one sequence."""
    ordinals: list[int] = []
    previous_timestamp: float | None = None
    ordinal = -1
    for point in points:
        timestamp = float(point.timestamp)
        if not math.isfinite(timestamp):
            raise ValueError("fixture timestamps must be finite")
        if previous_timestamp is not None and timestamp < previous_timestamp:
            raise ValueError("timestamps are not ordered")
        if previous_timestamp is None or timestamp != previous_timestamp:
            ordinal += 1
        ordinals.append(ordinal)
        previous_timestamp = timestamp
    return tuple(ordinals)


def _canonical_raw_row(
    *,
    seed: int,
    sequence_index: int,
    stream_id: str,
    point_index: int,
    batch_ordinal: int,
    x: float,
    y: float,
    timestamp: float,
) -> dict[str, Any]:
    return {
        "seed": seed,
        "sequence_index": sequence_index,
        "stream_id": stream_id,
        "point_index": point_index,
        "batch_ordinal": batch_ordinal,
        "x_bits_be": _binary64_be_hex(x),
        "y_bits_be": _binary64_be_hex(y),
        "t_bits_be": _binary64_be_hex(timestamp),
    }


def canonical_raw_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for sequence in fixture["sequences"]:
        for point in sequence["points"]:
            rows.append(
                _canonical_raw_row(
                    seed=point["seed"],
                    sequence_index=point["sequence_index"],
                    stream_id=point["stream_id"],
                    point_index=point["point_index"],
                    batch_ordinal=point["batch_ordinal"],
                    x=float.fromhex(point["x"]["hex"]),
                    y=float.fromhex(point["y"]["hex"]),
                    timestamp=float.fromhex(point["t"]["hex"]),
                )
            )
    return rows


def canonical_fixture_digest(fixture: dict[str, Any]) -> str:
    return _sha256(_canonical_json_bytes(canonical_raw_rows(fixture)))


def _build_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    import run_luna34_excursion_v1_multi_emitter_bridge as generator

    generator_path = ROOT / "run_luna34_excursion_v1_multi_emitter_bridge.py"
    generator_sha256 = _sha256(generator_path.read_bytes())
    if generator_sha256 != EXPECTED_GENERATOR_SHA256:
        raise RuntimeError("authorized generator source differs from the pinned baseline")
    spiral_path = ROOT / "tpcn" / "spiral_benchmark.py"
    spiral_sha256 = _sha256(spiral_path.read_bytes())
    if spiral_sha256 != EXPECTED_SPIRAL_BENCHMARK_SHA256:
        raise RuntimeError("authorized point generator differs from the pinned baseline")

    sequences: list[dict[str, Any]] = []
    for seed in SEEDS:
        point_sequences = generator._training_point_sequences(seed)
        if len(point_sequences) != SEQUENCES_PER_SEED:
            raise RuntimeError("authorized generator did not return exactly 64 sequences")
        for sequence_index, points in enumerate(point_sequences):
            stream_id = f"c{seed:02d}-{sequence_index:03d}"
            ordinals = batch_ordinals(points)
            records = []
            raw_rows = []
            audit_bits = []
            for point_index, (point, batch_ordinal) in enumerate(zip(points, ordinals)):
                x = float(point.x)
                y = float(point.y)
                timestamp = float(point.timestamp)
                audit = x + y
                if not all(math.isfinite(value) for value in (x, y, audit)):
                    raise ValueError("fixture coordinates and audit values must be finite")
                raw_rows.append(
                    _canonical_raw_row(
                        seed=seed,
                        sequence_index=sequence_index,
                        stream_id=stream_id,
                        point_index=point_index,
                        batch_ordinal=batch_ordinal,
                        x=x,
                        y=y,
                        timestamp=timestamp,
                    )
                )
                audit_bits.append(_binary64_be_hex(audit))
                records.append(
                    {
                        "seed": seed,
                        "sequence_index": sequence_index,
                        "stream_id": stream_id,
                        "point_index": point_index,
                        "batch_ordinal": batch_ordinal,
                        "x": _float_record(x),
                        "y": _float_record(y),
                        "t": _float_record(timestamp),
                        "audit_x_plus_y": _float_record(audit),
                    }
                )
            sequences.append(
                {
                    "seed": seed,
                    "sequence_index": sequence_index,
                    "stream_id": stream_id,
                    "point_count": len(records),
                    "source_sha256": _sha256(_canonical_json_bytes(raw_rows)),
                    "derived_audit_sha256": _sha256(
                        _canonical_json_bytes(audit_bits)
                    ),
                    "points": records,
                }
            )

    fixture: dict[str, Any] = {
        "schema": "TPCN-LUNA44-CANONICAL-POINT-FIXTURE-1",
        "canonical_identity": (
            "SHA-256 of compact sorted-key UTF-8 JSON over the ordered raw-row "
            "list; each row contains only seed, sequence_index, stream_id, "
            "point_index, batch_ordinal, and exact big-endian IEEE-754 binary64 "
            "hex for x, y, and t. Audit values and neural outputs are excluded."
        ),
        "sequences": sequences,
    }
    rows = canonical_raw_rows(fixture)
    fixture_digest = _sha256(_canonical_json_bytes(rows))

    execution_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    provenance = {
        "schema": "TPCN-LUNA44-CANONICAL-FIXTURE-PROVENANCE-1",
        "generator": {
            "sequence_builder": {
                "module": "run_luna34_excursion_v1_multi_emitter_bridge",
                "function": "_training_point_sequences",
                "source_path": "run_luna34_excursion_v1_multi_emitter_bridge.py",
                "source_sha256": generator_sha256,
            },
            "point_generator": {
                "module": "tpcn.spiral_benchmark",
                "function": "make_spiral_dataset",
                "source_path": "tpcn/spiral_benchmark.py",
                "source_sha256": spiral_sha256,
            },
            "source_repository_revision": SOURCE_REVISION,
            "point_generation_parameters": {
                "examples_per_class": 16,
                "train_seed": "12007 + seed",
                "evaluation_seed": "22017 + seed; evaluation points are not consumed",
                "spiral_config": asdict(generator.SpiralConfig()),
                "ordering": "random.Random(330000 + seed).shuffle(point_sequences)",
            },
        },
        "generation_execution_revision": execution_revision,
        "generation_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seeds": list(SEEDS),
        "sequences_per_seed": SEQUENCES_PER_SEED,
        "sequence_order": [
            f"c{seed:02d}-{sequence_index:03d}"
            for seed in SEEDS
            for sequence_index in range(SEQUENCES_PER_SEED)
        ],
        "point_counts": [
            {
                "stream_id": sequence["stream_id"],
                "point_count": sequence["point_count"],
            }
            for sequence in sequences
        ],
        "runtime": {
            "python_version": sys.version,
            "python_implementation": sys.implementation.name,
            "platform": platform.platform(),
            "library_versions": {
                "python_standard_library": sys.version,
                "external_dependencies": {},
            },
            "dependency_policy": (
                "Point generation uses Python standard-library random/math and "
                "repository modules; no external package is used to generate points."
            ),
        },
        "canonical_fixture_sha256": fixture_digest,
        "fixture_json_sha256": _sha256(_fixture_json_bytes(fixture)),
        "canonical_row_count": len(rows),
        "neural_execution_started": False,
        "serialization": (
            "UTF-8 JSON, sorted keys, compact separators, ordered row list, "
            "finite numbers only; raw values represented in identity as exact "
            "16-character big-endian IEEE-754 binary64 hex."
        ),
        "audit_boundary": (
            "x+y is stored only as a derived audit value with a separate "
            "derived_audit_sha256; neither audit values nor audit digests enter "
            "canonical fixture identity."
        ),
        "data_access_boundary": (
            "Only generated training point sequences were read. Labels, class "
            "metadata, evaluation streams, and neural outcomes were not read."
        ),
    }
    return fixture, provenance


def _materialization_record(
    fixture: dict[str, Any],
    fixture_bytes: bytes,
    provenance: dict[str, Any],
    *,
    invocation_id: str,
    process_id: int,
    started_at_utc: str,
    completed_at_utc: str,
    output_directory: Path,
) -> dict[str, Any]:
    rows = canonical_raw_rows(fixture)
    environment = provenance["runtime"]
    return {
        "invocation_id": invocation_id,
        "process_id": process_id,
        "started_at_utc": started_at_utc,
        "completed_at_utc": completed_at_utc,
        "output_directory": str(output_directory.resolve()),
        "generator_revision": SOURCE_REVISION,
        "materializer_source_sha256": _sha256(Path(__file__).read_bytes()),
        "generation_execution_revision": provenance["generation_execution_revision"],
        "environment_identity": _sha256(_canonical_json_bytes(environment)),
        "fixture_file_sha256": _sha256(fixture_bytes),
        "semantic_fixture_digest": canonical_fixture_digest(fixture),
        "byte_length": len(fixture_bytes),
        "record_count": len(fixture["sequences"]),
        "ordered_point_count": len(rows),
        "seed_sequence_point_order_sha256": _sha256(
            _canonical_json_bytes(
                [
                    [
                        row["seed"],
                        row["sequence_index"],
                        row["stream_id"],
                        row["point_index"],
                    ]
                    for row in rows
                ]
            )
        ),
        "exact_xyz_bits_sha256": _sha256(
            _canonical_json_bytes(
                [
                    [row["x_bits_be"], row["y_bits_be"], row["t_bits_be"]]
                    for row in rows
                ]
            )
        ),
    }


def _materialize_worker(output_directory: Path) -> None:
    if output_directory.exists():
        raise FileExistsError(f"materialization output already exists: {output_directory}")
    output_directory.mkdir(parents=True)
    invocation_id = uuid.uuid4().hex
    started_at_utc = datetime.now(timezone.utc).isoformat()
    fixture, provenance = _build_fixture()
    fixture_bytes = _fixture_json_bytes(fixture)
    completed_at_utc = datetime.now(timezone.utc).isoformat()
    record = _materialization_record(
        fixture,
        fixture_bytes,
        provenance,
        invocation_id=invocation_id,
        process_id=os.getpid(),
        started_at_utc=started_at_utc,
        completed_at_utc=completed_at_utc,
        output_directory=output_directory,
    )
    (output_directory / "fixture.json").write_bytes(fixture_bytes)
    (output_directory / "provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (output_directory / "materialization.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _verify_materialization(
    record: dict[str, Any], fixture: dict[str, Any], fixture_bytes: bytes
) -> None:
    rows = canonical_raw_rows(fixture)
    if record["fixture_file_sha256"] != _sha256(fixture_bytes):
        raise ValueError("materialization file SHA-256 does not match its output")
    if record["semantic_fixture_digest"] != canonical_fixture_digest(fixture):
        raise ValueError("materialization semantic digest does not match its output")
    if record["byte_length"] != len(fixture_bytes):
        raise ValueError("materialization byte length does not match its output")
    if record["record_count"] != len(fixture["sequences"]):
        raise ValueError("materialization record count does not match its output")
    if record["ordered_point_count"] != len(rows):
        raise ValueError("materialization point count does not match its output")
    expected_order_digest = _sha256(
        _canonical_json_bytes(
            [
                [
                    row["seed"],
                    row["sequence_index"],
                    row["stream_id"],
                    row["point_index"],
                ]
                for row in rows
            ]
        )
    )
    if record["seed_sequence_point_order_sha256"] != expected_order_digest:
        raise ValueError("materialization ordering digest does not match its output")
    expected_bits_digest = _sha256(
        _canonical_json_bytes(
            [[row["x_bits_be"], row["y_bits_be"], row["t_bits_be"]] for row in rows]
        )
    )
    if record["exact_xyz_bits_sha256"] != expected_bits_digest:
        raise ValueError("materialization raw point-bit digest does not match its output")


def _compare_materializations(
    record_a: dict[str, Any],
    fixture_bytes_a: bytes,
    record_b: dict[str, Any],
    fixture_bytes_b: bytes,
) -> dict[str, bool]:
    fixture_a = json.loads(fixture_bytes_a)
    fixture_b = json.loads(fixture_bytes_b)
    _verify_materialization(record_a, fixture_a, fixture_bytes_a)
    _verify_materialization(record_b, fixture_b, fixture_bytes_b)
    if record_a["invocation_id"] == record_b["invocation_id"]:
        raise ValueError("materializations must have distinct invocation identifiers")
    if record_a["process_id"] == record_b["process_id"]:
        raise ValueError("materializations must come from distinct processes")
    if record_a["output_directory"] == record_b["output_directory"]:
        raise ValueError("materializations must use distinct output directories")
    for field in (
        "generator_revision",
        "materializer_source_sha256",
        "generation_execution_revision",
        "environment_identity",
    ):
        if record_a[field] != record_b[field]:
            raise ValueError(f"materializations differ in {field}")

    raw_rows_equal = canonical_raw_rows(fixture_a) == canonical_raw_rows(fixture_b)
    exact_bits_equal = [
        [row["x_bits_be"], row["y_bits_be"], row["t_bits_be"]]
        for row in canonical_raw_rows(fixture_a)
    ] == [
        [row["x_bits_be"], row["y_bits_be"], row["t_bits_be"]]
        for row in canonical_raw_rows(fixture_b)
    ]
    sequence_order_equal = [
        [sequence["seed"], sequence["sequence_index"], sequence["stream_id"]]
        for sequence in fixture_a["sequences"]
    ] == [
        [sequence["seed"], sequence["sequence_index"], sequence["stream_id"]]
        for sequence in fixture_b["sequences"]
    ]
    comparisons = {
        "fixture_bytes_equal": fixture_bytes_a == fixture_bytes_b,
        "file_sha256_equal": record_a["fixture_file_sha256"] == record_b["fixture_file_sha256"],
        "semantic_digest_equal": record_a["semantic_fixture_digest"] == record_b["semantic_fixture_digest"],
        "sequence_point_order_equal": sequence_order_equal,
        "point_by_point_exact_equal": raw_rows_equal and exact_bits_equal,
    }
    if not all(comparisons.values()):
        raise ValueError("independent fixture materializations differ")
    return comparisons


def materialize_independently(
    output_root: Path,
) -> tuple[bytes, dict[str, Any]]:
    if output_root.exists():
        raise FileExistsError(f"materialization root already exists: {output_root}")
    output_a = output_root / "materialization-a"
    output_b = output_root / "materialization-b"
    source_checkout = output_root.parent / f"{output_root.name}-pinned-source"
    subprocess.run(
        [
            "git",
            "worktree",
            "add",
            "--detach",
            str(source_checkout),
            SOURCE_REVISION,
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    try:
        worker_script = source_checkout / "scripts" / Path(__file__).name
        worker_script.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(__file__).resolve(), worker_script)
        for output_directory in (output_a, output_b):
            subprocess.run(
                [
                    sys.executable,
                    str(worker_script),
                    "--materialize-worker",
                    str(output_directory),
                ],
                cwd=source_checkout,
                check=True,
                capture_output=True,
                text=True,
            )
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(source_checkout)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    fixture_bytes_a = (output_a / "fixture.json").read_bytes()
    fixture_bytes_b = (output_b / "fixture.json").read_bytes()
    with (output_a / "materialization.json").open(encoding="utf-8") as source:
        record_a = json.load(source)
    with (output_b / "materialization.json").open(encoding="utf-8") as source:
        record_b = json.load(source)
    comparisons = _compare_materializations(
        record_a, fixture_bytes_a, record_b, fixture_bytes_b
    )
    with (output_a / "provenance.json").open(encoding="utf-8") as source:
        provenance = json.load(source)
    provenance["materializations"] = [record_a, record_b]
    provenance["committed_fixture_invocation_id"] = record_a["invocation_id"]
    provenance["materialization_comparison"] = {
        **comparisons,
        "independent_invocations": True,
        "statement": (
            "Two independent materializations produced identical canonical fixture "
            "bytes in the tested environment."
        ),
    }
    return fixture_bytes_a, provenance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--materialize-worker", type=Path)
    parser.add_argument("--refresh-provenance", action="store_true")
    arguments = parser.parse_args()
    if arguments.materialize_worker is not None:
        _materialize_worker(arguments.materialize_worker)
        return
    artifacts_exist = FIXTURE_PATH.exists() or PROVENANCE_PATH.exists()
    if artifacts_exist and not arguments.refresh_provenance:
        raise FileExistsError(
            "Luna-44 fixture materialization is one-time; refusing to overwrite "
            "an existing fixture or provenance manifest"
        )
    with tempfile.TemporaryDirectory(
        prefix="luna44-materializations-", dir=ARTIFACT_DIRECTORY.parent
    ) as temporary_directory:
        fixture_bytes, provenance = materialize_independently(
            Path(temporary_directory) / "runs"
        )
    ARTIFACT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    if FIXTURE_PATH.exists():
        if FIXTURE_PATH.read_bytes() != fixture_bytes:
            raise RuntimeError(
                "refusing to refresh provenance for a different canonical fixture"
            )
    else:
        FIXTURE_PATH.write_bytes(fixture_bytes)
    PROVENANCE_PATH.write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    fixture = json.loads(fixture_bytes)
    print(
        f"wrote {FIXTURE_PATH.relative_to(ROOT)} and "
        f"{PROVENANCE_PATH.relative_to(ROOT)}; "
        f"sequences={len(fixture['sequences'])}, "
        f"points={provenance['canonical_row_count']}, "
        f"sha256={provenance['canonical_fixture_sha256']}, "
        f"materializations="
        f"{provenance['materializations'][0]['invocation_id']},"
        f"{provenance['materializations'][1]['invocation_id']}"
    )


if __name__ == "__main__":
    main()
