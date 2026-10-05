---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-Luna-34 eligibility-capacity and lifecycle review"
  task_id: "luna-0-independent-review-luna34-eligibility-capacity-20261004"
  component: "Luna-34 blocker reproduction, eligibility ledger lifecycle, and bounded next authorization"
  status: "PASS — BLOCKER REPRODUCED; LUNA-35 AUTHORIZED / NOT EXECUTED"
  contract_version: "1.2"
  branch: "main"
  base_revision: "4d77489eaebadf638f22996d1d0d49e162b378ab"
  result_revision: "Luna-0 review publication on origin/main"
  owner: "Luna-0 Architecture Guardian"
  classification: ["OBSERVATION", "INDEPENDENT VERIFICATION", "GOVERNANCE DECISION"]
  hypothesis: "The required two-node, prediction_capacity=8 runtime deterministically accumulates one distinct source eligibility trace per canonical emission until the source ledger's 16-entry hard bound rejects emission 17; predictor expiry does not retire those eligibility entries."
  counter_hypothesis: "The fixed no-edge fixture completes or an existing predictor/reward/character lifecycle event retires a resident trace before the seventeenth unique source trace."
  interfaces_relied_on:
    - "Luna-34 public runtime fixture, config, runner and test artifacts"
    - "EligibilityLedger.record_activity / apply_signal / optional expiry / reset"
    - "ExcursionCharacterRuntime.start_character / _consume_emission / end_character / _destroy_character"
    - "LocalPredictor.observe / expire"
  label_information_boundary:
    - "Reproduction accessed only generated point sequences, never labels or label-bearing metadata."
  timing_assumptions:
    - "Eligibility and predictor timestamps are causal local event times; predictor expiry does not imply eligibility expiry."
  reset_boundaries:
    - "Runtime allocates new ledgers for each character and drops ledger references at character destruction."
  resource_bounds:
    - "prediction_capacity=8; two ledgers; max_traces=16 per ledger; 32 aggregate allocated trace slots; runtime event budget=1024; queue capacity=128."
  authorized_scope:
    - "Independently reproduce and instrument the first Luna-34 failure without modifying production behavior."
    - "Review eligibility capacity/retirement semantics, prior Luna-5/Luna-8/Luna-13A evidence, Luna-34 compliance, and focused/full regression."
    - "Authorize a single bounded eligibility lifecycle characterization as Luna-35."
  unauthorized_scope:
    - "No production fix, capacity/expiry change, Luna-34 rerun, propagation-to-emission measurement, efficacy measurement, ACP change, or Luna-36 authorization."
  controls:
    - "Luna-34 first-failure fixture: seed 0, NO_EDGE_CONTROL, sequence 4."
    - "Existing one-point no-edge focused runtime test as low-activity context."
  measurements:
    - "16 resident unique traces at capacity; failed insertion is source excursion 17 at t=255.79833294576443 after 59 processed source events."
    - "16 linked predictions expired by t=255.29833294576443; none matched, no prediction error delivered, no reward reached."
    - "Luna-34 changed exactly the six authorized deliverables."
  information_boundary_check:
    - "No labels, readout outputs, or class-derived information used."
  hardware_mapping:
    - "Software-reference lifecycle review only; no hardware evidence."
  architecture_invariants_touched: ["A02", "A07", "A08", "A11", "A15"]
  preserves:
    - "Architecture Contract 1.2 and accepted ACP-0007."
    - "Luna-33 verdict NOT SUPPORTED IN THIS SETUP."
    - "Luna-34 mechanism hypothesis remains UNDETERMINED."
    - "Deterministic finite eligibility overflow behavior; no silent eviction."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-35.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-independent-review-luna34-eligibility-capacity-20261004.md"
  tests_added: []
  tests_passing:
    - "Focused eligibility/runtime/Luna-34 slice: 71 passed."
    - "Full suite: 929 passed, 1 skipped."
    - "Test collection: 930 tests."
    - "Luna-34 runner/tests compilation and git diff --check passed."
    - "Independent no-edge reproduction with test-local audit wrappers confirmed exact failure and capacity occupancy."
  tests_failed: []
  tests_not_run:
    - "Full Luna-34 960-execution mechanism diagnostic remains blocked/not rerun."
    - "Luna-35 lifecycle characterization is authorized but not executed."
    - "CUDA test body skipped because CUDA is unavailable."
  assumptions:
    - "Luna-34's first uncaught run followed the runner's nested seed/condition/sequence order; independent replay confirms the first failure at seed 0 / no-edge / sequence 4."
  unresolved:
    - "Whether retaining predictor-expired traces until character destruction is required delayed-credit behavior or avoidable occupancy remains to be characterized."
    - "No declared/tested contract ties predictor_capacity numerically to eligibility max_traces."
    - "A legitimate capacity for this workload and a safe Luna-34 execution path are not established."
  recommended_next_agent: ["Luna-35 Eligibility Capacity Lifecycle Characterization"]
---

# Independent post-Luna-34 review

## Baseline, authorities, and scope

Review began after fetching `origin/main` at clean synchronized `main`:

```text
HEAD = origin/main = 4d77489eaebadf638f22996d1d0d49e162b378ab
worktree = clean
```

Read the Luna-34 contract, runner, tests, artifacts and handoff; the Luna-0
post-Luna-33 decision; ACP-0007; Architecture Contract 1.2; workflow and
changelog; `tpcn/eligibility.py`; `tpcn/experiment_excursion_runtime.py`;
`tpcn/predictive_coding.py`; and the Luna-5, Luna-8 and Luna-13A handoffs and
relevant tests.

The commit changes relative to Luna-34 are exactly the six files listed in
its handoff: runner, focused tests, `config.json`, `results.json`,
`summary.json`, and Luna-34 handoff. No production, ACP, workflow, changelog,
Luna-33 or historical result file changed. The artifacts accurately describe
one incomplete attempt, no serialized character result, and undetermined
outcomes. The runner writes its three artifacts only after all seed/condition
loops complete; thus the reported first failure prevented normal run output.
No hidden full-design retry, silent capacity increase, selective condition
skip, or scientific result inference was found. The focused tests call only
small fixtures and do not amount to a full matrix retry.

## Independent blocker reproduction

The exact first failure was reproduced from the committed point-generation
function with local instrumentation wrappers around existing ledger/predictor
methods. The command was an inline Python invocation of the `.venv` Python
interpreter that called `_training_point_sequences(0)` and then
`_character_record(seed=0, sequence_index=4, condition="NO_EDGE_CONTROL",
points=...)`; it did not write artifacts or change repository files.

Observed first failure:

| Field | Observed |
|---|---|
| Seed / condition / sequence | `0` / `NO_EDGE_CONTROL` / `4` |
| Opaque character ID / points | `c00-004` / 20 |
| Ledger | `luna34:c00-004:ledger:source` |
| Exception | `EligibilityCapacityError: eligibility trace capacity reached` |
| Occupancy / per-ledger capacity | 16 / 16 |
| Incoming activity | source emission `source:excursion:17`, trace `luna34:c00-004:source:excursion:17`, predictor `...prediction:16` |
| Emission timestamp / payload | `255.79833294576443` / `0.5406345932947867` |
| Runtime/source-neuron processed events | 59 / 59 |
| Canonical emissions already appended | 17 |

The 16 resident trace IDs are the unique source emissions 1–16. They have
zero credit. All 16 linked predictor records were observed to expire before
the failed insertion; the predictor had 16 expirations, 19 unmatched
observations, zero matched predictions, one still-outstanding prediction,
and no delivered prediction errors. The resident eligibility records still
existed after predictor expiration. No neutral end-character reward occurred:
the exception preceded `end_character()`.

The four earlier no-edge sequence records returned in memory, but the list
comprehension did not finish, so no `run_experiment()` artifacts were written.
The failure coordinate claimed “not captured” in the initial Luna-34 artifact
describes its first uncaught attempt; the independent replay now establishes
the exact first coordinate.

## Capacity derivation and eligibility lifetime

`ExcursionCharacterRuntime.start_character()` creates one
`EligibilityLedger` per neuron with
`max_traces = prediction_capacity * max(1, len(neurons))`. For this fixed
two-node fixture, each ledger has 16 entries. Since there are two ledgers,
aggregate allocated maximum is 32; the source-local limit remains 16. The
node-count multiplier is applied once in each ledger constructor and then
there are `len(neurons)` separate ledgers, yielding an aggregate
`prediction_capacity * node_count²` allocation for networks with at least one
node. The code and current tests do not document or assert a normative
relationship between outstanding prediction capacity and eligibility trace
capacity. A capacity slot represents a distinct local `trace_id`, not a
prediction.

Each canonical emission creates an `EligibilityActivity` with trace ID
`namespace:character:event_id`; a source emission additionally carries its
new predictor ID. Luna-34 therefore creates one distinct source trace for
each source emission. In the reproducer, each of the first 16 records refers
to a different prediction ID, so one prediction does not fan out into
multiple eligibility entries. The generic ledger can match a signal against
more than one trace sharing a prediction ID but deterministically selects
one trace; that condition was not present here.

`EligibilityLedger.record_activity()` advances/decays local time, updates an
existing trace or raises before adding a new unique trace at capacity. Its
`expiry` is optional and defaults to `None`; the integrated runtime does not
pass an expiry. With no expiry, elapsed-time decay changes values but does
not release slots. A configured expiry only removes a trace when a later
ledger activity/signal invokes `_decay_to()` and the trace age is strictly
greater than that expiry. `apply_signal()` updates credit but does not remove
a matched trace. Unmatched signals do not mutate or decay trace state.
Predictor expiry is a separate operation and has no callback that removes
the corresponding eligibility trace.

The runtime supplies the existing character boundary: it creates new
predictor/ledger state on every `start_character()`, and
`_destroy_character()` clears its ledger references at `end_character()`.
Luna-34 creates a fresh runtime/neuron set per character. Successive streams
do not share eligibility ledgers in this path. At the reproduced failure,
the character did not reach its existing reset boundary.

## Contract and historical checks

Luna-8 explicitly describes finite trace capacity, optional expiry and
deterministic overflow without silent eviction. `test_trace_capacity_has_deterministic_overflow`
asserts that a second unique trace at capacity raises and leaves the first
trace resident. The same handoff describes reset as clearing trace state.
Luna-13A establishes bounded retry-idempotent reward identity behavior; that
bounded identity table is separate from trace slots. Reward identity and
duplicate detection did not contribute to this failure.

Consequently the **overflow exception itself is expected bounded-capacity
behavior**, and no established invariant proves a production defect. However,
the derived limit is not part of Luna-34's explicit config, there is no public
runtime control for it, and no declared workload envelope promises fewer than
16 source emission traces in a character. The exact generated fixture reaches
17. Predictor expiry and ledger retention are separate, with no current
contract resolving whether that persistence is needed for delayed credit or
is avoidable capacity pressure. This is not enough evidence to label the
runtime defective or to raise its capacity.

No safe correction to the fixture preserves both the authorized fixed
training points and the required runtime interface; dropping points or
increasing capacity would change the declared experiment. A direct neuron
simulation that bypasses integrated eligibility would not be the same
authorized runtime path. Luna-34 therefore remains validly **BLOCKED** under
its frozen constraints; its propagation-to-emission hypothesis remains
**UNDETERMINED**.

## Regression validation

- Focused `tests/test_eligibility.py`, `tests/test_excursion_integration.py`,
  and Luna-34 tests: **71 passed**.
- Full suite: **929 passed, 1 skipped**.
- Collection: **930 tests**.
- The pre-Luna-34 baseline was 920 passed, one skip, and 921 collected.
  Luna-34 added exactly nine focused tests, explaining the +9 test and
  collection counts. No unrelated test-count change was observed.
- The skipped test remains the CUDA case; CUDA is unavailable.
- Luna-34 runner/test compilation and `git diff --check` passed.
- Luna-35 is not executed in this review.

## Governance decision

**Luna-34 blocker independently confirmed. No production defect established.
Luna-35 authorized / not executed, solely for bounded eligibility
capacity/lifecycle characterization.**

The new contract is
`.github/agents/luna-35.agent.md`. It authorizes only two no-edge diagnostic
fixtures: the 20-point `c00-004` capacity reproducer and a one-point
character-reset control. It forbids a propagation-to-emission retry, all
edge conditions, efficacy endpoints, capacity/expiry changes, and production
edits. Luna-35 must return to Luna-0; no Luna-36 is authorized.

Architecture Contract 1.2, ACP-0007, the Luna-33 **NOT SUPPORTED IN THIS
SETUP** verdict, and the Luna-34 original mechanism question are unchanged.
This review does not identify an architecture change requirement.
