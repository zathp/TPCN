# Luna-47F: retained causal candidate replay

This directory is an offline, standard-library diagnostic. It does not import
TPCN or run a network. Read [PROTOCOL.md](PROTOCOL.md) before interpreting rows.

Run from the isolated repository root:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47f'
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' experiments/luna47f/diagnostic.py --check
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m pytest -q tests/test_luna47f_diagnostic.py tests/test_luna47f_retained.py
```

The published output already exists, so use `--check`: it recomputes both
retained phases, requires exact canonical analysis equality and checks source,
code and all protected hashes without writing. Initial generation uses the same
command without `--check` and requires the fixed output to be absent. Never
remove a source fixture or retained input to reproduce this diagnostic.
Raw working-byte/code hashes deliberately bind the original materialization;
another checkout/environment may fail this strict identity check even if it
would produce equal analytical rows. Cross-platform parity is not established.

`artifacts/luna47f/diagnostic.json` contains:

- `analysis.rows`: **2,420** enumerated pairs, including duplicates;
- `analysis.summary`: separate proxy/deposition families; do not pool them;
- `source_inventory`: 12 published input identities, exact working and Git-blob
  SHA-256/lengths and checkout-materialization classification;
- `trace_roles`: maps each row's logical `phase` JSON pointer to initial/replay
  files. Rows preserve event IDs, node IDs, stream, exact times and trigger chain;
- `retained_configuration`: complete retained source configuration/provenance;
- `non_mutation`: all 878 non-owned tracked-file pre/post SHA-256 values;
- `analysis.blocked_metrics`: absent information, never imputed values.

`artifacts/luna47f/validation.json` records commands, tests and all observed
failures. The handoff records scientific interpretation and publication gates.

## Reading a candidate

An `opportunity: true` row is compatible and inside the fixed temporal window.
It is not an edge. `existing_edge_duplicate` and
`repeated_endpoint_proposal` overlap and must not be summed as distinct rejected
opportunities. The 235 novel proxy rows represent the **same one endpoint
pair** (`source` -> `destination`) over 108 streams, not 235 new edges.
Static capacity is evaluated independently against the frozen graph for each
row; hypothetical proposals never consume capacity.

`local-deposition` compares two retained event-local deposition changes.
`output-drive-proxy` compares emitted drive against a later deposition and
does **not** establish intrinsic source-state-delta compatibility.
All novel proxy rows have zero destination canonical-emission association.
Their hop reduction is an analytical geometric opportunity, not a measured
latency/resource/learning benefit. Source-local availability and usable edges
remain BLOCKED. Nothing in this diagnostic is fed back into computation.
