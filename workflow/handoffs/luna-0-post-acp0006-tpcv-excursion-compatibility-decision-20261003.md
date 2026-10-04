# Luna-0 Post-ACP-0006 TPCV / EXCURSION_V1 Compatibility Decision

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Versioned instantaneous EXCURSION_V1 TPCV snapshot decision"
  task_id: "luna-0-post-acp0006-tpcv-excursion-compatibility-decision-20261003"
  component: "CPU TPCV visualization/replay compatibility with EXCURSION_V1"
  status: "DECISION C — VERSIONED EXCURSION VISUALIZATION FORMAT REQUIRED; LUNA-27 AUTHORIZED"
  contract_version: "TPCV-1 retained; TPCV-2 authorized; architecture contract unchanged"
  branch: "main"
  base_revision: "622a62c78df2af696920c4c5d1d85c10ecc15baf"
  result_revision: "uncommitted governance publication"
  publication_revision: "uncommitted; HEAD remains 622a62c78df2af696920c4c5d1d85c10ecc15baf"
  dependencies:
    - "Luna-22 and Luna-26 closure evidence at the baseline"
    - "TPCV-1 and CPU visualization contracts/handoffs"
  owner: "Project owner; pragmatic default selected because owner unavailable"
  classification: ["GOVERNANCE", "REPRESENTATION DECISION", "INDEPENDENT FAILURE REPRODUCTION", "BOUNDED AUTHORIZATION"]
  hypothesis: "TPCV-1 can represent the current EXCURSION_V1 epoch observation without changing the meanings of its existing neuron fields."
  counter_hypothesis: "A field mapping requires inventing an activation/activity meaning or misrepresenting persistent excursion observations as current activity."
  interfaces_relied_on:
    - "NeuronRecord.from_neuron and VisualizationSnapshot.from_components"
    - "CPUTrainingCapture epoch-boundary observer"
    - "ReplaySequence.frames, ReferenceVisualizer.frames and changes"
    - "TPCV-1 parser/exporter and version-1 wire representation"
  label_information_boundary:
    - "Snapshot records contain no training label or future input."
    - "No label, reward, or future structural decision may enter a neuron observation."
  timing_assumptions:
    - "CPUTrainingCapture observes at epoch boundaries."
    - "Luna-12C governance describes TPCV-1 as snapshot-level activity and prohibits fabricated event pulses/timing."
    - "No interval-activity accumulator is present in the current observer."
  reset_boundaries:
    - "No new runtime state or reset boundary is authorized by this review."
  resource_bounds:
    - "Current TPCV-1 record, identifier, snapshot, and replay bounds remain unchanged."
    - "Any future version must retain explicit bounded parsing and sequence limits."
  authorized_scope:
    - "Governance review and focused reproduction of the three CPU visualization tests."
    - "Publication of this decision, Luna-27 agent contract, workflow entry, and authorization handoff."
    - "Luna-27 implementation is authorized only for the exact owned files and acceptance checks below."
  unauthorized_scope:
    - "No visualization implementation, test repair, consumer migration, or model change in this Luna-0 invocation."
    - "Do not execute Luna-27 in this Luna-0 invocation."
    - "No GPU, ModelSim, FPGA, FPAA, or hardware-equivalence work."
    - "No Luna-12B, Luna-12E, Luna-12L, spiral, temporal-analysis, or 3D-viewer repair."
    - "No change to MultiExcursionNeuron equations/state machine, ACP-0006 scheduler, prediction/error logic, eligibility/reward, or IR-2."
  controls:
    - "Clean requested starting revision and branch checked."
    - "All three tests in tests/test_cpu_visualization.py run independently."
    - "No production implementation changed."
  measurements:
    - "Focused CPU visualization reproduction: 3 failed, all at missing MultiExcursionNeuron.activation."
    - "Full-suite figures are cited from the current independent closure record, not rerun in this governance task."
  information_boundary_check:
    - "TPCV record fields do not include labels or future inputs."
    - "No future data is required to describe the observed adapter failure."
  hardware_mapping:
    - "Canonical representation must remain backend-neutral."
    - "Luna-13 consumes TPCV-1 logical records; Luna-14 wraps TPCV payloads for diagnostic transport."
    - "No backend parity or hardware equivalence is claimed."
  architecture_invariants_touched: ["A01", "A04", "A07", "A08", "A15"]
  preserves:
    - "Luna-22 and Luna-26 exact closure scopes."
    - "TPCV-1 historical bytes and parser semantics."
    - "Downstream-only capture/replay and current parser bounds."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - ".github/agents/luna-27.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003.md"
    - "workflow/handoffs/luna-0-post-acp0006-tpcv-excursion-compatibility-decision-20261003.md"
  tests_added: []
  tests_passing:
    - "Starting branch main, HEAD == origin/main == 622a62c78df2af696920c4c5d1d85c10ecc15baf, worktree clean before publication."
    - "Luna-26 closure evidence: topology plus focused integration 60 passed; prescribed ACP-0006 regression set 342 passed."
  tests_failed:
    - "`C:\\Users\\zathp\\AppData\\Local\\Programs\\Python\\Python311\\python.exe -m pytest -q tests\\test_cpu_visualization.py`: 3 failed in 0.37s; every failure raises AttributeError for missing MultiExcursionNeuron.activation from NeuronRecord.from_neuron."
  tests_not_run:
    - "Full CPU suite was not rerun; the exact baseline is 804 passed, 24 failed, 1 skipped, 829 collected, per the independent Luna-26 closure evidence."
    - "No compile, lint, GPU, ModelSim, FPGA, or hardware-equivalence validation was run; no production code changed."
  assumptions:
    - "The owner was unavailable to answer interactively; the requested pragmatic fallback selects the recommended instantaneous, versioned representation."
    - "The epoch-boundary capture and existing TPCV-1 contracts remain authoritative."
  unresolved:
    - "Luna-27 must implement and verify the exact TPCV-2 observer semantics and acceptance checks below."
  recommended_next_agent:
    - "Luna-27 TPCV-2 EXCURSION_V1 Snapshot Visualization; return to Luna-0 for independent review."
```

## Terminal governance verdict

**DECISION C — VERSIONED EXCURSION VISUALIZATION FORMAT REQUIRED;
LUNA-27 AUTHORIZED.**

**Starting revision:** clean branch `main`, with `HEAD == origin/main ==
622a62c78df2af696920c4c5d1d85c10ecc15baf` (`docs: pin independent closure
revision`). **Publication revision:** this handoff and its changelog entry are
uncommitted; no commit was created.

### Luna-22 and Luna-26 closure verification

The current independent review and changelog preserve:

- **Luna-22 — CLOSED / INDEPENDENTLY VERIFIED** only for the accepted first
  fixed-topology `EXCURSION_V1` CPU software-reference integration.
- **Luna-26 — CLOSED / INDEPENDENTLY VERIFIED** only for the authorized
  multi-hop prediction-error routing correction.
- Luna-23, Luna-24, Luna-25 retain their exact prior closed scopes.

The closure does not establish predictive efficacy, useful delayed-credit
learning, EXCURSION_V1 structural plasticity, downstream migration,
historical Luna-22 dataset reconstruction, writer-disjoint efficacy,
GPU/FPGA/FPAA equivalence, or calibrated physical energy.

Closure evidence at this baseline records:

| Check | Result |
|---|---:|
| Topology plus focused integration | 60 passed |
| Prescribed ACP-0006 regression set | 342 passed |
| Full CPU suite | 804 passed, 24 failed, 1 skipped |
| Test collection | 829 |

These are cited from the reviewed closure record. The full suite was not
rerun in this governance task.

### Focused failure reproduction

Ran:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q tests\test_cpu_visualization.py
```

**OBSERVED:** all three tests fail:

- `test_capture_modes_do_not_change_training_result`
- `test_snapshot_sequence_is_deterministic_and_replays_offline`
- `test_replay_rejects_missing_malformed_and_over_limit_data`

Each failure follows:

```text
CPUTrainingCapture.observe
 -> VisualizationSnapshot.from_components
 -> NeuronRecord.from_neuron
 -> getattr(neuron, "activation")
 -> AttributeError: 'MultiExcursionNeuron' object has no attribute 'activation'
```

The default `ExperimentConfig.neuron_model` is `EXCURSION_V1`; the CPU
capture path observes the runner's resulting neurons at epoch boundaries.
The failure is therefore a current default-model compatibility gap, not a
malformed-replay result. The replay validation test cannot reach its
malformed-record assertion because capture fails first.

The excursion neuron already exposes `state` as an alias of `x`, so TPCV-1
`state` has a plausible direct instantaneous observation. `active` and
`activation` do not have an accepted excursion meaning. The excursion exposes
mode, pending internal work, processed-event count, and bounded emissions,
but none is interchangeable with the historical TANH scalar output. In
particular, serializing a last emission as the current activation could expose
a stale emission as a current snapshot value.

TPCV-1's `processed_events` field and the excursion's
`processed_event_count` are a naming-level adapter mismatch for the broad
concept of events processed. The E2 count includes its processed internal
events as well as external events, so values are not automatically
cross-model-equivalent unless the field is specified as the total processed
event count.

### Observation timing and replay audit

The CPU observer samples only at epoch boundaries; it does not retain a
per-epoch emission accumulator. Existing Luna-12C workflow governance
requires snapshot-level activity and explicitly prohibits synthesized event
pulses or timing. Accordingly, interval activity and event-by-event histories
are not supported by the current visualization contract. This does not define
whether an EXCURSION_V1 record should include only instantaneous `x`, include
mode/pending-work, or expose a prior emission as a separately timestamped
observation.

`ReferenceVisualizer.frames()` exposes each snapshot's `active`, `state`, and
`activation`; `changes()` compares the complete neuron records between
adjacent snapshots. `ReplaySequence.frames()` and `.changes()` delegate to
that reader. The 3D viewer and temporal analysis interpret `active` as
snapshot-level activity and use `activation` as a generic recorded scalar.
None has a dynamics-model discriminator. Existing TPCV-1 bytes remain
decodable and must not be reinterpreted.

### Option matrix

| Candidate | Semantic honesty | Historical compatibility | Information loss | Replay ambiguity | Implementation scope | Existing artifacts | CPU visualization tests | Luna-13 GPU exporter | Future ModelSim / FPGA | Architecture / ACP impact | Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **A — TPCV-1 legacy-only** | Honest if TPCV-1 is explicitly restricted to the historical scalar/TANH observation and the CPU caller explicitly selects `TANH_LEGACY`. | Preserves version-1 wire bytes and meanings. | EXCURSION_V1 state/mode/emissions are not visualized. | Low for version-1 artifacts if all are attributed to the legacy model; no new model inference. | Small bounded legacy CPU path/test adjustment; E2 visualization remains a separate future task. | Decode unchanged. | Could pass by explicitly running legacy visualization; current default E2 tests would otherwise remain a valid missing-coverage signal. | Luna-13's state/activation exporter remains legacy-shaped; no model marker exists. | TPCV-1 remains portable but limited to the legacy scalar observation; no backend-specific fields. | Governance clarification only; no ACP if computational semantics remain unchanged. | **Not selected:** Luna-12A's published scope does not explicitly declare the path legacy-only, and the owner has not accepted excluding E2. |
| **B — E2 observer adapter into TPCV-1** | Not honest under the existing contract: `state = x` is plausible, but no scalar activation or active predicate is defined for E2. Mapping x, mode, pending work, m_peak, or stale emission into the old scalar/bit would change or fabricate meaning. | Wire bytes remain parseable, but consumers would interpret fields using the old model semantics. | Mode, pending work, and emission identity/timing cannot be represented; any chosen scalar loses distinct E2 state. | High: TPCV-1 has no dynamics-model field, and the same bytes cannot disambiguate legacy versus E2 meaning. | Small code diff but broad semantic damage across replay/readers. | Byte-compatible but semantic reinterpretation risk. | May make tests green while asserting an unapproved field mapping. | Same logical schema but no model marker; parity can repeat the ambiguity. | Backend-neutral bytes, but backend implementations would need an external unstated mapping. | No core ACP needed in principle, but the proposal is rejected because it violates TPCV field semantics. | **Rejected.** |
| **C — explicitly versioned excursion visualization schema** | Honest under the selected snapshot semantics: `state=x`; `active=(mode != N)` means an excursion is currently admitted, not that a TANH output is nonzero; no scalar activation is defined. | TPCV-1 decoder/bytes remain unchanged; TPCV-2 is dispatched explicitly and cannot reinterpret v1 bytes. | A snapshot is not a checkpoint; no emissions, queues, provenance, ledgers, or identity counters are serialized. | Low: TPCV-2 normatively identifies EXCURSION_V1; do not infer model from numeric values. | Bounded CPU snapshot/parser/replay implementation and tests only; no blanket downstream migration. | Preserved and still decodable as v1. | Covers E2 with explicit current-state semantics and no fabricated `.activation` on the neuron. | Luna-13 TPCV-1 exporter remains unchanged; no GPU EXCURSION_V1 semantics are claimed. | Backend-neutral bytes; Luna-14 transport is not changed and hardware decoding remains unverified. | Visualization-format governance only; no ACP because computation semantics do not change. | **SELECTED — Luna-27 authorized** for instantaneous TPCV-2 snapshots only. |

### Architecture and information-boundary audit

- **A01 — event-driven computation:** epoch capture remains an existing
  observer boundary; it does not create neural time. No interval accumulator
  or tick is authorized here.
- **A04 — bounded resources:** current record/sequence/parser caps remain in
  force. Any future interval metric or added field must have explicit finite
  bounds; no per-neuron unbounded event log is acceptable.
- **A07 — local learning/information boundary:** visualization is downstream
  only; labels, future inputs, unadmitted events, future rewards, and future
  structural decisions are not neuron observations.
- **A08 — bounded dynamics/replay:** deterministic serialization, offline
  replay, malformed/missing/oversize rejection, and snapshot-frequency
  capture invariance remain required.
- **A15 — backend-neutral reference:** CPU/GPU/ModelSim/FPGA adapters must
  share an explicitly versioned semantic representation. This review makes
  no hardware-equivalence claim.

No A01-A15 clause changes. No ACP is required for a downstream observational
format decision; no computational architecture departure is proposed.

### Terminal representation and authorization

**Decision C** selects `TPCV-2`, dedicated to instantaneous
`EXCURSION_V1` observations. The version is the model discriminator; no
numeric-value inference is permitted. TPCV-1 bytes, parser interpretation,
and existing replay artifacts remain unchanged.

At an epoch-boundary snapshot:

- `state` is the excursion neuron's existing `state` alias, `x`.
- `active` is true exactly when `mode != N`; it means an excursion mode is
  currently admitted at the snapshot, not nonzero TANH activation.
- `mode` is the explicit bounded enum `N`, `S_PENDING`, `S_RETURN`, or
  `M_ACTIVE`.
- `pending_internal_work` is whether `pending_internal_event` exists; do not
  serialize its payload, queue sequence, or runtime checkpoint data.
- `processed_events` is the total processed-event count exposed by
  `processed_event_count`, including processed external and internal events.
- No scalar activation is defined for TPCV-2. The record must encode/report
  it as unavailable (high-level representation `None` if a shared shape
  requires the field), without adding an `activation` property to
  `MultiExcursionNeuron`.
- No last-emission payload, interval accumulator, or event history is
  serialized. The observation is instantaneous at the capture boundary.

- **TPCV decision:** `DECISION C — VERSIONED EXCURSION VISUALIZATION FORMAT
  REQUIRED; LUNA-27 AUTHORIZED`.
- **New format version:** TPCV-2, for EXCURSION_V1 only.
- **Luna-27 authorized:** **yes; not executed in this invocation**.
- **Agent contract:** `.github/agents/luna-27.agent.md`.
- **Authorization handoff:**
  `workflow/handoffs/luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003.md`.
- **Exact owned files:** `tpcn/visualization.py`,
  `tpcn/cpu_visualization.py`, `tests/test_visualization.py`,
  `tests/test_cpu_visualization.py`,
  `workflow/docs/luna/VISUALIZATION_CONTRACT.md`, and
  `workflow/handoffs/luna-27-tpcv2-excursion-snapshot-visualization-20261003.md`.
- **Explicitly prohibited:** `tpcn/excursion_neuron.py`,
  `tpcn/experiment_excursion_runtime.py`, `tpcn/experiments.py`,
  `tpcn/ir2.py`, `tpcn/gpu_visualization.py`,
  `tpcn/fpga_visualization.py`, `tpcn/viewer_3d.py`,
  `tpcn/temporal_analysis.py`, all unrelated failure-group tests, and all
  hardware/runtime/core work.

### Remaining full-suite downstream groups

The other 21 failures are outside this review and must not be repaired by a
future bounded CPU TPCV compatibility task:

| Group | Count | Classification |
|---|---:|---|
| Luna-12B structural integration | 4 | Structural/default-model consumers |
| Luna-12E legacy observables | 2 | Legacy model observables |
| Luna-12L temporal scale | 8 | Temporal-scale/classifier policy assumptions |
| Spiral benchmark | 1 | Benchmark control result |
| Temporal analysis | 3 | Analysis against legacy/default assumptions |
| 3D viewer | 3 | Replay/viewer compatibility |

Together with the three CPU visualization failures reproduced above, these
match the independent closure baseline of 24 failures.

## Decision rationale and Luna-27 acceptance

The original owner-choice question could not be answered interactively; under
the requested pragmatic fallback, choose the recommended snapshot-only
versioned option. This matches the existing Luna-12C requirement to show
snapshot-level activity without inventing event pulses. `mode != N` is an
explicit semantic predicate for an excursion currently in a non-neutral
mode; it does not claim output magnitude or event emission. TPCV-2 carries no
activation scalar, last emission, or interval activity.

The alternatives are not interchangeable: `x != 0` can describe residual
state while the mode is neutral; pending work alone omits active modes that
currently have no queued internal event; “emitted since previous snapshot”
is interval activity and would require an explicit accumulation/reset
boundary; and last emission can be stale at the capture time. `mode != N`
directly answers whether an excursion mode is active at the instantaneous
snapshot and preserves `x` separately as the state value.

Luna-27 must:

- Keep the current 32-byte header structure, 1 MiB snapshot cap, record/ID
  limits, canonical ordering, finite-number checks, and strict framing for
  TPCV-1. Define TPCV-2 as version byte `2`; dispatch by version, never by
  numeric values.
- Use the TPCV-2 neuron record layout: length-prefixed UTF-8 ID; flags for
  `active`, optional position, and pending internal work; a bounded mode
  enum; finite `state:f64`; `processed_events:u32`; and optional signed
  32-bit position. TPCV-2 does not serialize a scalar activation. Connection
  records retain their TPCV-1 layout and meaning.
- Preserve deterministic export/parse, offline replay, bounded malformed
  input failure, and all TPCV-1 historical byte/round-trip semantics.
- Reject unsupported versions, malformed flags/modes, truncated/oversized
  records, and sequences mixing TPCV-1 and TPCV-2 model semantics.
- Verify capture disabled/every epoch/every N epochs produces identical
  computational and training results; repeated TPCV-2 captures are byte
  deterministic and replay offline.
- Keep the capture downstream-only: no event, queue, scheduler, neuron,
  prediction, learning, reward, topology, or training behavior changes;
  fixed topology remains unchanged and no labels/future inputs are exported.
- Run all three focused CPU tests, the existing visualization tests, and the
  focused GPU TPCV-1 regression to prove v1 stays unchanged. Do not repair the
  other 21 full-suite downstream failures.
- Update only the listed owned files. Return to Luna-0 with a handoff and
  exact validation; do not claim GPU EXCURSION_V1, ModelSim/FPGA, or hardware
  equivalence.
