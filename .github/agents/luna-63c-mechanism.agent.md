---
name: "Luna-63C Nonlinear Excursion Mechanism"
description: "Build and verify only the isolated Luna-63C recall-gated excursion mechanism after the independent numerical certificate gate; no sequence echo, efficacy, ACP, or core promotion."
tools: [read, search, edit, execute]
agents: []
---

# Luna-63C — isolated mechanism execution

**AUTHORIZED / NOT EXECUTED — CERTIFICATE GATED.** The project owner has
authorized a bounded, isolated Luna-63C mechanism experiment. This contract
does not make implementation or fixture execution immediately eligible:
first prepare the independent numerical/mechanistic certificate described
below, then stop for a separate Luna-0 certificate review. Runtime
implementation and C0–C7 execution are prohibited until that review is
recorded as PASS and the exact frozen certificate/implementation revision is
entered into the follow-on execution record.

The only authorized scientific question is whether the reviewed two-state
system holds/suppresses output while `RECALL` is inactive and, when `RECALL`
permits traversal, produces the design-predicted excursion and canonical
event without `RECALL` acting as excitatory input. This is a mechanism test,
not a memory-order or sequence-recall test.

## Authority and immutable source pins

- Reviewed design: `3e7d31b9a527e908b21abee3766906084e7cd082`
- Latest design/review handoff: `a303ebb835b72fdd01c86df478431b8638aacbb4`
- Design disposition: **PASS WITH LIMITATIONS — design gate only**
- Main integration uses the exact documents from those source revisions.
  The main cherry-pick commits preserve their content and do not replace
  these provenance pins.
- The former `.github/agents/luna-63c.agent.md` remains the design-only
  contract and is not amended or superseded.

Read the two pinned design documents, this contract, the independent
numerical certificate decision, `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`,
the acceptance criteria, ACP-0008, and the cited current event/runtime
semantics before work. Do not consume Luna-63B work or results. Luna-63B
remains blocked on its own numerical prerequisite. Luna-63A supports only its
separately reviewed scalar HOLD result; it is neither an implementation
dependency nor evidence for this field.

## Exact reviewed model — do not substitute

State is `X=(x,y)`, in normalized state units, with invariant disk
`x²+y²≤16`; local time is TU and `R∈{0,1}`. Store takes only a predeclared
signed local fixture value, clips once to `x_store∈[-4,4]`, sets
`A=|x_store|`, `p=sign(x_store)`, and loads `X=(pA,0)`. There are no task
labels, symbol sequences, answer buffers, evaluator truth, or 63B inputs.

The exact frozen parameter point is `α=1 TU⁻¹`, `ω=1 TU⁻¹`; the vector field
is:

```text
xdot = R(-αx - ωy)
ydot = R( ωx - αy)
```

With these exact parameters:

```text
xdot = R(-x - y)
ydot = R( x - y)
```

For active time `s(t)=∫R(u)du`, the reviewed exact flow is:

```text
X(t) = exp(-s) [[cos(s), -sin(s)],
                [sin(s),  cos(s)]] X(t0)
```

`R=0` freezes both coordinates; `R=1` permits only this field. RECALL is a
binary gate change after old-gate settling, never an additive input/current,
impulse, state load, threshold change, phase reset, or direct spike command.
The candidate field is linear; its event/lifecycle adapter is hybrid.

Use exactly:

```text
g     = exp(-π/4)/sqrt(2)
theta = 2g = sqrt(2) exp(-π/4)
q     = theta/2 = g
h(X)  = p*y - theta
```

An output is eligible only at the first certified upward crossing of
`h(X)=0`, with certified positive `d(p*y)/ds`, `armed=true`, and
`issued=false`. The adapter commits one immutable canonical `EXCURSION`
record with payload `p·1`; a later downward crossing `p*y=q` re-arms but
does not clear `issued`. For `A≤2`, including the exact tangent at `A=2`,
there is no upward crossing. For `A>2`, the first lobe has one upward
crossing. Quiet is the first inward `r=q` boundary; for `A≤q`, commit
`QUIET_ENTRY` atomically at STORE without evaluating `ln(A/q)`. For `A>q`,
quiet active time is `s_q=ln(A/q)`. The absolute episode lifetime is
`T_life=H+T_q+1 TU`, with `H=2 TU` and `T_q=ln(4/q)`.

Preserve the design's terminal reasons, output persistence, generation/token
invalidation, internal-before-external equal-time precedence, admissible
timestamp reserve/settle/install order, clock domain `[0,2^20] TU`, and
upward-rounded binary64 boundary conversion. A crossing's mathematical root
state is distinct from its converted output timestamp. Its interval
endpoints must yield the same `ceil64`; the emitted time must be strictly
future and strictly before converted expiry. `nextafter` is only a candidate,
never a clamp or fallback.

The maximum accounting is immutable:

- 16 within-budget addressed input attempts;
- one recorded 17th `REJECTED_CAP_OVERFLOW` attempt, then closed ingress;
- 24 unique timer records;
- one output record;
- 42 total unique records maximum.

Do not change these limits. The overflow record's disposition is committed
before abort cleanup/READY; retain `terminal_reason=ABORTED` and any output
already committed. This accounting must be enforced, not merely reported.

## Stage A — certificate only; no runtime implementation

Before creating a candidate model, fixture runner, or event adapter, prepare
a standalone certificate from the exact equations above. The oracle must not
import, call, or share propagation, root, timer, threshold, conversion, or
lifecycle code with the future candidate. It may use hand derivation and/or a
separate rigorously bounded interval reference in
`experiments/luna63c/certificate/`; any certificate helper must be isolated
from candidate runtime modules and have independently justified rounding
and transcendental enclosures.

The certificate must establish, or explicitly fail to establish:

1. rest state and eigenvalue/stability facts;
2. the invariant disk and declared finite operating region;
3. `RECALL` at neutral state produces no motion/output;
4. subthreshold `A∈{q/2,1,2}` behavior, including exact `A=2` tangency;
5. supra-threshold `A=4` initial condition and release trajectory;
6. event surface, direction, uniqueness, and re-arm;
7. quiet/terminal condition and finite lifetime;
8. active-time to absolute-time mapping and strict-future/expiry ordering;
9. exact comparison/error semantics, including the design's strict
   `||X_candidate−X_oracle||₂ < theta/4` check for `A=1` checkpoints;
10. root/time interval refinement and conversion rules;
11. timer and unique-record bounds;
12. attempt-17 overflow and ingress closure.

Use the reviewed interval requirements: outward enclosures, precision from
256 through at most 1024 bits, no more than 128 bisections per root, and
transcendental remainder/directed-rounding bounds. These are maximum work
bounds, not a certificate by themselves. State comparisons, root existence,
direction, tangent rejection, event order, timestamp ceiling and resource
accounting are distinct claims. Unresolved signs/order/ceilings at a cap
mean **BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE**, not a pass.

Freeze all numeric comparison rules and expected event/output fields in the
certificate before implementation. Exact equality is used where justified;
otherwise use the design's derived bound or an independently justified
predeclared ULP/absolute-relative bound. Do not tune tolerances to candidate
output. If no defensible arithmetic/error bound is available, stop blocked.

The Stage A deliverable is a certificate report, any separately owned
certificate-only source, source pins, reproducible commands, and an explicit
pass/fail table. Then stop. Luna-0 independently reviews it; Stage B remains
locked until that review is recorded PASS against exact hashes.

## Stage B — conditional isolated implementation and fixtures

After the Stage A PASS, work only on an isolated branch rooted at the then
current main and only under `experiments/luna63c/`. Do not import or modify
production TPCN runtime modules. The experimental path is opt-in/disabled by
default; do not replace production neurons, alter defaults, edit ACPs or A01–
A15, remove Luna-62, or connect to sequence echo.

Implement the reviewed analytic/interval event-time strategy; do not introduce
a neural global timestep or arbitrary fixed-step solver. If a deterministic
integration method is unavoidable, it must be separately justified against
the reviewed design, have bounded error/step behavior, and demonstrate that
event categories are not step-size artifacts; otherwise stop for Luna-0
review rather than substitute it. Internal calculations are not neural
timesteps. Enforce the design's root isolation, `ceil64`, strict-future,
causal ordering, timer and 42-record rules.

Freeze and run the exact reviewed C0–C7 definitions and values; do not
reinterpret their names:

| Fixture | Reviewed setup and required result |
|---|---|
| C0 | Neutral `READY`, `X=(0,0)`, `R=0`, no STORE: no episode, motion, timer or output. |
| C1 | In `READY`, `RECALL(R=1)` then `RECALL(R=0)`: gate changes only; no state load, episode, motion or output. |
| C2 | Fresh `A∈{0,q/2,q,1,2}`; exact `A=q` symbolic boundary and certified representable neighbors. `A≤q` is atomic `QUIET_ENTRY`; `q<A<2` contracts quietly; `A=2` tangent/no event. |
| C3 | Fresh `A=4`, `R=0`; HOLD durations `{0,1,2}` and separate expiry-boundary case: held state, no output; expiry equality preempts same-time RECALL. |
| C4 | Fresh `A=4`, continuous `R=1` beginning by `t_store+H`, with at least `T_q` active release before expiry: one certified output, re-arm, quiet, and valid time certificates. |
| C5 | Same `A=4` release after HOLD durations `{0,1,2}` with uninterrupted `T_q` active release: compare active-time trajectories/root offsets; absolute timestamps shift and are independently converted. |
| C6 | Same initial state/release origin as C4 with `R=1`: compare to the analytic semigroup after active-time alignment. |
| C7 | Duplicate/alternating RECALL, RESET before/after commit, stale timer, re-arm/quiet tie, expiry equality, semantically invalid packet at valid expiry time, timestamp-invalid packet, overflow/post-abort ingress, output/expiry coalescence, near clock limit and below-one-ULP positive delay. Exact outcomes and fail-closed rules follow the reviewed report. |

The primary causal contrast must hold the exact same stored state, field
parameters, thresholds, timing, and output configuration constant; vary only
`R`. At least compare `A=4` held with `R=0` against the matched `R=1` release.
Do not interpret C0/C1 as sufficient evidence for the supra-threshold causal
contrast.

The controls must also make these individual claims explicit:

- Neutral + RECALL never emits and the neutral state remains neutral.
- A subthreshold state with RECALL permitted never crosses the canonical
  output surface.
- The same preloaded excursion-capable state stays output-quiet while held
  with `R=0`, and the matched `R=1` case yields the design-predicted event.
- The event is caused by the field crossing, not a direct RECALL command.
- After the intended event the declared quiet/terminal rule is observed;
  absence of later events over a short arbitrary observation window is not
  evidence of quiet.

Before any scientific interpretation, independently verify runtime
conformance for state bounds, event/timer ordering, equal-time precedence,
crossing direction/one-shot behavior, re-arm, quiet, overflow, output
persistence, unique-record accounting, and strict-future schedule. A
trajectory plot or output count cannot substitute for these checks. Preserve
failures, unresolved cases, commands, platform/interpreter/dependency pins,
and raw deterministic fixture outcomes in the execution handoff.

Perform at least two genuinely independent fresh executions/materializations
for deterministic replay. Do not duplicate one result artifact. Compare
event records, state traces/artifacts, canonical output identity/time and
record counts. Retain per fixture the implementation trajectory/result,
independent oracle/certificate, maximum state error, event-time error,
event-count agreement, and terminal-state agreement; state whether the oracle
is a rigorous closed-form interval reference or only qualitative.

Required regressions after Stage B:

1. focused Luna-63C mechanism tests;
2. numerical-certificate tests;
3. event-time/representability tests;
4. event-crossing/re-arm tests;
5. record-bound/overflow tests;
6. relevant E2/excursion regressions;
7. historical/core regressions required by this contract;
8. the full repository suite if shared/production-imported code is touched.

Shared/production imports or edits are not authorized; if they prove
necessary, stop and request Luna-0/owner review rather than proceeding under
this contract. No task efficacy, training, labels, sequence order/memory,
hardware equivalence, or ACP acceptance is in scope.
Report exact test counts and skips for every required regression family.

## Required scientific disposition vocabulary

The execution handoff must select exactly one, with evidence and limitations:

- **SUPPORTED — RECALL-GATED NONLINEAR EXCURSION** only if all primary causal
  and numerical gates pass;
- **PARTIALLY SUPPORTED** if gating is demonstrated but a bounded
  terminal/quiet or timing behavior remains incomplete;
- **NOT SUPPORTED** if neutral/subthreshold RECALL causes an output or the
  intended excursion fails;
- **BLOCKED** for uncertified numerical semantics, solver failure, bound
  violation, event-time ambiguity, or invalid provenance.

Even full support means only that a preloaded state can traverse this reviewed
field into a canonical excursion/output under RECALL gating. It does not
establish order encoding, sequence memory/replay, adaptive-time integration,
task echo, training, generalization, hardware equivalence, or production
architecture.

Do not modify protected historical evidence from Luna-53–58, Luna-60,
Luna-62, Luna-63A, or Luna-63B. Luna-63B remains
**LUNA-63B NUMERICAL ORACLE PREREQUISITE REQUIRED**. Do not create or
authorize Luna-64.

## Stop conditions and final gate

Stop without implementing/running the scientific fixtures if:

- the certificate has any unresolved required field, error bound, root/order
  proof or expiry/timestamp conversion;
- the exact reviewed semantics cannot be represented in the bounded runtime;
- any result requires changing an equation, parameter, threshold, bound, event
  rule, fixture or tolerance;
- a result depends on 63A implementation artifacts, 63B state/results, labels,
  sequence identity or task/evaluator information;
- the event queue/semantics require a production change or global neural
  clock; or
- resource, queue, timer, identity or timestamp capacity is exceeded.

After Stage B, publish the exact experimental branch revision and execution
handoff, then stop for **independent Luna-0 runtime/conformance review**. No
integrated sequence echo, Luna-64, ACP adoption, architecture promotion or
production/default change follows automatically.
