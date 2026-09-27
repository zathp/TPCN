# Luna-12G - Spiral Handedness Temporal Classification Benchmark

## Status and boundary

Luna-12G is authorized by Luna-0 on 2026-09-27 after acceptance of the
Luna-12F corrected external readout handoff. It is a synthetic,
software-reference benchmark. It does not authorize real handwriting,
GPU/FPGA/ModelSim acceptance, hardware promotion, or a core architecture
change. No ACP is required.

## Classes and generator

Generate an ordered center-outward spiral with a shared pre-translation start at `(0, 0)`:

```text
r(t) = a * t
x(t) = r(t) * cos(theta(t))
y(t) = h * r(t) * sin(theta(t))
```

Use `h = +1` and `h = -1` as the two external classes, with monotonically
increasing `theta(t)`. The reference implementation uses 12-20 points,
240-320 time units, scale 0.8-1.2, angular speed 1.7-2.5 turns per duration,
radial growth 0.7-1.1, rotation 0-2pi, x/y translation -1..1, timing jitter
0-0.08, coordinate noise 0-0.025, and radial jitter 0-0.04. The `+1` sign is
called `spiral-left`; `-1` is `spiral-right`, with positive y upward and theta
increasing with time. Both classes use the same duration, sample count,
radius schedule, path-length rule, and initial location before translation.

For every example, record seed, target handedness, rotation, scale,
translation, angular speed, radial-growth parameter, coordinate-noise
parameter, radial-jitter parameter, sampling-timing parameter, sample count,
duration, and path-length summary. Target metadata is generator/evaluation
metadata only.

## Nuisance and split protocol

Apply global rotation, scale, translation, angular speed, bounded radial
growth, sampling timing, mild coordinate noise, and mild radial jitter using
the same independent distributions for both classes. Global rotation is
mandatory in the evaluation set. Use independent derived seeds or generator
streams for train and evaluation. Store canonical metadata and a digest of
the generated sequence so accidental example reuse is detectable. Do not use
future points for normalization or feature construction.

## Required runs and controls

Run the same declared split, budgets, and reporting schema for:

1. No-learning evaluation with external readout learning disabled.
2. Fixed-topology learning.
3. Structural-plasticity learning.
4. Evaluation sequences with point order randomly permuted.
5. Time reversal, with the transformation and expected geometric meaning
   defined before scoring. Report whether the transformed target is expected
   to invert, remain unchanged, or be ambiguous under that definition.
6. Same-handedness pairs with changed nuisance parameters.
7. Opposite-handed pairs with identical nuisance parameters and inverted `h`.

The no-learning result is a shortcut check, not a required baseline winner.
Perfect no-learning performance requires investigation before any claim that
the benchmark measures useful learned temporal classification. Fixed versus
structural performance must be reported even when plasticity is neutral or
harmful.

## Metrics and isolation evidence

Record accuracy, per-class accuracy, confusion matrix, prediction loss,
confidence, decision margin, reward, energy and proxy units, utility, event
count, active-neuron fraction, connection count/utilization, mutation counts,
and represented readout classes. Include per-example generator metadata and
the ordered/shuffled/reversed transform used.

Labels may be consumed by the external readout only after label-free neural
processing. They must not be encoded in event types or payloads, IDs, neuron
or predictor state, topology routing, mutation evidence, structural-plasticity
decisions, energy state, or prediction input. Relabeling an identical stream
is a required isolation test.

## Evidence standard

There is no numeric accuracy pass threshold. Acceptance requires evidence that
the benchmark is nontrivial, both classes are represented and measurable,
ordered input is compared with shuffled and reversal controls, train/eval are
disjoint, no-learning is measured, fixed and structural learning are separated,
and all unexplained shortcuts or poor results are reported rather than hidden.