---
tpcn_handoff:
  agent: "Luna-59"
  luna_identifier: "Luna-59"
  descriptive_name: "Event/deadline reward-interface design prerequisite"
  task_id: "luna-59-event-deadline-interface-design"
  component: "Documentation-only task-output and delayed-credit interface design"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "b0d62765534c54947e84d53677fb65824aff4b07"
  result_revision: "uncommitted documentation changes"
  dependencies:
    - "Published authorization contract at origin/main b0d62765534c54947e84d53677fb65824aff4b07"
    - "Luna-3 predictive-coding interface as described by ACP-0006 and current source"
    - "Luna-8 local eligibility/reward interface as described by ACP-0006 and current source"
    - "Luna-5 reward/energy boundary; coordination requested before any cross-component implementation"
  owner: "Project owner; Luna-0 arbitrates interfaces and ACP governance"
  classification:
    - "documentation-only proposed interface design"
    - "design prerequisite complete; task-efficacy experiment not authorized"
    - "no experiment arms, parameter search, task values, or reward semantics selected"
  hypothesis: "not applicable - no experiment"
  counter_hypothesis: "not applicable - no experiment"
  interfaces_relied_on:
    - "ExcursionEmission and EventType.EXCURSION as actual canonical output events"
    - "LocalPredictor Prediction IDs, target keys, timestamps, expiry, Observation and explicit PredictionError"
    - "EligibilityActivity, EligibilityTrace, RewardSignal and bounded EligibilityLedger"
    - "Bounded event queue, deterministic tie ordering, finite topology delay and character reset"
    - "A–Z StreamingCharacterClassifier, ACTIVITY_EVENT and END_CHARACTER as current non-task-specific readout"
    - "Luna-5 activity-cost-proxy metering and explicit reward-adjusted utility boundary"
  label_information_boundary:
    - "Proposed task labels, targets and outcome decisions remain downstream-only until a separately approved reward boundary."
    - "No label, target marker, task ID encoding, or synthetic silence event is proposed as a neural input."
    - "Native numeric Prediction/PredictionError remains distinct from task event/deadline outcome."
  timing_assumptions:
    - "All proposed task times are logical event timestamps; no global neural clock or wall-clock polling."
    - "Proposed event/deadline equality uses the actual deterministic timestamp/sequence order; task values and the final tie policy remain owner decisions."
    - "A routed output is observed only after emission and cumulative finite route delays."
  reset_boundaries:
    - "Proposed trial-local queue, predictor, eligibility, reward-ID, readout and evaluator scratch reset; only owner-approved frozen configuration may persist."
    - "No cross-trial or cross-split learned state for the fixed/no-training disposition."
    - "No reset or runtime policy was implemented or exercised."
  resource_bounds:
    - "No new state or capacity introduced."
    - "Observed integrated-runtime ledger defaults: max_reward_identities=64, decay_time_constant=4.0, trace_limit=1.0, credit_limit=1.0, expiry=None; default max_traces=prediction_capacity * neuron_count."
    - "Historical Luna-54 configuration only: eligibility_capacity_per_ledger=1024, prediction_capacity=8, prediction_expiry=4.0, queue_capacity=128, runtime_event_budget=1024, per-neuron event budget=4096, settling_horizon=4.0; not task selections."
    - "Reward payload is a finite scalar with no task-unit contract in the reviewed ACP; energy uses activity-cost-proxy, not calibrated joules."
    - "Future task event/output/ledger capacities, expiry, reward units and overflow require a separate owner-approved contract."
  authorized_scope:
    - "Write workflow/docs/luna/LUNA_59_EVENT_DEADLINE_INTERFACE_DESIGN.md."
    - "Write workflow/handoffs/luna-59-event-deadline-interface-design.md from the repository handoff template."
    - "Read-only inspection of authoritative docs, ACPs, source, tests, configurations and retained artifacts."
    - "Provide two dispositions, exactly eight logical outcome cases, compatibility findings, owner decisions, anti-shortcut requirements and stop-on-missing-interface."
  unauthorized_scope:
    - "Any code, test, runner, configuration, dataset, artifact, ACP, architecture contract, changelog, or workflow-body change."
    - "Runtime execution, fixture execution, scientific replay, benchmark, simulation, experiment, parameter calculation/search, or tuning."
    - "Selecting any efficacy arm, numerical task value, rate, threshold, or Luna-58 destination value."
    - "Creating omission credit, silent-state eligibility, reward broadcast, global registry, or unreviewed task-learning semantics."
  controls:
    - "Design requirements only: identical ambiguous prefixes; no class-coded ID/marker/amplitude/count/duration; matched order/gap controls; independently specified timing-destroyed/reversed outcomes; no target influence before scored prediction; causal route/component intervention; label-swapped identical-input non-interference; reset/split isolation."
    - "No control trial or experiment was executed."
  measurements:
    - "Read-only compatibility findings from source/ACP/test/config/artifact inspection only."
    - "Preserved owner metric: held-out balanced accuracy, >= +10 percentage points versus predeclared comparator, <= +5 percentage points FPR degradation, majority declared-seed direction if stochastic or exact independent replay if deterministic."
    - "No scientific samples or efficacy, benchmark, energy, hardware or task metric were measured."
  information_boundary_check:
    - "PASS by document review: proposed task target/outcome remains downstream; no target/label/silence is introduced into neural inputs."
    - "Current task-output and absence-attribution interfaces are explicitly classified NOT SUPPORTED or unresolved rather than bridged."
  hardware_mapping:
    - "Conceptual only: preserve event identity, payload, local timestamps, finite queue/route and bounded ledger semantics; no FPGA/FPAA/hybrid validation."
  architecture_invariants_touched:
    - "No architecture clause, ACP, runtime or implementation changed."
    - "Design relies on A01-A08, A09-A11 and A15 as applicable; optional A12/A13 are not promoted or made requirements."
  preserves:
    - "Luna-3 local prediction IDs/timestamps, explicit PredictionError events, bounded outstanding state and causal routing."
    - "Luna-8 actual-activity-only eligibility and explicit unmatched/expired outcomes."
    - "Luna-5 reward/energy separation and activity-cost-proxy boundary; coordination remains required."
    - "Owner metrics, open task/split/numeric decisions, no authorized arms, no automatic Luna-58 rate adoption, and separate pending Luna-58 review."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_59_EVENT_DEADLINE_INTERFACE_DESIGN.md"
    - "workflow/handoffs/luna-59-event-deadline-interface-design.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All runtime tests, unit tests, fixtures, simulations, scientific replays, benchmarks and artifact execution: not run; explicitly prohibited by this dispatch."
    - "Full suite and Luna-11 verification: not run; outside scope."
    - "FPGA/VHDL/FPAA/hybrid validation: not run."
  assumptions:
    - "The fetched published contract and owner-objective restatement are authoritative; no separate owner attachment beyond the recorded restatement was available in the reviewed sources."
    - "All task timing rules in the design are proposals, not existing runtime behavior."
    - "No task parameter, numerical rate, reward unit, penalty formula, or arm was selected from retained data."
  unresolved:
    - "Owner decision on source-emission versus routed-arrival observation point and output sink."
    - "Target/event schedule, eligible interval/deadline/close, equality order and absence resolution."
    - "Fixed/no-training versus governed-training disposition and, if needed, governed task-outcome-to-credit interface/ACP decision."
    - "Trial generator, independent outcome rule, splits/population/counts/repetitions, nuisances, comparator, arms, budgets, scoring and duplicate penalty."
    - "Luna-5 reward/energy interface review and Luna-3 native prediction-interface confirmation if reused."
    - "Independent Luna-58 review remains separate and open if relied on."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian and project owner: review the proposed output boundary, eight case rules, no-training/training choice, missing-interface findings, task/split metrics and open ACP boundary; no experiment or implementation is authorized by this handoff."
---

# Luna-59 event/deadline interface design — handoff

## Outcome and owned scope

**COMPLETE — documentation-only design prerequisite.** The two authorized
documents are the only intended changes. They describe a proposed observable
task-output mapping, distinguish actual emission/routed arrival/native
prediction/native error/evaluator outcome, provide the required eight
logical outcome cases, compare exactly two dispositions (fixed/no-training
and governed training), and record compatibility, owner decisions,
anti-shortcut constraints and stop-on-missing-interface behavior.

No semantics were implemented, adopted, or promoted. No architecture,
runtime, ACP, workflow/changelog, test, runner, configuration, dataset or
artifact was edited. No commit or push was made; Luna-0 retains publication
authority.

## Architecture evidence

- **OBSERVED:** Current canonical eligibility starts only from actual local
  activity; ACP-0006 §7 excludes silent accumulator changes and explicitly
  leaves absent first-readout-emission reward unmatched.
- **OBSERVED:** Native prediction/error is numeric next-input forecasting
  with local prediction identity and later causal observation; expiry does
  not create omission error (ACP-0006 §§5–6).
- **OBSERVED:** The event runtime provides finite queued delivery and
  deterministic timestamp/sequence order. ACP-0008 is opt-in, disabled by
  default, and does not modify reward/eligibility/prediction semantics.
- **INFERRED:** Current interfaces do not identify a task output/deadline,
  decide absence, or provide fair task-recipient attribution for all eight
  logical outcomes.
- **PROPOSED:** Downstream-only output observation and task-outcome boundary
  with existing actual event identities; any missing event/reward route or
  silence recipient stops for owner/Luna-0 review. No ACP is drafted.
- A01–A15 text and status are unchanged; optional A12/A13 remain optional.
  No integration, efficacy, energy, hardware, Luna-11, or production gate
  is claimed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `git ls-remote origin refs/heads/main` | Repository `zathp/TPCN`; Windows_NT; seed N/A | `origin/main` returned `b0d62765534c54947e84d53677fb65824aff4b07` | Read-only command output |
| `git rev-parse HEAD; git rev-parse origin/main; git status --short; git diff --check` before edits | Windows_NT checkout; no interpreter or seed | `HEAD` and `origin/main` both equal authorization SHA; clean before edits; baseline diff check clean | Read-only command output |
| Read authoritative contract, Luna-59 authorization, workflow, acceptance criteria, ACP-0006/0008, source/tests, configs and retained Luna-45/55/58 evidence | Revision `b0d62765534c54947e84d53677fb65824aff4b07`; read-only | Reviewed; no source/test/artifact execution | Source paths cited in design |
| Post-edit review of the two authorized documents; `git diff --check`; `git diff --no-index --check -- NUL <each authorized document>` | Windows_NT; no interpreter or seed; uncommitted docs | Both documents reviewed; no whitespace diagnostics. The no-index checks return 1 for content differences and emit no whitespace-error output; ordinary `git diff --check` is clean. Only the two authorized documents appear in `git status --short`. | Read-only document review and command output |

## Benchmark and resource results

Not applicable; no benchmark, sample, trial, execution, parameter
calculation, replay, task metric or resource measurement was run. Seed is
not applicable. Historical trace/credit/runtime bounds and scalar reward
handling are recorded in the design and `resource_bounds` solely as
compatibility context; no task unit, value, setting or utility assumption is
selected. Owner metrics are preserved as requirements, not reported as
outcomes. Retained Luna-45/55/58 mechanism values are documented only as
distinct historical configuration contexts; no task arm or rate is selected.

## Assumptions, limitations and unresolved issues

All event/deadline semantics in the design are proposals, not existing
behavior. The current governed interface does not establish the event-output
observation boundary, target schedule/deadline, silence-resolution event,
task reward recipient, task-specific duplication penalty, or fairness rule
for all eight cases. No omission credit is invented. The owner decision
source reviewed here is the published objective restatement; no separate
owner attachment was available, and no claim is made to have read one.
Luna-58’s independent review remains separate and pending if relied upon.

## Reproduction and rollback

No code or scientific state changed. No rollback is required. The two
documentation edits remain uncommitted and unpublished; the authorized
baseline is `b0d62765534c54947e84d53677fb65824aff4b07`. Preserve unrelated
working-tree changes. Do not commit or push; Luna-0 owns publication.

## Next assignment

Project owner and Luna-0 should review the two documents, decide the output
observation point and task contract, choose no-training or separately
governed training, and resolve missing attribution/energy decisions. A
future experiment requires its own complete authorization after all gates
close. Stop here: zero experiments, code changes, tests, runtime execution,
or scientific execution.
