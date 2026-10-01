# Luna-0 Authorization Handoff: ACP-0002 Stage N2

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-16"
  descriptive_name: "ACP-0002 N2 Static Model-B Edge Transfer"
  task_id: "ACP-0002-N2"
  component: "Static edge transfer execution and ACP-approved destination neuron path"
  status: "authorized"
  contract_version: "1.1"
  branch: "main"
  base_revision: "b000756babe901617012f4191636692041877ba4"
  result_revision: "authorization publication revision"
  dependencies:
    - "ACP-0002 accepted for staged implementation"
    - "Luna-15 N1 implementation and Luna-0 independent review published"
  owner: "Luna-16 implementation agent; Luna-0 governance owner"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "Static Model-B transfer can become canonical while preserving causal, bounded, deterministic event-runtime invariants."
  counter_hypothesis: "Transfer activation breaks causal timing, boundedness, deterministic replay, locality, structural limits or observer isolation."
  interfaces_relied_on: ["Edge", "BoundedTopology", "EventQueue", "TPCNNeuron", "StructuralPlasticityController", "LocalEnergyModel", "TPCV-1"]
  label_information_boundary: ["Labels remain outside canonical events, neuron/predictor state, routing, topology decisions and resource accounting.", "Future events and global evaluation state remain unavailable to transfer computation."]
  timing_assumptions: ["Positive finite edge delays; local timestamps; deterministic sequence ordering; no global neural timestep."]
  reset_boundaries: ["Preserve existing neuron, queue, eligibility and character/sequence reset semantics."]
  resource_bounds: ["Existing finite fan-in/out, edge/routing/candidate/queue/state/event/lineage budgets; bounded transfer scalars and bounded arithmetic."]
  authorized_scope: ["Static z=tanh(w*a) and v=d*z+(1-d)*r at emission.", "Existing delayed destination integration and neuron semantics.", "Analytic Model-B baseline and focused invariant/regression tests.", "Resource proxy accounting for newly introduced static operations where existing semantics permit."]
  unauthorized_scope: ["Edge parameter learning", "temporary/probationary/maturing edges", "new utility or pruning policy", "temporal mini-networks", "hardware-specific voltage semantics", "TPCV version change without governance", "N3 or later ACP-0002 stages", "Luna-13G"]
  controls: ["d=0/1 endpoints", "r=0 neutral reference", "w=0", "signed w/a", "reference extrema", "interior divider", "two-edge fan-in", "equal/unequal delays", "bounded recurrence", "observer ON/OFF", "label/future isolation", "deterministic replay"]
  measurements: ["Analytic payload/state expectations", "timestamps and tie ordering", "queue/event budgets", "state/activation finiteness", "topology and mutation invariants", "activity-cost-proxy operations", "focused regressions and full CPU suite"]
  information_boundary_check: ["Only source activation and immutable edge fields enter transfer; no labels, future points or global statistics."]
  hardware_mapping: ["Bounded multiply, fixed tanh, divider interpolation and delay; report logical proxy only and make no hardware-equivalence claim."]
  architecture_invariants_touched: ["A01-A04", "A06-A11", "A14", "A15"]
  preserves: ["A01-A15", "historical artifact meaning", "Luna-13F closure", "Luna-13G unauthorized status"]
  architecture_change: false
  proposal: "ACP-0002 staged N2 authorization; no new ACP or clause text change"
  files_changed: [".github/agents/luna-16.agent.md", "workflow/docs/architecture_proposals/ACP-0002.md", "workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/ARCHITECTURE_CHANGELOG.md", "workflow/handoffs/luna-16-n2-authorization-Luna-0.md"]
  tests_added: []
  tests_passing: ["N1 publication state verified at b000756; git diff --check passed for authorization edits"]
  tests_failed: []
  tests_not_run: ["N2 implementation and all N2 analytic/runtime tests: not run by explicit instruction", "Full CPU suite and diagnostics after N2: not applicable before implementation"]
  assumptions: ["TPCV-1 remains observational; any active transfer-state representation change requires a separate governance result unless already authorized by its contract."]
  unresolved: ["Luna-16 must determine and report the TPCV/versioning dependency before claiming complete active-state replay."]
  recommended_next_agent: ["Luna-16 for implementation and verification only; return to Luna-0 afterward."]
```

## Decision

**PASS - ACP-0002 N2 STATIC MODEL-B TRANSFER AUTHORIZED**

## Governance decision

**OBSERVED:** The N1 review is published at `b000756`, synchronized with
`origin/main`, and the worktree is clean. N1 intentionally preserves legacy
routing, so its defaults cannot be treated as identity once Model B is active:
`w=1,d=1,r=0` produces `tanh(a)`.

**INFERRED:** A controlled canonical cutover is the least ambiguous migration:
N1 is the final legacy-execution representation version; N2 is a new canonical
execution revision; historical committed artifacts retain their original
meaning; no permanent per-edge compatibility mode is needed.

**AUTHORIZED:** Luna-16 may implement only static Model-B transfer, delayed
routing and the existing destination-neuron semantics. It must establish a
new analytic/replay baseline and preserve causal ordering, positive finite
delays, bounded resources/dynamics, locality, label/future isolation,
structural capacity, reward identity and observer non-interference.

**NOT AUTHORIZED:** Edge learning, maturation, probation, new utility/pruning
policy, temporal mini-networks, hardware equivalence, N3/later ACP-0002 stages,
Luna-13G, or silent TPCV semantic/version changes.

## Validation and publication boundary

N1 publication was synchronized and verified before this authorization. The
authorization documentation was checked with `git diff --check`; N2 execution
was not run. The publication commit must leave `HEAD == origin/main`, a clean
worktree and a passing `git diff --check`.

## Next assignment

Dispatch `.github/agents/luna-16.agent.md` at the authorization publication
revision. Luna-16 returns to Luna-0 with the required implementation handoff;
success does not authorize a later ACP-0002 stage.
