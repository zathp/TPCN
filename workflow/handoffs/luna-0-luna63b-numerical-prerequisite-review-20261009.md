# Luna-0 independent numerical prerequisite review — Luna-63B

**BLOCKED — full oracle/tolerance prerequisite.**
The candidate's rational terminal-state oracle and binary64 recurrence budget
are analytically supportable under the stated update order. The complete
prerequisite remains blocked by the leaky scalar control's exponential-error
certificate and unresolved exact observation/metadata semantics. This is not
a test result, adoption of `0.04 SU`, or execution authorization.

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent Luna-63B numerical oracle and tolerance prerequisite"
  task_id: "luna-0-luna63b-numerical-prerequisite-review-20261009"
  component: "Read-only analytical review of proposed candidate and controls"
  status: "blocked; no execution authorized"
  contract_version: "1.2"
  branch: "main"
  base_revision: "e52098b2141a3f121f23b512e877783a64ef8baa"
  result_revision: "Published with Luna-63 governance handoff"
  dependencies:
    - "Luna-63B design report and handoff at fe3ebe5fdd2e018e79dd640fa4f94548ebba8701"
    - "Luna-63B agent contract and separate authorization"
  owner: "Project owner"
  classification: ["INDEPENDENT MATHEMATICAL REVIEW", "NUMERICAL PREREQUISITE"]
  hypothesis: "The frozen candidate has an independent exact-state oracle and numerical criteria separated from floating-point uncertainty."
  counter_hypothesis: "The scalar control or exact state/observation semantics lack a complete independent certificate."
  interfaces_relied_on: ["Proposed two-port packet, peak, prediction, residual and encoding equations"]
  label_information_boundary: ["No evaluator truth or other lane evidence used"]
  timing_assumptions: ["Frozen dyadic local event times and stated packet update order"]
  reset_boundaries: ["Analytical only; no model instantiated"]
  resource_bounds: ["Proposed 32-packet/10-scalar candidate envelope only"]
  authorized_scope: ["Independent equations/error-bound derivation; read-only review"]
  unauthorized_scope: ["Editing candidate, tests, execution contract, simulation or trial"]
  controls: ["Primary order pairs, polarity assignments, peak/prediction expiry and scalar controls"]
  measurements: ["Analytical rational states and IEEE-754 forward-error estimates only"]
  information_boundary_check: ["No experiment execution or diagnostic callback"]
  hardware_mapping: ["Not applicable; no hardware analysis or equivalence claim"]
  architecture_invariants_touched: ["A01-A02, A06-A08, A15 assessed; none changed"]
  preserves: ["No ACP or architecture promotion; no execution authorization"]
  architecture_change: false
  proposal: null
  files_changed: ["This independent numerical review record"]
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All code, oracle, replay, non-interference, simulation, trial and hardware tests"]
  assumptions: ["Exact frozen packet inputs are represented as the stated dyadic values."]
  unresolved:
    - "Exponential library/build error guarantee for leaky scalar control"
    - "Complete exact metadata, invalid-input, expiry, settlement, ID, deadline and signed-zero oracle"
    - "Explicit observation anchors for long control histories"
    - "Owner disposition of the proposed 0.04 SU threshold"
  recommended_next_agent: ["Owner/Luna-0 to publish the missing freeze before any execution decision"]
```

## Scope and result

Reviewed the complete Luna-63B design and handoff at
`fe3ebe5fdd2e018e79dd640fa4f94548ebba8701`, its agent contract, Luna-63
authorization, Luna-62 independent gate, architecture contract and applicable
workflow sources. No code or tests were executed, no files were changed by the
numerical reviewer, and no 63A result was consumed.

Disposition: **LUNA-63B NUMERICAL ORACLE PREREQUISITE REQUIRED**. The exact
candidate amplitude oracle and a candidate binary64 error budget can be
substantiated analytically. That does not close the full protocol: a scalar
control uses exponentials whose error is uncertified, and the exact metadata
and observation oracle is incomplete. There is no 63B execution contract.

## Independent candidate-state oracle

Initially all ten amplitude coordinates are `+0`; both predictions are valid
zero through 12 TU. Before a valid arrival, due deadlines are settled with
equality-expiry first: generation expiry, prediction expiry, then peak expiry.
Encoding evolution is identity between packets. Peak expiry clears rails and
`d` without depositing release; prediction expiry invalidates `q` without a
residual; generation expiry/fault clears all amplitude state.

For each present port `j`:

\[
p_{j,\pm}^{+}=\max(p_{j,\pm}^{-},v_{j,\pm}),\quad
r_j^\pm=p_{j,+}^\pm-p_{j,-}^\pm,\quad
d_j=r_j^+-r_j^-.
\]

Use the frozen pre-packet prediction:

\[
\epsilon_j=d_j-q_j,\qquad a_j=d_j-\epsilon_j/2=(d_j+q_j)/2
\]

when valid and unexpired. Otherwise `epsilon=0` and `a=d/2`. An absent port
has zero increment and no observation. Both candidate updates use the
pre-packet predictions:

\[
x^+=\operatorname{clip}_4(x^-+a_A),\qquad
y^+=\operatorname{clip}_4(y^-+a_B).
\]

Only after both deposits, replace predictions by
`q_A=y^+/4`, `q_B=x^+/4`. A simultaneous packet cannot use updated `x` to
compute its current B increment. The candidate has only `max` and clipping
nonlinearities; no inter-event z leak.

For expired peaks, valid predictions and inactive clipping, let
`alpha,beta ∈ {-1,+1}` be the signed A/B unit inputs. Then:

| History | Exact terminal `(x,y)` | Last residual |
|---|---|---|
| AB | `(alpha/2, beta/2 + alpha/16)` | `beta - alpha/8` |
| BA | `(alpha/2 + beta/16, beta/2)` | `alpha - beta/8` |
| AAB | `(alpha, beta/2 + alpha/8)` | `beta - alpha/4` |
| ABA | `(129 alpha/128 + beta/16, beta/2 + alpha/16)` | `63 alpha/64 - beta/8` |
| BAA | `(alpha + beta/8, beta/2)` | `alpha - beta/8` |

These equations cover all four polarity assignments. Exact primary distances
are `sqrt(2)/16` for AB/BA and either `sqrt(113)/128` or `sqrt(145)/128` for
the matched-count pairs; minimum is about `0.08305 SU`. With identity HOLD,
they persist across the design's declared delay/offset observations. This is
conditional algebra, not simulated evidence, and does not adopt the proposed
`0.04 SU` acceptance threshold.

Additional analytically derived checks include: AA at `(1,6)` ends at `(1,0)`
while A at 6 ends at `(1/2,0)`; AAB/ABA/BAA differences are count matched;
no-input and zero-present from zero remain `(0,0)` encoding; and the 32-packet
alternating positive fixture reaches `(4,4)` by packet 12 and remains clipped.
This derivation does not establish bitwise runtime replay.

## Candidate binary64 error budget

Assume round-to-nearest binary64 with `u=2^-53`, exact frozen input conversion,
the stated scalar operation order, and no reassociation/FMA. A conservative
per-present-port absolute budget is `64u SU` per affected encoding coordinate.
The report's encoding propagation has infinity-norm factor at most `9/8`;
clipping is nonexpansive. For at most 32 packets:

\[
E_{32}\le64u\sum_{k=0}^{31}(9/8)^k
=512u((9/8)^{32}-1)<22016u<2.45\times10^{-12}\text{ SU}.
\]

This substantiates the report's `<3e-12 SU` inequality under those assumptions.
It is not a blanket Lipschitz bound for arbitrary perturbation to all ten
coordinates and metadata. For the actual finite dyadic fixtures, the reviewed
operations appear exactly representable in binary64 in the literal update
order; wrong exact dyadic results must not be excused by the broader bound.

With coordinate error at most `E`, pair-distance perturbation is at most
`2 sqrt(2) E`, before metric operation rounding. Thus the proposed `1e-9 SU`
distance tolerance is numerically ample under a fixed accurate square-root
operation. A distance difference over the minimum algebraic separation is
much larger than numerical error, but the threshold itself remains an owner
decision. Exact repeat equality and non-interference remain separate runtime
acceptance checks.

## Scalar controls and unresolved full certificate

For event increments `g_k=(d_A,k-d_B,k)/2`, the no-leak control is
`s(t)=sum_{t_k<=t} g_k`; this commutative aggregate is equal across matched
permutations in unsaturated fixtures. For the leaky scalar, the exact-real
oracle is:

\[
s(t)=\sum_{t_k\le t}g_k e^{-(t-t_k)/4},\quad t<48.
\]

It can distinguish order from recency and is not a known-insufficient
baseline. The design proposes an 80-digit Decimal oracle, but digit count
alone does not certify exponential error. One conservative recurrence bound
is `E_scalar <= 516u + 132b`, where `b` bounds the implementation's absolute
error for each decay factor; `b <= 7e-13` would suffice for the proposed
`1e-10` absolute floor, provided the stated arithmetic assumptions and domain
are documented. The selected exponential implementation's library/build error
guarantee and independent reference rounding/conversion bounds are missing.

Other blockers:

- The shared anchor `L=8` precedes last inputs in long control histories;
  prefix versus terminal/HOLD observations must be named and frozen.
- Exact oracle semantics are missing for fault-time timestamp changes,
  invalid-packet validation versus due-expiry precedence, scheduled versus
  lazy settlement and observation-copy timestamps, retained IDs/generation
  fields and cleared deadlines/tokens, and signed zero under bitwise checks.
- A duplicate packet after a due peak expiry illustrates an ambiguity:
  scheduled settlement at 1.5 and validation-before-lazy-settlement at 2 can
  agree on amplitude but differ on committed time/status.
- Exact platform/build and operation order, independent oracle owner, and
  explicit accept/reject of the 0.04 SU criterion require a new published
  pre-execution freeze.

**No execution is authorized.** Do not loosen tolerances, change fixtures, or
choose constants to clear these blockers. A later authorization must resolve
each issue explicitly and be independently reviewed before any trial.
