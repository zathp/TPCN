# Luna-0 Handoff — Luna-65 S1-B Verifier and Wrapper Implementation

Gate: `L65-PHASE2A-S1B-VERIFIER-WRAPPER-IMPLEMENTATION`

Status: **IMPLEMENTED, NOT EXECUTED. S1-B EXECUTION: NOT AUTHORIZED.**

## Authorization and baseline

- Owner authorization: S1-B verifier and wrapper implementation (non-executing); decisions D-S1B-1 to D-S1B-5 adopted.
- Baseline commit: `86bf3fd16a6105300124751260e6b1de80b14538` (S1-B execution contract).
- Generator (unchanged): blob `088d569c1787e08e3995d10d94aade8517093093`, CRLF SHA-256 `DD2A3DF5D51F234B9A90F8C58F69ED84CDD02DC5B9379B1D19A71CB15D719212`.
- S1-B contract (unchanged): blob `b251e3d09d7e12d1008b34ec3e8c3dd2dbd6e3a2`.
- Blocked supervisor scaffold: untracked, unmodified, SHA-256 `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`.

## Implementation files (allowlist)

| File | Role |
| --- | --- |
| `scripts/luna65_phase2a_ledger_sizing_verifier.py` | Read-only independent verifier (stdlib: gzip, hashlib, json, pathlib, sys, zlib) |
| `scripts/luna65_phase2a_s1b_wrapper.ps1` | Frozen attended PowerShell 5.1 wrapper path |

Identities (worktree CRLF SHA-256 / Git blob, as reviewed in this revision):

- Verifier: `27D5969035DAE923CADC3518D2C1A398CEB3413EAB702A4298E71FE2F1EB7D6E` / `2170dc8c8bd1ceb734136d9b4ed36bb47b55c916`.
- Wrapper: `07BCCEE260B8BBAFF8B0FA5F56D657E470AA7B4EF105D24060D472AAB19802A1` / `99b1127ecfef683c2769e24451bf7e825ba7a030`.

The wrapper requires `-ExpectedWrapperSha256` and the verifier hashes the wrapper file itself; both `invocation.lock` and `wrapper.json` are written in the same canonical JSON form (sorted keys, compact, ASCII-escaped, trailing LF) that the verifier requires. `taskkill` is bounded (5 s) and a hang fails closed.

## Interfaces

Wrapper: `-RunId <yyyymmddThhmmssZ>-<7 hex> -ExpectedVerifierSha256 <hex> -ExpectedWrapperSha256 <hex>`. It writes `<parent>\<run-id>.wrapper\invocation.lock` and `wrapper.json` (schema `luna65-s1b-wrapper-v1`, at most 16,384 bytes) next to the generator output directory `<parent>\<run-id>`. Parent: `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\phase2a-sizing`, which must be pre-created and empty. The interpreter is the base Python 3.11.4 with `-I -B`. Exit codes: 0 COMPLETED, 10 not completed, 20 preflight failure, 21 not confirmed, 30 log write failure. The wrapper does not run the verifier.

Verifier: `--run-root --wrapper-dir --repo-root --expected-wrapper-sha256`. Output `VERIFIED_<CLASS>` / `FINAL <CLASS>` (exit 0), or `EVIDENCE_REJECTED` / `FINAL GENERATOR_FAILURE (evidence rejected ...)` (exit 3). The verifier does not trust the generator's fit declaration; it rebuilds all 8,196 records, replays the LCG, validates the gzip stream and sizes, and counts the aggregate retained bytes (output + lock + wrapper.json <= 1,048,576).

## Validation performed (non-executing only)

Source inspection, SHA-256, Git blob, line-ending and trailing-whitespace checks, AST import and forbidden-API scan, in-memory Python compile, PowerShell parse-only syntax check, allowlist `git status`. Nothing was imported, invoked or run.

## Limitations (unchanged and disclosed)

No Job Object; `taskkill /T /F` is best-effort; whole-tree termination is not established; CPU and wall guards are cooperative; memory unmeasured and unenforced; same-user tampering (D-R7P-2) unresolved; PID-reuse false positives fail closed; no gzip is retained for EXCEEDS/failure outcomes so record content cannot be verified there.

## Remaining prerequisites before S1-B

1. Owner decision on D-R7P-1 (still undecided).
2. A fresh owner execution authorization naming the final published commit, verifier and wrapper identities, and the run id.
3. Luna-0 preflight and attended execution under that authorization, then read-only verification.

## Boundaries

S1-B execution NOT AUTHORIZED. Supervisor implementation and qualification NOT AUTHORIZED. Windows RP probes NOT AUTHORIZED. Phase 2A/2B fixtures NOT AUTHORIZED. Full Spiral BLOCKED. Luna-64 corrective execution BLOCKED. Luna-63C FROZEN.
