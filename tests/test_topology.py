import math
from pathlib import Path

import pytest

from tpcn.event_runtime import Event, EventQueue, EventType, QueueCapacityError
from tpcn.topology import BoundedTopology, TopologyCapacityError, TopologyError


def make_topology() -> BoundedTopology:
    return BoundedTopology(("a", "b", "c", "d"), fan_in_limit=1, fan_out_limit=2, edge_capacity=3)


def test_fan_in_and_fan_out_are_rejected_at_connection_time() -> None:
    topology = make_topology()
    topology.connect("a", "b", 1.0)
    with pytest.raises(TopologyCapacityError):
        topology.connect("c", "b", 1.0)
    topology.connect("a", "c", 2.0)
    with pytest.raises(TopologyCapacityError):
        topology.connect("a", "d", 3.0)


def test_invalid_nodes_edges_and_delays_are_rejected() -> None:
    topology = make_topology()
    with pytest.raises(TopologyError):
        topology.connect("missing", "b", 1.0)
    with pytest.raises(TopologyError):
        topology.connect("a", "missing", 1.0)
    with pytest.raises(ValueError):
        topology.connect("a", "b", 0.0)
    topology.connect("a", "b", 1.0)
    with pytest.raises(TopologyError):
        topology.connect("a", "b", 2.0)


def test_route_preserves_edge_delay_and_uses_luna_one_queue() -> None:
    topology = make_topology()
    topology.connect("a", "b", 1.25)
    queue = EventQueue(capacity=4)
    emitted = Event(3.0, "a", "ignored", EventType.SIGNAL, 0.5)
    queued = topology.route(emitted, queue)

    assert queued[0].destination == "b"
    assert queued[0].timestamp == pytest.approx(4.25)
    with pytest.raises(IndexError):
        queue.pop_ready(4.24)
    assert queue.pop_ready(4.25).payload == pytest.approx(math.tanh(0.5))


def test_successful_route_admits_complete_fan_out() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (("a", "b", 1.0), ("a", "c", 2.0)), fan_in_limit=2, fan_out_limit=2
    )
    queue = EventQueue(capacity=2)

    queued = topology.route(Event(0.0, "a", "ignored", EventType.SIGNAL, 0.5), queue)

    assert [event.destination for event in queued] == ["b", "c"]
    assert len(queue) == 2


def test_route_excludes_only_visited_destinations_before_atomic_admission() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c", "d"),
        (("a", "b", 1.0), ("a", "c", 2.0), ("a", "d", 3.0)),
        fan_in_limit=2,
        fan_out_limit=3,
    )
    queue = EventQueue(capacity=3)
    event = Event(0.0, "a", "ignored", EventType.CONTROL, {"opaque": True}, event_id="e", lineage_id="l")

    class RecordingObserver:
        def __init__(self) -> None:
            self.edges = []

        def record_route(self, edge, original, routed) -> None:
            self.edges.append((edge, original, routed))

    observed = RecordingObserver()

    queued = topology.route(event, queue, exclude_destinations=("b",), observer=observed)

    assert [item.destination for item in queued] == ["c", "d"]
    assert [item.sequence for item in queued] == [0, 1]
    assert [edge.destination for edge, _, _ in observed.edges] == ["c", "d"]
    assert all(item.payload is event.payload for item in queued)
    assert [(item.event_id, item.lineage_id) for item in queued] == [("e", "l"), ("e", "l")]

    next_event = topology.route(
        Event(1.0, "a", "ignored", EventType.CONTROL, None),
        queue,
        exclude_destinations=("b", "c", "d"),
    )
    assert next_event == ()
    assert len(queue) == 2

    excluded_queue = EventQueue(capacity=3)
    assert topology.route(
        Event(0.0, "a", "ignored", EventType.CONTROL, None),
        excluded_queue,
        exclude_destinations=("b", "c", "d"),
    ) == ()
    legal = topology.route(Event(0.0, "a", "ignored", EventType.CONTROL, None), excluded_queue)
    assert legal[0].sequence == 0


def test_excluded_destination_does_not_consume_sequence_or_break_capacity_atomicity() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c", "d"),
        (("a", "b", 1.0), ("a", "c", 2.0), ("a", "d", 3.0)),
        fan_in_limit=2,
        fan_out_limit=3,
    )
    queue = EventQueue(capacity=2)
    event = Event(0.0, "a", "ignored", EventType.CONTROL, None)

    queued = topology.route(event, queue, exclude_destinations=("b",))
    assert [item.destination for item in queued] == ["c", "d"]
    assert [item.sequence for item in queued] == [0, 1]

    full_queue = EventQueue(capacity=2)
    existing = full_queue.push(Event(0.0, "existing", "a", EventType.CONTROL, None))
    before_sequence = full_queue._next_sequence
    with pytest.raises(QueueCapacityError, match="complete fan-out"):
        topology.route(event, full_queue, exclude_destinations=("b",))
    assert len(full_queue) == 1
    assert full_queue.peek() == existing
    assert full_queue._next_sequence == before_sequence


def test_rejected_fan_out_is_atomic_and_retryable_without_duplicates() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (("a", "b", 1.0), ("a", "c", 2.0)), fan_in_limit=2, fan_out_limit=2
    )
    queue = EventQueue(capacity=2)
    existing = Event(0.0, "existing", "b", EventType.SIGNAL, None)
    queue.push(existing)
    event = Event(0.0, "a", "ignored", EventType.SIGNAL, 0.5)

    with pytest.raises(QueueCapacityError):
        topology.route(event, queue)
    with pytest.raises(QueueCapacityError):
        topology.route(event, queue)

    assert len(queue) == 1
    assert queue.peek() is not None
    assert queue.peek().destination == "b"

    assert queue.pop_ready(0.0).source == "existing"
    queued = topology.route(event, queue)
    assert [item.destination for item in queued] == ["b", "c"]
    assert [item.destination for item in queue.drain()] == ["b", "c"]


def test_seeded_construction_is_deterministic_and_finite() -> None:
    kwargs = dict(edge_count=4, fan_in_limit=2, fan_out_limit=2, seed=17, propagation_delay=0.5)
    first = BoundedTopology.seeded(("n3", "n1", "n2", "n0"), **kwargs)
    second = BoundedTopology.seeded(("n3", "n1", "n2", "n0"), **kwargs)

    assert first.edges == second.edges
    assert len(first) == 4
    assert len(first.nodes) == 4


def test_route_is_compatible_with_serial_and_batched_queue_processing() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (("a", "b", 1.0), ("a", "c", 2.0)), fan_in_limit=2, fan_out_limit=2
    )

    def run(batch: bool) -> list[tuple[str, float]]:
        queue = EventQueue(capacity=8)
        topology.route(Event(0.0, "a", "ignored", EventType.SIGNAL, 0.5), queue)
        result = []
        while queue:
            ready = queue.pop_ready_batch(queue.peek().timestamp) if batch else [queue.pop_ready(queue.peek().timestamp)]
            result.extend((event.destination, event.timestamp) for event in ready)
        return result

    assert run(False) == run(True)


def test_routing_respects_finite_pending_queue_capacity() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (("a", "b", 1.0), ("a", "c", 2.0)), fan_in_limit=2, fan_out_limit=2
    )
    queue = EventQueue(capacity=1)

    with pytest.raises(QueueCapacityError):
        topology.route(Event(0.0, "a", "ignored", EventType.SIGNAL, 0.5), queue)
    assert len(queue) == 0


def test_topology_has_no_spatial_reservoir_dependency() -> None:
    source = Path(__file__).parents[1] / "tpcn" / "topology.py"
    text = source.read_text(encoding="utf-8")
    assert "signal_copy_distance" not in text
    assert "spatial" not in text.lower()