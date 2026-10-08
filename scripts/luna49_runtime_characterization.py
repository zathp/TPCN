"""Read-only numerical and provenance comparisons for the Luna-44 fixture."""

from __future__ import annotations

import hashlib
import argparse
import json
import math
import os
import platform
import random
import struct
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Any, Mapping


CANONICAL_FIXTURE_SHA256 = (
    "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629"
)
CANONICAL_PROVENANCE_SHA256 = (
    "6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22"
)
DISPOSITION_IDENTICAL = "EXACTLY IDENTICAL"
DISPOSITION_NUMERIC_ONLY = "NUMERICALLY DIFFERENT — DISCRETE RESULT IDENTICAL"
DISPOSITION_BOUNDARY_SENSITIVE = "BOUNDARY SENSITIVE"
DISPOSITION_CHANGED = "DISCRETE RESULT CHANGED"
DISPOSITION_NOT_TESTED = "NOT TESTED / OUT OF SCOPE"

_SIGN_BIT = 1 << 63
_UINT64_MASK = (1 << 64) - 1
_FLOAT_FIELDS = ("x", "y", "t", "audit_x_plus_y")
_STRUCTURE_FIELDS = ("seed", "sequence_index", "stream_id", "point_index", "batch_ordinal")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _float_from_record(record: Mapping[str, str]) -> float:
    value = float.fromhex(record["hex"])
    if not math.isfinite(value):
        raise ValueError("fixture comparison only accepts finite binary64 values")
    return value


def _ordered_binary64(value: float) -> int:
    if not math.isfinite(value):
        raise ValueError("ULP distance requires finite binary64 values")
    bits = int.from_bytes(struct.pack(">d", value), "big")
    if bits & _SIGN_BIT:
        return (~bits) & _UINT64_MASK
    return bits | _SIGN_BIT


def ulp_distance(left: float, right: float) -> int:
    """Return representable binary64 steps between two finite values."""
    return abs(_ordered_binary64(left) - _ordered_binary64(right))


def describe_float_difference(historical: float, current: float) -> dict[str, Any]:
    if not math.isfinite(historical) or not math.isfinite(current):
        raise ValueError("fixture comparison only accepts finite binary64 values")
    absolute = abs(current - historical)
    return {
        "historical": historical,
        "current": current,
        "historical_hex": historical.hex(),
        "current_hex": current.hex(),
        "historical_bits_be": struct.pack(">d", historical).hex(),
        "current_bits_be": struct.pack(">d", current).hex(),
        "absolute_difference": absolute,
        "relative_difference": absolute / abs(historical) if historical else None,
        "ulp_distance": ulp_distance(historical, current),
    }


def compare_independent_materializations(
    record_a: Mapping[str, Any],
    bytes_a: bytes,
    record_b: Mapping[str, Any],
    bytes_b: bytes,
) -> dict[str, Any]:
    if record_a["invocation_id"] == record_b["invocation_id"]:
        raise ValueError("materializations must have distinct invocation identifiers")
    if record_a["process_id"] == record_b["process_id"]:
        raise ValueError("materializations must come from distinct processes")
    if record_a["output_directory"] == record_b["output_directory"]:
        raise ValueError("materializations must use distinct output directories")
    if bytes_a != bytes_b:
        raise ValueError("independent fixture materialization bytes differ")
    return {
        "independent_invocations": True,
        "fixture_bytes_equal": True,
        "fixture_sha256_equal": hashlib.sha256(bytes_a).hexdigest()
        == hashlib.sha256(bytes_b).hexdigest(),
        "semantic_digest_equal": record_a["semantic_fixture_digest"]
        == record_b["semantic_fixture_digest"],
        "exact_xyz_bits_equal": record_a["exact_xyz_bits_sha256"]
        == record_b["exact_xyz_bits_sha256"],
        "ordering_equal": record_a["seed_sequence_point_order_sha256"]
        == record_b["seed_sequence_point_order_sha256"],
    }


def compare_discrete_decisions(
    historical: Mapping[str, Any], current: Mapping[str, Any]
) -> dict[str, Any]:
    decisions = sorted(set(historical) | set(current))
    comparisons = {}
    for name in decisions:
        if name not in historical or name not in current:
            comparisons[name] = {
                "classification": DISPOSITION_CHANGED,
                "historical": historical.get(name),
                "current": current.get(name),
            }
            continue
        same = historical[name] == current[name]
        comparisons[name] = {
            "classification": DISPOSITION_IDENTICAL if same else DISPOSITION_CHANGED,
            "historical": historical[name],
            "current": current[name],
        }
    return comparisons


def runtime_metadata() -> dict[str, Any]:
    return {
        "os": platform.platform(),
        "os_name": os.name,
        "architecture": platform.machine(),
        "python_version": sys.version,
        "python_implementation": sys.implementation.name,
        "python_build": platform.python_build(),
        "python_compiler": platform.python_compiler(),
        "libc": platform.libc_ver(),
        "sysconfig": {
            name: sysconfig.get_config_var(name)
            for name in ("CC", "CONFIG_ARGS", "MULTIARCH")
        },
        "point_generation_external_dependencies": {},
        "math_module": getattr(math, "__file__", "built-in"),
        "historical_libc_libm": "not captured as a library identity in provenance",
        "windows_crt_observation": {
            "path": r"C:\WINDOWS\System32\ucrtbase.dll",
            "file_version": "10.0.19041.3636",
            "source": "PowerShell Get-Item VersionInfo on 2026-10-08",
        },
    }


def _point_value(point: Mapping[str, Any], field: str) -> float:
    return _float_from_record(point[field])


def compare_fixtures(historical: Mapping[str, Any], current: Mapping[str, Any]) -> dict[str, Any]:
    historical_sequences = historical["sequences"]
    current_sequences = current["sequences"]
    if len(historical_sequences) != len(current_sequences):
        raise ValueError("fixture sequence counts differ")

    stats: dict[str, dict[str, Any]] = {
        field: {
            "differing_points": 0,
            "maximum_absolute_difference": 0.0,
            "maximum_relative_difference": 0.0,
            "maximum_ulp_distance": 0,
            "ulp_histogram": {},
            "first_difference": None,
        }
        for field in _FLOAT_FIELDS
    }
    structure_equal = True
    sequence_order_equal = True
    point_count = 0
    first_coordinate_divergence = None
    timestamp_gaps = []

    for old_sequence, new_sequence in zip(historical_sequences, current_sequences):
        if (old_sequence["seed"], old_sequence["sequence_index"], old_sequence["stream_id"]) != (
            new_sequence["seed"], new_sequence["sequence_index"], new_sequence["stream_id"]
        ):
            sequence_order_equal = False
        old_points = old_sequence["points"]
        new_points = new_sequence["points"]
        if len(old_points) != len(new_points):
            raise ValueError("fixture point counts differ")
        previous_timestamp = None
        for old_point, new_point in zip(old_points, new_points):
            point_count += 1
            identity_equal = all(old_point[field] == new_point[field] for field in _STRUCTURE_FIELDS)
            structure_equal = structure_equal and identity_equal
            if previous_timestamp is not None:
                gap = _point_value(old_point, "t") - previous_timestamp
                if gap > 0:
                    timestamp_gaps.append(gap)
            previous_timestamp = _point_value(old_point, "t")

            location = {
                "seed": old_point["seed"],
                "sequence_index": old_point["sequence_index"],
                "stream_id": old_point["stream_id"],
                "point_index": old_point["point_index"],
            }
            for field in _FLOAT_FIELDS:
                old_value = _point_value(old_point, field)
                new_value = _point_value(new_point, field)
                if old_value == new_value:
                    continue
                difference = describe_float_difference(old_value, new_value)
                field_stats = stats[field]
                field_stats["differing_points"] += 1
                field_stats["maximum_absolute_difference"] = max(
                    field_stats["maximum_absolute_difference"], difference["absolute_difference"]
                )
                if difference["relative_difference"] is not None:
                    field_stats["maximum_relative_difference"] = max(
                        field_stats["maximum_relative_difference"], difference["relative_difference"]
                    )
                field_stats["maximum_ulp_distance"] = max(
                    field_stats["maximum_ulp_distance"], difference["ulp_distance"]
                )
                histogram = field_stats["ulp_histogram"]
                key = str(difference["ulp_distance"])
                histogram[key] = histogram.get(key, 0) + 1
                item = {**location, "field": field, **difference}
                if field_stats["first_difference"] is None:
                    field_stats["first_difference"] = item
                if field in ("x", "y") and first_coordinate_divergence is None:
                    first_coordinate_divergence = item

    return {
        "point_count": point_count,
        "sequence_count": len(historical_sequences),
        "sequence_order_equal": sequence_order_equal,
        "point_identity_and_batch_ordinals_equal": structure_equal,
        "coordinate_and_audit_values_equal": all(
            stats[field]["differing_points"] == 0 for field in ("x", "y", "audit_x_plus_y")
        ),
        "timestamps_bit_identical": stats["t"]["differing_points"] == 0,
        "minimum_positive_historical_timestamp_gap": min(timestamp_gaps)
        if timestamp_gaps
        else None,
        "first_coordinate_divergence": first_coordinate_divergence,
        "fields": stats,
        "historical_intermediate_values": (
            "Not retained. The canonical fixture contains final x/y/t and derived x+y only; "
            "historical trig, rotation, and Gaussian-noise operands/results cannot be recovered "
            "uniquely from those final coordinates."
        ),
    }


def trace_first_coordinate_point(
    historical_fixture: Mapping[str, Any], current_fixture: Mapping[str, Any]
) -> dict[str, Any]:
    repository_root = Path(__file__).resolve().parents[1]
    if str(repository_root) not in sys.path:
        sys.path.insert(0, str(repository_root))
    from tpcn.spiral_benchmark import SpiralConfig, make_spiral_dataset

    seed = 0
    sequence_index = 0
    point_index = 3
    dataset = make_spiral_dataset(
        examples_per_class=16,
        train_seed=12007 + seed,
        evaluation_seed=22017 + seed,
        config=SpiralConfig(),
    )
    examples = list(dataset.train)
    random.Random(330000 + seed).shuffle(examples)
    example = examples[sequence_index]
    current_sequence = current_fixture["sequences"][sequence_index]
    historical_sequence = historical_fixture["sequences"][sequence_index]
    if current_sequence["stream_id"] != "c00-000" or historical_sequence["stream_id"] != "c00-000":
        raise ValueError("expected first divergence stream c00-000")
    if len(example.points) != len(current_sequence["points"]):
        raise ValueError("traced generator sequence does not match the materialized sequence")
    for generated, record in zip(example.points, current_sequence["points"]):
        if (generated.x.hex(), generated.y.hex(), generated.timestamp.hex()) != (
            float.fromhex(record["x"]["hex"]).hex(),
            float.fromhex(record["y"]["hex"]).hex(),
            float.fromhex(record["t"]["hex"]).hex(),
        ):
            raise ValueError("traced generator output differs from the retained current run")

    metadata = example.metadata
    source_point_index = (
        metadata.sample_count - 1 - point_index
        if metadata.traversal == "inward"
        else point_index
    )
    fraction = source_point_index / (metadata.sample_count - 1)
    cos_rotation = math.cos(float(metadata.rotation))
    sin_rotation = math.sin(float(metadata.rotation))
    rng = random.Random(metadata.seed ^ 0x5EED5EED)
    for _ in range(1, metadata.sample_count):
        rng.uniform(-metadata.timing_jitter, metadata.timing_jitter)

    selected: dict[str, Any] | None = None
    for index in range(1, source_point_index + 1):
        radial_jitter = rng.uniform(-metadata.radial_jitter, metadata.radial_jitter)
        point_fraction = index / (metadata.sample_count - 1)
        radial_base = metadata.radial_growth * point_fraction
        radius = radial_base + radial_jitter
        angle_rate = metadata.angular_speed * point_fraction
        angle_turns = angle_rate * 2.0
        theta = angle_turns * math.pi
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        scaled_radius = float(metadata.scale) * radius
        local_x = scaled_radius * cos_theta
        handed_scaled_radius = metadata.handedness * float(metadata.scale)
        handed_scaled_radius = handed_scaled_radius * radius
        local_y = handed_scaled_radius * sin_theta
        rotated_x_cos_term = cos_rotation * local_x
        rotated_x_sin_term = sin_rotation * local_y
        rotated_x = rotated_x_cos_term - rotated_x_sin_term
        rotated_y_sin_term = sin_rotation * local_x
        rotated_y_cos_term = cos_rotation * local_y
        rotated_y = rotated_y_sin_term + rotated_y_cos_term
        noise_x = rng.gauss(0.0, float(metadata.coordinate_noise))
        noise_y = rng.gauss(0.0, float(metadata.coordinate_noise))
        coordinate_x_before_offset = rotated_x + noise_x
        coordinate_y_before_offset = rotated_y + noise_y
        current_x = metadata.offset_x + coordinate_x_before_offset
        current_y = metadata.offset_y + coordinate_y_before_offset
        if index == source_point_index:
            selected = {
                "source_point_index": index,
                "fraction": point_fraction,
                "raw_spiral_angle": theta,
                "radius": radius,
                "sin_angle": sin_theta,
                "cos_angle": cos_theta,
                "unrotated_coordinate": {"x": local_x, "y": local_y},
                "rotation_constant": metadata.rotation,
                "sin_rotation": sin_rotation,
                "cos_rotation": cos_rotation,
                "rotated_before_noise": {"x": rotated_x, "y": rotated_y},
                "noise_source_and_value": {
                    "generator": "random.Random.gauss(0.0, coordinate_noise)",
                    "x": noise_x,
                    "y": noise_y,
                },
                "coordinate_before_offset": {
                    "x": coordinate_x_before_offset,
                    "y": coordinate_y_before_offset,
                },
                "offset": {"x": metadata.offset_x, "y": metadata.offset_y},
                "current_final": {
                    "x": current_x,
                    "y": current_y,
                },
                "operations": [
                    {"operation": "math.cos(rotation)", "operands": [metadata.rotation], "result": cos_rotation},
                    {"operation": "math.sin(rotation)", "operands": [metadata.rotation], "result": sin_rotation},
                    {"operation": "radial_growth * fraction", "operands": [metadata.radial_growth, point_fraction], "result": radial_base},
                    {"operation": "radial_base + radial_jitter", "operands": [radial_base, radial_jitter], "result": radius},
                    {"operation": "angular_speed * fraction", "operands": [metadata.angular_speed, point_fraction], "result": angle_rate},
                    {"operation": "angle_rate * 2.0", "operands": [angle_rate, 2.0], "result": angle_turns},
                    {"operation": "angle_turns * pi", "operands": [angle_turns, math.pi], "result": theta},
                    {"operation": "math.cos(theta)", "operands": [theta], "result": cos_theta},
                    {"operation": "math.sin(theta)", "operands": [theta], "result": sin_theta},
                    {"operation": "scale * radius", "operands": [metadata.scale, radius], "result": scaled_radius},
                    {"operation": "scaled_radius * cos(theta)", "operands": [scaled_radius, cos_theta], "result": local_x},
                    {"operation": "handedness * scale", "operands": [metadata.handedness, metadata.scale], "result": metadata.handedness * metadata.scale},
                    {"operation": "handed_scaled_radius * radius", "operands": [metadata.handedness * metadata.scale, radius], "result": handed_scaled_radius},
                    {"operation": "handed_scaled_radius * sin(theta)", "operands": [handed_scaled_radius, sin_theta], "result": local_y},
                    {"operation": "cos(rotation) * local_x", "operands": [cos_rotation, local_x], "result": rotated_x_cos_term},
                    {"operation": "sin(rotation) * local_y", "operands": [sin_rotation, local_y], "result": rotated_x_sin_term},
                    {"operation": "rotated_x_cos_term - rotated_x_sin_term", "operands": [rotated_x_cos_term, rotated_x_sin_term], "result": rotated_x},
                    {"operation": "sin(rotation) * local_x", "operands": [sin_rotation, local_x], "result": rotated_y_sin_term},
                    {"operation": "cos(rotation) * local_y", "operands": [cos_rotation, local_y], "result": rotated_y_cos_term},
                    {"operation": "rotated_y_sin_term + rotated_y_cos_term", "operands": [rotated_y_sin_term, rotated_y_cos_term], "result": rotated_y},
                    {"operation": "rotated_x + gaussian_noise_x", "operands": [rotated_x, noise_x], "result": coordinate_x_before_offset},
                    {"operation": "rotated_y + gaussian_noise_y", "operands": [rotated_y, noise_y], "result": coordinate_y_before_offset},
                    {"operation": "offset_x + coordinate_x_before_offset", "operands": [metadata.offset_x, coordinate_x_before_offset], "result": current_x},
                    {"operation": "offset_y + coordinate_y_before_offset", "operands": [metadata.offset_y, coordinate_y_before_offset], "result": current_y},
                ],
            }
    if selected is None:
        raise RuntimeError("could not trace requested source point")

    old_point = historical_sequence["points"][point_index]
    new_point = current_sequence["points"][point_index]
    historical_x = float.fromhex(old_point["x"]["hex"])
    historical_y = float.fromhex(old_point["y"]["hex"])
    current_x = float.fromhex(new_point["x"]["hex"])
    current_y = float.fromhex(new_point["y"]["hex"])
    if (selected["current_final"]["x"].hex(), selected["current_final"]["y"].hex()) != (
        current_x.hex(), current_y.hex()
    ):
        raise ValueError("intermediate trace does not reconstruct the current point")
    return {
        "stream_id": "c00-000",
        "output_point_index": point_index,
        "generator_point_index": source_point_index,
        "label": metadata.label,
        "traversal": metadata.traversal,
        "nuisance_parameters": {
            "rotation": metadata.rotation,
            "scale": metadata.scale,
            "offset_x": metadata.offset_x,
            "offset_y": metadata.offset_y,
            "angular_speed": metadata.angular_speed,
            "radial_growth": metadata.radial_growth,
            "coordinate_noise": metadata.coordinate_noise,
            "radial_jitter": metadata.radial_jitter,
        },
        "current_intermediates": selected,
        "historical_final": {"x": historical_x, "y": historical_y},
        "current_final": {"x": current_x, "y": current_y},
        "historical_vs_current": {
            "x": describe_float_difference(historical_x, current_x),
            "y": describe_float_difference(historical_y, current_y),
            "x_plus_y": describe_float_difference(
                _point_value(old_point, "audit_x_plus_y"),
                _point_value(new_point, "audit_x_plus_y"),
            ),
        },
        "historical_intermediates": "NOT RETAINED; cannot be uniquely reconstructed from final coordinates",
        "serialization": {
            "format": "decimal repr plus Python float.hex; canonical identity uses packed big-endian binary64",
            "historical_x_hex": historical_x.hex(),
            "current_x_hex": current_x.hex(),
            "historical_y_hex": historical_y.hex(),
            "current_y_hex": current_y.hex(),
        },
    }


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def build_report(
    canonical_fixture_path: Path,
    canonical_provenance_path: Path,
    materialization_root: Path,
) -> dict[str, Any]:
    fixture_hash_before = sha256_file(canonical_fixture_path)
    provenance_hash_before = sha256_file(canonical_provenance_path)
    if fixture_hash_before != CANONICAL_FIXTURE_SHA256:
        raise ValueError("canonical fixture SHA-256 does not match its protected identity")
    if provenance_hash_before != CANONICAL_PROVENANCE_SHA256:
        raise ValueError("canonical provenance SHA-256 does not match its protected identity")

    historical = load_json(canonical_fixture_path)
    historical_provenance = load_json(canonical_provenance_path)
    repository_root = Path(__file__).resolve().parents[1]
    repository_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repository_root, check=True, capture_output=True, text=True
    ).stdout.strip()
    diagnostic_git_blob = subprocess.run(
        ["git", "hash-object", str(Path(__file__).resolve())],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    current_a_path = materialization_root / "materialization-a" / "fixture.json"
    current_b_path = materialization_root / "materialization-b" / "fixture.json"
    current_a_bytes = current_a_path.read_bytes()
    current_b_bytes = current_b_path.read_bytes()
    current_a_record = load_json(materialization_root / "materialization-a" / "materialization.json")
    current_b_record = load_json(materialization_root / "materialization-b" / "materialization.json")
    independent_comparison = compare_independent_materializations(
        current_a_record, current_a_bytes, current_b_record, current_b_bytes
    )
    current = json.loads(current_a_bytes)
    comparison = compare_fixtures(historical, current)

    fixture_hash_after = sha256_file(canonical_fixture_path)
    provenance_hash_after = sha256_file(canonical_provenance_path)
    if (fixture_hash_before, provenance_hash_before) != (fixture_hash_after, provenance_hash_after):
        raise RuntimeError("read-only characterization changed a canonical artifact")

    return {
        "schema": "TPCN-LUNA49-RUNTIME-CHARACTERIZATION-1",
        "authorization_contract_revision": "7739ad7af868e2b2f5ebcf9685c25978022a25af",
        "authorization_identifier_as_supplied": "59e5ab7b475b74a23faeddc2563eedf1e044 (unresolved; not a full Git object ID)",
        "starting_revision": "7739ad7af868e2b2f5ebcf9685c25978022a25af",
        "diagnostic_repository_revision_at_capture": repository_revision,
        "diagnostic_source_path": "scripts/luna49_runtime_characterization.py",
        "diagnostic_source_sha256": sha256_file(Path(__file__)),
        "diagnostic_source_git_blob": diagnostic_git_blob,
        "canonical_source_revision": historical_provenance["generator"]["source_repository_revision"],
        "canonical_source_identities": historical_provenance["source_files"],
        "canonical_fixture_sha256": fixture_hash_before,
        "canonical_semantic_digest": historical_provenance["semantic_fixture_digest"],
        "canonical_provenance_sha256": provenance_hash_before,
        "historical_runtime": historical_provenance["runtime"],
        "historical_retained_materializations": historical_provenance["materializations"],
        "current_runtime": runtime_metadata(),
        "runtime_matrix": [
            {
                "runtime": "CPython 3.12.3 / Linux x86_64 / glibc 2.39 / GCC 13.3.0",
                "evidence": "two independently recorded post-publication materializations in canonical provenance",
                "fixture_sha256": CANONICAL_FIXTURE_SHA256,
                "classification": "BYTE-DETERMINISTIC IN RETAINED EVIDENCE; Luna-49 exact replay not available",
            },
            {
                "runtime": "CPython 3.11.5 / Windows x64",
                "evidence": "Luna-48 reviewed independent materializations",
                "fixture_sha256": "60f551e06072b3fb7e814affa97f4a01e079c426d6044d3e710ad9a219ed907e",
                "classification": "BYTE-DETERMINISTIC IN REVIEWED RUNS; environment-dependent from canonical",
            },
            {
                "runtime": "CPython 3.11.4 / Windows 10 x64 / UCRT 10.0.19041.3636",
                "evidence": "two independent Luna-49 materializations",
                "fixture_sha256": "60f551e06072b3fb7e814affa97f4a01e079c426d6044d3e710ad9a219ed907e",
                "classification": "BYTE-DETERMINISTIC; environment-dependent from canonical",
            },
            {
                "runtime": "CPython 3.10 / Windows",
                "evidence": "Luna-48 review reports the first differing point and nuisance inputs matched Python 3.11 Windows",
                "fixture_sha256": None,
                "classification": "VALUE OBSERVATION ONLY; full fixture determinism not established",
            },
            {
                "runtime": "CPython 3.12 / Windows and other Linux runtimes",
                "evidence": "not installed or available in the execution environment",
                "fixture_sha256": None,
                "classification": "NOT ESTABLISHED",
            },
        ],
        "current_materializations": [current_a_record, current_b_record],
        "current_independent_materialization_comparison": independent_comparison,
        "current_fixture_sha256": current_a_record["fixture_file_sha256"],
        "current_semantic_digest": current_a_record["semantic_fixture_digest"],
        "canonical_comparison": comparison,
        "first_coordinate_operation_trace": trace_first_coordinate_point(historical, current),
        "historical_runtime_reproduction": "NOT ESTABLISHED: Python 3.12.3/Linux/glibc 2.39 unavailable here",
        "downstream_decisions": {
            "point_order_timestamps_batch_ordinals": DISPOSITION_IDENTICAL
            if comparison["sequence_order_equal"]
            and comparison["point_identity_and_batch_ordinals_equal"]
            and comparison["timestamps_bit_identical"]
            else DISPOSITION_CHANGED,
            "canonical_fixture_identity_gate": DISPOSITION_CHANGED,
            "canonical_fixture_identity_gate_note": (
                "Expected provenance distinction: fresh Windows file/semantic hashes do not equal "
                "the historical canonical identity; fresh values must not be substituted for the fixture."
            ),
            "neuron_threshold_crossings_routes_and_Luna46_categories": DISPOSITION_NOT_TESTED,
            "reason": (
                "The retained downstream artifacts contain decisions from the historical fixture, "
                "but no equivalent fresh-runtime decision outputs. Recomputing them would execute "
                "an excluded Luna-44/Luna-46/Luna-47 scientific path."
            ),
            "threshold_margin": "UNKNOWN: no downstream threshold values were re-evaluated under this contract boundary",
            "timestamp_order_boundary_margin": {
                "minimum_positive_historical_intra_sequence_gap": comparison["minimum_positive_historical_timestamp_gap"],
                "timestamp_variation": 0.0,
                "assessment": "EXACTLY IDENTICAL; no timestamp delta approaches the positive-order boundary",
            },
        },
        "retained_gate_drift": {
            "luna46_catalog": {
                "classification": "CHECKOUT-MATERIALIZATION INVARIANT; retained Git object valid",
                "expected_git_blob_sha256": "a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e",
                "windows_working_bytes_sha256": "5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80",
                "lf_normalization_matches_git_blob": True,
            },
            "luna47f": {
                "classification": "EXPECTED RETAINED-SNAPSHOT DRIFT; later governance rebaseline required",
                "replay_failure": "retained input drift",
                "retained_protected_entries": 995,
                "current_protected_entries": 999,
                "differing_protected_entries": 54,
                "causes_observed": [
                    "reviewed Luna-48 generator/verifier and governance source changes",
                    "subsequent governance additions",
                    "Git-LF-to-CRLF checkout materialization for retained JSON evidence",
                ],
                "retained_scientific_artifacts_modified": False,
            },
        },
        "runtime_matrix_limitations": [
            "Python 3.10/Windows, Python 3.12/Windows, and Linux runtimes were unavailable.",
            "The current CPython 3.11.4 Windows build uses MSC v.1934; platform.libc_ver() is empty.",
            "The historical provenance records glibc 2.39 and GCC 13.3.0 but no exact libm binary identity.",
        ],
        "canonical_artifacts_unchanged": True,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "artifacts" / "luna49-runtime-reproducibility-20261008" / "characterization.json",
    )
    parser.add_argument("--refresh", action="store_true")
    arguments = parser.parse_args()
    if arguments.output.exists() and not arguments.refresh:
        raise FileExistsError(f"refusing to overwrite existing diagnostic artifact: {arguments.output}")
    report = build_report(
        root / "artifacts" / "luna44-canonical-fixture" / "fixture.json",
        root / "artifacts" / "luna44-canonical-fixture" / "provenance.json",
        root / "artifacts" / "luna49-runtime-reproducibility-20261008" / "current-runs",
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {arguments.output}; current_sha256={report['current_fixture_sha256']}; "
        f"canonical_unchanged={report['canonical_artifacts_unchanged']}"
    )


if __name__ == "__main__":
    main()