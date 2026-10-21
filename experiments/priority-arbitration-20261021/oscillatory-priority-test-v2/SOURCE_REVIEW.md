# Independent Luna-0 prospective review

Reviewer: separate agent `/root/luna0_update_matched_review`, 2026-10-21.

**Source/readiness adjudication: PASS for the declared synthetic matrix.** No original matrix or extra training fit was executed by this reviewer. This is permission to assess the fixed experiment as evidence, not a prediction of a positive scientific result. Final publication remains subject to evidence review.

Frozen source manifest SHA-256: `6cf75309fa99c3928c1e5dd2815a40060d02909994e0b955548be394c329b1eb`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| plan.json | 4290 | 3df4f42b1db11898f245c749e2cc46826929778808ca1a6663f7908359cd081b |
| learner.py | 5571 | 09e24d8e8152371743f106345afddd85c21d77799222b8e98a402eb30e6fed74 |
| study.py | 7170 | d0bb9a2923683fb6eea94a0c4f35eee5d9d16feca303ad5f1ce0f38cc6638ef0 |
| test_learner.py | 4317 | 56b694af1747cea9bbfef1dd2182fba2f7b14555497a86b346fef3a7acd86743 |
| verify.py | 2019 | 07efd292eaf516f8f097f2bc3a338a4aee9b61bfb50933f186f98743773a2efb |

The reviewer independently checked all five byte lengths and hashes, read all five files, and ran the 15 focused unit tests: 15 passed in 0.057 seconds, exit 0. Python used the repository virtual environment; bytecode writes were disabled. The arbiter dependency identity is `3e9d66a258da0d76f08fb73a966a9c6d7da3af5ab538ea562ac9e534cf161534`; its original package manifest identity is `d12404ec1b29c50f9756af9e6b47bf0503f06a7e3492372a4262ca32e54c7bda`.

The primary arm is fixed prospectively at `error_time_8`; multipliers 4 and 16 are exploratory and cannot replace it. The source enforces exactly 111 accepted updates at observation steps 288, 304, ..., 2048 for every learning run. It preserves the actual clipped absolute trial score and origin center at observation time. Delayed feedback follows monotonically ordered observation IDs, is processed only when due, and is received before the corresponding update tick. No future feedback is flushed. Regression uses the last 256 received samples and rejects a degenerate predictor. Unit checks cover duplicate IDs, receipt ordering and origin time, finite input checks, bounded queues/windows, period scaling, physical-time phase, and exact weight totals.

The plan prospectively distinguishes physical-time delays/periods from observation-count update cadence/window length. Adaptive amplitude is recomputed from previously received error at every probe. Plant dynamics and delay are supplied constants. No labels enter the runtime arbiter.

Declared budgets are 400,000 plant observations and 50,000 heldout choices including the three prescribed replays; one original 192-run matrix uses 393,216 and 49,152 respectively. The three replays bring totals to 399,360 and 49,920. The prospective result cap is 4 MiB, explicitly enlarged before execution to retain every update audit. The matrix wall cap is 60 seconds. The replay helper starts a fresh wall clock, so final evidence must additionally establish that observed matrix-plus-replay time stays within 60 seconds; it must not claim a single continuous wall guard across both commands.

Interpretation limits: overlapping rolling OLS has phase lag, moving-center/endogenous-regressor bias, and stale target-shift samples. Equal accepted update counts remove the earlier cadence confound but do not produce an unbiased gradient or optimize each method's gain. The 256 heldout arbiter choices per model test probability plumbing, not learned task efficacy. This study cannot qualify E1, neural classification, the original memory/event budgets, or production readiness.

No source edits were made by the reviewer. Final claims, row counts, audit windows, budgets, deterministic replay evidence, report accuracy, and final artifact identities remain to be reviewed after the authorized run.
