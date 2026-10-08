---
tpcn_handoff:
  agent: "Luna-49 Runtime Reproducibility Characterization"
  luna_identifier: "Luna-49"
  descriptive_name: "Runtime/numerical reproducibility characterization"
  task_id: "luna-49-runtime-reproducibility-20261008"
  component: "Luna-44 numerical materialization provenance"
  status: "complete - PASS WITH FOLLOW-UP"
  contract_version: "1.0"
  branch: "main"
  starting_revision: "7739ad7af868e2b2f5ebcf9685c25978022a25af"
  execution_revision: "the published commit containing this handoff; see Git commit metadata"
  owner: "Project owner"
  classification:
    - "runtime/numerical provenance characterization"
    - "diagnostic and read-only retained-data review"
    - "no scientific experiment or architecture change"
  authorization_contract_revision: "7739ad7af868e2b2f5ebcf9685c25978022a25af"
  authorization_identifier_as_supplied: "59e5ab7b475b74a23faeddc2563eedf1e044; unresolved and not a full Git object ID"
  canonical_fixture_sha256: "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629"
  canonical_provenance_sha256: "6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22"
  canonical_source_revision: "a79494cd66be28fd291ed11eddd62d342f457cfd"
  label_information_boundary:
    - "No labels or class outcomes were read into computation."
  runtime_matrix:
    - "Two independent CPython 3.11.4 Windows 10 x64 materializations: byte-identical."
    - "Two reviewed CPython 3.11.5 Windows x64 materializations: same reported fixture SHA as Luna-49."
    - "CPython 3.10 Windows matched the first differing point in Luna-48 review; full fixture SHA not established."
    - "Historical CPython 3.12.3 Linux/glibc 2.39/GCC 13.3.0 environment unavailable for fresh Luna-49 replay."
  measurements:
    - "Per-field exact binary64 bits, absolute/relative differences, ULP distances, and distributions over 5,164 points."
    - "Current-only angle/radius/trigonometric/rotation/Gaussian-noise operation trace for c00-000 point 3."
    - "Two independent current materialization records and exact runtime/source identities."
    - "Read-only comparison of retained Luna-46 and Luna-47F gate drift."
  architecture_change: false
  proposal: null
  files_changed:
    - ".gitattributes"
    - "scripts/luna49_runtime_characterization.py"
    - "tests/test_luna49_runtime_characterization.py"
    - "artifacts/luna49-runtime-reproducibility-20261008/"
    - "workflow/handoffs/luna-49-runtime-reproducibility-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_passing:
    - "Luna-49 focused: 7 passed."
    - "Luna-44 fixture/provenance: 60 passed."
    - "Luna-46 retained diagnostic: 165 passed, 1 skipped."
    - "Luna-47 focused retained suite: 306 passed."
    - "Historical/core regression: 676 passed."
    - "Full suite: 1,645 passed, 1 skipped."
  tests_failed:
    - "Two Luna-44 exact comparisons: fresh Windows materialization differs from the pinned historical Linux fixture."
    - "Luna-46 raw catalog SHA check: Windows CRLF checkout bytes differ from the valid pinned Git blob."
    - "Luna-47F retained check: retained input/snapshot drift after later source/governance changes and CRLF checkout."
  tests_not_run:
    - "Fresh downstream neural/route/threshold/category replay; prohibited scientific execution and no fresh decision outputs retained."
    - "CPython 3.12.3/Linux exact historical-runtime replay; that environment was unavailable."
  limitations:
    - "Historical intermediate trig, rotation, and Gaussian-noise values were not retained and cannot be uniquely recovered from final coordinates."
    - "Exact historical libm binary identity was not recorded."
    - "Downstream neural decision margins and cross-runtime category stability remain unknown."
  final_disposition: "PASS WITH FOLLOW-UP"
  next_step: "Luna-49 execution -> Luna-0 independent review"
---

# Luna-49 Runtime Reproducibility Characterization

## Starting State and Authorization

Fetched all remotes. The worktree was clean and both `HEAD` and `origin/main`
were `7739ad7af868e2b2f5ebcf9685c25978022a25af`. The committed Luna-49
contract is present at that revision. The supplied authorization identifier
`59e5ab7b475b74a23faeddc2563eedf1e044` does not resolve as a Git object and is
not a complete SHA-1 commit ID; the exact published revision containing the
authoritative Luna-49 contract is `7739ad7af868e2b2f5ebcf9685c25978022a25af`.
The contract at that revision governed this execution.

Canonical fixture SHA-256 and provenance SHA-256 were independently verified
before and after analysis. Neither changed. The pinned source Git-object
revision remains `a79494cd66be28fd291ed11eddd62d342f457cfd`; no canonical source,
fixture, provenance, parameter, or retained scientific artifact was modified.

## Runtime Matrix

| Runtime | Evidence and materialization identity | Classification |
|---|---|---|
| CPython 3.12.3, Linux x86_64, glibc 2.39, GCC 13.3.0 | Historical provenance records two separate processes/invocations with fixture SHA `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629` and semantic digest `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`. Kernel recorded as Linux 6.17.0-1022-azure. | Byte-deterministic in retained records; exact Luna-49 replay unavailable. |
| CPython 3.11.5, Windows x64 | Luna-48 review records two independent runs with SHA `60f551e06072b3fb7e814affa97f4a01e079c426d6044d3e710ad9a219ed907e`. | Byte-deterministic in reviewed runs; differs from historical. |
| CPython 3.11.4, Windows 10 x64 | Luna-49 made two independent materializations. Python build `d2340ef`, MSC v.1934, UCRT `10.0.19041.3636`; `core.autocrlf=true`; no external generation dependencies. Both runs SHA `60f551e06072b3fb7e814affa97f4a01e079c426d6044d3e710ad9a219ed907e`, semantic digest `2822c60d20569d82a220ef0de80813575f0b5adf240c611e011936cfb50a5876`. | Byte-, value-, and structurally deterministic across the two runs; differs from historical. |
| CPython 3.10, Windows | Luna-48 review reports matching nuisance inputs and first differing point compared with Python 3.11 Windows. A full fixture hash was not retained in the review finding. | First-point value observation only; full fixture determinism not established. |
| CPython 3.12, Windows; other Linux versions | No matching runtimes, WSL distribution, or Docker runtime were available. | Not established. |

The current Windows `libc_ver()` is empty. The current CRT file identity was
observed as `C:\WINDOWS\System32\ucrtbase.dll`, file version
`10.0.19041.3636`. Historical provenance records glibc 2.39 and GCC 13.3.0,
but not an exact libm binary/build identity. Point generation imports no
external packages; Python standard-library `random` and `math` plus repository
code are the relevant dependencies.

The two Luna-49 materialization records have distinct invocation IDs and
process IDs, and equal byte length (3,451,415), sequence/order digest, exact
coordinate-bit digest, file SHA, and semantic digest. Their source revision is
the pinned generator Git object above; the executed materializer source SHA-256
is recorded in `artifacts/luna49-runtime-reproducibility-20261008/current-runs/`.

## Numerical Origin

The first observable divergence remains `c00-000`, output point 3, field `x`:

| Field | Historical | Current | Absolute difference | Relative difference | ULP |
|---|---:|---:|---:|---:|---:|
| `x` | `0.16917642496961385` | `0.16917642496961388` | `2.7755575615628914e-17` | `1.6406290427649215e-16` | 1 |
| `y` | `-0.33382994490947676` | `-0.3338299449094767` | `5.551115123125783e-17` | `1.6628571546003924e-16` | 1 |
| `x+y` audit | `-0.1646535199398629` | `-0.16465351993986282` | `8.326672684688674e-17` | `5.0570875665032e-16` | 3 |

The exact historical/current hex values and packed binary64 bits, operands,
and current intermediate outputs are in the diagnostic JSON. For the current
runtime, the trace records angle `3.572409320972708`, radius
`0.23941996807196836`, `sin(angle)=-0.41761298601157304`,
`cos(angle)=-0.9086250018101514`, rotation `1.3013446012222407`,
`sin(rotation)=0.9639169935271708`, `cos(rotation)=0.2662029856886286`,
rotated pre-noise coordinates, Gaussian noise values, offset additions, and
the final serialized coordinates. The diagnostic reproduces the current
`x/y` exactly from those operations.

Historical trigonometric, rotation, and Gaussian-noise intermediates were not
retained. The final `x/y` values do not uniquely identify them, so the first
historical primitive that diverged cannot be proven from existing evidence.
The pinned spiral implementation uses `math.sin` and `math.cos` for point
generation. CPython `random.Random.gauss` also uses the standard-library
`_cos` and `_sin` operations to construct Gaussian noise, providing a second
possible libm-dependent path. The current and historical generator source
identities/operation order match; the parameters, sequence order, timestamps,
and counts match. Python 3.10 and 3.11 Windows agreement at the first known
point, plus the 3.11.4/3.11.5 Windows fixture-hash agreement, argue against a
Python-version-only explanation. They do not isolate the Windows CRT/libm from
Linux libm, Gaussian-noise trig, or compiler/runtime arithmetic.

Serialization is not supported as the origin: both decimal and exact `float.hex`
records faithfully encode the different generated binary64 values; the packed
bits differ before canonical comparison. No tolerance, rounding, or
canonicalization was introduced.

Across 5,164 points in the 3.11.4 Windows comparison:

- `x`: 219 differing points; maximum 128 ULP and absolute difference `4.440892098500626e-16`.
- `y`: 195 differing points; maximum 64 ULP and absolute difference `2.220446049250313e-16`.
- timestamps: 0 differing points.
- audit `x+y`: 231 differing points; maximum 256 ULP and absolute difference `4.440892098500626e-16`.

The full ULP histograms, per-field first differences, maximum relative
differences, source identities, runtime metadata, materialization hashes, and
operation trace are retained in
[`characterization.json`](../../artifacts/luna49-runtime-reproducibility-20261008/characterization.json).

## Structural and Decision Sensitivity

All 320 sequence IDs, point counts/order, point identities, batch ordinals,
and timestamps are equal; timestamps are bit-identical. The minimum positive
historical intra-sequence timestamp gap is `12.926386673536356`, while the
measured timestamp variation is zero. The input-order/timestamp/batch decision
is **EXACTLY IDENTICAL**, with no movement toward its positive-order boundary.

The canonical fixture identity gate changes, as expected: the Windows file
SHA and semantic digest do not equal the historical fixture identities. This
is a provenance rejection of the fresh fixture as a substitute, not evidence
that the historical fixture is invalid.

No fresh neural/route/threshold replay was performed. Retained downstream
files contain historical-fixture decisions only; computing counterpart
threshold crossings, routes, or Luna-46 categories would execute the excluded
scientific paths. The retained Luna-46 historical counts remain
212 `NO-RECEPTIONS`, 33 `TEMPORAL-RETENTION-LIMITED`, and 75 `DRIVE-LIMITED`;
their cross-runtime margins and category stability are **UNKNOWN**. No
scientific equivalence conclusion is made.

## Retained Gate Drift

The Luna-46 read-only catalog failure is a checkout-materialization invariant
failure, not corrupted evidence. The catalog Git blob SHA is exactly its
expected `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.
The Windows working copy has SHA
`5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80`, one extra
CRLF byte, and normalizing CRLF to LF reproduces the Git blob byte-for-byte.
The gate hashes checkout bytes as though they were canonical blob bytes.
No artifact or test was changed to hide this.

The Luna-47F read-only test fails at `retained input drift`; its later
protected-snapshot comparison is also stale. The retained snapshot has 995
protected entries, versus 999 at the pre-publication measurement, with 54
entry differences. They include the reviewed Luna-48 generator/verifier and
governance changes, later governance additions, and LF-to-CRLF materialization
of retained JSON inputs. The failure is **expected retained-artifact drift
after reviewed source changes, compounded by checkout materialization**. It
does not establish altered Luna-47 scientific evidence. Rebaseline, suppression,
or repair remains outside Luna-49; later governance should review the
protected-file scope and whether an additive retained snapshot is needed.

## Test Results and Classification

| Gate | Result |
|---|---|
| Luna-49 focused diagnostics | 7 passed |
| Luna-44 fixture/provenance/materialization | 60 passed, 2 failed |
| Luna-46 retained diagnostic | 165 passed, 1 failed, 1 skipped |
| Luna-47A-G retained focused suite | 306 passed, 1 failed |
| Historical/core and Luna-34 through Luna-45 regression | 676 passed, 2 failed |
| Full repository suite | 1,645 passed, 4 failed, 1 skipped |

The two Luna-44 failures are valid same-environment exactness invariants that
are not portable when run against the environment-pinned Linux fixture from
Windows. They are not obsolete and were not weakened. The two fresh Windows
materializations pass byte/value/structure equality with each other.

The additional Luna-46 failure is the raw checkout-byte versus Git-blob
invariant described above. The Luna-47F failure is retained input/snapshot
drift, not a new runtime scientific result. All four failures remain visible;
no red result is described as green.

## Disposition

- Fixture validity: **VALID AND ENVIRONMENT-PINNED**; no contradictory evidence.
- Exact numerical reproducibility: **BYTE-DETERMINISTIC within the two observed Windows runs and the two retained historical runs; not cross-environment byte-identical**.
- Exact historical-runtime reproduction: **NOT ESTABLISHED** in this execution because Python 3.12.3/Linux/glibc 2.39 was unavailable.
- Scientific reproducibility: **NOT ESTABLISHED** for downstream neural decisions; structural input order/timestamps are identical, while threshold/category margins remain unknown.
- Final disposition: **PASS WITH FOLLOW-UP**.

The bounded follow-up is the unavailable exact historical runtime and unknown
downstream discrete sensitivity. This execution does not establish efficacy,
mechanism usefulness, hardware equivalence, or architecture promotion. No
Luna-50 is authorized.

Required next step: **Luna-49 execution -> Luna-0 independent review**.