# Luna-2 Canonical Event Neuron Handoff

```yaml
tpcn_handoff:
  agent: Luna-2 Canonical Event Neuron
  task_id: "canonical-event-neuron"
  component: "bounded canonical event-driven neuron"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "53ae36d"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A09", "A11", "A15"]
  preserves:
    - "Luna-1 Event, EventQueue, LocalClock, LocalTimestamp, and PropagationDelay semantics."
    - "Local event processing with no global neural clock or all-neuron update."
    - "Prediction, prediction-error, reward utility, delayed-credit, topology, and classifier ownership boundaries."
    - "Hardware-neutral bounded reference behavior without spatial-reservoir dependency."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/canonical_neuron.py"
    - "tpcn/__init__.py"
    - "tests/test_canonical_event_neuron.py"
    - "workflow/handoffs/canonical-event-neuron-Luna-2.md"
  tests_added:
    - "tests/test_canonical_event_neuron.py"
  tests_passing:
    - "python -m pytest -q tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py (27 passed after joint correction)"
    - "python -m compileall -q tpcn tests"
  tests_failed: []
  tests_not_run:
    - "Luna-11 acceptance suite and streaming classifier benchmark: not implemented."
    - "Predictive coding/error events, reward-adjusted energy utility, delayed credit, structural plasticity, and hardware equivalence: outside this assignment."
  assumptions:
    - "Numeric event payloads are the minimal local activation interface; later event types may define richer local payload contracts."
    - "State decay uses abstract time units and exponential local elapsed-time decay."
    - "The activity hook receives only (neuron_id, local timestamp, activation)."
  unresolved:
    - "Luna-3 must define prediction matching and explicit prediction-error event semantics."
    - "Luna-5 and Luna-8 must replace the current local accounting/eligibility placeholders with their owned policies."
  recommended_next_agent:
    - "Luna-3: add local predictive state and explicit error events without changing receive/emit causality."
    - "Luna-5: define local energy/resource accounting against activity hooks."
    - "Luna-8: define delayed-credit behavior using the eligibility hook."
    - "Luna-11: independently verify the integrated acceptance matrix after downstream components exist."
```

## Outcome and owned scope

Added `TPCNNeuron` in `tpcn/canonical_neuron.py` and exported it from the
package, including the public `from tpcn import TPCNNeuron` interface. The
neuron has bounded signed state, bounded tanh activation, a
monotonic neuron-local clock, exponential local elapsed-time decay, addressed
numeric event receipt, and queue-backed event emission. Emission uses
`EventQueue.push_propagated`; it never mutates a destination inline.

The module exposes local `prediction_state`, `prediction_error`,
`eligibility_state`, and `energy_state` fields plus a local activity hook for
downstream roles. These are compatibility surfaces only. This assignment does
not implement predictive coding, explicit error events, a utility objective,
delayed credit, classifier behavior, topology construction, structural
plasticity, or hardware behavior.

## Architecture evidence

- **A01-A03:** `receive_event()` advances only the addressed neuron's local
  clock; irregular event timestamps drive decay, and `emit_event()` queues
  propagation through Luna-1. Tests cover idle neurons, local elapsed time,
  and delayed destination mutation.
- **A04/A08:** state is clamped to `[-state_limit, state_limit]`, activation is
  bounded to `[-1, 1]`, and no pending state is added outside the finite Luna-1
  queue.
- **A05:** no spatial coordinates or reservoir dependency was introduced.
- **A06/A07:** no prediction policy or global state is consumed. Non-numeric,
  label-like payloads are rejected, and the activity hook receives local data
  only.
- **A09/A11:** local activity and eligibility fields/hooks are exposed for
  compatible downstream ownership; no Luna-5 energy utility or Luna-8 delayed
  credit policy is implemented.
- **A12-A13/A14:** no mandatory pathway count, learned gate, or structural
  plasticity was introduced.
- **A15:** the reference uses bounded scalar state, fixed local fields, and
  runtime primitives suitable for later software/hardware mapping.

No Architecture Change Proposal is required or requested. No contract clause
was changed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_canonical_event_neuron.py` | Windows PowerShell, Python 3.10.8 | Pass, 9 tests including public import regression | Focused Luna-2 suite |
| `python -m pytest -q` | Windows PowerShell, Python 3.10.8; deterministic tests use seed 17 | Pass, 27 tests | Full available pytest suite |
| `python -m compileall -q tpcn tests` | Windows PowerShell, Python 3.10.8 | Pass | Package and tests compile |
| VS Code file diagnostics | Current workspace | No errors in touched Python files | `canonical_neuron.py`, `__init__.py`, and focused tests |

## Benchmark and resource results

Dataset, split, classification, prediction metrics, connectivity utilization,
hardware timing, and calibrated energy units are not applicable to this
component and were not run. The local `energy_state` is an activity proxy and
not a utility decision or physical energy measurement. No global neural tick
or execution-batch timestep is used.

## Assumptions, limitations and unresolved issues

The canonical input contract is deliberately numeric and local. Luna-3 may
define richer typed payloads or event categories through compatible interfaces,
but must preserve causal queue delivery and label isolation. The current
`energy_state` and `eligibility_state` fields provide bounded local extension
points only; downstream owners must define their semantics before integration.

The package-level import is covered by a public API regression test. No neuron
API redesign was made.

## Reproduction and rollback

From the repository root, run:

```text
python -m pytest -q
python -m compileall -q tpcn tests
```

The work is uncommitted on `main` at the recorded revision. Remove the three
Luna-2 implementation/test/export additions to restore the pre-assignment
Luna-2 state while preserving unrelated topology and agent changes.

## Next assignment

Luna-3 should consume `TPCNNeuron` and define local prediction matching plus
explicit causally propagated error events. Luna-5 and Luna-8 should establish
the policies behind the local energy and eligibility extension points. Luna-4
can consume the unchanged Luna-1 queue contract for bounded topology.