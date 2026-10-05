from __future__ import annotations

from types import SimpleNamespace

import pytest

import run_luna34_excursion_v1_multi_emitter_bridge as luna34
from tpcn.event_runtime import EventType
from tpcn.stroke_dataset import StrokePoint
from tpcn.structural_observation import StructuralObservationPlane


def _plane(
    neighbors: dict[str, tuple[str, ...]] | None = None,
    *,
    nodes: tuple[str, ...] = ("source", "destination"),
    association_window: float = 4.0,
) -> StructuralObservationPlane:
    if neighbors is None:
        neighbors = {"source": ("destination",), "destination": ()}
    return StructuralObservationPlane(
        nodes,
        neighbors,
        neighborhood_limit=1,
        reverse_observer_limit=1,
        history_capacity=8,
        candidate_capacity=4,
        association_window=association_window,
        maximum_score=3,
        propagation_delay=0.4,
    )


def _one_point() -> tuple[StrokePoint, ...]:
    return (StrokePoint(0.6, 0.6, timestamp=0.0),)


def test_conditions_construct_only_the_predeclared_fixed_model_b_topologies() -> None:
    no_edge = luna34._topology("NO_EDGE_CONTROL")
    default = luna34._topology("DEFAULT_STATIC_EDGE")
    sensitivity = luna34._topology("STATIC_N2_BOUND_SENSITIVITY")

    assert no_edge.nodes == default.nodes == sensitivity.nodes == ("source", "destination")
    assert [len(item) for item in (no_edge, default, sensitivity)] == [0, 1, 1]
    assert (default.edges[0].edge_weight, default.edges[0].divider_strength, default.edges[0].reference) == (
        1.0,
        1.0,
        0.0,
    )
    assert (
        sensitivity.edges[0].edge_weight,
        sensitivity.edges[0].divider_strength,
        sensitivity.edges[0].reference,
    ) == (2.0, 1.0, 0.0)
    assert all(edge.propagation_delay == 1.0 for edge in (*default.edges, *sensitivity.edges))
    assert all(item.edge_capacity == item.routing_capacity == 1 for item in (no_edge, default, sensitivity))


def test_runtime_trace_reconciles_source_emission_transfer_and_destination_replay() -> None:
    record = luna34._character_record(
        seed=0,
        sequence_index=0,
        condition="DEFAULT_STATIC_EDGE",
        points=_one_point(),
    )
    source_emissions = [
        item for item in record["canonical_emissions"] if item["emitter_id"] == "source"
    ]
    routes = record["routed_contributions"]

    assert source_emissions
    assert len(routes) == len(source_emissions)
    assert all(
        route["emission_event_id"] == emission["event_id"]
        and route["emission_timestamp"] == emission["timestamp"]
        and route["arrival_timestamp"] - route["emission_timestamp"] == 1.0
        and route["destination"] == "destination"
        and route["route_depth"] == 1
        for route, emission in zip(routes, source_emissions, strict=True)
    )
    assert all(
        route["transformed_payload"]
        == pytest.approx(__import__("math").tanh(emission["payload"]), abs=1e-12)
        for route, emission in zip(routes, source_emissions, strict=True)
    )
    assert all(
        route["destination_state_after"]
        == pytest.approx(
            route["destination_state_before"] + route["transformed_payload"],
            abs=1e-12,
        )
        for route in routes
    )
    assert record["execution"]["completed"]
    assert record["execution"]["pending_event_count"] == 0
    assert record["destination_state_replay"]["replayed_emissions"] == [
        {
            key: item[key]
            for key in ("event_id", "emitter_id", "timestamp", "payload")
        }
        for item in record["canonical_emissions"]
        if item["emitter_id"] == "destination"
    ]


def test_observation_recipients_do_not_inflate_distinct_emitter_count() -> None:
    plane = _plane()
    plane.observe_emission("source", "source:event-1", 0.0)
    plane.observe_emission("destination", "destination:event-1", 0.5)
    snapshot = plane.freeze()

    distinct = {
        (observation.emitter_id, observation.event_id)
        for observation in snapshot.observations
    }
    assert snapshot.observation_count == 2
    assert len(snapshot.observations) == 3
    assert len(distinct) == 2
    assert len(snapshot.candidates) == 1


def test_candidate_requires_local_source_first_positive_interval_within_window() -> None:
    valid = _plane()
    valid.observe_emission("source", "s-1", 1.0)
    valid.observe_emission("destination", "d-1", 5.0)
    assert len(valid.freeze().candidates) == 1

    for first, second in (
        (("source", "s", 1.0), ("destination", "d", 1.0)),
        (("destination", "d", 0.5), ("source", "s", 1.0)),
        (("source", "s", 0.0), ("destination", "d", 4.0001)),
    ):
        plane = _plane()
        plane.observe_emission(*first)
        plane.observe_emission(*second)
        assert plane.freeze().candidates == ()

    nonlocal_plane = _plane(
        {"source": ("destination",), "destination": (), "other": ()},
        nodes=("source", "destination", "other"),
    )
    nonlocal_plane.observe_emission("source", "s-2", 0.0)
    nonlocal_plane.observe_emission("other", "o-2", 0.5)
    assert nonlocal_plane.freeze().candidates == ()


def test_character_local_evidence_is_fresh_for_each_character() -> None:
    first_character = _plane()
    first_character.observe_emission("source", "s-1", 0.0)
    first_character.observe_emission("destination", "d-1", 0.5)
    assert len(first_character.freeze().candidates) == 1

    second_character = _plane()
    second_character.observe_emission("destination", "d-2", 0.75)
    assert second_character.freeze().candidates == ()


def test_generated_training_stream_reads_only_points_and_uses_declared_order(monkeypatch) -> None:
    points = _one_point()

    class PointOnlyExample:
        def __init__(self) -> None:
            self.points = points

        @property
        def label(self):
            raise AssertionError("labels must not be read")

        @property
        def metadata(self):
            raise AssertionError("label-bearing metadata must not be read")

    calls = []

    def fake_dataset(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(train=tuple(PointOnlyExample() for _ in range(64)))

    monkeypatch.setattr(luna34, "make_spiral_dataset", fake_dataset)
    first = luna34._training_point_sequences(3)
    second = luna34._training_point_sequences(3)

    assert calls == [
        {
            "examples_per_class": 16,
            "train_seed": 12010,
            "evaluation_seed": 22020,
            "config": luna34.SpiralConfig(),
        }
    ] * 2
    assert len(first) == 64
    assert first == second
    assert all(sequence == points for sequence in first)


def test_same_timestamp_points_are_batched_without_reordering() -> None:
    points = luna34._input_points(
        (
            StrokePoint(0.1, 0.2, timestamp=0.0),
            StrokePoint(0.3, 0.4, timestamp=0.0),
            StrokePoint(0.5, 0.6, timestamp=1.0),
        )
    )

    assert luna34._point_batches(points) == (
        ((0.0, 0.30000000000000004), (0.0, 0.7)),
        ((1.0, 1.1),),
    )


def test_no_edge_is_a_completed_negative_control() -> None:
    record = luna34._character_record(
        seed=0,
        sequence_index=1,
        condition="NO_EDGE_CONTROL",
        points=_one_point(),
    )

    assert record["execution"]["completed"]
    assert record["execution"]["receiving_neuron_count"] == 1
    assert record["execution"]["max_route_depth"] == 0
    assert record["routed_contributions"] == []
    assert not any(
        item["emitter_id"] == "destination"
        for item in record["canonical_emissions"]
    )
    assert record["structural_observation"]["legal_candidate_count"] == 0


def test_character_record_and_serialized_digest_are_deterministic() -> None:
    first = luna34._character_record(
        seed=2,
        sequence_index=7,
        condition="STATIC_N2_BOUND_SENSITIVITY",
        points=_one_point(),
    )
    second = luna34._character_record(
        seed=2,
        sequence_index=7,
        condition="STATIC_N2_BOUND_SENSITIVITY",
        points=_one_point(),
    )

    assert first == second
    assert luna34._canonical_json(first) == luna34._canonical_json(second)
    assert first["replay_digest"] == second["replay_digest"]
    assert all(
        trace["event_id"] is not None
        for trace in first["canonical_emissions"]
    )
