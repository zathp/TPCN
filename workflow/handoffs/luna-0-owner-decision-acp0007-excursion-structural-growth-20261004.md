# Luna-0 Owner Decision — ACP-0007 EXCURSION_V1 Structural Growth

**DECISION: ACCEPTED WITH OWNER-SPECIFIED LOCAL OBSERVATION CONTRACT.**

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-0 ACP-0007 owner decision"
  descriptive_name: "EXCURSION_V1 structural re-entry decision"
  task_id: luna-0-owner-decision-acp0007-excursion-structural-growth-20261004
  component: "ACP-0007 and contract version 1.2"
  status: complete
  contract_version: "1.2"
  branch: main
  base_revision: 2e692337d339704eebf5b9d060409be25804be8e
  result_revision: "this handoff's governance publication commit"
  dependencies: ["ACP-0006", "Luna-0 structural re-entry readiness review"]
  owner: "Project owner"
  classification: ["GOVERNANCE", "ARCHITECTURE DECISION"]
  hypothesis: "An explicit bounded observation contract permits a local E2 growth experiment without changing general core defaults."
  counter_hypothesis: "The authorized observation contract cannot be implemented without changing protected core behavior or violating locality/boundedness."
  interfaces_relied_on:
    - "Canonical ExcursionEmission identity and timestamp"
    - "TemporalAssociationPolicy bounded count evidence"
    - "StructuralPlasticityController"
    - "BoundedTopology and post-character E2 lifecycle"
  label_information_boundary:
    - "No labels, payload magnitude, prediction loss, reward, readout, accuracy, energy, global metrics, or future/held-out data enters structural scoring."
  timing_assumptions:
    - "Only strictly later timestamps within the declared association window form evidence."
    - "Mutation is permitted only at the inactive post-character/pre-next-character boundary after successful settling and teardown."
  reset_boundaries:
    - "Evidence and candidate state reset and are consumed per character."
    - "Grown topology persists only within the experiment; experiment reset creates a new model/topology namespace."
  resource_bounds:
    - "Static neighborhood and reverse observers are finite and explicit."
    - "History, candidates, scores, event work, and growth attempts are bounded."
    - "At most one growth attempt and one admitted edge per completed character; no pruning."
  authorized_scope:
    - "Accept ACP-0007 with the local observation, lifecycle, growth-only, and validation conditions stated in the proposal."
    - "Authorize Luna-28 implementation and verification only."
  unauthorized_scope:
    - "Luna-13F efficacy/resource claims, A14 promotion, pruning, ACP-0002 N3, neuron or prediction/reward/readout changes, IR-2 changes, downstream migrations, and hardware equivalence."
  controls:
    - "Fixed-topology EXCURSION_V1 remains the default and rollback control."
    - "Observation-on/mutation-off must be behaviorally non-interfering."
  measurements:
    - "No experiment rerun or implementation verification is claimed by this decision."
  information_boundary_check:
    - "Only actual canonical emission identity and timestamp may enter the bounded structural observation plane."
  hardware_mapping:
    - "No hardware result or equivalence claim; bounded local semantics remain hardware-neutral requirements."
  architecture_invariants_touched: ["A01", "A03", "A04", "A07", "A08", "A14", "A15"]
  preserves:
    - "A01-A15 substantive text and scope"
    - "ACP-0006 fixed-topology default"
    - "Luna-13F NOT SUPPORTED useful-growth prediction and NOT ESTABLISHED resource benefit"
    - "No post-guard pass claim for the 19 structural downstream failures"
    - "Luna-12E classification separating routed activity causation from unchanged prediction loss and legacy clock assertions"
  architecture_change: true
  proposal: "workflow/docs/architecture_proposals/ACP-0007.md — Accepted"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0007.md"
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-owner-decision-acp0007-excursion-structural-growth-20261004.md"
    - "workflow/handoffs/luna-0-authorization-luna-28-excursion-local-temporal-growth-20261004.md"
    - ".github/agents/luna-28.agent.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Luna-28 implementation and acceptance tests"
    - "Downstream assertions after the structural guard"
    - "Hardware equivalence"
  assumptions:
    - "The detailed project-owner decision supplied in the conversation is authoritative for ACP-0007 acceptance conditions."
  unresolved:
    - "Whether mechanism-valid growth improves a task or resource tradeoff; no such claim is authorized by ACP-0007."
  recommended_next_agent:
    - "Luna-28 under the separate Luna-0 authorization handoff; then Luna-0 independent review"
```

## Decision and interpretation

The project owner accepted ACP-0007 with the complete local temporal
observation terms published in the proposal. This permits only the bounded,
opt-in, growth-only EXCURSION_V1 experiment and does not make structural
plasticity a default or a general required behavior. The authoritative
contract is now version 1.2; A01-A15 clause text and scope are unchanged.

The observation plane receives only identity and timestamp from actual
canonical `ExcursionEmission` instances. A static directed neighbor fabric
and reverse-observer limits are explicit and finite. Only strict positive
local temporal order within the configured window increments bounded
association counts. Per-character evidence is frozen after successful
settling, consumed at the quiescent boundary, and can cause at most one
bounded growth attempt. The configured positive delay is not learned.
Topology persists across later characters only within the experiment, and the
same bounded topology is used by E2 routing.

Pruning, N3 parameter learning, neuron/prediction/reward/readout changes,
IR-2 extension, downstream migrations, hardware implementation/equivalence,
and efficacy/resource claims are excluded. Luna-13F's useful-growth
prediction remains **NOT SUPPORTED** and resource benefit remains **NOT
ESTABLISHED**.

## Preserved evidence

The historical readiness review remains **BLOCKED at that time**: the five
downstream test groups reported 19 failures and 12 passes; every failure
terminated at the intentional E2 structural-mode guard. The 69 focused
structural/evidence regression tests passed. No result establishes the
downstream assertions after the guard.

The separate Luna-12E classification remains unchanged: the reachable
topology intervention causally changes routed activity (12 to 14 processed
events, route depth 0 to 1, and edge-transfer proxy 0 to
1.358357398350786) while aggregate prediction loss remains exactly
1.1724999999999999. The exact post-evaluation clock expectations are legacy
observables inconsistent with the current E2 settle/reset lifecycle; neither
is evidence that the other failed invariant is repaired.

## Validation and next step

This is a governance decision and publication, not an implementation run.
Luna-28 tests, post-guard downstream behavior, and hardware equivalence are
not run. See the separate authorization handoff for exact implementation
scope and acceptance gates.
