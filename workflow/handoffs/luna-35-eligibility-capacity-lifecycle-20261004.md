---
tpcn_handoff:
  agent: "Luna-35 Eligibility Capacity Lifecycle Characterization"
  luna_identifier: "Luna-35"
  descriptive_name: "Two-fixture eligibility capacity and lifecycle characterization"
  task_id: "luna-35-eligibility-capacity-lifecycle-20261004"
  component: "Per-character eligibility creation, predictor expiry, reward attribution, bounded capacity, and reset"
  status: "PASS — EXPECTED LIFECYCLE CONFIRMED; RETURNED TO LUNA-0"
  contract_version: "1.2"
  branch: "main"
  base_revision: "5b24e13216bc5adac518bb9d8c69d2342d75c2a2"
  result_revision: "Luna-35 publication commit"
  owner: "Luna-0 Architecture Guardian"
  classification: ["OBSERVATION", "LIFECYCLE CHARACTERIZATION", "DETERMINISTIC REPLAY"]
  hypothesis: "The exact Luna-34 two-node no-edge stream creates distinct eligibility records which remain resident after their linked predictor records expire and reaches the fixed per-ledger capacity before character completion."
  counter_hypothesis: "Predictor expiry, a delivered prediction error/reward, or another current runtime lifecycle event retires or reuses an eligibility record before the fixed capacity is reached."
  interfaces_relied_on:
    - "Luna-34 point generation, point conversion, and equal-timestamp batch helpers"
    - "EligibilityLedger.record_activity / _decay_to / apply_signal"
    - "ExcursionCharacterRuntime.start_character / end_character / _destroy_character"
    - "LocalPredictor.create_prediction / observe / expire"
  label_information_boundary:
    - "Only the selected examples' points were read and saved; no label or label-bearing metadata was accessed."
  timing_assumptions:
    - "The eligibility ledger advances only on its own addressed activity or signal events, not on predictor expiration."
    - "Point index 19 names the incoming batch whose admission attempt first failed; runtime source code drains earlier pending events before admitting that point."
  reset_boundaries:
    - "end_character applies its outer-readout reward before _destroy_character."
    - "_destroy_character clears the runtime's predictor and ledger references; the subsequent character start allocates fresh, empty ledgers."
  resource_bounds:
    - "Two neutral MultiExcursionNeuron(config=E1Config()) nodes; no route edges."
    - "prediction_capacity=8; max_traces=16 in each per-node ledger; 32 aggregate allocated slots."
    - "queue_capacity=128; event_budget=1024; settling_horizon=4.0; prediction_expiry=4.0."
    - "EligibilityLedger.expiry is None in the integrated runtime."
  authorized_scope:
    - "Execute only the fixed 20-point c00-004 no-edge capacity reproducer and one one-point no-edge lifecycle control."
    - "Capture bounded event-local predictor, eligibility, signal, occupancy, and character-boundary evidence."
    - "Replay the same two fixtures once for deterministic evidence comparison."
  unauthorized_scope:
    - "No edge conditions, full Luna-34 design, efficacy endpoint, capacity/expiry change, production edit, ACP change, or Luna-36 authorization."
  measurements:
    - "Primary fixture: 16 successful unique eligibility creations, zero removals, peak/final source occupancy 16/16, and a rejected seventeenth insertion."
    - "Failure: input point index 19 admission call; source and runtime processed-event counts 59; source:excursion:17 at t=255.79833294576443."
    - "All 16 linked predictions expired (last expiry t=255.29833294576443); all 16 eligibility records remained resident; no prediction-error/reward signal reached the ledger before failure."
    - "Control: one eligibility creation; neutral reward matched its explicit trace ID without changing occupancy; destruction released one ledger trace reference; next-character ledgers were fresh and empty."
    - "Two-fixture deterministic replay digests matched: 45485ddfafac2878e267a8e5dcc4ab76c3c335f279802ac98b0d5c44758920cb."
  architecture_change: false
  proposal: null
  files_changed:
    - "run_luna35_eligibility_capacity_lifecycle.py"
    - "tests/test_luna35_eligibility_capacity_lifecycle.py"
    - "artifacts/luna35-eligibility-capacity-lifecycle/config.json"
    - "artifacts/luna35-eligibility-capacity-lifecycle/results.json"
    - "artifacts/luna35-eligibility-capacity-lifecycle/summary.json"
    - "workflow/handoffs/luna-35-eligibility-capacity-lifecycle-20261004.md"
  tests_added:
    - "Three focused Luna-35 tests for exact occupancy, predictor/reward/reset lifecycle, and replay/artifact bounds."
  tests_passing:
    - "Focused Luna-35, eligibility, excursion integration, and prediction tests: 77 passed."
    - "Full repository suite: 932 passed, 1 skipped; 933 collected."
    - "The full-suite skip is tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics because CUDA is unavailable."
    - "compileall for tpcn, tests, Luna-35 runner: passed."
    - "Pylance diagnostics on the Luna-35 runner and tests: no diagnostics."
    - "Deterministic replay: exact two-fixture observation digests match."
    - "git diff --check: passed."
  tests_failed: []
  tests_not_run:
    - "No additional unique fixture, topology condition, Luna-34 edge comparison, 960-execution design, or efficacy run was performed."
    - "No CUDA test body ran because CUDA is unavailable."
  assumptions:
    - "The supplied requested revision string was not a resolvable Git commit; in the unavailable-user fallback, execution used the clean synchronized origin/main revision 5b24e13216bc5adac518bb9d8c69d2342d75c2a2."
  unresolved:
    - "No contract says predictor expiration must retire an eligibility entry."
    - "Whether retaining predictor-expired traces until character destruction is the desired capacity policy remains unresolved."
    - "The fixed fixtures do not establish a general per-character workload-capacity guarantee."
  recommended_next_agent: ["Luna-0 Architecture Guardian"]
---

# Luna-35 completion handoff

## Baseline and scope

Fetched `origin/main` before any code change. The worktree was clean and
`HEAD == origin/main == 5b24e13216bc5adac518bb9d8c69d2342d75c2a2` on `main`.
The request also supplied
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb`; Git could not resolve that
identifier as a commit. The user was unavailable to clarify, so the run used
the actual clean synchronized `origin/main` published Luna-0 authorization
revision and records that fact in `config.json`. The Luna-34 evidence baseline
remains `4d77489eaebadf638f22996d1d0d49e162b378ab`.

The implementation changed only the six files authorized by
`.github/agents/luna-35.agent.md`. Instrumentation is confined to the
Luna-35 runner: wrappers call the original ledger, predictor, and runtime
methods exactly once, and record pre/post state without changing capacity,
expiry, reward, prediction, neuron, or topology behavior. Only the two
predeclared no-edge fixtures ran. Replay reran those same fixtures; it did not
introduce a third fixture.

## Exact fixtures and capacity

The reproducer used seed `0`, `NO_EDGE_CONTROL`, shuffled sequence index `4`
(`c00-004`), all 20 original training points, and the unchanged
`random.Random(330000)` shuffle. Input is `point.x + point.y` at the original
point timestamp. The one-point control used only point 0 of this same
generated point sequence, with the same transform. Both networks used two
neutral `MultiExcursionNeuron(config=E1Config())` instances and no route edges.

Runtime source inspection confirms that `start_character()` creates one
ledger per node with
`max_traces = prediction_capacity * max(1, len(neurons))`. With
`prediction_capacity=8` and two nodes, this gives 16 trace slots in each of
two ledgers, 32 allocated slots total. Each slot is local to its ledger.
Integrated runtime construction supplies no eligibility `expiry`.

## Primary fixture: predictor expiry and capacity failure

The first 16 source canonical emissions each created one distinct eligibility
entry. Each activity record includes its node and ledger, trace/prediction/
canonical-emission IDs, creation ordinal, timestamp, magnitude, predictor
status, and occupancy transition. Source occupancy advanced `0/16 -> 1/16`
through `15/16 -> 16/16`; no trace was removed.

The seventeenth activity was rejected:

| Observation | Value |
|---|---|
| Failing `admit_external_batch` point index | `19` |
| Trigger point | `t=269.4146695418062`, `x=1.606716300249158`, `y=1.2517434830559917`, input `2.8584597833051495` |
| Failure phase | Runtime drained earlier pending events before admitting point 19; the point itself had not yet been admitted |
| Source / runtime processed event counts | `59 / 59` |
| Canonical emission | sequence `17`, ID `source:excursion:17`, timestamp `255.79833294576443` |
| Eligibility insertion | `luna35:c00-004:source:excursion:17`, linked predictor `luna35:c00-004:predictor:prediction:16` |
| Occupancy after time decay, immediately before rejection | `16/16` |
| Exception | `EligibilityCapacityError: eligibility trace capacity reached` |

All 16 resident entries are preserved in `results.json`, including their
identities, prediction IDs, post-decay values, credits, and timestamps.
Immediately before the failed insertion, each had `last_timestamp` equal to
`255.79833294576443`; values were decayed but nonzero and credits were zero.
The attempted seventeenth prediction was still outstanding. Sixteen prior
predictors had expired; the first expired at `14.198344366156627` and the last
at `255.29833294576443`. For every expiry, the linked eligibility trace was
observed resident. Predictor expiry did not advance the corresponding ledger
clock or remove the trace.

The fixed sequence reached 17 predictor creations and 19 point observations
before failure. No prediction-error or reward signal reached a ledger, and
`end_character()` was not reached, so its neutral reward did not precede or
cause the overflow. Occupancy reconciles as `0 + 16 creations - 0 removals =
16`; the next unique insertion was rejected without eviction.

## Lifecycle control: reward and character destruction

The one-point fixture created one source eligibility trace at `t=0.5`
(`0/16 -> 1/16`), linked to its single outstanding predictor. The end-character
neutral reward at `t=4.0`, message ID
`neutral-luna35-lifecycle-0`, explicitly matched the trace ID. Its attribution
status was `matched`; the trace value decayed from `0.4227634632752029` to
`0.176234031147182`, its zero reward left credit at `0.0`, and occupancy
remained `1/16 -> 1/16`. The reward did not retire the entry.

Immediately before `_destroy_character`, the source ledger still contained
that one trace. The runtime destroys the character by clearing its ledger
references (not by a predictor-expiry callback or per-trace retirement
event); the observed whole-ledger release was one trace reference. Starting
the next character allocated distinct source and destination ledger IDs with
zero traces. The accounting reconciles:
`0 + 1 creation - 0 eligibility-expiry removals - 1 character-boundary
release = 0`.

The experiment also confirmed what the implementation expects for a
within-character eligibility retirement: `_decay_to()` removes an entry only
if that ledger has an eligibility `expiry` and a later ledger event advances
time beyond it. Predictor expiry does not call this ledger operation.
`apply_signal()` credits a matched entry and does not remove it. Since the
integrated runtime configures `expiry=None`, no per-entry eligibility expiry
event is active in these fixtures; the observed close of live character state
is the existing end-character destruction boundary.

## Classification and limits

**EXPECTED LIFECYCLE CONFIRMED**, narrowly: eligibility and predictor
lifetimes are separate; no established contract says predictor expiration
retires eligibility; matched neutral reward did not delete the entry; the
existing character boundary released the ledger state and the next character
started with fresh empty ledgers. This confirms the observed behavior and
does not resolve whether the per-character capacity policy is desirable for
all workloads.

No production defect is established. The fixed evidence is sufficient for
Luna-0 to consider a separately bounded governance/diagnostic proposal that
defines the desired relationship between predictor lifetime, eligibility
retention, and workload capacity. It does not itself authorize changing
production behavior. Luna-34 remains **BLOCKED / UNDETERMINED**; its edge
conditions and propagation-to-emission question were not run or answered.
Luna-33 remains unchanged. No architecture change or Luna-36 is recommended
or authorized.

## Artifacts and validation

The complete event evidence, including all 20 primary input points, all
activity attempts, predictor creation/observation/expiry identities, the full
pre-failure resident trace set, the control reward transition, and both
character boundaries is in:

- `artifacts/luna35-eligibility-capacity-lifecycle/config.json`
- `artifacts/luna35-eligibility-capacity-lifecycle/results.json`
- `artifacts/luna35-eligibility-capacity-lifecycle/summary.json`

The deterministic replay digests match:
`45485ddfafac2878e267a8e5dcc4ab76c3c335f279802ac98b0d5c44758920cb`.

- Focused Luna-35 + eligibility + excursion integration + prediction tests:
  **77 passed**.
- Full suite: **932 passed, 1 skipped; 933 total**. The skip is
  `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`
  because CUDA is unavailable.
- Luna-35 added 3 focused tests; full-suite count increased by exactly 3 from
  the reviewed pre-Luna-35 930 tests.
- `compileall -q tpcn tests run_luna35_eligibility_capacity_lifecycle.py`:
  passed.
- Pylance syntax and file diagnostics: no syntax errors or diagnostics.
- `git diff --check`: passed.

**Luna-35 complete; returned to Luna-0 for independent post-Luna-35 review.
No Luna-36 authorized.**
