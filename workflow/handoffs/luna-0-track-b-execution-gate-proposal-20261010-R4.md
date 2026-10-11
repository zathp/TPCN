# Luna-0 — Luna-64 Track B R4 scientific validity gate

**GATE:** `L64-TB-GATE-20261010-R4`  
**PROTOCOL REVISION:** `4.3.0-draft`  
**STATUS:** CORRECTIVE GOVERNANCE CANDIDATE — REVIEW REQUIRED  
**REVIEW VERDICT:** PENDING  
**OWNER APPROVAL:** NOT PROVIDED  
**PILOT AUTHORIZATION:** NOT PROVIDED  
**IMPLEMENTATION / SCIENTIFIC EXECUTION:** NOT PERFORMED  
**EXECUTION BRANCH / WORKTREE:** NOT CREATED  
**ARCHITECTURE PROMOTION:** NOT AUTHORIZED

This R4 proposal addresses the eight R3 independent-review blockers and
preserves the Luna-64 contract and original documentation-only governance
record. All scientific choices below are candidate experiment semantics,
not owner-approved policy or TPCN architecture. R4 can at most become
**READY FOR OWNER AUTHORIZATION OF THE FEASIBILITY-ONLY PILOT**. It cannot
authorize that pilot, efficacy execution, implementation, or architecture
promotion.

## 1. Reconciliation and R3 finding matrix

At preparation, `HEAD == main == origin/main ==
73aaa50f97ceab322907875ae4dcf23e7541c3b5`. The working tree already contains
modified workflow/changelog files and untracked Luna-64/R0–R3 governance
artifacts. No such file has been discarded or silently treated as committed.
The independent R3 review confirmed all six R3 package hashes and returned
**BLOCKED**. Its eight blockers map to R4 as follows:

| # | R3 finding | Candidate correction | Independently testable acceptance condition | Status |
|---|---|---|---|---|
| 1 | Equal-share eligibility does not establish temporal selectivity; 8 TU covers all task events. | Replace equal share with a local event score-delta gate and bounded exponential recency kernel; add near irrelevant and distant informative events. | Golden tests distinguish equal-strength events by age, equal-age events by local contribution, reduce near zero-contribution distractor attribution, exclude age `> H`, and compare uniform and recency-only controls. | Specified in R4 candidate; review required. |
| 2 | PCN event-to-event latent transition / reset was incomplete. | Fully define event-triggered state, decay, impulse input, latent initialization, four inference steps, prediction/error, parameter update, silence, simultaneous ordering and resets. | Independently reproduce three-event state trace and verify reset, lazy silence and equal-time transitions from protocol bytes. | Specified in R4 candidate; review required. |
| 3 | R3 validator silently accepted duplicate keys. | Add a strict JSON parser that detects duplicate object keys before materialization, require the exact protocol-derived Draft 2020-12 schema, and test invalid inputs through the public CLI. | Public CLI rejects duplicate root/nested keys, malformed/nonfinite input, permissive or mismatched schema, and all schema/cross-field negatives. | R4.1 local tests pass; independent re-review pending. |
| 4 | Bootstrap replay keys and outcome regions were incomplete/overlapping. | Freeze exact generator and bootstrap key fields, explicit two-comparison family mapping, both adjusted CI fields, missing policy and priority-ordered exhaustive decisions. | Reproduce generator/bootstrap goldens; test both CI bounds, missing-CI and verdict boundaries. | R4.1 tests pass locally; independent re-review pending. |
| 5 | 20 seeds and 32 computational units lacked justification. | Withdraw 32 abstract units. Use explicit parameter/state/operation/storage counts. Do not assert efficacy power where between-seed variance is unknown; isolate pilot from efficacy decisions. | Recompute all parameter/state counts and operations; document why no efficacy sample size or power claim is made; pilot outputs cannot tune efficacy thresholds. | No efficacy-power claim. |
| 6 | Runtime / memory ceilings were unmeasured for 1.2M episodes. | Replace immediate 1.2M-run authorization request with a bounded, feasibility-only pilot proposal and analytical work/space model. | Recompute episodes/events/PCN iterations/operation range/log bytes; no runtime claim until measured by a separately authorized pilot. | Runtime remains **UNVERIFIED**. |
| 7 | Governing inputs absent from manifest and uncommitted. | Add a working-tree provenance inventory containing raw SHA-256, Git blob OID when available, commit/tree presence and status for governing/history inputs. Define two-stage publication and re-verification. | Independent reviewer reproduces all hashes; publication freeze commit is recorded only after approved documentation publication and final content re-hash. | **NOT IMMUTABLE**: governing source artifacts are currently uncommitted. |
| 8 | Cost-benefit question not measured. | Freeze accuracy, attribution-specificity, work, memory, reward work, event-cost proxy, and cost-per-correct metrics; require efficacy plus an operation-ratio constraint. | Statistical decision is success only if both efficacy and attribution thresholds pass while cost caps pass; excessive cost or worse accuracy cannot pass. | Candidate metric; no results exist. |

The R3 proposal, protocol, schema, golden fixtures, consistency report,
manifest and independent review remain unchanged.

### R4 independent-review corrections

The first R4.0 independent package review used manifest SHA-256
`F6608F27BDF0A55F219B9BDFE43CD780ABB39503934F39CFE06F50A0278BCD8D`.
Reviewer A passed the scientific-mechanism scope. Reviewer B returned
**BLOCKED** for four issues: the outcome function checked only one of two
required CI bounds; the two-comparison family was not mapped to exact
estimands; task generator key fields were not fully encoded; and a
permissive caller-supplied schema could bypass protocol-shape validation
while CLI negatives were not tested comprehensively. Reviewer C verified
resource arithmetic and hashes but marked overall readiness **BLOCKED**
because the inventory/package are uncommitted and mutable.

Protocol revision 4.2.0-draft defined the two primary bootstrap estimands as
N−L balanced accuracy and the per-seed minimum of the N−U / N−R specificity
contrasts, with both lower confidence bounds required to be strictly
positive. It freezes TRAIN/EVAL, split-local ordinals, balanced-block index,
DELTA/NU draw names, counter encoding and full-digest modulo mapping. The
validator now requires the exact schema deterministically derived from the
protocol, and its test harness sends all declared negative cases through
the public CLI. These corrections are candidate revisions only; an
independent re-review of the new manifest is required.

Reviewer B's R4.1.0 re-review then demonstrated that finite but impossible
metric values (for example accuracy 2 or a negative operation ratio) could
still reach SUCCESS. Protocol 4.2.0-draft now declares the valid domains for
accuracy, paired effects, confidence bounds, specificity and resource ratios;
the decision function classifies any out-of-domain result as INCONCLUSIVE,
with boundary and invalid-range fixtures. Independent re-review is still
pending.

Reviewer B's R4.2 review identified that raw attribution-specificity scores
are in `[0,1]`, while paired N−U and N−R effects are in `[-1,1]`. Comparing
raw scores to effect thresholds could therefore misclassify valid negative
comparisons as out of domain. Protocol 4.3.0-draft keeps the arm-level scores
(`specificity_n`, `specificity_u`, `specificity_r`) separate as `[0,1]`
values; the decision helper computes both signed paired effects before
applying their `0.10` thresholds. The primary bootstrap estimand remains the
per-seed minimum of those two signed effects. A fixture requires an in-domain
negative comparison to classify as FAILURE, not INCONCLUSIVE. Generator and
bootstrap keys are versioned to R4.3.0. These are candidate corrections only
and have not yet received independent review.

The independent R4.3 review returned **BLOCKED** on mutable/uncommitted
provenance, ambiguity about pilot replay workload/cost, and the missing
deterministic reward-delay assignment and evaluation reward rule. The review
reproduced local static tests, accepted signed paired-effect classification,
and found no Luna-63C contamination or architecture promotion. The candidate
now binds both Luna-63C boundary contracts in its input inventory, defines
two identical bounded workload passes (with counterfactual omission replay
excluded), doubles episode/reception/operation caps accordingly, and fixes
training-delay assignment plus reward-free frozen evaluation. These changes
are not independently reviewed yet and do not cure the immutable-freeze
blocker; see the separate R4 review handoff.

## 2. Candidate temporal attribution rule

This is a bounded local *credit proxy*, not causal identification. At
received event `k`, the decoder has only the current event, its own previous
state, the physical elapsed time, current readout parameters, and prior local
state. Let `h_k` be the post-inference latent feature and
`ell_k = wᵀh_k + b`. Let `ell_(k-1)` be the logit immediately before this
event, calculated with the same readout parameters. After the final prediction
`a ∈ {0,1}`, define the label-free local contribution estimate:

```text
g_k = clip((2a - 1) * (ell_k - ell_(k-1)), -1, +1)
K(age) = exp(-age / 2 TU) * 1[0 <= age <= 8 TU]
v_k = (2a - 1) * concat(h_k, 1)
q_k = K(t_a - t_k) * g_k
E_local = clip(sum_k(q_k * v_k), -4, +4) componentwise
theta_after = clip(theta_before + 0.01 * r * E_local, -1, +1)
```

`a` is the already-recorded prediction, never a target. `r ∈ {-1,+1}` is
delayed evaluator correctness feedback emitted only after prediction:
`+1` correct, `-1` incorrect. The learner sees only `r`; no target, label,
control identity, future event, or evaluation statistic enters the mechanism.
The local score delta `g_k` is an online contribution estimate, not a
counterfactual causal effect. It may misattribute nonlinear interactions.
The claim under test is *selective association consistent with local
contribution and time*, not identification of causal responsibility.

For identical saved event features, comparison arms use the same update
vectors `v_k` and only differ in weights:

- **Uniform:** `q_k = 1/n` for the `n` eligible receptions.
- **Recency-only:** `q_k = K(age)/max(1, sum_j K(age_j))`.
- **Local-temporal (candidate):** `q_k = K(age) * g_k`; no sum-normalization.

All arms clip the final `E` and readout parameters as above. The candidate
kernel has `H=8 TU`, `tau_e=2 TU`; `age=H` is included and `age>H` is
excluded. An empty eligible set yields a zero vector. Reward zero yields
exactly zero reward-driven update. A stable delivery identity within the
bounded episode ledger is settled at most once; duplicate delivery is a
no-op. Eligibility snapshots are immutable after activation and survive
input-trace expiry through the reward deadline.

For offline attribution evaluation only, replay each frozen evaluation
episode once per captured input event with that one decoder reception
omitted; retain every other event at its original physical and decoder time,
the activation trigger (including when omitting D), and frozen parameters.
Let `d_i=abs(ell_full-ell_without_i)` at the original activation trigger and
`m_i=||q_i v_i||_1` be that arm's predeclared event-credit mass. Episode
specificity is
`sum_i(m_i * 1[d_i>1e-6])/sum_i(m_i)`; zero denominator is invalid. Average
episode scores equally within seed, then compare paired per-seed N−U and N−R.
This counterfactual calculation is evaluator-only: it is not transmitted to
the learner and is not evidence of causal identification.

## 3. Candidate event-state transition

PCN state is `s_k=(z_k, t_k, V, c, w, b, H_k, L_k)` where `z` is four
bounded latent coordinates, `t_k` is the last input timestamp, `V[8,4]` and
`c[8]` are predictive parameters, `w[4]` and `b` are readout parameters,
`H_k` is at most four event records, and `L_k` is the bounded eligibility /
credit ledger. For an input `(x_k,t_decoder,k)`:

```text
dt_k = t_decoder,k - t_decoder,(k-1)         # integer microticks, dt >= 0
z0_k = exp(-dt_k / (2 TU)) * z_(k-1)        # each coordinate clipped to [-1,1]
z_k^(0) = z0_k
for j = 0..3:
    xhat_k^(j) = tanh(V z_k^(j) + c)
    epsilon_k^(j) = x_k - xhat_k^(j)
    q_k^(j) = epsilon_k^(j) elementwise (1 - xhat_k^(j)^2)
    grad_z = -V^T q_k^(j) + (z_k^(j) - z0_k)
    z_k^(j+1) = clip(z_k^(j) - (1/16) grad_z, -1, +1)
xhat_k = tanh(V z_k^(4) + c)
epsilon_k = x_k - xhat_k
grad_V = -q_k^(4) (z_k^(4))^T
grad_c = -q_k^(4)
V <- clip(V - 0.001 grad_V, -1, +1); c <- clip(c - 0.001 grad_c, -1, +1)
h_k = z_k^(4); ell_k = w^T h_k + b
```

`x_k` is an 8-vector impulse with one named channel amplitude and zeros
elsewhere. It is not held during silence. `z0_k` is the prior latent after
lazy exponential decay, and is the initialization for all four event-local
inference steps. The updated latent `z_k^(4)` persists to the next event.
No integration or update is executed during a silent interval; the elapsed
time is applied exactly once at the next reception. At equal physical
timestamps, input identities sort UTF-8 lexicographically, then child ordinal;
each equal-time event executes serially with `dt=0` against the immediately
preceding state. This is an event order, not a global timestep.

Initial state for each training or evaluation episode is exactly
`z=0,t=0,H=empty,L=empty`; the first input has `dt=0`. Per-arm/per-seed
parameters persist across training episodes only after physical cleanup.
Evaluation uses a frozen copy of trained parameters and resets all episodic
state identically. Cleanup resets `z`, local clock, event history, eligibility,
pending rewards and duplicate guards. Normal arms receive decoder timestamps
identical to physical event timestamps. In X only, let
`block=floor(split_local_ordinal/8)`; on odd blocks map
`decoder_gap_ticks=10,000,000-physical_gap_ticks`, and on even blocks retain
the physical gap. Decoder ticks are then
`[0, decoder_gap_ticks, decoder_gap_ticks+1,000,000,
decoder_gap_ticks+2,000,000]`. Physical timestamps and event identities
still determine event order, reward due times, eligibility ages, and
cleanup; decoder ticks alone drive PCN elapsed-time integration. This
specifies the temporal-disruption control without changing physical reward
timing or exposing labels.

During TRAIN, assign the ordered reward delays `[0,1,8,9,15,16] TU` by
`split_local_ordinal mod 6`; the same ordinal receives the same delay across
all matched arms and seeds. During EVAL, send no correctness reward and
perform no reward settlement or learner update. For the feasibility-only
pilot, both workload passes use the same initial learned parameters and
identical input bytes/seeds. Its only “replay” is the full workload rerun and
canonical-output-digest comparison. Counterfactual per-event omission replay
is excluded from the pilot and belongs only to a separately authorized
efficacy analysis.

## 4. Task, readout, and arms

The synthetic primary task retains the balanced order×gap XNOR:
A/B first at tick zero; the second A/B symbol after 4 or 6 TU; a nearby
unlabelled distractor N at `gap+1 TU`; distractor D at `gap+2 TU` and
activation. Thus activation occurs by 8 TU, the first informative input may
be 8 TU old at the inclusive horizon, and a distractor can be one event-step
from activation. Counts/amplitudes are block-matched. No label or future event
is in `x_k`. Generator ordinals, split, draws, pairing and per-cell balancing
are frozen in the protocol. Global ordinals 0–95 are TRAIN and 96–143 are EVAL; the
split-local ordinal resets to zero within each split. Balanced-block index
is `floor(split_local_ordinal/8)`. Counter-mode draws use canonical
pipe-delimited UTF-8 fields `L64-R4.3|seed|split|block|draw_name|counter`,
with split exactly TRAIN/EVAL, draw exactly DELTA/NU, counter zero, and the
full SHA-256 digest interpreted as an unsigned big-endian integer modulo
three. Each block shares its sampled DELTA and NU values across its eight
examples.

Every arm uses `p=sigmoid(wᵀh+b)`; predict 1 iff `p>0.5`, ties are 0. All
arms get the same physical sequence, number of opportunities and reward
schedule. Arms are:

1. **A cost-only** — fixed zero head, no trainable parameters.
2. **U uniform-credit PCN** — same PCN and readout as N, uniform event credit.
3. **R recency-only PCN** — same PCN and readout as N, kernel-only credit.
4. **L parameter-matched linear temporal decoder** — same `V[8,4]`, `c[8]`,
   state and readout sizes; replace `tanh(u)` with `u`; same local-temporal
   credit.
5. **N nonlinear PCN** — event-state contract above with local-temporal
   credit.
6. **X temporal disruption** — same nonlinear decoder and local credit as N,
   but apply the balanced, within-cell decoder-view gap permutation.

This matrix estimates separate effects of nonlinear inference (N−L),
credit specificity (N−U/N−R), and stable temporal mapping (N−X). It does not
assume a causal or energy benefit. No widening beyond four latent coordinates
is proposed. The abstract R3 "32 computational units" cap is withdrawn; no
scientific meaning is assigned to a hand-counted unit. Candidate hard model
limits are 45 trainable parameters, 8 input channels, 4 latent coordinates,
8 reconstruction coordinates, 4 retained event summaries, 8 eligibility
records and one captured credit record.

## 5. Outcomes, statistical replay, and cost-benefit

The endpoint and ordered classification procedure are encoded in the protocol.
For each complete seed, the first primary effect is
`balanced_accuracy_N-balanced_accuracy_L`. The second is
`min(specificity_N-specificity_U, specificity_N-specificity_R)`; separate
N−U and N−R specificity means must each also meet their declared threshold.
The inputs are arm-level means in `[0,1]`; only their computed paired
differences are compared with the signed `[-1,1]` effect domain and `0.10`
threshold. Out-of-domain raw scores or derived effects are INCONCLUSIVE;
valid negative paired effects are FAILURE when other required inputs are
valid.
Bootstrap those two explicitly named per-seed estimands.
Use 100,000 paired seed-cluster bootstrap replicates and exact SHA-256
counter draws keyed by protocol revision, gate, comparison, replicate index
and selected draw index. Intervals are percentile 97.5% per comparison using
nearest ranks; comparison-family alpha is .05 with two primary comparisons.
The exact bytes/ordinal mapping are protocol constants. Two small fixtures
exercise a positive and a zero/degenerate result with independently
enumerable bootstrap values; CI endpoint equality uses exact closed-interval
comparisons in binary64 output serialization.

Decision precedence is exhaustive:

1. **INCONCLUSIVE** if a paired seed is missing/aborted/invalid, a class or
   attribution denominator is empty, a required cost measure is unavailable,
   output is nonfinite, or any validity/overflow cap is breached.
2. Otherwise **SUCCESS** only if all predeclared efficacy, attribution, cost
   and validity conditions in the protocol pass, including strict positive
   adjusted lower bounds and equality rules.
3. Otherwise **FAILURE**.

These regions are mutually exclusive and exhaustive. Intermediate accuracy
or effect values, CI touching zero, exact threshold equality where the
threshold is strict, greater cost than the cap, and lower accuracy are
**FAILURE**, not unspecified or retroactively tuned. No seed replacement.
This does not assert that 20 seeds are adequately powered; R4 authorizes no
efficacy study.

Cost measures: count scalar adds/subtracts/multiplies/divides/comparisons,
`tanh`, `exp`, parameter and state reads/writes, reward-record operations,
maximum live model/eligibility bytes, and existing `activity-cost-proxy`
event charges. Never aggregate these as physical energy or joules. Report
`ops per correct discrimination` using the explicit zero-correct value
`+∞`, and incremental ops per additional correct versus L. Successful
efficacy must also meet the protocol's added-op ratio cap and memory cap.
Accuracy improvement at excessive cost is FAILURE; lower cost with worse
accuracy is FAILURE. The cost-benefit claim remains software-operational,
not an energy or hardware claim.

Design-stage power: between-seed variance is unknown and unmeasured, so
reliable power cannot be established. For paired mean effect `δ`, an
approximate planning relation under a normal model is
`n ≈ ((z_(1-α/2)+z_(power))*σ_seed/δ)^2`; with two-sided per-comparison
`α=.025`, 80% power and `δ=.10`, the multiplier is approximately
`(2.241+0.842)^2/.10^2`, so `n` depends directly on the unknown `σ_seed²`.
This is an illustration, not a sample-size justification. Do not use an
unpowered pilot to claim efficacy. Any later efficacy sample-size amendment
requires a separately reviewed preregistration before evaluation labels or
effect summaries are inspected.

## 6. Bounded future feasibility-only pilot (not authorized)

Candidate pilot workload: 6 arms × fixed seeds `{6401,6402,6403}` × (96
training workload episodes + 48 evaluation workload episodes) = **2,592
episodes per pass**. Run that exact workload twice, resetting all model
parameters and episodic state to their declared initial values before pass
two and reusing the same per-episode seeds and input bytes. Compare canonical
output digests; any mismatch aborts the pilot. The two passes total **5,184
episodes** and at most **20,736 input receptions**. An aborted pass retains
partial output and does not replace episodes or seeds.

The pilot's use of “replay” means only this byte-identical deterministic
workload rerun. Per-event counterfactual omission replay for attribution
specificity is expressly excluded from the pilot (zero such passes); it is
reserved for a separately authorized full efficacy run. EVAL episodes do
not receive correctness rewards or perform reward settlement/update. TRAIN
reward delays are assigned by `split_local_ordinal mod 6` over the frozen
ordered delay list; matched episodes use the same delay across all arms and
seeds. Pilot evaluation workload is not scored for efficacy; it validates
bounded execution, deterministic replay, memory, and artifact capture. No
tuning or threshold changes may be based on pilot behavior. Pilot evidence
cannot be pooled into any efficacy result.

Analytical counted-op ceiling across both passes: at most five decoder arms
use four-event PCN/linear workload, so no more than `4,320 × 4 = 17,280`
decoder receptions. The proposed enforced ceilings of 2,048 scalar
operations per decoder event and 256 episode-level scalar operations across
each of 5,184 episodes yield at most **36,716,544 counted scalar
operations**. No nonzero lower-bound
claim is made. The counter increments for every executed scalar add,
subtract, multiply, divide, or comparison in decoder, eligibility, reward,
and lifecycle arithmetic; it excludes loop/index work, memory accesses,
serialization, hashing, `tanh`, and `exp`, which are separately tallied or
excluded from the throughput estimate. Exceeding either hard counter ceiling
aborts the pilot. These are enforceable workload bounds, not observed
throughput.

Pilot proposal caps, all conditional on separate owner approval:

- one logical CPU core; 900 CPU seconds / 1,200 wall seconds;
- 512 MiB process working set;
- at most 5,184 episodes across both deterministic passes, at most 20,736 receptions;
- 25 MiB total artifacts, no network/GPU/hardware dependencies;
- immediate abort on any count, memory, time, schema, replay or path breach.

At assumed throughput of 10^5 counted scalar ops/s, the scalar-op ceiling
would take roughly 367 seconds before interpreter, transcendental, hashing,
I/O and startup overhead. Throughput is not measured; wall time and completion are
**UNVERIFIED** until a separately authorized pilot. If measured time exceeds
the cap, report pilot failure; do not increase it. A future full efficacy
gate requires its own protocol revision, independent review and owner
authorization after pilot evidence.

Memory analytic inventory: fixed parameters (45 binary64 values = 360 bytes
per PCN arm), four-coordinate latent, bounded event/eligibility records and
one credit record per live episode; serialized event/protocol records are
bounded by 25 MiB total output. Interpreter/runtime baseline and allocator
overhead are not analytically certified; the 512 MiB cap is an abort limit,
not a predicted peak.

## 7. Provenance, paths, and publication sequence

[`luna-0-track-b-execution-gate-r4-input-inventory-20261010.json`](luna-0-track-b-execution-gate-r4-input-inventory-20261010.json)
records raw SHA-256, Git blob object IDs, HEAD membership and worktree status
for the contract, original governance record, workflow, changelog, A01–A15,
acceptance criteria, ACP-0008, Luna-63C protection authorization, R0–R3
proposals and reviews. Uncommitted inputs explicitly have no publication
commit and do **not** form an immutable provenance chain.

The candidate package is limited to the existing experimental document/
protocol namespace `workflow/handoffs/` and `experiments/luna64/`. It does
not modify the Luna-64 contract, existing workflow/changelog, production,
tests, ACP, or Luna-63C files. The previously proposed execution allowlist
remains unchanged; the R4 validator is governance validation, not runtime
Luna-64 implementation. If governance determines that this location is not
allowed, stop and request an explicit governance allowlist amendment.

Publication sequence if and only if R4 review passes:

1. Independently review exact R4 candidate bytes; do not call working-tree
   hashes immutable.
2. Obtain explicit owner approval for **documentation publication only**.
3. Publish the already accepted Luna-64 contract/governance record and
   existing workflow/changelog changes as a documentation-only freeze commit,
   preserving their semantics and all unrelated work.
4. Recompute blob IDs and hashes from that commit; update the R4 inventory in
   a second governance-only commit, and verify remote publication.
5. Re-review the committed freeze and R4 package, recording both SHAs.
6. Only then may the R4 status say ready for owner authorization of the
   bounded pilot. Pilot execution still needs separate explicit owner
   approval. No experimental branch/worktree is created by these steps.

At this candidate stage the inventory is not immutable; no commit or push
was performed. A mutable working tree is not a freeze.

## 8. Validation and disposition

Permitted now: strict parser/schema tests on protocol/fixture bytes, small
deterministic PCN and eligibility golden calculations, and unit checks of
bootstrap and verdict rules. Prohibited now: pilot, training, efficacy,
benchmark, runtime/memory measurement, branch/worktree creation, production
change, Luna-63C edit, or architecture promotion.

R4 cannot receive PASS unless independent reviewers reproduce all required
static/statistical fixtures, assess the candidate semantics, find no
unresolved governance issue, and the governing-input chain is immutable and
reverified. Owner approval remains separately required even after PASS.

**Current disposition:** R4.3 candidate preparation only. The latest
independent review package has not yet been reviewed; generated schema,
goldens, inventory and manifest must be regenerated after the candidate
stabilizes. Governing inputs remain uncommitted, so the provenance chain is
not immutable and remains a freeze blocker. Owner approval has not been
provided for this exact candidate. No branch/worktree, pilot, implementation,
efficacy run, or architecture promotion is authorized.
