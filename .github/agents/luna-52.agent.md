# Luna-52 — Retained Provenance Compatibility and Public Verification Closure

## Status

**AUTHORIZED / NOT EXECUTED** by the Luna-0 governance decision published with
this contract. Luna-52 is a correction-only verification task, not a scientific
experiment.

## Role and objective

Close only the two follow-up gates retained after Luna-51:

1. separate Luna-47B's authenticated historical Luna-46 analyzer source from
   reviewed current analyzer source, and reconstruct through the historical
   source rather than requiring today's checkout to remain byte-identical to
   it; and
2. add adversarial coverage of Luna-47F's public `--check` entry point,
   including its actual provenance and non-mutation checks.

The shared objective is to prove retained-provenance identity without
rewriting history or rejecting unrelated reviewed repository evolution.
Preserve all scientific artifacts, rules, outcomes, and interpretations.

## Baseline and authoritative inputs

- Starting revision: `e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e`.
- Luna-51 authorization and execution handoff:
  `workflow/handoffs/luna-51-provenance-guard-correction-20261008.md`.
- Luna-51 independent review: accepted with follow-up at the same published
  revision.
- Luna-0 authorization:
  `workflow/handoffs/luna-0-review-luna51-authorize-luna52-20261008.md`.
- Luna-47B protocol and retained execution handoff:
  `experiments/luna47b/PROTOCOL.md` and
  `workflow/handoffs/luna-47b-drive-accumulation-gain-20261006.md`.
- Luna-47F protocol, diagnostic, retained records, and existing tests.
- Luna-46 historical analyzer at authorization revision
  `789dda5988daf72f375d9713bd76a6da2b9e8b34`, path
  `run_luna46_depth_scaling_diagnostic.py`, Git blob
  `08f217daec167b2abc82f5988dba660c19f4ae0e`.
- Luna-46 reviewed current source at Luna-51 revision
  `e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e`, same path, Git blob
  `59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4`.
- Production/evidence baseline `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
- `workflow/ARCHITECTURE_CONTRACT.md` and
  `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`.

## Repository-evidence finding

Luna-47B's historical analyzer blob is retrievable from Git and is identical
at its authorization revision and recorded execution revision
`38891b81754ce385c55f96e4020e2bf04c2b9a5d`. Luna-51 changed the current
Luna-46 file in provenance verification: it authenticates the pinned catalog
Git object independently from checkout bytes and permits only exact
LF-to-CRLF materialization. The Luna-51 diff changes integrity/read
verification code, not the Luna-46 scientific analysis, recurrence, or verdict.
The Luna-47B `reconstruct()` guard nevertheless compares the whole current
analyzer file to the historical source bytes. That is an overbroad
current-source immutability check.

The appropriate compatibility classification is **MIXED (Case D)**:

- historical analyzer source identity, Luna-47B protocol and execution source,
  evidence inputs, and retained output remain historically anchored;
- the exact historical Luna-46 analyzer must remain recoverable and must be
  the code used by historical Luna-47B reconstruction;
- the current Luna-46 analyzer is a separate identity and may evolve under
  reviewed governance; Luna-51's source blob is the reviewed current identity;
- current code must never be presented as the historical code or silently
  substituted during historical reconstruction.

The existing Luna-47F `--check` command passes on the unmodified published
tree and invokes retained-record checks, pinned protocol/code identity checks,
all twelve consumed-input checks, replay checks, the live pre/post mutation
guard, and retained-output comparison. Existing tests exercise this command
only on the passing unmodified state; the adversarial mutations are helper
tests. The missing public-path coverage is real, but is not by itself evidence
of an implementation defect.

## Authorized ownership

Only these implementation and test surfaces may change:

- `experiments/luna47b/diagnostic.py` and `tests/test_luna47b_gain.py`.
- `tests/test_luna47f_diagnostic.py` and/or
  `tests/test_luna47f_retained.py`.
- If strictly required to enable real public-path verification,
  `experiments/luna47f/diagnostic.py`; no scientific scoring changes.
- This contract, a Luna-52 execution handoff, the corresponding current
  `workflow/docs/luna/LUNA_WORKFLOW.md` entry, the
  `workflow/ARCHITECTURE_CHANGELOG.md` entry, and the Luna-0 authorization
  handoff if its execution-state link must be updated.

Do not edit any retained scientific artifact, prior Luna-47 protocol or
handoff, Luna-46 scientific output, Luna-44 fixture/provenance, ACP, or
architecture contract.

## Luna-47B historical-source requirements

- Retrieve the historical analyzer bytes from the exact pinned Git revision
  and verify both revision/path Git blob
  `08f217daec167b2abc82f5988dba660c19f4ae0e` and the historical execution
  identity before use.
- Use the authenticated historical analyzer implementation for the
  Luna-47B retained reconstruction, isolated from the current module import.
  Do not substitute the current `run_luna46_depth_scaling_diagnostic.py`
  module when reconstructing the historical run.
- Verify the current analyzer separately against the reviewed Luna-51 blob
  `59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4` (with only exact governed
  checkout materialization accepted). Do not replace the historical pin with
  the current blob or claim that the current source was used historically.
- Preserve Luna-47B execution source/protocol identities and all retained
  inputs, numerical values, output bytes, verdicts, and artifact hashes.
- The retained result is evidence to verify, not an output to regenerate,
  rebaseline, rewrite, or overwrite. Tests may reconstruct in memory only.
- Fail closed if the historical object or pinned source identity is
  unavailable/mismatched, if current source diverges from its separately
  reviewed identity, or if reconstruction tries to substitute current source.
- Do not introduce scientific algorithm, recurrence, parameter, hypothesis,
  outcome, or protocol changes.

### Required Luna-47B adversarial tests

Must pass:

- historical analyzer object is retrievable and matches the revision/blob pin;
- reconstruction uses that historical object, while separately identifying
  the reviewed current Luna-46 source;
- the current reviewed source may differ without invalidating historical
  reconstruction;
- retained Luna-47B result and validation bytes remain unchanged.

Must fail:

- missing historical analyzer object or changed historical source pin;
- changed retained input, Luna-47B protocol/configuration, or retained result;
- current source substituted for historical reconstruction;
- unauthorized current-source bytes reported as the reviewed successor.

Tests must exercise the reconstruction/public verification route where
applicable, and must not just assert a helper's returned metadata.

## Luna-47F public `--check` requirements

- Exercise the real CLI entry point as a subprocess with `--check` in isolated,
  disposable repository state. Inspect exit code and diagnostic output.
- Do not mutate the actual worktree, retained evidence, or remote repository.
- The public path must reach and exercise historical source/protocol lookup,
  all consumed-input identities, retained evidence verification, analysis
  replay, and live pre/post non-mutation checks.
- Mutated fixtures must be constructed independently of implementation
  outputs; no test may generate expected metadata using the checker and feed
  it back unchanged as its own oracle.
- If a mutation would be rejected earlier by the dirty/non-owned change
  guard, use a clean committed state in the isolated clone (or equivalent)
  so the relevant historical identity check is actually exercised.
- Test live pre/post mutation through the actual `--check` invocation with a
  deterministic test harness, not only by calling
  `verify_live_nonmutation()` directly.
- Preserve public behavior and read-only semantics; no production test hooks,
  scoring changes, regenerated output, or relaxed verification.

Must fail through public `--check`:

1. substantive mutation of a consumed scientific input;
2. wrong historical input identity;
3. protected protocol or configuration mutation;
4. protected retained result/validation mutation;
5. same-path content substitution;
6. deterministic mutation during the public check, if the live guard's
   lifecycle is exercised by the harness.

Must pass through public `--check`:

1. unchanged published inputs and retained evidence;
2. unrelated later tracked source/repository evolution;
3. an unrelated governance-file addition;
4. the exact LF-to-CRLF checkout transformation where applicable.

The CLI pass on an unchanged repository is necessary but not sufficient.
Helper-only adversarial coverage does not satisfy this gate.

## Repository gate

Run and report exact results for:

- new Luna-52 tests;
- `tests/test_luna47b_gain.py`;
- `tests/test_luna47f_diagnostic.py` and
  `tests/test_luna47f_retained.py`;
- `tests/test_luna46_depth_scaling_diagnostic.py`;
- Luna-44/Luna-51 focused provenance regressions;
- the historical/core regression selection;
- the complete repository test suite.

The full suite must become meaningfully green. The existing Windows directory
symlink privilege skip may remain and must be identified as such. Do not hide
failures by skipping, xfail, deleting, weakening assertions, rebaselining, or
omitting tests.

## Protected artifacts and scientific boundary

Record pre/post hashes and prove byte identity for:

| Artifact | Baseline SHA-256 |
|---|---|
| Luna-47B retained result | `b120d2cc5718649fb0d57d93611ddb89b45113e79c0d3003cf330fe092d0fb83` |
| Luna-47B validation | `1ef630d88e4699e9bcc1e5d05e2cc868f12f38a3958f8f1a065a4132df628fe0` |
| Luna-46 original retained output | `32561efb9f81996133bc930751083b2678c455668e47f0cd854e7985ad0616df` |
| Luna-46 corrective pre-label output | `1c3843127c3de1e9b380fd06571282f0c19cf48a820730bc3ffa1dd5b11e65d4` |
| Luna-46 corrective retained output | `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` |
| Luna-47F retained result | `f24a56bf5a92f622c4dfdb661116a83a76df1f7b0ae0056d20920360ca3cbb7c` |
| Luna-47F validation | `e3c8cb236f57908319893c2e109a2c94f5dd8d50e6953f48810da74259a62c29` |

No scientific replay, neural execution, parameter search, mechanism
composition, efficacy, topology/growth, alternate-runtime sensitivity, or
hardware experiment is authorized. The tests validate only existing retained
evidence and provenance boundaries. Preserve the frozen scientific state:
Luna-46 **MIXED**; no integrated Luna-47 mechanism, task efficacy, or useful
structural growth established; Luna-47G remains synthetic tolerance evidence;
hardware equivalence unestablished; alternate-runtime sensitivity **UNKNOWN /
NOT TESTED**; fresh historical Linux regeneration remains parked.

No A01-A15 change or ACP is proposed. This successor does not authorize a
scientific successor.

## Forbidden actions

- Do not edit, regenerate, normalize, replace, or rebaseline any retained
  scientific input, result, validation artifact, or historical source object.
- Do not change Luna-47B/Luna-47F science, hypotheses, protocol, numerical
  rules, outputs, thresholds, verdicts, or interpretation.
- Do not replace the historical analyzer pin with the current analyzer blob;
  weaken source checks to file-existence checks; or present current source as
  historically used.
- Do not suppress, skip, xfail, delete, or broadly relax a failing test.
- Do not make the public-path tests depend on mutating the real worktree or
  writing retained evidence.
- Do not run a scientific experiment, modify A01-A15/ACP, or authorize
  Luna-53.

## Completion and publication

Leave a completed Luna-52 handoff with source/object identities, exact artifact
hashes, public-path adversarial results, all test counts, unrun checks, and
scientific interpretation. Update the workflow and changelog with evidence.
Commit authorized work, push to `origin/main`, fetch, verify
`HEAD == origin/main` and a clean worktree, then stop for independent Luna-0
review. Do not execute anything beyond this contract's correction-only
verification scope.
