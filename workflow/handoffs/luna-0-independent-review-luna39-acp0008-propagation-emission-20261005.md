# Luna-0 Independent Post-Luna-39 Review — ACP-0008 Propagation-to-Emission Diagnostic

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-Luna-39 scientific and governance review"
  task_id: "luna-0-independent-review-luna39-acp0008-propagation-emission-20261005"
  component: "EXCURSION_V1 ACP-0008 propagation-to-emission mechanism"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "a185c6321b06f58df2bd7b22c56b1d23cb7d67e5"
  result_revision: "commit containing this handoff"
  dependencies: ["Luna-39"]
  owner: "Project owner"
  classification: ["PASS WITH FOLLOW-UP", "SUPPORTED under N2 sensitivity only"]
  hypothesis: "Destination-only ACP-0008 integration changes the Luna-37 no-emission result under at least one predeclared edge condition."
  counter_hypothesis: "The historical arm fails reproduction, or the integrated destination produces no canonical emission."
  interfaces_relied_on: ["MultiExcursionNeuron", "IntegrationConfig", "ExcursionCharacterRuntime", "BoundedTopology"]
  label_information_boundary: ["Inputs reconstructed from points only; input digests and per-character records match across arms."]
  timing_assumptions: ["Local event timestamps; slow-state decay is elapsed-time exponential."]
  reset_boundaries: ["Fresh neurons and character-scoped ledgers per character."]
  resource_bounds: ["1920 executions; eligibility_capacity 1024 per ledger; peak occupancy 19; fixed queue/event bounds from Luna-39."]
  authorized_scope: ["Independent evidence reconstruction", "post-Luna-39 handoff", "workflow and changelog update"]
  unauthorized_scope: ["Production changes", "ACP-0008 promotion", "Luna-40 execution"]
  controls: ["Luna-37-matched legacy arm", "no-edge control", "default static edge w=1"]
  measurements: ["Canonical emissions", "integration traces", "stream invariance", "capacity accounting", "replay digest"]
  information_boundary_check: ["Passed; no label/class information observed in inputs or retained records."]
  hardware_mapping: ["Not applicable; CPU software-reference diagnostic only."]
  architecture_invariants_touched: ["Reviewed A01, A02, A03, A08, A15 evidence through ACP-0008; no contract change."]
  preserves: ["Luna-37 historical verdict", "Luna-34 BLOCKED / UNDETERMINED", "Luna-33 and ACP-0007 unchanged"]
  architecture_change: false
  proposal: null
  files_changed: ["workflow/handoffs/luna-0-independent-review-luna39-acp0008-propagation-emission-20261005.md", "workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/ARCHITECTURE_CHANGELOG.md"]
  tests_added: []
  tests_passing: ["227 focused", "998 full-suite"]
  tests_failed: []
  tests_not_run: []
  assumptions: ["Committed Luna-39 evidence is complete and comes from the verified revision."]
  unresolved: ["Whether to pursue a separately specified investigation of naturally generated/learned routed strength; ACP-0008 promotion remains a project-owner decision."]
  recommended_next_agent: ["Project owner decision; no Luna-40 authorized."]
```

## Outcome and reviewed state

Reviewed Luna-39 revision `a185c6321b06f58df2bd7b22c56b1d23cb7d67e5`.
Fetched `origin/main` and verified at review start:

- `HEAD == origin/main == a185c6321b06f58df2bd7b22c56b1d23cb7d67e5`
- branch `main`
- clean worktree.

**Review verdict: PASS WITH FOLLOW-UP. Scientific result: SUPPORTED only under
`STATIC_N2_BOUND_SENSITIVITY` (`w=2`).** ACP-0008 integration plus the
N2-strength routed input can bridge propagation to canonical emission in this
bounded setup, while the default static edge remains insufficient. No
production defect is identified. Luna-37 remains historically **NOT SUPPORTED
IN THIS SETUP** under the previous architecture.

## Scope and contract compliance

The Luna-39 commit adds exactly its six authorized files: runner, focused tests,
config, results, summary, and execution handoff. There are no production,
architecture-proposal, ACP, or governance changes in that commit. Inspection of
the committed configuration and runner confirmed:

- two arms and exactly three predeclared conditions per arm;
- seeds 0–4, 64 characters per seed, 1,920 total arm-condition-character
  executions;
- the Luna-37 task-derived streams and bounds, with no label/class inputs;
- `eligibility_capacity=1024` passed explicitly, without retry or substitution;
- source neuron configuration is identical between arms; only the destination
  receives opt-in `IntegrationConfig()`;
- `theta_E=1.0` and ACP-0008 parameters are fixed at their predeclared defaults;
- no parameter sweep, task-efficacy endpoint, structural growth, pruning, or
  ACP change; no ACP-0008 promotion claim and no Luna-40 authorization.

## Historical-equivalence gate and upstream invariance

Independently paired all 960 integration-disabled character records with Luna-37
and compared input digests, source input events, all canonical emissions,
routed contributions, and maximum route depth. Every record matched exactly.
The legacy arm therefore passes the committed historical-equivalence gate:

| Condition | Source emissions | Transfers | Destination receptions | Destination canonical emissions |
|---|---:|---:|---:|---:|
| NO_EDGE_CONTROL | 1715 | 0 | 0 | 0 |
| DEFAULT_STATIC_EDGE (`w=1`) | 1715 | 1715 | 1715 | 0 |
| STATIC_N2_BOUND_SENSITIVITY (`w=2`) | 1715 | 1715 | 1715 | 0 |

Compared the two Luna-39 arms for every seed, condition, and character.
Source input digests/events and source canonical emissions (identities, times,
payloads) match. All upstream routed schedules also match on transfer identity,
source, destination, emission and arrival timestamps, transformed payload,
sign/magnitude, delay, route path and depth. No schedule mismatches were found.
The runtime-global `receive_sequence` differs on 171 paired routed records
because destination-local integration emissions consume queue sequence
numbers. Destination post-transfer state differs as expected; neither field is
part of the upstream causal stream comparison.

## Independent aggregate reconstruction

The following totals were independently recomputed from the lowest-level
character records and compared with `summary.json`; all summary comparisons
matched. “Integrated/direct” count destination canonical emissions classified
from the event trace, not receptions or nonzero state. Occupancy columns are
the maximum ledger peak and maximum ledger final occupancy over each cell.

| Arm | Condition | Chars | Source-emitting chars | Receiving chars | Destination-emitting chars | Integrated-emitting chars | Direct-emitting chars | Source emissions | Transfers / receptions | Destination emissions (integrated / direct) | Max `|z|` | Max `|x|` | Max depth | Peak / final occupancy | Runtime events |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Legacy | No edge | 320 | 297 | 0 | 0 | 0 | 0 | 1715 | 0 / 0 | 0 (0 / 0) | 0 | 0 | 0 | 19 / 19 | 9394 |
| Legacy | Default `w=1` | 320 | 297 | 297 | 0 | 0 | 0 | 1715 | 1715 / 1715 | 0 (0 / 0) | 0 | 0.685455 | 1 | 19 / 19 | 11109 |
| Legacy | N2 `w=2` | 320 | 297 | 297 | 0 | 0 | 0 | 1715 | 1715 / 1715 | 0 (0 / 0) | 0 | 0.932688 | 1 | 19 / 19 | 11109 |
| ACP-0008 | No edge | 320 | 297 | 0 | 0 | 0 | 0 | 1715 | 0 / 0 | 0 (0 / 0) | 0 | 0 | 0 | 19 / 19 | 9394 |
| ACP-0008 | Default `w=1` | 320 | 297 | 297 | 0 | 0 | 0 | 1715 | 1715 / 1715 | 0 (0 / 0) | 0.763164 | 0.685455 | 1 | 19 / 19 | 11109 |
| ACP-0008 | N2 `w=2` | 320 | 297 | 297 | 27 | 27 | 0 | 1715 | 1715 / 1715 | 31 (31 / 0) | 1.118173 | 1.913373 | 1 | 19 / 19 | 11186 |

The integration-enabled N2 arm has 27 characters with both source and
destination emitters, 270 source-only characters, and 23 characters with no
emitter. Its 31 destination emissions include four additional emissions after
the first emission in an emitting character.

## Capacity and negative-control audit

The committed per-character records contain 3,840 ledger records (two ledgers
for each of 1,920 executions). All have effective configured capacity 1024;
all satisfy `initial + created - removed = final`; no errors, eviction,
automatic growth, or retry occurred. Maximum peak and final occupancy are both
19, strictly below capacity. Total eligibility creations are 1715 in each
legacy condition, 1715 for integrated no-edge and default-edge, and 1746 for
integrated N2 (1715 source plus 31 destination emission traces); removals are
zero.

Both no-edge arms have no source-to-destination edge, transfer, reception,
integration trace, slow-state accumulation, or destination canonical emission.
They are valid negative controls. The destination state remains neutral
(`x=0`, `z=0`).

## ACP-0008 transition and emission audit

Read the production `_advance_to` and integration-enabled neuron path against
ACP-0008, then independently recomputed all 3,430 retained integration trace
entries. The event-local slow decay, input addition, and discharge equations
agree with the stored trace to floating-point roundoff:

- maximum `z`-decay formula discrepancy: `5.56e-17`;
- maximum input/integration formula discrepancy: `1.12e-16`;
- maximum discharge and post-discharge state discrepancy: `0`;
- invalid trace transitions: `0`.

The default-edge integration arm accumulates slow state (`1715` updates) but
never reaches `theta_Z=1`; maximum `|z|=0.763164`, and there are no discharges
or destination emissions. N2 also has 1715 integration updates; maximum
`|z|=1.118173`, with 31 discharges and 31 canonical emissions across 27
characters. All 31 emissions map to production destination emission identities
and timestamps and are independently classified as `integrated_discharge`.
There are zero direct destination emissions in every arm and condition.

For every claimed integrated emission, the retained history has at least two
contributing receptions, nonzero slow state before the final contributing
input, threshold-reaching post-input state, a discharge, and an ordinary
canonical emission 0.5 time units later. The contribution history spans 2–17
receptions; consecutive contributing arrivals are 12.927767–79.889902 time
units apart, with retained slow fractions from 0.000339 to 0.274507.

Representative N2 trace (`seed=0`, `c00-001`):

1. At `t=1.5`, input `-0.872284336961` yields `z=-0.872284336961`.
2. At `t=20.496044330790`, after `18.996044330790` time units, decay retains
   fraction `0.149627795324`; the two contributing routed events span an
   accumulation interval of `18.996044330790`, and `z` immediately before the
   final input is `-0.130517982235`.
3. The final routed input contributes `-0.913372503744`, yielding
   `z=-1.043890485979`; the production discharge is `-1.0` at that event.
   The final input alone is below `theta_Z`; the retained prior state is
   required to reach the discharge boundary.
4. The mapped canonical destination emission occurs at `t=20.996044330790`,
   exactly the configured ordinary emission delay later.

This establishes that the N2 result uses retained prior routed evidence; it is
not merely a reception, a state update, a stored `integrated` flag, or a
single-input threshold crossing.

## Replay and independent rerun

The committed full-run replay digest is identical across runs:
`5a19be65e2386e585eb50877c80f3114ee7383fda7b2a8324642440618b963d6`.
Independently reran the complete 1,920-execution experiment and its full replay
from the reviewed revision into a temporary directory. The rerun completed,
passed historical reproduction, again produced 31 N2 and zero default-edge
destination emissions, and reproduced the same initial/replay digest. The
temporary output was removed after verification.

## Scientific interpretation and governance

The bounded mechanistic result is **SUPPORTED only under the predeclared N2
strength sensitivity**. With the default static edge (`w=1`), ACP-0008
integration accumulates but does not produce a canonical destination emission.
With the fixed N2 edge (`w=2`), slow-state retention and discharge produce 31
canonical emissions on 27/320 characters. Luna-37 remains historically
**NOT SUPPORTED IN THIS SETUP** under its non-integrating destination; this is
a new ACP-0008 result, not a revision of Luna-37.

This strengthens the evidence that ACP-0008 can bridge propagation to emission
under the bounded tested condition. It does not establish task efficacy,
ACP-0007 candidate formation, beneficial growth, pruning benefit, accuracy,
prediction or resource benefit, temporal specificity, generality, calibrated
parameters, hardware equivalence, or an optimal weight. ACP-0008 remains
**ACCEPTED — EXPERIMENTAL, OPT-IN**. No architecture contract promotion is
made. Luna-34 remains **BLOCKED / UNDETERMINED**; Luna-33 and ACP-0007 are
unchanged.

Because emissions occurred only at the deliberately predeclared N2 sensitivity
and not at the default edge, a possible subsequent question is whether
naturally generated or learned routed strengths can create this accumulation
without hand-selecting a stronger static edge. The present evidence does not
define that learning mechanism or a sufficiently bounded experiment contract.
That is a project-owner decision boundary; **no Luna-40 was created or
authorized**. No parameter tuning is recommended by this review.

Known ACP-0008 follow-ups remain outside this review: integration-enabled IR-2
and TPCV-2 export, package-root `IntegrationConfig` export, Luna-38 Fixture I's
direct private `_z` setup, and parameter calibration. None invalidated Luna-39.

## Validation

| Command / procedure | Result |
|---|---|
| Independent aggregate, trace-equation, capacity, and stream reconstruction | All six cell summaries match; 0 bad trace transitions; 0 capacity reconciliation errors; 0 source/schedule mismatches |
| Independent full Luna-39 experiment rerun | 1920 executions; legacy gate passed; result and replay digests equal committed digest |
| Focused Luna-39/Luna-38/Luna-37/Luna-36/neuron/runtime/eligibility/predictive-coding tests | 227 passed |
| Full suite | 998 passed, 1 skipped; 999 collected |
| Skip | `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`; CUDA unavailable |
| Test-count change | Exactly +8 Luna-39 tests over 990 passed, 1 skipped, 991 collected |
| `git diff --check` | Clean after the governance changes |

No production source or test changes were made by this review. Next action:
project-owner decision on whether any follow-up is warranted; no Luna-40 is
authorized.
