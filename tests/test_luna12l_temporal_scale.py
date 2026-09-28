from dataclasses import asdict, replace

import pytest

from tpcn.experiments import ExperimentConfig, evaluate
from tpcn.spiral_benchmark import generate_traversal_pair, make_spiral_dataset
import tpcn.temporal_scale as temporal_scale
from tpcn.temporal_scale import CLASS_LABELS, POLICIES, SCALES, run_luna12l_condition, run_luna12l_suite


def test_four_classes_are_deterministic_and_matched_by_traversal() -> None:
    dataset = make_spiral_dataset(examples_per_class=2, train_seed=11, evaluation_seed=19)
    assert {item.label for item in dataset.train} == set(CLASS_LABELS)
    assert dataset == make_spiral_dataset(examples_per_class=2, train_seed=11, evaluation_seed=19)
    outward, inward = generate_traversal_pair(7, handedness="left")
    assert outward.metadata.nuisance_tuple == inward.metadata.nuisance_tuple
    assert outward.metadata.traversal == "outward"
    assert inward.metadata.traversal == "inward"
    assert sorted((point.x, point.y) for point in outward.points) == sorted((point.x, point.y) for point in inward.points)
    assert tuple(point.timestamp for point in outward.points) == tuple(point.timestamp for point in inward.points)
    assert outward.points != inward.points


def test_labels_do_not_change_canonical_four_class_trace() -> None:
    example = make_spiral_dataset(examples_per_class=1, train_seed=3, evaluation_seed=4).evaluation[0]
    relabeled = replace(example, label=CLASS_LABELS[-1])
    config = ExperimentConfig(max_points=len(example.points), prediction_capacity=len(example.points), max_classes=4)
    first = evaluate((example.as_synthetic(),), config=config)
    second = evaluate((relabeled.as_synthetic(),), config=config)
    assert first.event_trace == second.event_trace
    assert first.metrics.energy == second.metrics.energy
    assert first.metrics.prediction_loss == second.metrics.prediction_loss


def test_scale_runner_retains_all_policies_and_causal_evidence() -> None:
    results = run_luna12l_suite(seeds=(0,))
    assert len(results) == len(SCALES) * len(POLICIES)
    assert {result.scale for result in results} == {"reference", "expanded"}
    assert all(result.edge_count <= next(scale for scale in SCALES if scale.name == result.scale).edge_capacity
               for result in results)
    temporal = run_luna12l_condition("temporal", seed=0, scale=SCALES[0])
    assert temporal.shortcut_selected
    assert temporal.causal_intervention_changed
    assert temporal.prediction_loss >= 0.0
    assert temporal.proxy_energy >= 0.0


@pytest.mark.parametrize("policy", POLICIES)
def test_requested_policy_is_executed_by_classifier(policy: str) -> None:
    result = run_luna12l_condition(policy, seed=0, scale=SCALES[0])
    assert result.requested_policy == policy
    assert result.executed_policy == policy
    assert result.classifier_config_digest


def test_policy_changes_classifier_execution_state() -> None:
    fixed = run_luna12l_condition("fixed", seed=0, scale=SCALES[0])
    temporal = run_luna12l_condition("temporal", seed=0, scale=SCALES[0])
    assert fixed.executed_policy != temporal.executed_policy
    assert (fixed.classifier_topology_edges, fixed.edge_count) != (temporal.classifier_topology_edges, temporal.edge_count)


def test_requested_scale_reaches_classifier_configuration() -> None:
    reference = run_luna12l_condition("fixed", seed=0, scale=SCALES[0])
    expanded = run_luna12l_condition("fixed", seed=0, scale=SCALES[1])
    assert reference.requested_scale == reference.executed_scale == "reference"
    assert expanded.requested_scale == expanded.executed_scale == "expanded"
    assert reference.classifier_neuron_count != expanded.classifier_neuron_count
    assert reference.classifier_config_digest != expanded.classifier_config_digest


def test_policy_scale_cross_product_preserves_provenance_and_serialization() -> None:
    results = run_luna12l_suite(seeds=(0,))
    assert {(result.requested_policy, result.executed_policy, result.requested_scale, result.executed_scale)
            for result in results} == {
                (policy, policy, scale.name, scale.name)
                for scale in SCALES for policy in POLICIES
            }
    serialized = asdict(results[0])
    assert serialized["requested_policy"] == serialized["executed_policy"]
    assert serialized["requested_scale"] == serialized["executed_scale"]
    assert serialized["classifier_neuron_count"] > 0


def test_condition_fails_on_classifier_provenance_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    original = temporal_scale._classification_metrics

    def mismatched(policy: str, seed: int, scale: object) -> dict[str, object]:
        result = original(policy, seed, scale)  # type: ignore[arg-type]
        result["executed_policy"] = "fixed" if policy != "fixed" else "temporal"
        return result

    monkeypatch.setattr(temporal_scale, "_classification_metrics", mismatched)
    with pytest.raises(RuntimeError, match="provenance"):
        run_luna12l_condition("temporal", seed=0, scale=SCALES[0])
