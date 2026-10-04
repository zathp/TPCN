"""Luna-12L four-class scale and energy/prediction evidence collector.

HISTORICAL COMPATIBILITY EXPERIMENT; NOT CURRENT EXCURSION_V1 / ACP-0007
EFFICACY EVIDENCE.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Literal

from .experiments import ExperimentConfig
from .spiral_benchmark import make_spiral_dataset, run_policy_control
from .temporal_capacity import CapacityPressureConfig, run_temporal_capacity

Policy = Literal["fixed", "baseline", "random", "temporal", "reversed"]
POLICIES: tuple[Policy, ...] = ("fixed", "baseline", "random", "temporal", "reversed")
CLASS_LABELS = (
    "spiral-left-outward", "spiral-right-outward",
    "spiral-left-inward", "spiral-right-inward",
)


@dataclass(frozen=True, slots=True)
class ScaleConfig:
    name: str
    neuron_count: int
    edge_capacity: int
    fan_in_out: int
    candidate_history_capacity: int
    queue_event_capacity: int
    growth_attempts: int
    examples_per_class: int = 2


SCALES = (
    ScaleConfig("reference", 7, 6, 2, 8, 16, 3),
    ScaleConfig("expanded", 12, 10, 3, 12, 24, 5),
)


@dataclass(frozen=True, slots=True)
class FourClassMetrics:
    scale: str
    policy: Policy
    requested_scale: str
    executed_scale: str
    requested_policy: Policy
    executed_policy: Policy
    seed: int
    class_count: int
    classifier_neuron_count: int
    classifier_fan_in_limit: int
    classifier_fan_out_limit: int
    classifier_edge_capacity: int
    classifier_candidate_capacity: int
    classifier_config_digest: str
    classifier_topology_edges: int
    accuracy: float
    per_class_accuracy: tuple[tuple[str, float], ...]
    confusion: tuple[tuple[str, str, int], ...]
    prediction_loss: float
    prediction_error_count: int
    proxy_energy: float
    event_count: int
    activation_count: int
    edge_count: int
    active_edge_utilization: float
    accepted_additions: int
    rejected_mutations: int
    rejection_reasons: tuple[tuple[str, int], ...]
    candidate_exposure: int
    candidate_considered: int
    growth_attempts: int
    fan_in_saturation: float
    fan_out_saturation: float
    path_hops: float
    path_delay: float
    shortcut_selected: bool
    causal_intervention_changed: bool
    replay_digest: str
    order_control_accuracy: float
    order_control_prediction_loss: float
    represented_classes: tuple[str, ...]
    class_separation: float
    accuracy_per_event: float
    accuracy_per_proxy_energy: float
    proxy_energy_per_correct: float | None
    events_per_correct: float | None
    energy_unit: str = "activity-cost-proxy; uncalibrated"


def _classification_metrics(policy: Policy, seed: int, scale: ScaleConfig) -> dict[str, object]:
    dataset = make_spiral_dataset(
        examples_per_class=scale.examples_per_class,
        train_seed=12007 + seed * 100,
        evaluation_seed=12017 + seed * 100,
    )
    max_points = max(len(item.points) for item in dataset.train + dataset.evaluation)
    config = ExperimentConfig(
        epochs=2,
        max_points=max_points,
        prediction_capacity=max_points,
        max_classes=4,
        seed=seed,
        neuron_model="TANH_LEGACY",
        structural_plasticity=policy != "fixed",
        structural_policy=policy,
        topology_edge_capacity=scale.edge_capacity,
        topology_fan_in=scale.fan_in_out,
        topology_fan_out=scale.fan_in_out,
        topology_node_count=scale.neuron_count,
        candidate_capacity=scale.candidate_history_capacity,
        max_growth_per_epoch=scale.growth_attempts,
    )
    selected = run_policy_control(dataset, policy=policy, config=config)
    reverse_control = run_policy_control(dataset, policy=policy, config=config, order_transform="reverse")
    diagnostics = dict(selected.per_class_accuracy)
    config_digest = hashlib.sha256(json.dumps(asdict(config), sort_keys=True).encode()).hexdigest()
    return {
        "accuracy": selected.accuracy,
        "per_class_accuracy": selected.per_class_accuracy,
        "confusion": selected.confusion,
        "prediction_loss": selected.prediction_loss,
        "prediction_error_count": selected.prediction_error_count,
        "proxy_energy": selected.energy,
        "event_count": selected.event_count,
        "activation_count": selected.active_neuron_count,
        "represented_classes": selected.represented_classes,
        "class_separation": selected.margin,
        "class_metrics_complete": set(diagnostics) == set(CLASS_LABELS),
        "order_control_accuracy": reverse_control.accuracy,
        "order_control_prediction_loss": reverse_control.prediction_loss,
        "executed_policy": policy,
        "executed_scale": scale.name,
        "class_count": len(CLASS_LABELS),
        "classifier_neuron_count": scale.neuron_count,
        "classifier_fan_in_limit": scale.fan_in_out,
        "classifier_fan_out_limit": scale.fan_in_out,
        "classifier_edge_capacity": scale.edge_capacity,
        "classifier_candidate_capacity": scale.candidate_history_capacity,
        "classifier_config_digest": config_digest,
        "classifier_topology_edges": selected.connection_count,
    }


def run_luna12l_condition(policy: Policy, *, seed: int, scale: ScaleConfig) -> FourClassMetrics:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")
    structural_config = CapacityPressureConfig(
        node_count=scale.neuron_count,
        fan_in_limit=scale.fan_in_out,
        fan_out_limit=scale.fan_in_out,
        edge_capacity=scale.edge_capacity,
        routing_capacity=scale.edge_capacity,
        candidate_capacity=scale.candidate_history_capacity,
        history_capacity=scale.candidate_history_capacity,
        max_growth_attempts=scale.growth_attempts,
        queue_capacity=scale.queue_event_capacity,
        max_events=scale.queue_event_capacity,
    )
    structural = run_temporal_capacity(policy, seed=seed, config=structural_config)
    classification = _classification_metrics(policy, seed, scale)
    if classification["executed_policy"] != policy or classification["executed_scale"] != scale.name:
        raise RuntimeError("classifier condition provenance does not match requested condition")
    replay = structural.metrics.after
    intervention = structural.causal_intervention
    return FourClassMetrics(
        scale.name, policy, scale.name, str(classification["executed_scale"]), policy,
        str(classification["executed_policy"]), seed, int(classification["class_count"]),
        int(classification["classifier_neuron_count"]), int(classification["classifier_fan_in_limit"]),
        int(classification["classifier_fan_out_limit"]), int(classification["classifier_edge_capacity"]),
        int(classification["classifier_candidate_capacity"]), str(classification["classifier_config_digest"]),
        int(classification["classifier_topology_edges"]), float(classification["accuracy"]), classification["per_class_accuracy"],
        classification["confusion"], classification["prediction_loss"], classification["prediction_error_count"],
        classification["proxy_energy"], classification["event_count"], classification["activation_count"], structural.metrics.edge_count,
        structural.metrics.active_edge_utilization, structural.metrics.accepted_additions,
        structural.metrics.rejected_mutations, structural.metrics.rejection_reasons,
        structural.metrics.candidates_exposed, structural.metrics.candidates_considered,
        structural.metrics.growth_attempts, structural.metrics.fan_in_saturation,
        structural.metrics.fan_out_saturation,
        sum(replay.path_hops) / max(1, len(replay.path_hops)),
        sum(replay.path_delays) / max(1, len(replay.path_delays)),
        structural.metrics.shortcut_selected, bool(intervention and intervention.changed),
        replay.digest,
        float(classification["order_control_accuracy"]),
        float(classification["order_control_prediction_loss"]),
        tuple(classification["represented_classes"]),
        float(classification["class_separation"]),
        float(classification["accuracy"]) / max(1, int(classification["event_count"])),
        float(classification["accuracy"]) / max(float(classification["proxy_energy"]), 1e-12),
        float(classification["proxy_energy"]) / classification["accuracy"] if classification["accuracy"] else None,
        int(classification["event_count"]) / classification["accuracy"] if classification["accuracy"] else None,
    )


def run_luna12l_suite(*, seeds: tuple[int, ...] = (0, 1, 2, 3, 4),
                      scales: tuple[ScaleConfig, ...] = SCALES) -> tuple[FourClassMetrics, ...]:
    return tuple(
        run_luna12l_condition(policy, seed=seed, scale=scale)
        for scale in scales for seed in seeds for policy in POLICIES
    )


__all__ = ["CLASS_LABELS", "FourClassMetrics", "POLICIES", "SCALES", "ScaleConfig",
           "run_luna12l_condition", "run_luna12l_suite"]
