import copy
import hashlib
import json
import math
import struct
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.build_luna44_canonical_fixture import (
    _canonical_json_bytes,
    batch_ordinals,
    canonical_fixture_digest,
    canonical_raw_rows,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIRECTORY = ROOT / "artifacts" / "luna44-canonical-fixture"
FIXTURE_PATH = ARTIFACT_DIRECTORY / "fixture.json"
PROVENANCE_PATH = ARTIFACT_DIRECTORY / "provenance.json"
EXPECTED_POINT_COUNT = 5164
EXPECTED_CANONICAL_FIXTURE_SHA256 = (
    "6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305"
)
EXPECTED_FIXTURE_JSON_SHA256 = "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629"


@pytest.fixture(scope="module")
def fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def provenance():
    return json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))


def _bits(value):
    return struct.pack(">d", value)


def test_fixture_has_exactly_five_seeds_and_64_ordered_sequences_each(fixture):
    sequences = fixture["sequences"]
    assert len(sequences) == 5 * 64
    for seed in range(5):
        seed_sequences = [item for item in sequences if item["seed"] == seed]
        assert len(seed_sequences) == 64
        assert [item["sequence_index"] for item in seed_sequences] == list(range(64))
        assert [item["stream_id"] for item in seed_sequences] == [
            f"c{seed:02d}-{index:03d}" for index in range(64)
        ]


def test_all_point_identities_values_and_batch_ordinals_are_valid(fixture):
    for sequence in fixture["sequences"]:
        points = sequence["points"]
        assert sequence["point_count"] == len(points) > 0
        assert [point["point_index"] for point in points] == list(range(len(points)))
        ordinals = [point["batch_ordinal"] for point in points]
        assert ordinals[0] == 0
        assert all(right - left in (0, 1) for left, right in zip(ordinals, ordinals[1:]))
        assert all(left <= right for left, right in zip(ordinals, ordinals[1:]))
        for point in points:
            assert point["seed"] == sequence["seed"]
            assert point["sequence_index"] == sequence["sequence_index"]
            assert point["stream_id"] == sequence["stream_id"]
            for field in ("x", "y", "t", "audit_x_plus_y"):
                item = point[field]
                decimal_value = float(item["decimal"])
                hex_value = float.fromhex(item["hex"])
                assert math.isfinite(decimal_value)
                assert _bits(decimal_value) == _bits(hex_value)
            x = float.fromhex(point["x"]["hex"])
            y = float.fromhex(point["y"]["hex"])
            audit = float.fromhex(point["audit_x_plus_y"]["hex"])
            assert _bits(audit) == _bits(x + y)


def test_canonical_digest_is_stable_and_recomputed(fixture, provenance):
    digest = canonical_fixture_digest(fixture)
    assert digest == EXPECTED_CANONICAL_FIXTURE_SHA256
    assert digest == provenance["canonical_fixture_sha256"]
    rows = canonical_raw_rows(fixture)
    assert len(rows) == EXPECTED_POINT_COUNT
    assert len(rows) == provenance["canonical_row_count"]
    assert provenance["fixture_json_sha256"] == EXPECTED_FIXTURE_JSON_SHA256
    assert hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest() == provenance[
        "fixture_json_sha256"
    ]
    assert canonical_fixture_digest(json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))) == digest
    for sequence in fixture["sequences"]:
        sequence_rows = [
            row for row in rows
            if row["seed"] == sequence["seed"]
            and row["sequence_index"] == sequence["sequence_index"]
        ]
        assert hashlib.sha256(_canonical_json_bytes(sequence_rows)).hexdigest() == sequence[
            "source_sha256"
        ]
        audit_bits = [
            _bits(float.fromhex(point["audit_x_plus_y"]["hex"])).hex()
            for point in sequence["points"]
        ]
        assert hashlib.sha256(_canonical_json_bytes(audit_bits)).hexdigest() == sequence[
            "derived_audit_sha256"
        ]


def test_canonical_digest_excludes_derived_audit_values(fixture):
    changed = copy.deepcopy(fixture)
    point = changed["sequences"][0]["points"][0]
    point["audit_x_plus_y"] = {"decimal": "999.0", "hex": "0x1.f380000000000p+9"}
    assert canonical_fixture_digest(changed) == canonical_fixture_digest(fixture)


def test_batch_ordinals_use_numeric_timestamp_equality_and_preserve_order():
    points = [
        SimpleNamespace(timestamp=0.0),
        SimpleNamespace(timestamp=-0.0),
        SimpleNamespace(timestamp=1.0),
        SimpleNamespace(timestamp=1.0),
        SimpleNamespace(timestamp=2.0),
    ]
    assert batch_ordinals(points) == (0, 0, 1, 1, 2)
    with pytest.raises(ValueError, match="not ordered"):
        batch_ordinals(
            [SimpleNamespace(timestamp=2.0), SimpleNamespace(timestamp=1.0)]
        )


def test_fixture_contains_no_labels_or_class_metadata(fixture):
    forbidden = {"label", "metadata", "class", "handedness", "evaluation"}

    def keys_in(value):
        if isinstance(value, dict):
            return set(value).union(*(keys_in(item) for item in value.values()))
        if isinstance(value, list):
            return set().union(*(keys_in(item) for item in value))
        return set()

    assert not (keys_in(fixture) & forbidden)
    assert all(set(sequence) == {
        "seed",
        "sequence_index",
        "stream_id",
        "point_count",
        "source_sha256",
        "derived_audit_sha256",
        "points",
    } for sequence in fixture["sequences"])
    assert all(
        set(point)
        == {
            "seed",
            "sequence_index",
            "stream_id",
            "point_index",
            "batch_ordinal",
            "x",
            "y",
            "t",
            "audit_x_plus_y",
        }
        for sequence in fixture["sequences"]
        for point in sequence["points"]
    )


def test_provenance_is_complete_and_matches_fixture(fixture, provenance):
    generator = provenance["generator"]
    sequence_builder = generator["sequence_builder"]
    assert sequence_builder["module"] == "run_luna34_excursion_v1_multi_emitter_bridge"
    assert sequence_builder["function"] == "_training_point_sequences"
    assert sequence_builder["source_path"] == "run_luna34_excursion_v1_multi_emitter_bridge.py"
    assert sequence_builder["source_sha256"] == (
        "17e581cf702fae1f56889472a967d2e8e5fec37cc041edba8247da14a0a8b5db"
    )
    point_generator = generator["point_generator"]
    assert point_generator["module"] == "tpcn.spiral_benchmark"
    assert point_generator["function"] == "make_spiral_dataset"
    assert point_generator["source_path"] == "tpcn/spiral_benchmark.py"
    assert point_generator["source_sha256"] == (
        "2ffb1b5ebb23f016436043118bc675eddaa14bfd923129359fe61a12df94d9f0"
    )
    assert generator["source_repository_revision"] == "a79494cd66be28fd291ed11eddd62d342f457cfd"
    assert generator["point_generation_parameters"] == {
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
    assert provenance["generation_execution_revision"]
    assert provenance["seeds"] == list(range(5))
    assert provenance["sequences_per_seed"] == 64
    assert provenance["sequence_order"] == [
        f"c{seed:02d}-{index:03d}" for seed in range(5) for index in range(64)
    ]
    assert len(provenance["point_counts"]) == 320
    assert all(item["point_count"] == sequence["point_count"] for item, sequence in zip(
        provenance["point_counts"], fixture["sequences"]
    ))
    runtime = provenance["runtime"]
    assert runtime["python_version"]
    assert runtime["python_implementation"]
    assert runtime["platform"]
    assert runtime["library_versions"]["python_standard_library"] == runtime["python_version"]
    assert runtime["library_versions"]["external_dependencies"] == {}
    assert runtime["dependency_policy"].startswith("Point generation uses Python")
    assert provenance["canonical_fixture_sha256"] == canonical_fixture_digest(fixture)
    assert provenance["original_publication_materialization"] == {
        "invocations": 1,
        "canonical_fixture_sha256": EXPECTED_CANONICAL_FIXTURE_SHA256,
        "independent_repeat_performed": False,
    }
    assert provenance["neural_execution_started"] is False
    assert "not read" in provenance["data_access_boundary"]
    assert "neither audit values nor audit digests enter" in provenance["audit_boundary"]
