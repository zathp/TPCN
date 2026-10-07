# Luna-47D evidence catalog

The canonical scientific result is `evidence.json`, generated from committed
source `ee522bf6c4882bb09b9bc0af2520e50c3d1a3589`.
Its verdict is **SUPPORTED only for the frozen synthetic regimes**.

* `evidence.json`: full initial/replay trajectories, identities, rational
  timestamps, state boundaries, metrics, fixture/configuration/source hashes,
  13 negative controls, symmetry and integrity/replay digests.
* `initial-pre-idle-correction.json`: **SUPERSEDED, NOT CANONICAL**.
  Retained unchanged from source `9c75e547a67239027d6f8ec8b7f26bc1eae3188e`.
  It incorrectly reports idle neutral recovery at 144 instead of 0.
  All non-idle primary results are identical to canonical evidence.
  Its historical embedded SUPPORTED label is not a current acceptance claim.
* `focused-tests.xml`: final focused tests, 98 passed.
* `applicable-tests.xml`: unchanged applicable regressions, 374 passed,
  1 failed (Luna-46 retained Luna-45 catalog checkout-byte hash).
* `full-tests.xml`: full repository run, 1,422 passed, 2 failed, 7 errors,
  1 CUDA-unavailable skip. Failures/errors are retained without relaxation.
* `validation.json`: commands, counts, corrective history and verified catalog
  byte diagnosis. XML files retain exact failure/test identities and details.

Verify from the lane checkout using its configured Python 3.11.5 interpreter:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47d'
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m experiments.luna47d.run --verify
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m pytest -q tests/test_luna47d_output_model.py
```

The verifier recomputes all fixture/output identities, timestamps, states,
metrics, controls and digests in a fresh process. It checks the source manifest
against the recorded committed source revision. `--generate` is exclusive-create
and refuses dirty worktrees; it must not overwrite this evidence.
For a fresh generation, use the recorded source revision in a fresh checkout
with no existing canonical artifact. No dependency on Luna-47A/B/C exists.

The internal integrity digest hashes sorted, canonical UTF-8/LF JSON excluding
the digest field, not the raw checkout file. Git may convert checkout line
endings. Source SHA-256 identities explicitly normalize CRLF to LF, while
initial/replay canonical records compare exactly. Cross-platform float-byte
equivalence is not established.

Independent Luna-0 review is pending. This catalog neither waives regression
failures nor establishes network reachability, efficacy, production readiness,
architecture promotion or hardware equivalence.
