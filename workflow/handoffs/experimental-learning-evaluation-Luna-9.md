# Luna-9 Experimental Learning and Evaluation

```yaml
tpcn_handoff:
  agent: Luna-9 Experimental Learning and Evaluation
  task_id: "experimental-learning-evaluation-luna-9"
  component: "experimental training, evaluation, metrics, and controlled learning behavior"
  status: "complete-with-regression-blocker"
  contract_version: "1.0"
  branch: "main"
  base_revision: "af5575c0a629f101486bf36d930218eecdef77b"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A15"]
  preserves:
    - "Validated Luna-1 through Luna-8 event, routing, prediction, reward, eligibility, and classification contracts."
    - "Labels remain outside core inference; orchestration metrics are evaluation-only."
    - "Real dataset benchmarking and hardware acceptance remain deferred."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/experiments.py"
    - "tests/test_experiments.py"
    - "workflow/handoffs/experimental-learning-evaluation-Luna-9.md"
  tests_added:
    - "tests/test_experiments.py: 8 focused deterministic experiment tests"
  tests_passing:
    - "python -m pytest -q tests/test_experiments.py: 8 passed"
    - "python -m pytest -q tests/test_experiments.py tests/test_eligibility.py tests/test_predictive_coding.py tests/test_event_runtime.py: 34 passed"
    - "python -m compileall -q tpcn tests"
    - "git diff --check"
    - "Workspace diagnostics for owned files: no errors"
  tests_failed:
    - "python -m pytest -q: collection blocked by dirty core edits omitting ACTIVITY_EVENT and LocalEnergyModel exports and RewardMessage.to_reward_signal()."
  tests_not_run:
    - "Full regression could not collect four suites because of the unrelated public-contract defects above."
    - "Joint Luna-9/Luna-10 integration review: not run."
    - "Actual dataset benchmark: not run; dataset/version/split is unresolved."
    - "FPGA, FPAA, hybrid, calibrated hardware, and hardware acceptance: not run."
  assumptions:
    - "The current dirty worktree contains the validated Luna-11 software-reference baseline and unrelated changes are preserved."
    - "Stable topology is the default; topology adaptation is accessed only through a future public Luna-10 interface."
  unresolved:
    - "Updates belong to the bounded outer-loop readout; no hidden core neuron parameters are claimed."
  recommended_next_agent:
    - "Luna-0: run a dedicated joint review against the Luna-11 baseline after Luna-9 and Luna-10 complete."
```

## Outcome and owned scope

Luna-9 owns `tpcn/experiments.py`, `tests/test_experiments.py`, and this
handoff. It delivers a deterministic A/Z synthetic temporal workload, bounded
training/evaluation APIs, prediction loss, classification, reward, utility,
energy and activation metrics, bounded metric history, replay digest, and
label-isolation tests. It does not claim trainable core weights.

No ACP was required. The implementation uses only existing public interfaces
and leaves the stable topology unchanged. The post-implementation gate is a
joint Luna-0 review; no later dataset or hardware phase is authorized here.

The runner adds an instance-local, bounded outer-loop readout. It does not
claim hidden core weights or alter Luna-1 through Luna-8 behavior.

## Architecture evidence

- A01-A03: workloads use canonical `Event` records with explicit local
  timestamps and queued prediction-error delivery; no global neural timestep
  or wall-clock value is used.
- A04/A08: workload length, queue capacity, classifier activity, prediction
  capacity, ledger traces, counters, and metric history are finite.
- A06-A07/A11: `LocalPredictor` creates delayed local prediction errors and
  `EligibilityLedger` receives reward/error events. Labels are external
  metadata used only after classification for evaluation reward.
- A09-A10: `LocalEnergyModel` reports activity-cost-proxy units and
  `RewardAdjustedUtility` supports the event-only versus utility retention
  comparison; inactivity is not treated as success.
- A15: the API is a deterministic Python reference harness over serializable
  event/data records. Hardware acceptance was not run.

No experimental architecture departure or ACP was introduced. Explicit gates,
structural plasticity, and real dataset benchmarking remain outside this task.

## Validation record

Environment: Windows PowerShell, Python 3.10.8, base revision
`af5575ce0a629f101486bf36d930218eecdef77b`, current dirty worktree, synthetic
seeds `0`, `3`, and `7`.

| Command or procedure | Observed result | Evidence |
|---|---|---|
| `python -m pytest -q tests/test_experiments.py` | 8 passed | Workload determinism, metrics, bounded history/replay, label isolation, learning, reward modes, reset isolation |
| `python -m pytest -q tests/test_experiments.py tests/test_eligibility.py tests/test_predictive_coding.py tests/test_event_runtime.py` | 34 passed | Focused Luna-9 and directly exercised public interfaces |
| `python -m pytest -q` | blocked at collection | Dirty core edits omit public exports and `RewardMessage.to_reward_signal()`; four suites cannot import |
| `python -m compileall -q tpcn tests` | passed | No compilation output/errors |
| Workspace diagnostics for owned files | no errors | `tpcn/experiments.py`, `tests/test_experiments.py` |
| `git diff --check` | passed | No whitespace errors |
| `python -m pytest -q tests/test_luna11_adversarial.py` | blocked at collection | Missing `ACTIVITY_EVENT` export from dirty `tpcn.__init__`; no Luna-9 failure was reported |

## Benchmark and resource results

The controlled workload contains two synthetic classes (`A`, `Z`), three
timestamped points per example, and no selected real dataset or split. The
default two-examples-per-class evaluation produced accuracy `1.0`, positive
prediction loss, 12 input activity events, 12 activations, positive local
energy in `activity-cost-proxy` units, and deterministic predictions. Training
history is capped by `history_limit`; replay digest and metrics match across
identical runs. Utility ablation is limited to the public `net` utility
interface and does not compare explicit gates.

Dataset benchmark, hardware acceptance, calibrated energy, connectivity
utilization, and joint integration are **not run**.

## Assumptions, limitations and unresolved issues

The experiment layer reports updates to its bounded outer-loop readout, not
core neuron parameters. “Convergence” means repeated deterministic metric
stability. Core parameter learning remains unspecified by the validated public
classifier interface.

The full regression blocker belongs to Luna-0 and the owners of the modified
energy, classifier, and package-export files. Luna-9 does not repair it because
those paths are outside this role's ownership.

## Reproduction and rollback

Run from the repository root:

```text
python -m pytest -q tests/test_experiments.py
python -m pytest -q
python -m compileall -q tpcn tests
git diff --check
```

The result is uncommitted. Restore only the three Luna-9-owned paths if a
rollback is authorized; unrelated dirty files listed by `git status --short`
were preserved.

## Next assignment

Return control to Luna-0 for public-contract repair and joint Luna-9/Luna-10
review against the Luna-11 software-reference baseline. Integration readiness
is **blocked pending that repair and review**, and no dataset or hardware gate
is claimed.
