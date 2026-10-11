# Luna-0 — Track B / Luna-64 corrective execution gate R1

**GATE ID:** `L64-TB-GATE-20261010-R1`  
**PREDECESSOR:** `L64-TB-GATE-20261010-R0`  
**PREDECESSOR SHA-256:** `5B4C8E74C3536AEA7111C749970FF44BA3DB8855317679C6EF013EAB5149CF08`  
**STATUS:** DRAFT FOR INDEPENDENT REVIEW — NOT FROZEN  
**OWNER APPROVAL:** NOT PROVIDED  
**EXECUTION AUTHORIZATION:** NOT GRANTED  
**LUNA-64 CONTRACT:** PRESERVED, NOT AMENDED  
**LUNA-63C:** READ-ONLY / NO DEPENDENCY / NO SCOPE CHANGE

This is a corrective proposal only. R0 and its independent review remain
unchanged. No experiment, smoke test, benchmark, branch, or worktree has been
created. This R1 text proposes resolutions but is not evidence of their
acceptance or feasibility. An independent review PASS and explicit owner
approval of this exact R1 package are separate required gates.

## 1. Reconciled authority and state

The R0 SHA was recomputed from its current bytes and matches the reviewed
predecessor digest above. `HEAD == origin/main ==
73aaa50f97ceab322907875ae4dcf23e7541c3b5`. The checkout is not clean: the
previous Luna-64 contract, initial governance handoff, workflow/changelog
updates, R0 proposal, and R0 review are local uncommitted governance
artifacts. This draft and its protocol are likewise not committed.

The initial governance PASS is preserved as a documentation-only governance
PASS. It does not authorize an experiment. The Luna-63C Stage-A certificate
remains independently gated and Stage B remains blocked pending its own
certificate review. R1 neither relies on nor changes the Luna-63C chain.

## 2. R0 finding-to-correction traceability

| R0 finding | Proposed R1 correction | Testable acceptance condition | Independent verification procedure | State |
|---|---|---|---|---|
| 1. Reward origin, content, recipient, and same-time order unresolved | §3 defines local activation as the only proposed reward origin, typed immutable identities, event phases, and a label-blind reward source; no reward is calculated from evaluator truth | Replaying an event graph produces exactly the same IDs/order; duplicate delivery creates no duplicate credit; evaluator labels are inaccessible to generator/decoder/reward code; exact-time expiry preempts credit | Reviewer inspects protocol/code boundary and independently constructs same-time, duplicate, label-canary, and replay fixtures | Proposed; requires reviewer and owner acceptance |
| 2. Eight-TU trace expiry conflicts with 16-TU reward delay | §4 selects bounded two-stage activation-associated credit records; input eligibility is snapshotted at activation and retained past the maximum reward due time | Credit record has fixed cap and TTL; reward at due time is credited before the next-representable expiry; delivery at/after expiry is rejected; no eligible input is silently dropped | Reviewer recomputes maximum links/records and checks 8-TU trace expiry, 0/4/16-TU rewards and the exact nextafter boundary | Proposed; resource fit unverified |
| 3. Decoder/training lifecycle incomplete | §5 and `luna64-track-b-protocol-r1.json` define intended lifecycle fields, but do not invent a PCN learning rule absent from the accepted contract | All arms must have complete frozen equations, initialization, training persistence, reset/evaluation, reward semantics, PRNG, precision, and operation bounds in the accepted protocol | Independent reviewer must be able to implement from protocol alone and reproduce a hand-calculated fixture | **BLOCKING: exact PCN / reward-learning equations still require an accepted design decision** |
| 4. Dataset not replayable | §6 defines counter-based digest-derived random words, namespace/ordinal mapping, event alphabet, episode layout, splits, and a generator conformance fixture | Independent generators match all event IDs, exact binary64 time bits, conditions, and truth labels across all fixed fixture IDs | Reviewer implements generator independently from prose/config and compares canonical bytes/digests | Proposed; full generator fixture not generated in this governance-only phase |
| 5. Arm fairness and endpoint scoring ambiguous | §§5,7 specify common inputs, transformations, outputs, `N/A` scoring when no decoder exists, class definitions, confusion counts, and attribution protocol | No arm gets labels/bonus feedback; same episode identities are paired; absent output is not scored as false or correct; controls preserve event multiset/count | Reviewer tests transformed episode identity and verifies metric code/hand calculations against tiny fixtures | **BLOCKING: cannot freeze endpoints until the local activation/readout rule is approved** |
| 6. Statistical plan incomplete | §8 proposes seed-cluster paired bootstrap, exact resampling and Bonferroni-adjusted intervals with missing/zero-denominator policies | Analysis implementation matches an independent miniature fixture and returns deterministic intervals/adjustments | Reviewer independently computes the fixture and verifies resampling units and family | Proposed; low cluster count remains a stated power limitation |
| 7. Runtime budget unsupported | §9 gives deterministic maximum work/space formulas and conservative operation totals; empirical feasibility remains explicitly unverified | Reviewer recomputes bounds; any arithmetic excess forces budget revision, and no runtime-feasibility claim is accepted without separately authorized measurement | Reviewer independently recomputes episode/replay/operation maxima and checks no performance result is claimed | **BLOCKING: proposed four-hour ceiling lacks empirical support** |
| 8. LWU definition/instrumentation absent | §10 locates the established `LocalEnergyModel` proxy and refuses to rename it LWU or add new unit weights | If retained proxy is used, all values/counters follow the existing API/unit and the experiment does not claim LWU; otherwise a project-owner-approved definition and review are required | Reviewer checks source/API and instrumented counters against exact event fixtures; verifies there is no physical-joule claim | **BLOCKING: repository defines activity-cost-proxy, not LWU or operation-weighted energy** |

Every row requires a separate reviewer disposition. “Proposed” is not
“resolved”; the blocker rows prevent R1 from being declared ready for owner
approval or execution.

## 3. Proposed reward provenance and causal event contract

### 3.1 Proposed label-blind origin

Candidate-only proposal: after receiving and processing any `B` input, a
shared local postsynaptic adapter emits exactly one `ACTIVATION` event, even
if the separate episode-close classifier has no positive decision. This
causal event is the same in all five arms and depends only on the current B
reception and the adapter's fixed rule, not on evaluator truth or model
accuracy. It creates a reward origin with value `+1.0`, addressed to the same
instance; due time is `activation_time + delay_TU`, where delay is a
predeclared treatment value `{0, 4, 16}`. No generator class, evaluator
label, correctness score, future event, or benchmark condition field is an
input to reward creation. For the designated no-reward treatment, the
delivery mechanism is disabled by the experiment harness; the decoder gets
no treatment flag, only the absence of a reward message. Every arm receives
the same activation/reward event stream; A records but ignores rewards, B
uses eligibility, and C/D/E use their specified local update rules.

This proposed intrinsic activation reward avoids an evaluator-derived scalar,
but it may not constitute the scientifically intended activation reward or
support every arm. It therefore requires explicit independent review and
owner acceptance before freeze. It is not a contract amendment.

### 3.2 Stable identities and relations

IDs are deterministic tuples serialized canonically as strings:

- input: `(gate_id, split, seed, episode_ordinal, input_ordinal)`;
- reception: `(input_id, decoder_instance_id, "receive")`;
- activation: `(reception_id, "B-activation")`;
- reward origin: `(activation_id, "reward-origin")`;
- reward delivery: `(reward_origin_id, "delay", delay_code)`;
- credit assignment: `(reward_delivery_id, eligibility_snapshot_id,
  source_input_id)`;
- energy-cost accounting: `(reception_id, "event-cost")`.

Creation time and ownership are stored separately from identity. Each input
has exactly one reception in an episode replay and exactly one event-cost
record. Reward origin is a child of one activation; delivery is a child of
one origin; each credit is a child of one delivery and one frozen eligibility
entry. The receiver keeps bounded seen-ID sets; a duplicate ID is an explicit
duplicate/no-op outcome, never applied twice. Replay uses the same IDs and
canonical serialization.

### 3.3 Lifecycle and ownership

1. The generator creates an immutable input record and its stable input ID;
   it owns timestamp, channel, episode ordinal, and split metadata.
2. The decoder-local receiver validates the time and ID, records one
   reception, and charges one immediate event cost before later reward status
   is known.
3. The same local receiver admits the event to its bounded history or records
   a typed overflow and invalidates the episode.
4. Eligibility updates from only the causal local history and current
   reception; no label or future input is available.
5. After every valid B reception, the shared local adapter creates one
   activation event; it is not a classifier decision.
6. The activation owner creates one fixed-value reward-origin record with
   child identity.
7. The delivery owner schedules/delivers that origin using the declared
   delay; retries keep the same delivery identity.
8. The eligibility owner applies each delivery once to the frozen
   activation snapshot, recording one credit assignment per source input.
9. Local lifecycle cleanup expires records at the specified endpoint and
   records each expiry; episode reset clears only episode-local bounded state.

The energy meter owns event-cost IDs; the decoder owns reception/history and
eligibility IDs; the shared adapter owns activation/reward-origin IDs; the
delivery queue owns delivery IDs; credit ledger owns assignment IDs. No
component may synthesize another component's ID or re-charge an existing
reception.

### 3.4 Total deterministic same-time ordering

Time is the physical logical timestamp in TU, stored as binary64 with the
exact generator integer/rational source retained as provenance. Tie keys are
not physical time. For equal physical time, process by:

1. `EXPIRY` / invalidation of entries whose expiry time equals this time;
2. `RECEPTION`, ordered by stable input ID;
3. `ACTIVATION`, ordered by parent reception ID then activation ordinal;
4. `REWARD_ORIGIN`, ordered by activation ID;
5. `REWARD_DELIVERY`, ordered by reward-origin ID then delay code;
6. `CREDIT_ASSIGNMENT`, ordered by delivery ID then source input ID;
7. `CLEANUP`, ordered by owning record ID.

Child events are processed only after their causal parent; phases plus parent
precedence form a total order. No queue/map iteration, thread schedule, or
allocation order is consulted. Same-time reward can credit an input only if
its reception causally precedes the activation, the eligibility snapshot
contains that reception, and the snapshot has not expired. An input at exact
eligibility expiry is not admitted to that expiring eligibility. A delivery
at exact credit-record expiry is rejected because expiry precedes delivery.
The proposal sets expiry to `nextafter(due,+∞)` so a reward at the exact due
time precedes expiry without an arbitrary epsilon. The reviewer must verify
representability and strict-future semantics before freeze.

This scheduler is confined to the isolated experiment adapter. It does not
change the canonical production event queue or establish global neural ticks.

## 4. Eligibility choice: Option B, activation-associated bounded credit

R1 proposes **Option B** rather than silently extending every input trace to
16 TU.

- Input eligibility is a scalar event-local exponential trace with
  `tau_e=1 TU`, cap `1.0`, and expiry after `8 TU`; updates occur only on
  receptions and local event handling, not on a global timestep.
- On activation, snapshot the current nonzero eligible input IDs and their
  eligibility values into one activation-associated credit record. This
  preserves causal ancestry as observed by the mechanism but is not itself
  proof that an input caused activation.
- Maximum episode inputs: 32. Maximum activations: one per reception, hence
  32. Maximum activation credit records: 32. Maximum source links:
  `32 × 32 = 1,024` per episode. Record payload is at most 32 pairs of
  `(input_id, eligibility_binary64)`.
- Credit record lifetime: until reward due at activation+16 TU is handled, or
  terminal expiry at `nextafter(activation+16 TU,+∞)`, whichever is first
  under the frozen event order. The reward at the exact due timestamp is
  delivered before this strictly later expiry; a delivery at expiry is
  rejected.
- Capacity overflow rejects the creating activation/reward child chain,
  emits an explicit `CREDIT_CAP_OVERFLOW`, invalidates that episode, and
  cannot evict old records or create partial credit. An overflow is not a
  valid sample.
- Reward ID application is idempotent; expired/unknown snapshots produce a
  typed `CREDIT_EXPIRED` record and no update. Cleanup is bounded.

To guarantee a 16-TU reward, expiry is proposed as the next representable
timestamp after due. This binary64 boundary rule is not yet independently
verified. Option A would instead retain
each eligibility for at least 16 TU plus this same boundary rule, increasing
occupancy of input identities and event history; Option B limits long-lived
state to the activations actually created.

## 5. Model and lifecycle specification boundary

All arms use a single decoder instance per `(seed, arm, training run)`.
Parameters persist across the ordered training episodes for that run, then
are frozen for evaluation. Per-episode dynamic traces, histories, activation
ordinals, credit records, and duplicate-ID sets reset at episode start.
Parameter arrays reset once per seed/arm from a named deterministic
initialization namespace. Evaluation has no updates, and all reward events
are logged but ignored by the frozen parameter update path.

Common numeric representation proposed: IEEE-754 binary64; reject NaN/Inf;
no silent clipping except explicitly defined state clamps; stable sums in
input-ordinal order; exact ID/order comparison; strict threshold comparisons.
The precise threshold and decoder equations must be in the final accepted
machine-readable protocol, not left to the execution worker.

| Arm | Input/state proposal | Forward and score interface | Learning/reward lifecycle | Bounds/status |
|---|---|---|---|---|
| A: immediate energy only | No temporal state or trainable parameters | No decoder output; discrimination metrics are `NOT_APPLICABLE`, not zero or failure | Event cost only; no eligibility or reward update | At most one event-cost record per reception |
| B: simple eligibility | One bounded trace per input channel, event-driven decay `e_i(t)=min(1,Σ exp(-(t-t_ij)/1 TU))`, 8-TU expiry; activation-associated credit snapshot | No predictive decoder; report eligibility/credit attribution diagnostics only; predictive performance `NOT_APPLICABLE` | On delivered shared local activation reward, candidate scalar channel weight update `w_i←clip(w_i+η r e_i,[-1,1])`; `η` still requires freeze | At most 8 traces + 32 activation records × 32 links per episode |
| C: linear temporal decoder | Eight channel traces plus fixed-delay feature `f_i(t;d)=Σ exp(-(t-t_ij)/1 TU)` for `d∈{0.5,1,2,4}`; finite 8-TU event horizon | Candidate linear score `s=b+Σ w_ik f_ik`; activation/output threshold and readout semantics are not yet frozen | Must specify local prediction-error/activation-reward update; not permitted to use class label | ≤32 hidden scalar units; ≤256 parameters; per-input operation ceiling from config |
| D: nonlinear PCN decoder | Same causal feature vector as C; hidden state `z∈[-1,1]^8`; prediction vector over 8 channels | Candidate `z=tanh(Wf+b)`, `xhat=tanh(Vz+c)`; internal residual `δ=x-xhat` is prediction error, never the reward; readout/activation equation is not yet frozen | Must specify bounded local PCN state/parameter updates and their relationship to delayed reward; no future input or evaluator truth | ≤32 SCU, ≤256 parameters; PCN update count must be frozen |
| E: disrupted nonlinear control | Same D equations and initial parameters; for each episode, reverse the deterministic assignment of event identities to the episode’s sorted timestamp slots, preserving count and exact time multiset | Same D score/readout | Same D update and reward handling; treatment transform is applied before any decoder access | Pair by underlying episode ID; transformed event list hashed separately |

**Blocking design gap:** the italicized/unfixed fields above (learning rates,
PCN update law, output/readout threshold, activation generation, activation
reward recipient and reward scale) are the experiment's central mechanism,
not implementation details. R1 cannot claim that the arms are fully
specified without a reviewed exact protocol and owner approval if it
constrains/changes the accepted contract. The table is a proposal for that
decision, not execution-ready authorization.

## 6. Deterministic generator proposal

Generator version `L64-GEN-1`. Input channels are `A`, `B`, `N0..N5`.
Event time uses integer microticks where one TU is 1,000,000 ticks;
serialization stores both integer ticks and the exact binary64 conversion.
Episode identity is `(version, split, seed, ordinal)`.

Randomness is counter-derived rather than mutable stream state. For every
draw, compute SHA-256 of UTF-8 canonical
`L64-GEN-1|seed|split|episode_ordinal|draw_name|draw_ordinal`; interpret the
first 64 digest bits as unsigned big-endian integer `u`, then map to integer
range `[0,n)` by `floor(u*n/2^64)`. No rejection sampling is used; the tiny
modulo bias is avoided by this floor map but finite-bin discretization remains
part of the generator. Random draw names are fixed per condition.

Each ordinary episode has exactly four magnitude-1.0 events: one A, one B,
one N0 and one N1. N0/N1 are nuisance identities and their times are independent integer
microticks in `[6,7.999999] TU`, drawn from named counters. This fixed late
nuisance window prevents changing event count and is retained in every
paired arm.

- Order positive: A at 0.25 TU, B at `0.25+gap`, where `gap` is uniform in
  integer microticks `[750000,1250000]`.
- Order negative: B at 0.25 TU, A at `0.25+gap`; same gap draw and nuisance
  event time draws as its paired positive episode.
- Timing short/long: A precedes B; gap intervals `[750000,1250000]` and
  `[2000000,3000000]` microticks. For pair identity, draw a single `g∈[0,1]`
  integer fraction and map both endpoints using the same g index.
- Uncorrelated: A and B each independently assigned a time in integer
  microticks `[250000,4250000]`, from distinct named draws; no order/gap
  conditioning. Exact event counts remain four.
- Silent: zero input events. No activation or reward is supplied by the
  generator.
- No-reward: ordinary matched streams; the proposed local reward delivery is
  withheld as an experimental treatment, without exposing a treatment flag
  to decoder state.

Training ordinals are `0..9999`; each consecutive block of 5 is assigned in
fixed order to order, timing, uncorrelated, silent, and no-reward conditions.
Within order/timing groups, the binary condition alternates by
`floor(ordinal/5) mod 2`; reward delay treatment cycles by
`floor(ordinal/5) mod 3` across `{0,4,16}`. Thus the three rewarded task
families each have 2,000 examples split across the three delay values as
667/667/666; this imbalance is deterministic and reported. Silent/no-reward
remain controls. Evaluation ordinals are `10000..11999`, allocated as
follows: 400 order (200/class), 400 timing (200/class), 400 uncorrelated,
396 delayed-reward probes (132/delay), 202 silent, 202 no-reward. The 396
probes are 132 base episodes (66 order, 66 timing, balanced within each
binary class); each base episode is cloned with delay 0, 4, and 16 TU and
gets a distinct episode/reward identity while retaining a shared base-ID for
paired analysis. Ordinal blocks are order `10000..10399`, timing
`10400..10799`, uncorrelated `10800..11199`, delayed probes
`11200..11595`, silent `11596..11797`, and no-reward `11798..11999`.
The two control strata have IDs independent of primary rows. Five seeds
remain `6401..6405`.

**Open generator ambiguity:** the preceding allocation is not executable
until all draw-name conventions, exact base-ID mappings, and generated
golden digests are recorded in a fixture. This draft does not claim that
condition has been met.

**Blocking generator gap:** the exact paired episode map, full evaluation
allocation, label truth for overlaps, activation/reward schedule, and
golden expected fixture digests are not yet generated or frozen. The prose
above is not yet enough to claim a published reproducible dataset.

## 7. Scoring proposal

Evaluation labels are generated only in evaluator-owned records:
`order=1` for A-before-B and `0` for B-before-A; `timing=1` for short-gap and
`0` for long-gap. Uncorrelated, silent, and no-reward are control strata, not
additional classes in primary accuracy.

For C/D/E, prediction is a binary output at the local episode-close cue, an
explicit external event at the declared end time; the close cue contains no
label or expected output. A and B have no decoder and are reported as
`NOT_APPLICABLE` for predictive endpoints. This close-cue output interface
and exact decoder threshold remain to be frozen with model equations.

Primary task endpoints: order balanced accuracy and timing balanced accuracy
on held-out episodes. Report confusion matrices, class-conditional TPR/FPR,
false activation on silent/no-reward/uncorrelated controls, and invalid /
overflow counts. No output is distinguished from a negative prediction; a
missing/corrupt record invalidates the sample.

Attribution diagnostic: for each delivered reward, record the eligibility
snapshot's per-input values and exact parameter deltas. Replay from a copy of
pre-episode state with one input removed and separately shifted by +2 TU.
These are counterfactual diagnostic interventions, not online inputs.
An input is “mechanistically influential” only if the predeclared activation
score changes by at least 0.05 absolute and the corresponding update changes
by at least 0.01. Report precision/recall against these intervention-defined
influence cases; do not call temporal proximity alone causal contribution.
These thresholds are proposed and remain subject to independent review.

Magnitude-control diagnostic: replay each held-out ordinary episode twice
from the same pre-episode state, scaling all four event magnitudes by 0.5
and 1.5 while keeping channel identities, times, event count, and labels
fixed. Record score, activation, local update, and meter changes separately;
these replays are diagnostics and do not replace the primary magnitude-1.0
evaluation.

Primary resource endpoints are received-event count, activation/reward count,
per-category repository energy proxy, exact scalar operation counts, peak
trace/credit occupancy, and correct episodes per declared proxy unit only if
the proxy unit is accepted. Report B/C/D/E predictive results separately;
do not fabricate a score for A/B.

## 8. Statistical analysis proposal

Five fixed seeds are clusters; episode IDs are paired across arms. Primary
comparison family is D−C and D−E for order balanced accuracy and timing
balanced accuracy (four comparisons). For each seed, compute arm metrics
over the corresponding paired test episodes; primary effect is the equal
weight mean of five seed-specific differences (not pooled event accuracy).

Enumerate all `5^5=3,125` ordered seed-index tuples with replacement (no
bootstrap RNG). In each tuple, retain all paired episode records within each
sampled seed, recompute the seed-specific endpoint and the equal-weight mean
of the five seed-specific paired differences. Sort the 3,125 estimates;
quantile uses nearest-rank `ceil(p*N)` (1-based, clamped to `[1,N]`). For
the four primary comparisons use Bonferroni-adjusted two-sided intervals at
98.75% each (quantiles `[0.00625,0.99375]`, ranks 20 and 3,106), giving
familywise nominal alpha 0.05 under the bootstrap assumptions. No separate
p-value test is added. Five seed clusters remain a severe inferential
limitation; degenerate or unsupported intervals yield `INCONCLUSIVE`, not a
relaxed gate. Report all five seed-level results and the complete ordered
tuple convention so the interval is exactly reproducible.

No hyperparameter tuning on evaluation data. Missing/overflow episodes are
reported and treated as invalid; if any arm/seed has >1% invalid episodes,
primary scientific verdict is `BLOCKED`. A class with zero valid samples
makes that endpoint undefined and verdict `INCONCLUSIVE`. Zero correct
episodes makes “cost per correct” infinite/undefined, reported as such; no
epsilon substitution. Numeric equality is exact for IDs, event order, counts
and binary64 replay on identical platform; hand fixtures use `1e-12`
absolute/relative check only for derived arithmetic, never near activation or
expiry decision boundaries.

Success thresholds remain R0 proposals only until independent acceptance:
balanced accuracy ≥0.70 on both primary endpoints; D−C and D−E ≥0.10
absolute on both endpoints; all four 98.75% adjusted interval lower bounds
above zero; D−C positive in at least four of five seeds for both endpoints;
uncorrelated/silent/no-reward false activation ≤0.05; delayed performance
difference ≤0.10; and proxy cost ratios
≤2× C and ≤4× A if a valid common proxy is available. If proxy is not
authoritatively defined, the energy-efficiency criterion is blocked, not
waived. No test-set-based threshold revision.

## 9. Analytical resource feasibility (not an empirical result)

R0 ceilings imply at most:

- training: `5 arms × 5 seeds × 10,000 = 250,000` episodes;
- evaluation: `5 × 5 × 2,000 = 50,000` episodes;
- paired input-removal/time-shift and magnitude diagnostics: at most 10
  altered replays per ordinary four-event episode, hence up to `500,000`
  additional replays;
- total upper bound: `800,000` episode executions before integrity replays;
- at most 32 inputs/episode and 1,024 scalar operations/input gives
  32,768 operations/episode; naive product upper bound is about
  `26.21 billion` scalar operations, excluding setup, serialization and hash
  costs.

The 4-hour proposal would require at least about 1.82 million counted scalar
operations/second at that loose maximum, before interpreter and I/O overhead.
This is arithmetic, not a runtime measurement. The analytical upper bound
does not establish feasibility, so the four-hour ceiling is **not justified**
for the R0 exposure limits. Do not run a feasibility microbenchmark under this
gate. A separately reviewed protocol must lower its workload or receive
separate explicit authorization for an isolated non-scientific feasibility
microbenchmark; any benchmark must use only a non-evaluation smoke fixture.

Storage bound proposal per instance: at most 256 history entries, 8 trace
scalars, 32 credit records × 32 links, 256 parameters, 32 SCU, ≤32 activation
records, and ≤32 input/reception/cost records, plus fixed-size logs. The
serialized raw log is bounded by 64 KiB/episode if each record is capped at
256 bytes and there are at most 256 records; any exceeded cap stops the run.
Worst-case OS/process memory remains empirical and unverified. CPU=1 logical
core and memory=2 GiB are stop ceilings, not demonstrated adequate limits.

## 10. Energy metering and LWU finding

Repository inspection found no authoritative definition or occurrence of
**LWU** outside R0. The existing
[`energy_utility.py`](../../tpcn/energy_utility.py)
defines `LocalEnergyModel` snapshots with unit default
`activity-cost-proxy`, configurable nonnegative activity costs, and counters
`events_received`, `events_emitted`, `neuron_activations`,
`operator_activations`, `state_changes`, `connection_activity`, and
`prediction_errors`. It does not define per-op LWU weights, calibrated joules,
or language/runtime overhead.

R1 therefore **does not define LWU and does not adopt R0's invented
operation-weight coefficients**. A compatible fallback proposal is to record
the existing unit and exact category counts/cost inputs through the established
API, leaving per-operation counts (add/multiply/exp/tanh/read/write) as a
separate dimensionless operation ledger, not energy. Do not combine the two
into “energy per correct” unless a reviewed conversion is authorized.

This is still a blocker to the requested operation-weighted energy-proxy
comparison: exact cost values supplied per activity category and experimental
meter ownership/idempotency need protocol-level validation. If the owner
requires the label LWU, the owner must approve a definition and its scope
before any instrumented run. No hardware energy or joule equivalence is
claimed.

## 11. Isolation and branch/worktree proposal

- Branch name, only after all gates: `experiment/luna64-track-b-ltrd`.
- Dedicated worktree only; never create it before independent review and
  explicit owner approval.
- The current `73aaa50f97ceab322907875ae4dcf23e7541c3b5` is a source baseline
  candidate, not an execution base. First commit the accepted governance
  freeze as docs-only; then branch the isolated worktree at that resulting
  immutable SHA and record its tree identity.
- Allowed writes: `experiments/luna64/**`,
  `tests/test_luna64_*.py`, `artifacts/luna64/**`, and the assigned Luna-64
  execution handoff only.
- Forbidden writes: `tpcn/**`, all existing tests, `experiments/luna63c/**`,
  `artifacts/luna63c/**`, all Luna-63C fixtures/certificates/manifests/
  W/T/E/N5/corrective records, architecture contracts/ACPs/defaults,
  unrelated experiments or governance artifacts, and any production merge.
- Any required file outside allowed writes stops work pending separate
  authorization. No task data from network or private sources; no GPU or
  hardware dependency.

## 12. Required independent review and owner gate

The independent reviewer must examine the exact R1 bytes and protocol
configuration, not a digest copied from this document. Reviewer verifies the
matrix, event lifecycle, lifetime/tie semantics, model equations, generator
golden fixture, scoring, analysis arithmetic, analytical runtime/space bound,
meter API compatibility, baseline and frozen-path boundaries. The reviewer
must not edit the R1 package or execute it.

No owner authorization is inferred from this request. Even if review returns
PASS, the owner must explicitly approve gate ID `L64-TB-GATE-20261010-R1`
and the package SHA-256. Only after that approval may the docs-only gate be
committed and an execution worktree created at the freeze commit.

## 13. R1 draft disposition

**Independent review:** pending.  
**Owner approval:** not provided.  
**Publication:** draft only; no workflow/changelog authorization entry is
made.  
**Execution:** not authorized.  
**Known blockers:** exact reward/activation/PCN equations; independent
verification of eligibility timestamp representability; fully frozen
generator fixtures and evaluation allocation;
validated statistical fixture; empirical runtime feasibility (no run
authorized); and authoritative LWU definition or a reviewed alternative
using the existing activity-cost-proxy without claiming LWU.

If the independent review finds any blocker unresolved, preserve its review
as a separate record and prepare R2; do not publish an authorization claim.
