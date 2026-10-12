# Luna-0 RP-2 B01 acceptance and direct-interpreter review

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "RP-2 direct-interpreter governance and independent review"
  task_id: "L65-PHASE2A-RP2-DIRECT-INTERPRETER-CORRECTIVE-DESIGN"
  component: "Luna-65 Phase 2A RP-2 governance"
  status: "blocked"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "45121227d96c6fa13357c6bdf5fba0d99d8d7352"
  result_revision: "uncommitted; no publication"
  dependencies: ["Frozen R7 production profile", "Preserved corrected RP-2 contract and independent review history"]
  owner: "Project owner"
  classification: ["governance-only", "design", "four independent exact-byte review lanes"]
  hypothesis: "Direct hash-bound base Python eliminates the venv descendant-descriptor and handle-forwarding obstacle for a narrow synthetic experiment."
  counter_hypothesis: "A complete direct experiment still lacks compatible trusted-launcher admission and descriptor/access bindings."
  interfaces_relied_on: ["Windows restricted-token/process/job/pipe APIs", "Preserved RP-1 interpreter evidence", "Read-only executable hash/version-resource/PE-header inspection"]
  label_information_boundary: ["No TPCN imports, fixtures, data, training, capacity counters or benchmarks"]
  timing_assumptions: ["10 s active; <=5 s cleanup; 20 s attended outer; unexecuted and not hard real-time"]
  reset_boundaries: ["No RP-2 invocation consumed", "RP-1 consumed, no retry"]
  resource_bounds: ["Unqualified 64 MiB job charge", "8-process safety backstop; only one expected child", "5 s job user-time", "1 MiB aggregate logical evidence"]
  authorized_scope: ["B01 prospective owner-policy adoption", "Separate direct-base candidate", "A-D independent governance review", "Local completed handoff"]
  unauthorized_scope: ["Source implementation", "Token/job/probe/Python execution", "Windows security changes", "RP-3", "Supervisor work", "Phase 2A/2B fixtures", "Full Spiral", "Luna-64 corrective execution"]
  controls: ["Preserve historical contract and handoffs byte-for-byte", "No edits after candidate identity freeze", "Do not confuse owner decision with technical review", "No staging/commit/push"]
  measurements: ["Git ancestry and file hashes", "PE architecture and version resources only"]
  information_boundary_check: ["Read-only metadata/documentation plus governance documents; no scientific computation"]
  hardware_mapping: ["Not applicable; no hardware-equivalence claim"]
  architecture_invariants_touched: ["A07 isolation boundary preserved", "A08 boundedness requirements preserved, not tested"]
  preserves: ["All A01-A15 semantics", "Full-chain B02 BLOCKED findings", "RP1_CONTRACT_DEFECT", "Frozen production venv profile", "Untracked supervisor", "Existing workflow and authorization records", "Luna-63C FROZEN"]
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_RP2_DIRECT_INTERPRETER_DESIGN.md"
    - "workflow/handoffs/luna-0-luna65-rp2-direct-interpreter-review-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["Every runtime compatibility, token, job, child, fixture, supervisor and benchmark test"]
  assumptions: ["Version resources and retained RP-1 evidence are identity evidence, not a fresh Python runtime observation"]
  unresolved: ["Exact Medium probe/outer admission and stop route", "Actual token-object descriptor binding and acceptance expectations", "Separate owner direct-base experimental approval", "Later RP-2A/RP-2B source/execution authorizations"]
  recommended_next_agent: ["Luna-0: bounded launcher-admission and descriptor-contract correction, followed by same-byte A-D review; no implementation"]
```

## Outcome and owned scope

**BLOCKED - RP-2 DIRECT-INTERPRETER CONTRACT INCOMPLETE.**

**OBSERVED:** Expected baseline and prior corrected contract identities match.
The configured `tpcn-luna-workflow` paths were absent; authoritative tracked
counterparts under `workflow` were read. HEAD and locally recorded upstream
match the baseline. Required S1-B/RP-1 ancestry succeeded; no fetch performed.

Two new local governance documents only. Existing corrected contract,
preparation/correction handoffs, workflow changes, supervisor scaffold and
S1-B authorization record were not modified. The old contract stays BLOCKED.
No staging, commit, push, token creation, API compatibility experiment,
interpreter import/invocation, fixture, source implementation or Windows
configuration change occurred.

## B01 owner-policy adoption

The current instruction supplies the B01 owner amendment if affirmatively
adopted. Luna-0 adopted it prospectively in candidate section 2:
SeChangeNotifyPrivilege must be present and the only enabled privilege.
Other entries may remain only disabled; complete LUID/name/attribute
enumeration/readback required; unexpected enablement fails.

DISABLE_MAX_PRIVILEGE, Low SID 4096, mandatory policy 3, frozen SID/group rules,
no restricting SIDs, non-elevated Medium launcher, no acquisition/repair/
enabling of privileges and no administrator elevation remain required.
This is not acceptance of direct launch or authority for RP-2A.
Historical B01-awaiting-approval wording is preserved as historical text.

## Feasibility, descriptors and handle design

**OBSERVED:** Read-only Get-FileHash/Get-Item VersionInfo and PE-header reads
confirmed exact base executable
`C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe`,
SHA-256 `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`,
version resources 3.11.4, AMD64 0x8664, PE32+ 0x020B.
This agrees with historical RP-1 Python 3.11.4/64-bit evidence.
Base pytest/_pytest entry files and one .pth file exist; complete startup/
import/DLL closure is not established by these existence checks.

**INFERRED:** Direct creation can remove the intermediate venv descriptor/
handle-transfer boundary from this proposed experiment. The retained process/
thread handles offer an observation and termination route without reopening
the Low child. Host feasibility remains unexecuted, including quota-privilege,
SD creation, Python initialization, job/UI and snapshot behavior.

Candidate section 4 contains the exact proposed owner/DACL/mandatory-label
targets, matrix and handle masks for Medium launcher, Low child, initial child
thread, stdout/stderr/ledger pipes, token references, job, sentinel and workers.
Low child/thread targets have zero allow ACEs and OWNER RIGHTS deny
READ_CONTROL/WRITE_DAC; pipe targets are explicitly Low and permit the
intentional same-user pipe operations. New job/sentinel targets are Medium.
Target SDDL is a proposal, not observed created-object evidence.

Three write handles only reach the child through HANDLE_LIST; stdin NULL.
Parent read ends and process/thread/token/job/evidence references do not.
Parent closes child writes before resume and inspection writer duplicates
before EOF. Parent alone owns the job and retains child termination authority.
Creation-returned handles do not prove child ACL-denial requirements.

**UNRESOLVED:** X-M is specified for a future Medium probe without a complete
outer creation/admission route. Existing shell/VS Code process descriptors
cannot be asserted to match or edited under this scope. Actual source/derived/
admitted-token object SDs remain unbound, separate from token field values.
No successful returned handle can conceal these missing details.

## Independent exact-byte review

All four separate Luna-11 lanes independently verified the same final
candidate identity. No candidate edits followed that freeze.

| Representation | Identity |
|---|---|
| Checkout SHA-256 | `374AB0328B62966EEA7C1E52E9E9E25BB40D973863177DEC4160D077E1C2A476` |
| Raw CRLF Git blob | `d76c14c0fd9c50dd1e57245bad0a5c1cc5c566f0` |
| Git-clean LF blob | `66356a9328e6fc4dfc28e8b8eb2fdbbfc0cdf15d` |

| Lane | Actual verdict | Findings and integration disposition |
|---|---|---|
| A token/privilege/process security | BLOCKED | B01 sound; direct child descriptor/returned-handle approach sound as design. Medium probe X-M admission is a genuine missing contract route. Token-object SD representation is better categorized as later binding/readback obligation, not an invented constructor SD. |
| B direct Python/inheritance | PASS, lane only | Exact base identity, one boundary, three-handle allowlist, unchanged workload specification, future literal/closure binding and U1-U3 checkpoints accepted. No runtime compatibility evidence. |
| C containment/cleanup/evidence | BLOCKED | Internal limits, duplicate-writer closure, cancellation, EOF/cessation proof, high-water reserve accounting and failure precedence accepted. Outer admission/stop route and token SD bindings incomplete; review also cited pending direct approval. |
| D scope/provenance/isolation | PASS, lane only | Baseline, preserved contract/scaffold and history verified; B01 adoption valid; direct experiment stays unapproved; production/science/authorization boundaries intact. |

Reviewer interpretation limits are preserved, not silently treated as facts:

- A described mandatory policy as being set. The candidate permits Low
  TokenIntegrityLevel setting but requires policy 3 READBACK without repair;
  no TokenMandatoryPolicy-setting operation is authorized.
- B's broad "insurmountable" wording about the old venv route is not adopted
  as an impossibility theorem. The old full-chain descriptor/access plan
  remains unproven/incomplete, as recorded by the previous corrective review.
- B's comments about PSS/NtQueryObject do not turn NtQueryObject into a stable
  public ABI guarantee; its documented change/removal and error caveats remain.
- C cited pending owner approval as a blocker. Pending approval alone does
  not make a technical design incomplete; the integration adopts the actual
  missing outer route, independently of approval status.
- A's proposed correction would admit the Medium probe using its actual
  host-assigned SD instead of requiring X-M. That is not silently adopted:
  the owner requested an exact process/thread descriptor/access plan.
  Its denial/observation scope would need explicit reviewed reconciliation.

No integrated PASS. No implementation-readiness or enforcement claim.

## Validation record and preserved identities

| Procedure actually performed | Result |
|---|---|
| git status/HEAD/branch/local-upstream/merge-base ancestry | Expected baseline; pre-existing dirty worktree retained; empty staging index |
| Preserved old contract checkout/raw/clean blob checks | SHA-256 `E573ADA32D746E6766D21420C845FF6AA09B18107F05523A6F1BE8913EE3A313`; raw `489707e18bf422c370678a1433aad983fd14e552`; clean `f61847d0c93f59b189142c5544caf9791e32bbe4` |
| Base executable hash/version resources/PE reads | Matching bound Python 3.11.4 AMD64 identity, no launch |
| Static exact base startup-path existence checks | pytest/_pytest present; .pth present; no complete closure claim |
| Microsoft public API documentation inspection | Design evidence only, no host API execution |
| Four independent same-byte reviews | A/C BLOCKED, B/D PASS lane only |
| CRLF-aware git diff --check | Passed after using core.whitespace=cr-at-eol; initial default check flagged preserved pre-existing workflow CRLF, not a new change |
| New candidate no-index whitespace check | No diagnostics; exit 1 reflects new-file difference |
| Post-review candidate/old contract/scaffold hashes | Unchanged; full protected-record checks repeated at completion |
| Runtime/source/fixture tests | NOT RUN / NOT AUTHORIZED |

Benchmark metrics, seeds, neural energy, hardware equivalence and integration
acceptance tests are not applicable to this governance review.
All proposed limits remain unqualified/unexecuted. No evidence leaf created.

## Owner approval needed and production gaps

Candidate section 8 supplies exact proposed decision **D-RP2-DIRECT-1**:
approve only this hash-bound direct-base 3.11.4 AMD64 single-process RP-2
experimental profile, reviewed restricted token/API/descriptors/three handles,
unchanged synthetic specification/four-variable environment and candidate
10/5/20-second, 64-MiB, eight-process, five-second-user-time, one-MiB envelope.
It expressly does NOT approve a production interpreter change or implementation/
execution. **This decision is not accepted in this gate.**

Direct-base evidence cannot establish venv launch compatibility, root-to-base
handle forwarding, the internal venv job, venv environment/startup propagation,
or production pytest/fixture invocation. All remain independent prerequisites
for the frozen production profile. Old full-chain B02 remains preserved.

## Publication, next assignment and remaining RP-2A prerequisites

**No publication identities.** Candidate/handoff are local, unstaged.
Workflow is deliberately not edited: publication is conditional on all
required decisions and same-byte review success. The handoff is a disposition
record, not a separately independently approved publication package.

Next bounded assignment, Luna-0: choose and specify a compatible exact Medium
outer/probe admission/stop route and process/thread/worker descriptor plan
without existing-object edits, an unreviewed helper or a hidden weakening
of denial claims. Define token-object readback acceptance/binding obligations.
Then obtain fresh A-D review of one corrected identity and separately obtain
owner acceptance of D-RP2-DIRECT-1. Preserve this candidate/review history.

Only after that: reviewed governance package publication/fetch verification;
separate owner RP-2A source allowlist authority; exact FFI/SD serialization,
granted masks, worker/outer mechanics, literal/quoting/schema/import closure,
accounting and all cleanup paths frozen and independently statically reviewed.
Any wrapper/helper needs its own explicit allowlist decision.
RP-2B later needs reviewed/published source and an exact distinct execution
grant binding command/capture/run-id/paths/operator/stop procedure.

RP-2 source/execution, RP-3, supervisor implementation/qualification and
Phase 2A/2B fixtures NOT AUTHORIZED. Full Spiral and Luna-64 corrective
execution BLOCKED. Luna-63C FROZEN. Integration remains blocked.

## Reproduction and rollback

Reproduce identity checks with read-only Get-FileHash and git hash-object,
distinguishing checkout CRLF from Git-clean LF. Inspect the linked
[candidate](../docs/luna/LUNA_65_PHASE2A_RP2_DIRECT_INTERPRETER_DESIGN.md)
and preserved historical contract/handoffs. Never run a probe to reproduce
this governance result. No existing file was altered by this gate, so rollback
requires no restoration or security operation; retain these two new records
as review history and preserve all unrelated dirty/untracked work.
