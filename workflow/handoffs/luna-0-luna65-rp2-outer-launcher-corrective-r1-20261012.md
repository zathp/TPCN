# Luna-0 RP-2 outer-launcher corrective R1 handoff

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Medium probe admission, outer stop and token-object binding"
  task_id: "L65-PHASE2A-RP2-OUTER-LAUNCHER-CORRECTIVE-R1"
  component: "Luna-65 Phase 2A RP-2 direct experimental governance"
  status: "complete"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "45121227d96c6fa13357c6bdf5fba0d99d8d7352"
  result_revision: "uncommitted; reviewed design only; no publication"
  dependencies: ["Preserved direct candidate 374AB032...C2A476", "Preserved corrected RP-2 E573ADA3...3A313", "Frozen R7 production profile and prior A-D findings"]
  owner: "Project owner"
  classification: ["governance-only", "design", "four independent same-byte reviews"]
  hypothesis: "Ordinary Medium process descriptors and exact token-object access/readback rules can close design ambiguity without new privileges."
  counter_hypothesis: "Independent Low cessation on probe loss needs a different authority/lifecycle policy than sole-job/no-transfer."
  interfaces_relied_on: ["CreateProcessW", "CreateRestrictedToken same-input-rights rule", "OpenProcessToken", "GetKernelObjectSecurity", "GetTickCount64", "Retained process handles and kill-on-close job"]
  label_information_boundary: ["No TPCN imports, datasets, E2 counters, training, fixtures or benchmarks"]
  timing_assumptions: ["10 s active; <=5 s cleanup; 20 s attended outer; best effort, no hard guarantee"]
  reset_boundaries: ["No RP-2 invocation consumed", "RP-1 remains consumed; no retry"]
  resource_bounds: ["64 MiB proposed job charge", "8-process backstop, one expected Low process", "5 s job user-time backstop", "1 MiB aggregate logical evidence with unchanged reserve"]
  authorized_scope: ["Medium/outer/token governance correction", "Independent A-D exact-byte review", "Local handoff"]
  unauthorized_scope: ["Source/wrapper implementation", "Probe/interpreter execution", "Token/job creation", "Windows configuration edits", "RP-3", "Supervisor work/qualification", "Phase 2A/2B fixtures", "Full Spiral", "Luna-64 corrective execution"]
  controls: ["No edits after R1 hash freeze", "All historical bytes preserved", "Owner-policy decisions explicit and unaccepted", "No staging/commit/push"]
  measurements: ["Repository and executable hashes, Git state, documentation semantics only"]
  information_boundary_check: ["Read-only files/Git/public API documentation; no scientific runtime"]
  hardware_mapping: ["Not applicable; no equivalence claim"]
  architecture_invariants_touched: ["A07 isolation and A08 boundedness requirements preserved, not tested"]
  preserves: ["All A01-A15 semantics", "Accepted B01", "Low X-L/P-L/three-handle/direct identity design", "Prior B/D PASS findings", "Old full-chain B02 BLOCKED history", "All execution prohibitions", "Scaffold/workflow/handoffs unchanged", "Luna-63C FROZEN"]
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_RP2_OUTER_LAUNCHER_CORRECTIVE_R1.md"
    - "workflow/handoffs/luna-0-luna65-rp2-outer-launcher-corrective-r1-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All runtime compatibility and token/job/process tests", "All fixtures, supervisor qualification and benchmarks"]
  assumptions: ["Ordinary Windows-issued descriptors can be queried with requested access; runtime feasibility unmeasured"]
  unresolved: ["Owner D-RP2-DIRECT-1", "Owner D-RP2-MEDIUM-1", "Owner D-RP2-OUTER-1 or stronger separately reviewed recovery design", "Future exact source/host/literal/closure/static bindings"]
  recommended_next_agent: ["Luna-0: obtain three owner decisions; if OUTER-1 rejected, dispatch bounded independent Low authority/lifecycle design; no implementation yet"]
```

## Outcome and owned scope

**PASS - RP-2 DIRECT CONTRACT READY FOR OWNER DECISION.**

This is an integrated design-decision readiness result, NOT implementation
readiness, owner acceptance, runtime feasibility, independent Low fault
containment or supervisor qualification.

**OBSERVED:** Baseline/local upstream match
`45121227d96c6fa13357c6bdf5fba0d99d8d7352`; branch as above; empty index.
Existing workflow modifications, untracked contracts/handoffs and scaffold
were preserved byte-for-byte. No remote fetch or publication occurred.

Two additive local governance records only. The probe source remains absent;
no wrapper/source generated, Python imported/invoked, token/job/Low process
created, probe/fixture executed or Windows configuration modified.

## Medium admission and descriptor decision

The [R1 candidate](../docs/luna/LUNA_65_PHASE2A_RP2_OUTER_LAUNCHER_CORRECTIVE_R1.md)
specifies existing attended Windows PowerShell 5.1 outer O using native
CreateProcessW once to launch the same hash-bound base Python as Medium
probe P, suspended under O's existing non-elevated primary security context.
No impersonation, credentials, elevation or alternative Low creation API.

Proposed NULL process/thread security attributes use ordinary Windows-issued
P process/initial-thread descriptors. O receives and retains the native
process/thread handles; admission queries owner/DACL/label, image, PID plus
creation FILETIME, actual token fields and granted masks before one resume.
Required operational unions are process 0x00121401 and thread 0x00120042;
actual full returned capabilities are recorded, not denied or hidden.

No custom protected DACL or OWNER RIGHTS denial is needed for the retained
outer handle route. No existing shell SD is edited. No Low-to-trusted-process
ACL denial/U4/U6 claim follows. The proposed exception applies ONLY to this
diagnostic P/initial thread, not production B-min W/P.
P-created job/sentinel/native worker X-M targets stay unchanged; Low process/
thread X-L and pipes P-L stay unchanged.

## Outer stop, evidence and independently uncontained residual

O inherits no job or Low process/token handle. P remains sole job owner;
no job duplicate, new observer job, service, ETW or global process census.
O receives two Medium capture streams only; L still receives exactly three
Low writes. O is proposed sole diagnostic evidence-file writer, and P relays
byte-recoverable independent Low streams and structured observations.
All simultaneous representations share the unchanged 1 MiB cap/reserve.

Native GetTickCount64 supplies a common host uptime epoch. O0 starts before
the one Medium creation attempt; P0 starts at probe entry. Preserve P0+10
active, min(F+5,P0+15,O0+20) cleanup/finalization and O0+20 outer cutoff.
O initiates its finite stop on earlier fault/operator request or O0+15 if
P is still active, reserves <=5 seconds, and attempts TerminateProcess on
the retained exact P handle AT MOST ONCE. Bounded waits and capture-reader
cancellation observe P exit/EOF; no name-based/PID-only kill, retry or
termination guarantee.

**INFERRED:** O can independently observe P's cessation, but cannot
independently confirm/recover L/D after P loss under sole-job/no-transfer.
Kill-on-close does not prove cessation. If L was not assigned, job close
cannot kill it. Creation/publication races and unavailable descendant
observations remain UNKNOWN_FAIL_CLOSED. An unobserved Low survivor could
continue beyond the diagnostic deadline; its lifetime is NOT bounded by
this report or an UNKNOWN label.

The owner-approved production B-min residuals do not automatically accept
this diagnostic limitation. Proposed D-RP2-OUTER-1 explicitly accepts it
for owner decision only; rejection requires separately reviewed authority/
lifecycle design. There is no independent-containment PASS here.

## Token-object matrix and necessary rights correction

R1 section 6 completes the matrix:

| Token reference | Route/type/contained integrity | Required mask | Owner of reference |
|---|---|---|---|
| O own primary | OpenProcessToken self; Medium | QUERY + READ_CONTROL = 0x20008 | O |
| P primary, admission query | OpenProcessToken from retained P; Medium | 0x20008 | O |
| P source construction token | OpenProcessToken self; primary Medium | ASSIGN_PRIMARY + DUPLICATE + QUERY + ADJUST_DEFAULT + READ_CONTROL = 0x2008B | P |
| Derived R | One CreateRestrictedToken of P source; primary; set contained IL Low only | SAME input rights, 0x2008B | P |
| Admitted L primary | OpenProcessToken from retained L; Low | 0x20008 | P |
| L self-query | Unchanged literal, own primary Low | TOKEN_QUERY = 0x8 | L |

The old source 0x2000A mask was insufficient: Microsoft's constructor
documentation says its returned handle has the same rights as the input.
0x2008B on source is necessary to receive ASSIGN_PRIMARY/ADJUST_DEFAULT
on R. Acquiring object access under an existing DACL is not acquiring/
enabling a privilege. Source token is never adjusted; only R's contained
TokenIntegrityLevel is set. Mandatory policy 3 is read back without repair.

Every reference is non-inheritable, verified and locally closed. No token
transfer to O/L, no TOKEN_ALL_ACCESS/MAXIMUM_ALLOWED/privilege-adjustment
or WRITE_DAC/WRITE_OWNER/SYNCHRONIZE token requests.

Read actual OS-issued token-object SD with bounded GetKernelObjectSecurity
OWNER/GROUP/DACL/LABEL queries and READ_CONTROL. Token contents, TokenOwner,
TokenDefaultDacl and Low IL are NOT the token object's SD. Bind actual
self-relative bytes/decoded semantics and requery for drift before final use;
no fabricated static SDDL or audit-SACL privilege. No new descriptor needed.
Wrong/incomplete fields, inaccessible/undecodable SD or semantic drift refuse
admission and follow failure/cleanup precedence, not ACL/token repair.

## Independent review identities and verdicts

All four lanes independently verified identical R1 checkout SHA-256 and the
unchanged direct dependency. Candidate was not edited after review freeze.

| Representation | Canonical identity |
|---|---|
| R1 checkout SHA-256 | `F9913AC44C268291988F549A110B2EFCC4777139A2BB8BD0DA407DF020FABEFB` |
| R1 raw CRLF Git blob | `7c6c5113494604b1f2f9494c4ab207c8d3705226` |
| R1 Git-clean LF blob | `8abb50dfef732da71cee94b1623c61b3f4f8e49e` |
| Direct dependency checkout SHA-256 | `374AB0328B62966EEA7C1E52E9E9E25BB40D973863177DEC4160D077E1C2A476` |
| Preserved corrected RP-2 checkout SHA-256 | `E573ADA32D746E6766D21420C845FF6AA09B18107F05523A6F1BE8913EE3A313` |

| Lane | Actual verdict | Independent disposition |
|---|---|---|
| A Medium SD/token rights | PASS - RP-2 DIRECT CONTRACT READY FOR OWNER DECISION | Ordinary Medium admission, retained handles, source-mask correction, object-SD/readback distinction complete as design. |
| B Low/direct/inheritance preservation | PASS - RP-2 DIRECT CONTRACT READY FOR OWNER DECISION | No introduced conflict with direct identity/Low descriptors/B01/four-variable environment/three Low writes/U1-U3 controls. |
| C outer/fault/cleanup/evidence | PASS - RP-2 DIRECT CONTRACT READY FOR OWNER DECISION | Finite stop/evidence/ownership rules complete for exact proposed narrower fault boundary; independent Low recovery on P loss explicitly absent and subject to owner decision. |
| D governance/provenance/isolation | PASS - RP-2 DIRECT CONTRACT READY FOR OWNER DECISION | Historical identities and restrictions preserved; proposed exceptions not accepted or applied to production; scientific isolation intact. |

Review interpretation limits:

- B's checkout SHA matched, but its raw/clean blob labels were inconsistent.
  Canonical values above were verified directly with --no-filters and --path,
  and matched D's report. No bytes changed to reconcile that metadata.
- B's phrase "only three handles" is restricted to inherited parent handles;
  the child's runtime-opened/self-query handles remain legal and separately
  inventoried. Total handle census is not required to contain only three.
- A's characterization of custom X-M as unworkable is not an impossibility
  finding. It was unnecessary for this retained-handle route, not universally
  impossible for newly created objects.
- C's "bounded residual" wording applies to termination attempts/observation
  and evidence, NOT the duration of an unconfirmed surviving Low process.
  No containment or hard termination guarantee is adopted.

## Owner decisions and publication boundary

All three remain **PROPOSED / NOT ACCEPTED**:

1. D-RP2-DIRECT-1: exact direct-base Low diagnostic instead of venv chain,
   unchanged synthetic profile/envelope; no production interpreter switch.
2. D-RP2-MEDIUM-1: ordinary Windows-issued P/initial-thread SDs with readback,
   no custom X-M/OW requirement or Low-denial claim; two Medium capture
   streams and O as sole diagnostic evidence-file writer. Production B-min
   unchanged. Exact approval text is in R1 section 7.
3. D-RP2-OUTER-1: accept independent P-only stop/observation, sole P job
   ownership, UNKNOWN on missing Low cessation and potential survivor beyond
   deadline/probe-loss races/outer hang; no recovery guarantee, retries or
   production fault-model amendment. Exact approval text is in R1 section 7.

**No publication identity.** No commit/push/workflow update prepared as
accepted authority. R1 is independently reviewed; this disposition handoff
is not a separately reviewed publication package. After owner decisions,
review/freeze the complete governance package including an additive workflow
entry, then publish and fetch-verify exact identities. Old contracts/handoffs
remain immutable dependencies and retain BLOCKED history.

## Validation record

| Actual procedure | Result |
|---|---|
| HEAD/branch/local-upstream/status/index inspection | Expected baseline; pre-existing dirty work preserved; empty index |
| Candidate/direct/corrected contract and protected-record Get-FileHash | All expected identities matched before and after reviews |
| Base Python executable Get-FileHash | `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`; no launch |
| Public Microsoft API documentation inspection | Constructor same-input-rights rule verified; default process/thread and token-object access semantics documented |
| Four independent exact-byte reviews | A-D PASS for owner decision only |
| Raw/clean Git blob verification | Canonical values above; no object publication/staging |
| CRLF-aware diff --check / new-document check | No whitespace diagnostics; no-index difference exit 1 distinguished from check failure |
| Editor problem checks | No errors in governance documents |
| Probe source existence | Absent; not created or modified |
| Runtime/token/job/process/source/fixture validation | NOT RUN / NOT AUTHORIZED |

No benchmark metric, energy, seed, hardware realization or neural integration
result is applicable. Limits remain unqualified/unexecuted.

## Remaining RP-2A prerequisites and next assignment

Luna-0 obtains separate owner disposition of all three decisions. If OUTER-1
is rejected, independent Low observation/recovery authority and handle/job
lifecycle must be separately designed/reviewed; no implementation shortcut.
Then reviewed governance publication/fetched-identity verification.

RP-2A still needs a NEW explicit source allowlist including exact attended
outer wrapper/interop host. Bind process command/env/cwd/nonce/uptime parsing,
FFI/SD decoder/rights ABI/source-mask fix, host/startup/import closure,
unchanged embedded Low literal/quoting/grammar and byte-recoverable relay,
single-writer all-representation accounting/reserve, bounded readers and all
normal/failure/outer termination paths. Static independent review only, no
probe imports/token/job/child execution. Any new helper needs explicit authority.

RP-2B requires later separately granted exact execution identities, command,
run ID, fresh path/preflight/operator/stop procedure and published source.
Direct future U1-U3 success cannot establish production venv launcher,
root-to-base handle forwarding, internal job, environment/startup propagation
or full production pytest invocation compatibility.

RP-2 implementation/execution, RP-3, supervisor implementation/qualification,
Phase 2A/2B fixtures NOT AUTHORIZED. Full Spiral and Luna-64 corrective
execution BLOCKED. Luna-63C FROZEN. Stop after this design review.

## Reproduction and rollback

Reproduce only read-only file/Git identity checks; distinguish checkout CRLF
from Git-clean LF. Review R1 together with its immutable direct dependency
and prior BLOCKED records. No existing file needs restoration; retain these
new governance records as history. No source, token or security rollback
operation is applicable. Preserve all unrelated worktree changes.
