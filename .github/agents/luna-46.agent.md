---
name: Luna-46 Offline Depth-Scaling Diagnostic
description: Diagnose signed drive, cancellation, and temporal retention from reconciled frozen Luna-44/Luna-45 evidence without changing production computation.
---

# Luna-46 - Offline Depth-Scaling Diagnostic

## Authorization and identity

**AUTHORIZED / NOT EXECUTED.** The project owner's exact specification,
forwarded in the same-task correction of 2026-10-06, authorizes only this
bounded offline diagnostic. Commit A is governance only. Baseline:
`d1f901d3d995dc013f22dd086ae1ed8ffd28293d`; branch:
`copilot/luna46-depth-scaling-diagnostic`. The authorization revision is the
commit introducing this contract and
[authorization handoff](../../workflow/handoffs/luna-0-authorization-luna46-depth-scaling-diagnostic-20261006.md).
Resolve and retain that exact commit identity before later code or analysis.
This is not a later independent review and does not authorize Luna-47.

Classification before code work: **OFFLINE ANALYSIS / MECHANISM DIAGNOSTIC /
VERIFICATION**, not a production neuron, tuning experiment, efficacy study,
or architecture promotion. Hypothesis: second-hop non-crossing reflects
temporal-retention loss. Counter-hypothesis: insufficient signed drive or
cancellation explains non-crossing even without decay. Mixed and negative
results are valid; classifications below, not this hypothesis, decide verdicts.

Read the actual `workflow/` architecture contract/changelog, workflow,
acceptance criteria, proposal README/template, handoff template, this contract,
ACP-0007/0008, and Luna-42 through Luna-45 handoffs and corrective evidence.
Preserve Luna-42 **PASS WITH FOLLOW-UP**, Luna-43 **BLOCKED / DESTINATION
COMPARISON UNDETERMINED**, Luna-44's reviewed canonical-fixture
relay-propagation baseline, and Luna-45 **NOT SUPPORTED IN THIS SETUP**.
Do not reopen or reinterpret Luna-45. ACP-0007 stays unchanged/disabled;
ACP-0008 stays experimental, opt-in, unpromoted. No A01-A15 or ACP change:
A07 permits downstream offline statistics; none may feed computation.
No hardware equivalence, energy benefit, prediction benefit, or efficacy claim.

## Prerequisite gates and retained-only input

The merged corrective review `5ebc9ae7dcaae7ff45f0769686885dcae3f2dea4`
is an ancestor of baseline. It verifies retained-provenance-only ancestry,
canonical replay byte equality and no blocking review findings. Current
baseline tests: Luna-45 focused 75 passed; existing regression 348 passed,
2 known failures; full 1164 passed, 2 known failures, 1 CUDA skip.
The two Windows-versus-frozen-Linux fixture comparisons remain failed
(exit 1), separately accepted baseline exceptions, never relaxed or hidden.
There were no new failures. Whitespace checks passed. These gates precede
authorization; a new failure blocks later work.

Use retained raw emissions, enqueues, successful receptions, trajectory,
configuration, and integrity/provenance evidence from:

- `artifacts/luna45-acp0008-depth2-destination-integration-20261006/`
  (22 catalogued files, including calibrated initial/replay enqueue/reception);
- `artifacts/luna44-acp0008-independent-routing-rerun-20261005/`
  for the fair first-hop comparison;
- `artifacts/luna45-corrective-verification-20261006-r1/verification.json`.

Check hashes/lengths, revisions, frozen configuration/fixture identity,
catalog coverage, and initial/replay identities before interpretation.
Do not generate inputs or infer missing raw events from temporal proximity.
For each sequence use only successful actual destination receptions,
independently reconciled one-to-one against raw `relay -> destination`
enqueues by event/queue identity, endpoints, payload bits, and timestamp.
Preserve retained deterministic order and exact provenance; duplicate,
missing, orphan, mutated or truncated evidence is BLOCKED, never dropped.
Use the calibrated destination stream; preserve other arms without changing
them. Verify initial/replay analytical outputs deterministically.

Retained evidence is the first choice. Only if it proves insufficient for a
required observation may the later worker use observation-only capture of
the unchanged frozen experiment. Record the precise missing field and reason
first; keep all parameters, configuration, inputs, topology, seeds, bounds,
resets, and event semantics identical and prove capture non-interference.
No alternate run or changed production configuration is permitted. This
Commit A executes neither retained analysis nor observation-only capture.

## Signed oracles and exact partition

Reset `z=0` and `z0=0` per character. For signed retained routed payload `u_i`
at successful retained arrival `t_i`, use exact retained prior timestamps:

```text
dt_i = t_i - t_(i-1)
z_i = exp(-0.0125 * dt_i) * z_(i-1) + u_i
z0_i = z0_(i-1) + u_i
tau = 1 / 0.0125 = 80
theta_Z = 1.0
```

Validate tau and unchanged threshold/configuration. Compare reconstructed
actual state to the retained Luna-45 trajectory at corresponding boundaries.
Respect the retained prior update timestamp, including intervening events;
do not invent a first-arrival interval or silently skip production updates.
Any inability to reconcile recurrence/trajectory boundaries is BLOCKED.
Distinguish pre/post-decay, input, and any recorded clipping/discharge
boundaries; the formula is not permission to remove actual production
semantics. Report actual crossings as such, not as a production change.
The zero-decay accumulator has discharge disabled **only offline**, keeps
signed prefixes, and never replaces the actual recurrence or neuron.

Inherit exactly
`64 * sys.float_info.epsilon * max(1, abs(observed), abs(expected))`
for equation-derived reconstruction comparisons, retaining observed,
expected, residual and bound. Raw bits, copied values, timestamps/elapsed
subtraction, identity/order/provenance, discrete classification and replay
bytes/digests remain exact. No threshold tolerance: crossing is `abs(z)>=1`
at the canonical integration threshold boundary, not an efficacy or emission
claim. Do not round a near-crossing up or use absolute-value accumulation as
a substitute for signed evidence.

Partition every sequence, with the following priority:

1. **NO-RECEPTIONS:** zero successful receptions; count these but exclude
   them from mechanism-category fractions.
2. **ALREADY-CROSSING:** actual recurrence crosses; this has priority over
   all remaining reception-bearing categories.
3. **TEMPORAL-RETENTION-LIMITED:** actual never crosses, but at least one
   signed zero-decay prefix satisfies `abs(z0_i)>=1`.
4. **CANCELLATION-LIMITED:** zero-decay never crosses, but
   `sum(abs(u_i))>=1`.
5. **DRIVE-LIMITED:** `sum(abs(u_i))<1` and neither oracle crosses.

Record threshold boundaries and category rationale per sequence. An empty
denominator or incomplete evidence cannot yield a support verdict.

## Predeclared measurements

Keep per-sequence identities and full signed reception order. Report counts,
category fractions, actual and zero-decay signed extrema and maximum absolute
state, total absolute routed magnitude, and first crossing where applicable.
Report aligned constructive input versus opposing-sign input using the
pre-input signed state as the reference, with zero-reference cases separate.
For opposing-sign cancellation record the cancelled magnitude
`min(abs(pre_input_state), abs(u_i))` separately from sign reversal/overshoot;
never conflate it with decay loss.

Report retained fraction `rho_i=exp(-0.0125*dt_i)` per interval, with explicit
zero-state/zero-denominator policies for any aggregate retention ratio.
Signed decay loss is `z_previous-z_pre_input`; absolute loss is
`abs(z_previous)-abs(z_pre_input)` at the reconciled decay boundary.
Keep signed and absolute summaries separate, and include constructive
same-sign run lengths (zero inputs separately identified; no invented sign).

Arrival-gap distributions must include zero ties. Also report positive-gap
count, mean, median, percentiles and maximum; predeclare the percentile
estimator and requested levels in tests before analysis. Empty/singleton
gap sets are explicit, not fabricated zeros. Compare gaps and run durations
to tau=80 using the same retained logical-time units.
Any critical-rate estimate is offline only and allowed only when
mathematically unique under the declared signed equation/domain; state that
domain and prove uniqueness. Non-monotone signed cases, absent roots and
multiple roots must be reported without forcing an estimate. No rate sweep
or configuration recommendation is authorized.

Compare matched Luna-44 calibrated `source -> relay` and Luna-45 calibrated
`relay -> destination` streams where fair: pin common fixture/sequence/reset,
phase and capture semantics, and disclose differences in frequency, gaps,
payload distributions, signs and same-sign runs. Do not assert identical
layer statistics or treat upstream and downstream as equal exposure.
If fair comparison is unavailable, report the limitation, not a fabricated
depth comparison or an alternate experiment.

## Broad verdicts (fixed before analysis)

Let `N` be the reception-bearing sequence count, `R` the retention-limited
count, and `D` the combined drive-limited plus cancellation-limited count.
Keep already-crossing in N and disclose it separately.
`substantial = ceil(0.25*N)`; `material = ceil(0.10*N)`.

- **SUPPORTS TEMPORAL-RETENTION BOTTLENECK:** `R >= substantial` and
  `D < material`.
- **SUPPORTS DRIVE/CANCELLATION BOTTLENECK:** `D >= ceil(0.75*N)` and
  `R < material`.
- **MIXED:** any other complete/reconciled dataset, including when both
  R and D reach material and otherwise any valid split satisfying neither
  support rule.
- **BLOCKED:** insufficient/corrupt evidence, recurrence mismatch, or
  missing required raw inputs. N=0 is insufficient mechanism evidence.

Publish counts/fractions and cutoff integers alongside verdict. Do not
silently change cutoffs, exclude unfavorable sequences, or claim efficacy.

## Later implementation ownership and acceptance

Commit A owns only this agent contract, the authorization handoff,
`workflow/docs/luna/LUNA_WORKFLOW.md`, and `workflow/ARCHITECTURE_CHANGELOG.md`.
No code, tests, artifacts, retained analysis, or science in Commit A.
Later Luna-46 work is bounded to a new offline diagnostic, its focused tests,
new diagnostic output, and execution handoff; no historical files may be
mutated. Predeclare paths, schema, metric definitions, capacities, and
provenance before code, then retain code/configuration/execution revision,
environment, input hashes and deterministic output digests. Bound processing
to the retained sequence/event inventory and surface malformed inputs.

Before retained interpretation, focused synthetic tests must cover:

- each category and priority, exact threshold equality and near-boundary
  non-crossing, signed cancellation versus absolute drive, zero/singleton
  receptions, reset isolation, and denominator policies;
- closed-form decay, exact lambda/tau/threshold, zero-decay signed prefixes,
  same-time ties/order, prior timestamps/intervening updates, recurrence
  tolerance boundaries without threshold tolerance;
- retention, signed/absolute decay loss, constructive alignment,
  cancellation/overshoot, sign/zero runs, timing and percentile edge cases;
- unique versus non-unique/non-monotone/absent critical-rate cases;
- exact verdict cutoff boundaries, already-crossing inclusion, N=0,
  both-material and residual MIXED cases;
- missing/extra/duplicate/orphan/mutated/truncated raw captures, source and
  endpoint changes, payload/timestamp-bit changes, catalog corruption,
  one-to-one reconciliation and retained-provenance-only ancestry;
- fair/missing first-hop comparison, deterministic replay and canonical byte
  equality, raw-artifact immutability, labels excluded and downstream-only
  operation; capture ON/OFF non-interference if capture is necessary.

Retained integrity checks are required in addition to synthetic analytical
tests. Report passed/failed/not-run/not-applicable separately; new failures
block interpretation. Return evidence to Luna-0 for later review without
self-approval. No promotion or successor follows automatically.

## Absolute exclusions

No tuning, parameter changes/sweeps, alternate configurations or changed
production configuration. No WEMA, ACP-0008/core/neuron/runtime/routing/
topology/fixture changes; no ACP-0007 growth/pruning; no fixture generation,
Luna-45 reopening, efficacy claim, architecture promotion, hardware claim,
or Luna-47 authorization. If this scope cannot answer the diagnostic,
return the precise limitation rather than repairing or expanding it.
