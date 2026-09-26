# Luna-0 Milestone 1 Architecture Intake

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  task_id: "milestone-1-event-classifier-intake"
  component: "repository assessment, dependency graph, and architecture gate"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "fda3f03"
  result_revision: "uncommitted documentation-only assessment"
  architecture_invariants_touched: []
  preserves:
    - "A01-A15 contract remains unchanged."
    - "Legacy reservoir and signal-copy implementations remain separate baselines."
    - "Milestone 1 remains streaming and predictive, with explicit error events and local resource accounting."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/milestone-1-event-classifier-intake-Luna-0.md"
  tests_added: []
  tests_passing:
    - "python -m compileall -q tpcn Main.py train_tpcn.py"
  tests_failed: []
  tests_not_run:
    - "pytest suite: no tests collected"
    - "Milestone 1 streaming benchmark: not implemented"
    - "Luna-11 acceptance suite: not implemented"
  assumptions:
    - "workflow/ is the current authoritative documentation location; the tracked tpcn-luna-workflow deletion state is preserved."
    - "Dataset, version, split, time units, tie ordering, capacities, utility formula, and hardware tolerances remain open decisions."
  unresolved:
    - "No event runtime, event neuron, bounded topology, stroke stream, classifier interface, or Milestone 1 verification suite exists in the active implementation."
    - "No Luna-1 through Luna-11 implementation handoffs exist yet."
  recommended_next_agent:
    - "Luna-1: define and test hardware-neutral event semantics before dependent core work."
```

## Repository assessment

The active implementation is a legacy/experimental collection, not an Event Classifier Milestone 1 implementation:

| Component | Current state | Milestone 1 disposition |
|---|---|---|
| Event runtime and causal queue | Missing | Luna-1 prerequisite |
| Canonical event neuron | Missing | Luna-2 after Luna-1 |
| Bounded topology and finite routing | Partial legacy masks in `tpcn/signal_copy_distance/space.py`; no event graph | Luna-4 after Luna-1, with new bounded graph contract |
| Predictive coding and explicit error events | Partial batched tensor prediction/error in `train_tpcn.py` and signal-copy trainer; no event representation | Luna-3 after Luna-2/Luna-4 |
| Local energy and utility | Activity-like/tonic options exist in legacy trainer; no local reward-adjusted API | Luna-5, parallel after interfaces are agreed |
| Sequential stroke dataset | Missing | Luna-6, parallel; dataset/split must be declared |
| Delayed credit | Delayed tensor error buffers exist in legacy code; no event eligibility/reward interface | Luna-8, parallel; coordinate with Luna-5 |
| Classification interface | Missing | Luna-7 after core predictive interfaces and stroke stream |
| Verification suite | Missing; `pytest` collected no tests | Luna-11 after Luna-7 |
| Emergent gating | Missing as Milestone 1 core | Deferred Luna-9 until verification passes |
| Structural plasticity | Optional legacy edge growth exists | Deferred Luna-10 until verification passes |
| Hardware realization | Existing unrelated VHDL cell/artifacts | Not evidence for event-core equivalence; defer hardware gate |

The existing `DistanceSignalCopyNet` has finite masks and a structural edge budget, but its `step()` method advances a whole batch synchronously and uses continuous matrix propagation. `train_tpcn.py` also contains a spatial reservoir backend and global/distributed reductions. These are useful legacy comparisons only and do not satisfy A01-A07 for the new core.

## Dependency-aware task graph

```text
Luna-1 Event Runtime
    |
    +--> Luna-2 Canonical Event Neuron --+
    |                                    +--> Luna-3 Predictive Coding / Error Events
    +--> Luna-4 Bounded Topology --------+

Luna-5 Energy / Utility ------------------------------+
Luna-6 Sequential Stroke Dataset --------------------+--> Luna-7 Classification Interface --> Luna-11 Verification
Luna-8 Delayed Credit -------------------------------+

After Luna-11 passes the baseline gate only:
    Luna-9 Emergent Gating
    Luna-10 Structural Plasticity
```

Luna-5 and Luna-8 need a shared interface decision for local activity, usefulness, eligibility, delayed reward, and cost units. Luna-6 can proceed independently once the dataset and causal preprocessing protocol are recorded. Luna-7 must keep labels outside the reusable core and consume only streamed stroke events plus declared reward/error messages.

## Ownership and bounded assignments

| Role | Owned scope | Completion evidence |
|---|---|---|
| Luna-1 | Event, queue, local time, delay, event ordering, batching semantics | Causality, positive delay, irregular timestamps, deterministic tie policy tests |
| Luna-2 | Canonical bounded-state event neuron | Local receive/advance/emit behavior and bounded-state tests |
| Luna-4 | Finite graph, fan-in/out, routing and capacity checks | Construction/rewiring rejection and finite propagation tests |
| Luna-3 | Local prediction matching and explicit error events | Delayed target/error event test; no instantaneous distant effect |
| Luna-5 | Local activity cost and reward-adjusted utility API | Energy reconciliation plus high-cost useful/unproductive behavior tests |
| Luna-6 | Native temporal stroke event stream and splits | Causal START/stroke/END stream, no future-point preprocessing, reproducible split |
| Luna-8 | Eligibility and delayed reward/credit | Later reward modifies eligible local activity without global state leakage |
| Luna-7 | External readout/training interface for classification | Streaming declared class count, label isolation, final readout protocol |
| Luna-11 | Independent verification and benchmark evidence | Acceptance matrix with pass/fail/not-run evidence on exact revision |
| Luna-0 | Contract review, interface conflict resolution, final integration gate | Completed architecture review and linked handoffs; no unapproved ACP departure |

Every implementation assignment must use the handoff template and name exact owned files, dependencies, acceptance checks, baseline revision, and next role. Parallel assignments require stable interfaces and non-overlapping ownership.

## Architecture risks

- **Global timestep leakage (A01-A03):** existing trainers use synchronous batch/step loops; execution batches must not become neural time.
- **Spatial reservoir contamination (A05):** `train_tpcn.py` and inspiration modules depend on spatial reservoir concepts; they cannot be used as the reusable core.
- **Global learning leakage (A07):** distributed reductions and aggregate tensor losses must not enter core neuron inputs or replace local learning.
- **Unbounded state/topology (A04, A08, A14):** capacities, queue overflow, pending-event policy, and bounded state must be explicit before rewiring or growth.
- **Predictive identity loss (A06):** a classifier-only implementation is insufficient; prediction targets and explicit propagated error events are required.
- **Energy objective collapse (A09-A10):** inactivity must not be rewarded as efficiency; useful expensive activity and unproductive expensive activity need separate evidence.
- **Delayed-credit ambiguity (A11):** eligibility scope, reward arrival, expiry, and attribution must be defined before integration.
- **Dataset and label leakage:** the actual stroke dataset, classes, writer-disjoint split where available, causal preprocessing, and reset rules are open.
- **Premature experiments:** Luna-9 gating and Luna-10 structural plasticity are blocked until Luna-11 verifies the baseline classifier architecture.
- **Hardware overclaim (A15):** existing VHDL artifacts do not establish event-core equivalence or calibrated energy measurements.

## Validation record

| Command or procedure | Revision/environment | Result |
|---|---|---|
| Read contract, changelog, workflow, acceptance criteria, ACP template, and handoff template | `main` at `fda3f03`; current `workflow/` | Complete |
| `git status --short`, branch, revision, recent log | Windows PowerShell | Main at `fda3f03`; user-managed workflow migration changes present |
| `python -m pytest --collect-only -q` | Local Python | No tests collected; exit code 1 |
| `python -m compileall -q tpcn Main.py train_tpcn.py` | Local Python | Passed |

## ACP status and integration readiness

No ACP is required for this assessment. The planned work can preserve A01-A15 if it introduces the event interfaces rather than adapting the legacy reservoir into the core. An ACP becomes mandatory if an implementation proposes changing a contract invariant or promoting an experimental departure.

Milestone 1 is **not integration-ready**. It is blocked at the missing Luna-1 event runtime and has no verification evidence, streaming classifier, predictive error-event path, delayed credit, or reward-adjusted local energy benchmark. The next bounded assignment is Luna-1, with Luna-2 and Luna-4 queued behind its stable event contract.

## Reproduction and rollback

This handoff is documentation-only. Preserve unrelated working-tree changes. No implementation rollback is required; removing this handoff removes the assessment record.

## Next assignment

Assign Luna-1 to define the event schema, queue semantics, local timestamps, positive propagation delays, equal-time ordering, late-event policy, finite queue behavior, deterministic seed behavior, and batched/unbatched equivalence fixture. Luna-1 must leave its own completed handoff before Luna-2 or Luna-4 implementation begins.
