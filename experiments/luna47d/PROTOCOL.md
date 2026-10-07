# Luna-47D frozen protocol — 2026-10-06

Status at declaration: NOT EXECUTED. Commit this protocol, fixture, model,
tests and planned handoff BEFORE generating any outcome artifact.
Authorization baseline: `789dda5988daf72f375d9713bd76a6da2b9e8b34`.
Production/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Contract 1.2; A01–A03, A08 and A15 unchanged. No ACP.

## Identity, hypothesis and boundary

This is a standalone synthetic output-model experiment, not a TPCN neuron.
It imports only the standard library; no A/B/C implementation, production
runtime, network, topology, labels or Luna-46 data enters its computation.
Luna-46's reviewed MIXED verdict is context, not trajectory-generation evidence.
The scalar fixtures prescribe finite **accumulator increments**, not raw
network inputs. The entire resulting trajectory is frozen by fixture and rule.
No assertion is made that upstream TPCN computation can produce these drives.

HYPOTHESIZED: within the declared regime, charge consumption compresses
closely spaced moderate increments to one output, permits a finite burst
for extreme excitation, and returns to neutral.
Counter-hypothesis: counts, timing, boundedness or neutral recovery fail.
This is not a test of efficacy, learning, reachability or hardware equivalence.

## Precisely tested rule

Reset `q=0`, no due event, no contributor IDs at each trajectory.
Between event boundaries, `q(t)=q(t0)*exp(-lambda*(t-t0))`.
At an input, add its signed prescribed increment. If `abs(q)>=theta` and
no opportunity is pending, schedule one at `t+period`. No output occurs
at input time. A pending opportunity is not reset by later inputs.
At an opportunity, recheck the exact threshold (no threshold tolerance).
If below threshold, record an explicit non-emission. Otherwise emit signed
unit output, then set
`q=sign(q)*max(0,abs(q)-quantum)`.
If residual `abs(q)>=theta`, schedule the next opportunity at `t+period`.
There is no autonomous pumping, threshold reset, sign reversal or global tick.
The "threshold oscillator" is thus a finite sequence of local opportunities
powered exclusively by residual charge, not a permanently cycling oscillator.
Return is dissipative consumption plus analytic leakage, not output clipping.

Exact rational logical timestamps are used for all inputs, opportunities,
outputs and final observations; units are arbitrary, NOT seconds.
At ties, input events execute in fixture list order BEFORE the due opportunity.
The pending event has a stable ID; canceled emission opportunities remain
in the state trace. Output IDs are `<trajectory>/out/<ordinal>`.
Contributors are all input identities since the last exact-zero reset;
they indicate participation, not attribution weights. Every input is reconciled
to its trace row and zero or more exact output identities. No missing output
is called compression merely because it is absent.

## Parameters, bounds and reasons (no search or tuning)

Primary constants: theta=1, quantum=4, lambda=0.125, period=1/2,
neutral epsilon=1e-6, state/absolute-drive budget=32, max inputs=16,
max opportunities=128, max outputs=32, time span <=64, observation tail=144.
Unit output amplitude is +/-1. These are dimensionless mechanism constants,
not production recommendations.

Allowed configuration domain (validation tests only): theta in [0.5,2],
quantum in [theta,8], lambda in (0,1], period in [1/8,1],
epsilon in (0,1e-3], tail at least `log(32/epsilon)/lambda`.
The one explicitly declared weak-drain negative control uses quantum=1;
everything else remains primary. No sweep, fitted parameter or adaptive rule.

The 4-unit drain is deliberately greater than the entire <=3.75-unit moderate
cluster charge; it tests a concrete compression mechanism. A moderate increment
must survive the half-unit delay: the minimum isolated crossing is
`theta*exp(lambda*period)`, approximately 1.06449. A threshold crossing alone
does NOT guarantee output. This expected negative is retained.
Extreme charge 8, 12 or 32 exceeds one drain and supports multiple opportunities.

Absolute state <=32 follows from total absolute input <=32 and strictly
dissipative evolution. Each output removes at least theta units, so at
theta=1 the total output count <=32, independently of the watchdog.
Under other legal theta values the bound is floor(32/theta).
The watchdog (128 opportunities) must raise, NEVER truncate or count a
truncated stream as a success. A single pending opportunity bounds the queue.
Input/contributor/trace storage is finite (16 inputs, 128 opportunities and
one final observation). No external excitation is applied after the last input.

The conservative primary recovery bound from last input is
`log(32/1e-6)/0.125 < 144` logical units, even if no output drains charge.
Recovery means permanently `abs(q)<=epsilon` after last excitation, not
exact zero. Exact-zero reset after consumption is reported separately.
No-output residuals are not artificially reset to neutral at observation.

## Frozen families and expected primary outcomes

`fixtures.json` freezes event ID suffixes, rational times, positive drive values,
expected counts, and family meanings. Every family is run for + and - polarity,
including sign-mirrored cancellation. No random seed is needed.

| Family | Input times / increments (positive orientation) | Expected outputs |
|---|---|---:|
| idle | none | 0 |
| subthreshold | 0 / 0.5 | 0 |
| subthreshold-near | 0 / 0.999 | 0 |
| subthreshold-cluster | 0,1/8,1/4 / 0.3 each | 0 |
| threshold-boundary | 0 / 1 | 0 (leaks before due) |
| marginal-crossing | 0 / 1.01 | 0 (negative boundary) |
| moderate-low | 0 / 1.25 | 1 |
| moderate-high | 0 / 2.5 | 1 |
| moderate-cluster | 0,1/8,1/4 / 1.25 each | 1 |
| extreme-low | 0 / 8 | 2 |
| extreme | 0 / 12 | 3 |
| extreme-cap | 0 / 32 | 7 |
| extreme-cluster | 0,1/8,1/4 / 4 each | 3 |
| cancellation | 0,0 / 2.5,-2.5 | 0 |
| separated-moderate | 0,2 / 1.25,1.25 | 2 (outside compression window) |

All nonempty primary emitting streams must have first latency=1/2 from
first input and subsequent spacings >=1/2. The extreme isolated/cluster
streams have exact spacing=1/2. Signs mirror without changing counts/times.
Idle latency and output spacing are null, not zero. Moderate compression
is a declared short cluster, NOT arbitrary widely separated moderate arrivals.

## Measurement, replay and falsification gates

Record every input ID/time/drive, pre/post state, local opportunity ID/time,
output ID/time/sign/contributor list, no-emission reason, final residual,
maximum absolute state, counts, first latency, spacings, recovery time and
delay from last input, zero-return status, configuration and fixture hashes.
Recovery crossing is an analytic binary64 metric, NOT a scheduled event.
Trace boundaries suffice to reconstruct the entire continuous trajectory.

Binary64 calculations: equation checks abs/rel tolerance 1e-12; NO threshold
tolerance. Exact IDs and rational times compare exactly. Initial/replay
canonical JSON bytes must match exactly in the recorded interpreter/platform.
Cross-platform byte equivalence is not presumed; record interpreter/platform.
Artifacts contain both initial and replay records and digests, source revision,
Git blob identities and normalized-LF SHA-256 of code/protocol/tests/fixture,
per-trajectory hashes and artifact integrity digest. Artifact verification
must recompute from committed fixtures, not accept stored counts.

Explicit retained negative controls:
* weak drain quantum=1 on both moderate-cluster polarities: fail compression
  if output count differs from the primary one-output requirement;
* reject lambda=0, period=0, quantum=0, too-short recovery horizon,
  excessive absolute drive and nonfinite drive;
* corrupt a primary record to represent extra/self-sustaining output,
  missing output, excessive output budget, state overflow, and failed neutral recovery; gate must reject
  and identity-level replay reconciliation must detect each corruption.
These synthetic fault records are NOT observations of the primary model.
Tests additionally cover late/duplicate inputs, exact threshold boundary,
event ties, prefix causality, reset, state conservation/consumption,
no idle ticks, and analytic recovery.

SUPPORTED: all primary count/timing/bounds/recovery/symmetry/replay gates pass
and every negative control is detected. PARTIALLY SUPPORTED: some primary
families pass but a primary scientific gate fails. NOT SUPPORTED: no target
compression/burst family passes. BLOCKED: provenance/execution/identity
reconciliation prevents trustworthy interpretation. Preserve every failure.
A SUPPORTED result applies ONLY to the predeclared synthetic regime.

Focused tests and applicable unchanged event/neuron/topology/EXCURSION
regressions will run; full suite may run if feasible. Platform and existing
regression failures stay failures. Commit outcome evidence and completed
handoff, push isolated branch, verify clean/ref parity, stop for independent
Luna-0 review. No merge, successor, production change, architecture promotion,
learning/energy/accuracy/hardware claim or cross-lane dependency is authorized.
