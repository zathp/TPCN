# Luna-72A-M2D Resource and Lifecycle Contract

## Status

Proposed contract for a later separately authorized implementation and
qualification. No resource measurements were made. Finite configured bounds
are not host feasibility evidence and do not qualify R4.

## Deterministic per-condition bounds

Use seven fixed treatment conditions (P, N, C, I, T, O+, O-) and one exact
replay of each: fourteen total condition executions in a future authorized
protocol.
Do not add cells, random sweeps, adaptive retries, route variations, or
parameter search.

| Resource | Proposed limit | Terminal rule |
|---|---:|---|
| Neurons/topology | 3 neurons, 2 static edges, `edge_capacity=2`, `fan_in_limit=1`, `fan_out_limit=1`, `routing_capacity=2` | Refuse any extra node/edge, cycle, alternate route, or topology mutation. |
| Path depth | 2 edges maximum (`B→X→D`) | Reject/stop if a route exceeds two transfers. |
| Queue | 16 pending event records | Queue refusal/overflow stops the condition; no drop, partial route, or retry. |
| E1 local state | Three configured E1 instances; each `|x|<=8`, provenance `P=16`, and at most one valid pending internal event | Any clipping is normal configured E1 behavior; truncation, event-budget exhaustion, or `theta_M`/M-boundary report prevents a causal PASS and stops the condition. |
| Per-neuron E1 work | `E1Config.event_budget=16` for B, X and D | E1 budget exhaustion is a terminal failure. |
| Queue processing | At most 32 processed queue events per condition | Stop before processing beyond 32; incomplete result is failure. |
| Queue admissions/created work | At most 32 total root admissions, E1 internal-event admissions, and per-edge routed copies per condition | Stop before admission beyond 32; count emissions separately as neuron outputs. |
| Returned emissions | At most 8 per condition | More than the proposed fixture can produce is a bounded-run failure. |
| Observer output | 128 total observer records and 128 contributor/root references per condition; category caps in `04-m2d-event-provenance-contract.md` also apply | Refuse record growth beyond any cap; preserve bounded failure counters. |
| Logical horizon | Process through `t=40.0`; maximum event timestamp 40.0 | If queued/pending work remains at the horizon, mark incomplete and fail. |
| Wall-time guard | 10 seconds per condition; 140 seconds for the fourteen-condition suite | Stop on the first exceeded guard; no automatic retry. These are proposed ceilings, not performance expectations. |
| Retained artifact | 1,048,576 bytes total for the suite, including failure evidence and manifest-excluded outputs | Refuse to append/serialize beyond the cap; retain a bounded incomplete status record if possible. |

The primary schedule predicts fewer than 32 queue admissions/processed events,
fewer than eight emissions, and fewer than 128 observer records in any
condition. The limits deliberately leave headroom but remain small. Every
actual count and peak must be measured in a future run; successful operation
under these bounds does not establish behavior at larger scale.

## Host memory guards — separate metrics

Preserve both historical limits without conflating them:

- Python `tracemalloc` **current traced bytes**: maximum
  `134,217,728` bytes (128 MiB).
- Windows process **current RSS/working set**: maximum `536,870,912` bytes
  (512 MiB).
- Traced peak is a separate diagnostic only; it must not substitute for
  traced current or current RSS.

For a future authorized implementation, reject an already-active Python
tracer rather than stopping/restarting or silently sharing its trace. Report
pre-trace values as unavailable, not zero. Start the controlled trace before
constructing trial neurons/topology/queue. Sample both current metrics
separately at: configuration admission; topology/neuron construction; root
queue admission; each event dispatch; each hop receipt; each E1 threshold and
emission boundary; destination receipt; result serialization; and cleanup.
Read and preserve the sample before applying each guard. Failure to obtain
either metric is a guard failure, not a fallback to the other metric.

Sampling is point-in-time, not a continuous peak guarantee. Record the sample
times and measurement method. Host RSS and elapsed time need not be
deterministic across replay. Resource tracing/observation must be bounded and
must not retain unbounded snapshots or a second full event history.

## Admission, failure, and cleanup lifecycle

1. Validate the frozen protocol, exact source identity, output destination,
   all configured capacities and both guard interfaces before admitting roots.
   Refuse unknown protocol values, active tracer state, invalid limits, missing
   output path or a source-manifest mismatch before any condition runs.
2. Allocate only bounded topology/neuron/queue/observer state. Sample both
   host metrics and check limits before the first root admission.
3. Check event, queue, observer, time, wall, artifact and host bounds before
   every relevant admission/dispatch/record/serialization action. A failed
   check is terminal for the current condition and aborts the suite; do not
   continue with later arms.
4. On failure, preserve only bounded failure evidence: exact condition and
   event/dispatch ordinal, exception/guard reason, last successful metrics,
   queue peak and pending count/identity/timestamp summaries, neuron modes/
   pending event/provenance truncation, and partial artifact byte count.
   Never mark incomplete output as successful and never clear pending work
   before recording it.
5. Close/flush the bounded artifact, release queue, observer and runtime
   references, then record cleanup samples while the controlled measurement
   remains active. A cleanup/flush guard failure remains a failed result.
6. No automatic retries, silent default limits, limit increases, workload
   shrinkage after observing failure, or outcome-driven parameter changes.

These are proposed semantics. Existing `EventQueue` and topology already
refuse capacity overflow, but they do not provide all cumulative creation,
observer, artifact, or host-phase safeguards. Those safeguards belong to
future isolated M2D code, not production runtime changes.

## What bounds guarantee, and what they do not

**Design-level guarantees if correctly implemented:** finite graph and
outdegree; maximum route depth two; finite pending queue; finite E1 state,
local event budget and provenance; finite run work, observer, horizon,
artifact and host thresholds; fail-closed stop semantics.

**Still empirical/unresolved:** actual Python traced-current and Windows RSS
for the isolated harness, monitor overhead, host wall time, allocator
behavior, serialized artifact size, and whether the complete fourteen-run
suite finishes inside the ceilings. M1's bounded prefix and M2's no-run
disposition are not measurements of this harness.

**R4 comparability:** M2D changes the neuron mechanism and causal estimand
relative to frozen R3. A mechanism PASS, bounded resource PASS, or small
fixture completion does not establish 192-cell resource feasibility or make
M2D results exchangeable with R3. R4 remains blocked absent its separate
owner decision and qualification.
