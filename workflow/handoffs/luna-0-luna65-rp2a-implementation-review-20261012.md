# Luna-0 Luna-65 RP-2A implementation and static-review handoff

**Gate:** `L65-PHASE2A-RP2A-IMPLEMENTATION`
**Date:** 2026-10-12
**Status:** BLOCKED - RP-2A IMPLEMENTATION INCOMPLETE; all four independent
same-byte A-D reviews complete. No conditional publication.

## Affirmative adoption and verified authority

Luna-0 affirmatively adopts the owner's current instruction authorizing only
two new executable sources and the published candidate's nonexecuting static
checks. RP-2B execution is NOT AUTHORIZED. This record does not change any
historical contract or claim implementation review has passed.

Verified HEAD and authorized branch:
`f47c48a947e48867c629817fa1031cb93729e440`,
`governance/luna64-r4.3-freeze-20261010`.

| Frozen input | Verified identity |
|---|---|
| R1 CRLF checkout SHA-256 | `F9913AC44C268291988F549A110B2EFCC4777139A2BB8BD0DA407DF020FABEFB` |
| R1 published Git blob | `8abb50dfef732da71cee94b1623c61b3f4f8e49e` |
| R1 published LF SHA-256, verified in publication record | `3687B832C403F55B3B1085510784C902B70BC0F6B523C8A3F64A95E52ED48CD8` |
| RP-2A candidate checkout SHA-256 | `4C4420998DE2B87745F8F7565B4CCA5B1CDBE7A619E9DE804D38BC1A5D07D9AE` |
| RP-2A candidate Git blob | `97615eda16190c82e977cf71a7ba0439cad84e13` |
| Frozen Python executable SHA-256 | `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F` |

Frozen interpreter:
`C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe`.
File resources read without launch report Python 3.11.4.

Implementation ownership is limited to:

- `scripts/luna65_phase2a_rp2_compatibility_probe.py`
- `scripts/luna65_phase2a_rp2_outer_wrapper.ps1`

No helper module or generated binary is authorized. Additional changes are
limited to reviewed implementation governance and identity records.

## Preserved exclusions

The untracked supervisor scaffold remains SHA-256
`67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`.
The excluded local S1-B final authorization record remains SHA-256
`BB9134CB7FF1813D495575FA80F912EEFB6E6A7C7A86F720CDAD829CAC925451`.
Neither is modified or staged.

## Static-validation boundary

Targets must never be imported, invoked, dot-sourced or used by a self-test.
No Add-Type/native interop execution, token construction, Job Object creation,
process launch, runtime tests, dependency changes or compatibility probe is
permitted. Only source-text parsing, inspection, hashes, Git and permitted
editor diagnostics are authorized.

The observed text-parser host is existing Windows PowerShell 5.1.19041.6456,
`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`, SHA-256
`9785001B0DCF755EDDB8AF294A373C0B87B2498660F724E76C4D53F9C217C7A3`.
This binds permitted ParseFile/ParseInput checks, not a future RP-2B launch
approval. No target wrapper or embedded native code is executed.

## Required disposition

All four independent lanes must review identical final source bytes:
A security/token/FFI, B interpreter/inheritance, C lifecycle/evidence, and
D governance/provenance. Integrated PASS is static source review only.
Publication is conditional on integrated PASS and exact staged-byte review.
On BLOCKED, preserve source and findings without claiming execution readiness.

Missing required Low cessation evidence must remain
`RP2_UNKNOWN_FAIL_CLOSED`, with explicit operator alert that containment is
unresolved. Direct-base Python does not establish production venv compatibility.

RP-2B, RP-3, production supervisor implementation/qualification and Phase 2A/2B
fixtures are NOT AUTHORIZED. Full Spiral and Luna-64 corrective execution
remain BLOCKED; Luna-63C certification remains FROZEN.

## Frozen partial source identities

The implementer returned incomplete sources, not a working controller.
Both files are ASCII CRLF without trailing whitespace, independently checked.
These exact bytes are frozen for all four review lanes; no source is staged.

| Source | Checkout SHA-256 | Raw Git blob | Git-clean LF blob |
|---|---|---|---|
| Probe | `61878844D02DFF788E295068ED641EB9139EAB9E93FC173036D988C4AF50443C` | `55d33d74be390480392c46bd502c8e99077d676e` | `97892008cacfb74c4ea30b6b4af63930699a0b2a` |
| Outer wrapper | `B91AD9764733DEDD7D2EB052047B5121B1DF3F3BD71D639D5FEA4328C907A19B` | `99c88ca3aface71d6a6afb463008617096e60b5c` | `e87058d84fbb521a278c9a233a306af98cbc8a9c` |

Implementer-reported text checks: probe and literal AST parsing passed using
the hash-bound base interpreter with parser-only `-I -S -B`; replacement
PowerShell encoded-command ParseFile passed. No probe import or bytecode
generation was reported. Embedded C# was neither compiled nor semantically
validated. Literal: 6,583 ASCII bytes, SHA-256
`D9EC540BCEA9326C67A791DA6C59FC11357C00396B707EEB9FE278FCD08BF2A0`.
These are parser/source observations, not compatibility evidence.

Unfinished obligations include effective startup/import/DLL/pytest and outer
host/compiler closure, both admission controllers, Low token/job/pipe
construction, U1-U3/PSS/object observations, 10/5/20 timing controllers,
bounded byte-preserving evidence accounting, and finite cessation/cleanup.
Static user-site pywin32 hook discovery is a dependency-binding question,
not demonstrated runtime incompatibility. Refusal barriers do not fulfill
these implementation obligations and do not justify publication.

## Nonexecuting-validation boundary incident

The implementer disclosed a prohibited wrapper invocation attempt during the
initial syntax check. A nested absolute `powershell.exe -Command` lost quotes
in native argument serialization; the assignment RHS became an unquoted
wrapper path, which PowerShell attempted to invoke.

The reported error was `MissingMandatoryParameter` for `RunId`, `EvidenceLeaf`,
`ReviewedProbeHash` and `ReviewedWrapperHash`. Parameter binding rejected
the attempt before the wrapper body; no separate target Python process,
wrapper child process, token/job/native API execution was reported.
This is a no-invocation boundary breach even though the body did not run.
The body-nonexecution account is supported by reported parameter-binding
diagnostics, not a separate runtime forensic audit.

The original tool's overall exit code zero came from later Git commands, not
parser success. That check is INVALID, and its success-shaped exit is not used
as validation evidence. A later explicitly encoded ParseFile-only command
passed without evaluating target source.

The exact command, diagnostics and successful replacement parser commands are
retained in the session tool artifact:
`C:\Users\Patrick\AppData\Local\Temp\1791836862170-copilot-tool-output-ca0b2028c900499f90f85df516437a25.txt`.
No incident command is repeated. No explicit bytecode, assembly, helper or
evidence-leaf artifact was reported; incidental parser-host caches were not
inspected and their absence is NOT certified. Infrastructure generated tool
output spill files outside the repository. Excluded-file hashes remain intact.

Publication remains prohibited without integrated implementation PASS.
The sources and findings are preserved locally on BLOCKED; RP-2B is not
authorized and no compatibility invocation is claimed.

## Independent same-byte implementation review integration

All lanes independently verified the exact source pair above and frozen
baseline. A/B/C/D returned **BLOCKED - RP-2A IMPLEMENTATION INCOMPLETE**.
Lane B retracted its unsupported source-truncation/syntax finding after
reading the full tail and reverifying the unchanged 547/217-line sources.
Its corrected report, not the erroneous truncation finding, is integrated.

| Lane | Verified findings |
|---|---|
| A - security/token | Source mask 0x2008B is declared but construction/admission paths are absent. Token-object descriptor helper is not integrated; user/group/integrity validation is incomplete. X-L descriptor construction and handle ownership are absent. Probe 537-543 and wrapper 211-217 explicitly refuse/incomplete. |
| B - interpreter/inheritance | Image/version/architecture checks are not integrated; startup/import/DLL/host closure is incomplete. Two-write Medium and three-write Low launch/admission, U2 parsing and U3/PSS controllers are missing. Quote/environment helpers and the complete literal do not supply orchestration. Source-truncation finding fully retracted. |
| C - lifecycle/evidence | No O0/P0 timing, once-only retained-handle stop controller, job-limit configuration/readback, bounded readers/cancellation/EOF, aggregate reserve accounting or cessation-verdict integration. UNKNOWN alert helper is not called. |
| D - governance/provenance | Frozen identities, new-source allowlist, historical preservation and excluded hashes verified. Incomplete sources/closure prevent publication. No-invocation incident confirmed with execution-extent caveat retained above. |

These are missing implementation deliverables, not evidence that Windows
execution fails or that the reviewed design must be relaxed. Hostile denial
tests outside approved U1-U3 claims are not newly imposed requirements.
The required sentinel/inheritance observations remain missing.

No source changes are made while these reviewed bytes are frozen. No commit,
push, fetched-source publication, compatibility consumption or readiness
claim is made. Any completed successor bytes require fresh exact-byte review.

Corrected Lane B full report retained:
`C:\Users\Patrick\AppData\Local\Temp\1791837142622-copilot-tool-output-8b1b9b48d73d43f183e3bb8771cb98b4.txt`.
Luna-0 preserves the reviewed source pair and findings and stops at this
BLOCKED disposition. No actual RP-2B command, run ID or evidence destination
is authorized.

## RP-2B prerequisites, not authorization

Complete missing RP-2A obligations without relaxing frozen requirements;
freeze complete source/literal/startup/host identities; obtain fresh same-byte
independent A-D PASS, exact staged-byte/newline verification, and conditional
commit/push/fetch publication verification. Reconcile the procedural incident
before presenting a readiness claim.

Only afterward may the owner consider a separate RP-2B grant binding the
verified implementation revision/hashes, interpreter and attended host,
exact command/run ID, approved evidence destination and preflight, operator,
one-invocation/zero-retry policy, 10/5/20 envelope and fail-closed termination/
cessation limitations. None of those execution permissions is granted here.
