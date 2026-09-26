# Luna-0 Joint Review: Luna-2 and Luna-4 Handoffs

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  task_id: "joint-review-luna-2-luna-4"
  component: "joint review of canonical event neuron and bounded topology"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "53ae36d"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A07", "A08", "A15"]
  preserves:
    - "Both handoffs preserve the Luna-1 queued event and local-time semantics."
    - "Neither component introduces a spatial-reservoir dependency, global neural clock, global learning state, or classifier logic."
    - "A06, A09-A14 remain downstream or explicitly disabled as stated by the handoffs."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/joint-review-Luna-0-luna-2-luna-4.md"
  tests_added: []
  tests_passing:
    - "python -m pytest -q tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py (27 passed)"
    - "python -m compileall -q tpcn tests (reported passing by both handoffs; not rerun for this review)"
  tests_failed: []
  tests_not_run:
    - "Full Luna-11 acceptance suite and streaming classification benchmark."
    - "Predictive coding/error events, local energy utility, delayed credit, structural plasticity, and hardware equivalence."
  assumptions:
    - "The package-level export claimed by Luna-2 is intended to be part of its public interface."
    - "Topology fan-out under queue backpressure should be replayable without duplicate edge deliveries."
  unresolved: []
  recommended_next_agent:
    - "Luna-3: define local prediction matching and explicit causally propagated error events."
    - "Luna-11: independently verify the integrated acceptance matrix after downstream components exist."
```

## Review outcome

The two handoffs are architecturally compatible and do not require an ACP. Both correctly keep neuron dynamics and graph routing on top of Luna-1's event queue, preserve local timestamps and delayed propagation, and leave predictive coding, energy, delayed credit, classification, and structural plasticity to their assigned downstream roles.

The two correction findings are **resolved**. The bounded Luna-2/Luna-4 integration gate passes. This is not a contract departure; both fixes preserve A01-A15 and required no ACP. The broader first integration milestone remains incomplete until predictive coding, energy, delayed credit, classifier, and Luna-11 acceptance evidence exist.

## Findings

### 1. Medium: Luna-2 claims a package export that is absent, resolved

`canonical-event-neuron-Luna-2.md` says `TPCNNeuron` was exported from the package, but `tpcn/__init__.py` imports and lists topology symbols without importing or listing `TPCNNeuron`. The implementation is available only through `tpcn.canonical_neuron`.

Resolution: `tpcn/__init__.py` now exports `TPCNNeuron`, and the focused neuron suite includes a package-level import regression test. `from tpcn import TPCNNeuron` succeeds. No neuron API redesign was made.

### 2. Medium: Luna-4 fan-out routing is not atomic under queue backpressure, resolved

`BoundedTopology.route()` pushes outgoing edges one at a time. With two outgoing edges and an `EventQueue(capacity=1)`, the first event remains queued and the second push raises `QueueCapacityError`. A retry can therefore duplicate the first delivery, while a caller that abandons the retry loses the second delivery.

Resolution: `route()` preflights complete fan-out capacity before enqueueing. Rejected fan-out leaves existing queue contents unchanged; repeated failure is deterministic, retry after capacity is available produces both edges once, and successful routing admits the complete fan-out. Regression tests cover each required case.

## Validation record

| Command or procedure | Result | Evidence |
|---|---|---|
| `python -m pytest -q tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py` | Pass, 27 tests | Corrected joint suite |
| `python -c "import tpcn; print(tpcn.TPCNNeuron.__name__)"` | Pass, prints `TPCNNeuron` | Public package export verified |
| Two-edge route with insufficient capacity | Deterministic `QueueCapacityError`; queue unchanged | Atomic fan-out regression tests |
| `git status --short` and `git log -1 --oneline` | Uncommitted Luna-2/Luna-4 work on `main`; HEAD `53ae36d` | Review baseline |

## Architecture assessment

- A01-A03: preserved by both implementations; queue-backed delivery and local neuron clocks are compatible.
- A04: finite nodes, edges, fan-in/out and queue capacity are present; fan-out admission is atomic under queue capacity failure.
- A05, A07-A08, A15: no observed departure in these two components.
- A06, A09-A14: correctly not claimed as implemented, except that Luna-2 exposes placeholder fields which its handoff explicitly labels compatibility surfaces.
- ACP status: not required. The corrections are compatible implementation and documentation changes.
- Correction gate: passed for Luna-2 and Luna-4. Luna-3 is authorized to proceed on the corrected interfaces.

## Next assignment

Luna-3 is authorized to define local prediction matching and explicit error events on the corrected runtime/neuron interfaces. Luna-11 remains responsible for independent integration evidence once predictive coding, energy, delayed credit, and the streaming benchmark exist. The full architecture milestone is not yet integration-ready because those downstream capabilities are still unimplemented.
