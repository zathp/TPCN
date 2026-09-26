# Luna-4 Bounded Topology Handoff

```yaml
tpcn_handoff:
  agent: Luna-4 Bounded Topology
  task_id: "bounded-topology"
  component: "finite event graph, bounded connectivity, and routing metadata"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "fda3f03"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A07", "A08", "A14", "A15"]
  preserves:
    - "Luna-1 owns Event, EventQueue, timestamp, delay, ordering, batching, and pending capacity semantics."
    - "Coordinates, spatial reservoirs, classifier state, neuron dynamics, and global learning state are absent."
    - "Legacy signal-copy and spatial-reservoir implementations remain untouched."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/topology.py"
    - "tpcn/__init__.py"
    - "tests/test_topology.py"
    - "workflow/handoffs/bounded-topology-Luna-4.md"
  tests_added:
    - "tests/test_topology.py"
  tests_passing:
    - "python -m pytest -q tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py (27 passed after joint correction)"
    - "python -m compileall -q tpcn tests"
  tests_failed: []
  tests_not_run:
    - "Full Luna-11 acceptance suite: not implemented."
    - "Streaming classification, predictive coding, delayed credit, and local energy: outside this assignment."
    - "FPGA, FPAA, hybrid, and hardware equivalence validation: not run."
  assumptions:
    - "Topology edges require finite strictly positive delays; Luna-1 remains capable of representing zero-delay queued events for its own runtime tests."
    - "Routing pending capacity is supplied by the Luna-1 EventQueue; topology does not maintain an unbounded pending-event buffer."
    - "Fan-out admission is atomic: capacity is checked for the complete logical fan-out before any delivery is enqueued."
  unresolved:
    - "Hardware-specific routing backpressure and precision tolerances remain downstream integration decisions."
  recommended_next_agent:
    - "Luna-0: review the topology interface and evidence before milestone integration."
    - "Luna-2: consume node identifiers and route events through BoundedTopology without changing Luna-1 semantics."
```

## Outcome and owned scope

Added `BoundedTopology` and immutable `Edge` metadata in `tpcn/topology.py`.
The graph has a finite node set, edge capacity, routing capacity, declared
fan-in and fan-out limits, unique directed edges, endpoint validation, and
strictly positive finite per-edge propagation delays. `seeded()` creates a
reproducible bounded graph from sorted endpoint candidates. `route()` preflights
capacity for the complete logical fan-out, then emits one event per outgoing
edge through Luna-1's `EventQueue.push_propagated`, so remote delivery remains
queued and causal. A rejected fan-out leaves the queue unchanged and is safe to
retry.

The package exports the topology interfaces without changing legacy models.
Focused tests cover all owned rejection and routing behavior, deterministic
construction, atomic fan-out admission, queue preservation after rejection,
retry without duplicates, finite pending capacity, serial/batched queue
compatibility, and the absence of a spatial-reservoir dependency.

## Architecture evidence

- **A01-A03:** `route()` never mutates a destination and delegates arrival time
  to `EventQueue.push_propagated`; complete fan-out admission is checked before
  queue mutation. Tests verify delayed readiness and serial / batched
  equivalence.
- **A04:** node, edge, fan-in, fan-out, routing, and downstream pending-event
  resources are finite and reject overflow or invalid connections.
- **A05:** the module contains no spatial-reservoir import, field, or required
  initialization.
- **A07-A08:** topology exposes only local graph metadata and bounded resource
  state; it retains no event history or global learning state.
- **A14:** the constrained `connect()` interface is suitable for later local
  structural adaptation, but structural plasticity is not implemented.
- **A15:** the graph uses fixed records, finite collections, deterministic
  construction, and explicit rejection paths suitable for software and later
  hardware mappings.

A06 and A09-A13 remain downstream responsibilities. No ACP is required or
requested; no contract invariant was changed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py` | `main`, uncommitted, Windows PowerShell, Python 3.10.8, seeded topology test seed 17 | Pass, 27 tests | Corrected joint runtime, neuron, and topology suite |
| `python -m compileall -q tpcn tests` | Windows PowerShell, Python 3.10.8 | Pass | Package and tests compile |
| `git diff --check` | `main`, uncommitted | Pass | No whitespace errors |

## Benchmark and resource results

The streaming dataset, classification metrics, prediction metrics, energy
proxy, and utility model are not applicable to this topology-only assignment.
The topology tests establish four finite nodes in the deterministic fixture,
bounded edge counts, fan-in/out rejection, positive edge delays, and a finite
pending queue. No global timestep or spatial coordinate input is used.

## Assumptions, limitations and unresolved issues

The reference topology uses opaque string node identifiers and treats edge
delay as routing metadata only. It does not implement node execution,
prediction, error events, learning, energy, delayed credit, classifier logic,
gating, or structural plasticity. A downstream integration must provide a
finite `EventQueue` and define hardware-specific retry/backpressure behavior.

The current worktree also contains unrelated uncommitted Luna-2 files; they
were preserved and are not part of this assignment.

## Reproduction and rollback

From the repository root, run the commands in the validation table. The
baseline is `fda3f03`; the result is uncommitted. Removing the topology module,
its package exports, focused tests, and this handoff restores this assignment
without reverting unrelated worktree changes.

## Next assignment

Luna-3 may consume the topology as a bounded routing dependency while retaining
ownership of neuron state transitions. Luna-11 and later integration roles must
consume the same Luna-1 queue semantics and keep prediction/error, labels,
energy, and delayed credit outside this topology layer.