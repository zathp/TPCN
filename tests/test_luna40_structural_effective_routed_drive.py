from __future__ import annotations

from dataclasses import asdict
from types import SimpleNamespace
from unittest import mock

import pytest

import run_luna39_acp0008_propagation_emission_diagnostic as luna39
import run_luna40_structural_effective_routed_drive as luna40
from tpcn.event_runtime import Event, EventQueue, EventType
from tpcn.excursion_neuron import E1Config, IntegrationConfig, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.structural_observation import StructuralObservationPlane
from tpcn.structural_plasticity import StructuralPlasticityController
from tpcn.topology import BoundedTopology


def _plane() -> StructuralObservationPlane:
    return StructuralObservationPlane(
        luna40.NODES,
        {"source": ("destination",), "relay": (), "destination": ()},
        neighborhood_limit=2,
        reverse_observer_limit=2,
        history_capacity=8,
        candidate_capacity=4,
        association_window=4.0,
        maximum_score=3,
        propagation_delay=0.4,
    )


def _actual_emission(node: str, *, input_time: float) -> dict[str, object]:
    neuron = MultiExcursionNeuron(node, config=E1Config(event_budget=4096))
    queue: EventQueue[Event] = EventQueue(capacity=8)
    neuron.receive_event(
        Event(input_time, node, node, EventType.INPUT, 1.2, event_id=f"{node}-input"),
        queue,
    )
    emissions = []
    while queue:
        next_event = queue.peek()
        assert next_event is not None
        emission = neuron.receive_event(queue.pop_ready(next_event.timestamp), queue)
        if emission is not None:
            emissions.append(emission)
    assert len(emissions) == 1
    emission = emissions[0]
    return {
        "emitter_id": emission.source,
        "event_id": emission.event_id,
        "timestamp": emission.timestamp,
        "payload": emission.payload,
    }


def _candidate_from_actual_emissions(*, destination_input_time: float = 1.0):
    plane = _plane()
    source_emission = _actual_emission("source", input_time=0.0)
    destination_emission = _actual_emission(
        "destination", input_time=destination_input_time
    )
    for emission in (source_emission, destination_emission):
        plane.observe_emission(
            str(emission["emitter_id"]),
            emission["event_id"],  # type: ignore[arg-type]
            float(emission["timestamp"]),
        )
    snapshot = plane.freeze()
    assert len(snapshot.candidates) == 1
    return snapshot.candidates[0], source_emission, destination_emission


def _one_node_integration_run(
    values: tuple[tuple[float, float], ...],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    node = "destination"
    neuron = MultiExcursionNeuron(
        node,
        config=E1Config(event_budget=4096, integration=IntegrationConfig()),
    )
    topology = BoundedTopology(
        (node,),
        fan_in_limit=1,
        fan_out_limit=1,
        edge_capacity=1,
        routing_capacity=1,
    )
    captured: dict[str, list[dict[str, object]]] = {}
    original_reset = MultiExcursionNeuron.reset

    def reset_with_snapshot(
        instance: MultiExcursionNeuron, *, timestamp: float = 0.0
    ) -> None:
        captured["trace"] = [asdict(entry) for entry in instance.integration_trace]
        captured["emissions"] = [asdict(item) for item in instance.emissions]
        original_reset(instance, timestamp=timestamp)

    runtime = ExcursionCharacterRuntime(
        (neuron,),
        topology,
        queue_capacity=128,
        event_budget=1024,
        settling_horizon=4.0,
        prediction_capacity=8,
        prediction_expiry=4.0,
        max_activity_events=1024,
        namespace="luna40-trace-test",
        eligibility_capacity=1024,
    )
    with mock.patch.object(MultiExcursionNeuron, "reset", reset_with_snapshot):
        runtime.start_character(
            "trace-case",
            0,
            timestamp=0.0,
            predictor_source=node,
            readout_sources=(node,),
            input_destination=node,
        )
        for timestamp, value in values:
            runtime.admit_external_batch(((timestamp, value),))
        result = runtime.end_character(
            last_external_timestamp=values[-1][0],
            reward=0.0,
            reward_delay=0.0,
            reward_message_id="neutral",
        )
    assert result.execution.completed
    emissions = []
    for item in captured["emissions"]:
        emissions.append(
            {
                "event_id": item["event_id"],
                "timestamp": item["timestamp"],
                "payload": item["payload"],
            }
        )
    return captured["trace"], emissions


def test_existing_public_runtime_composes_observation_growth_and_integration() -> None:
    points = luna39.base._training_point_sequences(0)[0]
    topology = luna40._initial_topology()
    controller = StructuralPlasticityController(
        topology,
        candidate_capacity=12,
        max_growth_per_adaptation=1,
        local_neighbors=luna40._neighbors_for("LOCAL_GROWTH_ENABLED"),
    )
    record, final_topology, attempts = luna40._run_character(
        arm="LOCAL_GROWTH_ENABLED",
        seed=0,
        sequence_index=0,
        points=points,
        topology=topology,
        controller=controller,
        attempts_so_far=0,
    )
    assert len(final_topology) == 2
    assert attempts == 0
    assert record["runtime"]["completed"] is True
    assert record["eligibility"]["effective_capacity_per_ledger"] == 1024
    assert len(record["eligibility"]["ledgers"]) == 3
    assert record["initial_topology_for_character"] == record["intermediate_topology_after_character"]


def test_equal_time_actual_canonical_emissions_do_not_form_candidate() -> None:
    result = luna40._equal_time_negative_control()
    assert result["used_actual_canonical_emissions"] is True
    assert result["same_timestamp"] is True
    assert result["observation_count"] > 0
    assert result["candidate_count"] == 0
    assert result["passed"] is True


def test_actual_ordered_emissions_form_candidate_and_controller_edge_defaults() -> None:
    candidate, source, destination = _candidate_from_actual_emissions()
    assert destination["timestamp"] > source["timestamp"]
    assert candidate.observer == candidate.source == "source"
    assert candidate.destination == "destination"
    assert candidate.score == 1
    assert candidate.propagation_delay == 0.4

    topology = luna40._initial_topology()
    controller = StructuralPlasticityController(
        topology,
        candidate_capacity=12,
        max_growth_per_adaptation=1,
        local_neighbors={"source": ("destination",)},
    )
    mutation = controller.grow(candidate)
    assert mutation.status == "grown"
    assert mutation.edge is not None
    assert mutation.edge.source == "source"
    assert mutation.edge.destination == "destination"
    assert mutation.edge.propagation_delay == 0.4
    assert mutation.edge.edge_weight == 1.0
    assert mutation.edge.divider_strength == 1.0
    assert mutation.edge.reference == 0.0
    assert len(controller.topology) == 3


@pytest.mark.parametrize(
    ("edge_capacity", "fan_in_limit", "expected_reason"),
    ((2, 2, "edge_capacity"), (3, 1, "fan_in_full")),
)
def test_controller_rejects_actual_evidence_at_declared_topology_bound(
    edge_capacity: int,
    fan_in_limit: int,
    expected_reason: str,
) -> None:
    candidate, _, _ = _candidate_from_actual_emissions()
    topology = BoundedTopology.from_edges(
        luna40.NODES,
        (("source", "relay", 1.0), ("relay", "destination", 1.0)),
        fan_in_limit=fan_in_limit,
        fan_out_limit=2,
        edge_capacity=edge_capacity,
        routing_capacity=3,
    )
    controller = StructuralPlasticityController(
        topology,
        candidate_capacity=12,
        max_growth_per_adaptation=1,
        local_neighbors={"source": ("destination",)},
    )
    before = luna40._topology_records(topology)
    mutation = controller.grow(candidate)
    assert mutation.status == "full_capacity"
    assert mutation.reason == expected_reason
    assert luna40._topology_records(controller.topology) == before


def test_observation_only_and_empty_neighborhood_controls_are_neural_noninterfering() -> None:
    points = luna39.base._training_point_sequences(0)[0]
    records = {}
    for arm in luna40.ARMS:
        topology = luna40._initial_topology()
        controller = (
            StructuralPlasticityController(
                topology,
                candidate_capacity=12,
                max_growth_per_adaptation=1,
                local_neighbors=luna40._neighbors_for(arm),
            )
            if arm == "LOCAL_GROWTH_ENABLED" else None
        )
        records[arm], _, _ = luna40._run_character(
            arm=arm,
            seed=0,
            sequence_index=0,
            points=points,
            topology=topology,
            controller=controller,
            attempts_so_far=0,
        )
    frozen = luna40._neural_projection(records["FROZEN_NO_OBSERVATION"])
    assert luna40._neural_projection(records["FROZEN_OBSERVATION_ONLY"]) == frozen
    assert luna40._neural_projection(records["NO_LOCAL_EVIDENCE_CONTROL"]) == frozen
    assert records["FROZEN_OBSERVATION_ONLY"]["structural"]["observation_count"] > 0
    assert records["NO_LOCAL_EVIDENCE_CONTROL"]["structural"]["candidates"] == []
    assert records["NO_LOCAL_EVIDENCE_CONTROL"]["growth"]["attempted"] is False


def test_destination_emission_classification_comes_from_integration_trace() -> None:
    integrated_trace, integrated_emissions = _one_node_integration_run(
        ((0.0, 0.4), (2.0, 0.4), (4.0, 0.4), (6.0, 0.4))
    )
    assert len(integrated_emissions) == 1
    integrated = luna40._destination_classification(
        integrated_emissions[0], integrated_trace
    )
    assert integrated["classification"] == "integrated_discharge"
    assert integrated["discharge_amount"] != 0.0
    assert abs(integrated["z_before_discharge"]) >= integrated["theta_Z"]

    direct_trace, direct_emissions = _one_node_integration_run(((0.0, 1.2),))
    assert len(direct_emissions) == 1
    direct = luna40._destination_classification(direct_emissions[0], direct_trace)
    assert direct["classification"] == "direct"
    assert direct["discharge_amount"] == 0.0


def test_label_isolation_generator_never_reads_label_metadata() -> None:
    points = luna39.base._training_point_sequences(0)[0]

    class Example:
        @property
        def points(self):
            return points

        @property
        def label(self):
            raise AssertionError("label metadata must not be read")

    def generator(**kwargs):
        assert kwargs["examples_per_class"] == 16
        assert kwargs["train_seed"] == 12007
        assert kwargs["evaluation_seed"] == 22017
        return SimpleNamespace(train=tuple(Example() for _ in range(64)))

    with mock.patch.object(luna39.base, "make_spiral_dataset", generator):
        sequences = luna39.base._training_point_sequences(0)
    assert len(sequences) == 64
    assert all(sequence == points for sequence in sequences)


def test_bounded_full_character_record_replays_deterministically() -> None:
    points = luna39.base._training_point_sequences(0)[0]
    records = []
    for _ in range(2):
        topology = luna40._initial_topology()
        plane_controller = StructuralPlasticityController(
            topology,
            candidate_capacity=12,
            max_growth_per_adaptation=1,
            local_neighbors=luna40._neighbors_for("LOCAL_GROWTH_ENABLED"),
        )
        record, _, _ = luna40._run_character(
            arm="LOCAL_GROWTH_ENABLED",
            seed=0,
            sequence_index=0,
            points=points,
            topology=topology,
            controller=plane_controller,
            attempts_so_far=0,
        )
        records.append(record)
    assert luna40._digest(records[0]) == luna40._digest(records[1])
    assert records[0]["runtime"]["events_processed"] <= 1024
    assert records[0]["runtime"]["queue_peak"] <= 128
    assert records[0]["structural"]["observation_work"] <= 1024 * 3
    assert records[0]["growth"]["attempt_budget_limit"] == 4


def test_all_arms_begin_from_identical_declared_static_topology() -> None:
    signatures = [
        luna40._topology_records(luna40._initial_topology())
        for _ in luna40.ARMS
    ]
    assert all(signature == signatures[0] for signature in signatures)
    assert [edge["identity"] for edge in signatures[0]] == [
        "source->relay",
        "relay->destination",
    ]
    assert all(
        edge["w"] == 1.0 and edge["d"] == 1.0 and edge["r"] == 0.0
        for edge in signatures[0]
    )


def test_experiment_digest_material_contains_causal_topology_and_z_evidence() -> None:
    points = luna39.base._training_point_sequences(0)[0]
    topology = luna40._initial_topology()
    record, _, _ = luna40._run_character(
        arm="FROZEN_OBSERVATION_ONLY",
        seed=0,
        sequence_index=0,
        points=points,
        topology=topology,
        controller=None,
        attempts_so_far=0,
    )
    assert record["initial_topology_for_character"]
    assert "routes" in record and "destination_integration_trace" in record
    assert "destination_emissions" in record and "effective_drive" in record
    assert record["input_digest"]
    assert len(luna40._digest(record)) == 64
