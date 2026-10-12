# Luna-65 — Spiral Current-Network Resumption

**Status:** Interface plan independently reviewed; additive public API is the
lowest-risk proposed path. Implementation, fixture checks, and benchmark
execution each remain unauthorized. Full-replication E2 identity capacity
is not analytically established.  
**Dispatch chain:** Luna-0 → Luna-65 → Luna-0.  
**Classification:** bounded synthetic benchmark and readout efficacy
experiment; software reference only.  
**Baseline:** `f2ce64b1c514d6e2cf5fc9b741418e5c944da59a`.  
**Historical reference:** Luna-12G, whose TANH_LEGACY results/artifacts remain
separate and immutable.

## Hypothesis and scope

**H1:** On previously unseen geometric paths, the current
`EXCURSION_V1` software-reference path with a fixed bounded topology and
external readout can learn the directed winding label from temporal order.
An exact matched pair contains the same coordinates and timing schedule in
opposite event orders and carries opposite labels. A static point-set
shortcut cannot distinguish members of a pair.

**Counter-hypothesis:** Paired directed-order accuracy does not exceed chance,
the ordered condition is not better than the label-conflicted shared-shuffle
control, or results are unstable across fixed network seeds. Any such valid
result is a negative or inconclusive efficacy outcome, not an implementation
success.

This experiment tests the current software-reference workload path, not a
production architecture claim. It does not test a structural-learning
benefit, handwriting, hardware equivalence, or an architecture change. No ACP
is proposed or required.

## Historical baseline: Luna-12G preserved

Luna-12G was a synthetic two-class software-reference experiment authorized
2026-09-27. Its preserved handoff reports 32 examples per class in each
training/evaluation split, 20 epochs, train/evaluation seeds `12007`/`12017`,
and runner seed `17`. Sequence digests were disjoint. It had no validation
split or multi-seed uncertainty estimate.

| Luna-12G condition | Accuracy | Left | Right | Final edges | Structural decisions |
|---|---:|---:|---:|---:|---|
| Fixed topology + learning | 0.53125 | 0.46875 | 0.59375 | 1 | 0 |
| Structural plasticity + learning | 0.53125 | 0.46875 | 0.59375 | 7 | 325 (12 additions, 8 prunes) |
| Shuffled order | 0.53125 | 0.46875 | 0.59375 | 1 | 0 |
| Time reversal | 0.53125 | 0.46875 | 0.59375 | 1 | 0 |

The fixed and structural confusion counts were identical: left→left 15,
left→right 17, right→left 13, right→right 19. No-learning reported 0.0 but
represented no readout classes; that is not a meaningful chance baseline.
Reported prediction loss was 0.0 in all conditions. Structural topology used
more edges and more events without improving accuracy; its reported energy
proxy increased from 357.6535 to 371.0408 and utility declined from -353.6535
to -367.0408. This does not establish structural efficacy.

The historical generator/run-controls family is explicitly
`TANH_LEGACY`; Luna-32 later made that compatibility choice explicit. It is
not current `EXCURSION_V1` / ACP-0007 efficacy evidence. Preserve
`artifacts/spiral-handedness-12g/`, its original handoff, and the Luna-32
compatibility record byte-for-byte. The historical shuffled and reversal
controls retained the original labels; the resumption below corrects the
semantics by defining labels as *directed* winding and inverting labels on
time reversal.

## Dataset, matched information, and splits

Use generated point sequences only. Define geometric handedness `g` as +1
for the existing positive-y / increasing-angle path and -1 for its
reflection. Define traversal direction `d` as +1 for forward event order and
-1 for exact reversal. The task label is the sign of `g*d`. Thus reversing
the exact same coordinates changes the directed winding label and does not
change any point value, point count, spatial nuisance, or timing interval.
Keep target label, `g`, and generator metadata outside the event stream.

At point fraction `u=i/15`, generate the shared base curve with
`r = radial_growth*u`, `theta = angular_speed*2*pi*u + rotation`,
`x = offset_x + scale*r*cos(theta)`, and
`y = offset_y + g*scale*r*sin(theta)`. Use 16 points, duration 240 for
train/validation and the test reference schedule, rotation U[0, 2*pi),
scale U[0.8, 1.2], each translation U[-1, 1], angular speed U[1.7, 2.5]
turns per duration, radial growth U[0.7, 1.1], radial jitter U[0, 0.04],
and coordinate noise U[0, 0.025]. Set random timing jitter to zero; the
explicit test timing factors below are the only timing intervention.
Perturbations are sampled once per base curve and shared by both orders.
These bounds retain the historical generator's nuisance envelope but do not
reuse its task data or historical result.

For every base curve, create exactly two examples: the original point order
and its exact reversal. They share a pair ID and point-set digest and have
opposite labels. Balance geometric `g` within each split and pair all examples
before splitting. Split **base curves**, not individual members, so no curve,
reversal, or matched point set can cross train/validation/test.

Per each of eight replications:

| Split | Base curves | Geometric handedness | Task examples |
|---|---:|---:|---:|
| Train | 64 | 32 per `g` | 128 (64 per directed label) |
| Validation | 32 | 16 per `g` | 64 (32 per directed label) |
| Test | 128 | 64 per `g` | 256 (128 per directed label) |

Use 16 points per curve; same shared base point set for each forward/reverse
pair. Rotation, scale, translation, radial growth, and point coordinates
must have identical class-symmetric distributions. Do not normalize from
future points or use labels/metadata for input construction. Keep all
generated streams, pair IDs, split IDs and SHA-256 digests in a manifest.

Use independent deterministic seed streams per replication `s` in
`65001..65008`: network seed `s`, train generator seed `s+100000`,
validation seed `s+200000`, test seed `s+300000`, shuffle seed `s+400000`,
and bootstrap seed `65999`. Derived per-curve seeds must be a published,
stable function of the split seed, curve index, and geometric `g`, never the
task label or traversal direction.

For each base sequence, test timing factors `0.5`, `1.0`, and `2.0` applied
to its same monotonically increasing 16-point schedule, with reference
duration 240 time units (durations 120, 240, 480). Each matched direction
pair receives exactly the same intervals. Use the same held-out base curves
at every factor.

## Conditions and controls

1. **No-learning diagnostic:** evaluate the untrained current path without
   fitting prototypes. If it has no valid two-class output, report accuracy
   as `N/A`, class representation as empty, and emissions/features separately;
   do not report the absence of classes as zero accuracy or chance.
2. **Fixed-topology learning (primary):** fit the bounded external readout on
   the ordered training examples for 20 fixed epochs, then freeze model,
   topology and prototypes before validation/test scoring.
3. **Matched shared-shuffle control:** for each held-out base curve, apply
   one deterministic shuffle and use that *same shuffled coordinate order*
   for both opposite-label members. The two control rows must have bytewise-
   identical event inputs, including the same class-neutral example ID,
   payloads, and timestamps; only the evaluator-side labels differ. Run the
   same frozen model/readout. This is an information-boundary negative
   control, not a claim that a model should classify contradictory identical
   inputs: deterministic identical predictions are required and yield
   exactly 0.5 accuracy within every pair. Different predictions make the
   protocol invalid and indicate an input/identifier/label leak. This control
   checks point-set shortcuts and label isolation; the ordered-versus-shuffle
   contrast is secondary to the primary paired-order result.
4. **Reversal control:** compare the exact opposite-order pair using the
   inverted directed-winding labels. Report both members' joint correctness
   and whether predicted labels invert. Do not reuse Luna-12G's same-label
   reversal scoring.
5. **Timing sensitivity:** report classification, prediction match/error,
   and queue outcomes at all three timing factors without refitting or
   changing the task label. The 1.0 factor is the primary efficacy test;
   0.5 and 2.0 are secondary diagnostics only.

Validation is an independent split used for reporting diagnostics only:
per-class accuracy, confusion, feature/readout separation, loss, and the
fixed 20-epoch training history may be inspected and reported. The 20 epochs
remain frozen regardless of validation convergence or score. Validation may
not select epochs, seeds, thresholds, model parameters, or a winning
checkpoint. Report validation/test differences with their intervals as a
possible split-generalization limitation; do not retune or rerun. Report all
eight seeds; no test-driven retuning, exclusion, retry, or replacement seed
is permitted.

## Exact current-network configuration

Use one `ExperimentRunner` / `ExperimentConfig` per replication, with the
following settings frozen for every primary and test-control pass:

```text
neuron_model                 = EXCURSION_V1
epochs                       = 20
history_limit                = 20
max_points                   = 16
prediction_capacity          = 16
learning_enabled             = true
reward_mode                  = neutral
reward_delay                 = 0
activation_mode              = event_only
max_classes                  = 2
structural_plasticity        = false
structural_observation       = false
topology_node_count          = 8
topology_initial_edges       = 8
topology_edge_capacity       = 8
topology_fan_in              = 2
topology_fan_out             = 2
queue_capacity               = 128
event_budget                 = 1024 per example
prediction_expiry            = 64 time units
settling_horizon             = 65 time units
eligibility traces           = 128 maximum per node ledger (derived)
eligibility decay constant   = 4 time units
eligibility expiry           = none; ledger destroyed at example reset
```

Initial graph construction is seeded from the network seed, has positive
one-unit edge delays, and must be serialized exactly in each replication
manifest. All temporal conditions for one replication reuse the same frozen
initial graph. No topology changes are permitted. Current `EXCURSION_V1`
defaults stay unchanged; benchmark-specific settings remain local to this
contract.

The current public runner assigns an input neuron by workload position,
`index % node_count`; that assignment is part of this contract, not a routing
change. For each split with `P` base-curve pairs, put one member of every pair
at row `i` and the other at row `i+P`, using the same base-curve order for
every condition. Here `P` is 64, 32, or 128, each divisible by eight, so both
members enter the same seeded input neuron. Use the same row layout for
ordered, reversal, shared-shuffle, no-learning, and all timing-factor passes.
The manifest must record row, pair, and assigned input-neuron identities and
verify their match without consulting labels.

Within a matched pair, use one class-neutral `example_id` for both members;
labels and row ordinals remain evaluator-side metadata and must not appear in
point-event payloads, input IDs, or routing decisions. The current runner
also passes each workload row as `character_index` in classifier boundary
metadata, so pair rows have different boundary indices. This is a permitted
record-identity difference only if the trace/source confirms that it only
delimits classifier records and cannot affect neural input, routing,
features, reward, or prediction. In the shared-shuffle control, point-event
input bytes must be identical, with identical input-neuron, predictor-source,
and destination assignments. Per-example reset must give each member the same graph, weights, selected
input node, and character-local computational state. During training, the
external readout is intentionally updated in fixed workload order, so do not
claim its state is identical across training-pair members. At validation and
test, the readout is frozen and must be identical for both members of each
pair. The persistent E2
input/episode/lineage/output identity high-water counters are permitted to
differ only as bookkeeping; record them and verify that they cannot affect
node selection, routing, features, labels, or predictions. If the runner or
trace cannot establish these equivalences, classify the control as
protocol-invalid and make no efficacy inference; do not alter routing or
reset/reconstruct the network to force equivalence.

Run conditions in this fixed order per replication: untrained no-learning
diagnostic; 20 training epochs; validation; frozen ordered test at timing
factors 0.5, 1.0, and 2.0; then the matched-shuffle test once at the
reference factor 1.0. The reversal comparison is reported from the
corresponding ordered test pairs and is not a separately refitted model. Do
not reorder conditions to avoid resource or identity limits.

## Runner interface review — design only

The current public APIs are `ExperimentRunner.evaluate(workload)` and
`ExperimentRunner.train(workload)`. `evaluate` can evaluate a singleton and
returns aggregate `ExperimentMetrics`, but its internal workload index is
always zero for a singleton. It does not update prototypes. `train` preserves
the runner's network and readout across calls on one instance, but performs
an initial full-workload evaluation, every configured full-workload training
epoch, and a final full-workload evaluation. Its observer is called once per
epoch with aggregate metrics; it is not an example-level completion hook.
`ExperimentRunner.reset()` recreates the network and clears prototypes, so it
must not be called between examples or conditions.

Internally, `_execute` processes a workload in a list comprehension.
`E1EventBudgetExceeded` and other raised errors abort that comprehension,
but an incomplete-settling or returned event-budget-exhausted result does
not: remaining examples are still run. The public metrics expose aggregate
completion, budget exhaustion, and incomplete-settling counts only after the
whole pass. During `train`, `_run_excursion_example` updates the prototype
even when the result reports incomplete settling. Therefore neither public
batch API satisfies the required per-example fail-fast contract for returned
incomplete results.

**Option A — current public APIs only: rejected.** Singleton `evaluate`
cannot select the contract's workload-position input neuron, while
singleton `train` adds before/after executions, runs the configured number
of epochs for that one example, and cannot check status before a training
update. Batch `train` does not stop on returned incomplete results. Capacity
exceptions propagate but do not produce a typed per-example result or
rollback earlier updates in the pass. Adapting workloads or relying on
`TrainingObserver` would change input-node assignment or observe too late.

**Option B — downstream-only adapter: technically possible but not selected.**
At this pinned revision, a subclass could use `_ensure_topology`,
`_run_example(example, index, update=...)`, `_ExampleRun`, and private network
state to preserve indices and inspect results. However, those are unsupported
private interfaces; direct calls bypass `_execute()`'s aggregate metrics and
`last_neurons` refresh, and require custom metric aggregation and private
access to all nodes for identity snapshots. Using only public
`evaluate`/`train` does not solve these limitations. A baseline pin reduces
drift risk but does not make those dependencies supported. This is rejected
in favor of an additive public method rather than a duplicated private
adapter.

**Option C — minimal additive runner interface: selected for owner review;
not implemented or authorized.** Add `ExperimentRunner.execute_example(
example, *, index, update=False)` with explicit workload index and a typed,
immutable `ExampleExecutionResult`. One call must execute exactly one
example, use the existing computation once, preserve the same runner,
network/topology, learned prototypes and identity counters, and return that
example's assigned input node, readout diagnostics, trace/replay digest,
`BoundedExecutionResult`, settling/budget state, reward and all-node identity
snapshots. The existing public `neuron_to_ir2_e2()` can serialize every
neuron's identity high-water values and capacity; the new method must include
one snapshot per network node, not just the selected input neuron.

For `update=True`, the new method must invoke the existing example
computation with readout mutation disabled, then commit exactly one
sum/count prototype update only if execution completed with no pending work,
no exhaustion, and no capacity failure. A failed example must not update the
readout. Do not change the existing `train()` behavior or signatures.
Explicitly report a typed failure for returned incomplete/budget status and
known capacity exceptions, including `E1EventBudgetExceeded`, queue,
prediction, eligibility, and character-buffer exhaustion. The runtime's
currently untyped event-budget `RuntimeError` must become a dedicated
`RuntimeEventBudgetExceeded` subclass so the API can classify it without
message parsing. Preserve the specific failure kind. Do not blanket-catch
exceptions: invalid input and
unexpected runtime errors remain visible and stop orchestration. If an error
leaves character-local state active, discard transient runtime state and
reset only per-character neuron state while retaining the runner, topology,
prototypes, and identity high-water counters before returning/raising. Never
call `ExperimentRunner.reset()` for this cleanup.

The Luna-65 adapter calls this method once per example in the contract's
fixed order and original row index, checks the result before requesting the
next example, and marks the whole replication invalid on any failure. It
streams per-example records into predeclared deterministic aggregates; it
does not use or emulate `TrainingObserver`/`TrainingResult` callbacks.
`ExperimentRunner.evaluate()` and `.train()` remain unchanged for existing
callers. The new method is a separate public experimental execution surface
and does not silently alter existing aggregation semantics.

The minimal proposed source scope is an additive result type and method in
`tpcn/experiments.py`, the dedicated runtime budget exception in
`tpcn/experiment_excursion_runtime.py`, and focused tests. Obtain identity
snapshots using the existing public serializer in `tpcn/ir2.py`; no serializer
change is proposed. No neural
computation, event order, reward formula, topology, seed, workload feature,
or task control may change. Validate successful per-example trace/reward
equivalence to the existing path at the same workload index; prototype
update parity on successful runs; no update on returned or raised failure;
one-call fail-fast; exact row-index routing; same-runner state continuity;
identity persistence/snapshots; and repeatable replay. New public API
compatibility requires its own review before benchmark execution.

Keep interface unit tests separate from capacity fixtures. The focused
`tests/test_luna65_execute_example.py` unit tests may use at most 16
hand-authored, two-point `SyntheticExample` calls with fixed artificial label
tokens solely to verify successful prototype sum/count commits and failed-
call no-update behavior. This unit-test lane has no task labels, Spiral data,
split data, accuracy/efficacy scoring, or benchmark training. It must not call
`ExperimentRunner.train()`; configure neutral reward so the artificial label
cannot enter reward, eligibility, or utility. Its assertions are API
compatibility tests, not benchmark evidence.

These unit tests also inject predeclared expected typed failures and
unexpected exceptions. An expected incomplete/capacity failure must return
the typed result; an unexpected exception must propagate after cleanup. Both
stop orchestration before a subsequent API call and invalidate the affected
replication; neither retries. A predeclared negative test may continue to the
next independent test scenario only after asserting the exact failure kind,
cleanup, preserved counters, and no readout update. Stop the test process at
the first failed assertion, unexpected exception, unplanned capacity failure,
or resource-limit violation. Each test process is bounded to 2 minutes,
2 CPU-minutes, 256 MiB, and 1 MiB of output.

| Review dimension | A — existing public APIs | B — downstream adapter | C — additive public API |
|---|---|---|---|
| Required changes | None; only workload orchestration. | Adapter/subclass calls private initialization, per-example, and network state. | Add `execute_example`, immutable result, and typed runtime-budget error; focused tests. |
| Compatibility risk | No API change, but singleton index and explicit pre/post evaluations alter the required pass ordering and cannot satisfy this contract. | High for the direct-call adapter: private methods/results/state are not supported extension points; pinning limits but does not remove drift. | Comparatively low, conditional on implementation and parity tests; existing `evaluate()`/`train()` remain unchanged. |
| Determinism and state continuity | Existing batch order is deterministic, but singleton index is always zero; a runner preserves state only if the same instance is reused. | Can preserve row index/order and reuse one runner/network if carefully implemented; dependent on pinned internals. | Explicit original index and one computation call; retain runner/network/topology/readout and E2 counters. |
| Fail-fast behavior | Raised errors abort a pass, but returned incomplete status is aggregated after later examples already ran. | Adapter can stop after each direct private call, but must itself classify failures and clean up partial state. | One-example result makes returned failures observable before another call; known capacity errors are typed, unexpected errors propagate. |
| Capacity accounting | Aggregate status; no supported all-node identity snapshot. Does not establish 2,048-counter sufficiency. | Requires private all-node network access; public serializer can serialize supplied neurons but not discover them. | Return per-node high-water/capacity snapshots via public serializer; full-replication sufficiency still needs a separate bound. |
| Tests and provenance | Existing behavior can be regression-tested but cannot pass the fail-fast acceptance check. | Requires adapter parity, call-stop, cleanup, index, snapshot, and replay tests tied to exact private-API revision. | Requires per-example parity/failure/update/cleanup/index/snapshot/replay tests tied to exact API, config, seed and reviewed revision. |

For exact parity with current `train()` pass count, the proposed adapter
executes one training-set evaluation before learning, 20 update passes, and
one training-set evaluation after learning, each one example at a time and
in the same stable order. These evaluation passes are read-only. This retains
the existing 22 training-set passes while adding fail-fast checks and
preserving the explicit no-learning, validation, ordered-test, and
shared-shuffle conditions below.

`reward_mode=neutral` is mandatory in training, validation, no-learning and
test conditions. In the present runner, the `EXCURSION_V1` evaluation callback
can derive reward from `example.label` and send a reward signal to an
eligibility ledger unless reward mode is neutral. Neutral mode leaves the
supervised external readout as the only label-conditioned update and keeps
test labels out of reward, eligibility and utility computation. The scorer
may read a sealed prediction and its label only after that example's runtime
has been destroyed.

Any unapproved change to feature construction, task-label handling, reward,
readout, topology, runtime, or model semantics blocks execution and returns
to Luna-0.

## Predeclared measurements and classifications

Primary task measurements:

- Balanced accuracy, overall and per directed label; confusion matrix,
  represented classes, readout centroid/count, margin and confidence.
- Per-curve matched-pair joint accuracy: both exact-order members correctly
  classified; and direction discrimination: predicted labels differ for the
  two opposite-order members.
- Shared-shuffle paired accuracy and pairwise output identity.
- Reversal-inversion accuracy and whether predictions invert.
- Accuracy and paired differences by timing factor. Report seed-level
  results and a 95% paired, seed-and-base-curve-cluster bootstrap interval.
- Frozen replay digest over input streams, exact topology, event trace,
  readout state and predictions.

Predeclared efficacy interpretation: at reference timing 1.0, an above-chance
result requires the 95% cluster-bootstrap lower bound for held-out balanced
accuracy to exceed 0.50. Evidence of order dependence additionally requires
the reference-timing ordered-versus-shared-shuffle balanced-accuracy point
difference of at least 0.05 and its 95% paired interval to exclude zero. The
`0.05` value is a proposed minimum
practically interesting difference, not an empirically established property
of this task; the owner must explicitly accept or replace it before
execution. Use 10,000 deterministic hierarchical paired-bootstrap
replicates: resample the eight seed clusters, then base-curve IDs within each
selected seed, retaining both members of each pair and using the same
sampled seed/curve indices for ordered and shared-shuffle comparisons; report
percentile 2.5th and 97.5th bounds. Bootstrap RNG seed is `65999`. The design
does not claim a power guarantee at this effect size; show seed-level
outcomes and interval width. No optional stopping, post-result threshold
changes, or new seeds. A failed threshold is a valid negative/inconclusive
result.

Timing-factor results are predeclared secondary diagnostics only. The
twofold-shorter/base/twofold-longer schedules test sensitivity to absolute
event intervals while preserving coordinates, order, and pair labels. No
direction or invariance is assumed; report each factor and paired contrasts
with intervals, do not select a favorable factor, and do not use timing
results to alter the primary verdict or tune the model.

For each stream, record processed events, input/excursion emissions,
intermediate/destination activations, prediction matches/unmatched/errors/
expiry, peak and final queue occupancy, completion and budget status,
readout reward (neutral zero), energy and the named uncalibrated event-based
proxy components, connection count/capacity, edge list, fan-in/out
distributions, deterministic replay identity, and—only when already
observable—per-edge traffic/use. Distinguish admissions from matches.

The current public experiment metrics expose aggregate emissions/activations,
prediction match/unmatched/expiry and error counts, queue occupancy and
pending events, edge list/capacity/fan utilization, event-based energy
components, and replay digests. Prediction-admission totals, per-example
eligibility creation/expiry details, edge lifecycle/use counters on this
runner path, and per-layer source/intermediate/destination activation
breakdowns are not uniformly exposed by the existing public metrics. The
current eligibility ledger has no time-based expiry configured in this path;
it decays and is destroyed at the per-example reset. Report that lifecycle
policy and mark per-trace expiry counts `unavailable`, not zero. Mark other
unsupported fields `unavailable` unless already present in the exact
runner/trace. They may be added only as independently reviewed,
downstream-only bounded instrumentation that proves on/off computational
equality. Do not alter computation to satisfy a reporting field.

Failure classes:

- **Protocol invalid:** split/pair overlap, label leak, replay mismatch,
  unapproved behavior, invalid output/manifest. Stop and report; no efficacy
  inference.
- **Resource/technical failure:** queue/event cap, incomplete settling,
  output cap, or external supervisor termination. Report the first exact
  cause; no retries under this contract.
- **Valid no-learning/negative result:** complete deterministic run with no
  represented classes, no above-chance accuracy, no matched-pair
  discrimination, or no order advantage. Preserve the result; do not tune.
- **Inconclusive:** confidence intervals include the preregistered boundary
  or seed-level outcomes materially disagree. Do not expand the budget.

## Resource budget and execution authority

No benchmark command is executable at the design stage. After independent
review and exact owner authorization, Luna-65 must implement and review this
contract's CLI before invoking it. The intended single invocation is:

```text
python run_spiral_resumption.py --contract workflow/docs/luna/LUNA_65_SPIRAL_RESUMPTION.md --seeds 65001,65002,65003,65004,65005,65006,65007,65008 --output artifacts/spiral-resumption-luna65
```

The runner does not exist at the baseline revision; this command is a frozen
future CLI contract, not a command run or validated here.

| Resource | Proposed ceiling | How counted |
|---|---:|---|
| Replications | 8, exactly the listed seeds | One sequential pass; zero retries |
| Sequence executions | 4,160/replication; 33,280 total (128 training × 22 passes, 64 validation, 768 ordered tests, 256 shared-shuffle tests at reference timing, 256 no-learning tests) | No generated sample may cross a split; reversal members are included in each paired set |
| Workload event bound | 1,024 processed events/example; 4,259,840/replication and 34,078,720 total; queue capacity 128 | Runtime-enforced; any exhaustion is a failed/incomplete replicate |
| CPU | 15 CPU-minutes/replication; 120 CPU-minutes total | Proposed monitor/enforcer target, not qualified here |
| Wall time | 20 minutes/replication; 160 minutes total, sequential | Proposed external watchdog target; no unbounded rerun |
| Memory | 1 GiB process high-water | Proposed monitor/enforcer target, not qualified here |
| Artifacts | 8 MiB/replication; 64 MiB aggregate, including manifests and traces | Runner must reject output growth; exact enforcement is unqualified |

In addition to the per-character event budget of 1,024, the current runner
constructs each EXCURSION_V1 neuron with `E1Config.event_budget=2,048`.
Input, episode, lineage, and output-event identity high-water counters are
bounded by that per-neuron setting and persist across character reset; the
reset clears character-local computation but deliberately does not reuse
those identities. Do not reset identity counters, enlarge their capacity,
reconstruct the network between conditions, or infer that the aggregate
per-character event cap guarantees identity capacity for the full
replication. Record counter high-water values and stop on the first identity
capacity failure. Such exhaustion is a technical failure, not a negative
efficacy outcome.

The four E2 identity counters have distinct allocation sites: input identity
is allocated for an unassigned input event; episode identity for ordinary
admission, multi-excursion admission, and multi-to-ordinary transition;
lineage identity for ordinary admission and a new multi lineage; output-event
identity for each ordinary or multi emission. Runtime-admitted external
point events carry explicit IDs, so those points do not consume the neuron's
auto-generated input identity in the current path. `generation_token` and
per-character processed-event counters reset at character boundaries; the
four identity counters do not.

**Capacity conclusion: not analytically sufficient.** The 2,048 identity
ceiling is per neuron and per identity counter, while the proposed complete
replication allows 4,259,840 processed events across 4,160 example runs.
Even a coarse worst-case per-neuron allocation bound derived from total
processed events exceeds 2,048. Workload position distributes input nodes,
but multi-hop routing, neuron activation patterns, and counter-specific
allocations do not have a proved tighter per-replication upper bound.
Historical averages, typical-fixture consumption, or the fact that a single
example is capped at 1,024 do not prove capacity sufficiency across persistent
resets. No sufficiency claim is made.

### Separately authorized deterministic interface/capacity fixture protocol

This is a proposal for a separately owner-authorized capacity fixture check
after the interface addition and API unit tests, not an authorization to
implement or run either. Capacity fixtures use hand-authored scalar event
inputs only, `update=False`, and neutral reward. The API's required
`SyntheticExample.label` may contain only a fixed artificial evaluator-side
token; it is not a task label and must not enter the event/reward path.
Capacity fixtures perform no readout updates, training, scoring, or efficacy
measurement.

1. In a separately bounded direct-neuron unit-test lane, exercise all four
   identity allocation paths with the production E2 cap of 2,048; retain the
   same neuron over reset boundaries; verify exact high-water values,
   persistence, and explicit failure on the first over-capacity allocation.
   Exercise fallback input-ID allocation through the documented direct
   contribution API without an explicit event ID. Separately verify
   per-character counters reset. Bound the lane to exactly 2,049 allocation
   attempts for each of the four counters (8,196 attempts total). The
   expected rejection on attempt 2,049 is asserted as a negative case and
   does not stop other predeclared counter tests.
2. Use the existing eight-node fixed-topology construction at each of the
   eight declared network seeds and exactly 16 frozen hand-authored
   high-activation character fixtures per seed. Each fixture has at most 16
   external inputs, queue capacity 128, and at most 1,024 processed events.
   This caps the network-level check at 128 character executions and 131,072
   processed events (and at most 2,048 external inputs). Exactly 16 is the
   frozen schedule absent an earlier failure: preserve the same network
   across each seed's 16 character resets, stop immediately on unexpected
   capacity exhaustion, and report all unexecuted fixtures. Do not repeat or
   replace fixtures. Record exact per-neuron counters. Runtime-admitted inputs
   have explicit IDs, so verify the fallback input-identity counter remains
   unchanged; fallback allocation is covered only by item 1. This lane
   covers only network-level executions, not the separate direct-counter
   allocation attempts.
3. In the separately bounded API unit-test lane, inject one returned
   incomplete result and each expected typed event, identity, queue,
   prediction, eligibility, and character-buffer capacity failure. Verify
   each becomes an explicit typed result and no next API call occurs. Also
   inject an unexpected exception and verify it propagates after cleanup and
   stops orchestration. Verify successful consecutive calls retain the same
   runner/network/topology, honor the explicit row index, and reproduce
   deterministic traces and neutral reward behavior. Readout-update checks
   belong only to the artificial-label API unit tests, not the capacity
   fixtures.
4. Run the two future test modules as separate, separately authorized
   invocations:

   ```text
   pytest -q tests/test_luna65_execute_example.py
   pytest -q tests/test_luna65_capacity_fixture.py
   ```

   Each process has proposed ceilings of 2 minutes wall time, 2 CPU-minutes,
   256 MiB process memory, 1 MiB artifacts, and zero retries. These resource
   limits are targets, not demonstrated enforcement; the test host must
   explicitly enforce termination before the fixture authorization. Expected
   failures explicitly declared in negative tests count as passing only after exact assertions;
   stop at the first assertion failure, unexpected exception/capacity
   failure, or limit violation. Any network-level capacity exhaustion stops
   that network check immediately. Record revision, configuration, seed,
   test output, exact counter high-water snapshots, and file hashes.

Passing these bounded API tests and capacity fixtures can validate failure
detection, determinism, state continuity, and the tested fixtures; it cannot establish
full-replication identity sufficiency unless the fixture is accompanied by a
separately reviewed proof that it bounds every allowed protocol execution.
If exhaustion occurs, or no such bound is proven, execution stays blocked.
No counter reset, capacity increase, or network reconstruction is allowed
without separate review and owner authorization.

The runtime event/queue bounds are enforced by the current software reference.
The CPU, wall, memory and artifact ceilings are only proposed budgets until an
owner-approved host supervisor has demonstrated their enforcement and
termination behavior. Monitoring is not enforcement. No Hyper-V supervisor is
a prerequisite in this contract. Do not alter existing repository execution
restrictions or claim this budget is enforced without evidence. If an
acceptable controller is unavailable, execution remains blocked.

## Files, controls, and acceptance gate

If owner-authorized, Luna-65 owns only:

- `run_spiral_resumption.py`
- `tpcn/spiral_resumption.py` (external-workload generation and split manifest
  only; no core change)
- focused tests and frozen outputs under `artifacts/spiral-resumption-luna65/`
- a completed handoff under `workflow/handoffs/`

Luna-65 must first prove paired coordinate/digest identity, exact class and
nuisance balance, split disjointness, chronology, label isolation,
same-seed replay, and the assigned-input/equivalent-computation conditions
on fixtures. It must inspect completion/capacity status for each example and
stop at the first incomplete or exhausted example, rejecting the entire
affected replication for efficacy. Existing `ExperimentRunner.evaluate()`
and `.train()` aggregate whole workloads and cannot provide that per-example
fail-fast boundary. The selected plan therefore requires the separately
reviewed additive `execute_example()` API and a typed runtime event-budget failure; their
implementation and focused
tests are a prerequisite, not an already available capability. Partial
prototype updates from a failed replication must never be scored as valid
efficacy. No retry is permitted.

The bounded fixture protocol can test the proposed API and identify
counter-specific exhaustion on its fixtures; it cannot by itself prove
full-replication identity sufficiency. That uncertainty remains an execution
blocker unless a separately reviewed bound proves sufficiency. A detected
exhaustion is a technical failure, not evidence for or against the scientific
hypothesis.

Only after the additive API, focused interface tests, an acceptable
full-replication capacity argument, same-seed replay on fixtures,
independent Luna-0 review, owner authorization, and qualified resource
enforcement pass may the CLI be considered for a distinct exact execution
authorization. Do not overwrite any historical files.

Before execution, Luna-0 must independently accept the contract and confirm
that the CLI, metrics, supervisor, artifact policy, current baseline, and
owner authorization agree. After execution, a different Luna-0 review must
classify every result and decide whether any separately authorized next
experiment is justified. This contract authorizes neither execution nor
structural plasticity.
