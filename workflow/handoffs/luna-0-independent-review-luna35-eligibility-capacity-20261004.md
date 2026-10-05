---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-Luna-35 eligibility lifecycle review"
  task_id: "post-luna35-eligibility-capacity-lifecycle-review"
  component: "EXCURSION eligibility ledgers, predictor expiry, delayed reward"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "b0507cb68776011dba482907b0ac763bec2a225f"
  result_revision: "The Git commit containing this handoff and governance update"
  dependencies:
    - "Luna-35 eligibility-capacity-lifecycle characterization"
    - "Luna-0 post-Luna-34 eligibility-capacity review"
  owner: "Luna-0"
  classification:
    - "EXPECTED BOUNDED BEHAVIOR"
    - "CONTRACT AMBIGUITY"
    - "PUBLIC API LIMITATION"
  hypothesis: "Predictor expiry is not an eligibility retirement event, and retained eligibility can still support delayed reward attribution."
  counter_hypothesis: "An established invariant requires eligibility retirement on predictor expiry or another lifecycle event that Luna-35 failed to observe."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime per-node eligibility ledgers"
    - "Predictor expiration and identity"
    - "EligibilityLedger creation, decay, capacity, and apply_signal behavior"
    - "EXCURSION end-character reward and character-destruction paths"
  label_information_boundary:
    - "No labels or task-accuracy endpoints used."
  timing_assumptions:
    - "Predictor expiration and eligibility ledger time are separate lifecycle operations."
    - "Timestamps are the software-reference logical timestamps recorded by the runtime."
  reset_boundaries:
    - "Eligibility ledger objects are scoped to a character runtime and released at character destruction."
  resource_bounds:
    - "Each ledger is bounded by prediction_capacity * max(1, neuron_count); for two nodes and prediction_capacity=8, each ledger has 16 slots."
  authorized_scope:
    - "Independently reconstruct both authorized Luna-35 fixtures."
    - "Audit production lifecycle and historical delayed-credit intent."
    - "Run focused and full regression suites."
    - "Make one bounded next-governance decision."
  unauthorized_scope:
    - "Change production semantics or capacity."
    - "Rerun Luna-34 propagation conditions or ACP-0007 efficacy."
    - "Change reward, eligibility, predictor-expiry, architecture, or pruning semantics."
    - "Authorize Luna-37."
  controls:
    - "Luna-35 no-edge capacity reproducer: seed 0, sequence index 4, c00-004, 20 input points."
    - "Luna-35 one-point no-edge lifecycle/reset control."
    - "Existing reward idempotency tests and an isolated production delayed-credit probe after predictor expiry."
  measurements:
    - "Per-entry creation and predictor identity, predictor expiration, ledger occupancy, lifecycle signal, removal, and final status."
    - "Exact source/destination occupancy accounting and peak occupancy."
    - "Deterministic replay digest for both fixed fixtures."
  information_boundary_check:
    - "No labels enter neural computation."
    - "Review used no task outcome as evidence for eligibility behavior."
  hardware_mapping:
    - "Not applicable; software-reference lifecycle review only."
  architecture_invariants_touched:
    - "A09/A11: bounded local resource accounting and delayed credit."
    - "No architecture invariant or contract was changed."
  preserves:
    - "A later reward can use a retained trace after predictor expiry."
    - "Existing exact finite-capacity rejection behavior."
    - "Per-character cleanup and empty ledgers for the next character."
    - "Luna-33 verdict and historical Luna-34 BLOCKED / UNDETERMINED status."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-36.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-independent-review-luna35-eligibility-capacity-20261004.md"
  tests_added: []
  tests_passing:
    - "77 focused tests passed."
    - "932 full-suite tests passed."
  tests_failed: []
  tests_not_run:
    - "CUDA visualization execution was skipped because CUDA is unavailable."
    - "No Luna-34 condition or efficacy experiment was run."
  assumptions:
    - "The published revision b0507cb68776011dba482907b0ac763bec2a225f is the Luna-35 ending revision under review."
  unresolved:
    - "No documented workload-to-eligibility-capacity contract states that the existing derived default accommodates every per-character workload."
    - "No propagation-to-emission conclusion is established by this review."
  recommended_next_agent:
    - "Luna-36, limited to backward-compatible per-ledger eligibility capacity configuration."
---

# Luna-0 independent post-Luna-35 review

## Outcome and reviewed scope

**PASS — LUNA-35 EVIDENCE INDEPENDENTLY RECONSTRUCTED.** Review began after
fetching `origin/main` at
`b0507cb68776011dba482907b0ac763bec2a225f`. At the start,
`HEAD == origin/main`, branch was `main`, and the worktree was clean. The
published Luna-35 contract, handoff, runner, tests, result artifact, Luna-34
contract and handoff, prior Luna-0 review, workflow, changelog, ACP-0007,
architecture contract, historical Luna-8 delayed-credit material, and
relevant production code were reviewed.

Luna-35 contract compliance: **PASS**. It used exactly the two authorized
no-edge fixtures. It did not change production semantics, raise capacity,
alter `prediction_capacity`, rerun Luna-34 edge conditions, test efficacy,
change reward or predictor-expiration semantics, change eligibility
semantics, modify architecture, or authorize a later Luna. All conclusions
below were reconstructed from the published Luna-35 result and production
code rather than accepted solely from its classification.

## Fixture 1 — fixed capacity reproducer

The fixture is seed `0`, `NO_EDGE_CONTROL`, sequence index `4`, ID `c00-004`,
20 input points, two nodes, and per-ledger capacity 16. It creates the
following ordered source traces. Each trace links by identity to the
predictor shown; the predictor expiration event records its expiration
timestamp and a snapshot showing the eligibility entry still resident:

| Creation sequence | Eligibility trace | Linked predictor |
|---:|---|---|
| 1 | `luna35:c00-004:source:excursion:1` | `luna35:c00-004:predictor:prediction:0` |
| 2 | `luna35:c00-004:source:excursion:2` | `luna35:c00-004:predictor:prediction:1` |
| 3 | `luna35:c00-004:source:excursion:3` | `luna35:c00-004:predictor:prediction:2` |
| 4 | `luna35:c00-004:source:excursion:4` | `luna35:c00-004:predictor:prediction:3` |
| 5 | `luna35:c00-004:source:excursion:5` | `luna35:c00-004:predictor:prediction:4` |
| 6 | `luna35:c00-004:source:excursion:6` | `luna35:c00-004:predictor:prediction:5` |
| 7 | `luna35:c00-004:source:excursion:7` | `luna35:c00-004:predictor:prediction:6` |
| 8 | `luna35:c00-004:source:excursion:8` | `luna35:c00-004:predictor:prediction:7` |
| 9 | `luna35:c00-004:source:excursion:9` | `luna35:c00-004:predictor:prediction:8` |
| 10 | `luna35:c00-004:source:excursion:10` | `luna35:c00-004:predictor:prediction:9` |
| 11 | `luna35:c00-004:source:excursion:11` | `luna35:c00-004:predictor:prediction:10` |
| 12 | `luna35:c00-004:source:excursion:12` | `luna35:c00-004:predictor:prediction:11` |
| 13 | `luna35:c00-004:source:excursion:13` | `luna35:c00-004:predictor:prediction:12` |
| 14 | `luna35:c00-004:source:excursion:14` | `luna35:c00-004:predictor:prediction:13` |
| 15 | `luna35:c00-004:source:excursion:15` | `luna35:c00-004:predictor:prediction:14` |
| 16 | `luna35:c00-004:source:excursion:16` | `luna35:c00-004:predictor:prediction:15` |

For each of these 16 records, the saved `predictor_expirations` observation
contains its `expires_at`, actual `expired_at`, matching eligibility
identity, and an `eligibility_after_predictor_expiration` snapshot with
status `resident`. The linked trace remains in the source ledger after
expiration. No prediction-error or reward signal reached the ledger before
the failure. The fixed artifact contains each exact per-record timestamp and
state.

Independent occupancy reconstruction:

```text
initial 0 + successful creations 16 - removals 0 = final 16
```

Peak occupancy is exactly 16/16. The first rejected operation attempts
creation 17, `source:excursion:17`, linked to
`luna35:c00-004:predictor:prediction:16`, at
`255.79833294576443`. Its attempted magnitude is
`0.5406345932947867`; source occupancy is 16 immediately before rejection.
The failure is raised while `admit_external_batch` drains pending events,
before input point index 19 is admitted; it is not evidence that the
nineteenth point itself produced the emission. The character never reaches
its end/reset boundary.

The runtime formula is `prediction_capacity * max(1, neuron_count)`.
With two nodes and `prediction_capacity=8`, this yields 16 slots per
ledger (32 allocated slots in total). Predictor expiry frees predictor
records but does not remove linked eligibility records.

## Fixture 2 — lifecycle and character-reset control

The one-point no-edge fixture creates
`luna35:luna35-lifecycle-0:source:excursion:1` at timestamp `0.5`, linked to
`luna35:luna35-lifecycle-0:predictor:prediction:0`. The ordinary
end-character path delivers one neutral reward to the source eligibility
ledger at timestamp `4.0`, message ID
`neutral-luna35-lifecycle-0`, explicitly matching that trace ID.

| Transition | Occupancy | Trace state |
|---|---:|---|
| Before reward | 1 | Value `0.4227634632752029`, credit `0.0` |
| After matched neutral reward | 1 | Value `0.176234031147182`, credit `0.0` |
| Immediately before character destruction | 1 | Trace still resident |
| Immediately after destruction | 0 runtime-held references | One trace reference released |
| Fresh next-character ledgers | 0 | New ledger IDs; no entries |

The signal is recognized as `matched`; it is not a retirement operation.
No predictor expired in this one-point control (`expired_predictions=0`).
Thus this fixture establishes ordinary reward matching and character
cleanup, but does **not** alone establish reward after predictor expiration.
The saved accounting is:

```text
initial 0 + successful creations 1 - ledger-expiry removals 0
  - character-boundary releases 1 = post-boundary occupancy 0
```

Deterministic replay reproduces the exact two fixtures. The first and replay
observation digests are both
`45485ddfafac2878e267a8e5dcc4ab76c3c335f279802ac98b0d5c44758920cb`.

## Production lifecycle and delayed-credit audit

**OBSERVED:** predictor expiration and eligibility retirement are separate
operations in production. Expiration removes predictor records. Eligibility
is created on canonical emission and remains in its bounded ledger unless
an eligibility expiry is configured and processed by a later ledger
operation, or the ledger/runtime is released at character destruction.
The integrated runtime leaves eligibility expiry unset. `apply_signal()`
decays/updates matching credit but does not remove the trace. Reward and
prediction-error delivery are not general-purpose trace retirement events.

**ESTABLISHED INTENDED BEHAVIOR:** historical Luna-8 and A11 require
causally delayed credit. An eligibility record retains the prediction
identity needed to match a later reward. The production ledger probe
independently confirmed that a trace remains addressable after its predictor
expired at time 2 and a matching reward at time 3 can still be applied by
prediction ID, with occupancy remaining one. Automatically deleting the
eligibility trace on predictor expiry would destroy that already supported
delayed-reward path. The probe was a bounded in-memory runtime check, not a
third Luna-35 fixture or a persisted experiment artifact.

There is no established invariant requiring predictor expiry to retire
eligibility. Nor is there a documented universal workload/capacity guarantee
or integrated automatic cleanup deadline for a long-lived character with no
matching credit signal. Entries are finite, hard-bounded per ledger, and
character-scoped; they are therefore not an unbounded cross-character
memory leak. They can nevertheless consume capacity until the character
ends, and a workload can reach the deterministic capacity rejection.

Duplicate delivery does not change the matched result for the same reward
message identity under the existing idempotency behavior. Fixture 2 itself
delivers one reward only; duplicate behavior was checked separately against
the established production implementation/tests and was not presented as a
fixture measurement.

## Capacity-contract conclusion

**EXPECTED BOUNDED BEHAVIOR** describes the 17th-create rejection: the
existing finite bound rejects new unique traces instead of evicting existing
traces. The fixture does not establish a defect merely because its workload
fills that bound.

**CONTRACT AMBIGUITY / PUBLIC API LIMITATION** describes the capacity
configuration: the runtime derives eligibility capacity from
`prediction_capacity` and neuron count, provides no independent
per-eligibility-ledger setting, and no documented workload-to-capacity
contract guarantees that the derived value is sufficient for all
per-character workloads.

No caller/fixture lifecycle violation or **PRODUCTION LIFECYCLE DEFECT** is
established. Removing eligibility at predictor expiry is not a compatible
repair because a delayed reward can still need the retained trace. A
backward-compatible finite capacity setting is the narrow next step; it
changes no retirement or credit semantics and makes no claim that any chosen
capacity is universally sufficient.

## Implication for Luna-34 and scientific limits

Luna-35 clarifies the original reproducible Luna-34 blocker but does not make
the authorized Luna-34 diagnostic valid to execute unchanged: its
fixed-capacity stream still deterministically fills the source ledger before
the character boundary. The review does **not** rewrite or reopen Luna-34.
Luna-34 remains historically **BLOCKED / UNDETERMINED**.

No authorized edge condition, propagation-to-emission result, multi-emitter
behavior, candidate formation, temporal specificity, structural-growth
benefit, task efficacy, accuracy improvement, or architecture requirement
is established. Luna-33 remains **NOT SUPPORTED IN THIS SETUP**. ACP-0007
and architecture are unchanged.

## Validation

Validation was run against the reviewed published revision before governance
edits:

| Command or procedure | Revision / environment / seed | Result | Evidence |
|---|---|---|---|
| Focused Luna-35, eligibility, excursion integration, and predictive-coding tests | `b0507cb68776011dba482907b0ac763bec2a225f`; Python 3.11.5 | 77 passed | Test runner output |
| Full repository test suite | Same revision; Windows 10; Python 3.11.5 | 932 passed, 1 skipped, 933 collected | `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics` skipped because CUDA is unavailable |
| Deterministic replay | Luna-35 saved runner, seed 0; exactly two fixed fixtures | Pass; digests match | `artifacts/luna35-eligibility-capacity-lifecycle/results.json` |
| Python compilation | Reviewed baseline | Pass | Compilation command completed |
| `git diff --check` | Governance changes | Run before commit | Review publication check |

The baseline comparison is 929 passed, one skipped, 930 collected before
Luna-35, versus 932 passed, one skipped, 933 collected now. Exactly three
Luna-35 tests account for the collection increase. No test failure or
regression was found.

## Files and governance

Evidence reviewed:

- `.github/agents/luna-35.agent.md`
- `workflow/handoffs/luna-35-eligibility-capacity-lifecycle-20261004.md`
- `artifacts/luna35-eligibility-capacity-lifecycle/results.json`
- `run_luna35_eligibility_capacity_lifecycle.py`
- `tests/test_luna35_eligibility_capacity_lifecycle.py`
- Production eligibility, predictor, reward, and EXCURSION runtime code
- Historical Luna-8 delayed-credit contract and prior Luna-0/Luna-34 review

Governance files updated:

- `.github/agents/luna-36.agent.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- This independent review handoff

No production code, Luna-35 evidence, Luna-34 conclusion, Luna-33 verdict,
ACP-0007, or architecture contract was modified.

## Next assignment

**Luna-36 — AUTHORIZED / NOT EXECUTED.** Add only an optional positive,
finite per-ledger `eligibility_capacity` setting to the EXCURSION runtime
and its quiescent-IR2 construction path. When omitted, preserve the exact
existing formula. Test compatibility and unchanged lifecycle behavior.
Do not change predictor expiry, eligibility retirement, reward behavior,
event ordering, experiments, or architecture. Full contract:
`.github/agents/luna-36.agent.md`.

No Luna-37 is authorized. Return to Luna-0 after Luna-36 for independent
review. Any subsequent bounded propagation-to-emission diagnostic requires
a separate Luna contract and remains unexecuted and unauthorized here.
