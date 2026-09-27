# Luna-10 Structural Plasticity and Topology Adaptation Handoff

```yaml
tpcn_handoff:
  agent: Luna-10 Structural Plasticity and Topology Adaptation
  task_id: "structural-plasticity-luna-10"
  component: "bounded local deterministic topology adaptation"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "af5575ce0a629f101486bf36d930218eecdef77b"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A07", "A08", "A14", "A15"]
  preserves:
    - "Validated Luna-1 event timing, Luna-4 bounded routing, and all Luna-5 through Luna-8 public contracts."
    - "Finite nodes, edges, fan-in/out, routing resources, and deterministic replay."
    - "Real dataset benchmarking and hardware acceptance remain deferred."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/structural_plasticity.py"
    - "tests/test_structural_plasticity.py"
    - "workflow/handoffs/structural-plasticity-Luna-10.md"
  tests_added:
    - "tests/test_structural_plasticity.py: 13 focused tests"
  tests_passing:
    - "Focused structural-plasticity suite: 13 passed"
    - "Owning dependency regression slice: 57 passed"
    - "python -m compileall -q tpcn tests: passed"
    - "git diff --check: passed"
  tests_failed:
    - "Full pytest collection is blocked by unrelated dirty-worktree integration imports: missing existing tpcn exports and missing tpcn/experiments.py"
  tests_not_run:
    - "Full repository regression completion: blocked during collection by the unrelated imports above."
    - "Dataset benchmark: not run; dataset/version/split remains unresolved."
    - "Hardware acceptance: not run; FPGA, FPAA, hybrid, and calibrated evidence remain deferred."
    - "Joint Luna-9/Luna-10 integration review: not run; requires Luna-0 authorization."
  assumptions:
    - "The current dirty worktree contains unrelated changes that must be preserved."
    - "The public BoundedTopology API is stable; foundational topology changes are out of scope."
  unresolved:
    - "Full repository collection must be repaired by the owning integration changes before a complete regression count can be reported."
    - "Hardware backpressure and precision tolerances remain downstream integration decisions."
  recommended_next_agent:
    - "Luna-0: review this handoff and the unrelated collection blockers before joint integration."
```

## Outcome and owned scope

Implemented `StructuralPlasticityController` above the public `BoundedTopology`
API. `CandidateEvidence` is immutable, source-observed evidence with no label
or reward fields. The public API is `submit`, `select`, `grow`, `adapt`,
`adapt_many`, `prune`, `prune_by_score`, `state`, `candidates`, and `topology`.

Locality is either the finite topology node set, when no neighborhood map is
needed, or an explicit directed `local_neighbors` map. A candidate must have
an observer equal to its source, distinct endpoints in the topology, and a
destination in the configured source neighborhood. No topology-wide search is
performed by the controller.

Growth is bounded by `candidate_capacity`, topology edge capacity, fan-in/out,
and `max_growth_per_adaptation`. `adapt_many` selects by descending score,
then source, destination, and evidence identifier; duplicate endpoint records
keep the deterministic best record. The complete selected batch is staged
through `BoundedTopology.from_edges` and committed only after all constraints
pass, so capacity or degree failure leaves the current topology unchanged.
Single-edge retries report explicit `duplicate`, `full_capacity`, `rejected`,
or `grown` statuses and never create duplicate edges.

Pruning is an explicit safe-point operation. `prune_by_score` accepts only
finite caller-supplied edge scores, removes the lowest scores with stable
endpoint ties, and honors `minimum_edge_count`; there is no mutation history
or wall-clock dependency. Rebuilding preserves all edge propagation metadata.
Already queued events remain owned by the runtime queue and are delivered with
their original delay; only future routing sees the new topology.

`PlasticityState` exposes edge, routing, candidate, fan-in/out, growth, and
retention bounds. Candidate inspection is sorted and read-only. No persistent
history, RNG, labels, future events, or global state is retained.

Owned files changed: `tpcn/structural_plasticity.py`,
`tests/test_structural_plasticity.py`, and this handoff. No topology, Luna-9,
Luna-11, runtime, neuron, classifier, or package-export files were modified.

## Architecture evidence

- **A01-A03:** No neural clock or wall-clock dependency is used. Routing stays
  delegated to `BoundedTopology.route`; pruning changes only future routing and
  leaves queued delayed events intact.
- **A04:** Node, edge, fan-in/out, routing, candidate, growth, retention, and
  edge-capacity limits are finite. Duplicate, rejection, and capacity-full
  outcomes are explicit.
- **A05:** No spatial reservoir or coordinate dependency is introduced.
- **A07:** Evidence must identify a local observer equal to the source;
  selection consumes only supplied bounded records and no labels or global
  evaluation state.
- **A08:** Controller state is bounded by candidate and topology capacities and
  retains no event or mutation history.
- **A14:** Structural changes use explicit local evidence and public bounded
  topology operations. Batch commits are atomic and pruning is retention
  bounded. This remains an experimental supported layer; no ACP is required
  and no core invariant was promoted.
- **A15:** Immutable records, finite collections, deterministic ordering, and
  explicit rejection paths preserve software-reference and hardware mapping
  options.

## Validation record

Environment: Windows PowerShell, Python 3.10.8, current uncommitted worktree,
base revision `af5575ce0a629f101486bf36d930218eecdef77b`. Tests use fixed
inputs and no random seed; deterministic ordering is explicit.

| Command or procedure | Observed result | Evidence |
|---|---|---|
| `python -m pytest -q tests/test_structural_plasticity.py` | 13 passed | Locality, deterministic ties, duplicate/rejection/full-capacity outcomes, atomic batch growth, fan-in/out, pruning/in-flight routing, bounded state, replay, retention, isolation |
| `python -m pytest -q tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py tests/test_predictive_coding.py tests/test_eligibility.py tests/test_structural_plasticity.py` | 57 passed | Owning dependency regression slice |
| `python -m pytest -q` | collection blocked | Unrelated dirty-worktree imports: missing existing `tpcn` exports and missing `tpcn/experiments.py`; no Luna-10 test failure observed |
| `python -m compileall -q tpcn tests` | passed | No compilation errors |
| Workspace diagnostics for owned implementation and tests | no errors | `get_errors` returned no errors |
| `git diff --check` | passed | No whitespace errors |
| Dataset benchmark | not run | Dataset/version/split not selected |
| Hardware acceptance | not run | FPGA/FPAA/hybrid and calibrated checks deferred |
| Joint Luna-9/Luna-10 integration review | not run | Luna-0 review remains required |

The owned software-reference checks pass. Full repository regression remains
blocked by unrelated collection errors in the current dirty worktree. Dataset,
hardware, and joint integration gates remain not run as listed above.

## Next assignment

Luna-10 returns control to Luna-0. The dedicated joint review remains pending
and this handoff does not authorize dataset benchmarking or hardware acceptance.
