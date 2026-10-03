"""Character-scoped CPU adapter for the accepted E2 excursion integration."""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from typing import Callable, Iterable

from .eligibility import (
    ELIGIBILITY_ACTIVITY_EVENT,
    EligibilityActivity,
    EligibilityLedger,
    RewardSignal,
)
from .energy_utility import LocalEnergyModel, RewardAdjustedUtility, RewardMessage
from .event_runtime import (
    BoundedExecutionResult,
    Event,
    EventQueue,
    EventType,
)
from .excursion_neuron import ExcursionEmission, MultiExcursionNeuron
from .ir2 import (
    EXCURSION_V1,
    IR2Mode,
    IR2UnsupportedRuntimeError,
    TPCNIR2,
    neuron_from_ir2_e2,
)
from .predictive_coding import (
    PREDICTION_ERROR_EVENT,
    LocalPredictor,
    Observation,
    PredictionError,
)
from .streaming_classifier import (
    ACTIVITY_EVENT,
    ClassificationResult,
    StreamingCharacterClassifier,
)
from .stroke_dataset import CharacterBoundary, END_CHARACTER, START_CHARACTER
from .topology import BoundedTopology, Edge


@dataclass(frozen=True, slots=True)
class RouteContext:
    causal_roots: tuple[str, ...]
    route_depth: int
    route_path: tuple[str, ...]
    roots_truncated: bool = False


@dataclass(frozen=True, slots=True)
class ExcursionCharacterResult:
    trace: tuple[tuple[object, ...], ...]
    classifier_result: ClassificationResult
    feature: float
    emission_count: int
    silent_event_count: int
    prediction_loss: float
    matched_predictions: int
    unmatched_predictions: int
    expired_predictions: int
    matched_credit: int
    unmatched_credit: int
    peak_queue_occupancy: int
    pending_event_count: int
    beyond_deadline_event_count: int
    incomplete_settling: bool
    execution: BoundedExecutionResult
    energy: float
    energy_components: tuple[tuple[str, float], ...]
    max_route_depth: int
    provenance_truncated: bool
    reward_attribution: str
    reward: float
    reward_update_latency: float
    utility: float
    active_neuron_count: int
    receiving_neuron_count: int
    emitting_neuron_count: int


class ExcursionCharacterRuntime:
    """One bounded queue and sidecar for one character's entire lifetime."""

    def __init__(
        self,
        neurons: Iterable[MultiExcursionNeuron],
        topology: BoundedTopology,
        *,
        queue_capacity: int,
        event_budget: int,
        settling_horizon: float,
        prediction_capacity: int,
        prediction_expiry: float,
        max_activity_events: int,
        namespace: str,
    ) -> None:
        self.neurons = tuple(neurons)
        if not self.neurons or any(not isinstance(n, MultiExcursionNeuron) for n in self.neurons):
            raise TypeError("neurons must be a non-empty collection of MultiExcursionNeuron instances")
        self.by_id = {neuron.neuron_id: neuron for neuron in self.neurons}
        if len(self.by_id) != len(self.neurons):
            raise ValueError("neuron identifiers must be unique")
        if not isinstance(topology, BoundedTopology) or set(topology.nodes) != set(self.by_id):
            raise ValueError("topology nodes must match the excursion network")
        for name, value in (
            ("queue_capacity", queue_capacity),
            ("event_budget", event_budget),
            ("prediction_capacity", prediction_capacity),
            ("max_activity_events", max_activity_events),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        self.settling_horizon = self._nonnegative(settling_horizon, "settling_horizon")
        self.prediction_expiry = self._nonnegative(prediction_expiry, "prediction_expiry")
        if not isinstance(namespace, str) or not namespace:
            raise ValueError("namespace must be a non-empty string")
        self.topology = topology
        self.queue_capacity = queue_capacity
        self.event_budget = event_budget
        self.prediction_capacity = prediction_capacity
        self.max_activity_events = max_activity_events
        self.namespace = namespace
        self.queue: EventQueue[Event] | None = None
        self._sidecar: dict[int, RouteContext] = {}
        self._queued_timestamps: dict[int, float] = {}
        self._event_contexts: dict[str | int, RouteContext] = {}
        self._node_roots: dict[str, tuple[str, ...]] = {}
        self._node_truncation: dict[str, bool] = {}
        self._delivered_errors: set[tuple[str, str]] = set()
        self._predictor: LocalPredictor | None = None
        self._prediction_roots: dict[str, tuple[str, ...]] = {}
        self._prediction_lineages: dict[str, int] = {}
        self._ledgers: dict[str, EligibilityLedger] = {}
        self._classifier: StreamingCharacterClassifier | None = None
        self._meter: LocalEnergyModel | None = None
        self._edge_transfer_cost = 0.0
        self._prediction_error_cost = 0.0
        self._utility: RewardAdjustedUtility | None = None
        self._readout_sources: frozenset[str] = frozenset()
        self._predictor_source: str | None = None
        self._input_destination: str | None = None
        self._trace: list[tuple[object, ...]] = []
        self._emissions: list[ExcursionEmission] = []
        self._readout_sum = 0.0
        self._readout_count = 0
        self._prediction_loss = 0.0
        self._matched_predictions = 0
        self._unmatched_predictions = 0
        self._silent_count = 0
        self._matched_credit = 0
        self._unmatched_credit = 0
        self._processed = 0
        self._peak_queue = 0
        self._last_event_timestamp: float | None = None
        self._last_external_timestamp: float | None = None
        self._max_route_depth = 0
        self._provenance_truncated = False
        self._active = False

    @classmethod
    def from_quiescent_ir2(
        cls,
        ir: TPCNIR2,
        *,
        queue_capacity: int,
        event_budget: int,
        settling_horizon: float,
        prediction_capacity: int,
        prediction_expiry: float,
        max_activity_events: int,
        namespace: str,
    ) -> "ExcursionCharacterRuntime":
        """Start only from a uniformly excursion, quiescent IR-2 boundary."""
        if not isinstance(ir, TPCNIR2):
            raise TypeError("ir must be a validated TPCNIR2 record")
        if ir.events:
            raise IR2UnsupportedRuntimeError(
                "integrated IR-2 startup requires an empty shared event queue"
            )
        if any(record.dynamics_model != EXCURSION_V1 for record in ir.neurons):
            raise IR2UnsupportedRuntimeError(
                "integrated IR-2 startup requires a uniformly selected EXCURSION_V1 model"
            )
        for record in ir.neurons:
            if (
                record.mode is not IR2Mode.N
                or record.pending_internal_event is not None
                or record.ordinary_episode_id is not None
                or record.multi_episode_id is not None
                or record.lineage_id is not None
            ):
                raise IR2UnsupportedRuntimeError(
                    "integrated IR-2 startup rejects live-network resume"
                )
            if (
                record.x != 0.0
                or record.unassigned_provenance_count > 0
                or record.unassigned_provenance_truncated
            ):
                raise IR2UnsupportedRuntimeError(
                    "integrated IR-2 startup rejects residual state or unassigned provenance"
                )
        nodes = tuple(record.neuron_id for record in ir.neurons)
        edges = tuple(
            Edge(
                edge.source,
                edge.destination,
                edge.propagation_delay,
                routing_cost=edge.routing_cost,
                edge_weight=edge.w,
                divider_strength=edge.d,
                reference=edge.r,
                legacy_identity=edge.legacy_identity,
            )
            for edge in ir.edges
        )
        topology = BoundedTopology.from_edges(
            nodes,
            edges,
            fan_in_limit=ir.fan_in_limit,
            fan_out_limit=ir.fan_out_limit,
            edge_capacity=ir.edge_capacity,
            routing_capacity=ir.routing_capacity,
        )
        neurons = tuple(neuron_from_ir2_e2(record) for record in ir.neurons)
        return cls(
            neurons,
            topology,
            queue_capacity=queue_capacity,
            event_budget=event_budget,
            settling_horizon=settling_horizon,
            prediction_capacity=prediction_capacity,
            prediction_expiry=prediction_expiry,
            max_activity_events=max_activity_events,
            namespace=namespace,
        )

    @staticmethod
    def _nonnegative(value: Real, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"{name} must be a real number")
        result = float(value)
        if not math.isfinite(result) or result < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")
        return result

    @property
    def sidecar(self) -> dict[int, RouteContext]:
        return dict(self._sidecar)

    def start_character(
        self,
        character_id: str,
        character_index: int,
        *,
        timestamp: float,
        predictor_source: str,
        readout_sources: Iterable[str],
        input_destination: str,
    ) -> None:
        if self._active:
            raise RuntimeError("a character is already active")
        if not isinstance(character_id, str) or not character_id:
            raise ValueError("character_id must be a non-empty string")
        sources = frozenset(readout_sources)
        for node in (predictor_source, input_destination, *sources):
            if node not in self.by_id:
                raise ValueError(f"configured node {node!r} is not in the network")
        if not sources:
            raise ValueError("at least one readout source is required")
        start_time = self._nonnegative(timestamp, "timestamp")
        self.queue = EventQueue[Event](self.queue_capacity)
        self._sidecar.clear()
        self._queued_timestamps.clear()
        self._event_contexts.clear()
        self._node_roots = {node: () for node in self.by_id}
        self._node_truncation = {node: False for node in self.by_id}
        self._delivered_errors.clear()
        self._prediction_roots.clear()
        self._prediction_lineages.clear()
        self._predictor_source = predictor_source
        self._readout_sources = sources
        self._input_destination = input_destination
        self._predictor = LocalPredictor(
            f"{self.namespace}:{character_id}:predictor",
            max_outstanding=self.prediction_capacity,
            error_destination=predictor_source,
        )
        self._ledgers = {
            node: EligibilityLedger(
                f"{self.namespace}:{character_id}:ledger:{node}",
                max_traces=self.prediction_capacity * max(1, len(self.neurons)),
                decay_time_constant=4.0,
            )
            for node in self.by_id
        }
        self._classifier = StreamingCharacterClassifier(
            max_activity_events=self.max_activity_events,
        )
        self._meter = LocalEnergyModel(
            f"{self.namespace}:{character_id}:meter",
            max_counter=self.event_budget * 8,
        )
        self._edge_transfer_cost = 0.0
        self._prediction_error_cost = 0.0
        self._utility = RewardAdjustedUtility()
        self._trace = []
        self._emissions = []
        self._readout_sum = 0.0
        self._readout_count = 0
        self._prediction_loss = 0.0
        self._matched_predictions = 0
        self._unmatched_predictions = 0
        self._silent_count = 0
        self._matched_credit = 0
        self._unmatched_credit = 0
        self._processed = 0
        self._peak_queue = 0
        self._last_event_timestamp = None
        self._last_external_timestamp = None
        self._max_route_depth = 0
        self._provenance_truncated = False
        self._character_id = character_id
        self._character_index = character_index
        self._root_identity = 0
        self._feature_count_limit = self.event_budget
        assert self._classifier is not None
        self._classifier.ingest_event(
            Event(start_time, character_id, "classifier", START_CHARACTER, CharacterBoundary(character_index))
        )
        for neuron in self.neurons:
            neuron.reset(timestamp=start_time)
        self._active = True

    def _queue(self) -> EventQueue[Event]:
        if not self._active or self.queue is None:
            raise RuntimeError("no active character queue")
        return self.queue

    def _attach(self, queued: Event, context: RouteContext) -> None:
        if len(self._sidecar) >= self.queue_capacity:
            raise BufferError("character route sidecar capacity reached")
        self._sidecar[queued.sequence] = context
        self._queued_timestamps[queued.sequence] = queued.timestamp
        self._peak_queue = max(self._peak_queue, len(self._queue()))

    def _remember_event_context(self, event_id: str | int, context: RouteContext) -> None:
        if event_id not in self._event_contexts and len(self._event_contexts) >= self.event_budget:
            raise BufferError("character causal-context capacity reached")
        self._event_contexts[event_id] = context

    def _refresh_node_roots(
        self,
        neuron: MultiExcursionNeuron,
        context: RouteContext,
        current_event_id: str | int | None,
    ) -> None:
        if neuron.mode.value == "M_ACTIVE":
            active_episode = neuron.multi_episode_id
        else:
            active_episode = neuron.ordinary_episode_id
        provenance = tuple(
            entry
            for entry in neuron.provenance
            if entry.episode_id == active_episode
            or (active_episode is None and entry.episode_id is None)
        )
        roots: list[str] = []
        truncated = context.roots_truncated
        capacity = neuron.config.provenance_capacity
        for entry in provenance:
            provenance_context = self._event_contexts.get(entry.event_id)
            if provenance_context is None and entry.event_id == current_event_id:
                provenance_context = context
            if provenance_context is None:
                continue
            for root in provenance_context.causal_roots:
                if root not in roots:
                    if len(roots) >= capacity:
                        truncated = True
                    else:
                        roots.append(root)
            truncated |= provenance_context.roots_truncated
        self._node_roots[neuron.neuron_id] = tuple(roots)
        self._node_truncation[neuron.neuron_id] = truncated
        self._provenance_truncated |= truncated

    @staticmethod
    def _merge_root_values(roots: Iterable[str], capacity: int) -> RouteContext:
        merged: list[str] = []
        truncated = False
        for root in roots:
            if root not in merged:
                if len(merged) >= capacity:
                    truncated = True
                    continue
                merged.append(root)
        return RouteContext(tuple(merged), 0, (), truncated)

    def admit_external_batch(self, contributions: Iterable[tuple[float, float]]) -> None:
        """Admit all currently available external values at one timestamp."""
        queue = self._queue()
        batch = tuple(contributions)
        if not batch:
            return
        timestamp = self._nonnegative(batch[0][0], "timestamp")
        if any(self._nonnegative(item[0], "timestamp") != timestamp for item in batch):
            raise ValueError("external batch timestamps must be equal")
        if self._last_external_timestamp is not None and timestamp < self._last_external_timestamp:
            raise ValueError("late external input precedes the admitted input watermark")
        self._process_before(timestamp)
        earlier_pending = queue.peek()
        if earlier_pending is not None and earlier_pending.timestamp < timestamp:
            raise RuntimeError("event budget exhausted before the next external timestamp")
        assert self._predictor is not None and self._input_destination is not None
        for _, value in batch:
            contribution = self._nonnegative_payload(value)
            root = f"{self._character_id}:input:{self._root_identity}"
            self._root_identity += 1
            input_event = Event(
                timestamp,
                self._character_id,
                self._input_destination,
                EventType.INPUT,
                contribution,
                event_id=root,
            )
            self._remember_event_context(
                root,
                RouteContext((root,), 0, (self._input_destination,)),
            )
            # The target is observed only when its contribution is admitted.
            observation = Event(
                timestamp,
                self._character_id,
                self._predictor.predictor_id,
                "observation",
                Observation("external-input:scalar", contribution),
                event_id=root,
            )
            resolution = self._predictor.observe(observation)
            if resolution.error is None:
                self._unmatched_predictions += 1
            if resolution.error is not None:
                self._matched_predictions += 1
                self._prediction_loss += abs(resolution.error.error)
                lineage_id = self._prediction_lineages.pop(resolution.error.prediction_id, None)
                error_event = Event(
                    timestamp,
                    self._predictor_source,
                    self._predictor.error_destination,
                    PREDICTION_ERROR_EVENT,
                    resolution.error,
                    event_id=resolution.error.prediction_id,
                    lineage_id=lineage_id,
                )
                queued_error = queue.push(error_event)
                causal_roots = self._merge_root_values(
                    (*self._prediction_roots.pop(resolution.error.prediction_id, ()), root),
                    self.by_id[self._predictor_source].config.provenance_capacity,
                )
                self._attach(
                    queued_error,
                    RouteContext(
                        causal_roots.causal_roots,
                        0,
                        (self._predictor.error_destination,),
                        causal_roots.roots_truncated,
                    ),
                )
            queued = queue.push(input_event)
            self._attach(queued, self._event_contexts[root])
        self._last_external_timestamp = timestamp
        self._process_through(timestamp)

    @staticmethod
    def _nonnegative_payload(value: Real) -> float:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("external contribution must be a real number")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError("external contribution must be finite")
        return result

    def _process_before(self, timestamp: float) -> None:
        queue = self._queue()
        while self._processed < self.event_budget and queue:
            event = queue.peek()
            assert event is not None
            if event.timestamp >= timestamp:
                break
            self._process_one(queue.pop_ready(event.timestamp))

    def _process_through(self, timestamp: float) -> None:
        queue = self._queue()
        while self._processed < self.event_budget and queue:
            event = queue.peek()
            assert event is not None
            if event.timestamp > timestamp:
                break
            self._process_one(queue.pop_ready(timestamp))

    def _process_one(self, event: Event) -> None:
        queue = self._queue()
        context = self._sidecar.pop(event.sequence, None)
        self._queued_timestamps.pop(event.sequence, None)
        if context is None:
            raise RuntimeError(f"queued event {event.sequence} has no route context")
        self._processed += 1
        self._last_event_timestamp = event.timestamp
        self._max_route_depth = max(self._max_route_depth, context.route_depth)
        self._meter_observe_event(event)
        self._trace.append(
            (
                event.timestamp,
                event.source,
                event.destination,
                event.event_type,
                event.payload,
                event.sequence,
                event.event_id,
                event.lineage_id,
                context.causal_roots,
                context.route_depth,
                context.route_path,
                context.roots_truncated,
            )
        )
        if event.event_type == PREDICTION_ERROR_EVENT:
            self._deliver_prediction_error(event, context)
            return
        neuron = self.by_id.get(event.destination)
        if neuron is None:
            raise ValueError(f"event destination {event.destination!r} is not a neuron")
        emission = neuron.receive_event(event, queue)
        if emission is None:
            self._silent_count += 1
        self._refresh_node_roots(neuron, context, event.event_id)
        pending = neuron.pending_internal_event
        if pending is not None and pending.queue_sequence >= 0 and pending.queue_sequence not in self._sidecar:
            internal_context = RouteContext(
                self._node_roots[neuron.neuron_id],
                context.route_depth,
                context.route_path,
                self._node_truncation[neuron.neuron_id],
            )
            if len(self._sidecar) >= self.queue_capacity:
                raise BufferError("character route sidecar capacity reached")
            self._sidecar[pending.queue_sequence] = internal_context
            self._queued_timestamps[pending.queue_sequence] = pending.timestamp
            self._peak_queue = max(self._peak_queue, len(queue))
        if emission is None:
            return
        self._consume_emission(emission, context)

    def _consume_emission(self, emission: ExcursionEmission, parent: RouteContext) -> None:
        del parent
        queue = self._queue()
        assert self._predictor is not None and self._classifier is not None
        self._emissions.append(emission)
        trace_id = f"{self.namespace}:{self._character_id}:{emission.event_id}"
        prediction_id: str | None = None
        if emission.source == self._predictor_source:
            prediction = self._predictor.create_prediction(
                "external-input:scalar",
                emission.payload,
                timestamp=emission.timestamp,
                expires_at=emission.timestamp + self.prediction_expiry,
            )
            prediction_id = prediction.prediction_id
            self._prediction_roots[prediction_id] = self._node_roots[emission.source]
            self._prediction_lineages[prediction_id] = emission.lineage_id
        ledger = self._ledgers[emission.source]
        ledger.record_activity(
            Event(
                emission.timestamp,
                emission.source,
                ledger.ledger_id,
                ELIGIBILITY_ACTIVITY_EVENT,
                EligibilityActivity(trace_id, abs(emission.payload), prediction_id),
                event_id=emission.event_id,
                lineage_id=emission.lineage_id,
            )
        )
        if emission.source in self._readout_sources:
            if self._readout_count >= self._feature_count_limit:
                raise BufferError("readout excursion event capacity reached")
            activity = Event(
                emission.timestamp,
                emission.source,
                "classifier",
                ACTIVITY_EVENT,
                emission.payload,
                event_id=emission.event_id,
                lineage_id=emission.lineage_id,
            )
            self._classifier.ingest_activity(activity)
            self._readout_sum += emission.payload
            self._readout_count += 1
        self._meter_observe_emission(emission)
        self._trace.append(
            (
                emission.timestamp,
                emission.source,
                emission.source,
                "excursion_emission",
                emission.payload,
                emission.event_id,
                emission.sequence,
                emission.episode_id,
                emission.lineage_id,
                self._node_roots[emission.source],
                self._node_truncation[emission.source],
            )
        )
        emitted = emission.as_event(emission.source)
        routed = self.topology.route(emitted, queue)
        emitted_context = RouteContext(
            self._node_roots[emission.source],
            0,
            (emission.source,),
            self._node_truncation[emission.source],
        )
        self._remember_event_context(emission.event_id, emitted_context)
        for event in routed:
            destination_context = RouteContext(
                emitted_context.causal_roots,
                1,
                (emission.source, event.destination),
                emitted_context.roots_truncated,
            )
            self._attach(event, destination_context)
            self._meter_observe_edge(event, timestamp=emission.timestamp)
        self._peak_queue = max(self._peak_queue, len(queue))

    def _deliver_prediction_error(self, event: Event, context: RouteContext) -> None:
        payload = event.payload
        if not isinstance(payload, PredictionError):
            raise TypeError("prediction-error event payload must preserve PredictionError")
        key = (payload.prediction_id, event.destination)
        if key in self._delivered_errors:
            return
        if len(self._delivered_errors) >= self.event_budget * max(1, len(self.neurons)):
            raise BufferError("prediction-error delivery guard capacity reached")
        self._delivered_errors.add(key)
        ledger = self._ledgers[event.destination]
        attribution = ledger.apply_signal(
            Event(event.timestamp, event.source, ledger.ledger_id, event.event_type, payload)
        )
        if attribution.status == "matched":
            self._matched_credit += 1
        elif attribution.status in ("unmatched", "expired"):
            self._unmatched_credit += 1
        self._meter_observe_error(payload, event.timestamp)
        forwarded = self.topology.route(event, self._queue())
        for routed in forwarded:
            self._attach(
                routed,
                RouteContext(
                    context.causal_roots,
                    context.route_depth + 1,
                    context.route_path + (routed.destination,),
                    context.roots_truncated,
                ),
            )
            self._meter_observe_edge(routed, timestamp=event.timestamp)

    def _meter_observe_event(self, event: Event) -> None:
        assert self._meter is not None
        self._meter.observe_event(event)

    def _meter_observe_emission(self, emission: ExcursionEmission) -> None:
        assert self._meter is not None
        self._meter.observe_activity(
            "events_emitted",
            cost=abs(emission.payload),
            timestamp=emission.timestamp,
        )

    def _meter_observe_edge(self, event: Event, *, timestamp: float) -> None:
        assert self._meter is not None
        self._meter.observe_activity(
            "connection_activity",
            cost=abs(event.payload) if isinstance(event.payload, Real) else 1.0,
            timestamp=timestamp,
        )
        self._edge_transfer_cost += abs(event.payload) if isinstance(event.payload, Real) else 1.0

    def _meter_observe_error(self, error: PredictionError, timestamp: float) -> None:
        assert self._meter is not None
        self._meter.observe_activity(
            "prediction_errors",
            cost=1.0 + abs(error.error),
            timestamp=timestamp,
        )
        self._prediction_error_cost += 1.0 + abs(error.error)

    def end_character(
        self,
        *,
        last_external_timestamp: float,
        reward: float | Callable[[ClassificationResult, float], float],
        reward_delay: float,
        reward_message_id: str,
    ) -> ExcursionCharacterResult:
        queue = self._queue()
        assert self._classifier is not None
        assert self._predictor is not None
        assert self._meter is not None
        assert self._utility is not None
        last_timestamp = self._nonnegative(last_external_timestamp, "last_external_timestamp")
        horizon = last_timestamp + self.settling_horizon
        while self._processed < self.event_budget and queue:
            event = queue.peek()
            assert event is not None
            if event.timestamp > horizon:
                break
            self._process_one(queue.pop_ready(horizon))
        pending = len(queue)
        beyond_deadline = sum(timestamp > horizon for timestamp in self._queued_timestamps.values())
        incomplete = bool(pending)
        expired = self._predictor.expire(horizon)
        for prediction in expired:
            self._prediction_roots.pop(prediction.prediction_id, None)
            self._prediction_lineages.pop(prediction.prediction_id, None)
        result_event = self._classifier.ingest_event(
            Event(horizon, self._character_id, "classifier", END_CHARACTER, CharacterBoundary(self._character_index))
        )
        if not isinstance(result_event, ClassificationResult):
            raise RuntimeError("classifier did not return its completed character result")
        resolved_reward = (
            reward(result_event, self._readout_sum / self._readout_count if self._readout_count else 0.0)
            if callable(reward)
            else reward
        )
        attribution_status = "unmatched"
        reward_latency = 0.0
        message_timestamp = horizon + self._nonnegative(reward_delay, "reward_delay")
        message = RewardMessage(reward_message_id, resolved_reward, message_timestamp)
        self._utility.observe_reward(message)
        readout_emissions = [
            emission for emission in self._emissions if emission.source in self._readout_sources
        ]
        if readout_emissions:
            first = readout_emissions[0]
            trace_id = f"{self.namespace}:{self._character_id}:{first.event_id}"
            ledger = self._ledgers[first.source]
            attribution = ledger.apply_signal(
                Event(
                    message_timestamp,
                    "outer-readout",
                    ledger.ledger_id,
                    "reward",
                    RewardSignal(resolved_reward, message_id=reward_message_id, trace_id=trace_id),
                )
            )
            attribution_status = attribution.status
            if attribution.status == "matched":
                reward_latency = message_timestamp - horizon
            else:
                self._unmatched_credit += 1
        else:
            self._unmatched_credit += 1
        snapshot = self._meter.snapshot()
        counters = dict(snapshot.counters)
        components = (
            ("event_processing", float(counters["events_received"])),
            ("emitted_amplitude", sum(abs(item.payload) for item in self._emissions)),
            ("edge_transfer", self._edge_transfer_cost),
            ("prediction_error", self._prediction_error_cost),
        )
        completed = not incomplete
        execution = BoundedExecutionResult(
            completed,
            self._processed >= self.event_budget and pending > 0,
            self.event_budget,
            self._processed,
            pending,
            "incomplete_settling" if incomplete else "completed",
            self._last_event_timestamp,
            self._peak_queue,
        )
        final = ExcursionCharacterResult(
            tuple(self._trace),
            result_event,
            self._readout_sum / self._readout_count if self._readout_count else 0.0,
            len(self._emissions),
            self._silent_count,
            self._prediction_loss,
            self._matched_predictions,
            self._unmatched_predictions,
            self._predictor.expired_count,
            self._matched_credit,
            self._unmatched_credit,
            self._peak_queue,
            pending,
            beyond_deadline,
            incomplete,
            execution,
            sum(value for _, value in components),
            components,
            self._max_route_depth,
            self._provenance_truncated,
            attribution_status,
            float(resolved_reward),
            reward_latency,
            self._utility.evaluate(snapshot.energy, resolved_reward).utility,
            sum(neuron.mode.value != "N" for neuron in self.neurons),
            sum(neuron.processed_event_count > 0 for neuron in self.neurons),
            len({emission.source for emission in self._emissions}),
        )
        self._destroy_character(horizon)
        return final

    def _destroy_character(self, timestamp: float) -> None:
        self.queue = None
        self._sidecar.clear()
        self._queued_timestamps.clear()
        self._event_contexts.clear()
        self._delivered_errors.clear()
        self._prediction_roots.clear()
        self._prediction_lineages.clear()
        for neuron in self.neurons:
            neuron.reset(timestamp=timestamp)
        if self._classifier is not None:
            self._classifier.reset()
        self._predictor = None
        self._ledgers.clear()
        self._meter = None
        self._utility = None
        self._active = False

    def reset(self) -> None:
        """Destroy active character state while preserving E2 identity counters."""
        if self._active:
            timestamp = self._last_event_timestamp or 0.0
            self._destroy_character(timestamp)
        else:
            self.queue = None
            self._sidecar.clear()


__all__ = [
    "ExcursionCharacterResult",
    "ExcursionCharacterRuntime",
    "RouteContext",
]
