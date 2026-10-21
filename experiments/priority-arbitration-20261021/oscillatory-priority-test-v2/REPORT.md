# Fixed-update-cadence oscillatory priority test — 21 October 2026

## Result

The original fixed matrix completed: 192 runs, with exactly 111 scheduled and accepted updates in every learning run. The primary error/time oscillator ×8 had lower mean final error than both controls in three of four cases, but higher overall mean error than the fixed oscillator. **The predeclared improvement criterion was not met.** No parameters were retuned and no replacement primary was selected.

This removes the unequal-update-count confound from v1. It does not establish an unbiased gradient, statistical superiority, neural efficacy, or production readiness.

## Overall mean final squared error

Lower is better. This is squared error of the final continuous sigmoid(center) against an external synthetic target service share, not classification accuracy or a metric computed from the 256 heldout draws.

| Method | Mean error |
| --- | ---: |
| No learning | 0.090000000 |
| Paired perturbation | 0.013073905 |
| Fixed oscillator | 0.000270708 |
| Error/time oscillator ×4 (exploratory) | 0.000214753 |
| Error/time oscillator ×8 (primary) | 0.000288911 |
| Error/time oscillator ×16 (exploratory) | 0.000335711 |

## Primary comparison by case (8 paired seeds each)

| Case | Paired perturbation | Fixed oscillator | Primary ×8 |
| --- | ---: | ---: | ---: |
| fast | 0.000019911 | 0.000024769 | 0.000007485 |
| slow | 0.022156496 | 0.000064806 | 0.000029356 |
| delayed | 0.004423519 | 0.000029904 | 0.000008504 |
| target_shift | 0.025695694 | 0.000963352 | 0.001110300 |

Target-shift performance prevents the primary from beating the fixed oscillator overall. Multiplier ×4 had a lower descriptive aggregate error than either control in this matrix, but was prospectively exploratory: it cannot replace the ×8 primary or turn this experiment into a positive primary result. Any claim about ×4 requires a new prospective confirmation.

## What changed from v1

All learning arms update at observation steps 288, 304, …, 2048, independent of probe-wave period. At each update, a rolling ordinary least-squares slope uses the last 256 received losses and their stored actual clipped absolute trial scores. The center may move during a wave. Delayed feedback is tagged by its immutable observation ID, origin time, trial score and origin center; it is never reconstructed using a newer center.

This is not only a cadence change: v1 used complete-cycle loss-versus-perturbation slopes with a center and amplitude frozen per cycle. V2 uses overlapping receipt windows, moving centers, and error-adaptive amplitude recomputed at each probe from previously received feedback. Even the paired control now uses the rolling estimator and common cadence. Cross-version metric differences cannot be attributed solely to cadence.

There are 32 no-learning controls with zero updates and 160 learning runs with 111 accepted updates each (17,760 original-matrix learning updates). Zero gradients still count as accepted update evaluations; degenerate predictor variance is a skipped update and would stop the matrix. There were no skips. Every update audit records [observation step, physical time, received sample count, first ID, last ID, predictor sum of squared deviations, clipped gradient, resulting center].

## Prospective experiment

- Six arms: no learning; paired block probes (period 4); fixed triangular oscillator (period 32); error/time triangular oscillators with period multipliers 4, 8 and 16. Primary is ×8.
- Four supplied synthetic cases: state time constant 1/delay 0; time constant 8/delay 0; time constant 4/delay 16; time constant 4/delay 8 with target changing halfway from 0.8 to 0.2. Other targets stay 0.8.
- Eight seeds 0–7 per case/arm; 2,048 observations with physical-time intervals [0.5, 1.5, 0.75, 1.25, 1]. Shared seeded Gaussian noise (standard deviation 0.002) across arms within each case/seed. Paired probe signs have a separate seeded generator.
- Time-scaled period = multiplier × max(supplied state time constant, feedback delay, error EMA time constant 4). Periods in fast/slow/delayed/shift cases: ×4 = 16/32/64/32, ×8 = 32/64/128/64, ×16 = 64/128/256/128.
- Error-dependent amplitude is bounded 0.1–0.8; fixed and paired controls use 0.4. Centers start at zero and remain in [-4,4]; common gain 0.7, gradient clipped to ±2 and step clipped to ±0.2.
- The external plant is an exact first-order low-pass response to a sigmoid trial score. Loss is squared filtered response error plus measurement noise. Targets remain outside the runtime arbiter.
- Primary success required lower overall mean final error than both paired and fixed controls, plus lower case mean than both in at least three of four cases. Only the case-count requirement passed.

## Validation and limits

15 focused unit tests passed for the author and independently for Luna-0 before execution. Source/readiness [review](SOURCE_REVIEW.md) passed before the matrix. Three prescribed exact training replays (primary ×8, seed 0, fast/delayed/target-shift) reproduced the complete result rows, including all 111 update audits and heldout counts. These are verification replays, excluded from the 192-run averages.

The original matrix consumed 393,216 plant observations and 49,152 heldout arbiter choices. Including replay, totals are 399,360 ≤ 400,000 observations and 49,920 ≤ 50,000 choices. Every model uses 256 draws with separate evaluation seeds 10000–10007 through the unchanged original arbiter. Frequency sanity checks passed; these checks validate weight application, not downstream task benefit.

The original matrix took 2.937 seconds; the replay command took 0.164 seconds including interpreter startup. Their observed sum is 3.101 seconds, below 60 seconds. The matrix and replay have separate 60-second wall guards; there is no single continuous guard across the commands. Timings are diagnostics, not performance benchmarks. The prospective result-file cap was 4 MiB to preserve all audits; results.json is 1,758,467 bytes. Pending queues are bounded to 128, receipt windows to 256 and update records to 111 per learning run. Unreceived losses at observation 2,048 remain pending; no future flush or extra learning is performed.

Rolling loss-versus-trial regression retains phase lag, moving-center/endogenous-regressor bias, correlated overlapping windows, and stale samples across a target shift. A common learning gain is not per-method hyperparameter optimization. State constants and feedback delay are supplied from the toy model rather than estimated from neurons. Single case/seed cohorts and descriptive averages do not establish statistical superiority. Weight quantization is positive integer A/B weights summing to 1000; the primary metric uses the continuous score probability instead.

No production source, frozen qualification packet, E1 implementation, or original v1 evidence was changed. The unresolved E1 rearm failure remains separate. This synthetic study does not clear R4 or Luna-72B.

## Next step

If continuing optimizer research, prospectively confirm exploratory ×4 on new seeds and separately predeclare a lag/window-sensitivity control. Do not select its favorable result as a retrospective replacement primary. Actual neural event-ordering evaluation still requires the separate E1 repair and readiness process.

## Reproduction and evidence

`source-manifest.json` freezes plan, learner, driver, tests and replay script. `results.json` holds all 192 model states, weights, evaluation counts and update audits; `summary.csv` includes case/arm means, sample standard deviations and last-quarter errors. `verification.json` and `verification-timing.json` preserve exact replay evidence. `unit-validation.json` preserves the author's focused test command. `manifest.json` inventories final retained artifacts, excluding itself. The final independent publication adjudication is in `LUNA0_REVIEW.md`.

The unchanged sibling `../local-priority-lottery-v1` is the runtime dependency. Imports have no training side effects. Run unit tests with bytecode disabled. Running study.py or verify.py writes new evidence exclusively and refuses to overwrite archived output; use a fresh copy and remove only generated outputs in that copy when planning a reproduction. Reproduction is additional experimental work, outside this archived budget.
