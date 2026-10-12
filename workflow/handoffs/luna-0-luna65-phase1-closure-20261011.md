# Luna-0 Handoff — Luna-65 Phase 1 Closure

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-65 Phase 1 independent closure and publication"
  task_id: "luna65-phase1-closure-20261011"
  component: "ExperimentRunner per-example interface"
  status: "complete"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "abb92b1d43a57fb9ab37bb27e847fef4480567ac"
  result_revision: "same commit containing this handoff; full object ID in publication report"
  dependencies: ["Luna-65 Phase 1 owner authorization"]
  owner: "repository owner"
  classification: ["software-reference API", "bounded API unit tests", "governance closure"]
  hypothesis: "A supported one-example runner API can expose completion/failure before the next example without changing aggregate evaluate/train behavior."
  counter_hypothesis: "Expected failures are not distinguishable, cleanup loses persistent identities, or successful-only readout updates diverge from the current per-example path."
  interfaces_relied_on:
    - "ExperimentRunner._run_example internal computation path"
    - "ExcursionCharacterRuntime"
    - "neuron_to_ir2_e2 public serializer"
  label_information_boundary:
    - "Tests use only the artificial evaluator token token-a."
    - "Reward mode is neutral; no task labels or benchmark inputs are used."
  timing_assumptions: ["No neural global clock added."]
  reset_boundaries:
    - "Per-character neuron/runtime state resets."
    - "Runner, topology, prototypes and persistent E2 identity high-water counters remain."
  resource_bounds:
    - "Focused test process configured for 120 s wall, 120 CPU s and 256 MiB process memory."
    - "Retained stdout/stderr artifact was capped at 1 MiB; emitted pipe bytes may exceed that cap before termination."
    - "No general-purpose supervisor qualification is claimed."
  authorized_scope:
    - "tpcn/experiments.py"
    - "tpcn/experiment_excursion_runtime.py"
    - "tests/test_luna65_execute_example.py"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "this closure handoff"
  unauthorized_scope:
    - "Capacity fixtures"
    - "Spiral training, evaluation, scoring or data generation"
    - "Simon Says execution"
    - "Luna-64 corrective execution"
    - "Luna-63C modification"
  controls:
    - "No benchmark fixtures or benchmark data."
    - "No training or scoring."
    - "Test command used -x; process stopped at first assertion failure."
    - "Two corrected invocations followed separate explicit owner authorizations."
  measurements:
    - "Final invocation: 11 passed in 0.14 s."
    - "Final supervisor wall elapsed: 400 ms."
    - "Final-run peak process memory: 29,847,552 bytes."
    - "Final-run retained output: 101 bytes."
    - "Reported process CPU accounting: 0 ms at accounting resolution; not zero use."
  information_boundary_check:
    - "Artificial token absent from event trace as asserted by the focused test."
  hardware_mapping: "No hardware equivalence claim."
  architecture_invariants_touched: []
  preserves:
    - "Existing evaluate() and train() behavior."
    - "Current neuron recurrence, prediction/error, reward and structural-plasticity semantics."
    - "Luna-12G historical TANH_LEGACY evidence."
    - "Luna-63C and Luna-64 records."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/experiments.py"
    - "tpcn/experiment_excursion_runtime.py"
    - "tests/test_luna65_execute_example.py"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna65-phase1-closure-20261011.md"
  tests_added: ["tests/test_luna65_execute_example.py"]
  tests_passing: ["11 focused API tests in the final separately authorized invocation."]
  tests_failed:
    - "First invocation stopped on a test-only assertion typo; corrected after separate owner authorization."
    - "Next invocation stopped on an incorrect assumption that failed admission consumed identity; corrected after separate owner authorization."
  tests_not_run:
    - "Capacity fixtures"
    - "Spiral benchmark"
    - "Simon Says benchmark"
    - "Full repository suite"
  assumptions:
    - "The reported final pytest output is represented by the execution result in the preceding session transcript; the temporary output file was removed."
  unresolved:
    - "No standalone raw test log or immutable test-run manifest was retained for independent replay of the reported final invocation."
    - "The output controller capped saved artifact bytes but did not strictly cap bytes emitted into the pipe before termination."
    - "The CPU timer measurement resolved to 0 ms and is not usable as a usage estimate."
    - "CPU and memory Job Object ceilings were configured but not stress-tested by exceeding them."
    - "Persistent E2 identity ceiling sufficiency for a complete replication remains unproven."
    - "Benchmark execution remains blocked."
  recommended_next_agent:
    - "Luna-65: only after explicit owner authorization, prepare a separate capacity-fixture request; do not execute under this closure."
```

## Outcome and scope

**PASS WITH FOLLOW-UP — LUNA-65 PHASE 1 CLOSED WITH DOCUMENTED LIMITATIONS.**
The additive `ExperimentRunner.execute_example(example, *, index,
update=False)` API and the typed `RuntimeEventBudgetExceeded` exception were
implemented in the authorized production files. The result is a frozen
dataclass with explicit `ExampleFailureKind` categories, execution and
settling status, readout diagnostics, deterministic replay digest, and
per-node identity snapshots obtained through the existing
`neuron_to_ir2_e2()` serializer.

The API performs the underlying EXCURSION computation with internal readout
mutation disabled, commits one readout sum/count only after successful
completion, converts expected incomplete and known capacity outcomes to
explicit result failures, and propagates unexpected exceptions after
per-character cleanup. The API rejects structural-plasticity configurations.
The pre-existing `evaluate()` and `train()` aggregate call paths retain their
prior behavior; the compatibility cleanup option defaults off. No call to
`ExperimentRunner.reset()` was added.

No architecture clause was changed, no ACP was opened, and no neural
recurrence, prediction/error, reward, or structural-plasticity semantics were
modified. Existing scientific controls remain frozen. This closure is an API
implementation gate only and supplies no efficacy result.

## Independent review and baseline

The expected branch was `governance/luna64-r4.3-freeze-20261010`, with
baseline and upstream both at
`abb92b1d43a57fb9ab37bb27e847fef4480567ac`. The worktree had only the three
authorized implementation/test paths modified before this governance
closure; the index was clean. The Luna-65 contract SHA-256 was recomputed as
`1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777`.

The independent implementation review returned
**PASS — LUNA-65 PHASE 1 READY FOR LUNA-0 CLOSURE**. It found no
high-confidence implementation blocker. Luna-0 independently checked the
source scope, implementation identities, focused tests and phase boundaries
against the contract. No tests were rerun during this closure.

## Focused-test evidence

The final reported command was:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -x tests/test_luna65_execute_example.py
```

The reported output was `11 passed in 0.14s`. The tests make 14
`execute_example()` calls plus one baseline `_run_example()` computation,
for 15 hand-authored two-point synthetic computations total. Inputs carry
only artificial token `token-a`, and the runner uses neutral reward. No
benchmark fixture, Spiral/Simon Says data, training, scoring, capacity
fixture or scientific run was used.

The first invocation stopped on a test assertion typo after 3 tests passed.
The owner separately authorized one corrected invocation, which stopped on
a second test assumption after 10 tests passed. The owner separately
authorized one final corrected invocation, which passed all 11 tests.
These are recorded as three invocations with two separately authorized
correction runs, not as silent retries under the original zero-retry
authorization.

The temporary output file for the final run was removed after being read.
The final tool output is available in the prior execution transcript, but
there is no separately retained raw stdout/stderr file, test-run manifest,
or immutable execution artifact to independently re-parse now. The pass
count, call count and measurements in this handoff are therefore recorded
from that reported output, not from a newly recovered independent log.

## Resource-control evidence and limitations

The final invocation used a Windows Job Object process with configured
per-process CPU-time and process-memory limits, a wall-time monitor, and
stdout/stderr capture into a file that retained at most 1 MiB. A separate
wall-time probe demonstrated termination at approximately 1.08 seconds for
a one-second ceiling. The final test invocation measured 400 ms wall time,
29,847,552 bytes peak process memory, and 101 bytes of retained output.
The Job Object memory limit was configured, but no over-limit memory process
was used to test termination. The CPU-time limit was configured, but the
final process accounting result of 0 ms is resolution-limited and must not
be interpreted as zero CPU consumption; no over-limit CPU process was used
to validate the CPU termination boundary.

A separate output probe emitted 2,000,000 bytes. The supervisor received
1,114,112 bytes from the pipe before stopping the child, while the retained
output file was capped at 1,048,576 bytes. Therefore, the retained artifact
limit was demonstrated, but total emitted bytes were not strictly capped at
1 MiB. The focused test itself emitted only 101 retained bytes and did not
approach this output condition.

These limits applied to the focused Phase 1 invocation only. This experiment
does not qualify the supervisor for Luna-64, capacity fixtures, or benchmark
execution.

## Source and governance identities

Raw SHA-256 identities recomputed from the current working-tree files:

| Path | SHA-256 |
|---|---|
| `workflow/docs/luna/LUNA_65_SPIRAL_RESUMPTION.md` | `1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777` |
| `tpcn/experiments.py` | `CABB81DA36280E7CDCF614B8B3E2CD5567035C20C6706A85B25B1A73310E967D` |
| `tpcn/experiment_excursion_runtime.py` | `DF007154939C6C554A3D914C15CE91C87954BEEEBF29DF416EE27D138F119D5A` |
| `tests/test_luna65_execute_example.py` | `DE32193D0E87059E995331E6B490DBEFD26020EB11C9EAFF3EBD27316D4C7D1D` |

The repository uses automatic text normalization for these Python/test files
and the Luna-65 contract; `workflow/docs/luna/LUNA_WORKFLOW.md` is explicitly
`-text`. The handoff is subject to the repository's text auto rule. Review
and staging must preserve the reviewed bytes. No architecture changelog
entry is required because this is a compatible API addition and governance
closure, not an architecture change.

## Preserved boundaries and unresolved gates

- Full-replication E2 identity-counter sufficiency remains unproven.
- E2 direct-counter and network capacity fixtures remain **NOT AUTHORIZED**.
- Full Spiral benchmark execution remains **BLOCKED**.
- Spiral training, evaluation, scoring, and dataset generation were not run.
- Simon Says execution was not run.
- No scientific-effectiveness claim is made.
- Luna-64 corrective execution remains unauthorized.
- Frozen Luna-63C and blocked Luna-64 records remain unchanged.
- No merge to `main` is authorized.

## Reproduction and rollback

The focused command above is retained as a reproduction reference only;
running it again requires separate owner authorization. No benchmark
reproduction command is authorized. The implementation has not been
committed as of this handoff. If rollback is separately authorized, revert
only the exact Luna-65 implementation/test/governance publication commit;
preserve unrelated worktree changes and all historical artifacts.

## Next assignment

Luna-65 may prepare a separately bounded capacity-fixture request only after
explicit owner authorization. It must not execute fixtures or benchmarks
under this closure. Before any future Spiral execution, resolve the
full-replication E2 capacity argument and obtain separate review and exact
owner execution authorization.
