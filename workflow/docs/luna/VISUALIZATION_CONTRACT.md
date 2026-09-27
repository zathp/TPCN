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

## Reference tooling

`VisualizationSnapshot.from_components()` pulls public neuron state and
topology edges. `export_snapshot()` and `parse_snapshot()` provide deterministic
serialization and validation. `ReferenceVisualizer` exposes machine-readable
frames and adjacent changed/added/removed neuron and connection sets.
`SnapshotCollector` is an optional bounded buffer; disabled capture returns
without storing or consuming a snapshot.

## Later targets

- CPU visualization and offline replay use this version-1 parser.
- Luna-13 uses `tpcn.signal_copy_distance.TorchSnapshotExporter` to produce
  the same logical records. It captures a detached hidden-state vector and
  recurrent structural mask only at the requested epoch interval, then uses a
  synchronous device-to-host transfer and the canonical CPU exporter. This is
  deliberately a correctness-first path; double buffering and device-side
  compact records are deferred until measurement justifies them.
- GPU capture is optional and downstream-only. The transfer may synchronize the
  requested tensors, but it is not on the model computation path and does not
  change event ordering, propagation, rewards, topology updates, timestamps,
  bounded queues, or deterministic workload results.
- The signal-copy model has no native processed-event counter or per-edge
  delay. The adapter therefore defaults those observable fields to `0` and
  `1.0` respectively unless supplied by the caller; labels, rewards, queues,
  gradients, and optimizer state remain unsupported.
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