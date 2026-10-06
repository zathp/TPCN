---
name: Luna-45 ACP-0008 Depth-2 Destination Integration Mechanism
description: Compare disabled, default, and calibrated destination integration on the frozen Luna-44 fixture with a frozen calibrated relay on the fixed source-relay-destination route; mechanism only.
---

# Luna-45 — ACP-0008 Depth-2 Destination Integration Mechanism

## Authorization and execution boundary

**Luna-45 — AUTHORIZED / NOT EXECUTED.** Authorization is the **project
owner's** direct directive (2026-10-06) for this bounded mechanism experiment;
Luna-0 only gates, records and reviews it and does not self-authorize or
approve its own result. Execution begins only after the owner approves
publication of this governance update and its authorization revision is
recorded. Baseline: revision `dbb440c763509781ee7ac5e4f2924851dde8e19c` on
branch `copilot/luna45-depth2-destination-integration` (published from
`origin/main`). This contract does not authorize Luna-46, parity work, tuning,
efficacy, or any architecture change. Phase 1 (this governance pass) runs no
experiment.
Before editing or running, read the architecture contract, ACP-0008, ACP-0007,
the Luna-42/43/44 contracts, runners and evidence, the independent Luna-44
review, and
`workflow/handoffs/luna-0-authorization-luna45-depth2-destination-integration-20261006.md`.
Verify the exact authorization revision, branch, clean worktree and baseline
before execution. Publish the owned runner, tests and configuration before
running; capture a non-null execution revision, runner hash, frozen
configuration digest and environment identity. If any required provenance,
gate or interface assumption cannot be verified, stop BLOCKED and return to
Luna-0. Do not retry with altered limits or parameters.

## Objective and falsifiable hypothesis

On the frozen committed Luna-44 fixture, with a relay held at the calibrated
`decay_rate_z=0.0125` in every arm, determine whether destination integration
configuration changes destination integration-mediated emissions. Destination
conditions are exactly:

1. disabled (`integration=None`);
2. default (`IntegrationConfig()`, `decay_rate_z=0.1`);
3. calibrated (`IntegrationConfig(decay_rate_z=0.0125)`).

Hypothesis: destination integration configuration can change destination
integration-mediated emissions under the fixed routed stream. No destination
emission or between-arm difference is guaranteed; a null or negative result is
valid. Counter-hypothesis: destination emissions are identical across arms or
absent. Mechanism only: no classification, accuracy, task efficacy, prediction
benefit, reward/utility, energy benefit or structural-growth claim.

## Frozen fixture (consume; never generate)

Load only the committed `artifacts/luna44-canonical-fixture/fixture.json` and
`provenance.json`. The experiment must not call the spiral generator or the
fixture builder. Verify before any arm runs:

- fixture size `3451453` bytes; file SHA-256
  `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`;
- semantic (canonical) digest
  `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`;
- seeds `0..4`, 64 sequences per seed, 320 sequences, 5,164 ordered points,
  stream IDs `c{seed:02d}-{sequence_index:03d}`;
- complete pinned provenance manifest: path
  `artifacts/luna44-canonical-fixture/provenance.json`, SHA-256
  `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`, Git blob
  `eb9179abae7eed10891e6022832f16735111b220`, manifest revision
  `86e5a2f389af06b06bf04a614edaed88e0847902`, fixture revision
  `6413cffe6982bccc6698af6bebfae51f04e71dd9`, and every source file path,
  revision and SHA-256 recorded in that manifest.

Any mismatch is BLOCKED. Consume only ordered point `x/y/t` (loaded from the
reversible `float.hex` representation). Read no labels, classes, evaluation
data or label-bearing metadata. Compute `float(x) + float(y)` independently per
point, arm and replay as in Luna-44; do not feed the stored audit value.

## Frozen interface and conditions

Use production `MultiExcursionNeuron`, `ExcursionCharacterRuntime` and
`BoundedTopology`. Topology is exactly `source -> relay -> destination`, both
ordinary fixed Model-B edges with delay `1.0`, `w=1.0`, `d=1.0`, `r=0.0`; no
shortcut or return edge; fan-in/out limit 2, edge/routing capacity 3; identical
and static in all arms. Source integration is `None`. Relay integration is the
calibrated `decay_rate_z=0.0125` in all arms, unchanged. Only the destination
integration condition varies. All other ACP-0008 and E1 parameters, thresholds,
delays, bounds and the Luna-44 resource limits (queue 128; runtime event and
activity budgets 1024; neuron event budget 4096; eligibility capacity 1024 per
ledger; prediction capacity 8 / expiry 4.0; settling horizon 4.0) remain at the
reviewed Luna-44 values. Fresh runtime/neuron state per sequence.

## Required gates, measurements and acceptance

Predeclare every check, field, count and digest rule in the runner and tests
before execution. Gates run in order G1 → G2 → G3 → G4; any failed gate stops
the run **BLOCKED** and no destination interpretation is made.

### Float and exactness policy (Luna-44 committed policy; do not invent)

Use exactly the policy predeclared by Luna-44
(`FLOAT_POLICY_FORMULA` and `numerical_policy` in
`run_luna44_acp0008_canonical_fixture_rebaseline.py` and
`workflow/handoffs/luna-0-authorization-luna44-canonical-fixture-rebaseline-20261005.md`):
`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`, applied
only to equation-derived binary64 reconstructions (per-run `x+y`, ordinary
source-emission payload, Model-B routed payload, onward arrival timestamp, and
relay/destination recurrence fields: x/z after decay, x/z after input,
discharge amount, post-discharge x/z), each reported separately with observed,
expected, residual and bound. Everything else is **exact**: raw fixture
identity and bits, point/batch order, event IDs/order, source/destination,
route/path/depth, causal roots and provenance, queue sequence, mode/threshold
and emission classifications, discharge sign, counts, elapsed-time deltas
(exact binary64 subtraction), strict-future causality, same-run payload copies,
hard bounds and replay digests. The tolerance cannot waive any exact check and
no new tolerance or multiplier may be introduced for destination quantities.

### G1 — Historical calibrated Luna-44 upstream gate

Before any destination arm is interpreted, reconcile the Luna-45 calibrated
upstream against the authoritative retained calibrated-arm evidence in
`artifacts/luna44-acp0008-independent-routing-rerun-20261005/` (summary
runner revision `4baab60f87b820db800e04d0eb3277fb0e94f9b3`, fixture revision
`6413cffe6982bccc6698af6bebfae51f04e71dd9`), identifying the exact retained
arm records used. Compare: (a) the fixture identity/digests and per-sequence
raw-input digests; (b) source emissions; (c) `source -> relay` enqueue records
and actual receptions; (d) relay integration state and trajectory and
integrated emissions; (e) `relay -> destination` enqueue records. Discrete
quantities must be exact; floating quantities use only the policy above. If the
retained evidence is missing, ambiguous, or any quantity differs, G1 fails:
**BLOCKED**, no destination interpretation, no tuning or relaxation. This does
not re-adjudicate or rewrite Luna-44 (PASS / SUPPORTED relay propagation;
Luna-42 PASS WITH FOLLOW-UP; Luna-43 BLOCKED / DESTINATION COMPARISON
UNDETERMINED).

### G2 — Cross-arm invariance

Across the three destination arms, for every sequence and in full order, these
must be identical: source emission history; the independently captured
`source -> relay` queue-admission and reception captures; the relay
integration trajectory (z/x before/after decay and input, elapsed time,
discharge); relay emissions; and `relay -> destination` enqueue records; plus
input digests. Any variation is **BLOCKED** (condition isolation failure).

### G3 — Independent route capture and reconciliation (both edges)

Capture two **distinct sites** for each routed event on both edges, retained in
raw form for initial and replay:

- **Queue-side (admission) record:** event ID; source; destination; exact
  payload bits (decimal plus `float.hex`); enqueue time; scheduled/arrival
  time; route, path and depth; causal roots and provenance (including
  `originating_emission_id`, roots_truncated); queue sequence.
- **Receiver-side (actual processing) record**, captured independently where
  the receiver consumes the event: event ID; source; destination; exact payload
  bits; actual reception timestamp; path and depth; provenance; receiver state
  before and after.

Reconcile one-to-one by queue sequence/event identity and report **separately**
the counts: enqueue, reception, matched, unmatched enqueue, unmatched
reception, orphan receptions, duplicate enqueue and duplicate reception, and
mismatches by source, destination, event ID, payload, timing, route/path/depth,
and causal/provenance. Source equality is exact
(`enqueue.source == reception.source`); the retained source-only mutation
regression test (`test_route_reconciliation_rejects_source_mutation_with_details`
or its successor in the Luna-45 tests) must fail reconciliation and must be
run. Every count of unmatched/orphan/duplicate/mismatch must be zero to pass.

### G4 — Bounds and completion

Record and enforce, per arm and per sequence, all configured capacities and
their observed high-water marks: queue capacity 128, runtime event budget and
activity budget 1024, neuron event budget 4096, eligibility capacity 1024 per
ledger, prediction capacity 8 / expiry 4.0, settling horizon 4.0, topology
fan-in/out 2 and edge/routing capacity 3; plus **pending events** at
completion (must be zero at settling, otherwise reported and BLOCKED) and
completion/settling status. Retain every failed, incomplete or
resource-exhausted arm; do not retry with raised limits.

### Destination evidence (after G1–G4 pass)

For every relay emission routed to the destination and every destination
reception, retain: character/stream ID; relay emission ID; route/admission
(queue sequence, enqueue and scheduled times); reception event ID(s); payload
and arrival time; destination fast state before and after decay and after
update; `z` before decay; exact elapsed time; `z` after decay; routed
contribution; `z` after contribution; discharge decision, amount and sign;
resulting `z`; direct versus integration-mediated classification; and the
canonical emission ID when one occurs. **Recompute `z_new` and the discharge
independently from the production equation** (as Luna-44's relay oracle:
`z_decay = z_before*exp(-decay_rate_z*dt)`; integrate only when mode is normal
and `abs(x_input) < theta_e`; discharge `sign(z_input)*theta_z` when
`abs(z_input) >= theta_z` and `x_input*z_input >= 0`) and verify decision,
amount and sign; classification is derived from that independent recomputation
and the actual emission record, never trusted from the neuron's integrated
flag alone. A mismatch is BLOCKED. The disabled arm must show no integration
state or integrated emission.

### Per-arm report

For each arm report: destination receptions; maximum `|z|` (and the sequence,
time and event where reached); direct and integration-mediated emission counts;
unique emitting characters; timing from the preceding relay emission(s) to each
destination emission; and the number of contributing receptions before each
discharge. Report between-arm differences. Retain these values even when there
are no emissions.

### Candidate-opportunity precursor analysis (conditional)

Only if a destination arm has canonical emissions, apply the existing ACP-0007
association semantics unchanged: for an ordered pair of **canonical emitters**
`source canonical emitter -> destination canonical emitter`, with source
emission at `t_s` and destination emission at `t_d`, count a pair only when
`0 < t_d - t_s <= association_window` (the existing ACP-0007 window; equal-time
emissions do not qualify) and no `source -> destination` edge exists. Capture
the exact source canonical emission ID and time and the exact destination
canonical emission ID and time for every pair, plus counts, unique characters
and the ordering. Report these only as **"candidate-opportunity precursors"**.
The relay is not a precursor endpoint. The relay emission stays a required link
in each destination emission's causal chain (see the supported-result
criterion) and its timing is a **separate** metric (relay emission to
destination emission, and canonical source emission to relay emission), not the
association timing. Never instantiate candidates, run the structural
controller or growth, change the window, or imply benefit.

### Outcomes

No accuracy, effect-size or count threshold is invented; a negative result is
valid. Outcomes are evaluated per the rules below and only after the replay
semantics below have been applied.

**Genuine chain.** A destination canonical emission is *genuine
integration-mediated* only if its full chain is independently reconstructable
from retained evidence, with each link verified at its own capture site:

1. canonical source evidence and the canonical source emission;
2. `source -> relay` queue-admission and actual receiver reception;
3. relay retained integration state/trajectory (independently recomputed);
4. relay integration-mediated canonical emission;
5. `relay -> destination` queue-admission;
6. destination reception;
7. destination integration and discharge (independently recomputed `z_new`,
   discharge decision, amount and sign);
8. the destination canonical emission, classified integration-mediated by that
   recomputation and the emission record.

Direct destination emissions (ordinary episodes not produced by an integrated
discharge) never support the primary hypothesis; they must be counted and
reported separately. A destination emission whose chain cannot be reconstructed
is a BLOCKED mandatory failure, not support.

**SUPPORTED / PASS.** All of G1–G4, destination-evidence verification and
replay pass, and at least one genuine integration-mediated destination
canonical emission exists **in the calibrated destination arm
(`DESTINATION_CALIBRATED`, `decay_rate_z=0.0125`)**, because the primary
hypothesis asks whether the frozen calibration supports depth-2 emission. A
genuine emission only in the default arm, or only direct emissions, never
yields SUPPORTED. Report arm-wise emissions and between-arm differences; do not
interpret the difference as efficacy.

**PASS WITH FOLLOW-UP.** The same core support exists (at least one genuine
integration-mediated canonical emission in `DESTINATION_CALIBRATED`), but there are bounded,
non-blocking questions (for example an unexplained but non-contradictory
between-arm pattern or a documented limitation). List each question, why it is
non-blocking and who decides it. It may never be used to excuse a failed gate,
an unreconstructable chain, or a replay failure.

**NOT SUPPORTED IN THIS SETUP.** Permitted only when all gates, destination
evidence verification and replay pass and the calibrated destination arm has
**no** genuine integration-mediated canonical emission, **even if the default
arm (or any other arm) has one**. Report arm-wise emissions and account
explicitly for every case: no destination emission at all, direct-only
destination emissions (counted and reported, not support), or default-arm-only
integrated emissions, together with
maximum `|z|`, timing and contributing-reception evidence. This is a valid,
non-blocked negative result and must not be described as a failure of the
platform or as efficacy evidence.

**BLOCKED.** Any mandatory failure: G1–G4, destination-evidence mismatch or
unreconstructable chain, missing or unverifiable provenance or fixture
identity, resource exhaustion, or an initial/replay blocker (preserved as
specified below).
### Replay semantics and digests

Replay each arm from reset in the same environment after its initial run; replay must pass before any outcome above other than BLOCKED is declared.
Predeclare the digest material: per arm and phase, a canonical UTF-8 JSON
(sorted keys, compact separators) SHA-256 over the fixture and input digests,
frozen configuration, source emissions, both edges' queue-side and
receiver-side captures, relay trajectory and emissions, destination evidence
records (all fields above), per-arm report, bounds high-water marks and pending
counts, and the reconciliation counts — excluding wall-clock times, process
IDs, paths and environment strings. Equality criteria: identical digests, with
discrete content byte-equal and floating content bitwise equal in the same
environment (the float policy is for equation reconstruction, not for replay
equality). Blocker preservation: if the **initial** run is BLOCKED, no replay is
run and no replay or summary digest is produced for that arm or phase; if the
**replay** is BLOCKED or differs after a successful initial run, preserve the
initial artifacts and digest unchanged and record a separate replay blocker
(do not overwrite or discard either).

### Artifact provenance and retention

Publish the owned runner, tests and configuration before running. Record the
authorization revision and handoff digest; fixture revision and digests;
runner revision and file hash; non-null execution revision; configuration
digest; environment; and per-arm, initial and replay artifact digests. Retain
config, results, replay, initial and replay enqueue and reception raw captures,
and summary in a new `artifacts/luna45-…/` directory without overwriting
existing artifacts.

## No-tuning and exclusions (restated)

All of the following remain prohibited: any tuning or sweep of decay,
thresholds, gains, delays, weights, capacities or budgets; relay variation
(relay is `decay_rate_z=0.0125` in every arm); topology change, added edges or
any `source -> destination` edge; ACP-0007 growth, pruning, controller use or
candidate instantiation; fixture generation or edits; efficacy,
classification, prediction, reward, utility or energy claims; Windows/Linux
fixture-parity work; production/ACP/architecture changes; any promotion; and
Luna-46.
## Owned files and exclusions

Own only a new Luna-45 runner, focused tests, a new Luna-45 artifact directory,
and the completed execution handoff
`workflow/handoffs/luna-45-acp0008-depth2-destination-integration-<date>.md`.

Do not change: neuron, runtime, routing, topology, classifier, readout or
production APIs; the fixture, builder, verifier or provenance; ACP-0007 or
ACP-0008; architecture documents; previous runners, tests, artifacts or
handoffs. Do not tune parameters, change topology, instantiate ACP-0007
candidates or growth, claim efficacy, address Windows/Linux fixture-parity, or
authorize Luna-46. ACP-0008 remains experimental, opt-in and unpromoted;
ACP-0007 remains unchanged and disabled.

## Validation environment and return

Run under Python 3.11.5 with process-local overrides
`GIT_CONFIG_COUNT=2`, `GIT_CONFIG_KEY_0=core.autocrlf`,
`GIT_CONFIG_VALUE_0=false`, `GIT_CONFIG_KEY_1=core.eol`,
`GIT_CONFIG_VALUE_1=lf`. Run the new focused tests, applicable ACP-0008,
runtime, routing and Luna-44 regressions, the full suite, and `git diff
--check`. The two known Windows-versus-frozen-Linux fixture materialization
comparisons and the CUDA skip are documented baseline conditions and are not
relaxed; any other failure stops the task and returns to Luna-0. Report exact
commands, revision, environment, counts and artifact digests, classifying each
check as passed, failed, not run or not applicable. Return the handoff to Luna-0
for independent review; do not self-review, claim promotion, or authorize a
successor.
