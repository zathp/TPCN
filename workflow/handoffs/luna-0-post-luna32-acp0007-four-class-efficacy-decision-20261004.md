# Luna-0 governance decision — post-Luna-32 ACP-0007 four-class efficacy

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Post-Luna-32 ACP-0007 four-class efficacy authorization"
  task_id: "luna-0-post-luna32-acp0007-four-class-efficacy-decision-20261004"
  component: "Scientific feasibility and bounded Luna-33 dispatch"
  status: "complete-authorization-not-executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "cc66e6a4affb044bf726d92510bcfd214c1f698f"
  result_revision: "34d286cc53dd8c80d00a660b00f516f900c3d4db"
  dependencies:
    - "Luna-32 closed and independently verified"
    - "Accepted ACP-0007"
    - "Public ExperimentRunner and EXCURSION_V1 runtime observables"
  owner: "Luna-0 within the bounded experimental-dispatch authority"
  classification: ["OBSERVATION", "VERIFICATION", "GOVERNANCE"]
  hypothesis: "Public ACP-0007 interfaces are sufficient to compare matched fixed, observation-only, temporal-growth, and temporal-order-destroyed EXCURSION_V1 four-class conditions and measure later use of admitted edges."
  counter_hypothesis: "The required matched initial topology, structural decisions, held-out metrics, or exact later route use requires private setup or new runtime semantics."
  architecture_invariants_touched: []
  preserves: ["Architecture Contract 1.2 / A01-A15", "accepted ACP-0007", "historical Luna-12L NOT SUPPORTED result and frozen artifacts"]
  architecture_change: false
  proposal: null
  tests_passing:
    - "Full baseline suite: 908 passed, 0 failed, 1 CUDA-unavailable skip; 909 collected."
    - "Public API/source feasibility audit: sufficient; no private topology injection or core/API change required."
  tests_failed: []
  tests_not_run:
    - "Luna-33 efficacy experiment and all outcome-bearing previews: not run by design."
  assumptions:
    - "The seeded public topology initializer is deterministic from matched ExperimentConfig inputs."
    - "Five paired seeds are exploratory evidence and not a population guarantee."
  unresolved:
    - "Whether the predeclared profile naturally engages growth and later held-out edge use is an experimental outcome, not established by this authorization."
  recommended_next_agent: ["Luna-33 after this dispatch is published", "Luna-0 for independent review"]
```

## Starting state and scientific boundary

The decision began at clean synchronized `main`,
`HEAD == origin/main == cc66e6a4affb044bf726d92510bcfd214c1f698f`
(`docs: close Luna-32 historical compatibility`). The full baseline suite was
independently rerun: **908 passed, 0 failed, 1 skipped; 909 collected**. The
skip is the CUDA-dependent visualization test because CUDA is unavailable.

Luna-32 is **CLOSED / INDEPENDENTLY VERIFIED** for historical model-explicit
compatibility only. The corrected historical Luna-12L result remains
**NOT SUPPORTED / UNCHANGED**; its artifact and handoffs remain frozen. The
explicit-TANH compatibility run is not the same experiment as the retained
artifact.

Current scientific status is preserved:

| Claim | Status before Luna-33 |
|---|---|
| EXCURSION_V1 event/runtime mechanism | **ESTABLISHED** |
| Bounded local structural-growth mechanism | **ESTABLISHED IN TESTED MECHANISM FIXTURE** |
| ACP-0007 task efficacy / four-class efficacy | **NOT ESTABLISHED** |
| Prediction benefit | **NOT ESTABLISHED** |
| Resource benefit | **NOT ESTABLISHED** |
| Hardware equivalence | **NOT ESTABLISHED** |
| E2 pruning / ACP-0002 N3 | **NOT AUTHORIZED** |

This decision authorizes one new, separate efficacy experiment; it reports no
Luna-33 result and does not alter those statuses.

## Feasibility audit

**OBSERVED:** Public `ExperimentConfig` can select `EXCURSION_V1`, explicitly
enable ACP-0007 observation and growth, declare every node's static bounded
neighborhood, set the finite edge/fan-in/fan-out/queue/event/growth limits,
and set `topology_node_count` and `topology_initial_edges`. Public topology
initialization derives its initial edges deterministically from the shared
configuration seed and node/capacity settings. Therefore A–D can start with
identical per-seed topology without private graph injection; the public
`TrainingResult.before.metrics.topology_edges` records that starting graph.

**OBSERVED:** `ExperimentRunner.train()` supplies training metrics and before/
after evaluations; `evaluate()` uses `update=False`. Public metrics expose
bounded structural decisions, per-character before/after topology snapshots,
candidate and observation counts, growth attempts/admissions/rejections,
execution status, topology utilization, task/prediction metrics, and activity
proxies. The runner exposes the final topology and readout prototypes.

**OBSERVED:** `EvaluationResult.event_trace` retains runtime route context,
including exact route paths. A later held-out EXCURSION event can therefore
be checked for traversal of an exact edge shown as newly admitted by a
structural decision. This is downstream measurement; no route trace is fed
to structural learning.

**INFERRED:** Existing APIs suffice for a matched fixed / observation-only /
growth / coordinate-to-time-order-destroyed efficacy comparison and for exact
grown-edge use accounting. No production change, private topology injection,
or ACP amendment is needed. Realized candidate exposure and growth are not
guaranteed; Luna-33 must report them and may conclude **INCONCLUSIVE**.

## Bounded Luna-33 design and hypothesis

The dispatch is `.github/agents/luna-33.agent.md`. Luna-33 tests this joint,
falsifiable hypothesis:

> In one declared four-class synthetic temporal-spiral reference setup,
> growth-only ACP-0007 `e2_local_temporal` training improves canonical
> held-out accuracy over matched fixed topology (C > A), and that improvement
> depends on preserved training point order (C > D).

Conditions, paired per seed:

- **A:** canonical training order, fixed topology, structural observation off.
- **B:** canonical training order, observation on, mutation off.
- **C:** canonical training order, ACP-0007 `e2_local_temporal` growth on.
- **D:** same growth configuration and training sample set as C, but each
  training character's coordinate pairs are shuffled among the original
  ordered timestamp slots; held-out evaluation remains canonical. This keeps
  each example's coordinate multiset, timestamp vector, duration, point count
  and non-coordinate point metadata intact while destroying the mapping from
  coordinate to temporal position.

Use `SpiralConfig()` and `make_spiral_dataset` with 16 examples per class
(64 training, 64 evaluation), seeds 0–4, disjoint generated split seeds
`12007 + seed` and `22017 + seed`. Apply fixed, label-order-independent
training/evaluation permutations from `330000 + seed` and `330001 + seed`.
For D, draw one per-example coordinate-shuffle seed from
`random.Random(330002 + seed)` in the shuffled training order. Shuffle only
the example's `(x, y)` pairs and put them into the original ordered timestamp
slots; preserve each slot's other point metadata, the sample ID and external
label. Verify the coordinate multiset, ordered timestamp vector, duration and
point count remain identical. Do not reassign or regularize timestamps.

The one bounded reference uses eight nodes, eight seeded initial edges, edge
capacity 16, fan-in/out 2, and a fixed one-successor directed ring observation
neighborhood with 2/2 declared neighborhood/reverse-observer limits. These
are experimental settings, not architecture invariants, historical
Luna-12L scales, or a claim that any particular motif is useful. A–D share
all runner settings, hard resource limits, split, seeds, and per-seed initial
topology; only the authorized observation/mutation switches and D training
point order differ.

ACP-0007/Luna-28 tested bounds are retained where applicable: association
window 4.0, history 8, candidate capacity 4, maximum score 3, growth delay
0.4, growth-attempt budget 16, queue 128, event budget 1024. The complete
settings and deterministic ordering are frozen in the dispatch.

## Predeclared outcomes

Primary endpoint: canonical held-out accuracy, paired by seed. Report all
per-seed and per-class results. Secondary outputs include prediction loss,
prediction/error/credit counters, processed events, excursions, route depth,
edge-transfer and other uncalibrated activity-cost proxies, final topology,
utilization, candidate exposure, admissions/rejections, and exact held-out
route use of newly admitted edges.

The joint hypothesis is **SUPPORTED ONLY IN THIS DECLARED SETUP** if:

1. A/B observation non-interference passes for all five seeds on canonical
   predictions, event traces, topology, prototypes, execution/task/prediction
   outputs and proxy counters (observer-owned evidence may differ).
2. At least four of five C runs admit an edge that is later traversed by a
   canonical held-out EXCURSION route, as shown by the exact public route path.
3. Both paired mean accuracy contrasts, C–A and C–D, are positive, and each
   contrast is positive in at least four of five seeds.
4. All seeds complete under the predeclared bounded execution without missing
   classes or silent exclusion of failed, no-growth, rejected, or
   budget-exhausted results.

If either paired mean C–A or C–D is non-positive after valid execution, the
joint task-efficacy hypothesis is **NOT SUPPORTED** in this setup; report
each contrast separately. Positive means that fail the four-of-five,
engagement, non-interference, or valid-execution gate are **INCONCLUSIVE**.
There is no inherited absolute accuracy threshold; five seeds remain
exploratory.

Observation-only B versus A is a mandatory implementation non-interference
check, not an efficacy claim. Candidate counts/opportunity and realized
emissions may differ in D because its temporal order is the intervention;
report actual exposure and do not characterize it as equal realized
candidate opportunity. Equal conditions mean equal samples, presentation
counts, budgets, topology initialization per paired seed, and declared caps.

## Scope, clauses, and exclusions

Authorized work is limited to `.github/agents/luna-33.agent.md` (this
dispatch), the standalone runner and its focused tests, the named Luna-33
artifact directory, and its completion handoff as listed in the dispatch.
The current decision changes only this handoff, the Luna agent dispatch,
`workflow/docs/luna/LUNA_WORKFLOW.md`, and `workflow/ARCHITECTURE_CHANGELOG.md`.

No architecture clause changes. The experiment operates within accepted
ACP-0007 and may report applicable evidence for A01–A08, A10–A11, A14–A15;
it does not promote experimental behavior. Labels remain outside structural
evidence; reward mode is neutral. Pruning, N3, edge-parameter learning, core
runtime/API changes, historical artifact/control edits, visualization
integration, and hardware/GPU/FPGA/FPAA equivalence are excluded.

**ACP required: NO. Architecture change: NO.** Contract 1.2, A01–A15,
accepted ACP-0007, and acceptance criteria are unchanged. E2 pruning and N3
remain **NOT AUTHORIZED**. Prediction benefit, resource benefit, and hardware
equivalence remain **NOT ESTABLISHED**. Luna-33 is **AUTHORIZED / NOT
EXECUTED**. Required next sequence: `Luna-0 -> Luna-33 -> Luna-0`.

## Governance validation and next assignment

Baseline validation was performed before this authorization:

| Procedure | Result |
|---|---|
| Repository branch/revision/worktree | Clean `main`; `HEAD == origin/main == cc66e6a4affb044bf726d92510bcfd214c1f698f` |
| Full test suite | 908 passed, 0 failed, 1 conditional CUDA-unavailable skip |
| Collection | 909 tests |
| Outcome-bearing efficacy run or preview | **NOT RUN BY DESIGN** |

No code, experiment, tests, data, metrics, or result artifact were changed or
generated for Luna-33. The next assignment is **Luna-33** under the exact
dispatch above. Luna-0 will independently review the completed evidence
before any closure or successor decision.
