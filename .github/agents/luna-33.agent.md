---
name: Luna-33 ACP-0007 Four-Class EXCURSION_V1 Efficacy
description: Run a bounded, matched four-class EXCURSION_V1 experiment testing task efficacy of ACP-0007 local temporal growth; no core or architecture change.
---

# Luna-33 — ACP-0007 Four-Class EXCURSION_V1 Efficacy

## Authorization and baseline

```text
Luna-0 -> Luna-33 -> Luna-0
```

Luna-33 is **AUTHORIZED / NOT EXECUTED** by
`workflow/handoffs/luna-0-post-luna32-acp0007-four-class-efficacy-decision-20261004.md`.
Code baseline: `cc66e6a4affb044bf726d92510bcfd214c1f698f` (Luna-32 closed).
Before execution, verify clean `main`, `HEAD == origin/main`, and that the
latest authorization publication contains this exact dispatch and decision.
The code under test must match the stated baseline; stop and return to Luna-0
if relevant code, ACP-0007, or the authorized design differs.

Classification: **EXPERIMENT + OBSERVATION + FOCUSED VERIFICATION**.
This experiment is within accepted ACP-0007, does not amend Architecture
Contract 1.2 or A01-A15, and must not self-close or authorize a successor.

## Question and falsifiable hypothesis

**H1:** In the declared four-class synthetic temporal-spiral reference setup,
growth-only ACP-0007 `e2_local_temporal` training improves canonical held-out
classification accuracy over matched fixed topology (C > A), and the
improvement depends on the preserved training order (C > D).

The hypothesis is **not supported** if either paired mean accuracy contrast
`C - A` or `C - D` is non-positive after valid execution. It is **supported
only within this declared setup** if both mean contrasts are positive, each
contrast is positive in at least four of five paired seeds, and the
mechanism-engagement and non-interference gates below pass. Positive means
that fail the seed-consistency or engagement gates are **INCONCLUSIVE**, not
support. Five seeds are exploratory evidence, not a population guarantee.

## Conditions

For each seed 0–4, construct one deterministic, disjoint train/evaluation
dataset pair, and run four fresh, matched `ExperimentRunner` instances:

| Condition | Training data | Observation | Mutation |
|---|---|---|---|
| A | Canonical point order | Off | Off; fixed topology |
| B | Canonical point order | On | Off; observation-only |
| C | Canonical point order | On | On; `e2_local_temporal` |
| D | Same samples as C, each training character's point order shuffled | On | On; `e2_local_temporal` |

All four conditions use the same canonical, held-out evaluation workload.
For D, shuffle only the coordinate pairs within each training example and
assign them to the original ordered timestamp slots. This destroys the
coordinate-to-time order while preserving each example's coordinate
multiset, timestamp vector, duration, point count, sample ID, and other point
metadata. Labels remain external readout
supervision/evaluation and are never passed to structural evidence. Use
`reward_mode="neutral"` so correctness cannot change neural reward. No
historical `TANH_LEGACY` control, Luna-12L artifact, or historical efficacy
result may be reused.

## Frozen reference design

- Use `make_spiral_dataset(examples_per_class=16, train_seed=12007 + seed,
  evaluation_seed=22017 + seed, config=SpiralConfig())`: four declared
  classes, 64 training and 64 held-out examples per seed. This is one
  bounded synthetic reference setup, not real-data evidence and not the
  historical Luna-12L scale.
- Independently shuffle the generated training and evaluation example tuples
  with `random.Random(330000 + seed)` and `random.Random(330001 + seed)`.
  These orders are shared by A–D for each seed and avoid the generator's
  class-grouped index schedule. For D, iterate the shuffled training order,
  draw one `getrandbits(32)` coordinate-shuffle seed per example from
  `random.Random(330002 + seed)`. Shuffle only that example's `(x, y)` pairs
  with a fresh `random.Random(point_seed)`. Rebuild each point at its original
  timestamp slot, preserving `pen_state` and `stroke_boundary`, and retain
  the original sample ID and external label. Verify D preserves the
  coordinate multiset, ordered timestamp vector, duration, and point count.
  Do not use a transform that reassigns or regularizes timestamps.
- Use `topology_node_count=8`, `topology_initial_edges=8`,
  `topology_edge_capacity=16`, `topology_fan_in=2`, and
  `topology_fan_out=2`. This seeded public initializer supplies the same
  initial graph to A–D within each seed and leaves bounded growth headroom.
  Eight nodes are a newly declared experimental reference, not a historical
  scale or invariant.
- Declare the static directed observation fabric as the eight-node ring:
  `neuron-i: (neuron-(i+1 mod 8),)` for every `i`. Use neighborhood and
  reverse-observer limits 2/2. The fabric is fixed for every condition and
  seed; it is not recomputed from labels, candidate outcomes, or the mutable
  topology.
- Shared runner settings: `neuron_model="EXCURSION_V1"`,
  `structural_policy="e2_local_temporal"`, `epochs=1`, `max_points=20`,
  `max_classes=4`, `learning_enabled=True`, `activation_mode="event_only"`,
  `reward_mode="neutral"`, `queue_capacity=128`, `event_budget=1024`,
  `settling_horizon=4.0`, `prediction_expiry=4.0`,
  `structural_association_window=4.0`,
  `structural_history_capacity=8`, `structural_candidate_capacity=4`,
  `structural_maximum_score=3`, `structural_growth_delay=0.4`,
  `structural_growth_attempt_budget=16`, `max_growth_per_epoch=1`, and
  `mutation_history_limit=64`. Keep all other `ExperimentConfig` options
  identical across conditions and declare them in the artifact config.
- A has observation and plasticity disabled. B/C/D have observation enabled;
  C/D have plasticity enabled. A–D retain the same `e2_local_temporal` policy
  identifier; the policy has no effect when mutation is disabled.
- Parameters use the Luna-28 tested bounded observation values where
  applicable. The ring's actual neighborhood/reverse-observer degree is 1;
  its declared limits remain finite at 2.

Do not tune this profile based on accuracy, candidate counts, or seed outcomes.
If a required metric cannot be exposed by existing public APIs, stop and
return the specific gap to Luna-0; do not add core APIs or use private
topology/runtime injection.

## Public interfaces and evidence gates

Use `ExperimentConfig`, `ExperimentRunner.train()`,
`ExperimentRunner.evaluate()`, `TrainingResult.before`,
`TrainingResult.history`, `TrainingResult.evaluation`,
`EvaluationResult.event_trace`, `ExperimentMetrics.structural_decisions`,
`ExperimentRunner.topology`, and `ExperimentRunner.prototypes`.

For each seed/condition:

1. Preserve the pre-training topology from `TrainingResult.before.metrics`.
   A–D must have identical initial topology edges and delays for that seed.
2. Capture the trained topology, every bounded structural decision and
   rejection reason, candidate/observation/growth counters, resource
   utilization and all five-seed results. Do not silently drop failed,
   budget-exhausted, incomplete-settling, or no-growth seeds.
3. Evaluate the same canonical held-out set with `update=False`. Confirm
   evaluation did not mutate topology or prototypes.
4. Verify observation non-interference: for each seed, A and B have identical
   canonical neural/task results, including predictions, event trace,
   topology, prototypes, execution counters, prediction metrics, and activity
   proxies; observer-owned evidence counters may differ.
5. For C, derive admitted edges from public structural-decision
   `topology_before`/`topology_after` snapshots. A grown edge counts as
   **later used** only if a held-out canonical EXCURSION event's public
   `route_path` contains that exact directed edge. A topology edge's mere
   existence is not route-use evidence. Require at least one admitted edge
   later used in at least four of five C seeds for the support gate.
6. Record training candidate opportunities and realized observations,
   candidates, attempts, admissions, rejections, saturation, and budget
   exhaustion. A–D receive equal sample counts, training effort, structural
   bounds and candidate capacity; do not claim equal *realized* candidate
   exposure when D changes temporal order.

If the A/B non-interference gate fails, stop the efficacy interpretation and
return the regression to Luna-0. If the C route-use gate or valid-execution
gate fails, classify the efficacy result **INCONCLUSIVE**; do not repair the
mechanism or retry with tuned settings under this authorization.

## Measurements and decision rules

Primary endpoint: canonical held-out overall accuracy, paired by seed.
Report per-class accuracy, confusion, represented/missing classes,
prototype counts, margins, and every seed rather than only an aggregate.

Secondary diagnostics: held-out prediction loss and prediction/error/credit
counters; processed events, excursions/activations, maximum route depth,
edge-transfer proxy, other activity-cost proxies and units, final topology,
edge/fan-in/out utilization, candidate evidence/rejection counts, admissions,
and exact grown-edge route use. Activity/energy values are uncalibrated model
proxies, never physical joules. Do not claim prediction or resource benefit
from topology movement, accuracy, event counts, or proxy values alone.

Apply the joint support rule in “Question and falsifiable hypothesis.” If
either paired mean `C-A` or `C-D` is non-positive, report the joint
task-efficacy hypothesis **NOT SUPPORTED** in this setup, with the individual
contrasts shown. If both means are positive but any four-of-five,
route-engagement, non-interference, or valid-execution gate fails, report
**INCONCLUSIVE**. There is no pre-existing absolute accuracy threshold.

## Owned files and exclusions

Luna-33 may add/change only:

```text
run_luna33_acp0007_four_class_efficacy.py
tests/test_luna33_acp0007_four_class_efficacy.py
artifacts/acp0007-luna33-four-class-efficacy/config.json
artifacts/acp0007-luna33-four-class-efficacy/results.json
artifacts/acp0007-luna33-four-class-efficacy/summary.json
workflow/handoffs/luna-33-acp0007-four-class-efficacy-20261004.md
```

Do not change core/runtime/configuration APIs, accepted ACP-0007, Architecture
Contract, acceptance criteria, workflow/changelog governance, historical
Luna-12L or spiral controls/artifacts, or unrelated tests. No pruning, N3,
edge-parameter learning, readout redesign, TPCV work, hardware/GPU/FPGA/FPAA
claims, or architecture promotion is authorized. If any owned-file list
expansion or incompatible API change appears necessary, stop and return to
Luna-0.

## Verification and completion

Add focused tests for exact dataset transforms/splits, label-neutral D
coordinate-to-time permutation and timestamp preservation, all four config
identities and matched initial topology
provenance, public metric extraction, no evaluation mutation, exact edge
route-use extraction, deterministic artifact serialization, and retention of
negative/failed seeds. Run:

```text
python -m pytest tests/test_luna33_acp0007_four_class_efficacy.py -q
python run_luna33_acp0007_four_class_efficacy.py --output-dir artifacts/acp0007-luna33-four-class-efficacy
python -m pytest -q
python -m compileall -q tpcn tests run_luna33_acp0007_four_class_efficacy.py
git diff --check
```

Record exact revision, Python/environment, commands, seeds, configuration,
dataset/split digests, full per-seed results, failures, and verdict in the
completion handoff. Report clauses A01-A08, A10-A11, A14-A15 as applicable;
state that the work is an ACP-0007 experiment, not architecture promotion.
Keep task efficacy distinct from prediction benefit, resource benefit, and
hardware equivalence; the latter three remain **NOT ESTABLISHED** absent
separate evidence. Return to Luna-0 for independent review. Commit/push and
close only under the user's explicit instruction or a later bounded
authorization; this dispatch alone does not authorize self-closure.
