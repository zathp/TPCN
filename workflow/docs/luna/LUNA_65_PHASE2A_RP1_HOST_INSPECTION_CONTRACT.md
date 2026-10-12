# Luna-65 Phase 2A RP-1 Read-Only Host Inspection — Contract and Execution-Authorization Candidate

Gate: `L65-PHASE2A-RP1-READONLY-HOST-INSPECTION`
Status: governance only. **RP-1 execution: NOT AUTHORIZED.** Nothing in this document was executed.

## 1. Baseline

| Item | Value |
|---|---|
| Branch / HEAD | `governance/luna64-r4.3-freeze-20261010` / `948f5e70a43a3524dfef6bbe8f04bbd041770fd6` (equal to remote at preparation) |
| Corrected verifier | SHA-256 `D6FE8CBF8D82D077E4AD5FFF552570C7A6BBE97C79A25E91A8A5435C4D7DA996`, blob `4bfdb74620b6bff2d53bde1aed762c05f3600e14` |
| Published U1–U8 and RP-1 candidate | `LUNA_65_PHASE2A_R7_OWNER_DECISIONS_AND_PROFILES.md` (§4 list), `LUNA_65_PHASE2A_R7_PREIMPLEMENTATION_READINESS.md` §5 and §5.1 |
| Preserved | S1-B original `GENERATOR_FAILURE / EVIDENCE_REJECTED` record, corrected verifier report (`66DB3DC0…F39BA`), all S1-B evidence. Generator, wrapper and verifier are not rerun. |

## 2. What RP-1 can and cannot establish (U1–U8)

Published RP-1 scope: U4 query and U5, with a ceiling of 30 s wall, 5 MiB output outside the repository, one invocation, zero retries. This contract keeps those ceilings.

| # | RP-1 contribution (read-only observation) | Not established by RP-1 |
|---|---|---|
| U1 | Token privileges held (`SeAssignPrimaryTokenPrivilege`, `SeIncreaseQuotaPrivilege`), elevation, UAC policy. Context only. | Whether `CreateProcessAsUser` succeeds with a restricted Low token (RP-2). |
| U2 | Interpreter chain identity: base and `.venv` paths, SHA-256, `pyvenv.cfg`, `sys.version` and prefixes read by a fixed `-I -B -c` query; Windows edition/build; PowerShell 5.1 identity. | Starting the interpreter under the Low token, UI limits, no-console, imports (RP-2). |
| U3 | none | Handle inheritance through the launcher (RP-2). |
| U4 | The invoking process integrity level and existing integrity labels and DACLs on the repository, interpreter, and evidence directories (`icacls` display). | Whether a Low process is denied `PROCESS_DUP_HANDLE`, `PROCESS_TERMINATE`, `VM_WRITE` or query rights (RP-3). |
| U5 | A **bounded sample** of integrity labels and DACLs at the profile root, `AppData`, `AppData\Local`, `AppData\LocalLow` and its children, and `%TEMP%`. | A complete enumeration of Low-labelled writable locations, and registry `AppDataLow`. A full enumeration needs its own contract and budget. The owner decision to accept or remove Low-writable locations remains open. |
| U6 | The label and relabel privilege (`SeRelabelPrivilege`) state as held or not held. | Whether a label can be attached at creation without it (RP-3). |
| U7 | `netsh advfirewall show allprofiles` policy observation. | Network non-use or enforcement. No enforcement is claimed. |
| U8 | none (accepted limit, owner decisions B and C) | Not provable. |
| Job Object API | kernel32/ntdll file version and hash only. | **Runtime availability and semantics are NOT evaluated by RP-1**; they remain documentation-based until RP-2. |

Host inspection is read-only observation. It is not runtime compatibility qualification and does not prove enforcement of any property.

## 3. Execution identity (to be frozen at owner authorization)

| Item | Value |
|---|---|
| Probe source | `scripts/luna65_phase2a_rp1_host_inspection.ps1` (candidate; untracked at preparation; Windows PowerShell 5.1; no newly implemented native code, no `Add-Type`) |
| Worktree SHA-256 (CRLF) | `E538FFC2FCC5E38A80E711440AFE4E1BC079E7413832E0BB9A8C4943034CC049` |
| Git blob | `2ac7eccd62b0d9d32c15d9f262da47379d38df73` |
| Deviation from the published candidate | §5.1 named a Python source `luna65_phase2a_windows_probe.py`. A PowerShell script with built-in cmdlets and Windows system tools replaces it so that no newly implemented native or compiled artifact (and its temporary-file side effects) is needed. The probe still launches fixed-argument system executables (`whoami.exe`, `icacls.exe`, `netsh.exe`, `git.exe`, and the base and `.venv` Python interpreters) under per-command timeouts; those native processes are part of the boundary the owner is accepting. Section errors, timeouts, start failures, nonzero native exits and skipped commands yield `RP1_PARTIAL` rather than `RP1_COMPLETE`; an unconfirmed child kill yields the final marker `RP1_UNKNOWN_FAIL_CLOSED`, which takes precedence. This needs explicit owner acceptance. |
| Run ID (frozen candidate) | `20261012T220000Z-5d2e7b4` (rule `yyyymmddThhmmssZ-<7 lowercase hex>`; must not have been used) |
| Evidence directory | `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp1` (does not exist at preparation; to be created by a separate owner-authorized directory step, with a reparse-point check, as for S1-B) |
| Output files | `rp1-20261012T220000Z-5d2e7b4.out.txt`, `rp1-20261012T220000Z-5d2e7b4.err.txt`; neither may exist before launch |
| Working directory | `C:\Users\Patrick\Documents\ActiveCode\TPCN` |
| Invocation count | exactly one; zero retries |

### 3.1 Exact command (cmd.exe is used for byte-faithful redirection)

```
cd /d C:\Users\Patrick\Documents\ActiveCode\TPCN
cmd.exe /d /c ""C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File C:\Users\Patrick\Documents\ActiveCode\TPCN\scripts\luna65_phase2a_rp1_host_inspection.ps1 -RunId 20261012T220000Z-5d2e7b4 > C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp1\rp1-20261012T220000Z-5d2e7b4.out.txt 2> C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp1\rp1-20261012T220000Z-5d2e7b4.err.txt"
```

`-ExecutionPolicy Bypass` is process-scoped only (as in the S1-B wrapper) and changes no host setting. An attending operator stops the process if it has not exited after 45 s (the script's own budget is 27 s) and records that as `RP1_UNKNOWN_FAIL_CLOSED`, with no retry.

### 3.2 Read-only command set executed by the script

| Section | Operations (all read-only) |
|---|---|
| S00 | UTC time, script SHA-256 of itself, PowerShell version/edition, bitness, user, session id, `Get-ExecutionPolicy -List` |
| S01 | `Win32_OperatingSystem` (2 s timeout), `HKLM\...\CurrentVersion` values, hashes of kernel32/ntdll/advapi32 |
| S02 | `WindowsIdentity` and role check, `HKLM\...\Policies\System` values (`EnableLUA`, `ConsentPromptBehaviorAdmin`, `FilterAdministratorToken`), `whoami /all /fo list` |
| S03 | existence, SHA-256 and size of the base and `.venv` interpreters; fixed `python -I -B -c "<print sys.version, executable, prefixes, platform>"` on each; first 20 lines of `pyvenv.cfg` |
| S04 | repository and `.venv` and evidence-parent existence, attributes and reparse flag; `git --no-optional-locks rev-parse HEAD` |
| S05 | `icacls <path>` (display only) for repository, `scripts`, `.venv\Scripts`, base interpreter directory, evidence parent, `TPCN` directory |
| S06 | `icacls` display of bounded wildcard targets: profile root children, `AppData` children, `LocalLow` and children, `AppData\Local` children, `%TEMP%` |
| S07 | `netsh advfirewall show allprofiles` |
| S08 | end time, elapsed, `RP1_COMPLETE` |

### 3.3 Prohibited side effects

No writes except the two shell redirections to the named files. The only child processes are those started by the script's `RunNative` helper (`whoami`, `icacls`, `netsh`, `git`, and the two interpreter queries), each with a fixed read-only argument string and a timeout. The script contains no `Set-*` (other than `Set-StrictMode`), `New-*`, `Remove-*`, `Out-File`, `Add-Content`, `Add-Type`, `Start-Process`, `Stop-*`, registry writes, `icacls` options other than a bare path (no `/grant`, `/deny`, `/setintegritylevel`, `/save`, `/restore`, `/reset`, `/inheritance`, `/remove`, `/T`), `netsh` subcommands other than `show`, network connections, service or firewall changes, elevation, token changes, or Job Object creation. `git` runs with `--no-optional-locks` and only `rev-parse`. The `python` queries run with `-I -B` (no bytecode writes) and import no project source. A static scan of the candidate for the prohibited tokens is part of review.

### 3.4 Resource limits

27 s internal wall budget, per-command timeouts of 4–5 s (on timeout the child is killed, cessation is waited on for up to 2 s and recorded as `TIMEOUT_KILLED_CONFIRMED`; an unconfirmed kill emits `KILL_UNCONFIRMED RP1_UNKNOWN_FAIL_CLOSED` and skips all later native commands), 45 s outer attended limit, 4,000,000-character stdout cap enforced by truncating the line that crosses the cap (`CAP_TRUNCATED`), 20 stderr lines per command, 5 MiB combined output ceiling (checked after the run). Each native child's output is buffered whole by `ReadToEndAsync` before line limits apply; that buffering is bounded only by the per-command timeout and is not an enforced memory limit. Memory is neither measured nor enforced, and no Job Object is used; the limits are cooperative or best-effort.

## 4. Evidence and provenance

- Preflight (before launch): HEAD equals the remote and `948f5e70…`; tracked tree clean; script SHA-256 and blob equal §3; evidence directory exists, is an ordinary directory (no reparse point) and is empty; neither output file exists; run ID unused; operator attending.
- After the run: record exit code, both output files' size and SHA-256, elapsed time, and the header `script_sha256` and `run_id` against the bound values. Preserve the files unmodified. Do not rerun.
- Independent review of the output (not the executor): every section S00–S08 has a matching BEGIN and END; `RP1_COMPLETE` present; no `ERROR`, `TIMEOUT`, `START_FAIL` or `SKIPPED_BUDGET` unless classified; output under the ceilings; no file other than the two outputs was created in the evidence directory; repository status unchanged.
- Expected observations (not assumptions): the current account is a non-elevated standard-integrity (Medium) token; `SeAssignPrimaryTokenPrivilege`, `SeIncreaseQuotaPrivilege` and `SeRelabelPrivilege` not held (previously reported absent); interpreter hashes `4FB049EE…181F` (base) and `B5442B36A3855E9A02E5745DB3449D8EC91F4FFEFD9CF92CC8B0535112F0F0CE` (launcher), Python 3.11.4. A deviation is recorded and classified, never corrected.

## 5. Failure classifications

| Class | Meaning |
|---|---|
| `RP1_COMPLETE_OBSERVED` | All sections complete with `RP1_COMPLETE`, bindings and limits verified. |
| `RP1_PARTIAL` | One or more sections reported `ERROR`, `TIMEOUT`, `START_FAIL` or `SKIPPED_BUDGET`; the affected U items remain unproven. |
| `RP1_BINDING_FAILURE` | Identity, preflight or header mismatch; results are not accepted. |
| `RP1_LIMIT_VIOLATION` | Output, time or file-set ceiling exceeded. |
| `RP1_UNKNOWN_FAIL_CLOSED` | The process did not exit within 45 s or cessation was not established. |
| `RP1_CONTRACT_DEFECT` | The observation contradicts the contract; return for re-review, do not waive. |

A consumed invocation is not retried whatever the class.

## 6. Owner decisions required before execution

1. Accept the PowerShell substitute for the published Python probe file (§3).
2. Authorize creation of the evidence directory `...\luna65\rp1` (directory only, with reparse check).
3. Authorize publication of the probe source before execution, or accept execution of the exact reviewed local file with its SHA-256 and blob bound. Preferred: publish first, so the executed bytes are in a verified commit.
4. Accept that S06 is a bounded sample only, that the Job Object API is not evaluated, and that U3, U6 capability, U7 enforcement and U8 are not addressed.
5. Confirm the operator and the one-invocation, zero-retry rule.

## 7. Authorization state

**RP-1 execution: NOT AUTHORIZED.**
**RP-2/RP-3: NOT AUTHORIZED.**
**Supervisor implementation and qualification: NOT AUTHORIZED.**
**Phase 2A/2B fixtures: NOT AUTHORIZED.**
**Full Spiral: BLOCKED.**
**Luna-64 corrective execution: BLOCKED.**
**Luna-63C: FROZEN.**
