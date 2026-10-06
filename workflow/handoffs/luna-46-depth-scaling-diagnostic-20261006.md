---
tpcn_handoff:
  agent: "Luna-46 implementation worker; independent review pending"
  luna_identifier: "Luna-46"
  descriptive_name: "Offline depth-scaling diagnostic"
  task_id: "luna-46-depth-scaling-diagnostic-20261006"
  component: "Downstream offline evidence analysis"
  status: "complete - MIXED; independent review pending"
  contract_version: "1.2"
  branch: "copilot/luna46-depth-scaling-diagnostic"
  base_revision: "d1f901d3d995dc013f22dd086ae1ed8ffd28293d"
  authorization_revision: "bb080228bac2287da49c1b47fc1484b436a59106"
  implementation_revision: "0e00929db35df89dfefcf28418abc7cc734ef380"
  implementation_correction_revision: "8c3c1aacb2211ba82c8596d8b5de8fbcb28c6148"
  analysis_revision: "8c3c1aacb2211ba82c8596d8b5de8fbcb28c6148"
  artifact_publication_revision: "Commit C publishing this handoff and retained JSON; exact commit returned after publication"
  result_revision: "Commit C publishing this handoff and retained JSON; exact commit returned after publication"
  dependencies:
    - "Commit A Luna-0 authorization at bb080228bac2287da49c1b47fc1484b436a59106"
    - "Merged Luna-45 corrective review and retained evidence"
  owner: "Project owner"
  classification:
    - "OFFLINE ANALYSIS"
    - "MECHANISM DIAGNOSTIC"
    - "MIXED"
    - "not efficacy or production configuration evidence"
    - "independent Luna-0 review pending"
  hypothesis: "Some depth-2 destination sequences cross theta_Z in the signed zero-decay oracle but not at the frozen calibrated rate."
  counter_hypothesis: "Many sequences remain below threshold even without decay because total routed drive is insufficient."
  interfaces_relied_on:
    - "Luna-45 calibrated destination emission, enqueue, successful reception, trajectory, integration trace, frozen configuration, and integrity catalog"
    - "Luna-44 calibrated source-to-relay emission, enqueue/reception, frozen configuration, and retained fixture provenance"
    - "Committed Luna-46 downstream-only analyzer"
  label_information_boundary:
    - "No labels were used; analysis is downstream-only and does not feed neural computation."
  timing_assumptions:
    - "Retained logical-time units; lambda=0.0125, tau=80, theta_Z=1.0."
    - "Each character is analyzed independently; retained prior update timestamps are used."
  reset_boundaries:
    - "Analysis state resets to zero per retained character; no cross-character accumulation."
  resource_bounds:
    - "320 retained characters, at most 4096 observations per character, 100 MiB input file limit."
  authorized_scope:
    - "Verify pinned retained inputs and independently reconcile actual enqueues/receptions."
    - "Reconstruct frozen actual recurrence and offline signed zero-decay accumulator."
    - "Measure sign, decay, arrival timing and fair retained depth comparison."
  unauthorized_scope:
    - "No parameter/configuration changes, tuning, sweeps, alternate runs, production/neuron/runtime/topology/fixture edits, WEMA, ACP changes, efficacy, architecture promotion, or Luna-47."
  controls:
    - "Exact input file lengths, SHA-256, artifact digests, provenance, catalog coverage, fixture/configuration identities, and retained initial/replay byte equality."
    - "Independent one-to-one enqueue/reception checks on exact identities, payload bits, endpoints, timestamps and event order."
    - "Offline actual recurrence checked at every recorded update boundary with the committed binary64 tolerance; no threshold tolerance."
    - "Replay analysis canonical bytes compared exactly."
  measurements:
    - "Per-sequence signed/absolute input, actual and zero-decay state, crossings, category, constructive/opposing evidence, retention, decay loss, timing, and roots_truncated metadata."
    - "Pooled timing, category verdict, and matched Luna-44 first-hop versus Luna-45 second-hop descriptions."
  information_boundary_check:
    - "PASS: input and output are downstream-only. No output is supplied to any TPCN computation."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 or ACP change; offline analysis only."
  preserves:
    - "Luna-42 PASS WITH FOLLOW-UP"
    - "Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED"
    - "Luna-44 reviewed canonical-fixture relay-propagation baseline"
    - "Luna-45 NOT SUPPORTED IN THIS SETUP"
    - "ACP-0007 unchanged/disabled; ACP-0008 experimental, opt-in, unpromoted"
  architecture_change: false
  proposal: null
  files_changed:
    - "run_luna46_depth_scaling_diagnostic.py"
    - "tests/test_luna46_depth_scaling_diagnostic.py"
    - "artifacts/luna46-depth-scaling-diagnostic-20261006.json"
    - "workflow/handoffs/luna-46-depth-scaling-diagnostic-20261006.md"
  tests_added:
    - "Synthetic recurrence, zero-decay, sign, category, threshold, timing, resource, capture mutation, replay, verdict, and deterministic-output tests."
  tests_passing:
    - "Luna-46 focused: 122 passed."
    - "Post-correction relevant regression: 470 passed; the two documented platform failures remain separately recorded."
    - "Post-correction full suite: 1286 passed; two documented platform failures; one CUDA-unavailable skip."
    - "Retained integrity/provenance-only gate: PASS for 33 pinned input identities; no sequence analysis during this gate."
    - "Retained Luna-45 analysis: completed; replay and analytical outputs byte-identical."
    - "py_compile and git diff --check passed."
  tests_failed:
    - "tests/test_luna44_canonical_fixture.py::test_two_fresh_process_materializations_match_committed_fixture - known Windows versus frozen-Linux bytes differ at offset 490."
    - "tests/test_luna44_canonical_fixture_verification.py::test_two_fresh_process_materializations_match_exactly - known Windows versus frozen-Linux semantic digest mismatch."
  tests_not_run:
    - "Independent Luna-0 review is pending."
    - "No observation-only capture or science rerun."
    - "CUDA test skipped because CUDA is unavailable."
  assumptions:
    - "Matching roots_truncated=true is retained bounded causal-root metadata, not evidence that the enqueue/reception capture files are incomplete; the flag and roots are preserved and reported."
    - "The computed offline no-decay accumulator is analytical only and does not assert that a production neuron with another decay value would behave identically."
  unresolved:
    - "Independent Luna-0 verification of artifact identities, recurrence, zero-decay results, classifications, timing, parameter non-mutation and tests."
    - "Cross-platform fixture materialization parity remains unresolved."
  recommended_next_agent:
    - "Fresh Luna-0 independent review and governance disposition; no Luna-47."
---

# Luna-46 offline depth-scaling diagnostic

## Outcome and scope

**OBSERVED:** The retained Luna-45 calibrated destination stream was analyzed
offline after Commit B and its bounded-root metadata correction were published.
The analysis uses actual retained relay-to-destination enqueues and successful
receptions. It does not rerun Luna-45, generate a fixture, modify a production
setting, or feed results back to TPCN.

The result is **MIXED** under the exact predeclared Luna-0 cutoffs. Of 320
sequences, 108 contain one or more destination receptions and 212 have none.
Among the 108 reception-bearing sequences:

| Category | Count | Fraction |
|---|---:|---:|
| ALREADY-CROSSING | 0 | 0 |
| TEMPORAL-RETENTION-LIMITED | 33 | 30.56% |
| CANCELLATION-LIMITED | 0 | 0 |
| DRIVE-LIMITED | 75 | 69.44% |

Here `substantial = ceil(0.25 * 108) = 27`, `material = ceil(0.10 * 108) =
11`, and the drive/cancellation support cutoff is `ceil(0.75 * 108) = 81`.
Retention-limited sequences are substantial, but the combined drive and
cancellation count is not below material. The drive/cancellation count is
not at least 81 and retention is not below material. Therefore neither
support verdict applies; the predeclared residual verdict is **MIXED**.
No sequence crosses the actual frozen recurrence threshold. All 33
retention-limited sequences cross only in the offline signed zero-decay
prefix oracle. The remaining 75 do not reach threshold even under zero decay;
no cancellation-limited sequence was observed.

**INFERRED, bounded:** A meaningful subset of these retained sequences had
enough signed available drive to cross without decay, while temporal leakage
prevented an actual crossing. The retained result is relevant to a future
owner decision about adaptive timescale integration, but does not establish
that WEMA is the solution or that changing a production timescale would
improve a task. The larger drive-limited group prevents treating leakage as
the sole explanation. No efficacy, prediction, energy, utility, or hardware
claim is made.

Historical scientific dispositions are preserved: Luna-42 **PASS WITH
FOLLOW-UP**; Luna-43 **BLOCKED / DESTINATION COMPARISON UNDETERMINED**;
Luna-44 reviewed canonical-fixture relay-propagation baseline; Luna-45
**NOT SUPPORTED IN THIS SETUP**. This diagnostic does not reinterpret
Luna-45. ACP-0007 remains unchanged/disabled. ACP-0008 remains experimental,
opt-in, and unpromoted.

## Exact provenance and retained integrity

| Identity | Value |
|---|---|
| Baseline / branch | `d1f901d3d995dc013f22dd086ae1ed8ffd28293d` / `copilot/luna46-depth-scaling-diagnostic` |
| Authorization revision | `bb080228bac2287da49c1b47fc1484b436a59106` |
| Analyzer implementation revision | `8c3c1aacb2211ba82c8596d8b5de8fbcb28c6148` |
| Analyzer source SHA-256 | `efa935eecbac7f6cec077ee4397de103cbab09c8e1d2117d4e1c269d2f2a2c1c` |
| Luna-45 runner / execution revision | `97a93b394d071413075a1f102fdef695664722ff` |
| Luna-45 fixture SHA-256 / semantic digest | `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629` / `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305` |
| Luna-45 config digest | `cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a` |
| Luna-45 integrity catalog SHA-256 | `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e` |
| Luna-44 runner / execution revision | `4baab60f87b820db800e04d0eb3277fb0e94f9b3` |
| Luna-44 config digest | `942b86a9cd7a3965265ec9d01aff7e0b0e2bf68b309f0e0bd22dc4cbae71884e` |
| Analysis artifact bytes / SHA-256 | 2,315,475 / `a507a5eac1ca4df483c8493bb3bb6cc6a4f1b95c56837c9c77e760320c534d60` |
| Analysis internal output digest | `b942e908fd188fac08801e4635dced265e5e5ae6f79d2f2a879d4ecca491cb1a` |
| Analytical initial/replay digest | `fd22cf6ba530fd727d7c199c9f2dc3eed3351fa554368288a817fc45813eb649` |

The integrity-only pre-analysis pass verified 33 pinned inputs, including the
Luna-45 22-file catalog, Luna-44 retained files, fixture and manifest
identities, source revisions, runner Git blobs, provenance, and required
ancestry. It completed without sequence statistics. The analyzer then
revalidated the input inventory and exact provenance before reading
sequences. All three Luna-45 arm initial/replay canonical phase byte pairs
matched their pinned phase digests. Luna-46 initial/replay per-sequence
analytical results were canonical-byte equal.

The Luna-45 raw event capture explicitly records `roots_truncated=true` for
5 of 235 calibrated destination receptions and `false` for the other 230.
Enqueue and reception values match exactly for roots and this flag; the
analyzer preserves and reports these bounded provenance metadata values.
They are not missing raw capture rows. No enqueues or receptions were
inferred or dropped. The Luna-45 independent review's source-root ancestry
verification remains authoritative for its causal claims; this diagnostic
does not claim complete root expansion for the five flagged records.

## Recurrence, sign, and retention results

For every retained destination update, the actual signed recurrence used
`lambda = 0.0125`, `tau = 80`, and unchanged `theta_Z = 1.0`. The retained
prior update timestamp was used, including intervening destination updates.
Equation checks used the committed bound
`64 * sys.float_info.epsilon * max(1, abs(observed), abs(expected))`;
raw payload/timestamp bits, sequence/event identities and deterministic
ordering were exact. There was no threshold tolerance. The zero-decay oracle
accumulated the same signed routed payloads without decay or discharge and was
never run as a neuron configuration.

| Quantity | Observed |
|---|---:|
| Successful destination receptions | 235 |
| Maximum actual signed `z` | `0.7535008144325297` |
| Minimum actual signed `z` | `-0.8284450023885981` |
| Maximum actual `abs(z)` | `0.8284450023885981` |
| Maximum signed zero-decay prefix | `1.7301488759150065` |
| Minimum signed zero-decay prefix | `-2.071533974476769` |
| Maximum zero-decay `abs(z)` | `2.071533974476769` |
| Actual crossing sequences | 0 |
| Zero-decay crossing sequences | 33 |
| Signed sum of routed inputs | `1.9795521186613219` |
| Sum of absolute routed inputs | `79.9121686887004` |
| Constructively aligned input magnitude | `43.04945679159747` |
| Opposing-sign input magnitude / cancellation | 0 / 0 |
| Aggregate signed decay loss | `0.9406065988045669` |
| Aggregate absolute decay loss | `32.87495008346142` |
| Maximum absolute zero-decay-minus-actual state difference | `1.243088972088171` |

Per-input retained fractions `rho_i` across the 235 receptions had mean
`0.3564213728635379`, median `0.35476072231171557`, p90
`0.6086048221882489`, minimum `0.019848052773280955`, and maximum
`0.8097173944673821`. The aggregate nonzero-prior retention ratio had 127
entries (zero prior states are reported as undefined, not full retention),
mean `0.3836741335690604`, median `0.3710314638608945`, p90
`0.6093492952201253`.

The analyzer measures decay at every retained destination update boundary,
not only the routed reception boundaries, so its summed decay loss includes
decay across intervening local destination events. Signed and absolute loss
are separately reported. The category oracle remains based on actual routed
signed inputs and the retained production recurrence.

## Timing and depth comparison

Destination reception inter-arrival gaps include zero ties; this run had no
zero gaps. Across 127 within-character intervals, mean gap was
`85.02553518676737`, median `79.3174729376263`, p75 `117.00313879569995`,
p90 `135.49262068046568`, p95 `146.6972352970952`, p99
`175.37006810775276`, maximum `196.54118747571587`. Percentiles use the
predeclared linear interpolation at `(n-1)*p`; gaps are compared with
`tau=80`, not treated alone as causal proof.

There were 108 constructive same-sign destination runs, lengths mean
`2.175925925925926`, median 2, maximum 6. Their 127 within-run gaps had the
same distribution as all destination gaps; no zero-payload events occurred.

The matched Luna-44 source-to-relay versus Luna-45 relay-to-destination
comparison passed the common fixture, sequence identity, phase, reset, and
capture-semantics checks. It is descriptive only; layer statistics are not
assumed equal.

| Metric | Source -> relay | Relay -> destination |
|---|---:|---:|
| Routed events | 1,715 | 235 |
| Inter-arrival intervals | 1,418 | 127 |
| Summed within-stream inter-arrival duration | `40194.06825478446` | `10798.242968719456` |
| Mean inter-arrival duration | `28.345605257252796` | `85.02553518676737` |
| Reciprocal mean inter-arrival interval (intervals per logical-time unit) | `0.03527883743968141` | `0.011761172661876184` |
| Routed event rate over common fixture observation window (receptions per logical-time unit) | `0.01919241978881272` | `0.0026298651022571362` |
| Inter-arrival mean / median | `28.34560525725278` / `18.745645230767586` | `85.02553518676737` / `79.3174729376263` |
| Inter-arrival p90 / p95 / p99 / max | `71.26844559107914` / `90.9904284452375` / `116.33489908346476` / `144.04056750003937` | `135.49262068046568` / `146.6972352970952` / `175.37006810775276` / `196.54118747571587` |
| Positive / negative / zero payloads | 868 / 847 / 0 | 121 / 114 / 0 |
| Same-sign runs: count, mean length, median, max | 325, `5.276923076923077`, 4, 19 | 108, `2.175925925925926`, 2, 6 |
| Same-sign run-gap mean / median / max | `27.845856659595746` / `18.697324030991602` / `144.04056750003937` | `85.02553518676737` / `79.3174729376263` / `196.54118747571587` |

The reciprocal mean interval uses interval count divided by the sum of
within-character first-to-last arrival durations; it is not an event count
divided by the common observation window. The event rate uses routed event
counts divided by the summed first-to-last frozen fixture timestamp duration
over matched characters (`89358.19552048748` logical-time units). Both the
lower event rate and longer inter-arrival intervals at the second hop are
observed in these matched retained streams. They do not prove a causal effect
of hop depth or show that the two layers should have identical input
statistics.

## Validation record

Environment: Windows 10 build 19045, CPython 3.11.5, 64-bit AMD64.

| Command or procedure | Observed result |
|---|---|
| `git status --short --branch`; HEAD and `git ls-remote` check | Clean, published branch at analyzer correction revision before analysis |
| `python -m pytest tests\test_luna46_depth_scaling_diagnostic.py -q -rs` | 122 passed |
| Luna-46/Luna-45/Luna-44/ACP-0008/runtime/routing regression selection | 470 passed, 2 known failures; exit 1 |
| `python -m pytest -q -rs` | 1,286 passed, 2 known failures, 1 CUDA-unavailable skip; exit 1 |
| `python -m py_compile run_luna46_depth_scaling_diagnostic.py tests\test_luna46_depth_scaling_diagnostic.py` | Passed |
| `git diff --check HEAD^ HEAD` | Passed |
| `verify_integrity()` | PASS; 33 pinned inputs, integrity/provenance only, no sequence analysis |
| `python run_luna46_depth_scaling_diagnostic.py --output artifacts\luna46-depth-scaling-diagnostic-20261006.json` | Exit 0; `MIXED`; deterministic output readback passed |
| Recompute output digest from canonical JSON without `output_digest` | Matches `b942e908fd188fac08801e4635dced265e5e5ae6f79d2f2a879d4ecca491cb1a` |
| Recheck selected Luna-45 initial/replay raw and result files against catalog | All six hashes and byte lengths match |
| Independent Luna-0 review | Pending; this handoff is not approval |

The two known failures remain failed, not relaxed or hidden:

1. `tests/test_luna44_canonical_fixture.py::test_two_fresh_process_materializations_match_committed_fixture` — Windows materialization bytes differ from the frozen Linux fixture at offset 490.
2. `tests/test_luna44_canonical_fixture_verification.py::test_two_fresh_process_materializations_match_exactly` — Windows materialization semantic digest differs from the frozen Linux fixture.

The full suite skipped `tests/test_gpu_visualization.py:61` because CUDA is
unavailable. No new test failure was observed. The earlier first analyzer
attempt stopped before writing output because it incorrectly treated matching
bounded `roots_truncated` metadata as missing capture evidence. A separate
published correction preserves and reports this flag, requires exact
enqueue/reception agreement, and has synthetic tests for matching and mutated
values. The first blocked attempt wrote no artifact; the published result
above was created only after correction and the post-correction regression
and full-suite gates.

## Interpretation limits and next assignment

**OBSERVED:** 33 sequences cross threshold in the offline zero-decay signed
oracle but not in the actual frozen recurrence; 75 reception-bearing
sequences remain drive-limited; no cancellation-limited or actual-crossing
sequence was found. **INFERRED:** both temporal retention and insufficient
drive contribute in this setup. **HYPOTHESIZED:** an adaptive timescale might
help some sequences, but this was not tested and is not a Luna-46 result.

No rate search or critical-rate estimate was performed. The analyzer records
the optional estimate as not computed because it has no uniqueness solver.
No production configuration was run at another rate. Luna-45's result,
architecture status and historical outcomes remain unchanged.

**Next:** a fresh Luna-0 reviewer must verify the artifact hashes and exact
raw stream reconciliation; independently recompute actual and zero-decay
recurrences, category counts and representative sequences in every nonempty
category; recompute timing distributions; inspect unchanged production
parameters; and rerun focused/full tests. Review must explicitly address the
five matching bounded-root flags, the two known fixture failures, one CUDA
skip, the MIXED verdict, and the boundary on adaptive integration relevance.
No Luna-47 is authorized.
