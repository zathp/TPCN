# Luna-21 Completion Handoff — ACP-0004 E2 Multi-Excursion Runtime

```yaml
tpcn_handoff:
  agent: Luna-21
  luna_identifier: "Luna-21"
  descriptive_name: "ACP-0004 E2 multi-excursion runtime"
  task_id: "luna-21-e2-multi-excursion-20261003"
  component: "hardware-neutral E2 runtime and IR-2 E2 adapters"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "0d26c3d6bd253ce3be1a3877ec5f2fcb0cf62868"
  result_revision: "bfc866be053f9692382d1be5e048f5b4d280e5f6"
  dependencies:
    - "Luna-0 ACP-0004 E2 authorization at the base revision"
    - "ACP-0004 E1 independently closed"
    - "ACP-0005 / TPCN-IR-2 revision 1 independently closed"
    - "ACP-0002 N2 Model-B transfer"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "The authorized E2 state machine can be implemented as a bounded event-driven extension without changing closed E1 or IR-2 schema revision 1."
  counter_hypothesis: "E2 requires a global timestep, unbounded work, E1 behavior changes, or an IR-2 schema revision."
  interfaces_relied_on:
    - "SingleExcursionNeuron and EventQueue"
    - "BoundedTopology Model-B routing"
    - "IR2Neuron / TPCNIR2 schema revision 1"
    - "neuron_from_ir2 E1-only capability boundary"
  label_information_boundary:
    - "E2 receives no labels, evaluation state, learning, reward, or global orchestration state."
  timing_assumptions:
    - "Local analytic decay; positive finite M emit, M re-arm, and ordinary delays."
    - "Destination-local external-before-internal ordering remains owned by EventQueue."
    - "No global neural timestep."
  reset_boundaries:
    - "Reset clears E2 state, pending validity, active provenance, and character-local output while preserving bounded identity high-water marks."
  resource_bounds:
    - "Bounded accumulator, provenance ring, one valid pending internal event, monotonic counters, generation token, and event budget."
  authorized_scope:
    - "E2 M_ACTIVE ARMED/REFRACTORY execution and M_EMIT/M_REARM."
    - "E2-to/from validated TPCN-IR-2 revision 1 objects."
    - "Focused E2 tests and completion evidence."
  unauthorized_scope:
    - "H2, N3, learning/reward redesign, backend or hardware work, approximation, calibration, hardware equivalence, IR-3, and A01-A15 amendments."
  controls:
    - "Existing E1 behavior and reset semantics."
    - "Historical neuron_from_ir2 remains E1-only."
    - "TPCN-IR-2 schema_revision remains 1."
    - "ACP-0002 N2 Model-B edge transfer remains unchanged."
  measurements:
    - "Deterministic event counts, output identities, finite-return bounds, reset continuity, provenance lifecycle, and regression/test totals."
    - "No classification, learning, energy-benefit, backend, or hardware measurements."
  information_boundary_check:
    - "E2 decisions use only local state, local time, current external contribution, and bounded causal provenance."
  hardware_mapping:
    - "None; logical excursions remain backend-neutral and no hardware equivalence is claimed."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A11", "A15"]
  preserves:
    - "A01-A15"
    - "Independently closed ACP-0004 E1 behavior"
    - "Independently closed ACP-0005 TPCN-IR-2 schema revision 1"
    - "ACP-0002 N2 Model-B semantics"
  architecture_change: false
  proposal: "ACP-0004"
  files_changed:
    - "tpcn/excursion_neuron.py"
    - "tpcn/ir2.py"
    - "tpcn/__init__.py"
    - "tests/test_e2_multi_excursion.py"
    - "tests/test_e2_ir2.py"
    - "tests/test_ir2.py"
    - "workflow/handoffs/luna-21-e2-multi-excursion-20261003.md"
  tests_added:
    - "tests/test_e2_multi_excursion.py"
    - "tests/test_e2_ir2.py"
    - "Two IR-2 malformed-state/future-pending fixtures in tests/test_ir2.py"
  tests_passing:
    - "Focused E2 runtime and E2 IR-2: 44 passed."
    - "E1 and IR-2 regression suites: 41 passed."
    - "Model-B and event-runtime regressions: 254 passed."
    - "Topology regression suite: 9 passed."
    - "Full CPU suite: 668 passed, 1 skipped, 0 failed."
    - "compileall, targeted py_compile, and git diff --check passed."
  tests_failed: []
  tests_not_run:
    - "GPU/FPGA/FPAA backends, ModelSim, hardware equivalence, calibration, H2, N3, and learning/benchmark evaluations; these are unauthorized or outside Luna-21 scope."
  assumptions:
    - "When reconstructing a valid E1-only IR-2 record through the E2 capability, missing optional M settings use the validated E2 defaults; E2-produced records preserve their explicit configured values."
    - "Identity high-water counters are capped by the declared event budget; exhaustion is explicit and does not wrap or reuse an identity."
  unresolved: []
  recommended_next_agent:
    - "Luna-0: independently review the actual Luna-21 implementation and completion evidence."
```

## Outcome and scope

**OBSERVED:** Added `MultiExcursionNeuron` as an additive E2 runtime using
the existing local-time accumulator, event queue, bounded provenance ring,
and Model-B excursion payload. The historical E1-only runtime retains its
single-excursion behavior and out-of-scope M boundary. M admission is
inclusive at `theta_M` and is supported from `N`, `S_PENDING`, and
`S_RETURN`.

**OBSERVED:** M admission allocates `multi_episode_id` from the shared
episode counter and preserves or establishes the causal lineage. `ARMED`
owns one `M_EMIT`; `REFRACTORY` owns one `M_REARM`. M output uses the sign at
the emission transition and exactly `A_max`, applies the bounded
no-crossing discharge, and produces a distinct output-event identity.
Final residual S receives a distinct shared-counter ordinary ID with the
same lineage; direct M-to-N allocates no ordinary episode.

**OBSERVED:** External arrivals cancel the current valid pending generation,
decay and clip state, record provenance, and either leave M through the
canonical residual transition or replace the appropriate phase event.
Queue-driven tests establish external-before-M-internal ordering at equal
timestamps. Stale, canceled, duplicate, wrong-generation, wrong-episode,
wrong-kind, wrong-timestamp, wrong-sequence, and wrong-source internal
deliveries do not mutate neuron state or create outputs.

**OBSERVED:** The active provenance ring is re-owned at M admission and
M-to-final-S transitions without changing retained event IDs, timestamps,
signed contributions, order, or lineage. Truncation remains sticky across
the final-S transition; already-emitted M records retain their M identity.
Direct M-to-N closes and clears the M-owned active provenance.

**OBSERVED:** Reset from both M phases clears state, phase, valid pending
work, provenance, and character-local emissions. Output, shared episode,
lineage, and automatic input IDs remain monotonic across reset. Lifetime
identity allocation is bounded by `event_budget`; budget exhaustion is
explicit. A configured positive delay that cannot advance representable
local time is rejected rather than creating a zero-time transition.

**OBSERVED:** `neuron_to_ir2_e2` / `neuron_from_ir2_e2` use the shared
validated `IR2Neuron` / `TPCNIR2` revision-1 objects. Round trips restore
`ARMED` with the original pending `M_EMIT`, `REFRACTORY` with the original
pending `M_REARM`, and continuation after a prior M output without
duplicate scheduling. The historical `neuron_from_ir2` continues to raise
`IR2UnsupportedRuntimeError` for `M_ACTIVE`.

**INFERRED:** The exercised state machine satisfies the authorized bounded,
deterministic, causal E2 contract under the listed test configurations.
This is software-reference evidence only; it is not architecture promotion,
hardware equivalence, or learning evidence.

## Architecture evidence

| Clause | Evidence |
|---|---|
| A01-A02 | Local event-triggered analytic decay; no global timestep; positive-delay checks. |
| A03-A04 | Existing finite-delay event queue and bounded Model-B topology are unchanged; E2 fan-out uses the existing route. |
| A08 | One valid pending event, finite return, generation/identity bounds, and explicit event-budget exhaustion. |
| A11 | Bounded provenance preserves causal ownership and truncation; no learning or reward behavior is added. |
| A15 | Runtime and IR-2 remain hardware-neutral; no backend validation is claimed. |

A05 remains reservoir-free, A12-A13 remain optional, A14 is not activated,
and A01-A15 contract text is unchanged.

## Required fixture evidence

- Exact `theta_M` enters M; `nextafter(theta_M, 0)` remains ordinary.
- Positive and negative `theta_M`, intermediate `±6`, and maximum `±X_max`
  return within `ceil((q_0 - theta_hold) / Delta_x_E)`.
- Multiple M excursions have unique output IDs and strictly increasing
  timestamps; threshold fixtures cover `theta_E`, `theta_hold`, and
  `theta_M` boundaries.
- Promotion from `N`, `S_PENDING`, and `S_RETURN`; final-S identity and
  lineage continuity; direct M-to-N without an empty ordinary ID.
- Provenance exact-capacity and overflow boundaries, truncation stickiness,
  re-ownership, ordering, and immutable already-emitted M records.
- Reset in `ARMED` and `REFRACTORY`, stale M-event no-ops, and output,
  episode, lineage, and automatic-input identity continuity.
- External magnitude reduction and sign reversal in both M phases; equal-time
  external-before-`M_EMIT` and external-before-`M_REARM`.
- Invalid stale tuple variants, duplicate delivery, no zero-time burst,
  finite positive-delay checks, and smallest terminating tested
  event-budget sequence.
- Non-default Model-B fan-out and E2 IR-2 `ARMED`, `REFRACTORY`, and
  post-emission continuation round trips.

The named fixtures are in `tests/test_e2_multi_excursion.py`,
`tests/test_e2_ir2.py`, and the added malformed-state tests in
`tests/test_ir2.py`.

## Validation record

All commands ran from the repository root with Python 3.11.5.

| Command | Result |
|---|---|
| `python -m pytest -q tests\test_e2_multi_excursion.py tests\test_e2_ir2.py` | PASS — 44 passed, 0 failed, 0 skipped |
| `python -m pytest -q tests\test_excursion_neuron.py tests\test_ir2.py` | PASS — 41 passed, 0 failed, 0 skipped |
| `python -m pytest -q tests\test_acp0002_n2.py tests\test_event_runtime.py` | PASS — 254 passed, 0 failed, 0 skipped |
| `python -m pytest -q tests\test_topology.py` | PASS — 9 passed, 0 failed, 0 skipped |
| `python -m pytest -q` | PASS — 668 passed, 0 failed, 1 skipped |
| `python -m compileall -q tpcn tests` | PASS |
| `python -m py_compile` on the changed Python files | PASS |
| `git diff --check` | PASS |

The focused Pylance diagnostics for the E2 runtime and new E2 tests are clean.
`tpcn/ir2.py` reports one existing unused-import warning for `IREvent`; no
Pylance errors were reported for the changed implementation.

The full-suite skip is recorded as skipped; backend/hardware suites were not
run because they are outside the authorization. During implementation,
early focused fixture assertions were corrected as boundary and stale-event
expectations were clarified; the final focused and full runs above have no
failures.

## Files and revisions

Implementation started from clean `main` at
`0d26c3d6bd253ce3be1a3877ec5f2fcb0cf62868`, equal to fetched `origin/main`.
The implementation commit is `8c0bdbc012410d93e2e212adac251390ec0d22d7`;
the final required boundary/provenance fixture commit is
`bfc866be053f9692382d1be5e048f5b4d280e5f6`.

The handoff is an evidence-only follow-up. No architecture contract,
changelog, IR-2 schema revision, backend, hardware, or learning files were
changed.

## Assumptions, limitations, and next assignment

No unresolved implementation blocker remains within Luna-21 scope. The
one skipped full-suite case is included in the count above; no additional
authorized validation was left unrun. GPU/FPGA/FPAA, ModelSim, hardware
equivalence, calibration, H2, N3, and learning evaluations remain not run
and unauthorized/out of scope.

**Next:** Luna-0 independently reviews the actual implementation at
`bfc866be053f9692382d1be5e048f5b4d280e5f6` and this handoff. Luna-21 does not
authorize a successor or claim independent closure.

**Terminal status: PASS — READY FOR INDEPENDENT REVIEW**
