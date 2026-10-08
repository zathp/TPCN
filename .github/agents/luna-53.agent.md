---
name: Luna-53 ACP-0008 Destination Retention Causal Confirmation
description: Test whether slower destination z retention selectively produces discharge and canonical emission on retained Luna-46 streams.
---

# Luna-53 — ACP-0008 Destination Retention Causal Confirmation

## Authorization

**AUTHORIZED / NOT EXECUTED.** This is one bounded, opt-in experimental
mechanism experiment. It is not task efficacy, production integration,
architecture promotion, hardware validation, or a change to canonical
semantics. Execute only after this contract is published on `origin/main`.

The governance baseline is
`ef257f5030fba5814c0f8a2c729a4f740e90f576`; the exact publication commit
containing this contract is the Luna-53 authorization revision. Record its
full SHA as the execution base. Luna-52 is closed: its clean committed
validation passed and the documentation-only follow-up review returned PASS.
No Luna-53 contract existed at the governance baseline.

Luna-46 remains **MIXED**. Luna-47A/B component conclusions are restricted
to their measured setup. No task-level efficacy, useful structural-growth
efficacy, production integration, or hardware equivalence is established.
ACP-0008 remains **accepted, experimental, opt-in, and disabled by default**.
This authorization uses its existing parameter surface; it does not amend
ACP-0008 or A01-A15.

Read the current architecture contract, changelog, workflow, acceptance
criteria, ACP process/template, handoff template, ACP-0008, Luna-46 and
Luna-47A/B contracts/handoffs, and the Luna-0 Luna-47 review before execution.
Relevant boundaries are A01, A02, A06, A07, A08, and A15. No global neural
clock, labels, or offline analysis may enter neuron computation.

## One hypothesis and causal question

**Hypothesis:** On the authenticated frozen destination-arrival streams,
changing only the destination ACP-0008 slow-state decay rate from the
historical value `decay_rate_z=0.0125` (`tau_z=80`) to the single
predeclared value `decay_rate_z=0.00125` (`tau_z=800`) will cause at least
one new `z` discharge and linked canonical E2 emission in the 33
Luna-46 `TEMPORAL-RETENTION-LIMITED` streams, while causing none in the
75 `DRIVE-LIMITED` or 212 `NO-RECEPTIONS` streams.

The one causal uncertainty is whether the selective representability response
seen in Luna-47A's isolated accumulator transfers to the existing bounded
ACP-0008 E2 destination neuron, including its unchanged fast-state
qualification, sign check, discharge, and ordinary emission scheduling.

This is a mechanism confirmation on frozen destination inputs. It does not
test network/task utility, learning, downstream propagation, or whether the
new emissions improve prediction or classification.

## Evidence and retained input boundary

Use only the authenticated Luna-46/Luna-47A retained evidence; do not
regenerate the Luna-44 fixture or rerun its source/relay network.

| Evidence | Pinned identity at governance baseline |
|---|---|
| Luna-45 frozen destination configuration | `artifacts/luna45-depth2-frozen-config-20261006-r2/config.json`; file SHA-256 `a19bf911ebe04c52aba7d83e376faac853519db3308419ca8bfcad35143858e1`; configuration digest `cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a`; Git blob `1fcf4e9865d1b6d1af9f39ab74d399eb6496b166` |
| Luna-45 retained raw-route integrity catalog | `artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json`; file SHA-256 `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`; Git blob `b1aaef4006422f321922bfb58425e4fb646d96b9` |
| Luna-44 canonical fixture used by Luna-45 | Fixture revision `6413cffe6982bccc6698af6bebfae51f04e71dd9`; file SHA-256 `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`; semantic SHA-256 `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305` |
| Luna-46 corrected diagnostic | `artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`; SHA-256 `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e`; Git blob `9506369d97babf7bc0ef15ed52efb738dcdcd549`; 2,337,377 checkout bytes |
| Luna-47A extracted input bundle | `artifacts/luna47a/inputs.json`; SHA-256 `03b5a27700723afa266e63b516c6b3dfbc9a7accc6983d21a4f7a12e4383b185`; Git blob `24989419f87dcf49ff0a651e5909c995e0d25fc0`; 10,665,778 bytes |
| Luna-47A fixed-rate results | `artifacts/luna47a/results.json`; SHA-256 `d1cac5065410767a42a35f99b659b4a4377f1b84d300e5cfd3ed304600322cff`; Git blob `1526d1d15cbb59b0ca3d0fa04ef04f1c2c803f8f` |

Verify exact identities against the committed Git objects at the recorded
baseline; distinguish Git blob IDs from content SHA-256 and accept only the
repository's exact declared LF-to-CRLF materialization where applicable.
Reconcile every extracted input event to the Luna-45 raw route record and
Luna-46 reconstruction. Use both retained `initial` and `replay` phases;
preserve all 320 stream identities and the 235 successful destination
receptions. The Luna-46 category labels are evaluation-only strata. They
must not be supplied to the E2 neuron or runtime.

The existing evidence supports the experiment but does not pre-answer it:
Luna-46 has 212 no-reception streams, 33 temporal-retention-limited streams,
75 drive-limited streams, and zero cancellation-limited/already-crossing
streams. No destination stream crossed the historical `z` threshold or
emitted at the calibrated rate. The signed zero-decay diagnostic crossed in
33 streams. Luna-47A's isolated accumulator at `tau_z=800` crossed in 19/33
retention-limited streams, with 75/75 drive-limited streams still below
threshold and no target clipping. Those crossings were representability,
not discharge or emission.

## Frozen conditions

Run the existing `MultiExcursionNeuron`/E2 event runtime on each stream as a
single isolated destination neuron. Inject only the exact retained
relay-to-destination arrivals, with their signed payloads, original timestamps
and deterministic queue order. Process internally scheduled events with the
existing runtime. Do not execute or alter upstream nodes or route any new
emission onward.

| Condition | `decay_rate_z` | All other parameters |
|---|---:|---|
| Historical control | `0.0125` | Exact destination `E1Config`/`IntegrationConfig` from the authenticated Luna-45 configuration |
| Single intervention | `0.00125` | Identical configuration except for `IntegrationConfig.decay_rate_z` |

The intervention value is the previously declared Luna-47A `tau_z=800`
condition, selected because it showed a partial, control-discriminating
response without target clipping. It is not newly fitted to Luna-53 output.
Do not run `tau_z=8000`, a rate sweep, calibration, or a fallback parameter.
Use the unchanged E2 implementation, event queue, `theta_E`, `theta_Z`,
`input_gain`, `z_max`, fast decay, event budgets, return/emission delays,
reset boundary, routing/event semantics, and fixed retained input order.

Run two fresh deterministic executions per condition, one for each retained
initial/replay phase, with a separate execution identity for each
condition/phase pair. The phases are replay records, not independent
scientific samples. Compare complete event/state outcomes exactly where the
runtime contract requires exact replay. Do not describe a second
materialization of one run as an independent run.

## Controls, measurements, and prediction

The historical control is mandatory and must reproduce the recorded
destination baseline behavior before the intervention is interpreted.
Retention-limited streams are the positive mechanistic group. The 75
drive-limited streams are the primary mechanistic negative control; the 212
no-reception streams are a second negative control for destination-only
retention.

Record, per stream and every relevant local/runtime event:

- source event identity, payload bits, timestamp, prior local clock, queue
  sequence, and reset identity;
- fast `x` and slow `z` states before/after decay, qualification, input,
  discharge, and all scheduled transitions;
- whether each input was excluded from or added to `z`, with the runtime's
  existing reason/classification;
- `z` threshold margins, sign agreement, discharge amount, and linked
  canonical emission identity, payload and time;
- pending/internal event counts, bounded-state maxima, clipping, event-budget
  use, and termination/settling status;
- category-level counts, target overlap with Luna-47A's 19 `tau_z=800`
  scalar-crossing streams, and raw per-event data sufficient to recompute all
  summaries.

**Positive prediction:** relative to the historical control, the intervention
increases `z` retention and creates at least one new integration discharge
with its existing scheduled canonical emission in the 33 target streams.
Any resulting emission should be attributable to the existing ACP-0008
discharge path, not direct fast-state input admission. The exact emission
count is not predicted from the scalar accumulator because E2 qualification,
sign agreement, discharge and pending-event behavior remain active.

**Negative prediction:** neither the 75 drive-limited streams nor the 212
no-reception streams gains a `z` discharge or canonical emission. Report any
deviation without relabeling or removing a control case.

Predeclared interpretation:

- **SUPPORTED, within this frozen setup:** baseline is compatible; the
  intervention produces at least one target-group discharge and linked
  emission; neither negative-control group produces a discharge/emission;
  all changes follow the frozen runtime path and replay is exact.
- **PARTIALLY SUPPORTED:** the intervention changes target `z` accumulation
  or reaches its threshold but no target canonical emission follows, while
  both negative-control groups remain non-crossing; or the target responds
  but one or more drive-limited controls also respond, defeating selectivity.
- **NOT SUPPORTED:** no target-group `z` retention/discharge/emission response
  occurs despite valid, compatible execution.
- **BLOCKED:** provenance, historical baseline compatibility, execution
  determinism, boundedness, or required validation fails. Do not reinterpret
  a blocked run as a scientific negative.

An emission in a no-reception stream is a provenance/input-isolation failure
and blocks interpretation; it is not evidence for or against retention.

## Falsification and prohibited interventions

The hypothesis is refuted or weakened if:

- target streams show no treatment-induced `z` discharge;
- treatment produces no linked canonical emission after the predicted
  discharge;
- drive-limited controls respond as often as the target, weakening the
  selective-mechanism claim;
- a no-reception control receives input or emits, blocking the run as an
  input-isolation/provenance failure;
- a change appears without the declared local retention/discharge path;
- the historical condition fails exact retained compatibility;
- runs differ under identical inputs/configuration, exceed finite bounds, or
  require modified queue order, event budget, threshold, gain, discharge,
  output rule, topology, or input content.

Only `decay_rate_z` may differ between the two conditions. Do not change
`input_gain`, `discharge_quantum`, `z_max`, fast decay, any threshold,
emission/return delay, input amplitude, route delay, noise qualification,
topology, or runtime source. No labels, task outcomes, global statistics,
WEMA variants, gain interventions, candidate growth, or hardware-derived
parameter changes may be included.

## Artifacts, validation, and interpretation boundary

Write only to `experiments/luna53/`, `artifacts/luna53/`,
`tests/test_luna53_*.py`, and
`workflow/handoffs/luna-53-acp0008-destination-retention-20261008.md`.
Retain protocol/configuration before generating outcomes; include exact
execution revision, source/config/input identities, both conditions, all
per-event records, initial/replay and fresh-run identities, validator output,
result classification, SHA-256 digests, and reproduction commands. Never
overwrite or modify Luna-44/45/46/47 artifacts.

The lane must add focused checks for input provenance/reconciliation, exact
baseline compatibility, the frozen recurrence and E2 discharge/emission
linkage, negative controls, deterministic replay, resource limits, and
rejection of changes to any non-intervention parameter. Run the applicable
ACP-0008/E2 and Luna-44/45/46/47 provenance regressions, then the full
repository suite. Record actual pass/fail/skip results, exact artifact hashes,
clean worktree and pushed execution commit. A known skip is acceptable only
if its existing governed platform limitation is identified; failures may not
be waived or hidden.

This contract tests only whether a retained-input integration mechanism can
selectively produce destination discharge/emission in its named diagnostic
class. It does not establish task efficacy, useful prediction, energy benefit,
generalization, architecture adoption, or hardware equivalence. Preserve
Luna-46 **MIXED**, ACP-0008's experimental status, all A01-A15 clauses, and
all historical negative/blocked findings. After publication of execution
evidence, stop for independent Luna-0 review. Luna-53 does not authorize a
successor, integration, or architecture promotion.
