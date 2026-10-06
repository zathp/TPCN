from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts import verify_luna44_canonical_fixture as verifier


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "luna44-canonical-fixture"
MANIFEST_PATH = ARTIFACTS / "provenance.json"
FIXTURE_PATH = ARTIFACTS / "fixture.json"


@pytest.fixture(scope="module")
def fresh_materializations(tmp_path_factory):
    root = tmp_path_factory.mktemp("luna44-independent-materializations")
    directories = (root / "materialization-a", root / "materialization-b")
    for output_directory in directories:
        subprocess.run(
            [
                sys.executable,
                "scripts/build_luna44_canonical_fixture.py",
                "--output-dir",
                str(output_directory),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    return directories


def _write_inputs(tmp_path, manifest, fixture):
    manifest_path = tmp_path / "provenance.json"
    fixture_path = tmp_path / "fixture.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    fixture_path.write_text(json.dumps(fixture), encoding="utf-8")
    manifest["fixture_byte_length"] = fixture_path.stat().st_size
    manifest["fixture_json_sha256"] = hashlib.sha256(
        fixture_path.read_bytes()
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, fixture_path


def _verify_mutation(tmp_path, manifest, fixture):
    manifest_path, fixture_path = _write_inputs(tmp_path, manifest, fixture)
    return verifier.verify_fixture(
        manifest_path,
        fixture_path,
        ROOT,
        expected_manifest_sha256=None,
        expected_fixture_sha256=None,
    )


def test_independent_verifier_accepts_materialized_manifest(fresh_materializations):
    first_directory, _ = fresh_materializations
    result = verifier.verify_fixture(
        first_directory / "provenance.json",
        first_directory / "fixture.json",
        ROOT,
        expected_manifest_sha256=None,
    )

    assert result["manifest_sha256"]
    assert result["fixture_file_sha256"] == verifier.FIXTURE_FILE_SHA256
    assert result["semantic_fixture_sha256"] == verifier.SEMANTIC_FIXTURE_SHA256
    assert result["fixture_byte_length"] == 3_451_453
    assert result["sequence_count"] == 320
    assert result["point_count"] == 5164
    assert result["source_files_verified"] == 4


def test_missing_manifest_source_file_fails_loudly(tmp_path, fresh_materializations):
    first_directory, _ = fresh_materializations
    manifest = json.loads((first_directory / "provenance.json").read_text(encoding="utf-8"))
    fixture = json.loads((first_directory / "fixture.json").read_text(encoding="utf-8"))
    manifest_path, fixture_path = _write_inputs(tmp_path, manifest, fixture)

    with pytest.raises(verifier.FixtureVerificationError, match="missing source file"):
        verifier.verify_fixture(
            manifest_path,
            fixture_path,
            tmp_path,
            expected_manifest_sha256=None,
            expected_fixture_sha256=None,
        )


def test_incorrect_source_sha_fails_loudly(tmp_path, fresh_materializations):
    first_directory, _ = fresh_materializations
    manifest = json.loads((first_directory / "provenance.json").read_text(encoding="utf-8"))
    fixture = json.loads((first_directory / "fixture.json").read_text(encoding="utf-8"))
    manifest["source_files"][0]["sha256"] = "0" * 64

    with pytest.raises(verifier.FixtureVerificationError, match="source SHA-256 mismatch"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_fixture_file_digest_mismatch_fails_loudly(tmp_path, fresh_materializations):
    first_directory, _ = fresh_materializations
    manifest = json.loads((first_directory / "provenance.json").read_text(encoding="utf-8"))
    fixture = (first_directory / "fixture.json").read_bytes() + b" "
    manifest_path = tmp_path / "provenance.json"
    fixture_path = tmp_path / "fixture.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    fixture_path.write_bytes(fixture)

    with pytest.raises(verifier.FixtureVerificationError, match="fixture file SHA-256 mismatch"):
        verifier.verify_fixture(
            manifest_path,
            fixture_path,
            ROOT,
            expected_manifest_sha256=None,
            expected_fixture_sha256=None,
        )


def test_incorrect_fixture_point_count_fails_loudly(tmp_path, fresh_materializations):
    first_directory, _ = fresh_materializations
    manifest = json.loads((first_directory / "provenance.json").read_text(encoding="utf-8"))
    fixture = json.loads((first_directory / "fixture.json").read_text(encoding="utf-8"))
    sequence = fixture["sequences"][-1]
    sequence["points"].pop()
    sequence["point_count"] -= 1
    manifest["point_counts"][-1]["point_count"] -= 1

    with pytest.raises(verifier.FixtureVerificationError, match="fixture point count mismatch"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_binary64_decimal_hex_mismatch_fails_loudly(tmp_path, fresh_materializations):
    first_directory, _ = fresh_materializations
    manifest = json.loads((first_directory / "provenance.json").read_text(encoding="utf-8"))
    fixture = json.loads((first_directory / "fixture.json").read_text(encoding="utf-8"))
    point = fixture["sequences"][0]["points"][0]
    point["x"]["decimal"] = repr(float.fromhex(point["x"]["hex"]) + 1.0)

    with pytest.raises(verifier.FixtureVerificationError, match="round-trip mismatch"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_manifest_configuration_mismatch_fails_loudly(tmp_path, fresh_materializations):
    first_directory, _ = fresh_materializations
    manifest = json.loads((first_directory / "provenance.json").read_text(encoding="utf-8"))
    fixture = json.loads((first_directory / "fixture.json").read_text(encoding="utf-8"))
    manifest["seeds"] = [1, 2, 3, 4, 5]

    with pytest.raises(verifier.FixtureVerificationError, match="seed configuration"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_two_fresh_process_materializations_match_exactly(fresh_materializations):
    first_directory, second_directory = fresh_materializations
    assert first_directory != second_directory
    first_provenance = json.loads(
        (first_directory / "provenance.json").read_text(encoding="utf-8")
    )
    second_provenance = json.loads(
        (second_directory / "provenance.json").read_text(encoding="utf-8")
    )
    assert first_provenance["generation_execution_revision"] == (
        second_provenance["generation_execution_revision"]
    )
    assert first_provenance["materializer"]["sha256"] == (
        second_provenance["materializer"]["sha256"]
    )
    assert first_provenance["generation_timestamp_utc"] != (
        second_provenance["generation_timestamp_utc"]
    )
    result = verifier.compare_materializations(
        first_directory / "fixture.json",
        second_directory / "fixture.json",
    )
    assert result == {
        "fixture_byte_length": 3_451_453,
        "fixture_file_sha256": verifier.FIXTURE_FILE_SHA256,
        "semantic_fixture_sha256": verifier.SEMANTIC_FIXTURE_SHA256,
        "record_count": 5164,
        "all_binary64_bits_and_order_equal": True,
    }
