# Luna-0 — Luna-63C isolated mechanism authorization

**AUTHORIZED / NOT EXECUTED — CERTIFICATE GATED.** The project owner requested
a bounded isolated mechanism experiment based on the independently reviewed
Luna-63C design. This governance record authorizes certificate preparation
only at this time. Implementation and C0–C7 fixture execution are blocked
until the certificate receives an independent Luna-0 **PASS**. The later
mechanism execution remains on a separate isolated branch and requires a
final independent Luna-0 review.

## Design evidence integrated

The narrowest evidence-preserving disposition was **CHERRY-PICK REVIEWED
DESIGN EVIDENCE**. The source branch contains only the design report and
handoff across these three commits:

| Source commit | Evidence | Source file scope |
|---|---|---|
| `a1a7d377a0f48af750fbfe6da62fe54179bf833b` | Original design and provenance handoff | Two Luna-63C Markdown documents |
| `3e7d31b9a527e908b21abee3766906084e7cd082` | Four-review-finding correction | Same two documents |
| `a303ebb835b72fdd01c86df478431b8638aacbb4` | Independent design review handoff | Handoff only |

The main integration cherry-picked these exact commits, in order, producing
integration commits `5520ccc`, `a0d4c1a`, and `fe33a96`. The reviewed source
pins remain the branch SHAs, not their new cherry-pick object identities:

- **Reviewed design SHA:** `3e7d31b9a527e908b21abee3766906084e7cd082`
- **Latest handoff SHA:** `a303ebb835b72fdd01c86df478431b8638aacbb4`
- **Independent design disposition:** **PASS WITH LIMITATIONS — design gate
  only**, no design-gate blocker, no implementation or experiment authorized
  by that review.

The earlier `a1a7d37` design review was BLOCKED and is superseded only by the
corrected `3e7d31b` design review. The final design review confirmed the exact
reviewed revision. The pinned design and handoff are now on `main`; the old
design contract remains design-only and unchanged.

## Exact frozen intervention

The equations and parameters below are transcribed from §§3–5 of the pinned
design; this is not a new model:

```text
α = 1 TU⁻¹
ω = 1 TU⁻¹
R ∈ {0,1}

xdot = R(-αx - ωy)
ydot = R( ωx - αy)

X(t) = exp(-s) [[cos(s), -sin(s)],
                [sin(s),  cos(s)]] X(t0)
s(t) = ∫ R(u) du

g     = exp(-π/4)/sqrt(2)
theta = 2g = sqrt(2) exp(-π/4)
q     = theta/2 = g
h(X) = p*y - theta
```

`X=(x,y)`, `x²+y²≤16`; STORE clips the predeclared local fixture state once
to `x_store∈[-4,4]`, sets `A=|x_store|`, `p=sign(x_store)`, and loads
`X=(pA,0)`. `R=0` exactly freezes the whole field; `R=1` allows only the
reviewed field. A canonical output is committed at the first certified
upward `h=0` crossing only when `armed=true`, `issued=false`, and
`d(p*y)/ds>0`; its payload is `p·1`. The first downward `p*y=q` crossing
re-arms but does not clear `issued`. Exact `A≤2` has no upward crossing,
including tangency at `A=2`; `A>2` has one rising first-lobe crossing.
Quiet is first inward `r=q`; `A≤q` commits `QUIET_ENTRY` at STORE without
evaluating `ln(A/q)`. For `A>q`, `s_q=ln(A/q)`. Fixed lifetime:
`T_life=H+T_q+1 TU`, `H=2 TU`, `T_q=ln(4/q)`. Clock domain and certified
binary64 conversion follow the pinned design.

The required maximum is **16 within-budget attempts + 1 overflow record +
24 timers + 1 output = 42 unique records**. This is a hard cap, not an
expected or measured count. The experiment is not a memory-order test.

## Staged authorization and gate

### Stage A — authorized now: numerical/mechanistic certificate only

Luna-63C may prepare a standalone certificate and separately owned
certificate-only oracle material. It must not implement the candidate runtime
or run C0–C7 yet. The certificate must be independent of the future candidate
implementation and address all twelve requirements in
`.github/agents/luna-63c-mechanism.agent.md`: rest, stability, bounded region,
neutral RECALL, subthreshold behavior, excursion initial condition, event
surface/direction, quiet/terminal behavior, strict-future event time, record
budget, timers, and overflow.

Use only the reviewed event-aware closed-form/interval method: outward
enclosures, 256–1024-bit precision, at most 128 bisections per root, rigorous
transcendental remainder and directed-rounding bounds. State tolerances do not
prove event/timestamp categories. Freeze the numeric comparison rules before
any implementation. If the certificate cannot bound a required value or
ordering, record **BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE**; do not
implement the experiment.

Luna-0 must independently review the exact certificate files/commit and
either publish PASS or BLOCKED. This is the pre-implementation gate.

### Stage B — conditionally authorized: isolated implementation and C0–C7

This authorization permits Stage B only after the Stage A certificate has an
independent Luna-0 PASS recorded against immutable hashes. Then implementation
is confined to `experiments/luna63c/` on an isolated branch, opt-in and
disabled by default. The exact C0–C7 fixture names, initial values, hold
durations, TTLs, and outcomes are those in the pinned design report; the
execution contract quotes them. No equation/parameter/threshold/tolerance
changes, no production runtime, no tests that alter production behavior, no
sequence echo, no 63A implementation import, and no 63B dependency.

The primary causal contrast uses the identical stored `A=4` state and all
identical settings, comparing inactive RECALL hold (`R=0`) against permitted
release (`R=1`); only the gate differs. Verify runtime conformance before
interpreting trajectories or event counts: state bounds, ordering/ties,
canonical crossing, re-arm, quiet, strict-future output, expiry, overflow,
42-record cap, and immutable output persistence.

The final Stage B handoff must pin source/platform/runtime/dependency
revisions, commands, raw fixture outcomes and actual validations. Then stop
for independent Luna-0 review. A Stage A certificate PASS does not itself
count as experiment evidence or final runtime review.

### Required execution report

Use only these scientific dispositions:

- **SUPPORTED — RECALL-GATED NONLINEAR EXCURSION** when all primary causal
  and numerical gates pass;
- **PARTIALLY SUPPORTED** when RECALL gating passes but a bounded
  terminal/quiet or timing condition does not;
- **NOT SUPPORTED** when neutral/subthreshold RECALL emits or the intended
  excursion fails;
- **BLOCKED** for incomplete numerical certification, solver failure,
  resource-bound violation, event-time ambiguity, or invalid provenance.

For each fixture preserve the implementation trajectory/result and
independent oracle, maximum state error, event-time error, event-count and
terminal-state agreement, record/timer use, and the oracle's assurance level
(rigorous interval/closed-form versus qualitative). Perform at least two
genuinely independent fresh executions/materializations; compare event
records, state traces, canonical output identity/time and record counts. A
copied artifact is not an independent replay.

Before interpretation, enforce the runtime conformance gate: state bounds,
internal/external ordering and ties, timers, crossing direction/one-shot
behavior, re-arm, quiet, strict-future scheduling, overflow and the 42-record
maximum. Required regression families are focused Luna-63C, numerical
certificate, event-time/representability, crossing/re-arm, record-bound/
overflow, relevant E2/excursion and historical/core regressions; run the
full repository suite if shared/production-imported code is touched. Such
touches are outside this authorization and require stopping for a new
decision. Report exact test counts and skips for each family.

Even a supported outcome means only that a preloaded state can be released
through the reviewed field into a canonical excursion/output under RECALL.
It does not establish order encoding, sequence memory/replay, adaptive-time
integration, task echo, training, generalization, hardware equivalence or
production architecture.

## Architecture and information boundaries

This is an isolated pre-ACP experiment under the proposal process, not an
ACP, architecture promotion, or core/default change. A01–A15 are unchanged.
No code, fixture or event is wired into sequence echo. No task labels,
sequence identities, external answer buffers, evaluator truth or 63B material
are allowed. The scientific intervention is the exact reviewed field and
gate; RECALL is not direct excitation. Luna-63A's scalar HOLD result is
background only and does not establish 63C field behavior.

The existing `EventQueue` has deterministic insertion ties including
external-before-internal behavior for one destination at equal time. The
reviewed 63C contract instead requires component-local internal boundaries
to settle before same-time external records. Implement that only inside the
isolated experiment adapter; do not silently change the production queue.
The E2 `nextafter` case is narrow and does not certify continuous-root event
conversion for this field.

## Governance evidence and validation

| Check | Result |
|---|---|
| Before-governance main identity | `main == origin/main == d006e1bc6ff09627df8fe7f6c1213380b953291f`; clean after fetch |
| Reviewed design branch | Fetched `origin/experiment/luna63c-nonlinear-excursion-design`; design SHA `3e7d31b9a527e908b21abee3766906084e7cd082`; latest handoff `a303ebb835b72fdd01c86df478431b8638aacbb4` |
| Source branch status | Clean; fetched latest SHA matched `a303ebb...` |
| Design review | Independent Luna-0 **PASS WITH LIMITATIONS**, exact design SHA |
| Main evidence integration | Three documentation-only cherry-picks; no unreviewed descendants |
| Numerical certificate | **NOT RUN / NOT YET AVAILABLE** |
| Implementation, tests, solver, C0–C7, experiment | **NOT RUN**; specifically not executed in this governance invocation |
| ACP/core/default/hardware validation | **NOT APPLICABLE / NOT RUN**; no adoption or hardware claim |

The next role is **Luna-63C Mechanism**, Stage A certificate preparation
only. Stage B remains blocked pending independent Luna-0 certificate PASS.
No integrated sequence echo or Luna-64 is authorized.

## Required Luna-0 governance report

This handoff records each required decision item:

| Required item | Governance disposition |
|---|---|
| Authoritative starting `main` | `d006e1bc6ff09627df8fe7f6c1213380b953291f`; verified equal to fetched `origin/main`, clean before integration |
| Reviewed design SHA | `3e7d31b9a527e908b21abee3766906084e7cd082` |
| Latest design handoff SHA | `a303ebb835b72fdd01c86df478431b8638aacbb4` |
| Evidence integration | **CHERRY-PICK REVIEWED DESIGN EVIDENCE**, exact three source-ordered documentation commits |
| Independent design review | **PASS WITH LIMITATIONS — design gate only** |
| Numerical-certificate readiness | **NOT READY / NOT RUN**; Stage A certificate only is released |
| Exact equations/parameter pin | Frozen as transcribed above and in the new execution contract; `α=ω=1 TU⁻¹`, exact stable-focus field and thresholds |
| Solver strategy | Closed-form, event-aware interval approach per reviewed design; no neural global timestep or arbitrary fixed-step substitution |
| Event-time semantics | Exact root distinct from upward-rounded binary64 event time; interval endpoint ceilings must agree; strict future and expiry order enforced |
| Bounded accounting | **16 + 1 + 24 + 1 = 42** maximum; overflow is explicit and ingress closes |
| C0–C7 fixture freeze | **FROZEN** to the reviewed design names and values in the execution contract |
| Primary causal contrast | Same preloaded `A=4`, parameters, thresholds and timing; only `R=0` hold versus matched `R=1` release differs |
| Neutral-control criterion | `READY` neutral with RECALL changes gate only; no state load/motion/output |
| Subthreshold-control criterion | Reviewed C2 boundaries, including `A=q/2`, `A=1`, `A=2`, produce no canonical output |
| Excursion criterion | C4 supra state has one certified upward crossing only under the specified uninterrupted release condition |
| Terminal/quiet criterion | Re-arm, finite `r=q` quiet/reset, expiry, output persistence and terminal reason follow the reviewed event order |
| Deterministic replay | At least two independent fresh executions; compare records, traces, output identity/time and record counts |
| Regression requirements | Focused mechanism, certificate, event-time, crossing/re-arm, budget/overflow, relevant E2/excursion, historical/core; full suite if shared code is touched (which is unauthorized) |
| 63C execution disposition | **AUTHORIZED CONDITIONALLY / NOT EXECUTED**; Stage B blocked until Luna-0 PASS on the certificate |
| Contract created | `.github/agents/luna-63c-mechanism.agent.md`; existing design-only contract remains unchanged |
| Workflow/changelog | Additive status entries only; no architecture contract or ACP edits |
| Governance commit SHA | This handoff's containing governance commit; no self-reference |
| Push/fetch verification | Pending publication of this governance commit |
| Clean-worktree confirmation | Main was clean before edits; final clean status pending commit/push |
| 63B status | Unchanged: **LUNA-63B NUMERICAL ORACLE PREREQUISITE REQUIRED** |
| Integrated echo | Not authorized; no integrated echo task ran |
| ACP adoption | None |
| Luna-64 | Not authorized or created |
