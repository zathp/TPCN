---
name: "Luna-62 Bounded Sequence-Memory Architecture Proposal"
description: "Compare bounded local event-driven sequence-memory and RECALL-gated replay architectures; design only, no implementation or trials."
tools: [read, search, edit]
---

# Luna-62 — Bounded sequence-memory architecture proposal

**AUTHORIZED / NOT EXECUTED.** This is a documentation-only architecture
proposal assignment authorized by Luna-0. It follows the completed Luna-61
delayed symbolic event-sequence echo design. Luna-62 does not authorize an
ACP, implementation, task trial, training, efficacy claim, or successor.

## Dispatch identity and scope

```yaml
tpcn_handoff:
  agent: "Luna-62"
  luna_identifier: "Luna-62"
  descriptive_name: "Bounded sequence-memory architecture proposal"
  task_id: "luna-62-sequence-memory-architecture-proposal"
  component: "Local event-driven symbolic sequence storage and RECALL-gated replay; design only"
  status: "authorized; not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "694b34e0e80af21f89547d1124315ef8913fce35"
  result_revision: "not executed"
  dependencies:
    - "Owner-selected delayed symbolic event-sequence echo and Luna-61 design"
    - "Current ARCHITECTURE_CONTRACT.md, acceptance criteria, ACP process and handoff template"
    - "Existing event, E2 neuron/runtime, topology, prediction, eligibility and reward semantics"
  owner: "Project owner; Luna-0 independently reviews completed proposal"
  classification: ["ARCHITECTURE DESIGN", "READ-ONLY COMPATIBILITY REVIEW"]
  hypothesis: "At least one bounded, local, event-driven computational memory candidate can preserve symbolic identity, order and multiplicity through a delay and release it only after a genuine RECALL event without an external answer buffer or global neural clock."
  counter_hypothesis: "All candidates either externalize the memory, fail to preserve arbitrary bounded sequence order and repetition, violate a core constraint, or require an unresolved owner architecture choice."
  interfaces_relied_on:
    - "Event, EventQueue, EventType, local timestamps and finite propagation"
    - "MultiExcursionNeuron, ExcursionEmission and E2 runtime"
    - "BoundedTopology, prediction/error, eligibility and reward boundaries"
    - "Luna-61 symbolic task definition and canonical output-source preference"
  label_information_boundary:
    - "Expected output remains evaluator-only LISTEN truth; it never enters the proposed neural computation."
    - "RECALL is a genuine cue event and carries no stored symbols, expected sequence, or output count."
  timing_assumptions:
    - "Event/local elapsed time only; no global neural timestep."
    - "No task-performance-based timing or parameter selection."
  reset_boundaries:
    - "Specify bounded expiry, reset and re-arm semantics; do not execute a trial."
  resource_bounds:
    - "Design only; discuss finite K_sequence including candidate prototype capacities 2, 4 and 8 without selecting a production value."
    - "No code, generated task data, fixtures, runtime state or performance measurement."
  authorized_scope:
    - "Read current architecture, Luna-61, ACP and relevant implementation evidence."
    - "Create workflow/docs/luna/LUNA_62_SEQUENCE_MEMORY_ARCHITECTURE.md."
    - "Create workflow/handoffs/luna-62-sequence-memory-architecture.md using the handoff template."
    - "Compare candidate mechanisms, specify one justified leading candidate or report that none is identified, and define a future falsification boundary."
  unauthorized_scope:
    - "All source, runtime, neuron, topology, task adapter, evaluator, test, fixture, data, training or experiment changes."
    - "Implementing, executing or benchmarking sequence memory or recall."
    - "Creating or accepting an ACP, changing ACP status, changing A01-A15, or promoting a candidate to default."
    - "Authorizing Luna-63 or any implementation, task efficacy, learning, reward/credit or hardware work."
  controls:
    - "Do not store the answer in a task-level Python list, external FIFO, evaluator, fixture feedback path, or global-timestep shift register as the neural solution."
    - "A test/evaluator may retain LISTEN truth solely as an independent oracle."
    - "Treat audit provenance as non-computational unless it causally changes future network events."
    - "Do not claim an explicit internal token/chain is not FIFO-like; state its actual scientific and architectural role."
    - "Do not infer recall from recurrence, scalar decay, provenance, WEMA, or peak-hold without an explicit identity/order/replay mechanism."
  measurements:
    - "None; architecture design only."
  information_boundary_check:
    - "RECALL contains no answer data; no evaluator, label, expected length or output-derived selection controls replay."
  hardware_mapping:
    - "Assess qualitative FPGA bounded registers/RAM/queues/FSM/routing cost and FPAA/analog feasibility; no hardware tests or equivalence claim."
  architecture_invariants_touched:
    - "Assess A01-A04, A06-A08, A11, A14-A15; preserve A12-A13 optionality. No clause change."
  preserves:
    - "Luna-61 task truth, anti-leakage boundary, and distinction between current scalar state/provenance and computational sequence memory."
    - "Existing prediction/error, emission identity, eligibility, reward and topology semantics."
    - "ACP-0008 remains opt-in and is not presumed to solve symbolic memory."
  architecture_change: false
  proposal: null
  files_changed: []
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All tests, code execution, task generation, task trials, scoring, training, benchmark, simulation and hardware validation; not authorized."
  assumptions:
    - "A coherent design is not evidence of implemented or demonstrated recall."
  unresolved:
    - "Whether any candidate is acceptable under existing clauses or requires an ACP before implementation."
    - "Owner/architecture choice if materially distinct candidates remain equally plausible."
  recommended_next_agent:
    - "Independent Luna-0 review of both exact Luna-62 deliverables; no automatic ACP or implementation."
```

## Required reading and evidence discipline

Read the current `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/README.md`,
`workflow/docs/architecture_proposals/ACP-TEMPLATE.md`, and
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`.

Read `.github/agents/luna-61.agent.md`,
`workflow/docs/luna/LUNA_61_TASK_OUTPUT_ASSIGNMENT.md`,
`workflow/handoffs/luna-61-task-output-assignment.md`, the Luna-0
Luna-61 review/governance record, and relevant Luna-60 interface records.
Inspect current event queue, E2 neuron/runtime, bounded topology, native
prediction/error, eligibility and reward semantics. Pin the exact baseline
and code evidence. Separate **OBSERVED**, **INFERRED**, and **HYPOTHESIZED**.
Do not rely on legacy examples as amendments to the architecture contract.

If a required artifact or source is absent, record the exact path and
limitation. Do not invent the contents of an absent review or claim an
ancestry check that was not possible.

## Central question

Determine whether there is a smallest bounded, local, event-driven
computational mechanism that preserves an ordered sequence of event
identities through a delay, stays silent during storage, and causally emits
that sequence only after RECALL—without relying on a conventional external
FIFO or global neural clock.

The selected task remains:

`LISTEN → DELAY → RECALL → RECALL OUTPUT`

Truth is exactly the external LISTEN sequence. The initial symbolic
vocabulary proposal is `A, B, C, D`. A central discriminating target is:

`A → C → B` stored in that order, silent through DELAY, then emitted as
`A → C → B` after RECALL.

## Anti-cheating and architectural boundaries

The LISTEN sequence must not be retained outside the proposed TPCN
computation and replayed by task software. Forbidden as the neural solution:

- a Python list or other task-level buffer of input symbols;
- an external FIFO of the expected sequence;
- evaluator-managed output replay or fixture feedback;
- a global-timestep shift register outside neural dynamics.

Oracle/evaluator truth storage may exist only to score output and must not
generate it. A candidate may use an internal ordered chain/token structure,
but must classify whether it is computational state, metadata, or a task
adapter and explain what scientific property it tests. Do not call a
FIFO-like structure a neural memory without justification.

Preserve, as practical and explain any tension with:

- event-driven computation and local elapsed time; no required global tick;
- finite local state, queue/event budgets, topology, fan-in/out and routing;
- causal event identity and finite propagation;
- deterministic software-reference semantics where required;
- local learning boundaries, no label leakage, and existing predictive
  coding/error semantics;
- later FPGA compatibility and plausible analog/hybrid implementation.

Do not change contract clauses, existing ACPs, defaults, production code or
ACP status. Treat any new order-bearing persistent computation or
RECALL-specific event transition as potentially material architecture
change; assess whether an ACP is required before implementation. Luna-62
may recommend a governance path but is not authorized to draft or accept an
ACP.

## Required analysis

The design report must include:

1. **Architecture gap.** State what Luna-61 established and what existing
   runtime/state/provenance does not establish. Keep observed facts separate
   from design inference.
2. **Candidate comparison table.** Compare at least:
   - chained local memory cells;
   - event-linked sequence chain, explicitly distinguishing computation
     from provenance/eligibility bookkeeping;
   - distributed temporal state trajectory;
   - local token/ring replay;
   - recurrent neural replay with concrete state and causal release
     semantics, or mark it underdefined/weak;
   - conventional FIFO as an engineering/oracle reference, not presumed
     TPCN memory.

   Columns must address identity, multiplicity, order, cue-gated replay,
   event-driven operation, boundedness/locality, FPGA fit, analog/hybrid
   fit, qualitative state/routes scaling with vocabulary `V` and capacity
   `K`, and main risk.
3. **One leading candidate at most.** If recommended, specify its
   components/state, event types, symbol identity, write/store semantics,
   hold/decay/expiry, inspectable order invariant, repeated-symbol behavior,
   genuine RECALL semantics, transition to replay, causal progression and
   timing, output mapping, completion, reset/re-arm, capacity and explicit
   overflow behavior. Explain ordinary TPCN interaction and failure modes.
   A recommendation is not adoption.
4. **Sequence capability accounting.** Separately answer identity, store,
   order, multiplicity, variable delay, silence while storing, cue
   detection, replay gating, sequential release, output identity,
   completion, finite capacity, overflow, reset/re-arm, and ordinary state
   interaction.
5. **FIFO/reference analysis.** Explain what scientific claim an explicit
   ordered queue would test, when an internal chain is effectively a FIFO,
   and why an external answer buffer cannot count as the network's memory.
6. **Capacity and timing.** Define symbolic `K_sequence`; discuss capacity
   2, 4 and 8 as candidate sizes only. State non-silent overflow behavior
   options and their tradeoffs; do not choose via task performance. Define
   event causing each replay transition, whether delay is local/parameterized
   or otherwise, and how replay terminates without an evaluator clock or
   expected output length.
7. **End marker and reset.** Compare tail/no-successor, bounded count and
   explicit EOS. Define bounded cleanup and deterministic repeated-trial
   re-arm; do not let evaluator report completion to the network.
8. **Ordinary computation and learning boundary.** Classify the design as a
   separate experimental subsystem, an integration into predictive neurons,
   or an unproven generalized capability. Identify future trainable surfaces
   only; do not design training, task credit or a reward rule.
9. **Prediction/error/reward compatibility.** Analyze identities for
   original LISTEN event, memory entry and replay emission; account for
   atomic fan-out identity and duplicate-credit ambiguity. Preserve the
   known missing-output/silence-credit limitation. No reward fabrication or
   eligibility change.
10. **Computational-state classification.** For every retained symbol,
    order, link, token and provenance field, identify whether it is
    computational state affecting future events, provenance-only state,
    or evaluator-only state. Only the first may count as the memory.
11. **Hardware and continuous-state concepts.** Discuss qualitative FPGA
    state/routing cost and FPAA/analog or hybrid division of responsibility.
    Address whether WEMA or peak-hold could support evidence/gating, without
    claiming they encode arbitrary order absent an explicit mechanism.
12. **Falsifiability.** Specify future deterministic tests that include:
    store `A B` and `B A`; show computational internal states differ;
    RECALL and verify causal order; store `A A` and receive two separate
    emissions; variable/longer delay retention; capacity boundary and
    overflow; premature-output suppression; and deterministic replay.
    Include the Luna-61 target `A C B`. No such tests may be run in Luna-62.
13. **Smallest future prototype boundary.** If justified, propose a
    mechanism-only fixture (for example `V=2` or `4`, `K_sequence=2`, no
    training, no distractors initially, explicit RECALL, exact event traces).
    Do not generate the fixture or select parameters from performance.
14. **ACP and clauses.** Map relevant A01-A15 clauses, identify compatible
    implementation vs material architecture change, and state whether an
    ACP is required before implementation. Do not amend clauses or ACP
    status.
15. **Explicit non-claims and disposition.** Select exactly one:
    - `BOUNDED SEQUENCE-MEMORY ARCHITECTURE PROPOSED — ACP REQUIRED`
    - `BOUNDED SEQUENCE-MEMORY ARCHITECTURE PROPOSED — MECHANISM PROTOTYPE MAY BE CONSIDERED`
    - `NO SATISFACTORY LOCAL RECALL ARCHITECTURE IDENTIFIED`
    - `SEQUENCE-ECHO REQUIRES OWNER ARCHITECTURE CHOICE`

    State that design alone establishes no recall ability, task efficacy,
    capacity, generalization, learning, or hardware equivalence.

## Stop conditions and next gate

Stop and report the blocker if no candidate preserves the constraints, if
the task requires a new owner choice, or if repository evidence materially
contradicts the Luna-61 findings. Do not resolve a material architecture
choice by implementation.

Deliver only the architecture design and completed handoff. After Luna-62,
**independent Luna-0 review is mandatory** before any ACP or implementation
decision. No Luna-63 or other successor is authorized.
