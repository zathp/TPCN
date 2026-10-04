# Luna-12 Visualization Contract

Visualization is not part of the canonical TPCN computational architecture. It
is an observability and verification facility used to inspect structure
formation and activity across CPU, GPU, simulation, and FPGA implementations.

The interface is downstream-only:

```text
TPCN state -> pull snapshot -> exporter/parser/reference visualizer
```

No renderer, file, transport, queue consumer, or display may inject events or
be required for TPCN correctness. The CPU implementation is in
`tpcn/visualization.py`.

## TPCV version 1

The canonical representation is a bounded binary record stream with the ASCII
magic `TPCV`. All integers and IEEE-754 doubles are big-endian. UTF-8 strings
are length-prefixed and may contain at most 255 encoded bytes. Record order is
canonicalized before export: neurons sort by `neuron_id`; connections sort by
`(source, destination)`.

The 32-byte header is:

| Offset | Width | Field |
| ---: | ---: | --- |
| 0 | 4 | magic `TPCV` |
| 4 | 1 | format version, currently `1` |
| 5 | 1 | flags, bit 0 means incomplete capture; other bits reserved and zero |
| 6 | 2 | reserved, zero |
| 8 | 4 | capture epoch, unsigned 32-bit |
| 12 | 8 | capture timestamp, nonnegative IEEE-754 double |
| 20 | 4 | neuron record count, unsigned 32-bit, bounded to 65,535 |
| 24 | 4 | connection record count, unsigned 32-bit, bounded to 65,535 |
| 28 | 4 | body byte length, unsigned 32-bit |

Each neuron record contains a one-byte identifier length, the identifier, then
`flags:u8, reserved:u8, state:f64, activation:f64, processed_events:u32`.
Neuron flag bit 0 is active/inactive and bit 1 indicates an optional position.
When present, position is two signed 32-bit coordinates. Other neuron flag and
reserved values are invalid.

Each connection record contains `source_length:u8, source:bytes,
destination_length:u8, destination:bytes, propagation_delay:f64`. The current
TPCN topology has propagation delay but no connection strength, so no synthetic
strength field is exported. Future fields require a new format version.

The complete encoded snapshot is bounded to 1 MiB by the CPU reference path.
Export rejects oversized records; parsing rejects truncation, bad UTF-8,
invalid values, count/size overflow, unsupported versions, nonzero reserved
bits, mismatched body framing, and trailing bytes. Empty snapshots are valid.
`incomplete=true` is the explicit result when a producer cannot provide a
complete capture; it is never inferred from missing records. Numeric values are
finite. IDs, counts, epochs, and coordinates have the limits above; no wraparound
or silent truncation is permitted.

The format deliberately omits classifier labels, reward messages, queue
contents, and hidden global state. A caller may provide only separately
authorized observable records, and exporting them must not consume or mutate
the source state.

## TPCV version 2 — EXCURSION_V1 snapshots

TPCV-2 is a separate, instantaneous CPU observation format for
`EXCURSION_V1`. The header remains 32 bytes with the same field widths,
bounds, flags, and reserved bits as TPCV-1; only the version byte is `2`.
The version is the model discriminator. Numeric values must not be used to
infer model identity, and existing TPCV-1 records are not reinterpreted.

Each TPCV-2 neuron record contains:

```text
identifier_length:u8, identifier:utf8,
flags:u8, mode:u8, state:f64, processed_events:u32,
[position_x:i32, position_y:i32 if flags.position]
```

Flag bit 0 is `active` and must equal `(mode != N)`; bit 1 marks the optional
position; bit 2 marks pending internal work; remaining bits are reserved zero.
Mode codes are `0=N`, `1=S_PENDING`, `2=S_RETURN`, and `3=M_ACTIVE`. `state`
is the neuron's current `x`; `processed_events` is its total processed-event
count, including external and internal events. `pending_internal_work` only
reports whether an internal event is pending.

TPCV-2 defines no scalar activation. The shared decoded frame view uses
`activation=None` in the fourth field of the existing neuron tuple to state
that activation is unavailable; the tuple then appends `mode`,
`pending_internal_work`, and `processed_events`. It does not substitute state,
mode, an emission, or interval activity. TPCV-2 is not a runtime checkpoint
and omits pending-event payloads and sequence IDs, emission/history,
provenance, identity counters, prediction/eligibility ledgers, and queue state.
Capture remains downstream-only at existing epoch boundaries.

TPCV-2 retains TPCV-1 connection records, UTF-8 identifier limits,
coordinates, record-count and one-megabyte snapshot bounds, deterministic
ordering, uniqueness checks, and strict framing/value validation. CPU replay
retains each snapshot's version and rejects a sequence mixing TPCV versions.
Offline record loading checks the per-snapshot bound before reading the file.

## Reference tooling

`VisualizationSnapshot.from_components()` pulls public neuron state and
topology edges. `export_snapshot()` and `parse_snapshot()` provide deterministic
serialization and validation. `ReferenceVisualizer` exposes machine-readable
frames and adjacent changed/added/removed neuron and connection sets.
`SnapshotCollector` is an optional bounded buffer; disabled capture returns
without storing or consuming a snapshot.

## Later targets

- CPU visualization and offline replay support TPCV-1 and TPCV-2. TPCV-1
  retains the historical scalar record semantics; TPCV-2 is CPU-only for
  `EXCURSION_V1` under the Luna-27 scope.
- Luna-13 uses `tpcn.gpu_visualization.TorchSnapshotExporter` to produce the
  same logical records. It pulls caller-supplied detached state and activation
  tensors plus bounded directed connections only at the requested epoch
  interval, then uses a synchronous device-to-host transfer and the canonical
  CPU exporter. This is deliberately a correctness-first path; double
  buffering and device-side compact records are deferred until measurement
  justifies them.
- GPU capture is optional and downstream-only. The transfer may synchronize the
  requested tensors, but it is not on the model computation path and does not
  change event ordering, propagation, rewards, topology updates, timestamps,
  bounded queues, or deterministic workload results.
- The adapter does not invent model semantics. Processed-event counts are
  zero when the caller does not provide them, and edge delays must be supplied
  as canonical connection records. Labels, rewards, queues, gradients, and
  optimizer state remain unsupported.
- Supported capture frequency is every positive integer epoch interval; a
  disabled exporter performs no tensor transfer. Expected overhead is one
  host copy and canonical serialization per captured snapshot, dependent on
  tensor size and device transfer cost. Performance is observational only and
  is not an architecture requirement.
- Luna-14 may add ModelSim hexadecimal/binary trace export and a downstream
  FPGA diagnostic path for the DE1-SoC.
- VGA and/or Ethernet are later display/transport targets, not computational
  dependencies.

GPU, ModelSim, FPGA, VGA, and Ethernet implementations are outside Luna-12.