---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-15 contract creation"
  descriptive_name: "ACP-0002 Edge/Neuron Data Model and Compatibility"
  task_id: "luna-15-n1-contract-creation"
  component: "agent contract and authoritative workflow"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "a24773eac26151c02b953158df9eb19766184c60"
  result_revision: "uncommitted"
  dependencies:
    - "ACP-0002 Accepted for staged implementation"
    - "Luna-0 mathematical review and ACP-0002 handoff"
    - "existing event runtime, topology, neuron and structural-plasticity APIs"
  owner: "Luna-0 / project owner"
  classification:
    - "IMPLEMENTATION CONTRACT CREATION"
    - "N1 ONLY"
    - "CPU software reference"
    - "return to Luna-0 for independent review"
  hypothesis: "N1 can add bounded explicit edge/neuron state and compatibility representation without changing routed payload semantics or deterministic event behavior."
  counter_hypothesis: "The N1 representation cannot preserve legacy construction, structural-plasticity, observer, replay or payload behavior without a separately reviewed architecture change."
  interfaces_relied_on:
    - "TPCN Edge and BoundedTopology"
    - "TPCNNeuron and existing neuron gain/input-gain compatibility"
    - "event runtime, EventQueue and delayed routing"
    - "structural-plasticity topology rebuild and bounded admission interfaces"
    - "observer/instrumentation interfaces"
    - "ACP-0002 Model B schema and bounds"
  label_information_boundary:
    - "Labels, future outcomes and evaluation results must not enter N1 representation or routing."
    - "No global trainer state or utility-learning mechanism is introduced."
  timing_assumptions:
    - "Existing positive finite propagation delay, event timestamp and sequence semantics remain unchanged."
    - "N1 introduces no global neural timestep and no transfer-time behavior."
  reset_boundaries:
    - "No new reset or learning boundary is introduced; existing topology persistence/reset policy remains authoritative."
  resource_bounds:
    - "edge_weight/w_ij in [-2,2]"
    - "divider_strength/d_ij in [0,1]"
    - "reference/r_ij in [-1,1]"
    - "neuron_gain/g_j in [0,2]"
    - "existing finite topology, fan-in/out, queue, event and delay limits"
  authorized_scope:
    - "Create .github/agents/luna-15.agent.md."
    - "Implement only N1 edge/neuron data model and compatibility representation."
    - "Add analytic and regression tests for bounds, compatibility, replay, observers, structural interfaces and payload preservation."
    - "Update relevant documentation and this handoff."
    - "Return to Luna-0 for independent review after N1 implementation."
  unauthorized_scope:
    - "N2 propagation or Model-B transfer activation"
    - "Adaptive edge learning, temporary/probationary connections or maturation"
    - "Local time-series mini-NNs or new utility-learning mechanisms"
    - "A01-A15 changes or ACP promotion"
    - "Luna-13G authorization or reopening Luna-13F"
    - "Treating N1 completion as automatic N2 authorization"
  controls:
    - "Legacy constructor and identity-adapter regression"
    - "Payload/event/timestamp/delay preservation"
    - "Deterministic repeated representation and replay"
    - "Structural-plasticity creation/rebuild compatibility"
    - "Observer/instrumentation ON/OFF non-interference"
    - "Explicit no-transfer activation check"
  measurements:
    - "Validated field values and rejected invalid values"
    - "Serialized/inspected representation stability"
    - "Event trace and routed payload equality before/after N1 representation"
    - "Legacy, topology and observer regression outcomes"
  information_boundary_check:
    - "N1 contains no labels, future outcomes, global statistics or new learning signal."
    - "N1 does not change the event payload or compute Model B."
  hardware_mapping:
    - "Finite logical scalar fields remain hardware-neutral."
    - "No FPGA/FPAA implementation or hardware-equivalence claim is authorized."
  architecture_invariants_touched:
    - "A01"
    - "A03"
    - "A04"
    - "A08"
    - "A15"
  preserves:
    - "A01-A15 unchanged"
    - "ACP-0002 Accepted for staged implementation"
    - "Luna-13F CLOSED"
    - "Luna-13G unauthorized"
    - "existing routed payload semantics and event-driven runtime"
  architecture_change: false
  proposal: "ACP-0002"
  files_changed:
    - ".github/agents/luna-15.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-15-n1-contract-creation-Luna-0.md"
  tests_added: []
  tests_passing:
    - "Authoritative contract and ACP-0002 reviewed before contract creation."
    - "Starting revision matched origin/main before editing."
  tests_failed: []
  tests_not_run:
    - "Luna-15 N1 implementation: not run by instruction."
    - "Production tests: not run; this is contract creation only."
    - "Hardware checks: not run and not applicable to contract creation."
  assumptions:
    - "The current repository root uses workflow/ as the authoritative path."
    - "The published revision is recorded after the requested commit and push."
  unresolved:
    - "N1 implementation details and test results remain for Luna-15 and independent Luna-0 review."
    - "N2 transfer execution remains separately gated and unauthorized."
  recommended_next_agent:
    - "Luna-15, only for the exact N1 scope in .github/agents/luna-15.agent.md"
    - "Luna-0 independent review after N1 completion"
---

## Outcome and authorization evidence

`OBSERVED`: ACP-0002 is **Accepted for staged implementation** at the starting
revision. The contract preserves the accepted normalized domains and future
Model-B equation as architecture context.

`INFERRED`: N1 can be implemented as a representation and compatibility step
without changing routed payload semantics, because transfer execution is
explicitly deferred and the existing event runtime remains the owner of delay,
identity, ordering and delivery.

`HYPOTHESIZED`: Focused analytic and regression tests can demonstrate that the
new bounded fields, legacy mapping, topology rebuild paths, observer paths and
replay representation do not alter existing behavior.

No N1 implementation was executed in this Luna-0 contract-creation task.

## Validation record

| Command or procedure | Revision / environment | Observed result | Evidence |
|---|---|---|---|
| Read architecture contract, ACP-0002, workflow and handoff template | `a24773e`, Windows | Passed; ACP accepted, contract 1.1 and A01-A15 unchanged | Authoritative governance files |
| Inspect agent-contract and Luna-0 handoff conventions | `a24773e`, Windows | Passed; creation-only and return-to-Luna-0 patterns preserved | Existing `.github/agents` and handoffs |
| Luna-15 N1 implementation | Not applicable | Not run by instruction | Explicitly prohibited in this task |
| Production regression suite | Not applicable | Not run; contract creation only | No production code authorized or changed |
| Hardware validation | Not applicable | Not run | No hardware work authorized |

## Next assignment

Luna-15 is authorized only for N1 edge/neuron data model and compatibility
representation under `.github/agents/luna-15.agent.md`. It must preserve routed
payload semantics, add no transfer execution or learning, and return to Luna-0
for independent review. N1 completion does not authorize N2.
