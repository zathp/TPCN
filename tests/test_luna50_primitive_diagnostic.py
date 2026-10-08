import math

import pytest

from scripts.luna50_primitive_diagnostic import (
    _DrawRecorder,
    _GaussianTrace,
    compare_values,
    distinct_materializations,
    float_record,
    build_report,
)
from pathlib import Path
import hashlib


def test_raw_random_draw_sequence_matches_random_random():
    traced = _DrawRecorder(12007 ^ 0x5EED5EED)
    control = __import__("random").Random(12007 ^ 0x5EED5EED)
    traced_values = [traced.random() for _ in range(8)]
    control_values = [control.random() for _ in range(8)]
    assert traced_values == control_values
    assert traced.raw_uniforms == control_values


def test_gaussian_trace_reports_draws_transform_and_cached_call_order():
    recorder = _DrawRecorder(31415)
    traced = _GaussianTrace(recorder)
    first, first_trace = traced.gauss(0.0, 0.25)
    second, second_trace = traced.gauss(0.0, 0.25)
    reference = __import__("random").Random(31415)
    assert first == reference.gauss(0.0, 0.25)
    assert second == reference.gauss(0.0, 0.25)
    assert first_trace["cache_hit"] is False
    assert second_trace["cache_hit"] is True
    assert first_trace["raw_uniform_draw_range"] == [0, 2]
    assert second_trace["raw_uniform_draw_range"] == [2, 2]


def test_finite_binary64_reporting_preserves_bits_and_rejects_nonfinite():
    assert float_record(-0.0)["bits_be"] == "8000000000000000"
    with pytest.raises(ValueError, match="finite"):
        float_record(math.inf)


def test_materialization_identity_requires_distinct_processes_and_paths():
    distinct = [
        {"invocation_id": "a", "process_id": 1, "output_directory": "one"},
        {"invocation_id": "b", "process_id": 2, "output_directory": "two"},
    ]
    assert distinct_materializations(distinct)
    assert not distinct_materializations([distinct[0], distinct[0]])
    assert not distinct_materializations(
        [distinct[0], {**distinct[1], "process_id": distinct[0]["process_id"]}]
    )
    assert not distinct_materializations(
        [distinct[0], {**distinct[1], "output_directory": distinct[0]["output_directory"]}]
    )


def test_mismatch_report_is_data_driven_and_names_first_difference():
    report = compare_values({"x": 1.0, "y": 2.0}, {"x": 1.0, "y": 3.0})
    assert report["all_equal"] is False
    assert report["first_difference"] == "y"
    assert report["fields"]["x"]["equal"] is True
    assert report["fields"]["y"]["absolute_difference"] == 1.0


def test_windows_control_report_does_not_mutate_canonical_artifacts():
    root = Path(__file__).resolve().parents[1]
    protected = [
        root / "artifacts/luna44-canonical-fixture/fixture.json",
        root / "artifacts/luna44-canonical-fixture/provenance.json",
    ]
    before = [hashlib.sha256(path.read_bytes()).hexdigest() for path in protected]
    report = build_report()
    after = [hashlib.sha256(path.read_bytes()).hexdigest() for path in protected]
    assert before == after
    assert report["canonical_after"]["unchanged"] is True
    assert report["execution"]["materializations"].startswith("NOT RUN:")