# Luna-47B retained deposition-gain diagnostic

Read [PROTOCOL.md](PROTOCOL.md) first. Results are in
`artifacts/luna47b/results.json`; validation is in `validation.json`.
This experiment does not run the network or alter production computation.

From this isolated branch in a clean worktree:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47b'
& 'C:/Users/zathp/Documents/programming/TPCN/.venv/Scripts/python.exe' -m pytest -q tests/test_luna47b_gain.py
& 'C:/Users/zathp/Documents/programming/TPCN/.venv/Scripts/python.exe' -m experiments.luna47b.diagnostic --replay
```

Replay regenerates the artifact in memory, checks the pinned execution
revision is an ancestor, verifies protocol/code committed content, verifies
all pinned committed evidence, and demands exact artifact bytes.
It never overwrites the result. Exact-byte replay includes Python/environment
and checkout-source hashes, so use the recorded environment/materialization.
Portable mathematical replay is also covered by the focused tests.

For a new initial artifact, use the original committed execution revision
`38891b8` in a separate clean checkout and run the module without `--replay`.
The initial path must not already exist. No broader parameter search is
authorized.

The result contains all 320 identities and their preserved categories.
Every sequence includes full retained input/state boundaries, unit-gain
analytical states, critical gain (or explicit no-crossing), two local
critical brackets when applicable, and each global gain trajectory.
Counterfactual states stop at the first threshold boundary; later retained
inputs remain visible with censored states. This is intentional: post-trigger
discharge, fast-state admission, new events and changed future activity were
not simulated or inferred.
