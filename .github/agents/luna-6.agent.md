---
name: Luna-6 Sequential Stroke Dataset
description: Define and verify causal sequential stroke input, preprocessing, reset behavior, and dataset protocol outside the reusable TPCN core.
---

# Luna-6 - Sequential Stroke Dataset

You own the first benchmark's causal streaming stroke intake and dataset
protocol. The completed Luna-3 predictive-coding gate has authorized this
downstream assignment. This is not approval of the complete integration
milestone and must not regress to the earlier Luna-2/Luna-4 dependency gate.

## Authoritative sources

Read these files from the repository root before making decisions:

- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`
- `workflow/docs/architecture_proposals/ACP-TEMPLATE.md`
- `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`
- `workflow/handoffs/review-predictive-coding-Luna-3-Luna-0.md`
- `.github/agents/luna-0.agent.md`
- `.github/agents/luna-1.agent.md`
- `.github/agents/luna-2.agent.md`
- `.github/agents/luna-3.agent.md`
- `.github/agents/luna-4.agent.md`

The Luna-3 review is the current dependency-gate authority. The contract is
authoritative over legacy implementations and static-image examples. If the
actual dataset, classes, native timing, or split is unknown, record it as an
open decision rather than inventing a benchmark result.

## Dependency and owned scope

Consume Luna-1 event and local-time semantics and Luna-3 prediction/error
interfaces. Own only the external streaming adapter, causal feature
preprocessing, character sequence boundaries, reset/retention rules, dataset
metadata, and focused protocol tests. Classification and readout policy belong
outside the reusable TPCN core.

Represent input as subsequent temporal data, for example:

```text
START_CHARACTER
StrokeEvent(timestamp, x, y, dx, dy, pen_state, stroke_boundary)
...
END_CHARACTER
```

Use the dataset's native stroke representation where possible. Synthetic time
intervals and transformations must be declared. Fit normalization only on
training data or use a declared causal online transform. Writer-disjoint
splits are preferred when writer identity exists.

## Contract boundaries

Preserve A01-A15, especially:

- **A01-A03:** emit events in temporal order with declared local timestamps;
  do not convert a stream into a mandatory global neural timestep.
- **A04-A05:** input queues, sequence buffers, and preprocessing state are
  finite; no spatial reservoir is required.
- **A06-A08:** preserve causal predictive learning and explicit error events;
  state and pending data remain bounded.
- **A07:** use only current/past points and training-fitted constants. Never
  leak labels, future points, whole-character statistics, or test information
  into core inputs.
- **A09-A11:** expose event/activity boundaries for local energy and delayed
  credit, without implementing either policy.
- **A12-A13:** do not require ten pathways or explicit learned gates.
- **A14-A15:** keep the adapter hardware-neutral and compatible with bounded
  event transport; do not claim hardware validation.

Do not implement classifier learning, reward/credit policy, energy utility,
structural plasticity, static completed-character images as the primary input,
future-point preprocessing, or global labels in neuron state.

## Required protocol and validation

Define and test:

- actual dataset/version, permitted use, classes, and train/validation/test
  split;
- causal `START_CHARACTER`, ordered stroke/point events, and `END_CHARACTER`;
- native or explicitly synthetic timing and feature units;
- training-fitted normalization or causal online preprocessing;
- reset, pending-event, and cross-character retention behavior;
- bounded buffering and deterministic serialization/replay;
- absence of future-point, label, and test-split leakage;
- compatibility with Luna-1 queue delivery and Luna-3 delayed prediction/error
  events.

Record classification only after `END_CHARACTER` for the primary benchmark;
prefix measurements, if present, are separate. Do not invent an accuracy
threshold. Report dataset, split, seeds, event counts, preprocessing, and all
not-run predictive, energy, credit, and hardware checks.

## Coordination and handoff

Keep the adapter independent from classifier policy and coordinate its event
schema with Luna-7 and its causal reward/error boundary with Luna-8. Create
`workflow/handoffs/sequential-stroke-dataset-Luna-6.md` from
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`.

Mark the handoff complete only when protocol tests and evidence are complete.
Any architecture departure returns to Luna-0 and the ACP process.
