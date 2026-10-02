# Luna-0 Architecture Update Handoff: ACP-0003

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Heterogeneous execution and backend separation architecture update"
  task_id: "luna-0-architecture-update-acp-0003"
  component: "Canonical execution semantics, TPCN Execution IR boundary and GPU/FPGA/FPAA backend governance"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "434a000029ebf52d87d15ece6d3681eafdfd23f1"
  result_revision: "uncommitted architecture documentation"
  dependencies:
    - "ACP-0002 N2 closed"
    - "ACP-0002 Model-B edge and canonical neuron semantics"
    - "A01-A15 contract version 1.1"
  owner: "Project owner; Luna-0 Architecture Guardian"
  classification: ["OBSERVATION", "ARCHITECTURE-PROMOTION"]
  hypothesis: "A canonical logical IR and explicit backend contracts can support GPU, FPGA and FPAA realizations without promoting device details into TPCN semantics."
  counter_hypothesis: "The proposed IR cannot represent timing, bounds, equal-time fan-in, state portability or approximation errors without device-specific leakage."
  interfaces_relied_on: ["Event", "EventQueue", "LocalTimestamp", "PropagationDelay", "Edge", "TPCNNeuron", "ACP-0002 Model-B", "TPCV-1"]
  label_information_boundary:
    - "Labels remain outside canonical events, routing, prediction/error computation and backend approximation state."
  timing_assumptions:
    - "Logical event time, backend scheduling time and wall-clock time remain distinct."
    - "No GPU/FPGA hardware clock becomes a global neural timestep."
    - "FPAA continuous time must declare a mapping to logical timestamps and finite delays."
  reset_boundaries:
    - "Existing canonical reset boundaries remain authoritative; backend realization state requires explicit import/reset policy."
  resource_bounds:
    - "Finite nodes, edges, fan-in/out, queues, state, event budgets and backend buffers."
    - "Logical resource proxies remain distinct from FPGA/FPAA physical cost."
  authorized_scope:
    - "Create and review ACP-0003 documentation."
    - "Define the conceptual IR boundary, capability matrix, approximation classes and staged dependency order."
    - "Update workflow/changelog/handoff governance records."
  unauthorized_scope:
    - "Production GPU, FPGA or FPAA backends"
    - "CUDA/RTL/FPAA implementation or calibration"
    - "Edge learning or ACP-0002 N3/later stages"
    - "Attractor/event-compression neuron implementation"
    - "Luna-13F reopening or Luna-13G authorization"
    - "A01-A15 contract amendment or hardware-equivalence claim"
  controls:
    - "ACP-0002 N2 canonical equations and equal-time sequential fan-in"
    - "GPU batching versus logical event ordering"
    - "Fixed-point and analog approximation error classes"
    - "Serialization/state portability versus backend realization state"
    - "Equal-time FPAA simultaneous integration as an explicit open issue"
  measurements:
    - "Repository governance and baseline revision inspected"
    - "No production execution or hardware validation performed"
  information_boundary_check:
    - "IR excludes CUDA, RTL, physical channel and PCB details."
    - "Instrumentation and visualization remain downstream-only."
  hardware_mapping:
    - "GPU native is the high-precision reference."
    - "GPU FPGA and GPU FPAA are approximation/emulation modes, not hardware."
    - "FPGA and FPAA native responsibilities are separated but not yet accepted as a physical partition."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A12", "A13", "A14", "A15"]
  preserves:
    - "A01-A15 text and meaning"
    - "ACP-0002 N2 closed status and Model-B semantics"
    - "TPCV-1 limited downstream-only purpose"
    - "Luna-13F closed and Luna-13G unauthorized"
  architecture_change: true
  proposal: "ACP-0003 Under review; owner acceptance required"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/README.md"
    - "workflow/handoffs/luna-0-architecture-update-ACP-0003.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All production backend, IR, GPU, FPGA, FPAA, hybrid and hardware-equivalence tests: not run; no implementation authorized."
  assumptions:
    - "The project-owner request starts ACP review but is not an explicit acceptance decision."
    - "The local repository's workflow directory is the equivalent of the requested tpcn-luna-workflow path."
  unresolved:
    - "IR schema/versioning, quantizers, analog model/calibration, equal-time analog mapping, hybrid partition and backend tolerances require later decisions."
  recommended_next_agent:
    - "Luna-0/project owner: decide ACP-0003 status."
    - "After acceptance only: bounded IR/interface implementation assignment."
```

## Outcome and owned scope

**OBSERVED:** ACP-0003 was created as the next unused proposal identifier and
is `UNDER REVIEW`. The proposal separates canonical TPCN semantics from device
approximation contracts and device mappings for GPU native, GPU FPGA
approximation, FPGA native, GPU FPAA approximation, FPAA native and a possible
FPGA+FPAA hybrid.

**INFERRED:** The canonical boundary can remain hardware-neutral if logical
state, event identity, local time, finite delays and bounds are portable while
quantization, calibration, clocks, physical channels and layout remain mapping
state.

**HYPOTHESIZED:** Staged equivalence tests can identify architecture,
approximation, backend implementation and calibration failures separately.
No result is measured yet.

## Decision summary

- ACP identifier: ACP-0003.
- Status: `ACP-0003 UNDER REVIEW`.
- Central rule: canonical TPCN semantics -> device approximation contract -> device implementation.
- IR boundary: portable logical topology, Model-B parameters, bounded neuron state and event records; no CUDA, RTL, physical channel or PCB details.
- GPU native: high-precision reference and research implementation.
- GPU FPGA approximation: declared fixed-point/resource-constrained FPGA emulation.
- FPGA: eventual finite event/control and arithmetic implementation; DE1-SoC details remain noncanonical.
- GPU FPAA approximation: declared continuous/noisy dynamical emulation, not reduced precision alone.
- FPAA: eventual physical dynamical realization with calibration and interface limits declared.
- FPGA+FPAA: hardware research hypothesis, not an approved mapping.
- Equal-time fan-in: canonical sequential semantics remain; simultaneous FPAA summation is not exact by default and requires serialization or explicit approximation tolerance.
- State portability: one canonical logical state plus separate backend realization/calibration state.
- Calibration: permitted as a mapping layer that cannot redefine logical parameters.
- Equivalence hierarchy: analytic -> GPU native -> GPU FPGA -> FPGA; analytic/reference -> GPU FPAA -> physical FPAA; hybrid separately.
- Accounting: logical event/activity proxies remain separate from hardware resource and measured-power estimates.
- Attractor neuron: IR-compatible future extension only; no implementation authorized.
- A01-A15: reviewed and preserved; no contract text change.
- ACP-0002: N2 closed and authoritative; N3 and later stages unauthorized.
- Luna-13F: closed. Luna-13G: unauthorized.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Read authoritative contract, workflow, acceptance criteria, proposal template, ACP-0002 and N2 review | `main` at `434a000029ebf52d87d15ece6d3681eafdfd23f1` | passed | repository documents |
| Inspect branch and worktree | same | `main`, clean before edits | repository state inspection |
| Production backend/hardware equivalence tests | not run; no implementation authorized | not run | out of scope |

## Integration readiness

Not ready for implementation. ACP-0003 requires project-owner acceptance and
later concrete decisions for IR versioning, fixed-point policies, analog
models/calibration, equal-time analog behavior and equivalence tolerances.

## Next assignment

Project owner/Luna-0 must decide whether to accept ACP-0003 for staged
implementation. If accepted, the next bounded assignment is an IR/backend
interface foundation only, with no production hardware backend, edge learning,
ACP-0002 N3, Luna-13F reopening or Luna-13G authorization.
