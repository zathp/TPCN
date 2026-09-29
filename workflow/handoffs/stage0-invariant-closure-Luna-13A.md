---
tpcn_handoff:
  agent: Luna-13A
  luna_identifier: "Luna-13A"
  descriptive_name: "Stage-0 Software Reference Invariant Closure"
  task_id: "stage0-invariant-closure"
  component: "CPU software reference classifier, structural admission, and bounded event execution"
  status: "blocked"
  terminal_status: "BLOCKED — REWARD CONTRACT DECISION REQUIRED"
  contract_version: "1.1"
  branch: "main"
  base_revision: "00d00fdfa74aa8dcf7102b8906b153778e475dcd"
  result_revision: "uncommitted"
  tree_state: "dirty; only listed implementation, focused tests, and this handoff are changed"
  dependencies: []
  owner: "Luna-0"
  classification:
    - "OBSERVED: implementation and verification work is complete for classifier monotonicity, projected structural capacity, and bounded recurrent execution."
    - "OBSERVED: reward delivery authority remains contradictory; reward work is blocked at the mandatory architecture decision point."
  hypothesis: "OBSERVED: stale classifier finalization mutates only because finalize_character did not validate timestamp before mutation; projected batch admission must validate aggregate degrees before topology replacement; bounded queue occupancy alone does not bound recurrent lifetime work."
  counter_hypothesis: "A focused test failure, post-validation mutation, individually-valid jointly-invalid admission, or budget-exhausted run reported as completed would falsify the corresponding repair."
  interfaces_relied_on:
    - "StreamingCharacterClassifier.ingest_event and finalize_character"
    - "StructuralPlasticityController.adapt_many and _commit_growth"
    - "EventQueue, BoundedTopology, and execute_bounded"
    - "ExperimentRunner and ExperimentMetrics"
  label_information_boundary:
    - "OBSERVED: no labels were added to core neural events, topology routing, classifier activity, or recurrent execution."
    - "OBSERVED: labels remain external readout/training information."
  timing_assumptions:
    - "OBSERVED: classifier timestamps remain monotonic; stale finalization is rejected before mutation; equal-time behavior follows existing event ordering."
    - "OBSERVED: recurrent routing preserves finite positive edge delays and queue tie ordering."
  reset_boundaries:
    - "OBSERVED: classifier reset clears character-local timestamp, active state, scores, result, and committed state."
    - "OBSERVED: experiment network reset remains character-local."
  resource_bounds:
    - "OBSERVED: execute_bounded requires a positive integer finite event budget and reports processed, pending, configured budget, peak occupancy, and termination reason."
    - "OBSERVED: reward identity tracking was not added because the reward contract is unresolved."
  authorized_scope:
    - "Repair four Stage-0 surfaces only: classifier temporal monotonicity, reward-contract decision evidence, projected structural capacity, and bounded recurrent execution."
    - "Add focused tests, this handoff, and relevant documentation."
  unauthorized_scope:
    - "GPU, CUDA, FPGA, FPAA, hardware equivalence, dataset benchmark, temporal-policy efficacy, and successor-Luna authorization."
    - "Changing reward semantics without Luna-0 authority."
  controls:
    - "OBSERVED: focused classifier stale/equal/future and direct/dispatched tests."
    - "OBSERVED: focused projected fan-in/fan-out, duplicate, simultaneous-failure, atomic rejection, reason, and observer-equivalence tests."
    - "OBSERVED: recurrent positive-delay execution tested at budgets 1, 2, 8, and 64."
  measurements:
    - "OBSERVED: focused Stage-0/regression selection: 98 passed."
    - "OBSERVED: full CPU suite: 234 passed, 1 skipped."
    - "OBSERVED: compileall and git diff --check completed without output/errors."
    - "NOT APPLICABLE: GPU/hardware measurements."
  information_boundary_check:
    - "OBSERVED: existing Luna-12N label isolation and instrumentation negative controls remain covered by the passing regression suite."
  hardware_mapping:
    - "OBSERVED: CPU-only software reference validation."
    - "NOT APPLICABLE: CUDA/GPU/FPGA/FPAA execution."
  architecture_invariants_touched:
    - "A01 event-driven operation"
    - "A02 intrinsic temporal state"
    - "A04 bounded topology"
    - "A06 explicit predictive/error event path preserved"
    - "A07 local learning preserved"
    - "A08 bounded state and dynamics"
    - "A11 delayed credit preserved but reward delivery contract unresolved"
    - "A15 hardware independence"
  preserves:
    - "Positive finite inter-neuron delays"
    - "No global timestep or centrally clocked neural execution"
    - "No label leakage or unrestricted backpropagation"
    - "Existing reset and information-boundary rules"
    - "Luna-12N configured-versus-actual accounting, timestamps, provenance, and intervention distinctions"
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/streaming_classifier.py"
    - "tests/test_streaming_classifier.py"
    - "tpcn/structural_plasticity.py"
    - "tests/test_structural_plasticity.py"
    - "tpcn/event_runtime.py"
    - "tpcn/experiments.py"
    - "tpcn/__init__.py"
    - "tests/test_event_runtime.py"
    - "workflow/handoffs/stage0-invariant-closure-Luna-13A.md"
  tests_added:
    - "Classifier stale finalization atomicity, equal-time/future ordering, direct/dispatched agreement, and state evidence."
    - "Projected structural-capacity and rejection-reason tests."
    - "Bounded recurrent execution budget/status tests."
  tests_passing:
    - "python -m pytest -q tests/test_streaming_classifier.py tests/test_eligibility.py tests/test_event_runtime.py tests/test_structural_plasticity.py tests/test_luna12h_temporal.py tests/test_luna11_adversarial.py tests/test_luna12m_edge_instrumentation.py tests/test_luna12n_temporal_direction.py: 98 passed."
    - "python -m pytest -q tests/test_event_runtime.py tests/test_experiments.py: 26 passed."
    - "python -m pytest -q: 234 passed, 1 skipped."
    - "python -m compileall -q tpcn tests: passed."
    - "git diff --check: passed."
  tests_failed: []
  tests_not_run:
    - "GPU/hardware tests as architecture evidence: not applicable to CPU-only Stage 0; the optional CUDA skip does not block this assignment."
  assumptions:
    - "INFERRED: the existing classifier timestamp ordering contract is authoritative for stale rejection and equal-time acceptance."
    - "INFERRED: structural batch admission is all-or-none and deterministic reason precedence is duplicate, edge capacity, fan-in, then fan-out, followed by topology capacity fallback."
  unresolved:
    - "BLOCKER: reward authority is contradictory. Production EligibilityLedger.apply_signal currently repeatedly applies identical numeric RewardSignal values when no message identity exists; test_luna11_adversarial.py explicitly asserts this non-idempotent behavior. Other architecture/documentation claims retain duplicate-suppression or exactly-once language."
    - "DECISION PACKET: Model A would add bounded logical reward identity tracking with declared reset, retention, and eviction semantics, make same-message replay credit once, and preserve distinct equal-valued messages as independent. Model B would retain repeated application, remove obsolete exactly-once claims, and make replay intentionally non-idempotent."
    - "CONSEQUENCES: Model A adds bounded state and deterministic replay requirements; Model B avoids identity state but makes duplicate delivery materially affect credit and replay results. Neither may be selected by this agent."
    - "Affected reward surfaces include tpcn/eligibility.py, tpcn/energy_utility.py, tests/test_eligibility.py, tests/test_luna11_adversarial.py, architecture contracts, and replay/handoff documentation."
  recommended_next_agent:
    - "Luna-0 independent Stage-0 review is required. Luna-0 must resolve the reward contract contradiction before any reward implementation or promotion decision."
    - "Do not authorize, dispatch, or approve Luna-13B or any successor Luna from this handoff."
---

## Outcome and owned scope

This run closed three Stage-0 implementation surfaces. `StreamingCharacterClassifier.finalize_character` now validates timestamp legality before any mutation and exposes its local timestamp for atomic before/after evidence. Structural batch growth now preflights projected fan-in, fan-out, edge capacity, and duplicates before replacement; rejected batch results retain meaningful deterministic reasons. `execute_bounded` centralizes finite recurrent execution accounting and is integrated into the experiment network and metrics.

The reward surface was inspected but intentionally unchanged. The current production behavior and repository authority disagree about whether repeated delivery of the same logical reward is idempotent. That is an architecture decision, not a test-only repair.

## Classifier evidence

**OBSERVED:** stale finalization with `START` at `t=0`, activity at `t=8`, and direct finalization at `t=5` is rejected before mutation. The focused tests compare local timestamp, active state, scores, result/output, character index, activity count, and committed state before and after. Accepted equal-time and future finalization, dispatched entry, and retry behavior pass.

**INFERRED:** the ordering contract is monotonic local time with equal-time events accepted according to existing sequence ordering; stale events are atomic no-ops through rejection.

## Structural-capacity evidence

**OBSERVED:** jointly invalid candidate batches are rejected atomically using projected degree counts. Duplicate/existing edges and simultaneous capacity causes are covered, with deterministic reason precedence and reason-preserving `MutationResult` values. Instrumentation on/off equivalence remains covered by the Luna-12M negative control.

## Recurrent-budget evidence

**OBSERVED:** positive-delay recurrent fixtures at budgets `1`, `2`, `8`, and `64` distinguish `completed` from `budget_exhausted` and report configured budget, processed count, pending count, termination reason, last timestamp, and peak occupancy. No global timestep, hidden tick, or unbounded retry loop was introduced.

## Reward decision packet

**OBSERVED:** repeated identical numeric rewards currently credit repeatedly when no logical message identity is present; this is asserted by the existing adversarial test. **OBSERVED:** repository documentation/tests also contain exactly-once or duplicate-suppression expectations. **INFERRED:** the authority is contradictory.

**HYPOTHESIZED:** Model A is preferable if replay determinism and logical-message delivery semantics are authoritative, but this is only a recommendation for Luna-0 and is not an implementation decision here. Model B is coherent if every delivered event is intentionally an application. Luna-0 must select and document one model, including reset, bounded retention/eviction, equal-valued distinct rewards, and replay semantics.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Focused Stage-0/regression pytest selection | Windows CPU, working tree based on `00d00fd` | 98 passed | pytest output |
| Runtime and experiment pytest selection | Windows CPU, working tree based on `00d00fd` | 26 passed | pytest output |
| Full CPU pytest suite | Windows CPU | 234 passed, 1 skipped | pytest output; skip is optional CUDA/GPU and not applicable |
| `python -m compileall -q tpcn tests` | Windows CPU | passed | no output/errors |
| `git diff --check` | working tree | passed | no output/errors |
| GPU/CUDA/FPGA/FPAA execution | CPU-only Stage 0 | not applicable/not run | explicitly out of scope |

## Benchmark and resource results

No dataset benchmark, GPU result, hardware result, physical-energy result, or architecture-promotion result was produced. The recurrent execution measurements above are software event-accounting measurements only. Classification/prediction and local utility metrics remain existing experiment outputs; this assignment does not claim efficacy improvement.

## Assumptions, limitations and unresolved issues

The reward contradiction is the sole release blocker identified by the required Stage-0 decision point. No reward identity set, eviction policy, or replay contract was invented. Unrelated worktree changes were not reverted.

## Reproduction and rollback

From the repository root, run the validation commands in the table. The safe restoration point is revision `00d00fdfa74aa8dcf7102b8906b153778e475dcd`; implementation changes are currently uncommitted and can be reviewed or selectively reverted without changing the published Luna-13A contract commit.

## Next assignment

Return to Luna-0 for independent Stage-0 review and reward-contract resolution. This handoff does not authorize Luna-13B or any successor Luna. A later temporal structural-selection experiment remains only a future direction contingent on Luna-0 review.
