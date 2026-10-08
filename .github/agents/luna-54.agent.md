# Luna-54 — Relay event-generation and propagation mechanism

## Authorization

**AUTHORIZED / NOT EXECUTED.** This contract authorizes one bounded retained-input
mechanism experiment only. It does not authorize a production change, efficacy
run, architecture change, ACP amendment, parameter promotion, or successor.

- **Task:** `luna-54-relay-temporal-retention-propagation-20261008`
- **Baseline:** `1bee6673ac68e99303d33053e197f41fe78b913f`
- **Decision owner:** Project owner, through Luna-0 scientific selection
- **Executor:** Luna-54
- **Independent review:** Luna-0 after execution

## Scientific question

**HYPOTHESIZED:** In the 75 Luna-46 `DRIVE-LIMITED` streams, changing only
the relay's ACP-0008 `integration.decay_rate_z` from the retained value
`0.0125` to `0.00125` will cause at least one additional relay E2 discharge
and canonical emission with an authenticated, correctly routed destination
reception, compared with the matched historical relay control.

This tests relay-local event generation and propagation over the frozen
relay-to-destination edge. It does not test destination gain, route reliability,
task efficacy, or whether the intervention is useful outside these retained
streams.

**Counter-hypothesis:** The relay-only retention change produces no additional
valid routed relay emissions in the primary 75 streams, or observed differences
cannot be causally traced to authenticated source-to-relay inputs and reproduced.

## Evidence motivating the single intervention

The published Luna-53 destination-retention intervention was independently
reviewed **PASS**, limited to its frozen setup: 19/33 temporal-retention-limited
streams discharged and emitted; 0/75 drive-limited and 0/212 no-reception
streams responded. It does not establish that relay retention has the same
effect.

In retained Luna-45/Luna-46 records:

- The 75 `DRIVE-LIMITED` streams have 676 source-to-relay receptions and 109
  relay emissions, each matched by a destination reception. Every one of the
  676 relay inputs integrates; 567 integration records do not discharge or
  emit at that integration.
- These 75 streams receive 109 destination events in total: 43 streams receive
  one, 30 receive two, and two receive three. All 75 remain below threshold in
  the signed zero-decay oracle; their total absolute drive ranges
  `0.30418816662944315`–`0.9884338239909127`. The retained destination inputs
  do not oppose in sign. This is not destination cancellation or a recorded
  route-loss result.
- The 212 `NO-RECEPTIONS` streams split into 23 with no source-to-relay input
  and 189 with one or more: the latter contain 558 integrated relay inputs but
  no relay emission. These 189 are an upstream-active secondary stratum, not
  assumed negative controls.
- The 14 Luna-53 temporal-retention-limited streams not rescued at destination
  decay `0.00125` each receive three same-sign destination events; all three
  integrate and their zero-decay oracle crosses. Preserve this subgroup as a
  separate secondary stratum; do not relabel it as drive-limited.

The evidence localizes a testable relay event-generation bottleneck, but does
not prove that relay decay is its cause. Individual non-emitting events are
integration observations, not structural candidate rejections. No structural
plasticity, candidate admission, or topology change is tested.

## Frozen inputs and conditions

Use the exact Luna-45 calibrated depth-two source/relay/destination records
and authenticated event-route captures retained at baseline
`1bee6673ac68e99303d33053e197f41fe78b913f`:

- `artifacts/luna45-acp0008-depth2-destination-integration-20261006/initial-destination_calibrated.json`
  Git blob `701dace35f1ca511cbb7275a2d5dd9737964aed7`
- `artifacts/luna45-acp0008-depth2-destination-integration-20261006/replay-destination_calibrated.json`
  Git blob `83014b8c0cc3be014b3831051237c552c87bead6`
- `artifacts/luna45-acp0008-depth2-destination-integration-20261006/initial-destination_calibrated-reception.json`
  Git blob `b0f7965894c89ab3655a583ccd2db6486e4e3966`
- `artifacts/luna45-acp0008-depth2-destination-integration-20261006/replay-destination_calibrated-reception.json`
  Git blob `bb1af6d2b3853581c03fd10556e437d5eb555e5a`
- `artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json`
  Git blob `b1aaef4006422f321922bfb58425e4fb646d96b9`
- `artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`
  canonical SHA-256
  `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e`
- `artifacts/luna53/summary.json`
  Git blob `b03993adfb358c575c80f6637e7b50903061ddb2`

Verify evidence against immutable Git blobs and each repository-declared
integrity record. On Windows, treat only the documented exact LF-to-CRLF
checkout materialization as equivalent; do not normalize numerical or event
evidence or weaken any exact integrity check.

Run one matched control and one intervention, each in fresh deterministic
initial and replay executions (four executions total):

1. **Control:** frozen Luna-45 calibrated source, relay (`decay_rate_z=0.0125`),
   destination (`decay_rate_z=0.0125`), topology, edge weights, delays, event
   ordering and reset behavior.
2. **Intervention:** identical except relay
   `integration.decay_rate_z=0.00125`. Do not change destination decay or any
   other configuration field.

Inject only the authenticated retained source-to-relay reception records into
the relay E2 runtime. Do not rerun the source network, regenerate inputs, or
replay relay outputs as inputs. Route newly generated relay canonical emissions
over the unchanged relay-to-destination edge; process the destination normally
and stop at destination output. Preserve exact times, phase/event identities,
payload bits, queue order, lineage, enqueues, and receptions.

## Groups and measurements

Keep original Luna-46 labels and stream identities downstream-only. Runtime
inputs must not include group labels or any post-run statistic.

- **Primary:** all 75 `DRIVE-LIMITED` streams. Report per-stream and aggregate
  relay input integrations, state/discharge/emission events, newly matched
  relay-to-destination enqueues/receptions, destination integration and
  discharge/emission, and treatment-minus-control route counts. The primary
  response is an additional valid relay canonical emission that is enqueued
  and received at the destination, with complete causal lineage.
- **Secondary, separately reported:** 189 original `NO-RECEPTIONS` streams
  that have source-to-relay inputs; 23 original `NO-RECEPTIONS` streams with
  zero source-to-relay inputs; all 33 `TEMPORAL-RETENTION-LIMITED` streams,
  preserving the 19 Luna-53 responders and 14 nonresponders. Do not pool these
  with the primary target or silently change their labels.
- **Full compatibility population:** all 320 streams, including all 1,715
  source-to-relay and 235 relay-to-destination control pairs per phase.

Exact canonical event lineage is required; an integration-threshold crossing
without canonical emission and a relay emission without destination reception
do not count as the primary response. Record admissions/integrations separately
from discharges, emissions, enqueue success, and reception. Preserve all
negative and unexpected outcomes.

## Boundedness, controls and decision rule

Inherit the frozen Luna-45 execution bounds: 320 streams per phase; queue
capacity 128; runtime event budget 1,024; per-neuron event budget 4,096;
empty per-stream runtime/neuron reset; existing exact event-time and settling
rules. No sweep, extra condition, gain/threshold/input/topology change,
training, structural adaptation, or task run.

Before interpreting treatment:

1. Verify every input/event/raw capture against its pinned source identity.
2. Reconcile all 1,715 retained source-to-relay input records per phase to
   their authenticated historical route pairs without rerunning the source.
   Reproduce the full 320-stream historical relay-to-destination control
   exactly, including all 235 route pairs, original destination traces, and
   target-group counts of 676 relay inputs and 109 relay emissions/receptions.
3. Verify the independent initial/replay control digests and exact same-condition
   initial/replay treatment digests. Reconcile every enqueue/reception pair.
4. Confirm the 23 no-source-to-relay-input controls have no relay discharge,
   canonical emission, or downstream reception. Any such output is an
   isolation failure, not a positive result.
5. Confirm finite event/resource bounds and report any overflow, clipping,
   truncation, invalid lineage, or recurrence mismatch explicitly.

**SUPPORTED within this frozen mechanism setup** only if at least one primary
stream has a reproducible treatment-minus-control increase in relay E2
discharges that produce canonical emissions, are correctly routed, and are
received at the destination with authenticated input lineage, while all
integrity, control-compatibility, no-input-isolation, boundedness, and replay
gates pass. Otherwise the primary hypothesis is **NOT SUPPORTED** or
**INCONCLUSIVE** as appropriate; explain gate failures. Secondary-only
responses do not satisfy the primary criterion and must be reported as such.
No numerical efficacy threshold is implied.

## Boundaries and handoff

- **Architecture:** no A01–A15 amendment and no ACP. Use existing event-time
  local integration and bounded E2 execution. ACP-0008 stays experimental,
  opt-in and disabled by default; `0.00125` is not a production default.
- **Not authorized:** destination-gain retest, event qualification/gain/
  threshold sweeps, general efficacy, production changes, hardware equivalence,
  architecture promotion, Luna-55 or any other successor.
- Preserve Luna-46 `MIXED`, Luna-53's reviewed result and all historical
  evidence. Do not claim that the relay intervention diagnoses every
  no-reception stream or establishes task utility.
- Record exact code, protocol, verifier, evidence Git blobs, environment,
  execution revision, per-phase digests and actual tests in the Luna-54
  execution handoff. No execution has occurred under this authorization.
- After the bounded run, stop for independent Luna-0 review. That review is the
  next assignment; do not self-promote or launch another experiment.
