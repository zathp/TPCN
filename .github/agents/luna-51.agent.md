# Luna-51 — Historical Evidence Identity Regression Correction

## Status

**AUTHORIZED / NOT EXECUTED** by Luna-0 governance decision published from
`da67433220d92d926d4c4e84e5b9fa08cda4bb10`. The authorization SHA is the
commit that adds this contract and the linked Luna-0 handoff.

## Role and objective

Correct only the provenance/test invariants responsible for the four known
repository-suite failures: the two Luna-44 alternate-runtime exact comparisons,
the Luna-46 catalog checkout-byte hash, and the Luna-47F retained inventory
failure. The shared rule is that authenticated historical evidence identity
must not be confused with platform-dependent checkout bytes or unrelated later
repository evolution.

This is a test/provenance correction, not a scientific experiment. Preserve
all historic results and make no claim about efficacy or cross-runtime
scientific sensitivity.

## Baseline and authoritative inputs

- Starting revision: `da67433220d92d926d4c4e84e5b9fa08cda4bb10`.
- Luna-50 authorization: `b49f6642957ea630598b576c3c57f8862e436a14`.
- Luna-50 execution: `da67433220d92d926d4c4e84e5b9fa08cda4bb10`.
- Luna-50 execution handoff: `workflow/handoffs/luna-50-historical-runtime-reconstruction-20261008.md`.
- Luna-0 review and authorization handoff: `workflow/handoffs/luna-0-independent-review-luna50-and-authorization-luna51-20261008.md`.
- Luna-44 canonical fixture/provenance and pinned Git-object source records.
- Luna-46 corrective diagnostic and its pinned Luna-45 catalog.
- Luna-47F protocol, diagnostic, retained result, validation record and tests.
- `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, and `workflow/docs/luna/LUNA_WORKFLOW.md`.

## Authorized ownership

Only the following implementation/test surfaces may be changed as necessary:

- `scripts/build_luna44_canonical_fixture.py` and Luna-44 fixture/provenance tests.
- `run_luna46_depth_scaling_diagnostic.py` and `tests/test_luna46_depth_scaling_diagnostic.py`.
- `experiments/luna47f/diagnostic.py`, `tests/test_luna47f_diagnostic.py`, and `tests/test_luna47f_retained.py`.
- A Luna-51 execution handoff and the corresponding current entries in `workflow/docs/luna/LUNA_WORKFLOW.md` and `workflow/ARCHITECTURE_CHANGELOG.md`.

No edits to historical Luna-44/Luna-46/Luna-47 handoffs, protocols, source
pins, scientific result files, or retained result JSON are authorized.

## Required invariant corrections

### Luna-44 runtime-aware materialization

- Keep the committed fixture and provenance file hashes, semantic digest,
  source Git-object identities, configuration, ordering and exact binary64
  values strictly verified.
- Keep the two-fresh-process same-environment comparison exact for bytes,
  point bits, structure, ordering and semantic digest.
- Compare fresh materialization output to the canonical fixture exactly only
  when the recorded runtime is demonstrated to match the declared canonical
  generation runtime. On other runtimes, report deterministic alternate-runtime
  divergence as diagnostic evidence; do not classify it as canonical artifact
  mutation or a failed same-runtime determinism check.
- Do not weaken canonical artifact verification, use tolerances for canonical
  bits, or change generator parameters/source pins.

### Luna-46 catalog identity

- Authenticate the retained catalog using its pinned baseline Git object and
  Git-blob identity where repository identity is intended.
- Handle checkout bytes separately. Permit only the specifically verified
  exact LF/CRLF materialization transformation; do not apply blanket newline
  normalization to arbitrary inputs.
- Continue validating parsed content, internal digest, file inventory,
  per-file byte/content pins, provenance pins and retained scientific output.
- A substantive byte/content change, wrong source revision/blob, or changed
  catalog entry must still fail.

### Luna-47F retained identity and live non-mutation

- Replace the historical whole-repository snapshot comparison with a bounded
  manifest of only the inputs and source that define the Luna-47F execution:
  its consumed Luna-45 files, canonical Luna-44 fixture/provenance, consumed
  Luna-46 result, Luna-47F code/protocol/configuration and retained result.
- Compare stable historical identities (baseline Git blob/source revision,
  exact permitted checkout materialization, canonical content/artifact
  digests), not the current hashes of unrelated tracked files.
- Retain a separate fresh pre/post observation during each check invocation
  to detect writes made by that invocation. Do not compare the old all-repo
  pre-snapshot against the modern repository.
- Preserve the existing retained analysis and result bytes. Do not regenerate
  or rebaseline `artifacts/luna47f/diagnostic.json` or its validation record.

## Required adversarial tests

Tests must demonstrate that the corrected guards reject:

- a substantive mutation to protected historical source;
- a wrong pinned source revision or Git blob;
- altered consumed scientific input or unauthorized fixture substitution;
- altered protocol/configuration;
- altered retained result or internal digest.

Tests must also demonstrate that they accept only the governed irrelevant
variations:

- exact LF/CRLF checkout transformation where applicable;
- later unrelated governance-file changes;
- reviewed unrelated source/repository evolution outside the historical
  consumed-input set;
- alternate-runtime Luna-44 materialization that is internally valid and
  repeatable but not bit-identical to the canonical Linux fixture.

Tests must not be tautological or merely restate helper outputs. Preserve
canonical hashes and run at least one mutation through the public verification
path for each protected evidence class.

## Forbidden actions

- Do not modify, regenerate, normalize, replace or rebaseline the canonical
  Luna-44 fixture or provenance.
- Do not modify, rebaseline, weaken or replace Luna-46/Luna-47 scientific
  artifacts or retained Luna-47F output.
- Do not change scientific hypotheses, configurations, generator parameters,
  source pins, analysis outputs, verdicts, thresholds or tolerance policies.
- Do not run Luna-44, Luna-46, Luna-47, or any other neural/scientific replay,
  training, mechanism, efficacy, route, threshold or sensitivity experiment.
- Do not skip, xfail, delete, broadly relax or hide failing tests; do not use
  blanket newline normalization or bless current repository snapshots as new
  historical truth.
- Do not provision or install a historical runtime, use CUDA, change A01-A15,
  propose an ACP, claim hardware equivalence, or authorize Luna-52.
- Do not execute this contract during the Luna-0 governance authorization.

## Acceptance gates

1. Canonical Luna-44 fixture SHA-256 remains
   `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`,
   semantic digest remains
   `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`, and
   provenance SHA-256 remains
   `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22` before
   and after all validation.
2. All four existing failures are resolved by asserting the correct invariant;
   no test is suppressed or weakened. Luna-44 canonical artifact verification
   remains exact, alternate-runtime repeatability remains exact within that
   runtime, and canonical-runtime exact regeneration remains separately
   classified.
3. Luna-46 verifies the original pinned catalog object and content, tolerates
   only its exact governed checkout materialization, and fails adversarial
   content/source mutations.
4. Luna-47F accepts unrelated later repository evolution, still detects
   invocation-time mutation, and rejects mutations to every consumed
   historical input/source/protocol/result class.
5. Existing Luna-46 verdict remains **MIXED**; Luna-47 remains non-integrated
   and does not establish task-level efficacy or useful structural growth.
6. Relevant focused tests pass, the historical/core selection passes, and the
   complete repository suite is green (or Luna-0 explicitly governs any
   remaining non-green result before scientific work resumes).
7. Record all commands, counts, environment, evidence identities and any
   unavailable checks in the Luna-51 execution handoff. Return to Luna-0 for
   independent review. This authorization does not declare integration ready
   or authorize another successor.

## Governance boundary

No A01-A15 clause or ACP changes. This contract corrects provenance guards and
test interpretation only. Luna-0 is the next and only review role after
execution; Luna-52 is not authorized.