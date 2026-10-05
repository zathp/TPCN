from __future__ import annotations

import json
import random

from tpcn.experiments import ExperimentRunner, SyntheticExample
from run_luna33_acp0007_four_class_efficacy import (
    CONDITIONS,
    INITIAL_TOPOLOGIES,
    LABELS,
    RING_NEIGHBORS,
    SEEDS,
    _admitted_edges,
    _canonical_json,
    _destroy_coordinate_time_order,
    _route_uses,
    _summary_results,
    _write_json,
    build_config,
    build_dataset,
    verify_topology_profile,
)
from tpcn.stroke_dataset import StrokePoint


def test_dataset_splits_and_order_are_deterministic_disjoint_and_four_class() -> None:
    for seed in SEEDS:
        first = build_dataset(seed)
        second = build_dataset(seed)
        generated, canonical_train, canonical_evaluation, _ = first
        assert first == second
        assert len(canonical_train) == len(canonical_evaluation) == 64
        assert {item.label for item in canonical_train} == set(LABELS)
        assert {item.label for item in canonical_evaluation} == set(LABELS)
        assert not (
            {item.sequence_digest for item in generated.train}
            & {item.sequence_digest for item in generated.evaluation}
        )
        assert len({item.example_id for item in canonical_train}) == 64
        assert len({item.example_id for item in canonical_evaluation}) == 64


def test_d_intervention_preserves_multiset_timestamps_metadata_and_changes_assignment() -> None:
    _, canonical_train, _, transformed = build_dataset(0)
    changed = 0
    seed_stream = random.Random(330002)
    for original, actual in zip(canonical_train, transformed, strict=True):
        point_seed = seed_stream.getrandbits(32)
        coordinates = [(point.x, point.y) for point in original.points]
        random.Random(point_seed).shuffle(coordinates)
        assert actual.example_id == original.example_id
        assert actual.label == original.label
        assert len(actual.points) == len(original.points)
        assert [(point.x, point.y) for point in actual.points] == coordinates
        assert sorted((point.x, point.y) for point in actual.points) == sorted(
            (point.x, point.y) for point in original.points
        )
        assert [point.timestamp for point in actual.points] == [
            point.timestamp for point in original.points
        ]
        assert actual.metadata.duration == original.metadata.duration
        assert [
            (point.pen_state, point.stroke_boundary) for point in actual.points
        ] == [
            (point.pen_state, point.stroke_boundary) for point in original.points
        ]
        changed += sum(
            left != right
            for left, right in zip(
                [(point.x, point.y) for point in original.points],
                [(point.x, point.y) for point in actual.points],
                strict=True,
            )
        )
    assert changed > 0
    assert any(
        [(point.x, point.y) for point in original.points]
        != [(point.x, point.y) for point in actual.points]
        for original, actual in zip(canonical_train, transformed, strict=True)
    )


def test_all_conditions_share_frozen_config_except_declared_treatment() -> None:
    for seed in SEEDS:
        configs = {condition: build_config(seed, condition) for condition in CONDITIONS}
        for condition, config in configs.items():
            assert config.neuron_model == "EXCURSION_V1"
            assert config.structural_policy == "e2_local_temporal"
            assert config.topology_node_count == 8
            assert config.topology_initial_edges == 2
            assert config.topology_edge_capacity == 16
            assert config.topology_fan_in == config.topology_fan_out == 2
            assert config.structural_neighbors == RING_NEIGHBORS
            assert config.structural_neighborhood_limit == 2
            assert config.structural_reverse_observer_limit == 2
            assert config.structural_plasticity == (condition in ("C", "D"))
            assert config.structural_observation == (condition != "A")
        for condition in CONDITIONS[1:]:
            a_values = {
                field: getattr(configs["A"], field)
                for field in configs["A"].__dataclass_fields__
                if field not in {"structural_observation", "structural_plasticity"}
            }
            other_values = {
                field: getattr(configs[condition], field)
                for field in configs[condition].__dataclass_fields__
                if field not in {"structural_observation", "structural_plasticity"}
            }
            assert a_values == other_values


def test_public_initialization_matches_all_five_known_topologies_and_paired_conditions() -> None:
    observed = verify_topology_profile()
    for seed in SEEDS:
        expected = sorted(INITIAL_TOPOLOGIES[seed])
        for condition in CONDITIONS:
            assert observed[str(seed)][condition] == [list(edge) for edge in expected]


def test_heldout_evaluation_does_not_mutate_topology_or_prototypes() -> None:
    runner = ExperimentRunner(build_config(0, "C"))
    example = SyntheticExample(
        "nonmutation",
        (StrokePoint(0.2, 0.4, timestamp=0.0),),
        LABELS[0],
    )
    runner.train((example,))
    before_topology = tuple(
        sorted((edge.source, edge.destination, float(edge.propagation_delay)) for edge in runner.topology.edges)
    )
    before_prototypes = runner.prototypes
    runner.evaluate((example,))
    after_topology = tuple(
        sorted((edge.source, edge.destination, float(edge.propagation_delay)) for edge in runner.topology.edges)
    )
    assert after_topology == before_topology
    assert runner.prototypes == before_prototypes


def test_admitted_edges_come_only_from_grown_decision_snapshots() -> None:
    class Decision:
        def __init__(self, status, before, after, candidate_rank=1, candidate=None):
            self.status = status
            self.topology_before = before
            self.topology_after = after
            self.candidate_rank = candidate_rank
            self.selected_candidate = candidate
            self.reason = None

    candidate = type("Candidate", (), {"score": 2})()
    old = (("a", "b", 1.0),)
    grown = old + (("b", "c", 0.4),)
    admitted = _admitted_edges(
        (
            Decision("grown", old, grown, candidate=candidate),
            Decision("rejected_capacity", grown, grown, candidate=candidate),
        )
    )
    assert admitted == [
        {
            "source": "b",
            "destination": "c",
            "delay": 0.4,
            "decision_rank": 1,
            "score": 2,
            "status": "grown",
            "reason": None,
        }
    ]


def test_exact_excursion_route_use_requires_the_directed_edge_in_route_path() -> None:
    edges = [{"source": "a", "destination": "b"}]
    used_trace = ((1.0, "a", "b", "excursion", 0.5, 8, "evt", None, (), 1, ("a", "b"), False),)
    assert _route_uses(edges, used_trace)[0]["edge"] == ("a", "b")
    merely_present_trace = ((1.0, "a", "a", "excursion", 0.5, 8, "evt", None, (), 0, ("a",), False),)
    assert _route_uses(edges, merely_present_trace) == []
    wrong_direction_trace = ((1.0, "b", "a", "excursion", 0.5, 8, "evt", None, (), 1, ("b", "a"), False),)
    assert _route_uses(edges, wrong_direction_trace) == []
    non_excursion_trace = ((1.0, "a", "b", "signal", 0.5, 8, "evt", None, (), 1, ("a", "b"), False),)
    assert _route_uses(edges, non_excursion_trace) == []


def test_artifact_json_serialization_is_deterministic(tmp_path) -> None:
    first = {"b": [2, 1], "a": {"y": 1.25, "x": True}}
    second = {"a": {"x": True, "y": 1.25}, "b": [2, 1]}
    assert _canonical_json(first) == _canonical_json(second)
    assert json.loads(_canonical_json(first)) == first
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    _write_json(first_path, first)
    _write_json(second_path, second)
    assert first_path.read_bytes() == second_path.read_bytes()


def _summary_fixture(ca, cd, *, valid=True, noninterference=True, route=True):
    conditions = {}
    for seed in SEEDS:
        values = {
            "A": 0.5,
            "B": 0.5,
            "C": 0.5 + ca[seed],
            "D": 0.5 + ca[seed] - cd[seed],
        }
        conditions[str(seed)] = {}
        for condition in CONDITIONS:
            conditions[str(seed)][condition] = {
                "status": "completed",
                "valid_execution": valid,
                "training_classes_represented": True,
                "all_classes_represented": True,
                "evaluation_nonmutation_passed": True,
                "heldout": {
                    "predictions": [],
                    "event_trace_sha256": "empty",
                    "event_trace_count": 0,
                    "readout_diagnostics": [],
                    "metrics": {"accuracy": values[condition]},
                },
                "initial_topology": [],
                "topology_after_training": [],
                "training": {
                    "prototypes": [],
                    "before": {"predictions": [], "event_trace_sha256": "empty", "event_trace_count": 0, "readout_diagnostics": [], "metrics": {}},
                    "after": {"predictions": [], "event_trace_sha256": "empty", "event_trace_count": 0, "readout_diagnostics": [], "metrics": {}},
                    "history": [{}],
                },
                "structural": {"admitted_edges_later_used": ([{}] if route else [])},
            }
    if not noninterference:
        conditions["0"]["B"]["heldout"]["metrics"]["accuracy"] += 0.01
    return {"conditions": conditions}


def test_support_rule_distinguishes_nonpositive_means_and_failed_engagement() -> None:
    not_supported = _summary_results(_summary_fixture([0.0] * 5, [0.1] * 5))
    assert not_supported["scientific_efficacy_verdict"] == "NOT SUPPORTED IN THIS SETUP"
    inconclusive = _summary_results(_summary_fixture([0.1] * 5, [0.1] * 5, route=False))
    assert inconclusive["scientific_efficacy_verdict"] == "INCONCLUSIVE"
    supported = _summary_results(_summary_fixture([0.1] * 5, [0.1] * 5))
    assert supported["scientific_efficacy_verdict"] == "SUPPORTED ONLY IN THIS DECLARED SETUP"
    four_of_five = _summary_results(
        _summary_fixture([0.1, 0.1, 0.1, 0.1, 0.0], [0.1] * 5)
    )
    assert four_of_five["scientific_efficacy_verdict"] == "SUPPORTED ONLY IN THIS DECLARED SETUP"
    three_of_five = _summary_results(
        _summary_fixture([0.1, 0.1, 0.1, 0.0, 0.0], [0.1] * 5)
    )
    assert three_of_five["scientific_efficacy_verdict"] == "INCONCLUSIVE"
    failed_validity = _summary_results(
        _summary_fixture([0.1] * 5, [0.1] * 5, valid=False)
    )
    assert failed_validity["scientific_efficacy_verdict"] == "INCONCLUSIVE"


def test_noninterference_failure_blocks_scientific_interpretation() -> None:
    summary = _summary_results(
        _summary_fixture([0.1] * 5, [0.1] * 5, noninterference=False)
    )
    assert summary["scientific_efficacy_verdict"] == "BLOCKED — EXPERIMENT CONTRACT/RUNTIME DEFECT"


def test_execution_failure_retains_missing_arm_and_blocks_summary() -> None:
    data = _summary_fixture([0.1] * 5, [0.1] * 5)
    data["conditions"]["2"]["C"] = {"status": "failed", "error": {"type": "RuntimeError"}}
    summary = _summary_results(data)
    assert data["conditions"]["2"]["C"]["status"] == "failed"
    assert summary["scientific_efficacy_verdict"] == "BLOCKED — EXPERIMENT CONTRACT/RUNTIME DEFECT"
    assert summary["paired_c_minus_a"]["2"] is None


def test_no_pruning_or_n3_in_run_profile() -> None:
    config = build_config(0, "C")
    assert not hasattr(config, "pruning")
    assert not hasattr(config, "edge_parameter_learning")
    assert config.topology_edge_capacity == 16
