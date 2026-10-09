# Luna-59 — Event/Deadline Reward-Interface Design

**Disposition:** Documentation-only design prerequisite complete; proposed
interfaces and compatibility findings only. Not an efficacy experiment, an
implementation, an ACP, or architecture approval.

**Authority checked:** `origin/main` resolved to
`b0d62765534c54947e84d53677fb65824aff4b07`; local `HEAD` and `origin/main`
were both that revision and the working tree was clean before these edits.

**Scope:** This design and its handoff only. No execution, code/test/config/
artifact/ACP/architecture change, reward-rule adoption, experiment arm, or
parameter selection is authorized.

## 1. Evidence and status vocabulary

- **OBSERVED** means directly stated in a reviewed source file or retained
  record at the authorized revision. It does not mean tested or newly
  reproduced in this task.
- **INFERRED** means a compatibility consequence of observed interfaces.
- **PROPOSED** marks a design suggestion requiring owner/Luna-0 review; it is
  not existing behavior.
- **UNKNOWN / NOT SUPPORTED** marks a task-facing interface or decision that
  the current sources do not establish. Do not bridge it by implementation.

### Read-only evidence reviewed

**OBSERVED:** ACP-0006 sections 5–11 describe the numeric next-input
prediction boundary, explicit later-observation errors, actual-emission-only
eligibility, readout silence, first-readout-emission reward attribution,
finite settling, and reset boundaries. ACP-0008 remains opt-in and disabled
by default; it does not change prediction, error, eligibility, or reward
semantics. A01–A15 and the acceptance criteria remain authoritative.

**OBSERVED:** `tpcn/excursion_neuron.py` represents a canonical emission as
`ExcursionEmission(event_id, sequence, source, timestamp, payload,
lineage_id, episode_id, event_type=EXCURSION)`. The event is created after
the neuron’s delayed emission transition; a threshold/discharge or an
internal pending event is not itself that canonical output.
`tpcn/event_runtime.py` orders queued work by logical timestamp and
deterministic sequence, applies finite propagation delay, and does not mutate
a remote destination inline.

**OBSERVED:** `tpcn/predictive_coding.py` stores bounded local numeric
predictions with IDs, target keys, creation timestamps, optional
`expected_resolution_at` and expiry. An observation at the same target key
can match the oldest eligible prediction and produce a signed
`PredictionError` at observation time. `expected_resolution_at` is metadata;
it does not define a task deadline. `expire()` removes an unresolved record;
expiry does not itself create a missed-event error. Generic
`emit_prediction()` can enqueue `PREDICTION_EVENT`, but ACP-0006 says the
integrated adapter does not use it for the task-output path.

**OBSERVED:** `tpcn/eligibility.py` bounds trace count, trace/credit values,
expiry (when configured), and retained reward IDs. A trace is created from
an addressed `EligibilityActivity`; reward/error application identifies an
existing trace by `trace_id` or `prediction_id`. An unmatched signal returns
`unmatched` without trace mutation; a signal that decays/removes a formerly
matching trace returns `expired`. Distinct reward IDs are independent;
duplicate IDs within the bounded retention window are no-ops.

**OBSERVED configuration context, not a task selection:** the integrated
runtime creates local ledgers with `decay_time_constant=4.0`,
`trace_limit=1.0`, `credit_limit=1.0`, no expiry unless configured, and
`max_reward_identities=64`; its default trace capacity is
`prediction_capacity * neuron_count`. The reviewed Luna-54 frozen runtime
configuration explicitly used `eligibility_capacity_per_ledger=1024`,
`prediction_capacity=8`, `prediction_expiry=4.0`, queue capacity 128,
runtime event budget 1,024, per-neuron event budget 4,096, and settling
horizon 4.0. These describe that retained mechanism configuration only.
They are not proposed task bounds, a universal default, or a basis for
selecting a future trace/expiry/reward setting.

**OBSERVED:** `tpcn/experiment_excursion_runtime.py` creates task-independent
numeric prediction records and eligibility traces while consuming actual
emissions. It projects actual readout-source emissions into
`ACTIVITY_EVENT`; it does not create an activity event for silence. At
`end_character`, the existing outer reward is derived after the classifier
result, addresses only the first actual readout-source emission trace, and
is applied to that local ledger. If there is no readout emission, credit is
explicitly unmatched. This is not a task-deadline outcome interface.

**OBSERVED:** `tpcn/streaming_classifier.py` implements a bounded A–Z
character readout finalized at `END_CHARACTER`; it is not an event/deadline
task evaluator. `tpcn/experiments.py` keeps labels outside the canonical
event stream until the label-free readout exists, then uses them in the
outer reward/prototype path. `tpcn/energy_utility.py` declares
`activity-cost-proxy` units and separates local energy metering from
reward-adjusted utility; neither is calibrated physical energy. Reward
payloads are finite scalar values, but the reviewed ACP does not assign a
task reward unit or a permanent utility equation. The Luna-54 configuration's
`neutral_reward=0.0` and `reward_delay=0.0` are historical mechanism settings,
not proposed task reward units, delay, or defaults.

**OBSERVED:** The Luna-58 handoff, configuration, and retained summary
describe bounded ACP-0008 mechanism evidence only. Its `0.00001` destination
rate is not an event/deadline task parameter and is not selected here.
Luna-55’s HH/RH/HR/RR configurations, Luna-54’s runtime limits, and the
frozen Luna-45 configuration are distinct historical mechanism contexts, not
task arms or a task-scale calibration.

**Not performed:** No source execution, test, artifact verification,
simulation, scientific replay, parameter calculation/search, benchmark,
dataset generation, or efficacy measurement. The cited existing tests
(`tests/test_predictive_coding.py`, `tests/test_eligibility.py`, and the
Luna-58 focused test) were read as evidence of their intended public
interfaces only; they were not run.

## 2. Proposed event/deadline interface

This section defines a candidate contract for owner review. It does not say
the project currently has these task events or task semantics.

### 2.1 Event identities and observation point

**PROPOSED:** Count a task output only when a designated downstream
evaluation boundary observes an actual canonical `EXCURSION` event from a
predeclared output source. Do not infer an output from membrane/integration
state, an internal discharge, an `S_EMIT` scheduling record, an activity
aggregate, a native scalar prediction, or the absence of an event.

The observation record should preserve, without rewriting:

| Field | Proposed meaning |
|---|---|
| `source` | The emitting neuron/source already carried by the canonical event. |
| `destination` | The predeclared output observation boundary; current code does not define a task-output port. |
| `event_type` | Actual `EXCURSION`; not a synthetic task-specific neural event. |
| `payload` | The actual signed canonical emission payload. |
| `event_id` | The canonical emission’s stable identity; do not make a prediction ID from silence. |
| `lineage_id` | Preserve when available; do not use truncated lineage as proof that all causal work is known. |
| `emission_timestamp` | Timestamp of the canonical emission at its source. |
| `observation_timestamp` | Timestamp the event reaches the chosen evaluator boundary. If a routed boundary is chosen, it is emission time plus the actual cumulative edge delays. |
| `trial_token` | Opaque evaluator-side association only; never encode class, target, or outcome in a neural input or event identity. |

**UNKNOWN / NOT SUPPORTED:** There is no current public task-output port or
decision specifying whether the scored event is (a) a source emission
observed downstream at emission time or (b) an actual routed arrival at a
declared output sink. This must be chosen before task construction. The
candidate above uses an observation boundary and preserves both source
emission time and boundary-arrival time, so end-to-end timing cannot hide
propagation delay. If the boundary cannot observe a real routed event, stop;
do not fabricate a sink arrival.

### 2.2 Source events are not target events

**PROPOSED:** The positive target event/time and its independent trial
schedule belong only to the external task generator/evaluator. A target is
not sent to the TPCN as an input, `Observation`, prediction match, eligibility
record, or reward before the task’s declared outcome-resolution boundary.
Negative/ambiguous trial status is likewise evaluator-only until an
authorized causal reward decision is made.

The terms must remain distinct:

1. **Discharge/state crossing:** local neuron-state behavior; not an
   externally scored output.
2. **Canonical emission:** actual `ExcursionEmission` / `EXCURSION` with
   source, payload, event identity, lineage and emission timestamp.
3. **Queued/routed event:** the same causal signal in the finite topology;
   each arrival follows its declared edge delay. A multi-hop path’s arrival
   is not the original emission timestamp.
4. **Native prediction:** `Prediction`/optional `PREDICTION_EVENT` for a
   configured scalar target; not the task event output.
5. **Native prediction error:** explicit `PREDICTION_ERROR_EVENT` only after
   a later observation matches a native prediction; not the task’s positive,
   negative, omission, early, late, or duplicate score.
6. **Evaluator outcome:** downstream-only decision made under the frozen
   task schedule; not a neural output or evidence that a silent neuron
   emitted.

For a routed output to be before a positive target, the causal requirement
would be
`t_discharge <= t_emission < t_observation < t_target` in the evaluator’s
declared total order. In a path with positive emission and route delays,
`t_observation = t_discharge + emission_delay + sum(path_edge_delays)`;
therefore a source discharge before the target alone is insufficient.
This is a causal feasibility condition, not a measured capability or
selected task horizon.

### 2.3 Proposed time windows and deterministic boundaries

Let `t_start`, `t_ambiguous_end`, `t_open`, `t_target`, `t_deadline`, and
`t_close` be logical event times from a frozen trial contract. **All values,
units, schedules, and their relation to one another remain unresolved.**
No rate, horizon, input scale, threshold, or window is selected from
Luna-45/55/58 data.

**PROPOSED boundary policy:** the ambiguous prefix is
`[t_start, t_ambiguous_end)`; task eligibility is
`[t_open, t_deadline]`; a first output before `t_open` is premature, and one
after `t_deadline` but no later than `t_close` is late. Timestamp equality
at `t_ambiguous_end` is outside the ambiguous prefix. Timestamp equality at
`t_open` is eligible. At `t_deadline`, an output counts on time only if its
actual queued event is observed before the evaluator’s deadline-close
marker in the canonical `(timestamp, queue sequence)` order; otherwise the
deadline has already closed. A same-time target/output comparison must use
the same declared event ordering, and a predictive success must precede the
target marker; the target marker is never delivered into the neural path.

The runtime’s existing deterministic event ordering is evidence for
repeatable event ordering, not proof that a task evaluator already implements
this boundary policy. The owner must decide whether the positive deadline is
strictly before the target or may coincide with it, and approve/revise the
proposed tie rule.

`t_close` is a proposed finite end-of-trial adjudication point. Absence can
only be declared after the complete allowed output window has closed and all
required evaluator-observable events through `t_close` have been accounted
for. A queue/budget failure, missing route event, truncation that prevents
the required attribution, or absent interface is incomplete/missing
evidence—not silence, a miss, or a correct negative. No wall-clock polling
or synthetic neural timestep is proposed.

Timing reports may retain raw
`delta_target = t_observation - t_target` when a target time exists and
`delta_deadline = t_observation - t_deadline`; their primary penalty/weight,
whether error is signed or absolute, and any duplicate-efficiency formula
remain owner decisions. No reward units or reward magnitudes are invented.

## 3. Eight logical outcome cases (design only; not executed)

Rows use the proposed event definition and boundary rules above. `t_resolve`
means the time the downstream evaluator can make the corresponding outcome
decision from the frozen task contract. For a future governed-training
choice, feedback cannot be delivered before `t_resolve`; it becomes
available only on a permitted causal reward event’s arrival. The reward
value, mapping, recipient set, and utility formula are not specified here.
No existing silent-state trace is presumed.

| # | Logical case and proposed decision | First-output score / timing report | Terminal outcome | Earliest outcome/reward availability | Existing attributable local work |
|---:|---|---|---|---|---|
| 1 | **On-time positive:** positive trial; first observed output is within the inclusive eligible interval and precedes the target marker under the total event order. | Correct positive/TP candidate. Preserve `delta_target` and `delta_deadline`; exact primary timing score is unfrozen. | Positive detected on time. Later outputs cannot alter this first-output decision. | After the independent target/outcome resolution, no earlier than `t_resolve`, then only after causal delivery. | The actual first output has its own emission trace at its source if that source is an eligibility ledger. A native prediction ID exists only if that emission came from a configured native predictor; it is not the task ID. |
| 2 | **Missed positive:** positive trial; no qualifying output through `t_close` (including no on-time or late first output in the declared observation window). | False negative/FN candidate; no output timestamp or timing residual. | Missed positive. | At absence resolution at/after `t_close`, then only after causal delivery. | No task-output trace exists. Other actual local emissions may have traces, but no current rule binds them to this missed outcome. **No omission trace or omission credit is invented.** |
| 3 | **Correct negative silence:** negative trial; no output through `t_close`. | Correct negative/TN candidate; no output timing residual. | Correct silence. | At negative-silence resolution at/after `t_close`, then only after causal delivery. | No task-output trace exists. Existing eligibility for any other actual emission is not an eligibility trace for silence. No credit recipient is established. |
| 4 | **False-positive negative:** negative trial; at least one output, with the first output not already classified as an ambiguous-prefix output. | False positive/FP candidate on the first output; report first-output latency from the predeclared start and later duplicate count separately. | Negative trial violated silence. | After the evaluator is permitted to adjudicate the negative trial (proposed no earlier than `t_close`), then causal delivery. | First actual output has an emission trace if the source ledger is eligible. The negative task outcome does not identify an existing trace under current semantics. |
| 5 | **Premature first output:** positive trial; first output occurs before `t_open` and outside the ambiguous-prefix case. | Premature/error; it cannot be counted as an on-time TP. Preserve the signed distance from `t_open`; exact primary treatment is unfrozen. | Premature output; the later target does not retroactively make it correct. | After the evaluator’s positive-trial decision at/after `t_resolve`, then causal delivery. | Actual first emission trace exists if its source is eligible. Current prediction IDs identify native numeric forecasts, not task timing eligibility. |
| 6 | **Late first output:** positive trial; no qualifying earlier first output and the first output is after `t_deadline` but no later than `t_close`. | Late/error and positive FN candidate; preserve `delta_deadline`. It cannot rescue the on-time first-output decision. | Late output. | At late-output observation for the fact of lateness; task reward/credit only after the full outcome is adjudicated at/after `t_resolve`, then causal delivery. | The late actual emission may have a source-local trace if still retained. Whether it can receive credit for task failure is not specified by the current task/reward interface. |
| 7 | **Duplicate after first output:** one or more further actual output events occur after a first output in the same trial and before reset. This is an orthogonal efficiency condition: retain the applicable first-output score from cases 1, 4, 5, or 6. | Freeze the first-output score; count each actual duplicate once and report an explicit efficiency penalty only after the owner freezes its formula. Duplicates never rescue an incorrect first output. | Duplicate/efficiency condition attached to the first-output outcome; no new correctness vote. | Each duplicate is observable when its event arrives; task feedback only after the duplicate penalty/outcome rule is adjudicated, no earlier than `t_resolve`. | Each actual duplicate has its own event identity and may have its own source-local trace. No current rule assigns the duplicate penalty to that trace; existing outer reward targets only the first readout emission. |
| 8 | **Ambiguous-prefix output:** the first observed output is in `[t_start, t_ambiguous_end)`, where positive/negative classes share the predeclared identical prefix. This classification takes precedence over the other first-output cases. | Invalid premature/false-output candidate for both eventual classes; do not count as correct merely because the later label is positive. Report its time and the prefix boundary. | Ambiguous-prefix silence violation. | Observable at output arrival; label-independent prefix violation may be recorded then, but any learning reward waits for an explicitly authorized outcome/delivery boundary. | Actual output trace exists if its source is eligible. The ambiguous-prefix violation has no current task reward identity or recipient. |

The eight rows are outcome rules, not measured cases or selected rewards.
For every case, a reward recipient is either an already existing,
explicitly identified actual-emission trace or **absent/unresolved**. A
deadline, a task label, an internal state value, or a failure to emit does
not create a `trace_id`, `prediction_id`, or zero-valued `EligibilityActivity`.

## 4. The two design dispositions

These are the only two dispositions considered. Neither is an experiment
authorization.

### A. Fixed mechanism / no task training

**PROPOSED:** Freeze model configuration, topology, readout and any
pre-initialized state before held-out scoring. Do not use task labels to
produce reward, update parameters, fit prototypes, alter structure, change
thresholds, or carry learned state across trials. Keep a downstream
label-aware evaluator that observes only the declared actual output events
and applies the frozen trial schedule. Reset trial-local queue, neuron
temporal state, local predictor records, eligibility/credit state and
readout/evaluator scratch state at a declared trial boundary; retain only
the explicitly frozen configuration and evaluator’s disjoint bookkeeping.
Training/validation/test state must not cross boundaries.

Native `Prediction`/`PredictionError` records, when present, must be reported
as native numeric next-input forecasting, separately from event/deadline
task outputs and scores. Their existence is not evidence of correct task
prediction or of a task omission error. A no-training study can assess the
fixed mechanism’s task behavior only if the owner first approves an actual
task-output observation boundary and task contract. It cannot claim that
reward learning solved missed positives or correct silence; it tests neither
task-reward learning nor new omission attribution. If no output boundary is
available, stop as **NOT SUPPORTED BY CURRENT GOVERNED INTERFACE**.

### B. Governed task training / delayed reward

**OBSERVED:** Existing credit can update bounded local eligibility that was
created by actual activity, if a later signal identifies an extant trace or
prediction ID and reaches that ledger. ACP-0006 §7 expressly excludes
eligibility from silent accumulator changes; the integrated outer reward
addresses the first actual readout-source emission and is unmatched when
there is none.

**INFERRED:** Existing governed IDs and causal error events can represent
some outcomes that identify actual emitted work (for example, credit to one
explicit trace ID after an on-time output). They cannot fairly represent all
eight cases as a task policy today: the task has no output/deadline/absence
event contract; negative silence and missed positive cases may have no
task-output trace; task IDs are not native numeric prediction IDs; duplicates
need a predeclared penalty recipient; and no existing rule defines which
local upstream traces, if any, own a task-level outcome.

**PROPOSED missing interface for owner review, not implementation:**

1. A bounded, downstream-only task evaluator observes the approved output
   event and independent target schedule. It resolves each trial only at
   its predeclared causal time and emits no labels into the neural runtime.
2. If training is selected, an explicit **task-outcome-to-credit bridge**
   must name the resolved outcome time, stable idempotent message identity,
   scalar reward units/value, addressed local `trace_id` or native
   `prediction_id`, destination ledger, expiry/overflow behavior, and
   permitted causal event route. The event is queued and applied only when
   delivered; an external evaluator must never mutate a remote ledger inline.
3. Attribution to upstream work must be based on explicitly retained,
   bounded, event-causal IDs/lineage available to the relevant recipient.
   Missing/truncated/unmatched identity stays missing/unmatched. No global
   registry, global reward broadcast, unlimited trace set, backpropagation,
   silent-state eligibility, or fabricated omission trace is proposed.
4. If the owner requires learning from a positive miss or correct silence
   when no existing actual-emission trace is addressable, the current
   governed interface does **not** support that capability. The owner must
   decide whether to accept a separately reviewed semantic change through
   the ACP process or choose disposition A. Luna-59 does not amend ACP-0006
   or create an omission-credit rule.

The existing `RewardSignal` payload may be a transport candidate only when
its current fields and route satisfy the reviewed contract. It does not
itself solve task resolution, local recipient selection, queue delivery, or
reward-policy fairness. Luna-5 must review the separation of reward
availability, local energy/usefulness observation and utility accounting
before any cross-component implementation. Do not pick a utility equation,
reward scale, learning rule, or task arm here.

## 5. Current-interface compatibility matrix

“Supported” below means that the code/ACP defines the cited primitive; it
does not mean task/deadline compatibility or a passing verification result.

| Interface question | Current source/ACP evidence | Finding for event/deadline design |
|---|---|---|
| Actual source output identity and time | `tpcn/excursion_neuron.py` (`ExcursionEmission`, `_emit_ordinary`); `tpcn/experiment_excursion_runtime.py` (`_consume_emission`); ACP-0006 §§7–9 | **SUPPORTED primitive:** actual canonical emission has source, signed payload, event ID, lineage and emission time. **NOT SUPPORTED task mapping:** no approved task output port or output timing policy. |
| Discharge versus emission | `tpcn/excursion_neuron.py`; ACP-0004 as bounded by ACP-0006 | **SUPPORTED distinction:** internal state/discharge and delayed `S_EMIT` are not the observable canonical emission. Score only the actual event. |
| Finite route timing | `tpcn/event_runtime.py`, `tpcn/topology.py`; ACP-0006 §§2–4 and A03 | **SUPPORTED primitive:** queued events use finite edge delay and deterministic ordering. **MISSING EVIDENCE/interface:** no task output sink or end-to-end deadline consumer is defined. |
| Native prediction IDs/events | `tpcn/predictive_coding.py`; `tests/test_predictive_coding.py`; ACP-0006 §5 | **SUPPORTED for numeric next-input prediction:** bounded ID, local timestamp, target key, expiry and optional event emission. **NOT SUPPORTED task event prediction:** no task target/deadline mapping; integrated path records a prediction but does not enqueue a task `PREDICTION_EVENT`. |
| Native expiry/absence | `LocalPredictor.expire()`; ACP-0006 §§5–6 | **SUPPORTED:** expiry removes an unresolved native prediction, and a later observation cannot match it. **NOT SUPPORTED:** expiry does not create an omission error, task false-negative event, or silence reward. |
| Prediction error delivery | `LocalPredictor.observe/process_observation`; runtime `_deliver_prediction_error`; ACP-0006 §6 and A06 | **SUPPORTED for matched native observation:** explicit signed error is causally queued/routed. **NOT SUPPORTED:** this is not task truth, deadline status, or label broadcast. |
| Eligibility creation and local credit | `tpcn/eligibility.py`; `tpcn/experiment_excursion_runtime.py`; `tests/test_eligibility.py`; ACP-0006 §7 and A08/A11 | **SUPPORTED for actual addressed activity and an existing trace/prediction identity:** bounded decay/credit/expiry and finite duplicate-ID retention. Historical Luna-54 per-ledger bound was 1,024 traces; runtime defaults include `tau=4.0`, value limits 1.0, and 64 retained reward IDs. **NOT SUPPORTED:** silent-state eligibility or identity-free task-wide credit. These values are not selected for the task. |
| Delayed outer reward in integrated run | runtime `end_character`; `tpcn/experiments.py`; `tpcn/energy_utility.py`; ACP-0006 §§7–9, 11, 16 | **PARTIAL:** reward is evaluated after label-free readout and targets the first actual readout trace; absent readout emission is unmatched. Current operation is not the proposed general routed task-outcome bridge. |
| Silence/readout | `tpcn/streaming_classifier.py`; ACP-0006 §§8–9 | **SUPPORTED for current A–Z character protocol:** no `ACTIVITY_EVENT` on silence and deterministic classifier finalization at `END_CHARACTER`. **NOT SUPPORTED:** event/deadline binary/temporal scoring, missed-positive adjudication, or rewarded correct silence. |
| Fixed/no-training evaluation | `tpcn/experiments.py`; ACP-0006 §§8–11 | **PARTIAL:** label-free stream then external label use is an existing boundary, but prototype/reward behavior is present in the experiment path. The requested frozen event/deadline evaluator and isolation policy require owner-approved design. |
| Energy/reward interface | `tpcn/energy_utility.py`; `experiments/luna54/config.json`; A09–A10; ACP-0006 §16 | **SUPPORTED proxy primitive:** finite local `activity-cost-proxy` and explicit utility boundary. Reward is a finite scalar without a task-unit contract in the reviewed ACP; the exact future utility rule is not fixed. **MISSING:** task-specific reward scale, event/output accounting agreement and metric policy; no calibrated joules or physical mapping. Luna-5 review required before integration. |
| ACP-0008 parameter context | ACP-0008; `experiments/luna54/config.json`; `experiments/luna55/config.json`; `experiments/luna58/config.json`; frozen Luna-45 config | **OBSERVED configurations only:** `integration=None` remains canonical disabled default; the opt-in `IntegrationConfig` default is `decay_rate_z=0.1`; historical values include Luna-45/Luna-55/Luna-54 settings. Luna-58’s `0.00001` was a bounded mechanism intervention selected against previously examined nonresponders. **NOT a task calibration:** no rate/arm selected or searched here; no automatic adoption. |
| Trial/split and anti-shortcut contract | Owner objective in `.github/agents/luna-59.agent.md`, Luna workflow and changelog | **MISSING:** target schedule, exact windows, generator, outcome rule, population/splits/counts, repetitions, comparator, arms, budgets and duplicate penalty. They remain owner decisions. |

## 6. Task contract and anti-shortcut gates to freeze

Before any future scientific dispatch, the owner and Luna-0 must freeze all
of the following without post-outcome selection or historical stratum
relabeling:

- Target event schedule and independent outcome-generation rule.
- Task-output source/sink and event identity/payload/timestamp mapping.
- Eligible interval, deadline, ambiguous-prefix boundaries, trial close,
  equality/tie order and absence-resolution rule.
- Trial generator version; matched positive/negative trial counts and
  matched nuisances, event order/gaps, amplitudes, counts and durations.
- Disjoint provenance and train/validation/held-out splits; exact held-out
  counts and independently executed repetitions.
- Predeclared historical/default comparator and justified mechanism/component
  arms. No arm is authorized by this document.
- Queue/event/trace/readout budgets and overflow, censoring, truncation,
  expiry, reset and incomplete-run policy.
- First-output scoring, TPR/FNR/FPR policy, premature/late treatment,
  duplicate count and explicit efficiency-penalty formula, and falsification
  criteria.
- Secondary metrics: native prediction matches/errors/expiry separately from
  task errors; output latency; processed/emitted/routed events; activity and
  energy-proxy units; topology utilization; queue/budget/pending/clipping/
  truncation; and replay identity.
- Whether disposition A or B is selected. If B, an owner-approved local
  recipient and reward-delivery contract (and ACP review if semantics
  change).

Anti-shortcut requirements:

1. Positive and negative examples share identical ambiguous prefixes; there
   is no class-coded trial ID, marker, amplitude, event count, or total
   duration.
2. Match event order/gap nuisances. Include timing-destroyed/reversed controls
   whose expected outcomes are independently specified, not inferred from
   observed network response.
3. No target event, target label, or target-derived feature may reach a
   scored predictor before its allowed output time.
4. Include a predeclared causal route/component intervention; graph changes
   alone are not causal task evidence.
5. Label-swapped, identical-input trials must not alter neural events,
   state, routing, prediction/error computation or structure.
6. Reset and split boundaries must prevent predictor, queue, eligibility,
   readout, reward-ID and hidden evaluator state from leaking across trials
   or partitions, except for explicitly frozen state approved in advance.

## 7. Owner decisions and stop conditions

**Owner/Luna-0 decision requests (all remain open):**

1. Approve or reject the proposed canonical-output observation point and
   whether event-time scoring uses source emission time, routed arrival time,
   or both with one declared primary.
2. Freeze the target schedule, whether successful output must strictly
   precede the target event, eligible interval/deadline/close, ambiguous
   prefix, equal-time ordering, and when silence becomes adjudicable.
3. Choose disposition A (fixed/no task training) or B (governed training).
   If B, decide whether task feedback may credit only explicitly identified
   existing actual-emission traces. If credit from silence/no emitted work is
   required, route it through a separate ACP/owner decision; do not infer
   authorization from this document.
4. Approve trial generator/provenance/splits/counts/repetitions, matched
   nuisances, comparator, scientifically justified arms, resource budgets,
   first-output and duplicate metrics, secondary metrics and falsification
   criteria. The held-out threshold and FPR margin below are owner-defined
   requirements, not evidence of a pass.
5. Ask Luna-5 to review reward availability versus energy/usefulness and
   proxy accounting before any shared implementation; ask Luna-3 to confirm
   native prediction/error identity compatibility if it is reused. Luna-8
   owns only eligibility/credit attribution, not task policy or classifier.
6. Keep independent Luna-58 review as a separate open evidence gate if any
   later decision relies on that result. This design does not close it.

Stop with **NOT SUPPORTED BY CURRENT GOVERNED INTERFACE** if a required
observable output, causal arrival, absence-resolution event, task-reward
recipient, event route, or local eligibility identity cannot be named.
Do not fill missing information with intuition, an unseen target, synthetic
zero activity, silent eligibility, a global lookup, reward broadcast, or an
ACP-0006 reinterpretation.

## 8. Preserved owner metric and scope boundary

The owner objective is held-out balanced accuracy as primary, with at least
**+10 percentage points** versus the predeclared historical/default
comparator and no more than **+5 percentage points FPR degradation**.
For stochastic studies, direction must agree in a majority of declared
seeds; for deterministic studies, require exact independently executed
replay. Matched positive/negative trials and temporal anti-shortcut controls
are required. Application benchmarks are deferred. E+49 has no task-label
mapping and no target-crossing requirement.

These are future requirements, not results. Exact target, interval/deadline,
comparator, population/split, penalty formula, task-output rule,
no-training/training decision and arms remain unfrozen. No experiments,
arms, numerical task parameters, thresholds or rates are authorized here.
Luna-58’s `0.00001` is not automatically adopted. This work does not establish
benchmark, energy, Luna-11, hardware, efficacy, generalization, architecture
conformance, or production readiness.
