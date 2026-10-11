# Luna-0 — Track B / Luna-64 proposed execution gate

**GATE ID:** `L64-TB-GATE-20261010-R0`  
**STATUS:** PROPOSED FOR INDEPENDENT GOVERNANCE REVIEW — NOT FROZEN  
**OWNER APPROVAL:** NOT PROVIDED FOR THIS EXACT GATE PACKAGE  
**EXECUTION:** NOT AUTHORIZED  
**LUNA-64 CONTRACT:** PRESERVED; no amendment is made by this proposal.

This proposal responds to the blockers recorded in
`luna-0-track-b-governance-authorization-20261010.md`. It is an additive,
documentation-only gate proposal. It does not create a branch/worktree, edit
experiment or production code, revise the Luna-64 contract, or grant execution
authorization. A review PASS is separate from project-owner approval.

## 1. Reconciled current status

The existing governance PASS is preserved as a PASS for the original
documentation-only governance task; it is not an execution-gate review or
execution authorization.

The recorded execution blockers are:

1. No owner-approved branch/worktree name or isolated checkout exists.
2. No frozen resource/compute budget exists.
3. The contract defines the scientific intent and candidate arms broadly, but
   does not freeze exact stimuli, reward schedule, generator, split, seeds,
   metrics, statistical procedure, or numerical comparison rules.
4. The contract/handoff and workflow/changelog updates are present in the
   working tree but are not in Git at the current source baseline. Therefore
   they cannot yet be the immutable, committed execution contract.
5. No independent review of an exact gate package has been completed.
6. No owner approval has been provided for this exact gate ID and its content.

Current repository evidence: branch `main`; `HEAD` and `origin/main` both
resolve to `73aaa50f97ceab322907875ae4dcf23e7541c3b5`. The worktree has
uncommitted governance changes (including the Luna-64 contract) and this
proposal. The SHA is an immutable source-code baseline candidate only; it
does not contain the uncommitted contract/handoff or this proposal.

The current Luna-63C mechanism authorization remains independently
certificate-gated. Its Stage-A numerical/mechanistic certificate is not yet
reviewed PASS; Stage-B remains blocked. Track B must neither alter nor rely on
that certificate chain.

## 2. Proposed isolation and baseline

### Branch/worktree

- Proposed branch: `experiment/luna64-track-b-ltrd`
- Proposed layout: a dedicated Git worktree, not a subdirectory or shared
  checkout; no branch/worktree is to be created before owner approval.
- Proposed source baseline: `73aaa50f97ceab322907875ae4dcf23e7541c3b5`.
- Required freeze prerequisite: before the execution worktree is created,
  commit the already reviewed Luna-64 contract and governance PASS, the
  accepted gate package, and any necessary governance index/changelog updates
  as documentation-only changes. Record the resulting commit SHA. That
  resulting SHA—not the pre-freeze candidate above—must be the exact execution
  branch base. Do not amend or replace the existing governance PASS.
- Require the final execution branch to start exactly at the recorded
  governance-freeze SHA and to remain separate from `main` until final
  scientific review. No cherry-picking from any other experiment branch.

### Allowed writes on the execution branch

Only the following new paths are proposed for execution-owned changes:

- `experiments/luna64/**`
- `tests/test_luna64_*.py`
- `artifacts/luna64/**`
- `workflow/handoffs/luna-64-track-b-ltrd-execution-20261010.md`

The following are read-only inputs, not execution-owned write paths:

- `.github/agents/luna-64.agent.md`
- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- the accepted governance and gate handoffs
- applicable ACP documents and architecture acceptance criteria
- Luna-63C contracts, fixtures, certificates, reconciliation records and
  handoffs

Any needed path outside the allowed-write list is a stop-and-request decision,
not an implied permission.

### Forbidden writes and actions

- All production/core paths, including `tpcn/**`, and all existing tests except
  the dedicated Luna-64 test filenames above.
- All `experiments/luna63c/**`, `artifacts/luna63c/**`, Luna-63C manifests,
  frozen fixtures, C0-C7 semantics, W/T/E/N5 certificate evidence and
  corrective reconciliation records.
- Architecture contract, ACP status/content, default configuration, workflow
  architecture decision records, unrelated experiment code/data/artifacts.
- GPU/analog/hardware dependencies, external services, network-fetched task
  data, production integration, merges/cherry-picks, and any claim of
  architecture promotion or resolution of Luna-63C blockers.
- Changes to seeds, thresholds, generator, data split, model size, training
  exposure, resource ceilings or metrics after the freeze.

## 3. Proposed frozen resource budget

All values below are proposed ceilings. They become frozen only if the
independent review passes and the owner approves this exact gate package.

| Resource | Proposed ceiling / frozen definition |
|---|---|
| Dataset | Deterministically generated synthetic temporal streams only; no downloaded or private data |
| Arms | A–E below, all evaluated on matched streams |
| Seeds | Five fixed seeds: `6401, 6402, 6403, 6404, 6405`; seeds identify stream generation and any initialization randomness |
| Train exposure | At most 10,000 episodes per arm per seed, total across all training conditions |
| Evaluation exposure | Exactly 2,000 held-out episodes per arm per seed, total across all evaluation conditions |
| Event history | At most 256 retained event records per decoder instance; fixed finite retention horizon 8.0 logical time units |
| Eligibility | At most 256 scalar eligibility entries per instance, each clamped to `[-1,1]`, with fixed expiry at age 8.0 logical time units |
| Decoder | At most 32 scalar computational units (SCU): one SCU is one scalar hidden activation/state. At most 256 scalar parameters and 1,024 counted scalar arithmetic/activation operations per received event |
| Trial bound | At most 32 input events per episode; maximum episode span 16 logical time units; one local decoder instance per episode |
| Overflow | Reject the event/update that would exceed a cap, record an explicit typed overflow and terminate that episode as invalid. Never evict silently, truncate into a valid result, or continue learning from the invalid episode |
| Runtime | Single deterministic CPU worker; 4 hours maximum wall-clock for the complete frozen run, including all arms/seeds and replay |
| CPU | One logical CPU core; no parallel trial execution |
| Memory | 2 GiB maximum resident memory for the runner |
| Accelerator/dependency | No GPU, accelerator, network, or hardware dependency; use repository-declared dependencies only |
| Stop-on-budget | Exceeding a time, CPU, memory, event, operation, or episode limit stops the run and yields `BLOCKED`; partial runs are not success-shaped |

The submitted values fit a software-only deterministic synthetic study in
principle; actual runtime feasibility is unverified. A dry-run may be used
only after approval, must use a separately declared non-scientific smoke
fixture, and may not inspect or tune on frozen evaluation outcomes. If the
4-hour or 2-GiB cap proves inadequate, stop and request a separately reviewed
budget revision before scientific execution.

## 4. Proposed dataset and protocol

### Generator and split

Use logical time units (TU), with no global neural timestep. Each episode is
generated on demand by a versioned deterministic PRNG from its seed and
episode ordinal. The same generated episode identity and event list is
replayed unchanged across arms. Use separate generator namespaces:

- training: episode ordinals `0..9999`;
- evaluation: episode ordinals `10000..11999`.

No evaluation stream, class, expected outcome or evaluator truth is exposed
to the mechanism. Keep all class labels and scoring in a separate evaluator.
Generators and episode IDs are content-hashed before running.

Use eight input-channel identities: `A`, `B`, and six nuisance channels
`N0..N5`. Every ordinary comparison episode contains exactly four events:
one `A`, one `B`, and two nuisance events. The nuisance-channel identities
and jitter are deterministic and matched by episode ID across arms.

The generator emits these balanced conditions:

1. **Order:** `A` then `B` versus `B` then `A`, same event multiset, event
   count, nuisance events, and absolute event-time multiset.
2. **Timing:** `A` then `B` with inter-event gap in `[0.75,1.25]` TU versus
   the same ordered channel multiset with gap in `[2.0,3.0]` TU; nuisance
   events are yoke-matched and total count is identical.
3. **Uncorrelated:** `A` and `B` times independently sampled from the
   declared episode window, without the target order/gap relation, with
   identical event counts and matched nuisance channels.
4. **Silent:** zero input events and no activation/reward event.
5. **No-reward:** ordinary matched event streams but no reward is delivered.

Jitter is uniform over the declared intervals using the per-seed PRNG;
timestamps are serialized as binary64 and rational generator coordinates.
Same-time ties use a stable episode event ordinal, not allocation or hash-map
order. Evaluation has 400 order episodes (200 per order), 400 timing episodes
(200 per gap class), 400 uncorrelated episodes (balanced against their
yoked-count controls), 400 delayed-reward episodes (equal counts for each
delay 0, 4, and 16 TU), 200 silent episodes, and 200 no-reward episodes.
The generator must reject future timestamps or labels presented to the
decoder; episode truth stays evaluator-only.

The training set uses 2,000 episodes from each of the five condition families
above, balanced within binary condition, with delayed rewards stratified
equally over delays 0, 4, and 16 TU. If this family allocation cannot be
implemented without leaking evaluator labels into decoder computation, stop
before execution and request a contract-level clarification.

### Learning and reward boundary

The reward signal is an explicitly identified local event delivered only
after the episode's final input event, at its frozen declared delay. The
decoder receives the scalar reward event, not the evaluator label or the
expected class. For the no-reward and silent conditions there is no reward
event. The evaluator may associate reward-present/reward-absent episodes with
the protocol solely for analysis; it must not route class truth into neural
state, update logic, eligibility selection, timing, or stopping.

Immediate received-event cost is recorded once at reception, before later
reward eligibility is known. Reward application has a distinct identity and
must be idempotent. It must not subtract or reapply the already-recorded
event-cost penalty. Arithmetic and state-access work used by the decoder and
reward update is separately counted below.

This proposed reward boundary requires explicit confirmation in independent
review: if delivering delayed reward in this manner is judged to expose
forbidden task truth or to exceed the existing Luna-64 contract, the gate is
BLOCKED until the owner separately clarifies the permitted reward source.

## 5. Proposed arm definitions

Each arm has the same input streams, initial-state policy, event opportunities,
reward identities, training exposure and evaluation episodes. Match trainable
scalar parameter count where applicable (maximum 256); record unavoidable
differences. Use deterministic initialization from the episode seed. Learning
rates and all thresholds must be constants in the versioned protocol before
the first scientific run.

| Arm | Frozen treatment |
|---|---|
| A — cost only | Immediate local event-cost accounting; no temporal eligibility and no weight update |
| B — simple eligibility | Event cost plus a bounded scalar trace per input identity, `e_i(t)=min(1, Σ exp(-(t-t_ij)/1 TU))`, expiring at 8 TU; apply the same delayed reward to eligible input parameters |
| C — linear temporal decoder | Event cost plus a linear decoder over the bounded fixed-delay history; train with the same local delayed reward interface as B |
| D — nonlinear PCN decoder | Event cost plus the same input history/capacity as C and a bounded nonlinear predictive-coding decoder with at most 32 SCU; internal prediction-error state is kept distinct from external reward/eligibility |
| E — ordering negative control | Same nonlinear decoder, parameter initialization, cost, eligibility, exposure and reward as D, but permute event temporal-order associations using a frozen per-episode deterministic permutation that preserves identity and count while breaking sequence order |

The contract does not specify decoder equations, parameter update equations,
initialization distribution, PCN error schedule, or reward scaling. To prevent
post-outcome choices, these details—including B/C/D update rules—must be
attached as a machine-readable protocol and independently reviewed/frozen
before any scientific run. This package does not invent a mathematical
equation where the accepted contract has left a design choice open.

## 6. Measurements and resource/energy proxy

Report per episode and per arm/seed:

- balanced accuracy on order and timing discrimination, by condition;
- order-sensitivity difference between the matched `A→B` and `B→A` streams;
- false activation/reinforcement rate on uncorrelated, silent and no-reward
  controls;
- delayed reward response for delays 0, 4 and 16 TU;
- per-input eligibility, per-input weight update and counterfactual event
  ablation response;
- maximum/mean retained history and eligibility occupancy;
- input events, decoder operations, memory reads/writes, reward updates,
  overflows and invalid episodes;
- exact deterministic replay equality of records and summaries.

Use an algorithmic energy proxy called **local-work units (LWU)**; it is not
joules or a hardware-energy estimate. Freeze these deterministic weights:

- one received input/reward event: 1 LWU, charged at reception exactly once;
- one scalar add/subtract/multiply/compare: 1 LWU;
- one scalar division: 4 LWU;
- one `exp`, `tanh`, or sigmoid evaluation: 8 LWU;
- one scalar state/parameter read or write: 1 LWU.

Count actual operations and accesses in the reference runner; no arm-specific
estimation and no omissions for supposedly negligible work. Report event
LWU, decoder-compute LWU, reward-update LWU and total LWU separately.
Primary efficiency is held-out correct episodes per 1,000 LWU; also report
absolute LWU per episode and per correct episode. Do not call these physical
energy or calibrated power.

For causal attribution specificity, freeze a paired counterfactual evaluation:
replay the exact held-out episode from its pre-episode state once per event
with that event removed and once with its timestamp shifted by +2 TU (when
within the declared episode bound). Record the change in the decoder's
activation/prediction score and resulting per-event eligibility/update.
Classify an event as causally influential only if removal changes the
predeclared score by at least `0.05`; publish attribution precision/recall
against these intervention outcomes, without using the evaluator class label.

## 7. Proposed success/failure criteria and statistics

All criteria are proposals and must be frozen before data generation. Primary
outcomes are paired on identical episode IDs across arms. For the primary
discrimination endpoint, D must:

1. achieve order and timing balanced accuracy of at least `0.70` each;
2. exceed C by at least `0.10` absolute balanced accuracy on each endpoint;
3. exceed E by at least `0.10` absolute balanced accuracy on each endpoint;
4. have a paired two-sided 95% cluster-bootstrap confidence interval whose
   lower bound is above zero for both D−C and D−E on each endpoint, using
   10,000 bootstrap draws resampling the five seed clusters (not individual
   events); adjust the four primary comparisons by Holm's procedure;
5. show a positive D−C endpoint difference in at least four of five seeds;
6. keep balanced accuracy on silent/no-reward and uncorrelated negative
   controls at or below `0.55`, and false activation/reinforcement at or below
   `0.05`;
7. demonstrate reward delay sensitivity: at delay 16 TU, D's correct-episode
   rate is not more than `0.10` below its delay-0 rate, and its attribution
   specificity remains greater than the matched uncorrelated control;
8. have D total LWU per correct evaluation episode no more than `2.0×` C's
   and no more than `4.0×` A's, with all LWU components published.

These thresholds are prospective decision criteria, not claims about likely
outcomes. If the five-seed clustered uncertainty procedure is degenerate,
bootstrap conditions cannot be met, or a primary comparison is missing, the
result is `INCONCLUSIVE`, not a success.

- **Scientific success:** all eight criteria pass with deterministic replay
  and resource/boundedness checks passing.
- **Scientific failure / NOT SUPPORTED:** any primary efficacy threshold
  fails with the confidence interval entirely at or below zero, or a negative
  control exceeds its false-activation limit.
- **INCONCLUSIVE:** estimates fall between success and failure criteria,
  uncertainty is too wide, or some but not all criteria pass.
- **BLOCKED:** provenance/replay failure, budget overflow, information-boundary
  breach, unbounded state/work, invalid reward identity/accounting, missing
  primary artifact, unauthorized file change, or unresolved numeric ambiguity.

Report metric definitions, confusion matrices, per-seed results, all trial
counts, confidence intervals, adjusted p-values, operation counts and
negative results. No thresholds may be changed after evaluation outcomes are
seen.

## 8. Numerical tolerance and reproducibility

- Event identity, event order, exact rational fixture coordinates, reward
  identity, update count, overflow disposition and replayed canonical JSON:
  exact equality.
- Binary64 state/score equality across two replays in the same interpreter and
  platform: exact bitwise equality.
- Cross-platform comparisons are not success criteria. Record OS, Python
  version, dependency lock/hash, CPU model, Git SHA and protocol/fixture hashes.
- Independent high-precision analytical checks for generator times and
  simple eligibility use a relative/absolute tolerance of `1e-12`; decoder
  causal outcome classification is exact at the predeclared `0.05` score
  threshold, with no hidden tolerance around it.
- Any non-finite timestamp/value, unresolved tie, representability issue or
  threshold comparison ambiguity is a visible failure/block, never a clamp
  or silent fallback.

The independent reviewer must assess whether these tolerances are suitable
for the specified implementation language/runtime before they can be frozen.

## 9. Independent review and authorization gates

Required order:

1. Independent Luna-0 review this exact gate package and record a separate
   verdict, findings, and artifact hash. The review must cover fairness,
   reproducibility, reward leakage/accounting, feasibility, statistics,
   allowed/forbidden paths, exact branch/worktree plan, and Luna-63C isolation.
2. Address any review blockers by a new versioned proposal; do not erase this
   record or treat the original governance PASS as the gate review.
3. Obtain explicit project-owner approval naming `L64-TB-GATE-20261010-R0`
   and the accepted package hash. Requesting preparation is not approval.
4. Commit the accepted contract, original governance PASS, approved gate and
   required governance index/changelog entries; record that freeze commit SHA.
5. Only then create the dedicated worktree/branch at that exact SHA and dispatch
   Luna-64.

Independent review verdict for this proposal: **PENDING**. Owner approval:
**NOT PROVIDED**. Execution authorization: **NOT GRANTED**.

## 10. Remaining open design gate

The accepted Luna-64 contract intentionally describes the model class and
scientific objectives but not an exact decoder/update implementation. This
proposal therefore refuses to select equations after inspecting any result.
Before this gate can be called fully frozen, the execution protocol must
specify the linear/nonlinear decoder equations, PCN prediction/error updates,
local reward/eligibility update rule and initialization as a versioned,
reviewed artifact. If these cannot be agreed without changing the Luna-64
contract, stop and obtain an explicit owner decision; do not silently amend
the preserved contract.

## 11. Current execution decision

**READY FOR INDEPENDENT REVIEW ONLY.**  
**NOT READY FOR OWNER APPROVAL until that review is completed and any
findings are resolved.**  
**NOT AUTHORIZED TO CREATE THE EXECUTION BRANCH/WORKTREE OR BEGIN LUNA-64.**
