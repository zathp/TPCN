---
name: "Luna-63C Nonlinear Excursion Neuron Design Prerequisite"
description: "Design only one bounded nonlinear excursion neuron with recall-gated trajectory and canonical event conversion; no implementation, simulation, trials, or sequence-echo integration."
tools: [read, search, edit]
agents: []
---

# Luna-63C — bounded nonlinear excursion design prerequisite

**DESIGN ONLY AUTHORIZED / NOT EXECUTED.** This assignment defines one
mathematically explicit candidate and a falsifiable future mechanism protocol.
It does not authorize implementation, simulation, trials, canonical runtime
changes, task efficacy, integrated echo, ACP adoption, or architecture
promotion.

The project owner has authorized considering this design prerequisite after
the independently reviewed Luna-63A and Luna-63B results. Pin the actual
governance baseline supplied by the orchestrator; do not infer revision or
source identity from an old handoff. Work only in the assigned isolated branch
and worktree. Do not create branches or change files outside the ownership list.

## Owned deliverables

Only edit:

- `workflow/docs/luna/LUNA_63C_NONLINEAR_EXCURSION_DESIGN.md`
- `workflow/handoffs/luna-63c-nonlinear-excursion-design-20261009.md`

Use `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` and complete every
applicable field. Keep equations and thresholds explicitly proposed and
unexecuted. Do not edit an ACP, architecture contract/changelog, workflow
index, agent contract, production code, tests, or artifacts.

## Design question

Specify one exact, low-dimensional, bounded neuron candidate that can:

1. remain at a stable neutral rest;
2. retain a displaced internal state;
3. return subthreshold states without producing an output event;
4. traverse a defined excursion for an appropriate stored state;
5. return to neutral after the excursion;
6. optionally show mathematically demonstrated damped spiral return; and
7. gate trajectory traversal with RECALL, without RECALL alone causing a spike.

Compare at least two plausible model families before selecting at most one:
FitzHugh-Nagumo-like excitable dynamics, excitable/spiral normal forms,
bounded polynomial/vector fields, and a threshold-oscillator hybrid.
Do not select by biological resemblance. Compare boundedness, stable rest,
reproducibility, event interpretation, and qualitative digital/FPGA/analog
realizability. If no single candidate satisfies the design envelope, report
the exact blocker rather than combining candidates or expanding state.

## Required explicit formulation

For the selected candidate define:

- all state coordinates, units, initial/reset state, and finite bounds;
- the exact continuous-time vector field or exact event-driven recurrence;
- parameter values/ranges and why they yield stable neutral rest;
- HOLD versus RECALL equations and whether the gate freezes all dynamics or
  only selected terms;
- evidence that HOLD cannot diverge from an unstable frozen state;
- a neutral-state RECALL control that produces no spike;
- a subthreshold displaced-state RECALL control that returns without a spike;
- a supra-threshold stored-state RECALL case with exactly one excursion;
- a held supra-threshold state with no output while RECALL is absent;
- return-to-rest and any optional damped spiral claim, including fixed point,
  eigenvalue/stability analysis, damping and finite return condition;
- all clamps/saturation and failure/expiry rules.

Do not use a direct RECALL-to-spike term. Define how a state-space trajectory
is traversed on release. If whole-field multiplication by a zero gate would
freeze an unstable state, identify and reject or repair that formulation
within the same single candidate before claiming a bounded design.

## Canonical event conversion

Define a deterministic crossing rule from continuous state to one canonical
event: crossing section/threshold, direction, hysteresis/re-arm, duplicate
suppression, and at-most-one event per excursion. Specify how an output event
is scheduled strictly in the representable future under existing event
semantics, including behavior when a positive delay is below timestamp
resolution. Do not introduce a global neural timestep or zero-delay recursive
cascade. No implementation or conformance claim is permitted.

## Unexecuted falsification protocol

Freeze an analytical and future executable protocol for:

1. neutral + RECALL → no output;
2. subthreshold state + RECALL → no output;
3. supra-threshold stored state + no RECALL → no output while held;
4. that same state + RECALL → exactly one excursion/event;
5. equivalent release after distinct HOLD durations → same release trajectory
   within an independently justified numerical bound;
6. ungated reference trajectory;
7. deterministic recurrence/trajectory and event conversion;
8. bounded return to neutral, expiry, and representable-future scheduling.

Define an independent oracle, operation and solver/step bounds, numerical
error/tolerance derivation, exact deterministic fields, and pass/fail rules.
No arbitrary tolerance or outcome-tuned threshold. State how independent
replay and equation or high-precision reference avoid sharing the candidate
implementation. No simulation, code, tests, trajectories, or trials in this
design assignment.

## Architecture and evidence boundary

Map A01-A08 and A12-A15. Preserve A06 prediction/error capability and A07
locality as separate core obligations; do not claim the excursion design
implements learning, prediction-error propagation, local energy/utility, or
delayed credit (A09-A11). Bound state, event generation, and lifetime (A08).
Identify every departure from ACP-0008 as isolated experimental proposal, not
accepted semantics. No spatial reservoir, global evaluator input, answer
buffer, sequence decoder, or label-conditioned state.

This model design must not consume unpublished 63B work/results, 63A raw
artifacts, evaluator truth, or any external sequence buffer. The reviewed
63A conclusion may be cited only as the isolated scalar HOLD result; it does
not establish this candidate's stability, event conversion, or output.
Luna-62 remains proposed and ACP-required; no alternative is adopted.

## Stop and acceptance

Deliver a self-contained candidate specification and unexecuted protocol, or
report **LUNA-63C DESIGN STILL UNBOUNDED** with the exact missing equations or
owner choices. An independent Luna-0 review is required. A bounded design
may only make a future mechanism experiment eligible for a separate decision;
this contract does not authorize that experiment.

Never claim recall, sequence memory, task efficacy, hardware equivalence,
ACP acceptance, core promotion, integrated sequence echo, or Luna-64. Stop
after the design report and handoff.
