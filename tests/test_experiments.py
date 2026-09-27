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
    assert result.metrics.event_count == result.metrics.activation_count == len(result.event_trace)
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
    assert after.event_trace == before.event_trace
    assert after.metrics.event_count == before.metrics.event_count
    assert runner.history == trained.history


def test_delayed_sparse_and_neutral_rewards_are_bounded_and_observable() -> None:
    workload = make_synthetic_workload(examples_per_class=1)
    delayed = train(workload, config=ExperimentConfig(epochs=2, reward_delay=4.0, reward_mode="sparse"))
    neutral = train(workload, config=ExperimentConfig(epochs=2, reward_mode="neutral"))

    assert delayed.history[-1].reward_update_latency == 4.0
    assert neutral.parameter_updates == 0
    assert len(delayed.history) == len(neutral.history) == 2


def test_independent_runner_instances_and_reset_do_not_cross_contaminate() -> None:
    workload = make_synthetic_workload(examples_per_class=1, seed=3)
    config = ExperimentConfig(epochs=1)
    first = ExperimentRunner(config)
    second = ExperimentRunner(config)

    first.train(workload)
    untouched = second.evaluate(workload)
    first.reset()

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
    assert utility.metrics.retained_count <= event_only.metrics.retained_count