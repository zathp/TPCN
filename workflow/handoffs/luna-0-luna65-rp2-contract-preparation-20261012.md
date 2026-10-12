# Luna-0 Luna-65 RP-2 Contract Preparation

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "RP-2 restricted-token compatibility contract preparation"
  task_id: "L65-PHASE2A-RP2-CONTRACT-PREPARATION"
  component: "Luna-65 Phase 2A governance"
  status: "blocked"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "45121227d96c6fa13357c6bdf5fba0d99d8d7352"
  result_revision: "uncommitted; BLOCKED; no publication"
  dependencies: ["Frozen D-R7-4 R7 profile", "RP-1 corrective publication"]
  owner: "Project owner"
  classification: ["governance-only", "compatibility-contract preparation"]
  hypothesis: "A reviewed synthetic test can falsify or establish bounded U1-U3 compatibility without changing R7 or running scientific fixtures."
  counter_hypothesis: "The frozen profile or required evidence cannot be realized without an unapproved change."
  interfaces_relied_on: ["Windows restricted-token/process/job/pipe APIs", "Frozen venv launcher and base Python 3.11.4"]
  label_information_boundary: ["No TPCN, dataset, E2 counter, training or benchmark access."]
  timing_assumptions: ["Proposed 10 s active; 5 s cleanup; 20 s attended outer deadline; best-effort, not hard real-time."]
  reset_boundaries: ["No invocation consumed; RP-1 already consumed and cannot be retried."]
  resource_bounds: ["Proposed 64 MiB job charge, 8-process backstop, 5 s job user CPU, 1 MiB retained output; source-level parent limits only."]
  authorized_scope: ["Contract and governance preparation", "Four-lane independent review", "Conditional governance-only publication on integrated PASS"]
  unauthorized_scope: ["RP-2A source implementation", "RP-2B execution", "RP-1 rerun or source change", "RP-3", "Supervisor implementation/qualification", "Fixtures", "Windows security configuration changes"]
  controls: ["Exact baseline ancestry and R7/RP-1 source identities", "Preserve unrelated untracked files", "No token/process/host experiment", "No source fallback or profile reinterpretation"]
  measurements: ["Repository hashes/ancestry only; no new runtime or host compatibility observations"]
  information_boundary_check: ["Read-only governance/source/docs; no scientific execution"]
  hardware_mapping: ["Not applicable; no hardware equivalence claim"]
  architecture_invariants_touched: []
  preserves: ["RP1_CONTRACT_DEFECT", "R7 profile pending explicit blocker resolution", "U1-U8 unproven", "Luna-63C frozen; Luna-64 corrective and full Spiral blocked"]
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md"
    - "workflow/handoffs/luna-0-luna65-rp2-contract-preparation-20261012.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All RP-2 runtime questions", "All supervisor/fixture/benchmark tests"]
  assumptions: ["R7 literal profile is not silently amended by compatibility design"]
  unresolved: ["B01 requires explicit profile decision", "B02 requires exact compatible descriptor/access plan", "Post-review compatible clarifications not independently re-reviewed", "W/P process-local environment meaning outside the RP-2 synthetic workload"]
  recommended_next_agent: ["Luna-0: obtain explicit owner B01 decision and separately reviewed B02 plan; re-review exact revised package before any RP-2A authorization"]
```

## Outcome and owned scope

**OBSERVED:** baseline and upstream are
`45121227d96c6fa13357c6bdf5fba0d99d8d7352`; all four required ancestors
verified. Final RP-1 handoff blob
`bd0a457045fadeb2bc817ff7a080bbe8374eb5a0` and CRLF SHA-256
`4537ADD62A7037713F3F3E7FF14A15B43FE8537E327540C610AB59B32A4C8861`
verified; original probe SHA-256/blob unchanged. Historical
`RP1_CONTRACT_DEFECT` and one consumed invocation preserved.

Excluded local source/record checkout hashes at start:

- supervisor scaffold: `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`;
- S1-B final authorization record: `BB9134CB7FF1813D495575FA80F912EEFB6E6A7C7A86F720CDAD829CAC925451`.

**INFERRED:** documentation conflicts/underspecification prevent a complete
implementation-ready contract without a reviewed profile decision. They
do not establish host incompatibility. The proposed contract preserves exact
R7 requirements, specifies U1-U3 sequence/evidence, synthetic import-only
workload, bounded handle-inventory negative control, cleanup/classifications,
and separate RP-2A/RP-2B authorizations. No source is written.

## Architecture evidence

No A01-A15 clause changes; all neural acceptance checks are not applicable
to governance preparation, not claimed passing. No ACP required. U1-U8
remain unproven; a future bounded RP-2 PASS cannot qualify B-min containment.

## Validation record

| Procedure | Revision | Result |
|---|---|---|
| Branch/HEAD/upstream/ancestry | baseline above | PASS; tracked tree initially clean; two unrelated untracked files preserved |
| RP-1 probe/handoff and R7 identity checks | baseline above | PASS; hashes/blobs recorded in contract |
| Microsoft API documentation inspection | 2026-10-12 | Semantics and evidence limitations documented; no host APIs run |
| Four independent review lanes | first-draft identities below | A BLOCKED; B BLOCKED; C BLOCKED; D PASS lane only; integrated BLOCKED |
| Runtime compatibility / source static validation | not authorized | NOT RUN |

## Benchmark and resource results

Not applicable. No workload, benchmark, source, token, job or process test
executed; no result or enforcement qualification claimed.

## Independent review and publication

**BLOCKED — RP-2 CONTRACT INCOMPLETE.**

Four separate Luna-11 read-only reviews were obtained. No reviewer edited,
staged, published, ran imports/tests/host probes or implemented a source.

| Lane | Verdict | Preserved findings / disposition |
|---|---|---|
| A Windows semantics | BLOCKED | DISABLE_MAX_PRIVILEGE disables, not promised deletion; R7 "only privilege entry" needs an explicit decision. Shared-SID child descriptor is underspecified, not proven impossible: creation-returned root handles may permit literal no-workload-ACE access, but full chain access/descriptor still needs exact review. Integrity-group treatment clarified prospectively. |
| B Interpreter/handles | BLOCKED | Parent/workload environment distinction, launcher/base topology, startup hooks/dependency closure, READY checkpoint protocol and exact per-stream grammar needed. Bounded PSS plus duplicate/compare/basic NtQueryObject rights method accepted as suitable in principle, not runtime evidence or proof of no transient leak. |
| C Safety/resources/evidence | BLOCKED | Startup content identities, normal/failure phase deadlines with independent design rationale, and aggregate all-file high-water/reserve evidence needed. |
| D Governance/provenance | PASS, lane only | Required ancestry/profile/probe/handoff hashes and unchanged historical verdict verified; no extra governance blocker, no authority for implementation/execution/publication while A-C BLOCKED. |

The first reviewed contract was 30,632 CRLF bytes:

- checkout SHA-256 `5186CB531E77826180206C350A735CEE00AD401F347B5C3666DF2080715FC8A3`;
- raw checkout blob `4a8ce6554727e2344bdea1278a711573ecce5511`;
- LF SHA-256 `9D5BED4F0A3F9E7CD23EC6C700EB198DEBE9DFB5F887A4B3C2E3351F3898B31C`;
- candidate normalized Git blob `a41272f83f26ee01bf52af152c1597ba6c3c7ff0`.

Lane D independently verified the first handoff raw SHA-256
`3DFB71E0B35017E302F292BE71690DE37DA110264EFBCE387D7585E72CBF7641`,
LF SHA-256 `8CB87539E429C7F283A9F4644A104B4D118ACB643A22E11CC793055874CFF91A`,
normalized blob `1e9d66657171cd4af897590bfb82e71c4fab5cba`; workflow raw
SHA-256 `28A411E882C1CCC1282DA76D4496422B6C019063C8004790F4F4EE8AC239CF91`,
raw-CRLF Git blob `b964f5add4f21bfba9139f56c9570eff4cf6de7e` (`-text`).
CRLF-aware diff checks passed. These identities identify the reviewed drafts,
not the post-review candidate or a publication.

Compatible clarifications were incorporated into the candidate contract after
review: startup/hook/path/dependency content binding; literal expected two-process
mapping; exact READY-dwell-END ordering and required future grammar binding;
capture-allocation caveat; normal/failure deadlines and timing rationale;
all-file high-water/reserve model; narrower B02 wording. They are not independently
re-reviewed, do not remove the profile blocker, and do not constitute PASS.
Exact bytes must be re-bound/re-reviewed before a later integrated PASS.

No files staged, no commit or push, no new publication identity. All evidence
is governance/source/documentation interpretation only; U1-U8 remain unproven.

## Reproduction and rollback

Read the new contract against the hash-bound R7 profile and baseline; do not
run a probe. Changes are limited to the contract, this handoff and workflow.
No historical source/evidence or unrelated untracked files may be reverted.

## Next assignment

Smallest next owner prerequisite is an explicit B01 decision: retain the
construction and require only SeChangeNotifyPrivilege enabled (other entries
disabled), or retain the only-entry requirement and separately authorize a
reviewed token-construction change. Neither option is accepted by this draft.
Luna-0 also needs a reviewed literal-compatible B02 descriptor/access plan;
only if impossible must an owner approve changing the no-workload-ACE term.
Then independently review the exact revised contract/handoff/workflow.
Only after integrated contract PASS may the owner
authorize RP-2A source implementation/static review; RP-2B needs another
explicit execution authorization after source publication and independent
review. RP-3, supervisor work, fixtures and benchmarks remain unauthorized.
