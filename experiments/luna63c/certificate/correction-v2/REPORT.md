# Luna-63C corrective Stage A package, version 2

**BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE: N1 partial, N3 partial,
N4 conditional only, N5 incomplete. N2 CLOSED for this proposed package.**
No assertion of `CERTIFICATE PREPARED — N1–N5 CLOSED` is made.
N6 is **Stage B conformance only**, not a Stage A blocker.

## Authority, identity, history and isolation

Corrective preparation baseline: clean
`experiment/luna63c-stage-a-certificate`, local HEAD and its origin branch
`181b6440821e1dd6beede7e34cab9b6baada601a`; main remains
`73aaa50f97ceab322907875ae4dcf23e7541c3b5`. No fresh fetch is claimed.
The corrective assignment included a read-only 993-line assignment attachment.
That material was supplied and reviewed, not edited.
Retained independent Luna-0 review information is conversation-provided:
BLOCKED, N1–N5 incomplete, N6 Stage B only, spacing and publication/hash
corrections. No separate final certificate review file is found in tracked
handoffs. This is not independently reviewed or published corrective evidence.

Design and handoff source pins remain respectively
`3e7d31b9a527e908b21abee3766906084e7cd082` and
`a303ebb835b72fdd01c86df478431b8638aacbb4`.
Read-only comparisons confirm integrated copies unchanged at the corrective
baseline. The mechanism contract remains the committed
`.github/agents/luna-63c-mechanism.agent.md` with Stage A-only authorization.
Read extents/source hashes from the published `../sources.json` and retained
prior context remain applicable; the exact event/numerical requirements and
pinned design/handoff were reread. No 63B work/results or 63A implementation
is used. No production module is imported.

All five prior certificate files remain byte-for-byte untouched. Their
authoritative evidence is the frozen published revision above. This additive
`correction-v2/` package does not revise or overwrite that evidence. Its new
raw-Git-content manifest must be independently reviewed after parent
publication. The old checker's exact-directory-file-set assertion is a v1
layout assertion: adding a versioned subdirectory means that assertion should
be reproduced at the frozen v1 revision, not misreported as a mathematical
regression. The v2 integrity checker verifies old files against the frozen
revision explicitly; no old checker or manifest is amended.

### Frozen equations and exact content preserved

`alpha=omega=1 TU^-1`, `X=(x,y)`, `R in {0,1}`, invariant disk `r<=4`.
`xdot=R*(-x-y)`, `ydot=R*(x-y)`;
`X(s)=exp(-s) Rot(s) X(0)`, active time is the integral of R.
STORE clips signed local value once to [-4,4], loads `(p*A,0)`,
`p=sign(x_store)`, `A=abs(x_store)`, `sign(0)=0`.
`g=exp(-pi/4)/sqrt(2)`, `theta=2g`, `q=g`, `h=p*y-theta`.
`H=2`, `T_q=ln(4/q)`, `T_life=3+T_q`, clock `[0,2^20] TU`.

The accepted v1 real-arithmetic proofs are incorporated without alteration:
release equilibrium 0/eigenvalues -1±i; R=0 all states frozen;
Lyapunov derivative -R*r^2; disk invariance; neutral RECALL does nothing;
A<=2 no upward crossing, A=2 exact tangent; A4 unique rising and descending
first-lobe roots; re-arm never clears issued; radial quiet resets to neutral;
finite lifetime; primary contrast same preload/parameters/timing with only R
changed. Field is linear, event/lifecycle is hybrid. No output stimulus,
phase reset, threshold tuning or integration timestep has been introduced.

## Rigorous enclosure method and assurance boundary

`calculate.py` is a certificate-owned, independent **exact-equation interval
calculation**, not a runtime-under-test, fixture runner, lifecycle engine,
neural solver or event adapter. It has no imports from production or any
candidate module. No future candidate may import/reuse its propagation/root/
conversion code. All calculation is integers/rationals except final IEEE
bit encoding/display and exact `as_integer_ratio` checks. No libm exp, log,
sin, cos, atan or sqrt accuracy assumption occurs in these witness proofs.

Interval endpoints are signed integers divided by S=2^256. This is 256-bit
fractional resolution; arbitrary-size exact integer bookkeeping retains
integer parts and product bits. No rounding to nearest is used by the oracle.
Addition/subtraction are exact on the lattice. Multiplication takes min/max
of four products and floors/ceilings their quotients by S. Reciprocal of a
positive interval uses `[floor(S^2/hi),ceil(S^2/lo)]/S`. Positive integer
division rounds out. Every remainder is added outward after ceiling to
the lattice. All intermediate integer arithmetic is exact in CPython.
Thus fixed-point rounding cannot invalidate an enclosure; widened dependency
bounds may only cause unresolved comparisons.

Precision is fixed at the allowed initial 256 bits; escalation is zero.
There are exactly 128 bisections per root, never more. Each sign, derivative,
endpoint ceiling and order assertion must resolve, or this calculation fails.
No cap is interpreted as a certificate. These are finite interval-expression
calculations, not time steps.

### Transcendental proofs

* Machin identity `pi=16 atan(1/5)-4 atan(1/239)`. Sum k=0..127 of
  `(-1)^k z^(2k+1)/(2k+1)` with absolute alternating-series tail at most
  `z^257/257`. Valid for z=1/5,1/239. Evaluate exact rationals then enclose
  outward. Identity can be verified by tangent addition:
  tan(2 atan(1/5))=5/12, tan(4 atan(1/5))=120/119,
  tan(4 atan(1/5)-atan(1/239))=1; this angle is in (0,pi/2),
  hence pi/4 (no periodic ambiguity).
* sqrt(2): integer square root of `2*S^2`; strict squares of the lower and
  upper adjacent integers straddle `2*S^2`.
* `ln(2)=2 sum(k>=0) (1/3)^(2k+1)/(2k+1)`, from integrating
  `2/(1-z^2)`. Sum 128 terms, remaining positive tail bounded by
  `2*(1/3)^257/[257*(1-1/9)]`.
* For exp(-x), x in [0,6], sum exp(x) terms k=0..192 outward.
  Positive remaining tail is bounded by
  `6^193/193! / (1-6/194)` because subsequent term ratios are at most
  6/194. Reciprocal gives exp(-x) enclosure.
* For sin/cos, x in [0,6], sum 96 parity terms outward. Degrees are 191
  and 190. Taylor Lagrange remainder bounds are `6^192/192!` and
  `6^191/191!`: all real derivatives have absolute value at most one.
  No alternating-term monotonicity is assumed for initial terms.
  No range reduction is needed within this explicit bounded domain.
* Quiet/expiry use exact `T_q=(5/2)ln(2)+pi/4` and `T_life=T_q+3`.
  This avoids a generic logarithm evaluator, **not** a certificate of
  ln(A/q) for all entry-neighbor values or arbitrary pending C7 schedules.

The arithmetic tests check the stated remainder caps are less than one
2^-256 lattice quantum; rounding enclosures still include that quantum.
None of the series is treated as exact without its tail.

## N1: rigorous constants and A4 roots, incomplete full coverage

`witnesses.json` stores integer endpoints/denominators, not decimal estimates,
for pi, sqrt2, ln2, q, theta, T_q and T_life. Root bracketing starts at
[0,1/2] for the rising theta section and [1,3] for the descending q section.
The analytic monotonicity proof is still required: [0,1/2] lies below pi/4,
and [1,3] lies above pi/4 and below pi. The calculated pi enclosure verifies
these facts. Bisection retains certified opposite endpoint signs and finally
certifies strictly positive/negative derivative over each whole root bracket.
The A4 root widths are exactly 2^-129 TU and 2^-127 TU respectively.
Every sign enclosure and derivative enclosure is serialized.

This substantively discharges the former absence of constant and A4
root witnesses. N1 as a whole stays **partial**: no generic quiet logarithm
for the non-symbolic q neighbors and no completed bounds for all required
C7 exact-time mappings are claimed. No analytic amplitude decision is
replaced by rounded searching; tangent rejection stays symbolic.

## N2: adjacent q values CLOSED

Strict enclosure of exact q between adjacent positive normal binary64 values:

```text
below = 0x1.4a226c87ef13fp-2
above = 0x1.4a226c87ef140p-2
```

The proof compares exact rational decoded floats to both outward q endpoints
and verifies consecutive IEEE bit integers. This establishes strict sides
and adjacency without a float subtraction or libm nextafter approximation.
Symbolic A=q is still the exact oracle boundary, quiet-at-entry. It is not
replaced by either neighbor. A=q/2 remains the symbolic local fixture.
Below q enters QUIET_ENTRY; above q enters HOLD and requires a positive
quiet-time certificate, not epsilon equality. N2 is closed for the proposed
v2 evidence only, subject to independent review.

## N3: restricted common-ceiling and ordering certificates

Positive-normal integer conversion computes exponent from numerator bit length,
then ceilings the integer significand to 53 bits, handling binade carry.
It constructs IEEE bits and **proves** the previous value < endpoint <=
constructed value using exact rational decoding. For every boundary interval
both endpoint constructions must be identical. This proves the least binary64
ceiling rather than using nextafter as a fallback. Conversion is deliberately
restricted to positive normal endpoints; other domains are not silently
accepted.

For the **certificate example** STORE origin 0, A4 uninterrupted release
after d=0,1,2, map exact b=d+s_root. Expiry stays fixed, independent of d.
Each shift is independently converted; interval assertions prove
`d < t_up < t_rearm < t_quiet < t_exp`, all inside the clock domain.
These are mathematical reference calculations, not C3–C6 executions or a
complete selection of their packet/identity/observation materializations.

| HOLD d | ceil64 up | ceil64 re-arm | ceil64 quiet |
|---|---|---|---|
| 0 | 0x1.94f1f78d970b2p-3 | 0x1.2138dadc287bbp+1 | 0x1.42568b46d6f7cp+1 |
| 1 | 0x1.329e3ef1b2e17p+0 | 0x1.a138dadc287bbp+1 | 0x1.c2568b46d6f7cp+1 |
| 2 | 0x1.194f1f78d970cp+1 | 0x1.109c6d6e143dep+2 | 0x1.212b45a36b7bep+2 |

Converted expiry for all three is `0x1.612b45a36b7bep+2`.
Canonical mathematical root state remains
`(p*A*exp(-s_up)*cos(s_up),p*theta)`, never state at converted t_emit.
Canonical output fields and persistence remain exactly the v1 table:
fresh monotone lifetime ID/sequence, local source, episode/lineage, payload
p*1, EXCURSION, immutable t_emit; armed false/issued true at commit.

The unit arithmetic test proves ceil64(1+2^-54)=1+2^-52, but this is an
abstract conversion lemma, not a certificate of an unmaterialized C7 crossing.
N3 stays partial: arbitrary STORE origins/pauses, near-clock admission,
output/expiry coalescence and fully reachable below-ULP event schedules lack
complete interval witnesses. No clamping or altered precedence is allowed.

## N4: conditional binary64 state-error proof, not operational closure

A completely specified **hypothetical** checkpoint graph for A=1 is:

1. Take s as an exact representable dyadic checkpoint, independently from
   STORE origin and accumulated active-time state; no recurrence.
2. Compute E=RN64(exp(-s)), C=RN64(cos(s)), D=RN64(sin(s)), each correctly
   rounded under IEEE round-to-nearest ties-to-even.
3. Compute x=RN64(E*C), y=RN64(E*D). For p=-1 use exact sign flip.
   No FMA, state clipping, phase approximation or mutable threshold.
   s in {0,1/2,1,2}; normal finite results, exact zero sin(0), no underflow.

This is a proposed arithmetic specification/proof, **not implemented**
candidate propagation. With u=2^-53, each nonzero computed coordinate
has at most three relative-error factors (two correctly-rounded
transcendentals and one multiplication), hence absolute error <= gamma3
`3u/(1-3u)` because true |exp(-s)cos/sin(s)|<=1.
At zero use exact result; negative cos values obey the same absolute bound.
Squared state error is <=2*gamma3^2. The test verifies exactly as rationals
`2*gamma3^2 < theta_lo^2/16`, preserving the strict design norm
`||candidate-oracle||_2 < theta/4`.

The interval A1 checkpoint enclosures are frozen in witnesses for exact
s=0,1/2,1,2 as **proposed certificate-only** checkpoint values, not candidate
results. Oracle uncertainty is retained; future comparisons must bound actual
candidate-coordinate distance against the true oracle box. Event/timestamp,
direction and tangent proofs remain distinct.

N4 remains **BLOCKED**, not closed by assumptions: no candidate libm or
implementation has an independently established correct-rounding guarantee,
no adopted arithmetic specification for active-time accumulation/general
semigroup state updates exists, and no operational disk/threshold/timer error
proof has been derived. The graph cannot silently replace the reviewed
event-aware runtime or require the future candidate to share this oracle.
Do not infer a platform libm contract from IEEE basic-operation behavior.

## N5: exact reviewed C0–C7 entries retained; numeric freeze incomplete

`../expected_outcomes.json` at the baseline is the exact normative symbolic
table; this v2 report supplements it only with proved reference values.
No fixture name, preload, duration, resource cap, tolerance or outcome changes.

| Entry | Exact required state/transitions/outcome, preserved |
|---|---|
| C0 | READY, (0,0),R=0,no STORE: no episode/motion/timer/output; NONE. |
| C1 | READY RECALL1 then0: gate only, (0,0), no episode/timer/output. |
| C2 | Fresh {0,q/2,q,1,2}, plus certified q neighbors above: A<=q atomic QUIET_ENTRY/READY no log/timer; q<A<=2 HOLD then contraction/QUIET if enough active time, otherwise EXPIRED; A2 tangent no event; armed=false,issued=false. |
| C3 | Fresh A4,R0,HOLD {0,1,2} and separate expiry case: (4p,0) held,s0,no output; expiry clears EXPIRED before same-time RECALL. |
| C4 | A4,continuous release by t_store+2,at least T_q active before expiry: unique upward output, REFRACTORY, down re-arm, QUIET/READY; issued retained. |
| C5 | Same A4 release after {0,1,2}, uninterrupted T_q: exact active-time state/root offsets equal; independently shifted absolute ceilings, not required bit-identical. |
| C6 | Same initial state/origin as C4,R1: analytic semigroup after active alignment, same event/terminal fields. |
| C7 | All lifecycle/time cases below; fail closed on unresolved certificate, not approximate pass. |

Exact episode limits remain 16 within-budget attempts + one attempt17 overflow,
24 created/scheduled timers, one output, 42 unique records. At most one live
flow token plus one expiry; created cancelled timers remain charged. Stale
episode/generation/token has no state/output effect. Idempotent RECALL creates
no duplicate timer. Minimum nonredundant full uninterrupted A4 plan still has
two inputs/four timers/one output (seven records); no measured count claimed.
Input attempts/accepted/rejected, timer created/cancelled/stale/current,
output committed/processed and the four-disposition partition remain separate.

C7 exact rule preservation and remaining **materialization questions**:

| Required case | Frozen exact rule / unresolved numeric materialization |
|---|---|
| duplicate RECALL | Old-gate settle, idempotent, no phase reset/duplicate timer; counts toward eight RECALL/sixteen attempts. Numeric delivery ordinals/times not frozen. |
| alternating RECALL | Sum release durations only; pause cancels flow not expiry; resume from settled state. Full numeric schedule/ceilings absent. |
| RESET before commit | Settle first; cancel unreached output, ABORTED before READY. Exact RESET offset absent. |
| RESET after commit | Same ABORTED, immutable output survives exactly once. Exact offset relative to root versus delivery absent. |
| stale timer | Token mismatch no state/output effect; processed-stale not new record. Numeric token generation/delivery schedule absent. |
| re-arm/quiet tie | Exact tie re-arm first then quiet, issued retained. Analytic issued A>2 preload has strict re-arm<quiet, so no reachable such tie exists in this family. Synthetic scheduler-conformance injection would require a reviewed definition, not invented physics. |
| expiry equality | Expiry preempts external application/uncommitted boundary. At STORE origin0, the interval proves T_life strictly between adjacent binary64 values, so a binary64 packet cannot equal exact expiry. Packet at converted expiry is different; a symbolic equality test needs an explicit permitted representation. |
| valid-time invalid payload at expiry | Reserve, settle expiry, install, REJECTED_SEMANTIC with EXPIRED retained. Distinguish exact versus converted expiry as above; no bypass or model fault. |
| timestamp invalid | Audit consumed, REJECTED_TIMESTAMP; no settlement/time/key advance. Full malformed/late/domain/order encodings absent. |
| attempt17 overflow | After sixteen addressed attempts, final ID/offered17, processed-current REJECTED_CAP_OVERFLOW before cleanup/READY; no timestamp validation/settlement, ABORTED, existing output persists. Full packet set/ordinals absent. |
| post-abort ingress | Closed before component addressing; no ID/record; new STORE only with ordinary guard. Numeric ingress adapter action unspecified. |
| output/expiry coalescence | Suppress uncommitted crossing if converted emission>=expiry; fail closed, previously committed record persists. Reachable binary64 pause/release schedule not constructed. |
| near clock limit | Require exact expiry and ceiling in domain before admission; reject without episode otherwise. Adjacent admission packet times not certified here. |
| below-ULP positive delay | nextafter candidate only; common ceiling/strict future/expiry proof required. Abstract lemma proven; reachable event/processed-key schedule absent. |

Input precedence remains audit, admissibility/reserve, old-gate internal
settlement, install, semantic application. Internal-before-external equal
time; expiry wins ties; allowed exact re-arm/quiet tie re-arm first.
Malformed timestamp cannot settle; valid-time malformed payload must settle
before rejection. Overflow is the sole bypass, with disposition before
cleanup/READY and closed ingress. Committed output cannot be cancelled by
reset/expiry/quiet/overflow/generation. These are normative protocol statements,
not an adapter or scientific execution.

These unresolved questions cannot be closed by choosing arbitrary new
semantics or labels. The corrective assignment permits numeric certificates,
not changing the design's representation/event rules. N5 is incomplete;
the proposed checkpoint subset alone does not make it a complete freeze.

## Disposition and required stop

| Gate | Corrective result |
|---|---|
| N1 | PARTIAL: rigorous constants/remainders/root-direction witnesses produced; complete input/quiet/mapping coverage absent. |
| N2 | CLOSED: q adjacency and strict sides proved. |
| N3 | PARTIAL: common ceil/order for specified reference origins; C7 full numerical ordering unresolved. |
| N4 | CONDITIONAL ONLY: exact hypothetical arithmetic bound; no operationally certified candidate arithmetic. |
| N5 | INCOMPLETE: numeric checkpoint proposal; complete unambiguous C7 freeze unavailable. |
| N6 | STAGE B ONLY. Not counted as a Stage A blocker or executed. |

Thus combined disposition remains **BLOCKED — NUMERICAL CERTIFICATE
INCOMPLETE**. Stop certificate work at this bounded attempted closure.
Independent Luna-0 review of exact v2 hashes is required; there is no Stage B
authorization, scientific support result, training/task/order/sequence claim,
hardware equivalence, ACP/default adoption, integration or Luna-64.
No runtime, adapter, solver-under-test or scientific C0–C7 was implemented/run.
Only the exact-equation certificate calculation and arithmetic/integrity tests
were executed. No commit, push, staging, dependency installation or production
edit occurs in this preparation.

## Reproduction, environment and replay obligations

Observed environment: CPython 3.11.4 (MSC v1934 64-bit AMD64),
Windows 10.0.19045, Git 2.53.0.windows.1, PowerShell 5.1.19041.6456.
Only standard library, exact integers and Fraction; no numerical dependencies,
random seeds, global neural clock, libm transcendental estimates or task data.

Commands from root:

```powershell
python -B experiments/luna63c/certificate/correction-v2/calculate.py --check
python -B experiments/luna63c/certificate/correction-v2/test_certificate.py
python -B experiments/luna63c/certificate/correction-v2/integrity.py --prepare
git --no-pager diff --check
```

Parent must publish exact proposed Git-clean blobs and run `integrity.py`
without `--prepare` for committed HEAD/index/checkout verification. The
manifest excludes itself; its outer raw Git blob SHA256 is reported separately.
The historical sources are verified at their pinned revisions, not assumed
from mutable HEAD source paths. No checkout newline format is authoritative.
LF/CRLF clean-filter equivalence is proved with Git object identities.

Two fresh deterministic numerical reference recomputations using the same
`calculate.py` implementation are run as certificate checks only. These are
not two independent implementations or independent recomputations; a second
implementation was not performed. No two-run scientific fixture replay is
claimed.
Validation record: two separate fresh `calculate.py --check` processes produce
and compare the complete deterministic interval witness data; each passes.
`test_certificate.py`: **9 passed, 0 failed, 0 skipped**, certificate-only.
`integrity.py --prepare`: **55 passed, 0 failed**, proposed Git-clean blob
integrity/portability only, not committed publication verification.
`git diff --check` and explicit new-file trailing-whitespace/JSON checks pass.
No failures or unresolved midpoint signs/common ceilings occurred in the
restricted A4 reference calculations. This does not resolve the broader
N1/N3/N4/N5 gaps documented above or authorize runtime work.
Future Stage B still requires independent fresh fixture executions and all
v1 replay/error/event-count/terminal/resource preservation checks after a
separate numerical PASS, never by copying these reference results.
The Stage B regression families all remain NOT RUN (zero executions and zero
framework skips); certificate tests do not substitute for them.
