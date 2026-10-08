---
tpcn_handoff:
  agent: "Luna-50 Historical Runtime Reconstruction"
  luna_identifier: "Luna-50"
  descriptive_name: "Historical Luna-44 CPU runtime reconstruction and primitive diagnostics"
  task_id: "luna-50-historical-runtime-reconstruction-20261008"
  component: "Generator runtime provenance; CPU-only diagnostic"
  status: "BLOCKED — HISTORICAL RUNTIME UNAVAILABLE"
  contract_version: "1.2"
  branch: "main"
  base_revision: "b49f6642957ea630598b576c3c57f8862e436a14"
  result_revision: "published commit containing this handoff"
  dependencies:
    - "Luna-50 authorization contract committed at b49f6642957ea630598b576c3c57f8862e436a14"
    - "Luna-49 execution baseline named in the contract: be6e2d2df179be842208724d20b00d9497d4e4a4"
    - "Canonical generator source a79494cd66be28fd291ed11eddd62d342f457cfd"
    - "Canonical materializer source 10994419cec3646d30d965372f88d10605d83d57"
  owner: "Project owner; Luna-0 independent review"
  classification:
    - "UNAVAILABLE: historical Linux runtime could not be provisioned"
    - "Windows CPython 3.11.4 control only; not a Linux near-match"
    - "no two-run fixture materialization"
    - "no scientific or neural execution"
  hypothesis: "If the exact historical Linux runtime is unavailable, only a Windows primitive control can be retained and the historical first-divergence cause remains unassigned."
  counter_hypothesis: "An exact or meaningful Linux CPU runtime could support independent fresh materializations and identical-operand primitive comparison; none was accessible here."
  interfaces_relied_on:
    - ".github/agents/luna-50.agent.md"
    - "workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md"
    - "scripts/verify_luna44_canonical_fixture.py"
    - "scripts/luna50_primitive_diagnostic.py"
    - "artifacts/luna44-canonical-fixture/fixture.json and provenance.json"
    - "Luna-49 current Windows characterization and historical review records"
  label_information_boundary:
    - "No labels, neural outcomes, or downstream categories were read into computation."
  timing_assumptions:
    - "Only generator point timestamp bits for c00-000 output point 3 were compared."
  reset_boundaries:
    - "The diagnostic uses the pinned generator's local Random seed and reproduces only one selected training sequence point; it does not invoke the fixture materializer."
  resource_bounds:
    - "CPU-only Windows control; CUDA not used."
    - "No runtime, dependencies, WSL distribution, container engine, or host libraries installed or modified."
  authorized_scope:
    - "Verify canonical identities and source Git objects."
    - "Add a portable primitive diagnostic and focused tests."
    - "Capture an explicitly partial Windows control and record historical unavailability."
    - "Write additive evidence only under artifacts/luna50-historical-runtime-20261008/."
    - "Update this handoff and the two authorized workflow records."
  unauthorized_scope:
    - "No canonical fixture/provenance edits or regeneration."
    - "No Luna-46/Luna-47 retained artifact edits or repairs."
    - "No generator semantics, pins, parameters, math/random implementations, or criteria changes."
    - "No CUDA/GPU generation, neural/scientific replay, ACP/architecture change, or Luna-51 authorization."
  controls:
    - "Verified exact starting HEAD and origin/main b49f6642957ea630598b576c3c57f8862e436a14 with clean worktree."
    - "Recorded separately that the contract baseline field is be6e2d2df179be842208724d20b00d9497d4e4a4; it is not the mandatory Luna-50 starting revision."
    - "WSL exposed only its installer/help stub; Docker and Podman were absent; no Linux endpoint or credentials were supplied."
    - "Canonical fixture/provenance SHA-256 and pinned generator/materializer Git blobs verified before and after."
    - "No canonical or Luna-46/Luna-47 retained file was modified."
  measurements:
    - "Windows runtime, OS, compiler/build, architecture, libc/libm lookup, locale, selected environment variables, process/invocation identity, and source byte identities retained in the JSON artifact."
    - "Windows c00-000 point 3 trace records 20 raw MT uniforms, target Gaussian transforms/cache, trig inputs/outputs, arithmetic order, final bits, and JSON numeric round trip."
    - "Historical final x/y/t comparison is retained; historical intermediate values and Linux primitive comparison are unavailable."
    - "Two independent historical-runtime materializations: NOT RUN."
  information_boundary_check:
    - "PASS: no labels, neural paths, training, or downstream scientific evaluation."
  hardware_mapping:
    - "Windows x64 CPU control only; CUDA NOT USED."
    - "Target Linux x86_64/CPython 3.12.3/glibc 2.39/GCC 13.3.0: UNAVAILABLE."
  architecture_invariants_touched:
    - "No A01-A15 clause or ACP changed."
  preserves:
    - "Canonical fixture SHA-256 66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629."
    - "Canonical semantic digest 6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305."
    - "Canonical provenance SHA-256 6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22."
    - "All Luna-46/Luna-47 retained scientific artifacts and known red checks."
  architecture_change: false
  proposal: null
  files_changed:
    - "scripts/luna50_primitive_diagnostic.py"
    - "tests/test_luna50_primitive_diagnostic.py"
    - "artifacts/luna50-historical-runtime-20261008/windows-control.json"
    - "workflow/handoffs/luna-50-historical-runtime-reconstruction-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "Six tests for MT draws, Gaussian transform/cache, finite binary64 bits, independent identity, mismatch reporting, and canonical artifact non-mutation."
  tests_passing:
    - "Luna-50 focused: 6 passed."
    - "Luna-49 focused: 7 passed; combined diagnostic selection: 13 passed."
    - "Luna-44 standalone verifier: exit 0."
  tests_failed:
    - "Luna-44 fixture/provenance/materialization files: 17 passed, 2 failed; Windows output differs from frozen historical fixture and semantic digest."
    - "Luna-46 focused: 165 passed, 1 failed, 1 skipped; raw checkout bytes fail the pinned catalog Git-blob SHA invariant."
    - "Luna-47A-G focused: 306 passed, 1 failed; retained replay detects stale input inventory."
    - "Historical/core regression selection: 350 passed, 2 failed; the two known Luna-44 cross-runtime comparisons."
    - "Full repository suite: 1651 passed, 4 failed, 1 skipped; exactly the two Luna-44, Luna-46 checkout-byte, and Luna-47F stale-inventory failures."
  tests_not_run:
    - "Exact/near-match Linux target provisioning and two independent pinned-source fixture materializations: unavailable; not run."
    - "Windows/Linux identical-operand primitive comparison: unavailable."
    - "Luna-44 materializer CLI was not run as a Luna-50 materialization; existing tests invoke temporary Windows materializations only."
  assumptions:
    - "The recorded historical fixture final bits are authoritative retained observations; they do not determine unique historical intermediates."
    - "A one-ULP coordinate difference is not assigned to libm, Gaussian conversion, or arithmetic without identical Linux operands and prior draws."
  unresolved:
    - "Historical runtime reproduction, two-run Linux materialization, and first primitive divergence remain unresolved."
    - "The existing Luna-46 checkout-byte and Luna-47F retained-snapshot failures remain outside Luna-50 scope."
  recommended_next_agent:
    - "Luna-0 independent review of this bounded blocked execution; no successor is authorized."
---

# Luna-50 Historical Runtime Reconstruction

## Disposition

**BLOCKED — HISTORICAL RUNTIME UNAVAILABLE.** The mandatory execution started
from authorization revision `b49f6642957ea630598b576c3c57f8862e436a14`, where
`HEAD == origin/main` and the worktree was clean. The `be6e2d2df179be842208724d20b00d9497d4e4a4`
value in the contract is the Luna-49 execution baseline field, not Luna-50's
starting revision or authorization SHA.

## Environment And Provenance

**OBSERVED:** The available host is Windows 10 build 19045 x64 with CPython
3.11.4, MSC v.1934. `platform.libc_ver()` and `find_library("m")` returned no
library identity. WSL returned only its installer/help stub; Docker and Podman
were absent. No remote Linux endpoint or credentials were provided. No host
runtime, dependency, system library, or WSL installation was attempted.
Classification is **UNAVAILABLE**, not exact, near, or Linux-only comparison.
CUDA was not used.

Canonical fixture/provenance identities were verified before and after:

- Fixture SHA-256: `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`.
- Semantic digest: `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`.
- Provenance SHA-256: `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`.

The pinned generator Git-object SHA-256 values match the provenance manifest:
sequence builder `17e581cf702fae1f56889472a967d2e8e5fec37cc041edba8247da14a0a8b5db`,
point generator `2ffb1b5ebb23f016436043118bc675eddaa14bfd923129359fe61a12df94d9f0`,
and point representation `daca268597e2467bf984922ee77736b584bef9743b6f41ad729d7cb4d3c3ede7`.
The pinned materializer Git-object SHA-256 is
`696051cc3690aafc9f342e569697469a111757c37c2666b0c026333e6b16efce`. Blob
IDs and checkout/executed source-byte identities, including LF/CRLF status,
are recorded in the JSON evidence. The point generator and Luna-50 diagnostic
source bytes were executed for the bounded control. The sequence builder and
materializer were not invoked for fresh materializations; the current
materializer checkout differs from its pinned blob and is explicitly not
claimed as executed source.

## Windows Control

The command
`python scripts/luna50_primitive_diagnostic.py --output artifacts/luna50-historical-runtime-20261008/windows-control.json`
generated only the bounded Windows control, not a fixture materialization.
The final retained report has invocation `80a6cec7330c40b6b9e949761fd15417`,
process 19004, selected environment/locale and runtime data, exact binary64 strings
and bits, all 20 raw uniform values through point 3, Gaussian transform
inputs/intermediates/results and cache state, trig inputs/outputs, ordered
coordinate products/sums, final coordinate bits, and JSON numeric
serialization round trips. The reconstructed Windows point matches its
generator output bit-for-bit.

Against the retained historical final point at `c00-000`, output point 3:

| Field | Historical | Windows control | Result |
|---|---|---|---|
| `x` | `0.16917642496961385`, `3fc5a792b63fd50d` | `0.16917642496961388`, `3fc5a792b63fd50e` | 1 ULP |
| `y` | `-0.33382994490947676`, `bfd55d7845f3f2a3` | `-0.3338299449094767`, `bfd55d7845f3f2a2` | 1 ULP |
| `t` | `81.33339605974454`, `405455565c6d4df5` | `81.33339605974454`, `405455565c6d4df5` | bit-identical |

**OBSERVED:** The Windows x Gaussian call consumes two raw uniforms and the
following y call consumes the cached Gaussian value. **NOT AVAILABLE:** no
historical intermediate operands/results or Linux runtime were available for
the identical-input comparison. PRNG-versus-math divergence and the first
historical primitive cause therefore remain **UNASSIGNED**; no libm cause is
asserted. The canonical fixture contains final bits only and cannot uniquely
recover its old intermediates.

Evidence file: `artifacts/luna50-historical-runtime-20261008/windows-control.json`;
SHA-256 `3ddd9205112c153db4d98c49e5c2dbeb9c4e9bba19b75c66adc99b8e30696497`,
33,944 bytes.
The JSON record includes exact before/after canonical hashes and source
identities. Two fresh matching-runtime materializations are **NOT RUN**.

## Validation Record

Environment for commands: CPython 3.11.4 / Windows 10 x64, from authorization
revision `b49f6642957ea630598b576c3c57f8862e436a14`, plus only the additive
Luna-50 changes described here. Commands and observed counts:

| Command | Result |
|---|---|
| `python -m pytest tests/test_luna50_primitive_diagnostic.py -q` | 6 passed, exit 0 |
| `python -m pytest tests/test_luna49_runtime_characterization.py -q` | 7 passed, exit 0 |
| `python -m pytest tests/test_luna50_primitive_diagnostic.py tests/test_luna49_runtime_characterization.py -q` | 13 passed, exit 0 |
| `python scripts/verify_luna44_canonical_fixture.py` | PASS, exit 0 |
| `python -m pytest tests/test_luna44_canonical_fixture.py tests/test_luna44_canonical_fixture_verification.py -q -rs` | 17 passed, 2 failed, exit 1 |
| `python -m pytest tests/test_luna46_depth_scaling_diagnostic.py -q -rs` | 165 passed, 1 failed, 1 skipped, exit 1 |
| Luna-47A-G eight-file focused pytest selection, `-q -rs` | 306 passed, 1 failed, exit 1 |
| Established historical/core and Luna-34 through Luna-45 selection, `-q -rs` | 350 passed, 2 failed, exit 1 |
| `python -m pytest -q -rs` | 1,651 passed, 4 failed, 1 skipped, exit 1 |

The full-suite failures are exactly the two known Luna-44 Windows-versus-frozen
fixture comparisons, the Luna-46 raw checkout-byte catalog hash, and the
Luna-47F stale retained input inventory. The single Luna-46 skip is the
Windows directory-symlink privilege check. No failure was suppressed or
repaired; no errors were reported. The Luna-50 focused checks pass.

## Scope And Next Step

No two-run materialization, Linux runtime comparison, CUDA generation,
scientific/neural path, canonical artifact write, Luna-46/Luna-47 repair,
architecture clause, ACP, or successor authorization occurred. The
Luna-44-verifier/materialization tests above run as required regression
validation only; their temporary Windows materializations are not Luna-50
historical-runtime runs.

**Next:** return to Luna-0 for independent review of this blocked execution.
No Luna-51 is authorized. No architecture clause or ACP is changed.