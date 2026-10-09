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
non-finite state, invalid gate, counter exhaustion, or failed scheduling
precondition faults closed to the neutral state without emitting.

## 4. HOLD, RECALL, and event semantics

### 4.1 Gate and finite lifetime

`R=0` means HOLD; `R=1` means release permission. `R` multiplies the stable
flow only. In particular, `F(0)=0` for both values of `R`, so neutral + RECALL
cannot create motion or an event. The gate supplies no energy to the state:
under release, `r` decreases monotonically even while `y` temporarily grows.

An absolute episode lifetime starts at `start_time`. The predeclared
maximum-HOLD fixture is `H=2 TU`; the release return bound is
\[
T_q=\ln(4/q),\quad q=\theta/2.
\]
The proposed expiry is `T_life=H+T_q+1 TU`: the longest fixture HOLD, plus
the maximum active return time from any allowed state, plus one `α⁻¹`
relaxation interval. This gives every C0–C7 release fixture time to finish
before expiry and keeps a no-RECALL held state finite-lived. Expiry is
absolute from store, not renewed by duplicate cues.

On every addressed event, the future adapter must first settle local age
and any due quiet/expiry boundary, then validate/apply the event. At
`event_time >= start_time + T_life`, expiry equality preempts RECALL: invalidate
the episode generation, clear `X` to zero, suppress stale crossings and
reject the cue. The existing queue's external-before-internal same-time tie
rule is not changed; this episode-age precheck defines expiry precedence for
this proposed component. Invalid, late, over-budget, or stale-generation
events are rejected deterministically. Duplicate `R=1` cues are idempotent;
at most eight RECALL gate records (including duplicates) are accepted per
episode. A new store is rejected until the current episode is quiet or
expired.

### 4.2 Thresholds derived from the excursion

For a stored state `X(0)=(pA,0)` with `A=|x_store|`, `0≤A≤4`, release gives:

\[
x(s)=pAe^{-s}\cos s,\qquad y(s)=pAe^{-s}\sin s.
\]

The first positive-polarity output-coordinate peak occurs at `s=π/4`,
because `d(e^{-s}\sin s)/ds=e^{-s}(\cos s-\sin s)`. Its amplitude factor
is
\[
g=e^{-\pi/4}/\sqrt2.
\]
The event threshold is chosen as half the maximum first-lobe peak at the
declared state bound:
\[
\theta=(4g)/2=2g=\sqrt2e^{-\pi/4}.
\]
This is an exact proposed definition, not a measurement or a tuned outcome
threshold. The hysteresis/re-arm and quiet radius are both
`q=θ/2`: this makes the subthreshold control's peak exactly the reset
surface, keeps the quiet disk strictly inside the event surface, and gives a
finite reset radius. No decimal approximation is required to implement the
mathematical specification.

### 4.3 Event surface, direction, hysteresis, and one-shot rule

For `p≠0`, the oriented event surface is
\[
h(X)=p\,y-\theta=0,\qquad d(p\,y)/ds>0.
\]
The event is emitted only on an armed crossing from `h<0` to `h≥0` with
strictly positive directional derivative. A tangent touch is not a crossing.
For `p=0`, the episode remains neutral and has no event surface.

On crossing, transition `ARMED → REFRACTORY`, set `event_issued=true`, and
create exactly one proposed canonical excursion record with polarity `p`
and fixed normalized payload `p·1`. It is a neuron event, not a direct
RECALL response. The episode-level `event_issued` latch is never cleared
before quiet/expiry, so duplicate cues, a gate pause/resume, and a later
numerical recross cannot create a second event.

The hysteretic re-arm surface is `p·y=q`, crossed downward after emission.
The transition is `REFRACTORY → REARMED`; it only records that the excursion
has left the output band and does not clear `event_issued`. Quiet completion
occurs at the first inward crossing `r≤q`, then sets `(x,y)=(0,0)`, mode
`QUIET`, invalidates the episode generation, and permits a later independent
store. A non-event subthreshold release uses the same quiet completion.
Since `|y|≤r=q<θ` at quiet, reset cannot manufacture an event.

### 4.4 Required controls and exactly-one argument

* **Neutral + RECALL:** `A=0` is the invariant origin; `p=0`; no event.
* **Subthreshold + RECALL:** `A=1` gives a first peak `g=θ/2<θ`; no
  crossing; `r` contracts to `q` and quiet-reset occurs.
* **Supra-threshold held:** `A=4`, `R=0` leaves `(p4,0)` unchanged and
  silent until release or expiry.
* **Same state + RECALL:** `A=4` has first peak `4g=2θ`. The event surface
  is crossed once on the strictly increasing interval `0<s<π/4`, then the
  downward hysteresis surface is crossed before quiet completion. The radius
  reaches `q` after `T_q=ln(4/q)=ln(8/θ)=ln(4√2)+π/4`. The strict bound
  `T_q<π` follows from `ln(4√2)<2<9/4<3π/4` (`e²>4√2` and `π>3`).
  Thus the episode quiet-resets before a second positive half-turn can reach
  the event section. Equivalently later positive lobes, if the quiet reset
  were omitted, are attenuated by `e^{-2π}` and are below `q`, since
  `2e^{-2π}<1/2`; they cannot produce another crossing.
* For any `A≤2`, the first-lobe maximum is at most `2g=θ`. At equality it
  only touches the event surface with zero derivative; the directional
  crossing rule rejects it. For `2<A≤4` the first lobe crosses once before
  quiet. The C fixtures use `A=1` and `A=4`, with large analytic margins.

These are hand-derived consequences of the equations. No state trajectory
was evaluated or simulated.

## 5. Completion, numerical reference, and bounded future execution

### 5.1 Proposed event record and scheduler

At the first oriented crossing, the future adapter may represent the output
using the existing *shape* of a canonical excursion emission:
fresh source-local event ID, monotone source-local sequence, source,
timestamp, fixed payload, episode ID, and lineage ID. The event type is
`EXCURSION`. These are proposed fields; no current `ExcursionEmission`
constructor, mode transition, or runtime API is claimed to support this
field. The future adapter must preserve the envelope and routing identity
rules and use the repository's finite event queue.

Let `t*` be the certified continuous crossing time and `t_prev` the last
committed local event time. The logical output time is the least finite
binary64 timestamp no earlier than a certified upper bound on `t*`, and
strictly greater than `t_prev`. If positive `t*−t_prev` is below timestamp
resolution, choose at least `nextafter(t_prev,+∞)`; if that successor is
non-finite, overflow occurs, or the root interval cannot determine a unique
upward-rounded time within the solver bound, fault closed with no emission.
This is a proposed general candidate rule, not a claim that current E2
implements a general continuous-root scheduler. It is consistent with the
existing narrow E2 correction that uses `nextafter` when a positive re-arm
delay is unrepresentable. Propagation still follows existing causal edge
delays; no inline mutation, zero-delay recursive cascade, or global neural
tick is introduced.

### 5.2 Exact independent oracle and future numerical bounds

The independent mathematical oracle is the closed-form semigroup
\[
X(s)=e^{-s}
\begin{bmatrix}\cos s&-\sin s\\ \sin s&\cos s\end{bmatrix}X_0,
\]
with active time accumulated only across RECALL-enabled intervals. It is to
be implemented separately from any candidate adapter using outward-rounded
256-bit rational intervals for `π`, `exp`, `sin`, `cos`, and `ln`; it must not
call the candidate's propagation or event-root routine. On the required
domain, `0≤s≤T_q<4`; Maclaurin remainders after 128 terms are bounded by
`e⁴·4¹²⁸/128!` for `exp` and `4¹²⁸/128!` for `sin/cos`, each below
`2⁻¹⁶⁰`. Directed-rounding accumulation is included in the returned interval;
if interval width, root direction, or timestamp rounding cannot be certified,
the oracle reports unresolved rather than rounding to a desired outcome.
The `π` interval is obtained independently from Machin's identity
`π=16 atan(1/5)−4 atan(1/239)` with 128 alternating-series terms per
arctangent and its next-term remainder bound.
For `ln`, the reference uses range reduction to `[1,2)` followed by the
`2·atanh((u−1)/(u+1))` series with its geometric tail bound, also capped at
128 terms and failing closed if the bound is not met.

For each supra fixture, isolate the first crossing on `[0,π/4]` and the
downward re-arm crossing on `[π/4,π]` by interval bisection; isolate the
quiet radius by the closed-form `ln(A/q)` interval. Use at most 128 bisections
per crossing and 128 series terms per transcendental evaluation. Starting
event functions are strictly monotone on their declared brackets; interval
sign ambiguity at the cap is a failure, not a permissive threshold. There is
no ODE integration step and no global simulation timestep. State evaluation
is event-driven via the exact semigroup at local input, gate, section,
quiet, and expiry times.

The smallest no-event analytic margin is the subthreshold fixture's
`δ=θ−θ/2=θ/2`. A future numerical candidate must satisfy
`||X_candidate−X_oracle||₂ < δ/2 = θ/4` at every frozen checkpoint; this
leaves a strict half-margin for classifying the no-crossing control. The
independent oracle itself must certify a narrower interval than `θ/4` or
the check is unresolved. Event count and crossing direction are exact
discrete criteria; event timestamp must equal the certified upward binary64
conversion above, not merely fall within a chosen time tolerance.

Future deterministic fields to freeze before any separate authorization:
baseline/source hashes; IEEE-754 binary64 and rounding mode; parameter bit
patterns; event timestamps and tie order; store values; gate history; local
state and lifecycle records; root brackets/iteration counts; directed
interval endpoints; expiry/quiet generation; output ID/sequence/payload/
episode/lineage/timestamp; event-budget and queue results. No randomness is
needed. A second implementation must not share the candidate's propagator,
root solver, threshold helper, or mutable state.

Per episode the candidate accepts at most one STORE and eight RECALL records,
including duplicates; it schedules at most one crossing event, one re-arm,
one quiet completion, and one expiry. The local event budget is 16, including
accepted inputs and generated events. Queue-capacity failure applies
backpressure/fault semantics and cannot be reported as quiet success.
Episode lifetime is at most `T_life`; state, timer identity, episode number,
and event counters must not wrap in an active episode. Exhaustion invalidates
the episode and clears it without emission.

## 6. Unexecuted falsification protocol (C0–C7)

All items below are future tests only. The state/preload lists, intervals,
expected inequalities, event budgets and rules are to be frozen before any
separately authorized executable work. The task contract authorizes none of
that work here.

| Fixture | Frozen setup | Required observation / falsifier |
|---|---|---|
| C0 — neutral, no RECALL | `X=(0,0)`, `R=0`, then expiry. | No output; invariant neutral state; any motion/event falsifies the field/gate contract. |
| C1 — neutral + RECALL | `X=(0,0)`, set `R=1`. | No output and no direct gate response. |
| C2 — subthreshold held and released | `X=(±1,0)`, `R=0` through each declared HOLD checkpoint, then `R=1`. | HOLD exact; no oriented section crossing; finite quiet reset to neutral. |
| C3 — supra-threshold held | `X=(±4,0)`, `R=0` through pre-expiry observations and through the `H=2` fixture bound. | State remains fixed and silent while held; at the absolute expiry boundary the state clears and any simultaneous RECALL is rejected. |
| C4 — supra-threshold release | Same fresh `X=(±4,0)` and identical configuration, then `R=1`. | One correctly oriented crossing and exactly one canonical event, then re-arm/quiet/neutral; zero or multiple events falsify the proposal. |
| C5 — unequal HOLD duration replay | The same supra preload released after HOLD durations `{0,1,2} TU`. | Analytic active-time trajectories and crossing conversion are identical after release within the independently derived state bound; no age-dependent store drift. |
| C6 — ungated reference | Initialize the same state and set `R=1` from store time. | Matches the same analytic reference as C4 after its release origin; no extra integration/solver tick. |
| C7 — determinism, bounds, expiry, timing | Replay C0–C6 with exact same event histories; include duplicate RECALL, pause/resume, expiry equality, queue-capacity fault, and an event time where positive delay is below one ULP. | Bit-identical discrete lifecycle/event fields and deterministic numeric checkpoints; one bounded output at most; bounded return/expiry; every scheduled output timestamp is finite and strictly future. |

**Independent procedure:** compare a candidate adapter against the separately
written certified interval/closed-form oracle. Check neutral eigenvalues and
Lyapunov derivative algebraically, threshold maxima and crossing direction
from the formula, event order/count, radius invariant, the stated error bound,
and conversion to strict-future binary64 time. Failure, unresolved interval,
overflow, or exceeded event/solver bound is a fail-closed outcome, not a
passing sample. No plots alone, shared code path, outcome-tuned threshold, or
test-selected parameters are sufficient.

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
The fixed 16-event/128-bisection bounds are proposed for this candidate only.

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
series and interval rules above are proposed future oracle requirements;
they were not executed in this design assignment.

### Validation and non-claims

| Procedure | Result |
|---|---|
| Read assigned contract, owner attachment, architecture/governance/prior design and current runtime source | Completed read-only; source identities and inspected extents above. |
| Hand derivations: equilibrium, eigenvalues, Lyapunov function, event lobe and radius/reset bounds | Proposed analytic derivation only; not machine-checked or independently reviewed. |
| Candidate implementation, tests, solver, simulations, trajectories, trials, training, task efficacy, hardware | **NOT RUN**; prohibited by this assignment. |
| Whitespace/scope check | PASS; PowerShell found no trailing whitespace, and Git status showed exactly the two authorized untracked paths. No test suite run. |

The design does not claim recall, symbolic sequence memory, sequence order,
task efficacy, learning, prediction-error propagation, energy/utility,
delayed credit, hardware equivalence, ACP acceptance, core/default promotion,
integrated echo, or Luna-64. A bounded design only makes a separately
authorized mechanism experiment eligible for consideration.

## 9. Proposed next gate

After the parent performs the authorized documentation publication, the
exact published design and handoff require **independent Luna-0 review**.
Only after that review may the owner/Luna-0 consider a separate bounded
mechanism authorization. No experiment follows automatically.
