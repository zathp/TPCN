# Isolated arbiter test report — 21 October 2026

## Result
Sampler and arbitration-policy checks passed, with a demonstrated strict-priority fairness limitation.
The existing arbiter source was not modified. No neuron, training loop or M2E qualification ran.

Original 15 unit tests passed again.
The main study made82,370 arbiter selections and recorded226 successful checks. A separate replay supplement made16,384 selections and passed16 winner-stream checks.
Total additional study selections:98,754. Unit-test internal selections are separate from that count.

## Weighted sampling
Sixteen fixed seeds (0..15),1,024 independent decision slots per seed/case;16,384 selections per case.

| Weights | Expected shares | Observed shares |
|---|---|---|
| 1:1 | 50% /50% | 50.85% /49.15% |
| 3:1 | 75% /25% | 75.46% /24.54% |
| 9:1 | 90% /10% | 90.25% /9.75% |
| 1:1:2:4 | 12.5% /12.5% /25% /50% | 12.42% /12.45% /24.45% /50.68% |
| All-zero, four candidates | 25% each via declared fallback | 24.82% /25.17% /25.27% /24.73% |

All per-seed and aggregate frequency checks met the prospectively declared absolute standardized count-deviation threshold of6.
This is a finite sampler regression. It does not establish independence of every pseudo-random output, train priorities, or prove prediction/classification improvement.

## Ordering, locality and replay
- Out-of-locality and lower-priority candidates did not affect the selected local pool or decision in64 paired checks.
- Earlier logical timestamps took precedence over newer high-priority requests.
- All16 weighted3:1 seed streams replayed exactly after reversing candidate input order, matching the previously saved winner-stream SHA-256.
- A finite64-event backlog over eight connections drained without loss or duplicates, preserving FIFO order within each connection.
- Existing unit cases also verify invalid values, zero weights, duplicate heads, bounded sampler failure and candidate capacity.

## Fairness limitation
A low-priority request with weight100 was presented alongside256 successive same-timestamp higher-priority requests with weight1.
The higher-priority request won every time; the low-priority request received zero service during that backlog. It was served when the high-priority backlog ended.

This follows the strict priority rule: weights compete within a selected class, not across classes.
A continuing same-timestamp high-priority backlog can therefore postpone the low-priority class indefinitely. The finite burst result is not a general bounded-wait guarantee.
An aging, reserved-share or maximum-wait policy would need a separately specified change; none was added during this test.

## Coverage correction
The original study's replay_case field was descriptive text, while its branch compared an exact case ID. Consequently that branch did not run in the first study.
The original plan, study and results remain intact and do not claim full-stream replay coverage. replay-plan.json and replay_supplement.py explicitly cover the missing weighted31 case and compare against the first run's saved stream hashes.
No arbiter source or weights were tuned, and the frequency study was not rerun.

## Evidence and scope
- plan.json /study.py /results.json: original fixed study and complete per-seed data.
- replay-plan.json /replay_supplement.py /replay-results.json: explicit coverage supplement.
- manifest.json: retained artifact identities, excluding itself.

The main study took approximately0.891 seconds and the supplement0.188 seconds on this host; these are diagnostic elapsed times, not a controlled performance comparison.
Source/model identity and replay keys are in the JSON records. The input weights are illustrative fixed values, not trained weights.

## Proposed training for the alternative: learned priority, random ties
This alternative has not been trained or implemented here.
I would first train external per-connection ranking scores within the same eligible locality/priority pool:
1. Collect representative same-time arbitration situations and reproduce identical initial state for competing legal orderings.
2. Compare A-first versus B-first using downstream task loss, with the known class label used only by the external loss. Declare delay/work/rare-event terms before collecting targets.
3. Learn a score ordering from those comparisons. Start with per-connection scores; context-dependent scores require causally available local features and their own declared interface.
4. At runtime, serve the highest score and use seeded random selection only for ties. Define fixed-point scores or a tie policy explicitly; arbitrary floating scores may almost never tie.
5. Evaluate held-out examples and seeds against FIFO, uniform randomness and the weighted lottery, including starvation/rare-event outcomes.

Unlike the currently tested lottery, scores3 and1 would always put the first signal ahead when both are eligible. A3:1 lottery gives it a75% chance.
Counterfactual ranking trials require a numerically stable neural reference first; the separate E1 rearm stall remains unresolved.
