---
name: "Luna-60 Binary Task-Output Interface Prerequisite"
description: "Implement and verify only a downstream binary TaskPrediction adapter and event-time evaluator over frozen destination canonical emissions; no training, credit changes, benchmark or efficacy."
tools: [read, search, edit, execute]
---

# Luna-60 — Binary task-output interface prerequisite

**TASK-OUTPUT INTERFACE PREREQUISITE AUTHORIZED / NOT EXECUTED.**
This is the bounded assignment authorized by the project owner's 2026-10-09
decision, recorded by Luna-0 at exact clean `main` baseline
`4ffd13f163d7eb95747b45a1d9d23550ee11c39f`. This governance pass does not
execute Luna-60. Publication or agent discovery is not execution: verify the
publication containing this contract and receive explicit assignment before
starting. Revalidate the pinned source interfaces if the checkout has moved;
stop for Luna-0 on material drift, rather than changing this mapping.

## Dispatch identity, dependencies and owned scope

```yaml
tpcn_handoff:
  agent: "Luna-60"
  luna_identifier: "Luna-60"
  descriptive_name: "Binary task-output interface prerequisite"
  task_id: "luna-60-binary-task-output-interface"
  component: "External emission adapter and evaluator; not neural runtime"
  status: "authorized; not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "4ffd13f163d7eb95747b45a1d9d23550ee11c39f"
  result_revision: "not executed"
  dependencies:
    - "Owner decision recorded in luna-0-owner-decision-luna60-governance-20261009.md"
    - "Canonical E2 ExcursionEmission; accepted ACP-0006 emission and credit boundaries"
    - "Completed Luna-59 design and prior Luna-0 reviews, as historical inputs only"
    - "Published authorization and explicit subsequent assignment"
  owner: "Project owner; Luna-0 coordinates and independently reviews completion"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "Not a scientific experiment; a pure external mapping can preserve canonical emission identity and timing without affecting neural computation."
  counter_hypothesis: "Required output observation needs a new neural primitive or labels/state mutation; stop rather than implement it."
  interfaces_relied_on: ["ExcursionEmission", "EventType.EXCURSION", "existing deterministic event ordering"]
  label_information_boundary: ["Truth is evaluator-only; adapter has no truth/label input; no feedback into neurons."]
  timing_assumptions: ["Logical event time only; inclusive evidence/deadline interval; finite complete scoring window."]
  reset_boundaries: ["Trial-local evaluator reset; emission IDs are namespaced by trial/window; no cross-trial learned state."]
  resource_bounds: ["One channel; one primary record; finite declared duplicate/event and identity capacities; no neural resource additions."]
  authorized_scope:
    - "experiments/task_output_interface.py"
    - "tests/test_luna60_task_output_interface.py"
    - "workflow/docs/luna/LUNA_60_TASK_OUTPUT_INTERFACE.md"
    - "workflow/handoffs/luna-60-binary-task-output-interface.md"
  unauthorized_scope: ["All other files; neural/runtime/classifier changes; training; rewards; eligibility; omission credit; benchmarks; efficacy; scientific replay; tuning; ACP promotion."]
  controls: ["Eight outcome fixtures; exact boundary checks; identical-input label swap; adapter enabled/disabled non-interference; boundedness and deterministic fixture repetition."]
  measurements: ["Fixture assertions only; frozen balanced-accuracy and separate timing/duplicate metrics; no efficacy measurements."]
  information_boundary_check: ["Output mapping cannot inspect truth, future input, neural state, amplitude, or historical outcome strata."]
  hardware_mapping: ["External observer/evaluator only; preserve source event identity/time; no backend or hardware equivalence claim."]
  architecture_invariants_touched: ["A01-A08, A11, A14-A15 preserved; no clause amendment."]
  preserves: ["Canonical emission, finite routing, numeric prediction/error, actual-activity eligibility and existing reward semantics."]
  architecture_change: false
  proposal: null
  files_changed: []
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All implementation and verification: not executed at authorization."]
  assumptions: ["Synthetic unit fixtures do not constitute a frozen scientific task or efficacy population."]
  unresolved: ["Scientific target construction, task times, population/splits, comparator, arms and budgets require later separate authorization."]
  recommended_next_agent: ["Luna-0: independent bounded interface review after Luna-60 handoff; no automatic scientific successor."]
```

Read `workflow/ARCHITECTURE_CONTRACT.md`, `ARCHITECTURE_CHANGELOG.md`,
`docs/luna/LUNA_WORKFLOW.md`, `docs/architecture/ACCEPTANCE_CRITERIA.md`,
`docs/architecture_proposals/README.md`, `ACP-TEMPLATE.md` and
`docs/luna/AGENT_HANDOFF_TEMPLATE.md` (all relative to `workflow/`).
Also read the three 2026-10-09 owner/Luna-59 handoffs named by the governance
handoff, the completed `LUNA_59_EVENT_DEADLINE_INTERFACE_DESIGN.md`,
ACP-0006 §§4–11, this contract and its Luna-0 authorization handoff.
The historical `tpcn-luna-workflow/` package is absent; use tracked `workflow/`.

## Frozen existing source and observation boundary

Exactly one task channel: `target-before-deadline`.
Exactly one designated source: neuron ID **`destination`**.
Observe **source emission time**, not routed arrival time. Map every actual
`ExcursionEmission` with `source == "destination"` and
`event_type == EventType.EXCURSION` to an affirmative task prediction.
Do not gate by payload sign, amplitude, state, lineage, target truth or
performance. Other nodes' emissions remain internal to the task; do not
disable their computation or routing. No synthetic negative output exists.

Source evidence at the baseline:

- `tpcn/excursion_neuron.py:251–284,631–667`: frozen emission record,
  delayed `_emit_ordinary` transition, ID `<neuron_id>:excursion:<sequence>`,
  source/time/sequence/lineage/episode; not a threshold or pending `S_EMIT`.
  Git blob: `c0bdece6b15009db4e2b7d69c3242be174b5de80`.
- `tpcn/experiment_excursion_runtime.py:554–589,635–661`: processing
  returns the canonical emission; `_consume_emission` already observes
  `(source,event_id,timestamp)` before existing consumers and finite routing.
  Git blob: `b4e074f0139f3fcfb59189c8313c934c551d6bcb`.
- `experiments/luna54/run.py:924–946,957–967`: existing governed neuron
  `destination`, `readout_sources=("destination",)` and canonical emission
  capture. Git blob: `08a95b44ddec1d2788d9a914b9653f86abd6d151`.
  This proves source availability only; do not run/modify that driver, adopt
  its classifier, reuse its samples as task labels, or select its parameters.

Implement a standalone downstream adapter accepting the existing immutable
canonical emission plus frozen trial/window metadata. No runtime hook or
runtime edit is needed for this prerequisite. Test the real canonical
emission path using short unit fixtures; do not instantiate or use the A–Z
classifier. Existing observer tuples are corroborating evidence, not a
license to fabricate missing canonical fields. A later application hookup
is not authorized here.

If this cannot be done using existing emissions, return
**TASK-OUTPUT SOURCE REQUIRES ARCHITECTURE DECISION** with the exact missing
primitive; do not substitute arrivals, hidden state, scalar predictor,
classifier output, new neural sink, or synthetic scoring events.

## Frozen binary record and inference boundary

`TaskPrediction` schema revision 1 contains:

- `trial_id`, `evaluation_window_id`;
- `channel_id = "target-before-deadline"`, `source_id = "destination"`;
- `prediction_event_id = emission.event_id`,
  `prediction_time = emission.timestamp`, `emission_sequence = emission.sequence`;
- `target_type = "designated-target-event"`, `predicts_occurrence = true`;
- stable `prediction_id` reconstructible without collisions from the tuple
  `(trial_id,evaluation_window_id,channel_id,prediction_event_id)`.

Copy identity/time exactly; do not create a native `Prediction` ID or reuse
a reward/eligibility identity as the task prediction identity. Preserve
canonical order, using source sequence to break equal emission times.
An exact re-observation of the same identity is not a new emission/duplicate;
conflicting content for an identity must fail clearly.

One frozen `TaskWindow` per trial reconstructs the record's meaning:
same trial/window/channel/target type, logical time unit,
`t_start <= t_evidence <= t_deadline < t_close`, all finite, and declared
finite observation/identity bounds. The complete scoring window is inclusive
`[t_start,t_close]`; `t_close` is a required finite external observation
boundary for distinguishing late output from silence. These ordering rules
are frozen now; numeric scientific values are not selected by this contract.
Unit-test values are only fixture constants, not task calibration.

Trial/window/source mapping is fixed before inference and any evaluation;
IDs and windows must not encode truth or be neural inputs. Only the evaluator
receives appropriately timed truth: whether the designated event occurred
in the trial's before-deadline target window, and actual occurrence time
when available. No label-based output selection. No global clock, polling,
target marker injected into neurons, new `EventType`, queued task event,
deadline/silence event, or state/threshold/routing/reward/eligibility change.
External finalization is a function over completed observations, not an event
in the neural queue. No target information enters the adapter.

## Frozen event-time scoring — all eight acceptance categories

The first distinct valid canonical task output in the scoring window is
primary, including a temporally incorrect pre-evidence output. Later distinct
outputs are duplicates, never replacements. Temporal validity is separate
from record validity: an early output must not be dropped as invalid data.

| Required category | Frozen evaluator result |
|---|---|
| On-time positive | First output in inclusive `[t_evidence,t_deadline]`: TRUE POSITIVE / ON-TIME. |
| Missed positive | No output through inclusive deadline: FALSE NEGATIVE. At complete close, if still no output, subtype SILENT/MISSED; never manufacture a prediction record. |
| Correct negative silence | No output through the entire inclusive scoring window: TRUE NEGATIVE only after verified completion. |
| False-positive negative | Any valid task output in the scoring window: FALSE POSITIVE, including early or post-deadline outputs; retain timing subtype separately. |
| Premature | First output `< t_evidence`: PREMATURE and incorrect. On a positive it counts FN for on-time sensitivity; on a negative it counts FP. A later on-time duplicate cannot rescue it. |
| Late | Positive first output `> t_deadline` and `<= t_close`: LATE, distinct from silence, and FN for on-time scoring. No-output-at-deadline FN is provisional as to subtype until close. |
| Duplicate | Each later distinct output retains its own TaskPrediction identity and is counted separately; primary outcome unchanged. No duplicate penalty/reward or credit semantics. |
| Ambiguous-prefix | Identical positive/negative prefixes end at `t_evidence`; prefix emissions `< t_evidence` are PREMATURE/incorrect. Verify equal prefix inputs yield identical mapped outputs regardless of external truth; continued negative silence is TN only at complete close. |

Duplicate and ambiguous-prefix are diagnostic categories, not extra confusion
matrix cells. An emission exactly at evidence or deadline is on-time for a
positive; one exactly at close is still scored. Equal-time events retain
canonical order, not label order. An emission outside the scoring window is
reported separately as out-of-window and never reassigned to another trial.
No pre-evidence or late error becomes correct retroactively.

Incomplete observation, pending due work, truncation or capacity exhaustion
must be explicit INCOMPLETE/CENSORED, not scored silence, TP/TN success or
evidence of efficacy. Verify completeness through deadline/close from the
external fixture driver, never by advancing neurons on a synthetic tick.
No output means evaluator inference only: no silence neuron, event,
prediction identity, eligibility trace, reward recipient or omission credit.

## Metrics and finite observation

For complete trials use exactly one confusion-matrix contribution per trial:
positive on-time primary = TP, every other positive = FN;
negative silence through close = TN, every emitting negative = FP.
`balanced_accuracy = (TP/(TP+FN) + TN/(TN+FP))/2`;
`FNR=FN/(TP+FN)`, `FPR=FP/(TN+FP)`, `TPR=TP/(TP+FN)`.
Undefined denominators must be explicit N/A, not fabricated zero/perfect
scores; report excluded incomplete trials and denominators.

Retain premature, late, silent-miss, out-of-window and duplicate counts,
first-emission timing, `deadline_lead_time = t_deadline - prediction_time`,
and target-relative lead time `t_target - prediction_time` only where an
actual target and emission both exist. Negative/absent lead times are N/A;
no imputed emission timestamp. Report signed timing and conditional sample
counts. No efficiency penalty formula, reward scalar or optimization.
Prior owner +10 pp balanced-accuracy / <=+5 pp FPR efficacy criteria remain
future gates, not acceptance scores for unit fixtures.

Require explicit finite per-trial emission and identity capacities, bounded
identifier lengths and a bounded current-trial accumulator; retain one primary
plus duplicate counters and only bounded optional detail. Validate order,
unique identities, finite times, reset and window metadata. Observation
overflow marks evaluation incomplete without mutating/backpressuring neural
execution; no global unbounded registry. Flush/reset evaluator state at trial
close; never infer cross-trial learning or change canonical reset behavior.

## Verification, exclusions and handoff

Future Luna-60 may implement only the four owned files and execute focused
unit/regression tests for this interface. Required fixtures: all eight rows,
both inclusive equality boundaries, close equality, complete versus censored
silence, first premature/late followed by an on-time duplicate, internal
non-designated emissions, signed-payload independence, identity collision/
re-observation/order/reset/bound rejection, and zero-denominator metrics.

Include at least one actual canonical emission obtained through the existing
delayed neuron event path. Handcrafted immutable emissions for evaluator
boundary unit tests must be labeled fixtures, never injected as neural scoring
events or presented as scientific outputs. Repeat fixtures deterministically.
Adapter enabled/disabled and evaluator truth-swapped identical-input fixtures
must preserve emission identities/times, neural state, pending events,
routing and any native prediction/error/eligibility/reward state exercised.
Where not exercised, mark those checks N/A rather than claiming they pass.
Evaluator-only facts may change scores, never outputs or neural state.

Record focused tests, relevant existing excursion/runtime regressions, full
regression where applicable, syntax/static/editor diagnostics and whitespace
checks with exact revision/environment/commands. Do not silently repair any
pre-existing failure; report it. No experiment, benchmark, scientific replay,
historical artifact evaluation, task efficacy, generator/dataset production,
parameter/threshold/rate/gain search, source selection by held-out score,
classifier/prototype training, structural growth/pruning, reward changes,
duplicate penalty, silence/omission credit, hardware implementation,
calibration, ACP or A01-A15 promotion is authorized.

Complete the repository handoff template in the owned handoff and document
the implemented schema, source pins, fixtures and procedures in the owned
interface document. Distinguish OBSERVED / INFERRED / HYPOTHESIZED; passed /
failed / not-run / N/A; changed/unchanged behavior; boundedness; limitations;
and promotion boundary. Stop for independent Luna-0 review. Passing interface
fixtures does not authorize a task study, efficacy claim or trained learner.
