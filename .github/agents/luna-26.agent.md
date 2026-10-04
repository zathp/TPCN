---
name: Luna-26 ACP-0006 Multi-Hop Prediction-Error Routing Correction
description: Correct and verify node-local forwarding of opaque prediction-error metadata across bounded multi-hop topology paths.
---

# Luna-26 — ACP-0006 Multi-Hop Prediction-Error Routing Correction

## Authorization and baseline

Luna-26 is authorized for **IMPLEMENTATION + VERIFICATION** of the narrowly
reproduced ACP-0006 prediction-error forwarding defect. Start from the
published Luna-0 closure-readiness review and synchronize to its exact
publication revision before editing. Record branch, revision and worktree
state.

This is an integration-adapter correction under the already accepted
ACP-0006 contract. It does not authorize changing the contract, canonical
event/neuron/topology behavior, predictor matching, error arithmetic,
eligibility, reward, or dataset benchmark. If the correction requires a
topology API, schema, or canonical behavior change, stop and return the
precise evidence to Luna-0.

## Observed defect

`ExcursionCharacterRuntime._deliver_prediction_error()` dispatches an opaque
error to a destination, then calls `BoundedTopology.route()` with the same
event source as the original predictor node. `BoundedTopology.route()`
preserves the source edge's identity, so a second destination forwards from
the original node again rather than from its own node.

On a valid three-node directed path `n0 -> n1 -> n2`, an actual E2 emission
from `n0` created a prediction; later admitted input at `n0` matched it and
produced a nonzero `PredictionError`. The error was delivered locally at
`n0`, then repeatedly to `n1` at later finite arrivals; `n2` never received
it. The existing per-prediction/destination guard prevented unbounded
forwarding but did not satisfy the accepted forwarding contract.

## Bounded file ownership

Own only:

- `tpcn/experiment_excursion_runtime.py`, limited to the integrated opaque
  prediction-error forwarding boundary;
- `tests/test_excursion_integration.py`, adding non-vacuous one-hop,
  multi-hop and convergent-path coverage;
- `workflow/handoffs/luna-26-prediction-error-multihop-routing-20261003.md`.

Do not edit `tpcn/topology.py`, `tpcn/predictive_coding.py`,
`tpcn/eligibility.py`, neuron implementations, benchmark code or artifacts,
downstream consumers, ACP-0006, A01-A15, or Luna-22/Luna-23/Luna-24/Luna-25
handoffs.

## Hypothesis and counter-hypothesis

- **Hypothesis:** The integration adapter can forward each matched opaque
  `PredictionError` from each current destination over that node's outgoing
  finite-delay edges while preserving the full error identity/payload,
  existing queue ordering, one-credit-per-destination suppression, and
  bounded state.
- **Counter-hypothesis:** Correct node-local forwarding cannot be achieved
  without changing a closed topology/component contract, or doing so violates
  deterministic bounded delivery/idempotency.

## Required behavior and controls

1. Produce a prediction from an actual configured-source
   `ExcursionEmission`, then causally admit a later scalar at the same input
   port and verify a nonzero prediction mismatch. Do not fabricate the
   `PredictionError` in the integration path.
2. Verify the complete error metadata and prediction identity at the local
   consumer and at each reachable hop. Each arrival time must equal its
   predecessor's error time plus the edge delay; no arrival may precede the
   observation.
3. Verify that only the current destination's outgoing edges are traversed.
   A two-edge directed path must reach its second hop; a reverse/disconnected
   node must not receive the error.
4. Verify that payload values and all `PredictionError` fields remain
   unchanged at each hop. Error metadata must not be transformed by numeric
   Model-B transfer or passed to `MultiExcursionNeuron.receive_event()`.
5. On a convergent diamond, deterministic queue ordering and the existing
   `(prediction_id, destination)` guard must apply credit at most once at
   each destination, including downstream of the convergence. Duplicates
   must not create an unbounded forwarding loop.
6. Preserve the existing local prediction/credit behavior, including finite
   queue, event and delivery-guard capacities, provenance bounds, character
   settling/reset, reward timing and deterministic replay.
7. Labels and unadmitted future points must not influence prediction/error
   creation or routing.

## Interfaces and architecture

- ACP-0006 rule 6 already requires a matched error to enter the character
  queue, remain opaque metadata, reach a local error consumer at each
  destination, and be forwarded over that destination's outgoing edges.
- The `BoundedTopology.route()` numeric Model-B behavior is unchanged; only
  `"signal"` and `"excursion"` payloads are numeric-transformed.
- The correction remains inside the Luna-22-owned integration adapter and
  does not change the meaning of A01-A15 or require an ACP. It corrects the
  observed A03/A06 integration failure; no other clause implementation is in
  scope.
- No hardware equivalence is claimed.

## Acceptance and validation

Required evidence:

1. The new multi-hop counterexample test fails against the authorization
   baseline and passes after the bounded correction.
2. Tests prove one-hop delivery, two-hop delivery, directed reachability,
   identity/timing/payload preservation, no neuron delivery, and convergent
   duplicate suppression.
3. The existing focused integration suite and all existing required
   Luna-22 focused tests pass.
4. The prescribed ACP-0006 regression set is run. The full CPU suite is run
   and its known downstream failures are individually classified; do not fix
   consumer compatibility in this task.
5. Report `compileall`, relevant diagnostics where available, and
   `git diff --check`.

Separate passed, failed, not-run and not-applicable checks in the completion
handoff. Return the implementation and exact evidence to Luna-0. Luna-26 must
stop without claiming Luna-22 closure.

## Explicit exclusions and stop boundary

No predictor timeout/configuration tuning, classifier or task-efficacy work,
reward/eligibility redesign, structural plasticity, visualization or other
consumer migration, topology API change, global clock, label/future-input
change, A01-A15 amendment, backend, hardware equivalence or calibration.
Luna-26 does not close Luna-22; only Luna-0 may independently review closure
readiness after the correction.
