# Luna-63C C0-C7 fixture freeze

**Disposition: FROZEN — AWAITING INDEPENDENT LUNA-0 REVIEW.**

This is the unexecuted, design-derived C0-C7 fixture inventory for the
Luna-63C Stage-A certificate. It freezes fixture identities, input families,
event identities, mathematical time sources, checkpoint identities, and
ordinal dependencies. It does not calculate numerical enclosures, binary64
ceilings, or final ordinals. Those remain N1/N3/N4 work after this freeze is
independently reviewed.

No solver, runtime, C0-C7 scientific fixture, numerical certificate, Lane S,
or N5 synthesis was run. This artifact is not a numerical certificate or
Stage-B authorization.

## Authority and scope

The governing sources are:

- reviewed design revision
  `3e7d31b9a527e908b21abee3766906084e7cd082`;
- latest design handoff revision
  `a303ebb835b72fdd01c86df478431b8638aacbb4`;
- N4 requirements schema
  `workflow/docs/luna/LUNA_63C_N4_CERTIFICATION_REQUIREMENTS.md`, frozen at
  `9cc92adb56e388d8675d538410b319fd8d8841a5` and independently reviewed at
  `47dd26f08dfa113565ad41f1abe34888eed0e0bf`;
- the owner clarifications recorded in this freeze.

The source certificate at
`experiments/luna63c/certificate/expected_outcomes.json` remains an immutable
historical v1 artifact with its original null fields and manifest. This
separate freeze supersedes those nulls for the C0-C7 fixture contract; it
does not rewrite that blocked report or imply numerical evidence.

The intervention remains exactly:

```text
X=(x,y)
xdot = R*(-x-y)
ydot = R*(x-y)
alpha = omega = 1 TU^-1
X(s) = p*A*exp(-s)*(cos(s), sin(s))
g = exp(-pi/4)/sqrt(2)
theta = 2*g
q = g
h(X) = p*y-theta
H = 2 TU
T_q = ln(4/q) TU
T_life = H+T_q+1 TU
T_clock = 2^20 TU; event clock is inclusive [0,T_clock]
```

No alternate field, solver, equation, parameter, threshold, or tolerance is
introduced. The analytic flow and every root/time claim remain subject to
independent N1/N4 evidence.

## Owner-frozen decisions

### C2 / A=1 checkpoints

The A=1 state-comparison observations are exact active/reference times
`0`, `1/2`, `1`, and `2` TU. They are not external events, timers, or record
allocations and are not converted to binary64 event timestamps.

At active time `s`, the exact flow oracle is
`X_oracle(s)=p*exp(-s)*(cos(s),sin(s))`. The candidate state is the actual
hybrid state at the observation: it follows the same flow until the exact
quiet time `s_q=ln(1/q)=pi/4+(ln 2)/2`, then the reviewed terminal transition
clears it to `(0,0)`. Thus at `s=2`, after quiet, the ideal candidate is
`(0,0)` while the unreset flow oracle is
`p*exp(-2)*(cos(2),sin(2))`. The ideal discrepancy is `exp(-2)`, which is
strictly below the owner-selected acceptance ceiling `theta/4`; N4 must
certify the candidate/oracle comparison under that strict rule. The
observation itself does not cause or move the quiet transition.

For every checkpoint the required comparison is
`||X_candidate-X_oracle||_2 < theta/4`, with strict inequality and the L2
norm. `theta/4` is the acceptance ceiling, not a claim about measured
implementation error. Equality fails; an uncertainty interval that straddles
the ceiling remains unresolved. No smaller or wider bound is substituted.

### C7 lifecycle and event-time decisions

1. A committed output persists from mathematical root/commit `t_root` until
   it is processed at `t_emit`. Lifecycle cleanup/reset follows processing.
   If reset shares the represented timestamp with processing, output
   processing has precedence and reset follows logically. The required trace
   is `t_root <= t_emit < t_reset` in lifecycle order.
2. Expiry coalescence means two distinct governed real times map to the same
   binary64 timestamp under the reviewed ceiling conversion. The expiry
   precedence rule applies at that represented tie. Exact-real equality is
   not separately manufactured.
3. The reviewed A=4 trajectory has mathematical
   `s_rearm < s_quiet`. No synthetic equality fixture is created. If the
   independently certified represented timestamps coalesce, the reviewed
   re-arm-before-quiet precedence applies while the strict mathematical
   ordering is retained as evidence.
4. A positive sub-ULP case uses the already-frozen C2 upper representable
   neighbor of `q` and a clock origin near the inclusive clock limit where
   the exact positive quiet delay is below the cause timestamp's ULP. N4
   must certify the unique ceiling and strict-future relation; `nextafter`
   is not a fallback.
5. Every C7 case using magnitude `A=4` fixes `p=+1`, including inherited
   C4 schedules. C7 does not leave A=4 polarity implicit or duplicate those
   lifecycle cases for the opposite orientation.

These decisions do not alter the vector field, parameters, thresholds,
arithmetic profile, fixtures C0-C6, record/timer/output caps, N4 schema, or
Stage-B authorization.

## Fixture and checkpoint inventory

`fixtures.json` is the machine-readable inventory. Every scheduled event has
a stable fixture-local identity, a mathematical or external-input time
source, and an ordinal dependency. Numerical lanes must materialize certified
times and ordinals; this freeze does not preselect those results.

### C0 — neutral, no RECALL

Start in `READY` at `X=(0,0), R=0`; no input is delivered. The sole checkpoint
is the initial neutral state. No episode, timer, output, or unique event
record exists.

### C1 — neutral + RECALL

Deliver `RECALL(R=1)` followed by `RECALL(R=0)` while in `READY`, with
nondecreasing valid input time and delivery order. Their time values are
external fixture inputs, not selected numerical outputs. At both records
the state remains `(0,0)`; neither packet creates a STORE, episode, timer,
motion, or output. Both input records are counted.

### C2 — entry/subthreshold boundaries and tangency

Use exactly the existing magnitude family:

```text
0, q/2, q, greatest binary64 strictly below q,
least binary64 strictly above q, 1, 2
```

The exact `q` case is a symbolic boundary oracle, not a fabricated binary64
equality. Neighbor values are defined by their exact directed relation to
mathematical `q`; N4 supplies their eventual encodings. For every nonzero
state, preserve both signed orientations through the design's `p` convention;
do not alter A, the field, or the event threshold to make one pass.

Each case starts with one `STORE(R=0,A)` at fixture origin. Cases `0`, `q/2`,
`q`, and the lower neighbor terminate atomically as `QUIET_ENTRY`; they do not
evaluate `ln(A/q)` or schedule a timer. Cases `1`, `2`, and the upper
neighbor receive `RECALL(R=1)` at the same input timestamp after STORE by
external delivery ordinal, then follow uninterrupted active time until
quiet. There is no artificial positive HOLD duration. All C2 cases produce
zero canonical outputs. The exact `A=2` tangent is not a crossing.

For A=1, observe the complete `(x,y)` candidate state and the independent
flow-oracle state at exact active times `{0,1/2,1,2}` TU. These observations
do not add events or change lifecycle. For this fixture the quiet event lies
before `s=2`; the expected hybrid candidate is therefore cleared at the last
observation while the comparison oracle remains the exact flow formula.

### C3 — supra-threshold held

Start each fresh `A=4` episode with `R=0`. Observe the held state for exactly
the reviewed HOLD durations `{0,1,2}` TU; no output or continuous motion
occurs during HOLD. C3 does not release after those HOLD observations; release
after `{0,1,2}` is the separate C5 replay. The separate expiry-boundary
instance supplies a valid RECALL input at the represented expiry time. The
expiry timer precedes that external input, commits `EXPIRED`, and prevents
revival.

### C4 — supra-threshold release

Start a fresh `A=4` episode and release at fixture origin (`HOLD=0`) by
`RECALL(R=1)`. Keep the gate continuously open through the reviewed crossing,
re-arm, and quiet boundaries, supplying at least `T_q` active time before
expiry. The required event identities are the upward crossing/commit, output
processing, downward re-arm, quiet, and expiry schedule. The one-output claim
is conditional on the reviewed release requirement and successful root,
time, causal-order, and expiry certificates.

### C5 — unequal-HOLD replay

Use three fresh matched `A=4` instances with exact HOLD durations
`{0,1,2}` TU, then uninterrupted `R=1` for at least `T_q`. Active-time
states and root offsets match the exact semigroup. Absolute event times shift
by each HOLD duration and are certified independently; bit-identical
absolute timestamps are not required.

### C6 — ungated reference

Use the same `A=4` initial state and release origin as C4 with `R=1`.
This is the independent exact-semigroup reference, not a second execution of
the candidate propagation or lifecycle code. Align active-time origins and
compare the reviewed crossing, re-arm, quiet, and terminal classifications.

### C7 — lifecycle/time edge cases

The 14 design-listed subcases are retained, with owner clarifications applied
to reset/output persistence, expiry coalescence, and re-arm/quiet ordering.
Each subcase has its own stable identity in `fixtures.json`:

Every subcase starts in a fresh neutral `READY` instance unless it explicitly
inherits an earlier case. The sole cross-case inheritance is post-abort
ingress, which follows the completed overflow case. A timer event identity
names one created timer record; creation, cancellation, pop, stale processing,
and invalidation refer to that record unless a distinct replan is explicitly
named.

1. Duplicate RECALL: settle first; idempotent application creates no phase
   reset or duplicate live timer; STORE, initial RECALL, and duplicate RECALL
   share a valid represented input time and are ordered by external delivery
   ordinals. Accepted duplicates consume input budget.
2. Alternating RECALL: only open-gate durations add active time; pause cancels
   the original crossing timer after positive active time strictly below the
   upward root; expiry remains live. Resume no later than `t_store+H` creates
   a distinct crossing timer. Continue uninterrupted through the crossing,
   re-arm, and quiet boundaries; quiet precedes and invalidates expiry.
3. RESET before output commit: settle old gate and due boundaries, abort,
   clear uncommitted state/timers, and invalidate the generation; no output
   is created.
4. RESET after output commit: hold the committed output persistently from
   `t_root` to `t_emit`; process it once, then reset/cleanup. If represented
   times tie, processing precedes reset. Preserve its ID, timestamp, payload,
   and immutable output record. The fresh A=4 schedule inherits C4 through
   output processing; reset is before the scheduled re-arm boundary and
   invalidates the already-created flow and expiry timer records.
5. Stale timer: process the canceled generation/token as stale, with no
   state/output effect and no second unique record. Its identity is the
   crossing timer created by STORE/RECALL; pause invalidates it before its
   original due time, and the stale pop references that same record.
6. Re-arm before quiet: inherit the full C4 A=4 schedule, including STORE,
   RECALL, crossing, committed output processing, re-arm, quiet, and the
   STORE-created expiry record. Certify strict real-time
   `s_rearm<s_quiet`; do not synthesize equality. Apply re-arm-before-quiet
   precedence only if governed binary64 conversion coalesces their
   represented times.
7. Expiry coalescence: choose a semantically valid external packet with
   real time distinct from expiry but the same governed binary64 ceiling.
   The fresh A=4 STORE is the cause of the expiry record; hold the gate closed
   through expiry. Expiry processes first and the packet cannot revive the
   episode.
8. Semantically invalid packet at expiry: use the same represented-time
   coalescence condition and the same fresh held A=4 STORE/expiry prefix, but
   supply an in-domain RECALL with nonbinary gate value. Settle and commit
   expiry first, then install the external key and record
   `REJECTED_SEMANTIC`.
9. Timestamp-invalid packet: cover malformed/nonfinite, out-of-domain,
   late, and unorderable envelopes in separate fresh instances, each after
   an accepted A=4 STORE has established the processed timestamp key and
   expiry record. Each consumes audit identity/count but does not settle or
   advance model time or ordering key; expiry is not popped in these cases.
10. Overflow attempt 17: accept one STORE and eight RECALLs (including
    duplicates), then issue seven semantically invalid STORE attempts while
    the episode remains active. The initial RECALL begins `A=4` release; after
    output processing and before re-arm, the seven duplicate RECALLs and seven
    invalid STOREs share one admissible binary64 timestamp in causal delivery
    order. These are the 16 within-budget attempts. Then commit
    `REJECTED_CAP_OVERFLOW` as processed-current before cleanup/READY; retain
    `ABORTED` and the already-committed and processed output. Do not
    timestamp-validate or settle attempt 17.
11. Post-abort ingress: close before component addressing; allocate no
    component attempt ID or record.
12. Output/expiry coalescence: use a late/paused A=4 release whose
    fresh STORE creates the expiry record and the gate remains closed until a
    late RECALL. Continue uninterrupted so the mathematical crossing precedes
    expiry but the certified output and expiry ceilings coincide. Suppress the
    uncommitted output and fail closed; no output record is allocated. A
    previously committed output in a separate lifecycle remains immutable.
    If no such schedule can be certified under the reviewed model, mark this
    edge case blocked rather than fabricate a result.
13. Near-clock admission: define the last binary64 STORE origin whose exact
    expiry remains within `[0,T_clock]` and its immediate successor. Test
    them in separate fresh `READY` instances. Accept only the in-domain case
    and its expiry record; reject the successor before episode/timer
    allocation.
14. Positive sub-ULP delay: use the C2 upper-neighbor-of-q state and the
    near-clock origin above in a fresh `READY` instance. STORE it, create the
    expiry record, then apply a distinct `RECALL(R=1)` at the same binary64
    timestamp after STORE by external delivery ordinal; create the quiet
    timer from that processed RECALL. The positive quiet delay is below one
    cause-time ULP and must have a unique common ceiling strictly after that
    cause and before expiry. Quiet terminal invalidates the existing expiry
    record. Failure to establish any condition remains blocked.

Each C7 schedule is constrained only by these reviewed source relations.
The exact external binary64 inputs needed to witness a relational edge,
certified ceilings, and destination ordinals are N3/N4 results, not invented
fixture-freeze constants.

## Shared event, ordering, and accounting contract

- Input processing is `audit -> timestamp admissibility/reservation ->
  settle old gate and due internal boundaries -> install external key ->
  semantic validation/application`.
- Internal boundaries precede external inputs at a shared represented time.
  External ties use their delivery ordinals. Expiry preempts every
  uncommitted boundary and same-time external application. The sole allowed
  exact internal tie is re-arm followed by quiet; the owner additionally
  requires preserving the analytic strict re-arm-before-quiet ordering when
  represented timestamps coalesce.
- Crossing commit is at mathematical `t_root`; output processing is at
  represented `t_emit`. A pending committed output cannot be cleared before
  processing. Reset after processing cannot rewrite/retract it.
- Timer kinds are crossing, re-arm, quiet, and absolute expiry. At most one
  live flow-boundary timer and one live expiry timer exist. A stale/cancelled
  timer remains one unique record and changes disposition; it is not recreated
  by popping it.
- Every input attempt through 16, the single overflow attempt, every unique
  timer record, and the single output record is counted exactly once.
  Output processing and terminal cleanup are lifecycle transitions on the
  existing output/timer records, not extra records.
- Maximum unique records remain exactly bounded by
  `16 + 1 + 24 + 1 = 42`. Timer creation is capped at 24 across all timer
  kinds; no per-kind expansion is authorized. No record is allocated after
  closed-ingress rejection.
- Event ordering and final ordinals are derived first from mathematical
  causal order and then from governed binary64 conversion and precedence.
  Queue insertion order is never the authority.

## N1/N3/N4 and W/T/E coverage contract

`fixtures.json` maps every checkpoint, external input, timer boundary,
output lifecycle event, and terminal event to its fixture-local identity,
mathematical/external time source, N1 witness requirement, N3 event mapping,
N4-A/N4-B requirements, and ordinal dependency. For non-events, the map
marks N3/N4-B not applicable with a reason.

- **W / N1:** independently certify state/root/quiet/tangency witnesses,
  including all A=1 observations and the four clarified C7 relations.
- **T / N3:** materialize exact fixture-input timestamp encodings, event
  boundary ceilings, strict-future results, and the complete ordinal
  dependency graph for all frozen event identities.
- **E / N4:** independently verify outward arithmetic, precision agreement,
  event-time ceilings, clock-domain and expiry mapping, equal-time ordering,
  and the owner-frozen strict A=1 error criterion.
- **N5:** remains a later immutable synthesis of completed N1/N3/N4 evidence.
  It does not select new fixtures or add mathematics.

The partial untracked W/T/E artifacts and their historical blocked handoffs
are not modified or promoted by this freeze. W/T/E remain paused until
independent Luna-0 PASS on this exact fixture inventory.

## Resource, execution, and claim boundaries

The existing fixed bounds are unchanged: 16 within-budget attempts, one
recorded overflow attempt, 24 timer records, one output, and 42 unique records
maximum; at most one live flow token and one live expiry token; 256/512-bit
required arithmetic with conditional escalation through 1024 bits and at
most 128 root bisections. No numerical result, implementation behavior,
runtime enforcement, spike, recall-gating result, hardware equivalence, task
efficacy, ACP acceptance, A01-A15 change, 63B dependency, sequence echo, or
Luna-64 follows from this inventory.
