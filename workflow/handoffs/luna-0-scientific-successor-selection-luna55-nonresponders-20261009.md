# Luna-0 Scientific Successor Selection — Luna-55 Nonresponders

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-55 nonresponder comparison and Luna-58 authorization"
  task_id: "luna-0-scientific-successor-selection-luna55-nonresponders-20261009"
  component: "Read-only retained-evidence analysis and bounded experiment authorization"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "c6adc71c26f6226bcbbfb442c4c22cb11cdb3cd2"
  result_revision: "Luna-58 contract publication; no scientific execution"
  dependencies:
    - "Luna-55 accepted execution and frozen selection"
    - "Luna-57 provenance correction and clean repository gate"
  owner: "Luna-0"
  classification:
    - "read-only scientific successor selection"
    - "finite destination-retention mechanism authorization"
    - "AUTHORIZED / NOT EXECUTED"
  hypothesis: "One fixed finite destination decay rate of 0.00001 crosses all six Luna-55 RR nonresponders under actual E2 while preserving control selectivity."
  counter_hypothesis: "Any of the six fails, a negative control crosses, the route changes, or deterministic/provenance/bounds checks fail."
  interfaces_relied_on:
    - "Luna-1 event ordering and local elapsed-time semantics"
    - "Luna-19/E2 destination integration and threshold discharge"
    - "Luna-45 source events, Luna-46 oracle, Luna-53/54 retained arms, Luna-55 RR route"
  label_information_boundary:
    - "Labels and evaluation strata are offline-only; no labels are read by neural runtime."
    - "Target membership is fixed from authenticated Luna-55 selection."
  timing_assumptions:
    - "Retained timestamps are local event timestamps; elapsed intervals drive z decay."
    - "No global neural timestep is introduced."
  reset_boundaries:
    - "Luna-55 RR nonresponders had no destination discharge/reset/refractory transition before or after their three receptions."
    - "The threshold-solving recurrence is valid through the final reception because all inputs are same-sign and prior prefixes remain below threshold."
  resource_bounds:
    - "Future phases retain 320 streams, queue 128, runtime budget 1024, per-neuron budget 4096, settling horizon 4.0."
    - "Current Luna-55 retained phases report 1715 source inputs and 421 destination routes."
  authorized_scope:
    - "Read-only comparison of all 16 frozen Luna-55 target streams."
    - "One predeclared finite destination-rate intervention at 0.00001."
    - "Contract/workflow/changelog publication only in this selection pass."
  unauthorized_scope:
    - "No neural experiment, runner, replay, sweep, artifact generation, task efficacy, or architecture change in this pass."
    - "No further parameter selection or Luna-59 authorization."
  controls:
    - "Ten Luna-55 RR responders as positive controls."
    - "E+49, E0 10, NR1 189, and NR0 23 as separate negative/control populations."
    - "33-stream secondary temporal-retention stratum reported separately."
  measurements:
    - "Per-stream source count, RR relay output count and peak, destination arrival count/timestamp/payload, zero-decay oracle peak, RR peak, headroom/deficit, decay loss, and destination discharge."
    - "Finite-rate critical boundary solved offline from retained event sequences; no experiment run."
  information_boundary_check:
    - "Offline-only target/control selection; labels do not enter neural computation."
  hardware_mapping:
    - "Not applicable; software-reference evidence only."
  architecture_invariants_touched:
    - "A01/A02/A04/A06 preserved; no core behavior changed."
  preserves:
    - "All historical Luna-45/46/53/54/55 artifacts, pins, outcomes, and ACP-0008 status."
    - "Luna-55 PARTIALLY SUPPORTED conclusion within its frozen setup."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-58.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-scientific-successor-selection-luna55-nonresponders-20261009.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "No neural runner, replay, or artifact-generation command was run."
    - "No unit/full test suite was run; this publication is documentation and experiment authorization only."
  assumptions:
    - "Published Luna-55 evidence at the pinned Git objects is authoritative."
    - "The next implementation must authenticate the listed objects and rerun actual E2; offline recurrence is a prediction, not execution evidence."
  unresolved:
    - "Whether the single predeclared finite rate rescues all six under actual E2."
    - "No separate standalone Luna-55 review handoff was located; the workflow changelog records that independent review completed."
  recommended_next_agent:
    - "Luna-58 — implement and execute only the published finite destination-retention contract; then stop for independent Luna-0 review."
```

## Outcome and decision

**OBSERVED:** At clean baseline
`c6adc71c26f6226bcbbfb442c4c22cb11cdb3cd2`, Luna-55 remains
**PARTIALLY SUPPORTED**: HH/RH/HR crossed 0/16 and RR crossed 10/16. This
review compared the exact 16 frozen targets against retained Luna-55 RR,
Luna-54 HH/RH, Luna-53 HR, and the Luna-55 signed zero-decay selection.
No scientific runner or replay was run.

**DECISION: Luna-58 finite destination-retention rescue AUTHORIZED / NOT
EXECUTED.** The six streams do not show greater absolute decay loss than
responders; their distinguishing feature is near-zero headroom under a
same-sign, decay-free E2 accumulation. The retained RR finite-decay loss
exceeds that available headroom in each of the six. Their actual RR routing
matches RH exactly, and their E2 destination traces show no prior discharge,
reset, refractory mode, or clipping. This supports one causal, one-parameter
test rather than another zero-decay oracle diagnostic or an unbounded sweep.

## Retained evidence and identities

The selection and RR phase identities at the authorization baseline are
listed in the [Luna-58 contract](../../../.github/agents/luna-58.agent.md).
The Luna-55 configuration digest is
`d99b31646791f37e9242dfb9089e299dc6ab31e21bc0f96b244e92a6f4bed708`;
its source-input phase digest is
`d73c99d83847b50bb5cb66920b95c3546d818874f582b6b6d9d8c5bfa90aaa3b`.
The authenticated Luna-54 intervention initial/replay inputs share scientific
digest
`4170a2688438a2f86a7b9c907d86efff006309ecdc5bf57e14011d6a5033ed54`.
selection SHA-256 is
`2ac7b79015c00d5055b1b6226ce23239f691ba07a368e80768737e39f0b2bd57`.
The retained RR initial and replay phase digests are respectively
`402494efd10b62d22b2e0b5a5d6dce878c4c20460f41cdec2c64b9a6c571e576` and
`360c85b9ef511cc6c442df8b70be6646d2418bd6d7159954d9c6409378cc49b8`.
The RR result records use execution source
`ca378b216e962de2a81b0d3ada741867fa4b1fce` with a dirty worktree; that
historical execution identity is not represented as a clean runner checkout.

The four arrival counts below are destination arrivals in HH/RH/HR/RR order.
For each RR stream, `t:p` entries are destination timestamp and signed payload;
display values are rounded, and the retained JSON is authoritative. RR route
signatures (event ID, payload bits, timestamp, source, destination) match RH
for all 16 targets. `zero margin` is decay-free peak minus threshold 1;
`RR margin` is threshold 1 minus the RR peak. Positive RR margin means
noncrossing. Relay peak is maximum absolute `z_after_input` on the RR relay.

| Stream | RR | Source inputs / RR relay emissions | Dest. arrivals HH/RH/HR/RR | RR destination `t:payload` | Gaps | Zero peak / headroom | RR peak / margin | Decay loss | RR relay peak | RR destination discharges |
|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| c00-011 | N | 9 / 3 | 2/3/2/3 | 66.165986:+0.330003344, 171.505287:+0.334584585, 213.591223:+0.336656685 | 105.339, 42.086 | 1.001244615 / 0.001244615 | 0.928558926 / 0.071441074 | 0.072685689 | 1.230539 | 0 |
| c00-032 | R | 11 / 4 | 2/4/2/4 | 47.001667:-0.338234139, 112.976599:-0.315793765, 178.962072:-0.359204730, 222.949264:-0.343099242 | 65.975, 65.985, 43.987 | 1.356331877 / 0.356331877 | 1.229778182 / -0.229778182 | 0.126553695 | 1.304236 | 1 |
| c00-037 | N | 10 / 3 | 2/3/2/3 | 74.129734:-0.334311647, 168.966881:-0.306230859, 216.387231:-0.361662935 | 94.837, 47.420 | 1.002205442 / 0.002205442 | 0.930118780 / 0.069881220 | 0.072086661 | 1.308261 | 0 |
| c01-012 | R | 13 / 4 | 2/4/2/4 | 56.283517:+0.312236417, 96.289891:+0.321887214, 202.814820:+0.341989876, 242.807161:+0.328420263 | 40.006, 106.525, 39.992 | 1.304533770 / 0.304533770 | 1.169053310 / -0.169053310 | 0.135480460 | 1.299842 | 1 |
| c01-020 | N | 10 / 3 | 2/3/2/3 | 104.277808:-0.360306004, 205.588871:-0.327118801, 281.623657:-0.322018583 | 101.311, 76.035 | 1.009443389 / 0.009443389 | 0.908144939 / 0.091855061 | 0.101298450 | 1.236468 | 0 |
| c01-041 | R | 13 / 4 | 2/4/2/4 | 102.223232:-0.346739036, 135.264860:-0.345088289, 234.431737:-0.319898974, 284.072901:-0.323174387 | 33.042, 99.167, 49.641 | 1.334900687 / 0.334900687 | 1.186578624 / -0.186578624 | 0.148322063 | 1.211648 | 1 |
| c01-050 | R | 12 / 4 | 3/4/3/4 | 50.208868:-0.326797653, 160.373835:-0.313723743, 191.822645:-0.360719468, 239.030077:-0.305774721 | 110.165, 31.449, 47.207 | 1.307015585 / 0.307015585 | 1.188262071 / -0.188262071 | 0.118753514 | 1.246771 | 1 |
| c02-010 | R | 13 / 4 | 2/4/2/4 | 55.565870:-0.306980522, 143.181769:-0.343023701, 248.318053:-0.329896751, 283.365428:-0.365227676 | 87.616, 105.136, 35.047 | 1.345128650 / 0.345128650 | 1.199783044 / -0.199783044 | 0.145345607 | 1.158867 | 1 |
| c02-015 | N | 9 / 3 | 2/3/2/3 | 94.029662:+0.361077707, 203.302038:+0.327359985, 257.980581:+0.313578584 | 109.272, 54.679 | 1.002016276 / 0.002016276 | 0.913480642 / 0.086519358 | 0.088535634 | 1.234525 | 0 |
| c02-019 | R | 13 / 4 | 3/4/3/4 | 71.966775:-0.349076119, 168.583166:-0.312208467, 209.947220:-0.318592723, 265.151744:-0.311722277 | 96.616, 41.364, 55.205 | 1.291599585 / 0.291599585 | 1.159965593 / -0.159965593 | 0.131633992 | 1.235986 | 1 |
| c02-023 | N | 9 / 3 | 2/3/2/3 | 37.734978:+0.367433992, 159.466479:+0.337071329, 263.858830:+0.304983531 | 121.732, 104.392 | 1.009488852 / 0.009488852 | 0.877783571 / 0.122216429 | 0.131705281 | 1.360840 | 0 |
| c02-046 | N | 10 / 3 | 1/3/1/3 | 79.351371:+0.321528984, 181.141575:+0.337065153, 308.437077:+0.345770872 | 101.790, 127.296 | 1.004365009 / 0.004365009 | 0.874718355 / 0.125281645 | 0.129646655 | 1.183885 | 0 |
| c03-023 | R | 10 / 4 | 2/4/2/4 | 49.852157:-0.330344171, 96.698476:-0.354909312, 190.370835:-0.366845059, 237.241776:-0.326157919 | 46.846, 93.672, 46.871 | 1.378256462 / 0.378256462 | 1.231216174 / -0.231216174 | 0.147040289 | 1.175891 | 1 |
| c03-058 | R | 13 / 4 | 2/4/2/4 | 87.803861:-0.357674580, 189.736749:-0.317726739, 240.659928:-0.320410252, 308.531524:-0.312671200 | 101.933, 50.923, 67.872 | 1.308482771 / 0.308482771 | 1.152334071 / -0.152334071 | 0.156148700 | 1.235604 | 1 |
| c04-001 | R | 11 / 4 | 2/4/2/4 | 92.231691:+0.348852718, 181.507196:+0.345307687, 248.422933:+0.310874567, 315.330750:+0.325198683 | 89.276, 66.916, 66.908 | 1.330233655 / 0.330233655 | 1.167202781 / -0.167202781 | 0.163030874 | 1.413719 | 1 |
| c04-043 | R | 12 / 4 | 2/4/2/4 | 54.314460:-0.312734251, 139.877465:-0.350043103, 174.080665:-0.327223535, 276.751534:-0.380029832 | 85.563, 34.203, 102.671 | 1.370030721 / 0.370030721 | 1.199659343 / -0.199659343 | 0.170371378 | 1 |

All 16 retained RR destination traces are in mode N before each listed input.
The six nonresponders have three single-sign arrivals, no destination
discharge, and no prior reset/refractory transition. The nonresponders'
zero-decay critical rates (highest rate that reaches threshold on the retained
sequence) are:

The authenticated 320-stream RR record has seven relay-root-truncation flags,
all outside the 16 primary targets; all 16 target streams have complete source
and relay root expansion. The experiment contract therefore requires exact
baseline parity for those seven off-target flags and no new truncation, not an
incorrect blanket claim that the full population had none.

| Stream | Critical `decay_rate_z` | Predicted peak at `1e-5` | Predicted surplus |
|---|---:|---:|---:|
| c00-011 | 0.0000198645553135 | 1.000617682 | 0.000617682 |
| c00-037 | 0.0000356018277244 | 1.001585015 | 0.001585015 |
| c01-020 | 0.000107230422834 | 1.008556337 | 0.008556337 |
| c02-015 | 0.0000261994163776 | 1.001245824 | 0.001245824 |
| c02-023 | 0.0000808453897409 | 1.008307241 | 0.008307241 |
| c02-046 | 0.0000375821114584 | 1.003200480 | 0.003200480 |

The offline recurrence uses the runtime's event-time update
`z_i = z_(i-1) * exp(-lambda * (t_i - t_(i-1))) + p_i`, with `z_0=0`,
`input_gain=1`, `discharge_quantum=1`, and `z_max=4`. For each target, every
prefix before the final input remains strictly below threshold; the final
zero-decay sums shown above exceed threshold but remain far below `z_max`.
This closes the zero-decay-oracle-versus-actual-E2 question for these retained
same-sign sequences. The finite-rate prediction remains an offline
calculation, not evidence that the modified runtime crosses.

## Comparison and bounded successor rationale

**OBSERVED:** Nonresponders have zero-decay headroom only
`0.001245–0.009489`; responders have `0.291600–0.378256`. Nonresponders'
RR threshold deficit is `0.069881–0.125282`; responders' RR surplus is
`0.152334–0.231216`. The nonresponders' finite-decay peak loss is
`0.072087–0.131705`, which overlaps the responders' `0.118754–0.170371`.
RR-to-zero-decay peak ratios overlap (`0.869533–0.928072` nonresponders,
`0.875644–0.909141` responders); max-gap and duration ranges also overlap.
The primary structural difference in retained inputs is three RR arrivals
for each nonresponder versus four for each responder, giving much smaller
decay-free signed drive. Thus do not claim the nonresponders experienced
disproportionately greater absolute decay or a distinct timing regime.

**INFERRED:** With identical RR arrivals and no intervening destination state
transition, the missing threshold crossings are caused by finite destination
decay consuming more than the nonresponders' very small positive headroom.
The exact E2 update and the retained same-sign sequences establish that
zero-decay actual E2 would cross at the final event, so a separate
zero-decay-only runtime diagnostic is not necessary to resolve the oracle
mismatch.

**HYPOTHESIZED:** A single `decay_rate_z=0.00001` is low enough to cross all
six while keeping the 49 E+ controls below threshold. Offline use of the same
recurrence at this value predicts no crossing in E+49 (peak range
`0.624439–0.999331`), E0 10 (`0.306569–0.688705`), NR1 189 (maximum
`0.691157`), or NR0 23 (zero). The predicted minimum E+ threshold margin is
`0.000669121`; actual future runtime outcomes must replace these predictions.
The 33 secondary streams are not negative controls and remain separately
reported.

## Architecture evidence and boundaries

No A01-A15 clause, core runtime, architecture contract, or ACP changes. The
successor changes one already experimental, opt-in ACP-0008 destination
`decay_rate_z` value; it retains local elapsed-time decay and the full bounded
causal route. Labels remain evaluation-only. No task efficacy, production,
hardware, calibrated-energy, generalization, or architecture-promotion claim
is made.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Read-only extraction of retained Luna-53/54/55 JSON and recomputation of all 16 RR recurrences | Windows checkout; baseline `c6adc71c26f6226bcbbfb442c4c22cb11cdb3cd2` | PASS; 16 streams, route signatures RH/RR equal 16/16, all six same-sign prefixes below threshold until final event | Linked retained artifacts and table above |
| Bisection of six finite-rate threshold boundaries and evaluation of single candidate `1e-5` across frozen strata | Offline arithmetic over retained events only | PASS as design derivation; no runner/runtime confirmation | Values above |
| Neural runner/replay, artifact generation, unit suite, full suite | Not run by design | NOT RUN | Selection pass is read-only; future contract requires execution/tests |
| Custom-agent frontmatter/paths and `git diff --cached --check` | Publication checkout, Windows | PASS; required metadata/links present and no whitespace errors | Luna-58 contract and staged diff |

## Assumptions, limitations and unresolved issues

- RR artifact provenance authenticates the retained stream values; RR's
  historical execution worktree was dirty, so no claim is made that this
  analysis regenerates its execution revision.
- Offline recurrence is exactly appropriate before the first threshold
  crossing for these sequences; it cannot substitute for future full E2
  execution after the rate change.
- Initial/replay phases are deterministic reproducibility checks, not
  independent observations or a population-level efficacy test.
- No separate standalone Luna-55 independent-review handoff was located in
  this checkout; the workflow changelog records that independent review
  completed on `e6a5b7c900a023c70aa2776e039a4094f02962b4`.
- Integration readiness is **not applicable**; Luna-58 has not executed.

## Reproduction and rollback

The read-only derivation can be reproduced by loading the authenticated
selection and RR stream objects listed in the Luna-58 contract, sorting each
destination's retained receptions by their recorded order, and applying the
recurrence stated above. It does not invoke `run_phase`, a scientific runner,
or any artifact writer. This review changed no historical evidence. Rollback
for the authorized experiment is to discard only new Luna-58 code/results
after preserving its handoff; do not revert or rewrite Luna-45/46/53/54/55
history.

## Next assignment

**Luna-58** owns the contract's experiment-only implementation and execution.
It must report the exact single-field intervention, actual E2 crossing times,
full route/replay/bounds evidence, separate control strata, test results, and
unresolved gates, then stop for independent read-only Luna-0 review.
