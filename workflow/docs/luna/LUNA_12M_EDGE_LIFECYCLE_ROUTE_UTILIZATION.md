# Luna-12M - Edge Lifecycle, Route Utilization, and Competing-Path Instrumentation

**Classification:** `OBSERVATION`, `VERIFICATION`, `IMPLEMENTATION`  
**Baseline:** `7f8ea2df5896d3ea7cd7d41a4f1bd8298c0dc015`

## Purpose

Make individual edge lifetimes and actual routed traffic observable before any
future direction, decay-gating, protection, weakening, or pruning experiment.
This milestone does not redesign structural learning, promote A14, change
decay or pruning semantics, add a classifier objective, or authorize a
successor Luna.

## Contract boundary

The observer is downstream-only. Routing, neuron state, prediction/error,
energy, eligibility, mutation selection and random consumption must be
unchanged when observation is disabled. Labels and global path analysis remain
outside canonical decisions. The implementation uses finite ring buffers and
saturating counters; dropped diagnostic history is visible through declared
bounds rather than backpressure.

## Diagnostic contract

An edge identity is `(source, destination, generation)`. Generation increments
when an endpoint pair is removed and later recreated. Lifecycle records cover
candidate proposal/consideration/rejection, creation, pruning and removal.
Per-edge records contain delay, routing cost, creation time, first/last use and
saturating routed-event count. Bounded traffic records retain event type,
emission time and arrival time. Offline summaries may compare old and new
routes, hops and cumulative delay; they must not feed those results back into
structural decisions.

Decay records retain neuron, local timestamp, `delta_t`, decay rate, pre-state,
residual state, post-state and the derived exponential factor. Persistent edge
strength, utility and eligibility are audited as **not present**; traffic count
is only a derived diagnostic and is not connection strength.

## Evidence gate

`PASS` requires lifecycle identity, per-edge traffic, competing-path
distinction, supported pruning/removal attribution, decay context, bounded
deterministic records and exact ON/OFF computational equality. A missing
replacement relation or hardware export is `PASS WITH FOLLOW-UP` when the
core observer remains valid. Any execution influence, ambiguous edge lifetime,
unbounded storage or nondeterminism is `BLOCKED`.

All results return to Luna-0. This specification does not authorize temporal
direction or intrinsic-decay-gated shortcut verification.

Future inherited or genetic hyperparameters, hyperparameter evolution, local
micro-networks and learned decay controllers remain outside this milestone.
They are research notes only and require a separate architectural decision.