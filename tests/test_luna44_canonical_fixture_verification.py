from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts import build_luna44_canonical_fixture as builder
from scripts import verify_luna44_canonical_fixture as verifier


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "luna44-canonical-fixture"
MANIFEST_PATH = ARTIFACTS / "provenance.json"
FIXTURE_PATH = ARTIFACTS / "fixture.json"


@pytest.fixture(scope="module")
def fresh_materializations(tmp_path_factory):
    root = tmp_path_factory.getbasetemp() / "luna44-independent-materializations"
    builder.materialize_independently(root)
    return root / "materialization-a", root / "materialization-b"


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
        require_post_publication_evidence=False,
    )


def _committed_inputs():
    return (
        json.loads(MANIFEST_PATH.read_text(encoding="utf-8")),
        json.loads(FIXTURE_PATH.read_text(encoding="utf-8")),
    )


def test_committed_manifest_is_pinned_and_fully_verified():
    result = verifier.verify_fixture(MANIFEST_PATH, FIXTURE_PATH, ROOT)

    assert result["manifest_sha256"] == verifier.MANIFEST_SHA256
    assert result["fixture_file_sha256"] == verifier.FIXTURE_FILE_SHA256
    assert result["semantic_fixture_sha256"] == verifier.SEMANTIC_FIXTURE_SHA256
    assert result["point_count"] == 5164


def test_missing_manifest_source_file_fails_loudly(tmp_path, fresh_materializations):
    manifest, fixture = _committed_inputs()
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
    manifest, fixture = _committed_inputs()
    manifest["source_files"][0]["sha256"] = "0" * 64

    with pytest.raises(verifier.FixtureVerificationError, match="source SHA-256 mismatch"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_fixture_file_digest_mismatch_fails_loudly(tmp_path, fresh_materializations):
    manifest, _ = _committed_inputs()
    fixture = FIXTURE_PATH.read_bytes() + b" "
    manifest["fixture_byte_length"] = len(fixture)
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
            require_post_publication_evidence=False,
        )


def test_incorrect_fixture_point_count_fails_loudly(tmp_path, fresh_materializations):
    manifest, fixture = _committed_inputs()
    sequence = fixture["sequences"][-1]
    sequence["points"].pop()
    sequence["point_count"] -= 1
    manifest["point_counts"][-1]["point_count"] -= 1

    with pytest.raises(verifier.FixtureVerificationError, match="fixture point count mismatch"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_binary64_decimal_hex_mismatch_fails_loudly(tmp_path, fresh_materializations):
    manifest, fixture = _committed_inputs()
    point = fixture["sequences"][0]["points"][0]
    point["x"]["decimal"] = repr(float.fromhex(point["x"]["hex"]) + 1.0)

    with pytest.raises(verifier.FixtureVerificationError, match="round-trip mismatch"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_manifest_configuration_mismatch_fails_loudly(tmp_path, fresh_materializations):
    manifest, fixture = _committed_inputs()
    manifest["seeds"] = [1, 2, 3, 4, 5]

    with pytest.raises(verifier.FixtureVerificationError, match="seed configuration"):
        _verify_mutation(tmp_path, manifest, fixture)


def test_two_fresh_process_materializations_match_exactly(fresh_materializations):
    first_directory, second_directory = fresh_materializations
    assert first_directory != second_directory
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
