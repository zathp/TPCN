# Luna-65 RP-2A corrective R1 source traceability

**Gate:** `L65-PHASE2A-RP2A-IMPLEMENTATION-CORRECTIVE-R1`
**Status:** Successor pair received integrated static A-D PASS; execution
and runtime qualification NOT AUTHORIZED. Initial mapping/review history retained.
**Baseline:** `f47c48a947e48867c629817fa1031cb93729e440`

P denotes `scripts/luna65_phase2a_rp2_compatibility_probe.py`.
O denotes `scripts/luna65_phase2a_rp2_outer_wrapper.ps1`.
Locations in the original matrix are one-based against the INITIAL reviewed
pair below. Successor location adjustments and identity bindings are recorded
in the supplement before renewed review. Function existence
alone is not completeness; independent reviewers must inspect its callers,
failure paths and evidence semantics. The matrix records connected paths
observed in source, not successful execution.

| Source | Checkout SHA-256 | Git-clean LF blob |
|---|---|---|
| P | `A61B1D2E7D87570EEA290F089DE91B44E275AAC81584214E47353F3275698A34` | `68b85729abef615022478bcf686ace20bb102dc2` |
| O | `28DA090B2639A72B7A57D8F4AA9F27D610C1F81CA992366170BBF82A5D5CB8F4` | `b07e34d10005c19cb2073a6c5454503d6df63641` |

Frozen literal remains 6,583 ASCII bytes, SHA-256
`D9EC540BCEA9326C67A791DA6C59FC11357C00396B707EEB9FE278FCD08BF2A0`.
Authoritative precedence: accepted owner decisions, immutable R1 corrections,
direct design and non-superseded older details. No profile relaxation is
authorized by this matrix.

## Connected obligation matrix

C4/C5/C6 refer to published RP-2A candidate sections 4/5/6; R3/R4/R5/R6 to
frozen R1 sections 3/4/5/6; D3/D4 to direct design sections 3/4. Exact
observations and invariants in those sources remain authoritative.

All runtime qualification entries below are **NOT RUN / NOT AUTHORIZED**.
Static method S means read source and caller/control-flow/FFI ownership; H
means read-only SHA-256/Git/materialization inspection; A means isolated text
AST/literal parsing; PS means trusted-shell ParseFile/ParseInput on text,
never evaluating source or interop. Implementer-reported parser checks are
distinct from independent completeness review.

| Obligation / contract | Connected function and source location | Required evidence fields or records | Failure behavior in source to review | Nonexecuting verification | Outstanding runtime qualification |
|---|---|---|---|---|---|
| Entry connection; C4/C6 | P main:1734 -> Controller.run:1362 -> cleanup:1515; O top-level try:790/catch:934/finally:939 | P0, stop_reason, FINAL; report.verdict | exceptions classified; cleanup/report failure UNKNOWN | S/A/PS | actual entry/failure paths |
| Frozen source/image identity; C4/D3 | P source_digest, verify_closure:793, identity; O Assert-Hash:77, preflight:790, actual host image | source_hash, image_hash, host_hash, identity | hash/PE/path/version mismatch blocks admission | S/H | actual image versus source-bound identity |
| Startup/import/DLL/absence closure; C4 | P tree_identity:761, verify_closure:793 called by run; O Verify-HostTree:86, Verify-PythonClosure:132 called by preflight | U2 closure, host_files, host_DLL_manifests, module origins | closure/search-path drift fails, no import discovery/workaround | S/H/A | exact environment import feasibility, resolution and hooks |
| O own Medium/non-elevated account/session; R3/R6 | O Read-Token:431, Admit-Medium:485, No-Impersonation:496 at preflight | O-primary Fields/SD, O_token | mismatch, impersonation or forbidden privilege fails | S/PS | own token access and actual context |
| Actual token-object SD versus contained fields; R6/C4 | P token:978, Native.token_fields:496, descriptor, drift:988; O Read-SD:379, Read-Token:431 | fields, sd/raw/semantic_equal, rights | unreadable/semantic drift blocks PASS | S/A/PS | SD access/ordinary descriptor forms |
| Source primary mask 0x2008B; R6 | P run:1362 -> token:978 -> rights; source stored/closed | U1 source fields/sd/rights | actual rights/noninherit mismatch fails | S/A | real source grant and handle rights |
| One restricted constructor and deny-only groups; C4/R6 | P run -> restricted_token:1001 | U1 derived, disabled_groups | constructor or group mismatch prevents resume | S/A | constructor semantics and permitted groups |
| Derived SAME rights/Low IL/policy3/B01; C4/R6 | P restricted_token:1001 -> SetTokenInformation, enforce_token:622 | derived rights, privileges/LUID/attributes, integrity/policy | no privilege repair; failure blocks admission | S/A | Low setting, ChangeNotify-only enabled, mandatory policy |
| Source/derived/child token reconciliation; C4 | P enforce_token:622; token/drift at suspended and READY paths | U1 source, derived, child-suspended, child-READY | discrepancies/SD drift fail | S/A | assigned-token differences and legal attribute conversion |
| X-L/P-L/X-M descriptors; D4/C4 | P Descriptor:725/target_sd:745 used in configure_job/run/create/workers; O New-XM-SA:503/Admit-XM:586 | SD raw/decoded owner/ACL/label, worker and pipe rights | invalid/readback mismatch fails; no descriptor repair | S/A/PS | actual creation-returned descriptors and access |
| Sole job, effective limits; C4/R4 | P configure_job:1041 -> job_observation:1073 -> cleanup | job-configured flags/memory/user_time/ui/end_action; resources | readback/membership/descendant mismatch fails | S/A | job nesting/UI/quota behavior; 64 MiB/8/5-second suitability |
| Medium exact two writes/ordinary SDs; R3 | O preflight:790 -> two CreatePipe -> attribute list -> CreateProcessW:872 | Medium-pipe descriptors/rights; admission record | one attempt, no alternative API or retry | S/PS | ordinary pipe/Medium descriptor compatibility |
| Suspended Medium admission and rights; R3 | O Admit-Medium:485 plus pre-resume top-level path | P retained PID/time/image/SD/token/rights | no resume until checks/readers ready; exact stop on failure | S/PS | masks 0x00121401/0x00120042, full handles and query timing |
| O command/environment/nonce/O0; R3/R4 | O Quote-Arg, environment/argv:864-872; P main:1734 | P0/O0/source_hash/nonce | ambiguous/expired/future metadata fails | S/A/PS | actual quoting/environment propagation |
| Low exactly three approved writes; D3/D4 | P run:1362 pipe setup -> create:1241 | write rights, CREATE_RESULT, parent/suspended inventory | exact HANDLE_LIST; exclude read/token/job/outer references | S/A | Windows inheritance and numerical handles |
| Low creation-time JOB_LIST and X-L SDs; D3/C4 | P create:1241 -> sole CreateProcessAsUserW:1276 | BEFORE_LOW_ATTEMPT, CREATE_RESULT; Low-identity/SD/job | one attempt/no postassign; 1314 fails without repair | S/A | quota exception/API success and assigned job |
| Low four-variable env/frozen literal; C4/D3 | P environment helper/create:1241; literal and accept_line:1293 | literal bytes/hash; READY environment/argv/cwd/modules | mismatch or unknown imports fail | S/A/H | actual startup under three-/four-variable blocks |
| Suspended Low admission; C4/D4 | P run after create:1362 -> token, target_sd, identity, membership/inventory | child-suspended, Low-identity, job pids, suspended/complete | failed admission never resumes child | S/A | descriptor/token/image/handle snapshots |
| Parent census and excluded sentinel; C4/U3 | P run sentinel -> bounded_inventory:1489 -> inventory:1115 | parent/complete, sentinel identity/rights | cap/incomplete/unmatched forbidden object fails | S/A | finite census/API support |
| Suspended/READY PSS and object identity; C4/U3 | P inventory:1115, compare_inventory:1179, bounded_inventory:1489 | suspended/complete, READY/complete, object comparisons/original flags/access | PSS/NT unsupported -> partial; mismatches fail | S/A | PSS ABI/NT rights, complete bounded census |
| Runtime opens versus inheritance; C4/U3 | P compare_inventory:1179 during READY path | classified runtime handles, query-only self token compare | parent match/forbidden inherited object fails | S/A | stock Python runtime handles and object comparison |
| Three streams READY/END grammar; C4/U2 | literal -> P NativeReader:1697/drain:1340/accept_line:1293; O Validate-LowStreams:697 | LOW_BYTES, READY/END per stdout/stderr/ledger | wrong order/identity/extra bytes/missing records fail | S/A/PS | runtime bytes, console absence and import output |
| Redundant writes and three EOFs; C4/R4 | P run closes write/reference duplicates before resume; cleanup:1515 | Low_EOF, worker/owned_remaining ledger | unresolved EOF/worker/handles -> UNKNOWN | S/A | actual EOF and cancellation |
| Shared 10/5/20 budgets; R4 | P tick:905/cleanup_end:912/run/cleanup; O O0:868 monitor/finally | uptime offsets, F/end_tick, stop/last-active/first-zero | deadline stops; no extension or hard-latency guarantee | S/A/PS | API latency, scheduling and clock epoch |
| Bounded native readers/observers; R4/C4 | P NativeWorker:1648/NativeReader:1697; O Start-Reader:512/Start-TokenQuery:533/Await-TokenQuery:568 | queue/cancel/join/outstanding_workers | bounded waits; preserve live storage; UNKNOWN if unjoined | S/A/PS | callbacks/runspaces, cancellation and storage lifetime |
| Byte-preserving relay/schema/sequence; R4/C4 | P emit:916/drain:1340; O Receive-Relay:655/Drain-Medium:724 | schema L65-RP2-RELAY-1, sequence, lengths/hex | encoding/sequence/lost bytes fail | S/A/PS | actual stream scheduling and relay integrity |
| Sole O evidence owner/fresh reparse-free leaf; R4 | O Check-Route:592/Write-Artifact:632/preflight/finally | artifacts/files lengths/hash report | drift/existing leaf/write error fails; no P files | S/PS | filesystem race/permissions/leaf creation |
| 1 MiB all-representation accounting; R4/C4 | P retain_metadata:890/reserve_parse:897/emit:916; O Charge:604/Retain-O:611 | highwater, retained bytes, remote/live reservation, reserve | reserve-before-write/overflow -> failure, no PASS | S/A/PS | accounting adequacy and memory/disk logical bounds |
| Exact O finite at-most-one stop; R4/R5 | O Stop-Exact:754/monitor/finally | terminate_calls, P_signalled, P_exit, Medium_EOF | retained-handle request only, missing cessation UNKNOWN | S/PS | stop/wait behavior, never whole-tree guarantee |
| P failure cleanup and sole job last; R4/R5 | P cleanup:1515 -> cleanup_close/worker waits/drift/last job | Low_signalled/job_zero/Low_EOF/errors/owned_remaining | cleanup continues through evidence errors; unresolved UNKNOWN | S/A | no-child/unknown-create races, last-handle effects |
| Cessation-dependent classification/alert; R5/owner OUTER-1 | P cleanup FINAL; O final checks:984-1024/Alert-Unresolved | cessation_confirmed, O_independently_observes_Low=false, verdict/operator_alert | missing Low evidence UNKNOWN, never PASS | S/A/PS | P loss/unassigned child risk; operator reporting |
| Scientific/production boundary; C4/C6 | P/O fixed constants, literal/imports, terminal report | scientific_claim/scientific_isolation | no extra workload, production compatibility not asserted | S/A/H | no production venv qualification in RP-2B |
| Exact bytes/static-only/conditional publication; C5/C6 | review manifests and this matrix; no source review result authorizes execution | identities/static results/A-D verdicts/publication receipt | any unauthorized invocation stops; BLOCKED prevents publication | S/H/A/PS | separate owner RP-2B grant after verified publication |

## Review and interpretation limitations

Implementer-reported text AST, literal guard, ParseFile/ParseInput, FFI arity/
API-call census, encoding/materialization checks and editor diagnostics passed.
No target invocation/import, Add-Type, compilation, token/job/process trial,
tests or fixtures was reported during this correction. That is a declared
procedure record, not an independent runtime forensic audit.

The earlier attempted-wrapper-invocation incident remains in the immutable
blocked handoff and is not erased by corrective parser results.
Implementation completeness, precise ABI/ownership and accounting adequacy are
pending independent A-D review; runtime feasibility is explicitly not inferred.

## A1/A2 successor mapping - renewed review identity

**Status:** Frozen successor for same-byte independent A-D follow-up; not PASS.

| Source | Successor checkout SHA-256 | Successor Git-clean LF blob |
|---|---|---|
| P, 1,791 lines | `B8F669C68ED5768E4126FFA87E855002A5E7E5E116999E81E4AAE1CA69CE2427` | `e76c2abf728072315c779da990cf9a5e445f1a00` |
| O, 1,042 lines | `F7C39C0FC849F61AFFF71A07AC8DCC7BDBEBA91D9971B44BCCF96B0C01ABE2A7` | `3c29b21952e08100da2779c1a7fb02dcc930acdf` |

Initial pair remains preserved in session `files/rp2ar1-reviewed-pair/`.
Only two source hunks changed: P 11 additions/2 removals; O 10 additions/
1 removal. Literal and frozen requirements unchanged.

The original obligation rows continue to map unchanged functions. Adjust
all P locations after the A1 hunk by +9 (bounded_inventory 1498, cleanup 1524,
NativeWorker 1657, NativeReader 1706, main 1743). Adjust all O locations after
the A2 hunk by +9 (catch 943, finally 948, terminal checks 993-1033).
Before those hunks locations are unchanged. The following replaces the
original token-reconciliation/drift mapping:

| Obligation / contract | Connected successor location | Evidence and failure | Static method | Runtime qualification |
|---|---|---|---|---|
| A1 admitted token identity and SD binding through last use; R6 | P Controller.run 1452-1469, runtime comparator still 1190-1194 | READY/admitted CompareObjectHandles result; original child_sd used for READY and both final drift checks after comparison; unexpected identity/semantic drift fails; references close afterward | S/A plus renewed A review | NOT RUN: object identity and semantic versus byte drift |
| A2 O/P final SD readbacks and byte-only difference reporting; R6 | O top-level 914-927 | bounded O-token-final-readback/P-token-final-readback records include actual fields/SD, raw_equal and semantic_equal; accounted retention; records before rejection/closure; record/accounting errors propagate | S/PS plus renewed A/C review | NOT RUN: actual descriptor representation drift and evidence budget |

Medium source already-enabled ChangeNotify has published direct/R1 support
distinct from Low B01. The same-context O/P admission checks remain unchanged;
no privilege enabling/repair or profile amendment is introduced. Reviewers
must determine compliance rather than infer it from this interpretation.

## Integrated successor review

Renewed A/B/C/D independently reviewed both successor identities above and
returned **PASS - RP-2A SOURCE COMPLETE; READY FOR SEPARATE RP-2B
AUTHORIZATION REVIEW**. Initial A1/A2 BLOCKED findings and the initial
corrective pair remain historical; the successor supplement is the current
source binding. No lane PASS is runtime evidence or an execution grant.

Conditional publication requires independent exact staged-package verification.
The completion handoff records the six-path allowlist and remaining RP-2B
owner/host/command/evidence/operator/qualification prerequisites.
