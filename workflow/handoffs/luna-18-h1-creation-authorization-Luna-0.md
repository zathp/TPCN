# Luna-0 Creation and Authorization Handoff: Luna-18 H1

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-18"
  descriptive_name: "ACP-0003 H1 Execution IR and Backend Interface Skeleton"
  task_id: "luna-18-h1-creation-authorization"
  component: "Hardware-neutral Execution IR and minimal backend interface contract"
  status: "authorized-not-started"
  contract_version: "1.1"
  branch: "main"
  base_revision: "a757fe510c5b3545da2161b27a53deaae01676bf"
  result_revision: "uncommitted governance update"
  dependencies:
    - "ACP-0003 accepted for staged implementation"
    - "ACP-0002 N2 closed"
  owner: "Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION"]
  hypothesis: "A minimal versioned logical IR and backend interface can preserve canonical TPCN state without device-specific leakage."
  counter_hypothesis: "H1 requires backend details or cannot preserve Model-B parameters, ordering, timing and bounded state."
  interfaces_relied_on: ["Edge", "BoundedTopology", "TPCNNeuron", "Event", "EventQueue", "ACP-0002 Model-B", "TPCV-1"]
  label_information_boundary:
    - "Labels remain outside canonical IR, event payloads, routing and backend declarations."
  timing_assumptions:
    - "Logical timestamps, positive finite delays and deterministic sequence ordering are portable."
    - "Hardware clocks, batching and backend scheduling are not neural time."
  reset_boundaries:
    - "Existing canonical reset/retention boundaries remain unchanged."
  resource_bounds:
    - "IR represents finite topology, fan-in/out, queue/state bounds and logical workload counts where in scope."
  authorized_scope:
    - "Create .github/agents/luna-18.agent.md."
    - "Implement only TPCN-IR-1 or an equivalent explicit IR version."
    - "Create minimal backend identity/capability/equivalence/policy interfaces."
    - "Create safe canonical conversion and supported reference reconstruction paths."
    - "Add focused H1 validation and return to Luna-0."
  unauthorized_scope:
    - "GPU-FPGA or GPU-FPAA approximation"
    - "Actual GPU, FPGA, FPAA or FPGA+FPAA execution"
    - "Calibration, physical voltage semantics or hardware acceptance"
    - "Attractor/event-compression neuron"
    - "Adaptive edge learning, probationary connections or structural maturation"
    - "ACP-0002 N3/later stages, Luna-13G or A01-A15 changes"
  controls:
    - "Non-default w, d, r, tau, g and lambda round-trip"
    - "Unsupported-version, invalid-bound and invalid-delay rejection"
    - "Canonical runtime trace and structural-decision invariance"
    - "TPCV-1 remains separate and downstream-only"
  measurements:
    - "IR schema/version validation"
    - "Canonical conversion and reference round-trip equality"
    - "Backend capability/equivalence/policy declaration validation"
    - "Focused tests, static validation and diff check"
  information_boundary_check:
    - "No CUDA, RTL, physical channel, DAC, PCB, calibration or device-memory details in canonical IR."
  hardware_mapping:
    - "Future backend and calibration state attach outside canonical IR."
    - "Luna-17 remains the reserved cross-backend hardware-equivalence gate."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A15"]
  preserves:
    - "A01-A15 unchanged"
    - "ACP-0002 N2 Model-B semantics and closed status"
    - "TPCV-1 limited observability purpose"
    - "Luna-13F CLOSED and Luna-13G unauthorized"
  architecture_change: false
  proposal: "ACP-0003 accepted for staged implementation; H1 authorized"
  files_changed:
    - ".github/agents/luna-18.agent.md"
    - ".github/agents/luna-0.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-18-h1-creation-authorization-Luna-0.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "H1 implementation and all production/backend/hardware tests: not run."
  assumptions:
    - "Historical Luna-15/Luna-16 hardware reservations remain preserved as historical records, not current assignments."
  unresolved:
    - "Future FPGA-native and FPAA-native roles receive new numbers when separately authorized."
  recommended_next_agent:
    - "Luna-18 for H1 implementation only; return to Luna-0 for independent review."
```

## Numbering reconciliation

**OBSERVED:** `.github/agents/luna-15.agent.md` is the active ACP-0002 N1
contract, and `.github/agents/luna-16.agent.md` is the active ACP-0002 N2
contract. `.github/agents/luna-17.agent.md` does not exist, and no Luna-17
implementation handoff was found.

**DECISION:** The older workflow reservation of Luna-15 as FPGA/VHDL and
Luna-16 as FPAA is retained as historical planning context but superseded by
the actual ACP-0002 N1/N2 assignments. Luna-17 remains:

`RESERVED / NOT AUTHORIZED / NO ACTIVE CONTRACT`

with the current intended role `hardware-equivalence / cross-backend hardware
acceptance`. Future FPGA-native and FPAA-native implementation roles receive
new numbers when authorized; Luna-17 is not created or executed here.

## H1 authorization

Luna-18 is created and authorized for H1 only. H1 covers `TPCN-IR-1` or an
equivalent explicit version, canonical state conversion/reconstruction, minimal
backend capability and equivalence declarations, sequential/coincident policy
declarations, state separation and focused tests. It does not implement any
production backend, approximation, calibration, attractor neuron or learning.

H1 has not been executed. Luna-0 must independently review its completion.
H2 is not authorized.

## Status boundary

ACP-0003: **ACCEPTED FOR STAGED IMPLEMENTATION**.

ACP-0002 N2: **CLOSED**. ACP-0002 N3: unauthorized. A01-A15: unchanged.
Luna-13F: **CLOSED**. Luna-13G: unauthorized.
