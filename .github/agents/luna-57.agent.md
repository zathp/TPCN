---
name: Luna-57 ACP-0008 Provenance Materialization Correction
description: Correct only the three reproduced Luna-55 checkout-materialization provenance test failures.
---

# Luna-57 — Luna-55 Checkout-Materialization Provenance Correction

## Authorization

**AUTHORIZED / NOT EXECUTED.** Execute only after this contract is published on
`origin/main`. This is a bounded test/provenance correction, not a scientific
experiment, architecture change, ACP revision, or authorization to regenerate
evidence. Preserve the accepted Luna-55 result and every historical identity.

Baseline authorization: `a5d145d6751ee82a5fae1e2f8ad2f647d06438bc`.
Read the current architecture contract, workflow, changelog, acceptance
criteria, handoff template, this contract, and the Luna-0 authorization
handoff before editing.

## Finding and scope

The three failing nodes listed below are all representation-check defects:
they compare a current checkout's raw SHA or length to a SHA/length recorded
for a different, explicitly permitted line-ending materialization, after (or
instead of) authenticating the immutable Git object. The exact historical Git
objects, permitted materializations, integrity metadata, and Luna-55
scientific artifacts were verified unchanged at authorization time.

Authorized implementation ownership is limited to:

- `experiments/luna55/run.py`
- `tests/test_luna55_factorial.py`
- One Luna-57 execution handoff under `workflow/handoffs/`

Do not edit selected/published scientific artifacts, source data, configurations,
frozen selection membership, hash/blob/revision literals, `.gitattributes`,
other runners/tests, or the Luna-55 summary/results/catalog. Do not inspect
the six existing noncrossing target streams or alter their interpretation.

## Required correction

1. Preserve fixed revision and Git-blob authentication as the authority for
   each of the eight Luna-55 retained phase inputs. Do not substitute a
   checkout-derived identity for the pinned object.
2. Accept a current checkout only when its bytes are exactly the authenticated
   Git object or exactly that object's LF-to-CRLF materialization. Do not use
   broad newline normalization as the acceptance test. Continue verifying
   phase identity, schema, execution revision, artifact digest, and all
   scientific/selection pins.
3. Treat the selection's recorded `checkout_sha256` as historical materialized
   checkout metadata, not as a requirement that every later checkout have
   identical bytes. Verify that the stored digest describes one of the exact
   permitted materializations, independently of the current checkout.
4. For the Luna-46 helper pin, keep the fixed blob
   `9506369d97babf7bc0ef15ed52efb738dcdcd549`, verify the current bytes are
   exactly LF or exact CRLF for that object, and establish that the legacy
   helper hash/length (`0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e`,
   `2337377`) identifies one of those exact forms. Preserve the embedded
   semantic-digest check and restoration of any temporarily adapted helper
   state. Do not require the legacy hash to differ from the current checkout
   hash: equality is valid when both represent the same exact CRLF bytes.
5. Do not change any historical hash, blob, revision, artifact, or scientific
   result to make a comparison pass.

## Required regression evidence

The following three existing nodes must pass without invoking a scientific
runner:

- `tests/test_luna55_factorial.py::test_luna55_retained_phase_pins_and_population_partition`
- `tests/test_luna55_factorial.py::test_luna55_reauthenticates_stale_luna46_file_pin_without_mutating_history`
- `tests/test_luna55_factorial.py::test_composed_rr_preserves_relay_route_identity_from_rh`

Run the complete `tests/test_luna55_factorial.py` module and the repository
test suite. Add bounded tests demonstrating that exact LF and exact CRLF
materializations are accepted, while changed content, mixed/non-CRLF carriage
returns, a wrong blob/revision, and a missing Git object are rejected. Record
any host-capability skip accurately; the authorization baseline's symlink
skip was Windows `WinError 1314`, while its CUDA test passed.

Permitted validation is regression/unit testing only. Do not invoke
`experiments/luna55/run.py`, `run_phase`, `summarize`, any scientific replay,
parameter sweep, or artifact-generation command. Confirm protected inputs and
published Luna-55 outputs remain byte/object-identical after tests.

## Architecture and stop boundary

No A01–A15 clause changes; no ACP is required. Preserve event computation,
causal experiment interpretation, label isolation, and all accepted historical
results. This correction does not close Luna-55's scientific limitations or
authorize a scientific successor.

After implementation, tests, and the execution handoff are complete, stop for
an independent Luna-0 review. Do not authorize or begin Luna-58 or any
scientific work.
