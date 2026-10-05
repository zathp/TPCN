# Luna-0 Independent Post-Luna-37 Review — Propagation-to-Emission Mechanism Diagnostic

Reviewed revision: `295309866c367cfeda7e42b4a42a47e813dd88ec` (`HEAD == origin/main`, clean worktree at start).

## Verdict
**NOT SUPPORTED IN THIS SETUP** (valid experiment; hypothesis of downstream canonical emission not observed). Contract compliance: **PASS**. No production defect. No architecture change. **Luna-38 not created.**

## Contract compliance
`git diff 905ee21..295309866` adds exactly the six contract-owned files (runner, tests, config/results/summary, handoff). No production, governance, ACP-0007, or Luna-33/34/35/36 file changed. Seeds 0–4, 64 characters per seed, three predeclared conditions (960 executions), declared bounds, `eligibility_capacity=1024` once, no retry, no growth, no pruning, no efficacy endpoint, no Luna-38.

## Capacity audit (from `results.json`, every ledger)
Configured capacity 1024 for all ledgers; `initial + created − removed = final` for all; peak occupancy 19 (< 1024); 1715 creations and 0 removals per condition; no capacity errors. Predictor `max_outstanding` stayed at the declared `prediction_capacity=8`; capacity was not rescaled.

## Stream audit
For each seed, character ids, input digests and event budgets are identical across the three conditions; source-silent/emitting patterns are identical across conditions (silence is a genuine stream outcome: 297/320 characters emit in each condition).

## Independent quantitative reconstruction (from lowest-level records, not summary)
| Condition | Chars | Source-emitting | Receiving | Dest-emitting | Source emissions | Transfers | Dest receptions | Dest emissions | Max depth | Peak/final occupancy |
|---|---|---|---|---|---|---|---|---|---|---|
| NO_EDGE_CONTROL | 320 | 297 | 0 | 0 | 1715 | 0 | 0 | 0 | 0 | 19/19 |
| DEFAULT_STATIC_EDGE | 320 | 297 | 297 | 0 | 1715 | 1715 | 1715 | 0 | 1 | 19/19 |
| STATIC_N2_BOUND_SENSITIVITY | 320 | 297 | 297 | 0 | 1715 | 1715 | 1715 | 0 | 1 | 19/19 |

All totals match `summary.json`; no mismatch. Destination internal events: 0 in all conditions; all destination modes after transfer remained `N`.

## Controls and edges
No-edge control: `edge` is null, zero routed contributions, zero destination receptions/state changes/emissions, no alternate route: a genuine negative control. Default edge: source→destination, w=1, delay 1.0, reference 0, routed on every source emission. N2: identical except w=2. Transfer/payload ratio in records is exactly 1 (transformed payload already includes the weight).

## Canonical-emission and mathematical findings
Destination canonical emissions: 0 (no production destination emission event exists; absence is not a parsing artifact because every non-source emitter id is counted and the source emissions are present). Reception and state change are distinct from emission and were never conflated.

The earlier `tanh(1)` / `tanh(2)` single-transfer approximation does not describe the production fixture: source emission payloads are ≈0.25–0.47. Observed destination state after transfer: maximum **0.6855 (w=1)** and **0.9327 (w=2)**, both below `theta_E = 1`. Inter-arrival gaps are ≥12.9 time units against decay_rate 1.0, so pre-arrival destination state is ≤1.6e-6 and accumulation is negligible. Hence: no single transfer crosses threshold and no accumulation occurs. This explains the absence of emission mechanistically with observed values. The w=2 maximum is close to but below threshold; this is observed headroom, not a claim that any other weight would behave differently.

## Deterministic replay
Digest `abc52f98491be836445930eccb4bbf8988b61568b15e9d7633bbe20277390a7f` equal across first run and replay in the artifact. I independently re-executed the full experiment (to a temporary directory): initial and replay digests both equal the artifact digest and the classification reproduces.

## Relation to bootstrap-gap classification
**Strengthened and mechanistically refined.** Valid routing (1715 transfers, depth 1) never produces downstream canonical emission under w=1 or w=2; the gap is explained by sub-threshold transferred magnitude plus decay between sparse events. Luna-33 verdict unchanged; Luna-34 remains historically BLOCKED / UNDETERMINED.

## Validation
Focused (Luna-34/35/36/37 test files): 32 passed. Full suite: 952 passed, 1 skipped (CUDA unavailable), 953 collected (baseline 945/946 + 7 Luna-37 tests). `git diff --check` clean (see commit).

## Prohibited conclusions respected
No claim about efficacy, candidate formation, growth, pruning, generality to other topologies/streams, or that an architecture change is warranted.

## Next governance decision
Luna-38 is **not** authorized. The result is fully explained by observed values; any further step (for example, changing what a transfer can contribute, or a different stimulus regime) is either an architecture/ACP question or an arbitrary parameter sweep, both outside bounded-diagnostic authority. ACP-0007 efficacy work is not warranted by this evidence. A project-owner decision is required for direction.
