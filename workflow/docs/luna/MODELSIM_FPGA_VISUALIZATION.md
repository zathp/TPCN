# Luna-14 ModelSim and DE1-SoC Foundation

This milestone adds a downstream diagnostic path. It does not participate in
event routing, topology mutation, classifier state, reward state, or core
reset semantics.

## Trace framing

The canonical Luna-12 `TPCV` v1 snapshot remains the payload. The bridge does
not redefine it. ModelSim emits one uppercase hexadecimal 32-bit word per
line, in this order:

| Word | Field | Encoding |
| ---: | --- | --- |
| 0 | trace magic | `TRC1` (`0x54524331`) |
| 1 | version and flags | version in bits 31..16, flags in bits 15..0 |
| 2 | sequence | unsigned 32-bit |
| 3 | payload length | unpadded byte count |
| 4..N | payload | TPCV bytes, big-endian words, zero-padded |
| last | CRC-32 | CRC-32 of the unpadded payload |

Words and bytes are big-endian. Word order is fixed, and snapshot records are
already sorted by the TPCV exporter. The trace decoder is in
`tpcn.fpga_visualization`.

Flags are `RESET=0x0001`, `SNAPSHOT_START=0x0002`, `SNAPSHOT_END=0x0004`,
`INCOMPLETE=0x0008`, and `UNKNOWN=0x0010`. A reset frame has an empty payload
and resets only diagnostic buffering. Snapshot start/end are explicit, so a
consumer never infers a boundary from timing or missing words.

ModelSim or HDL text output containing any `X` or `Z` in a word is accepted as
a diagnostic token but rejected by default. The decoder reports the unknown
value rather than treating it as a valid TPCV value. An inspection caller may
request replacement with zero for framing analysis, but CRC or canonical TPCV
validation still fails unless the replacement happens to be separately
regenerated.

## FPGA interface

`VHDL_implementation/tpcn_diag_stream.vhd` is a fixed-width 32-bit FIFO with
an intentionally one-way producer interface:

```text
clk, viz_rst
in_valid, in_data[31:0]
out_valid, out_data[31:0], out_ready
overflow, dropped_count[31:0]
```

There is no producer `ready` signal. A full FIFO drops the incoming
diagnostic word, sets sticky `overflow`, and increments saturating
`dropped_count`; the TPCN producer cannot stall. `viz_rst` clears only this
diagnostic state. The TPCN core may share a board-wide reset by deliberate
integration choice, but no such coupling exists in this module.

## DE1-SoC output strategy

VGA is the first local path. `tpcn_diag_vga.vhd` provides a minimal 640x480
timing generator: up to 256 active cells are shown as a 16x16 green grid, and
a red corner indicator shows a nonzero dropped-record counter. It consumes
diagnostic counters only. No Ethernet stack is added; Ethernet remains a
future host-streaming option for richer snapshots.

The current HDL repository is a cell skeleton rather than a complete DE1-SoC
top-level, clock constraint, pin assignment, or board image. Therefore this is
an interface/foundation, not hardware acceptance or hardware equivalence.

## Verification intent

The Python tests exercise a known topology/activity snapshot through export,
ModelSim-style hex framing, and the Luna-12 parser. They also check malformed
unknown handling, independent reset boundaries, and non-blocking overflow.
Compile/elaboration and physical VGA timing/resource checks remain hardware
environment checks and are reported separately in the handoff.