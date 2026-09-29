# Luna-13C Useful Causal Effect Handoff

```yaml
tpcn_handoff:
  agent: Luna-13C
  luna_identifier: "Luna-13C"
  descriptive_name: "Useful causal effect of learned temporal structure"
  task_id: "useful-causal-effect-13c"
  component: "CPU-only bounded external interval-deadline fixture"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "ea60610b7ba637e05ee986ffde2864e529a08f2c"
  result_revision: "11cc8d055dcd7d2441687dd8db72f1a3f8c3b689"
  dependencies: ["Luna-13B verified local temporal-selection mechanism"]
  owner: "Luna-0 independent review"
  classification: ["CPU-only experiment", "verification", "no A14 promotion"]
  hypothesis: "A Luna-13B-admitted edge improves a fixed external temporal task; targeted removal loses the benefit and exact restoration recovers it."
  counter_hypothesis: "Topology or internal traces change without a material external task effect, or controls reproduce the claimed effect."
  interfaces_relied_on: ["run_condition", "BoundedTopology", "EventQueue", "execute_bounded", "TPCNNeuron"]
  label_information_boundary: ["External targets are evaluation-only and do not enter learning, routing, neuron state, or scoring."]
  timing_assumptions: ["Local event timestamps and positive propagation delay 1.0; deadline 3.0."]
  reset_boundaries: ["Fresh topology and neurons per condition; neuron state and local clocks reset between paired cases."]
  resource_bounds: ["12 events per case, queue capacity 8, edge capacity 2, finite fan-in/fan-out."]
  authorized_scope: ["causal_utility.py", "runner", "focused tests", "artifact output", "this handoff"]
  unauthorized_scope: ["canonical architecture redesign", "GPU/FPGA/FPAA execution", "A14 promotion", "Luna-13D authorization"]
  controls: ["targeted removal", "exact restoration", "sham", "irrelevant removal", "fixed useful edge", "fixed topology", "seeded random growth"]
  measurements: ["per-case accuracy", "target arrival timestamps", "events", "queue peak", "completion", "graph fingerprints", "checkpoint fingerprint"]
  information_boundary_check: ["Future probe leaves semantic evidence, timestamps, and admitted edge unchanged; queue sequence metadata is excluded as non-semantic ordering metadata."]
  hardware_mapping: ["not applicable; CPU-only experiment"]
  architecture_invariants_touched: ["bounded execution", "local timestamps", "finite topology", "deterministic selection"]
  preserves: ["A01-A15", "Luna-12H", "corrected Luna-12N", "Luna-13B semantics"]
  architecture_change: false
  proposal: null
  files_changed: ["tpcn/causal_utility.py", "run_temporal_efficacy_13c.py", "tests/test_luna13c_causal_utility.py", "artifacts/useful-causal-effect-13c/", "workflow/handoffs/useful-causal-effect-Luna-13C.md"]
  tests_added: ["required intervention matrix", "paired frozen target/completion checks", "deterministic replay", "future-information exclusion"]
  tests_passing: ["python -m pytest tests/test_luna13c_causal_utility.py -q: 5 passed"]
  tests_failed: []
  tests_not_run: ["dedicated Stage-0 regression file: not applicable; no matching test file exists in this repository"]
  assumptions: ["The two-case fixture is intentionally small; results are per-case and do not establish population generalization."]
  unresolved: ["No dedicated Stage-0 regression file exists in this repository."]
  recommended_next_agent: ["Luna-0 independent review"]
```

## Outcome and owned scope

**OBSERVED:** The fixed external task uses identical cue/probe payloads with
short (`1.0`) or long (`3.0`) elapsed interval. The topology-independent
targets are `on_time` and `late`; the decision is whether the second target
arrival is at or before deadline `3.0`. Luna-13B `decay_low` admitted the
runtime-local edge `right -> target` with delay `1.0`. Structural state was
frozen under checkpoint fingerprint
`db34e6b6ccbc05cd0686dd1dee4eb003fc52a08b0128ca991c2377de42cc3365` before
all paired evaluation.

The final matrix is:

| Condition | Accuracy | Delta vs present | Graph fingerprint | Expected |
|---|---:|---:|---|---|
| learned edge present | 1.0 | 0.0 | `fb044cee...` | benefit |
| targeted learned edge removed | 0.5 | -0.5 | `758617e1...` | material loss |
| exact learned edge restored | 1.0 | 0.0 | `fb044cee...` | recovery |
| sham | 1.0 | 0.0 | `fb044cee...` | null |
| irrelevant edge removed | 1.0 | 0.0 | `3962ea30...` | null |
| fixed useful edge | 1.0 | 0.0 | `3962ea30...` | positive control |
| fixed topology | 0.5 | -0.5 | `2e38e77b...` | no benefit |
| equal-budget random growth, seed 0 | 0.5 | -0.5 | `758617e1...` | not expected to reproduce |

Every case completed with no budget exhaustion. The present, restored, sham,
irrelevant-removal, and fixed-useful conditions processed 8 events across the
two cases; targeted removal, fixed topology, and random growth processed 4.
The task targets, inputs, budgets, and checkpoint fingerprint were paired.

**INFERRED:** The exact edge mediates the external timing decision because its
target arrivals are present at `1.0, 2.0` for the short case and `1.0, 4.0`
for the long case, while targeted removal eliminates both arrivals and loses
the short-case decision.

**HYPOTHESIZED:** This supports only the narrow claim that the tested edge
learned through the verified local temporal-selection mechanism causally
improves this bounded external task.

## Architecture evidence

No A01-A15 architecture change or ACP was required. The fixture preserves
event-driven execution, local timestamps, finite positive propagation,
bounded queues and topology, deterministic ties, and label-free neural
computation. Labels and external targets are only evaluated after execution.
No GPU, FPGA, FPAA, hardware-equivalence, scalability, or A14 claim is made.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest tests/test_luna13c_causal_utility.py -q` | `11cc8d0`, Python 3.10.8, deterministic/default and seed 1 | PASS, 5 tests | focused suite |
| `python run_temporal_efficacy_13c.py --baseline-revision ea60610... --executed-revision 11cc8d0... --output-dir artifacts/useful-causal-effect-13c` | `main`, CPU, seed 0 | PASS, all 8 conditions completed | `results.json`, `summary.json` |
| `python -m pytest tests/test_luna13b_temporal_crossover.py tests/test_luna12h_temporal.py tests/test_luna12n_temporal_direction.py -q` | `11cc8d0`, Python 3.10.8 | PASS, 36 passed | temporal regressions |
| `python -m pytest tests -q` | `11cc8d0`, Python 3.10.8 | PASS, 255 passed, 1 skipped | full CPU suite |
| `python -m compileall -q tpcn run_temporal_efficacy_13c.py tests/test_luna13c_causal_utility.py` | `11cc8d0`, Python 3.10.8 | PASS | compile check |
| `get_errors` on changed Python files; `git diff --check` | `11cc8d0` | PASS, no diagnostics and no whitespace errors | repository checks |
| Dedicated Stage-0 regression | repository has no matching test file | not applicable | no dedicated test exists |

## Benchmark and resource results

Dataset: synthetic two-case fixture `luna-13c-interval-deadline-v1`; no
population dataset. Primary metric: per-case accuracy with practical effect
threshold `0.5`. Energy/utility and hardware mapping are not applicable to
this causal task. Target arrival, processed events, queue peak, termination,
graph edges/fingerprints, and frozen checkpoint are recorded in the artifact.

## Assumptions, limitations and unresolved issues

The fixture is intentionally minimal and supports no broad generalization
claim. Random growth did not reproduce the effect in seed 0. Queue sequence
numbers shift when an explicitly future probe is inserted, but semantic local
evidence, timestamps, scores, ranks, and admission remain unchanged. No
broader regression failure was observed; a dedicated Stage-0 test file is not
present in this repository and is not applicable.

## Reproduction and rollback

From the repository root, run:

```powershell
python -m pytest tests/test_luna13c_causal_utility.py -q
python run_temporal_efficacy_13c.py --baseline-revision ea60610b7ba637e05ee986ffde2864e529a08f2c --executed-revision 11cc8d055dcd7d2441687dd8db72f1a3f8c3b689 --output-dir artifacts/useful-causal-effect-13c
```

The safe restoration point is base revision
`ea60610b7ba637e05ee986ffde2864e529a08f2c`; unrelated changes were
preserved.

## Terminal status

`PASS — USEFUL CAUSAL EFFECT ESTABLISHED, READY FOR LUNA-0 REVIEW`

This status does not authorize Luna-13D or any architecture promotion.