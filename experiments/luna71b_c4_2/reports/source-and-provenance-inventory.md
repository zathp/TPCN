# Luna-71B-C4.2 Source and Provenance Inventory

## Correction-pass addendum (2026-10-15)

**INCOMPLETE — CORRECTION REQUIRED remains the governing review disposition.**
The initial inventory below is retained as historical evidence, including its
initial manifest hash and before/after table. Current source hashes are in
`source-manifest.json`, SHA-256
`43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719`.
Both corrected event-runtime copies have SHA-256
`e16a48af25657e5a45773248adbed37dd41782f4ef51fba9fd1e2cda013617fd`.
Only those two copied source files were changed in this correction pass.
All other variant source hashes remain unchanged.

The six PPC-11 modules and the focused test were also corrected; see
`correction-pass-report.md`. Tests now import the copied **event runtime
primitives only** under synthetic module names, using synthetic events and
handlers. They do not import or execute neurons, model contexts, runners,
training, inference, or a pilot. The original report's no-source-import
statement describes the initial pass only.

`run_authorized_pair` is now explicitly preflight-only: even a valid grant
cannot dispatch its arbitrary callback. Full model/source/trace-bound
dispatch and online full-stream comparison are unimplemented, not enforced.
Existing bytecode caches are excluded from the source manifest and were not
deleted or certified; no future source-loading identity claim is made.
The frozen fixture payload manifest remains absent. P01 therefore always
records an explicit fixture-identity incompleteness in the comparator.
The initial inventory's future-dispatch statements are superseded by this
fail-closed restriction. A fresh Luna-0 review passed the bounded corrections
only; PPC-11 remains incomplete and no smoke-pilot eligibility is established.

## Scope and identities

- Worktree: `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna71b-c4-2`
- Branch: `experiment/luna71b-c4-2-bilateral-capture`
- Required baseline: commit `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`
- Governing C4.1 artifact-manifest SHA-256:
  `2f18d694784a6a583b0a7c01e6cc89f1313c2d65c7c6b5346a7cd4d993d3f1fa`
- Frozen pilot-plan SHA-256:
  `60cde6b4929be4408fcecdcf3ac7104d5cb7b3365d94d55b568431e54fb5bc3f`
- Current copied-source manifest:
  [`source-manifest.json`](source-manifest.json), SHA-256
  `43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719`.
  It lists every copied source file under both variants, the seven PPC-11
  implementation modules, each raw SHA-256, and each source's conservative
  runtime-identity inclusion.

The nine C4.1 artifacts and their raw hashes were verified before this
implementation. No C4.1 artifact, historical source tree, pilot plan, or source
identity copy was changed. The frozen plan contains IDs and content/input
hashes, including 48 execution-order IDs per split, plus the initial parameter
snapshot/digest. It does **not** contain event payloads. The copied inputs are
only the plan and preparation-execution text; no immutable event fixture was
loaded, generated, or inferred.

## C4.2 edits to copied source files

“Before” is the raw C4.1 source identity recorded in
`workflow\handoffs\luna71b-c4.1\04-source-identity-inventory.md`; “after” is
the raw SHA-256 of the current copied file. The runtime baseline was recorded
as a shared Luna-71B runtime identity.

| Copied source file | Before SHA-256 | After SHA-256 |
|---|---|---|
| `variants\original\tpcn\event_runtime.py` | `151096ac3a1f6b1a528dfe9be98c8110385021bc453cdf9e5f0ad27e793ee77f` | `ed1f5992bb3977d7cfb98ce9c8c729572bf6d6791c40a23482ed8c76997668d9` |
| `variants\original\tpcn\luna70_readout_learning.py` | `b2af493ad44ceca22a5d2994ebee53cb61cdc44d04ab743e34e7517d79f07b75` | `12fb0848abc83facabab7f0eaaf064ffaf966364579845df6fbc14da13e55b65` |
| `variants\instrumented\tpcn\event_runtime.py` | `151096ac3a1f6b1a528dfe9be98c8110385021bc453cdf9e5f0ad27e793ee77f` | `ed1f5992bb3977d7cfb98ce9c8c729572bf6d6791c40a23482ed8c76997668d9` |
| `variants\instrumented\tpcn\luna70_readout_learning.py` | `939b55ed6bfa27360e6be53122c91a26153b2b7531b9fb29ee0c4801e8bc2d55` | `44e72ff1c5bd5ada9d2b6d1a6e7312e94e6574296c6626bf49c6e174a777b17d` |
| `variants\instrumented\tpcn\luna71b_trace.py` | `28b336061c029013545f1cf114e82ef60303f5ebc747fd92090e17aee1ded515` | `256239286551b04c79328431563b2d6bc492c1b1793d092bd8081337d6558cd8` |

The original and instrumented event-runtime copies are byte-identical after the
hook additions. No runner, test snapshot, input, or other copied source file
was edited. Their current hashes are in the source manifest.

## Existing source differences: not capture passivity

The original and instrumented source snapshots were not normalized or
substituted for one another. The following Luna-71B baseline differences remain
material and must not be collectively characterized as passive capture:

- The instrumented runner adds `_validate_full_config` and per-split plus total
  exposure limits, configuration caps, and cooperative wall-clock checks at
  exposure boundaries. Its training/evaluation orchestration and run controls
  differ from the original runner.
- The instrumented runner has a trace-writer/budget factory and additional
  trace provenance/metadata handling. Those mechanisms are runner changes,
  separate from C4.2's optional source hooks.
- The instrumented model's `run_example` uses an `ObservedQueue` wrapper and
  adds diagnostic calculations (including `expected_delta`) around model
  behavior. This is an existing observer/diagnostic difference, not evidence
  that original and instrumented executions are behaviorally equivalent.
- The C4.2 original-side additions are limited to optional capture parameters
  and source-transition hooks. The new event-runtime observer callbacks are
  no-ops when no observer is supplied. This establishes an opt-in design, not
  measured non-interference. The instrumented side retains its pre-existing
  observer and diagnostic differences.

For reference, the C4.1 inventory identifies the unmodified original and
instrumented runners as `1d4ff78f184db7720b23795e6c16f30b6f88214979566c52baff4cb3d19da47f`
and `f82eba8a5c5c0bed8b6aa7b51e9a83f2d3a920a8afbf15ec32f2bb859b7db7ac`,
respectively. They were not executed here.

## Passive-evidence boundary and provenance limits

- Capture hooks observe source transition arguments and queue state. They do
  not call state-mutating model APIs to inspect hidden state.
- C4.2 tests import only the PPC-11 utility package and use synthetic records
  and doubles. The fail-closed driver test verifies source identities and stops
  at the absent fixture-payload manifest before dispatch; it asserts that its
  execution callback was not called and that no `tpcn` source module was loaded.
- No source variant, training runner, model, pilot, R6 result, or dataset was
  imported or executed. No neural training, inference, or pilot occurred.
- No separate neural-execution authorization or event-payload fixture
  manifest is present. A future call remains blocked until both are supplied,
  independently verified, and bound to the source manifest and plan.
- Source hashes establish file identity only. They do not establish historical
  source-to-run lineage, bilateral runtime equivalence, passive behavior of
  the existing instrumented observer, or PPC-11 readiness.
