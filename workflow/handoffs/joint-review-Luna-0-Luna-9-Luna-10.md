# Luna-0 Joint Integration Review: Luna-9 and Luna-10

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  task_id: "joint-review-luna-0-luna-9-luna-10"
  component: "experimental learning/evaluation and bounded structural plasticity"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "af5575c0a629f101486bf36d930218eecdef77b"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Luna-1 through Luna-8 validated causal event, prediction, reward, eligibility, and classification contracts."
    - "Luna-11 software-reference baseline and its evidence remain unchanged."
    - "Experimental plasticity remains optional A14 work; labels remain outside core inference."
    - "Real dataset benchmarking and hardware acceptance remain deferred."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-9.agent.md"
    - ".github/agents/luna-10.agent.md"
    - "tpcn/experiments.py"
    - "tests/test_experiments.py"
    - "tpcn/structural_plasticity.py"
    - "tests/test_structural_plasticity.py"
    - "workflow/handoffs/experimental-learning-evaluation-Luna-9.md"
    - "workflow/handoffs/structural-plasticity-Luna-10.md"
    - "workflow/handoffs/joint-review-Luna-0-Luna-9-Luna-10.md"
  tests_added:
    - "tests/test_experiments.py: 5 focused tests"
    - "tests/test_structural_plasticity.py: 7 focused tests"
  tests_passing:
    - "Serial Luna-9/Luna-10 focused suites: 12 passed"
    - "Serial full regression with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1: 101 passed"
    - "python -m compileall -q tpcn tests"
    - "Workspace diagnostics for owned implementation and tests: no errors"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "Real dataset benchmark: not run; dataset/version/split remains unresolved."
    - "FPGA, FPAA, hybrid, calibrated hardware, and hardware acceptance: not run."
  assumptions:
    - "The current dirty worktree is the validated Luna-11 software-reference baseline plus these Luna-9/Luna-10 changes; unrelated changes were preserved."
    - "Luna-9 stable-topology experiments and Luna-10 public topology adaptation remain independently usable; no private cross-module dependency was introduced."
  unresolved:
    - "The Luna-9 harness reports zero core parameter updates because the current public classifier has no trainable parameter API; this is an explicit limitation, not a convergence claim."
    - "Hardware backpressure, precision, and calibrated energy remain unvalidated."
  recommended_next_agent:
    - "Luna-0: retain the gate and plan any later dataset benchmark separately; do not authorize hardware acceptance from this review."
```

## Outcome

The Luna-9 and Luna-10 implementation slices are locally complete and pass a
joint software-reference review. Luna-9 adds a deterministic A/Z synthetic
stream experiment/evaluation API with prediction loss, classification, reward,
energy, activation, bounded-history, replay, and label-isolation metrics.
Luna-10 adds a local-evidence structural-plasticity controller with bounded
candidate storage, deterministic selection, legal growth/pruning, finite
capacity checks, inspectable state, and preserved in-flight queued routing.

The integration boundary is small and explicit: Luna-9 uses stable public TPCN
interfaces and defaults to stable topology; Luna-10 exposes its controller and
state through its own public module and does not depend on Luna-9 private code.
Neither implementation changes foundational runtime, topology, reward identity,
eligibility, classifier timing, or Luna-11 evidence.

## Architecture evidence

- **A01-A03:** serial focused and full regression checks pass; experiments use
  explicit event timestamps and queued prediction-error delivery, while
  plasticity delegates routing to `BoundedTopology.route`.
- **A04-A05/A08:** workload, queue, prediction, candidate, edge, fan-in/out,
  routing, and metric resources are finite; no spatial reservoir is introduced.
- **A06-A07/A11:** prediction/error and delayed reward remain canonical events;
  evaluation labels are consumed only after the classifier result, and
  structural candidates require source-local evidence.
- **A09-A10:** the experiment metrics expose activity-cost-proxy energy and
  reward-adjusted utility retention without treating inactivity as success.
- **A14:** topology adaptation is bounded, local, deterministic, and explicitly
  experimental. It does not alter the core contract and requires no ACP.
- **A15:** both additions are deterministic software-reference modules with
  finite records and explicit rejection paths. No hardware equivalence claim is
  made.

## Validation record

| Command or procedure | Observed result | Evidence |
|---|---|---|
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_experiments.py tests/test_structural_plasticity.py` | 12 passed | Both newly owned focused suites, serial run |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q` | 101 passed | Full repository regression, serial run |
| `python -m compileall -q tpcn tests` | passed | No compilation errors |
| Workspace diagnostics for owned files | no errors | `experiments.py`, `structural_plasticity.py`, and focused tests |
| `git diff --check` | passed | No whitespace errors |

## Benchmark and resource results

The Luna-9 workload is synthetic A/Z data with three timestamped points per
example; it is not a real dataset benchmark. Its default evaluation reports
accuracy `1.0`, positive prediction loss, 12 input events and activations,
positive `activity-cost-proxy` energy, and deterministic replay. The harness
reports `parameter_updates: 0` because no trainable public classifier API
exists. Luna-10 tests establish finite candidate and topology state, bounded
fan-in/out and edge capacity, deterministic growth/pruning, and preserved
in-flight propagation. Physical energy calibration, connectivity benchmarking
on a real dataset, and hardware traces are not applicable/not run.

## Gate decision

**Passed for the authorized Luna-9/Luna-10 software-reference slice.** No
unresolved contract violation or ACP-triggering departure was found. This does
not authorize real dataset benchmarking or hardware acceptance. Any later
benchmark must select and document a dataset, causal preprocessing, split,
seed, prediction/error metrics, energy proxy, and connectivity utilization.
Hardware work remains blocked until the software semantics and reference traces
are separately prepared.

## Reproduction and rollback

Run from the repository root without reverting unrelated worktree changes:

```text
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest -q tests/test_experiments.py tests/test_structural_plasticity.py
python -m pytest -q
python -m compileall -q tpcn tests
git diff --check
```

The result is uncommitted. A rollback of this phase removes only the two Luna-9
and Luna-10 implementation/test files and their handoffs/agent profiles; it
must preserve the validated Luna-11 changes and all unrelated dirty files.

## Next assignment

Return control to Luna-0. The next bounded decision is dataset benchmark
planning, not execution; hardware acceptance remains deferred. No additional
Luna role is authorized by this review.
