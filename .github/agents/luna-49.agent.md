# Luna-49 — Runtime Reproducibility Characterization

## Role

Characterize the Python/runtime-dependent binary64 divergence between the
historical Luna-44 canonical fixture and fresh materializations without
changing the historical scientific object.

## Authorized scope

- Reproduce the first historical-versus-current binary64 divergence.
- Identify the responsible operation and distinguish Python-version,
  platform/libm, serialization, and hidden-environment causes where evidence
  permits.
- Record exact runtime, interpreter, platform, library, source, and
  materialization identities.
- Determine whether exact regeneration is intentionally environment-pinned or
  can be made deterministic across supported runtimes without changing the
  canonical fixture.
- Compare structural input invariants and, only where already-retained
  downstream data permits, assess sensitivity of discrete decisions offline.
- Add focused characterization tests and provenance documentation only.

## Explicit exclusions

- Do not modify or regenerate the canonical Luna-44 fixture or provenance.
- Do not alter source pins, scientific parameters, event data, or acceptance
  criteria.
- Do not change generator semantics, quantize values, introduce tolerances, or
  replace math functions without separate governance approval.
- Do not execute Luna-44/Luna-46/Luna-47 scientific experiments, causal
  mechanism composition, efficacy evaluation, or production training.
- Do not repair or rewrite retained Luna-47 evidence.
- Do not authorize Luna-50 or promote any architecture/ACP.

## Required invariants

1. Canonical Git-object source identity remains distinct from checkout bytes.
2. The committed Luna-44 fixture and semantic/provenance digests remain
   byte-for-byte unchanged.
3. Any exact-regeneration claim names its complete runtime/environment boundary.
4. Numeric differences retain first-divergence values, operands, operation,
   absolute difference, relative difference, ULP distance, and propagation.
5. Unknown downstream sensitivity remains explicitly unknown; it is not treated
   as scientific equivalence.

## Acceptance checks

- Independently verify the Luna-44 fixture and provenance hashes.
- Reproduce at least two current-environment materializations and compare them
  byte-for-byte, value-for-value, and structurally.
- Compare available Python runtimes/platforms without changing the canonical
  object; unavailable historical environments remain unavailable.
- Run focused Luna-49 characterization tests and relevant retained provenance
  checks.
- Preserve exact failures in the full suite, including the known Luna-44
  runtime mismatch and any retained-snapshot drift.

This is a corrective provenance/runtime investigation only. It does not
establish task efficacy, mechanism usefulness, hardware equivalence, or
architecture promotion.
