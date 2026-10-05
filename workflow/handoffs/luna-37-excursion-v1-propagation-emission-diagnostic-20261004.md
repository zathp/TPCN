# Luna-37 Handoff — EXCURSION_V1 Propagation-to-Emission Mechanism Diagnostic

## Starting revision
`905ee21343ef5a69770f49e40966a40bcc40b0f5` (`main == origin/main`, clean). Luna-34 remains historically BLOCKED / UNDETERMINED; Luna-33 and ACP-0007 unchanged.

## Files added (contract-owned only)
- `run_luna37_excursion_v1_propagation_emission_diagnostic.py`
- `tests/test_luna37_excursion_v1_propagation_emission_diagnostic.py` (7 tests)
- `artifacts/acp0007-luna37-propagation-emission-diagnostic/{config,results,summary}.json`
- this handoff

No production, governance, or Luna-33/34/35/36 files were touched. The Luna-34 runner is imported read-only.

## Execution
Luna-34 fixture unchanged (seeds 0-4, 64 characters, 3 conditions = 960 executions, same streams, bounds), plus `eligibility_capacity=1024` via the Luna-36 API (predeclared, untuned, not retried). Run once; the full workload was replayed a second time internally.

## Results
| Condition | Source emitting chars | Source emissions | Routed transfers | Dest receptions | Dest state changes | Dest canonical emissions | Max route depth |
|---|---|---|---|---|---|---|---|
| NO_EDGE_CONTROL | 297 | 1715 | 0 | 0 | 0 | 0 | 0 |
| DEFAULT_STATIC_EDGE | 297 | 1715 | 1715 | 1715 | 1715 | 0 | 1 |
| STATIC_N2_BOUND_SENSITIVITY | 297 | 1715 | 1715 | 1715 | 1715 | 0 | 1 |

- Maximum destination pre-threshold decayed magnitude: 1.318e-06 (w=1), 2.038e-06 (w=2), against threshold 1.
- Per-seed destination emissions: 0 in every seed and condition.
- No incomplete characters; no legal candidates.

## Capacity / occupancy evidence
- Effective capacity 1024 per ledger in every character (both ledgers); runtime property 1024.
- Creations 1715 per condition; removals 0; peak and max final occupancy 19 (< 1024). All ledgers reconcile (`0 + created - removed = final`).
- No `EligibilityCapacityError`. Previously blocking Luna-34 character (seed 0, index 4) now completes with 18 creations > 16.

## Determinism
Replay digests equal: `abc52f98491be836445930eccb4bbf8988b61568b15e9d7633bbe20277390a7f`.

## Terminal classifications
- `DESTINATION EMISSION ABSENT IN ALL CONDITIONS`
- No-edge control is a valid negative control (zero transfers/receptions; not contaminated).
- Not emitted: `PRESENT UNDER DEFAULT`, `PRESENT ONLY UNDER N2`, `STATIC N2 CHANGES RESULT`, `INCONSISTENT WITH POST-LUNA-33`, `BLOCKED`.

Reception/state change occurred in every routed transfer but never reached canonical emission. This is consistent with the post-Luna-33 interpretation for this single fixture.

## Validation
- Focused Luna-37 tests: 7 passed.
- Full suite: 952 passed, 1 skipped (CUDA), 953 collected (baseline 945/946 + 7 new tests).
- compileall clean; `git diff --check` clean.

## Prohibited conclusions
No claim of efficacy, candidate formation, growth, generality, accuracy, or that an architecture change is or isn't required. Absence of emission here is limited to this fixture, these three conditions and bounds.

## Unresolved questions
Whether any bounded configuration (outside Luna-37's scope) yields destination emission remains for Luna-0 to decide. No Luna-38 is authorized.
