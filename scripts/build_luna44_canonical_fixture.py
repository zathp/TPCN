"""Build the label-free Luna-44 canonical point-stream fixture.

Run once before any neural execution:
    python scripts/build_luna44_canonical_fixture.py

This script invokes only the authorized Luna-34 training-point-sequence
generator. It never calls a scientific runner or reads labels or metadata.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import math
import platform
import struct
import subprocess
import sys
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
        "pre_freeze_materialization_invocations": 2,
        "pre_freeze_materialization_digests": [fixture_digest, fixture_digest],
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


def main() -> None:
    if FIXTURE_PATH.exists() or PROVENANCE_PATH.exists():
        raise FileExistsError(
            "Luna-44 fixture materialization is one-time; refusing to overwrite "
            "an existing fixture or provenance manifest"
        )
    fixture, provenance = _build_fixture()
    ARTIFACT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_bytes(_fixture_json_bytes(fixture))
    PROVENANCE_PATH.write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {FIXTURE_PATH.relative_to(ROOT)} and "
        f"{PROVENANCE_PATH.relative_to(ROOT)}; "
        f"sequences={len(fixture['sequences'])}, "
        f"points={provenance['canonical_row_count']}, "
        f"sha256={provenance['canonical_fixture_sha256']}"
    )


if __name__ == "__main__":
    main()
