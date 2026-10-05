# Luna-0 Independent Review — Luna-33 ACP-0007 Four-Class EXCURSION_V1 Efficacy

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent reproduction and bounded governance closure of Luna-33"
  task_id: "luna-0-independent-review-luna-33-acp0007-four-class-efficacy-20261004"
  component: "Luna-33 artifact, verdict, interpretation, and closure audit"
  owner: "Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT VERIFICATION", "EXPERIMENT REPRODUCTION", "ARTIFACT AUDIT", "GOVERNANCE CLOSURE"]
  status: "PASS — LUNA-33 CLOSED / INDEPENDENTLY VERIFIED WITHIN DECLARED SCOPE"
  contract_version: "1.2"
  branch: "main"
  review_start_revision: "f62936243f6fab39210392a3f17e3c4df9fe99e3"
  reviewed_implementation_revision: "58e330454278101ad7ca52dce03067eb4b95927b"
  reviewed_artifact_revision: "58e330454278101ad7ca52dce03067eb4b95927b"
  scope_publication_revision: "f62936243f6fab39210392a3f17e3c4df9fe99e3"
  review_publication_revision: "governance-only closure publication containing this handoff"
  final_origin_main: "verified after publication; see the closure commit"
  worktree_at_review_start: "clean; HEAD == origin/main"
  architecture_change: false
  proposal: null
  dependencies:
    - "Corrected Luna-33 authorization at 89f05f3d7c7ce18646d8b4302b74c66e90ee0895"
    - "Frozen code baseline cc66e6a4affb044bf726d92510bcfd214c1f698f"
    - "Accepted ACP-0007"
  hypothesis: "The published Luna-33 experiment is reproducible, passes its non-interference and valid-execution gates, and its published verdict follows the frozen decision rule."
  counter_hypothesis: "A reproducibility mismatch, contract failure, unexplained candidate extraction result, or verdict inconsistent with the predeclared rule blocks closure."
  interfaces_relied_on:
    - "Committed Luna-33 runner and focused test"
    - "ExperimentConfig and public ExperimentRunner.train()/evaluate()"
    - "Public topology and structural decision/evidence records"
    - "Public EXCURSION route paths and deterministic result artifacts"
  label_information_boundary:
    - "Labels remain external readout supervision/evaluation and are absent from structural observations."
    - "No accuracy, reward, readout result, or held-out result enters candidate evidence."
  timing_assumptions:
    - "Structural temporal association uses canonical emission timestamps and 0 < dt <= 4.0."
    - "No common neural timestep or timing reinterpretation was introduced."
  reset_boundaries:
    - "Review compares each fresh seed/condition run; structural evidence is character-local and bounded."
    - "Held-out evaluation uses the public non-updating evaluation path."
  resource_bounds:
    - "8 nodes, 2 initial edges, edge capacity 16, fan-in/out 2."
    - "Observation ring and source histories/candidates, queues, event budget, settling, attempts, and growth remain within the frozen dispatch."
  authorized_scope:
    - "Reproduce and audit the published runner, artifacts, focused tests, frozen verdict, and bounded architecture claims."
    - "Publish this independent review handoff and close only the exact Luna-33 experiment scope in workflow/changelog."
  unauthorized_scope:
    - "No runner, test, artifact, core/runtime/API, ACP, historical-result, or profile changes."
    - "No profile tuning, new efficacy run, architecture promotion, hardware claim, or Luna-34 authorization."
  controls: ["A/B observation non-interference", "C versus A fixed-topology comparison", "C versus D coordinate-time-order intervention"]
  measurements:
    - "Byte-level artifact reproduction and exact five-seed/four-condition completeness"
    - "Held-out accuracy, class/confusion reconciliation, structural observation/candidate/admission counters, and exact later route use"
    - "Public held-out topology/prototype non-mutation and execution-bound checks"
  information_boundary_check:
    - "Independently verify static observation locality and that labels/task outputs do not enter structural evidence."
  hardware_mapping:
    - "Software-reference verification only; hardware equivalence is not established."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A10", "A11", "A14", "A15"]
  preserves: ["Architecture Contract 1.2 / A01-A15", "accepted ACP-0007", "default EXCURSION_V1 behavior", "historical Luna-12L and Luna-13F results"]
  files_reviewed:
    - ".github/agents/luna-33.agent.md"
    - "workflow/handoffs/luna-0-post-luna32-acp0007-four-class-efficacy-decision-20261004.md"
    - "workflow/handoffs/luna-0-luna33-topology-feasibility-correction-20261004.md"
    - "workflow/handoffs/luna-33-acp0007-four-class-efficacy-20261004.md"
    - "workflow/docs/architecture_proposals/ACP-0007.md"
    - "workflow/handoffs/luna-28-excursion-local-temporal-growth-20261004.md"
    - "workflow/handoffs/luna-0-final-closure-review-Luna-13F-closed.md"
    - "workflow/handoffs/energy-prediction-four-class-scale-Luna-12L.md"
    - "run_luna33_acp0007_four_class_efficacy.py"
    - "tests/test_luna33_acp0007_four_class_efficacy.py"
    - "artifacts/acp0007-luna33-four-class-efficacy/config.json"
    - "artifacts/acp0007-luna33-four-class-efficacy/results.json"
    - "artifacts/acp0007-luna33-four-class-efficacy/summary.json"
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna-33-acp0007-four-class-efficacy-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Independent artifact reproduction: all three JSON files byte-identical."
    - "Luna-33 focused tests: 12 passed."
    - "Combined regression suite: 244 passed."
    - "Full suite: 920 passed, 1 CUDA-unavailable skip; 921 collected."
    - "Compileall and Pylance diagnostics: passed/no errors."
  tests_failed: []
  tests_not_run:
    - "GPU/CUDA execution beyond the documented unavailable-device skip."
    - "FPGA, FPAA, hardware equivalence, and any real-dataset efficacy; out of scope."
  assumptions:
    - "Five seeds are exploratory evidence for this declared setup, not a population guarantee."
    - "The bounded observation evidence and policy implementation are interpreted under the accepted ACP-0007 local-history semantics."
  unresolved:
    - "The task effect of successfully engaged growth and temporal specificity remain not established because candidates/admissions were zero."
    - "Any cause-focused follow-up requires a separate Luna-0 decision."
  pre_execution_contamination: "LIMITED-NONOUTCOME"
  scientific_efficacy_verdict: "NOT SUPPORTED IN THIS SETUP"
  engaged_growth_task_effect: "NOT ESTABLISHED"
  temporal_specificity_of_engaged_growth: "NOT ESTABLISHED"
  recommended_next_agent: ["Luna-0 Architecture Guardian; no new assignment is authorized"]
  successor: "NOT AUTHORIZED"
```

## Terminal verdict

**PASS — LUNA-33 ACP-0007 FOUR-CLASS EXCURSION_V1 EFFICACY EXPERIMENT
INDEPENDENTLY VERIFIED / CLOSED** within the exact four-class synthetic
reference experiment declared by the corrected dispatch.

The independent execution and artifact audit pass. The predeclared joint H1
result is **NOT SUPPORTED IN THIS SETUP**. This is not evidence that
successfully engaged ACP-0007 growth is ineffective or harmful: candidates
did not form, growth was never attempted, and no edge was admitted. The
effect of engaged growth and temporal specificity of engaged growth remain
**NOT ESTABLISHED**.

## Review start, lineage, and publication scope

The review synchronized `origin/main` and verified branch `main`,
`HEAD == origin/main == f62936243f6fab39210392a3f17e3c4df9fe99e3`,
subject `docs: publish Luna-33 efficacy handoff`, with a clean worktree.
The reviewed lineage is:

| Revision | Role |
|---|---|
| `cc66e6a4affb044bf726d92510bcfd214c1f698f` | Luna-32 closed / frozen code-under-test baseline |
| `34d286cc53dd8c80d00a660b00f516f900c3d4db` | Original Luna-33 authorization |
| `e83cb286fe6ef71652d2b209f8dc5c2d85a797b4` | Original authorization finalization |
| `7be17ffb5b85c2aeb955f00f1269ea5b0731c4ef` | Original matched-topology blocker publication |
| `6206eb11f2160adcd38b032ee7b7fe86fcc187d9` | Stop-report provenance finalization |
| `89f05f3d7c7ce18646d8b4302b74c66e90ee0895` | Corrected pre-outcome topology authorization |
| `58e330454278101ad7ca52dce03067eb4b95927b` | Runner, focused tests, and deterministic artifacts |
| `f62936243f6fab39210392a3f17e3c4df9fe99e3` | Luna-33 completion handoff publication and review start |

The diff from authorization revision `89f05f3...` to implementation revision
`58e3304...` contains exactly the five authorized runner/test/config/results/
summary paths. The diff from `58e3304...` to review-start revision `f629362...`
contains only the authorized Luna-33 handoff path. There are no core/runtime/
API, ACP, historical evidence, workflow, or unrelated-test changes in either
publication range.

The same-path stop-to-completion handoff reuse is **ACCEPTABLE**. The original
blocked report is recoverable from both `7be17ff...` and `6206eb1...`; the
change between those two records only finalizes handoff-publication metadata.
The original eight-edge initialization failure remains accurate historical
evidence and has not been erased or rewritten as an outcome-bearing run.

## Corrected profile, topology, and configuration audit

The committed runner and config agree on:

| Setting | Audited value |
|---|---:|
| Nodes | 8 |
| Initial edges | 2 |
| Original infeasible initial-edge count | 8 |
| Edge capacity | 16 |
| Fan-in / fan-out | 2 / 2 |
| Correction reason | `pre-outcome public-initializer feasibility` |
| No efficacy preview before correction | `true` |

The dispatch diff from the original authorization to the corrected
authorization changes the topology initial-edge setting and explanatory
authorization text only. The correction handoff records its pre-outcome
feasibility sweep; seeds, node count, capacity, fan limits, observation fabric,
growth bounds, data/split, A-D design, D intervention, endpoint, support rule,
and public initializer remain frozen.

The committed public initializer was independently exercised for all five
seeds and all four conditions. A/B/C/D initial edge/delay topologies agree
within each seed and match the predeclared matrix:

| Seed | Initial edges (delay 1.0) |
|---:|---|
| 0 | `neuron-7 -> neuron-4`; `neuron-6 -> neuron-2` |
| 1 | `neuron-3 -> neuron-5`; `neuron-7 -> neuron-6` |
| 2 | `neuron-2 -> neuron-1`; `neuron-4 -> neuron-1` |
| 3 | `neuron-2 -> neuron-4`; `neuron-6 -> neuron-4` |
| 4 | `neuron-3 -> neuron-4`; `neuron-4 -> neuron-0` |

The static observation map is the label- and result-independent directed ring
`neuron-i -> neuron-(i+1 mod 8)`, unchanged across B/C/D. A–D use the same
`EXCURSION_V1`, `e2_local_temporal`, one-epoch, neutral-reward profile and
bounded topology, queue, event, candidate, history, score, settling, delay,
and attempt settings; only the declared observation/plasticity flags and D
training transform differ. No TANH control, pruning, or N3/edge-parameter
learning is present.

The frozen structural bounds are preserved: neighborhood/reverse-observer
limits 2/2, association window 4.0, history 8, candidate capacity 4,
maximum score 3, growth delay 0.4, attempt budget 16, and one maximum growth
per epoch. The dispatch and artifact contain no result-dependent retuning.

## Dataset, split, and D-intervention audit

For each seed, the independent audit regenerated 64 training and 64
evaluation examples, with 16 per class, using training seed `12007 + seed`,
evaluation seed `22017 + seed`, training-order seed `330000 + seed`,
evaluation-order seed `330001 + seed`, and D point-shuffle seed stream
`330002 + seed`. Generated training/evaluation sample-ID and sequence-digest
sets are disjoint. Generated metadata, ordered train, ordered evaluation,
and destroyed-order digests all reproduce the committed config values.

| Seed | Ordered train SHA-256 | Ordered held-out SHA-256 | D train SHA-256 | D examples changed / coordinate slots reassigned |
|---:|---|---|---|---:|
| 0 | `74393067e0809e4b990fa8a9afd829f27874124932e06183ea84d3861919c1fe` | `7889c0ecd3fdf6e165e8377b0fa49e66a240803df4424802d7e3bdfc6989eaab` | `1c90ff65dc442a17320232f018717d52d507a04fa4b4c24851ff4a493fbb3ce9` | 64 / 959 |
| 1 | `6dd3b825da69c9babca053027531e8b1d2bb1d259019d8c6e957fb1e5b58a9a2` | `2b02a4bc11e8569f6d31c93c85c51a082e876b1754bc914fb9c5751f88243f8a` | `1fa22e977304da961c9587747488ddb426eb1d56a1e385872a373f277ecc1d0a` | 64 / 996 |
| 2 | `132a7af86e20de3fb3a26680ae5346f50eb305fa893d5aea2ceffcac30aad14b` | `39b75b3c5dea62199a86bd340b08eaf21541a39b1349b160507567548ea16f7c` | `51a57a4191865a2bd68eb135d0db6c9afbc2ebcefbd490975408ffc02c4ee7c2` | 64 / 970 |
| 3 | `cb5c1bee4df4836354e49d76822d3aad61ac93fbcc04d4891f1ebe3dfdf038b5` | `3642b2013dfc9dcdf0751634d6c5914874236458e9245191ec1cff57cefa0f88` | `1e65b0ec32638c26a67c4185fe4c063fd987a3c8efac33248a3f07ad220f653d` | 64 / 979 |
| 4 | `0b049303db0539d7d004464be49912b4bc95d1f9624db307eda752f19947bd5d` | `386c1cd8498d109331c276e3a269588cb4a1738259c40096c5a951cf1f923848` | `0aaa1efdfd48238c7315a71ab599ea72077d184c4823f3c280dcc098415212c5` | 64 / 948 |

Across all five seeds, D preserves every example ID and external label,
coordinate multiset, point count, exact ordered timestamp vector, duration,
`pen_state`, and `stroke_boundary`. Coordinate-to-time assignments change
nontrivially in every example. No timestamps are shuffled or regenerated.

## Focused-test and pre-execution contamination audit

The 12 focused Luna-33 tests cover deterministic/disjoint data generation,
D metadata and timestamp preservation, frozen matched configuration,
five-seed public topology initialization and paired equality, held-out
topology/prototype non-mutation, decision-snapshot-based admitted-edge
extraction, exact directed EXCURSION route-path use (including wrong
direction, non-EXCURSION, and topology-presence-only negatives), deterministic
JSON serialization, support-rule and four-of-five boundaries, failed-arm
retention, and the no-pruning/no-N3 profile. They exercise public generation,
configuration, runner, and route-helper behavior; they do not load published
artifact output as their oracle. The explicit ring-map config assertion is
supplemented by the independent observation evidence audit below.

**PRE-EXECUTION CONTAMINATION: LIMITED-NONOUTCOME.** One earlier uncommitted
failing focused-test draft partially trained the seed-0 C workload while
testing evaluation non-mutation. That was a test-fixture execution, not a
retained or examined efficacy result. The reported draft failures were
fixture/assertion and summary-fixture mechanics. No accuracy, paired
contrast, growth result, or other outcome informed a profile change; no
scientific parameter was changed after that partial test. The full corrected
focused suite passed before the formal 20-arm experiment ran. This limited
test execution is disclosed, but is not material outcome contamination and
does not block the predeclared inference.

## Artifact reproduction and integrity

The independent rerun used the committed runner, the frozen Python 3.11.5
environment, and a fresh temporary output directory; the committed
`artifacts/` directory was not overwritten. All three regenerated files
matched byte-for-byte by independent SHA-256:

| Artifact | Committed and independently regenerated SHA-256 |
|---|---|
| `config.json` | `50FE0410F57504643DD37487DBC14D1CA3320D1BAE00246F935928C9C295B5B6` |
| `results.json` | `B6D9C917D1F1D8F53F526B55D0EBC2499C1CEF0013E3825A779088E16CC950C8` |
| `summary.json` | `646BB3F2B29B8E41CC5A452B1F8424EAEB5718C041B9335E3AC5442989D2BCEA` |

The result schema contains exactly five seeds and four conditions per seed:
20/20 records, with no omitted, filtered, or success-shaped replacement for
an execution failure. Every record reports `completed`, valid execution,
represented training/evaluation classes, and held-out non-mutation.

## Execution, observation, and non-mutation evidence

All 20 runs have completed execution, zero event-budget exhaustion, zero
incomplete settling, zero pending events, and all four classes represented.
The independent public-API rerun trained and evaluated every arm; the
`ExperimentRunner.evaluate()` path executes with `update=False`. Direct
before/after comparisons found topology and prototypes unchanged in **20/20**
arms, and reproduced each artifact's topology, prototypes, predictions,
accuracy, and confusion records.

A/B canonical non-interference was independently recomputed for all five
seeds. Predictions, event-trace SHA/count, readout diagnostics, topology,
prototypes, training before/after/history metrics, held-out metrics,
execution counters, prediction metrics, and activity proxies match exactly;
only explicitly observer-owned structural evidence fields are excluded.

| Seed | B/C/D observed emissions | B/C/D observation work |
|---:|---:|---:|
| 0 | 338 | 676 |
| 1 | 361 | 722 |
| 2 | 306 | 612 |
| 3 | 314 | 628 |
| 4 | 396 | 792 |

These totals were recomputed from each actual `StructuralDecision.evidence`
record. Each observed emission generates the bounded self/reverse-observer
work shown. The evidence records contain only emitter identity/event
identity/timestamp and observer; labels and task outputs do not enter
structural evidence.

## Zero-candidate, decision-status, and route-use audit

Every C and D seed has 64 structural decisions. The independent audit
recomputed `candidate_pair_opportunities` as the sum of each decision's
candidate-list length plus `candidate_rejections`. Every C/D decision has an
empty candidate list and zero candidate rejections; each seed's total is
zero. Retained candidates, growth attempts, admissions, growth rejections,
capacity/saturation rejections, incomplete-settling decisions, and budget
exhaustions are also zero. All 64 C/D decisions per seed have substantive
status `no_candidate`; B's 64 decisions per seed are `observation_only`.

The recorded bounded per-source observation histories were independently
checked against the static successor ring and the ACP-0007 interval
`0 < dt <= 4.0`. No eligible source-own-emission followed by permitted
neighbor-emission pair occurs in the retained source-local windows. The
candidate lists, rejection counts, decision statuses, and recomputed
opportunity totals agree. **CAUSE OF ZERO CANDIDATES:** no temporally ordered
source-neighbor association was admitted into the bounded policy evidence;
the artifact does not indicate a candidate extraction/bookkeeping defect.
This conclusion is bounded by the declared per-source history capacity and
does not claim any unbounded whole-character event chronology.

No C seed admitted an edge. No C admitted edge was later used; the exact
directed-edge EXCURSION route-path criterion is not satisfied in any seed.
`c_route_engagement_seed_count` is 0 and the route-engagement gate is false.
Structural observation is **ENGAGED**; candidate formation is **NOT
ENGAGED**; structural mutation is **NOT ENGAGED**.

## Accuracy, contrasts, and verdict precedence

Overall held-out accuracy was independently recomputed from each confusion
record (64 examples per arm); per-class accuracy reconciles to the same
confusion counts and is identical A–D within each seed:

| Seed | A | B | C | D | C-A | C-D |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.250000 | 0.250000 | 0.250000 | 0.250000 | 0 | 0 |
| 1 | 0.296875 | 0.296875 | 0.296875 | 0.296875 | 0 | 0 |
| 2 | 0.234375 | 0.234375 | 0.234375 | 0.234375 | 0 | 0 |
| 3 | 0.250000 | 0.250000 | 0.250000 | 0.250000 | 0 | 0 |
| 4 | 0.156250 | 0.156250 | 0.156250 | 0.156250 | 0 | 0 |
| **Mean contrast** |  |  |  |  | **0.0** | **0.0** |
| **Positive seeds** |  |  |  |  | **0/5** | **0/5** |

The predeclared precedence says that after valid execution, either
non-positive paired mean yields **NOT SUPPORTED IN THIS SETUP**. Both means
are exactly zero, so the published verdict follows the frozen rule even
though route engagement also failed. No post-hoc rule change was made.

Interpretation is bounded:

- **JOINT PREDECLARED H1:** NOT SUPPORTED IN THIS SETUP.
- **Effect of actually engaged ACP-0007 growth on task accuracy:** NOT
  ESTABLISHED by Luna-33; no candidate formed, no growth was attempted, and
  no edge was admitted.
- **Temporal-order specificity of engaged growth:** NOT ESTABLISHED. C-D=0
  with zero C and D candidate opportunities does not show that time order is
  irrelevant to an engaged mechanism.
- **Prediction benefit:** NOT ESTABLISHED. Reported zero prediction loss is
  not a prediction-benefit criterion.
- **Resource benefit:** NOT ESTABLISHED. Activity/energy values are
  uncalibrated model proxies, not joules; no topology growth occurred.
- **Hardware equivalence:** NOT ESTABLISHED.

Historical Luna-12L remains **NOT SUPPORTED / UNCHANGED**. Luna-13F's
general useful-growth prediction remains **NOT SUPPORTED / UNCHANGED**.
Neither is superseded by Luna-33.

## Independent validation record

Environment: Windows 10 build 19045, 64-bit CPython 3.11.5 at
`C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe`.

| Procedure | Independent result |
|---|---|
| Fresh experiment reproduction to a new temporary directory | Passed; all three JSON files byte-identical by SHA-256 |
| `python -m pytest tests\test_luna33_acp0007_four_class_efficacy.py -q` | **12 passed** |
| Combined regression: Luna-33, Luna-28 growth, Luna-12B, EXCURSION_V1 neuron/integration, E2 multi-excursion, structural plasticity/topology, and ExperimentRunner tests | **244 passed** |
| `python -m pytest -q -rs` | **920 passed, 0 failed, 1 skipped** |
| CUDA skip | `tests/test_gpu_visualization.py:61`; CUDA unavailable |
| `python -m pytest --collect-only -q` | **921 collected**; no deletions, xfail additions, unconditional skip additions, or deselections in the publication scope |
| `python -m compileall -q tpcn tests run_luna33_acp0007_four_class_efficacy.py` | Passed |
| Pylance problems on the Luna-33 runner and focused test | No errors in either file |
| `git diff --check` | Passed at review start; governance publication is checked again before commit |

The combined regression command was:

```text
python -m pytest -q tests\test_luna33_acp0007_four_class_efficacy.py tests\test_luna28_excursion_structural_growth.py tests\test_luna12b_integration.py tests\test_excursion_neuron.py tests\test_excursion_integration.py tests\test_e2_multi_excursion.py tests\test_structural_plasticity.py tests\test_topology.py tests\test_experiments.py
```

## Architecture and governance status

| Clause | Independent audit |
|---|---|
| A01 | PASS — event-driven execution semantics unchanged |
| A02 | PASS — local logical-time and intrinsic state semantics unchanged |
| A03 | PASS — finite delayed causal route semantics unchanged |
| A04 | PASS — bounded topology, queue, event, candidate, history, and growth limits preserved |
| A05 | PASS — no spatial reservoir dependency introduced |
| A06 | PASS — prediction/error computation unchanged |
| A07 | PASS — labels/readout/task outputs are not structural inputs; static bounded observation fabric |
| A08 | PASS — deterministic, bounded execution and settling gates preserved |
| A10 | PASS — energy/activity remain diagnostic proxies |
| A11 | PASS — reward/learning boundary unchanged; neutral reward used |
| A14 | PASS WITH ACP-0007 EXPERIMENTAL SCOPE ONLY |
| A15 | PASS FOR SOFTWARE REFERENCE ONLY; no hardware validation |

Architecture Contract **1.2 / UNCHANGED**. Accepted ACP-0007 **UNCHANGED**.
Architecture change: **NO**. Core/runtime/API change: **NO**. Default
EXCURSION_V1 behavior: **UNCHANGED**. E2 pruning: **NOT AUTHORIZED**. N3:
**NOT AUTHORIZED**. Hardware equivalence: **NOT ESTABLISHED**.

Luna-33 is **CLOSED / INDEPENDENTLY VERIFIED only within the declared
four-class ACP-0007 efficacy experiment scope**. This closure does not
authorize a new experiment, profile tuning, an architecture promotion, or
Luna-34. Any new investigation into candidate formation requires a separate
Luna-0 governance invocation.
