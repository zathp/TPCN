# Luna-48 — Canonical Fixture Materialization Provenance Correction

## Role

Correct the Luna-44 independent materialization path so that a pinned source
checkout is compared using its canonical Git-blob bytes (or an explicitly
equivalent LF materialization) on Windows and other supported environments.
This is a provenance/infrastructure correction only.

## Authorized scope

- Inspect and minimally correct `scripts/build_luna44_canonical_fixture.py`,
  its focused tests, and directly related provenance documentation.
- Preserve the pinned source revision
  `a79494cd66be28fd291ed11eddd62d342f457cfd`.
- Preserve the committed fixture bytes, semantic fixture digest, generation
  parameters, source identities, and acceptance criteria.
- Add deterministic tests that distinguish Git-blob identity, checkout
  materialization, generator semantics, and generated fixture identity.
- Re-run the Luna-44 canonical fixture gates and relevant historical
  compatibility tests on the actual supported checkout.

## Explicit exclusions

- Do not modify the canonical fixture to make a test pass.
- Do not change source revisions, pinned hashes, generation parameters,
  newline policy in the committed artifact, or fixture identity.
- Do not change TPCN architecture, neuron/runtime behavior, ACP status, or
  scientific hypotheses.
- Do not compose Luna-47A–G mechanisms.
- Do not execute a causal mechanism experiment or authorize Luna-49.
- Do not interpret this correction as evidence for Luna-48 scientific efficacy.

## Required invariants

1. The four manifest source identities must continue to match their declared
   Git objects and SHA-256 values.
2. The canonical fixture file and semantic digest must remain byte-for-byte
   unchanged.
3. Two independent materializations must agree in fixture bytes, binary64
   values, ordering, and semantic digest.
4. A CRLF checkout must not be silently hashed as if it were the canonical
   LF Git blob.
5. Source-text identity, generator semantic identity, fixture-byte identity,
   fixture semantic identity, and environment identity must remain distinct.
6. Missing, altered, or unverified source identity must fail loudly.

## Acceptance checks

- `tests/test_luna44_canonical_fixture.py`
- `tests/test_luna44_canonical_fixture_verification.py`
- `tests/test_luna44_acp0008_canonical_fixture_rebaseline.py`
- `tests/test_luna46_depth_scaling_diagnostic.py`
- Applicable full-suite regression, with exact failures retained if unrelated.
- Clean worktree, exact source/fixture hashes, and replayable provenance output.

The Luna-0 Architecture Guardian reviews the correction before any separate
causal question is considered. This contract does not authorize execution of
any Luna-47 mechanism or successor scientific experiment.
