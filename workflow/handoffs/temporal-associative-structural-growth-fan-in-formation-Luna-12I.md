# Luna-12I Dispatch Handoff

```yaml
tpcn_handoff:
  agent: Luna-12I Temporal-Associative Structural Growth and Fan-In Formation
  luna_identifier: "Luna-12I"
  descriptive_name: "Temporal-Associative Structural Growth and Fan-In Formation"
  task_id: "temporal-associative-structural-growth-fan-in-formation-luna-12i"
  component: "bounded local temporal-association candidate policy over Luna-4/Luna-10 topology"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "5689106"
  result_revision: "uncommitted"
  dependencies:
    - "Luna-4 bounded topology"
    - "Luna-10 structural plasticity"
    - "Luna-12E computational topology integration"
    - "Luna-12H intrinsic temporal state and unequal-delay evidence"
  owner: "Luna-0 Architecture Guardian"
  classification: ["EXPERIMENT", "VERIFICATION", "IMPLEMENTATION"]
  hypothesis: "Repeated source-local earlier-to-later activity can produce legal, bounded candidates that form useful convergent fan-in more often than matched random legal candidates."
  counter_hypothesis: "Temporal candidates do not improve convergent fan-in or path shortening over matched controls, or they increase rejection/churn/resource cost or prediction error without useful structural/task evidence."
  interfaces_relied_on:
    - "CandidateEvidence and StructuralPlasticityController"
    - "BoundedTopology and finite propagation delays"
    - "Canonical event timestamps and deterministic ordering"
  label_information_boundary:
    - "No labels, rewards, predictions, evaluation metrics, or future events enter candidate evidence."
  timing_assumptions:
    - "Only positive finite event timestamps and locally observed elapsed intervals are used."
    - "The experiment records its timing window as an experimental parameter; it is not a core invariant."
  reset_boundaries:
    - "Temporal observation history resets between declared sequences; topology/controller state is reset only between matched runs."
  resource_bounds:
    - "Finite observation history, candidate capacity, edge capacity, fan-in/out, growth budget, and mutation history."
    - "Every accepted edge has positive finite propagation delay."
  authorized_scope:
    - "Add a standalone source-local temporal-association policy that emits bounded CandidateEvidence."
    - "Add deterministic matched control fixtures for existing-policy, random-legal, temporal, shuffled-timing, and reversed-order conditions."
    - "Apply candidates through the existing bounded controller and measure fan-in, path delay, rejection causes, churn, and deterministic replay."
    - "Add focused tests, a reproducible experiment entry point/artifact if needed, and this completion handoff."
  unauthorized_scope:
    - "No change to A01-A15, no ACP promotion, and no mandatory timing formula or graph shape."
    - "No labels, global topology search, unrestricted learning, real-dataset claims, hardware acceptance, or classifier redesign."
    - "No replacement of the canonical event-routing topology or modification of Luna-12E runtime behavior."
  controls:
    - "Fixed topology/no growth."
    - "Existing Luna-10 structural policy with matched budgets."
    - "Random legal candidate selection with the same seed and budgets."
    - "Temporal-association candidates with the same seed and budgets."
    - "Timing-shuffled and reversed local observation order where the fixture permits."
  measurements:
    - "Accepted additions, fan-in/out utilization, convergent motif count, path length/delay, candidate/rejection causes, duplicate proposals, churn, event count, and bounded state."
    - "Prediction/error, energy/resource proxy, utility, and task metrics are recorded only when an existing runner fixture exercises them; topology appearance alone is not success."
  information_boundary_check:
    - "Each proposal is emitted by the source-local observer after a causally available local observation; no topology-wide statistic is consulted."
  hardware_mapping:
    - "Finite counters/history and positive-delay edge records map to bounded FPGA/FPAA/hybrid resources; software timestamps remain reference metadata until hardware units are declared."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A14", "A15"]
  preserves:
    - "Event-driven execution, local time, finite propagation, bounded topology/dynamics, label isolation, and downstream-only observability."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/temporal_association.py"
    - "tpcn/__init__.py"
    - "tests/test_luna12i_temporal_association.py"
    - "workflow/handoffs/temporal-associative-structural-growth-fan-in-formation-Luna-12I.md"
  tests_added:
    - "tests/test_luna12i_temporal_association.py: 4 focused tests"
  tests_passing:
    - "python -m pytest -q tests/test_luna12i_temporal_association.py: 4 passed"
    - "affected dependency slice: 58 passed"
    - "python -m pytest -q: 171 passed, 1 skipped"
    - "python -m compileall -q tpcn tests run_spiral_benchmark.py train_cpu_visualization.py"
    - "Workspace diagnostics for owned files: no errors"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "Full ExperimentRunner task-level temporal-association comparison: not run; this milestone owns the policy/control fixture only."
    - "Real dataset, GPU/FPGA/ModelSim, hardware equivalence, and architecture promotion: not applicable or unauthorized."
  assumptions:
    - "The existing Luna-10 controller remains the mutation authority."
    - "A source-local observer may retain a bounded recent event record for this experiment."
  unresolved:
    - "Task-level benefit, prediction/error change, energy/utility effect, and path-shortening benefit in the full ExperimentRunner remain untested."
    - "The policy's timing window and nearest-source rule remain experimental choices, not architecture requirements."
  recommended_next_agent:
    - "Luna-0 evidence review is complete; any Luna-12J work requires a separate dispatch."
```

## Dispatch and architectural question

Luna-12I is authorized on the current `main` baseline after Luna-12H's
intrinsic temporal-state and unequal-delay evidence. It tests whether a
source-local, bounded temporal association can guide structural growth toward
convergent causal structure. This is an experiment under ACP-0001, not a
change to the canonical architecture and not evidence that temporal growth is
useful until matched controls are run.

The falsifier is explicit: equivalent or worse convergent structure, path
delay, task/error behavior, or resource/churn behavior under temporal
association counts against the hypothesis. Failed admissions, duplicates,
capacity rejections, and negative seeds remain evidence.

## Implementation boundary

The policy may own only bounded local observation history and association
scores. It must emit the existing `CandidateEvidence` shape and use the
existing `StructuralPlasticityController` for locality, capacity, admission,
replacement, and pruning outcomes. It must not create a second topology or
feed labels, rewards, global statistics, or future events into a structural
decision.

The focused experiment will use a small deterministic event-sequence fixture
with at least one target receiving two legal source candidates. It will compare
fixed, existing-policy, random-legal, temporal, shuffled, and reversed
conditions under equal node, edge, fan-in/out, candidate, delay, growth, and
sequence budgets. The selected interval/window is experimental metadata only.

## Verification and gate

Required checks are focused policy and control tests, Luna-4/Luna-10 topology
and structural-plasticity regressions, Luna-12E routing regressions, relevant
Luna-12H temporal tests, full pytest, compile/static validation, workspace
diagnostics, and `git diff --check`. The completion record must separate
`OBSERVED`, `INFERRED`, and `HYPOTHESIZED` results and mark unavailable
real-dataset and hardware checks as not applicable.

The Luna-12I gate is **PASS** only if the policy is bounded, local,
deterministic, label-free, and all applicable regressions pass. Structural or
task improvement is not required for an experimental pass; any absence of
improvement must remain a recorded falsification/limitation. A failed
invariant or uncontrolled information path is **BLOCKED**. A passing
experiment authorizes only Luna-0 evidence review and does not promote the
mechanism or authorize Luna-12J without a separate dispatch.

## Completion evidence

### Outcome and unchanged behavior

Added `TemporalAssociationPolicy` and its bounded `TemporalAssociationState`
in `tpcn/temporal_association.py`. The policy accepts monotonic local
observations, retains at most `history_capacity` observations per node, and
increments a capped score only when a locally observed source is followed by a
declared local destination within the experimental positive time window. It
emits the existing `CandidateEvidence` interface with positive finite delay,
stable identifiers, and deterministic score/endpoint ordering.

Candidate capacity overflow is counted and reported as
`candidate_capacity`; reset clears sequence-local history, scores and rejection
evidence. No labels, rewards, predictions, evaluation metrics, topology-wide
statistics, random state, or future events enter the policy. The existing
`StructuralPlasticityController` remains responsible for admission, fan-in,
fan-out, edge capacity, locality and pruning. The canonical event runner,
Luna-12E routing, neuron semantics, contract and changelog were unchanged.

### Observed results

- **OBSERVED:** Three repeated `a -> c` local associations produce a bounded
  score of `3`, while a single `a -> d` association produces `1`; identical
  inputs reproduce identical candidates.
- **OBSERVED:** Reversing the local order removes the candidate in the control
  fixture. A grouped sequence produces score `2` because the policy uses the
  most recent source-local observation and the declared window.
- **OBSERVED:** Candidate capacity rejects the second distinct association and
  records `candidate_capacity: 1`; reset removes history, candidates and the
  rejection record.
- **OBSERVED:** Two temporal candidates targeting `c` are admitted through the
  existing bounded controller and produce two timestamped `a -> c` and
  `b -> c` arrivals at `t=1.0` in the real topology.
- **OBSERVED:** The matched random-legal control remains within edge and
  fan-in/out bounds. The fixture does not claim that temporal selection has
  better task or resource performance.
- **INFERRED:** The policy is compatible with A01-A04, A07-A08, A14 and A15
  because its state and output are finite, source-local, timestamp-based and
  delegated to existing bounded topology operations.
- **HYPOTHESIZED:** Repeated temporal association may improve useful
  convergent organization under a larger matched workload. This was not tested
  by the focused policy fixture and remains falsifiable.

### Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_luna12i_temporal_association.py` | Windows, Python reference, deterministic fixtures | passed: 4 | Bounded scoring, reversal, capacity/reset, convergent fan-in and random control |
| Affected dependency slice | Windows, deterministic | passed: 58 | Runtime, neuron, topology, structural plasticity, Luna-12E, Luna-12H, and 12I tests |
| `python -m pytest -q` | Windows, current worktree | passed: 171, skipped: 1 | Full repository regression |
| `python -m compileall -q tpcn tests run_spiral_benchmark.py train_cpu_visualization.py` | Current source | passed | No compilation errors |
| Workspace diagnostics | Owned implementation, tests and package export | passed | No errors found |
| `git diff --check` | Current worktree | passed | No whitespace errors |

### Gate decision

**PASS WITH FOLLOW-UP.** Luna-12I satisfies its bounded policy, locality,
label-isolation, deterministic replay, explicit rejection, fan-in routing and
regression criteria. The follow-up is required before any claim that temporal
association improves TPCN computation: run a separately controlled integration
comparison through the existing experiment path, including prediction/error,
energy/resource, path-delay, churn, and task metrics. This follow-up does not
promote the policy or alter A14.

Luna-12J is **not automatically authorized** by this handoff. It remains a
separate future experiment under the workflow and requires its own dispatch.
No real-dataset or hardware milestone is authorized by this result.

## Reproduction and rollback

Run `python -m pytest -q tests/test_luna12i_temporal_association.py` from the
repository root. Restore the pre-Luna-12I revision `5689106` and remove the
three Luna-12I implementation/test/export additions plus this handoff to
return to the prior state; no existing runtime or topology files require
rollback.

## Next assignment

Luna-0 retains architectural control. The next bounded work is an explicit
Luna-0 decision on whether to dispatch the task-level temporal-association
follow-up or separately dispatch Luna-12J. Until that dispatch, no later
implementation stage is authorized by Luna-12I.
