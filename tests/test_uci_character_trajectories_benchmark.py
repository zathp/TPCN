from __future__ import annotations

import numpy as np
import pytest
from scipy.io import savemat

from scripts.benchmark_uci_character_trajectories import (
    SOURCE_FILENAME,
    SPLIT_VERSION,
    SplitAssignment,
    TrajectoryRecord,
    as_workload,
    load_uci_dataset,
    make_split,
    parse_matlab_dataset,
)
from tpcn.event_runtime import EventType
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.experiments import ExperimentConfig, ExperimentRunner, SyntheticExample


def _write_dataset(path, *, bad_shape: bool = False, bad_value: bool = False) -> None:
    first = np.array([[1.0, 2.0, 3.0], [0.5, 1.5, 2.5], [0.0, 0.0, 0.0]])
    second = np.array([[4.0, 5.0, 6.0], [3.5, 4.5, 5.5], [1.0, 1.0, 1.0]])
    if bad_shape:
        second = np.ones((2, 3))
    if bad_value:
        first[0, 1] = np.nan
    mixout = np.empty((1, 8), dtype=object)
    for index in range(8):
        mixout[0, index] = first if index < 4 else second
    savemat(
        path,
        {
            "mixout": mixout,
            "consts": {
                "charlabels": np.array([[1, 1, 1, 1, 2, 2, 2, 2]], dtype=np.uint8),
                "key": np.array([["a", "z"]], dtype=object),
                "dt": np.array([[0.005]]),
            },
        },
    )


def test_matlab_parser_validates_source_schema_and_keeps_temporal_order(tmp_path) -> None:
    source = tmp_path / SOURCE_FILENAME
    _write_dataset(source)
    records = load_uci_dataset(source)

    assert len(records) == 8
    assert records[0].example_id == f"{SOURCE_FILENAME}:mixout[0000]"
    assert records[0].label == "a"
    assert records[0].velocities == ((1.0, 0.5), (2.0, 1.5), (3.0, 2.5))
    assert records[4].label == "z"


@pytest.mark.parametrize("invalid", ["shape", "value", "missing"])
def test_matlab_parser_rejects_invalid_source_records(tmp_path, invalid) -> None:
    source = tmp_path / SOURCE_FILENAME
    if invalid == "missing":
        with pytest.raises(ValueError, match="mixout and consts"):
            parse_matlab_dataset({})
        return
    _write_dataset(source, bad_shape=invalid == "shape", bad_value=invalid == "value")

    with pytest.raises(ValueError):
        load_uci_dataset(source)


def test_split_membership_uses_stable_sha256_rank_and_covers_classes() -> None:
    records = tuple(
        TrajectoryRecord(f"record-{index:03d}", index, class_code, label, ((float(index), 0.0),))
        for class_code, label in enumerate(("a", "z"), start=1)
        for index in range((class_code - 1) * 12, class_code * 12)
    )
    split = make_split(records)
    repeated = make_split(tuple(reversed(records)))

    assert split == repeated
    assert tuple(map(len, (split["train"], split["validation"], split["test"]))) == (8, 4, 4)
    for label in ("a", "z"):
        assert [sum(item.record.label == label for item in split[name])
                for name in ("train", "validation", "test")] == [4, 2, 2]
    membership = {
        name: {
            label: sorted(
                item.record.example_id
                for item in split[name]
                if item.record.label == label
            )
            for label in ("a", "z")
        }
        for name in ("train", "validation", "test")
    }
    assert membership == {
        "train": {
            "a": ["record-002", "record-004", "record-005", "record-009"],
            "z": ["record-014", "record-015", "record-019", "record-023"],
        },
        "validation": {
            "a": ["record-000", "record-006"],
            "z": ["record-013", "record-016"],
        },
        "test": {
            "a": ["record-003", "record-007"],
            "z": ["record-020", "record-021"],
        },
    }
    all_ids = [item.record.example_id for assignments in split.values() for item in assignments]
    assert len(all_ids) == len(set(all_ids)) == 16
    assert SPLIT_VERSION == "luna25-v1"


def test_split_rejects_class_without_required_coverage() -> None:
    records = tuple(
        TrajectoryRecord(f"record-{index}", index, 1, "a", ((0.0, 0.0),))
        for index in range(7)
    )
    with pytest.raises(ValueError, match="required"):
        make_split(records)


def test_workload_admits_only_current_scalar_in_order_without_label_payload(monkeypatch) -> None:
    record = TrajectoryRecord(
        "sample-0",
        0,
        1,
        "a",
        ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0)),
    )
    workload = as_workload((SplitAssignment("test", 0, record),))
    example = workload[0]
    assert isinstance(example, SyntheticExample)
    assert example.label == "a"
    assert [(point.x, point.y, point.timestamp) for point in example.points] == [
        (3.0, 0.0, 0.0),
        (7.0, 0.0, 0.005),
        (11.0, 0.0, 0.01),
    ]

    runner = ExperimentRunner(
        ExperimentConfig(
            epochs=1,
            max_points=8,
            topology_node_count=1,
            queue_capacity=32,
            event_budget=64,
            settling_horizon=1.0,
            prediction_expiry=1.0,
        )
    )
    admitted_batches = []
    admit_external_batch = ExcursionCharacterRuntime.admit_external_batch

    def observe_admissions(runtime, contributions):
        batch = tuple(contributions)
        admitted_batches.append(batch)
        admit_external_batch(runtime, batch)

    monkeypatch.setattr(
        ExcursionCharacterRuntime,
        "admit_external_batch",
        observe_admissions,
    )
    result = runner.evaluate(workload)
    assert admitted_batches == [
        ((0.0, 3.0),),
        ((0.005, 7.0),),
        ((0.01, 11.0),),
    ]
    admitted = [
        row for row in result.event_trace
        if len(row) > 3
        and (row[3].value if isinstance(row[3], EventType) else row[3]) == EventType.INPUT.value
    ]
    assert [row[4] for row in admitted] == [3.0, 7.0, 11.0]
    assert [row[0] for row in admitted] == [0.0, 0.005, 0.01]
    assert all("a" not in row for row in admitted)
