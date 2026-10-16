"""Bounded four-class temporal-order and singleton learning experiment."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import random
from numbers import Real
from typing import Any, Literal

from .canonical_neuron import TPCNNeuron
from .eligibility import (
    ELIGIBILITY_ACTIVITY_EVENT,
    REWARD_EVENT,
    CreditAttribution,
    EligibilityActivity,
    EligibilityLedger,
    RewardSignal,
)
from .event_runtime import Event, EventQueue, EventType, execute_bounded
from .luna66_minimal_learning import _clamp, _event_row as _base_event_row, wilson_interval
from .predictive_coding import (
    PREDICTION_ERROR_EVENT,
    LocalPredictor,
    Observation,
    Prediction,
    PredictionError,
)
from .topology import BoundedTopology


InputSymbol = Literal["A", "B"]
TemporalEvents = tuple[Event, ...]
Condition = Literal[
    "trained",
    "learning_disabled",
    "shuffled_rewards",
    "temporal_order_destroyed",
    "untrained",
    "silence_information_ablation",
]
OmissionErrorEventType = Literal["prediction_omission_error"]

CLASS_NAMES = {
    0: "A_then_B",
    1: "B_then_A",
    2: "A_only",
    3: "B_only",
}
INPUT_NODES = {"A": "input:A", "B": "input:B"}
SYMBOL_CODE = {"A": 1.0, "B": -1.0}
READOUT_NODES = tuple(f"readout:{name}" for name in CLASS_NAMES.values())
CONDITIONS: tuple[Condition, ...] = (
    "trained",
    "learning_disabled",
    "shuffled_rewards",
    "temporal_order_destroyed",
    "untrained",
    "silence_information_ablation",
)


@dataclass(frozen=True, slots=True)
class Luna67Config:
    seeds: tuple[int, ...] = (17, 29, 43)
    train_per_class: int = 100
    validation_per_class: int = 25
    test_per_class: int = 50
    epochs: int = 5
    first_time_min: float = 0.15
    first_time_max: float = 0.35
    nominal_gap_min: float = 1.0
    nominal_gap_max: float = 1.2
    second_event_jitter: float = 0.05
    observation_window: float = 1.35
    input_edge_delay: float = 0.05
    prediction_emit_delay: float = 0.05
    prediction_error_delay: float = 0.05
    readout_delay: float = 0.10
    readout_prediction_delay: float = 0.05
    reward_delay: float = 1.0
    neuron_decay_rate: float = 1.0
    prediction_eligibility_tau: float = 2.0
    reward_eligibility_tau: float = 4.0
    prediction_learning_rate: float = 0.25
    readout_learning_rate: float = 0.6
    queue_capacity: int = 16
    event_budget_per_example: int = 32
    topology_edge_capacity: int = 9

    def __post_init__(self) -> None:
        if not self.seeds or any(isinstance(seed, bool) or not isinstance(seed, int) for seed in self.seeds):
            raise ValueError("seeds must be a non-empty tuple of integers")
        for name in (
            "train_per_class",
            "validation_per_class",
            "test_per_class",
            "epochs",
            "queue_capacity",
            "event_budget_per_example",
            "topology_edge_capacity",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for name in (
            "first_time_min",
            "first_time_max",
            "nominal_gap_min",
            "nominal_gap_max",
            "second_event_jitter",
            "observation_window",
            "input_edge_delay",
            "prediction_emit_delay",
            "prediction_error_delay",
            "readout_delay",
            "readout_prediction_delay",
            "reward_delay",
            "neuron_decay_rate",
            "prediction_eligibility_tau",
            "reward_eligibility_tau",
            "prediction_learning_rate",
            "readout_learning_rate",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.first_time_min <= 0 or self.first_time_max < self.first_time_min:
            raise ValueError("first-time range must be positive and ordered")
        if self.nominal_gap_min <= self.second_event_jitter or self.nominal_gap_max < self.nominal_gap_min:
            raise ValueError("nominal second-event delays must be ordered and exceed jitter")
        if self.neuron_decay_rate <= 0 or self.prediction_eligibility_tau <= 0 or self.reward_eligibility_tau <= 0:
            raise ValueError("decay rates and eligibility time constants must be positive")
        if min(
            self.input_edge_delay,
            self.prediction_emit_delay,
            self.prediction_error_delay,
            self.readout_delay,
            self.readout_prediction_delay,
            self.reward_delay,
        ) <= 0:
            raise ValueError("all network propagation delays must be positive")
        maximum_second_arrival = self.nominal_gap_max + self.second_event_jitter + self.input_edge_delay
        if self.observation_window <= maximum_second_arrival:
            raise ValueError("common observation window must follow the latest routed second event")
        if self.topology_edge_capacity < 9:
            raise ValueError("topology_edge_capacity must accommodate the nine declared edges")
        if self.queue_capacity < 8:
            raise ValueError("queue_capacity must admit bounded four-channel fan-out and credit events")
        if self.event_budget_per_example < 16:
            raise ValueError("event_budget_per_example must admit a complete bounded episode")


@dataclass(frozen=True, slots=True)
class TemporalSequenceExample:
    example_id: str
    label: int
    events: TemporalEvents


@dataclass(frozen=True, slots=True)
class ExternalObservationDeadline:
    deadline_id: str
    first_event_id: str | int
    window_after_first_event: float
    source_kind: str = "external_evaluation_clock"


@dataclass(frozen=True, slots=True)
class OmissionErrorSignal:
    prediction_id: str
    target_key: str
    predicted_symbol: InputSymbol
    predicted_value: float
    observed_value: float
    error_value: float
    prediction_timestamp: float
    resolution_timestamp: float
    resolution_source: str


def _event_row(event: Event) -> dict[str, Any]:
    row = _base_event_row(event)
    if isinstance(event.payload, OmissionErrorSignal):
        row["payload"] = {
            "prediction_id": event.payload.prediction_id,
            "target_key": event.payload.target_key,
            "predicted_symbol": event.payload.predicted_symbol,
            "predicted_value": event.payload.predicted_value,
            "observed_value": event.payload.observed_value,
            "error_value": event.payload.error_value,
            "prediction_timestamp": event.payload.prediction_timestamp,
            "resolution_timestamp": event.payload.resolution_timestamp,
            "resolution_source": event.payload.resolution_source,
        }
    elif isinstance(event.payload, ExternalObservationDeadline):
        row["payload"] = {
            "deadline_id": event.payload.deadline_id,
            "first_event_id": event.payload.first_event_id,
            "window_after_first_event": event.payload.window_after_first_event,
            "source_kind": event.payload.source_kind,
        }
    elif isinstance(event.payload, Luna70CorrectiveFeedback):
        row["payload"] = {
            "message_id": event.payload.message_id,
            "prediction_id": event.payload.prediction_id,
            "target_class": event.payload.target_class,
            "correction_signs": event.payload.correction_signs,
        }
    return row


@dataclass(frozen=True, slots=True)
class Luna70CorrectiveFeedback:
    message_id: str
    prediction_id: str
    target_class: int
    correction_signs: tuple[int, int, int, int]


@dataclass(slots=True)
class FourClassTaskModel:
    next_symbol_weights: dict[InputSymbol, float]
    readout_weights: list[float]
    readout_biases: list[float]

    @classmethod
    def untrained(cls) -> "FourClassTaskModel":
        return cls({"A": 0.0, "B": 0.0}, [0.0] * 4, [0.0] * 4)

    def snapshot(self) -> dict[str, Any]:
        return {
            "next_symbol_weights": dict(self.next_symbol_weights),
            "readout_weights": list(self.readout_weights),
            "readout_biases": list(self.readout_biases),
        }


@dataclass(frozen=True, slots=True)
class SequenceResult:
    example_id: str
    predicted_class: int
    prediction_scores: tuple[float, float, float, float]
    readout_input_features: tuple[float, float]
    readout_score_margins: tuple[float, float, float, float]
    final_sequence_state: float
    state_before_silence: float
    state_after_silence: float
    silence_state_decay: float
    silence_state_integrated: bool
    completion_trigger: str
    completion_deadline: float
    first_event_timestamp: float
    first_event_network_timestamp: float
    first_event_id: str | int
    event_count: int
    second_event_id: str | int | None
    second_event_timestamp: float | None
    prediction_id: str
    prediction_value: float
    prediction_emitted_at: float
    prediction_target_symbol: str | None
    prediction_resolution_source: str
    prediction_resolution_event_id: str
    prediction_resolution_timestamp: float
    prediction_error: float
    prediction_error_eligibility: float
    prediction_error_credit: float
    prediction_created_count: int
    prediction_matched_count: int
    prediction_expired_count: int
    prediction_omitted_count: int
    omission_error_route_enabled: bool
    omission_error_route_event_id: str | None
    omission_error_lineage_id: str | None
    omission_error_prediction_id: str | None
    omission_error_predicted_symbol: str | None
    omission_error_value: float | None
    omission_error_delivery_timestamp: float | None
    omission_error_event_count: int
    omission_error_route_delivery_count: int
    omission_readout_reception_count: int
    readout_emissions_following_omission: int
    duplicate_omission_error_deliveries: int
    omission_feature_before_integration: float | None
    omission_feature_after_integration: float | None
    readout_prediction_id: str
    readout_timestamp: float
    reward_delivered: bool
    reward_message_id: str | None
    reward_value: float | None
    reward_timestamp: float | None
    reward_attribution_statuses: tuple[str, ...]
    reward_prediction_id: str | None
    reward_trace_ids: tuple[str, ...]
    reward_eligibilities: tuple[float, ...]
    reward_credits: tuple[float, ...]
    readout_weights_before: tuple[float, ...] | None
    readout_weights_after: tuple[float, ...] | None
    readout_biases_before: tuple[float, ...] | None
    readout_biases_after: tuple[float, ...] | None
    readout_arm: str
    channel_eligibility: tuple[float, float, float, float]
    weight_update_deltas: tuple[float, float, float, float] | None
    bias_update_deltas: tuple[float, float, float, float] | None
    correction_signs: tuple[int, int, int, int] | None
    feedback_applied_at: float | None
    correction_message_id: str | None
    correction_event_id: str | None
    correction_event_count: int
    input_events: int
    external_deadline_events: int
    internal_emissions: int
    routed_events: int
    prediction_events: int
    next_symbol_prediction_events: int
    readout_prediction_events: int
    prediction_error_events: int
    readout_events: int
    reward_events: int
    processed_events: int
    peak_queue_occupancy: int
    local_energy_proxy: float
    dropped_events: int
    admission_failures: int
    duplicate_reward_applications: int
    event_trace: tuple[dict[str, Any], ...]


def _dataset_bytes(examples: tuple[TemporalSequenceExample, ...], *, include_labels: bool) -> bytes:
    rows = []
    for example in examples:
        row: dict[str, Any] = {
            "example_id": example.example_id,
            "events": [
                {
                    "timestamp": event.timestamp,
                    "source": event.source,
                    "destination": event.destination,
                    "event_type": event.event_type.value if isinstance(event.event_type, EventType) else event.event_type,
                    "payload": event.payload,
                    "event_id": event.event_id,
                }
                for event in example.events
            ],
        }
        if include_labels:
            row["label"] = example.label
        rows.append(row)
    return json.dumps(rows, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def dataset_hashes(examples: tuple[TemporalSequenceExample, ...]) -> dict[str, str]:
    return {
        "content_sha256": hashlib.sha256(_dataset_bytes(examples, include_labels=True)).hexdigest(),
        "input_only_sha256": hashlib.sha256(_dataset_bytes(examples, include_labels=False)).hexdigest(),
    }


def generate_dataset(
    split: str,
    *,
    per_class: int,
    seed: int,
    config: Luna67Config,
) -> tuple[TemporalSequenceExample, ...]:
    if not isinstance(split, str) or not split:
        raise ValueError("split must be a non-empty string")
    if isinstance(per_class, bool) or not isinstance(per_class, int) or per_class <= 0:
        raise ValueError("per_class must be a positive integer")
    generator = random.Random(seed)
    specifications: list[tuple[int, float, float | None]] = []
    for label in CLASS_NAMES:
        for _ in range(per_class):
            first_time = generator.uniform(config.first_time_min, config.first_time_max)
            gap = None
            if label in (0, 1):
                gap = generator.uniform(config.nominal_gap_min, config.nominal_gap_max)
                gap += generator.uniform(-config.second_event_jitter, config.second_event_jitter)
            specifications.append((label, first_time, gap))
    generator.shuffle(specifications)

    examples: list[TemporalSequenceExample] = []
    for index, (label, first_time, gap) in enumerate(specifications):
        example_id = f"{split}:{index:05d}"
        first_symbol: InputSymbol = "A" if label in (0, 2) else "B"
        events = [
            Event(
                first_time,
                INPUT_NODES[first_symbol],
                INPUT_NODES[first_symbol],
                EventType.INPUT,
                SYMBOL_CODE[first_symbol],
                event_id=f"{example_id}:input:0",
            )
        ]
        if gap is not None:
            second_symbol: InputSymbol = "B" if label == 0 else "A"
            events.append(
                Event(
                    first_time + gap,
                    INPUT_NODES[second_symbol],
                    INPUT_NODES[second_symbol],
                    EventType.INPUT,
                    SYMBOL_CODE[second_symbol],
                    event_id=f"{example_id}:input:1",
                )
            )
        examples.append(TemporalSequenceExample(example_id, label, tuple(events)))
    return tuple(examples)


def _validate_input_events(events: TemporalEvents) -> None:
    if not isinstance(events, tuple) or len(events) not in (1, 2):
        raise ValueError("events must be a one- or two-Event tuple")
    symbols: list[str] = []
    event_ids: set[str | int] = set()
    for event in events:
        if not isinstance(event, Event):
            raise TypeError("events must contain only Event instances")
        symbol = next((key for key, node in INPUT_NODES.items() if node == event.source), None)
        if event.event_type != EventType.INPUT or symbol is None or event.destination != event.source:
            raise ValueError("each input must be an INPUT event addressed to its declared symbol port")
        if isinstance(event.payload, bool) or not isinstance(event.payload, Real):
            raise TypeError("input event payloads must be numeric symbol values")
        if not math.isfinite(float(event.payload)) or float(event.payload) != SYMBOL_CODE[symbol]:
            raise ValueError("input event payload must match its declared symbol channel")
        if event.event_id is None or event.event_id in event_ids:
            raise ValueError("input events must have distinct, stable event identities")
        symbols.append(symbol)
        event_ids.add(event.event_id)
    if len(symbols) == 2 and symbols[0] == symbols[1]:
        raise ValueError("two-event examples must contain one A and one B")
    if len(events) == 2 and events[0].timestamp >= events[1].timestamp:
        raise ValueError("input events must be supplied in strictly increasing timestamp order")


def _destroy_temporal_order(events: TemporalEvents) -> TemporalEvents:
    if len(events) == 1:
        return events
    first_time, second_time = events[0].timestamp, events[1].timestamp
    return (
        Event(first_time, INPUT_NODES["A"], INPUT_NODES["A"], EventType.INPUT, 1.0, event_id=events[0].event_id),
        Event(second_time, INPUT_NODES["B"], INPUT_NODES["B"], EventType.INPUT, -1.0, event_id=events[1].event_id),
    )


def _topology(
    config: Luna67Config,
    predictor_id: str,
    *,
    omission_error_route_enabled: bool = False,
    corrective_feedback_enabled: bool = False,
) -> BoundedTopology:
    nodes = (
        "input:A",
        "input:B",
        "sequence",
        predictor_id,
        "prediction_ledger",
        *READOUT_NODES,
        "readout_weight_ledger",
        "readout_bias_ledger",
        "readout_correction_ledger",
        "training_feedback",
        "outcome",
    )
    edges = (
        ("input:A", "sequence", config.input_edge_delay),
        ("input:B", "sequence", config.input_edge_delay),
        (predictor_id, "prediction_ledger", config.prediction_error_delay),
        *(
            (("prediction_ledger", "sequence", config.prediction_error_delay),)
            if omission_error_route_enabled
            else ()
        ),
        *((("sequence", node, config.readout_delay) for node in READOUT_NODES)),
        ("outcome", "readout_weight_ledger", config.reward_delay),
        ("outcome", "readout_bias_ledger", config.reward_delay),
        *(
            (("training_feedback", "readout_correction_ledger", config.reward_delay),)
            if corrective_feedback_enabled
            else ()
        ),
    )
    return BoundedTopology.from_edges(
        nodes,
        edges,
        fan_in_limit=3 if omission_error_route_enabled else 2,
        fan_out_limit=4,
        edge_capacity=max(
            config.topology_edge_capacity,
            9 + int(omission_error_route_enabled) + int(corrective_feedback_enabled),
        ),
        routing_capacity=4,
    )


def _class_sequence(label: int) -> tuple[str, ...]:
    return {
        0: ("A", "B"),
        1: ("B", "A"),
        2: ("A",),
        3: ("B",),
    }[label]


def run_example(
    model: FourClassTaskModel,
    *,
    example_id: str,
    events: TemporalEvents,
    config: Luna67Config,
    exposure_id: str,
    feedback_label: int | None = None,
    learning_enabled: bool = False,
    destroy_temporal_order: bool = False,
    silence_information_ablation: bool = False,
    omission_error_route_enabled: bool = False,
    readout_arm: str = "A",
    retain_event_trace: bool = True,
    ppc11_capture: Any = None,
) -> SequenceResult:
    if not isinstance(example_id, str) or not example_id:
        raise ValueError("example_id must be a non-empty string")
    _validate_input_events(events)
    if feedback_label is not None and (
        isinstance(feedback_label, bool)
        or not isinstance(feedback_label, int)
        or feedback_label not in CLASS_NAMES
    ):
        raise ValueError("feedback_label must be a valid four-class label or None")
    if readout_arm not in {"A", "B", "C", "D"}:
        raise ValueError("readout_arm must be one of A, B, C, or D")
    corrective_feedback_enabled = (
        readout_arm in {"C", "D"} and learning_enabled and feedback_label is not None
    )
    inputs = _destroy_temporal_order(events) if destroy_temporal_order else events
    if ppc11_capture is not None:
        parameters = model.snapshot()
        parameter_digest = hashlib.sha256(json.dumps(
            parameters, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")).hexdigest()
        ppc11_capture.emit("parameter_initial", manifest_sha256=parameter_digest,
                           parameters=parameters)
        for input_order, input_event in enumerate(inputs):
            ppc11_capture.emit(
                "input_event", event_type=getattr(input_event.event_type, "value", input_event.event_type),
                payload=input_event.payload, payload_type=type(input_event.payload).__qualname__,
                timestamp=input_event.timestamp, input_order=input_order,
                channel_id=input_event.source, event_id=input_event.event_id,
            )
    first_event = inputs[0]
    deadline_timestamp = first_event.timestamp + config.observation_window
    deadline_event = Event(
        deadline_timestamp,
        "external_evaluation_clock",
        "observation_deadline",
        EventType.CONTROL,
        ExternalObservationDeadline(
            f"{example_id}:common-deadline",
            first_event.event_id,  # type: ignore[arg-type]
            config.observation_window,
        ),
        event_id=f"{example_id}:common-deadline",
    )

    queue: EventQueue[Event] = EventQueue(config.queue_capacity, observer=ppc11_capture)
    for event in inputs:
        queue.push(event)
    queue.push(deadline_event)

    predictor_id = f"predictor:{exposure_id}"
    topology = _topology(
        config,
        predictor_id,
        omission_error_route_enabled=omission_error_route_enabled,
        corrective_feedback_enabled=corrective_feedback_enabled,
    )
    sequence_neuron = TPCNNeuron(
        "sequence",
        state_limit=2.0,
        decay_rate=config.neuron_decay_rate,
        neuron_gain=1.0,
    )
    readout_neurons = {
        node: TPCNNeuron(node, state_limit=2.0, decay_rate=0.0, neuron_gain=1.0)
        for node in READOUT_NODES
    }
    predictor = LocalPredictor(
        predictor_id,
        max_outstanding=1,
        error_destination="prediction_ledger",
    )
    prediction_ledger = EligibilityLedger(
        "prediction_ledger",
        max_traces=1,
        decay_time_constant=config.prediction_eligibility_tau,
        expiry=config.prediction_eligibility_tau * 3.0,
        credit_limit=2.0,
        max_reward_identities=2,
    )
    weight_ledger = EligibilityLedger(
        "readout_weight_ledger",
        max_traces=1,
        decay_time_constant=config.reward_eligibility_tau,
        expiry=config.reward_eligibility_tau * 2.0,
        credit_limit=2.0,
        max_reward_identities=2,
    )
    bias_ledger = EligibilityLedger(
        "readout_bias_ledger",
        max_traces=1,
        decay_time_constant=config.reward_eligibility_tau,
        expiry=config.reward_eligibility_tau * 2.0,
        credit_limit=2.0,
        max_reward_identities=2,
    )

    trace: list[dict[str, Any]] = []
    seen_inputs: list[Event] = []
    readout_outputs: dict[int, float] = {}
    readout_emissions: list[dict[str, Any]] = []
    prediction: Prediction | None = None
    prediction_created_count = 0
    prediction_matched_count = 0
    prediction_sink_timestamp: float | None = None
    prediction_error: PredictionError | None = None
    prediction_error_attribution: CreditAttribution | None = None
    prediction_trace_id: str | None = None
    omission_signal: OmissionErrorSignal | None = None
    omission_error_route_event_id: str | None = None
    omission_error_lineage_id: str | None = None
    omission_error_delivery_timestamp: float | None = None
    omission_error_value: float | None = None
    omission_error_predicted_symbol: InputSymbol | None = None
    omission_feature_before_integration: float | None = None
    omission_feature_after_integration: float | None = None
    omission_routed_prediction_ids: set[str] = set()
    omission_delivered_event_ids: set[str] = set()
    omission_error_route_count = 0
    omission_error_route_delivery_count = 0
    omission_readout_reception_count = 0
    readout_emissions_following_omission = 0
    duplicate_omission_error_deliveries = 0
    readout_prediction: Prediction | None = None
    readout_prediction_sink_timestamp: float | None = None
    predicted_class: int | None = None
    readout_features: tuple[float, float] | None = None
    readout_timestamp: float | None = None
    state_before_silence: float | None = None
    state_at_deadline: float | None = None
    reward_value: float | None = None
    reward_timestamp: float | None = None
    reward_attributions: dict[str, CreditAttribution] = {}
    weights_before: tuple[float, ...] | None = None
    weights_after: tuple[float, ...] | None = None
    biases_before: tuple[float, ...] | None = None
    biases_after: tuple[float, ...] | None = None
    channel_eligibility = (0.0, 0.0, 0.0, 0.0)
    weight_update_deltas: tuple[float, float, float, float] | None = None
    bias_update_deltas: tuple[float, float, float, float] | None = None
    correction_signs: tuple[int, int, int, int] | None = None
    feedback_applied_at: float | None = None
    correction_message_id: str | None = None
    correction_event_id: str | None = None
    correction_event_count = 0
    correction_signal: Luna70CorrectiveFeedback | None = None
    internal_emissions = 0
    routed_events = 0
    prediction_events = 0
    next_symbol_prediction_events = 0
    readout_prediction_events = 0
    prediction_error_events = 0
    readout_events = 0
    reward_events = 0
    duplicate_reward_applications = 0
    observation_event_id: str | None = None
    observation_source: str | None = None
    observation_timestamp: float | None = None
    observation_symbol: str | None = None

    def record_synthetic_event(event: Event) -> None:
        if retain_event_trace:
            trace.append(_event_row(event))

    def schedule_readout(
        timestamp: float,
        features: tuple[float, float],
        pending: EventQueue[Event],
    ) -> None:
        nonlocal readout_features, internal_emissions, routed_events
        if readout_features is not None:
            raise RuntimeError("four-class readout was scheduled more than once")
        readout_features = features
        if ppc11_capture is not None:
            ppc11_capture.emit("readout_feature", decision_id=f"{exposure_id}:readout",
                               decision_at=timestamp, feature=features[0])
        for class_index, node in enumerate(READOUT_NODES):
            weight = model.readout_weights[class_index]
            bias = model.readout_biases[class_index]
            drive = weight * features[0] + bias
            if ppc11_capture is not None:
                ppc11_capture.emit("readout_drive", decision_id=f"{exposure_id}:readout",
                                   class_index=class_index, weight=weight, bias=bias,
                                   feature=features[0], drive=drive)
            routed = topology.route(
                Event(
                    timestamp,
                    "sequence",
                    "sequence",
                    EventType.SIGNAL,
                    drive,
                    event_id=f"{exposure_id}:readout-drive:{class_index}",
                ),
                pending,
                exclude_destinations=tuple(other for other in READOUT_NODES if other != node),
            )
            routed_events += len(routed)
            internal_emissions += len(routed)

    def apply_corrective_if_ready(timestamp: float) -> None:
        nonlocal weights_before, weights_after, biases_before, biases_after
        nonlocal weight_update_deltas, bias_update_deltas, correction_signs
        nonlocal feedback_applied_at
        if (
            not corrective_feedback_enabled
            or correction_signal is None
            or set(reward_attributions)
            != {"readout_weight_ledger", "readout_bias_ledger"}
        ):
            return
        if (
            readout_prediction is None
            or correction_signal.prediction_id != readout_prediction.prediction_id
            or correction_signal.message_id != correction_message_id
            or reward_timestamp is None
            or timestamp < reward_timestamp
        ):
            raise RuntimeError("corrective feedback lost identity or arrived before its due time")
        weight_credit = reward_attributions["readout_weight_ledger"].credit
        bias_credit = reward_attributions["readout_bias_ledger"].credit
        if weight_credit != bias_credit:
            raise RuntimeError("weight and bias ledgers produced different delayed credits")
        credit_scale = config.readout_learning_rate * abs(weight_credit)
        correction_signs = correction_signal.correction_signs
        weights_before = tuple(model.readout_weights)
        biases_before = tuple(model.readout_biases)
        updated_weights = list(model.readout_weights)
        for channel, eligibility in enumerate(channel_eligibility):
            updated_weights[channel] = _clamp(
                updated_weights[channel]
                + credit_scale
                * correction_signs[channel]
                * readout_features[0]
                * eligibility,
                -3.0,
                3.0,
            )
        model.readout_weights[:] = updated_weights
        weight_update_deltas = tuple(
            after - before
            for before, after in zip(weights_before, model.readout_weights)
        )  # type: ignore[assignment]
        if readout_arm == "D":
            bias_update_deltas = (0.0, 0.0, 0.0, 0.0)
        else:
            updated_biases = list(model.readout_biases)
            for channel, eligibility in enumerate(channel_eligibility):
                updated_biases[channel] = _clamp(
                    updated_biases[channel]
                    + credit_scale * correction_signs[channel] * eligibility,
                    -3.0,
                    3.0,
                )
            model.readout_biases[:] = updated_biases
            bias_update_deltas = tuple(
                after - before
                for before, after in zip(biases_before, model.readout_biases)
            )  # type: ignore[assignment]
        weights_after = tuple(model.readout_weights)
        biases_after = tuple(model.readout_biases)
        feedback_applied_at = timestamp

    def handle(event: Event, pending: EventQueue[Event]) -> None:
        nonlocal prediction, prediction_sink_timestamp, prediction_error
        nonlocal prediction_error_attribution, prediction_trace_id, readout_prediction
        nonlocal readout_prediction_sink_timestamp, predicted_class, readout_features
        nonlocal readout_timestamp, state_before_silence, state_at_deadline
        nonlocal reward_value, reward_timestamp, weights_before, weights_after
        nonlocal biases_before, biases_after, internal_emissions, routed_events
        nonlocal channel_eligibility, weight_update_deltas, bias_update_deltas
        nonlocal correction_signs, feedback_applied_at
        nonlocal correction_message_id, correction_event_id, correction_event_count
        nonlocal correction_signal
        nonlocal prediction_events, prediction_error_events, readout_events
        nonlocal next_symbol_prediction_events, readout_prediction_events
        nonlocal reward_events, duplicate_reward_applications
        nonlocal prediction_created_count, prediction_matched_count
        nonlocal omission_signal, omission_error_route_event_id, omission_error_lineage_id
        nonlocal omission_error_delivery_timestamp, omission_error_value
        nonlocal omission_error_predicted_symbol, omission_feature_before_integration
        nonlocal omission_feature_after_integration, omission_error_route_count
        nonlocal omission_error_route_delivery_count, omission_readout_reception_count
        nonlocal readout_emissions_following_omission, duplicate_omission_error_deliveries
        nonlocal observation_event_id, observation_source, observation_timestamp, observation_symbol

        if retain_event_trace:
            trace.append(_event_row(event))

        if event.destination in INPUT_NODES.values():
            routed = topology.route(event, pending)
            routed_events += len(routed)
            internal_emissions += len(routed)
            return

        if event.destination == "sequence":
            if event.event_type == "prediction_omission_error":
                if not omission_error_route_enabled or not isinstance(event.payload, OmissionErrorSignal):
                    raise TypeError("sequence received an unexpected omission-error route event")
                signal = event.payload
                if (
                    omission_signal is None
                    or event.event_id != omission_error_route_event_id
                    or event.lineage_id != signal.prediction_id
                    or signal.prediction_id != prediction.prediction_id
                    or signal.resolution_source != "observation_deadline:missed_second_event"
                    or event.timestamp <= signal.resolution_timestamp
                ):
                    raise RuntimeError("omission-error route lost prediction identity or causal ordering")
                if event.event_id in omission_delivered_event_ids:
                    duplicate_omission_error_deliveries += 1
                    raise RuntimeError("duplicate omission-error event reached neural integration")
                omission_delivered_event_ids.add(str(event.event_id))
                omission_error_route_delivery_count += 1
                if ppc11_capture is not None:
                    ppc11_capture.emit(
                        "omission_delivery", prediction_id=signal.prediction_id,
                        route=[event.source, event.destination], payload=signal,
                        event_id=event.event_id, delivered_at=event.timestamp, outcome="delivered")
                omission_error_delivery_timestamp = event.timestamp
                omission_error_value = signal.error_value
                omission_error_predicted_symbol = signal.predicted_symbol
                elapsed = event.timestamp - sequence_neuron.clock.timestamp
                if elapsed < 0.0:
                    raise RuntimeError("omission error arrived before the sequence neuron's local time")
                omission_feature_before_integration = (
                    sequence_neuron.state
                    * math.exp(-config.neuron_decay_rate * elapsed)
                )
                sequence_neuron.receive_event(
                    Event(
                        event.timestamp,
                        event.source,
                        "sequence",
                        EventType.SIGNAL,
                        signal.error_value,
                        event_id=event.event_id,
                        lineage_id=event.lineage_id,
                    )
                )
                omission_feature_after_integration = sequence_neuron.state
                omission_readout_reception_count += 1
                schedule_readout(
                    event.timestamp,
                    (sequence_neuron.state, 1.0),
                    pending,
                )
                readout_emissions_following_omission += len(READOUT_NODES)
                return

            symbol = event.source.removeprefix("input:")
            if symbol not in ("A", "B"):
                raise ValueError(f"unexpected sequence input source {event.source!r}")
            seen_inputs.append(event)
            sequence_neuron.receive_event(event)
            if len(seen_inputs) == 1:
                target_key = f"next_after_{symbol}"
                prediction = predictor.create_prediction(
                    target_key,
                    model.next_symbol_weights[symbol],  # type: ignore[index]
                    timestamp=event.timestamp,
                    expected_resolution_at=deadline_timestamp,
                    expires_at=deadline_timestamp,
                )
                prediction_created_count += 1
                if ppc11_capture is not None:
                    ppc11_capture.prediction_created(prediction)
                prediction_trace_id = f"next-event-trace:{prediction.prediction_id}"
                pending.push(
                    Event(
                        event.timestamp,
                        "sequence",
                        "prediction_ledger",
                        ELIGIBILITY_ACTIVITY_EVENT,
                        EligibilityActivity(prediction_trace_id, 1.0, prediction.prediction_id),
                        event_id=event.event_id,
                    )
                )
                internal_emissions += 1
                emitted = predictor.emit_prediction(
                    prediction,
                    pending,
                    "prediction_sink",
                    delay=config.prediction_emit_delay,
                )
                internal_emissions += 1
                return

            if len(seen_inputs) != 2 or prediction is None:
                raise RuntimeError("sequence runtime received more than two input events")
            observation_symbol = symbol
            observation_event_id = str(event.event_id)
            observation_source = event.source
            observation_timestamp = event.timestamp
            observation = Event(
                event.timestamp,
                event.source,
                predictor.predictor_id,
                "observation",
                Observation(f"next_after_{seen_inputs[0].source.removeprefix('input:')}", SYMBOL_CODE[symbol]),  # type: ignore[arg-type]
                event_id=event.event_id,
            )
            resolution = predictor.process_observation(observation, pending, topology)
            if resolution.status != "matched" or resolution.error is None:
                raise RuntimeError(f"next-symbol observation did not match: {resolution.status}")
            prediction_error = resolution.error
            prediction_matched_count += 1
            if ppc11_capture is not None:
                ppc11_capture.prediction_matched(prediction.prediction_id, symbol, event.timestamp)
            routed_events += len(topology.outgoing(predictor_id))
            internal_emissions += 1
            return

        if event.destination == "observation_deadline":
            if not isinstance(event.payload, ExternalObservationDeadline):
                raise TypeError("completion event must be an external observation deadline")
            if len(seen_inputs) not in (1, 2):
                raise RuntimeError("common observation deadline arrived before the first routed input")
            state_before_silence = sequence_neuron.state
            if not silence_information_ablation:
                sequence_neuron.advance_state(deadline_timestamp - sequence_neuron.clock.timestamp)
            state_at_deadline = sequence_neuron.state
            if len(seen_inputs) == 1:
                first_symbol = seen_inputs[0].source.removeprefix("input:")
                observation_symbol = None
                observation_event_id = f"{example_id}:deadline:missed-second-event"
                observation_source = "observation_deadline:missed_second_event"
                observation_timestamp = event.timestamp
                absence_observation = Event(
                    event.timestamp,
                    observation_source,
                    predictor.predictor_id,
                    "observation",
                    Observation(f"next_after_{first_symbol}", 0.0),
                    event_id=observation_event_id,
                )
                record_synthetic_event(absence_observation)
                resolution = predictor.process_observation(absence_observation, pending, topology)
                if resolution.status != "matched" or resolution.error is None:
                    raise RuntimeError(f"deadline omission did not resolve the pending prediction: {resolution.status}")
                prediction_error = resolution.error
                prediction_matched_count += 1
                routed_events += len(topology.outgoing(predictor_id))
                internal_emissions += 1
                if omission_error_route_enabled:
                    return

            schedule_readout(event.timestamp, (state_at_deadline, 1.0), pending)
            return

        if event.destination in READOUT_NODES:
            class_index = READOUT_NODES.index(event.destination)
            readout_outputs[class_index] = readout_neurons[event.destination].receive_event(event)
            if ppc11_capture is not None:
                ppc11_capture.emit("readout_activation", decision_id=f"{exposure_id}:readout",
                                   class_index=class_index, pre_transfer=event.payload,
                                   post_transfer=readout_outputs[class_index])
            readout_emissions.append({"class_index": class_index, "event_id": event.event_id,
                                      "output_at": event.timestamp,
                                      "payload": event.payload,
                                      "activation": readout_outputs[class_index]})
            readout_events += 1
            if len(readout_outputs) < len(READOUT_NODES):
                return
            if len(readout_outputs) != len(READOUT_NODES) or readout_features is None:
                raise RuntimeError("four-class readout did not receive exactly four channel events")
            predicted_class = max(readout_outputs, key=readout_outputs.__getitem__)
            if ppc11_capture is not None:
                best_score = readout_outputs[predicted_class]
                tie_set = tuple(index for index in readout_outputs if readout_outputs[index] == best_score)
                ppc11_capture.emit("readout_decision", decision_id=f"{exposure_id}:readout",
                                   winner=predicted_class, tie_set=tie_set,
                                   tie_break_order=tuple(readout_outputs),
                                   tie_break_result=predicted_class)
            channel_eligibility = tuple(
                1.0 if readout_arm != "A" or index == predicted_class else 0.0
                for index in range(len(READOUT_NODES))
            )  # type: ignore[assignment]
            readout_timestamp = event.timestamp
            readout_prediction = predictor.create_prediction(
                "four_class_sequence_completion",
                float(predicted_class),
                timestamp=event.timestamp,
                expected_resolution_at=event.timestamp + config.reward_delay,
                expires_at=event.timestamp + config.reward_delay * 2.0,
            )
            if ppc11_capture is not None:
                ppc11_capture.prediction_created(readout_prediction)
            emitted = predictor.emit_prediction(
                readout_prediction,
                pending,
                "readout_prediction_sink",
                delay=config.readout_prediction_delay,
            )
            internal_emissions += 1
            for ledger, kind in (
                ("readout_weight_ledger", "weight"),
                ("readout_bias_ledger", "bias"),
            ):
                trace_id = f"{kind}-trace:{readout_prediction.prediction_id}"
                pending.push(
                    Event(
                        event.timestamp,
                        "readout",
                        ledger,
                        ELIGIBILITY_ACTIVITY_EVENT,
                        EligibilityActivity(trace_id, 1.0, readout_prediction.prediction_id),
                        event_id=f"{exposure_id}:{kind}-eligibility",
                    )
                )
                internal_emissions += 1
            if feedback_label is not None:
                reward_value = 1.0 if predicted_class == feedback_label else -1.0
                reward_timestamp = event.timestamp + config.reward_delay
                routed_reward = topology.route(
                    Event(
                        event.timestamp,
                        "outcome",
                        "outcome",
                        REWARD_EVENT,
                        RewardSignal(
                            reward_value,
                            message_id=f"reward:{exposure_id}",
                            prediction_id=readout_prediction.prediction_id,
                        ),
                        event_id=f"{exposure_id}:delayed-reward",
                    ),
                    pending,
                )
                if ppc11_capture is not None:
                    for feedback_event in routed_reward:
                        ppc11_capture.emit(
                            "feedback_schedule", feedback_id=feedback_event.payload.message_id,
                            origin_id=feedback_event.payload.prediction_id,
                            due_at=feedback_event.timestamp, scheduled_at=event.timestamp,
                            sign=1 if feedback_event.payload.reward >= 0 else -1,
                            magnitude=abs(feedback_event.payload.reward))
                routed_events += len(routed_reward)
                internal_emissions += len(routed_reward)
                if corrective_feedback_enabled:
                    correction_message_id = f"correction:{exposure_id}"
                    correction_event_id = (
                        f"{exposure_id}:corrective-feedback:{readout_prediction.prediction_id}"
                    )
                    correction_signs_for_target = tuple(
                        1 if index == feedback_label else -1
                        for index in range(len(READOUT_NODES))
                    )
                    routed_correction = topology.route(
                        Event(
                            event.timestamp,
                            "training_feedback",
                            "readout_correction_ledger",
                            "luna70_corrective_feedback",
                            Luna70CorrectiveFeedback(
                                correction_message_id,
                                readout_prediction.prediction_id,
                                feedback_label,
                                correction_signs_for_target,  # type: ignore[arg-type]
                            ),
                            event_id=correction_event_id,
                            lineage_id=readout_prediction.prediction_id,
                        ),
                        pending,
                    )
                    if len(routed_correction) != 1:
                        raise RuntimeError("corrective feedback did not traverse exactly one bounded route")
                    routed_events += len(routed_correction)
                    internal_emissions += len(routed_correction)
            return

        if event.destination == "prediction_sink":
            if not isinstance(event.payload, Prediction):
                raise TypeError("prediction sink received an invalid payload")
            if prediction is None or event.payload.prediction_id != prediction.prediction_id:
                raise RuntimeError("prediction sink received an untracked prediction")
            prediction_sink_timestamp = event.timestamp
            prediction_events += 1
            next_symbol_prediction_events += 1
            return

        if event.destination == "readout_prediction_sink":
            if not isinstance(event.payload, Prediction) or readout_prediction is None:
                raise TypeError("readout prediction sink received an invalid payload")
            if event.payload.prediction_id != readout_prediction.prediction_id:
                raise RuntimeError("readout prediction sink received an unexpected identity")
            readout_prediction_sink_timestamp = event.timestamp
            prediction_events += 1
            readout_prediction_events += 1
            return

        if event.destination == "readout_correction_ledger":
            if (
                event.event_type != "luna70_corrective_feedback"
                or not isinstance(event.payload, Luna70CorrectiveFeedback)
                or not corrective_feedback_enabled
                or event.payload.message_id != correction_message_id
                or event.event_id != correction_event_id
                or readout_prediction is None
                or event.payload.prediction_id != readout_prediction.prediction_id
                or event.lineage_id != readout_prediction.prediction_id
                or event.payload.target_class != feedback_label
            ):
                raise RuntimeError("invalid or unexpected corrective feedback event")
            if correction_signal is not None:
                raise RuntimeError("duplicate corrective feedback event")
            correction_signal = event.payload
            if ppc11_capture is not None:
                ppc11_capture.feedback_applied(
                    event.payload.message_id, event.payload.prediction_id, event.timestamp,
                    event.payload.correction_signs, 1.0, event.timestamp)
            correction_event_count += 1
            apply_corrective_if_ready(event.timestamp)
            return

        if event.destination == "prediction_ledger":
            if event.event_type == ELIGIBILITY_ACTIVITY_EVENT:
                if ppc11_capture is not None:
                    created_trace, existing_trace, previous_occupancy = (
                        prediction_ledger.record_activity_with_admission(event)
                    )
                    ppc11_capture.emit(
                        "eligibility_admission", trace_id=created_trace.trace_id,
                        owner=prediction_ledger.ledger_id, capacity=prediction_ledger.max_traces,
                        occupancy_before=previous_occupancy, decision="ADMITTED",
                        reason="existing_trace" if existing_trace else "capacity_available")
                    ppc11_capture.emit(
                        "eligibility_create", trace_id=created_trace.trace_id,
                        owner=prediction_ledger.ledger_id, trace_kind="prediction_error",
                        value=created_trace.value, created_at=created_trace.last_timestamp,
                        expires_at=(None if prediction_ledger.expiry is None else
                                    created_trace.last_timestamp + prediction_ledger.expiry))
                else:
                    prediction_ledger.record_activity(event)
                return
            if event.event_type != PREDICTION_ERROR_EVENT or not isinstance(event.payload, PredictionError):
                raise TypeError("prediction ledger received an unsupported event")
            attribution = prediction_ledger.apply_signal(event)
            if prediction is None or attribution.status != "matched" or attribution.trace_id != prediction_trace_id:
                raise RuntimeError(f"prediction error did not match the local trace: {attribution.status}")
            prediction_error_attribution = attribution
            prediction_error_events += 1
            if not seen_inputs:
                raise RuntimeError("prediction credit arrived without a local first-symbol context")
            first_symbol = seen_inputs[0].source.removeprefix("input:")
            before = model.next_symbol_weights[first_symbol]  # type: ignore[index]
            if learning_enabled:
                model.next_symbol_weights[first_symbol] = _clamp(
                    before + config.prediction_learning_rate * attribution.credit,
                    -1.0,
                    1.0,
                )
                if ppc11_capture is not None:
                    ppc11_capture.parameter_transition(
                        f"next_symbol_weights.{first_symbol}", "weight", before,
                        model.next_symbol_weights[first_symbol], event.destination, event.timestamp)
            if (
                omission_error_route_enabled
                and event.payload.observation_source == "observation_deadline:missed_second_event"
            ):
                if event.payload.prediction_id in omission_routed_prediction_ids:
                    duplicate_omission_error_deliveries += 1
                    raise RuntimeError("omission error was routed more than once for one prediction")
                omission_routed_prediction_ids.add(event.payload.prediction_id)
                predicted_symbol: InputSymbol = "A" if event.payload.predicted_value >= 0.0 else "B"
                omission_signal = OmissionErrorSignal(
                    prediction_id=event.payload.prediction_id,
                    target_key=event.payload.target_key,
                    predicted_symbol=predicted_symbol,
                    predicted_value=event.payload.predicted_value,
                    observed_value=event.payload.observed_value,
                    error_value=event.payload.error,
                    prediction_timestamp=event.payload.prediction_timestamp,
                    resolution_timestamp=event.payload.observation_timestamp,
                    resolution_source=event.payload.observation_source,
                )
                omission_error_route_event_id = (
                    f"{exposure_id}:omission-error:{event.payload.prediction_id}"
                )
                omission_error_lineage_id = event.payload.prediction_id
                routed_omission = topology.route(
                    Event(
                        event.timestamp,
                        event.destination,
                        "sequence",
                        "prediction_omission_error",
                        omission_signal,
                        event_id=omission_error_route_event_id,
                        lineage_id=omission_error_lineage_id,
                    ),
                    pending,
                )
                if len(routed_omission) != 1:
                    raise RuntimeError("omission error did not traverse exactly one bounded route")
                if ppc11_capture is not None:
                    routed_event = routed_omission[0]
                    ppc11_capture.emit(
                        "omission_route", prediction_id=event.payload.prediction_id,
                        route=[routed_event.source, routed_event.destination],
                        payload=routed_event.payload, event_id=routed_event.event_id,
                        routed_at=routed_event.timestamp)
                    ppc11_capture.gap(
                        "P04", "payload.omitted_symbol", "prediction_ledger omission-resolution branch",
                        "the source carries a missed-event observation but does not expose the omitted target symbol without external label information")
                omission_error_route_count += 1
                routed_events += len(routed_omission)
                internal_emissions += len(routed_omission)
            return

        if event.destination in ("readout_weight_ledger", "readout_bias_ledger"):
            ledger = weight_ledger if event.destination == "readout_weight_ledger" else bias_ledger
            if event.event_type == ELIGIBILITY_ACTIVITY_EVENT:
                if ppc11_capture is not None:
                    created_trace, existing_trace, previous_occupancy = (
                        ledger.record_activity_with_admission(event)
                    )
                    ppc11_capture.emit(
                        "eligibility_admission", trace_id=created_trace.trace_id,
                        owner=ledger.ledger_id, capacity=ledger.max_traces,
                        occupancy_before=previous_occupancy, decision="ADMITTED",
                        reason="existing_trace" if existing_trace else "capacity_available")
                    ppc11_capture.emit(
                        "eligibility_create", trace_id=created_trace.trace_id,
                        owner=ledger.ledger_id,
                        trace_kind="weight" if ledger.ledger_id == "readout_weight_ledger" else "bias",
                        value=created_trace.value, created_at=created_trace.last_timestamp,
                        expires_at=(None if ledger.expiry is None else
                                    created_trace.last_timestamp + ledger.expiry))
                else:
                    ledger.record_activity(event)
                return
            if event.event_type != REWARD_EVENT or not isinstance(event.payload, RewardSignal):
                raise TypeError("readout ledger received an unsupported event")
            attribution = ledger.apply_signal(event)
            if ppc11_capture is not None and event.payload.message_id is not None:
                ppc11_capture.feedback_applied(
                    event.payload.message_id, event.payload.prediction_id or "unknown-origin",
                    event.timestamp, 1 if event.payload.reward >= 0 else -1,
                    abs(event.payload.reward), reward_timestamp if reward_timestamp is not None else event.timestamp)
                ppc11_capture.emit(
                    "eligibility_consume", trace_id=attribution.trace_id,
                    owner=ledger.ledger_id, consumed_at=event.timestamp,
                    value=attribution.eligibility, outcome=attribution.status)
            expected_trace = (
                f"weight-trace:{readout_prediction.prediction_id}"
                if event.destination == "readout_weight_ledger" and readout_prediction is not None
                else f"bias-trace:{readout_prediction.prediction_id}"
                if readout_prediction is not None
                else None
            )
            if (
                attribution.status != "matched"
                or attribution.trace_id != expected_trace
                or readout_prediction is None
                or event.payload.prediction_id != readout_prediction.prediction_id
                or event.payload.message_id != f"reward:{exposure_id}"
            ):
                if attribution.status == "duplicate":
                    duplicate_reward_applications += 1
                raise RuntimeError(f"four-class delayed reward attribution failed: {attribution.status}")
            reward_attributions[event.destination] = attribution
            reward_events += 1
            if predicted_class is None or readout_features is None:
                raise RuntimeError("delayed class reward arrived before the readout decision")
            if corrective_feedback_enabled:
                apply_corrective_if_ready(event.timestamp)
                return
            feedback_applied_at = event.timestamp
            correction_signs = tuple(
                (1 if predicted_class == feedback_label else -1)
                if index == predicted_class and feedback_label is not None
                else 0
                for index in range(len(READOUT_NODES))
            )  # type: ignore[assignment]
            update_scale = config.readout_learning_rate * attribution.credit
            if event.destination == "readout_weight_ledger":
                weights_before = tuple(model.readout_weights)
                if learning_enabled:
                    old_weights = tuple(model.readout_weights)
                    for index, eligibility in enumerate(channel_eligibility):
                        if eligibility == 0.0 or index != predicted_class:
                            continue
                        delta = update_scale * readout_features[0]
                        model.readout_weights[index] = _clamp(
                            model.readout_weights[index] + delta * eligibility, -3.0, 3.0
                        )
                        if ppc11_capture is not None:
                            ppc11_capture.parameter_transition(
                                f"readout_weights.{index}", "weight", old_weights[index],
                                model.readout_weights[index], event.destination, event.timestamp)
                    weight_update_deltas = tuple(
                        after - before for before, after in zip(old_weights, model.readout_weights)
                    )  # type: ignore[assignment]
                weights_after = tuple(model.readout_weights)
            else:
                biases_before = tuple(model.readout_biases)
                if learning_enabled:
                    old_biases = tuple(model.readout_biases)
                    for index, eligibility in enumerate(channel_eligibility):
                        if eligibility == 0.0 or index != predicted_class:
                            continue
                        delta = update_scale
                        model.readout_biases[index] = _clamp(
                            model.readout_biases[index] + delta * eligibility, -3.0, 3.0
                        )
                        if ppc11_capture is not None:
                            ppc11_capture.parameter_transition(
                                f"readout_biases.{index}", "bias", old_biases[index],
                                model.readout_biases[index], event.destination, event.timestamp)
                    bias_update_deltas = tuple(
                        after - before for before, after in zip(old_biases, model.readout_biases)
                    )  # type: ignore[assignment]
                biases_after = tuple(model.readout_biases)
            return

        raise ValueError(f"event addressed to unknown four-class component {event.destination!r}")

    execution = execute_bounded(queue, handle, event_budget=config.event_budget_per_example)
    if not execution.completed:
        raise RuntimeError(
            f"bounded event budget exhausted for {exposure_id}: "
            f"processed={execution.processed_event_count}, pending={execution.pending_event_count}"
        )
    if (
        len(seen_inputs) != len(inputs)
        or len(seen_inputs) not in (1, 2)
        or prediction is None
        or prediction_created_count != 1
        or prediction_matched_count != 1
        or prediction_error is None
        or prediction_error_attribution is None
        or predicted_class is None
        or len(readout_outputs) != 4
        or readout_features is None
        or readout_timestamp is None
        or readout_prediction is None
        or state_before_silence is None
        or state_at_deadline is None
        or observation_event_id is None
        or observation_source is None
        or observation_timestamp is None
        or prediction_sink_timestamp is None
        or readout_prediction_sink_timestamp is None
        or prediction_error_events != 1
    ):
        raise RuntimeError(f"incomplete variable-length sequence execution {exposure_id}")
    if feedback_label is not None and (
        set(reward_attributions) != {"readout_weight_ledger", "readout_bias_ledger"}
        or len(reward_attributions) != 2
    ):
        raise RuntimeError(
            "training reward was not attributed once to each distinct local readout ledger: "
            f"{sorted(reward_attributions)}"
        )
    if feedback_label is None and reward_attributions:
        raise RuntimeError("inference received a task reward")
    if corrective_feedback_enabled and (
        correction_event_count != 1
        or correction_signal is None
        or correction_event_id is None
        or correction_message_id is None
        or feedback_applied_at is None
        or reward_timestamp is None
        or feedback_applied_at < reward_timestamp
    ):
        raise RuntimeError("corrective feedback was not causally applied once at its delayed time")
    if not corrective_feedback_enabled and correction_event_count:
        raise RuntimeError("an unenabled corrective feedback event was processed")

    second_event = seen_inputs[1] if len(seen_inputs) == 2 else None
    is_omission = second_event is None
    if is_omission and omission_error_route_enabled:
        if (
            omission_signal is None
            or omission_error_route_count != 1
            or omission_error_route_delivery_count != 1
            or omission_readout_reception_count != 1
            or readout_emissions_following_omission != len(READOUT_NODES)
            or omission_error_delivery_timestamp is None
            or readout_timestamp <= omission_error_delivery_timestamp
            or omission_feature_before_integration is None
            or omission_feature_after_integration is None
        ):
            raise RuntimeError("routed singleton omission did not causally precede its readout")
    elif (
        omission_error_route_count
        or omission_error_route_delivery_count
        or omission_readout_reception_count
        or readout_emissions_following_omission
        or omission_signal is not None
    ):
        raise RuntimeError("omission-error route was used outside an enabled singleton resolution")
    if duplicate_omission_error_deliveries:
        raise RuntimeError("duplicate omission-error delivery was detected")

    resolution_timestamp = observation_timestamp
    resolution_source = observation_source
    resolved_target = (
        None if second_event is None else second_event.source.removeprefix("input:")
    )
    if ppc11_capture is not None:
        ppc11_capture.emit("classification_output", predicted_class=predicted_class,
                           output_at=readout_timestamp, emissions=readout_emissions)
        final_parameters = model.snapshot()
        final_digest = hashlib.sha256(json.dumps(
            final_parameters, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")).hexdigest()
        ppc11_capture.emit("parameter_final", manifest_sha256=final_digest,
                           parameters=final_parameters)
        for item, path_name, reason in (
            ("P03", "prediction_expire", "expiry/settlement state is internal to LocalPredictor and not observed here"),
            ("P03", "prediction_settle", "readout prediction settlement is not exposed by this source path"),
            ("P04", "omitted_symbol", "the absent target symbol is not available to this model-visible source path without external label information"),
            ("P07", "eligibility_lifecycle", "ledger trace expiry/admission/consumption transitions are not fully captured"),
            ("P08", "feedback_lifecycle", "feedback scheduling, duplicates, and rejection outcomes are not fully captured"),
            ("P09", "parameter_transition", "initial/final snapshots are observed; no complete next-symbol update ordering is exposed by this path"),
        ):
            ppc11_capture.gap(item, path_name, "run_example source transitions", reason)
        ppc11_capture.unavailable_branches()
    next_symbol_prediction = "A" if prediction.predicted_value >= 0 else "B"
    anticipatory_prediction = (
        second_event is not None and prediction_sink_timestamp < second_event.timestamp
    )
    scores = tuple(readout_outputs[index] for index in range(4))
    score_margins = tuple(
        scores[index] - max(scores[other] for other in range(4) if other != index)
        for index in range(4)
    )
    return SequenceResult(
        example_id=example_id,
        predicted_class=predicted_class,
        prediction_scores=scores,  # type: ignore[arg-type]
        readout_input_features=readout_features,
        readout_score_margins=score_margins,  # type: ignore[arg-type]
        final_sequence_state=sequence_neuron.state,
        state_before_silence=state_before_silence,
        state_after_silence=state_at_deadline,
        silence_state_decay=state_before_silence - state_at_deadline,
        silence_state_integrated=not silence_information_ablation,
        completion_trigger="external_common_observation_deadline",
        completion_deadline=deadline_timestamp,
        first_event_timestamp=first_event.timestamp,
        first_event_network_timestamp=seen_inputs[0].timestamp,
        first_event_id=seen_inputs[0].event_id,  # type: ignore[arg-type]
        event_count=len(seen_inputs),
        second_event_id=None if second_event is None else second_event.event_id,
        second_event_timestamp=None if second_event is None else second_event.timestamp,
        prediction_id=prediction.prediction_id,
        prediction_value=prediction.predicted_value,
        prediction_emitted_at=prediction_sink_timestamp,
        prediction_target_symbol=next_symbol_prediction,
        prediction_resolution_source=resolution_source,
        prediction_resolution_event_id=observation_event_id,
        prediction_resolution_timestamp=resolution_timestamp,
        prediction_error=prediction_error.error,
        prediction_error_eligibility=prediction_error_attribution.eligibility,
        prediction_error_credit=prediction_error_attribution.credit,
        prediction_created_count=prediction_created_count,
        prediction_matched_count=prediction_matched_count,
        prediction_expired_count=predictor.expired_count,
        prediction_omitted_count=int(is_omission),
        omission_error_route_enabled=omission_error_route_enabled,
        omission_error_route_event_id=omission_error_route_event_id,
        omission_error_lineage_id=omission_error_lineage_id,
        omission_error_prediction_id=None if omission_signal is None else omission_signal.prediction_id,
        omission_error_predicted_symbol=omission_error_predicted_symbol,
        omission_error_value=omission_error_value,
        omission_error_delivery_timestamp=omission_error_delivery_timestamp,
        omission_error_event_count=omission_error_route_count,
        omission_error_route_delivery_count=omission_error_route_delivery_count,
        omission_readout_reception_count=omission_readout_reception_count,
        readout_emissions_following_omission=readout_emissions_following_omission,
        duplicate_omission_error_deliveries=duplicate_omission_error_deliveries,
        omission_feature_before_integration=omission_feature_before_integration,
        omission_feature_after_integration=omission_feature_after_integration,
        readout_prediction_id=readout_prediction.prediction_id,
        readout_timestamp=readout_timestamp,
        reward_delivered=len(reward_attributions) == 2,
        reward_message_id=None if reward_value is None else f"reward:{exposure_id}",
        reward_value=reward_value,
        reward_timestamp=reward_timestamp,
        reward_attribution_statuses=tuple(
            reward_attributions[key].status
            for key in ("readout_weight_ledger", "readout_bias_ledger")
            if key in reward_attributions
        ),
        reward_prediction_id=readout_prediction.prediction_id if reward_value is not None else None,
        reward_trace_ids=tuple(
            reward_attributions[key].trace_id or ""
            for key in ("readout_weight_ledger", "readout_bias_ledger")
            if key in reward_attributions
        ),
        reward_eligibilities=tuple(
            reward_attributions[key].eligibility
            for key in ("readout_weight_ledger", "readout_bias_ledger")
            if key in reward_attributions
        ),
        reward_credits=tuple(
            reward_attributions[key].credit
            for key in ("readout_weight_ledger", "readout_bias_ledger")
            if key in reward_attributions
        ),
        readout_weights_before=weights_before,
        readout_weights_after=weights_after,
        readout_biases_before=biases_before,
        readout_biases_after=biases_after,
        readout_arm=readout_arm,
        channel_eligibility=channel_eligibility,
        weight_update_deltas=weight_update_deltas,
        bias_update_deltas=bias_update_deltas,
        correction_signs=correction_signs,
        feedback_applied_at=feedback_applied_at,
        correction_message_id=correction_message_id,
        correction_event_id=correction_event_id,
        correction_event_count=correction_event_count,
        input_events=len(inputs),
        external_deadline_events=1,
        internal_emissions=internal_emissions,
        routed_events=routed_events,
        prediction_events=prediction_events,
        next_symbol_prediction_events=next_symbol_prediction_events,
        readout_prediction_events=readout_prediction_events,
        prediction_error_events=prediction_error_events,
        readout_events=readout_events,
        reward_events=reward_events,
        processed_events=execution.processed_event_count,
        peak_queue_occupancy=execution.peak_queue_occupancy,
        local_energy_proxy=sequence_neuron.energy_state
        + sum(neuron.energy_state for neuron in readout_neurons.values()),
        dropped_events=0,
        admission_failures=0,
        duplicate_reward_applications=duplicate_reward_applications,
        event_trace=tuple(trace),
    )


def _confusion_summary(examples: tuple[TemporalSequenceExample, ...], results: tuple[SequenceResult, ...]) -> dict[str, Any]:
    if len(examples) != len(results) or not examples:
        raise ValueError("every example must have exactly one prediction")
    matrix = [[0 for _ in CLASS_NAMES] for _ in CLASS_NAMES]
    for example, result in zip(examples, results):
        matrix[example.label][result.predicted_class] += 1
    per_class = {}
    for label, name in CLASS_NAMES.items():
        true_positive = matrix[label][label]
        support = sum(matrix[label])
        predicted = sum(matrix[row][label] for row in range(4))
        per_class[name] = {
            "label": label,
            "support": support,
            "correct": true_positive,
            "accuracy": true_positive / support,
            "recall": true_positive / support,
            "precision": true_positive / predicted if predicted else 0.0,
            "predicted_count": predicted,
            "wilson_95": wilson_interval(true_positive, support),
        }

    sequence_indices = [index for index, example in enumerate(examples) if example.label in (0, 1)]
    prediction_examples = [
        (examples[index], results[index])
        for index in sequence_indices
        if results[index].second_event_id is not None
    ]
    prediction_correct = sum(
        result.prediction_target_symbol
        == examples[index].events[1].source.removeprefix("input:")
        for index, result in enumerate(results)
        if result.second_event_id is not None
    )
    singleton_indices = [index for index, example in enumerate(examples) if example.label in (2, 3)]
    singleton_correct = sum(
        results[index].predicted_class == examples[index].label for index in singleton_indices
    )
    correct = sum(matrix[label][label] for label in range(4))
    total = len(examples)
    return {
        "examples": total,
        "correct": correct,
        "accuracy": correct / total,
        "accuracy_wilson_95": wilson_interval(correct, total),
        "confusion_matrix_rows_true_columns_predicted": matrix,
        "class_names_by_index": CLASS_NAMES,
        "per_class": per_class,
        "singleton_examples": len(singleton_indices),
        "singleton_correct": singleton_correct,
        "singleton_accuracy": singleton_correct / len(singleton_indices) if singleton_indices else None,
        "singleton_per_class": {
            name: per_class[name]
            for name in ("A_only", "B_only")
        },
        "sequence_examples_with_second_event": len(prediction_examples),
        "anticipatory_prediction_attempts": sum(
            result.next_symbol_prediction_events for result in results
        ),
        "anticipatory_prediction_coverage_over_all": sum(
            result.next_symbol_prediction_events for result in results
        ) / total,
        "anticipatory_prediction_coverage_over_two_event_sequences": (
            sum(
                result.next_symbol_prediction_events
                for result in results
                if result.second_event_id is not None
            ) / len(prediction_examples)
            if prediction_examples
            else None
        ),
        "singleton_next_symbol_prediction_attempts": sum(
            result.next_symbol_prediction_events
            for result in results
            if result.event_count == 1
        ),
        "anticipatory_prediction_correct": prediction_correct,
        "anticipatory_prediction_accuracy": (
            prediction_correct / len(prediction_examples) if prediction_examples else None
        ),
        "anticipatory_prediction_accuracy_wilson_95": (
            wilson_interval(prediction_correct, len(prediction_examples)) if prediction_examples else None
        ),
        "missed_prediction_resolved_as_silence": sum(
            result.event_count == 1
            and result.prediction_resolution_source == "observation_deadline:missed_second_event"
            for result in results
        ),
        "readout_coverage": sum(result.predicted_class is not None for result in results) / total,
        "mean_processed_events": sum(result.processed_events for result in results) / total,
        "mean_input_events": sum(result.input_events for result in results) / total,
        "total_external_deadline_events": sum(result.external_deadline_events for result in results),
        "total_internal_emissions": sum(result.internal_emissions for result in results),
        "total_routed_events": sum(result.routed_events for result in results),
        "total_prediction_events": sum(result.prediction_events for result in results),
        "total_next_symbol_prediction_events": sum(
            result.next_symbol_prediction_events for result in results
        ),
        "total_readout_prediction_events": sum(
            result.readout_prediction_events for result in results
        ),
        "total_prediction_error_events": sum(result.prediction_error_events for result in results),
        "total_readout_events": sum(result.readout_events for result in results),
        "total_reward_events": sum(result.reward_events for result in results),
        "max_peak_queue_occupancy": max(result.peak_queue_occupancy for result in results),
        "dropped_events": sum(result.dropped_events for result in results),
        "admission_failures": sum(result.admission_failures for result in results),
        "duplicate_reward_applications": sum(result.duplicate_reward_applications for result in results),
        "prediction_lifecycle": {
            "created": sum(result.prediction_created_count for result in results),
            "matched": sum(result.prediction_matched_count for result in results),
            "expired": sum(result.prediction_expired_count for result in results),
            "omitted": sum(result.prediction_omitted_count for result in results),
        },
        "omission_error_route": {
            "enabled": all(result.omission_error_route_enabled for result in results),
            "route_events_created": sum(result.omission_error_event_count for result in results),
            "route_events_delivered": sum(result.omission_error_route_delivery_count for result in results),
            "readout_receptions_after_omission": sum(
                result.omission_readout_reception_count for result in results
            ),
            "readout_emissions_following_omission": sum(
                result.readout_emissions_following_omission for result in results
            ),
            "duplicate_deliveries": sum(
                result.duplicate_omission_error_deliveries for result in results
            ),
            "singleton_omission_examples": sum(
                result.event_count == 1 for result in results
            ),
            "singleton_examples_integrated": sum(
                result.omission_readout_reception_count == 1 for result in results
            ),
            "mean_readout_delay_after_omission_delivery": (
                sum(
                    result.readout_timestamp - result.omission_error_delivery_timestamp
                    for result in results
                    if result.omission_error_delivery_timestamp is not None
                )
                / sum(result.omission_readout_reception_count for result in results)
                if sum(result.omission_readout_reception_count for result in results)
                else None
            ),
            "mean_absolute_neural_state_change_from_omission": (
                sum(
                    abs(result.omission_feature_after_integration - result.omission_feature_before_integration)
                    for result in results
                    if result.omission_feature_before_integration is not None
                    and result.omission_feature_after_integration is not None
                )
                / sum(result.omission_readout_reception_count for result in results)
                if sum(result.omission_readout_reception_count for result in results)
                else None
            ),
        },
        "mean_local_energy_proxy_per_example": sum(result.local_energy_proxy for result in results) / total,
        "mean_prediction_lead_time": (
            sum(
                result.second_event_timestamp - result.prediction_emitted_at
                for result in results
                if result.second_event_timestamp is not None
            ) / len(prediction_examples)
            if prediction_examples
            else None
        ),
        "mean_singleton_prediction_to_deadline_interval": (
            sum(
                result.completion_deadline - result.prediction_emitted_at
                for result in results
                if result.event_count == 1
            ) / len(singleton_indices)
            if singleton_indices
            else None
        ),
        "silence_state_integrated_examples": sum(result.silence_state_integrated for result in results),
        "mean_absolute_silence_state_decay": sum(abs(result.silence_state_decay) for result in results) / total,
    }


def _evaluate(
    model: FourClassTaskModel,
    examples: tuple[TemporalSequenceExample, ...],
    *,
    config: Luna67Config,
    condition: Condition,
    seed: int,
    destroy_temporal_order: bool = False,
    silence_information_ablation: bool = False,
    omission_error_route_enabled: bool = False,
    retain_event_trace: bool = False,
) -> tuple[dict[str, Any], tuple[SequenceResult, ...]]:
    before = model.snapshot()
    results = tuple(
        run_example(
            model,
            example_id=example.example_id,
            events=example.events,
            config=config,
            exposure_id=f"eval:{condition}:seed-{seed}:{example.example_id}",
            destroy_temporal_order=destroy_temporal_order,
            silence_information_ablation=silence_information_ablation,
            omission_error_route_enabled=omission_error_route_enabled,
            retain_event_trace=retain_event_trace,
        )
        for example in examples
    )
    if model.snapshot() != before:
        raise RuntimeError("validation/held-out evaluation mutated trainable parameters")
    return _confusion_summary(examples, results), results


def _paired_exact_p(discordant_a: int, discordant_b: int) -> float:
    total = discordant_a + discordant_b
    if total == 0:
        return 1.0
    lower_tail = min(discordant_a, discordant_b)
    tail_probability = sum(math.comb(total, index) for index in range(lower_tail + 1)) / (2 ** total)
    return min(1.0, 2.0 * tail_probability)


def _paired_comparison(
    examples: tuple[TemporalSequenceExample, ...],
    trained: tuple[SequenceResult, ...],
    control: tuple[SequenceResult, ...],
) -> dict[str, Any]:
    if len(examples) != len(trained) or len(examples) != len(control):
        raise ValueError("paired comparisons must use identical held-out examples")
    trained_only = control_only = 0
    for example, trained_result, control_result in zip(examples, trained, control):
        trained_correct = trained_result.predicted_class == example.label
        control_correct = control_result.predicted_class == example.label
        trained_only += int(trained_correct and not control_correct)
        control_only += int(control_correct and not trained_correct)
    return {
        "trained_correct_control_wrong": trained_only,
        "trained_wrong_control_correct": control_only,
        "mcnemar_exact_two_sided_p": _paired_exact_p(trained_only, control_only),
    }


def _train_condition(
    condition: Condition,
    *,
    seed: int,
    training_examples: tuple[TemporalSequenceExample, ...],
    config: Luna67Config,
    omission_error_route_enabled: bool = False,
) -> tuple[FourClassTaskModel, dict[str, Any], tuple[dict[str, Any], ...]]:
    model = FourClassTaskModel.untrained()
    if condition == "untrained":
        return model, {"epochs": 0, "epoch_metrics": []}, ()

    reward_labels = [example.label for example in training_examples]
    random.Random(seed + 900_001).shuffle(reward_labels)
    shuffled_feedback = {
        example.example_id: reward_labels[index]
        for index, example in enumerate(training_examples)
    }
    training_trace: list[dict[str, Any]] = []
    epoch_metrics: list[dict[str, Any]] = []
    for epoch in range(config.epochs):
        order = list(training_examples)
        random.Random(seed + 10_003 * (epoch + 1)).shuffle(order)
        epoch_results: list[tuple[TemporalSequenceExample, SequenceResult]] = []
        reward_matches = 0
        for example in order:
            feedback_label = (
                shuffled_feedback[example.example_id]
                if condition == "shuffled_rewards"
                else example.label
            )
            exposure_id = f"train:{condition}:seed-{seed}:epoch-{epoch}:{example.example_id}"
            result = run_example(
                model,
                example_id=example.example_id,
                events=example.events,
                config=config,
                exposure_id=exposure_id,
                feedback_label=feedback_label,
                learning_enabled=condition != "learning_disabled",
                destroy_temporal_order=condition == "temporal_order_destroyed",
                silence_information_ablation=condition == "silence_information_ablation",
                omission_error_route_enabled=omission_error_route_enabled,
                retain_event_trace=condition in ("trained", "silence_information_ablation"),
            )
            epoch_results.append((example, result))
            reward_matches += int(result.reward_delivered)
            for event_row in result.event_trace:
                event_row["example_id"] = example.example_id
                event_row["exposure_id"] = exposure_id
                training_trace.append({"record_type": "event", **event_row})
            training_trace.append(
                {
                    "record_type": "learning",
                    "example_id": example.example_id,
                    "exposure_id": exposure_id,
                    "scoring_label": example.label,
                    "feedback_label": feedback_label,
                    "true_sequence_length": len(example.events),
                    "predicted_class": result.predicted_class,
                    "prediction_id": result.prediction_id,
                    "prediction_value": result.prediction_value,
                    "prediction_emitted_at": result.prediction_emitted_at,
                    "prediction_resolution_source": result.prediction_resolution_source,
                    "prediction_resolution_event_id": result.prediction_resolution_event_id,
                    "prediction_resolution_timestamp": result.prediction_resolution_timestamp,
                    "prediction_error": result.prediction_error,
                    "prediction_error_eligibility": result.prediction_error_eligibility,
                    "prediction_error_credit": result.prediction_error_credit,
                    "prediction_created_count": result.prediction_created_count,
                    "prediction_matched_count": result.prediction_matched_count,
                    "prediction_expired_count": result.prediction_expired_count,
                    "prediction_omitted_count": result.prediction_omitted_count,
                    "omission_error_route_event_id": result.omission_error_route_event_id,
                    "omission_error_lineage_id": result.omission_error_lineage_id,
                    "omission_error_prediction_id": result.omission_error_prediction_id,
                    "omission_error_predicted_symbol": result.omission_error_predicted_symbol,
                    "omission_error_value": result.omission_error_value,
                    "omission_error_delivery_timestamp": result.omission_error_delivery_timestamp,
                    "omission_error_event_count": result.omission_error_event_count,
                    "omission_error_route_delivery_count": result.omission_error_route_delivery_count,
                    "omission_feature_before_integration": result.omission_feature_before_integration,
                    "omission_feature_after_integration": result.omission_feature_after_integration,
                    "readout_input_features": result.readout_input_features,
                    "prediction_scores": result.prediction_scores,
                    "readout_score_margins": result.readout_score_margins,
                    "readout_prediction_id": result.readout_prediction_id,
                    "readout_timestamp": result.readout_timestamp,
                    "next_symbol_prediction_events": result.next_symbol_prediction_events,
                    "readout_prediction_events": result.readout_prediction_events,
                    "reward_delivered": result.reward_delivered,
                    "reward_message_id": result.reward_message_id,
                    "reward_prediction_id": result.reward_prediction_id,
                    "reward_value": result.reward_value,
                    "reward_timestamp": result.reward_timestamp,
                    "reward_attribution_statuses": result.reward_attribution_statuses,
                    "reward_trace_ids": result.reward_trace_ids,
                    "reward_eligibilities": result.reward_eligibilities,
                    "reward_credits": result.reward_credits,
                    "readout_weights_before": result.readout_weights_before,
                    "readout_weights_after": result.readout_weights_after,
                    "readout_biases_before": result.readout_biases_before,
                    "readout_biases_after": result.readout_biases_after,
                    "input_events": result.input_events,
                    "external_deadline_events": result.external_deadline_events,
                    "internal_emissions": result.internal_emissions,
                    "routed_events": result.routed_events,
                    "prediction_events": result.prediction_events,
                    "prediction_error_events": result.prediction_error_events,
                    "readout_events": result.readout_events,
                    "reward_events": result.reward_events,
                    "processed_events": result.processed_events,
                    "peak_queue_occupancy": result.peak_queue_occupancy,
                    "duplicate_reward_applications": result.duplicate_reward_applications,
                }
            )
        correct = sum(result.predicted_class == example.label for example, result in epoch_results)
        epoch_metrics.append(
            {
                "epoch": epoch,
                "online_accuracy": correct / len(epoch_results),
                "correct": correct,
                "examples": len(epoch_results),
                "delayed_reward_decisions": reward_matches,
                "unique_readout_reward_applications": reward_matches * 2,
            }
        )
    return model, {"epochs": config.epochs, "epoch_metrics": epoch_metrics}, tuple(training_trace)


def _make_seed_datasets(seed: int, config: Luna67Config) -> dict[str, tuple[TemporalSequenceExample, ...]]:
    return {
        "train": generate_dataset(
            "train",
            per_class=config.train_per_class,
            seed=seed * 10_000 + 101,
            config=config,
        ),
        "validation": generate_dataset(
            "validation",
            per_class=config.validation_per_class,
            seed=seed * 10_000 + 211,
            config=config,
        ),
        "test": generate_dataset(
            "test",
            per_class=config.test_per_class,
            seed=seed * 10_000 + 307,
            config=config,
        ),
    }


def _first_event_distribution(examples: tuple[TemporalSequenceExample, ...]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for label, name in CLASS_NAMES.items():
        timestamps = [example.events[0].timestamp for example in examples if example.label == label]
        result[name] = {
            "count": len(timestamps),
            "mean": sum(timestamps) / len(timestamps),
            "minimum": min(timestamps),
            "maximum": max(timestamps),
        }
    return result


def run_experiment(
    config: Luna67Config | None = None,
    *,
    omission_error_route_enabled: bool = False,
) -> dict[str, Any]:
    config = Luna67Config() if config is None else config
    if not isinstance(omission_error_route_enabled, bool):
        raise TypeError("omission_error_route_enabled must be a bool")
    seed_results: list[dict[str, Any]] = []
    aggregate_correct = {condition: 0 for condition in CONDITIONS}
    aggregate_total = 0
    paired_rows: dict[str, list[tuple[int, int]]] = {
        condition: []
        for condition in CONDITIONS
        if condition != "trained"
    }
    aggregate_confusions = {
        condition: [[0 for _ in CLASS_NAMES] for _ in CLASS_NAMES]
        for condition in CONDITIONS
    }

    for seed in config.seeds:
        datasets = _make_seed_datasets(seed, config)
        dataset_manifests = {
            split: {
                "examples": len(examples),
                "class_counts": {
                    str(label): sum(example.label == label for example in examples)
                    for label in CLASS_NAMES
                },
                **dataset_hashes(examples),
                "first_event_timestamps_by_class": _first_event_distribution(examples),
            }
            for split, examples in datasets.items()
        }
        condition_results: dict[str, Any] = {}
        test_predictions: dict[str, tuple[SequenceResult, ...]] = {}
        frozen_test_examples = datasets["test"]

        for condition in CONDITIONS:
            model, training_report, training_trace = _train_condition(
                condition,
                seed=seed,
                training_examples=datasets["train"],
                config=config,
                omission_error_route_enabled=omission_error_route_enabled,
            )
            initial_parameters = FourClassTaskModel.untrained().snapshot()
            final_parameters = model.snapshot()
            destroy = condition == "temporal_order_destroyed"
            silence_ablation = condition == "silence_information_ablation"
            training_metrics, _ = _evaluate(
                model,
                datasets["train"],
                config=config,
                condition=condition,
                seed=seed,
                destroy_temporal_order=destroy,
                silence_information_ablation=silence_ablation,
                omission_error_route_enabled=omission_error_route_enabled,
            )
            validation_metrics, _ = _evaluate(
                model,
                datasets["validation"],
                config=config,
                condition=condition,
                seed=seed,
                destroy_temporal_order=destroy,
                silence_information_ablation=silence_ablation,
                omission_error_route_enabled=omission_error_route_enabled,
            )
            test_metrics, seed_test_predictions = _evaluate(
                model,
                frozen_test_examples,
                config=config,
                condition=condition,
                seed=seed,
                destroy_temporal_order=destroy,
                silence_information_ablation=silence_ablation,
                omission_error_route_enabled=omission_error_route_enabled,
                retain_event_trace=condition in ("trained", "silence_information_ablation"),
            )
            test_predictions[condition] = seed_test_predictions
            for row, values in enumerate(test_metrics["confusion_matrix_rows_true_columns_predicted"]):
                for column, value in enumerate(values):
                    aggregate_confusions[condition][row][column] += value
            aggregate_correct[condition] += test_metrics["correct"]
            condition_results[condition] = {
                "protocol": {
                    "training_labels_for_feedback": condition != "untrained",
                    "parameter_updates_enabled": condition not in ("learning_disabled", "untrained"),
                    "temporal_order_destroyed": destroy,
                    "silence_state_decay_ablation": silence_ablation,
                    "common_external_deadline_preserved": True,
                    "heldout_reward_enabled": False,
                },
                "training": training_report,
                "training_metrics_final_frozen": training_metrics,
                "validation_metrics": validation_metrics,
                "heldout_metrics": test_metrics,
                "initial_parameters": initial_parameters,
                "final_parameters": final_parameters,
                "training_trace": training_trace,
                "heldout_predictions": [
                    {
                        "example_id": example.example_id,
                        "label_for_scoring": example.label,
                        "true_sequence_length": len(example.events),
                        "first_event_timestamp": result.first_event_timestamp,
                        "first_event_network_timestamp": result.first_event_network_timestamp,
                        "completion_deadline": result.completion_deadline,
                        "predicted_class": result.predicted_class,
                        "correct": result.predicted_class == example.label,
                        "final_sequence_state": result.final_sequence_state,
                        "readout_input_features": result.readout_input_features,
                        "prediction_scores": result.prediction_scores,
                        "readout_score_margins": result.readout_score_margins,
                        "state_before_silence": result.state_before_silence,
                        "state_after_silence": result.state_after_silence,
                        "silence_state_decay": result.silence_state_decay,
                        "prediction_id": result.prediction_id,
                        "prediction_value": result.prediction_value,
                        "prediction_emitted_at": result.prediction_emitted_at,
                        "prediction_target_symbol": result.prediction_target_symbol,
                        "second_event_id": result.second_event_id,
                        "second_event_timestamp": result.second_event_timestamp,
                        "prediction_resolution_source": result.prediction_resolution_source,
                        "prediction_resolution_event_id": result.prediction_resolution_event_id,
                        "prediction_resolution_timestamp": result.prediction_resolution_timestamp,
                        "prediction_error": result.prediction_error,
                        "readout_timestamp": result.readout_timestamp,
                        "prediction_created_count": result.prediction_created_count,
                        "prediction_matched_count": result.prediction_matched_count,
                        "prediction_expired_count": result.prediction_expired_count,
                        "prediction_omitted_count": result.prediction_omitted_count,
                        "omission_error_route_event_id": result.omission_error_route_event_id,
                        "omission_error_lineage_id": result.omission_error_lineage_id,
                        "omission_error_prediction_id": result.omission_error_prediction_id,
                        "omission_error_predicted_symbol": result.omission_error_predicted_symbol,
                        "omission_error_value": result.omission_error_value,
                        "omission_error_delivery_timestamp": result.omission_error_delivery_timestamp,
                        "omission_error_event_count": result.omission_error_event_count,
                        "omission_error_route_delivery_count": result.omission_error_route_delivery_count,
                        "omission_readout_reception_count": result.omission_readout_reception_count,
                        "readout_emissions_following_omission": result.readout_emissions_following_omission,
                        "duplicate_omission_error_deliveries": result.duplicate_omission_error_deliveries,
                        "omission_feature_before_integration": result.omission_feature_before_integration,
                        "omission_feature_after_integration": result.omission_feature_after_integration,
                        "reward_delivered": result.reward_delivered,
                        "event_count": result.event_count,
                    }
                    for example, result in zip(frozen_test_examples, seed_test_predictions)
                ],
                "heldout_event_traces": (
                    [
                        {
                            "example_id": example.example_id,
                            "events": result.event_trace,
                        }
                        for example, result in zip(frozen_test_examples, seed_test_predictions)
                    ]
                    if condition in ("trained", "silence_information_ablation")
                    else []
                ),
            }

        for condition, comparison in (
            (
                name,
                _paired_comparison(
                    frozen_test_examples,
                    test_predictions["trained"],
                    predictions,
                ),
            )
            for name, predictions in test_predictions.items()
            if name != "trained"
        ):
            paired_rows[condition].append(
                (
                    comparison["trained_correct_control_wrong"],
                    comparison["trained_wrong_control_correct"],
                )
            )
            condition_results[condition]["paired_comparison_vs_trained"] = comparison
        seed_results.append(
            {
                "seed": seed,
                "dataset_generation_seeds": {
                    "train": seed * 10_000 + 101,
                    "validation": seed * 10_000 + 211,
                    "test": seed * 10_000 + 307,
                    "training_order_base": seed + 10_003,
                    "shuffled_reward_permutation": seed + 900_001,
                },
                "datasets": dataset_manifests,
                "conditions": condition_results,
            }
        )
        aggregate_total += len(frozen_test_examples)

    aggregate_metrics: dict[str, Any] = {}
    for condition in CONDITIONS:
        matrix = aggregate_confusions[condition]
        correct = sum(matrix[index][index] for index in range(4))
        total = sum(sum(row) for row in matrix)
        per_seed_metrics = [
            seed_result["conditions"][condition]["heldout_metrics"]
            for seed_result in seed_results
        ]
        per_class = {}
        for label, name in CLASS_NAMES.items():
            support = sum(matrix[label])
            predicted = sum(matrix[row][label] for row in range(4))
            true_positive = matrix[label][label]
            per_class[name] = {
                "label": label,
                "support": support,
                "correct": true_positive,
                "accuracy": true_positive / support,
                "recall": true_positive / support,
                "precision": true_positive / predicted if predicted else 0.0,
                "predicted_count": predicted,
                "wilson_95": wilson_interval(true_positive, support),
            }
        route_metrics = [metrics["omission_error_route"] for metrics in per_seed_metrics]
        route_deliveries = sum(item["route_events_delivered"] for item in route_metrics)
        prediction_lifecycle = {
            name: sum(metrics["prediction_lifecycle"][name] for metrics in per_seed_metrics)
            for name in ("created", "matched", "expired", "omitted")
        }
        aggregate_metrics[condition] = {
            "correct": correct,
            "examples": total,
            "accuracy": correct / total,
            "accuracy_wilson_95": wilson_interval(correct, total),
            "confusion_matrix_rows_true_columns_predicted": matrix,
            "class_names_by_index": CLASS_NAMES,
            "per_class": per_class,
            "singleton_correct": sum(
                matrix[label][label] for label in (2, 3)
            ),
            "singleton_examples": sum(sum(matrix[label]) for label in (2, 3)),
            "singleton_accuracy": (
                sum(matrix[label][label] for label in (2, 3))
                / sum(sum(matrix[label]) for label in (2, 3))
            ),
            "per_seed_accuracy": {
                str(seed_result["seed"]): seed_result["conditions"][condition]["heldout_metrics"]["accuracy"]
                for seed_result in seed_results
            },
            "prediction_lifecycle": prediction_lifecycle,
            "omission_error_route": {
                "enabled": all(item["enabled"] for item in route_metrics),
                "route_events_created": sum(item["route_events_created"] for item in route_metrics),
                "route_events_delivered": route_deliveries,
                "readout_receptions_after_omission": sum(
                    item["readout_receptions_after_omission"] for item in route_metrics
                ),
                "readout_emissions_following_omission": sum(
                    item["readout_emissions_following_omission"] for item in route_metrics
                ),
                "duplicate_deliveries": sum(item["duplicate_deliveries"] for item in route_metrics),
                "singleton_omission_examples": sum(
                    item["singleton_omission_examples"] for item in route_metrics
                ),
                "singleton_examples_integrated": sum(
                    item["singleton_examples_integrated"] for item in route_metrics
                ),
                "mean_readout_delay_after_omission_delivery": (
                    sum(
                        item["mean_readout_delay_after_omission_delivery"]
                        * item["readout_receptions_after_omission"]
                        for item in route_metrics
                        if item["mean_readout_delay_after_omission_delivery"] is not None
                    )
                    / route_deliveries
                    if route_deliveries
                    else None
                ),
                "mean_absolute_neural_state_change_from_omission": (
                    sum(
                        item["mean_absolute_neural_state_change_from_omission"]
                        * item["readout_receptions_after_omission"]
                        for item in route_metrics
                        if item["mean_absolute_neural_state_change_from_omission"] is not None
                    )
                    / route_deliveries
                    if route_deliveries
                    else None
                ),
            },
        }

    aggregate_paired = {}
    for condition, rows in paired_rows.items():
        trained_only = sum(pair[0] for pair in rows)
        control_only = sum(pair[1] for pair in rows)
        aggregate_paired[condition] = {
            "trained_correct_control_wrong": trained_only,
            "trained_wrong_control_correct": control_only,
            "mcnemar_exact_two_sided_p": _paired_exact_p(trained_only, control_only),
            "per_seed": {
                str(seed_result["seed"]): seed_result["conditions"][condition]["paired_comparison_vs_trained"]
                for seed_result in seed_results
            },
        }

    return {
        "experiment": "Luna-68 causal prediction-omission routing on Luna-67 four-class sequence learning",
        "experiment_arm": "B_routed_error" if omission_error_route_enabled else "C_route_disabled",
        "omission_error_route_enabled": omission_error_route_enabled,
        "task_is_historical_simon_says": False,
        "authorization_scope": "isolated research experiment; no Track B work",
        "base_revision": "f117ce51e7a805564e37252d3b5c99bda163ce57",
        "luna66_baseline": {
            "branch": "experiment/luna66-minimal-functional-learning",
            "source_sha256": {
                "experiment_module": "552b6a584ee540f69bc81ce92cffe6dd943ffca6e56ae74f6474f44bd314bb5f",
                "runner": "058725ccf18ac0a8a674a217fba7a99ca2f92840b237779c69eb972d33377388",
                "focused_tests": "b962f554612cb8d144fac4d7a900852d12bee83cedfba46d4627bf093017a826",
            },
            "artifact_sha256": "220fc5b0a655b5d7fed1314ff7ef736c56b6cbfc1137f925bdf56821abc52c96",
            "review": "Luna-0 independently reviewed; input-contract and provenance findings closed.",
        },
        "task": {
            "classes": {
                "0": {"name": "A_then_B", "sequence": ["A", "B"]},
                "1": {"name": "B_then_A", "sequence": ["B", "A"]},
                "2": {"name": "A_only", "sequence": ["A"]},
                "3": {"name": "B_only", "sequence": ["B"]},
            },
            "examples_per_class": {
                "training": config.train_per_class,
                "validation": config.validation_per_class,
                "heldout": config.test_per_class,
            },
            "all_classes_share_first_timestamp_distribution": True,
            "first_event_timestamp_distribution": {
                "family": "Uniform(first_time_min, first_time_max), independently sampled per example in every class and split",
                "range": [config.first_time_min, config.first_time_max],
            },
            "second_event_gap_distribution": {
                "applies_to_classes": [0, 1],
                "nominal_range": [config.nominal_gap_min, config.nominal_gap_max],
                "independent_uniform_jitter": [-config.second_event_jitter, config.second_event_jitter],
                "bounded_actual_range": [
                    config.nominal_gap_min - config.second_event_jitter,
                    config.nominal_gap_max + config.second_event_jitter,
                ],
                "singleton_second_event": "not supplied",
            },
            "common_external_observation_deadline_after_first_event": config.observation_window,
            "deadline_strictly_after_latest_routed_second_event": True,
            "input_event_has_no_label_or_sequence_length_metadata": True,
            "deadline_is_external_not_internal_neural_event": True,
        },
        "network_and_learning": {
            "components": [
                "Luna-1 bounded EventQueue and execute_bounded",
                "Luna-2 signed event-driven sequence TPCNNeuron with analytic local-time decay",
                "Luna-4 finite topology routing input, prediction error, four readout channels and reward",
                "Luna-3 LocalPredictor for one anticipatory next-symbol prediction and observed/missed prediction errors",
                "Luna-8 EligibilityLedger for prediction error and separate readout-weight/readout-bias delayed reward traces",
                "four-channel learned affine readout over sequence-neuron state; no handcoded class decision",
            ],
            "readout_rule": (
                "score[k]=tanh(tanh(w[k]*sequence_state+b[k])); argmax chooses the class. "
                "After delayed reward, only the selected class slope and bias receive bounded "
                "local updates proportional to their matching eligibility credit."
            ),
            "topology_nodes": 12,
            "topology_edges": 10 if omission_error_route_enabled else 9,
            "fan_in_limit": 3 if omission_error_route_enabled else 2,
            "fan_out_limit": 4,
            "queue_capacity": config.queue_capacity,
            "event_budget_per_example": config.event_budget_per_example,
            "weight_bounds": [-3.0, 3.0],
            "bias_bounds": [-3.0, 3.0],
            "prediction_weight_bounds": [-1.0, 1.0],
            "neuron_decay_rate": config.neuron_decay_rate,
            "prediction_learning_rate": config.prediction_learning_rate,
            "readout_learning_rate": config.readout_learning_rate,
            "reward_delay_after_class_decision": config.reward_delay,
            "global_neural_timestep": False,
            "training_feedback_absent_from_heldout_inference": True,
            "heldout_parameter_freeze_verified": True,
            "reward_message_identity_deduplicated_per_local_ledger": True,
        },
        "omission_error_intervention": {
            "edge": (
                "prediction_ledger -> sequence"
                if omission_error_route_enabled
                else None
            ),
            "event_emitted_only_after": (
                "one genuine matched prediction error whose observation source is the common deadline's missed-second-event resolution"
                if omission_error_route_enabled
                else None
            ),
            "signal_fields": (
                [
                    "prediction_id",
                    "target_key",
                    "predicted_symbol",
                    "predicted_value",
                    "observed_value",
                    "error_value",
                    "prediction_timestamp",
                    "resolution_timestamp",
                    "resolution_source",
                ]
                if omission_error_route_enabled
                else []
            ),
            "lineage_id_is_prediction_id": omission_error_route_enabled,
            "readout_deferred_until_after_integrated_omission": omission_error_route_enabled,
            "readout_learning_rule_and_reward_provenance_unchanged": True,
            "task_label_in_signal": False,
            "route_disabled_arm_should_match_frozen_luna67": not omission_error_route_enabled,
        },
        "completion_and_silence": {
            "external_deadline_event": "external_evaluation_clock -> observation_deadline; one event at first-event-time + common observation window",
            "internal_neural_completion_event": "none; the external deadline evaluates local state and emits the standard routed readout inputs",
            "normal_silence_mechanism": (
                "TPCNNeuron analytically decays state from its last input timestamp to the common deadline; "
                "a singleton's still-outstanding next-symbol prediction resolves at the same deadline as an explicit zero-valued absence observation."
            ),
            "silence_information_ablation": (
                "Preserves every input, prediction, common external deadline and missed-prediction error, "
                "but freezes sequence-neuron state across the silent interval. It isolates internal "
                "elapsed-time decay from input-event content and the shared decision boundary."
            ),
            "whether_classifier_self_detects_cessation": False,
            "interpretation_boundary": (
                "The classifier does not autonomously emit a silence event. It uses the same externally supplied "
                "observation boundary for every example; measured state changes and the freeze-state ablation "
                "show whether local elapsed-time decay adds useful information beyond the fixed window."
            ),
        },
        "controls": {
            "learning_disabled": "true labels delivered as delayed reward; parameter updates disabled",
            "shuffled_rewards": "one fixed seed-specific permutation of balanced training labels reused across epochs",
            "temporal_order_destroyed": "all two-event streams become A then B at their original timestamps; singletons remain unchanged",
            "untrained": "zero initialization; no training exposures",
            "silence_information_ablation": "same common deadline and reward procedure; freeze sequence-neuron decay only during silence",
            "ablation_information_limit": (
                "The shared external deadline remains necessary to define sequence completion. "
                "This ablation tests state-decay use, not an impossible task in which the observer is denied "
                "any sequence-end information."
            ),
        },
        "seeds": list(config.seeds),
        "aggregate_heldout_metrics_by_condition": aggregate_metrics,
        "aggregate_paired_heldout_comparisons_vs_trained": aggregate_paired,
        "seed_results": seed_results,
        "success_criteria": {
            "trained_heldout_accuracy_at_least_0_80": (
                aggregate_metrics["trained"]["accuracy"] >= 0.80
            ),
            "improves_over_learning_disabled": (
                aggregate_metrics["trained"]["accuracy"] > aggregate_metrics["learning_disabled"]["accuracy"]
            ),
            "improves_over_shuffled_rewards": (
                aggregate_metrics["trained"]["accuracy"] > aggregate_metrics["shuffled_rewards"]["accuracy"]
            ),
            "improves_over_temporal_order_destroyed": (
                aggregate_metrics["trained"]["accuracy"] > aggregate_metrics["temporal_order_destroyed"]["accuracy"]
            ),
            "improves_over_untrained": (
                aggregate_metrics["trained"]["accuracy"] > aggregate_metrics["untrained"]["accuracy"]
            ),
            "silence_ablation_is_reported_as_mechanism_test_not_primary_failure": True,
            "paired_test_examples_per_seed": config.test_per_class * 4,
        },
    }


__all__ = [
    "CLASS_NAMES",
    "CONDITIONS",
    "FourClassTaskModel",
    "Luna67Config",
    "SequenceResult",
    "TemporalSequenceExample",
    "dataset_hashes",
    "generate_dataset",
    "run_example",
    "run_experiment",
]
