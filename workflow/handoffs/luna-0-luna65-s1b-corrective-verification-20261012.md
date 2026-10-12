# Luna-0 Handoff — Luna-65 S1-B Corrective Verification

Gates: `L65-PHASE2A-S1B-CRLF-EVIDENCE-CORRECTION`, `L65-PHASE2A-S1B-VERIFIER-IDENTITY-CORRECTION`

## Dispositions (kept separate)

- **Original result (historical, unchanged):** `GENERATOR_FAILURE / EVIDENCE_REJECTED`. The original verifier (SHA-256 `27D5969035DAE923CADC3518D2C1A398CEB3413EAB702A4298E71FE2F1EB7D6E`, blob `2170dc8c8bd1ceb734136d9b4ed36bb47b55c916`) exited 3 with 49 PASS and 1 FAIL (check 13, stdout line ending).
- **Corrected result:** `S1-B RETAINED EVIDENCE VERIFIED — FITS_WORST`, produced by the corrected verifier reading the original single-execution evidence. The corrected verifier was NOT used for the original S1-B execution; the wrapper bound the original verifier hash.

## Original execution identity (unchanged)

- Source commit `5f089035c9582f6e1d3daae92fc825307c3ae57d`; run ID `20261012T180000Z-a3f19c5`; one generator invocation, consumed; zero retries.
- Generator blob `088d569c1787e08e3995d10d94aade8517093093`; wrapper SHA-256 `07BCCEE260B8BBAFF8B0FA5F56D657E470AA7B4EF105D24060D472AAB19802A1` (blob `99b1127ecfef683c2769e24451bf7e825ba7a030`).
- Original evidence (root `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\phase2a-sizing`), verified unmodified after re-verification:

| File | Bytes | SHA-256 |
|---|---|---|
| `20261012T180000Z-a3f19c5\results.jsonl.gz` | 516,918 | `43D4EC66A486A801E3A95C9A0730299EB2F092942127DE279872F7911596AAB2` |
| `20261012T180000Z-a3f19c5\sha256.json` | 243 | `097423E4B85FF15983FE4664EF58AE05394EDFCA3661214F8F0323875055539E` |
| `20261012T180000Z-a3f19c5\sizing.json` | 2,222 | `B3FD0F9C4F34284E372A7B1294AF4663EAFBE17BB624CF4EC55A0F3A1FF52269` |
| `20261012T180000Z-a3f19c5.wrapper\invocation.lock` | 189 | `7F3B4225DFD8453149C79BE862F63CAAAF9AD3FC90637E0A1A0FED6D538F01BC` |
| `20261012T180000Z-a3f19c5.wrapper\wrapper.json` | 1,736 | `28B90C1FC5AE18A26C4245B68E989C9D9792903DA442120D5AC02CD37DC7FAC9` |

## Diagnosis

`wrapper.json` stdout is exactly `FITS_WORST retained_bytes=519383\r\n`. The generator writes the summary with a terminal LF (`sys.stdout.write`); Windows text-mode capture produced CRLF. Class and number equal the recomputed values; the only difference is the terminal newline.

A second discrepancy was found: check 2 (verifier identity) compares `wrapper.json.verifier_sha256` with the running verifier's own hash, which fails by construction for any corrected verifier. The owner authorized a narrow second correction (gate `L65-PHASE2A-S1B-VERIFIER-IDENTITY-CORRECTION`).

## Corrective diff (only file changed: `scripts/luna65_phase2a_ledger_sizing_verifier.py`)

1. Added constant `ORIGINAL_VERIFIER_SHA256 = "27d5969035dae923cadc3518d2c1a398ceb3413eab702a4298e71fe2f1eb7d6e"`.
2. Check 2: compares `wrapper.json.verifier_sha256` to `ORIGINAL_VERIFIER_SHA256` (check remains active; the corrected verifier's own hash is reported in the detail field only).
3. Check 13: stdout must equal the summary plus exactly `\n` or `\r\n` (no stripping); `stdout_truncated is False` retained.

No imports added; no checks removed; the total remains 50.

## Corrected verifier identity

- SHA-256 (CRLF worktree) `D6FE8CBF8D82D077E4AD5FFF552570C7A6BBE97C79A25E91A8A5435C4D7DA996`
- Git blob `4bfdb74620b6bff2d53bde1aed762c05f3600e14`
- Static checks: ASCII-only, CRLF consistent, AST parse and compile OK, import allowlist unchanged.
- Independent review (rubber-duck lane A, agent `e20379f7-7ced-43b5-acd4-749daa5caa0e`): PASS.

## Re-verification (single read-only invocation)

Interpreter Python 3.11.4, flags `-I -B`, verifier args: `--run-root <run> --wrapper-dir <run>.wrapper --repo-root C:\Users\Patrick\Documents\ActiveCode\TPCN --expected-wrapper-sha256 07BCCEE2…02A1`.

- Exit 0; 50 of 50 checks PASS; `VERDICT VERIFIED_FITS_WORST`, `FINAL FITS_WORST`.
- Report (outside the original evidence): `C:\Users\Patrick\AppData\Local\TPCN\corrective-verification\corrected-verifier-report.txt`, SHA-256 `66DB3DC00A77E81F9C6DBFFE414FB9B2D08DCC2EBB110BD5A747330F97AF39BA`.
- 8,196 records; gzip 516,918 bytes vs 786,432 allocation (margin 269,514); output directory 519,383 bytes; aggregate retained 521,308 bytes vs 1,048,576 cap.
- No generator or wrapper rerun; original evidence files unchanged.

## Scope and residual limitations

Establishes only that the constructed width-bound synthetic ledger fit in this single invocation. Not established: universal worst-case compression bound, nominal-profile fit, two-run determinism, runtime E2 capacity, qualified resource enforcement, Spiral efficacy. No Job Object or qualified supervisor; memory unmeasured and unenforced; CPU/wall guards cooperative; `taskkill` best-effort; same-user tampering not prevented.

## Boundaries

Generator/wrapper rerun, supervisor implementation or qualification, Windows RP probes, Phase 2A/2B fixtures: NOT AUTHORIZED. Full Spiral and Luna-64 corrective execution: BLOCKED. Luna-63C: FROZEN. The supervisor scaffold and the local authorization record remain unpublished.
