# Luna-71B-C4.2-J — Focused validation and regression disposition

**Disposition:** Synthetic and static checks only. This evidence does not
establish runtime parity or authorize a paired pilot.

## Source and fixture identities

| Item | Identity |
|---|---|
| J worktree HEAD/tree | `e91818a5c974282e848dc43e52d3c0a534dcbf45` / `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749` |
| J source manifest | 18,762 bytes; SHA-256 `605a730361da6252173d5466e11fa412ffdecca45c26ffabc31ca384b23d2ec0`; detached checksum file SHA-256 `5665d7b7c8ed617edc471b914ec65fb5da9e6e61467a1ad695505aaea3e2f6c0` |
| J implementation manifest | 1,822 bytes; SHA-256 `5625a596ed8a134de0fce0ebaa79eaae6749b9f6f4672f65d606d3d63326540e`; detached checksum file SHA-256 `4b3f6da15f8e69d6c4573e3643dac56c3afcc1c06230984fbbfeffc0db10e66c` |
| J v2 corrective provenance report | 28,655 bytes; SHA-256 `3ac6e6f3b57f21e208066757c6d3f671ae58326db7365d7e62f2303927168b13` |
| H source manifest | 20,446 bytes; SHA-256 `1c12a5f149d022f9e7a4304aa2b32f0110fc802f855d018bee32014580ae5095` |
| H GN artifact manifest | 37,135 bytes; SHA-256 `b2cf392f1d596b352e5af0add83c269c91fc1c0a19f701a9e54de4f41eb1ec16` |
| Fixture manifest | 2,368 bytes; SHA-256 `839e58df80da69cdf7b63618afc9626b85a9aa9817885931189c58a6f9658f40` |
| Fixture event payload | 39,796 bytes; SHA-256 `520b1cedfeefe8b285d02dba7d26583f6581ac29cd82dc8571a4b9ba5ed4970e` |
| Initial parameters | 112 bytes; SHA-256 `5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a` |

The J identity preflight and synthetic fixture checks passed. The C4.2-N
fixture is a new identity, not a historical R6 reproduction.

## Test results

| Suite and exact execution context | Result | Disposition |
|---|---:|---|
| `python -m unittest discover -s tests -p test_luna71b_c4_2_j.py -q` in the J worktree, final bounded run after all corrections | 35 passed in 314.847s | PASS; includes source-trigger-linked P03 settlement, fail-closed invalid references, P11 diagnostic type/range checks without parity gating, identity-bound fixture/exposure inputs, unsupported P03 coverage rejection, exact evidence callsites, process-control exception propagation, label isolation, and static passivity |
| `python -m unittest discover -s tests -p test_luna71b_c4_2_j.py -k source_P04 -k observer_only_source -v` in J | 2 passed (intermediate run) | PASS; both J source variants use pending prediction/lineage evidence without false P04 gaps; actual P03 and route/admission gaps remain fail-closed |
| `python -m unittest discover -s tests -p test_luna71b_c4_2_gn.py -v` in detached J | 1 setup error; 0 tests ran | BLOCKED in this checkout: GN preflight rejects the detached branch because it requires its explicitly authorized H branch |
| Same GN suite in preserved H worktree at authorized branch `governance/luna71b-c4-2-h-corrections`, HEAD `e91818a5c974282e848dc43e52d3c0a534dcbf45` | 14 passed | PASS; includes preflight, fixture/manifest, static source-hook passivity, and no-neural-import checks |
| `python -m pytest -q tests\test_luna71b_c4_2.py` in J worktree | 31 passed; 3 failed at preflight; 13 subtests passed | 3 BLOCKED; no expected identities changed |

The three blocked C4.2 tests and their shared prerequisite failure are:

1. `test_driver_fails_closed_before_calling_execution_adapter` expected to
   reach the fixture-payload-manifest guard, but preflight stopped first with
   `frozen pilot plan is missing`.
2. `test_driver_rejects_mismatched_implementation_identity` expected the
   implementation-identity mismatch, but preflight stopped first with
   `frozen pilot plan is missing`.
3. `test_driver_rejects_mismatched_source_identity` expected the
   source-identity mismatch, but preflight stopped first with
   `frozen pilot plan is missing`.

These are recorded as blocked, not passes: the frozen pilot plan is absent
from the verified C4.2 checkout. Tests and expected hashes were not modified
to mask the prerequisite. The separate GN attempt in J is also retained as a
blocked result rather than silently replaced by the authorized H-baseline
run. The final GN attempt in J reported one `setUpClass` error and zero tests
because of the detached-branch identity gate; the authorized H-baseline run
passed all 14 tests.

A prior non-final concurrent invocation of two J test processes collided on
their shared temporary trace directory. Final bounded tests were run serially
and passed. The last 32-test run preserves a pre-existing test-artifact
directory if present (none was present); its teardown removes only artifacts
created by that run. No test was excluded.

## Scope and validation limits

- Synthetic tests and static inspection only; no fixture was run through the
  neural runner.
- No training, inference, neural dynamics, or paired-pilot execution occurred.
- Static passivity checks do not prove runtime passivity or neural parity.
- P03 settlement references are now required to link backward to a matching
  source-observed match/expiry record. Where the source emits settlement before
  an observable trigger, capture emits a gap and P03 remains incomplete.
- P11 operation/failure diagnostics are structurally typed and range-checked
  but remain non-gating for parity.
- The unavailable historical source-manifest preimage beginning `43fb…` and
  test-index preimage beginning `0ad1…` remain unresolved; the new fixture
  does not substitute for either.
- The capture package now has an injected v2 pair harness, but no real-source
  pair/backend was run. P03 remains incomplete where the source lacks a
  settlement path; P04 remains incomplete on actual anomalous route/admission
  branches whose evidence is unavailable. Thus no static PPC-11 readiness or
  RP-2B readiness is claimed.
