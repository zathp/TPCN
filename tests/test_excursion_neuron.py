import math
from dataclasses import replace

import pytest

from tpcn import (
    E1Config,
    E1EventBudgetExceeded,
    E1InternalEventKind,
    E1Mode,
    E1OutOfScopeBoundary,
    Edge,
    Event,
    EventQueue,
    EventType,
    SingleExcursionNeuron,
)
from tpcn.topology import BoundedTopology


def drain(neuron: SingleExcursionNeuron, queue: EventQueue[Event]) -> list:
    emissions = []
    while queue:
        event = queue.pop_ready(queue.peek().timestamp)
        emission = neuron.receive_event(event, queue)
        if emission is not None:
            emissions.append(emission)
    return emissions


def test_irregular_timestamps_use_local_decay_without_global_timestep() -> None:
    neuron = SingleExcursionNeuron("node")

    neuron.receive_contribution(0.0, 0.8)
    neuron.receive_contribution(0.25, 0.0)

    assert neuron.x == pytest.approx(0.8 * math.exp(-0.25))
    assert neuron.last_update_timestamp == pytest.approx(0.25)
    assert neuron.mode == E1Mode.N


def test_threshold_equality_admits_and_rearm_equality_returns_to_n() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)

    neuron.receive_contribution(0.0, 1.0, queue=queue)
    assert neuron.mode == E1Mode.S_PENDING
    assert neuron.pending_event is not None
    assert neuron.pending_event.kind == E1InternalEventKind.S_EMIT

    neuron.x = neuron.config.theta_r
    neuron.process_pending(queue=queue)

    assert neuron.mode == E1Mode.N
    assert neuron.pending_event is None


def test_rearm_strictly_above_threshold_does_not_use_tolerance() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    drain_until_internal(neuron, queue, 0.5)
    pending = neuron.pending_event
    assert pending is not None
    neuron.x = neuron.config.theta_r + 5e-13
    neuron.pending_internal_event = replace(pending, timestamp=neuron.last_update_timestamp, queue_sequence=-1)

    neuron.process_pending()

    assert neuron.mode == E1Mode.S_RETURN
    assert neuron.pending_event is not None


def test_close_contributions_compress_to_one_excursion() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)
    for timestamp in (0.0, 0.1, 0.2):
        neuron.receive_contribution(timestamp, 0.4, queue=queue)

    emissions = drain(neuron, queue)

    assert len(emissions) == 1
    assert neuron.input_contribution_count == 3
    assert len(emissions) < neuron.input_contribution_count
    assert emissions[0].timestamp == pytest.approx(0.7)


def test_widely_spaced_contributions_leak_without_admission() -> None:
    neuron = SingleExcursionNeuron("node")

    for timestamp in (0.0, 5.0, 10.0):
        neuron.receive_contribution(timestamp, 0.4)

    assert neuron.mode == E1Mode.N
    assert not neuron.emissions


def test_moderate_overshoot_has_at_most_one_ordinary_excursion() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)

    neuron.receive_contribution(0.0, 3.99, queue=queue)
    assert len(drain(neuron, queue)) == 1
    assert len(neuron.emissions) == 1


def test_admission_polarity_is_captured_before_opposite_input() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)

    neuron.receive_contribution(0.0, 1.0, queue=queue)
    neuron.receive_contribution(0.1, -0.2, queue=queue)
    emission = drain(neuron, queue)[0]

    assert emission.payload > 0.0
    assert neuron.emissions[0].lineage_id == emission.lineage_id


def test_negative_admission_mirrors_excursion_polarity() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)

    neuron.receive_contribution(0.0, -1.0, queue=queue)
    emission = drain(neuron, queue)[0]

    assert emission.payload == pytest.approx(-0.25)


@pytest.mark.parametrize(
    ("input_value", "expected"),
    ((1.0, 0.25), (2.5, 0.625), (3.99, 0.9975)),
)
def test_amplitude_map_is_exact_and_bounded(input_value: float, expected: float) -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)
    neuron.receive_contribution(0.0, input_value, queue=queue)

    assert drain(neuron, queue)[0].payload == pytest.approx(expected)


def test_external_event_precedes_equal_time_internal_emit() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    queue.push(Event(0.5, "external", "node", EventType.INPUT, 0.5, event_id="same-time"))

    first = queue.pop_ready(0.5)
    assert first.event_type == EventType.INPUT
    neuron.receive_event(first, queue)
    emission = neuron.receive_event(queue.pop_ready(0.5), queue)

    assert emission is not None
    assert emission.payload > 0.25
    assert neuron.m_peak > 1.0


def test_boundary_cancels_pending_event_and_stale_event_is_noop() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](16)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    stale = queue.peek()
    assert stale is not None

    neuron.receive_contribution(0.1, 3.5, queue=queue)

    assert neuron.out_of_scope is True
    assert neuron.boundary_reports
    assert neuron.pending_event is None
    assert neuron.receive_event(queue.pop_ready(0.5), queue) is None
    assert not neuron.emissions


def test_input_during_return_reschedules_finite_analytic_rearm() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](32)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    assert drain_until_internal(neuron, queue, 0.5)
    old_rearm = neuron.pending_event
    assert old_rearm is not None

    neuron.receive_contribution(0.75, 0.2, queue=queue)
    new_rearm = neuron.pending_event
    assert new_rearm is not None
    assert new_rearm.generation > old_rearm.generation
    assert new_rearm.timestamp == pytest.approx(
        0.75 + math.log(abs(neuron.x) / neuron.config.theta_r) / neuron.config.decay_rate
    )
    assert len(neuron.emissions) == 1
    drain(neuron, queue)
    assert len(neuron.emissions) == 1


def test_stale_rearm_is_a_noop_after_return_reschedule() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](32)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    assert drain_until_internal(neuron, queue, 0.5)
    old_rearm = neuron.pending_event
    assert old_rearm is not None

    neuron.receive_contribution(0.75, 0.2, queue=queue)
    assert neuron.pending_event is not None
    stale = queue.pop_ready(old_rearm.timestamp)

    assert neuron.receive_event(stale, queue) is None
    assert neuron.pending_event is not None
    assert len(neuron.emissions) == 1
    drain(neuron, queue)
    assert neuron.mode == E1Mode.N


def drain_until_internal(neuron: SingleExcursionNeuron, queue: EventQueue[Event], timestamp: float) -> bool:
    while queue and queue.peek().timestamp <= timestamp:
        event = queue.pop_ready(timestamp)
        neuron.receive_event(event, queue)
    return bool(neuron.emissions)


def test_event_and_lineage_identities_are_unique_across_episodes() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](64)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    first = drain(neuron, queue)[0]
    neuron.receive_contribution(first.timestamp + 2.0, 1.0, queue=queue)
    second = drain(neuron, queue)[0]

    assert first.event_id != second.event_id
    assert first.lineage_id != second.lineage_id
    assert first.episode_id != second.episode_id


def test_provenance_overflow_evicts_oldest_and_sets_truncation() -> None:
    config = E1Config(provenance_capacity=2)
    neuron = SingleExcursionNeuron("node", config=config)
    for index in range(3):
        neuron.receive_contribution(float(index), 0.1, event_id=f"input-{index}")

    assert len(neuron.provenance) == 2
    assert [entry.event_id for entry in neuron.provenance] == ["input-1", "input-2"]
    assert neuron.provenance_truncated is True


def test_replay_and_batched_delivery_are_deterministic() -> None:
    inputs = ((0.0, 0.4), (0.1, 0.4), (0.2, 0.4))

    def run(batched: bool) -> tuple:
        neuron = SingleExcursionNeuron("node")
        queue = EventQueue[Event](32)
        for timestamp, contribution in inputs:
            neuron.receive_contribution(timestamp, contribution, queue=queue)
        trace = []
        while queue:
            if batched:
                events = queue.pop_ready_batch(queue.peek().timestamp)
            else:
                events = [queue.pop_ready(queue.peek().timestamp)]
            for event in events:
                emission = neuron.receive_event(event, queue)
                if emission is not None:
                    trace.append((emission.event_id, emission.timestamp, emission.payload, emission.lineage_id))
        return tuple(trace), neuron.x, neuron.mode

    assert run(False) == run(True)
    assert run(False) == run(False)


def test_state_and_pending_event_remain_bounded_by_configuration() -> None:
    config = E1Config(event_budget=2)
    neuron = SingleExcursionNeuron("node", config=config)

    neuron.receive_contribution(0.0, 1.0)
    neuron.process_pending()
    with pytest.raises(E1EventBudgetExceeded):
        neuron.process_pending()

    assert abs(neuron.x) <= config.x_max
    assert neuron.processed_event_count <= config.event_budget


@pytest.mark.parametrize(
    "kwargs",
    (
        {"decay_rate": 0.0},
        {"decay_rate": -1.0},
        {"decay_rate": math.nan},
        {"decay_rate": math.inf},
        {"decay_rate": -math.inf},
        {"emission_delay": 0.0},
        {"emission_delay": -1.0},
        {"theta_r": 1.0, "theta_e": 1.0},
        {"theta_e": 2.0, "theta_hold": 1.0},
        {"theta_hold": 4.0, "theta_m": 4.0},
        {"theta_m": 9.0, "x_max": 8.0},
        {"provenance_capacity": 0},
        {"provenance_capacity": 65},
        {"event_budget": 0},
        {"decay_rate": True},
        {"provenance_capacity": True},
    ),
)
def test_e1_configuration_rejects_invalid_bounds(kwargs: dict) -> None:
    with pytest.raises((TypeError, ValueError)):
        E1Config(**kwargs)


def test_normal_analytic_rearms_terminate_without_micro_rearms() -> None:
    configs = (
        E1Config(),
        E1Config(decay_rate=0.1),
        E1Config(decay_rate=3.0, theta_r=0.125, theta_e=0.5, theta_hold=1.0, theta_m=2.0, x_max=4.0),
    )
    for index, config in enumerate(configs):
        neuron = SingleExcursionNeuron(f"node-{index}", config=config)
        queue = EventQueue[Event](64)
        neuron.receive_contribution(0.0, config.theta_e, queue=queue)
        emissions = drain(neuron, queue)

        assert len(emissions) == 1
        assert neuron.mode == E1Mode.N
        assert not queue


def test_provenance_isolated_between_completed_episodes() -> None:
    neuron = SingleExcursionNeuron("node", config=E1Config(provenance_capacity=2))
    queue = EventQueue[Event](64)
    for index, timestamp in enumerate((0.0, 0.1, 0.2)):
        neuron.receive_contribution(timestamp, 0.4, event_id=f"A-{index}", queue=queue)
    drain(neuron, queue)
    assert neuron.provenance_truncated is True

    neuron.receive_contribution(2.0, 0.4, event_id="B-0", queue=queue)
    neuron.receive_contribution(2.1, 0.7, event_id="B-1", queue=queue)

    assert neuron.mode == E1Mode.S_PENDING
    assert neuron.provenance_truncated is False
    assert [entry.event_id for entry in neuron.provenance] == ["B-0", "B-1"]
    assert len({entry.episode_id for entry in neuron.provenance}) == 1
    assert len({entry.lineage_id for entry in neuron.provenance}) == 1


def test_reset_cannot_revalidate_pre_reset_stale_internal_event() -> None:
    neuron = SingleExcursionNeuron("node")
    queue = EventQueue[Event](32)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    stale = queue.peek()
    assert stale is not None
    neuron.reset()
    neuron.receive_contribution(0.0, 1.0, queue=queue)

    assert neuron.receive_event(queue.pop_ready(0.5), queue) is None
    emissions = drain(neuron, queue)

    assert len(emissions) == 1
    assert emissions[0].episode_id == 2
    assert neuron.mode == E1Mode.N


def test_destination_local_equal_time_priority_preserves_unrelated_sequence_order() -> None:
    queue = EventQueue[Event](8)
    queue.push(Event(0.0, "node", "node", EventType.INTERNAL, "internal"))
    queue.push(Event(0.0, "control", "other", EventType.CONTROL, "control"))
    queue.push(Event(0.0, "source", "node", EventType.SIGNAL, "signal"))

    ordered = [event.payload for event in queue.pop_ready_batch(0.0)]

    assert ordered == ["control", "signal", "internal"]


def test_excursion_fanout_preserves_identity_and_applies_edge_specific_model_b() -> None:
    neuron = SingleExcursionNeuron("source")
    queue = EventQueue[Event](16)
    neuron.receive_contribution(0.0, 2.5, queue=queue)
    emission = drain(neuron, queue)[0]
    topology = BoundedTopology.from_edges(
        ("source", "left", "right"),
        (
            Edge("source", "left", 1.0, edge_weight=1.5, divider_strength=0.75, reference=0.2),
            Edge("source", "right", 2.0, edge_weight=-0.5, divider_strength=0.25, reference=-0.3),
        ),
        fan_in_limit=1,
        fan_out_limit=2,
    )
    routed_queue = EventQueue[Event](4)

    routed = topology.route(emission.as_event("left"), routed_queue)

    assert [event.event_id for event in routed] == [emission.event_id, emission.event_id]
    assert [event.lineage_id for event in routed] == [emission.lineage_id, emission.lineage_id]
    assert routed[0].sequence != routed[1].sequence
    assert routed[0].timestamp == pytest.approx(emission.timestamp + 1.0)
    assert routed[1].timestamp == pytest.approx(emission.timestamp + 2.0)
    assert routed[0].payload == pytest.approx(
        0.75 * math.tanh(1.5 * emission.payload) + 0.25 * 0.2
    )
    assert routed[1].payload == pytest.approx(
        0.25 * math.tanh(-0.5 * emission.payload) + 0.75 * -0.3
    )


def test_m_boundary_is_reported_without_executing_m_behavior() -> None:
    neuron = SingleExcursionNeuron("node")

    neuron.receive_contribution(0.0, 4.0)

    assert neuron.boundary_reports[-1].magnitude == pytest.approx(4.0)
    assert not neuron.emissions
    with pytest.raises(E1OutOfScopeBoundary):
        neuron.receive_contribution(1.0, 0.1)


@pytest.mark.parametrize("contribution", (math.nan, math.inf, -math.inf))
def test_nonfinite_external_contributions_are_rejected(contribution: float) -> None:
    neuron = SingleExcursionNeuron("node")

    with pytest.raises(ValueError):
        neuron.receive_contribution(0.0, contribution)


def test_excursion_payload_is_model_b_source_and_route_preserves_delay() -> None:
    neuron = SingleExcursionNeuron("source")
    queue = EventQueue[Event](16)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    emission = drain(neuron, queue)[0]
    routed_queue = EventQueue[Event](4)
    topology = BoundedTopology.from_edges(
        ("source", "destination"),
        (("source", "destination", 2.0),),
        fan_in_limit=1,
        fan_out_limit=1,
    )

    source_event = emission.as_event("destination")
    routed = topology.route(source_event, routed_queue)

    assert routed[0].timestamp == pytest.approx(emission.timestamp + 2.0)
    assert routed[0].payload == pytest.approx(math.tanh(emission.payload))
    assert routed[0].event_id == emission.event_id
    assert routed[0].lineage_id == emission.lineage_id
