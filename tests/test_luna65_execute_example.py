from dataclasses import replace

import pytest

from tpcn.eligibility import EligibilityCapacityError
from tpcn.event_runtime import QueueCapacityError
from tpcn.experiment_excursion_runtime import (
    ExcursionCharacterRuntime,
    RuntimeEventBudgetExceeded,
)
from tpcn.excursion_neuron import E1EventBudgetExceeded
from tpcn.experiments import (
    ExampleFailureKind,
    ExperimentConfig,
    ExperimentRunner,
    SyntheticExample,
)
from tpcn.ir2 import neuron_to_ir2_e2
from tpcn.predictive_coding import PredictionCapacityError
from tpcn.stroke_dataset import StrokePoint


@pytest.fixture
def artificial_example() -> SyntheticExample:
    return SyntheticExample(
        "unit-example",
        (
            StrokePoint(0.25, 0.5, timestamp=0.0),
            StrokePoint(0.75, 0.125, timestamp=1.0),
        ),
        "token-a",
    )


def make_runner() -> ExperimentRunner:
    return ExperimentRunner(ExperimentConfig(
        max_points=2,
        reward_mode="neutral",
        topology_node_count=4,
        topology_initial_edges=4,
        topology_edge_capacity=8,
        event_budget=128,
        settling_horizon=4.0,
        prediction_expiry=4.0,
    ))


def identity_counters(runner: ExperimentRunner) -> tuple[tuple[str, int, int, int, int], ...]:
    assert runner._network is not None
    return tuple(
        (
            record.neuron_id,
            record.next_event_identity,
            record.next_episode_identity,
            record.next_lineage_identity,
            record.next_input_identity,
        )
        for record in (
            neuron_to_ir2_e2(neuron) for neuron in runner._network.neurons
        )
    )


def test_execute_example_matches_existing_trace_and_neutral_reward(
    artificial_example: SyntheticExample,
) -> None:
    baseline = make_runner()
    baseline._ensure_topology((artificial_example,))
    baseline_run = baseline._run_example(artificial_example, 0, update=False)
    runner = make_runner()

    result = runner.execute_example(artificial_example, index=0)

    assert result.completed
    assert result.event_trace == baseline_run.trace
    assert result.prediction == baseline_run.raw_prediction
    assert result.reward == baseline_run.reward == 0.0
    assert all("token-a" not in repr(event) for event in result.event_trace)
    assert result.execution is not None and result.execution.completed
    assert len(result.identity_snapshots) == 4
    assert result.input_neuron_id == "neuron-0"
    assert result.failure_kind is None


def test_execute_example_preserves_network_and_commits_successful_readout_updates(
    artificial_example: SyntheticExample,
) -> None:
    runner = make_runner()

    first = runner.execute_example(artificial_example, index=1, update=True)
    topology = runner.topology
    second = runner.execute_example(artificial_example, index=3, update=True)

    assert first.completed and second.completed
    assert first.network_feature is not None and second.network_feature is not None
    assert first.input_neuron_id == "neuron-1"
    assert second.input_neuron_id == "neuron-3"
    assert topology is not None and runner.topology is topology
    assert runner.updates == 2
    assert runner.prototypes == (("token-a", first.network_feature + second.network_feature, 2),)
    assert first.readout_updated and second.readout_updated
    assert first.readout_diagnostic is not None and first.readout_diagnostic.reward == 0.0
    assert second.readout_diagnostic is not None and second.readout_diagnostic.reward == 0.0


def test_execute_example_replay_is_deterministic(
    artificial_example: SyntheticExample,
) -> None:
    first = make_runner().execute_example(artificial_example, index=2)
    second = make_runner().execute_example(artificial_example, index=2)

    assert first.event_trace == second.event_trace
    assert first.replay_digest == second.replay_digest
    assert first.identity_snapshots == second.identity_snapshots


@pytest.mark.parametrize(
    ("error", "failure_kind"),
    (
        (E1EventBudgetExceeded("identity limit"), ExampleFailureKind.E1_EVENT_BUDGET),
        (RuntimeEventBudgetExceeded("runtime limit"), ExampleFailureKind.RUNTIME_EVENT_BUDGET),
        (QueueCapacityError("queue full"), ExampleFailureKind.QUEUE_CAPACITY),
        (PredictionCapacityError("prediction full"), ExampleFailureKind.PREDICTION_CAPACITY),
        (EligibilityCapacityError("eligibility full"), ExampleFailureKind.ELIGIBILITY_CAPACITY),
        (BufferError("character buffer full"), ExampleFailureKind.CHARACTER_BUFFER_CAPACITY),
    ),
)
def test_expected_capacity_failures_are_returned_without_readout_updates(
    artificial_example: SyntheticExample,
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
    failure_kind: ExampleFailureKind,
) -> None:
    runner = make_runner()
    admission_calls = 0

    def fail_admission(
        _runtime: ExcursionCharacterRuntime,
        _batch: object,
    ) -> None:
        nonlocal admission_calls
        assert isinstance(_runtime, ExcursionCharacterRuntime)
        assert _batch is not None
        admission_calls += 1
        raise error

    monkeypatch.setattr(ExcursionCharacterRuntime, "admit_external_batch", fail_admission)

    result = runner.execute_example(artificial_example, index=2, update=True)

    assert admission_calls == 1
    assert not result.completed
    assert result.failure_kind is failure_kind
    assert not result.readout_updated
    assert runner.updates == 0 and runner.prototypes == ()
    assert runner.topology is not None
    assert all(counters[1:] == (0, 0, 0, 0) for counters in identity_counters(runner))
    assert runner._active_runtime is None


def test_incomplete_execution_is_returned_without_readout_update(
    artificial_example: SyntheticExample,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_end_character = ExcursionCharacterRuntime.end_character

    def return_incomplete(
        runtime: ExcursionCharacterRuntime,
        **kwargs: object,
    ) -> object:
        result = original_end_character(runtime, **kwargs)
        return replace(result, incomplete_settling=True)

    monkeypatch.setattr(ExcursionCharacterRuntime, "end_character", return_incomplete)
    runner = make_runner()

    result = runner.execute_example(artificial_example, index=1, update=True)

    assert not result.completed
    assert result.failure_kind is ExampleFailureKind.INCOMPLETE_SETTLING
    assert result.incomplete_settling
    assert not result.readout_updated
    assert runner.updates == 0 and runner.prototypes == ()


def test_unexpected_exception_propagates_after_character_cleanup(
    artificial_example: SyntheticExample,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_admission = ExcursionCharacterRuntime.admit_external_batch
    runner = make_runner()
    successful = runner.execute_example(artificial_example, index=1)
    assert successful.completed
    before = identity_counters(runner)
    topology = runner.topology
    admission_calls = 0

    def admit_then_fail(
        runtime: ExcursionCharacterRuntime,
        batch: object,
    ) -> object:
        nonlocal admission_calls
        admission_calls += 1
        original_admission(runtime, batch)
        raise RuntimeError("unexpected test exception")

    monkeypatch.setattr(ExcursionCharacterRuntime, "admit_external_batch", admit_then_fail)

    with pytest.raises(RuntimeError, match="unexpected test exception"):
        runner.execute_example(artificial_example, index=1, update=True)

    assert admission_calls == 1
    assert runner._active_runtime is None
    assert topology is not None and runner.topology is topology
    assert runner.updates == 0 and runner.prototypes == ()
    assert identity_counters(runner) == before
