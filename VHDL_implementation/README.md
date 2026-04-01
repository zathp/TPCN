# VHDL Simulation Starter (TPCN Cell Skeleton)

This folder contains a first-pass VHDL simulation setup using GHDL.

## Files
- `tpcn_cell.vhd`: Synthesizable TPCN cell skeleton with:
  - 10 gated pathway inputs
  - delayed-error ring buffer
  - Q8.8 fixed-point style integer math
- `tb_tpcn_cell.vhd`: Self-contained testbench
- `run_ghdl.ps1`: Analyze, elaborate, and run in one step

## Prerequisites
- GHDL installed and available in PATH

## Run
From this folder:

```powershell
.\run_ghdl.ps1
```

This generates `tpcn_cell_tb.vcd` for waveform inspection.

## Next suggested extensions
1. Replace flattened pathway bus with array-of-record style interfaces.
2. Add explicit gate normalization (softmax approximation or sum clamp).
3. Add local-neighborhood input ports to mimic spatial locality constraints.
4. Add energy penalty and sparse gate regularization outputs for training feedback.
