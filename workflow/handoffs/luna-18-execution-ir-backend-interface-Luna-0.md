# Luna-18 H1 Dispatch: Execution IR and Backend Interface Skeleton

```yaml
tpcn_handoff:
  agent: Luna-18
  luna_identifier: "Luna-18"
  descriptive_name: "H1 Execution IR and backend interface skeleton"
  task_id: "luna-18-h1-execution-ir-backend-interface"
  component: "Hardware-neutral logical IR and backend contract interfaces"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "663d45ec408dfa1251559f5ca912fd84abff3b99"
  result_revision: "uncommitted"
  dependencies:
    - "ACP-0003 accepted for staged implementation"
    - "ACP-0002 N2 closed"
  owner: "Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION"]
  hypothesis: "A minimal logical IR and backend interface can represent current canonical TPCN state without device-specific leakage."
  counter_hypothesis: "The minimal IR requires device details or cannot preserve current event, edge, neuron, timing and bound semantics."
  interfaces_relied_on: ["Edge", "TPCNNeuron", "Event", "EventQueue", "ACP-0002 Model-B"]
  label_information_boundary:
    - "Labels remain outside IR state, event payloads, routing and backend translation."
  timing_assumptions:
    - "Logical event timestamps and positive finite delays are represented explicitly."
    - "Backend clocks and batches are not neural time."
  reset_boundaries:
    - "IR must represent existing logical reset/retention boundaries without inventing new reset behavior."
  resource_bounds:
    - "Finite topology, fan-in/out, queue, state and event-budget fields remain explicit."
  authorized_scope:
    - "Canonical IR data contracts for current Edge, Neuron and Event state."
    - "Versioned translation boundary between canonical logical state and backend adapters."
    - "Backend interface declarations for reference, deterministic approximation and dynamical approximation modes."
    - "Round-trip and validation tests for logical state only."
  unauthorized_scope:
    - "GPU kernels, CUDA optimization or production backend execution"
    - "FPGA RTL/VHDL, DE1-SoC mapping or synthesis"
    - "FPAA circuit implementation, calibration or physical measurements"
    - "Numerical approximation modes"
    - "Attractor/event-compression neuron"
    - "Edge learning, ACP-0002 N3/later stages, structural maturation"
    - "Luna-13F reopening or Luna-13G authorization"
  controls:
    - "Canonical ACP-0002 N2 Model-B analytic values"
    - "IR round-trip equality for portable logical fields"
    - "Reject unknown versions, missing bounds, invalid delays and device fields"
    - "Verify serialization/translation does not alter event ordering metadata"
  measurements:
    - "Schema validation result"
    - "Round-trip logical-state equality"
    - "Rejected malformed/overflow cases"
    - "No backend numerical or hardware equivalence claim"
  information_boundary_check:
    - "IR contains no CUDA dimensions, RTL names, register addresses, physical channels, DAC assignments or PCB routes."
  hardware_mapping:
    - "Adapters may attach backend realization and calibration state outside canonical IR."
    - "Coincidence-window calibration is explicitly out of scope for H1."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A15"]
  preserves:
    - "A01-A15"
    - "ACP-0002 N2 Model-B semantics"
    - "TPCV-1 downstream-only boundary"
  architecture_change: false
  proposal: "ACP-0003 accepted for staged implementation"
  files_changed:
    - "tpcn/execution_ir.py"
    - "tpcn/backend.py"
    - "tpcn/__init__.py"
    - "tests/test_execution_ir.py"
  tests_added:
    - "tests/test_execution_ir.py"
  tests_passing:
    - "python -m pytest -q tests/test_execution_ir.py tests/test_acp0002_n1.py tests/test_acp0002_n2.py tests/test_event_runtime.py (277 passed)"
  tests_failed: []
  tests_not_run:
    - "All GPU, FPGA, FPAA, hybrid, approximation, calibration and hardware tests until later stages."
  assumptions:
    - "Canonical event payloads represented in the IR are JSON-serializable; unsupported payload objects are rejected explicitly."
  unresolved:
    - "Backend-specific quantizers, analog equations, calibration and coincidence tolerances remain later assignments."
  recommended_next_agent:
    - "Luna-0 for independent H1 review; H2 and all backend implementation remain unauthorized."
```

## Outcome

**OBSERVED:** `TPCN-IR-1` now validates and deterministically serializes bounded
edge, neuron, event and execution configuration records. Conversion preserves
non-default `w`, `d`, `r`, positive delay, gain, decay, state, local timestamp,
routing cost, event sequence and structural-grown edge state.

**OBSERVED:** `reference_from_ir` reconstructs the existing `Edge`,
`BoundedTopology`, `TPCNNeuron` and `Event` reference objects without changing
canonical execution code. TPCV-1 is not imported or embedded.

**INFERRED:** `BackendCapabilities`, `ApproximationContract`,
`BackendMappingResult`, `BackendDiagnostic`, `BackendRealizationState` and
`CalibrationState` provide the H1 boundary for all five named future backend
identities, E0-E4 declarations and sequential/coincident equal-time policies.
No physical coincidence-window value is represented.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Focused pytest selection | Python 3.11.5, repository working tree | PASS — 277 tests | terminal run |
| Static diagnostics | current working tree | PASS — no problems in touched Python files | Problems tool |
| `git diff --check` | current working tree | PASS | terminal run |
| GPU/FPGA/FPAA execution, approximation, calibration and hardware tests | N/A | not run; unauthorized/not applicable | scope boundary |
| Full production regression | N/A | not run; H1-focused validation only | scope boundary |

## Preserved and unresolved

- A01-A15, ACP-0002 N2 Model-B transfer, event timing/order, neuron decay,
  prediction/error, reward/idempotency, structural decisions and TPCV-1
  downstream-only semantics were not changed.
- A01-A15 remain unchanged; ACP-0002 N3, Luna-13F reopening and Luna-13G remain
  unauthorized.
- No commit was created, so the result revision is uncommitted.

## Dispatch boundary

Luna-18 is authorized to implement only H1, the canonical IR and backend
interface skeleton. It must return to Luna-0 before any numerical approximation,
GPU execution adapter, FPGA/FPAA implementation, attractor-neuron work or
hardware mapping begins. This dispatch does not authorize production backends.
