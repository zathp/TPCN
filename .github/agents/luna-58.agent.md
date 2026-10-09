---
name: Luna-58 Finite Destination Retention Rescue
description: Test one predeclared finite destination-retention rate against the six Luna-55 RR nonresponders.
---

# Luna-58 — Finite Destination Retention Rescue

## Authorization

**AUTHORIZED / NOT EXECUTED.** This is one bounded ACP-0008 mechanism
experiment, not a task-efficacy study, production recommendation, architecture
change, or hardware-equivalence claim. Execute only from a clean checkout after
this contract is published on `origin/main`.

Authorization baseline: `c6adc71c26f6226bcbbfb442c4c22cb11cdb3cd2`.
Read the architecture contract, changelog, workflow, acceptance criteria,
handoff template, Luna-55 contract and execution handoff, Luna-55 selection
handoff, and this contract before implementation. Luna-55 remains PARTIALLY
SUPPORTED within its frozen setup; its six nonresponders are not relabeled as
failures of the architecture.

## Question and hypothesis

**Question:** With the complete causal Luna-55 source-to-relay-to-destination
E2 path and the relay held at `decay_rate_z=0.00125`, does one predeclared
finite destination rate of `decay_rate_z=0.00001` produce an actual destination
threshold crossing in each of the six fixed Luna-55 RR nonresponders, without
changing the relay event stream or creating crossings in the frozen
zero-decay-insufficient/no-input controls?

**Hypothesis:** The six streams have same-sign RR destination inputs and no
prior destination discharge, reset, refractory interval, or clipping. Their
actual E2 recurrence under zero decay would cross `discharge_quantum=1` on
their final (third) input. For each retained RR sequence, the largest
finite decay rate that still crosses ranges from
`1.986455531354e-05` to `1.072304228834e-04`; the limiting stream is
`c00-011`. The single predeclared rate `1e-5`, derived offline as approximately
half the strictest boundary, is predicted to cross all six with at least
`0.000617681984` threshold surplus.

**Counter-hypothesis:** One or more of the six fails to cross under actual E2
at the predeclared rate, or their source/relay route changes; alternatively a
frozen negative-control group crosses. Any such result falsifies the
predeclared selective-rescue prediction for this setup. Do not tune the rate
after observing the experiment.

This is not evidence that nonresponders had a larger *absolute* decay loss:
their absolute loss overlaps the responders' range and is lower for several
streams. The discriminator is their much smaller decay-free headroom
(`0.001245–0.009489` versus `0.291600–0.378256` for responders). Their finite
decay loss (`0.072087–0.131705`) exceeds that headroom. The timing/gap,
retention-ratio, and decay-loss ranges overlap between groups.

## Frozen inputs and provenance

Use the Luna-55 frozen 320-stream population, with the 16 predeclared primary
streams unchanged. Authenticate source inputs, the selection, and the retained
RR initial/replay artifacts by their Git objects at the authorization
baseline, then validate their embedded scientific digests:

| Input | Git blob at authorization baseline | SHA-256 |
|---|---|---|
| `experiments/luna55/config.json` | `197ebd8efc5449e1e973d4c6d96bdf12f40e1f31` | `103594c2906fafb60684fc4f67adf22ffc0722eb268506e9d35d027bd98fcbba` |
| `artifacts/luna54/intervention-initial.json` | `6de22f1f5406f378e115a818e01e459ec6ddf3e6` | `62b4fe16da456a37ffe7014d495ce1e74ddad174bd853e1656a40256eee7b702` |
| `artifacts/luna54/intervention-replay.json` | `684fc1f3adfbd26dbbca1a656c1d14c5e8ac92a8` | `d7c3d69f9a6f184517eb465393eb6ace57e9210ef27a8cd5e8a5c52e1fb57bc4` |
| `artifacts/luna55-selection/post-luna54-destination-oracle.json` | `a63a5edddd6f24b2625192b398b74a84125b97bb` | `2ac7b79015c00d5055b1b6226ce23239f691ba07a368e80768737e39f0b2bd57` |
| `artifacts/luna55/rr-initial.json` | `b29e76709a6d502ee8f48aa4e4ea4f31fa9388ca` | `2043a03744af925345a34ee3e7e704914c35f13faf1e9175bab9c9e600ad8b8b` |
| `artifacts/luna55/rr-replay.json` | `61baf5aa4c42a0c518d0c0fbf91e110acd8fe987` | `7445773d6907488501a90d97064ebece57ccb9b0508b75df3f54fbe9a0555085` |
| `artifacts/luna55/summary-v3.json` | `063b03ea84933f930ce95b2fe15e8ee83e0e4172` | `5f1bba890f00c117a019dccf39948ec9b2169579f3ce749c81c03edfd85a3f86` |

The RR records' configuration digest is
`d99b31646791f37e9242dfb9089e299dc6ab31e21bc0f96b244e92a6f4bed708`.
Their source-input phase digest is
`d73c99d83847b50bb5cb66920b95c3546d818874f582b6b6d9d8c5bfa90aaa3b`;
the pinned Luna-54 intervention initial/replay records have common scientific
digest `4170a2688438a2f86a7b9c907d86efff006309ecdc5bf57e14011d6a5033ed54`.
Their reported execution worktree was dirty; do not claim the recorded
execution revision alone identifies a clean runner. Use current committed
code and the authenticated fixed input objects above. Preserve all historical
Luna-45/46/53/54/55 evidence and hashes.

## Authorized implementation ownership

Luna-58 may add or edit only:

- `experiments/luna58/run.py` and `experiments/luna58/config.json`
- `tests/test_luna58_finite_destination_retention.py`
- New result files under `artifacts/luna58/`
- One execution handoff under `workflow/handoffs/`
- This contract and the Luna workflow/changelog authorization records

No edits to `tpcn/`, the ACP-0008 contract, Luna-55 runner/tests/config,
historical source or result artifacts, the frozen selection, labels, or other
experiment runners are authorized. Do not change threshold, gain, payloads,
timestamps, source data, topology, relay configuration, route rules, neuron
model, or runtime budgets.

## Intervention and controls

- Run the unchanged causal source-to-relay-to-destination E2 event path for
  all 320 streams. Do not inject retained destination arrivals directly.
- The intervention changes exactly one field from Luna-55 RR:
  destination `integration.decay_rate_z: 0.00125 -> 0.00001`.
- Keep relay `integration.decay_rate_z=0.00125`; destination and relay
  `input_gain=1.0`, `discharge_quantum=1.0`, `z_max=4.0`, all other neuron
  parameters, and all runtime bounds remain unchanged.
- Compare with the retained RR condition. Require identical source inputs,
  relay canonical emissions, and complete route signatures at the destination
  for each stream, including event ID, payload bits, timestamp, source, and
  destination. Any upstream/route mismatch invalidates the retention-only
  interpretation.
- Primary targets, in frozen order:
  `c00-011, c00-032, c00-037, c01-012, c01-020, c01-041, c01-050,
  c02-010, c02-015, c02-019, c02-023, c02-046, c03-023, c03-058,
  c04-001, c04-043`.
  The six predicted rescues are
  `c00-011, c00-037, c01-020, c02-015, c02-023, c02-046`.
- Keep the ten existing RR responders as positive controls. Keep E+ (49),
  E0 (10), NR1 (189), and NR0 (23) as separate negative/control populations;
  do not merge strata or use their labels as runtime inputs. Report the
  33-stream secondary temporal-retention stratum separately.
- Run fresh bounded initial and deterministic replay phases. They verify
  reproducibility and are not independent samples.

## Execution bounds and required measurements

Preserve the Luna-55 bounds: 320 streams per phase, queue capacity 128,
runtime event budget 1,024, per-neuron event budget 4,096, and settling
horizon 4.0. Retain all source-input, route, destination-reception, integration,
discharge, state-bound, clipping, pending-queue, event-budget, and replay
records. Report source inputs, relay emissions, destination receptions,
pre/post-input `z`, elapsed time, signed payload, first threshold-crossing
time, discharge/reset/refractory transitions, and route reconciliation per
stream and in each separate stratum.

Acceptance requires:

1. Input identities and the sole changed configuration field match this
   contract; the runner is label-blind.
2. All 421 baseline RR route signatures per phase reconcile exactly with the
   unchanged source/relay path. All 16 primary target routes must have complete
   root expansion and zero truncation; the seven inherited off-target relay
   root-truncation flags in the authenticated RR baseline must match exactly,
   with no new truncation. No clipping, pending events, or bound failures are
   permitted.
3. Both deterministic phases match exactly for the same condition.
4. All six primary nonresponders cross under actual E2 in the intervention;
   all ten RR responders continue to cross. Record observed first-crossing
   times, not the unreset arithmetic peak after a crossing.
5. E+, E0, NR1 and NR0 remain without new destination crossings. Report
   secondary-stratum outcomes separately without using them to broaden the
   primary result.
6. Required Luna-58 tests and the full repository test suite pass from the
   committed implementation state. Confirm all protected historical files
   remain unchanged.

A missed primary crossing, a new crossing in any specified negative control,
route/input drift, provenance failure, nondeterminism, clipping, pending work,
or any failed runtime bound blocks a supported rescue claim. Report failures;
do not silently repair, tune, or widen the experiment.

## Architecture and interpretation boundary

Preserve A01-A15. The runtime remains event-driven and uses local elapsed
time, not a global neural timestep; evaluation strata and labels remain
downstream-only. Bounded propagation, state, and event budgets remain intact.
ACP-0008 remains experimental, opt-in, and disabled by default. No ACP or
architecture contract change is authorized. This experiment cannot establish
task efficacy, generalization, production suitability, calibrated physical
energy, hardware equivalence, or an architecture promotion.

Stop after the Luna-58 handoff for independent read-only Luna-0 review. Do not
authorize Luna-59 or another parameter search.
