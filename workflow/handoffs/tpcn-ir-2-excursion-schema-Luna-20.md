```yaml
tpcn_handoff:
  agent: Luna-20
  luna_identifier: "Luna-20"
  descriptive_name: "TPCN-IR-2 excursion execution schema"
  task_id: "tpcn-ir-2-schema"
  component: "hardware-neutral TPCN-IR-2 schema and E1 adapter"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "e55f0d96eb7e0ace3a2bf495f29a3bf99e48d2bb"
  result_revision: "80f3f26f37a742f2c9e13b7b4b9c6fdc01cd3771"
  dependencies: ["ACP-0005", "ACP-0004 E1", "ACP-0003 H1/TPCN-IR-1"]
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "A bounded, explicit IR-2 preserves supported E1 state and continuation semantics."
  counter_hypothesis: "Serialization loses ownership, ordering, truncation, or identity continuity."
  interfaces_relied_on: ["TPCN-IR-1", "ACP-0002 N2 Model-B", "ACP-0004 E1"]
  label_information_boundary: ["No labels or evaluation state are represented."]
  timing_assumptions: ["Local timestamps and finite delays are serialized.", "Destination-local external-before-internal ordering is explicit."]
  reset_boundaries: ["Reconstruction restores state and counters without calling reset."]
  resource_bounds: ["Finite provenance capacity, event budget, one pending internal event, and monotonic counters."]
  authorized_scope: ["IR-2 schema, deterministic serialization, validation, E1 conversion, IR-1 upgrade and downgrade rejection."]
  unauthorized_scope: ["M/E2 runtime, backends, learning, H2, N3, hardware, calibration and visualization semantics."]
  controls: ["Explicit version/model/mode discriminators and cross-field validation."]
  measurements: ["70 focused tests; 619 full-suite tests passed; 1 existing test skipped."]
  information_boundary_check: ["No prediction, eligibility, reward, energy, backend or calibration state is in IR-2."]
  hardware_mapping: ["Hardware-neutral logical record only; no device mapping or calibration."]
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A08", "A11", "A15"]
  preserves: ["A01-A15", "ACP-0002 N2 Model-B fields", "TPCN-IR-1 source representation", "TPCV-1 separation"]
  architecture_change: false
  proposal: "ACP-0005"
  files_changed:
    - "tpcn/ir2.py"
    - "tpcn/__init__.py"
    - "tests/test_ir2.py"
    - "workflow/handoffs/tpcn-ir-2-excursion-schema-Luna-20.md"
  tests_added: ["tests/test_ir2.py"]
  tests_passing: ["73 focused IR-2/E1/IR-1 tests", "622 full CPU tests", "1 existing skip"]
  tests_failed: []
  tests_not_run: ["GPU/FPGA/FPAA, M/E2 runtime, H2, N3, calibration and hardware equivalence (unauthorized)"]
  assumptions: ["The current publication revision e55f0d9 is the effective workspace baseline."]
  unresolved: ["Independent Luna-0 review remains required."]
  recommended_next_agent: ["Luna-0: independently review ACP-0005 implementation and evidence."]
```

## Outcome

**OBSERVED:** Added `TPCN-IR-2`, revision 1, with explicit
`TANH_LEGACY`/`EXCURSION_V1` dynamics, bounded E1 state, one valid pending
internal event, provenance truncation, identity high-water marks, Model-B edge
fields, deterministic JSON, and destination-local ordering metadata.

**OBSERVED:** `EXCURSION_V1` N, S_PENDING and S_RETURN records convert back to
the E1 reference without reset semantics. `M_ACTIVE` validates and serializes
as schema data but raises `IR2UnsupportedRuntimeError` in the E1 adapter.
IR-1 upgrades are explicit and excursion downgrade is rejected.

**INFERRED:** The adapter preserves A01-A15 and does not claim complete
live-runtime checkpoint semantics; TPCV-1 remains downstream-only.

## Validation record

| Command | Result |
|---|---|
| `python -m pytest -q tests\test_ir2.py tests\test_execution_ir.py tests\test_excursion_neuron.py` | PASS — 70 passed |
| `python -m pytest -q` | PASS — 619 passed, 1 skipped |
| `python -m py_compile tpcn\ir2.py tpcn\__init__.py tests\test_ir2.py` | PASS |
| `git diff --check` | PASS |

## Scope status

ACP-0005 implementation status is **PASS pending independent Luna-0 review**.
E2/M runtime, H2, N3, Luna-13F, Luna-13G, and all hardware/backend work were
not run and remain outside this assignment.

## Reproduction and rollback

Run the commands in the validation table from the repository root. The
authorized rollback baseline is `439e419a7e949d51fa487cac1acef0634c83215f`;
the publication workspace began at `e55f0d96eb7e0ace3a2bf495f29a3bf99e48d2bb`.

## Next assignment

Return to Luna-0 for independent IR-2 schema review and integration readiness
assessment. Do not close ACP-0005 or authorize M/E2.
