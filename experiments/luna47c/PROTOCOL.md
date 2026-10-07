# Luna-47C frozen protocol, v1 — pre-outcome

This document, implementation and tests must be committed before scoring.
Authorization 789dda5988daf72f375d9713bd76a6da2b9e8b34; production/evidence
baseline 2cef8ea4b37a4ae586e3f383511cba63c9268ddc. No other lane consumed.
Mechanism only, no production semantics, accumulator, topology, ACP or efficacy.

## Hypothesis and counter-hypothesis

An unbounded-observation adaptive envelope can inflate after a meaningful
spike and suppress later meaningful events. Clipping its target to twice its
prior envelope should reduce that failure, but may under-track larger noise
and fail on clustered signals. Neither adaptive method is presumed superior.

## Exact mechanism and frozen configuration

Three methods: fixed, adaptive, robust. All start/reset B=0, N=0.25, no last
timestamp. Input is only (timestamp, raw); evaluator truth never enters it.
Strictly increasing finite nonnegative timestamps, finite raw in [-16,16].
Time unit is arbitrary synthetic event time. First dt=1, thereafter actual
elapsed timestamp; no global tick or idle processing.

At arrival, r=raw-B, band=2N, E=sign(r)*max(|r|-band,0).
Qualification uses prior state, strict crossing, no tolerance or subtraction
of truth. Signed zero is not admitted. E is an excitation **value only**;
it is not stored or accumulated or routed to a neuron.

After qualification: B'=clip(B+(1-exp(-dt/20))*clip(r,-.25,.25),-4,4).
Fixed N'=.25. Adaptive target=|r|. Robust target=min(|r|,2N).
N'=clip(N+(1-exp(-dt/4))*(target-N),.05,16).
Use binary64 expm1 for coefficients. Identical baseline tracker across methods
isolates noise estimator effects. All parameters finite positive; at most four
slots (immutable config, B, N, last timestamp), no history in the mechanism.
The evaluator retains finite outputs separately: 16 fixtures x 3 methods x
240 events, with matched signal-free controls (23,040 event records total).
No learning, data-fitting, parameter search or cross-fixture retention.

## Generation, ground truth and reset

fixtures.py is the authoritative generator. No RNG or external dataset.
240 events per fixture, cyclic intervals (1,.5,1.5,.75); all dyadic event times.
Noise cycle (-.2,.1,-.1,.2,0,.15,-.15,0). Eight families, each with an exact
sign-negated mirror, and fresh qualifier per fixture/method/control:

* stationary: noise only, zero baseline;
* drift: baseline .8*clamp((index-40)/120,0,1), noise only;
* isolated: injected +8 at 60, -8 at 120, +8 at 180;
* clustered: +1.2 at 60..67, -1.2 at 140..147;
* mixed_signs: alternating +1.2/-1.2 at 60..79;
* near_boundary: .49,.50,.51,-.49,-.50,-.51 at 60,80,100,120,140,160;
  noise zero at these six events;
* contamination_chain: no noise, +8 at 60, +.9 at 61,62,64,68;
* noise_step: noise amplitude multiplied by four at 60..159, no real signal.

Only nonzero injected source signal is meaningful, regardless of its amplitude
or whether a method admits it. False admissions include all other events.
This deliberately makes near-band signals difficult; do not redefine truth to
match an estimator. The mirror negates baseline, noise and injected signal,
not time. Signal-free control removes only injection, preserving times,
baseline and noise; it runs independently and never affects the test mechanism.
Fixture hashes cover inputs **and** evaluator truth using canonical sorted-key
compact JSON UTF-8 plus LF. Event traces include B,N,band,raw,E,post-state,dt,time.

## Metrics and numerical comparisons (before interpretation)

For every fixture/method:

* false admissions: nonzero E on zero injected source; misses: zero E on
  nonzero injected source. Count wrong signs separately.
* baseline error: mean/max |B_before - true baseline|;
* baseline pull: max |B_after - signal-free B_after|;
* noise contamination: max(0,max(N_after - signal-free N_after));
  also report max absolute difference. No-signal fixtures have zero paired
  contamination by construction, not proof of an accurate noise estimate.
* recovery: after last meaningful event, first five consecutive events with
  both paired |B difference| and |N difference| <= .025. Report start/confirmation
  index and elapsed time from last meaningful event. No recovery in the finite
  window is right-censored; no signal is not-applicable. This is incremental
  contamination recovery, not a noise-tracking accuracy guarantee.
* positive/negative meaningful, missed and wrong-sign counts; mirrored maximum
  error in B,B_after,N,N_after,E, absolute tolerance 1e-12.

Same-environment canonical replay bytes and integer counts must match exactly.
Cross-platform arithmetic comparison tolerance is absolute 1e-12, not a promise
of byte identity across Python/libm versions. Threshold comparisons remain strict.
Recovery tolerance .025 is a separate, fixed scientific criterion.

Explicit failure-chain gate: adaptive post-spike N exceeds control by >.5,
at least one later .9 is missed, and all later signals would cross their matched
signal-free control thresholds. Robust protection: fewer later misses and
post-spike N < one-quarter adaptive post-spike N. Sign gate: all mirrors
within 1e-12. Universal gate: no false admissions or misses in any method/run.

Verdict: NOT SUPPORTED if failure chain or sign gate fails; SUPPORTED if robust
protection and universal gate pass; PARTIALLY SUPPORTED if robust protection
passes but universal gate fails; otherwise NOT SUPPORTED. BLOCKED only if
execution/provenance cannot be completed. This is support for isolated
qualification mechanisms, not efficacy or architecture promotion. No aggregate
ranking or winner selection. Preserve all tradeoffs and failures.

## Evidence, validation, review boundary

Emit replay.json (full fixtures/truth, method configuration, tested/control
events, per-run metrics, mirrors/gates, revision/environment/source hashes),
summary.json and manifest.json. Repeat same-process and fresh-process replay.
Reject dirty implementation/test publication and overwrite of replay.json.
Source hashes normalize LF for checkout portability; artifact hashes are actual
bytes. Focused tests: fixture coverage/truth isolation, deterministic replay,
bounded state/reset/time validation, exact formulas, sign symmetry and explicit
contamination chain. Applicable regression: event runtime, neuron, excursion
and topology boundary tests. Full suite attempted; retain platform failures
without weakening assertions. No output-path override or production input.

A01/A02: event-local scalar tracker, no shared clock; A07: truth isolated;
A08: explicit state/input/event bounds; A15: software experiment only, no
hardware validation/equivalence. No A-clause departure or ACP proposed.
Luna-46 MIXED is preserved and is context, not input or tuning evidence.
Push owned paths with completed handoff, stop for independent Luna-0 review.
