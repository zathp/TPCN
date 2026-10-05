# Luna-33 Completion Handoff — ACP-0007 Four-Class EXCURSION_V1 Efficacy

```yaml
tpcn_handoff:
  agent: "Luna-33 ACP-0007 Four-Class EXCURSION_V1 Efficacy"
  luna_identifier: "Luna-33"
  descriptive_name: "Bounded four-class ACP-0007 efficacy experiment"
  task_id: "luna-33-acp0007-four-class-efficacy-20261004"
  component: "EXCURSION_V1 four-class temporal spiral efficacy"
  status: "IMPLEMENTED / PUBLISHED — AWAITING INDEPENDENT REVIEW"
  contract_version: "1.2"
  branch: "main"
  code_baseline: "cc66e6a4affb044bf726d92510bcfd214c1f698f"
  authorization_publication: "89f05f3d7c7ce18646d8b4302b74c66e90ee0895"
  execution_start_revision: "89f05f3d7c7ce18646d8b4302b74c66e90ee0895"
  implementation_revision: "58e330454278101ad7ca52dce03067eb4b95927b"
  artifact_result_revision: "58e330454278101ad7ca52dce03067eb4b95927b"
  handoff_publication: "this completion handoff; published in the subsequent Luna-33 handoff commit"
  final_origin_main: "verified after push; final publication commit is the published main HEAD"
  architecture_change: false
  proposal: null
  scientific_efficacy_verdict: "NOT SUPPORTED IN THIS SETUP"
  implementation_terminal_verdict: "PASS — LUNA-33 ACP-0007 FOUR-CLASS EXCURSION_V1 EFFICACY EXPERIMENT COMPLETED / READY FOR INDEPENDENT REVIEW"
  recommended_next_agent: ["Luna-0 Architecture Guardian"]
```

## Decision

**The joint task-efficacy hypothesis is NOT SUPPORTED IN THIS SETUP.**

The five paired mean accuracy contrasts are zero for both comparisons:

| Contrast | Paired values, seeds 0–4 | Mean | Positive seeds |
|---|---|---:|---:|
| C − A | 0, 0, 0, 0, 0 | 0.000000 | 0/5 |
| C − D | 0, 0, 0, 0, 0 | 0.000000 | 0/5 |

The frozen decision rule does not support H1 because neither paired mean is
positive. Additionally, the mechanism-engagement gate failed: no C seed
admitted an edge, so no admitted C edge could later be shown on a held-out
canonical `EXCURSION` event's exact directed `route_path`. The
non-interference and valid-execution gates passed. This result is restricted
to the declared synthetic reference setup; it is not a population guarantee.

Task efficacy is distinct from prediction benefit, resource benefit, and
hardware equivalence. **Prediction benefit: NOT ESTABLISHED. Resource
benefit: NOT ESTABLISHED. Hardware equivalence: NOT ESTABLISHED.**

## Authorization, scope, and provenance

Execution began on clean `main` at
`89f05f3d7c7ce18646d8b4302b74c66e90ee0895`, with `HEAD == origin/main`.
This is the corrected Luna-0 authorization publication. The frozen code
baseline was `cc66e6a4affb044bf726d92510bcfd214c1f698f`; relevant runtime,
experiment, ACP-0007, and benchmark source matched the authorization's
baseline requirements.

The implementation and all three result artifacts are recorded in
`58e330454278101ad7ca52dce03067eb4b95927b`. This completion handoff is
published in the subsequent handoff-only commit. Only these six authorized
paths are changed by the two Luna-33 publication commits:

- `run_luna33_acp0007_four_class_efficacy.py`
- `tests/test_luna33_acp0007_four_class_efficacy.py`
- `artifacts/acp0007-luna33-four-class-efficacy/config.json`
- `artifacts/acp0007-luna33-four-class-efficacy/results.json`
- `artifacts/acp0007-luna33-four-class-efficacy/summary.json`
- `workflow/handoffs/luna-33-acp0007-four-class-efficacy-20261004.md`

No core/runtime/configuration API, accepted ACP-0007, Architecture Contract,
acceptance criteria, workflow/changelog governance, historical Luna-12L or
spiral control, or unrelated test was changed. No pruning, N3, edge-parameter
learning, readout redesign, visualization, or hardware/GPU/FPGA/FPAA claim is
included.

## Frozen design and execution

The runner uses the authorized four-class synthetic temporal-spiral profile:
`make_spiral_dataset(examples_per_class=16, train_seed=12007 + seed,
evaluation_seed=22017 + seed, config=SpiralConfig())`, for seeds 0–4.
Each seed has 64 training and 64 disjoint held-out examples, with 16 samples
per class in each split. The independent training and evaluation order
streams are `330000 + seed` and `330001 + seed`. D assigns each example's
coordinate multiset to its existing ordered timestamp slots using one
`getrandbits(32)` point-shuffle seed per example from `330002 + seed`;
timestamps, point count, duration, sample identity, labels, pen state, and
stroke-boundary metadata are preserved.

The public initialized topology uses eight nodes, two initial edges, edge
capacity 16, fan-in/out limits 2/2. The static observation fabric is the
fixed eight-node directed ring with neighborhood/reverse-observer limits
2/2. A–D have identical initial edge/delay snapshots for each paired seed.
All four conditions retain `e2_local_temporal`; A disables observation and
plasticity, B enables observation only, and C/D enable both. D alone uses the
coordinate-to-time permutation. Conditions share the authorized
`EXCURSION_V1`, one-epoch, event-only, neutral-reward workload and bounded
queue/event, settling, prediction, association, history, candidate, scoring,
growth-attempt, and mutation-history settings. The complete settings,
condition identity, topology profile, and dataset/split digests are in
`config.json`.

For each of five seeds, the runner created four fresh `ExperimentRunner`
instances (20/20 condition runs completed), trained using the authorized
public interface, and evaluated the same canonical held-out examples with
`update=False`. There were no runtime exceptions, omitted seeds, failed or
incomplete settling cases, event-budget exhaustion, or missing classes.
Held-out evaluation left topology and prototypes unchanged in all 20 runs.
All five A/B paired non-interference checks passed, including canonical task
results, prediction/event-trace comparisons, topology, prototypes, execution
counters, prediction metrics, and activity proxies; observer-owned evidence
counters were allowed to differ.

The scientific run was performed only after the focused tests passed. One
earlier draft of the evaluation-nonmutation focused test did partially train
on the full seed-0 C dataset while that test was initially failing. No
efficacy metrics from that test invocation were retained or examined. The
test was replaced with a one-example fixture; the formal five-seed,
four-condition execution followed after the corrected focused suite passed.

## Results

### Held-out accuracy and per-class accuracy

All four conditions had identical overall held-out accuracy per seed:

| Seed | A = B = C = D | Left-inward | Left-outward | Right-inward | Right-outward |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.250000 | 0.437500 | 0.062500 | 0.000000 | 0.500000 |
| 1 | 0.296875 | 0.000000 | 0.562500 | 0.000000 | 0.625000 |
| 2 | 0.234375 | 0.000000 | 0.437500 | 0.500000 | 0.000000 |
| 3 | 0.250000 | 0.562500 | 0.437500 | 0.000000 | 0.000000 |
| 4 | 0.156250 | 0.000000 | 0.375000 | 0.250000 | 0.000000 |

All four classes were represented in every evaluation. Per-condition
confusion matrices, readout/prototype counts, margins, predictions, and
complete evaluation metrics for every seed are retained in `results.json`;
the table above does not replace those records. Per-class accuracy and
confusion were identical across A–D within each seed. Every seed/condition
had four prototypes; no class was missing.

### Structural opportunity, admissions, and route engagement

| Seed | B/C/D observed emissions | B/C/D observation work | C/D candidate opportunities | C/D retained | C/D attempts | C/D admissions | C/D rejections | C/D saturation / budget exhaustion | C admitted edges later routed |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 338 | 676 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 |
| 1 | 361 | 722 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 |
| 2 | 306 | 612 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 |
| 3 | 314 | 628 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 |
| 4 | 396 | 792 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 |

A has zero observation emissions/work as configured. B/C/D received equal
sample counts, training effort, structural bounds, and candidate capacity;
the table reports realized observations and does not claim equal realized
candidate exposure. For each C seed, the route-use analysis found no admitted
edge and therefore no exact admitted directed edge later present in a
held-out canonical event's `route_path`. Merely having an edge in a topology
was not counted as route use.

### Diagnostics

Representative public C held-out diagnostics are recorded below; the full
per-condition values are in `results.json`. A and B additionally passed the
stricter exact non-interference comparison.

| Seed | Processed events | Excursions / activations | Max route depth | Prediction loss | Prediction errors | Mean margin (A/B/C; D) | Energy proxy | Edge-transfer proxy | Fan-in / fan-out utilization |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1829 | 306 | 1 | 0 | 0 | 0.051705105; 0.051705077 | 1968.506810 | 24.557674 | 0.125 / 0.125 |
| 1 | 1881 | 302 | 1 | 0 | 0 | 0.075954953; 0.075954947 | 2028.853441 | 31.622725 | 0.125 / 0.125 |
| 2 | 2081 | 395 | 1 | 0 | 0 | 0.051328907; 0.051328903 | 2269.809468 | 39.414509 | 0.125 / 0.125 |
| 3 | 2055 | 376 | 1 | 0 | 0 | 0.072142586; 0.072142588 | 2221.570292 | 27.999670 | 0.125 / 0.125 |
| 4 | 1830 | 289 | 1 | 0 | 0 | 0.054821628; 0.054821620 | 1967.938949 | 32.472862 | 0.125 / 0.125 |

The zero reported prediction loss or the uncalibrated energy/activity
diagnostics do not demonstrate prediction or resource benefit. These
activity/energy values are model proxies, not physical joules.
Per-seed/condition prediction, error, credit, activity, resource, topology,
and decision/rejection diagnostics are retained in `results.json`.

## Artifacts and reproducibility

The committed outputs are deterministic JSON:

| Artifact | SHA-256 |
|---|---|
| `config.json` | `50FE0410F57504643DD37487DBC14D1CA3320D1BAE00246F935928C9C295B5B6` |
| `results.json` | `B6D9C917D1F1D8F53F526B55D0EBC2499C1CEF0013E3825A779088E16CC950C8` |
| `summary.json` | `646BB3F2B29B8E41CC5A452B1F8424EAEB5718C041B9335E3AC5442989D2BCEA` |

Two final experiment executions produced byte-identical config, results,
and summary files. The configuration contains generated/ordered/destroyed
dataset digests for each seed; the results contain every seed/condition
record, full bounded structural decisions and rejection information,
topology snapshots, predictions, confusion, and event-trace hashes/counts.
Exact route-use events are stored if present; no C edge qualified.

Environment: Windows 10 build 19045, 64-bit CPython 3.11.5
(`C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe`).

## Validation record

| Procedure | Result |
|---|---|
| Authorization and baseline checks | Clean `main`; at start `HEAD == origin/main == 89f05f3d7c7ce18646d8b4302b74c66e90ee0895`; frozen code baseline matched |
| Public topology preflight | All five seeds initialized using the authorized public `ExperimentRunner`; A–D initial edge/delay snapshots match per seed |
| Formal experiment | 20/20 runs completed; all five seeds retained; no failed, incomplete, or budget-exhausted run |
| Focused Luna-33 suite: `python -m pytest tests/test_luna33_acp0007_four_class_efficacy.py -q` | **12 passed** |
| Relevant combined regression suite | **244 passed** |
| Final full suite: `python -m pytest -q -rs` | **920 passed, 1 skipped**; skipped test requires unavailable CUDA |
| Final test collection: `python -m pytest --collect-only -q` | **921 collected** |
| Final compile: `python -m compileall -q tpcn tests run_luna33_acp0007_four_class_efficacy.py` | Passed |
| Final Pylance diagnostics for runner and test | No errors found in either file |
| Staged and final whitespace validation: `git diff --cached --check` / `git diff --check` | Passed |
| Repeat experiment artifact comparison | Config, results, and summary SHA-256 values matched exactly |

## Architecture and interpretation audit

This work is an **ACP-0007 experiment, observation, and focused
verification**, not architecture promotion. Architecture Contract 1.2 and
A01–A15 were not amended. Applicable boundary observations:

- **A01–A08:** The work uses the existing causal EXCURSION_V1 event path,
  public bounded topology/routing and event-trace observables. No global
  neural timestep, alternate scheduler, nonlocal structural evidence, or
  label-dependent structural computation was introduced. Labels remain
  external readout supervision/evaluation; neutral reward prevents correctness
  from changing neural reward.
- **A10–A11:** Finite execution and resource diagnostics remain model
  proxies; no energy unit calibration, physical-energy claim, or predictive
  benefit claim is made.
- **A14–A15:** Growth remains the authorized opt-in `e2_local_temporal`
  software experiment. No hardware equivalence, GPU/FPGA/FPAA, or
  architecture-promotion claim is made.

The observation non-interference gate passed. The structural-growth
mechanism-engagement gate did not: there were zero candidate opportunities
and zero admissions in C. The result is not interpreted as evidence that
structural growth cannot help outside this profile, nor is the mechanism
repaired, tuned, or retried under this authorization.

Historical Luna-12L remains **NOT SUPPORTED / UNCHANGED**. Luna-13F's broader
useful-growth prediction remains **NOT SUPPORTED / UNCHANGED**. E2 pruning and
N3 remain **NOT AUTHORIZED**.

## Return to Luna-0

**PASS — LUNA-33 ACP-0007 FOUR-CLASS EXCURSION_V1 EFFICACY EXPERIMENT
COMPLETED / READY FOR INDEPENDENT REVIEW.** The scientific result remains
**NOT SUPPORTED IN THIS SETUP**.

Return to Luna-0 for independent review. Luna-33 is not self-closed, and this
handoff does not authorize a successor. No further efficacy run or profile
tuning is authorized by this dispatch.
