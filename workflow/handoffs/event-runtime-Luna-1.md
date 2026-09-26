# Luna-1 Event Runtime Handoff

```yaml
tpcn_handoff:
  agent: Luna-1 Event Runtime
  task_id: "event-runtime"
  component: "hardware-neutral event schema, local time, and bounded causal queue"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "fda3f03"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A07", "A08", "A15"]
  preserves:
    - "A01-A15 contract remains unchanged."
    - "Legacy signal-copy and spatial-reservoir implementations remain untouched."
    - "Runtime payloads remain opaque and contain no labels, prediction, reward, neuron, or topology semantics."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/event_runtime.py"
    - "tpcn/__init__.py"
    - "tests/test_event_runtime.py"
    - "workflow/handoffs/event-runtime-Luna-1.md"
  tests_added:
    - "tests/test_event_runtime.py"
  tests_passing:
    - "python -m pytest -q tests/test_event_runtime.py (9 passed)"
    - "python -m compileall -q tpcn tests"
  tests_failed: []
  tests_not_run:
    - "Full integration and Luna-11 acceptance suite: not implemented."
    - "FPGA, FPAA, hybrid, neuron, predictive coding, classifier, energy, and delayed-credit validation: outside this assignment."
  assumptions:
    - "Time units are abstract nonnegative floating-point units; downstream components choose their physical interpretation."
    - "Queue insertion is the deterministic tie source in the reference runtime; callers submit events serially or through a deterministic coordinator."
    - "Rejecting late events and overflow is the default bounded reference policy; callers provide retry/backpressure handling."
  unresolved:
    - "Hardware-specific retry/backpressure transport and numeric precision remain downstream integration decisions."
  recommended_next_agent:
    - "Luna-0: review this interface and evidence."
    - "Luna-2: canonical event neuron, after Luna-0 review."
    - "Luna-4: bounded topology, after Luna-0 review."
```

## Outcome and owned scope

Implemented `Event`, `EventQueue`, `LocalClock`, `LocalTimestamp`,
`PropagationDelay`, `EventType`, and opaque `EventPayload` in
`tpcn/event_runtime.py`. The package exports these runtime interfaces without
changing legacy implementations. No neuron dynamics, prediction, classifier,
topology mutation, gating, or spatial-reservoir behavior was added.

## Runtime interface decisions

- Events contain `timestamp`, non-empty `source`, non-empty `destination`,
  `event_type`, opaque `payload`, and a queue-assigned `sequence` tie key.
- Timestamps and delays are finite and nonnegative. Propagation uses
  `t_arrive = t_emit + tau`, with `tau >= 0`.
- Zero-delay events are still inserted into the queue. They cannot mutate a
  destination inline; timestamp plus sequence ordering gives deterministic
  causal behavior.
- Queue ordering is `(arrival timestamp, sequence)`. The sequence is assigned
  by insertion, so equal-time ordering does not depend on host scheduling.
- `LocalClock.advance_to(t)` returns `Delta t` and rejects values earlier than
  the component's committed local time. There is no global clock or tick.
- `EventQueue` has mandatory positive finite capacity. Overflow raises
  `QueueCapacityError` and leaves all pending events intact; it never drops an
  event silently.
- Late events are rejected with `LateEventError` by the local clock. The queue
  itself does not commit destination time, leaving that policy at the receiving
  component boundary.
- `pop_ready` removes one event and `pop_ready_batch` removes the same ordered
  ready prefix. Batching is an execution optimization only; emitted events are
  queued and cannot be processed inline. Serial and batched tests produce the
  same causal trace.
- No event history is retained after removal, and pending state is bounded by
  the configured queue capacity.

## Architecture evidence

- **A01-A02:** irregular local timestamps, elapsed time, idle queue behavior,
  and independent clocks are tested; no global neural timestep exists.
- **A03:** propagation arrival calculation and delayed readiness are tested;
  zero delay remains queued and ordered rather than becoming inline mutation.
- **A04/A08:** queue capacity, overflow/backpressure, and bounded pending state
  are explicit and tested.
- **A05:** the module has no coordinates or spatial-reservoir dependency.
- **A07:** dispatch carries only the event's local fields and opaque payload;
  no global state or evaluation data is introduced.
- **A15:** the reference uses fixed-schema records, a bounded priority queue,
  monotonic local time, and explicit rejection paths suitable for later
  software, FPGA, FPAA, or hybrid mappings.
- A06, A09-A14 remain available to downstream roles and are intentionally not
  implemented here. No A01-A15 clause was changed, so no ACP is requested.

## Validation record

| Command | Environment / seed | Result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_event_runtime.py` | Windows PowerShell, Python, deterministic queue tests and `random.Random(17)` | Pass, 9 tests | Focused runtime suite |
| `python -m compileall -q tpcn tests` | Windows PowerShell, local Python | Pass | Touched package and tests compile |

The tests cover irregular local times, no dispatch while idle, causal ordering,
finite propagation, zero-delay ordering, deterministic ties, explicit late
events, finite capacity/backpressure, bounded pending state, serial/batched
equivalence, seeded replay, and invalid timestamps/endpoints/delays.

## Assumptions, limitations, and unresolved issues

The time unit is deliberately abstract. Sequence identifiers are deterministic
for a deterministic submission order; a multi-producer transport must define
its own deterministic admission order before using this reference queue.
Numeric tolerance is exact for the Python reference's ordering and timestamp
arithmetic; hardware precision tolerances are not defined here.

Neuron dynamics, predictive coding, classification, energy utility, delayed
credit, experimental gating, structural plasticity, spatial-reservoir behavior,
and hardware validation are outside this assignment and remain not run.

## Reproduction and rollback

From the repository root, run the two validation commands above. The baseline
revision is `fda3f03`; the implementation is uncommitted. Removing the four
listed changed files restores the pre-assignment runtime state while preserving
the unrelated existing worktree changes.

## Next assignment

Luna-0 should review the interface and evidence. After approval, Luna-2 may
consume `Event`, `EventQueue`, and `LocalClock` for canonical local event
processing, while Luna-4 may consume the queue and propagation contract for
bounded topology and routing. Both dependent assignments are unblocked by this
runtime handoff, subject to Luna-0 review.