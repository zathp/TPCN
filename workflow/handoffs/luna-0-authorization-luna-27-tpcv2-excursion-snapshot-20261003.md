# Luna-0 Authorization — Luna-27 TPCV-2 EXCURSION_V1 Snapshot Visualization

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Authorize instantaneous TPCV-2 observation for EXCURSION_V1"
  task_id: "luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003"
  component: "CPU TPCV snapshot capture, parser, and offline replay"
  status: "AUTHORIZED — NOT EXECUTED"
  contract_version: "TPCV-1 preserved; TPCV-2 authorized for EXCURSION_V1"
  branch: "main"
  base_revision: "622a62c78df2af696920c4c5d1d85c10ecc15baf"
  result_revision: "uncommitted governance authorization"
  dependencies:
    - "Luna-0 post-Luna-22 TPCV / EXCURSION_V1 compatibility decision"
    - "Existing Luna-12 visualization contract and CPU replay path"
  owner: "Luna-27"
  classification: ["IMPLEMENTATION", "VERIFICATION", "DOWNSTREAM REPRESENTATION"]
  hypothesis: "TPCV-2 can serialize an honest, bounded instantaneous EXCURSION_V1 observation while preserving every existing TPCV-1 artifact and meaning."
  counter_hypothesis: "The required CPU capture/replay path cannot support the versioned observation without changing core computation or broad downstream consumers."
  interfaces_relied_on:
    - "VisualizationSnapshot/export_snapshot/parse_snapshot"
    - "CPUTrainingCapture and ReplaySequence"
    - "MultiExcursionNeuron public observations only"
  label_information_boundary:
    - "No label, future input, unadmitted event, future reward, or future structural decision may be serialized as current observation."
  timing_assumptions:
    - "Capture is an epoch-boundary instantaneous snapshot."
    - "No neural timestep or interval-activity accumulation is introduced."
  reset_boundaries:
    - "No new computation or reset semantics."
  resource_bounds:
    - "Retain 1 MiB snapshot cap, 65,535 record limits, 255-byte UTF-8 IDs, bounded replay sequence and metric limits."
    - "Mode is a fixed finite enum; no variable-size event history is added."
  authorized_scope:
    - "Implement the TPCV-2 CPU observation, encoding, decoding, and offline replay semantics listed in .github/agents/luna-27.agent.md."
    - "Update only the exact owned files listed there."
  unauthorized_scope:
    - "No runtime/core, neuron, scheduler, prediction/error, learning/reward, IR-2, or topology changes."
    - "No GPU/FPGA/FPAA, ModelSim, viewer/temporal-analysis migration, or hardware-equivalence work."
    - "No repair of the other 21 classified downstream full-suite failures."
  controls:
    - "TPCV-1 byte and semantic regression."
    - "Capture disabled/every epoch/every N epochs computational-result equivalence."
    - "Deterministic encoding and detached offline replay."
    - "Bounded parser and mixed-version rejection."
  measurements:
    - "Focused baseline reproduction: 3 CPU visualization tests fail at missing MultiExcursionNeuron.activation."
    - "Closure baseline: 60 topology/focused integration passed; 342 prescribed ACP-0006 tests passed; full CPU 804 passed, 24 failed, 1 skipped; 829 collected."
  information_boundary_check:
    - "TPCV-2 serializes only the defined current snapshot observations."
    - "No labels, future inputs, or future structural decisions."
  hardware_mapping:
    - "TPCV-2 is backend-neutral."
    - "GPU TPCV-1 export, ModelSim/FPGA transport, and hardware equivalence remain outside this authorization."
  architecture_invariants_touched: ["A01", "A04", "A07", "A08", "A15"]
  preserves:
    - "Luna-22 and Luna-26 exact closure scopes."
    - "TPCV-1 historical records and parser semantics."
    - "Downstream-only observation and fixed topology."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-27.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-post-acp0006-tpcv-excursion-compatibility-decision-20261003.md"
    - "workflow/handoffs/luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Luna-27 implementation and verification are not executed by this authorization."
  assumptions:
    - "The project owner was unavailable for the observation-choice question; the requested pragmatic fallback selected the recommended instantaneous, versioned representation."
  unresolved:
    - "No architectural or semantic selection remains within the bounded Luna-27 scope; any discovered incompatibility outside the exact scope returns to Luna-0."
  recommended_next_agent: ["Luna-27"]
```

## Authorization

**AUTHORIZED — NOT EXECUTED.** This Luna-0 invocation publishes the
representation decision and contract only. Luna-27 must not be started or
implemented as part of this authorization task.

## Selected semantics

**DECISION C — VERSIONED EXCURSION VISUALIZATION FORMAT REQUIRED;
LUNA-27 AUTHORIZED.**

TPCV-2 represents only instantaneous EXCURSION_V1 observations at existing
CPU epoch capture boundaries. The version byte `2` is the model discriminator.
Keep TPCV-1 bytes, historical decoding, and field interpretation unchanged.

The precise neuron semantics are:

- `state = x`.
- `active = (mode != N)`, explicitly meaning that a non-neutral excursion mode
  is currently admitted at the snapshot; it does not mean nonzero TANH output.
- `mode` is one of `N`, `S_PENDING`, `S_RETURN`, `M_ACTIVE`.
- `pending_internal_work` is the boolean existence of pending internal work;
  do not serialize pending-event payloads or queue sequence.
- `processed_events = processed_event_count`, including processed external and
  internal events.
- No scalar activation, last emission, interval activity, or event history is
  serialized. A shared decoded API may explicitly represent unavailable
  activation as `None`; never add `MultiExcursionNeuron.activation`.
- TPCV-2 is observational, not a runtime checkpoint.

The 32-byte header, big-endian encoding, one-megabyte record limit, maximum
record count, identifier bound, optional coordinates, connection encoding,
canonical order, and strict validation remain bounded. The TPCV-2 neuron
record has length-prefixed UTF-8 ID, flags for `active`, optional position,
and pending internal work, mode code `0..3`, finite `state:f64`,
`processed_events:u32`, and optional signed 32-bit coordinates. Connection
records retain their TPCV-1 layout and meaning.

## Exact ownership

Luna-27 owns only:

- `tpcn/visualization.py`
- `tpcn/cpu_visualization.py`
- `tests/test_visualization.py`
- `tests/test_cpu_visualization.py`
- `workflow/docs/luna/VISUALIZATION_CONTRACT.md`
- `workflow/handoffs/luna-27-tpcv2-excursion-snapshot-visualization-20261003.md`

All other files are outside scope, especially neuron/runtime/IR-2 code,
`tpcn/gpu_visualization.py`, `tpcn/fpga_visualization.py`,
`tpcn/viewer_3d.py`, `tpcn/temporal_analysis.py`, and the other 21 downstream
failure-group tests and implementations.

## Required verification and stop conditions

The agent contract `.github/agents/luna-27.agent.md` is normative. In
particular, Luna-27 must preserve exact TPCV-1 behavior; add deterministic
TPCV-2 round-trip and semantics checks; reject malformed, oversize,
unsupported, and mixed-version data; pass the three focused CPU tests,
existing visualization tests, and GPU TPCV-1 regression; and demonstrate
capture-on/off result equivalence and offline replay. Fixed topology and
label/future isolation remain unchanged.

If preserving TPCV-1 or implementing these exact semantics requires core
changes or ownership expansion, stop and return to Luna-0. Do not repair the
other 21 full-suite failures and do not claim GPU EXCURSION_V1, ModelSim/FPGA,
or hardware equivalence. After verification, return to Luna-0 for independent
review; do not self-close or authorize a successor.
