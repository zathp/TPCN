---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-51 follow-up governance and Luna-52 authorization"
  task_id: "luna-0-review-luna51-authorize-luna52-20261008"
  component: "Retained provenance compatibility and public verification coverage"
  status: "complete — Luna-52 authorized / not executed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e"
  result_revision: "published governance commit containing this decision"
  dependencies:
    - "Luna-51 correction publication e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e"
    - "Luna-51 independent review accepted with follow-up"
    - "Luna-47B protocol, retained result, validation, tests, and execution handoff"
    - "Luna-47F protocol, CLI, retained result, validation, and tests"
    - "Luna-46 historical analyzer Git object and Luna-51 corrected analyzer"
  owner: "Project owner; Luna-0 governance decision"
  classification:
    - "read-only governance review"
    - "correction-only Luna-52 authorized / not executed"
    - "no scientific experiment or architecture change"
  hypothesis: "The two remaining Luna-51 gates can be closed by separating historical and current source identity and adding public CLI adversarial coverage, without changing retained scientific evidence."
  counter_hypothesis: "Luna-47B depends on exact current analyzer immutability or Luna-47F public checks expose an implementation flaw requiring broader scope."
  interfaces_relied_on:
    - ".github/agents/luna-51.agent.md"
    - "workflow/handoffs/luna-51-provenance-guard-correction-20261008.md"
    - "experiments/luna47b/PROTOCOL.md"
    - "experiments/luna47b/diagnostic.py"
    - "experiments/luna47f/PROTOCOL.md"
    - "experiments/luna47f/diagnostic.py"
  label_information_boundary:
    - "No labels or task outcomes entered TPCN computation."
    - "No neural or scientific replay was run; existing retained records were inspected."
  timing_assumptions:
    - "No neural timing was evaluated."
  reset_boundaries:
    - "No TPCN runtime was created or reset."
  resource_bounds:
    - "Read-only Git/source/test/artifact inspection plus one full repository test run and one existing Luna-47F --check execution."
  authorized_scope:
    - "Create one unexecuted, correction-only Luna-52 contract for the two unresolved Luna-51 follow-ups."
    - "Luna-47B historical/current source compatibility without changing protocol, analysis, retained inputs, outputs, or verdict."
    - "Luna-47F public --check adversarial coverage without scientific scoring changes."
    - "Update workflow, changelog, and governance handoff; publish the authorization."
  unauthorized_scope:
    - "No Luna-52 execution in this governance invocation."
    - "No scientific replay/experiment, artifact mutation, rebaseline, A01-A15 change, ACP, hardware claim, or Luna-53."
  controls:
    - "Fetched origin; HEAD and origin/main both equal e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e; clean tree; Luna-51 and both evidence baselines are in ancestry."
    - "Historical Luna-46 analyzer blob 08f217daec167b2abc82f5988dba660c19f4ae0e is retrievable at Luna-47 authorization and recorded execution revisions."
    - "Current Luna-46 source blob 59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4 differs only in the reviewed provenance integrity/read path; Luna-51 did not modify scientific recurrence/analysis code."
    - "The only full-suite failure reproduces at tests/test_luna47b_gain.py::test_full_retained_reconstruction_and_determinism."
    - "The existing public Luna-47F --check succeeds but has no adversarial CLI-level mutation coverage."
    - "No repository files or retained artifacts were changed during the review."
  measurements:
    - "Full suite: 1,670 passed, 1 failed, 1 skipped; failure is the Luna-47B whole-current-analyzer equality guard; skip is a Windows directory-symlink privilege limitation."
    - "Direct python experiments/luna47f/diagnostic.py --check: PASS: retained analysis, replay, inputs, code and protected hashes."
  information_boundary_check:
    - "PASS: no input, label, or output was introduced into TPCN computation."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 clause changed."
  preserves:
    - "Luna-44 canonical fixture and parked historical Linux regeneration limitation."
    - "Luna-46 MIXED verdict."
    - "Luna-47 non-integrated status, no task efficacy, and no useful-growth claim."
    - "Luna-47G synthetic tolerance status and unestablished hardware equivalence."
    - "Alternate-runtime sensitivity remains UNKNOWN / NOT TESTED."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-52.agent.md"
    - "workflow/handoffs/luna-0-review-luna51-authorize-luna52-20261008.md"
    - "workflow/handoffs/luna-0-independent-review-luna50-and-authorization-luna51-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Existing Luna-47F public --check command returned success on unchanged published state."
  tests_failed:
    - "Full suite: 1,670 passed, 1 failed, 1 skipped; sole failure: tests/test_luna47b_gain.py::test_full_retained_reconstruction_and_determinism."
  tests_not_run:
    - "No Luna-52 tests; successor is authorized but not executed."
    - "No adversarial public-path mutation tests; these are required of Luna-52."
    - "No scientific experiment or neural replay."
  assumptions:
    - "Historical analyzer code at the pinned revision is the Luna-47B reconstruction dependency; it remains available in Git and is identical at the recorded Luna-47B execution revision."
  unresolved:
    - "Luna-47B historical reconstruction must execute the exact historical analyzer object, not current analyzer bytes."
    - "Luna-47F public --check must be tested against isolated adversarial states."
    - "No integration-ready claim until Luna-52 passes all gates and Luna-0 independently reviews its publication."
  recommended_next_agent:
    - "Luna-52 correction-only execution from e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e; then Luna-0 independent review."
---

# Luna-0 governance review — Luna-51 follow-ups

## Decision

**LUNA-52 CORRECTIVE FOLLOW-UP AUTHORIZED — NOT EXECUTED.**

The Luna-51 publication remains accepted for its three correction surfaces.
This review authorizes one narrowly bounded successor for the two remaining
provenance/verification gates:

1. Luna-47B's retained reconstruction must authenticate and use its historical
   Luna-46 analyzer source, while separately recognizing reviewed current
   source evolution; and
2. Luna-47F must gain adversarial tests through the real public `--check`
   path.

The complete scope and acceptance criteria are in
[`.github/agents/luna-52.agent.md`](../../.github/agents/luna-52.agent.md).
This authorization does not execute Luna-52. Required sequence:

**Luna-0 authorization → Luna-52 execution → Luna-0 independent review.**

No scientific successor, experiment, or Luna-53 is authorized.

## Starting state and reproduced evidence

Remotes were fetched. `HEAD == origin/main` at
`e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e`; the worktree was clean. The
published Luna-51 revision is in ancestry.

The full suite was run at this revision:

```text
1,670 passed, 1 failed, 1 skipped
```

The single failure is
`tests/test_luna47b_gain.py::test_full_retained_reconstruction_and_determinism`.
It fails at `experiments/luna47b/diagnostic.py::reconstruct` with
`BLOCKED: reviewed analyzer changed`: the test requires the current
`run_luna46_depth_scaling_diagnostic.py` to match the analyzer source from
`789dda5988daf72f375d9713bd76a6da2b9e8b34`.

The exact historical Luna-46 analyzer blob
`08f217daec167b2abc82f5988dba660c19f4ae0e` is retrievable and is identical
at the Luna-47B recorded execution revision
`38891b81754ce385c55f96e4020e2bf04c2b9a5d`. Luna-51's reviewed current
analyzer blob is `59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4`. The Luna-51 diff
changes provenance/integrity loading and Git checkout identity verification;
it does not alter Luna-46 scientific analysis or recurrence. The overbroad
guard is current-source byte equality, not the historical-source identity
requirement.

Luna-47B is therefore classified as **MIXED / Case D**:

- historical analyzer, protocol, evidence inputs, and retained output must
  remain exactly authenticated;
- the historical analyzer must be used for historical reconstruction;
- the current analyzer is separately authenticated and may evolve through
  reviewed governance;
- current source must never be silently substituted or represented as the
  historical source.

The existing
`python experiments/luna47f/diagnostic.py --check` command returned
`PASS: retained analysis, replay, inputs, code and protected hashes`. Inspection
confirms that `--check` runs retained result/validation checks, historical
protocol/code verification, twelve consumed-input identities, retained
replay checks, the pre/post protected-file guard, and retained-output
validation. Existing tests cover the clean CLI path but not adversarial
mutations through that path. This is a coverage gap, not evidence that the
checks currently fail.

## Protected artifacts

The hashes below were independently read from the unchanged published files
and are mandatory pre/post values for Luna-52:

| Artifact | SHA-256 |
|---|---|
| Luna-47B `results.json` | `b120d2cc5718649fb0d57d93611ddb89b45113e79c0d3003cf330fe092d0fb83` |
| Luna-47B `validation.json` | `1ef630d88e4699e9bcc1e5d05e2cc868f12f38a3958f8f1a065a4132df628fe0` |
| Luna-46 original retained output | `32561efb9f81996133bc930751083b2678c455668e47f0cd854e7985ad0616df` |
| Luna-46 corrective pre-label output | `1c3843127c3de1e9b380fd06571282f0c19cf48a820730bc3ffa1dd5b11e65d4` |
| Luna-46 corrective retained output | `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` |
| Luna-47F `diagnostic.json` | `f24a56bf5a92f622c4dfdb661116a83a76df1f7b0ae0056d20920360ca3cbb7c` |
| Luna-47F `validation.json` | `e3c8cb236f57908319893c2e109a2c94f5dd8d50e6953f48810da74259a62c29` |

No historical input or scientific outcome may be changed.

## Scope and acceptance

The two gates share a clear correction-only purpose: close retained-provenance
compatibility and public-verification coverage without changing historical
scientific evidence. They are authorized together in Luna-52 because their
owned surfaces are non-overlapping and neither changes scientific behavior.

Luna-52 must:

- load/authenticate the historical Luna-46 analyzer object at the pinned
  revision and execute that object for Luna-47B retained reconstruction;
- separately check the current Luna-46 source against the reviewed
  Luna-51 source identity; reject substitution, unavailable history, and
  unreviewed current changes;
- preserve the Luna-47B protocol, inputs, output, validation, exact algorithm,
  and verdict without artifact regeneration or rebaseline;
- test the real Luna-47F `--check` CLI in isolated disposable repository
  state, with required negative mutation cases and positive governed
  variation cases, including the live pre/post guard;
- report pre/post protected hashes and run the focused, historical/core, and
  full-suite gates. The full suite must be meaningfully green; the existing
  Windows symlink privilege skip may remain with explanation.

No full-suite green result is presumed by this authorization. No scientific
experiment, neural replay, efficacy or topology work, A01-A15 amendment, ACP,
or hardware validation is included.

## Next action and stop

Luna-52 may begin only at its exact authorized starting revision,
`e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e`, and must follow its contract.
After push/fetch equality and clean-worktree verification, stop for a new,
independent Luna-0 review. No scientific successor is authorized in this
decision.
