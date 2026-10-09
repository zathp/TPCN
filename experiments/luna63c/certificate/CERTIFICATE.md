# Luna-63C Stage A certificate report

Format: `luna63c-stage-a-report/1`. Preparation date: 2026-10-09.

**Disposition: BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE.**
This is a certificate-only, partially established mathematical report, not a
completed numerical certificate, runtime conformance verdict, mechanism result,
or Stage B authorization. Stop here for independent Luna-0 review. No runtime,
event adapter, propagation evaluator, root solver, timer engine, or C0–C7 runner
was created or executed. No runtime, adapter, solver or scientific fixture
execution is reported; this report remains blocked.

## 1. Identity, authority, provenance, and reproduction

The initially clean working tree was on `main` in
`C:\Users\Patrick\Documents\ActiveCode\TPCN`; local `HEAD`, `main`, and
`origin/main` each resolved to
`73aaa50f97ceab322907875ae4dcf23e7541c3b5`. This verifies local refs, not a
fresh remote fetch. The reviewed design revision is
`3e7d31b9a527e908b21abee3766906084e7cd082`; the latest handoff revision is
`a303ebb835b72fdd01c86df478431b8638aacbb4`. Read-only `git diff` comparisons
of each pinned document against baseline HEAD produced no differences.
Cherry-pick identities do not replace these source pins.

These ref/branch observations describe initial preparation, not permanent
reproduction requirements. The checker accepts a committed/published certificate
descendant by requiring the frozen baseline commit object to exist and be an
ancestor of HEAD, while checking every recorded source byte/hash/blob against
that baseline. It does not require branch `main` or stationary `main`/`origin/main`
refs. The parent's later refresh does not change the recorded no-fresh-fetch
preparation provenance.

`sources.json` identifies raw committed bytes by revision, Git blob and SHA256,
and records preparation environment, read extents, and generation method.
`expected_outcomes.json` is a deterministic **symbolic expectation** table;
null numeric certificates mean unresolved, not zero or a wildcard pass.
`manifest.json` hashes the report, table, metadata and checker as raw Git blob
content bytes from `git show HEAD:experiments/luna63c/certificate/<file>`
after the artifact publication commit, not checkout bytes.
The manifest excludes itself to avoid a circular hash; its outer SHA256 is
returned to the caller using the same blob-content scope. Original preparation
serialized UTF-8/CRLF without a BOM; repository `* text=auto` normalizes
these text blobs to LF. Fixed field order, fixed metadata and no current-time/
seed/random generation are used. These are versioned JSON documents, not
binary64 numeric oracle outputs. Hash raw committed content without further
normalization. Source hashes likewise use `git show revision:path` bytes.
LF and CRLF checkouts are permitted: the default checker proves that each
artifact's HEAD blob identity equals its index identity and its working-tree
identity after Git's path-specific clean filters. It also verifies that LF
and CRLF forms clean to the same blob. Checkout line endings are not an
independent invariant or the hash authority.

Read sources include the committed mechanism contract and authorization,
both exact pinned design documents, architecture contract, current relevant
changelog/workflow sections, acceptance criteria, ACP-0008, and cited current
queue, emission, E2 scheduling, emission-consumption and IR semantics.
The authorization's independent **63C numerical-certificate decision is
NOT RUN / NOT YET AVAILABLE**. Its design PASS WITH LIMITATIONS is not a
numerical PASS. Only prerequisite-decision/status material for the separate
63B lane was inspected; no 63B model, work artifact, state or result is an
oracle/dependency here. That lane remains
**LUNA-63B NUMERICAL ORACLE PREREQUISITE REQUIRED**. No 63A implementation or
historical evidence is used.

Reproduce **after the parent commits the updated artifacts**, from repository
root, without importing runtime code:

```powershell
git --no-pager rev-parse --verify '73aaa50f97ceab322907875ae4dcf23e7541c3b5^{commit}'
git --no-pager merge-base --is-ancestor 73aaa50f97ceab322907875ae4dcf23e7541c3b5 HEAD
git --no-pager diff 3e7d31b9a527e908b21abee3766906084e7cd082 HEAD -- workflow/docs/luna/LUNA_63C_NONLINEAR_EXCURSION_DESIGN.md
git --no-pager diff a303ebb835b72fdd01c86df478431b8638aacbb4 HEAD -- workflow/handoffs/luna-63c-nonlinear-excursion-design-20261009.md
python -B experiments/luna63c/certificate/check_certificate.py
git --no-pager diff --check
git --no-pager status --short --untracked-files=all
```

The checker prints every raw Git blob SHA256, including the manifest's outer
hash. Do not use `Get-FileHash` on checkouts or PowerShell text pipelines to
hash Git output: they may hash a different newline representation.

Before publication, manifest generation uses proposed LF content
`Path.read_bytes().replace(b"\r\n",b"\n")` only after proving its unfiltered
Git object ID equals the actual checkout's `git hash-object --path <path>
--stdin` clean-filter ID. Both commands are read-only (no `-w`); the
checker makes the same proof in explicit preparation mode:

```powershell
python -B experiments/luna63c/certificate/check_certificate.py --prepare
```

Calculate SHA256 of those proved proposed blob bytes, update the four manifest
entries, then calculate the proposed manifest's outer blob SHA256. This yields
prospective committed-content hashes, not a claim of publication. The parent
must commit all five paths with those exact content blobs and rerun the
default command; a dirty index/working tree fails that post-commit verification.
No commit, index write, push or fresh checkout is performed by this worker.

The checker is read-only metadata/hash/self-consistency code, not an oracle.
It neither evaluates the model nor establishes any outstanding mathematical
claim. No numerical dependency is installed. Hand proofs below can be
independently reconstructed from the exact equations.

## 2. Frozen model, parameter and information identity

State `X=(x,y)` is in SU, clock and active time in TU.
`alpha=omega=1 TU^-1`; `R` is exactly 0 or 1.

```text
B = [[-1,-1],[1,-1]]
dX/dt = R B X
s(t) = integral R(u) du
X(s) = exp(-s) [[cos(s),-sin(s)],[sin(s),cos(s)]] X(0)
x_store = clip(z_local,-4,4) once; A=abs(x_store); p=sign(x_store)
X(0) = (p A,0); sign(0)=0
g = exp(-pi/4)/sqrt(2); theta=2g; q=g
h(X) = p y-theta
H=2; T_q=ln(4/q); T_life=H+T_q+1
T_clock=2^20; 0<=t<=T_clock
```

No decimal approximation substitutes for these identities. STORE is a local,
predeclared signed fixture load, not RECALL. No task labels, sequence identity,
answer buffer, evaluator truth, training, or 63B inputs exist in this model.
The field is linear; threshold/lifecycle behavior is hybrid. The word
"nonlinear" in the authorized disposition is not evidence of a nonlinear ODE.

## 3. Equilibrium, stability, and operating region — exact proofs

For `R=1`, `det(B)=2`, so the unique equilibrium is the origin.
The characteristic polynomial is `(lambda+1)^2+1`; eigenvalues are
`-1+i` and `-1-i`. For `R=0`, **every state** is a frozen equilibrium;
the neutral state is common to both gates. Thus the unqualified assertion
"sole equilibrium" applies to the release field, not HOLD. Persistent
`R=0` does not give asymptotic attraction to zero.

For `V=(x^2+y^2)/2`, cancellation of the cross terms gives
`dV/dt=-R(x^2+y^2)=-2RV`. Consequently `r=A exp(-s)` and
`||X(s)||_2=A exp(-s)`. Release is globally exponentially stable in active
time; arbitrary gated flow is nonexpansive and converges to zero only if
active time diverges. HOLD is exactly constant. STORE puts `r<=4`, flow
cannot increase `r`, and terminal clearing maps to the origin. The disk
`x^2+y^2<=16` is invariant in exact arithmetic, hence each coordinate is
bounded by 4. This is not a proof that a rounded propagation routine stays
inside the disk. No numerical projection/clamp is authorized to hide error.

The finite operating region also includes binary gate, finite timestamps in
the stated clock domain, finite episode lifetime, finite unsigned 64-bit
lifetime attempt/episode/token/output identity counters with no wrapping,
and the immutable input/timer/output caps. Identity exhaustion or impossible
internal gate/state is fail-closed, not a successful quiet result.

## 4. Neutral, subthreshold, excursion, and causal contrast — exact proofs

At `X=0`, `BX=0`, so either gate leaves `X=0`.
`h=-theta<0`; no upward crossing or output occurs. In READY, RECALL changes
only `R`; it cannot load state, allocate an episode/timer, or emit.

For nonzero polarity set `z(s)=p y(s)=A exp(-s) sin(s)`.
Its derivative is `A exp(-s)(cos(s)-sin(s))`.
On `(0,pi/4)` it is positive; the peak is `Ag` at `pi/4`.
For `A=q/2`, STORE is already inside quiet; dynamic flow is not needed.
For `A=1`, the peak is `theta/2`, with margin `theta/2` to output.
For `A=2`, the peak is exactly `theta`, the derivative is zero, and
`z''(pi/4)=-2 A exp(-pi/4) cos(pi/4)<0`: an exact tangent, never an
upward event. For all `A<=2`, later positive-lobe maxima decrease by
`exp(-2pi)` per turn. Negative lobes cannot reach the positive oriented
section. These facts prove no output without a rounded threshold search.

For `A=4`, `X(0)=(4p,0)`, release gives
`(4p exp(-s)cos(s),4p exp(-s)sin(s))`, peak `4g=2theta`.
The rising root `s_up` is the unique solution of
`4 exp(-s)sin(s)=theta` in `(0,pi/4)`. Existence follows from opposite
endpoint signs and continuity; uniqueness/direction follow from the
strictly positive derivative. This is an exact existence/direction proof,
not a numeric isolating interval or a timestamp.

The matched control stores exactly the same `(4p,0)`, with the same
parameters, thresholds, STORE origin, lifetime, output policy and inspection
times. Only `R` differs. HOLD has `s=0`, state `(4p,0)` and `h=-theta`
through every HOLD duration `{0,1,2}` (and until expiry). Matched release
has the unique rising root provided sufficient active time precedes expiry.
RECALL supplies no current, impulse, phase reset or output command; it
multiplies the preexisting field. C0/C1 alone cannot establish this contrast.
These are mathematical predictions, not observed causal results.

## 5. Event, re-arm, quiet and one-output proofs

For any `2<A<=4`, define the rising root in `(0,pi/4)` as above.
After `pi/4`, `z` strictly decreases to zero at `pi`. Since `Ag>theta>q`,
there is exactly one downward `z=q` root `s_rearm` in `(pi/4,pi)`.
The root state for output is
`(p A exp(-s_up)cos(s_up),p theta)`, distinct from state at rounded
delivery time. Eligibility additionally requires prior-below-section,
`armed=true`, `issued=false`, and certified positive derivative.
Commit sets `armed=false`, `issued=true`, mode `REFRACTORY`, and creates
one immutable `EXCURSION` record with payload `p*1`.
Re-arm sets `armed=true` but never clears `issued` or leaves REFRACTORY.
Thus the generation can commit at most one output even if future lobes
were considered. Fresh STORE, not RECALL/re-arm, initializes a new issued bit.

For `A>q`, the first inward quiet root is `s_q=ln(A/q)>0`, since
`r'= -r<0`. For `A<=q`, quiet-at-entry is atomic at STORE; do not evaluate
`ln(A/q)`, especially at `A=0`. Equality is exact/symbolic where proven,
not an epsilon zone around a rounded `q`.

For excursion amplitudes `2<A<=4`, re-arm precedes quiet strictly:
`s_q<=T_q=ln(4sqrt(2))+pi/4<pi` by the design's elementary exponential
bound. Also `s_q>ln(2sqrt(2))+pi/4>pi/2`.
To justify the latter without decimals,
`ln(2)=2(1/3+(1/3)^3/3+...)>2/3`, so
`ln(2sqrt(2))=(3/2)ln(2)>1>pi/4`.
At `s_q` in `(pi/2,pi)`, `z(s_q)=q sin(s_q)<q`; by strict decrease
after the peak the re-arm root has already occurred. Output precedes
peak, which precedes re-arm, which precedes quiet. Quiet reset cannot
create an output because `r=q<theta`.

The special exact re-arm/quiet tie precedence is still a required adapter
rule, but **no issued A>2 episode of this exact preload/field has that tie**.
C7 must distinguish a proven reachable case from a synthetic scheduler
conformance case. No reachable tie fixture, injection method or numeric
tie timestamp is invented here. A subthreshold value with `s_q=pi/2`
does not turn into an issued episode or create a re-arm token.

Quiet and expiry clear `X,p,A,s`, set `R=0`, `armed=false`, invalidate
uncommitted generation/tokens, retain retired `issued`, metadata/IDs and
any immutable committed output. Terminal disposition commits before READY.
Retained reasons are exactly `NONE`, `QUIET_ENTRY`, `QUIET`, `EXPIRED`,
`ABORTED`, `FAULT`. RESET retains `ABORTED`; it is not QUIET. Output is
not owned by the cancellable timer generation and must be processed once.
A new STORE is blocked until a prior committed output has been processed.

## 6. Active/absolute time, lifetime, precedence and representability

For gate intervals, `s(t)` is the sum of lengths of completed release
intervals plus the current release length; HOLD contributes zero.
On the unique release interval starting at `(t_i,s_i)` containing root
`s*`, the exact absolute root is `b=t_i+(s*-s_i)`, with outward enclosure
of every subtraction/addition. At an exact pause-endpoint root, old-gate
settlement processes that root before the external pause, unless expiry wins.
For uninterrupted release after HOLD `d`, `b=t_store+d+s*`.
The semigroup identity follows from addition of angles and exponentials,
so equal accumulated active time means equal exact state/root offsets.
Absolute ceilings are recomputed independently after each HOLD shift;
binary64 absolute timestamp equality across C5 is not required.

Expiry is the fixed exact sum `t_store+T_life`, never renewed.
`T_life=3+T_q` is finite. Admission must prove this sum, and its ceiling,
inside `[0,2^20]` before allocating an episode. Continuous A=4 release
starting by `t_store+2` reaches quiet by `t_store+2+T_q`, at least one
TU before exact expiry. Under the finite clock domain this macroscopic gap
is far greater than one binary64 bin (the maximum spacing between adjacent
binary64 timestamps both within `[0,2^20]` is `2^-33` TU; the forward spacing
at `2^20` is `2^-32` TU, but its successor is outside the domain), so converting
these two boundaries cannot erase that gap.
This does not supply their actual ceilings or certify every C7 case.
Insufficient active time permits expiry with no exactly-one guarantee.

For every distinct causal internal boundary require a finite, in-domain
logical time strictly later than the last actually processed key/time.
Use `ceil64(b)`, the least finite binary64 value not smaller than exact `b`.
Refine an outward `[lo,hi]` until `ceil64(lo)=ceil64(hi)`.
For output require this common time strictly future and strictly less than
converted expiry. `nextafter(t_prev,+infinity)` is only a candidate;
never use it as a clamp, zero-delay fallback or unbounded search.
Mathematical order does not imply converted order: distinct boundaries
can coalesce. Coalesced-invalid output/expiry suppresses uncommitted output
and fails closed, retaining any previously committed output. An allowed
exact re-arm/quiet tie shares a logical time, re-arm first. Expiry wins
every exact tie with an uncommitted boundary.

Protocol order is frozen independently of field/timestamp proofs:

1. Audit ID/count first. Attempts 1–16 may proceed; attempt 17 is the
   exception described in section 8 and never settles its timestamp.
2. Validate only finite binary64 timestamp/domain and nondecreasing
   `(t,ordinal)`; reserve the external pair without installing it.
   The unified destination ordinal must leave due internal boundaries first.
   Invalid timestamp/order means `REJECTED_TIMESTAMP`, retained audit,
   no flow settlement and no time/key advance.
3. Settle old gate through admissible time. Process certified internal
   boundaries in exact order, internal-before-external at equal time;
   expiry first at an exact expiry tie. A reservation is not the processed
   key used by the strict-future test.
4. Install external pair after settlement, then semantic validation.
   Invalid gate/payload/mode means `REJECTED_SEMANTIC` after settlement,
   not a model fault. Valid-time invalid payload at expiry cannot evade
   expiry. Retain terminal reason and reject application to the retired
   generation. A timestamp-invalid packet cannot trigger expiry settlement.

The production EventQueue instead chooses external-before-internal for the
same destination at equal time. The E2 S_REARM nextafter exception applies
only to its scalar positive-delay case. Neither source certifies this field
or supplies the proposed local precedence. Production imports/changes remain
prohibited. The IR source explicitly is not an arbitrary live checkpoint.

## 7. Numerical comparison/error rules — frozen, but not discharged

Exact equality is required for gate values, integer counters, identities,
event categories/counts, payload `p*1`, terminal reasons, dispositions,
one-shot/persistence flags and exact certified logical timestamp identity.
Exact neutral/HOLD behavior is a mathematical requirement, not approximate
zero. Exact `A<=2` classification rejects tangency without numeric root
search. Symbolic `A=q` uses its proved identity; representable neighbors
must be derived by independent outward enclosure and adjacency proof.
Their hexadecimal values are currently **unresolved**.

For A=1 checkpoints the frozen check is strictly
`||X_candidate-X_oracle||_2 < theta/4`, never `<=`, never a tuned tolerance.
One can compare squared norm to `theta^2/16` with rigorous intervals:
take exact binary64 candidate coordinates as rationals; enclose the oracle
state outward; obtain an upper bound for squared distance and a lower
bound for `theta^2/16`. Pass only if the former is strictly less.
An overlap is unresolved/fail-closed, not approximate agreement.
This freezes an acceptance test, **not** a bound on a future candidate's
computed state. The A=1 peak margin explains why theta/4 is half the margin;
it cannot certify event topology, direction, timestamps, or disk adherence.

No candidate arithmetic graph, FMA policy, accumulation method, transcendental
implementation/error contract, threshold representation, checkpoint list,
or root/time rounding implementation has been specified and independently
bounded. Therefore no Stage B operational binary64 error bound is claimed.
Unit roundoff `2^-53` for round-to-nearest basic normal operations alone
does not bound library exp/sin/cos/log, cancellation, subnormals, accumulated
active time or threshold/root error. No arbitrary ULP/absolute-relative
tolerance is supplied. Exact event times require equality of certified
ceilings, not an event-time tolerance.

The required oracle arithmetic is outward bounded at 256 through at most
1024 bits, with at most 128 bisections per root. Rigorous pi/sqrt/exp/sin/
cos/log enclosures require justified range reduction, analytic remainder
and directed-rounding error bounds. Increasing precision alone is not a
proof. No such evaluator or numeric interval witnesses were prepared here;
zero root bisections and zero precision-refinement calculations were run.
No decimal package or system libm result is passed off as a rigorous bound.

In particular a narrow root interval can straddle a binary64 rounding
boundary; both endpoint ceilings need not agree after 128 bisections.
Exact equality to a representable boundary may require a symbolic proof.
Near q, near expiry, near the clock limit, or after a below-one-ULP delay,
neither cap guarantees sign/order/ceiling resolution. Each unresolved item
must abort without an uncommitted output. Analytic uniqueness above does
not discharge these numerical obligations.

## 8. Timer, attempt, output, and unique-record accounting

Immutable caps: 16 within-budget addressed inputs including initial STORE;
one additional overflow input; 24 created/scheduled unique timers including
cancellations; one committed output; total `17+24+1=42`.
Valid operation limits: STORE at most 1, RECALL at most 8 including accepted
idempotent duplicates, RESET at most 1 per episode. Rejected/duplicate/
malformed attempts still consume within-budget attempts. Lifetime uint64
counters must be checked before allocation and never wrap.

At most two live timer tokens: one next flow boundary (crossing, re-arm,
or quiet) and one fixed expiry. R=0 cancels unreached flow timers only,
not expiry; duplicate gate records do not replan or duplicate timers.
R=1 plans the next boundary from settled active time. Tokens carry episode,
generation and per-kind identity; mismatch is stale and cannot mutate
state or emit. A terminal transition invalidates all uncommitted tokens.
Created and cancelled records stay charged. Immediate quiet-at-entry has
no timer/output allocation.

For a simple accepted STORE, one uninterrupted RECALL release and full
completion, next-boundary-only planning requires one expiry and, for A=4,
crossing/re-arm/quiet: four timers, two inputs, one output, seven unique
records. For q<A<=2 it requires expiry/quiet: two timers, two inputs,
zero output, four unique records. For HOLD only, one STORE and expiry
are two unique records; expiry processing is not a new record.
These are conditional minimal-plan counts, not measured counts or a
universal claim about an unspecified adapter. Extra conformance inputs
are charged separately. With at most eight accepted gate records, a
nonredundant next-boundary planner would need no more than eight initial/
resume flow creations plus two post-boundary continuations and one
expiry (11); the authorized cap remains **24**, not 11. No plan may
arbitrarily reallocate until it reaches 24 and call that evidence.
No allocation algorithm/enforcement exists here; worst-case adherence
must still be independently verified before scientific interpretation.

Every unique record occupies exactly one disposition:
`pending`, `processed-current`, `processed-stale`, or
`cancelled-before-pop`. Rejected addressed inputs are processed-current.
Cancelled timer later popped changes disposition to processed-stale without
creating another record. Partition totals equal created input+timer+output
records and never exceed 42; cumulative pending and processed histories
cannot disguise over-allocation. Track offered, accepted, rejected,
timer-created, timer-cancelled, stale-popped, current-timer-processed,
output-committed and output-processed separately.

Attempt 17 is assigned its final lifetime audit ID and increments offered
to 17. Atomically commit `REJECTED_CAP_OVERFLOW` as processed-current
**before** cleanup/READY, without timestamp validation or settling.
Increment generation, clear uncommitted coordinates/polarity/magnitude/
active time/tokens, set R=0 and armed=false, retain issued, counters,
`terminal_reason=ABORTED`, and any previously committed output unchanged.
Close the retired episode's ingress; later packets receive no component ID
or component record. A later fresh STORE needs the READY/prior-output guard.
Queue/timer/identity exhaustion similarly fails closed, never quiet success.
The arithmetic 42 proof depends on actually enforcing each cap before
allocation; reporting counts afterward is insufficient.

## 9. C0–C7 expectation freeze and remaining materialization gaps

The accompanying table retains the reviewed names, states, amplitudes and
HOLD durations exactly. All listed outcomes are **required predictions**
or fail-closed rules, not experiments. Symbolic states/root identities,
transition fields, budget caps and conditional minimal-plan counts are
frozen. Concrete root intervals, q neighbors, ceilings, near-clock packets,
below-ULP packets, lineage/source strings, actual ID assignments and full
C7 schedules have not been independently certified; the table explicitly
leaves those null/unresolved. No arbitrary t_store, observation window,
checkpoint times, malformed-packet encoding, or RESET offset has been
invented to fill those gaps. A symbolic equality case is not automatically
a deliverable binary64 packet. In particular exact expiry equality and
converted-expiry arrival require separate proofs of their interpretation.

Therefore this is not a completed pre-execution serialized fixture freeze.
Before implementation eligibility, a reviewed certificate revision must
resolve the numerical fields and bind any remaining materialization details
without changing the reviewed setups, tolerances or fail-closed rules.

## 10. Required-claim pass/fail table

Here `PASS (analytic)` means exact real-arithmetic proof only; `SPECIFIED`
means normative protocol, not implementation evidence.

| Contract claim | Status | Evidence / unresolved gate |
|---|---|---|
| 1. Rest/eigenvalues/stability | PASS (analytic) | Section 3; R=0 all states frozen, R=1 unique stable origin. |
| 2. Disk/finite region | PASS (analytic); operational BLOCKED | Lyapunov proof; rounded candidate disk/identity enforcement absent (N4,N6). |
| 3. Neutral RECALL | PASS (analytic); adapter unexecuted | BX=0 and READY rules; no runtime claim. |
| 4. q/2,1,2; tangent | PASS (analytic); neighbor BLOCKED | Exact peak/tangent proof; representable q neighbors missing (N2). |
| 5. A=4 release/matched HOLD | PASS (analytic); numerical BLOCKED | Same preload/gate-only contrast; root/time witnesses missing (N1,N3). |
| 6. Surface/direction/uniqueness/re-arm | PASS (analytic); numerical BLOCKED | Monotonic lobe proofs; interval direction/order missing (N1,N3). |
| 7. Quiet/terminal/finite lifetime | PASS (analytic), SPECIFIED lifecycle | Radius/log proof; quiet/expiry conversions missing (N1,N3). |
| 8. Active/absolute time and strict order | Formula proved; BLOCKED | Mapping and macroscopic expiry margin; individual ceilings/C7 unproved (N3,N5). |
| 9. Exact comparison/error | Rule frozen; BLOCKED | Strict theta/4 test; no candidate operational error proof/checkpoints (N4,N5). |
| 10. Refinement/conversion | Rule frozen; BLOCKED | No outward transcendental implementation or root intervals (N1,N3). |
| 11. Timers/unique records | Conditional count proof, SPECIFIED; enforcement pending | Immutable 24/42 caps and partition; no adapter verification (N6). |
| 12. Attempt 17/closure | SPECIFIED; enforcement pending | Commit-before-cleanup and persistent output; no execution (N6). |

### Exact unresolved gates

* **N1:** No rigorous 256–1024-bit outward pi/sqrt/exp/sin/cos/log
  enclosures, remainder/range-reduction/directed-rounding proofs, numeric
  threshold bounds or <=128-bisection root/direction interval witnesses.
* **N2:** No certified hexadecimal binary64 neighbors of exact q, adjacency
  and entry comparison witnesses; symbolic q/q/2 are not rounded substitutes.
* **N3:** No common-endpoint ceil64 witnesses for output/re-arm/quiet/expiry
  or independently mapped C5 shifts; strict-future/domain/distinct-order/
  expiry comparisons, cap-resolution and below-ULP cases remain unproved.
* **N4:** No independently derived operational error bound for any specified
  candidate binary64 arithmetic, state/disk adherence, threshold representation
  and active-time accumulation. Strict A=1 norm check remains unevaluated.
* **N5:** No complete numeric pre-execution freeze: concrete A=1 checkpoints,
  delivery/order/ID/lineage materialization, C7 reset/pause/overflow/near-clock/
  coalescence/below-ULP schedules and reachable versus synthetic tie cases
  require reviewable independent certificates. Do not choose values silently.
* **N6:** No runtime cap/queue/identity/token/ordering/persistence enforcement
  evidence, by authorization. This is a future conformance gate, not a request
  to run Stage B now; symbolic accounting alone is not runtime validation.

N1–N5 alone are sufficient to block a completed Stage A numerical PASS.
N6 must remain a separately verified Stage B obligation after, not instead
of, an independent numerical PASS. None of these gaps warrants changing an
equation, cap, threshold, fixture or tolerance.

## 11. Deterministic future replay and validation boundary

After a separate Luna-0 PASS against exact frozen hashes/revision only,
two genuinely fresh executions/materializations must use the same declared
inputs/configuration/order/identity initialization and independently owned
oracle, not copied output artifacts or shared runtime numerical code.
Record platform/interpreter/dependency/compiler/FMA/rounding pins, commands,
raw deterministic outcomes, maximum state error, event-time error, event-count
and terminal-state agreement per fixture. Compare records/dispositions,
state traces, output identity/time/payload and all record counts. State error
is interval-certified; event-time agreement requires identical certified
ceil64 values; qualitative plots are not a numerical oracle.

Before interpretation verify disk bounds, old-gate settlement, precedence,
one-shot/direction, re-arm, quiet, expiry, strict future, immutable output,
tokens/generations, overflow/closure and 42 accounting. Preserve unresolved
cases and failures. Do not tune tolerance against candidate output.

Only certificate self-consistency/hash checks are run in this preparation.
The first checker invocation passed 55 assertions and failed one framing
assertion: the Windows edit tool serialized CRLF while the initial checker
expected LF. The SHA256 comparison had passed. Serialization metadata and
the checker were corrected to explicitly pin actual UTF-8/CRLF raw bytes,
not to normalize inputs or weaken numerical checks; the manifest was
recomputed. That intermediate CRLF checkout-hash policy was subsequently
superseded after independent review identified Git's LF blob normalization.
The final policy hashes raw Git content and checks HEAD/index/clean-filtered
checkout agreement, so LF/CRLF checkout choice cannot alter the hash.
This failed validation and intermediate policy are retained here, not suppressed.
All required Stage B regression families (focused mechanism, numerical
certificate arithmetic, event-time/representability, crossing/re-arm,
record-bound/overflow, relevant E2/excursion, historical/core) have **0 tests
executed, 0 test-framework skips reported; entire families NOT RUN because
Stage B is locked**. Full repository suite is NOT RUN; no shared/production
edit/import was made. Metadata checks are not any of those scientific tests.

The permitted disposition is exactly **BLOCKED — NUMERICAL CERTIFICATE
INCOMPLETE** (scientific execution disposition, if requested: **BLOCKED**,
no mechanism executed). It is not PARTIALLY SUPPORTED or NOT SUPPORTED:
there is no experimental evidence for either. This report makes no claim of
sequence memory/order/replay, task echo/efficacy, training, generalization,
adaptive-time integration, hardware equivalence, ACP acceptance, architecture
promotion, production defaults, integrated echo or Luna-64.
