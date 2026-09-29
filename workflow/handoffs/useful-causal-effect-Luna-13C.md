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
  result_revision: "685cd721f7ca108278aa2e3044b53d46981e5bbd"
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
  tests_passing: ["python -m pytest tests/test_luna13c_causal_utility.py -q: 6 passed"]
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
| equal-budget random growth, seed 0 | 1.0 | 0.0 | `3962ea30...` | can reproduce |

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
| `python -m pytest tests/test_luna13c_causal_utility.py -q` | `09995ad`, Python 3.10.8 | PASS, 6 tests | focused suite |
| temporary artifact regeneration and SHA-256 comparison | `09995ad`, source revision `685cd72`, CPU | PASS, both JSON files byte-identical | `results.json`, `summary.json` |
| targeted corrective and requested regression bundle | `09995ad`, Python 3.10.8 | PASS, 124 tests | 13C, 13B, 12H, 12N, Stage-0-related slices |
| `python -m pytest tests -q` | `09995ad`, Python 3.10.8 | PASS, 256 passed, 1 skipped | full CPU suite |
| `python -m compileall -q tpcn run_temporal_efficacy_13c.py tests` | `09995ad` | PASS | compile check |
| `get_errors`; `git diff --check` | `09995ad` | PASS, no diagnostics and no whitespace errors | repository checks |
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

`PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT ESTABLISHED, LIMITATIONS REMAIN`

This status does not authorize Luna-13D or any architecture promotion.

## Corrective evidence pass

The corrective pass used the same bounded topology-rebuild machinery for the
sham, with computational graph fingerprint unchanged. The fixed useful-edge
control was distinct from the learned edge: it used `right -> target` with
delay `0.5`, while the learned edge used delay `1.0`, and it scored `2/2`.
Random growth used `random.Random(seed).choice(source_ids)` with independent
seeds: seed 0 selected `right -> target` and scored `2/2`; seed 1 selected
`left -> target` and scored `1/2`. A real label-mutation attack swapped the
evaluation targets to `late, on_time`; structure and pre-output computation
remained unchanged.

The corrected artifact is `artifacts/useful-causal-effect-13c/`, generated
from a clean tree at revision `685cd721f7ca108278aa2e3044b53d46981e5bbd`.
Focused corrective validation passed `6` tests; the focused temporal
regression set passed `42` tests. Random growth can reproduce the effect for
one independent seed, so the result remains qualified and does not establish
selection superiority or general utility.

## Luna-0 independent corrective re-review

Reviewed corrective implementation revision `09995add7643e63f61c45602922238e319965113`;
the artifact provenance identifies source revision
`685cd721f7ca108278aa2e3044b53d46981e5bbd`, baseline
`ea60610b7ba637e05ee986ffde2864e529a08f2c`, and a clean generation tree.
The synchronized review tree was clean and `HEAD == origin/main`.

The sham was independently instrumented: sham, targeted removal, and restore
each called the bounded topology construction twice. Sham returned the exact
present graph and fingerprint, retained the learned edge, completed `2/2`,
and matched present traces/events. The learned edge is
`right -> target, delay 1.0`; the hand-designed positive control is
`right -> target, delay 0.5`, a distinct edge identity that reaches `2/2`.
Random replay produced seed 0 `right -> target`, `2/2`, and seed 1
`left -> target`, `1/2`; this is evidence of possible random reproduction,
not superiority evidence. Label mutation to `late, on_time` preserved
structural state, candidate evidence, graph decisions, traces, event counts,
and completion behavior.

The raw causal cases were: learned present, short target `on_time` with
output `on_time` and long target `late` with output `late`; targeted removal
changed only the short case to output `late`. Its target arrivals changed from
`(1.0, 2.0)` to none, while the long case remained `late`; exact restoration
returned `2/2`. All primary and 30-event budget runs completed with zero
pending events and no exhaustion. Fresh topology/neuron/reset construction
was equivalent across conditions, but the checkpoint remains a compact
metadata fingerprint rather than a serialized queue/eligibility/random-state
clone.

**Independent result:** `PASS WITH FOLLOW-UP — CAUSAL EFFECT VERIFIED,
BOUNDED LIMITATIONS REMAIN`. No A01-A15 clause changed. Luna-13D was not
created or executed; it is eligible for later contract creation only by
explicit project-owner authorization. The next scientific boundary is a
separately authorized finite-resource utility study covering pressure,
retention/pruning/replacement, and event/energy tradeoffs.