---
name: Luna-42 ACP-0008 Corrective Calibration Replication
description: Correct Luna-41's fixture and provenance contract, then rerun the same bounded ACP-0008 Phase A and gated Phase B without expanding its calibration search.
---

# Luna-42 — ACP-0008 Corrective Calibration Replication

## Authorization, dependency and baseline

Luna-42 is **AUTHORIZED / NOT EXECUTED** by
`workflow/handoffs/luna-0-acp0008-corrective-calibration-decision-20261005.md`.
Begin implementation only from the exact published revision recorded there.
Before any experiment run, publish the owned runner/tests/configuration as a
commit, fetch `origin`, and start execution only from clean synchronized
`main` at that runner commit (`HEAD == origin/main`). That committed runner
revision is the non-null `execution_revision` for the experiment. Capture
the execution commit and runner identity before starting the run. Do not
execute from an uncommitted runner. This agent contract is not permission to
execute during the Luna-0 governance pass.

Read this contract, the prior Luna-41 execution and independent review,
ACP-0008, ACP-0007, the Luna-0 calibration authorization, Luna-38/39
contracts and reviews, the Luna-40 report, and the current neuron/runtime/
topology interfaces. Luna-42 is a corrective replication, not a new
calibration search. It may correct only stimulus/provenance specification
and the explicitly defined numerical comparison policy below. It must not
change ACP-0008 equations, ACP-0007, production APIs, thresholds, timing
requirements, topology, resource bounds, or the candidate set.

If an existing production interface cannot express the fixture as written,
or if provenance cannot be established, stop **BLOCKED**. Do not repair
production code or invent a substitute stimulus.

## Objective and fixed candidate set

Repeat Luna-41's task-independent calibration using a causal, production-
generated source stimulus. Determine whether any of the same four
`decay_rate_z` values meets the same near/far temporal selectivity
requirements when actual routed values produced by the ordinary source and
Model-B edge are used as the relay contributions. If Phase A validly selects
a candidate, freeze it and run the already specified descriptive Phase B.

Test exactly, in order:

`0.1, 0.05, 0.025, 0.0125`

Change only `IntegrationConfig.decay_rate_z` in the enabled relay. Keep
`theta_E=1.0`, `theta_Z=1.0`, `input_gain=1.0`, `z_max=4.0`, and fast
`decay_rate=1.0`. Keep ACP-0007 disabled. Use no optimizer, additional
candidate, fallback, post-hoc selection, or task-informed decision. Apply
the Luna-41 selection rule unchanged: select the **largest**
`decay_rate_z` whose every Phase-A fixture passes.

## Causal Phase-A stimulus and route contract

Each fixture/candidate uses fresh source and relay neurons, a fresh bounded
event queue, and the unchanged `source -> relay` Model-B edge:
`delay=1.0`, `w=1.0`, `d=1.0`, `r=0.0`; fan-in/out, edge, routing and queue
bounds remain those of Luna-41 (queue capacity 64, processed-event limit
64, and each neuron event budget 64).

The source neuron is an ordinary production `MultiExcursionNeuron` with
`E1Config(decay_rate=1.0, theta_e=1.0, event_budget=64,
integration=None)` and otherwise unchanged defaults. The only external
stimulus value is the predeclared binary64 value represented by the JSON
number `1.6945957207744073` (negative mirror: its negation), derived before
execution from `4 * atanh(0.4)`. Schedule positive/negative inputs at the
unchanged local times:

| Fixture | Source input timestamps |
|---|---|
| ISOLATED | `0.0` |
| NEAR_PAIR | `0.0, 12.9` |
| NEAR_TRIPLE | `0.0, 12.9, 25.8` |
| FAR_TRIPLE | `0.0, 51.6, 103.2` |
| NEGATIVE_NEAR_TRIPLE | `0.0, 12.9, 25.8` |
| INTEGRATION_DISABLED | `0.0, 12.9, 25.8` |

Use negative source stimulus for `NEGATIVE_NEAR_TRIPLE`; all other fixtures
are positive. The disabled control uses relay
`E1Config(..., integration=None)`. All other relay arms use their fixed
ACP-0008 parameters and the candidate decay rate.

Do **not** inject, synthesize, replace, or require a hand-authored relay
payload of exactly `+/-0.4`. That decimal is only the nominal normalization
anchor for the isolated source fixture. The relay input is exclusively the
payload produced by the production path:

`declared source stimulus/config`
`-> source canonical emission`
`-> ordinary BoundedTopology Model-B transform`
`-> queued routed event`
`-> relay reception`.

Retain and reconcile every link, including source input event id/time/value,
source configuration, source canonical emission id/time/payload, edge
parameters, routed payload/id/time, and destination reception id/time/value.
Never call relay `receive_event` with a payload other than the queued
production-routed event. Source emission count must equal the scheduled
source input count for each fixture; canonical identities must be unique,
and each route/reception must reconcile one-to-one with its source emission.

The actual routed payloads may differ slightly across repeated near-spaced
source events because source fast state is persistent. This is part of the
frozen production stimulus, not a failure or a quantity to normalize away.
Recompute the recurrence oracle using each actual routed payload and its
actual relay-arrival timestamp. The measured `z` must not be used to invent
or alter routed inputs.

## Numerical comparison policy

Keep discrete/categorical acceptance criteria exact: candidate values and
selected candidate; event count and one-to-one event identities; fixture
schedule; emission count; integration/direct/none classification; event
ordering; route path; signs; control enablement; and replay identity/digest.
Compare declared source timestamps to their configured binary64 values
exactly. Compare a routed event and the matching relay reception payload
exactly because routing forwards the same computed float value. Replay
records and canonical digests must match exactly on the same execution
environment.

For independent floating-point equation checks (Model-B transform, source
ordinary-emission amplitude formula, ACP-0008 recurrence, analytic oracle,
and neutral-state bound), use this predeclared absolute error bound:

`tol(a, b) = 64 * sys.float_info.epsilon * max(1.0, abs(a), abs(b))`

This is a conservative binary64 rounding budget for the small fixed
sequence of multiplication, elementary-function, addition, clipping and
subtraction operations used by the source/edge/neuron equations. It is
defined from machine epsilon and operand scale before execution, not fitted
to Luna-41 observations. Record Python/platform identity, `sys.float_info`,
the computed tolerance rule, and each maximum residual. No separate
undocumented tolerance is permitted. This floating tolerance does not relax
any exact discrete criterion or allow a relay input to be replaced by an
ideal decimal.

For each recurrence step independently compute, from the **observed routed
event**:

`z_decay = z_previous * exp(-decay_rate_z * elapsed)`
`z_input = clip(z_decay + input_gain * routed_payload, -z_max, z_max)`

Integrate only when the unchanged ACP-0008 production conditions hold. Apply
the unchanged one-quantum signed discharge condition, then compare all
recorded decay/input/discharge/post-discharge state fields using the stated
floating-point tolerance. The oracle is a consistency check; it does not
alter candidates or selection.

## Phase-A criteria

Execute and retain all six fixtures for every candidate. Preserve exact
discrete criteria from Luna-41:

1. **ISOLATED:** one routed reception; no relay canonical emission.
2. **NEAR_PAIR:** two routed receptions at the configured spacing; no relay
   canonical emission.
3. **NEAR_TRIPLE:** three routed receptions at near spacing; exactly one
   integration-mediated relay canonical emission after the third reception;
   no direct emission.
4. **FAR_TRIPLE:** three routed receptions at far spacing; no relay
   canonical emission.
5. **NEGATIVE_NEAR_TRIPLE:** three negative routed receptions; exactly one
   negative integration-mediated relay emission; no direct emission.
6. **INTEGRATION_DISABLED:** the same positive near-triple source fixture
   with `integration=None`; no relay canonical emission and no slow-state
   trace/state.

For every enabled fixture, compare each production-trace state step with the
actual-input oracle under the numerical policy above; require `|z| <= 4.0`
exactly against the declared hard state bound; at most one discharge per
external event; correct polarity; and causal prior receptions for every
emission. Reconcile output amplitude with the unchanged ordinary emission
rule using the specified floating tolerance.

After at least `10 * tau_z` since the final routed input or discharge, issue
one public zero-valued relay input to force local-time decay. It is not
evidence. Require exactly one probe, `|z| < 1e-4`, and no canonical emission
at or after the probe. Use the same procedure for each enabled arm.

Run every Phase-A fixture/candidate record twice from reset. Require exact
serialized record and digest equality. Preserve all failures. If any source
stimulus fails to generate the required count of canonical emissions, if
event/reception reconciliation fails, if any control emits unexpectedly,
if equation/discrete/bound/replay checks fail, or if provenance is absent,
stop **BLOCKED**. Do not change stimulus, candidate, tolerance, timing or
limits to obtain a pass.

## Analytic prediction and candidate selection

Before examining any Phase-A outcome, record the frozen candidate set,
source fixture, equation, timing, thresholds, selection rule and predicted
threshold-crossing pattern. The prior ideal-input analysis predicts only
`0.0125` crosses on a three-input near triple. This is a hypothesis, not
acceptance evidence. Recompute the recurrence and predicted crossings from
the production-routed payloads retained for each fixture. Preserve both
the pre-execution prediction and the observed-actual-input oracle result.

Select only from normalized Phase-A controls using the largest-passing-rate
rule above. Phase B may not readjust, reselect, or replace the selection.
If no candidate passes, write the Phase-A freeze with null selection and do
not create or consume Phase-B streams.

## Freeze and gated Phase B

Before creating or reading any Phase-B sequence, persist and hash the full
Phase-A records, replay identities, selected candidate (or null), frozen
parameters, numerical policy, and configuration. The freeze must verify
against the saved artifact before any Phase-B helper is invoked.

Only if all Phase-A criteria pass and one candidate is selected may Phase B
run. Reuse Luna-41's fixed unlabeled stream protocol, sequence order, seeds
`0..4`, five-by-64 character sequences, fresh per-character neurons, and
resource bounds. Use the existing topology
`source -> relay -> destination`; both edges have `delay=1.0`, `w=1.0`,
`d=1.0`, `r=0.0`, fan-in/out limits 2, edge/routing capacity 3. Keep queue
capacity 128, runtime event budget 1024, max activity events 1024, neuron
event budget 4096, settling horizon 4.0, prediction capacity 8/expiry 4.0,
eligibility capacity 1024 per ledger and neutral reward 0.0.

Compare paired calibrated, default (`decay_rate_z=0.1`), and
integration-disabled relay arms on identical points and ordering. Read only
timestamps and point coordinates; labels/classes/task outcomes may not
enter inputs, records used for selection, or configuration. ACP-0007 remains
disabled. Source and destination remain integration-disabled. All routes
use production `BoundedTopology` and its existing fixed-`w=1` edge. Record
source emissions, routed relay payloads/receptions, relay `z`, direct and
integrated relay emissions, and any `relay -> destination` transfer with
event identity, timestamp, route and ordinary Model-B payload. Destination
emission is not required.

Phase B is descriptive. No emission is a valid negative outcome, not
permission to tune. Replay the complete paired Phase-B design from reset and
require exact record/digest equality. Any resource, causality, provenance, or
replay stop condition is reported without retry or bound increase.

## Provenance and artifact requirements

At execution startup, before experiment work or artifact creation:

1. Verify `HEAD == origin/main`, the required authorized starting revision,
   branch `main`, and a clean worktree (excluding only documented ignored
   caches). The required execution revision is the published commit that
   contains the exact runner, tests, and frozen configuration. If those
   files are not yet committed, publish them first and begin a new clean
   execution from that synchronized commit.
2. Record the non-null `git rev-parse HEAD` execution revision and confirm
   the runner is tracked by that commit.
3. Compute and record SHA-256 of the exact runner file and frozen config.

If any check cannot be made, record the reason and stop **BLOCKED**; a null
execution revision is never acceptable evidence. Keep the execution revision,
runner SHA-256, config digest, Python/platform/float identity, artifact digest,
Phase-A and (if reached) Phase-B replay digest in every primary JSON artifact
(`config.json`, Phase-A freeze, `results.json`, and `summary.json`) and the
handoff. The config digest is computed over the frozen configuration object
without its provenance envelope; the envelope records the execution revision,
runner hash and config digest. Verify HEAD and runner hash have not changed
before Phase-B stream creation and at completion. The deterministic replay
identity includes the candidate outcomes, frozen selection, state trajectories,
emission identities, route records and controls.

Define each artifact digest over canonical serialized artifact content with
its own digest field omitted; record the schema/canonicalization and hash
algorithm (SHA-256). The configuration digest hashes the complete frozen
configuration. Record both per-artifact digests and the aggregate run digest
so no self-referential hash is required.

## Scope, exclusions and handoff

Own only:

- `run_luna42_acp0008_corrective_calibration.py`
- `tests/test_luna42_acp0008_corrective_calibration.py`
- `artifacts/luna42-acp0008-corrective-calibration/`
- `workflow/handoffs/luna-42-acp0008-corrective-calibration-20261005.md`

No production/neuron/topology edits, ACP change, Architecture Contract
amendment, WEMA implementation, candidate expansion, threshold or time
change, task efficacy, structural growth, edge learning, promotion, hardware
equivalence, or biological-realism claim is authorized. Do not edit Luna-41
or prior historical evidence. ACP-0008 remains experimental, opt-in and
unpromoted; ACP-0007 remains unchanged and disabled.

Report exact baseline/execution revisions; checksums and digests; source
fixture configuration and each causal emission/route/reception; pre-execution
and actual-input analytic predictions; exact and floating-point criteria;
all candidate/fixture outcomes; selection proof; freeze-before-Phase-B
evidence; boundedness, neutral return and replay; Phase-B relay/onward-route
observations if reached; tests and limitations. Distinguish passed, failed,
not-run and not-applicable checks. Stop with **BLOCKED** rather than
reinterpreting a failed gate. Run the Luna-42 focused tests, the full
repository suite, and `git diff --check`; report exact counts and skip
reasons. Return results to Luna-0 for independent review.
