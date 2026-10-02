---
name: Luna-18 ACP-0003 H1 Execution IR and Backend Interface Skeleton
description: Implement only the hardware-neutral Execution IR and minimal backend interface skeleton authorized by ACP-0003 H1.
---

# Luna-18 - ACP-0003 H1 Execution IR and Backend Interface Skeleton

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/ACP-0003.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`,
`.github/agents/luna-0.agent.md`, and this contract before editing. Record the
exact starting revision, branch and worktree state. Preserve unrelated changes.
ACP-0003 is **Accepted for staged implementation**; this contract authorizes
only H1.

## Authorization and ownership

Own only the versioned hardware-neutral Execution IR, its minimal backend
contract/interface declarations, safe canonical conversion/reconstruction
helpers, focused H1 tests and the Luna-18 completion handoff. Confirm exact
file ownership with Luna-0 before editing if an existing module boundary is
unclear.

The IR must be independent from TPCV-1. TPCV-1 remains a downstream
observability format with its existing limited purpose.

## Required H1 representation

Use an explicit independent IR version such as `TPCN-IR-1`. The canonical
logical representation must support, within its declared scope:

- Edge: source, destination, edge weight `w`, divider strength `d`, reference
  `r`, positive logical propagation delay `tau`, and required canonical routing
  metadata.
- Neuron: identifier, decay rate `lambda`, bounded state/configuration,
  neuron gain `g`, and activation semantics.
- Event: source, destination, logical timestamp, payload, canonical event type,
  and identity/sequence information where existing ordering requires it.
- Network/execution configuration: enough bounded information to validate,
  map or reproduce the represented IR scope.

Preserve non-default `w`, `d`, `r`, `tau`, `g` and `lambda`. Do not drop Model-B
state during conversion or reconstruction. The smallest safe conversion path
from current canonical TPCN structures is required; an IR-to-reference adapter
or reconstruction path is required where safe within H1.

The IR must not contain CUDA dimensions, FPGA register addresses or RTL names,
FPAA channel identifiers, physical voltage assignments, DAC settings, PCB
routes, calibration coefficients or backend memory placement.

## Backend interface boundary

Create only minimal declarations for backend identity, capabilities,
approximation contract, canonical IR compatibility, applicable equivalence
levels, mapping/initialization results and diagnostics. The interface must be
able to name these future identities without falsely claiming implementation:
GPU native, GPU-FPGA approximation, FPGA native, GPU-FPAA approximation and
FPAA native.

Represent ACP-0003 equivalence levels without requiring one level for every
backend:

- E0 semantic;
- E1 numerical;
- E2 event;
- E3 functional;
- E4 statistical.

Represent equal-time policies at the contract boundary, including
`SEQUENTIAL_DETERMINISTIC` for canonical execution and
`COINCIDENT_WINDOW` for a future FPAA-like approximation. Do not assign a
physical coincidence-window value. That value belongs to backend/calibration
state, never canonical IR.

Keep these states separate:

- canonical logical state: portable network semantics;
- backend realization state: formats, memory/layout and scheduling;
- calibration state: physical conversion, leakage, mismatch, offsets and
  coincidence-window characterization.

Calibration and realization state must not redefine canonical parameters.

## Required invariants and tests

H1 is representation/interface work and must not change canonical execution.
Preserve Model-B transfer, event timing, deterministic ordering, neuron state
evolution, prediction/error semantics, reward/idempotency semantics and
structural decisions.

Add focused tests for:

- IR versioning and validation of edge, neuron and event records;
- non-default Model-B parameter, delay, gain and decay preservation;
- canonical-to-IR conversion and supported IR/reference round trip;
- unsupported-version rejection where parsing exists;
- backend capabilities and equivalence declarations;
- sequential and coincident-window policy declarations without a physical value;
- canonical/backend/calibration state separation;
- structural-grown edge conversion;
- TPCV/IR separation;
- runtime-semantic invariance.

Preserve finite bounds, positive finite delays, deterministic serialization and
bounded state. Failure-category names from ACP-0003 are for architecture,
approximation, backend implementation, calibration and hardware-limit reports;
do not replace ordinary software exceptions with them.

## Explicit prohibitions

Luna-18 MUST NOT implement or authorize:

- GPU-FPGA numerical approximation or actual GPU backend execution;
- actual FPGA/RTL/VHDL execution or DE1-SoC mapping;
- GPU-FPAA simulation or actual FPAA execution;
- FPGA+FPAA production mapping;
- calibration procedures or physical voltage semantics;
- leaky attractor/event-compression neuron behavior;
- adaptive learning of `w`, `d` or `r`, probationary edges or structural maturation;
- ACP-0002 N3 or later stages;
- Luna-13G;
- changes to A01-A15.

Do not execute a broad production regression campaign merely because this
contract lists future checks. Run focused H1 tests, relevant existing tests and
static validation, and mark all other checks not run.

## Completion and handoff gate

The completion handoff must report starting and result revisions, exact files,
IR version/schema, conversion and round-trip evidence, all preserved non-default
parameters, interface capability/equivalence declarations, equal-time policy
representation, state separation, focused tests, unchanged runtime semantics,
A01-A15, ACP-0003, ACP-0002 N3, Luna-13F and Luna-13G status.

A successful implementation may report:

`PASS — ACP-0003 H1 EXECUTION IR/BACKEND INTERFACE IMPLEMENTED`

but Luna-18 does not independently close H1 or authorize H2. Return to Luna-0
for independent review. H1 completion does not authorize numerical
approximation, production backends, attractor-neuron work, edge learning or
hardware equivalence.
