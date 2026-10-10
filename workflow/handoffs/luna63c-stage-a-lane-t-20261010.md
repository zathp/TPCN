# Luna-63C Stage-A Lane T (N3 event-time mapping) handoff

**Verdict: T BLOCKED — N3 NOT CLOSED.** 9 of 191 frozen events certified; 182 blocked. Certificate work only; no E, Lane S/N5, Stage B, runtime/candidate implementation or scientific C0–C7 execution ran. No architecture/ACP/A01–A15/field/fixture/cap change.

- Branch/worktree: `experiment/luna63c-stage-a-T`, `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna63c-T`, based on W COMPLETE `17907c67d52cc338249b66f28c3179cd97572c6e`.
- Owned: `experiments/luna63c/certificate/lane-t/**` (`convert.py`, `test_lane_t.py`, `inventory.json`, `schedule.json`, `manifest.json`, `.gitattributes`) and this handoff.
- Pins verified in code/tests: fixtures.json canonical SHA256 `AF81F339…70FB` (blob `8c4f9d20…`), FIXTURE_FREEZE.md SHA256 `B3BB25D6…667F` (blob `fc3d883e…`), W matrix SHA256 `0B5AB09A…0D9F`; source head `19caa49d…`, publication `583148e2…`, N4 `9cc92adb…`, arithmetic `87179ba2…`, design `3e7d31b9…`.
- W material consumed only from the committed lane-w matrix (exact rational enclosures at 256/512 bits). Parent untracked W/T/E artifacts were not used.

## Counts
- Events 191 = C1 2 + C2 31 + C3 4 + C4 8 + C5 24 + C6 3 + C7 119. Plus 15 observation-only rows (no N3 event).
- C7 reconciliation: 119 identities = DUPLICATE 5, ALTERNATING 16, RESET_BEFORE 7, RESET_AFTER 11, STALE 7, REARM_BEFORE_QUIET 12, EXP_COAL_VALID 4, EXP_COAL_INVALID 4, TIMESTAMP_INVALID 12, OVERFLOW_17 25 (ranges expanded), POST_ABORT 1, OUTPUT_EXPIRY_COALESCENCE 6, NEAR_CLOCK 3, POSITIVE_SUB_ULP 6. Each has exactly one row. C7: 9 certified (NEAR_CLOCK 3, SUB_ULP 6), 110 blocked.
- Blocked by primary reason: ABSOLUTE_ORIGIN_t_store_UNFROZEN 85, EXTERNAL_INPUT_TIME_UNSPECIFIED 80, INVALID_TIMESTAMP_ENVELOPE_NOT_FROZEN 12, RELEASE_ORIGIN_NOT_FROZEN_NUMERICALLY 3 (C6), NO_TIMESTAMP_BY_RULE… 2 (OVERFLOW ATTEMPT, CLOSED_EPISODE_INGRESS). Exact per-row IDs and reasons: `schedule.json`.

## Why blocked
The freeze never gives numeric `t_store`, fixture origin, `tau_on/off`, `t_ext`, `t_late`, pause/reset times or destination ordinals (it states they are N3/N4 results). Nothing was guessed. Blocked rows still carry the W-certified relative source (e.g. t_store+T_life) and frozen precedence, with null time/ordinal. All of C1–C6 and the remaining 110 C7 rows are blocked this way.

## Certified (exact)
- Near-clock: t* = floor64(2^20 − T_life) is unique over W's T_life enclosure: `0x1.ffff4f6a5d2e4p+19` (ULP 2^-33). Expiry ceiling is exactly 2^20 (inclusive, in domain, strictly after the cause). Successor `0x1.ffff4f6a5d2e5p+19`: exact t+T_life > 2^20, so STORE rejected out-of-domain before any episode/timer. Ordinals: instance 1 STORE 1, expiry created 2; instance 2 STORE 1 (rejected).
- Sub-ULP (scope: A = least binary64 above q at origin t*): W enclosure gives 0 < s_q ≈ 9.8e-17 < 2^-33; both endpoints ceil to t*+2^-33 (predecessor by exact bit decrement equals t*, so strictly future). Quiet precedes expiry (due 2^20). Exact accumulated bound uses 2^-1074 TU integer units; 2^-33 TU = 2^1041 units. nextafter is not used as evidence. Order: STORE 1, EXP_CREATED 2, RECALL_ON 3 (same time as STORE, external delivery order), QUIET_CREATED 4, QUIET 5, EXPIRY_INVALIDATED 6 (t*+2^-33).
- `final_ordinal` means 1-based position in the proven per-component causal/precedence order, not a destination delivery counter.

## Not certified (exact blockage)
- Output/expiry coalescence (6 rows), expiry-coalescence valid/invalid (8), C3 expiry-tie (2): packet choices (t_ext, t_late) are functionally determined only after the unfrozen t_store, so BLOCKED. Equal-time ties elsewhere: relation is frozen (internal before external; delivery ordinal) but no schedule exists to certify. Rearm-before-quiet: rule recorded, rows blocked.
- TIMESTAMP_INVALID (12): invalid envelopes not frozen. OVERFLOW_17 (25) and POST_ABORT (1): blocked on the unfrozen instance schedule; ATTEMPT/CLOSED ingress carry no timestamp/ordinal by rule.
- HOLD durations 0/1/2 TU contribute exactly 0 active units; authored offsets 2^1074 and 2^1075 units are recorded as constants only.

## Checks / environment
- `python -m unittest test_lane_t` (11 tests: pins, counts, per-case C7 reconciliation, unique ids, blocked-row invariants, grid ceil/floor, near-clock, sub-ULP, determinism/committed match); `python convert.py --check` OK; CRLF-aware `git -c core.whitespace=cr-at-eol diff --check` clean.
- CPython 3.11.4, pure-Python exact int/Fraction on W's committed rational enclosures (gmpy2/MPFR not used or installed in T). No dependency installs.

## To close T
Freeze (outside this lane) the numeric t_store/fixture origin, external input times and coalescence packet selections; then re-run `convert.py`, which would certify the dependent rows.