# Luna-0 Evidence Review - Luna-12M

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-0 review of Luna-12M"
  descriptive_name: "Edge lifecycle and route utilization evidence review"
  task_id: "luna-0-review-12m-edge-lifecycle"
  component: "review of bounded edge observer and competing-path artifact"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "7f8ea2df5896d3ea7cd7d41a4f1bd8298c0dc015"
  result_revision: "uncommitted"
  dependencies: ["Luna-12M completion handoff", "corrected Luna-12L review", "Luna-12K evidence"]
  owner: "Luna-0 Architecture Guardian"
  classification: ["ARCHITECTURE-REVIEW", "EVIDENCE-REVIEW"]
  architecture_change: false
  proposal: null
  gate: "PASS WITH FOLLOW-UP"
  historical_gate: "BLOCKED"
  successor_authorized: false
```

## Historical blocked findings

### P1 - Primary competing-path utilization is not represented as measured phase data

**Observed:** The artifact contains cumulative edge totals of 3 events on each
old edge and 1 event on the shortcut. Its `old_route_before`,
`old_route_after`, and `new_route_after` fields are constants emitted by the
fixture, not traffic counters or route observations derived by the analysis
layer. The raw trace labels can be manually parsed, but the required
before/after utilization result is therefore not directly machine-readable.

**Impact:** The artifact does not yet satisfy the primary question of whether
the old route remained dominant, lost traffic, coexisted, or was displaced
over time. A future direction/decay experiment must not rely on this summary.

**Required repair:** Add explicit bounded observation scopes or epoch/reset
records and compute per-edge traffic before mutation, after mutation, and
after removal from recorded events. Replace fixture constants with derived
values and test that changing the replay changes the measured values.

### P1 - Growth creation time is fabricated when no mutation timestamp exists

**Observed:** `EdgeInstrumentation.register_edge` defaults `timestamp` to
`0.0`, and controller growth calls the observer without a mutation timestamp.
The shortcut’s `created_at: 0.0` is consequently indistinguishable from
initial topology creation at time zero.

**Impact:** Edge lifetime and time-to-first-use cannot be trusted for grown
edges. The contract prohibits inventing semantic values.

**Required repair:** Record `null`/`not available in current architecture`
when no structural timestamp exists, or pass an existing canonical local
timestamp. Do not silently use zero as a growth timestamp.

### P2 - Capacity and fan-in/fan-out mutation rejection is not emitted by the observer

**Observed:** `StructuralPlasticityController._commit_growth` returns precise
`fan_in_full`, `fan_out_full`, and capacity reasons, but the observer receives
no candidate-rejected lifecycle event when `grow()` reaches that failure after
candidate submission. The fixture only demonstrates a `nonlocal` rejection.

**Impact:** The observer cannot audit all failed admissions required by A14 or
reconstruct rejection pressure in an instrumented run.

**Required repair:** Emit a bounded rejection record containing the candidate,
reason, and available timestamp for every failed commit path, including
`adapt_many`, without changing admission behavior.

## Passed evidence

**Observed:** Endpoint-plus-generation identity distinguishes remove/recreate
lifetime generations. Per-edge routed counts, first/last use, delay, routing
cost, candidate records, pruning, and decay context are recorded.

**Observed:** Ring buffers and saturating counters are bounded and deterministic.
Repeated same-seed instrumented replay is identical.

**Observed:** Instrumentation ON/OFF preserves fixture traces, digests, and
mutation results. Focused Luna-12M tests pass (`7`). The affected regression
slice passes (`76`), and the full suite passes (`201`, `1 skipped`). Compile,
workspace diagnostics, and `git diff --check` pass.

**Observed:** Persistent edge strength, utility, and eligibility are absent;
traffic count is correctly classified as a derived diagnostic rather than
learning state.

**Inferred:** The observer boundary itself is compatible with A01-A15 and no
ACP is required. This review does not approve any change to decay, direction,
pruning, protection, utility, or A14.

## Validation status

| Check | Status | Evidence |
|---|---|---|
| Stable edge identity | passed | focused test and artifact generations |
| ON/OFF non-interference | passed | exact fixture trace/digest/mutation comparison |
| Replay determinism | passed | repeated same-seed fixture |
| Bounded storage and overflow | passed | saturation/ring-buffer test |
| Per-edge traffic and decay context | passed | focused tests and artifact |
| Phase-scoped competing-route traffic | failed | cumulative counters/constants do not satisfy direct measurement |
| Accurate growth creation timestamp | failed | growth defaults to `0.0` |
| Complete rejection lifecycle | failed | commit-capacity rejection is not emitted |
| Replacement attribution | not available in current architecture | separate growth/pruning operations |
| Hardware export/equivalence | not applicable | outside Luna-12M scope |

## Historical decision and next bounded assignment

**Historical gate: BLOCKED.** This was an evidence-quality block, not an A01-A15
architecture violation. Luna-12M should remain the owner of the bounded repair
if implementation work is authorized: phase-scoped traffic accounting,
non-fabricated timestamps, and complete rejection callbacks. Re-run the focused
and affected suites plus artifact determinism after repair.

No temporal direction/decay-gated shortcut experiment, edge-protection policy,
pruning change, A14 promotion, or successor Luna is authorized by this review.

## Corrective rerun status

The historical `BLOCKED` decision above is retained for provenance and is
superseded by this reassessment. The corrected run is recorded in
`workflow/handoffs/edge-lifecycle-route-utilization-Luna-12M.md` and generated
under `artifacts/edge-instrumentation-12m-corrected/` with schema
`TPCN-EDGE-2`. It reports phase-measured route traffic, explicit unavailable
mutation timestamps, and lifecycle rejection records for every exercised
structural failure.

**Current gate: PASS WITH FOLLOW-UP.** The three primary evidence defects are
resolved. Remaining follow-up is limited to replacement attribution, hardware
export/equivalence, and persistent edge strength/utility/eligibility, none of
which is part of the current instrumentation milestone. No future experiment
or successor Luna is authorized by this status alone.