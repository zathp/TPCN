# Luna-12M Completion Handoff

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-12M"
  descriptive_name: "Edge Lifecycle, Route Utilization, and Competing-Path Instrumentation"
  task_id: "edge-lifecycle-route-utilization-luna-12m"
  component: "downstream bounded edge observer and competing-path fixture"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "7f8ea2df5896d3ea7cd7d41a4f1bd8298c0dc015"
  result_revision: "uncommitted"
  dependencies: ["corrected Luna-12L", "Luna-12K", "Luna-12H", "Luna-12E"]
  owner: "Luna-0 Architecture Guardian"
  classification: ["OBSERVATION", "VERIFICATION", "IMPLEMENTATION"]
  hypothesis: "Per-edge lifecycle and traffic observation can expose competing-route use without changing canonical execution."
  counter_hypothesis: "Observer hooks alter computation, are unbounded, nondeterministic, or cannot distinguish edge lifetimes."
  architecture_change: false
  proposal: null
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves: ["event-driven computation", "local time and finite unequal-delay propagation", "bounded topology", "local learning and label isolation", "hardware-neutral reference behavior"]
  unauthorized_scope: ["decay-gated growth", "direction change", "edge protection", "pruning change", "persistent edge strength", "new utility objective", "successor Luna"]
```

## Outcome

**OBSERVED:** `EdgeInstrumentation` records bounded lifecycle events, endpoint
plus generation identities, candidate/rejection outcomes, per-edge delay and
routing cost, saturating traffic counts, first/last emission timestamps and
bounded emission/arrival records. Removing and recreating `A -> B` produces
generations `0` and `1`.

**OBSERVED:** The deterministic fixture records the two-edge old route before
growth, the one-edge shortcut after growth, a rejected candidate, shortcut
pruning, and decay context. The artifact is versioned `TPCN-EDGE-1`.

**OBSERVED:** Instrumentation ON/OFF produces equal event traces, replay
digests and mutation outcomes. Repeated instrumented runs with the same seed
are equal.

**OBSERVED:** Storage is bounded by lifecycle and traffic ring buffers;
counters saturate at the declared limit. No persistent edge strength, utility
or eligibility exists in the current architecture. Traffic count is a derived
diagnostic only.

**INFERRED:** The current software reference can measure old/new route traffic
and causal delay before a future direction or decay experiment without adding
feedback into neural execution.

**HYPOTHESIZED:** Future route-protection or edge-weakening experiments may be
scientifically justified only after this observer is used to measure whether
new edges are used before ordinary pruning. No such policy was added here.

## Files changed

- `tpcn/edge_instrumentation.py`
- `tpcn/topology.py`
- `tpcn/structural_plasticity.py`
- `tpcn/canonical_neuron.py`
- `tpcn/__init__.py`
- `tests/test_luna12m_edge_instrumentation.py`
- `run_edge_instrumentation.py`
- `workflow/docs/luna/LUNA_12M_EDGE_LIFECYCLE_ROUTE_UTILIZATION.md`
- `.github/agents/luna-12m.agent.md`

## Validation

Focused tests: **7 passed**. Artifact runner: **passed** with equal ON/OFF
traces, digests and mutation results. Broader regression, compile, diagnostics
and `git diff --check` results are recorded after the full validation pass.

## Artifact and next action

Machine-readable output: `artifacts/edge-instrumentation-12m/edge_lifecycle.json`
and `artifacts/edge-instrumentation-12m/summary.json`.

The provisional gate is superseded by the Luna-0 review at
`workflow/handoffs/luna-0-review-12m.md`: **BLOCKED** pending repair of
phase-scoped traffic accounting, non-fabricated growth timestamps, and
complete capacity-rejection lifecycle records. Do not create or authorize a
successor Luna from this handoff.

## Instrumentation architecture

`BoundedTopology.route(..., observer=...)` forwards each already-created
routed event to the observer after queue admission. `StructuralPlasticityController`
forwards candidate and mutation outcomes. `TPCNNeuron` forwards existing local
decay values after its unchanged state transition. None of these callbacks can
return a decision or mutate the canonical objects.

Edge identities are `{source, destination, generation}`. Lifecycle records are
bounded ring-buffer entries for `candidate_proposed`, `candidate_considered`,
`candidate_rejected`, `edge_created`, `edge_pruned` and `decay_context`.
Traffic records contain identity, event type, emission timestamp and arrival
timestamp. Per-edge counters contain creation time, delay, routing cost,
traffic count, first use and last use. Counters saturate; ring buffers retain
the newest records within their declared capacity.

The fixture demonstrates old-route traffic before shortcut creation, old and
new traffic after creation, shortcut removal, a rejected candidate and
intrinsic decay data. Replacement attribution is **not available in the
current architecture** because growth and pruning are separate operations.
Edge weakening and time-since-last-use are offline derivable from the records;
they are not canonical edge strength.

## Validation record

| Command or procedure | Result | Evidence |
|---|---|---|
| `python -m pytest -q tests/test_luna12m_edge_instrumentation.py` | passed: 7 | identity, traffic, bounds, paths, decay, determinism, ON/OFF |
| Affected Luna/runtime/replay slice | passed: 76 | 12M, 12K, 12J, 12I, 12H, 12E, topology, plasticity, runtime, temporal analysis and CPU replay |
| `python run_edge_instrumentation.py --output artifacts/edge-instrumentation-12m` | passed | `edge_lifecycle.json` and `summary.json` |
| `python -m pytest -q` | passed: 201, skipped: 1 | full repository suite |
| `python -m compileall -q ...` | passed | touched and relevant runners compile |
| workspace diagnostics | passed | no errors in touched Python files |
| `git diff --check` | passed | existing LF/CRLF warning only |
| real dataset, hardware equivalence, FPGA/ModelSim acceptance | not applicable | outside Luna-12M scope |

## Reproduction and readiness

Run `python run_edge_instrumentation.py --output artifacts/edge-instrumentation-12m`.
The artifact is separate from TPCV-1 and does not change TPCV semantics.
The software-reference milestone is ready for Luna-0 evidence review, but no
future direction/decay policy is authorized. A later bounded experiment may
investigate whether an evaluation interval is needed only after traffic and
pruning evidence justify it. The inherited/local hyperparameter and micro-NN
idea remains future research only and was not implemented.

## Corrective rerun after Luna-0 BLOCKED review

The historical `BLOCKED` decision in `workflow/handoffs/luna-0-review-12m.md`
is preserved. Its three defects were repaired in the existing Luna-12M scope:

1. Phase traffic is recorded per edge for `PRE_SHORTCUT`, `POST_SHORTCUT`, and
  `POST_REMOVAL`. Multi-edge route traffic is the minimum measured traffic
  across the required route edges, not a sum of unrelated edge counters.
2. Missing mutation timestamps serialize as `null` with domain `unavailable`.
  Supplied event timestamps retain the `event_timestamp` domain, including a
  genuine `0.0` timestamp.
3. Failed structural attempts emit bounded `candidate_rejected` lifecycle
  records. The deterministic rerun exercises `duplicate`, `nonlocal`,
  `fan_in_full`, `fan_out_full`, `edge_capacity`, and `candidate_capacity`.

**OBSERVED:** The corrected artifact reports old-route traffic of `1` before
shortcut creation, `1` after creation, shortcut traffic of `1` after creation,
and old-route traffic of `1` after shortcut removal. The raw records show both
routes coexisting in `POST_SHORTCUT`.

**OBSERVED:** Creation records without a mutation timestamp contain `null` and
`unavailable`; the focused timestamp regression distinguishes this from a real
creation timestamp of `0.0` and `event_timestamp`.

**OBSERVED:** Controller rejection results match lifecycle records for all six
exercised reasons. Pruning is recorded, but no compatible mutation timestamp is
available, so edge age, lifetime, and time-since-last-use at pruning are
unavailable rather than inferred from experiment order.

**OBSERVED:** Instrumentation ON/OFF traces, digests, and mutation outcomes are
equal. Same-seed replay is deterministic, including traffic, lifecycle,
rejection records, and summaries. Storage remains bounded and counters remain
saturating.

**INFERRED:** The old and shortcut routes coexisted; a traffic crossover or
route dominance is not established because the fixture has one measured event
per route phase. After shortcut removal, routing returned to the old route.

**HYPOTHESIZED:** A future experiment may investigate route evaluation over a
longer observation window. No such policy was implemented here.

Corrected artifacts:

- `artifacts/edge-instrumentation-12m-corrected/edge_lifecycle.json`
- `artifacts/edge-instrumentation-12m-corrected/summary.json`

Validation: focused Luna-12M **10 passed**; Luna-12H through Luna-12K
regressions **24 passed**; `compileall` **passed**. The corrected artifact is
schema `TPCN-EDGE-2`. Persistent edge strength, utility, and eligibility remain
absent by design. Replacement attribution and hardware export remain
unavailable. **New gate: PASS WITH FOLLOW-UP.** Luna-0 may reassess the primary
evidence and decide whether a later direction/decay-aware shortcut experiment is
justified; this handoff does not authorize it.