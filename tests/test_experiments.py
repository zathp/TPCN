from tpcn.experiments import (
    ExperimentConfig,
    ExperimentRunner,
    EvaluationResult,
    evaluate,
    make_synthetic_workload,
    train,
)


def test_synthetic_workload_is_deterministic_and_label_metadata_is_external() -> None:
    first = make_synthetic_workload(examples_per_class=2, seed=7)
    second = make_synthetic_workload(examples_per_class=2, seed=7)

    assert first == second
    assert {example.label for example in first} == {"A", "Z"}
    assert all(not hasattr(point, "label") for example in first for point in example.points)


def test_evaluation_uses_canonical_events_and_reports_prediction_and_resource_metrics() -> None:
    result = evaluate(make_synthetic_workload(examples_per_class=2))

    assert isinstance(result, EvaluationResult)
    assert result.metrics.accuracy == 1.0
    assert result.metrics.prediction_loss >= 0.0
    assert result.metrics.event_count == result.metrics.processed_event_count
    assert result.metrics.activation_count == result.metrics.excursion_count
    assert result.metrics.event_count < len(result.event_trace)
    assert result.metrics.event_count >= 12
    assert result.metrics.energy > 0.0


def test_training_history_is_bounded_and_replay_is_exact() -> None:
    workload = make_synthetic_workload(examples_per_class=2, seed=3)
    config = ExperimentConfig(epochs=5, history_limit=2, max_points=3)

    first = train(workload, config=config)
    second = train(workload, config=config)

    assert len(first.history) == 2
    assert first.history == second.history
    assert first.evaluation == second.evaluation
    assert first.replay_digest == second.replay_digest
    assert first.parameter_updates > 0
    assert first.before is not None
    assert first.after is not None


def test_training_can_change_outer_readout_but_labels_stay_out_of_events() -> None:
    workload = make_synthetic_workload(examples_per_class=2)
    runner = ExperimentRunner(ExperimentConfig(epochs=2, max_points=3))

    before = runner.evaluate(workload)
    trained = runner.train(workload)
    after = runner.evaluate(workload)

    assert trained.parameter_updates > 0
    assert _trace_behavior(after.event_trace) == _trace_behavior(before.event_trace)
    assert after.metrics.event_count == before.metrics.event_count
    assert runner.history == trained.history


def test_delayed_sparse_and_neutral_rewards_are_bounded_and_observable() -> None:
    workload = make_synthetic_workload(examples_per_class=1)
    delayed = train(workload, config=ExperimentConfig(epochs=2, reward_delay=4.0, reward_mode="sparse"))
    neutral = train(workload, config=ExperimentConfig(epochs=2, reward_mode="neutral"))

    assert delayed.history[-1].reward_update_latency == 4.0
    assert neutral.parameter_updates == 4
    assert neutral.evaluation.metrics.reward == 0.0
    assert len(delayed.history) == len(neutral.history) == 2


def test_misclassified_class_acquires_supervised_readout_state() -> None:
    workload = make_synthetic_workload(examples_per_class=1, seed=7)
    result = train(workload, config=ExperimentConfig(epochs=1, seed=7, correct_reward=0.0))

    assert result.history[0].reward < 0.0
    assert result.history[0].readout_diagnostics[1].prediction == "A"
    assert result.history[0].readout_diagnostics[1].reward < 0.0
    assert result.history[0].readout_diagnostics[1].readout_updated
    assert result.parameter_updates == 2
    assert set(result.evaluation.metrics.represented_classes) == {"A", "Z"}
    assert result.evaluation.metrics.prototype_count == 2
    assert {label for label, _, _ in result.evaluation.readout_diagnostics[1].class_representations} == {"A", "Z"}


def test_readout_diagnostics_report_bounded_separation_and_class_metrics() -> None:
    workload = make_synthetic_workload(examples_per_class=5, seed=7)
    runner = ExperimentRunner(ExperimentConfig(epochs=20, seed=7, max_classes=2))
    result = runner.train(workload)
    metrics = result.evaluation.metrics

    assert len(runner.prototypes) == 2
    assert metrics.per_class_accuracy == (("A", 1.0), ("Z", 1.0))
    assert metrics.confusion == (("A", "A", 5), ("Z", "Z", 5))
    assert metrics.mean_margin >= 0.0
    assert all(d.class_distances for d in result.evaluation.readout_diagnostics)
    assert all(d.winning_distance <= d.runner_up_distance for d in result.evaluation.readout_diagnostics)


def test_readout_state_respects_max_classes_and_is_deterministic() -> None:
    workload = make_synthetic_workload(examples_per_class=1, seed=3)
    config = ExperimentConfig(epochs=3, seed=3, max_classes=2)
    first = ExperimentRunner(config)
    second = ExperimentRunner(config)

    first_result = first.train(workload)
    second_result = second.train(workload)

    assert len(first.prototypes) <= config.max_classes
    assert first.prototypes == second.prototypes
    assert first_result.evaluation.readout_diagnostics == second_result.evaluation.readout_diagnostics


def test_external_labels_do_not_change_neural_trace_or_topology() -> None:
    workload = make_synthetic_workload(examples_per_class=2, seed=11)
    relabeled = tuple(type(example)(example.example_id, example.points, "Z" if example.label == "A" else "A")
                      for example in workload)
    config = ExperimentConfig(
        epochs=2,
        seed=11,
        structural_plasticity=True,
        neuron_model="TANH_LEGACY",
    )

    first = ExperimentRunner(config)
    second = ExperimentRunner(config)
    first_result = first.train(workload)
    second_result = second.train(relabeled)

    assert first_result.evaluation.event_trace == second_result.evaluation.event_trace
    assert tuple((edge.source, edge.destination, edge.propagation_delay) for edge in first.topology.edges) == tuple(
        (edge.source, edge.destination, edge.propagation_delay) for edge in second.topology.edges)
    assert tuple(item[:4] for item in first_result.evaluation.event_trace) == tuple(
        item[:4] for item in second_result.evaluation.event_trace)


def test_independent_runner_instances_and_reset_do_not_cross_contaminate() -> None:
    workload = make_synthetic_workload(examples_per_class=1, seed=3)
    config = ExperimentConfig(epochs=1)
    first = ExperimentRunner(config)
    second = ExperimentRunner(config)

    first.train(workload)
    untouched = second.evaluate(workload)
    first.reset()
    second.reset()

    assert untouched == second.evaluate(workload)
    assert first.evaluate(workload) == untouched


def test_changed_labels_do_not_change_inference_event_trace() -> None:
    workload = make_synthetic_workload(examples_per_class=1)
    relabeled = tuple(type(example)(example.example_id, example.points, "Z" if example.label == "A" else "A")
                      for example in workload)

    first = evaluate(workload)
    second = evaluate(relabeled)

    assert first.event_trace == second.event_trace
    assert first.predictions == second.predictions
    assert first.metrics.energy == second.metrics.energy


def test_utility_ablation_is_supported_without_claiming_explicit_gates() -> None:
    workload = make_synthetic_workload(examples_per_class=1)
    event_only = evaluate(workload, config=ExperimentConfig(activation_mode="event_only"))
    utility = evaluate(workload, config=ExperimentConfig(activation_mode="utility"))

    assert event_only.predictions == utility.predictions
    assert event_only.event_trace == utility.event_trace
    assert event_only.metrics.energy == utility.metrics.energy
    assert utility.metrics.retained_count <= event_only.metrics.retained_count


def _trace_behavior(trace: tuple[tuple[object, ...], ...]) -> tuple[tuple[object, ...], ...]:
    """Compare causal stream behavior without character-local high-water IDs."""
    return tuple(
        (
            row[0],
            row[1],
            row[2],
            row[3],
            row[4] if isinstance(row[4], (int, float, str)) else type(row[4]).__name__,
        )
        for row in trace
    )