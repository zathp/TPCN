---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian; fresh independent reviewer"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of Luna-46 depth-scaling diagnostic"
  task_id: "luna-0-independent-review-luna46-depth-scaling-diagnostic-20261006"
  component: "Read-only review of downstream-only retained evidence"
  status: "complete — PASS / MIXED (independent evidence verification; not efficacy)"
  contract_version: "1.2"
  branch: "copilot/luna46-depth-scaling-diagnostic"
  base_revision: "b601ffecf6c0ddc8b87b878a31f4366b8fa3ac0a"
  result_revision: "Commit D contains this handoff and the two authorized governance updates; exact commit is returned in the completion report"
  dependencies:
    - "Luna-46 authorization bb080228bac2287da49c1b47fc1484b436a59106"
    - "Luna-46 implementation 0e00929db35df89dfefcf28418abc7cc734ef380"
    - "Luna-46 bounded-root metadata correction 8c3c1aacb2211ba82c8596d8b5de8fbcb28c6148"
    - "Luna-46 result publication b601ffecf6c0ddc8b87b878a31f4366b8fa3ac0a"
    - "Luna-45 execution and independent review; Luna-44 retained relay-propagation evidence and review"
  owner: "Project owner"
  classification:
    - "fresh independent read-only evidence review"
    - "offline mechanism diagnostic"
    - "MIXED"
    - "no efficacy, architecture promotion, or production recommendation"
  hypothesis: "Some second-hop sequences fail at the frozen rate because signed evidence decays below the threshold."
  counter_hypothesis: "Insufficient total routed drive explains many non-crossings even in the signed zero-decay oracle."
  interfaces_relied_on:
    - "Luna-46 exact authorization and predeclared decision rules"
    - "Luna-45 calibrated destination enqueue, successful reception, trajectory, integration trace, configuration, and 22-file integrity catalog"
    - "Luna-44 matched source-to-relay raw captures, frozen fixture, and provenance"
    - "Architecture Contract 1.2, acceptance criteria, workflow, proposal lifecycle, and handoff template"
  label_information_boundary:
    - "Review used stream IDs, timestamps, signed routed payloads, and retained state only; no class labels or outcomes were used."
    - "All analysis is downstream-only and was not supplied to a neuron, runtime, topology, or trainer."
  timing_assumptions:
    - "Retained logical-time values; exact local prior timestamps; lambda=0.0125, tau=80, theta_Z=1."
    - "Arrival gaps are descriptive and do not alone establish causality or a useful adaptive rate."
  reset_boundaries:
    - "Independent actual and signed zero-decay accumulators reset for each of 320 streams."
  resource_bounds:
    - "Review inventory: 320 streams, 235 destination updates/receptions, 4096-event per-stream authorization bound."
    - "No production resource or capacity was changed."
  authorized_scope:
    - "Independently verify catalog, raw route pairs, recurrences, classifications, timing, matched depth comparison, and tests."
    - "Publish only this new review handoff, workflow summary, and architecture changelog entry."
  unauthorized_scope:
    - "No source, test, result JSON, old handoff, ACP, runtime, topology, configuration, fixture, or production change."
    - "No analyzer execution, observation capture, alternate run, tuning, WEMA, efficacy claim, or Luna-47."
  controls:
    - "Pinned Commit C baseline and clean published branch."
    - "Independent standard-library Node calculations over raw JSON and binary64 values; no analyzer or production-runtime imports."
    - "Exact identities, source/reception ordering, payload bits, timestamps, and retained fixture/configuration pins."
    - "Existing process-scoped Git LF overrides for pytest; baseline failures kept as failures."
  measurements:
    - "Output bytes/SHA/internal digest; all 33 input identities; all 22 Luna-45 catalog entries and digests; six phase digests."
    - "Initial/replay enqueue and reception reconciliation; actual/zero-decay recurrence, thresholds, categories, timing, signs, and runs."
    - "Applicable tests, full suite, compilation, and whitespace validation."
  information_boundary_check:
    - "PASS: retained-event-only offline arithmetic; labels, future neural inputs, and feedback were not used."
  hardware_mapping:
    - "Not applicable; no hardware run, equivalence claim, or hardware acceptance."
  architecture_invariants_touched:
    - "No A01-A15 clause or ACP changed. A07 permits downstream offline analysis; it does not make these statistics neural inputs."
  preserves:
    - "Luna-42 PASS WITH FOLLOW-UP"
    - "Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED"
    - "Luna-44 reviewed canonical-fixture relay-propagation baseline"
    - "Luna-45 NOT SUPPORTED IN THIS SETUP"
    - "ACP-0007 unchanged/disabled; ACP-0008 experimental, opt-in, and unpromoted"
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna46-depth-scaling-diagnostic-20261006.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Luna-46 focused tests: 122 passed."
    - "Focused Luna-45/Luna-44/ACP-0008/runtime/topology regression: 237 passed."
    - "Full repository suite: 1286 passed."
    - "Independent retained identities, event reconciliation, recurrence, categories, phase digests, and timing calculations: PASS."
    - "py_compile and git diff --check: PASS."
  tests_failed:
    - "Known cross-platform failure: test_luna44_canonical_fixture.py::test_two_fresh_process_materializations_match_committed_fixture; Windows materialization differs from the frozen Linux fixture at byte 490."
    - "Known cross-platform failure: test_luna44_canonical_fixture_verification.py::test_two_fresh_process_materializations_match_exactly; Windows materialization semantic digest differs from the frozen Linux fixture."
  tests_not_run:
    - "No new diagnostic/analyzer run or retained experiment run; neither was needed or authorized for this read-only review."
    - "No hardware validation."
    - "No critical-rate estimate; the predeclared optional solver remains NOT COMPUTED."
  assumptions:
    - "The five roots_truncated=true values bound causal-root metadata only; exact paired queue/reception rows remain complete for this event inventory. Complete ancestry expansion is not claimed for those five."
    - "The two Windows-versus-frozen-Linux materialization failures and unavailable-CUDA skip are the documented baseline exceptions, not passes."
  unresolved:
    - "Cross-platform frozen-fixture materialization parity remains unresolved and unchanged."
    - "Whether adaptive-timescale integration can improve any task outcome is untested; no critical rate or recommendation follows."
  recommended_next_agent:
    - "Project owner: receive this evidence disposition; no successor is authorized."
---

# Luna-46 independent review — PASS / MIXED

## Disposition and scope

**PASS for the authorized evidence gates; the independently recomputed
scientific classification is MIXED.** The result is a downstream-only
mechanism diagnostic, not task efficacy, a production-parameter recommendation,
an architecture promotion, or proof that changing the timescale would produce
an emission. No blocking material mismatch or new test regression was found.

This review was read-only for all code, result JSON, and prior artifacts. The
only publication changes are this new handoff, `workflow/docs/luna/LUNA_WORKFLOW.md`,
and `workflow/ARCHITECTURE_CHANGELOG.md`. No older handoff or evidence was
amended. No ACP was created or changed; no Luna-47 is authorized.

## Exact reviewed identity and source artifacts

At review start local `HEAD` and
`origin/copilot/luna46-depth-scaling-diagnostic` both equaled
`b601ffecf6c0ddc8b87b878a31f4366b8fa3ac0a`; the branch was clean.
The three commits after authorization are the published implementation,
bounded-root metadata correction, and Commit C artifact publication. The
changed paths since authorization are limited to the Luna-46 analyzer, its
focused tests, its result JSON, and its execution handoff. No production
neuron/runtime/topology/configuration or fixture path changed.
The retained provenance and branch inventory show one frozen configuration
with initial/replay evidence only; no alternate configuration/run appears in
the reviewed changes or retained catalog. This review generated no experiment
run.

| Identity | Independently checked value |
|---|---|
| Authorization | `bb080228bac2287da49c1b47fc1484b436a59106` |
| Analysis/source revision | `8c3c1aacb2211ba82c8596d8b5de8fbcb28c6148` |
| Analyzer SHA-256 | `efa935eecbac7f6cec077ee4397de103cbab09c8e1d2117d4e1c269d2f2a2c1c` |
| Result file bytes / SHA-256 | 2,315,475 / `a507a5eac1ca4df483c8493bb3bb6cc6a4f1b95c56837c9c77e760320c534d60` |
| Result internal output digest | `b942e908fd188fac08801e4635dced265e5e5ae6f79d2f2a879d4ecca491cb1a` |
| Luna-45 runner / execution revision | `97a93b394d071413075a1f102fdef695664722ff` |
| Luna-45 runner SHA-256 | `078a4fb7020414a3a017006291b778576ea72aeff08024063d7040ffe3307085` |
| Luna-45 frozen config digest | `cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a` |
| Luna-45 fixture SHA / semantic digest | `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629` / `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305` |
| Luna-45 integrity catalog SHA-256 | `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e` |
| Luna-45 ordered catalog digest / catalog byte total | `ba8b040fcc57c1e46364f1264a2f64c99d33c4c50844d1653f19f8e38d1caa58` / 386,727,576 |
| Luna-44 runner / execution revision | `4baab60f87b820db800e04d0eb3277fb0e94f9b3` |

**PASS:** I independently checked SHA-256, byte length, provenance pins, and
internal digests for all 33 diagnostic source identities; all 22 Luna-45
catalogued files; the Luna-45 catalog itself; and the published diagnostic.
The six Luna-45 initial/replay phase digests (three arms in each phase) were
also reconstructed independently from the retained configuration, records,
and arm reports and matched both the phase files and retained summary.
Canonical initial/replay phase bytes matched. Both raw initial/replay enqueue
and reception event inventories were byte-value identical after parsing,
with phase identity kept separately.
The ordered 22-file catalog digest, frozen configuration digest, and total
catalogued byte count were independently recomputed and matched.

The Luna-45 calibrated raw capture files contain both the upstream
`source -> relay` and downstream `relay -> destination` routes. The complete
initial and replay files each reconcile **1,950 enqueue/reception pairs**;
within each, the downstream subset is **235 pairs**. Pair keys and ordering
were checked by stream, queue sequence, and event ID; endpoints,
originating-emission identity, payload and payload bits, scheduled and actual
arrival times, route depth, lineage, root lists, and flags matched exactly.
Initial and replay each had **zero duplicates, orphan receptions, unmatched
enqueues, missing rows, or pair mismatches**. No event was inferred.

### Bounded causal-root flags

Five of the 235 downstream events have `roots_truncated=true`, identically in
both initial and replay:

| Stream | Queue sequence | Event ID | Retained causal-root entries |
|---|---:|---|---:|
| `c01-006` | 43 | `relay:excursion:1` | 16 |
| `c01-035` | 42 | `relay:excursion:1` | 16 |
| `c02-058` | 38 | `relay:excursion:1` | 16 |
| `c04-009` | 43 | `relay:excursion:1` | 16 |
| `c04-042` | 42 | `relay:excursion:1` | 16 |

**OBSERVED:** Each flag and its 16-entry root list are equal at enqueue and
successful reception; all corresponding event rows are present and the
complete route inventory reconciles. **DISPOSITION:** these flags mark
bounded causal-root metadata, not missing or truncated enqueue/reception
capture rows. The root expansion is incomplete for those five events and is
disclosed as such; this review does not claim full causal ancestry expansion.

## Independent recurrence and category calculation

Without importing the Luna-46 analyzer or production runtime, I recomputed
each destination update from the retained trajectory’s prior state and exact
`prior_clock`, the retained timestamp, and the actual raw routed payload:

```text
z_pre = z_previous * exp(-0.0125 * (timestamp - prior_clock))
z_post = z_pre + payload
z_zero_post = z_zero_previous + payload
```

All **235/235** retained destination trajectory/integration-trace updates
matched the signed equation and the retained post-update slow-state trace.
The largest equation residual was `1.1102230246251565e-16`; the largest
applicable `64 * epsilon * max(1, |observed|, |expected|)` bound was
`1.4210854715202004e-14`. State, timestamp, queue and event ordering were
not relaxed. The actual frozen configuration remains `lambda=0.0125`,
`tau=80`, and `theta_Z=1`. All updates were integrating in N mode; there was
no threshold drift, discharge, clipping, direct admission, or destination
canonical emission. The largest observed `abs(x_after_input)` was
`0.39040381534442403`, below `theta_E=1`; destination canonical emissions
were zero. The zero-decay sum is an offline signed oracle only.

| Independently recomputed quantity | Result |
|---|---:|
| Sequences | 320 |
| Successful destination routed receptions / updates | 235 / 235 |
| Reception-bearing denominator `N` | 108 |
| Actual max / min signed state | `0.7535008144325297` / `-0.8284450023885981` |
| Actual maximum absolute state | `0.8284450023885981` |
| Zero-decay signed max / min prefix | `1.7301488759150065` / `-2.071533974476769` |
| Zero-decay maximum absolute prefix | `2.071533974476769` |
| Actual threshold-crossing sequences | 0 |
| Zero-decay signed-prefix crossing sequences | 33 |
| Signed / absolute routed-input total | `1.9795521186613232` / `79.91216868870043` |
| Constructive aligned / opposing routed-input magnitude | `43.04945679159746` / `0` |
| Signed / absolute decay loss | `0.9406065988045667` / `32.87495008346143` |

The small final-decimal differences from the published display values are
ordinary summation-order rounding; all reconstructed states and classifications
match, without a threshold tolerance.

Applying the exact predeclared priority independently gives:

| Category | Count |
|---|---:|
| `NO-RECEPTIONS` | 212 |
| `ALREADY-CROSSING` | 0 |
| `TEMPORAL-RETENTION-LIMITED` | 33 |
| `CANCELLATION-LIMITED` | 0 |
| `DRIVE-LIMITED` | 75 |

The cutoffs are `substantial=ceil(.25*108)=27`,
`material=ceil(.10*108)=11`, and drive/cancellation support
`ceil(.75*108)=81`. Retention is substantial (`33 >= 27`), but
drive/cancellation is not below material (`75` is not `< 11`); the
drive/cancellation count is also below 81 while retention is not below 11.
Neither support predicate applies, so **MIXED** is the correct predeclared
verdict.

### Per-stream first crossings in the zero-decay oracle

Actual recurrence crossings: **none**. The signed zero-decay oracle first
crosses `abs(z)>=1` in exactly these 33 streams; each listed event is the
first such prefix in its stream (the values remain signed):

| Stream | First crossing event / queue | Signed prefix |
|---|---|---:|
| `c00-001` | `relay:excursion:3` / 50 | -1.0773309684 |
| `c00-004` | `relay:excursion:3` / 52 | 1.0049796804 |
| `c00-040` | `relay:excursion:3` / 58 | -1.0287313108 |
| `c00-045` | `relay:excursion:4` / 80 | -1.3210508366 |
| `c00-062` | `relay:excursion:3` / 65 | -1.0273765079 |
| `c01-007` | `relay:excursion:4` / 81 | -1.3156698435 |
| `c01-009` | `relay:excursion:3` / 69 | 1.0063340985 |
| `c01-014` | `relay:excursion:4` / 80 | 1.3542969998 |
| `c01-034` | `relay:excursion:3` / 61 | -1.0364965336 |
| `c01-044` | `relay:excursion:3` / 61 | -1.0208105960 |
| `c01-048` | `relay:excursion:3` / 56 | 1.0265759708 |
| `c01-057` | `relay:excursion:3` / 62 | -1.0344851219 |
| `c02-004` | `relay:excursion:4` / 73 | -1.3398955905 |
| `c02-025` | `relay:excursion:3` / 76 | 1.0075072139 |
| `c02-034` | `relay:excursion:4` / 89 | 1.3606816653 |
| `c02-042` | `relay:excursion:3` / 55 | 1.0783841591 |
| `c02-047` | `relay:excursion:3` / 51 | -1.0131341968 |
| `c02-061` | `relay:excursion:3` / 50 | -1.0740950950 |
| `c03-005` | `relay:excursion:3` / 62 | -1.0210555894 |
| `c03-012` | `relay:excursion:3` / 65 | 1.0469970267 |
| `c03-014` | `relay:excursion:3` / 59 | 1.0439617962 |
| `c03-024` | `relay:excursion:4` / 73 | 1.3151846949 |
| `c03-032` | `relay:excursion:3` / 55 | 1.0583983778 |
| `c03-042` | `relay:excursion:3` / 48 | -1.0662612969 |
| `c03-044` | `relay:excursion:3` / 57 | -1.0274227758 |
| `c04-002` | `relay:excursion:3` / 73 | 1.0352612976 |
| `c04-008` | `relay:excursion:3` / 52 | 1.0779317558 |
| `c04-010` | `relay:excursion:3` / 63 | 1.0394007008 |
| `c04-017` | `relay:excursion:3` / 50 | -1.0419866524 |
| `c04-020` | `relay:excursion:3` / 49 | 1.0497169468 |
| `c04-040` | `relay:excursion:3` / 61 | -1.0545357604 |
| `c04-053` | `relay:excursion:3` / 63 | 1.0158523860 |
| `c04-059` | `relay:excursion:3` / 57 | 1.0163224398 |

### Fully traced representative streams

The following are raw destination-routed payloads in retained order. `z actual`
is the retained post-update state; `z0` is the independently accumulated
signed no-decay prefix.

| Stream / category | Queue, timestamp, payload, actual post-state, zero-decay post-prefix |
|---|---|
| `c00-000` — NO-RECEPTIONS | 0 successful destination receptions; no destination update or prefix. `roots_truncated_metadata`: 0 true / 0 false; no destination roots were available to classify. |
| `c00-005` — NO-RECEPTIONS | 0 successful destination receptions; no destination update or prefix. `roots_truncated_metadata`: 0 true / 0 false; no destination roots were available to classify. |
| `c00-001` — TEMPORAL-RETENTION-LIMITED | q10, t=21.99604433078976, u=-0.39040381534442403, z=-0.39040381534442403, z0=-0.39040381534442403; q32, t=136.074419627699, u=-0.34786241916471916, z=-0.4416658973499536, z0=-0.7382662345091432; q50, t=193.05078675727995, u=-0.33906473385459, z=-0.5557290268556354, z0=-1.077330968363733. |
| `c00-004` — TEMPORAL-RETENTION-LIMITED | q15, t=31.30654507464083, u=0.33715654886865337, z=0.33715654886865337, z0=0.33715654886865337; q32, t=73.85004346711325, u=0.34557578507600506, z=0.5436721550417447, z0=0.6827323339446585; q52, t=130.6363250918846, u=0.32224734649489795, z=0.5895864461379309, z0=1.0049796804395563; q68, t=173.0959736162853, u=0.36823583835820234, z=0.7150106965874958, z0=1.3732155187977586; q92, t=258.2983329457644, u=0.35693335711724805, z=0.6034101915795146, z0=1.7301488759150065. |
| `c00-002` — DRIVE-LIMITED | q36, t=239.41753438196076, u=-0.344492963776797, z=-0.344492963776797, z0=-0.344492963776797; total absolute drive 0.344492963776797. |
| `c00-003` — DRIVE-LIMITED | q19, t=61.979001780610666, u=0.32461756332327346, z=0.32461756332327346, z0=0.32461756332327346; q54, t=258.52018925632655, u=0.30668350577167675, z=0.33450705948238596, z0=0.6313010690949502; total absolute drive 0.6313010690949502. |

The first two empty streams’ route capture records were also checked: absence
means zero destination events after filtering the complete two-link captures,
not that upstream events were absent. No-reception streams are counted but
excluded from `N`.

## Timing and matched Luna-44 comparison

Destination inter-arrival gaps were recomputed within streams, without
cross-character intervals. There were no ties. Percentiles use linear
interpolation at `(n-1)*p`.

| Second-hop destination gaps | Independently computed |
|---|---:|
| Gap count | 127 |
| Mean / p50 / p75 | `85.02553518676733` / `79.3174729376263` / `117.00313879569995` |
| p90 / p95 / p99 | `135.49262068046568` / `146.6972352970952` / `175.37006810775276` |
| Maximum / zero gaps | `196.54118747571587` / 0 |
| Event interval frequency (127 / summed within-stream gap span) | `0.01176117266187619` |
| Same-sign run count / mean length / median / maximum | 108 / `2.175925925925926` / 2 / 6 |

The fair first-hop comparison was independently reconstructed from Luna-44’s
calibrated raw captures, not inferred from the Luna-45 rate. All 1,950
Luna-44 enqueue/reception pairs (both links) matched; filtering the original
source-to-relay hop yields 1,715 events and 1,418 within-stream gaps. The
common 320 stream IDs and frozen fixture are aligned. The interval frequency
uses the same interval-count / summed-within-stream-span definition.

| First-hop source-to-relay comparison | Independently computed |
|---|---:|
| Events / within-stream gaps | 1,715 / 1,418 |
| Mean / p50 / p90 | `28.345605257252778` / `18.745645230767586` / `71.26844559107914` |
| p95 / p99 / maximum | `90.9904284452375` / `116.33489908346476` / `144.04056750003937` |
| Event interval frequency | `0.035278837439681424` |
| Positive / negative / zero payloads | 868 / 847 / 0 |
| Same-sign run count / mean length / median / maximum | 325 / `5.276923076923077` / 4 / 19 |

Second-hop payload signs were independently `121 / 114 / 0` positive /
negative / zero. Its lower interval frequency, longer gaps, and shorter
same-sign runs are **OBSERVED** in this matched retained comparison.
**INFERENCE LIMIT:** the layer inputs and event opportunity differ; these
statistics do not establish that hop depth caused the differences or that
the layers should have equal statistics.

## Interpretation boundary and architecture status

**OBSERVED:** 33 reception-bearing streams have a signed zero-decay prefix
crossing while none crosses under the actual frozen recurrence; 75 streams
remain drive-limited even in the absolute-input bound; none is
cancellation-limited. The later/longer second-hop gaps are descriptive.

**INFERRED, narrowly:** both temporal retention and insufficient total drive
contribute under this frozen setup. **Adaptive-timescale relevance:** this
evidence supports considering the *question* of a separately authorized,
bounded adaptive-timescale investigation for the subset that crosses in the
zero-decay oracle. It does not establish that any finite alternate timescale
would cross, improve a task outcome, or be preferable. Most reception-bearing
streams (75/108) are drive-limited; this is not a universal retention remedy.
The predeclared critical-rate solver was not implemented and no rate estimate
or sweep was performed. Consistent with the owner’s ACP-0008 decision, this is
not a request or recommendation to implement WEMA, change a timescale, or
alter ACP-0008; any such work would require separate owner authorization and
its own contract. No efficacy claim is made.

Historical dispositions remain unchanged: Luna-42 **PASS WITH FOLLOW-UP**;
Luna-43 **BLOCKED / DESTINATION COMPARISON UNDETERMINED**; Luna-44’s reviewed
canonical-fixture relay-propagation baseline; Luna-45 **NOT SUPPORTED IN THIS
SETUP**. ACP-0007 remains unchanged/disabled. ACP-0008 remains experimental,
opt-in, and unpromoted. No A01–A15 clause changed.

## Validation record

Environment: Windows 10 build 19045; the documented CPython 3.11.5 executable
was used. Each pytest/compile command used only process-scoped
`core.autocrlf=false` and `core.eol=lf` overrides.

| Command or procedure | Result |
|---|---|
| Independent digest/catalog checks (33 source identities; 22 Luna-45 files; diagnostic bytes and internal digest) | PASS |
| Recomputed six initial/replay arm phase digests and canonical replay identities | PASS |
| Reconciled all 1,950 raw route pairs per phase and all 235 downstream pairs; initial/replay event identities exact | PASS; zero duplicate/orphan/missing/mismatched events |
| Recomputed every destination recurrence, slow-state trace, threshold, signed prefix, category, first crossing, and aggregate | PASS; 235 updates, zero recurrence/classification mismatches |
| Recomputed Luna-44 first-hop and Luna-45 second-hop timing, signs, runs, and frequency | PASS; fair common fixture/320-stream comparison |
| `python -m pytest tests\test_luna46_depth_scaling_diagnostic.py -q -rs` | **122 passed** |
| Luna-38–45, Luna-44 fixture/verifier, event-runtime, and topology regression selection | **237 passed, 2 known failures; exit 1** |
| `python -m pytest -q -rs` | **1,286 passed, 2 known failures, 1 skipped; exit 1** |
| `python -m py_compile run_luna46_depth_scaling_diagnostic.py tests\test_luna46_depth_scaling_diagnostic.py` | PASS |
| `git diff --check` at reviewed baseline | PASS |

The two failing assertions are unchanged documented Windows-versus-frozen-Linux
materialization comparisons:

1. `tests\test_luna44_canonical_fixture.py::test_two_fresh_process_materializations_match_committed_fixture`
   — bytes differ at offset 490.
2. `tests\test_luna44_canonical_fixture_verification.py::test_two_fresh_process_materializations_match_exactly`
   — frozen-Linux semantic digest mismatch.

Both were already recorded as baseline failures in the Luna-46 authorization
and execution handoffs; neither is relaxed, hidden, or newly introduced here.
The full suite’s `tests\test_gpu_visualization.py:61` was skipped because CUDA
is unavailable. No other test failure occurred.

The review did **not** rerun the Luna-46 analyzer, Luna-45 experiment, or
fixture generation; it recomputed from the pinned retained JSON instead.
Hardware validation, efficacy, and critical-rate estimation were not run.

## Reproduction, publication, and next assignment

Review inputs are the pinned artifacts listed in the Luna-46 execution
handoff, including `artifacts/luna45-acp0008-depth2-destination-integration-20261006/`,
`artifacts/luna44-acp0008-independent-routing-rerun-20261005/`, the canonical
fixture, and `artifacts/luna46-depth-scaling-diagnostic-20261006.json`.
The independent calculations used standard-library Node JSON, SHA-256,
binary64 arithmetic, and explicit per-stream loops. No analyzer or TPCN
runtime function was imported or called.

**Integration readiness:** PASS for this bounded evidence review only. The
MIXED mechanism result is valid and interpretable within its frozen scope;
the two known platform comparisons remain limitations, not blockers newly
introduced by Luna-46. There is no architecture promotion or successor
authorization.

**Next:** project owner receives the independent disposition and decides
whether any separate work is warranted. **Luna-47 is not authorized.**
