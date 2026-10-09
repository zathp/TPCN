# Luna-63B — bounded local predictive interpretation/state design

**DESIGN PREREQUISITE COMPLETE — INDEPENDENT REVIEW REQUIRED.**
**PROPOSED MODEL / UNEXECUTED.** No implementation or experiment authorized.
This is one candidate, not an amendment to ACP-0008 or the core. Fixed
predictive computation is sufficient for this narrowly proposed interpretation
component; predictive learning, error propagation between components and
integrated TPCN conformance are not established by it. Luna-0 must independently
decide whether this formulation satisfies the prerequisite before any separate
implementation/execution authorization. Rejection of that interpretation means
BLOCKED; do not substitute another candidate or enlarge the envelope.

## 1. Authority, identity and provenance

Assigned worktree: `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna63b`.
Branch: `experiment/luna63b-local-pcn-design`. Starting/design-source revision:
`e52098b2141a3f121f23b512e877783a64ef8baa` (owner-supplied clean baseline).
The agent's historical scientific baseline is
`8123147e04c6044d12023f541cf63130cdbb7dcc`, not the current checkout.
Contract is **v1.2**, at
`e52098b2141a3f121f23b512e877783a64ef8baa:workflow/ARCHITECTURE_CONTRACT.md`.
No distinct contract commit SHA is inferred from its version or blob.

OBSERVED: read the entire B agent; independent Luna-62 review first, then
the separate authorization's governing/source/B sections. That authorization
records published governance content revision
`e191cebfcd3a31cd4a1339fd8f445125c47e89ae`; its provenance follow-up is present
in the assigned baseline. This pin is documentary evidence, not a performed
Git ancestry check. Read worktree Git metadata: HEAD names the assigned branch,
and its loose branch ref contains the exact assigned baseline.
No main or other lane worktree content, trial results or artifacts is used.
Required governance lane summaries do not supply this model's constants,
HOLD law or scientific evidence.

OBSERVED: subsequently read all 1,157 lines of the owner's read-only attachment,
in ranges 1–180, 181–360, 361–540, 541–720, 721–900, 901–1080 and 1081–1157:
`C:\Users\Patrick\AppData\Roaming\Code\agentSessionData\00a4b25e-bb56-4501-ab4b-415f83f45089\attachments\050e3485-1c22-4408-b209-7245484d0137\Pasted text #1.txt`.
This is owner-provided context outside Git, not a claimed repository object.
No hash was computed; its exact path, line extent and owner-supplied identity
are the available provenance. The committed B contract takes precedence over
attachment-wide orchestrator/lane instructions. No other lane's branch,
scientific results, artifacts or contract was accessed. No claimed absent
attachment or incorrect-path lookup is part of this invocation.

**Publication status:** both deliverables are uncommitted edits. The exposed
tools have no execute/Git interface. Commit, push, fetch, remote verification,
diff/whitespace and clean-tree checks are NOT RUN. Publication SHA is unavailable,
not invented. The authorized publisher must pin the eventual design content
commit in a provenance-only follow-up to these same two files, identifying that
follow-up separately; a commit cannot honestly contain its own SHA.

Every source read is pinned by the exact starting tree plus path below. These
are Git tree selectors, not independently rehashed checkout/blob identities.
Historical blob identities in the review/authorization are inherited evidence
only; source verification remains pending publication checks.

| Source relative to repository root at `e52098b2141a3f121f23b512e877783a64ef8baa` | Read extent / role |
|---|---|
| `.github/agents/luna-63b.agent.md` | Entire; owned scope and envelope |
| `workflow/handoffs/luna-0-independent-review-luna62-20261009.md` | Entire, before authorization; independent gate, source pins, limitations |
| `workflow/handoffs/luna-0-luna63-mechanism-authorization-20261009.md` | 1–125, 155–171, 210–271; authority/source register/B/publication requirements, not other lane scientific input |
| `workflow/ARCHITECTURE_CONTRACT.md` | Entire; v1.2 A01–A15 and authority |
| `workflow/ARCHITECTURE_CHANGELOG.md` | 1–80; current governance/history |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | 1–130; current dependencies and gates |
| `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md` | 1–130, in sections; future verification requirements |
| `workflow/docs/architecture_proposals/README.md` | Entire; isolated branch versus promotion |
| `workflow/docs/architecture_proposals/ACP-TEMPLATE.md` | Entire; not an ACP created here |
| `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` | Entire; companion handoff schema |
| `workflow/docs/architecture_proposals/ACP-0008.md` | Entire; existing scalar x/z, decay/discharge, opt-in status |
| `tpcn/predictive_coding.py` | 1–300; scalar matching/error, not this vector interpretation |
| `tpcn/event_runtime.py` | 26–180; local time, bounded queue, equal-time priority |
| `Initial-Architecture-Attempts/TPCN_inspiration/wema_predictive_coding_docs/02_wema_formulation.md` | Entire; indexed smoothing |
| `Initial-Architecture-Attempts/TPCN_inspiration/wema_predictive_coding_docs/05_multiscale_wema.md` | Entire; indexed bank/weighted sum |

Directory listings were limited to this worktree's `workflow`, `workflow/docs/luna`
and `workflow/handoffs`; `.git` was read solely to follow this worktree's
administrative pointer to its HEAD/ref. The large-directory first listing and
several large-file reads were truncated; subsequent section reads cover the
extents claimed above, including the final acceptance-criteria hardware paragraph.

## 2. What is and is not being specified

HYPOTHESIZED: local, prediction-conditioned noncommuting event operators can
leave two bounded coordinates distinguishable at a later observation without
any output or external sequence buffer. INFERRED below: conditional algebra
supports that hypothesis in an unclipped, unexpired subdomain. Neither label
means OBSERVED retention, decoded order, replay, sequence memory capacity,
task efficacy or TPCN evidence from an arbitrary neural network.

Current `LocalPredictor` produces scalar predictions and matches the oldest
eligible keyed observation with explicit `observed - predicted` error. It does
not implement this F_PCN. WEMA prose/equations do not freeze a local event-time
peak/error/vector model. ACP-0008 provides scalar integration and a separated
output path, not these two encoding dimensions. The following added signed
peak rails, retained errors/predictions, vector coupling and finite identity
HOLD are **isolated experimental departures**, never relabeled existing APIs.

The candidate predicts the next signed capture delta **if the next presented
packet includes a given physical port**, from the opposite encoding coordinate.
It does not predict a desired symbol, answer or sequence position. Fixed weights
are an explicit prior, not fitted evidence of prediction accuracy.
Prediction residual causally changes the very next encoding update:
`innovation = delta - error/2`. The prediction and error cannot be removed
without changing the operator. No optimizer, trainer or evaluator participates.

### Architecture diagram and coordinate/WEMA rationale

```text
presented A/B signed packet (time/ID admission only)
       |
       v
four independent polarity peak rails -- capture delta d_j
       |                                      |
       |                           old q_j --> subtract --> epsilon_j
       |                                      |
       +-------------------------------> a_j = d_j - epsilon_j/2
                                              |
                      A deposit --> clip z_1   B deposit --> clip z_2
                                              |
                             next q_A = z_2/4; next q_B = z_1/4
                             (two records for subsequent information)

elapsed Phi: z identity until absolute expiry; peaks/predictions expire locally
output/excursion/decoder/recall: ABSENT (no downstream computational connection)
```

z_1 receives A interpretation; z_2 receives B interpretation. Each supplies
the other port's predictive context, so they are not duplicate scalar sums.
In vector notation the fixed predictor is
`q = [[0,1/4],[1/4,0]] z`; only two gain operations, not a general network.
The correction is an equal-weight blend of observed delta and prior prediction,
`a_j=(d_j+q_j)/2`, when matched. Linear unsaturated predictive coupling is
already noncommutative; the only nonlinearities are peak max and hard clipping,
chosen for bounds, not a hidden nonlinear order network.

Connection to WEMA is limited and explicit: this is an event-driven,
prediction-weighted deposition accumulator with `dz/dt=0` between inputs,
`z(t+)=clip_4(z(t-)+a)` at impulses, and absolute lifetime reset.
It is **not** the historical normalized `y_n=alpha*x_n+(1-alpha)*y_(n-1)`
or its multiscale bank. The proposed accumulator has fixed zero inter-event
leak, not adaptive leak and not an assumption that another lane succeeds.
Adding a positive or switched leak would change this freeze and require new
authorization. Identity retention is a named experimental departure from
ACP-0008's positive-decay scalar integration; no historical WEMA equivalence
is claimed. The attachment's WEMA direction is addressed without inventing
existing local equations or expanding the one-candidate envelope.

## 3. Domains and complete persistent state budget

Amplitude units: dimensionless normalized input/state units (SU).
Time unit: local TU, not seconds or a global neural tick. Lawful local event
times are dyadic multiples of `1/16 TU` in `[0,48]`; irregular scheduling is
permitted; admitted inputs are in `(0,47]`, leaving a final input-free TU
before lifetime expiry. A physical sender's propagation, if ever introduced, must precede
receipt by positive delay; this one-compartment assay assumes presented arrivals
only and tests no routing. Local timestamps are not an external global step.

| Persistent scalar | Count | Bound (SU) | Role / reset |
|---|---:|---|---|
| `p_A+`, `p_A-`, `p_B+`, `p_B-` | 4 | each `[0,1]` | Independent positive/negative peak magnitudes |
| `d` | 1 | `[-2,2]` | Latest processed port's signed capture delta; reused scratch for A then B |
| `q_A`, `q_B` | 2 | `[-1,1]` | At most two outstanding numeric predictions, one per fixed port |
| `epsilon` | 1 | `[-3,3]` | Latest processed port's explicit residual; reused A then B |
| `z_1`, `z_2` | 2 | each `[-4,4]` | Retained encoding, not output or diagnostic metadata |
| **Total** | **10** | | No other persistent amplitude/vector coordinates |

Transient old-state reads, incoming amplitudes, residuals and arithmetic
intermediates are not retained after a packet. `d`/`epsilon` are last-local
values, not occurrence lists. For a simultaneous two-port packet both update
increments use frozen old predictions; the two scalar scratch fields are
overwritten A then B. Diagnostic copies are downstream only.

Bounded computational metadata, separate from amplitude-coordinate roles:
one local timestamp in `[0,48]`; three deadline registers in `[0,48]` with valid
bits (peak, prediction, generation); two prediction-valid bits; two matched
status bits for the latest packet; one generation tag fixed to `1` (8-bit);
one last-admitted packet ID in `0..32` (8-bit); active/expired/fault enum.
No per-port last timestamp, occurrence link, topology, recurrence queue or FIFO.
No ID is used as a feature, coefficient, expected answer or symbol selector.
Packets have generation 1 and IDs `1..32` strictly increasing; IDs need not
encode a symbol or consecutive index. Reject duplicate/decreasing IDs and
late times; fault on exhaustion, invalid bounds/nonfinite values or an
unannounced second packet at the same timestamp. No automatic wrap/retry.
This deliberately does not offer arbitrary retransmission deduplication.
Same-input-time detection reuses the shared peak timer: before settlement,
if peak-valid and `peak_deadline-1/2 == incoming_time`, reject the second
packet. Input cutoff 47 ensures that deadline encodes the previous input time
exactly, without adding a last-event timestamp coordinate. An expired peak
cannot conceal an equal-time previous input because its TTL is strictly positive.

At most 32 admitted input packets and at most three live local expiry tokens,
one per role, with replacement rather than accumulating stale tokens.
An expiry performs no encoding increment. Budgeted input handling and at most
96 expiry firings make total computational work at most 128 handlers/instance.
External observation is read-only, never a computational event.
Generation lifetime is absolute, not refreshed: expiry at `48 TU`.
Only one generation ever runs in an instance; a fresh instance is required
after expiry/fault. No retained cross-instance state or surviving local work.

## 4. Immutable initialization and elapsed evolution

Initialization manifest is precisely this proposed document at its eventual
published content revision: all ten scalars `+0`; local time 0; generation 1;
last ID 0; ACTIVE; peak deadline invalid; two valid predictions `q_A=q_B=0`,
shared prediction deadline `12`; generation deadline `48`. Matched bits false.
Constants: peak lifetime `1/2`, prediction lifetime `12`, z bound `4`,
predictor gain `1/4`, error correction `1/2`, horizon `48`, packet budget `32`.
They are rational design choices for simple bounded arithmetic and a finite
assay, not selected by observed separation or another lane's outcomes.
No seed, learned checkpoint, dataset or opaque initialization.

For elapsed time `h>=0`, `Phi` is identity on z while active and before 48.
Peak expiry at or before the destination time clears all four rails and d,
invalidates the peak timer, and **does not feed release into z or prediction**.
Prediction expiry clears q and its valid bits, invalidates that timer; it
does not fabricate an observation/error. Epsilon is retained until the next
input or generation reset. Generation expiry clears all ten scalars, bits and
timers, sets EXPIRED and prevents any further input. Fault performs the same
cleanup with FAULT status. Invalid deadline registers are canonically zero.
Generation tag and last admitted ID remain bounded admission metadata;
the cleared amplitude state cannot be revived.

Reject nonnumeric/nonfinite times before deadline arithmetic. Every handler
rejects further input if already FAULT/EXPIRED without changing
that terminal status, then checks `t>=48` before any active capture.
Otherwise settle all due deadlines with
`deadline<=t`, generation before prediction before peak. This equality policy
is proposed, not `LocalPredictor`'s existing expiry-at-equality policy (which
allows a match). Scheduled timers and lazy settlement must give the same state.
Computational handlers advance the local timestamp to their due/arrival time;
late packets fault. Fault at a late packet retains the already committed
timestamp rather than rolling it back.
Repeated read-only observation computes Phi on a copy, never refreshes a
timer or changes the computational timestamp/state.

**HOLD is independently specified:** after the final presented LISTEN arrival,
there are no input events. z remains identical until its absolute generation
expiry. LISTEN/HOLD labels and observation time are evaluator descriptions,
not mode commands or leak gates supplied to F_PCN. Prediction/peak expiry
continues independently during HOLD. No recall, release cue or output exists.

## 5. Packet capture and exact event update order

A/B are fixed causal input ports. One externally presented timestamp packet
may contain zero, one or both ports. For each present port it contains at most
one positive magnitude `v_j+` and one negative magnitude `v_j-`, each `[0,1]`.
Missing polarity means zero. A present zero-amplitude port is a real
observation; an absent port is not. Opposite polarities at the same time are
captured on separate rails; neither overwrites/cancels the other peak.
Same-polarity simultaneous multiplicity is outside the packet envelope.
An implementation must not silently add an arrival aggregator/order buffer.

1. Validate time, packet/generation/ID/bounds; settle Phi/expiry before capture.
   Invalid input faults rather than returning a partial successful generation.
2. Freeze pre-packet z, q, prediction-valid bits and peak rails.
3. For each present port j, set `p_j+ := max(p_j+,v_j+)`,
   `p_j- := max(p_j-,v_j-)`. Other port rails stay unchanged.
   Capture replaces a smaller magnitude only; smaller arrivals do not lower
   a held peak. Define signed held input `r_j=p_j+-p_j-` and
   `d_j=r_j(new)-r_j(old)`. Positive means increased positive/net excitation.
   Both rails remain inspectable even when their net/delta is zero.
4. Clear both latest-packet matched bits first. If a valid q_j was issued before this packet and `t<prediction_deadline`,
   match that port's observed d_j once and set `epsilon_j=d_j-q_j`,
   `a_j=d_j-epsilon_j/2=(d_j+q_j)/2`. Record matched status.
   If invalid, set `epsilon_j=0`, unmatched status, and `a_j=d_j/2`;
   this is a declared nonpredictive fallback, not evidence of a resolved
   prediction. Set absent-port increment a_j to zero, with no residual.
5. `z_1(new)=clip_4(z_1(old)+a_A)`;
   `z_2(new)=clip_4(z_2(old)+a_B)`, where
   `clip_4(u)=min(4,max(-4,u))`. Both increments use pre-packet q.
   No within-packet A-to-B feedback; scratch d/epsilon are overwritten in
   fixed A-then-B port order, skipping absent ports.
6. Consume matched records and explicitly supersede every other old prediction.
   Issue exactly two new predictions:
   `q_A=z_2(new)/4`, `q_B=z_1(new)/4`, valid until `min(t+12,48)`.
   Target keys are the physical ports; target value is that port's next
   capture delta, available only on a subsequent packet. A record can be
   superseded by another-port packet before its target arrives; report this
   honestly, not as a correct prediction or FIFO match.
7. Refresh the **shared** peak deadline to `min(t+1/2,48)` for a packet with
   any present port. Prediction deadline replacement and peak replacement
   each keep only one live expiry. Commit last ID and local time.

Empty/no-port packets are not admitted inputs and cannot refresh deadlines;
use passive observation for the no-input control. A neutral but present
port can produce prediction-conditioned interpretation from nonzero prior z;
that effect must not be mislabeled input energy, a new symbol or spontaneous
output. Simultaneous equal +/- may similarly leave zero delta yet a nonzero
prediction-conditioned increment. The polarity control measures this explicitly.

`F_PCN` is exactly steps 3–7, with allowed causal inputs only this packet's
port presence/amplitudes, prior peak/q/valid state, prior z and local expiry
status. Delta/error are derived locally. Time and ID only enforce lifecycle/
admission, never choose neural coefficients. The predictor reads retained
encoding, makes a subsequent-information numeric prediction, exposes residual,
and uses that residual to change interpretation. Removing q/error reduces
the unclipped, independently captured-delta operators to commutative half-delta
accumulation (not a global claim about saturation/overlapping peaks); this is more than
renaming a scalar matcher. It is still only a **proposed fixed predictive
interpretation**, not a demonstration of useful learning or neural recall.

## 6. Noncommutativity, clipping and lifetime limits (algebra only)

For packets with one port each, intervening peak expiry, valid predictions,
and no clipping, write `x=z_1,y=z_2`, `c=1/8`, `a=d_A/2`, `b=d_B/2`.
The predictor invariant q_A=y/4, q_B=x/4 holds initially and after every input:

`T_A(x,y)=(x+c*y+a,y)`

`T_B(x,y)=(x,y+c*x+b)`.

Then

`(T_B o T_A - T_A o T_B)(x,y)=(-c*b-c^2*x, c*a+c^2*y)`.

At zero initialization with unit positive inputs, a=b=1/2 and the difference
is `(-1/16,1/16)`, exact norm `sqrt(2)/16`, from algebra, not a simulated trace.
For AAB versus ABA, subtracting the composed maps at zero gives
`(-c*b-c^2*a,c*a)=(-9/128,1/16)`.
For ABA versus BAA (same final A), the corresponding difference is
`(c^2*a-c*b,c*a)=(-7/128,1/16)`.
All intermediate coordinates for these short compositions are nonnegative
and at most `9/8`; hence clip_4 is inactive for these proofs. Sign reversal
negates the complete operators' states in the same unclipped domain.
These are conditional analytic conclusions, not observed numerical outcomes.

With expired predictions c becomes zero on that event; after overlapping
peak captures d need not equal presented amplitude; with clipping, the full
piecewise F above applies and the affine proof must not be extrapolated.
Saturation can erase distinctions; finite dimension/precision/lifetime
precludes an unbounded injective order encoder. No noise is permitted.
Phi is identity on z throughout eligible HOLD, so this source of distinction
is persistent noncommuting dynamics, not post-input leak recency. Count and
port-magnitude effects coexist and require controls.

## 7. Frozen future protocol — no trials here

All instances start from the exact manifest. Inputs below are arrivals,
not external order/answer lists consulted by computation. A symbol denotes
its fixed port present with magnitude 1 and positive polarity unless stated.
No ABC/CBA: C is outside this two-port envelope.

| Comparison / control | Arrival times (TU) | Purpose |
|---|---|---|
| AB versus BA | slots `1,4` | Counts and total magnitude matched; final-symbol/recency confounded alone |
| AAB versus ABA | slots `1,3,6` | Counts matched; unequal intervals; final symbol differs |
| ABA versus BAA | slots `1,3,6` | Counts matched and final port/amplitude/time A at 6 matched; earlier recency still possible in leaky control |
| AA versus A | AA at `1,6`, A only at `6` | Explicit count/magnitude confound, not pure order |
| AA versus AA_late | AA at `1,6`; AA_late at `5,6`, all unit amplitude | Equal count/magnitude with changed timing; expose peak/expiry and recency |
| AA_half versus A_unit | two A(+1/2) at `1,6`; one A(+1) at `6` | Total presented magnitude matched but counts differ; no pure-order claim |
| AB versus A-only / B-only | singles only at `4` | Count/port-exposure confounds, not evidence of order |
| No input versus zero inputs | no input; zero-present A at `1`, B at `4`; also A at `1,3,6` | Zero state and no fabricated evidence; inspect residual/status |
| Identical histories | every listed history repeated 3 fresh times | Deterministic replication, not independent samples |
| Polarity controls | AB/BA, AAB/ABA, ABA/BAA each repeated with both negative, A positive/B negative, A negative/B positive | Equal magnitude, frozen sign assignments in each pair |
| Simultaneous +/- capture | A carries +1 and -1 together at `1`; B likewise at `4`; repeat swapped ports | Separate peak signs, zero net, no invented tie ordering |
| Peak hold/expiry control | A(+1) at `1`, A(+1/2) at `5/4`; paired isolated A(+1/2) at `5/4`; inspect at `3/2,7/4` | Smaller arrival cannot overwrite larger rail; refreshed expiry equality at 7/4 clears |
| Prediction expiry control | A at `1`, B at `13` | Expiry equality invalidates old prediction before B; no affine-proof claim |
| Bounds/fault control | 32 packets at times `1+k`, k=0..31, alternating ports A first, IDs 1..32; separately append unlawful ID 33 at 33 | Clipping, bounded work, ID/budget exhaustion and fault cleanup; no separation selection |
| Admission fault controls | separate fresh instances: A at 1 ID 1 then B at 2 ID 1; A at 1 ID 1 then B at 15/16 ID 2; A at 1 ID 1 then a separate B packet at 1 ID 2 | Duplicate/decreasing ID, late arrival, and same-time second-packet faults, no buffering |

IDs are monotonic opaque transport IDs, not a runtime history index; rename
each short fixture's IDs by an order-preserving injection within 1..32 as a
future non-interference check (use 2,4,6 for the three-input fixtures).
Budget/exhaustion fixtures retain their fixed IDs.
All matched pairs share slots, magnitudes, initialization and measurement
times. Externally presented histories may be fixtures for input and oracle
measurement only. They never become F_PCN arguments, lookup tables or replay
computation.

Also record immediate post-commit encoding at each primary pair's shared final
input time: 4 for AB/BA and 6 for AAB/ABA and ABA/BAA; this is read-only
measurement, not an added input cue. Immediate margins use the same criterion.
Shared end-of-LISTEN observation anchor is `L=8 TU`, even for shorter lists.
Fixed delay set is `H={0,2,8,24}`; observe z at `L+H`, with diagnostic timing
sensitivity points `L+H-1/16`, `L+H+1/16`. All are after LISTEN and before 48.
Late-expiry probes at `48-1/16,48,48+1/16` require identity then zero/EXPIRED;
post-expiry observation is permitted although inputs are forbidden.
Matched pairs always use the same anchor/delay/offset. Survival is asserted
only over this finite delay set and before expiry, never indefinitely.

### Scalar controls, not a second model candidate

Run isolated scalar aggregate **controls only**, no extra coordinates in the
candidate. Same packets, peak/delta extraction, budget and reset, SU bounds 4:
`s(new)=clip_4(s(old)*exp(-(t-t_old)/4) + (d_A-d_B)/2)`
at input arrivals; at observation use the same elapsed exponential. Here A/B
weights +1/-1 are fixed port sensitivities, not labels. This leaky scalar can
distinguish AB/BA and even same-final-symbol permutations because earlier
weighted evidence decays differently. It is not a known-insufficient order
baseline. Its equation is an experimental comparison, not a WEMA equivalence.

Commutative/no-leak control:
`s(new)=clip_4(s(old)+(d_A-d_B)/2)`, Phi identity before expiry.
In the unsaturated primary fixtures this is a weighted sum independent of
permutation. Also report diagnostic raw total count, sum of magnitudes and
signed port totals, evaluator-only; do not feed them to either computation.
All control measurements and their distinctions must be reported, including
scalar recency effects and clipping; candidate separation alone is not an
advantage claim. No-leak saturation is not globally commutative.

### Metrics and predeclared criteria

Proposed initial platform: Windows x64, CPython 3.12.x, IEEE-754 binary64,
round-to-nearest ties-to-even, no fused/reassociated update arithmetic,
canonical +0 resets. Exact patch/build identifiers must be frozen by a
separately authorized future executor before outcomes; a different numerical
platform requires new freeze/authorization, not relaxed tolerances.

For each history w and observation t, `Z_w(t)=(z_1,z_2)`.
Euclidean distance `D(u,v;t)=sqrt(sum_i (Z_ui-Z_vi)^2)`.
Within-identical-history variation
`W(t)=max_w,max_repeats D(w_r,w_s;t)`.
Between-pair separation is D; margin `M=D-2W`.
Timing sensitivity `S_w(t)=max_{eta=+/-1/16} D(Z_w(t),Z_w(t+eta))`.
Report D/M for every pair/delay/polarity; count-confounded cases are separate.
No sequence decoder, learned boundary, threshold crossing or recall score.

Before any execution, proposed all-or-nothing criteria:

* Three repeats on the fixed platform have exact bitwise equality of all ten
  coordinates **and** computational metadata at corresponding input/expiry
  boundaries and observations. W=0 exactly, not just within tolerance.
* Independently derived rational-equation oracle for this dyadic candidate
  must match each coordinate to `1e-10 + 1e-12*abs(exact)` SU; status/IDs/
  deadlines/matching and reset are exact. Distance oracle tolerance `1e-9 SU`.
  The oracle must be independently authored, not import the future model.
* Primary AB/BA, AAB/ABA and same-final ABA/BAA require `M>=0.04 SU` for
  every H and listed polarity assignment. Negative or invalid outcomes remain
  failures, never replace constants/fixtures to improve separation.
* z is bitwise unchanged over all pre-expiry HOLD/delay/timing-offset points
  in each primary instance; S=0 exactly. At 48, all ten coordinates zero,
  expired status exact; no surviving match/token or state revival.
* No-input and zero-present histories from zero have exact zero encoding;
  separate rails/matching, peak/prediction equality expiry, bounds and fault
  controls obey their specified equations/status. No-leak matched aggregates
  agree within `1e-10 SU`; count-confounded results are not order support.
* Truth swap and observer off/slow/full checks preserve exact computational
  state; ID-renaming preserves it modulo the declared last-ID renaming.
  Error/residual influence must be checked against the
  equations; separation without correct prediction/error causality fails.

Tolerance derivation is independent of prospective outcomes: clipping/max
are nonexpansive; the unclipped one-packet map's infinity-norm Lipschitz
constant is at most `9/8` (simultaneous ports included). With binary64 unit
roundoff `u=2^-53`, bounded operands and the stated straight-line operations,
a conservative local error allowance is `64u SU` per packet. Through at most
32 packets, the bound is `64u*((9/8)^32-1)/(1/8) < 3e-12 SU`, before an
additional conservative rounding allowance for independent diagnostics.
Thus `1e-10` absolute is deliberately larger than this equation-rounding
bound yet many orders below the nontrivial `0.04` margin. Dyadic time/deadline
comparisons are exact. The future leaky scalar oracle needs independently
bounded high-precision exponential error (proposed 80-digit Decimal oracle,
absolute+relative `1e-10+1e-12*abs(exact)`); none is executed here.
A platform unable to establish these bounds fails this freeze.
No noise/draws. Any future noise requires a new authorization freezing draws,
bounds and margin versus variation.

## 8. Computational/diagnostic boundary and non-interference plan

Computational fields are exactly the ten coordinates, local timestamp, three
deadlines/valid bits, prediction/match bits, active/fault state, generation,
last ID, and current input packet (port presence, two signed magnitudes per
port, arrival time, generation, ID). Constants/initial manifest are immutable.
No external length, position, truth, sequence ID, oracle, final-answer index,
global timestep, reservoir, occurrence chain or history buffer is accessible.

Diagnostic-only fields: fixture names and presented sequence descriptions,
oracle states, observer snapshots/copies of computational fields, labels
correct/swapped, D/W/M/S, count/magnitude/port totals, matched/superseded/
expired counts, clipping indicators, comparison classification, hardware
estimates and publication checks. Logging may discard/drop records; it cannot
alter admission, timers, resource decisions or arithmetic.
Every actual future field not in this enumeration requires a reviewed freeze
update before execution.

Future non-interference test: identical packets/init, evaluator truth correct
versus deliberately swapped versus absent; capture enabled versus entirely
off versus full/slow diagnostic sink. Compare exact computational states and
local expiry work at all corresponding boundaries. Observer obtains copies
after commits or Phi-on-copy; it has no mutation/backpressure callback.
ID-renaming cannot change encoding/predictions/errors, though last-ID metadata
changes by the declared renaming. Oracle lives outside computation.
No evaluator feedback, expected-answer lookup or fixture-based replay.

## 9. Architecture and hardware boundaries

| Clause | Proposed preservation / limitation |
|---|---|
| A01 | Input/due-local-expiry only; no tick or all-neuron loop |
| A02 | Explicit Phi/F, local time, finite reset; algebraic order dependence weaker than ordered recall |
| A03 | Presented causal arrivals only; no intercomponent routing claim or instantaneous remote access |
| A04 | One compartment/two ports; no topology; declared packet/token/ID budgets |
| A05 | No spatial reservoir or hidden neural network |
| A06 | Numeric subsequent-delta predictions and explicit residual affect encoding; fixed computation only; remote error propagation capability remains a separate integration requirement |
| A07 | Fixed local state/current arrival only; no trainer, global statistics, truth or future input; learning absent, not demonstrated |
| A08 | Ten bounded SU scalars, clipping, three timers, 32 inputs, finite IDs/lifetime/fault; saturation may destroy order separation |
| A09–A11 | No energy, utility, reward or eligibility implementation/test; assay does not replace these capabilities |
| A12 | Two coupled encoding operators; ten pathways not required |
| A13 | No learned gate; port presence is causal input gating, optional-gate freedom preserved |
| A14 | No structural mutation; supported direction unchanged, neither implemented nor disproved |
| A15 | Qualitative burden only; no FPGA/FPAA/software equivalence |

Hardware burden: ten bounded registers, sign-separated peak compares, additions,
binary gain shifts, clips, valid/status/ID bits and three deadline registers/
local expiry roles. Fixed-point FPGA mapping is plausible, but sufficient
precision, timer realization, rounding and margin preservation are unverified.
FPAA/hybrid would need independent signed peak holds, coupled analog state,
finite lifetime/reset and drift/precision analysis; ideal identity HOLD is not
physical retention evidence. Binary64/dyadic convenience is a proposed
reference precision, not a core or all-analog architectural mandate.
Energy cost, physical joules and usefulness are not measured.

## 10. Checks, pending ownership and stop

OBSERVED checks: documentation/source reads; branch/ref metadata reads; creation
of only the two authorized Markdown deliverables using apply_patch.
INFERRED: bounds and conditional composition algebra above.
HYPOTHESIZED: the frozen future protocol would support finite state separation.
All scientific commands, traces, simulations, trials, scoring, training,
parameter search and hardware runs: **NOT RUN**. No tests added or passing.

Pending, only if separately authorized: independently authored equation oracle;
focused event ordering/local-time/late-ID tests; neuron separation/no-output
checks; predictor matching/supersession/expiry and residual-causality checks;
peak polarity/capture/equality expiry; z clipping/reset/state-budget regression;
deterministic replay, finite-delay and observer/truth non-interference.
Future production changes are not authorized; if a separate task ever touches
production, its full regression suite is required in addition to focused checks.

Independent Luna-0 must verify equations, update order, scalar/metadata bounds,
predictive interpretation/locality, controls/confounds, tolerance derivation
and initialization/source/publication provenance. No independent review is
performed here. Publisher must complete documentation Git checks/publication.
Future implementation/test owner is **not assigned by this handoff**.
No automatic successor, ACP, canonical mutation, task efficacy, integrated echo,
Luna-64, architecture promotion, decoder or sequence-memory claim. Stop.
