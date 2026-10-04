# Luna-0 Corrective Authorization — Luna-26 ACP-0006 Route-Path No-Revisit

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Authorize bounded Luna-26 route-path correction"
  task_id: "luna-0-authorization-luna-26-corrective-route-path-20261003"
  component: "ACP-0006 rule 3 no-revisit routing for opaque prediction errors"
  status: "authorized; implementation not yet executed"
  contract_version: "ACP-0006 1.1"
  branch: "main"
  base_revision: "c7fc9b7477e8419af2282969b936db3a242e751b"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "An optional route-path destination exclusion preserves legal outgoing fan-out and atomically prevents a repeated node from being queued."
  counter_hypothesis: "Existing topology routing cannot enforce the accepted no-revisit rule without changing unrelated topology behavior or losing atomic queue admission."
  architecture_change: false
  proposal: null
  architecture_invariants_touched: ["A03", "A04", "A06", "A08", "A09"]
  dependencies:
    - "Accepted ACP-0006 rule 3 and rule 6"
    - "Published Luna-26 implementation and independent blocked review"
  authorized_scope:
    - "Continue the existing Luna-26 assignment; do not create Luna-27."
    - "Add an optional, backward-compatible destination-exclusion argument to tpcn/topology.py BoundedTopology.route()."
    - "Use that argument only for integrated opaque prediction-error forwarding in tpcn/experiment_excursion_runtime.py, passing the current per-event route_path."
    - "Add/adjust focused coverage in tests/test_topology.py and tests/test_excursion_integration.py."
    - "Publish a Luna-26 corrective completion handoff and return to Luna-0 for independent review."
  unauthorized_scope:
    - "No ACP-0006, A01-A15, Model-B equation, event/neuron semantics, predictor matching, error arithmetic, eligibility, reward, readout, dataset, downstream-consumer, backend or hardware change."
    - "No removal or weakening of the per-(prediction_id, destination) delivery guard."
    - "No global visited-node state; exclusions are per routed-event path only."
    - "No broad topology API redesign or unrelated caller migration."
  controls:
    - "Reject only destinations already in the current route_path before queue preflight/push."
    - "Retain every non-repeated outgoing destination, including legal fan-out when one sibling edge would revisit a node."
    - "Ensure excluded events are not queued, sequenced, sidecar-attached, processed or energy-accounted."
    - "Preserve deterministic outgoing-edge order and atomic capacity failure for the legal fan-out."
    - "Preserve convergence: sibling paths may independently reach a shared node; only the existing delivery guard suppresses the later duplicate continuation."
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Corrective implementation and validation are not yet run."
    - "Hardware equivalence and physical-energy calibration are not authorized."
  unresolved:
    - "Luna-26 remains blocked pending implementation and independent Luna-0 review."
    - "Luna-22 remains blocked and is not closed."
  recommended_next_agent: ["Luna-26"]
```

## Evidence and reason for this bounded authorization

The independent review at base revision
`c7fc9b7477e8419af2282969b936db3a242e751b` observed a real generated error
with route path `("n0", "n1", "n0")` on `n0 -> n1 -> n0`. ACP-0006 rule 3
explicitly prohibits a repeated node within one routed-event path. The
destination dedupe guard terminates after the prohibited return event has
already been queued, processed and counted.

The current `BoundedTopology.route()` routes every outgoing edge from the
source and preflights the complete fan-out against queue capacity. It has no
way to filter one back-edge while retaining other legal edges from the same
node. Filtering the whole fan-out would incorrectly suppress legal routes;
queueing all edges and cancelling a revisit afterward would still create a
prohibited queued event and distort sequence, sidecar, event and cost
accounting. Therefore the correction is explicitly authorized to add one
optional exclusion parameter to the existing route API.

The new argument must default to the current behavior for every existing
caller. When supplied, `route()` filters only edges whose destination is in
the supplied current-path exclusion collection, then performs the existing
capacity preflight and queues all remaining edges atomically. The error
adapter must pass that arriving event's `RouteContext.route_path`. This
preserves path-local semantics: a node reached by a different legal sibling
path is not globally excluded. Existing per-destination deduplication remains
responsible for one local credit and one continuation at convergence.

This is a narrow implementation correction to an already accepted invariant;
it does not change the ACP, route timing, edge equations, or default
topology behavior. If the required semantics cannot be implemented within
this exact scope, stop and return the evidence to Luna-0 rather than adding
another Luna identifier or broadening the architecture.

## Required completion evidence

The Luna-26 corrective handoff must report:

- Exact baseline revision and files changed.
- A regression showing the prior route-path violation and corrected cycle
  that never queues a repeated destination.
- A graph containing both a back-edge to a visited node and a legal
  unvisited outgoing edge; only the back-edge is excluded.
- A directed path, unequal delays, non-identity Model-B parameters, opaque
  payload/identity preservation, and no neuron delivery.
- Equal-time convergence, distinct legal route paths to the same destination,
  per-destination dedupe, and exactly one post-convergence continuation.
- Route depth/path bounds; no repeated node on any queued error event.
- Proof that excluded edges consume no queue sequence, sidecar, processed
  event or edge/error cost; legal edge work retains existing accounting.
- Atomic queue-capacity failure for the post-exclusion legal fan-out.
- Character reset and delivery-guard behavior.
- The focused suite, prescribed ACP-0006 regressions, full-suite failure
  identities, collection count, compileall, diagnostics and `git diff --check`.
- Explicit passed/failed/not-run/not-applicable controls. No Luna-22 closure
  claim; the result returns to Luna-0 for independent review.
