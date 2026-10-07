"""Independently verify Luna-44 fixture provenance and materialization evidence.

Source identities are verified from their pinned Git objects rather than
platform-dependent checkout bytes.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
from typing import Any


MANIFEST_SHA256 = "6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22"
FIXTURE_FILE_SHA256 = "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629"
SEMANTIC_FIXTURE_SHA256 = "6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305"
SOURCE_REVISION = "a79494cd66be28fd291ed11eddd62d342f457cfd"
MATERIALIZER_REVISION = "10994419cec3646d30d965372f88d10605d83d57"
MATERIALIZER_SHA256 = "696051cc3690aafc9f342e569697469a111757c37c2666b0c026333e6b16efce"
EXPECTED_POINT_COUNT = 5164
EXPECTED_SEQUENCE_COUNT = 320
SEQUENCES_PER_SEED = 64
EXPECTED_FIXTURE_PATH = "artifacts/luna44-canonical-fixture/fixture.json"
EXPECTED_SOURCE_FILES = {
    "materializer": "scripts/build_luna44_canonical_fixture.py",
    "sequence_builder": "run_luna34_excursion_v1_multi_emitter_bridge.py",
    "point_generator": "tpcn/spiral_benchmark.py",
    "point_representation": "tpcn/stroke_dataset.py",
}
EXPECTED_GENERATION_PARAMETERS = {
    "examples_per_class": 16,
    "train_seed": "12007 + seed",
    "evaluation_seed": "22017 + seed; evaluation points are not consumed",
    "spiral_config": {
        "min_points": 12,
        "max_points": 20,
        "min_duration": 240.0,
        "max_duration": 320.0,
        "min_scale": 0.8,
        "max_scale": 1.2,
        "min_angular_speed": 1.7,
        "max_angular_speed": 2.5,
        "min_radial_growth": 0.7,
        "max_radial_growth": 1.1,
        "max_rotation": 6.283185307179586,
        "max_translation": 1.0,
        "max_timing_jitter": 0.08,
        "max_coordinate_noise": 0.025,
        "max_radial_jitter": 0.04,
    },
    "ordering": "random.Random(330000 + seed).shuffle(point_sequences)",
}
EXPECTED_ORDERING_RULE = (
    "for seed in ascending order, preserve the sequence order returned by "
    "_training_point_sequences(seed), identified as c{seed:02d}-{sequence_index:03d}"
)


class FixtureVerificationError(ValueError):
    pass


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _bits(value: float) -> str:
    return struct.pack(">d", value).hex()


def canonical_raw_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for sequence in fixture["sequences"]:
        for point in sequence["points"]:
            rows.append(
                {
                    "seed": point["seed"],
                    "sequence_index": point["sequence_index"],
                    "stream_id": point["stream_id"],
                    "point_index": point["point_index"],
                    "batch_ordinal": point["batch_ordinal"],
                    "x_bits_be": _bits(float.fromhex(point["x"]["hex"])),
                    "y_bits_be": _bits(float.fromhex(point["y"]["hex"])),
                    "t_bits_be": _bits(float.fromhex(point["t"]["hex"])),
                }
            )
    return rows


def _source_records(manifest: dict[str, Any]) -> dict[str, dict[str, str]]:
    records = manifest.get("source_files")
    if not isinstance(records, list):
        raise FixtureVerificationError("manifest source_files must be a list")
    by_role = {}
    for record in records:
        if not isinstance(record, dict):
            raise FixtureVerificationError("invalid manifest source-file record")
        role = record.get("role")
        if role in by_role:
            raise FixtureVerificationError(f"duplicate source role: {role}")
        by_role[role] = record
    if set(by_role) != set(EXPECTED_SOURCE_FILES):
        raise FixtureVerificationError("manifest source-file roles are incomplete")
    for role, expected_path in EXPECTED_SOURCE_FILES.items():
        if by_role[role].get("path") != expected_path:
            raise FixtureVerificationError(f"unexpected source path for {role}")
    return by_role


def _verify_source_files(
    manifest: dict[str, Any], repo_root: Path
) -> dict[str, dict[str, str]]:
    records = _source_records(manifest)
    for role, record in records.items():
        relative_path = Path(record["path"])
        source_path = (repo_root / relative_path).resolve()
        if not source_path.is_relative_to(repo_root.resolve()):
            raise FixtureVerificationError(f"source path escapes repository: {role}")
        if not source_path.is_file():
            raise FixtureVerificationError(f"missing source file: {record['path']}")
        revision = record.get("revision")
        if not isinstance(revision, str) or not revision:
            raise FixtureVerificationError(f"missing source revision: {record['path']}")
        try:
            committed = subprocess.run(
                ["git", "show", f"{revision}:{record['path']}"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            ).stdout
        except subprocess.CalledProcessError as error:
            raise FixtureVerificationError(
                f"source revision cannot provide {record['path']}: {revision}"
            ) from error
        if _sha256(committed) != record.get("sha256"):
            raise FixtureVerificationError(
                f"pinned revision source SHA-256 mismatch: {record['path']}"
            )
    materializer = manifest.get("materializer", {})
    if records["materializer"]["revision"] != materializer.get("repository_revision"):
        raise FixtureVerificationError("materializer revision does not match source manifest")
    if records["sequence_builder"]["revision"] != SOURCE_REVISION:
        raise FixtureVerificationError("sequence-builder revision is not pinned")
    if records["point_generator"]["revision"] != SOURCE_REVISION:
        raise FixtureVerificationError("point-generator revision is not pinned")
    if records["point_representation"]["revision"] != SOURCE_REVISION:
        raise FixtureVerificationError("point-representation revision is not pinned")
    if (
        materializer.get("path") != records["materializer"]["path"]
        or materializer.get("sha256") != records["materializer"]["sha256"]
        or materializer.get("repository_revision")
        != records["materializer"]["revision"]
    ):
        raise FixtureVerificationError("materializer identity does not match source manifest")
    return records


def verify_fixture(
    manifest_path: Path,
    fixture_path: Path,
    repo_root: Path,
    *,
    expected_manifest_sha256: str | None = MANIFEST_SHA256,
    expected_fixture_sha256: str | None = FIXTURE_FILE_SHA256,
    require_post_publication_evidence: bool = True,
) -> dict[str, Any]:
    """Validate committed fixture bytes and all pinned provenance inputs."""
    manifest_bytes = manifest_path.read_bytes()
    if expected_manifest_sha256 and _sha256(manifest_bytes) != expected_manifest_sha256:
        raise FixtureVerificationError("provenance manifest SHA-256 mismatch")
    try:
        manifest = json.loads(manifest_bytes)
        fixture_bytes = fixture_path.read_bytes()
        fixture = json.loads(fixture_bytes)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FixtureVerificationError(f"cannot read manifest or fixture: {error}") from error

    if manifest.get("schema") != "TPCN-LUNA44-CANONICAL-FIXTURE-PROVENANCE-1":
        raise FixtureVerificationError("unexpected provenance manifest schema")
    if manifest.get("manifest_version") != 1:
        raise FixtureVerificationError("unexpected provenance manifest version")
    source_records = _verify_source_files(manifest, repo_root)
    if manifest.get("generator", {}).get("source_repository_revision") != SOURCE_REVISION:
        raise FixtureVerificationError("fixture generation repository revision mismatch")
    if manifest.get("generator", {}).get("sequence_builder", {}).get(
        "source_sha256"
    ) != source_records["sequence_builder"]["sha256"]:
        raise FixtureVerificationError("sequence-builder source SHA-256 mismatch")
    if manifest.get("generator", {}).get("point_generator", {}).get(
        "source_sha256"
    ) != source_records["point_generator"]["sha256"]:
        raise FixtureVerificationError("point-generator source SHA-256 mismatch")
    if manifest.get("fixture_path") != EXPECTED_FIXTURE_PATH:
        raise FixtureVerificationError("canonical fixture path mismatch")
    if manifest.get("seeds") != list(range(5)):
        raise FixtureVerificationError("manifest seed configuration mismatch")
    if manifest.get("sequences_per_seed") != SEQUENCES_PER_SEED:
        raise FixtureVerificationError("manifest sequence configuration mismatch")
    if (
        manifest.get("sequence_count") != EXPECTED_SEQUENCE_COUNT
        or manifest.get("character_count") != EXPECTED_SEQUENCE_COUNT
    ):
        raise FixtureVerificationError("manifest sequence/character count mismatch")
    if manifest.get("expected_sequence_count") != EXPECTED_SEQUENCE_COUNT:
        raise FixtureVerificationError("manifest expected sequence count mismatch")
    if manifest.get("expected_point_count") != EXPECTED_POINT_COUNT:
        raise FixtureVerificationError("manifest expected point count mismatch")
    if manifest.get("generator", {}).get(
        "point_generation_parameters"
    ) != EXPECTED_GENERATION_PARAMETERS:
        raise FixtureVerificationError("manifest point-generation configuration mismatch")
    if manifest.get("ordering_rule") != EXPECTED_ORDERING_RULE:
        raise FixtureVerificationError("manifest ordering rule mismatch")
    if manifest.get("point_representation_format") != (
        "JSON decimal strings plus Python hexadecimal float strings for x, y, t; "
        "canonical identity includes only raw point metadata and the corresponding binary64 bits."
    ):
        raise FixtureVerificationError("manifest point representation mismatch")
    if manifest.get("binary64_encoding") != (
        "struct.pack('>d', float_value).hex(), exactly 16 lowercase hexadecimal "
        "characters in big-endian IEEE-754 binary64 encoding."
    ):
        raise FixtureVerificationError("manifest binary64 encoding mismatch")
    if manifest.get("canonical_serialization_format") != (
        "UTF-8 JSON, sorted keys, compact separators, ordered canonical raw-row "
        "list, finite numbers only"
    ):
        raise FixtureVerificationError("manifest canonical serialization mismatch")
    original = manifest.get("original_publication_materialization", {})
    if (
        original.get("publication_manifest_revision") != "be1f579281e1f39ed17776957f66cd9c40b83c83"
        or original.get("publication_manifest_git_blob")
        != "266a85a7ae42cf9ce66259db556776f0c7fc2e15"
        or original.get("generation_execution_revision")
        != "9226316be4935236ba3f6f511b4abfe8f23af278"
        or original.get("canonical_fixture_publications") != 1
        or original.get("independent_repeat_evidence_retained") is not False
        or original.get("original_independent_materialization_count")
        != "not established by retained evidence"
        or original.get("fixture_file_sha256") != FIXTURE_FILE_SHA256
        or original.get("semantic_fixture_digest") != SEMANTIC_FIXTURE_SHA256
    ):
        raise FixtureVerificationError("original materialization provenance mismatch")
    runtime = manifest.get("runtime", {})
    if require_post_publication_evidence:
        verification = manifest.get(
            "post_publication_independent_materialization_verification", {}
        )
        if verification.get("statement") != (
            "Post-publication independent fixture materialization verification "
            "produced identical canonical fixture bytes/digests under the declared environment."
        ):
            raise FixtureVerificationError("post-publication materialization statement missing")
        if verification.get("scope") != (
            "Same declared runtime environment only; no cross-platform determinism claim."
        ):
            raise FixtureVerificationError("post-publication materialization scope mismatch")
        if (
            verification.get("materializer_revision") != MATERIALIZER_REVISION
            or verification.get("materializer_sha256") != MATERIALIZER_SHA256
            or verification.get("materializer_path")
            != "scripts/build_luna44_canonical_fixture.py"
        ):
            raise FixtureVerificationError("post-publication materializer identity mismatch")
        runs = manifest.get("materializations")
        if not isinstance(runs, list) or len(runs) != 2:
            raise FixtureVerificationError("two independent materialization records are required")
        if [run.get("invocation_id") for run in runs] != verification.get("invocation_ids"):
            raise FixtureVerificationError("post-publication invocation identities mismatch")
        if (
            runs[0].get("invocation_id") == runs[1].get("invocation_id")
            or runs[0].get("process_id") == runs[1].get("process_id")
            or runs[0].get("output_directory") == runs[1].get("output_directory")
            or runs[0].get("started_at_utc") == runs[1].get("started_at_utc")
            or runs[0].get("environment_identity") != runs[1].get("environment_identity")
        ):
            raise FixtureVerificationError("materialization runs are not independent")
        for run in runs:
            if (
                run.get("generator_revision") != SOURCE_REVISION
                or run.get("generation_execution_revision") != SOURCE_REVISION
                or run.get("materializer_source_sha256") != MATERIALIZER_SHA256
                or run.get("byte_length") != 3_451_453
                or run.get("fixture_file_sha256") != FIXTURE_FILE_SHA256
                or run.get("semantic_fixture_digest") != SEMANTIC_FIXTURE_SHA256
                or run.get("record_count") != EXPECTED_SEQUENCE_COUNT
                or run.get("ordered_point_count") != EXPECTED_POINT_COUNT
                or len(run.get("seed_sequence_point_order_sha256", "")) != 64
                or len(run.get("exact_xyz_bits_sha256", "")) != 64
            ):
                raise FixtureVerificationError("materialization result does not match pinned fixture")
        comparison = manifest.get("materialization_comparison", {})
        required_equalities = (
            "fixture_bytes_equal",
            "file_sha256_equal",
            "semantic_digest_equal",
            "sequence_point_order_equal",
            "point_by_point_exact_equal",
            "independent_invocations",
        )
        if (
            any(comparison.get(key) is not True for key in required_equalities)
            or runs[0].get("fixture_file_sha256") != runs[1].get("fixture_file_sha256")
            or runs[0].get("semantic_fixture_digest") != runs[1].get("semantic_fixture_digest")
            or runs[0].get("byte_length") != runs[1].get("byte_length")
            or runs[0].get("record_count") != runs[1].get("record_count")
            or runs[0].get("ordered_point_count") != runs[1].get("ordered_point_count")
            or runs[0].get("seed_sequence_point_order_sha256")
            != runs[1].get("seed_sequence_point_order_sha256")
            or runs[0].get("exact_xyz_bits_sha256") != runs[1].get("exact_xyz_bits_sha256")
            or verification.get("verified_after_original_publication") is not True
        ):
            raise FixtureVerificationError("materialization equality evidence is incomplete")

    if not all(
        runtime.get(key)
        for key in ("python_version", "python_implementation", "platform")
    ):
        raise FixtureVerificationError("manifest runtime environment is incomplete")
    if runtime.get("library_versions", {}).get("external_dependencies") != {}:
        raise FixtureVerificationError("unexpected external point-generation dependency")
    if (
        runtime.get("library_versions", {}).get("python_standard_library")
        != runtime.get("python_version")
    ):
        raise FixtureVerificationError("Python standard-library environment is not pinned")
    if fixture.get("schema") != "TPCN-LUNA44-CANONICAL-POINT-FIXTURE-1":
        raise FixtureVerificationError("unexpected canonical fixture schema")
    if len(fixture.get("sequences", [])) != EXPECTED_SEQUENCE_COUNT:
        raise FixtureVerificationError("fixture sequence count mismatch")
    expected_order = [
        (seed, index, f"c{seed:02d}-{index:03d}")
        for seed in range(5)
        for index in range(SEQUENCES_PER_SEED)
    ]
    observed_order = [
        (item.get("seed"), item.get("sequence_index"), item.get("stream_id"))
        for item in fixture["sequences"]
    ]
    if observed_order != expected_order:
        raise FixtureVerificationError("fixture sequence ordering mismatch")

    point_count = 0
    for sequence in fixture["sequences"]:
        points = sequence.get("points", [])
        if sequence.get("point_count") != len(points):
            raise FixtureVerificationError(
                f"fixture sequence point count mismatch: {sequence.get('stream_id')}"
            )
        previous_timestamp = None
        batch_ordinal = -1
        for index, point in enumerate(points):
            if (
                point.get("seed") != sequence["seed"]
                or point.get("sequence_index") != sequence["sequence_index"]
                or point.get("stream_id") != sequence["stream_id"]
                or point.get("point_index") != index
            ):
                raise FixtureVerificationError("fixture point identity/order mismatch")
            values = {}
            for name in ("x", "y", "t"):
                try:
                    decimal_value = float(point[name]["decimal"])
                    hex_value = float.fromhex(point[name]["hex"])
                except (KeyError, TypeError, ValueError) as error:
                    raise FixtureVerificationError(
                        f"invalid binary64 representation for {name}"
                    ) from error
                if (
                    not math.isfinite(decimal_value)
                    or not math.isfinite(hex_value)
                    or _bits(decimal_value) != _bits(hex_value)
                ):
                    raise FixtureVerificationError(
                        f"binary64 decimal/hex round-trip mismatch: {name}"
                    )
                values[name] = hex_value
            timestamp = values["t"]
            if previous_timestamp is None or timestamp != previous_timestamp:
                if previous_timestamp is not None and timestamp < previous_timestamp:
                    raise FixtureVerificationError("fixture timestamp order decreases")
                batch_ordinal += 1
            if point.get("batch_ordinal") != batch_ordinal:
                raise FixtureVerificationError("fixture batch ordinal mismatch")
            point_count += 1
            previous_timestamp = timestamp
    if point_count != EXPECTED_POINT_COUNT:
        raise FixtureVerificationError(
            f"fixture point count mismatch: expected {EXPECTED_POINT_COUNT}, got {point_count}"
        )
    if manifest.get("canonical_row_count") != point_count:
        raise FixtureVerificationError("manifest canonical row count mismatch")
    if manifest.get("point_counts") != [
        {"stream_id": sequence["stream_id"], "point_count": len(sequence["points"])}
        for sequence in fixture["sequences"]
    ]:
        raise FixtureVerificationError("manifest per-sequence point counts mismatch")

    raw_rows = canonical_raw_rows(fixture)
    semantic_digest = _sha256(_canonical_json_bytes(raw_rows))
    fixture_sha256 = _sha256(fixture_bytes)
    if len(fixture_bytes) != manifest.get("fixture_byte_length"):
        raise FixtureVerificationError("fixture byte length mismatch")
    if fixture_sha256 != manifest.get("fixture_json_sha256"):
        raise FixtureVerificationError("fixture file SHA-256 mismatch")
    if expected_fixture_sha256 and fixture_sha256 != expected_fixture_sha256:
        raise FixtureVerificationError("fixture file SHA-256 is not pinned")
    if (
        semantic_digest != SEMANTIC_FIXTURE_SHA256
        or semantic_digest != manifest.get("semantic_fixture_digest")
        or semantic_digest != manifest.get("canonical_fixture_sha256")
    ):
        raise FixtureVerificationError("semantic fixture digest mismatch")

    return {
        "manifest_sha256": _sha256(manifest_bytes),
        "fixture_file_sha256": fixture_sha256,
        "semantic_fixture_sha256": semantic_digest,
        "fixture_byte_length": len(fixture_bytes),
        "sequence_count": len(fixture["sequences"]),
        "point_count": point_count,
        "source_files_verified": len(EXPECTED_SOURCE_FILES),
    }


def compare_materializations(first: Path, second: Path) -> dict[str, Any]:
    """Require byte-, record-, order-, and binary64-exact fixture equality."""
    first_bytes = first.read_bytes()
    second_bytes = second.read_bytes()
    if first_bytes != second_bytes:
        raise FixtureVerificationError("independent materialization bytes differ")
    first_fixture = json.loads(first_bytes)
    second_fixture = json.loads(second_bytes)
    first_rows = canonical_raw_rows(first_fixture)
    second_rows = canonical_raw_rows(second_fixture)
    if first_rows != second_rows:
        raise FixtureVerificationError("independent materialization point bits/order differ")
    if len(first_rows) != EXPECTED_POINT_COUNT:
        raise FixtureVerificationError("independent materialization point count mismatch")
    semantic_digest = _sha256(_canonical_json_bytes(first_rows))
    if semantic_digest != SEMANTIC_FIXTURE_SHA256:
        raise FixtureVerificationError("independent materialization semantic digest mismatch")
    return {
        "fixture_byte_length": len(first_bytes),
        "fixture_file_sha256": _sha256(first_bytes),
        "semantic_fixture_sha256": semantic_digest,
        "record_count": len(first_rows),
        "all_binary64_bits_and_order_equal": True,
    }
