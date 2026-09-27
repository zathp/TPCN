# Luna-12H Dispatch Handoff

```yaml
tpcn_handoff:
  agent: Luna-12H Intrinsic Temporal State, Recurrence, and Unequal-Delay Convergence
  task_id: "intrinsic-temporal-state-recurrence-unequal-delay-convergence-luna-12h"
  component: "canonical temporal state, bounded recurrence, and unequal-delay event-routing verification"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "3b2b03208286eca57d86e1d83359b9e233074d32"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A15"]
  preserves:
    - "Event-driven computation with no mandatory global neural timestep."
    - "Finite bounded topology, propagation, queue behavior, state, and recurrent dynamics."
    - "Label-free neural computation and the external readout boundary established by Luna-12F/12G."
    - "Independent Luna-13 and Luna-14 visualization/hardware branches."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/luna/LUNA_12H_TEMPORAL_STATE_RECURRENCE.md"
    - "workflow/README.md"
    - ".github/agents/luna-12h.agent.md"
    - "workflow/handoffs/intrinsic-temporal-state-recurrence-unequal-delay-convergence-Luna-12H.md"
    - "tests/test_luna12h_temporal.py"
  tests_added:
    - "tests/test_luna12h_temporal.py: 9 focused fixtures"
  tests_passing:
    - "python -m pytest -q tests/test_luna12h_temporal.py: 9 passed"
    - "focused and related regression slices: 118 passed"
    - "python -m compileall -q tpcn tests run_spiral_benchmark.py"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "Full pytest: not run in this pass; related regression slices passed."
    - "GPU/FPGA/ModelSim, real-dataset, and hardware acceptance: not applicable to Luna-12H."
  assumptions:
    - "A01-A03 and A08 already permit the requested local-state and bounded-recurrence semantics."
    - "The accepted Luna-12E routing path is the implementation integration point."
    - "Luna-12G results are motivating evidence, not evidence that the core lacks all possible temporal state."
  unresolved:
    - "The spiral benchmark remains order-insensitive at the external readout; this is a 12G limitation and not a failure of the intrinsic temporal fixtures."
    - "Cycle termination is demonstrated with an explicit finite event budget and queue capacity; the current generic runtime does not independently track lineage or reject a caller that continually re-routes a cycle."
  recommended_next_agent:
    - "Luna-12H implementation and verification role"
    - "Luna-0 review after the completed 12H evidence handoff"
```

## Authorization and outcome

Luna-0 authorizes Luna-12H on 2026-09-27 as an implementation and verification
milestone following Luna-12G. The architecture contract already permits local
elapsed-time state, finite propagation and bounded recurrent dynamics. This
change clarifies canonical evidence obligations; no ACP is required. The
existing canonical neuron and Luna-12E routing path already implement the
required semantics, so this milestone adds focused evidence without changing
production behavior.

## Required owned scope

Implement and verify intrinsic persistent state, event-time evolution,
temporal noncommutativity, unequal cumulative path delays, timestamp-preserving
fan-in, convergent old/new arrivals, path pruning, bounded cycles, reset
boundaries and label isolation. Use the accepted Luna-12E event-routing path;
do not create a second topology or an external temporal classifier.

## Required evidence after implementation

Run the twelve Luna-12H acceptance checks and the six specified fixtures,
including exact state/output/trace observations, edge and path delays,
emission/arrival timestamps, queue/tie order, pruning effects, reset behavior,
cycle bounds, seeds and label-isolation comparisons. Record time units,
capacities, decay/evolution law, pending-event policy and all applicable
regression, compile, diagnostic and diff checks.

## Verified implementation semantics

The canonical neuron uses event timestamp units and applies analytic
exponential decay before each event or explicit local observation:

```text
s(t1-) = clamp(s(t0+) * exp(-decay_rate * (t1 - t0)))
s(t1+) = clamp(s(t1-) + input_gain * payload)
activation = tanh(s)
```

The default state bound is `[-1, 1]`, event timestamps are monotonic per
neuron, equal-time queue ties use insertion sequence, and queue capacity is
finite. There is no global timestep, background event, or wall-clock input.
`reset()` clears character-local temporal, prediction, eligibility, energy,
activation, and processed-event state; topology is independently retained.

The pre-12H audit therefore found persistent bounded state and elapsed-time
evolution already present, rather than a memoryless event transform. A single
spike at `t=0` evolves to `exp(-0.5)` at `t=1` and `exp(-1.0)` at `t=2` for
decay rate `0.5`.

## Fixture results

- Ordered pair and equal multiset: `(+1,-1)` and `(-1,+1)` produce distinct
  state and activation traces at timestamps `0` and `1`.
- Interval sensitivity: the same pair at `0,1` and `0,5` produces distinct
  final states through the decay term.
- Unequal paths: direct `A->C` delay is `1.0`; long `A->B->D->C` cumulative
  delay is `1.5 + 1.0 + 1.5 = 4.0`.
- Convergence: old `t=0` and newer `t=3` source events produce C arrivals at
  `1.0`, `4.0`, `4.0`, and `7.0`; equal-time order is deterministic.
- Timing intervention: close and separated arrivals produce different C
  state. Removing either `A->B` or `A->C` removes that path's future effect.
- Recurrence: the `A<->B` cycle is executed under a four-event budget; local
  timestamps remain monotonic and the finite queue remains bounded.
- Reset/isolation: reset returns state and local time to zero; relabeling an
  identical event stream produces the same neural trace.
- Same-seed determinism: repeated identical event streams reproduce activation
  traces exactly.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Architecture/document review | `3b2b03208286eca57d86e1d83359b9e233074d32`, Windows, Python environment not used | passed for documentation scope | Contract, acceptance criteria, workflow, dispatch, and handoff created/updated |
| `python -m pytest -q tests/test_luna12h_temporal.py` | Python reference, deterministic fixtures | passed: 9 | Intrinsic state, order/interval sensitivity, unequal paths, convergence, pruning, fan-in ties, recurrence bound, reset, labels, determinism |
| Related regression slice | Python reference | passed: 118 | Canonical neuron, runtime, topology, predictive coding, structural plasticity, 12E, 12G, visualization/analysis and integration tests |
| `python -m compileall -q tpcn tests run_spiral_benchmark.py` | Python reference | passed | No compile errors |
| `git diff --check` | current worktree | passed | Git reported only existing line-ending warnings |

## Architecture decision

Existing architecture permits evolving recurrent local state and unequal-delay
finite propagation. The contract was clarified under A02, A03 and A08, with
related acceptance obligations under A01-A04, A07-A08 and A15. No ACP was
required. The focused evidence establishes software-reference integration
readiness for the Luna-12H temporal-state scope; Luna-0 should review this
handoff before promotion.

## Next assignment

Return control to Luna-0 for review of this completed evidence. Luna-13 and
Luna-14 remain independent.
