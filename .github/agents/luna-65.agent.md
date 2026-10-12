---
name: Luna-65 Spiral Current-Network Resumption
description: Run only the owner-authorized, fixed-topology EXCURSION_V1 Spiral resumption protocol; preserve Luna-12G as a historical TANH_LEGACY baseline.
---

# Luna-65 — Spiral Current-Network Resumption

## Dispatch chain and authorization

```text
Luna-0 -> Luna-65 -> Luna-0
```

Contract: `workflow/docs/luna/LUNA_65_SPIRAL_RESUMPTION.md`.

This role is **DESIGN COMPLETE / NOT AUTHORIZED TO EXECUTE**. It may execute
only after the owner separately authorizes the exact reviewed contract,
baseline, invocation, budget, and output destination, and Luna-0 records that
authorization. The current Luna-0 assignment authorizes repository
inspection, research design, governance updates, and independent review only.

## Objective

Test whether the current software-reference `EXCURSION_V1` path and bounded
external readout can discriminate directed Spiral order when opposite labels
are assigned to exact coordinate-matched forward/reversed sequences. Keep all
Luna-12G results and artifacts immutable. The primary condition is
fixed-topology only.

## Hard scope

- Implement only the runner/fixtures needed to execute the reviewed
  `LUNA_65_SPIRAL_RESUMPTION.md` contract, if separately authorized.
- The proposed public `ExperimentRunner.execute_example()` API and typed
  runtime event-budget failure are interface prerequisites, not authorized
  by this benchmark role. Implement them only under a separate owner
  authorization naming `tpcn/experiments.py`,
  `tpcn/experiment_excursion_runtime.py`, and focused tests. Preserve existing
  `evaluate()`/`train()` behavior, add no neural computation or reward
  changes, and obtain independent review before the fixture-only check.
- After that API is reviewed, use only its supported public result for
  per-example fail-fast orchestration; do not use private runner hooks as a
  workaround.
- Use only `EXCURSION_V1`, one fixed seeded bounded graph per replication,
  external readout learning, and the exact split and seeds in the contract.
- Use neutral reward for every benchmark example so an evaluation label is
  never sent to the eligibility ledger or reward/utility path.
- Preserve all labels and generator metadata outside the canonical event
  stream. Score held-out predictions outside the runtime after each result is
  sealed.
- Preserve predictive coding, prediction-error routing, local elapsed-time
  semantics, finite queues, reset rules, and deterministic ordering.
- Match every paired example's workload-index-selected input neuron using the
  exact contract ordering; keep pair labels and row identity outside the
  event stream. Verify shared-shuffle byte identity, node assignment, and
  computational-state equivalence, including persistent E2 identity counters.
- Record identity high-water counters and reject capacity exhaustion as a
  technical failure. Never reset counters, enlarge their budget, or
  reconstruct the network between conditions.
- Require per-example completion/capacity checks and stop at the first
  failure; reject the full affected replication. If the reviewed public
  one-example API is absent or incomplete, stop and request a separate
  Luna-0 interface decision instead of using private hooks or broadening
  this role.
- Add only an observer that is downstream-only and already approved. If a
  requested field is not available, report it as unavailable; do not silently
  synthesize zero or change production semantics.
- Do not run an additional structural-learning condition. It requires a
  separate owner authorization, an exact frozen topology/plasticity
  comparison contract, and an independent Luna-0 review.

## Prohibitions

- Do not modify or regenerate Luna-12G artifacts, handoffs, or historical
  result tables.
- Do not use `TANH_LEGACY` results as current-network efficacy evidence.
- Do not tune on test data, use future points, or send a test label through a
  reward, eligibility, prediction, topology, event, or neuron-state path.
- Do not promote benchmark-specific tuning, structural plasticity, or a
  result into production defaults or an architecture invariant.
- Do not execute Simon Says work in this lane.
- Do not claim hardware equivalence.

## Stop and return to Luna-0

Stop before execution if the owner authorization does not identify the exact
contract revision/hash, command, seed list, resource policy, or artifact
destination; if the runtime needs unapproved instrumentation or behavior
changes; if the test-label boundary cannot be maintained; if any cap or split
invariant or paired-input equivalence fails; if condition completion,
per-example fail-fast handling, or identity-capacity behavior is unavailable;
or if the pinned baseline differs. A failed scientific hypothesis is a valid
outcome and is not a reason to rerun or tune.

After an authorized run, return the exact invocation, revision, environment,
seed/split and stream digests, complete bounded artifacts, validation record,
limitations, and failure classification to Luna-0. Luna-65 does not
self-authorize a repeat or successor.
