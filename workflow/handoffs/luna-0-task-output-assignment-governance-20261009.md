# Luna-0 governance — task-output assignment and fixed-behavior viability

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-60 follow-up and task-output assignment decision"
  task_id: "luna-0-task-output-assignment-governance-20261009"
  component: "Fixed/no-training event/deadline viability and next bounded prerequisite"
  status: "complete; Luna-61 design prerequisite authorized, not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "dab2600680c1ef1c7e0c21747681bc16b2a72e99"
  result_revision: "this governance publication commit; exact SHA available from git log"
  dependencies:
    - "Luna-60 published authorization, implementation, final publication and independent review"
    - "Luna-59 event/deadline interface design and owner objective"
    - "Current architecture contract and accepted ACP-0006"
    - "Retained Luna-53/54/55/58 mechanism records"
  owner: "Project owner; Luna-0 records compatibility and bounded authorization"
  classification: ["READ-ONLY REVIEW", "GOVERNANCE"]
  hypothesis: "Luna-60's correct evaluator does not itself make the frozen destination output task-relevant; an independent task/target assignment is still required before fixed behavior or task learning can be interpreted."
  counter_hypothesis: "An existing independently defined event/deadline fixture already gives destination emissions a causal task meaning with an independently frozen configuration."
  interfaces_relied_on: ["Luna-60 TaskPrediction and TaskEvaluator", "ExcursionEmission", "ACP-0006 readout/prediction/eligibility/reward boundaries"]
  label_information_boundary: ["No task labels or targets entered neural execution in this review; all candidate task semantics remain external and unapproved."]
  timing_assumptions: ["Event-time only; no numeric task windows inferred from historical settling or mechanism times."]
  reset_boundaries: ["No execution; future task reset/split rules remain to be defined independently."]
  resource_bounds: ["Read-only repository inspection; one bounded documentation-only Luna-61 assignment."]
  authorized_scope:
    - "Verify current origin/main and Luna-60 publication chain."
    - "Inspect Luna-60 output/evaluator, relevant task and mechanism fixtures, ACP-0006 reward boundaries, and retained evidence."
    - "Create Luna-61 design contract, this governance handoff, and additive workflow/changelog status."
    - "Correct the Luna-60 handoff's mistyped implementation SHA with an explicit erratum."
  unauthorized_scope:
    - "Any task execution, generator/data creation, score calculation, training, tuning, arm selection or efficacy."
    - "Any source/readout substitution, runtime/reward/eligibility/code change, ACP or architecture-contract amendment."
    - "Any task-study authorization or automatic Luna-62."
  controls:
    - "Fetched origin; verified clean main, HEAD == origin/main, and Luna-60 authorization/publication ancestry."
    - "Inspected Luna-60 module and frozen source; confirmed downstream interfaces do not import or mutate runtime state."
    - "Compared actual retained task fixtures and historical mechanism roles; did not run them."
    - "Resolved incorrect implementation SHA in Luna-60 handoff against git object history."
  measurements:
    - "No scientific/task measurements."
    - "Read-only observations of source roles, existing fixture semantics and public credit interfaces only."
  information_boundary_check: ["No task truth was used as a neural input or passed into a runner; no task was generated or scored."]
  hardware_mapping: ["No hardware work or equivalence claim."]
  architecture_invariants_touched: ["A01-A08 and A11 preserved; no A01-A15 or ACP change."]
  preserves:
    - "Luna-60 PASS status and destination -> target-before-deadline mapping."
    - "ACP-0006 actual-emission-only eligibility and current unmatched-silence boundary."
    - "ACP-0008 remains experimental, opt-in and disabled by default."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-61.agent.md"
    - "workflow/handoffs/luna-0-task-output-assignment-governance-20261009.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-60-binary-task-output-interface.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All Python tests, experiments, fixture runs, data generation, task scoring and training; not authorized and not needed for governance."
    - "Hardware and full scientific replication; not run."
  assumptions:
    - "The latest published repository is the authority; historical reports are not presumed correct where Git objects disagree."
    - "A design recommendation is not owner approval of a future task or learning rule."
  unresolved:
    - "Concrete independent target event, task generator, population/splits, exact time windows, comparator and arms."
    - "Whether task-specific training is needed and whether a separately governed outcome-to-credit bridge is justified."
  recommended_next_agent:
    - "Luna-61: execute only the documentation-only assignment design, then stop for Luna-0 review."
    - "Project owner: any later task or training/efficacy work requires a separate explicit decision."
```

## Outcome and disposition

**TASK EFFICACY STILL NOT BOUNDED. LUNA-61 TASK-OUTPUT ASSIGNMENT DESIGN
PREREQUISITE AUTHORIZED — NOT EXECUTED.**

The Luna-60 interface is established and independently reviewed. It proves
that an actual canonical `destination` `EXCURSION` emission can be represented
as an affirmative `target-before-deadline` prediction and scored downstream.
It does not establish that the source has a task-specific meaning, predicts
an independently defined future target, or should emit selectively on
positive trials.

No fixed/no-training task evaluation is authorized. The currently described
destination is a terminal neuron in retained relay/destination mechanism
studies. It integrates propagated relay events and emits when its existing
neural dynamics produce a canonical excursion. The retained Luna-53/54/55/58
experiments study integration, discharge, retention, route and mechanism
strata; their target/control labels are downstream analysis of those
mechanism questions, not an independently defined event/deadline task.
The source was chosen for the task-output interface as the existing endpoint
of that causal mechanism path, not because it already encoded a task class.
Defining positive trials as those that cause this emission would be circular.

### Luna-60 N/A follow-up

**NON-BLOCKING BY CONSTRUCTION.** `experiments/task_output_interface.py`
accepts an immutable already-materialized `ExcursionEmission` and window
metadata. The adapter maps fields into a frozen task record; the evaluator
stores external records and computes outcomes. Neither imports nor receives
the runtime, topology, predictor, eligibility ledger or reward system, and
neither schedules, routes or delivers events. The Luna-60 real delayed-path
fixture verifies unchanged canonical emissions, neuron state, pending event
and queue state with the adapter enabled/disabled. Routing/native
prediction-error/eligibility/reward were not exercised, correctly recorded
N/A. Static interface isolation gives no reason to authorize a separate
test-only Luna to convert those checks to PASS.

### Existing task and learning evidence

- **OBSERVED:** Luna-13C's fixed external `on_time`/`late` targets and causal
  graph intervention are a small topology-utility fixture. It scores a
  constructed target-arrival decision, not canonical destination task-output
  emissions; it is not a held-out temporal event/deadline population.
- **OBSERVED:** Luna-12J tests temporal-association effects on four-class
  spiral classification, including historical `TANH_LEGACY` classifier
  paths. It is not the owner’s binary event/deadline task and does not assign
  destination emissions to an independent target.
- **OBSERVED:** Luna-53/54/55/58 use retained source/relay/destination event
  sequences to test bounded mechanism response. Their outcomes/strata are
  mechanism evidence; none defines a task target occurring independently
  before a fixed deadline.
- **OBSERVED:** ACP-0006 supports bounded eligibility for actual emitted
  activity and delayed credit addressed to extant IDs. Integrated external
  reward is tied to the first actual readout emission and is unmatched when
  no readout emission exists. It does not provide task-specific
  event/deadline assignment, omission error, or a credit identity for silence.
  The Luna-60 task record is external and is not a native predictor/reward ID.

**INFERRED:** a fixed evaluation could mechanically report metrics after a
task is invented, but without an independently governed target generator and
causal relationship to the frozen output, that score would not answer a
scientifically justified question about this network. Conversely, requiring
task training now is also premature: target semantics, input representation,
trial construction and target-to-credit attribution have not been frozen.
Emission-only reward may support a later narrow emitted-event learning study,
but not a full claim about correct silence or missed positives without
separate governed semantics.

`IntegrationConfig(decay_rate_z=0.00001)` from Luna-58 is not justified as a
task arm. No task parameters, thresholds, task times, output sources,
comparators, or effect claims are selected by this pass.

## Architecture evidence and decision

- A01-A03: future task must remain event-time causal; no deadline is inferred
  from settling horizon or global tick.
- A04/A08: no new state or runtime path is authorized here.
- A06-A07/A11: task prediction remains distinct from native numeric
  prediction/error and actual-emission local credit; labels stay external.
- A09-A10: no reward/energy formula or calibrated activity proxy is selected.
- A12-A13 remain optional; A14-A15 are not changed or newly certified.

No ACP is indicated: this review does not propose a core architectural
departure. If the future task requires a new neural output or omission-credit
primitive, stop for project-owner architecture governance rather than
implementing it implicitly.

The only justified immediate step is the bounded **documentation-only**
Luna-61 task-output assignment/viability design. It must inspect existing
fixtures, identify whether any independent non-circular target construction
is supportable, and distinguish a future fixed-behavior test from task
training. It may recommend that the output assignment is not supportable and
name the minimum owner decision instead of inventing a target. It cannot
generate data, run trials or authorize a scientific successor.

## Validation record

| Procedure | Revision / environment | Result |
|---|---|---|
| `git fetch origin`; status, branch, `HEAD`, `origin/main` | Windows; repository checkout | **PASS:** `main`, clean; `HEAD == origin/main == dab2600680c1ef1c7e0c21747681bc16b2a72e99`. |
| Ancestry checks for Luna-60 authorization and final publication | Same checkout | **PASS:** authorization `b1d8cc16261ea077b9d3b7c7cb24c975e4c721ee` and publication `dab2600680c1ef1c7e0c21747681bc16b2a72e99` are ancestors. Actual implementation commit is `fff8394807573f506cc7e42cdc4d40bca0d958f5`. |
| Read-only inspection of Luna-60 module/tests/handoff, Luna-59 design, ACP-0006, Luna-13C, Luna-12J and Luna-53/54/55/58 records | Same published revision | **PASS:** source/output, fixture and reward-scope evidence summarized above; no project code or science executed. |
| Task evaluation, data generation, training, efficacy, parameter selection, hardware validation | Not run | **NOT RUN / NOT AUTHORIZED.** |
| Tests for documentation/governance edits | Not run | **NOT APPLICABLE**; no executable source changed. |

### Publication identity correction

The Luna-60 completion handoff had a mistyped `result_revision`:
`fff83941e71372784cd962bdd5f9f645ab83d301` does not resolve to a Git commit.
The actual implementation commit is
`fff8394807573f506cc7e42cdc4d40bca0d958f5`, parented by the published
authorization commit. The final Luna-60 publication remains
`dab2600680c1ef1c7e0c21747681bc16b2a72e99`. The Luna-60 handoff is corrected
by this governance pass; no source/result contents changed.

## Assumptions, limitations and unresolved issues

The governing owner decision fixes the output channel and binary prediction
semantics but does not define the external target event, temporal task
generator, target schedule, held-out population, or justified configuration
arms. Historical mechanism traces cannot supply these by relabeling.
No data generator, task score, task feasibility result or causal efficacy
claim was produced.

## Next assignment

**Luna-61**, only after this governance publication is verified:
documentation-only task-output assignment and fixed-behavior viability
design under `.github/agents/luna-61.agent.md`, with exactly two owned
deliverables. Then stop for independent Luna-0 review. No task study,
training, reward change, omission credit, Luna-62 or efficacy authorization
is implied.
