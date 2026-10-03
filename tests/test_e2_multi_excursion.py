from __future__ import annotations

import math
from dataclasses import replace

import pytest

from tpcn import (
    E1Config,
    E1EventBudgetExceeded,
    E1InternalEventKind,
    E1Mode,
    Event,
    EventQueue,
    EventType,
    Edge,
    MultiExcursionNeuron,
    PendingInternalEvent,
    BoundedTopology,
)


def make_neuron(
    *,
    state: float = 0.0,
    budget: int = 4096,
    capacity: int = 16,
    delta_x_e: float = 0.5,
    delay: float = 0.01,
    decay_rate: float = 0.001,
    initial_timestamp: float = 0.0,
) -> MultiExcursionNeuron:
    return MultiExcursionNeuron(
        "n",
        config=E1Config(
            decay_rate=decay_rate,
            emission_delay=0.01,
            m_emit_delay=delay,
            m_rearm_delay=delay,
            delta_x_e=delta_x_e,
            event_budget=budget,
            provenance_capacity=capacity,
        ),
        initial_state=state,
        initial_timestamp=initial_timestamp,
    )


def drain(neuron: MultiExcursionNeuron, queue: EventQueue[Event]) -> list:
    output = []
    while queue:
        next_event = queue.peek()
        assert next_event is not None
        event = queue.pop_ready(next_event.timestamp)
        emission = neuron.receive_event(event, queue)
        if emission is not None:
            output.append(emission)
    return output


def test_exact_m_threshold_admits_and_just_below_remains_ordinary() -> None:
    neuron = make_neuron()
    neuron.receive_contribution(0.0, neuron.config.theta_m)
    assert neuron.mode == E1Mode.M_ACTIVE
    assert neuron.m_phase is not None

    below = make_neuron()
    below.receive_contribution(0.0, math.nextafter(below.config.theta_m, 0.0))
    assert below.mode == E1Mode.S_PENDING
    assert below.multi_episode_id is None
    assert below.pending_event is not None
    assert below.pending_event.kind == E1InternalEventKind.S_EMIT


@pytest.mark.parametrize("initial", (4.0, -4.0, 6.0, -6.0, 8.0, -8.0))
def test_positive_and_negative_finite_return_bound(initial: float) -> None:
    neuron = make_neuron(delta_x_e=1.0, delay=0.01)
    queue: EventQueue[Event] = EventQueue(512)
    neuron.receive_contribution(0.0, initial, queue=queue)
    multi_id = neuron.multi_episode_id
    assert multi_id is not None
    m_emissions = [
        emission
        for emission in drain(neuron, queue)
        if emission.episode_id == multi_id
    ]
    bound = math.ceil((abs(initial) - neuron.config.theta_hold) / neuron.config.delta_x_e)
    assert len(m_emissions) <= bound
    assert all(emission.payload == math.copysign(neuron.config.a_max, initial) for emission in m_emissions)
    assert neuron.mode == E1Mode.N
    assert len({emission.event_id for emission in m_emissions}) == len(m_emissions)


@pytest.mark.parametrize("state", (-0.2500000000000003, 0.2500000000000003))
def test_analytic_rearm_rounding_uses_earliest_future_timestamp(state: float) -> None:
    clock = 45.27906122689938
    previous_timestamp = math.nextafter(clock, -math.inf)
    elapsed = clock - previous_timestamp

    def continue_return() -> tuple[MultiExcursionNeuron, list[float], float]:
        neuron = make_neuron(
            state=state * math.exp(elapsed),
            budget=8,
            decay_rate=1.0,
            initial_timestamp=previous_timestamp,
        )
        neuron.mode = E1Mode.S_RETURN
        neuron.ordinary_episode_id = 1
        neuron.lineage_id = 1
        neuron.generation_token = 1
        neuron.pending_internal_event = PendingInternalEvent(
            neuron.neuron_id,
            1,
            1,
            E1InternalEventKind.S_REARM,
            clock,
        )
        decayed_state = neuron._clip(neuron.x * math.exp(-neuron.config.decay_rate * elapsed))
        analytic_delay = neuron._rearm_delay(abs(decayed_state))
        assert math.isfinite(analytic_delay) and analytic_delay > 0.0
        assert clock + analytic_delay == clock

        queue: EventQueue[Event] = EventQueue(8)
        neuron.process_pending(queue=queue)
        assert neuron.clock.timestamp == clock
        assert neuron.x == state
        pending = neuron.pending_event
        queued = queue.peek()
        assert pending is not None and queued is not None
        assert pending.kind == E1InternalEventKind.S_REARM
        assert pending.timestamp == math.nextafter(clock, math.inf)
        assert math.isfinite(pending.timestamp) and pending.timestamp > clock
        assert queued.timestamp == pending.timestamp
        assert isinstance(queued.payload, PendingInternalEvent)
        assert queued.payload.timestamp == pending.timestamp

        event_times = [clock]
        while queue:
            next_event = queue.peek()
            assert next_event is not None
            event = queue.pop_ready(next_event.timestamp)
            event_times.append(event.timestamp)
            neuron.receive_event(event, queue)

        assert all(later > earlier for earlier, later in zip(event_times, event_times[1:]))
        assert len(event_times) <= neuron.config.event_budget
        assert neuron.processed_event_count <= neuron.config.event_budget
        assert neuron.mode == E1Mode.N
        assert neuron.pending_event is None
        return neuron, event_times, analytic_delay

    first, first_times, first_delay = continue_return()
    second, second_times, second_delay = continue_return()

    assert first_delay == second_delay
    assert first_times == second_times == [clock, math.nextafter(clock, math.inf)]
    assert first.mode == second.mode == E1Mode.N
    assert first.processed_event_count == second.processed_event_count == 2


def test_multiple_m_excursions_have_distinct_ids_and_strictly_positive_spacing() -> None:
    neuron = make_neuron(delta_x_e=0.5)
    queue: EventQueue[Event] = EventQueue(512)
    neuron.receive_contribution(0.0, 8.0, queue=queue)
    multi_id = neuron.multi_episode_id
    emissions = drain(neuron, queue)
    m_emissions = [item for item in emissions if item.episode_id == multi_id]

    assert len(m_emissions) > 1
    assert len({item.event_id for item in m_emissions}) == len(m_emissions)
    assert all(later.timestamp > earlier.timestamp for earlier, later in zip(m_emissions, m_emissions[1:]))
    assert all(item.payload == neuron.config.a_max for item in m_emissions)


def test_final_ordinary_episode_has_shared_counter_and_continuous_lineage() -> None:
    neuron = make_neuron(delta_x_e=4.0, capacity=2)
    queue: EventQueue[Event] = EventQueue(64)
    for index in range(4):
        neuron.receive_contribution(0.0, 1.0, event_id=f"source-{index}", queue=queue)
    multi_id = neuron.multi_episode_id
    lineage_id = neuron.lineage_id
    assert multi_id is not None and lineage_id is not None
    before_final_s = neuron.provenance
    assert [entry.event_id for entry in before_final_s] == ["source-2", "source-3"]
    assert neuron.provenance_truncated

    m_emission = None
    while queue:
        m_emission = neuron.receive_event(queue.pop_ready(0.01), queue)
        if m_emission is not None:
            break
    assert m_emission is not None
    assert m_emission.episode_id == multi_id
    assert m_emission.lineage_id == lineage_id
    assert neuron.mode == E1Mode.S_PENDING
    ordinary_id = neuron.ordinary_episode_id
    assert ordinary_id is not None and ordinary_id != multi_id
    assert neuron.lineage_id == lineage_id
    assert [(entry.event_id, entry.timestamp, entry.contribution) for entry in neuron.provenance] == [
        (entry.event_id, entry.timestamp, entry.contribution) for entry in before_final_s
    ]
    assert all(entry.episode_id == ordinary_id for entry in neuron.provenance)
    assert all(entry.lineage_id == lineage_id for entry in neuron.provenance)
    assert neuron.provenance_truncated

    remaining = drain(neuron, queue)
    ordinary_emissions = [item for item in remaining if item.episode_id == ordinary_id]
    assert len(ordinary_emissions) == 1
    assert ordinary_emissions[0].lineage_id == lineage_id
    assert neuron.mode == E1Mode.N


def test_direct_m_to_n_does_not_allocate_empty_ordinary_episode() -> None:
    neuron = make_neuron()
    neuron.receive_contribution(0.0, 4.0, event_id="old-lineage")
    assert neuron.multi_episode_id == 1
    neuron.receive_contribution(0.1, -3.5, event_id="cancel-lineage")

    assert neuron.mode == E1Mode.N
    assert neuron.ordinary_episode_id is None
    assert neuron.multi_episode_id is None
    assert neuron._episode_identity == 1
    assert neuron.provenance == ()
    assert not neuron.emissions

    neuron.receive_contribution(0.2, 4.0, event_id="new-lineage")
    assert neuron.mode == E1Mode.M_ACTIVE
    assert [entry.event_id for entry in neuron.provenance] == ["new-lineage"]


def test_provenance_capacity_boundary_sets_sticky_truncation() -> None:
    neuron = make_neuron(capacity=2)
    for index in range(2):
        neuron.receive_contribution(0.0, 0.1, event_id=f"input-{index}")
    assert not neuron.provenance_truncated
    assert [entry.event_id for entry in neuron.provenance] == ["input-0", "input-1"]

    neuron.receive_contribution(0.0, 0.1, event_id="input-2")

    assert neuron.provenance_truncated
    assert [entry.event_id for entry in neuron.provenance] == ["input-1", "input-2"]


def test_s_return_promotes_to_m_without_breaking_its_lineage() -> None:
    neuron = make_neuron()
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 1.0, queue=queue)
    while neuron.mode != E1Mode.S_RETURN:
        event = queue.pop_ready(queue.peek().timestamp)
        neuron.receive_event(event, queue)
    prior_lineage = neuron.lineage_id
    neuron.receive_contribution(0.02, 3.1, queue=queue)

    assert neuron.mode == E1Mode.M_ACTIVE
    assert neuron.multi_episode_id is not None
    assert neuron.ordinary_episode_id is None
    assert neuron.lineage_id == prior_lineage
    assert neuron.pending_event is not None
    assert neuron.pending_event.kind == E1InternalEventKind.M_EMIT


@pytest.mark.parametrize(
    ("state", "expected_mode", "expected_phase", "emits"),
    (
        (math.nextafter(1.0, 0.0), E1Mode.N, None, False),
        (1.0, E1Mode.S_PENDING, None, False),
        (math.nextafter(1.0, math.inf), E1Mode.S_PENDING, None, False),
        (1.5, E1Mode.S_PENDING, None, False),
        (math.nextafter(1.5, math.inf), E1Mode.S_PENDING, None, True),
    ),
)
def test_m_emit_threshold_boundaries(
    state: float,
    expected_mode: E1Mode,
    expected_phase: str | None,
    emits: bool,
) -> None:
    neuron = make_neuron()
    neuron.receive_contribution(0.0, 4.0)
    pending = neuron.pending_event
    assert pending is not None
    neuron.clock.advance_to(pending.timestamp)
    neuron.x = state

    emission = neuron.process_pending()

    assert (emission is not None) is emits
    assert neuron.mode == expected_mode
    assert (neuron.m_phase.value if neuron.m_phase is not None else None) == expected_phase


@pytest.mark.parametrize(
    ("state", "expected_mode", "expected_phase"),
    (
        (math.nextafter(1.0, 0.0), E1Mode.N, None),
        (1.0, E1Mode.S_PENDING, None),
        (math.nextafter(1.0, math.inf), E1Mode.S_PENDING, None),
        (1.5, E1Mode.S_PENDING, None),
        (math.nextafter(1.5, math.inf), E1Mode.M_ACTIVE, "ARMED"),
    ),
)
def test_m_rearm_threshold_boundaries(
    state: float,
    expected_mode: E1Mode,
    expected_phase: str | None,
) -> None:
    neuron = make_neuron(delta_x_e=0.5)
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 8.0, queue=queue)
    assert neuron.receive_event(queue.pop_ready(0.01), queue) is not None
    pending = neuron.pending_event
    assert pending is not None and pending.kind == E1InternalEventKind.M_REARM
    neuron.clock.advance_to(pending.timestamp)
    neuron.x = state

    assert neuron.process_pending(queue=queue) is None
    assert neuron.mode == expected_mode
    assert (neuron.m_phase.value if neuron.m_phase is not None else None) == expected_phase


def test_external_input_during_armed_phase_reverses_later_m_payload() -> None:
    neuron = make_neuron(delta_x_e=0.5)
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 5.0, queue=queue)
    original = neuron.pending_event
    assert original is not None and original.kind == E1InternalEventKind.M_EMIT
    before_magnitude = abs(neuron.x)
    neuron.receive_contribution(0.05, -8.0, queue=queue)
    assert neuron.mode == E1Mode.M_ACTIVE
    assert neuron.x < 0.0 and abs(neuron.x) < before_magnitude
    assert neuron.m_phase is not None and neuron.m_phase.value == "ARMED"
    assert neuron.pending_event is not None
    assert neuron.pending_event.generation > original.generation

    outputs = drain(neuron, queue)
    assert outputs
    assert outputs[0].payload < 0.0


def test_external_input_during_refractory_phase_can_reverse_later_m_payload() -> None:
    neuron = make_neuron(delta_x_e=0.5)
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 8.0, queue=queue)
    first = neuron.receive_event(queue.pop_ready(0.01), queue)
    assert first is not None
    assert neuron.m_phase is not None and neuron.m_phase.value == "REFRACTORY"
    original = neuron.pending_event
    assert original is not None and original.kind == E1InternalEventKind.M_REARM
    before_magnitude = abs(neuron.x)

    neuron.receive_contribution(0.02, -10.0, queue=queue)
    assert neuron.mode == E1Mode.M_ACTIVE
    assert neuron.x < 0.0 and abs(neuron.x) < before_magnitude
    assert neuron.pending_event is not None
    assert neuron.pending_event.kind == E1InternalEventKind.M_REARM
    assert neuron.pending_event.generation > original.generation
    later = [item for item in drain(neuron, queue) if item.episode_id == first.episode_id]
    assert later
    assert later[0].payload < 0.0


def test_external_arrival_at_m_emit_timestamp_precedes_and_cancels_it() -> None:
    neuron = make_neuron()
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 4.0, queue=queue)
    queue.push(Event(0.01, "external", "n", EventType.INPUT, -4.0, event_id="cancel"))

    first = queue.pop_ready(0.01)
    assert first.event_type == EventType.INPUT
    neuron.receive_event(first, queue)
    assert neuron.mode == E1Mode.N
    assert neuron.receive_event(queue.pop_ready(0.01), queue) is None
    assert not neuron.emissions


def test_external_arrival_at_m_rearm_timestamp_precedes_and_cancels_it() -> None:
    neuron = make_neuron(delta_x_e=0.5)
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 8.0, queue=queue)
    first = neuron.receive_event(queue.pop_ready(0.01), queue)
    assert first is not None
    due = neuron.pending_event
    assert due is not None and due.kind == E1InternalEventKind.M_REARM
    queue.push(Event(due.timestamp, "external", "n", EventType.INPUT, -8.0, event_id="cancel"))

    external = queue.pop_ready(due.timestamp)
    assert external.event_type == EventType.INPUT
    neuron.receive_event(external, queue)
    assert neuron.mode == E1Mode.N
    assert neuron.receive_event(queue.pop_ready(due.timestamp), queue) is None
    assert len(neuron.emissions) == 1
    assert neuron.emissions[0] == first


@pytest.mark.parametrize(
    "mutation", ("generation", "episode", "kind", "timestamp", "sequence", "source")
)
def test_m_pending_event_rejects_mismatched_validity_tuple(mutation: str) -> None:
    neuron = make_neuron()
    queue: EventQueue[Event] = EventQueue(16)
    neuron.receive_contribution(0.0, 4.0, queue=queue)
    queued = queue.peek()
    assert queued is not None and isinstance(queued.payload, object)
    original = queued.payload
    assert hasattr(original, "generation")
    if mutation == "generation":
        payload = replace(original, generation=original.generation + 1)
        event = replace(queued, payload=payload)
    elif mutation == "episode":
        payload = replace(original, episode_id=original.episode_id + 1)
        event = replace(queued, payload=payload)
    elif mutation == "kind":
        payload = replace(original, kind=E1InternalEventKind.M_REARM)
        event = replace(queued, payload=payload)
    elif mutation == "timestamp":
        event = replace(queued, timestamp=queued.timestamp + 0.001)
    elif mutation == "source":
        event = replace(queued, source="other")
    else:
        event = replace(queued, sequence=queued.sequence + 1)

    before = (neuron.x, neuron.mode, neuron.pending_event, tuple(neuron.emissions))
    assert neuron.receive_event(event, queue) is None
    assert (neuron.x, neuron.mode, neuron.pending_event, tuple(neuron.emissions)) == before


def test_duplicate_m_internal_delivery_is_a_noop() -> None:
    neuron = make_neuron()
    queue: EventQueue[Event] = EventQueue(16)
    neuron.receive_contribution(0.0, 4.0, queue=queue)
    event = queue.pop_ready(0.01)
    emission = neuron.receive_event(event, queue)
    assert emission is not None
    snapshot = (neuron.x, neuron.pending_event, tuple(neuron.emissions))

    assert neuron.receive_event(event, queue) is None
    assert (neuron.x, neuron.pending_event, tuple(neuron.emissions)) == snapshot


@pytest.mark.parametrize("phase", ("ARMED", "REFRACTORY"))
def test_reset_during_m_clears_state_and_retains_identity_high_water(phase: str) -> None:
    neuron = make_neuron(delta_x_e=0.5)
    queue: EventQueue[Event] = EventQueue(64)
    neuron.receive_contribution(0.0, 8.0, queue=queue)
    if phase == "REFRACTORY":
        assert neuron.receive_event(queue.pop_ready(0.01), queue) is not None
    stale = neuron.pending_event
    assert isinstance(stale, PendingInternalEvent)
    stale_event = Event(
        stale.timestamp,
        "n",
        "n",
        EventType.INTERNAL,
        stale,
        sequence=stale.queue_sequence,
    )
    high_water = (
        neuron._event_identity,
        neuron._episode_identity,
        neuron._lineage_identity,
        neuron._input_identity,
    )

    neuron.reset(timestamp=2.0)
    assert neuron.mode == E1Mode.N
    assert neuron.x == 0.0
    assert neuron.m_phase is None
    assert neuron.multi_episode_id is None
    assert neuron.pending_event is None
    assert neuron.provenance == ()
    assert not neuron.emissions
    assert neuron.receive_event(stale_event, queue) is None
    assert (
        neuron._event_identity,
        neuron._episode_identity,
        neuron._lineage_identity,
        neuron._input_identity,
    ) == high_water

    neuron.receive_contribution(2.0, 4.0, queue=queue)
    assert neuron.multi_episode_id is not None
    assert neuron.multi_episode_id > 1
    assert neuron.lineage_id is not None and neuron.lineage_id > 1
    assert neuron.provenance[-1].event_id.endswith(":input:1")
    next_output = drain(neuron, queue)[0]
    assert next_output.sequence > high_water[0]


def test_smallest_terminating_event_budget_is_explicit_and_bounded() -> None:
    neuron = make_neuron(budget=4, delta_x_e=4.0, delay=0.001)
    queue: EventQueue[Event] = EventQueue(16)
    neuron.receive_contribution(0.0, 4.0, queue=queue)
    drain(neuron, queue)
    assert neuron.processed_event_count == 4
    assert neuron.mode == E1Mode.N
    assert len(queue) == 0

    exhausted = make_neuron(budget=3, delta_x_e=4.0, delay=0.001)
    exhausted_queue: EventQueue[Event] = EventQueue(16)
    exhausted.receive_contribution(0.0, 4.0, queue=exhausted_queue)
    with pytest.raises(E1EventBudgetExceeded):
        drain(exhausted, exhausted_queue)
    assert exhausted.processed_event_count == 3


def test_positive_configured_delay_that_cannot_advance_float_time_is_rejected() -> None:
    config = E1Config(
        m_emit_delay=math.nextafter(0.0, 1.0),
        m_rearm_delay=0.01,
    )
    neuron = MultiExcursionNeuron(
        "n",
        config=config,
        initial_timestamp=1e308,
    )

    with pytest.raises(ValueError, match="positive logical delay"):
        neuron.receive_contribution(1e308, 4.0)


def test_m_configuration_rejects_discharge_beyond_state_bound() -> None:
    with pytest.raises(ValueError, match="delta_x_e"):
        E1Config(x_max=8.0, delta_x_e=8.1)


def test_identity_high_water_is_bounded_across_repeated_resets() -> None:
    neuron = make_neuron(budget=2)
    neuron.receive_contribution(0.0, 4.0)
    neuron.reset(timestamp=1.0)
    neuron.receive_contribution(1.0, 4.0)
    assert neuron._episode_identity == 2
    assert neuron._lineage_identity == 2
    assert neuron._input_identity == 2

    neuron.reset(timestamp=2.0)
    with pytest.raises(E1EventBudgetExceeded, match="input identity budget"):
        neuron.receive_contribution(2.0, 4.0)
    assert neuron._episode_identity == 2
    assert neuron._lineage_identity == 2
    assert neuron._input_identity == 2


def test_nondefault_model_b_fanout_from_m_excursion() -> None:
    neuron = make_neuron(delta_x_e=4.0)
    queue: EventQueue[Event] = EventQueue(16)
    neuron.receive_contribution(0.0, 4.0, queue=queue)
    emission = neuron.receive_event(queue.pop_ready(0.01), queue)
    assert emission is not None
    topology = BoundedTopology.from_edges(
        ("n", "left", "right"),
        (
            Edge("n", "left", 0.2, edge_weight=1.4, divider_strength=0.7, reference=0.1),
            Edge("n", "right", 0.4, edge_weight=-0.6, divider_strength=0.3, reference=-0.2),
        ),
        fan_in_limit=1,
        fan_out_limit=2,
    )
    routed = topology.route(emission.as_event("left"), EventQueue(4))

    assert [item.payload for item in routed] == pytest.approx(
        [
            0.7 * math.tanh(1.4 * emission.payload) + 0.3 * 0.1,
            0.3 * math.tanh(-0.6 * emission.payload) + 0.7 * -0.2,
        ]
    )
    assert all(item.event_id == emission.event_id for item in routed)
