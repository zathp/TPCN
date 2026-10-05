---
name: Luna-43 ACP-0008 Destination Integration Mechanism
description: Compare disabled, default, and calibrated destination integration with a frozen calibrated relay on the reviewed fixed two-hop route.
---

# Luna-43 — ACP-0008 Destination Integration Mechanism

## Authorization and execution boundary

Luna-43 is **AUTHORIZED / NOT EXECUTED** only for the mechanism experiment
below, under the current project-owner direction and the matching Luna-0
authorization handoff. This contract supersedes the earlier, mistakenly
published test-comparison authorization. Do not execute that old test-only
assignment. This contract does not authorize Luna-44.

Before editing or running the experiment, read the architecture contract,
ACP-0008, ACP-0007, Luna-42 contract/runner/results, the independent post-Luna-42
review, and Luna-40/41/42 handoffs named by the authorization handoff. Verify
the exact authorization revision, branch, clean worktree, and synchronized
baseline before execution. Publish the owned runner/tests/configuration before
running; capture the non-null execution revision, runner hash, frozen config
digest, and environment identity. If required provenance or any interface
assumption cannot be verified, stop BLOCKED and return to Luna-0.

Luna-43 must not run in the Luna-0 authorization pass. Do not change production
code, execute historical Luna-40/41/42 runners, or modify their artifacts,
outcomes, or handoffs.

## Objective and falsifiable hypothesis

Using the exact reviewed Luna-42 Phase-B stream and bounds, determine whether
the already observed ACP-0008 calibrated relay emissions cause distinct
downstream destination behavior when the destination is configured with:

1. integration disabled (`integration=None`);
2. default integration (`IntegrationConfig()`, `decay_rate_z=0.1`); or
3. calibrated integration (`IntegrationConfig(decay_rate_z=0.0125)`).

The relay is always integration-enabled with the frozen calibrated
`decay_rate_z=0.0125` in all three arms. The hypothesis is that destination
integration configuration can change destination integration-mediated
emissions under this fixed routed stream. No destination emission or
between-arm difference is guaranteed; a null/negative result is valid.

This is mechanism-only. Do not score classification, accuracy, task efficacy,
prediction improvement, reward, utility, energy benefit, or structural-growth
benefit.

## Frozen interface and conditions

Use the existing production `MultiExcursionNeuron`,
`ExcursionCharacterRuntime`, and `BoundedTopology` APIs. Use only the static
directed edges:

- `source -> relay`
- `relay -> destination`

Both are ordinary fixed Model-B edges with delay `1.0`, `w=1.0`, `d=1.0`,
`r=0.0` (`divider_strength=1.0`, `reference=0.0`). No
`source -> destination` edge or other shortcut may exist. Keep the reviewed
three-node bounded topology, fan-in/out limits 2, and edge/routing capacities
3. Do not enable, invoke, or emulate ACP-0007 growth; topology is identical and
fixed in all arms.

Configuration by node:

- source: unchanged Luna-42 Phase-B E1 configuration, integration disabled;
- relay: unchanged Luna-42 Phase-B E1 configuration, ACP-0008 enabled at
  `decay_rate_z=0.0125`;
- destination: unchanged Luna-42 Phase-B E1 configuration, with only its
  integration condition varied across the three arms above.

All other ACP-0008 parameters and E1 parameters remain at the reviewed defaults:
`input_gain=1.0`, `discharge_quantum=1.0`, `z_max=4.0`, fast
`decay_rate=1.0`, and unchanged thresholds, delays, amplitude bounds,
provenance limits, and event budgets. Read the exact Luna-42 Phase-B runner
constants as the source of truth for stream and runtime bounds; do not infer or
retune them.

Reuse matched inputs and ordering from the Luna-42 Phase-B protocol: seeds
`0..4`, 64 sequences per seed, fresh per-character runtime/neuron state, and
the same points in each condition. Consume only each example's ordered point
coordinates/timestamps. Do not read labels, classes, evaluation outcomes, or
label-bearing metadata. Preserve the reviewed neutral reward and fixed
prediction/eligibility/runtime capacities. The outer classifier/readout is not
an endpoint and must not influence neural input or condition selection.

## Measurements and acceptance

Record the frozen configuration and exact topology for every arm. Reconcile
source emissions, `source -> relay` transfers/receptions, relay
integration-mediated emissions, `relay -> destination` transfers/receptions,
destination traces and emissions by event identity, timestamp, route and
payload. Distinguish direct from integration-mediated destination emissions.
Record fixed resource limits and observed event/queue/eligibility high-water
marks, completion/settling, bounded-state checks, and deterministic replay.
Ensure all arms have identical input digests and that the relay's configuration,
trace, emissions and onward route records are identical across arms throughout
each matched sequence; the fixed topology has no return path from destination
to relay.

Predeclare the comparison and causal acceptance checks in the runner/tests
before execution. Preserve exact identity/order/replay assertions; use the
already declared binary64 comparison formula only for equation-derived
floating-point reconstructions:

`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`

Passing the mechanism gate means valid bounded execution, exact matched inputs,
causal route/reception reconciliation, correct condition isolation, and
deterministic replay. It does not require a destination emission or a positive
effect. Report emissions and state observations without inventing an accuracy
threshold or efficacy conclusion. Retain any failed, incomplete, or
resource-exhausted arm; do not retry with increased limits or tuned parameters.

## Owned files and exclusions

Own only:

- `run_luna43_acp0008_destination_integration_mechanism.py`
- `tests/test_luna43_acp0008_destination_integration_mechanism.py`
- `artifacts/luna43-acp0008-destination-integration-mechanism/`
- `workflow/handoffs/luna-43-acp0008-destination-integration-mechanism-20261005.md`

Do not change neuron, runtime, routing, topology, classifier, readout, or
production APIs; ACP-0008/ACP-0007; architecture documents; previous runners,
tests, artifacts or handoffs; or any experiment parameters. Do not add an
architecture proposal: this is an experiment using the existing accepted
opt-in ACP-0008 behavior and static topology. ACP-0008 remains experimental,
opt-in and unpromoted; ACP-0007 remains unchanged and disabled.

## Validation and return

Run the new focused tests, applicable ACP-0008/runtime/routing regressions, the
full repository suite, and `git diff --check`. Report exact commands, revision,
environment, counts, skips, failures, and artifact digests. Classify every
check as passed, failed, not run, or not applicable. If any unrelated baseline
failure appears, stop and return to Luna-0 without expanding scope. Return the
completed handoff and evidence to Luna-0 for independent review. Do not
self-review, claim promotion, or authorize a successor.
