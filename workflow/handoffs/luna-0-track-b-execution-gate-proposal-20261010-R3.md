# Luna-0 — Luna-64 Track B execution gate R3

**GATE:** `L64-TB-GATE-20261010-R3`  
**STATUS:** GOVERNANCE DRAFT — INDEPENDENT REVIEW REQUIRED  
**OWNER APPROVAL:** NOT PROVIDED  
**EXECUTION AUTHORIZATION:** NOT GRANTED  
**IMPLEMENTATION / TRAINING / EFFICACY RUN:** NOT PERFORMED  
**ARCHITECTURE PROMOTION:** NOT AUTHORIZED

This is a proposed, falsifiable completion of the existing exploratory
Luna-64 Track B contract. It does not edit that contract, approve the new
task/readout/reward choices, or authorize any code, training, evaluation,
benchmark, execution branch, worktree, production integration, or
architecture change. The exact protocol and golden examples are machine
readable. Their preparation is governance work only.

## 1. Repository reconciliation and provenance

At reconciliation:

- Branch: `main`.
- `HEAD`, local `main`, and local `origin/main` all resolve to
  `73aaa50f97ceab322907875ae4dcf23e7541c3b5`.
- This commit identity has **not diverged** from R2's reviewed source
  baseline. The worktree is **not clean**: it contains the pre-existing
  uncommitted Luna-64 governance artifacts and R0/R1/R2 proposals/reviews,
  plus the new R3 draft package. These are not part of the baseline commit.
- No existing artifact was discarded, replaced, or silently incorporated.
- No Luna-64 execution branch/worktree was created.

The expected R2 proposal digest
`64529FD816824A3EAA246856C3BEF46E6FDD97CCDF8ED48830C27AEF558D5A0A` and
review digest
`4EF7AEA8ECD0207A52A8B259F74153E17EED192E671EB1650D8C82394320AA57` match
the files at reconciliation. The reviewed baseline is
`73aaa50f97ceab322907875ae4dcf23e7541c3b5`.

The R3 package uses the repository's existing `experiments/luna64/` protocol
location and handoff convention. The accepted Luna-64 contract,
documentation-only governance PASS, R0/R1/R2 evidence, architecture contract,
workflow/changelog, and Luna-63C authorization/corrective boundaries were
inspected. Luna-63C remains independent, read-only, and certificate-gated.

## 2. R2-to-R3 finding closure matrix

Every finding in the R2 independent review is represented below. “Resolved in
specification” means a concrete candidate rule now exists; it is not an
independent PASS, owner approval, or execution authorization.

| R2 review finding | R3 response | Status / evidence boundary |
|---|---|---|
| 1. No R2 protocol/golden; stale R1 timebase JSON | R3 adds protocol, strict structural JSON Schema, golden fixtures, and exact tick fields. R3 does not mutate the R1 protocol. | Resolved in R3 candidate artifacts; schema and cross-artifact validation still require independent review. |
| 2. Task generator, label/readout mapping absent | Defines a balanced 2×2 order-by-gap task, exact four-event stream, amplitudes, SHA-256 named draws, train/eval ordinal schedules, evaluator-only labels, and a five-arm shared readout. | Resolved as a candidate; evaluator/reward-oracle compatibility with the accepted contract needs explicit review/approval. |
| 3. Reward source and scientific objective unresolved | Defines a correctness-only, evaluator-side oracle emitted after the frozen prediction; `r=+1` for TP/TN and `r=-1` for FP/FN; only the signed scalar is sent to the reward sink. | Candidate resolved; explicit owner approval remains absent. No target/label enters inference. |
| 4. Arm E and dual-clock semantics incomplete | Physical timestamps govern all source/reward/settlement events. A seeded per-episode bijection changes only the decoder-visible short/long A/B gap category, with balanced cells and no future input. | Resolved in rule and generator cells; exact balance and causal isolation are mandatory independent checks. |
| 5. 8/16-TU lifecycle and cleanup conflict | Separates the 8-TU admission window from an immutable activation snapshot retained through the inclusive 16-TU reward deadline; expiry at deadline+1 tick precedes delivery; cleanup is fixed and bounded. | Resolved in candidate state machine and fixtures; all boundary cases must be independently checked. |
| 6. Runtime feasibility unestablished | Gives exact episode, event, state, parameter, operation, log, CPU, memory, and wall-clock ceilings and abort conditions. | Analytical ceilings only. Runtime is not measured and is not claimed as passed; empirical check belongs to a later authorized execution. |
| 7. LWC unapproved and unvalidated | Excludes LWC from acceptance. Retains raw counters and the existing `activity-cost-proxy` with explicit configuration; no joule claim. | Resolved by removal from the gate metric; LWC remains unapproved and unused. |
| 8. Finite differences not performed | Executed governance-only central differences for latent, all `V`, and all `c` components at three step sizes on one interior fixture. | Interior objective gradient check PASS; clipped-boundary derivatives, training loop, and efficacy were not tested. |
| 9. Five-seed interval exploratory | Proposes 20 fixed seeds, paired seed-cluster bootstrap, exact replicate count, quantiles, rank indices, multiplicity, and predeclared decision branches. | Method fully specified; no coverage/power claim or experiment result. Treat evidence as exploratory until independent review accepts adequacy. |
| 10. Luna-63C and source isolation | Keeps Luna-63C paths/evidence forbidden, preserves source baseline and no execution branch/worktree. | Boundary preserved; no Luna-63C file changed. |

The R3 task and readout are more specific than the R2 draft. They are
experimental design proposals inside the isolated Track B lane, not a change
to A01–A15, the Luna-64 contract, or a production architecture.

## 3. Frozen candidate task and generator

The authoritative numeric record is
[`luna64-track-b-protocol-r3.json`](../../experiments/luna64/luna64-track-b-protocol-r3.json).
The exact hand-calculable cases are in
[`luna64-track-b-golden-r3.json`](../../experiments/luna64/luna64-track-b-golden-r3.json).

The task is a binary XNOR of two locally observable temporal factors:

- `order_bit=0`: A then B; `order_bit=1`: B then A.
- `gap_bit=0`: physical A/B interval is 1 TU; `gap_bit=1`: interval is 3 TU.
- Target `y=1` iff `order_bit == gap_bit`; otherwise `y=0`.

Every primary episode contains exactly one A, one B, one N distractor, and one
D distractor. Amplitudes are `A=1+delta`, `B=1-delta`, `N=0.25+nu`,
`D=0.25-nu`, with `delta,nu ∈ {-1/16,0,+1/16}`. A block shares its two
amplitude-noise draws across every cell, so amplitude/count/magnitude do not
reveal the label. The order-by-gap cells are balanced: order alone and gap
alone have no label information; the relation between them is informative.

Times in ticks are `A/B first=0`, the other A/B symbol at gap `g`, N at
`g+1,000,000`, D at `g+2,000,000`. Thus D arrives at 3 TU (short) or 5 TU
(long). D is the final input and prediction time. No timestamp jitter,
dropout, or future preprocessing is used.

The generator uses fixed seeds `6401..6420` and SHA-256 named draws with the
exact encoding and modulo mapping in the protocol. Arm E's permutation bit
is not a random draw: it is derived from the balanced cell, zero-based seed
index, and split code using the protocol's exact formula. It uses disjoint
ordinal ranges: training `0..9999` and evaluation `10000..11999`; local ordinals
select the explicitly balanced cell schedule. Parameters persist across
training episodes per arm/seed; event state resets only after cleanup.
Training has 5,000 examples per class per arm/seed. Evaluation has 1,200
primary examples (600 per class, 300 per order×gap cell), 400 independent-label
controls, 200 silent controls, and 200 non-mutating reward-delivery audit
examples. Evaluation parameters are hash-frozen and no evaluator label enters
the model.

The uncorrelated control crosses order, gap, target, and Arm-E permutation
bits independently in balanced blocks. The silent control has no inputs and
evaluator target zero. The no-reward training control is the seventh block
schedule slot; the decoder receives no condition flag. The overflow probe is
a lifecycle-only capacity test, not a task episode.

## 4. Readout, objective, feedback, and energy separation

Every arm emits the same binary output contract at the final input time
(silence uses the declared 5-TU completion observation):

```text
p = sigmoid(w·h + b)
class = 1 iff p > 0.5; an exact tie is class 0
```

For arm A, `p=0.5` with the fixed empty readout and no trainable parameters.
B uses four unweighted symbol counts; C uses an eight-dimensional local
exponential event trace; D uses the four-dimensional PCN latent; E uses the
same PCN/readout dimensions with the Arm-E gap treatment. Trainable parameter
counts are respectively `0, 5, 9, 45, 45`, each below the cap 256. The full
feature and parameter definitions are in the protocol.

Three quantities are kept distinct:

1. **Predictive objective:** for the PCN only,
   `F=0.5||x-tanh(Vz+c)||²+0.5||z-z0||²`, with explicit error
   `epsilon=x-xhat`. It is updated immediately using local information and no
   task label.
2. **Task loss and activation reward:** the evaluator computes the binary
   correctness outcome only after the prediction has been recorded. The
   evaluator-side oracle maps TP/TN to `r=+1`, FP/FN to `r=-1`; only this
   scalar reward is delivered after the selected delay. It is not the PCN
   prediction error. The decoder's reward update uses the stored local
   eligibility and does not receive the label, condition ID, or target.
3. **Energy penalty:** every accepted input reception incurs exactly one
   unit in the configured `activity-cost-proxy`. Reward settlement incurs
   zero event-energy charge. This is not a calibrated physical-energy or
   joule measure.

Readout learning stores `e_i=(1/n)(2a-1)concat(h,1)` for each input still
eligible at prediction, then applies
`theta <- clip(theta + 0.01*r*sum_i(e_i), -1, 1)` on accepted reward.
Here `a` is the already-recorded class prediction. Thus TP/TN reinforce the
correct side and FP/FN reverse it; no labels enter inference. Arm A has no
trainable readout and records the feedback without updating parameters.
Training feedback delays are 0, 1, 8, 9, 15, and 16 TU, plus a deterministic
withheld-reward condition. Delay-stratified accuracy/update counts are
descriptive; the primary endpoint is frozen-evaluation balanced accuracy.

## 5. Arm E physical clock and decoder view

The **physical causal clock** is the integer timestamp from the generator. It
alone schedules reception, cost charge, reward origin/delivery, expiry,
settlement, and cleanup.

Arm E changes only the decoder-visible A/B gap code. The exact short/long
bijection bit is derived from the episode cell and seed/split phase; it is
fixed for that episode and is available at the second A/B reception from the
current and previous timestamps. The transform does not move events, relabel
targets, or alter amplitudes. N and D gaps are the fixed 1-TU view gap.
Complete blocks cross target/order/gap/permutation so the transformed gap is
balanced independently of target.

For each paired D/E episode, physical input IDs/times/magnitudes, target,
activation time/identity, reward origin identity/time, reward due time and
cleanup time are identical. The correctness reward sign may differ between
arms because their recorded predictions may differ under the same oracle
rule; that is the task outcome, not a timing-schedule difference. E's
permutation bit, split/seed derivation and class balance are protocol fields
and are explicitly testable. There is no physical-time remapping, future
access, or condition metadata in the readout.

## 6. Eligibility, delayed credit, reward, and cleanup

All time arithmetic and ordering is integer microticks (`1 TU=1,000,000
ticks`; `1 tick=0.000001 TU`). Exact expiry and tie comparisons have zero
tolerance.

| Event/state | Rule |
|---|---|
| Input reception | Charge cost once; store the input ID and its event-local trace. |
| Eligibility active | Input may be attributed while `activation_tick-input_tick <= 8,000,000`; expires after that age. |
| Prediction/activation | At final input, make and record prediction first; snapshot final feature, predicted class, and all still-valid input IDs. |
| Credit capture | One immutable bounded record; equal per-input shares of the saved readout eligibility. Snapshot survives input-trace expiry. |
| Reward origin | Evaluator oracle runs only after prediction; stable origin identity and due time are assigned. |
| Delivery | Delays through 16 TU are valid; due tick is inclusive. A withheld reward creates no delivery. |
| Settlement | Unique accepted reward applies at most one readout update; duplicate ID is a no-op. |
| Deadline/expiry | Deadline is activation +16 TU; expiry is deadline +1 tick. At that same expiry tick, EXPIRY precedes DELIVERY, so a reward there is rejected. |
| Logical completion | Final input completion; silent episodes complete at 5 TU. A pending captured record may survive logical completion. |
| Physical cleanup | Fixed expiry tick; remove episode state and duplicate guard, then and only then start the next serial episode. No second event cost is charged. |

Same-timestamp order is exactly `EXPIRY → RECEPTION/COST → LOCAL STATE /
PREDICTION → ACTIVATION/CAPTURE → REWARD ORIGIN → REWARD DELIVERY → CREDIT
SETTLEMENT → LOGICAL COMPLETION → PHYSICAL CLEANUP`, followed by canonical
parent ID and child ordinal. Nonfinite values, identity errors, or capacity
overflow invalidate the episode without eviction/truncation.

The golden file includes every requested delay boundary (0, 1, 8, 9, 15, 16,
17 TU), the exact expiry/delivery tie, duplicate reward, a logical completion
before delayed feedback, and eligibility at 8 TU versus 8 TU plus one tick.
At delay 17 TU the record has already expired and been removed; delivery is
rejected with no update. An activation at the maximum 5-TU task duration has
maximum cleanup at tick `21,000,001`. Silent episodes have no activation or
credit and clean at logical completion.

## 7. Golden fixtures and mathematical verification

The versioned golden file provides exact positive, negative, ambiguous
out-of-domain, distractor-containing, silent, delayed-reward, retention,
overflow, duplicate, and reward-boundary fixtures. It contains a one-event
nonlinear PCN inference reference with all initial parameters specified by
the protocol's exact `V` formula, `c=0`, `z=0`, and one-hot A input.

Governance-only scalar recurrence produced the fixture latent steps:

`0.015625`, `0.030196906457891`, `0.0437862730472156`,
`0.0564589876996739`.

The final prediction has `xhat[0]=0.0141138096577061`,
`xhat[4]=0.00705725629705554`, objective `0.487604501233078`, and the
nonzero analytic parameter gradients and first update are frozen in the
golden file. A zero readout emits the tie class 0. No reward is applied in
this fixture.

Central finite differences were **executed as governance math verification**,
not as learning or efficacy work. The scalar objective was evaluated
independently at `+h` and `-h` for all four latent entries, all 32 `V`
entries, and all eight `c` entries at an interior state. Maximum absolute
errors for `h={2^-12,2^-16,2^-20}` were respectively
`2.18525896267252e-8`, `8.48571213296623e-11`, and
`3.98371613474779e-11`, all below `1e-7`. The one-event recurrence and
gradient were separately hand/calculator-derived. This does **not** verify
clip-boundary derivatives, a running trainer, reward trajectories, or task
efficacy; those remain not run.

## 8. Resource and instrumentation contract

The proposed ceiling is 5 arms × 20 seeds × (10,000 train + 2,000 evaluation)
= **1,200,000 episode executions**, at most four receptions per task episode.
At most one episode/credit/pending reward is live; temporal history is capped
at four task entries and eligibility capacity at eight. Parameter counts are
0/5/9/45/45. D/E parameter storage is 45 binary64 values (360 bytes); one
captured readout gradient is at most nine binary64 values. Credit and event
logs have fixed capacities in the protocol.

The model-unit ceiling is 32, counting persistent task-feature coordinates,
PCN reconstruction coordinates, PCN latent coordinates, and the binary
readout logit. A/B/C/D/E use 1/5/9/13/13 units respectively; external inputs,
parameter storage, and bounded temporary scratch vectors are accounted
separately. The analytical work ceilings are at most 2,048 scalar
arithmetic/comparison operations, 48 `tanh`, and two `exp` calls per received
input (the local decay plus, on the final input, the readout sigmoid); at most 256 additional
episode-level scalar operations; and 8,448 scalar operations per episode.
These bounds are implementation acceptance caps, not measured costs. The
future authorized execution must stay within one logical core, 2 GiB working
set, and four hours; any exceedance/overflow/nonfinite state/out-of-path write
aborts without extending the budget. There is no GPU, network, or hardware
dependency.

Empirical runtime and memory feasibility are **not measured**. The current
governance gate does not authorize a smoke run or benchmark. Report raw
operation counters and configured `activity-cost-proxy` only; LWC is
unapproved and excluded from acceptance. No physical joule/power claim.

## 9. Statistical decision contract

The independent replication unit is the seed; arms are paired by seed and
episode ordinal. Primary endpoint is balanced accuracy on the 1,200 primary
frozen-evaluation episodes, with 600 instances/class. The two primary
comparisons are D−C and D−E. Per-seed effect is the paired difference in
balanced accuracy; aggregate effect is the equal-weight mean over 20 seeds.

The initial five-seed ceiling is replaced by 20 fixed seeds because five
independent seed clusters do not support stable interval assessment; this is
a predeclared, resource-bounded exploratory proposal, not a power-derived
sample size. No confirmatory coverage or power claim is made. If the
independent reviewer considers 20 insufficient for the proposed inference,
the outcome is a governance blocker, not permission to tune the seed count
after seeing evaluation results.

The protocol fixes 100,000 paired-seed bootstrap resamples per comparison,
SHA-256 named draws, 97.5% percentile interval per comparison, nearest-rank
indices 1,250 and 98,750, and Bonferroni family alpha .05 across the two
comparisons. Report per-seed results and raw confusion counts. No test-set
tuning, p-value substitution, epsilon for zero denominators, or replacement
of aborted seeds is allowed.

Success requires D balanced accuracy ≥0.70, each mean improvement ≥0.10,
both adjusted interval lower bounds >0, at least 16/20 positive D−C and
D−E seed effects, and valid negative-control/overflow rates as encoded in
the protocol. Failure and inconclusive branches are also fixed there.
Twenty seeds and the bootstrap do not by themselves establish confirmatory
coverage or power; report the result as exploratory unless the independent
review accepts the inference scope. Criteria are predeclared and may not be
changed after evaluation.

## 10. Protocol schema and consistency audit

Artifacts:

- [`luna64-track-b-protocol-r3.json`](../../experiments/luna64/luna64-track-b-protocol-r3.json)
- [`luna64-track-b-protocol-r3.schema.json`](../../experiments/luna64/luna64-track-b-protocol-r3.schema.json)
- [`luna64-track-b-golden-r3.json`](../../experiments/luna64/luna64-track-b-golden-r3.json)
- [`luna64-track-b-consistency-r3.json`](../../experiments/luna64/luna64-track-b-consistency-r3.json)
- [`validate-track-b-gate-r3.mjs`](../../experiments/luna64/validate-track-b-gate-r3.mjs)
- [`luna-0-track-b-execution-gate-r3-manifest-20261010.json`](luna-0-track-b-execution-gate-r3-manifest-20261010.json)

The schema is Draft 2020-12, requires every declared object key, rejects
additional keys recursively, rejects `null`, and validates JSON primitive
types. The repeatable validator checks the protocol against the recursive
schema, rejects a synthetic unknown key, recomputes the exact split balances
and named-draw fixtures, checks the timebase/lifecycle/resource bounds, and
recomputes the one-event PCN and all interior finite-difference gradients.
Its machine-readable report binds the exact proposal, protocol, schema,
golden fixture, and validator hashes. It is a local governance check, not an
independent review or execution authorization.

The protocol is the single authority for numeric constants. This handoff
explains the contract and gives explicit algebra; values duplicated in golden
fixtures are expected assertions, not separate configuration sources.
Golden fixture bytes, schema, protocol, consistency report and proposal are
bound by the R3 manifest.

## 11. Isolation, architecture and authorization boundary

If and only if a later exact-byte review and explicit owner approval pass,
the proposed execution branch remains
`experiment/luna64-track-b-ltrd` in a dedicated worktree based on the later
committed governance-freeze SHA. The existing allowlist is limited to
`experiments/luna64/**`, `tests/test_luna64_*.py`,
`artifacts/luna64/**`, and the named Luna-64 execution handoff. Production
`tpcn/**`, all other tests, all Luna-63C evidence and reconciliation,
contracts/ACPs/defaults, merges, promotion and hardware claims are forbidden.

A01–A15 and the production baseline are unchanged. The evaluator-side
correctness oracle, task output adapter, and reward learner are proposed
experimental interfaces and require acceptance; this R3 document does not
amend the accepted Luna-64 contract or authorize an architecture departure.
Luna-63C files and certificate chain were not modified.

## 12. Validation, review and disposition

**Performed:** repository/hash reconciliation; regenerated protocol schema;
the repeatable governance-only validator passed its recursive structural
check, unknown-key rejection, generator balance, named-draw, lifecycle,
resource-ceiling, PCN recurrence, and finite-difference checks. Exact
SHA-256 identities are recorded in the consistency report and manifest.

**Not performed:** a standards-compliant Draft 2020-12 validator execution
(none is available in the current environment); implementation, training,
test-set scoring, experiment,
runtime/memory benchmark, smoke run, execution worktree, commit, push, or
architecture promotion.

Independent Luna-0 review must evaluate every R2 finding, independently
recompute the task cells, reward sign/outcome table, Arm-E balance and causal
clock, lifecycle boundary fixtures, schema, golden hashes, PCN math,
parameter cap, resource ceilings, statistics and Luna-63C isolation. A review
PASS would mean only **READY FOR OWNER AUTHORIZATION**; it cannot authorize
execution. A BLOCKED review leaves all execution gates closed.

**Next bounded role:** independent Luna-0 reviewer, read-only on the exact
R3 manifest hashes. If any scientific design choice is incompatible with the
existing contract, stop for explicit owner direction; do not implement or
silently modify the contract.

**Current outcome:** R3 candidate package prepared; execution remains
**NOT AUTHORIZED**. Owner approval: **NOT PROVIDED**.
