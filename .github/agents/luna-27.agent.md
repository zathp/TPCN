---
name: Luna-27 TPCV-2 EXCURSION_V1 Snapshot Visualization
description: Implement bounded, deterministic CPU TPCV-2 snapshot capture and replay for EXCURSION_V1 while preserving TPCV-1.
---

# Luna-27 - TPCV-2 EXCURSION_V1 Snapshot Visualization

## Authorization and baseline

Luna-0 authorizes only this bounded CPU visualization representation task.
Start from `622a62c78df2af696920c4c5d1d85c10ecc15baf` or its documented
governance publication descendant, inspect current branch/worktree state, and
preserve unrelated changes.

Read:

- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`
- `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`
- `workflow/docs/luna/VISUALIZATION_CONTRACT.md`
- `workflow/handoffs/luna-0-post-acp0006-tpcv-excursion-compatibility-decision-20261003.md`
- this authorization: `workflow/handoffs/luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003.md`

Return to Luna-0 after implementation. Do not execute later work.

## Decision and observation contract

Implement the exact Luna-0 **Decision C** representation:

- TPCV-1 remains byte- and meaning-compatible. Existing artifacts decode
  identically; do not retrofit or infer model identity for version-1 records.
- TPCV-2 is dedicated to instantaneous `EXCURSION_V1` observations. The
  version is its model discriminator. Never infer a model from numeric values.
- Capture remains epoch-boundary, downstream-only observation. Do not record
  activity over an interval, emit synthetic pulses, or serialize a last
  emission as current activation.
- For TPCV-2, `state` is `MultiExcursionNeuron.state` (`x`); `active` is true
  iff `mode != N`, meaning an excursion mode is currently admitted at the
  snapshot; `mode` is one of `N`, `S_PENDING`, `S_RETURN`, `M_ACTIVE`;
  `pending_internal_work` is exactly
  `pending_internal_event is not None`; and `processed_events` maps to the
  total `processed_event_count`, including processed external and internal
  events.
- TPCV-2 has no scalar activation. Its binary record omits activation; a
  shared high-level decoded view may report `activation=None` as explicit
  unavailability. Do not add an `activation` property to the neuron or
  fabricate a substitute scalar.
- TPCV-2 is not a runtime checkpoint. Do not serialize pending-event payloads
  or sequence IDs, emissions/history, provenance, identity counters,
  prediction/eligibility ledgers, or queue state.

## TPCV-2 bounded wire representation

Keep the TPCV-1 32-byte big-endian header structure and bounds; set its version
byte to `2`. Header flags/reserved bits retain their existing meanings.
Epoch, nonnegative timestamp, neuron/connection counts, and body length retain
the TPCV-1 widths and validation rules.

Format identity is explicit: version `1` means historical TPCV-1
scalar/TANH records; version `2` means instantaneous EXCURSION_V1 records.
Do not infer a model from field values. TPCV-2 bytes must not be parsed as
TPCV-1, and TPCV-1 activation retains its historical scalar meaning. The v1
encoder's bytes and parser's historical behavior remain unchanged; any shared
version dispatch must preserve them exactly.

Each TPCV-2 neuron record contains:

```text
identifier_length:u8, identifier:utf8,
flags:u8, mode:u8, state:f64, processed_events:u32,
[position_x:i32, position_y:i32 if flags.position]
```

The mapping and record ordering are deterministic: the same observable neuron
and topology state at the same capture boundary produces identical TPCV-2
bytes.

Flag bit 0 is `active` and must equal `(mode != N)`; bit 1 indicates optional
position; bit 2 is `pending_internal_work`; all other bits are reserved zero.
Mode codes are `0=N`, `1=S_PENDING`, `2=S_RETURN`, and `3=M_ACTIVE`; all other
values are malformed. State is finite. Processed count is unsigned 32-bit.
IDs remain nonempty UTF-8 with a 255-byte limit; coordinates remain signed
32-bit.

TPCV-2 connection records retain the TPCV-1 `source_length, source,
destination_length, destination, propagation_delay:f64` representation and
meaning. Preserve deterministic ordering and uniqueness checks. The whole
snapshot remains bounded to 1 MiB, with at most 65,535 neuron and connection
records. Reject unsupported versions, invalid flags/modes, malformed UTF-8,
truncated/trailing data, invalid numbers, and all over-limit inputs. Do not
reinterpret TPCV-1 bytes.

Replay remains explicitly bounded: retain the CPU path's maximum snapshot
sequence length and metric-byte limit, enforce per-record size limits on load
as well as parse, preserve digest validation, and reject mixed-version
sequences unless they are explicitly defined as separate homogeneous
sequences. No unbounded identifier, mode text, or event history is allowed.

## Owned files

Own only:

- `tpcn/visualization.py`
- `tpcn/cpu_visualization.py`
- `tests/test_visualization.py`
- `tests/test_cpu_visualization.py`
- `workflow/docs/luna/VISUALIZATION_CONTRACT.md`
- `workflow/handoffs/luna-27-tpcv2-excursion-snapshot-visualization-20261003.md`

Do not modify shared files owned by other work, even if a test reveals an
unrelated defect. Ask Luna-0 before any ownership or semantics expansion.

## Required tests and evidence

Add focused checks that establish:

1. TPCV-1 fixtures, byte round-trip, frames, active/state/activation meanings,
   unsupported-version handling, bounds, and malformed-input rejection remain
   unchanged.
2. TPCV-2 has deterministic byte encoding, round-trip decoding, exact
   `EXCURSION_V1` version identity, state/mode/active/pending/count semantics,
   and no fabricated activation value.
3. Exercise reachable neuron/runtime states for neutral `N` (`active=False`,
   correct `x`, no pending work); `S_PENDING` (`active=True`, pending state
   where produced by the legitimate fixture); `S_RETURN` (`active=True`); and
   `M_ACTIVE` if reachable through the focused supported fixture. Do not
   mutate internals solely to manufacture a record. Retain processed count,
   snapshot timestamp, and fixed topology; no scalar activation is present in
   TPCV-2.
4. Unsupported versions, invalid mode/flag combinations, truncation,
   trailing bytes, oversized records, and mixed TPCV-1/TPCV-2 replay sequences
   fail boundedly and explicitly.
5. Preserve offline save/load, digest validation, frame inspection,
   record-count limits, missing-file, malformed-file, and oversize detection
   for the versioned representation.
6. All three tests in `tests/test_cpu_visualization.py` pass, including
   capture disabled/every epoch/every N epochs equivalence, deterministic
   repeated snapshots, offline replay, and malformed/missing/over-limit
   rejection.
7. Existing `tests/test_visualization.py` and
   `tests/test_gpu_visualization.py` pass without changing GPU semantics.
8. Capture is downstream-only: no queue ordering, neuron state/equations,
   event behavior, predictions/errors, learning, rewards, topology, or
   training-result changes. Capture disabled (`snapshot_every=0`), every
   epoch (`snapshot_every=1`), and interval capture (`snapshot_every=N`) must
   produce identical computational/training results for identical runs;
   capture may change only observer storage and I/O. Keep fixed topology and
   label/future isolation.

`processed_events` must be read from the model's existing observation:
`processed_events` on a legacy neuron and `processed_event_count` on an
excursion neuron. Do not add a canonical-core alias. Capture the snapshot
timestamp and topology at the existing boundary using deterministic ordering.

Run the smallest relevant suites, the focused CPU visualization tests, and
compile/diagnostics checks if available. Report the full-suite baseline and
preserve the other 21 classified downstream failures; do not repair them.
Do not claim EXCURSION_V1 GPU support, ModelSim/FPGA parity, or hardware
equivalence.

## Prohibited work and stop conditions

Do not modify:

- `tpcn/excursion_neuron.py`
- `tpcn/experiment_excursion_runtime.py`
- `tpcn/experiments.py`
- `tpcn/ir2.py`
- `tpcn/gpu_visualization.py`
- `tpcn/fpga_visualization.py`
- `tpcn/viewer_3d.py`
- `tpcn/temporal_analysis.py`
- any Luna-12B, Luna-12E, Luna-12L, spiral, or other unrelated failure-group
  tests or implementations

Do not add interval activity, emission history, event/queue state, structural
plasticity, model equations, core aliases, an ACP, or a new downstream
migration assignment. If TPCV-1 cannot be preserved or if these semantics
prove insufficient, stop and return to Luna-0 without broadening the task.
