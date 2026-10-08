import math
from pathlib import Path

import pytest

from scripts.luna49_runtime_characterization import (
    DISPOSITION_CHANGED,
    DISPOSITION_IDENTICAL,
    compare_discrete_decisions,
    compare_independent_materializations,
    describe_float_difference,
    build_report,
    runtime_metadata,
    sha256_file,
    ulp_distance,
)

ROOT = Path(__file__).resolve().parents[1]


def test_ulp_distance_counts_adjacent_binary64_values_in_both_signs():
    assert ulp_distance(1.0, math.nextafter(1.0, math.inf)) == 1
    assert ulp_distance(-1.0, math.nextafter(-1.0, -math.inf)) == 1


def test_float_difference_keeps_exact_bits_operands_and_relative_difference():
    historical = 0.16917642496961385
    current = 0.16917642496961388

    result = describe_float_difference(historical, current)

    assert result["historical"] == historical
    assert result["current"] == current
    assert result["absolute_difference"] == abs(current - historical)
    assert result["relative_difference"] == abs(current - historical) / abs(historical)
    assert result["ulp_distance"] == 1
    assert result["historical_bits_be"] != result["current_bits_be"]


def test_ulp_distance_rejects_nonfinite_values():
    with pytest.raises(ValueError, match="finite"):
        ulp_distance(math.inf, 1.0)


def test_runtime_metadata_records_platform_interpreter_and_build():
    metadata = runtime_metadata()

    assert metadata["os"]
    assert metadata["architecture"]
    assert metadata["python_version"]
    assert metadata["python_implementation"]
    assert "CC" in metadata["sysconfig"]
    assert metadata["point_generation_external_dependencies"] == {}


def test_independent_materializations_require_distinct_processes_and_invocations():
    base = {
        "invocation_id": "run-a",
        "process_id": 101,
        "output_directory": "a",
        "semantic_fixture_digest": "semantic",
        "exact_xyz_bits_sha256": "bits",
        "seed_sequence_point_order_sha256": "order",
    }
    other = {**base, "invocation_id": "run-b", "process_id": 202, "output_directory": "b"}

    result = compare_independent_materializations(base, b"fixture", other, b"fixture")

    assert result == {
        "independent_invocations": True,
        "fixture_bytes_equal": True,
        "fixture_sha256_equal": True,
        "semantic_digest_equal": True,
        "exact_xyz_bits_equal": True,
        "ordering_equal": True,
    }
    with pytest.raises(ValueError, match="distinct processes"):
        compare_independent_materializations(base, b"fixture", {**other, "process_id": 101}, b"fixture")


def test_discrete_decision_comparison_distinguishes_same_and_changed_results():
    result = compare_discrete_decisions(
        {"route": "A", "crossed": False},
        {"route": "A", "crossed": True},
    )

    assert result["route"]["classification"] == DISPOSITION_IDENTICAL
    assert result["crossed"]["classification"] == DISPOSITION_CHANGED


def test_report_traces_current_point_without_mutating_canonical_artifacts():
    fixture_path = ROOT / "artifacts/luna44-canonical-fixture/fixture.json"
    provenance_path = ROOT / "artifacts/luna44-canonical-fixture/provenance.json"
    materialization_root = ROOT / "artifacts/luna49-runtime-reproducibility-20261008/current-runs"
    fixture_hash_before = sha256_file(fixture_path)
    provenance_hash_before = sha256_file(provenance_path)

    report = build_report(fixture_path, provenance_path, materialization_root)

    trace = report["first_coordinate_operation_trace"]
    assert trace["stream_id"] == "c00-000"
    assert trace["output_point_index"] == 3
    assert trace["current_intermediates"]["sin_angle"]
    assert trace["historical_intermediates"].startswith("NOT RETAINED")
    assert report["canonical_artifacts_unchanged"]
    assert sha256_file(fixture_path) == fixture_hash_before
    assert sha256_file(provenance_path) == provenance_hash_before