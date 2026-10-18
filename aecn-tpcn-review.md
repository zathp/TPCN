## Scope and inspected identities

Read-only source and documentation review only. I did **not** edit files, run tests or experiments, profile workloads, or recompute hashes.

- The local review branch is `copilot/review-aecn-tpcn-brief`, at **`73aaa50f97ceab322907875ae4dcf23e7541c3b5`**. GitHub reports `main` at the same commit.
- The frozen R3 baseline named in the brief is **`11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`** (`governance/luna71b-c4-1-ppc11-freeze`).
- A separate M2D documentary-publication branch is **`governance/luna72a-m2d-evidence-publication`**, at **`c8a938194c534d7ba5ac73ba912b59e88657e601`**. Its commit adds 11 M2D documents; it is not `main`.

The code citations below refer to current `main` at `73aaa50…`, not to R3. The M2D documents describe a review at `11b6f52…`; they are documentary evidence, not executable results.

## Bottom line

Current `main` has deterministic event scheduling, local prediction/error matching, bounded eligibility ledgers, finite structural mutation, and activity-cost proxy meters. **It does not wire signed prediction error or eligibility into synaptic-weight updates or an online credit-driven topology rule.** Eligibility records credit, while the structural controller adds or removes edges from supplied candidate evidence. `Edge` transfer parameters are bounded and static in the core.

So this is a useful event-driven and mechanism substrate, but the brief’s stronger implication—distributed error and energy measurement supporting a controlled learning rule—is not established by the implemented path. In particular, credit delivery is not credit conservation, an energy proxy is not measured joules, and an E1 design proposal is not an implemented B-X-D network.

## Executable lifecycle and learning boundary

**Scheduling and neuron state.** The queue orders events by timestamp and insertion sequence; at equal timestamps, external events take precedence over internal events only for the same destination. Propagation is queued, not inline, and `execute_bounded` reports budget exhaustion and remaining work (`tpcn/event_runtime.py:3-14,116-180,182-227,248-279`).

For the canonical continuous neuron, each addressed event first decays state by elapsed local time, adds its payload, clips state, and computes bounded tanh activation. This is event-time integration, not a global timestep (`tpcn/canonical_neuron.py:92-139`). Excursion E1 uses a separate local accumulator and mode machine; external events update decayed/clipped state, while queued internal events govern emission/re-arm (`tpcn/excursion_neuron.py:396-481,730-790`). Neither mechanism is itself a learning rule.

**Prediction identity, matching, and expiry.** `LocalPredictor` assigns IDs from predictor identity plus a sequence, keeps a bounded outstanding set, and stores optional expected-resolution and expiry times (`tpcn/predictive_coding.py:108-169`). Observations match the oldest eligible prediction with the same target key; the signed error is `observed - predicted`, timestamped at the observation (`:210-255`). Expiry is strict-after: an observation exactly at `expires_at` is still eligible (`:210-239`). `expected_resolution_at` is recorded but does not determine matching order. Expiry is processed when `expire()` is called, including during observation—not by a scheduled expiry event.

**Error routing.** `process_observation` queues a `PredictionError` locally or routes it through a supplied topology (`tpcn/predictive_coding.py:257-278`). Topology applies Model-B transfer to numeric `signal`/`excursion` events, not to the error object, so the same signed error payload is forwarded unchanged (`tpcn/topology.py:204-250`).

The integrated excursion runtime applies an error at each destination ledger, then forwards it while excluding the route’s prior nodes. It deduplicates application by `(prediction_id, destination)` and bounds that guard by event budget × neuron count (`tpcn/experiment_excursion_runtime.py:665-708`). The integration tests exercise one-hop, two-hop, convergent, and capacity-failure cases; convergent paths can produce multiple arrivals at a node while applying the error only once there (`tests/test_excursion_integration.py:266-403,498-520`). This prevents repeated application at a single node in that runtime, **not aggregate credit amplification across different nodes**.

**Eligibility is bookkeeping, not parameter learning.** A ledger decays trace value and credit exponentially, bounds trace magnitude and accumulated credit, matches a reward/error to a prediction or trace, and returns a `CreditAttribution` (`tpcn/eligibility.py:150-222`). On match, it selects one trace deterministically and updates `credit` by `trace.value × signal`, clipped to `credit_limit`. No code in that operation updates an edge weight, neuron parameter, or topology.

One expiry concern: `_decay_to()` writes the current timestamp into every surviving trace’s `last_timestamp` (`:150-161`), and expiry later compares against that field (`:158-159`). Thus repeated unrelated ledger activity can refresh the timestamp used for expiry even when a trace’s eligibility was not refreshed. A trace-age policy should distinguish last activity time from last decay/update time.

## Plasticity control and topology

The structural controller enforces local provenance, candidate capacity, edge capacity, fan-in/out limits, and bounded batch growth. `grow()` commits an accepted candidate immediately; `adapt_many()` commits a selected batch atomically. Pruning is explicit, can honor a minimum edge count, and `prune_by_score()` uses supplied scores (`tpcn/structural_plasticity.py:62-108,115-206,208-255,285-325`). There is no edge probation/promotion lifecycle or built-in consolidation schedule. E1’s `S_PENDING`/M transitions are neuron-state transitions, not synaptic probation.

The temporal-association policy increments a bounded source-local score when observations fall within a time window (`tpcn/temporal_association.py:107-132`). The temporal-direction fixture separately constructs candidate records, including synthetic timing/fallback scores, then calls `grow()` in a configured loop (`tpcn/temporal_direction.py:123-205,359-421`). Those are concrete adaptation experiments, but not an online rule driven by ledger credit.

Edge parameters are bounded, but an `Edge` is a frozen record; routing applies the fixed transfer equation (`tpcn/topology.py:52-77,230-249`). The instrumentation explicitly says persistent edge strength, utility, and eligibility are “not present”; its usage score is a traffic diagnostic (`tpcn/edge_instrumentation.py:133-144`). Current tests do verify structural mutation and, in the Luna-28 E2 experiment, that accepted growth changes later routing (`tests/test_structural_plasticity.py:15-183`; `tests/test_luna28_excursion_structural_growth.py:587-629`). They do not establish credit-driven weight learning.

## Energy and compression

`LocalEnergyModel` explicitly names its units an activity-cost proxy, maintains local counters, and saturates energy/counters at configured maxima (`tpcn/energy_utility.py:1-8,102-201`). It counts categories such as received events, emitted events, activations, connection activity, and prediction errors, but does not create a system-wide distribution by neuron, edge, module, event type, or learning/inference/control/logging phase. `EdgeInstrumentation` measures bounded per-edge traffic, not per-edge energy (`tpcn/edge_instrumentation.py:95-144`).

The excursion runtime meters event receipt, emission amplitude, edge transfer, and prediction-error cost, then sums these into reported components (`tpcn/experiment_excursion_runtime.py:710-738,806-850`). These are declared proxy costs, not calibrated joules or a demonstrated complete accounting of computation and logging. Separately, the canonical neuron’s `energy_state` is accumulated absolute activation (`tpcn/canonical_neuron.py:134-136`), not a physical-energy measure.

ACP-0004 defines compression as input contributions divided by emitted excursions and specifies a bounded saturating amplitude map (`workflow/docs/architecture_proposals/ACP-0004.md:43-52,163-178`). That is a count ratio, not an objective that jointly measures task loss, retained information, energy, or learning benefit. A lower excursion count alone does not establish better learning or lower physical energy.

## Luna-72A record and evidence limits

The published M2D packet is recoverable **as a documentary packet on its separate branch**: `experiments/luna72a/results/m2d/01-m2d-baseline-provenance.md` through `11-m2d-artifact-manifest.json` are listed in commit `c8a9381…`. The M2D final adjudication says **design-document readiness: PASS**, but explicitly says implementation and execution readiness were not granted. The harness design is a proposed standalone three-node E1 composition; it excludes learning, reward, prediction-error, topology adaptation, and changes to R3/E2. It is not an implementation of `ExcursionCharacterRuntime` and not causal result evidence (`experiments/luna72a/results/m2d/03-m2d-harness-design.md`, `08-m2d-implementation-authorization-candidate.md`, `10-m2d-final-adjudication.md`).

The published M2D provenance document reports:
- The R3 eight-cell result as an infrastructure/mechanism sanity PASS, **not** recursive causal B-X-D relay evidence.
- M1 bounded-prefix profiling, but complete-cell/192-cell feasibility as **UNKNOWN**.
- M2 as **BLOCKED before execution**, with zero M2 cells and no M2 measurements.
- M2C Candidate B as a design recommendation, not an integrated E1 network path.

The current `main` checkout contains no `experiments/luna72a` results tree; the published M2D branch’s results listing contains `m2d`, not M1/M2/M2C primary packets. The M2D provenance/adjudication text reports historical manifest hashes and statuses, but the underlying M1/M2/M2C primary adjudications, manifests, and raw run evidence were not recoverable from those tracked paths. Thus the supplied claim that a 192-cell attempt stopped before its first event at the 128 MiB traced-memory limit remains **reported, not independently verified here**. The documentary record distinguishes the 134,217,728-byte Python traced-current limit from the 536,870,912-byte RSS limit; they must not be conflated.

The brief’s M2D manifest hash `6d2e…` was **not recomputed**. The tracked manifest lists hashes for deliverables 01–10 and excludes itself; the final adjudication says its self-hash was recorded separately. I therefore cannot authenticate the supplied hash from this review. Missing tracked primary evidence does not show that the historical work never occurred.

## Evidence ledger

| Category | Finding |
|---|---|
| **Implemented** | Event ordering and bounded execution; canonical neuron dynamics; local prediction matching/error events; bounded eligibility/credit accounting; finite topology growth/pruning; proxy-energy instrumentation. |
| **Test code present** | Predictor and ledger unit tests; integrated runtime error-routing and convergence tests; structural controller tests; proxy-energy tests. The integrated tests exercise production runtime paths, while unit tests establish component behavior. **I did not run any tests**, and do not claim a pass. |
| **Reported** | M2D design-readiness PASS and R3/M1/M2/M2C historical dispositions, in the separate branch’s documents; raw historical evidence remains unavailable here. |
| **Proposed** | M2D standalone E1 B-X-D harness, its counterfactual protocol, and future authorization candidate. These are design artifacts, not executable harness behavior. |
| **Unknown / not established** | Current online error-to-parameter learning; credit conservation across fanout; a complete learning/control energy distribution; calibrated joules; 192-cell feasibility or its exact stop point; causal B-X-D benefit from the reported R3 pilot. |

## Highest-impact shortfalls and practical next steps

1. **Connect credit to a controlled update rule before claiming neural learning.** Keep the existing inference path unchanged; add a separately scoped learning adapter that consumes matched, decayed eligibility and signed error, with explicit normalization, sign convention, per-edge update bounds, and deterministic application schedule. **Falsify it** with sign-reversal, delayed-credit, saturation, and label-isolation tests; verify that disabled learning leaves parameters and topology identical.

2. **Specify fanout allocation, not just event delivery.** The runtime deduplicates repeated delivery at one destination, but the same error may still affect multiple local ledgers. If the learning objective requires bounded total credit, define a fixed allocation across eligible recipients/edges and ensure recurrent paths cannot increase total update mass. **Falsify it** on one-edge, branching, convergent, and cyclic fixtures: hold the prediction/error fixed, vary fanout, and check that total absolute parameter change obeys the declared budget while reversed error reverses update direction.

3. **Add explicit plasticity controls and lifecycle.** Current growth is immediate; pruning is supplied-score driven. Before learning-driven mutation, add a declared update quota/window and candidate probation with independent evidence, a promotion threshold, and a removal/hold-down policy. **Falsify it** using noisy and alternating evidence, repeated identical events, capacity exhaustion, and fixed-topology controls; assert bounded changes, deterministic outcomes, and no oscillatory add/remove loop.

4. **Separate and reconcile energy attribution.** Retain proxy units unless calibrated physical measurements are available. Report per-event, per-edge, per-neuron/module and phase totals, including learning, inference, control and instrumentation overhead, with explicit overlap rules. **Falsify it** by reconciling event-level records to aggregates, checking saturation behavior, and asserting that instrumentation-on versus instrumentation-off does not silently alter computational traces.

5. **Correct trace expiry semantics if expiry means age since activity.** Track last activity separately from last decay time. **Falsify it** by inserting frequent unrelated ledger events between activity and expiry, then confirming an inactive trace still expires at the declared boundary.

Until these gaps are closed with separately reviewed and authorized work, the strongest supported claim is **bounded causal event processing and bookkeeping**, not an integrated, energy-optimized learning rule.
