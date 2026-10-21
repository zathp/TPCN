# Oscillatory priority learning test — 21 October 2026

## Result
The fixed experiment completed. The proposed error-amplitude/time-scaled oscillator learned on this synthetic task, but did not meet the predeclared criterion for improvement over paired perturbation and fixed-frequency oscillation. It had higher mean final error than both controls in all four cases.

This tests one interpretation: sustained error increases the size of a bounded triangular score sweep; the reversal frequency is a fixed function of supplied local time constants. Error does not directly change frequency, and the frequency multiplier is not learned.

## Overall mean final error
Lower is better; metric is squared difference between final frozen A-selection probability and the synthetic target service share. It is not classification accuracy.

| Method | Mean final squared error |
|---|---:|
| No learning | 0.09000000 |
| Paired perturbation descent | 0.00083217 |
| Fixed-frequency oscillator | 0.00395754 |
| Error-driven amplitude only | 0.00400890 |
| Time-scaled frequency only | 0.00944850 |
| Proposed combination | 0.00964374 |

## Per-case mean final error (8 seeds each)

| Case | Paired descent | Fixed oscillator | Proposed combination |
|---|---:|---:|---:|
| fast | 0.00005332 | 0.00004846 | 0.00010285 |
| slow | 0.00116569 | 0.00459021 | 0.00475173 |
| delayed | 0.00000284 | 0.00043572 | 0.00777116 |
| target_shift | 0.00210681 | 0.01075578 | 0.02594922 |

## What was implemented
- Scalar local priority score, bounded to[-4,4], converted through sigmoid and quantized to two positive integer connection weights summing to1000.
- Triangle-wave parameter drift and reversal around a frozen center within each cycle; ordinary control uses seeded two-sided block perturbations.
- Error-dependent amplitude bounded0.1..0.8; fixed-amplitude control0.4.
- Time-scaled period=8*max(state time constant, feedback delay, error-averaging time constant). Periods were32,64,128 and64 for fast/slow/delayed/target-shift cases.
- The center update uses the observed loss-versus-perturbation slope from completed, tagged cycles. Maximum center step0.2, common gain0.7; no analytic teacher gradient is supplied.
- Tagged delayed observations prevent loss from being assigned to the wrong probe cycle. Centers/amplitudes are held per cycle, with stale completed gradients applied to the current global center.

## Task and evaluation boundaries
The synthetic response is a first-order low-pass response to a trial selection probability. The external target is a service share0.8, changing to0.2 halfway through the shift case. Squared response error plus shared seeded Gaussian measurement noise supplies the learning signal.
The teacher target is used only by the external loss/evaluation, not the runtime arbiter. This is a calibration surrogate; there is no dataset, learned neuronal representation, E1/E2 simulation, real classification task or local prediction-credit learner.
All methods use the same initial center/state,2048 observations, irregular observation intervals and matched noise per case/seed. Eight training seeds0..7; separate evaluation seeds10000..10007.
Final frozen weights were exercised through the actual unchanged local-priority-lottery-v1 arbiter:256 evaluation choices per model. All frequency sanity checks passed. These draws check that the learned weights are applied correctly; they do not demonstrate downstream task improvement.

## Important tradeoff and limitations
Changing the oscillation period also changed the number of learning updates. In the delayed case, the proposed method made15 updates, the fixed oscillator63 and paired descent507. The proposed method therefore spent more of the fixed observation budget waiting for a full cycle.
Equal observation counts do not equal equal update counts, and a common gain is not an optimized per-method hyperparameter comparison. These are concrete confounds; the result rejects superiority of this exact configured candidate, not all error-driven oscillatory learning.
Error-amplitude-only and time-scaling-only controls also failed to improve the aggregate mean over the fixed oscillator here. No result was used to retune parameters or rerun the comparison.
Time constants/delay are supplied from the toy model, not estimated from neurons. Parameter clamps enforce bounds; they are not a convergence or network-stability proof. Delayed feedback still pending at the observation limit is recorded and was not flushed to gain extra learning.

## Validation and budgets
- 11 learner unit tests passed.
- Full fixed comparison:192 runs (6 arms*4 cases*8 seeds),393,216 synthetic observations and49,152 held-out arbiter choices.
- Additional exact replay checks: proposed method seed0 in fast/delayed/target-shift cases reproduced the complete per-run records, including trained scores, weights, checkpoints and evaluation counts.
- Including those verification replays: 399,360 observations <=400,000 and 49,920 choices <=50,000.
- Main execution approximately1.469s; replay checks0.031s. These are diagnostics, not a performance benchmark.
- No neural workload, old qualification retry, production edit or arbiter source change occurred.

## Next decisive experiment
Decouple the learned-center update cadence from the oscillation period: retain a slow probe wave but use a rolling, correctly tagged gradient estimate with a predeclared fixed update cadence. Compare update-matched controls and sweep frequency prospectively rather than select parameters from this outcome.
Only after a separate E1 rearm repair/readiness process should an actual event-ordering/classification experiment be attempted. This result does not clear R4 or Luna-72B.

## Files
- plan.json: prospective settings, metrics, success criterion and limits.
- learner.py /test_learner.py /study.py: exact experimental implementation and tests.
- results.json /summary.csv: every original run, seed, checkpoint and aggregate.
- models.json: all192 model snapshots (160 trained,32 no-learning controls), not deployed.
- replay-plan.json /verify_replay.py /replay-results.json: supplementary integrity verification, excluded from the independent-run averages.
- manifest.json: retained file sizes and SHA-256, excluding itself.
