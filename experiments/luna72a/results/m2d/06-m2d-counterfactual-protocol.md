# Luna-72A-M2D Counterfactual Protocol

## Status, estimand and interpretation

**Proposed only.** No M2D condition has been implemented, run, tested, or
profiled. This protocol asks whether event-driven B emissions alter X's
standalone E1 state enough to produce an X excursion delivered to D in one
fixed acyclic B-X-D fixture.

Primary estimand: change in X's event-time state trajectory, X ordinary
emission count/timestamp, and the matching X-origin D arrival under matched
conditions with B input present versus removed and with the B-X route blocked.
The predeclared meaningful effect is **one X emission and its matching D
receipt in P, versus zero in both N and C**, with X's recorded second-arrival
state at or above `theta_E=0.5`, below `theta_M=4`, and complete B-root
contributor provenance. This is a mechanism result for this exact fixture
only; it is not one-to-one relay, task efficacy, resource qualification, or
R4 comparability.

## Frozen trial environment

Use the E1 configurations, static edges, source revision, IDs, event horizon,
and bounds in `03-m2d-harness-design.md` and
`05-m2d-resource-lifecycle-contract.md`. No random decisions are needed; still
record a fixed protocol seed `0` and `randomness_used=false`. For each
condition/replay, instantiate fresh B/X/D neurons, same frozen configurations,
same edge descriptor identities, empty queue, zero initial states, local
clocks at zero, and empty provenance. No learning, reward, prediction/error,
topology adaptation, ACP-0008 state, or condition labels enter a neuron.

Primary conditions contain **no independent X input and no D input**. X's
state can change only from B-X event arrivals; D can change only from X-D
event arrivals. The independent-X positive-control arm is separately tagged
and is never used as an input in P/N/C/T/O.

Root event identities and input schedule ordinals are frozen. Removing a
root naturally changes subsequent queue sequence values; do not add dummy
events to equalize them. Record actual sequence/dispatch order. Exact queue
and trace equality is required between replays of the same condition, not
between different counterfactuals.

All B roots and I's X roots are external numeric `EventType.INPUT` events
with stable stimulus slots (`B-1`, `B-2`, `X-1`, `X-2`). The event/root IDs
are condition-scoped and repeat exactly in that condition's replay; matching
arms retain the same stimulus slot to document the intervention. No root
event is injected into D. A root starts with no E1 lineage; E1 creates its
own episode/lineage when an ordinary excursion is admitted.

## Conditions and exact proposed stimuli

All numeric values below are proposed deterministic stimulus values, not
observations. A future owner-approved protocol artifact must freeze these
bytes before a workload. If exact source arithmetic fails the stated margins,
stop and request a new owner disposition; do not tune from a run.

| Arm | B external root events | X external root events | Route intervention | Required interpretation |
|---|---|---|---|---|
| **P — B present** | `+1.1 @ t=0.0`, `+1.1 @ t=2.0` | none | B-X and X-D enabled | B emits twice; the two individually subthreshold B-X contributions combine at X to cross 0.5; X emits once and D receives that X emission. |
| **N — B removed** | none | none | B-X and X-D enabled | No upstream route event; X and D remain quiescent. This is the root-removal counterfactual. |
| **C — B-X disabled** | Same B stimulus slots/payloads/times as P; IDs are scoped to C | none | Exclude only X from B's topology route; retain fixed edge descriptors and X-D | B's two local emissions still occur; a blocked-route decision is recorded without inventing a transfer/arrival; X and D remain quiescent. This tests edge necessity. |
| **I — independent X positive control** | none | `+0.2683 @ t=0.6`, `+0.3025 @ t=2.6` | X-D enabled | X independently crosses its threshold and D receives an X-origin excursion. Its roots are X-local and cannot be called B-mediated. |
| **T — non-crossing control** | `+1.1 @ t=0.0` only | none | B-X and X-D enabled | B emits once and X receives one approximately `+0.2683` contribution, but X stays below 0.5 and emits nothing; D receives nothing. |
| **O+ — same-sign comparator** | `+1.1 @ t=0.0`, `+1.2 @ t=2.0` | none | B-X and X-D enabled | Two positive contributions combine at X and cross 0.5. This is paired with O- at the same times and equal second-input magnitude. |
| **O- — signed-opposition control** | `+1.1 @ t=0.0`, `-1.2 @ t=2.0` | none | B-X and X-D enabled | B emits a negative second excursion; the negative X contribution opposes the decayed first positive contribution, leaving X below threshold with no X emission/D receipt. |
| **R — replay** | Exact repeat of each arm | Exact repeat of each arm | Identical per arm | Re-run each arm from fresh identical state/config/queue and require exact same-arm canonical trace. |

All exogenous timestamps are distinct from due internal event times at the
same destination; no same-time tie is required for the primary fixture. A
separate unit test must check the current same-destination equal-time
external-before-internal queue rule. If a future harness encounters an
unplanned tie, it fails the fixture rather than selecting an undocumented
order.

## Analytic state checks (not execution evidence)

The E1 ordinary-output amplitude is
`A_min + (A_max-A_min)*clip((m_peak-theta_E)/(theta_M-theta_E),0,1)`.
For B's first input, this gives `0.275` at the frozen B parameters. Its
ordinary return event is scheduled using E1's analytic local return; at
`t=2`, the residual B state plus the second input produces a second positive
emission near `0.312`. The edge transform with `w=1,d=1,r=0` is `tanh(a)`,
so the two P arrivals are approximately `0.2683` and `0.3025`.

At X, the second event is two time units after the first and the configured
decay rate is `0.05`:

```text
x_X(t2+) = 0.2683 * exp(-0.05 * 2) + 0.3025
         ≈ 0.5453
```

Each contribution separately is below `theta_E=0.5`; the sum crosses it
without clipping or reaching `theta_M`. For O-, B's second input has the same
magnitude and opposite sign. Its E1 residual state must still admit a
negative B excursion; the transformed negative contribution at X is expected
to cancel the decayed first contribution and remain within `(-0.5,0.5)`.
For I, the two X-local inputs reproduce the approximate P contribution
magnitudes but have independent X-root identities. T contains only the first
subthreshold contribution.

The expected D transfer from the P X excursion is approximately
`tanh(0.2597)=0.254`, above `theta_E_D=0.2`. Exact actual state/emission values,
threshold margins, timestamps, and contributors must be computed from the
frozen E1 implementation during future tests. These calculations are design
checks only; no measured behavior is asserted here.

## Required observations

At every dequeue/receipt, record X's/B's/D's observed state before the event,
the source-equation-derived state after decay, signed contribution,
post-update state, mode, threshold, local time, event ID,
lineage/episode, queue sequence and dispatch ordinal. For each E1 internal
event, record pending kind/time/sequence and valid/stale result. For each
emission, record its new event ID, neuron-local sequence, timestamp, signed
payload, episode, full bounded contributor set and truncation state. For each
accepted transfer/arrival, record immutable edge descriptor identity,
Model-B pre/post-transfer payload, delay, send/arrival time and queue
sequence. For C, record a separate blocked-route decision with the source
emission, excluded edge descriptor and reason; do not create a transfer or
arrival record. At termination, record final states, modes,
provenance, emissions, D receipts, queue/pending counts, processed/created
counts, artifact bytes and resource samples.

The observer is downstream-only and bounded. It cannot change neural
payloads, sequence numbers, queue order, event IDs, route policy, or E1 state.
Lineage alone is insufficient for causal ancestry; use E1 contributor
provenance and the observer's explicit root/transfer mapping. Truncation or a
missing transfer-parent link invalidates a causal PASS.

## Acceptance and outcome classes

**Mechanism PASS** requires all:

1. P includes both B roots, two B emissions, accepted positive-delay B-X
   transfers, matching X receipts, and the analytically required local
   threshold crossing without M-boundary, clipping, or truncation.
2. P contains exactly one new X ordinary excursion after the crossing and
   exactly one matching X-D transfer/receipt at D.
3. N and C contain zero X emissions and zero D receipts; C still contains
   both B emissions and records the B-X blocked-route decision (with no
   fictional transfer or arrival).
4. I contains one X-local-rooted X emission and one matching D receipt with
   no B root in ancestry.
5. T contains one B emission/receipt at X, remains below threshold, and
   produces zero X emissions/D receipts.
6. O+ shows the declared same-sign crossing, while O- records a real negative
   B excursion, signed negative X contribution, opposing state update and
   zero X emissions/D receipts.
7. Same-arm replay produces byte-identical canonical state/event/emission/
   transfer/arrival/terminal evidence; no IDs, queue order, outcome, or
   provenance flags differ.
8. All hard bounds complete without overflow, timeout, out-of-scope boundary,
   identity reuse, observer failure, or missing evidence.

**NOT SUPPORTED** applies only if a valid, complete, replayable fixture runs
within all bounds but P fails to differ from N/C as predeclared. **INVALID /
UNINTERPRETABLE** applies if a control fails structurally, an expected event
is missing, an unexpected X/D root exists, the opposing polarity is not
produced, provenance is incomplete, replay differs, or any bound/invariant
fails. Do not tune and rerun an invalid trial.

Mechanism PASS is not evidence that a structural learner discovered a useful
path, that the task is learned, that resources scale, or that R4 is comparable.
