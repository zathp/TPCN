# Luna-72A-M2D Future Implementation Authorization Candidate

## Status — request for a separate owner decision

**NOT AUTHORIZED.** This is the exact proposed implementation design resulting
from the current owner-authorized design/readiness task. The current task
grants no executable implementation, test execution, profiling, benchmark, or
experiment. A new explicit owner grant and a fresh independent readiness PASS
are required before touching any proposed implementation/test file.

The design targets only the isolated standalone-E1 B-X-D mechanism fixture.
It is not an R3 replacement, E2 modification, R4 qualification, or Luna-72B
design.

## Exact baseline and preserved identities

- Source revision: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`
- Worktree/branch: `TPCN-luna72a`,
  `experiment/luna72a-competing-path-discovery`
- Frozen R3 source manifest:
  `70e1f44de464ffd4ad16366b76ca7d51f168cccaf199cd97de10276987cff62f`
- M1 manifest:
  `04ee13db3d5b8330053411ae4a91f8e9643114ba730272771044e158a884e6ba`
- M2 manifest:
  `818465480fc31ba88bdb8c79622f67e00d703d9ff4c4c65cb0df7495af439910`
- M2C manifest:
  `9c2e5d6c9dae754f1679d86f909e9609ef6a86b2c535d0e00e6b5ccf843d6ec6`

Before any future implementation, recreate and verify an exact-source
manifest for all imported source/contracts and include its raw SHA-256 in the
readiness artifact. If the baseline or any dependency differs, stop for a new
design/review; do not silently adapt.

## Proposed file allowlist (future grant only)

New files permitted by the candidate scope:

1. `experiments/luna72a/m2d/e1_harness.py` — isolated event dispatcher and
   adapter composition; constructs E1/topology and a small `EventQueue`
   subclass that counts admissions through `push` before delegating unchanged
   queue behavior; dispatches queued events and routes returned emissions.
2. `experiments/luna72a/m2d/provenance.py` — bounded downstream-only
   event/transition/transfer/arrival/terminal observer, explicit C-arm
   `BlockedRouteDecision` record, and canonical trace serializer. A blocked
   decision is not represented as a transfer or arrival.
3. `experiments/luna72a/m2d/protocol.json` — exact frozen configs, edges,
   root IDs/timestamps/payloads, arms, limits, and acceptance oracle.
4. `experiments/luna72a/m2d/runner.py` — invokes only the frozen conditions
   after a separately authorized execution gate; refuses mismatched source,
   protocol, limits, or invalid approval.
5. `tests/test_luna72a_m2d_e1_adapter.py`
6. `tests/test_luna72a_m2d_provenance.py`
7. `tests/test_luna72a_m2d_counterfactuals.py`
8. `tests/test_luna72a_m2d_fail_closed.py`

Only those new files are within the proposed writer allowlist. Do not edit
`tpcn/`, R3 `experiments/luna72a/engine.py`/runner/fixtures/source manifest,
M1/M2/M2C artifacts, architecture/ACP files, global tests, E2 integration, or
unrelated files. Generated run results are outputs, not source edits, and are
not authorized by this candidate.

## Proposed interface contract

The following is an adapter-level design; exact type annotations and imported
names must be confirmed against the frozen source before implementation.

```text
E1Harness(configs, topology, queue_capacity, event_budget,
          observer, max_route_depth) -> bounded harness
run_condition(condition_id, root_events, logical_horizon) -> trace/result
```

Implementation behavior:

- Build one `SingleExcursionNeuron` per node and one shared
  `EventQueue[Event]`.
- Admit only declared external `Event`s by queue push.
- On each dequeue, require a known destination, call
  `neuron.receive_event(event, shared_queue)`, and record a bounded
  before/after observation.
- If the receive returns an `ExcursionEmission`, create its event carrier with
  `emission.as_event(emission.source)` and call
  `BoundedTopology.route(carrier, shared_queue)`. Do not inline-update the
  destination or substitute `process_pending`/direct enqueue for topology
  routing.
- For C, record the bounded `BlockedRouteDecision` for the declared excluded
  B-X route separately from topology transfers, before routing. This decision
  is not a transfer or arrival and must not create either record.
- Enforce cumulative admissions by overriding queue `push` to refuse before
  the cap and then call `super().push` exactly once; current
  `push_propagated` delegates to `self.push`, so it counts propagated copies.
  Enforce logical horizon with `peek` and `pop_ready(through=40.0)`, because
  `execute_bounded` has no horizon argument. Enforce processed-event, wall and
  host guards independently.
- Unknown destination, invalid event, E1 boundary/budget error, queue/topology
  overflow, observer overflow, guard error or replay mismatch is a terminal
  failure with bounded failure evidence.

These names/signatures describe a new experimental adapter. They are not
present in the current codebase and must not be imported from or presented as
`ExcursionCharacterRuntime`.

## Frozen semantics and protocol

Use the exact numeric values and E1 state assumptions in
`03-m2d-harness-design.md`, route identity schema in
`04-m2d-event-provenance-contract.md`, bounds in
`05-m2d-resource-lifecycle-contract.md`, and controls/oracle in
`06-m2d-counterfactual-protocol.md`.

The future implementation must:

- Call current E1 methods for all decay, clipping, signed integration,
  threshold, local scheduling, stale-event validation, emission and rearm.
- Use one shared finite queue, positive-delay fixed edges and Model-B route
  transform; never create a global timestep.
- Start every arm from fresh neutral neuron instances, empty queue and
  zero-time clocks.
- Keep prediction/error/eligibility/reward/learning/topology-adaptation and
  ACP-0008 slow integration disabled.
- Keep P/N/C/T/O arms free of independent X/D sensory input; I is separately
  tagged and analyzed only as its independent positive control.
- Maintain bounded contributor/root mappings. A parent reference is not sole
  attribution; preserve multiple E1 contributors and truncation status.
- Use stable same-condition replay IDs and compare canonical traces exactly.

## Required future tests (not run here)

1. **API/config checks:** `E1Config` validity, standalone construction and
   state initialization, expected `receive_event`/internal scheduling
   semantics, and explicit no-E2 boundary.
2. **E1 state/emission tests:** positive and negative sign; decay; clipping;
   below/at/above `theta_E`; output delay and amplitude; internal event
   identity/sequence; single-excursion return/rearm; stale events; M-boundary
   stop; same-time external-before-internal ordering.
3. **Adapter composition:** event queue ordering, B-X and X-D delay/transfer,
   exact event identity preservation across a routed copy, distinct neuron
   emission IDs, terminal empty queue, and no inline delivery.
4. **Provenance:** multi-contributor episode, trigger vs contributor distinction,
   root resolution, static edge identity, transfer and arrival references,
   observer truncation, and truncation propagation. The C-arm test must require
   its `BlockedRouteDecision` while asserting that the excluded B-X route
   produces neither a transfer nor an arrival record.
5. **Counterfactual:** implement the P/N/C/I/T/O+/O- oracle exactly and run
   each twice only under a later authorized execution; require same-arm
   canonical byte equality.
6. **Fail-closed policy:** synthetic unit tests for queue/work/observer/artifact
   caps, time horizon, wall/resource metric failure, timeout and identity
   mismatch. Guard tests must use injected samples and must not artificially
   allocate memory or raise a real host limit.
7. **Scope regression:** assert no imports or execution through frozen R3 or
   E2 paths and verify the source allowlist / historical hashes before and
   after the future authorized run.

No test command or test result is asserted by this design.

## Future execution gate and qualification separation

Before implementation, Luna-0 must independently review the exact source
manifest, allowlist, schema, protocol JSON, tests/oracle, resource behavior,
failure behavior, and approval gate. A PASS must be recorded for the exact
hashes before any work. After implementation, a separate independent
source/test review and exact-run authorization are required before execution.

Future qualification must report these independently:

1. **Mechanism qualification:** Did the exact P/N/C/I/T/O fixture satisfy its
   causal, state, identity and replay oracle?
2. **Resource qualification:** Did the authorized fourteen-run workload
   complete under every approved cap and both independent host guards, with
   phase evidence? This remains empirical even if configured bounds are
   finite.
3. **R4 comparability:** Does this E1-specific estimand support any inference
   about the frozen R3 192-cell comparison? Current answer: **not established**.
   M2D cannot itself clear R4. A different estimand requires an explicit
   owner decision and a separately reviewed R4 protocol.

## Owner decision requested

After reviewing the independent M2D design adjudication, choose explicitly:

1. **Authorize M2D implementation and tests only**, limited to the allowlist
   above. No test execution involving a workload, profiling or experiment.
2. **Authorize implementation, tests and the bounded fourteen-condition
   mechanism/resource qualification**, conditional on the new exact-source
   independent readiness PASS and the exact protocol/hashes above.
3. **Decline M2D** and preserve M2 as blocked.

No option is inferred. Even option 2 does not authorize R4 or Luna-72B.
