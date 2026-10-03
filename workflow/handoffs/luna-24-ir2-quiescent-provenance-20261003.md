# Luna-24 Completion Handoff — ACP-0006 IR-2 Quiescent Provenance Boundary

```yaml
tpcn_handoff:
  agent: "Luna-24"
  luna_identifier: "Luna-24"
  descriptive_name: "ACP-0006 integrated IR-2 residual-provenance boundary correction"
  task_id: "luna-24-ir2-quiescent-provenance-20261003"
  component: "Integrated quiescent IR-2 startup validation"
  status: "complete; submitted for Luna-0 independent review"
  contract_version: "1.1"
  branch: "main"
  base_revision: "6c012f9feeff6481a44bd6d40414b4749b21db17"
  result_revision: "8e184e1bdceeb2873b2ea7479da953760b58ffbf"
  handoff_publication_revision: "The Git commit adding this file; exact hash is reported in the completion summary."
  dependencies:
    - "Accepted ACP-0006"
    - "Luna-0 second independent review of Luna-22"
    - "Luna-23 independently closed at the authorized starting tip"
    - "TPCN-IR-2 schema revision 1 and standalone E2 adapter"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "Integrated startup can reject assigned residual provenance and sticky truncation while preserving quiescent startup, identity high-water counters and standalone E2 reconstruction."
  counter_hypothesis: "Assigned provenance or truncation is required at the accepted fresh integrated initialization boundary."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime.from_quiescent_ir2"
    - "IR2Neuron revision-1 provenance, local state and identity counters"
    - "Standalone neuron_from_ir2_e2 reference conversion"
  label_information_boundary:
    - "Startup decisions depend only on serialized neuron state, model tags, IR-2 events/topology and declared adapter configuration."
    - "No label, future input, task metric or global neural state enters validation."
  timing_assumptions:
    - "Integrated startup is a fresh quiescent boundary, not live scheduler restoration."
    - "The exact state gate remains x == 0.0; no epsilon normalization is used."
  reset_boundaries:
    - "No E1/E2 state transition, reset behavior or scheduler continuation was changed."
  resource_bounds:
    - "Existing event, queue, topology and provenance capacities are unchanged."
  authorized_scope:
    - "Boundary validation in tpcn/experiment_excursion_runtime.py."
    - "Focused startup-boundary tests in tests/test_excursion_integration.py."
    - "This completion handoff."
  unauthorized_scope:
    - "IR-2 schema or standalone E2 adapter changes."
    - "Luna-22 closure, dataset remediation and downstream consumer migration."
    - "Architecture/changelog/workflow status updates."
  controls:
    - "Clean quiescent records, signed zero, exact positive/negative residuals and smallest positive/negative subnormal x."
    - "Valid high-water identities followed by an integrated excursion."
    - "Active E2 modes, shared queue, mixed-model records and standalone active/pending E2 round trips."
  measurements:
    - "Focused, reference, integration-regression and full-suite pytest results."
    - "Serialized signed-zero behavior, schema revision, identity allocations and exact residual-provenance startup outcomes."
  information_boundary_check:
    - "Validation is local to the IR-2 initialization record and shared queue/model selection."
  hardware_mapping:
    - "Hardware-neutral software-reference adapter only; no hardware equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A15"]
  preserves:
    - "A01-A15 and accepted ACP-0006."
    - "IR-2 schema revision 1 and serialized provenance meaning."
    - "Standalone E2 active/pending/provenance reconstruction."
    - "Luna-23 E2 representability behavior."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/experiment_excursion_runtime.py"
    - "tests/test_excursion_integration.py"
    - "workflow/handoffs/luna-24-ir2-quiescent-provenance-20261003.md"
  tests_added:
    - "Expanded residual-state/provenance rejection matrix, signed-zero acceptance, identity high-water continuation, shared-queue rejection and valid S_PENDING/S_RETURN/M_ACTIVE rejection."
  tests_passing:
    - "Focused integration: 43 passed."
    - "IR-2/E2 reference suite: 203 passed."
    - "Luna-22 focused integration controls: 55 passed."
    - "Prescribed integration regression set: 334 passed."
    - "Full CPU suite: 789 passed, 24 failed, 1 skipped."
    - "compileall, Pylance diagnostics and git diff --check passed."
  tests_failed:
    - "Full CPU suite retains the 24 known downstream failures; no new failing tests were observed."
  tests_not_run:
    - "Repository-reproducible sequential-dataset/split/per-class benchmark; unresolved from Luna-22 and outside scope."
    - "Hardware/backend equivalence."
    - "Integrated empty-network startup behavior."
  assumptions:
    - "ACP-0006 clause 13's fresh quiescent boundary excludes assigned provenance entries and sticky provenance truncation, as independently identified by Luna-0."
  unresolved:
    - "Luna-22 remains blocked pending dataset reproducibility/per-class evidence and separately authorized downstream compatibility decisions."
    - "TPCNIR2 accepts an empty neuron collection at schema construction; this task did not extend the schema or add a separate empty-network rule."
    - "The full-suite downstream failure groups remain unmodified and require future governance."
  recommended_next_agent:
    - "Luna-0 for independent verification; no downstream migration is authorized."
```

## Outcome and exact revisions

**OBSERVED:** Work began on clean `main` at the exact authorized tip
`6c012f9feeff6481a44bd6d40414b4749b21db17`, equal to `origin/main`. The
published Luna-22 review commit is an ancestor. The required Luna-23 closure
revision `c0e3e6905e329e5c268d6c63cbb3bd8d89345136` and its finalized handoff
are in the ancestry; Luna-23 was not reopened.

The implementation and test commit is
`8e184e1bdceeb2873b2ea7479da953760b58ffbf`. The handoff is published
separately. Only the three authorized files listed above are included in
Luna-24 commits.

**OBSERVED:** Before the correction, independently constructed valid
revision-1 records with either a non-empty `IR2Provenance` tuple or
`provenance_truncated=True` both returned an `ExcursionCharacterRuntime`
from `from_quiescent_ir2()`. A record with valid provenance fields was used,
not malformed schema data.

The adapter now rejects `record.provenance` and
`record.provenance_truncated` alongside the existing residual `x` and
unassigned-provenance checks, before topology or neuron reconstruction. It
does not clear or rewrite serialized values. The explicit error is
`IR2UnsupportedRuntimeError("integrated IR-2 startup rejects residual state or provenance")`.
The standalone E2 converter and IR-2 schema were not modified.

## Startup acceptance matrix

| Case | Observed result |
|---|---|
| Uniform `EXCURSION_V1`, mode N, x=0, no pending/episode/lineage/provenance | Accepted; deterministic integrated continuation test passes |
| `+0.0` and `-0.0`, serialized and parsed through IR-2 JSON | Both accepted; sign survives JSON parsing and numeric equality admits each |
| Valid nonzero event/episode/lineage/input identity high-water counters | Accepted and restored; subsequent output event, episode and lineage identities exceed prior high-water values |
| Positive and negative ordinary residual x | Rejected |
| Smallest positive and negative finite subnormal nonzero x | Rejected exactly |
| Structurally valid assigned provenance tuple | Rejected |
| `provenance_truncated=True` with empty tuple | Rejected |
| Assigned tuple and truncation together | Rejected |
| Positive unassigned provenance count or unassigned truncation | Rejected independently |
| Assigned plus unassigned provenance, and residual x plus assigned provenance | Rejected |
| `S_PENDING`, active `S_RETURN`, `M_ACTIVE`, including their valid pending-event records | Rejected as live-network resume |
| Mixed `EXCURSION_V1` / `TANH_LEGACY` records | Rejected |
| Valid non-empty shared IR-2 event queue | Rejected |
| Empty neuron collection | `TPCNIR2(())` is accepted by schema construction; integrated empty-network behavior was not tested or changed |
| Duplicate neuron IDs / edge endpoint missing from declared nodes | Rejected by `TPCNIR2` construction |

**OBSERVED:** Integrated activity from the high-water fixture produces
`n0:excursion:8`, output sequence `8`, and episode/lineage identities greater
than their pre-serialization high-water values. The input identity counter is
restored exactly and remains `8` in this adapter path because the integrated
external inputs carry explicit event IDs; no automatic input identity is
allocated in that fixture.

## Standalone IR-2 and Luna-23 controls

**OBSERVED:** The standalone E2 reference suite passed. It includes valid
active/pending round trips, provenance/truncation preservation, counter
restoration and pending continuation. The schema remains
`IR2_SCHEMA_REVISION == 1`, and serialized TPCN-IR-2 documents report revision
1. No `tpcn/ir2.py` or neuron-conversion code changed.

**OBSERVED:** The Luna-23 regression suite, `tests/test_e2_multi_excursion.py`,
passed as part of the 203-test reference run. The positive-delay,
strict-future representability correction remains unchanged.

## Architecture evidence

- **A01 — Event-driven:** no clock, scheduler or execution changes; startup
  only rejects non-quiescent records.
- **A02 — Local temporal state:** no local state/evolution rule changed;
  `x == 0.0` is checked without normalization.
- **A03 — Finite propagation:** pending-event and delay semantics are
  unchanged; records containing valid pending work remain rejected only at
  this fresh integrated boundary.
- **A04 — Bounded topology:** topology/resource limits are unchanged; no
  nodes, edges, paths or queues are added.
- **A08 — Bounded dynamics:** provenance and truncation are not erased or
  expanded; residual provenance is rejected instead of silently carried into
  the new character runtime.
- **A15 — Hardware independence:** this remains a software-reference
  integration guard; no hardware equivalence or backend claim is made.

The adapter decision uses only serialized local state, dynamics tags and the
shared IR-2 event queue. Labels, future inputs, task metrics and global neural
state do not participate.

## Validation record

Environment: Windows, selected Python 3.11.5.

| Command | Observed result |
|---|---|
| `python -m pytest -q tests/test_excursion_integration.py` | **43 passed** |
| `python -m pytest -q tests/test_ir2.py tests/test_e2_ir2.py tests/test_excursion_neuron.py tests/test_e2_multi_excursion.py` | **203 passed** |
| `python -m pytest -q tests/test_experiments.py tests/test_excursion_integration.py` | **55 passed** |
| Prescribed 13-file integration regression command from Luna-24 assignment | **334 passed** |
| `python -m pytest -q -rs` | **24 failed, 789 passed, 1 skipped** |
| `python -m compileall -q tpcn tests` | **Passed** |
| Pylance `textDocument/diagnostic` for source and focused tests | **No diagnostics** |
| `git diff --check` | **Passed** |

The single skip is `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics` because CUDA is unavailable.

**OBSERVED:** The full-suite failure count matches the 24 downstream failures
recorded in the post-Luna-23 baseline. The groups are:

| Consumer group | Failures | Classification |
|---|---:|---|
| CPU visualization | 3 | Downstream scalar activation assumptions |
| Luna-12B structural integration | 4 | Structural-plasticity/default-model compatibility |
| Luna-12E integration | 2 | Existing readout/legacy-observable expectations |
| Luna-12L temporal scale | 8 | Existing model/structure consumer expectations |
| Spiral benchmark | 1 | Existing benchmark/control compatibility |
| Temporal analysis | 3 | Downstream analysis consumer |
| 3D viewer | 3 | Downstream viewer consumer |
| **Total** | **24** | No consumer was edited |

The 14 additional startup-boundary cases collected by Luna-24 pass; total
full-suite passes increase from the recorded 775 to 789. No new failure was
observed.

## Limitations, blockers and terminal verdict

**NOT TESTED:** A retained sequential-dataset loader, split and per-class
benchmark. The Luna-22 evidence gate remains unresolved and out of scope.

**NOT APPLICABLE:** Hardware/backend equivalence, calibration, physical-energy
claims and downstream migration are not authorized by this task.

**INFERRED:** Rejecting residual assigned provenance and sticky truncation at
this fresh integrated boundary implements ACP-0006 clause 13 while preserving
the valid standalone E2 transfer semantics. This is an integration-boundary
rule only, not a claim that those revision-1 IR-2 fields are globally invalid.

**PASS — LUNA-24 ACP-0006 IR-2 QUIESCENT PROVENANCE BOUNDARY CORRECTION
READY FOR INDEPENDENT REVIEW.**

Return to Luna-0 for independent verification. Do not close Luna-22 or Luna-24,
perform downstream migration, or claim Luna-22 closure.
