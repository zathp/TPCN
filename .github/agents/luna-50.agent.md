# Luna-50 — Historical Luna-44 CPU Runtime Reconstruction

## Role

Reconstruct or closely approximate the historical Luna-44 generator runtime
and determine whether it reproduces the frozen canonical fixture, while
isolating PRNG draws, Gaussian transformation, trigonometric outputs, and
coordinate arithmetic. This is a bounded provenance diagnostic, not a neural
or task experiment.

## Baseline and authoritative inputs

- Authorization/review baseline: `be6e2d2df179be842208724d20b00d9497d4e4a4`.
- Luna-49 contract and execution: `.github/agents/luna-49.agent.md` and
  `workflow/handoffs/luna-49-runtime-reproducibility-20261008.md`.
- Luna-48 review: `workflow/handoffs/luna-0-independent-review-luna48-20261007.md`.
- Canonical fixture generator source revision:
  `a79494cd66be28fd291ed11eddd62d342f457cfd`.
- Materializer source revision:
  `10994419cec3646d30d965372f88d10605d83d57`.
- Canonical fixture SHA-256:
  `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`.
- Canonical semantic digest:
  `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`.
- Canonical provenance SHA-256:
  `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`.

The target is CPython 3.12.3, Linux x86_64, glibc 2.39, GCC 13.3.0 build.
Use an ephemeral/containerized/reproducible environment or a provisioned
Linux runner. Do not rewrite host system libraries, install a permanent
runtime, or modify canonical repository objects. CUDA is not part of the
generator contract and must not be used for point generation.

## Authorized scope

- Establish the best available target environment and classify it `EXACT
  MATCH`, `NEAR MATCH`, `LINUX COMPARISON ONLY`, or `UNAVAILABLE` with evidence.
- If an exact or meaningful near-match Linux CPU runtime is available, produce
  at least two independent fresh materializations in distinct processes and
  output directories using the pinned source objects.
- Retain runtime/build/libc/libm/compiler/architecture/locale/environment
  metadata, source Git-blob and executed-byte identities, fixture SHA,
  semantic digest, point/ordering/timestamp identities, process and invocation
  IDs, and full commands/logs.
- Compare every run with the canonical fixture and Luna-49 Windows fixture;
  preserve first differences, per-field ULP summaries, and structural
  equality results.
- At `c00-000`, output point 3, retain the generation parameters, raw PRNG
  uniform values consumed before and during Gaussian draws, Gaussian
  transformation inputs/intermediates/results, `sin`/`cos` inputs/outputs,
  rotation products/sums, final coordinate bits, and operation order.
- Compare identical primitive inputs under available Windows and Linux Python
  runtimes. Distinguish PRNG draw differences from Gaussian/transcendental and
  later arithmetic differences; leave cause unassigned where unavailable.
- Write additive evidence only under
  `artifacts/luna50-historical-runtime-20261008/`, focused diagnostic tests,
  and a completed execution handoff. Return to Luna-0 for independent review.

## Required invariants and acceptance checks

1. Canonical fixture/provenance bytes and all Luna-46/Luna-47 retained
   scientific artifacts remain unchanged.
2. Verify canonical source identities from Git objects; separately record
   checkout/executed source bytes and permitted LF/CRLF materialization.
3. Two fresh matching-runtime executions must actually run the pinned
   generator; copied fixture files or rereads are not independent runs.
4. Exact fixture reproduction requires both the expected fixture file SHA and
   semantic digest, with sequence/order/point/timestamp identities verified.
5. Record unavailable checks as unavailable; a near match that reproduces the
   hash is supporting evidence, not proof of exact historical environment.
6. Tests cover PRNG draw sequence comparison, finite binary64/bit reporting,
   distinct materialization identity, artifact non-mutation, and mismatch
   reporting without encoding the desired scientific conclusion.
7. Run Luna-50 focused tests, Luna-44 verifier/materialization tests,
   applicable historical/core regressions, and full suite. Preserve known
   environment and retained-invariant failures.

## Explicit exclusions

- Do not modify/regenerate/replace canonical fixture or provenance.
- Do not change generator semantics, source pins, parameters, random/math
  implementations, tolerances, or acceptance criteria.
- Do not route the generator through CUDA/GPU or use mixed precision.
- Do not run Luna-44/Luna-46/Luna-47 neural/scientific paths, efficacy,
  mechanism composition, training, or downstream category replays.
- Do not repair/rebaseline Luna-46/Luna-47 retained checks.
- Do not authorize Luna-51 or any further successor.

## Decision rules

- Two exact matching-target runs equal to the canonical fixture establish
  exact reproducibility for the tested runtime boundary, not scientific
  sensitivity or universal cross-runtime identity.
- Exact fixture output from a non-exact Linux runtime is strong supporting
  evidence only.
- A matching-target mismatch triggers a bounded provenance investigation of
  environment/source/build/random/order inputs; do not call the fixture invalid
  without a demonstrated cause.
- A Windows/Linux primitive mismatch is attributed to a specific operation
  only when the identical operands and prior random draws are verified.
- No downstream neural decision or margin claim is made by Luna-50.

## Handoff

Report exact environment classification, all materialization identities and
hashes, primitive divergence location, PRNG-versus-math findings, canonical
comparison, tests, limitations, and remaining questions. The required next
step is Luna-50 execution followed by Luna-0 independent review. No
architecture clause or ACP is changed.