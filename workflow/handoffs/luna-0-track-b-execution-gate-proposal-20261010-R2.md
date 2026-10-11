# Luna-0 — Track B / Luna-64 mathematical execution gate R2

**GATE:** `L64-TB-GATE-20261010-R2`  
**PREDECESSOR R1 PROPOSAL SHA-256:** `44BD46E561BDD9329616B38C3AE6A74A1E79BEB497BB274A4D552C6096FC46B6`  
**PREDECESSOR R1 PROTOCOL SHA-256:** `A90F167C5C09DC84E7B15B778770A3115CAB7AB91177AE3D0A026E755B013CAF`  
**PREDECESSOR R1 MANIFEST SHA-256:** `F5989C457A77203CC1D10534390F2720BC9C33612E675A375ED65BB71185812D`  
**R1 REVIEW SHA-256:** `2B92984E351CF305514CC2C15A79D64C4E25A495B89B5BDC026C7B638D8AD5A2`  
**R0 PROPOSAL SHA-256:** `5B4C8E74C3536AEA7111C749970FF44BA3DB8855317679C6EF013EAB5149CF08`  
**STATUS:** DRAFT FOR INDEPENDENT REVIEW — NOT FROZEN  
**OWNER APPROVAL:** NOT PROVIDED  
**EXECUTION:** NOT AUTHORIZED  
**LUNA-64 CONTRACT:** PRESERVED, NOT AMENDED  
**LUNA-63C:** READ-ONLY; NO DEPENDENCY; NO SCOPE CHANGE

This is governance/specification work only. No benchmark, experiment,
microbenchmark, generator materialization, experimental code, branch, or
worktree was created. R0, R1, both reviews, and their manifests remain
unchanged. R2 contains a fully written candidate PCN and proposed event
contract to make review concrete; unaccepted scientific choices and
unverified compatibility are explicitly not treated as resolved.

## 1. Reconciled source state

Current `HEAD == main == origin/main` is
`73aaa50f97ceab322907875ae4dcf23e7541c3b5`. The Luna-64 contract, governance
PASS handoff, workflow/changelog additions, R0/R1 documents and this R2
package are local uncommitted governance artifacts. This SHA is a
source-baseline candidate, not an execution freeze. The existing governance
PASS is documentation-only. Luna-63C Stage A remains certificate-gated and
Stage B remains blocked by its independent certificate review.

Repository-wide search finds no authoritative `LWU` definition. The
authoritative local software meter found is `LocalEnergyModel` in
[`energy_utility.py`](../../tpcn/energy_utility.py), whose default unit is
`activity-cost-proxy`; it does not define operation-equivalent energy or
joules. The architecture contract A09 likewise leaves the local estimate
hardware-dependent.

## 2. R1-to-R2 finding matrix

| R1 finding | R2 correction/proposal | Acceptance test required before any freeze | Independent verification | Disposition |
|---|---|---|---|---|
| 1. PCN equations incomplete; dense parameter count 336 exceeds 256 | §3 defines a tanh reconstruction PCN with a 4-state latent, an exact scalar objective, its full gradients, four fixed inference iterations, and 40 decoder parameters | Recompute all gradients by central finite differences on frozen fixtures; verify `P_total=40` and every state/parameter bound | Independently derive gradients, calculate counts, evaluate worked examples; compare to protocol JSON | Candidate math is complete; task-level readout/reward linkage still needs owner decision |
| 2. Timebase reciprocal error and missing fixtures | §4 fixes `1 tick = 10^-6 TU`, exact integer timestamps, delays and conversion examples | Check reciprocal units, nonnegative/increasing timestamps, serialization round-trip, tie and expiry cases | Recompute dimensional table and test fixture conversion independently | Timebase corrected in proposal; golden generated fixtures not materialized |
| 3. Arm E reward timing changes with transformed B times | §5 preserves physical reception IDs/times/rewards and confines control transformation to a decoder-view gap feature computed causally from the current observed gap | Across each paired D/E fixture, compare IDs, event count, magnitude, physical times, activation IDs and reward due ticks exactly; ensure transform has no future access | Independently apply transform to golden event stream and compare; audit that reward queue keys only use physical fields | Candidate proposal; needs independent causal-clock review because decoder-visible elapsed time and physical reward clock differ |
| 4. Credit expiry/episode reset conflict | §6 gives integer-tick state machine, expiry at due+1 tick, sequence-close vs settlement-close, serial episodes, and duplicate semantics | Exercise before/equal/after due, sequence close, no reward, duplicate, overflow, reset; verify pending record survives sequence close and not episode reset | Independently construct event traces and prove finite bound and exact phase order | Candidate rule is explicit; interaction with two clocks in E remains open |
| 5. Frozen evaluation conflicts with update-based attribution; scoring ambiguous | §7 separates training updates from evaluation inference; attribution is counterfactual *unapplied* update; labels exist only in evaluator; controls and A/B N/A metrics separated | Snapshot parameters before/after eval and prove equality; independently hand-score tiny confusion and attribution fixtures; no zero-imputation for N/A | Reviewer reproduces metrics and verifies reward/update boundary | Corrected proposal; primary readout/reward mechanism still requires owner decision |
| 6. Statistics incompletely specified | §8 enumerates `5^5` seed bootstrap tuples, equal-weight paired seed effects, quantile ranks, Bonferroni family, missing/zero rules | Miniature exact dataset must reproduce every order statistic, interval and pass/fail branch | Independent hand computation and exact arithmetic audit | Algorithm specified; five-seed inference remains low-power and unvalidated |
| 7. Workload/runtime feasibility weak | §9 gives count and memory bounds; keeps 4-hour ceiling as unverified stop limit, not a claim; no microbenchmark authorized | Recompute all event/inference/credit/storage bounds and include settlement events and report artifacts | Independent analytical upper-bound review; empirical feasibility may only be tested under a later explicit authorization | Empirical feasibility remains BLOCKED |
| 8. No authoritative LWU | §10 removes LWU and replaces it with proposed local work count (LWC), separate from `activity-cost-proxy` and explicitly nonphysical | Verify meter call/counter logs against event fixtures; perform coefficient sensitivity; owner must approve this new experimental proxy | Inspect repository meter authority; independently recalculate raw and weighted work | Proposed instrument only; no authoritative unit or approval |
| Additional: decoder/reward activation not consistently local | §5 distinguishes physical common activation from decoder prediction/readout; proposes a shared local event adapter | Show activation is caused only by local input with no task truth, and D/E reward provenance remains identical | Reviewer audits causal DAG and exact paired D/E reward schedule | **OPEN owner/scientific decision** |
| Additional: timebase mapping in protocol disagreed | §4 and JSON use `tu_per_tick=0.000001` and `ticks_per_tu=1,000,000` | Exact round-trip tests for all frozen durations | Independent reciprocal/dimensional check | Corrected draft |
| Additional: model capacity vs arms incomparable | §3 declares per-arm full counts and reports counts beside results | Recompute all trainable and runtime state counts; confirm cap ≤256 | Independent equation audit | Candidate counts supplied; task output/readout still missing |

The acceptance tests are required future freeze checks, not tests performed
here. An unresolved disposition blocks gate readiness.

## 3. Complete candidate PCN: equations and counts

This is one coherent **proposal**, not adopted TPCN architecture. It is a
small local predictive model. Numerical state and parameter values are
binary64; channels and bounds are exact.

### 3.1 Inputs, state, parameters

Input `x_t ∈ {0,1}^8` is one-hot event-channel identity
`[A,B,N0,N1,N2,N3,N4,N5]`. A silent interval causes no input event. Elapsed
time is local integer tick difference `Δt_tick`; define `Δt_TU=Δt_tick/10^6`.

Persistent state `z^- ∈ [-1,1]^4` is the latent state after the preceding
input. It decays only when this local unit next processes an event:

```text
d_t = exp(-Δt_TU / τ), τ = 2 TU
z0 = clip(d_t z^-, -1, 1)
```

Prediction parameters are `V ∈ [-1,1]^(8×4)` and `c ∈ [-1,1]^8`.
Initialization is fixed, no RNG:

```text
V[i,j] = 0.25 if i=j
         0.125 if i=j+4
         0 otherwise
c[i] = 0
z^- = 0
```

No trainable time constants, input projection, recurrence matrix, or task
labels exist. The recurrent temporal dependence is the bounded local state
`z^-` and analytic elapsed-time decay.

### 3.2 Prediction, error, objective, and inference

At reception, before incorporating `x_t`, form the one-step prediction:

```text
xhat_pre = tanh(V z0 + c)
epsilon_pre = x_t - xhat_pre
```

`epsilon_pre` is the explicit predictive-coding error. For event assimilation,
minimize the single declared objective over bounded latent `z`:

```text
y(z) = tanh(V z + c)
F_t(z) = 0.5 ||x_t - y(z)||_2^2 + (λ/2)||z-z0||_2^2
λ = 1
```

The analytic gradient is:

```text
g_z(z) = -V^T[(x_t-y(z)) ⊙ (1-y(z)⊙y(z))] + λ(z-z0)
```

Use fixed-step projected gradient inference with exactly four iterations,
not convergence detection:

```text
z^(0) = z0
z^(k+1) = clip(z^(k) - γ g_z(z^(k)), -1, 1), γ=1/16, k=0,1,2,3
z_t = z^(4)
xhat_t = tanh(V z_t+c)
epsilon_t = x_t-xhat_t
```

There is no claim of convergence; the fixed iteration cap is the definition.
Every operation is deterministic. Clipping is part of the declared update.
NaN/Inf faults the episode; it is never replaced.

### 3.3 Predictive learning and reward learning are separate

For `y=xhat_t` and inferred `z=z_t`, the objective's parameter gradients
holding the inferred state fixed (block-coordinate partial derivatives) are:

```text
q = (x_t-y) ⊙ (1-y⊙y)
g_V = -q z^T
g_c = -q
```

Predictive-error learning, if authorized, is an immediate bounded local SGD
step:

```text
V ← clip(V - η_PE g_V, -1, 1)
c ← clip(c - η_PE g_c, -1, 1)
η_PE = 1/1000
```

This is a partial-gradient step at the inferred latent, not the total
derivative through all four inference iterations. That choice is explicit.
It does not use a class label.

For each reception retain a bounded eligibility vector equal to its local
gradient contribution `(g_V,g_c)`, with event-driven decay
`a(Δt)=exp(-Δt_TU/τ_e)`, `τ_e=1 TU`, component clipping to `[-1,1]`, and
expiry after 8,000,000 ticks. At an accepted reward `r∈[-1,1]`, apply a
separate reward-modulated update:

```text
V ← clip(V - η_R r e_V, -1, 1)
c ← clip(c - η_R r e_c, -1, 1)
η_R = 1/100
```

The immediate event cost is recorded once at reception, before reward
eligibility is known. Neither `F_t`, `epsilon_t`, reward, nor the cost proxy
is substituted for another. Reward does not retroactively erase or recharge
the event cost.

If `r=0`, the reward parameter delta is exactly zero. If `r=+1` is delivered
after 4 TU, the eligibility is multiplied by `exp(-4)` before applying the
separate reward update; for 16 TU this eligibility would have expired under
the proposed 8-TU input trace, so an activation-associated snapshot is
required under §6.

### 3.4 Worked analytical example (not an executed experiment)

Consider one coordinate with `V[0,0]=0.5`, `c[0]=0`, `z0=0`, `x[0]=1`,
`λ=1`, and all other coordinates zero. At the initial point:

```text
y= tanh(0)=0
epsilon=1
g_z = -0.5
```

One inference update with `γ=1/16` gives `z=0.03125` (the protocol's four
steps repeat the same stated equation; this example reports the first step).
Then `y=tanh(0.015625)≈0.0156237286`, `epsilon≈0.9843762714`,
and `q=epsilon(1-y²)≈0.9841359`.

For the first coordinate:

```text
g_V = -q z ≈ -0.03075425
g_c = -q ≈ -0.9841359
```

One predictive learning update with `η_PE=0.001` therefore yields
`V≈0.5000307543`, `c≈0.0009841359`. A zero reward gives exactly no reward
update. A reward `r=1` four TU later applies the decayed stored gradient
`exp(-4)g`; with `η_R=.01`, the V reward increment is approximately
`+0.00000564`, distinct from the predictive update. These rounded values
illustrate the equations only; they are not a recorded numerical run or a
finite-difference check.

Required independent verification before freeze: central differences for
every component of `F_t` with respect to `z,V,c` on multiple interior
fixtures, step sizes `h∈{2^-12,2^-16,2^-20}`, maximum absolute gradient
error ≤`1e-7` away from clip boundaries; separate one-sided/clamp fixtures;
recompute the worked example in an independent implementation. None was run
for this governance draft.

### 3.5 Proposed parameter-count table

`P_total = Σ_j P_j`. Runtime states/history/eligibility are not trainable
parameters and are listed separately.

| Arm | Trainable parameter groups | `P_total` | Runtime state (not parameters) |
|---|---|---:|---|
| A cost-only | none | 0 | meter counters only |
| B simple eligibility/readout proposal | fixed one scalar weight per 8 channels | 8 | 8 traces, ≤32 identities |
| C linear next-channel predictor | `A∈R^(8×8)` plus `b∈R^8` | 72 | 8-channel local state |
| D nonlinear PCN | `V∈R^(8×4)` plus `c∈R^8` | 40 | latent 4, inference scratch 4, error/prediction vectors 8 each, eligibility gradient 40 |
| E same nonlinear PCN | exact same groups as D | 40 | D state plus transformed decoder-view clock |

All counts are at most 256. This does not solve capacity comparability or
primary task output: B/C/D/E must use one fully specified and accepted scoring
interface. That interface remains an explicit freeze gate.

## 4. Canonical integer timebase

| Quantity | Canonical representation |
|---|---|
| Base unit | integer microtick; `1 tick = 10^-6 TU`, equivalently `1 TU = 1,000,000 ticks` |
| Event timestamp | signed 64-bit integer ticks, nonnegative and episode-local |
| Binary64 conversion | display/interop only: `t_TU = ticks / 1,000,000`; never used to order or expire |
| Reward delays | `{0, 4, 16} TU` = `{0, 4,000,000, 16,000,000}` ticks |
| Eligibility trace expiry | event-local age `>8,000,000` ticks; entry at exact age equality remains valid |
| Credit record expiry | reward due tick + 1 tick |
| Logical sequence completion | final input event has been processed; no further inputs accepted |
| Physical episode cleanup | after all reward records settle/expire at final-input tick +16,000,001 ticks |
| Numerical tolerance | none for tick comparisons; exact integer equality/order; real-valued PCN checks use the specified independent gradient tolerance |
| Serialization | canonical JSON integer tick field; include `timebase_id="L64-TB-R2-1us"` |

Conversions: `0.25 TU → 250,000 ticks`; `4 TU → 4,000,000 ticks`;
`16 TU → 16,000,000 ticks`. `1 tick → 0.000001 TU`. A timestamp supplied
as non-integral ticks is invalid, not rounded. Overflow outside signed 64-bit
range faults visibly. Event order uses `(timestamp_ticks, phase, canonical
parent_id, child_ordinal)`; the phase is a deterministic tie-break, never a
replacement physical timestamp.

## 5. Arm E: causal temporal control proposal

The proposed E transform does not change physical input event IDs, times,
magnitudes, reward origins, reward due ticks, training opportunity count, or
evaluation targets. For each consecutive physical input gap
`g∈[0,8 TU]`, produce decoder-view gap:

```text
g_E = 8 TU - g
```

The gap is available at reception from the current and previous physical
timestamps; no future event is consulted. Equal-view-time ties use physical
event ordinal. E retains both physical and decoder-view times in separate
fields. Reward activation/delivery identity and timestamp use only physical
time, never `g_E`. Thus input/reward lineage is preserved even though
decoder temporal features are disrupted. A gap of exactly 8 TU maps to zero
view gap, with ordinal tie ordering.

This is a **complementary-gap temporal control**, not a random permutation and
not a time-shuffled dataset. It reverses short/long gap scale while preserving
event order. It can test sensitivity to timing relationships but cannot by
itself serve as an order-disruption negative control. If the accepted Luna-64
contract requires order disruption, this R2 control is insufficient and
requires an explicit scope decision; do not claim it disrupts order.

Open compatibility check: local decoder elapsed-time state uses decoder-view
time in E while reward is delivered on physical time. The implementation
would need a separately declared physical delivery queue and decoder-local
view clock without using one as the other's neural timestep. This draft
specifies both clocks but does not assert their event-runtime integration has
been validated. The independent reviewer must check the causal relation and
bounded adapter interface.

## 6. Credit state machine and episode lifecycle

This is a candidate Option B two-stage bounded credit design.

```text
ELIGIBILITY_ACTIVE
  -- local activation and nonempty eligible set --> CREDIT_CAPTURED
CREDIT_CAPTURED
  -- activation event committed --> AWAITING_REWARD
AWAITING_REWARD
  -- unique reward delivered before/equal due+0 tick --> REWARD_SETTLED
  -- expiry at due+1 tick without reward --> EXPIRED_WITHOUT_REWARD
  -- duplicate reward ID --> remain in current state; record DUPLICATE_NOOP
Any live state
  -- capacity/identity fault --> EPISODE_INVALID
REWARD_SETTLED or EXPIRED_WITHOUT_REWARD
  -- cleanup --> EPISODE_RECORD_REMOVED
Sequence complete is a separate flag; it does not erase pending credit.
Episode reset is permitted only after every credit is settled or expired.
```

Each episode has at most 32 inputs and one B event by the proposed generator,
so at most one activation-associated credit record per episode; the general
runner cap is 32 activations/records to fail closed if a generator changes.
Each record holds at most 32 `(input_id, eligibility_scalar, gradient40)`
links; max 32×32 links and 32×32×40 binary64 gradient elements per episode
under the fail-closed general cap. No records cross episode reset. Episodes
run serially; next episode may start only after the prior settlement horizon.

Same-tick phase precedence:

1. explicit expiry events whose expiry tick is this tick;
2. input reception/accounting;
3. local activation;
4. reward origin;
5. reward delivery;
6. credit application;
7. cleanup.

Credit expiry is due+1, so exact-due reward is processed one tick before
expiry; a delivery at expiry tick is rejected. The integer-tick examples:

| Case | Result |
|---|---|
| reward at `due−1` or `due` | accept once if parent/origin valid |
| reward at `due+1` or later | expired/no update |
| sequence completion at due | mark sequence complete; retain credit until settlement |
| reward after final input but before settlement | accept if within record due/expiry and origin identity valid |
| no reward | expiry record, no update |
| duplicate delivery | stable ID recognized, no second update |
| reset while any credit pending | invalid operation; reject reset |
| overflow | explicit typed overflow; episode invalid, no silent eviction/truncation |

**Open semantic gate:** the contract requires delayed activation reward but
does not identify the source of a beneficial/unbeneficial reward. The R1/R2
candidate fixed `+1` reward on B reception is local and label-free but may
reinforce every B independent of informativeness; it is not established as
the intended reward decoder objective. Do not treat that source as approved.

## 7. Training/evaluation separation and readout boundary

Training has mutable local predictor parameters and may perform the explicit
prediction-gradient and delayed reward-gradient updates in §3. Every update
records parameter snapshot ID, local gradient ID, reward ID if present,
before/after parameter hash, and separate update type. The evaluator labels
and condition IDs remain in an evaluator-only process/record.

At evaluation start, hash/freeze all model parameters. Each episode resets
latent, eligibility, credit, and duplicate-ID state; inference latent state
may update causally during the episode, but parameters may not. Reward may
settle credit diagnostics but cannot change parameters or readout. Report
prediction error, inference operations, local view/physical latency,
eligibility and credit occupancy, and *unapplied counterfactual* update
magnitude separately from actual updates. Verify before/after parameter
hash equality.

No agreed mapping currently turns PCN latent/prediction state into binary
order/timing output without evaluator truth or additional readout training.
The candidate readout is therefore **not specified**. A/B cannot produce
prediction accuracy; mark it `NOT_APPLICABLE`, not zero. The success criterion
cannot compare A's “cost per correct” when no correct denominator exists.
Before freeze, the owner must select a label-free local task-output interface
or authorize a separate downstream evaluator/readout protocol; that choice
must preserve the contract's no-label-leak boundary. Primary task efficacy
remains blocked until then.

## 8. Statistics and exact metric policy (proposal)

Keep R1's five seeds `6401..6405`, paired episode identities, and four
proposed primary comparisons `D−C` and `D−E` on order/timing balanced
accuracy. For a valid future scorer, per-seed confusion matrices are computed
first; balanced accuracy is the arithmetic mean of class-specific recall.
The comparison effect is equal-weight mean of the five per-seed paired
differences.

Enumerate all `5^5=3,125` seed-index tuples with replacement, recompute the
equal-weight paired effect for each, sort ascending, and use nearest-rank
order statistics 20 and 3,106 for each 98.75% interval. This is a proposed
Bonferroni family-wise 95% interval across four comparisons, not a claim of
valid coverage with five clusters. No p-value test is proposed. Report each
seed result. If an arm/seed has >1% invalid episodes, verdict is blocked; if
either class is absent, endpoint is undefined and inconclusive. For zero
correct outputs, cost-per-correct is undefined/infinite without epsilon.
No metric is imputed for A/B. Confusion labels for silent/uncorrelated
controls remain undefined pending the output-interface decision; only
predeclared event false-positive counts may be reported after activation
identity is frozen.

Success proposals (not authorized/frozen): D balanced accuracy ≥0.70 on both
tasks, D−C and D−E ≥0.10 on both, adjusted interval lower bounds >0, D−C
positive on at least four seeds, false output ≤0.05 on controls, and the
delayed-credit criterion only after approved reward/readout semantics.
The proxy-efficiency part of R0 is removed unless the LWC proposal in §10
passes owner and independent review. Do not use test outcomes to revise any
criterion.

## 9. Resource and runtime bound (analytical only)

Proposed caps retained unless separately approved:

- five arms × five seeds × 10,000 train episodes = 250,000;
- five × five × 2,000 evaluation episodes = 50,000;
- ≤32 physical input events/episode; one proposed B activation/episode;
- ≤4 inference iterations per event; at most 8×4×4×32 = 4,096 latent-gradient
  scalar contribution terms/episode for D/E, before parameter updates;
- ≤40 model parameters for D/E; ≤72 for C; ≤8 for B;
- ≤32 input eligibility entries; ≤32 credit records; ≤32 input links/credit;
- at most 32×32×40 = 40,960 stored gradient scalars if all defensive caps
  are simultaneously used; at 8 bytes/scalar = 327,680 bytes, excluding IDs;
- operation logs are capped by 256 records ×256 bytes = 65,536 bytes/episode;
  any overflow invalidates the episode;
- one active episode at a time, and no reset until reward settlement/expiry.

The R1 4-hour, one-core, 2-GiB limits are proposed hard stop ceilings, not
measured feasible budgets. Work bounds omit Python/runtime overhead and all
hash/serialization/log costs. No benchmark or microbenchmark ran. Therefore
feasibility remains unverified; a later separately authorized smoke run or a
revised analytical workload is required before treating this as an executable
gate.

## 10. LWU disposition and proposed LWC

Repository LWU is undefined. R2 removes all LWU/energy-per-correct acceptance
claims. Existing `activity-cost-proxy` remains a local configurable proxy and
must be reported only with its explicit supplied category costs and counts.

For experimental software work only, propose **L64 local-work count (LWC)**,
not an energy unit. Raw counters are authoritative and reported separately:
received events, cost-meter calls, inference iterations, scalar add/subtract/
multiply/divide/compare, `exp`/`tanh`, parameter/state reads/writes, eligibility
updates, credit record create/settle/expire, duplicate/drop/overflow counts.
One LWC is a declared dimensionless accounting score:

```text
LWC = 1*received_event
    + 1*scalar_add_subtract_multiply_compare
    + 4*scalar_divide
    + 8*(exp+tanh)
    + 1*(scalar_state_or_parameter_read+write)
    + 1*eligibility_update
    + 1*credit_record_create_or_settle
```

Coefficients are proposed conventions, not empirical hardware costs. Always
publish raw counters. Sensitivity table recomputes aggregate with special
function coefficient `8×{0.5,1,2}` and all other coefficients fixed; if the
arm ranking changes, no LWC-based efficiency conclusion is permitted.
Instrumentation is outside neural inputs and must be measured as separate
counter overhead; the counters do not themselves feed the decoder. No joule,
power, calibrated energy, or A09 physical-energy claim is made. Owner and
independent review must accept this new proposal before use; otherwise report
only raw operations and existing `activity-cost-proxy`.

## 11. Isolation and Luna-63C protection

Only after all independent review and owner gates may the proposed branch
`experiment/luna64-track-b-ltrd` and dedicated worktree be created. Execution
base must be the later committed governance-freeze SHA, not the current
`73aaa50f97ceab322907875ae4dcf23e7541c3b5`.

Allowed execution writes:

- `experiments/luna64/**`
- `tests/test_luna64_*.py`
- `artifacts/luna64/**`
- `workflow/handoffs/luna-64-track-b-ltrd-execution-20261010.md`

Forbidden: `tpcn/**`, all other tests, `experiments/luna63c/**`,
`artifacts/luna63c/**`, C0-C7 fixtures/semantics, W/T/E/N5 evidence, all
Luna-63C certificate/manifests/reconciliation files, architecture contracts,
ACPs/defaults, unrelated artifacts, merges, production integration, and
hardware dependencies. Any out-of-scope file need blocks and requires a new
authorization. No task truth, future events, or evaluation labels may enter
the model.

## 12. Publication and review boundary

This draft does not update workflow/changelog because it is not execution
ready and has not passed review. A new independent Luna-0 reviewer must verify
the exact R2 hashes, all equations and gradients, counts, timing, E control,
credit lifecycle, scoring, statistics, resource bounds, LWC authority, and
all R1 review findings. The reviewer must not implement or run the experiment.

If review is BLOCKED, preserve this R2 proposal and review separately, keep
execution blocked, and prepare R3 only after resolving findings/owner choices.
Even a review PASS would mean only **READY FOR OWNER AUTHORIZATION**. The
owner must approve this exact gate ID and bytes before documentation freeze
and worktree creation.

## 13. Current blockers / disposition

1. Owner/scientific decision on label-blind activation and reward source.
2. A single causal physical/view-time integration for E and reward settlement.
3. A readout that measures temporal discrimination without evaluator truth and
   is compatible across arms.
4. Independent finite-difference and worked-example verification; no checks
   executed in this governance phase.
5. Golden generator fixture and exact PRNG draw-name/materialization contract.
6. Empirical runtime feasibility remains unknown; microbenchmark unauthorized.
7. LWC is a new unapproved proposal; existing meter costs need fixed ownership
   and idempotency before use.
8. Statistical inference with five seed clusters has not been validated and
   remains explicitly exploratory.

**R2 independent review:** pending.  
**Owner approval:** not provided.  
**Execution authorization:** not granted.  
**Branch/worktree:** none.  
**Scientific evidence:** none.
