# Luna-63C — bounded stable-focus excursion design

**Disposition: LUNA-63C DESIGN BOUNDED — MECHANISM EXPERIMENT MAY BE
CONSIDERED.** This is a proposed, unexecuted design. It is not an experiment
authorization, an implementation contract, an ACP, or an architecture
adoption. Independent Luna-0 review is required before any later decision.

## 1. Authority, evidence boundary, and question

The authoritative starting revision is
`d006e1bc6ff09627df8fe7f6c1213380b953291f`; the assigned worktree was clean
on branch `experiment/luna63c-nonlinear-excursion-design` at that exact
revision. The committed `.github/agents/luna-63c.agent.md` at that baseline
controls this assignment.

The owner attachment `0db88cfc-a144-4171-a155-fea721c1bbe9` was read in four
sections, lines 1–240, 241–480, 481–720, and 721–927. The governing boundary
is documentation/design only: no implementation, code, test, numerical
solver, simulation, trajectory, trial, training, task-efficacy run, hardware
exercise, or Luna-64.

**OBSERVED, limited prior evidence:** the reviewed Luna-63A conclusion is
confined to exact zero-leak HOLD and resumed analytic scalar decay in its
isolated probe. That does not establish this model's stability, excursion,
event conversion, or output. Luna-63B remains a design-only proposal whose
separate numerical prerequisite is blocked; this design neither consumes
nor assumes any 63B equation, result, or unpublished material. Luna-62's
FIFO-like sequence-memory architecture remains **PROPOSED — ACP REQUIRED**,
not adopted. Luna-61's independent PASS remains conversation-provided, not
tracked-verified. No result in those tracks is used as evidence for the
candidate below.

The design question is narrow: can a finite local state remain displaced and
silent while held, then—only when RECALL permits its own stable-focus flow to
resume—cross one output section and return to neutral, with RECALL itself
providing no additive excitation?

## 2. Candidate-family comparison

| Family | Stable rest / excursion | Boundedness and event clarity | RECALL fit / reproducibility | Qualitative FPGA and analog fit | Main risk / decision |
|---|---|---|---|---|---|
| FitzHugh–Nagumo-like cubic excitable system | Can have a stable rest and a threshold-triggered large excursion for selected parameters. | Cubic voltage term alone does not supply a complete global invariant rectangle when coupled to an unbounded recovery coordinate; the excursion boundary and return must be derived for one exact parameter set. A section crossing is possible, but one-event proof is parameter-sensitive. | A stimulus-current term makes it easy for RECALL to become the effective excitation; gating all dynamics instead needs a separate HOLD stability/expiry proof. Numerical integration and threshold classification need explicit control. | Few state variables and arithmetic are qualitatively suitable for FPGA; analog nonlinear blocks are plausible but unvalidated. | Rejected for this first design: the required no-direct-RECALL-excitation and exactly-one-crossing argument would be more complex than necessary. |
| Stable-focus / spiral normal form plus event section | A focus has a provable stable neutral point; a displaced state rotates through an output section while its radius decays. | A compact invariant disk follows from a Lyapunov function. A derived amplitude band and a finite quiet boundary make event count and return auditable. | Whole-field gating freezes only a state whose ungated field is globally stable; the exact semigroup supports independent replay. The gate multiplies the field and is not an input. | Two state registers, fixed-coefficient coupled arithmetic, a comparator/FSM and a local timer are qualitatively FPGA-mappable. Coupled integrators, switches/sample-hold and comparators are qualitative analog/FPAA analogues. | **Selected, with a deliberate scope limit:** the flow is linear; the neuron is hybrid-nonlinear through the threshold, hysteresis, one-shot episode and quiet reset. It is not a claim of smooth FHN-like excitability. |
| Purpose-built bounded polynomial/vector field | A custom radial field could separately specify attraction, angular motion and excursion amplitude. | A complete polynomial invariant-region proof and a simple section-crossing count would have to be supplied; merely writing saturating terms is not such a proof. | A gate can be placed on flow, but its effect on stored-state drift and release must be established for the chosen field. | Finite polynomial arithmetic is qualitatively implementable; saturation/nonlinear analog accuracy would remain open. | Rejected as a family choice here: it adds field complexity without improving the exact proof over the selected stable focus. |
| Threshold-oscillator / excitable hybrid | A hybrid oscillator can generate repeatable events and a return state. | Threshold and phase rules can be made bounded, but without an additional amplitude/one-shot policy it naturally permits multiple spikes. | A gate could pause phase, but then recall can select timing/phase and the hybrid needs extra state and tie rules. | Counters/FSMs are FPGA-friendly in principle; analog phase/reset realization is only qualitative. | Rejected for the first mechanism: multi-spike behavior is not required to test HOLD → RELEASE → ONE EXCURSION → RETURN and complicates the claim. |

The spiral is **not an architectural necessity** and is not retained for
visual appeal. This particular stable focus is selected because its closed
form gives a direct stability proof, a fixed first-lobe threshold margin,
and a finite event-aware oracle. Multi-spike compression or sustained
oscillation is deferred.

## 3. Exact proposed candidate

### 3.1 State, units, and load

There are exactly two continuous state coordinates:

| Coordinate | Meaning | Units and bound |
|---|---|---|
| `x` | Signed local stored displacement—the candidate's WEMA-like state for this isolated mechanism, not a separate answer or sequence buffer. | normalized state units (SU); the joint state satisfies `x²+y² ≤ 16`, hence `|x| ≤ 4 SU` |
| `y` | Signed output/excursion coordinate. | SU; the same joint disk bound gives `|y| ≤ 4 SU` |

Time is in normalized local time units (TU). The local gate is binary
`R ∈ {0,1}`. A finite episode record also holds `p = sign(x_store)` (−1, 0,
or +1), the local store timestamp, episode/generation identity, mode, event
armed/issued flags, and a bounded cue counter. These are bounded event/
lifecycle metadata, not extra continuous coordinates or a sequence store.

The proposed local store operation, allowed only when `R=0` and no episode
is active, is:

```text
x <- clip(z_local, -4, +4)
y <- 0
p <- sign(x)
start_time <- local_event_time
mode <- HOLDING
event_armed <- true
event_issued <- false
```

`z_local` denotes only an already-available, bounded local accumulator value;
this document does not define how an upstream PCN or ACP-0008 state computes
it. Future mechanism fixtures may initialize the same states directly.
Values above the bound are clipped at this explicit store boundary. No
evaluator truth, symbol identity, sequence position, task label, global
statistic, or external answer buffer is admitted.

### 3.2 Field and exact flow

For one frozen proposed parameter point, `α = 1 TU⁻¹` and `ω = 1 TU⁻¹`:

\[
\dot{x}=R(-\alpha x-\omega y),\qquad
\dot{y}=R(\omega x-\alpha y).
\]

Equivalently, `dX/dt = R A X` for `X=(x,y)ᵀ` and
\[
A=\begin{bmatrix}-1&-1\\1&-1\end{bmatrix}.
\]

`α>0, ω>0` is the stable-focus regime; only `(1,1)` is proposed for this
design. For a constant gate over an interval, define active time
\[
s(t)=\int_{t_0}^{t}R(u)\,du.
\]
Then the exact mathematical flow is
\[
X(t)=e^{-s}
\begin{bmatrix}\cos s&-\sin s\\ \sin s&\cos s\end{bmatrix}X(t_0).
\]
Thus `R=0` freezes every coordinate exactly, and `R=1` releases the
ordinary field. Gate changes pause/resume active time; they do not add a
current, impulse, threshold shift, or phase reset.

### 3.3 Rest, stability, and bounds

The sole flow equilibrium is `(0,0)`. The Jacobian eigenvalues are
`−1 ± i`, with strictly negative real part. For
\[
V(x,y)=\tfrac12(x^2+y^2),\quad
\dot V=-R(x^2+y^2)=-2RV.
\]
Therefore the ungated release flow is globally exponentially stable, and
`r=√(x²+y²)` obeys `dr/ds=−r`. At `R=0`, `X` is constant, so HOLD cannot
diverge or expose an unstable frozen state; the neutral state remains fixed
for either gate value. On release the origin is asymptotically stable.

The closed disk `r≤4` is invariant: release strictly contracts its radius,
HOLD preserves it, and the explicit quiet reset maps inward to zero. No
unbounded polynomial or numerical saturation is hidden in the flow. A
non-finite state, an impossible nonbinary **internal** gate value, counter
exhaustion, or failed scheduling precondition faults closed to the neutral
state without emitting. A timestamp-admissible input packet whose gate value
is not exactly 0 or 1 is instead semantically rejected after old-gate
settlement under §4.3; it does not corrupt or fault an otherwise valid model.

## 4. HOLD, RECALL, and event semantics

### 4.1 Complete local state and lifecycle

At reset/initialization the local record is
`(R,mode,X,p,A,s,t_store,t_prev,prev_order,t_last,armed,issued,terminal_reason,delivery_attempt_id,episode_id,
generation,timer_tokens,output_status) =
(0,READY,(0,0),0,0,0,none,0,0,0,false,false,NONE,0,none,initial,none,NONE)`.
`sign(0)=0`. Neuron-lifetime delivery-attempt, episode, timer-token, and
output-ID counters are finite unsigned 64-bit integers, start at zero, and
never wrap or reset. Counter exhaustion faults closed.

For one active episode, retain exactly:

| Field | Meaning and lifecycle |
|---|---|
| `R` | Current binary gate. `0` holds; `1` permits the stable flow. |
| `mode` | `READY`, pre-output `HOLD`/`RELEASE`, post-output `REFRACTORY`, `QUIET`, `EXPIRED`, `ABORTED`, or `FAULT`. Before output, mode mirrors `R`; after output it remains `REFRACTORY` while `R` independently controls flow. A terminal transition clears to `READY` only when its terminal disposition is committed; the retained `terminal_reason` identifies that disposition. |
| `(x,y), p, A` | Current continuous coordinates, stored polarity, and immutable stored magnitude. `p=sign(x_store)`, `A=|x_store|`. |
| `s` | Accumulated active release time since STORE; changes only during `R=1`. |
| `t_store,t_prev,prev_order,t_last` | STORE time; `t_prev` and `prev_order` identify the latest actually processed internal record or timestamp-admissible external record, including one later rejected semantically, and its monotone destination-queue ordinal for same-time ordering. An incoming external pair is only transiently reserved during admissibility/settlement and is installed after due internal records; a timestamp-invalid record does not advance this key. `t_last` is the settlement frontier. Pending committed output is not processed until `t_emit`. `t_prev` is binary64; `t_last` may be an interval-enclosed mathematical root. |
| `armed,issued,terminal_reason` | `armed` starts true only for `A>2`; the first certified crossing changes it to false and permanently sets `issued=true` for that generation. Re-arm cannot clear `issued`. `terminal_reason∈{NONE,QUIET_ENTRY,QUIET,EXPIRED,ABORTED,FAULT}` is initialized `NONE`, set on terminal disposition, retained in `READY` for audit, and reset to `NONE` by a new STORE. |
| `episode_id,generation` | Monotone episode identity and cancellation generation. Every asynchronous timer carries both plus its per-kind token. |
| `delivery_attempt_id` | Neuron-lifetime monotone `uint64` assigned to every addressed input before validation; exhaustion faults closed. Per episode, at most 17 addressed attempts are recorded: 16 within-budget attempts plus one recorded cap-overflow attempt that aborts closed. After that abort, later ingress is rejected before component addressing and receives no component attempt ID. |
| Timers/tokens | At most one live next-flow-boundary token (`crossing`, `rearm`, or `quiet`) and one absolute `expiry` token. Replanning increments tokens; a popped nonmatching token is stale and has no state/output effect. |
| `output_status` | `NONE`, `COMMITTED`, or `PROCESSED`. A committed output record has a persistent neuron-lifetime ID/sequence and is not owned by the cancellable episode timer generation. |
| Counters | Per-episode offered/accepted input count, timer creations/cancellations, stale timer deliveries, and output status; all are bounded as specified in §5.2. |

`RECALL(R=v)` is the only gate-record form; the packet value `v` must be
exactly 0 or 1. A timestamp-admissible packet with another gate value is
semantically rejected after old-gate settlement; it is distinct from an
impossible nonbinary internal `R`, which faults closed under §3.3.
`STORE(R=0,A)` is accepted only in `READY` with current `R=0`; STORE with
`R=1` or during any other mode is rejected. `RESET(R=0)` is an answer-free
abort/reset record; RESET with `R=1` is rejected. Every timestamp-admissible event is settled under the **old** `R` before
semantic validation can change the gate or lifecycle.

* `RECALL(R=0)` pauses flow and cancels every not-yet-reached crossing,
  re-arm, or quiet timer; the absolute expiry timer is not cancelled.
  Before output, set mode to `HOLD`; after output, keep `REFRACTORY`.
  Repeating `R=0` is idempotent.
* `RECALL(R=1)` resumes flow from the settled state and schedules the next
  active-time boundary. Before output, set mode to `RELEASE`; after output,
  keep `REFRACTORY`. Repeating `R=1` is idempotent and does not restart
  the flow or duplicate a timer. In `READY`, it changes only the gate; no
  store, motion, or event is manufactured.
* `RESET(R=0)` first settles the old flow and every boundary due through the
  reset time. It then sets `R=0`, invalidates all uncommitted timers by
  incrementing `generation`, clears `X,p,A,s`, sets `armed=false`, and enters
  `ABORTED` then `READY`, atomically committing `terminal_reason=ABORTED`
  with that terminal disposition. Preserve `issued` as the retired generation's final
  audit bit; a later STORE initializes `issued=false` for its new generation.
  Retain neuron-lifetime episode/event IDs and counters; advance `t_prev`,
  `prev_order`, and the settlement frontier to the reset record, after settling
  internal boundaries due through it. Clear live timer
  tokens, but never rewind token counters. Retain `t_store` only as retired
  episode metadata. Any output already in `COMMITTED` state remains an immutable
  queued output with its original ID, payload and timestamp and must still
  be delivered/processed once; reset cannot retract it. A crossing not yet
  mathematically reached is cancelled and cannot later emit.
* The 17th addressed input after the 16 within-budget attempts is the single
  `REJECTED_CAP_OVERFLOW` record. Commit its `processed-current` disposition
  and terminal abort atomically: increment `generation`, set `R=0`, invalidate
  and clear all uncommitted timer tokens, clear uncommitted episode state
  `(X,p,A,s)`, set `armed=false`, retain `issued` and neuron-lifetime
  counters/IDs, and set `terminal_reason=ABORTED`. Preserve any output already
  in `COMMITTED` state unchanged for exactly-once delivery. The record's
  disposition is committed before the mode transitions to `READY`; retain
  `terminal_reason=ABORTED` in that terminal READY state. Close ingress for
  the retired episode: later packets are rejected before component addressing
  and receive neither attempt IDs nor episode records. A later STORE is
  subject to the ordinary READY/prior-output processing guard and starts a
  fresh generation.
* Quiet completion and expiry clear `(x,y,p,A,s)`, set `R=0` and `armed=false`,
  invalidate episode timers/generation, and retain `issued` as the retired
  generation's audit bit. Retain monotone identity counters, `t_store` metadata,
  and any already-committed output record. A new STORE initializes new-generation
  `issued=false`, `output_status=NONE`, and fresh per-episode counters; it is
  blocked until any prior committed output is processed. Expiry records `EXPIRED`; quiet records `QUIET`; after either terminal
  transition the local mode becomes `READY`.

### 4.2 Entry regions and finite absolute lifetime

A STORE attempt follows §4.3: its timestamp is checked first, then old-gate
settlement (if an episode exists), then semantic validation. Before accepting
a semantically valid STORE, require a finite value and derive its clipped
`A∈[0,4]`; prove exact `t+T_life` converts within `T_clock`, otherwise
reject without allocating an episode. On acceptance, set `X=(pA,0)`, `p=sign(x_store)`, `s=0`,
`t_store=t_prev=t_last=t`,
set `prev_order` to the STORE delivery ordinal, and set `R=0`.
Allocate a fresh episode/generation; set `timer_tokens=none` and initialize
`issued=false`, `terminal_reason=NONE`, `output_status=NONE`, fresh
per-episode counters, and `armed=(A>2)`. Initialize input counters to `offered=accepted=1` and
`rejected=0`; timer/output counters to zero; and the unique-record
disposition to one `processed-current` STORE. If `A>q`, enter `HOLD`.
Resolve quiet at entry before installing flow timers:

* `A=0`: neutral entry; no polarity, active timer, RECALL effect, or output.
  The accepted STORE transaction atomically commits
  `terminal_reason=QUIET_ENTRY`, `output_status=NONE`, and `mode=READY`;
  STORE is the terminal disposition record, so no intermediate `QUIET`
  mode is exposed.
* `0<A<q`: entry is strictly inside the quiet disk; no output or dynamic
  timer. The STORE transaction atomically commits
  `terminal_reason=QUIET_ENTRY`, `output_status=NONE`, and `mode=READY`;
  the STORE is the terminal disposition record.
* `A=q`: equality is quiet-at-entry, not a positive-time logarithmic
  deadline; no output or dynamic timer. The accepted STORE transaction
  commits `terminal_reason=QUIET_ENTRY` atomically and leaves `mode=READY`;
the STORE is the terminal disposition record.
* `q<A≤2`: held displacement is retained. On release it contracts without
  an output; at `A=2` the first lobe is exactly tangent and is not a
  directional crossing. Quiet time in active-time coordinates is
  `s_q=ln(A/q)>0`.
* `2<A≤4`: the first positive lobe has one upward threshold crossing,
  then one downward re-arm crossing, then quiet at `s_q=ln(A/q)`.

For `A≤q`, the expression `ln(A/q)` is not evaluated. At the exact
mathematical boundary `A=q`, quiet is resolved at STORE. A finite-precision
implementation must certify which side of `q` its exact stored input lies
on; unresolved equality/ordering fails closed without output.

For an active episode the absolute lifetime is `T_life=H+T_q+1 TU`, with
`H=2 TU` and `T_q=ln(4/q)`. The expiry instant is
`t_exp=t_store+T_life`; it is fixed at STORE and never renewed by gate
records. The extra `1 TU=α⁻¹` is a finite relaxation allowance, not an
unlimited wait. All C0–C7 releases that begin by `t_store+H` and supply
continuous `R=1` for `T_q` active units reach quiet at least one TU before
expiry.

The one-output C4 claim is conditional: for `A=4`, at least
`s_up(4)` uninterrupted-equivalent **accumulated active release** before
expiry is required to reach the crossing. Return-to-neutral additionally
requires accumulated active release `T_q` before expiry. A late, paused, or
expired episode that does not meet those budgets makes no exactly-one
excursion claim; expiry clears it without synthesizing an event. This
qualifies the guarantee rather than treating RECALL as a stimulus.

### 4.3 Settling and transition precedence

Every within-budget addressed input has two validation stages around
settlement. The sole exception is the bounded cap-overflow attempt described
in step 1, which is recorded and aborts before timestamp validation:

1. **Count/audit first.** Assign a nonwrapping neuron-lifetime
   `delivery_attempt_id` before inspecting the packet. If an episode is active,
   increment its offered-attempt count too. For attempts 1–16, these
   audit-counter changes do not advance `t_prev`, `t_last`, active time, or
   continuous/model state. The accepted STORE that creates an episode
   initializes its per-episode offered
   and accepted counts to one. Sixteen attempts are within budget. If another
   input is addressed after those 16, assign its lifetime ID, increment
   `offered` to 17, and atomically commit `REJECTED_CAP_OVERFLOW` as
   `processed-current` with the terminal abort defined in §4.1. This one
   bounded overflow record is not timestamp-validated or settled. Its
   disposition is committed before uncommitted state/tokens are cleared and
   mode becomes `READY`; retain `terminal_reason=ABORTED` and any already
   committed output. This is the episode's 17th and final addressed input
   record. No later input is addressed by the closed episode.
   Lifetime-ID exhaustion faults closed before an ID/record can be allocated.
2. **Timestamp admissibility.** Validate only whether the envelope has a
   binary64 finite timestamp `t∈[0,T_clock]` and a delivery ordinal such that
   `(t,ordinal)≥(t_prev,prev_order)` lexicographically and reserve that pair
   without installing it. One unified monotone destination ordinal orders
   internal and external records: same-time internal boundaries precede
   external records, while external records retain their delivery-ordinal
   order. The reservation must leave every certified internal boundary due
   through `t` before the external record in that total order. If
   timestamp/order admissibility or that reservation fails, disposition is
   `REJECTED_TIMESTAMP`: do not settle or advance computational time/state,
   since no valid position in the local event order exists. Audit ID/count is
   retained.
3. **Old-gate settlement before payload semantics.** For every admissible
   packet, settle old-`R` flow from `t_last` through `t`, processing all
   certified crossing, re-arm, quiet, and expiry boundaries due by `t` in
   exact mathematical order. Advance `(t_prev,prev_order)` as each internal
   record is actually processed. Same-time internal boundaries precede the
   reserved external record in the unified destination ordinal; among
   same-time internal boundaries use the boundary precedence in §5.1, and
   among external records use destination ordinals. Unresolved order faults
   closed. At an exact
   expiry tie, expiry wins and retires the generation before any same-time
   packet, regardless of whether its gate or payload would be valid. A due
   crossing commits only if both root and logical-time certificates meet the
   expiry/order rules. A dynamic quiet due at/before `t` likewise terminates
   before applying the packet.
4. **Install reservation; semantic validation/application.** After settlement,
   install the reserved external `(t,ordinal)` as `(t_prev,prev_order)`.
   Then validate packet
   kind, gate value, STORE payload, and mode. A timestamp-admissible but
   semantically invalid packet, including a gate field not exactly 0 or 1, is
   **rejected, not a model fault**: record
   `REJECTED_SEMANTIC`, preserve the settled model state and do not apply its
   payload. If settlement expired/quiet-terminated the episode, retain that
   terminal reason and reject the packet without applying it. Otherwise apply
   valid STORE/RECALL/RESET under §4.1. In `READY`, admissible inputs settle
   the neutral state (no-op); only a semantically valid STORE allocates an
   episode. The installed key advances for every timestamp-admissible external
   record, including semantic rejection; timestamp-invalid records never
   install their reservation.

Thus an invalid gate/payload at a valid expiry timestamp cannot bypass expiry;
it is semantically rejected after expiry is committed. An invalid/late
timestamp cannot be placed and therefore cannot trigger settlement. RECALL
changes the gate only after old-gate settling; it grants permission to the
field and is not direct excitation. For `A≤q`, STORE itself atomically commits
the `QUIET_ENTRY` terminal disposition with `mode=READY`; there is no
intermediate externally visible `QUIET` mode. Dynamic quiet and expiry commit
their terminal reason before clearing mode to `READY`.

An upward crossing commits only after both its mathematical root and logical
time are certified. It atomically sets `issued=true`, allocates the persistent
output ID/sequence once, and creates an immutable record due at `t_emit`.
A later pause, reset, expiry, stale timer, or quiet transition cannot cancel
it. A root coincident with expiry is not committed because expiry has
precedence.

### 4.4 Thresholds, event rule, and analytic cases

For a stored state `X(0)=(pA,0)` with `A=|x_store|`, release gives:

\[
x(s)=pAe^{-s}\cos s,\qquad y(s)=pAe^{-s}\sin s.
\]

The first positive-polarity output-coordinate peak occurs at `s=π/4`,
because `d(e^{-s}\sin s)/ds=e^{-s}(\cos s-\sin s)`. Its amplitude factor
is `g=e^{-π/4}/√2`. The proposed threshold is
`\theta=2g=\sqrt{2}e^{-π/4}` and `q=\theta/2=g`. This exact definition
puts the `A=4` peak at `2θ`, the `A=1` peak at `θ/2`, and the `A=2` peak
at exactly `θ`.

For `p≠0`, the oriented event surface is `h(X)=p·y−θ=0`, crossed upward.
The future adapter emits only if `armed=true`, `issued=false`, the state was
below the section, and the certified derivative `d(p·y)/ds` is strictly
positive.
Tangency is never promoted to a crossing. On the first certified crossing,
set mode to `REFRACTORY`, `armed=false`, `issued=true`, and commit one
canonical `EXCURSION` record with payload `p·1`. A later downward re-arm
crossing is at `p·y=q`; it sets `armed=true` without changing mode, and
`issued` remains true through quiet/expiry/reset.

* For `A≤2`, the first-lobe maximum `A g≤2g=θ`; equality at `A=2` is a
  tangent with zero derivative, so there is no crossing. Every later
  positive lobe is smaller by a factor `e^{-2π}`; there is no later output.
* For `A>2`, the first lobe is strictly increasing on `(0,π/4)` and has
  maximum `Ag>θ`; exactly one rising root lies in `(0,π/4)`. The downward
  re-arm root is unique after the maximum and before `π`, since
  `Ae^{-s}\sin s` strictly decreases there from `Ag>θ>q` to zero.
* Quiet is the first inward crossing `r=q`. For `A>q`, its active time is
  exactly `s_q=ln(A/q)`; at `A≤q` it was handled at entry. For `A=4`,
  `T_q=ln(4/q)=ln(8/θ)=ln(4√2)+π/4<π`. For the strict bound,
  `e²>1+2+2+4/3=19/3>6>4√2`, hence `ln(4√2)<2`; also
  `2<9/4<3π/4` from `π>3`. Thus `T_q<2+π/4<π`, before a second
  positive half-turn. `q<θ`, so quiet reset cannot itself create an event.

These are analytic statements about the proposed equations, not computed
trajectories. Event timestamps and root numerics are separately bounded in
§5.

## 5. Completion, numerical reference, and bounded future execution

### 5.1 Event record, logical time, and scheduler

A certified crossing commits one immutable canonical `EXCURSION` record with
fresh neuron-lifetime ID and sequence, source, logical timestamp, fixed
payload `p·1`, episode ID, and lineage ID. This is only a proposed record shape; no current `ExcursionEmission`
constructor, mode transition, or runtime API is claimed to implement it.
Commit occurs only after both mathematical-root and logical-time
certificates succeed; it atomically sets `issued=true` at `t_root`.
Delivery/processing occurs at `t_emit`, the converted timestamp. A failed
time/order certificate aborts without committing output. The event state
witness is `X(t_root)=(p A e^(−s*)cos(s*),pθ)`, not a state re-evaluated
at `t_emit`.
Subsequent pause, reset, quiet, expiry, stale timer, or episode-generation
change cannot retract an already committed output. Propagation uses existing
causal edge delays; no inline mutation, zero-delay recursive cascade, or
global neural tick is proposed.

`(t_prev,prev_order)` is the key of the last actually processed internal
record or installed timestamp-admissible external record, including one later
rejected for semantic payload or mode. An incoming external pair is transiently
reserved after comparison to the current key, but is not installed until
old-gate internal boundaries due through its timestamp have been settled.
The unified destination ordinal places internal boundaries at the same
timestamp before the external record;
internal ties use §5.1 boundary precedence, and external ties use destination
queue ordinal, not source-local sequence alone. A timestamp-admissible
duplicate, idempotent, or semantically rejected record installs
`(t_prev,prev_order)` after settlement. A malformed, late, out-of-domain, or
unorderable timestamp rejected as `REJECTED_TIMESTAMP` does not install the
reservation. The component clock domain
is `0≤t≤T_clock=2^20 TU`, inclusive. Every delivered and generated record
must have finite time in this domain and be nondecreasing in source history.
A distinct causal internal event that cannot be represented strictly after
the last actually processed key causes fail-closed episode abort; an incoming
external reservation does not move that key ahead of internal events due
before it. There is no zero-delay fallback, timestamp clamp, or unbounded
`nextafter` search.

Interpret every binary64 input timestamp as its exact real value. For an exact
mathematical boundary `b` and certified interval `[lo,hi]`, define
`ceil64(u)` as the least finite binary64 value `≥u`. Convert by refining the
outward interval until `ceil64(lo)=ceil64(hi)`; that common value is the
boundary's logical timestamp. Apply this rule to crossing, downward re-arm, quiet, and expiry. Converted
distinct causal boundaries must be strictly later than their predecessors,
except exact re-arm/quiet coincidence, which shares one timestamp and is
processed re-arm first. Every converted time must lie in-domain. For a
crossing also require `t_emit<t_exp_logical`; if positive
`t_root−t_prev` (where `t_prev` is the actually processed key before the
crossing, not a merely reserved external pair) is below one ULP,
`nextafter(t_prev,+∞)` is only a candidate and is accepted only when interval
rounding proves it is the unique ceiling. Failure to certify the unique
ceiling, finite successor, causal ordering, or expiry ordering by the stated
refinement caps aborts without committing an output.

For a crossing during a release interval, map its certified active-time
root `s*` to absolute time through the unique interval `[s_i,s_{i+1}]`
whose accumulated active time contains `s*`: `t_i+(s*−s_i)`, with all
additions enclosed outward. If the root equals a pause endpoint, settle and
commit it under the old `R` before applying that RECALL record (unless
expiry wins the exact tie). Paused intervals add no active time.

At STORE admission, require the exact expiry sum `t_store+T_life` to remain
inside the clock domain; otherwise reject STORE before allocating an episode.
The absolute expiry is the exact real sum `t_store+T_life`, with
`T_life=H+T_q+1`, interpreted before conversion. Same-time external records
are compared against that exact boundary; expiry wins equality, so the record
cannot resume or revive the expired episode. Distinct exact boundaries must
remain strictly ordered after conversion. If crossing, re-arm, quiet, expiry,
or a causally subsequent external record coalesce in a way that makes their
required order unrepresentable, fail closed. The sole allowed exact tie is
re-arm with quiet: re-arm is processed first, then quiet, retaining
`issued=true`. Expiry wins every exact tie with an uncommitted boundary.
A crossing mathematically before expiry is still suppressed if its converted
output time equals or exceeds converted expiry. A previously committed output persists through a later reset/expiry; its unchanged `t_emit` was already certified strictly before `t_exp_logical`. Reset cannot retract or rewrite it.

### 5.2 Independent analytic oracle and certification limits

The independent mathematical oracle is the closed-form semigroup
\[
X(s)=e^{-s}
\begin{bmatrix}\cos s&-\sin s\\ \sin s&\cos s\end{bmatrix}X_0,
\]
with active time accumulated only while `R=1`. A future implementation must
be separate from the candidate adapter and share no propagation, threshold,
root, timer, or mutable lifecycle code. Proposed arithmetic is outward-rounded
rational intervals, precision increased from 256 to at most 1024 bits. Every
transcendental enclosure must include a rigorous analytic remainder and
directed-rounding bound. If its evaluator cannot establish those bounds, the
oracle reports unresolved; this document does not claim such an evaluator
exists or has run.

Compute `Θ=[θ_lo,θ_hi]` from the exact definition
`θ=√2e^(−π/4)` and `Q=Θ/2`, refining as necessary. The no-crossing/crossing
decision is analytical, not a rounded threshold comparison: exact `A≤2`
means no crossing, including the `A=2` tangent; exact `A>2` means one upward
crossing. Entry quiet uses exact `A≤q`, with equality quiet-at-entry and no
`ln(A/q)` evaluation. For non-symbolic inputs, interval comparison must prove
`A<q` or `A>q`; exact equality is handled only when represented/proven as
that equality. If 1024-bit refinement cannot decide it, fail closed.

For `A>2`, isolate the unique rising root of
`f_A(s)=Ae^(−s)sin(s)−θ` on `(0,π/4)`: its derivative is strictly positive
there, and certified endpoint signs are opposite because `Ag>θ`. Isolate
the unique downward re-arm root of
`g_A(s)=Ae^(−s)sin(s)−q` on `(π/4,π)`: its derivative is strictly negative,
with certified opposite endpoint signs. For `A≤2`, the first-lobe maximum is
`Ag≤θ`; at `A=2` equality is an exact tangent with zero derivative. Later
positive lobes are smaller by `e^(−2π)`, so cannot cross. Quiet for `A>q`
has exact active time `s_q=ln(A/q)`; for `A≤q` it is immediate at entry.
These analytic arguments classify the events; numeric root search is not
used to decide whether the A=2 tangent is an event.

Root isolation may use interval bisection only while bracketing signs,
derivative direction, and active-time mapping are certified. Refine each root
interval and outward-rounded absolute-time sum until both endpoints have the
same `ceil64` value. Certify the order against re-arm, quiet, expiry, and
`t_prev` under the exact precedence in §5.1. At most 128 bisections per root
and 1024-bit transcendental precision are allowed. Those are work bounds,
not proofs: unresolved sign, derivative, exact-tie classification, time
ceiling, or distinct-boundary order at a cap is failure/no output. The root
certificate is the analytic uniqueness/direction argument plus certified
bracketing, interval-to-absolute-time mapping, and common ceiling—not the
iteration count alone.

For frozen subthreshold `A=1` state checkpoints, a future candidate must
certify `||X_candidate−X_oracle||₂<θ/4`; the oracle enclosure must be
narrow enough to establish that strict inequality or the comparison is
unresolved. This is only a state-value comparison. It does not certify
absence of a root, tangency, direction, root identity, crossing timestamp,
re-arm/quiet ordering, or expiry ordering. Those require the separate
amplitude proof and interval/root-order certificates. Event count, direction,
logical timestamp, lifecycle, and budget dispositions are exact pass/fail
fields, never inferred from the state norm.

### 5.3 Lifecycle and finite record accounting

The state fields and terminal transitions are defined in §4.1–§4.3. Maintain
separate monotone per-episode counters: total addressed input attempts;
accepted inputs; malformed/rejected inputs; timer records created;
timer tokens cancelled; stale timer records popped; current timer records
processed; output records committed; output records processed; and total
unique record dispositions. STORE at most 1, RECALL at most 8 (counting accepted idempotent
duplicates), RESET at most 1; at most 16 input attempts are within-budget per
episode, including malformed, rejected, and duplicate records. The STORE
that creates an episode is attempt one. One further addressed attempt may be
recorded as attempt 17, `REJECTED_CAP_OVERFLOW`; it is committed as a
`processed-current` record before the episode atomically aborts without
timestamp settlement. The transition increments generation, sets `R=0`,
clears uncommitted state and tokens, sets `armed=false` and retained
`terminal_reason=ABORTED`, and preserves any already committed output. The
mode becomes `READY` only after the overflow disposition is committed. The
closed episode addresses no further inputs, so the input-record bound is 17.
At most 24 unique timer records are created and scheduled over the episode;
cancellation remains charged to both creation and schedule budgets. At most
one output record is committed. Thus at most `17+24+1=42` unique
input/timer/output records exist; at most 42 records may be pending in the
component queue or processed in aggregate, and no identifier/counter wraps.

Every unique record is in exactly one disposition: `pending`,
`processed-current`, `processed-stale`, or `cancelled-before-pop`. Each
addressed input, including timestamp-, semantic-, or cap-overflow rejection,
is `processed-current` once its disposition is recorded. A cancelled
timer later popped changes from `cancelled-before-pop` to
`processed-stale`; it is not a second record or second disposition. Accepted,
scheduled, cancelled, popped, stale, and processed counts are never conflated.
On cap/queue exhaustion, abort the episode, invalidate all uncommitted tokens,
clear uncommitted state, and preserve an already committed output and its
pending delivery. Queue backpressure or any unresolved certificate is not a
quiet-success outcome.

## 6. Unexecuted falsification protocol (C0–C7)

All items below are future tests only. The state/preload lists, intervals,
expected inequalities, event budgets and rules are to be frozen before any
separately authorized executable work. The task contract authorizes none of
that work here.

| Fixture | Frozen setup | Required observation / falsifier |
|---|---|---|
| C0 — neutral, no RECALL | `READY`, `X=(0,0)`, `R=0`; no STORE. | No episode, timer, output, or motion. |
| C1 — neutral + RECALL | In `READY`, send `RECALL(R=1)` then `RECALL(R=0)`. | Gate changes only; no state load, episode, timer, or output. |
| C2 — entry/subthreshold boundaries | Fresh STORE values `A∈{0,q/2,q,1,2}`; hold, then release where applicable. Treat exact `A=q` as the symbolic oracle boundary; the finite candidate uses certified representable neighbors below/above `q`. | `A≤q` quiet-at-entry without evaluating `ln`; `q<A<2` no crossing then quiet; `A=2` tangent/no event; the `A≤q` STORE atomically commits `QUIET_ENTRY` while mode remains `READY`; lifecycle fields and timer counts match rules. |
| C3 — supra-threshold held | Fresh `A=4`, `R=0`; exercise HOLD durations `{0,1,2}` and separate expiry-boundary instance. | Exact HOLD/no output. Expiry equality clears before same-time RECALL; no timer revives generation. |
| C4 — supra-threshold release | Fresh `A=4`, uninterrupted `R=1` beginning by `t_store+H` and supplied for at least `T_q` active time before expiry. | One certified rising crossing/output, downward re-arm, quiet return, and all time certificates pass. Exactly-one guarantee applies only under this release condition; insufficient active release before TTL aborts without guarantee. |
| C5 — unequal HOLD duration replay | Same supra preload released after HOLD `{0,1,2} TU`, each with uninterrupted active release for `T_q`. | Active-time states/root offsets agree analytically. Absolute output/quiet timestamps shift with HOLD and are independently upward-converted; bit-identical absolute times are not required. |
| C6 — ungated reference | Same initial state and release origin as C4 with `R=1`. | Matches semigroup after aligning active-time origins; no solver/global tick. |
| C7 — lifecycle/time edge cases | Replay C0–C6; include duplicate and alternating RECALL, RESET before/after commit, stale token, re-arm/quiet tie, expiry equality with timestamp-admissible semantically invalid gate/payload, malformed/late/out-of-domain timestamp, the 17th addressed input after 16 within-budget attempts, post-abort ingress, output/expiry coalescence, near clock limit, positive delay below one ULP. | Timestamp-invalid attempts consume an attempt ID but do not settle/advance model time or ordering key; valid-time invalid-payload attempts advance the ordering key and settle old `R` first, so expiry equality preempts semantic rejection. For attempt 17, verify its `REJECTED_CAP_OVERFLOW` disposition is committed before generation abort, clearing of uncommitted state/tokens, retained `terminal_reason=ABORTED`, and transition to `READY`; preserve any already-committed output. Later ingress is not component-addressed or assigned an ID. Verify the 17+24+1=42 total-record cap, deterministic precedence, output persistence, unique record accounting and strict representability. Unresolved/coalesced-invalid cases fail closed; no state tolerance substitutes for a certificate. |

**Independent procedure:** compare a future adapter with a separately
implemented interval/closed-form oracle. Check neutral eigenvalues and
Lyapunov derivative algebraically; classify `A≤2` (including exact tangency)
without numeric root search; certify the `A>2` crossing, re-arm, quiet and
expiry order; compare lifecycle/disposition fields; and require identical
upward-rounded logical timestamps from both root-interval endpoints. State
error tolerance cannot substitute for root/time certification. Failure,
unresolved interval, overflow, unrepresentable ordering, or exceeded bound
is fail-closed, not a passing sample. No plots alone, shared code path,
outcome-tuned threshold, or test-selected parameters are sufficient.

## 7. Architecture, ACP, and claim boundary

| Clause | Design relationship and boundary |
|---|---|
| A01 — event-driven computation | Local continuous state is settled only at a local event, gate transition, predicted crossing, quiet event, or expiry. The analytic reference adds no neural tick. |
| A02 — local time/state | Two bounded local coordinates and explicit local timestamps are proposed. The flow is event-time/active-time based. New semantics are isolated and unaccepted. |
| A03 — finite propagation | A canonical crossing record is scheduled strictly in the local future; existing finite edge delays remain causal. No instantaneous propagated event is proposed. |
| A04 — bounded topology | One finite node/episode and bounded queue/event/counter resources are contemplated; no topology changes. |
| A05 — no spatial reservoir | None is used or added. |
| A06 — predictive coding | Preserved as a separate core capability/obligation. This candidate computes no prediction, prediction error, or propagated error event. |
| A07 — local learning | Only a bounded local stored displacement and gate are in scope. No labels, evaluator truth, global state, or learning rule enters the field. |
| A08 — bounded dynamics | Disk invariant, explicit quiet reset, finite TTL, event budget, solver bounds, and no-wrap failure policy bound state and lifetime. |
| A09 — local energy | No energy model or accounting is implemented or claimed. |
| A10 — utility | No reward/utility or energy tradeoff is implemented or claimed. |
| A11 — delayed credit | No eligibility, reward, or credit is implemented or claimed. |
| A12 — pathway count | No fixed pathway count is proposed; the optional-ten-pathway constraint is untouched. |
| A13 — explicit gating | The binary RECALL gate is only an isolated experimental control; explicit gates remain optional core behavior. |
| A14 — structural plasticity | No growth, pruning, topology mutation, or structural evidence is used. |
| A15 — hardware independence | Only qualitative software/FPGA/analog mappings are stated. No hardware equivalence, implementation, or feasibility validation is claimed. |

This is a substantial **isolated experimental departure**, not ACP-0008
semantics. ACP-0008 adds an opt-in bounded slow scalar integration state
`z` to the existing E1/E2 scalar `x`, with fixed positive decay, input-based
integration/discharge, and unchanged canonical E2 emission. This proposal
instead introduces a two-coordinate stable-focus field, identity HOLD,
binary whole-field RECALL gate, a section-crossing one-shot event, hysteretic
re-arm, finite radial quiet reset, and an absolute episode TTL. It does not
amend ACP-0008, alter the E1/E2 default, or establish an adopted architecture.
The proposed bounds are 16 within-budget input attempts plus one addressed overflow record, 24 timer records, one output, and 128 bisections per root; they are specific to this candidate.

Qualitative digital realization: two bounded state registers, fixed linear
coupled arithmetic, gate, norm/section comparisons, a small lifecycle FSM,
and a finite timestamp/event scheduler. Qualitative analog/FPAA analogy:
two coupled integrators, switched/held state or controlled conductance,
comparators and hysteresis. Hold leakage, parameter variation, event
quantization, analog noise, area, power, timing, or hardware equivalence have
not been measured. All-analog feasibility is unresolved.

## 8. Evidence register, source pins, and validation status

Pins are Git blob IDs resolved from the assigned baseline with
`git rev-parse HEAD:<path>`. Line ranges are the inspected source extents,
not claims that those components were executed.

| Baseline source | Blob | Read extent and use |
|---|---|---|
| `.github/agents/luna-63c.agent.md` | `a5682a768e86c80a675b2061e8e8e92b4b640996` | Full contract; ownership, exact design fields, no-execution and stop boundary. |
| `workflow/ARCHITECTURE_CONTRACT.md` | `3afc85f86dbc6992e01cb7ca26ebadfb49c09cab` | Full A01–A15 and authority text, lines 1–296. |
| `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md` | `510f44daab83c4def92c70617e2d5c731c5760d6` | Core event, bounded-state, A06/A07 acceptance boundary, lines 1–130. |
| `workflow/docs/architecture_proposals/ACP-0008.md` | `1fa832472ce1797061b117e96417d88238a35491` | Full ACP-0008 current scope, lines 1–142. |
| `workflow/handoffs/luna-0-63-governance-review-20261009.md` | `7e964754be00d4c4a7b7c2be187b37655c3eadab` | Current 63A limited conclusion, 63B numerical block, 63C authorization/status, lines 1–281. |
| `workflow/handoffs/luna-0-luna63b-numerical-prerequisite-review-20261009.md` | `e21d1507b148d5ddb52f76ad7c860a8c79eb9e58` | Full blocked prerequisite and non-execution status, lines 1–197. |
| `workflow/docs/luna/LUNA_63B_LOCAL_PCN_STATE_DESIGN.md` | `3e89ac1d2d7f91a26a12ce8ab4b64b6a7f5f1605` | Read current design/status sections; confirms proposal-only boundary, no 63B results consumed. |
| `workflow/handoffs/luna-0-independent-review-luna62-20261009.md` | `885ae4d5c8a95d130ce2b37245b4a0ada591bc31` | Full review, lines 1–190; PASS WITH LIMITATIONS, ACP required, no adoption. |
| `workflow/docs/luna/LUNA_62_SEQUENCE_MEMORY_ARCHITECTURE.md` | `f3ab79ccd08e5b561e7a2b58f9c6ad93b5c3427d` | Full 832-line proposal read in sections; proposed-only FIFO-like design and unresolved gates. |
| `workflow/docs/luna/LUNA_61_TASK_OUTPUT_ASSIGNMENT.md` | `77497b7a70f4d0f6fcd61eea94d08ef877e28dd1` | Full 522-line sequence-echo design read in sections; current runtime has no cue-controlled symbolic replay. |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `b89f43b1d9bbf218f600c9a755c58fe1a406dd63` | Current Luna-63/62/61 status sections read; no workflow edit authorized. |
| `workflow/ARCHITECTURE_CHANGELOG.md` | `e746ec83f79c9ac32dd0e363d2f19dc1a0200db9` | Current Luna-63A/B/C entry read; no changelog edit authorized. |
| `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` | `098d57a450d4824fdecb1eddd75b214c4111a776` | Full template read; applicable identity, scope, architecture, validation, limits, rollback, and next-agent fields completed below. |
| `tpcn/excursion_neuron.py` | `c0bdece6b15009db4e2b7d69c3242be174b5de80` | Read E1/E2 config/state and E1 event paths (`48–160`, `252–278`, `294–463`, `534–690`, `730–787`); E2 mode, gate-independent scalar updates, and strict-future scheduling (`797–930`, `982–1095`). |
| `tpcn/event_runtime.py` | `f4aacb5d782f19e30fd9e562d56d62faefa9002f` | Full file, lines 1–294: local monotone time, finite deterministic queue, same-destination external-before-internal ties, bounded execution. |
| `tpcn/experiment_excursion_runtime.py` | `b4e074f0139f3fcfb59189c8313c934c551d6bcb` | Read event processing/emission consumption, lines 520–690; actual E2 emission is consumed/routed only after neuron return. |
| `tpcn/execution_ir.py` | `055fd89cc762850e261da46afa7f5a2b56ea7d1d` | Read IR boundary, lines 1–160; portable config/initial-state IR is not arbitrary live-runtime state. |

### Proposed derivation provenance (hand analysis only)

1. The Jacobian gives `−1±i`; `V=½r²` gives `dV/dt=−Rr²`, hence active
   radius `r=Ae^{-s}` and bounded disk invariance.
2. `Ae^{-s}sin(s)` has its first positive peak at `s=π/4` with factor
   `g=e^{-π/4}/√2`. Setting `θ=2g` makes the `A=4` first peak `2θ` and
   the `A=1` peak `θ/2`.
3. The oriented derivative is positive before `π/4`; the high fixture
   therefore has one rising root. The downward `q=θ/2` hysteresis root is
   followed by `r=q` at `s=ln(4/q)`. `q<θ`; `T_q<π`, so quiet reset occurs
   before a second positive half-turn. The one-shot latch independently
   suppresses duplicate events.
4. With maximum fixture HOLD 2 TU and one extra `α⁻¹` after the maximum
   quiet time, `T_life=2+T_q+1` bounds every frozen future fixture and leaves
   the maximal planned release time to reach quiet.
5. The smallest no-event margin is `θ/2` for the subthreshold fixture;
   half that margin gives the future strict state tolerance `θ/4`. These are
   analytic candidate bounds, not measured numerical errors or outcomes.

No calculations were run to generate trajectories or observations. The
interval and certification rules above are proposed future oracle requirements;
they were not executed in this design assignment.

### Validation and non-claims

| Procedure | Result |
|---|---|
| Read assigned contract, owner attachment, architecture/governance/prior design and current runtime source | Completed read-only; source identities and inspected extents above. |
| Hand derivations: equilibrium, eigenvalues, Lyapunov function, event lobe and radius/reset bounds | Proposed analytic derivation only; no execution. The published draft received a separate Luna-0 BLOCKED verdict; follow-up correction addresses four recorded gaps. |
| Candidate implementation, tests, solver, simulations, trajectories, trials, training, task efficacy, hardware | **NOT RUN**; prohibited by this assignment. |
| Original publication whitespace/scope check | PASS at the original baseline publication stage; exactly the two authorized deliverables were written, no tests run. Historical, not current status. |
| Follow-up correction scope/whitespace check | PASS locally; `git diff --check` clean and only the two authorized tracked Markdown paths are modified. Parent publication/fetch/clean verification pending; no tests run. |

The design does not claim recall, symbolic sequence memory, sequence order,
task efficacy, learning, prediction-error propagation, energy/utility,
delayed credit, hardware equivalence, ACP acceptance, core/default promotion,
integrated echo, or Luna-64. A bounded design only makes a separately
authorized mechanism experiment eligible for consideration.

## 9. Proposed next gate

The parent must publish the current two-file correction, then obtain a
separate **independent Luna-0 re-review** of the corrected report/handoff.
The earlier published revision was blocked on four points addressed in
§§4–6; no review outcome for this correction is claimed. Only after the
re-review may the owner/Luna-0 consider a separate bounded mechanism
authorization. No experiment follows automatically.
