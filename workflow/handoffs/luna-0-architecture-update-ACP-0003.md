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
  result_revision: "uncommitted ACP-0003 staged-implementation decision"
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
    - "Model C: strict serialized validation mode plus Model B coincident analog approximation"
  measurements:
    - "Repository governance and baseline revision inspected"
    - "No production execution or hardware validation performed"
  information_boundary_check:
    - "IR excludes CUDA, RTL, physical channel and PCB details."
    - "Instrumentation and visualization remain downstream-only."
  hardware_mapping:
    - "GPU native is the high-precision reference."
    - "GPU FPGA and GPU FPAA are approximation/emulation modes, not hardware."
    - "FPGA and FPAA native responsibilities remain a research mapping; no final physical partition is accepted."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A12", "A13", "A14", "A15"]
  preserves:
    - "A01-A15 text and meaning"
    - "ACP-0002 N2 closed status and Model-B semantics"
    - "TPCV-1 limited downstream-only purpose"
    - "Luna-13F closed and Luna-13G unauthorized"
  architecture_change: true
  proposal: "ACP-0003 accepted for staged implementation; H1 only"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/README.md"
    - "workflow/handoffs/luna-0-architecture-update-ACP-0003.md"
    - "workflow/handoffs/luna-18-execution-ir-backend-interface-Luna-0.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All production backend, IR, GPU, FPGA, FPAA, hybrid and hardware-equivalence tests: not run; no implementation authorized."
  assumptions:
    - "The project-owner request starts ACP review but is not an explicit acceptance decision."
    - "The local repository's workflow directory is the equivalent of the requested tpcn-luna-workflow path."
  unresolved:
    - "IR schema details, quantizers, analog model/calibration, hybrid partition and backend tolerances remain later implementation decisions."
  recommended_next_agent:
    - "Luna-18: H1 Execution IR/backend interface skeleton only; return to Luna-0."
    - "Later: GPU approximation and physical backend assignments after H1 evidence."
```

## Outcome and owned scope

**OBSERVED:** ACP-0003 was created as the next unused proposal identifier and
is accepted for staged implementation. The proposal separates canonical TPCN semantics from device
approximation contracts and device mappings for GPU native, GPU FPGA
approximation, FPGA native, GPU FPAA approximation, FPAA native and a possible
FPGA+FPAA hybrid.

**INFERRED:** The canonical boundary can remain hardware-neutral if logical
state, event identity, local time, finite delays and bounds are portable while
quantization, calibration, clocks, physical channels and layout remain mapping
state.

**INFERRED:** Model C resolves the equal-time fan-in governance issue without
changing canonical N2 semantics: strict serialization is the validation mode,
while coincident analog integration is an explicit backend approximation.

**HYPOTHESIZED:** Staged equivalence tests can identify architecture,
approximation, backend implementation, calibration and hardware-limit failures
separately. No implementation result is measured yet.

## Decision summary

- ACP identifier: ACP-0003.
- Status: `ACP-0003 ACCEPTED FOR STAGED IMPLEMENTATION`.
- Central rule: canonical TPCN semantics -> device approximation contract -> device implementation.
- IR boundary: portable logical topology, Model-B parameters, bounded neuron state and event records; no CUDA, RTL, physical channel or PCB details.
- GPU native: high-precision reference and research implementation.
- GPU FPGA approximation: declared fixed-point/resource-constrained FPGA emulation.
- FPGA: eventual finite event/control and arithmetic implementation; DE1-SoC details remain noncanonical.
- GPU FPAA approximation: declared continuous/noisy dynamical emulation, not reduced precision alone.
- FPAA: eventual physical dynamical realization with calibration and interface limits declared.
- FPGA+FPAA: hardware research hypothesis, not an approved mapping.
- Equal-time FPAA model: Model C through Model B semantics; strict serialization is required for validation, while coincident analog fan-in is an explicit approximation.
- Strict serialization: validation/reference mode, not a permanent physical requirement.
- Coincidence window: backend contract/calibration state, never canonical network state.
- Equivalence: E0 semantic, E1 numeric, E2 event, E3 functional, E4 statistical; requirements vary by backend and mode.
- State portability: one canonical logical state plus separate backend realization/calibration state.
- Calibration: permitted as a mapping layer that cannot redefine logical parameters.
- Equivalence hierarchy: analytic -> GPU native -> GPU FPGA -> FPGA; analytic/reference -> GPU FPAA -> physical FPAA; hybrid separately.
- Accounting: logical event/activity proxies remain separate from hardware resource and measured-power estimates.
- Attractor neuron: future extension only; cheap per-arrival decay/accumulation/test and expensive transition work are recorded, but implementation requires a future neuron ACP.
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

ACP-0003 is ready for the bounded H1 implementation only. Production backend,
approximation, analog calibration and attractor-neuron work remain blocked on
later evidence and contracts.

## Next assignment

Luna-18 is authorized for the H1 Execution IR/backend interface skeleton. It
must return to Luna-0 with schema, round-trip, bounds and malformed-input
evidence before any GPU-FPGA, GPU-FPAA, FPGA, FPAA, hybrid or attractor work.
