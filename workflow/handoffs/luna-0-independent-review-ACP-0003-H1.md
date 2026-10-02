# Luna-0 Independent Review Handoff: ACP-0003 H1

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent ACP-0003 H1 Execution IR/backend review"
  task_id: "luna-0-independent-review-ACP-0003-H1"
  component: "TPCN-IR-1 and backend interface skeleton"
  status: "blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "b9dfae4357c8fd23963f16b4b6525c50ecdad25c"
  result_revision: "uncommitted review handoff"
  dependencies:
    - "ACP-0003 accepted for staged implementation"
    - "ACP-0002 N2 closed"
    - "Luna-18 H1 implementation published"
  owner: "Luna-0 Architecture Guardian"
  classification: ["VERIFICATION"]
  hypothesis: "H1 establishes a hardware-neutral IR/backend boundary without loss of current canonical state or false backend claims."
  counter_hypothesis: "H1 accepts or silently drops state that makes reconstruction ambiguous, or lacks required backend contract declarations."
  interfaces_relied_on:
    - "TPCN-IR-1"
    - "ExecutionIR"
    - "IREdge"
    - "IRNeuron"
    - "IREvent"
    - "reference_from_ir"
    - "BackendCapabilities"
    - "ApproximationContract"
    - "ACP-0002 N2 Model-B"
    - "TPCV-1"
  label_information_boundary:
    - "No labels or global evaluation state were introduced into the IR."
  timing_assumptions:
    - "Logical timestamps, positive finite propagation delays and sequence identities remain canonical."
    - "Backend clocks, batches and physical coincidence windows remain outside canonical IR."
  reset_boundaries:
    - "Canonical reset behavior was not changed."
  resource_bounds:
    - "IR carries finite topology, queue and event-budget declarations; reconstruction remains the canonical topology-capacity validator."
  authorized_scope:
    - "Independently verify H1 implementation and publication provenance."
    - "Run focused IR/canonical tests, full CPU regression, compilation and diff checks."
    - "Attack parameter preservation, temporal state, event ordering, serialization, bounds, TPCV separation and backend truthfulness."
    - "Record an independent closure or blocking decision."
  unauthorized_scope:
    - "H2 or any numerical approximation"
    - "GPU, FPGA, FPAA or hybrid execution"
    - "Calibration or hardware equivalence"
    - "Attractor neurons or edge learning"
    - "ACP-0002 N3, Luna-13F reopening or Luna-13G"
    - "Repairing the H1 implementation during independent review"
  controls:
    - "Non-default Model-B edge transfer and positive delay"
    - "Non-default neuron decay, gain, state and local timestamp"
    - "Equal-time event sequence serialization"
    - "Unsupported version, malformed field, NaN and invalid-delay rejection"
    - "Canonical topology capacity enforcement during reconstruction"
    - "TPCV-1 and TPCN-IR-1 separation"
    - "Implementation/publication commit-scope audit"
  measurements:
    - "Focused canonical/H1 tests: 311 passed"
    - "Full CPU suite: 554 passed, 1 skipped"
    - "Compilation and git diff check passed"
    - "Independent attack probes found three blocking defects"
  information_boundary_check:
    - "No device-specific fields were found in the canonical IR records."
    - "No executable GPU/FPGA/FPAA backend was exposed by H1."
  hardware_mapping:
    - "Backend realization and calibration remain declarations only."
    - "No hardware acceptance or equivalence claim was made."
  architecture_invariants_touched:
    - "A01"
    - "A02"
    - "A03"
    - "A04"
    - "A07"
    - "A08"
    - "A09"
    - "A10"
    - "A11"
    - "A14"
    - "A15"
  preserves:
    - "A01-A15 contract text"
    - "ACP-0002 N2 Model-B semantics"
    - "TPCV-1 downstream-only scope"
    - "ACP-0002 N3 unauthorized"
    - "Luna-13F CLOSED"
    - "Luna-13G unauthorized"
  architecture_change: false
  proposal: "ACP-0003 accepted for staged implementation; H1 remains unclosed pending correction and re-review."
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-ACP-0003-H1.md"
  tests_added: []
  tests_passing:
    - "Focused command: python -m pytest -q tests/test_execution_ir.py tests/test_acp0002_n1.py tests/test_acp0002_n2.py tests/test_event_runtime.py tests/test_topology.py tests/test_canonical_event_neuron.py tests/test_structural_plasticity.py — 311 passed."
    - "Full command: python -m pytest -q — 554 passed, 1 skipped."
    - "python -m compileall -q tpcn tests — passed."
    - "git diff --check — passed."
    - "Model-B non-default w/d/r, multiple transfer values, temporal decay, serialization, malformed numeric rejection and reconstruction capacity probes passed."
    - "HEAD equals origin/main; worktree was clean before this handoff."
  tests_failed:
    - "Unsupported activation model was accepted by IRNeuron and reconstructed with canonical tanh, silently dropping the declared activation model."
    - "Duplicate equal-time event sequence identities were accepted, so the serialized event set can contain ambiguous deterministic ordering identity."
    - "ApproximationContract cannot represent supported IR version, numerical tolerance, timing tolerance, stochastic/statistical requirement or declared approximation boundary."
  tests_not_run:
    - "Pylance diagnostics tool — not run."
    - "GPU, FPGA, FPAA, hybrid, approximation, calibration and hardware tests — unauthorized/not applicable to H1."
    - "A direct replay comparison was not counted: an ad hoc probe was stopped after its harness incorrectly re-routed events from their original source and began an artificial cycle; no repository code was changed."
  assumptions:
    - "The independent review protocol's approximation-contract field requirements are mandatory for H1 closure."
    - "An IR accepting a non-canonical activation model must reject it or preserve/execute it explicitly; silently coercing it to tanh is not acceptable."
    - "Equal-time sequence identity must be unique within a represented execution event set when it is used for deterministic ordering."
  unresolved:
    - "Whether H1 should explicitly document configuration/initial-state scope rather than calling ExecutionIR a live snapshot; current documentation does not clearly exclude prediction, eligibility, reward and energy runtime state."
    - "Whether IR construction should validate fan-in/fan-out directly or document reconstruction as the definitive capacity boundary."
  recommended_next_agent:
    - "Luna-18 to repair the three blocking H1 defects and clarify IR scope, followed by a fresh Luna-0 independent review."
```

## Outcome and owned scope

**OBSERVED:** The repository was synchronized at `HEAD == origin/main`:

- branch: `main`
- HEAD: `b9dfae4357c8fd23963f16b4b6525c50ecdad25c`
- HEAD tree: `7687d9a32a6d5b894ea45e228e3235c1dda4822e`
- worktree: clean before this handoff
- H1 implementation: `352c323c107cfbc1d670c7cd802bf67378b2715e`
- governance publication: `b69fd923d05231e3f890b3902a8cfd391a9a46c9`
- publication/provenance: `b9dfae4357c8fd23963f16b4b6525c50ecdad25c`

The implementation commit contains the authorized H1 implementation, exports,
focused tests and Luna-18 completion handoff. The later commits contain
governance/provenance changes only; no unrelated implementation was attributed
to Luna-18.

**OBSERVED:** `TPCN-IR-1` is distinct from TPCV-1, preserves non-default
Model-B fields (`w`, `d`, `r`, delay and routing cost), preserves non-default
neuron decay/gain/state/local timestamp, rejects unsupported versions and
malformed finite numeric values, and reconstructs topology capacity failures
instead of bypassing them.

**BLOCKED:** H1 cannot be independently closed because the following defects
are reproducible:

1. **Activation semantics are silently lossy.** `IRNeuron` accepts any
   non-empty `activation_model` ([execution_ir.py](../../tpcn/execution_ir.py#L95-L118)),
   while `reference_from_ir` always reconstructs the fixed `tanh` neuron
   ([execution_ir.py](../../tpcn/execution_ir.py#L277-L287)). A non-`tanh`
   declared model is therefore accepted and discarded rather than rejected or
   preserved.
2. **Equal-time ordering identity is not unique.** `IREvent` validates the
   range of `sequence` but `ExecutionIR` does not reject duplicate sequence
   values ([execution_ir.py](../../tpcn/execution_ir.py#L126-L186)). Two
   equal-time events can therefore claim the same tie identity, making
   deterministic reconstruction ambiguous.
3. **The approximation contract is incomplete.** `ApproximationContract`
   contains only backend, equivalence levels, equal-time policy and notes
   ([backend.py](../../tpcn/backend.py#L51-L56)). It cannot carry the H1 review
   protocol's required IR version, numerical tolerance, timing tolerance,
   stochastic/statistical requirement or declared approximation boundary.

**INFERRED:** The current `ExecutionIR` docstring calls the value a snapshot
([execution_ir.py](../../tpcn/execution_ir.py#L146-L147)), while the represented
state excludes prediction, eligibility, reward-idempotency, energy and
processed-event runtime fields. The handoff describes portable logical state
but does not explicitly say that this is configuration/initial-state transfer,
not a full live-runtime checkpoint. This scope must be made explicit before
claiming migration/replay semantics.

## Architecture evidence

The defects do not change A01-A15, ACP-0002 N2 or TPCV-1. They block the H1
interface/representation gate. No H2, backend implementation, approximation,
calibration, hardware equivalence, attractor, edge-learning, N3, Luna-13F or
Luna-13G work is authorized by this result.

The backend declarations do not instantiate CPU fallbacks for GPU/FPGA/FPAA
identities; the default `implemented` value remains false. No device-specific
fields were found in canonical IR records, and no fabricated physical resource
claims were made.

## Validation record

| Command or procedure | Revision / environment | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_execution_ir.py tests/test_acp0002_n1.py tests/test_acp0002_n2.py tests/test_event_runtime.py tests/test_topology.py tests/test_canonical_event_neuron.py tests/test_structural_plasticity.py` | `b9dfae4`, Python 3.11.5 | PASS — 311 passed | local run |
| `python -m pytest -q` | `b9dfae4`, Python 3.11.5 | PASS — 554 passed, 1 skipped | local run |
| `python -m compileall -q tpcn tests` | `b9dfae4`, Python 3.11.5 | PASS | local run |
| `git diff --check` | `b9dfae4` | PASS | local run |
| Non-default Model-B round trip and transfer attack | `b9dfae4` | PASS for `a` in `{-1,-0.25,0,0.4,1}` | independent probe |
| Temporal-state decay attack | `b9dfae4` | PASS for nonzero state and local timestamp | independent probe |
| Equal-time serialization attack | `b9dfae4` | Distinct sequence values survive; duplicate values incorrectly accepted | independent probe |
| Unsupported activation-model attack | `b9dfae4` | FAIL — accepted then reconstructed as `tanh` | independent probe |
| Approximation-contract shape attack | `b9dfae4` | FAIL — five required declaration dimensions absent | independent probe |
| GPU/FPGA/FPAA/hardware validation | H1 scope | Not run; unauthorized/not applicable | scope boundary |

## Benchmark and resource results

No streaming classification benchmark was required for this H1
representation review. No physical energy, GPU FLOP, FPGA utilization,
analog-power or hardware-equivalence claim was made. Logical finite topology
and queue bounds remain represented separately from backend resource estimates.

## Assumptions, limitations and unresolved issues

The review is blocked, not a rejection of ACP-0003. The minimal repair should
remain within H1: reject unsupported activation models or version their
extension, enforce unique deterministic event identities, extend the backend
approximation contract with explicit optional/unknown declaration fields, and
document the IR's exact configuration/live-state scope. No approximation or
hardware work is needed or authorized to resolve these findings.

## Reproduction and rollback

Start from `b9dfae4357c8fd23963f16b4b6525c50ecdad25c` and run the commands in
the validation table. The published H1 implementation remains the rollback
point; this review adds only the present handoff and does not modify the
implementation.

## Next assignment

Assign Luna-18 a bounded H1 correction task for the three listed defects and
scope clarification. After its focused tests and handoff are published, Luna-0
must repeat the independent attacks and either close H1 with the exact closure
phrase or record any remaining blocker. H2 remains unauthorized.
