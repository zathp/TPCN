# Luna-47F predeclared replay protocol (2026-10-06)

Authorization: `789dda5988daf72f375d9713bd76a6da2b9e8b34`.
Production/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
This protocol and implementation must be committed before outcome generation.
No TPCN runner, topology controller, fixture generator or production module is
imported. No edges are instantiated, admitted, removed, ranked or simulated.

## Identity, hypothesis and scope

Luna-47F, replay-only fan-in/shortcut candidate-generation diagnostic.
Hypothesis: compatible earlier-to-later causal changes offer nonduplicate
shortening/fan-in proposals. Counter-hypothesis: only existing routes, incompatible
changes, unavailable local information or no useful downstream activity exist.
The scientific hypothesis is not presumed true. A01-A04, A07, A08 and A14
are preserved, not amended. There is no ACP or hardware equivalence claim.

Read-only inputs: Luna-45 calibrated initial/replay phase, enqueue/reception,
configuration, integrity catalog and summary, canonical Luna-44 fixture/provenance,
and corrected Luna-46 output. The Luna-46 MIXED verdict is preserved. Older
Luna-12I/J/K/M/N handoffs inform interpretation only; historical TANH_LEGACY
efficacy/candidate totals are not pooled with EXCURSION_V1. No other lane is used.
Every consumed input is pinned to its baseline Git blob and working-byte SHA-256.

Pre-outcome provenance correction: the first execution attempt stopped at the
input gate (no scoring/output) because Git materialized LF JSON as CRLF.
Published bytes are therefore read directly from the baseline Git blob, checked
against the retained catalog/internal digests. Working bytes must equal that
blob **exactly**, or its exact LF-to-CRLF checkout transform with no other
changes. Record both byte lengths/hashes and the materialization classification.
No source file is rewritten, and no numeric value or trace identity is normalized.
This correction changes provenance handling only, not any scoring rule.

## Rules fixed before scoring

Time is retained logical time (no conversion to seconds). Reset per stream,
320 streams, at most 4096 routes/stream and 100 MiB/input. Association window
is **0 < target time - source time <= 4.0**, taken from retained Luna-45's
precursor window, not optimized. Equal-time/reverse pairs are excluded.
Two nonzero finite scalar deltas are compatible iff signs agree and
`min(abs(a), abs(b))/max(abs(a), abs(b)) >= 0.5`. Zero, opposing signs and
ratios below 0.5 remain rejected rows. No tolerance on windows/sign/ratio.
Equation reconciliation uses 64 binary64 epsilons times max(1, magnitudes).
Copied timestamps, event identities, payload bits, roots, route paths and
queue identities must be exact.

Two **separate**, nonpooled families:

1. `output-drive-proxy`: earlier node's canonical emitted signed payload
   versus later node's retained routed input. These share signed drive units
   but are **not** two intrinsic state deltas. Enumerate each actual direct
   route and each source->destination two-hop **trigger chain**.
2. `local-deposition`: earlier relay reception's `input_value` versus later
   destination reception's `input_value`, checked against
   `x_after_input-x_after_decay`. This isolates the event's local deposition
   from decay/discharge. Enumerate exact relay trigger -> destination chains.
   Source-local pre/post state deltas are absent: source->destination
   intrinsic-state compatibility is explicitly BLOCKED, not replaced by
   source point values, audit x+y, labels or invented states.

Two-hop identity is destination reception -> actual relay emission ->
retained relay `integration_trace_check.event_id` -> actual source->relay
reception -> actual source emission. The integration trace's emission id,
timestamp and input, and trajectory event identity, must independently match.
This proves the *trigger*, not exclusive/all contributing ancestry.
Truncated causal roots remain flagged; exact trigger identity does not expand
or repair bounded roots. Same node/cross-character pairs are forbidden.

Every enumerated observation pair (including rejected ones) is a machine-readable
row with endpoint, event, timestamp, JSON-pointer identity, deltas, similarity,
causal chain and classifications. A compatible in-window pair is an opportunity,
not a reachable/admitted edge. Candidate time is the later observation time.
Repeated endpoint proposals are counted within stream/family; static-edge
duplicates are separately counted. Neither repetition nor duplicates are removed.

## Graph and capacity classification (offline only)

Use only immutable retained fixed graph and static limits, checked against every
stream's resource fields. Duplicate iff the edge already exists; cycle-forming
iff target already reaches source (self-pairs excluded). Saturation checks
source fan-out, target fan-in, global edges and routing slots independently.
Do not consume hypothetical capacity across proposals. Missing limits yield
BLOCKED/null, never zero. A novel edge with an existing path length H>1 has
analytical **hop reduction H-1**; no graph is constructed to compute it.
Actual path delay is reported separately. New-edge delay/delay reduction are
BLOCKED because none is configured/admitted. Fan-in opportunity requires
nonduplicate endpoints and another existing incoming source; capacity-feasible
opportunities are separately counted. These are not created motifs.
A07 source-local availability of a downstream observation is BLOCKED: no
return observation-delivery channel is retained. Global replay is permitted
evaluation, not a deployable local policy.

## Specificity, downstream association and verdict

Report lag distribution, candidate times, lag bands (0,4] and (4,8], compatible
causal pairs outside the window, reverse-order exclusions, and same-stream
noncausal temporal coincidences. Coincidences are controls, never proposals.
No timestamp is shuffled or synthesized. Fixed route delays make lag specificity
largely mechanical; no statistical superiority over random growth is claimed.

Useful downstream *activity proxy* = exact trigger-linked canonical target
emission after its reception, within the same 4-unit window. Input deposition/
state change is reported separately and is not called useful emission. Task
utility, prediction-error improvement and efficacy are BLOCKED/not evaluated.
Downstream emission is an association with actual retained activity, not a
counterfactual benefit of the proposed edge.

Verdict for this bounded diagnostic:
- SUPPORTED only if at least one nonduplicate, capacity-feasible shortening/
  fan-in opportunity has exact downstream-emission association AND documented
  source-local observation availability.
- PARTIALLY SUPPORTED if any compatible nonduplicate capacity-feasible
  shortening/fan-in **proxy** opportunity exists, but the stronger gates fail.
- NOT SUPPORTED if scoring is valid but no such opportunity exists.
- BLOCKED if identity/delta/capacity evidence prevents the proxy scoring itself.

Metrics requiring intrinsic source deltas, local delivery, prospective delays
or utility stay explicitly BLOCKED even if the proxy verdict is partial.
Count-only positivity is not efficacy.

## Non-mutation, verification, publication and stop

Hash every tracked file outside the four owned scopes before/after replay;
retain per-file pre/post hashes plus aggregate digest. Check non-owned Git diff
against authorization and baseline artifact pins. Fixed output location is
`artifacts/luna47f/diagnostic.json`, no overwrite without `--check` (read-only).
Reject symlink/junction/reparse-point components and existing output.
Residual filesystem replacement races are not claimed solved.

Unit fixtures are explicitly synthetic tests, never retained evidence. Assert
determinism, strict causal direction, duplicate/cycle/saturation/repetition,
null missing-capacity behavior, roots limits, signature/identity failures and
non-mutation. After protocol commit, execute initial/replay analyses and compare
canonical bytes, run focused and applicable Luna-12/38/44/45/46/runtime/topology
regressions without suppressing baseline failures. Retain commands/environment.
Publish code, tests, rows, hashes, results and completed handoff on the isolated
branch, verify clean remote parity and stop for independent Luna-0 review.
