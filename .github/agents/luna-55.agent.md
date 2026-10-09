---
name: Luna-55 ACP-0008 Serial Retention Composition
description: Test whether independently supported relay and destination retention combine to produce selective destination discharge.
---

# Luna-55 — ACP-0008 Serial Relay/Destination Retention Composition

## Authorization

**AUTHORIZED / NOT EXECUTED.** This is one bounded, opt-in factorial
mechanism experiment. It tests the serial composition of the independently
supported Luna-54 relay-retention mechanism and Luna-53 destination-retention
mechanism. It is not task efficacy, production integration, architecture
promotion, hardware validation, or a change to canonical semantics.

Governance baseline: `d75ede92f90e7ba1e14f935eccbc26e3c326b8da`
(Luna-54 independent-review publication). Execute only after this contract is
published on `origin/main`. Record the exact execution base and per-phase
runner/source identities. Do not amend ACP-0008 or A01-A15.

Read the current architecture contract, acceptance criteria, workflow,
changelog, ACP process/template, handoff template, ACP-0008, and the Luna-53,
Luna-54, and Luna-46 contracts and retained evidence. Relevant boundaries are
A01-A03, A07-A08, and A15. ACP-0008 remains experimental, opt-in, and disabled
by default.

## Read-only selection result

The selection artifact
[`post-luna54-destination-oracle.json`](../../artifacts/luna55-selection/post-luna54-destination-oracle.json)
records per-stream values from authenticated Luna-54 control/intervention
replays. It does not change or regenerate any historical artifact.

On the 75 historical `DRIVE-LIMITED` streams:

- Luna-54 relay retention produced 78 additional destination arrivals in
  65/75 streams; historical/intervention destination crossings were 0/75.
- Applying Luna-46's signed zero-decay oracle to the exact Luna-54
  intervention arrivals gives 16/65 responders with a threshold crossing and
  49/65 without one.
- The 16 oracle-crossing streams are:
  `c00-011`, `c00-032`, `c00-037`, `c01-012`, `c01-020`, `c01-041`,
  `c01-050`, `c02-010`, `c02-015`, `c02-019`, `c02-023`, `c02-046`,
  `c03-023`, `c03-058`, `c04-001`, and `c04-043`.
- None of the 65 intervention arrival sequences has opposing-sign inputs.
  The zero-decay threshold margins in the 16 target streams range from
  `-0.3782564622628033` to `-0.0012446151850729`; their historical and
  Luna-54 actual margins remain positive.
- The 10 streams without additional primary arrivals remain distinct.
  None crosses the zero-decay oracle.

This selects a narrow composition question. It does not imply that finite
destination retention will reproduce every zero-decay crossing. The 49
zero-decay-noncrossing responders remain a separate total-drive-limited
negative-control group.

The no-reception strata also remain separate:

- `NR0`: 23 streams with zero source-to-relay input remain silent and receive
  no destination event.
- `NR1`: 189 upstream-active streams include 58 streams with 65 new
  Luna-54 destination arrivals. None crosses under zero decay; 54 response
  streams have complete roots and four retain root-truncation metadata.
- The 33 historical `TEMPORAL-RETENTION-LIMITED` streams are a separate
  secondary stratum, not part of the Luna-55 primary target.

The historical Luna-46 classifications are unchanged. These post-Luna-54
partitions are downstream-only evaluator strata and must not enter runtime
computation.

## Hypothesis and causal question

**Hypothesis:** On the 16 predeclared `DRIVE-LIMITED` streams whose exact
Luna-54 relay-retention destination arrivals cross the signed zero-decay
oracle, the relay-only retention change and destination-only retention change
are serially sufficient to produce at least one causal destination discharge
and linked canonical emission when composed, while neither single-retention
arm discharges those target streams.

The causal uncertainty is whether the additional relay-generated events have
sufficient signed drive for the destination only when temporal loss is also
reduced at the destination. A zero-decay crossing is an oracle prediction,
not evidence that the finite `0.00125` intervention will cross.

**Counter-hypothesis:** The target streams do not discharge under the
composed finite-retention condition, or the composed response is not distinct
from a single-mechanism arm, lacks causal route lineage, or is not selective
against the predeclared zero-decay-insufficient and no-event-supply controls.

## Frozen evidence and factorial conditions

Use the authenticated Luna-45 source-to-relay events pinned by the Luna-54
records. Preserve all 320 stream identities, source event identities,
payload bits, timestamps, ordering, reset boundaries, topology, route,
thresholds, and resource limits. Do not regenerate the Luna-44 fixture or
source data.

The factorial factors are only the two existing ACP-0008
`IntegrationConfig.decay_rate_z` values:

| Arm | Relay `decay_rate_z` | Destination `decay_rate_z` | Evidence |
|---|---:|---:|---|
| Historical / historical (HH) | `0.0125` | `0.0125` | Luna-54 control initial/replay |
| Relay retention only (RH) | `0.00125` | `0.0125` | Luna-54 intervention initial/replay |
| Destination retention only (HR) | `0.0125` | `0.00125` | Luna-53 intervention initial/replay |
| Composed (RR) | `0.00125` | `0.00125` | Execute two fresh deterministic phases under this contract |

The retained Luna-53 destination-only arm may supply HR only after execution
preflight verifies, for both initial and replay phases, exact per-stream
arrival identity/order, event IDs, payload bits, timestamps, endpoints,
destination configuration except for the declared decay value, and
destination recurrence compatibility with Luna-54 HH. The read-only
selection verified the replay arms: all 320 streams and 235 arrivals match
in order and bits, and all 235 historical destination trace values match
exactly; the pinned E2 neuron/event-runtime sources and destination
configuration also match. Repeat these checks for both phase artifacts before
reuse. If any check fails, do not combine those records as a factorial arm;
run a complete matched four-arm factorial using one frozen runner/source set
or stop and return to Luna-0.

All other parameters remain exactly as pinned by Luna-45/Luna-54, including
`input_gain=1.0`, `discharge_quantum=1.0`, `z_max=4.0`, `theta_e=1.0`,
`theta_m=4.0`, fast decay, delays, event budgets, and routing. No gain,
threshold, payload, amplitude, topology, or timing changes are authorized.
This is a fixed 2x2 mechanism comparison, not a parameter sweep.

The composed RR arm must execute the complete existing bounded E2
source-to-relay-to-destination path from the exact retained inputs. Use fresh
runtime/neuron state per stream and condition, deterministic initial/replay
phases, and the existing event-time ordering. Never inject the Luna-54
destination arrivals into RR: they are an oracle/input-compatibility
reference, while RR must regenerate its own relay arrivals causally.

Record each arm/phase's exact runner revision, source blobs, configuration
digest, artifact digest, and phase-specific execution identity. Do not use
one aggregate runner revision as a substitute for the identities of distinct
phases. Preserve the Luna-54 pre-treatment blocked runner attempt as a
pre-treatment failure, not as a scientific control.

## Predeclared populations

Primary target, `n=16`: exactly the stream IDs enumerated above. Membership is
fixed by the committed read-only Luna-55 selection artifact. The runtime
receives no class labels, target flags, oracle outputs, or post-run statistics.

Keep these negative-control strata separate:

1. `E+` total-drive-limited: the other 49 of the 65 Luna-54 primary arrival
   responders, whose exact intervention arrivals remain below threshold at
   zero decay.
2. `E0`: the 10 remaining Luna-46 `DRIVE-LIMITED` streams with no additional
   Luna-54 destination arrival.
3. `NR1`: all 189 upstream-active/no-historical-reception streams, with the
   58 arrival responders and 131 no-event-supply streams reported separately.
4. `NR0`: all 23 streams with no source-to-relay input.

Report the 33 historical `TEMPORAL-RETENTION-LIMITED` streams separately as
a secondary reference; do not merge them into the primary target or use them
to redefine historical classifications.

## Measurements and falsification

For every stream and arm, retain the exact source inputs, relay emissions,
destination enqueue/reception pairs, payload bits, timestamps/order, causal
roots/truncation, runtime/state traces, discharges, canonical emissions, and
resource counters. Report by arm and stream:

- destination threshold crossings, discharges, canonical emissions, and
  margins;
- relay event counts and exact route identities;
- for all primary streams, historical/Luna-54/zero-decay reference arrival
  counts, signed and absolute drive, positive/negative contributions,
  per-arm peak state, and threshold margins;
- exact recurrence, replay, configuration-isolation, input-lineage, route,
  reset, and resource-bound results.

The primary endpoint is a destination ACP-0008 integration discharge with a
linked canonical E2 emission and complete causal roots. A relay discharge,
emission, or successful destination reception alone is not a destination
response.

**Narrow composition support requires all of the following:**

1. At least one of the 16 target streams has a complete-lineage destination
   discharge and linked canonical emission in RR.
2. No target stream responds in HH, RH, or HR; otherwise the effect is not
   attributable specifically to serial composition.
3. None of the 49 zero-decay-noncrossing E+ controls, 10 E0 streams, 189 NR1
   streams, or 23 NR0 streams crosses in RR. Retain NR1 response/no-response
   subgroups separately.
4. Relay output identities and destination arrivals are invariant between
   RH and RR; destination-only retention must not alter upstream relay
   generation or route identity.
5. Both repetitions, recurrence audits, route reconciliation, bounds, and
   source/configuration gates pass.

Report the exact response count out of 16 and per-stream factorial contrasts;
do not promote one-or-more-stream support into a general population claim.
If RR has no qualifying target response, the finite serial-composition
hypothesis is not supported in this setup. If target responses occur in a
single-retention arm, the serial-interaction claim is falsified or
undetermined. Any response in a zero-decay-insufficient/no-input control,
unexpected route/output mutation, or incomplete causal root blocks the
selective composition claim.

## Verification and interpretation boundaries

- Authenticate source artifacts and Git-object pins; do not alter historical
  Luna-44 through Luna-54 artifacts.
- Reproduce HH compatibility before interpreting RR. Reconcile every routed
  event one-to-one by identity, endpoints, payload bits, time, order, and
  lineage.
- Run the historical-rate and destination zero-decay recurrence audits with
  the Luna-46 signed-prefix semantics. The oracle is read-only and must never
  be passed to the neuron/runtime.
- Confirm the only changes are the two declared `decay_rate_z` settings and
  that destination-only changes leave relay emissions/routes identical.
- Run independent initial/replay phases; require exact same-condition
  reproducibility, empty pending queues, no clipping, and all queue/runtime/
  per-neuron event limits respected.
- Run focused Luna-55 plus relevant Luna-53/Luna-54/Luna-46/E2 regressions,
  then the full repository suite. Preserve failures and governed skips
  explicitly; do not claim a pass if any test failed.

No task classification, prediction efficacy, reward/learning, utility,
production suitability, parameter optimality, hardware equivalence, or
architecture promotion is measured or authorized. No A01-A15 clause or
ACP-0008 text changes. No Luna-56 or further successor is authorized by this
contract; stop for independent Luna-0 review.
