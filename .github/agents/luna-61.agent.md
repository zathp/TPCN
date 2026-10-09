---
name: "Luna-61 Delayed Symbolic Event-Sequence Echo Design"
description: "Design only the bounded symbolic delayed-recall task and assess existing output and recall-gating viability; no implementation, experiment, or training."
tools: [read, search, edit]
---

# Luna-61 — Delayed symbolic event-sequence echo design prerequisite

**AUTHORIZED / NOT EXECUTED.** The project owner superseded the earlier
binary event/deadline task choice before Luna-61 began. Luna-0 amends this
existing documentation-only assignment in place; this is not a new Luna
number and does not authorize execution during this governance pass.

## Dispatch identity and scope

```yaml
tpcn_handoff:
  agent: "Luna-61"
  luna_identifier: "Luna-61"
  descriptive_name: "Delayed symbolic event-sequence echo design"
  task_id: "luna-61-task-output-assignment-design"
  component: "External symbolic task definition and output/gating viability; design only"
  status: "authorized; amended before execution; not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "8d0a739e7e8bb4f065cd04157864a96fc501b58c"
  result_revision: "not executed"
  dependencies:
    - "Owner decision selecting delayed symbolic sequence echo, published by Luna-0"
    - "Luna-60 task-output interface and completion handoff as historical interface evidence"
    - "Accepted ACP-0006 emission, prediction, eligibility and reward boundaries"
    - "Current architecture contract, acceptance criteria and handoff template"
  owner: "Project owner; Luna-0 reviews design and controls any later dispatch"
  classification: ["DESIGN", "READ-ONLY COMPATIBILITY REVIEW"]
  hypothesis: "An external symbolic echo target can define correct delayed recall independently, but current output identity, temporal retention and recall gating may not support a meaningful fixed/no-training evaluation."
  counter_hypothesis: "Existing event inputs, canonical output sources and cue-responsive temporal behavior already support a justified identity-preserving recall mapping without new primitives or task-specific training."
  interfaces_relied_on: ["Canonical event input and ExcursionEmission", "Luna-60 binary TaskPrediction as historical interface only", "event-time queue ordering", "bounded local eligibility and reward"]
  label_information_boundary: ["Expected output is an external copy of the presented input sequence. No expected answer, future symbol, phase label, or truth enters neural computation."]
  timing_assumptions: ["Logical event time only; no global neural tick. Numerical delays and output deadlines remain unselected."]
  reset_boundaries: ["Specify a prospective trial reset boundary in the design only; do not run a trial."]
  resource_bounds: ["Documentation only; no code, task data, generated fixtures, neural state or experimental resource use."]
  authorized_scope:
    - "Read-only inspection of task/event interfaces, neural inputs/emissions, existing readout and cue mechanisms, reset/credit boundaries, Luna-60, and governing documentation."
    - "Create workflow/docs/luna/LUNA_61_TASK_OUTPUT_ASSIGNMENT.md."
    - "Create workflow/handoffs/luna-61-task-output-assignment.md using the handoff template."
    - "Design the task semantics, controls, metrics and fixture provenance; assess output, recall-gating and fixed/no-training viability."
  unauthorized_scope:
    - "All implementation or edits outside the two owned design deliverables."
    - "Any runtime, neuron, routing, neural configuration, evaluator, reward, eligibility, classifier, test, or scientific-artifact change."
    - "Task-trial execution, synthetic data or fixture generation, replay, simulation, scoring, benchmark, efficacy or training."
    - "Readout search, held-out selection, threshold/configuration/window/delay tuning, or choosing mappings based on observed performance."
    - "Reward/penalty, omission credit, sequence-level credit, teacher forcing, supervised readout training, or new task-specific payload semantics."
    - "Architecture/ACP promotion, new output source implementation, or any scientific successor authorization."
  controls:
    - "Expected output is defined solely as the externally recorded LISTEN sequence, never by TPCN output."
    - "Use a small multi-symbol vocabulary; include repeated-symbol and matched-count order-confusable controls."
    - "Keep delay independent of sequence length where practical and specify distractors separately from target symbols."
    - "Novel sequence combinations are required in any future efficacy design if training/calibration is introduced."
    - "Treat the roadmap as design only; do not select numerical task times from observed TPCN performance."
  measurements: ["None; no trial, task data, score, or performance measurement is permitted."]
  information_boundary_check: ["The network receives each input symbol only when presented and the explicit RECALL cue; expected output, future symbols and evaluator truth remain external."]
  hardware_mapping: ["No hardware implementation or equivalence claim; identify representation/resource implications only."]
  architecture_invariants_touched: ["A01-A08 and A11 preserved; no core clause or A01-A15 requirement changes. A09-A10 are not calibrated; A12-A13 remain optional; A14-A15 are not evaluated."]
  preserves:
    - "Luna-60 binary destination -> target-before-deadline interface remains valid historical infrastructure, but is insufficient by itself for multi-symbol recall."
    - "No change to ACP-0006 emission, local prediction/error, eligibility or reward semantics."
    - "ACP-0008 remains experimental and opt-in."
  architecture_change: false
  proposal: null
  files_changed: []
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All tests, experiments, simulation, data generation, scoring and training; not authorized."]
  assumptions: ["The owner-selected task family is an assignment for design, not approval of implementation, training, efficacy, or a specific output architecture."]
  unresolved: ["Whether existing input/output primitives and cue-driven dynamics can express symbolic recall; output mapping, recall close rule, future task parameters, splits, comparator, and any required learning/architecture decisions."]
  recommended_next_agent: ["Luna-0: independently review the two design deliverables; no automatic Luna-62, experiment or training."]
```

## Required reading

Read the tracked `workflow/` architecture contract, changelog, Luna workflow,
acceptance criteria, ACP process/template and handoff template. Read the
Luna-60 agent contract, interface implementation, interface document and
completion handoff; the earlier Luna-0 owner-decision and task-output
governance records; Luna-59 design as historical work; relevant event input,
canonical emission, output-source, cue, reset and credit interfaces; and
applicable retained temporal fixtures. Record the exact baseline and
distinguish observed code behavior from design inference.

## Owner-selected task family and frozen trial semantics

The task is **delayed symbolic event-sequence echo/recall**, not binary
target-before-deadline prediction, classification, speech recognition, or
audio processing. The previous binary task choice is superseded before
Luna-61 execution; retain it only as historical design. Do not edit or
invalidate Luna-60.

A trial has these causal phases:

1. **LISTEN:** Present an externally generated ordered sequence of symbolic
   input events. The network receives each symbol only as its event arrives;
   it does not receive a separate expected answer.
2. **DELAY:** After the final input symbol, wait for a variable event-driven
   interval. The design must include zero intervening events, optional
   neutral timing events, and at least one future distractor condition whose
   symbols are not part of the target sequence. Vary delay independently of
   sequence length where practical. No fixed global neural timestep.
3. **RECALL:** Present one explicit `RECALL` event. This cue opens the
   recall-output phase. Sequence-output events before the cue are premature
   errors, not silence that the evaluator suppresses.
4. **RECALL OUTPUT:** The target is exactly the LISTEN sequence, with every
   occurrence and its order preserved. The evaluator matches actual output
   symbol events to this external target.

Propose the initial symbolic vocabulary `{A, B, C, D}` and corresponding
conceptual input channels `IN_A`, `IN_B`, `IN_C`, `IN_D`, plus `RECALL` and
any explicitly justified neutral/distractor inputs. Do not implement these
channels. No microphone/audio input, phoneme extraction, spectrogram,
speech-recognition pipeline, or language model is in scope.

The design must specify deterministic event-order treatment when an output
shares the RECALL timestamp: only canonical queue/event order determines
whether it is before or after the cue; do not add an artificial timestep.
Choose and justify one finite, event-time recall-close rule (for example an
explicit close event or a declared cue-relative logical-time deadline).
Unlimited response time is invalid. No timing values may be selected from
TPCN performance in this design task.

Ground truth for each trial is the independently generated LISTEN symbol
sequence. It is fixed before observing output. Repeated symbols are required
(for example `A A B A` or `C B C D`), as are matched-count order-confusable
sequences (for example `A B C`, `C B A`, and `A C B`). Specify controls
that defeat symbol-count/set-only strategies. No trial may be selected,
relabelled, or dropped based on TPCN output.

## Required design analysis

1. Inspect existing event input and canonical output semantics. Determine
   whether distinct symbolic identities can be represented on input and
   whether any existing output sources already provide distinct identities.
   Do not assume `destination` is multi-symbol output or select a source
   based on performance.
2. Compare and rank, from repository evidence, at least:
   - **One existing output source per symbol** (`OUT_A` … `OUT_D`): explicit
     source identity, but requires multiple governed output sources.
   - **One source with payload-coded symbol identity:** fewer sources, but
     risks introducing a new, currently ungoverned payload meaning.
   - **Existing classifier-style readout:** assess without assuming its
     semantics are valid for ordered event recall.
   A small downstream adapter may be recommended only if canonical records
   already preserve sufficient symbol identity, event order and time. Never
   fabricate multi-symbol results inside the evaluator. Define the minimum
   output record explicitly: trial/sequence identity, symbol identity, actual
   canonical event identity/source sequence, and logical event timestamp;
   establish how these are assigned without consulting expected output.
3. Determine whether the current architecture supports, without evaluator
   intervention, the causal behavior “store now, wait for RECALL, then emit
   distinct symbols in sequence.” Assess ordered identity retention,
   cue-triggered recall gating, and multiple ordered output events. The
   evaluator may score premature output but cannot make the network wait.
   If a required primitive is missing, classify it as a future prerequisite;
   do not implement or authorize an architecture change.
4. Assess fixed/no-training scientific viability. A fixed baseline is
   interpretable only if the input-to-output identity mapping, output
   behavior and configurations can be justified independently before
   evaluation. If the behavior or mapping would be arbitrary without
   task-specific learning, say so. Do not run a benchmark or infer viability
   from a score.
5. Analyze current eligibility/reward boundaries. Distinguish credit for
   actual emitted events from external sequence outcome assignment and from
   missing, wrong, premature or misplaced output credit. Document the
   delayed-credit problem without inventing reward, penalty, teacher
   forcing, sequence-level reward, omission identity, or supervised
   readout semantics.
6. Specify event-phase/reset/truth isolation and a deterministic scoring
   proposal. **Primary metric:** exact sequence accuracy; a trial is correct
   only when the complete output sequence has the exact symbols and order,
   with no omissions or insertions. Define how premature output and
   incomplete/censored trials are handled.
7. Specify secondary reporting separately, not as an ad hoc combined score:
   symbol accuracy; substitution, insertion, deletion and order/transposition
   counts using a deterministic edit-analysis algorithm and tie-break;
   exact-prefix length; recall latency; inter-output timing; premature
   output rate; duplicate count; total output count; and a governed energy/
   event proxy only if applicable.
8. Design controls and progression: repeated-symbol and matched-count
   order-confusable inputs; short and longer variable delay conditions
   independent of sequence length where practical; at least one DELAY
   distractor condition; and a capacity curve increasing sequence lengths
   (candidate stages 2, 3, 4, then longer). Define maximum reliable recall
   length as a future measured quantity, not an assumption. State expected
   diagnostic interpretations separately: correct symbols in wrong order
   suggests temporal-order failure; later omissions after a correct prefix
   suggest capacity/decay limitation; a distractor replacing a target symbol
   suggests interference; correct symbols emitted before RECALL suggest
   gating failure; and silence despite independently evidenced retained
   identity state suggests a readout/reconstruction problem. These are
   hypotheses to test, not causal conclusions from output scores alone.
9. Assess whether an initial future task could be bounded around four symbols
   and lengths 2–4 with matched recall trials, variable delay, repeated
   symbols and order controls. These are candidate design bounds only;
   freeze no final numeric times, task budget, trial count, or efficacy arm.
10. Define a future novel-sequence/generalization split. If training or
    calibration is later authorized, sequence combinations in held-out test
    must be disjoint from those used for training/calibration; preserve
    repeated symbols and control composition so memorizing whole strings is
    not sufficient. No training or split generation now.
11. Specify fixture provenance fields for any later deterministic fixture:
    vocabulary, sequences/lengths, delay and distractor schedule, recall and
    close semantics, expected outputs, generator revision/blob, seed if
    applicable, exact serialized event records and any disjoint
    train/calibration/test partition. Avoid environment-sensitive regenerated
    bytes without a declared identity policy.
12. Provide a staged roadmap only: short length-2 no-distractor echo;
    lengths 2–4 and variable delays; repeated/order-confusable sequences;
    delay distractors; novel sequence/length generalization; phoneme-like
    symbolic inputs; and only later a separately governed speech/audio
    front-end. This authorizes none of those stages.

## Relationship to Luna-60 and disposition

Luna-60 remains a valid, reviewed binary task-output/evaluator primitive.
Its single affirmative `destination` -> `target-before-deadline` mapping
cannot by itself represent a recalled sequence of distinct ordered symbols.
Determine whether future sequence support should use a sibling downstream
interface or requires a separately governed output primitive. Do not modify
Luna-60 implementation or redefine its binary contract.

Conclude using the most specific applicable design disposition:

- **SEQUENCE-ECHO TASK BOUNDED — OUTPUT/FIXTURE PREREQUISITE REQUIRED**
- **SEQUENCE-ECHO TASK BOUNDED — FIXED EVALUATION MAY PROCEED** (only if
  predeclared mappings and cue-responsive behavior already have independent
  architectural justification; this design task still cannot authorize the
  experiment)
- **SEQUENCE-ECHO REQUIRES MULTI-SYMBOL OUTPUT PRIMITIVE**
- **SEQUENCE-ECHO REQUIRES RECALL-GATING ARCHITECTURE DECISION**
- **SEQUENCE-ECHO TASK NOT YET BOUNDED**

Record any minimum owner decision required. A task definition, output
mapping, architecture recommendation or design disposition is not
authorization for implementation, training, task trials, or efficacy.

## Required deliverables and acceptance

Write only:

1. `workflow/docs/luna/LUNA_61_TASK_OUTPUT_ASSIGNMENT.md`
2. `workflow/handoffs/luna-61-task-output-assignment.md`

The task design must cover the exact task/phase/close semantics; vocabulary
and symbolic input proposal; expected outputs and silence; exact-sequence
primary and secondary metrics; repeated-symbol and order controls;
variable-delay/distractor/capacity/novel-sequence plans; input/output
representation alternatives; recall-gating and fixed/no-training viability;
learning/reward limits; fixture provenance; A01-A15 relevance; evidence
labels and not-run/N/A boundaries; final disposition; and the next bounded
prerequisite.

No tests are required or authorized because this is documentation-only design
work. Do not generate task data or fixtures, execute runners, score trials,
select configurations, tune parameters, train, or claim task efficacy. Stop
after the two deliverables for independent Luna-0 review. No automatic
Luna-62, task study, training, reward change or architecture promotion
follows.
