---
tpcn_handoff:
  agent: "Luna-34 EXCURSION_V1 Multi-Emitter Candidate-Formation Bridge"
  luna_identifier: "Luna-34"
  descriptive_name: "Bounded EXCURSION_V1 multi-emitter mechanism diagnostic"
  task_id: "luna-34-excursion-v1-multi-emitter-candidate-formation-bridge-20261004"
  component: "Fixed-edge propagation-to-emission bridge and ACP-0007 candidate observability"
  status: "BLOCKED — EXISTING PUBLIC API INSUFFICIENT"
  contract_version: "1.2"
  branch: "main"
  base_revision: "c6f0f3b0e8c2e4d0883c7e1627cd5112ab6fa937"
  api_baseline: "1e2f80aa9e37b332e0637f6ff8b0df18d5f2ceb6"
  owner: "Luna-0 Architecture Guardian"
  classification: ["EXPERIMENT", "OBSERVATION", "CAUSAL DIAGNOSTIC"]
  architecture_change: false
  proposal: null
  tests_added:
    - "tests/test_luna34_excursion_v1_multi_emitter_bridge.py"
  tests_passing:
    - "Focused Luna-34 tests: 9 passed."
    - "Full repository suite: 929 passed, 1 skipped."
    - "Runner and test compilation passed."
    - "git diff --check passed."
  tests_failed: []
  tests_not_run:
    - "Complete 960-execution diagnostic: blocked on the existing runtime eligibility-trace capacity."
    - "Per-condition mechanism counts and deterministic full-design replay."
    - "CUDA test body: skipped because CUDA is unavailable."
    - "Task efficacy, resource/prediction benefit, and hardware equivalence: excluded."
  recommended_next_agent: ["Luna-0 Architecture Guardian"]
---

# Luna-34 completion handoff

## Authorization and baseline

The execution began at clean synchronized `main`:

```text
HEAD = origin/main = c6f0f3b0e8c2e4d0883c7e1627cd5112ab6fa937
worktree before implementation = clean
```

The Luna-34 dispatch pins its public API facts to
`1e2f80aa9e37b332e0637f6ff8b0df18d5f2ceb6`. Between that API revision and
the requested execution baseline, the only committed changes are publication
of the dispatch/decision/workflow governance files; no runtime or experiment
code changed. The dispatch owns only the runner, focused tests, three
artifacts, and this handoff. Workflow and changelog edits were not made
because the governing Luna-34 contract explicitly prohibits them.

## Attempt and terminal classification

The exact authorized design was configured and invoked once:

```text
.venv\Scripts\python.exe run_luna34_excursion_v1_multi_emitter_bridge.py
```

It stopped with:

```text
EligibilityCapacityError: eligibility trace capacity reached
```

The exception arose while `ExcursionCharacterRuntime._consume_emission()`
called `EligibilityLedger.record_activity()`. The required runtime
configuration uses `prediction_capacity=8` and two nodes; the existing
runtime allocates `prediction_capacity * max(1, neuron_count)`, or 16,
eligibility entries per node. The full generated design could not complete
under that fixed contract. The uncaught first attempt did not preserve its
seed/condition/sequence index or return an `ExcursionCharacterResult`; the
runner writes artifacts only after every seed and condition finishes.

Accordingly, the independent terminal classification is:

```text
BLOCKED — EXISTING PUBLIC API INSUFFICIENT
```

This is not evidence that any condition failed to produce a downstream
emitter. Bridge status under each condition, candidate formation,
`|w|=2` sensitivity, and no-edge-control validity remain **NOT DETERMINED**.
No condition or input sequence was changed, and no second full experiment
attempt was made.

## Declared design (not completed)

The frozen plan used seeds 0–4; 16 examples per class; training generator
seeds `12007 + seed`; evaluation generator seeds `22017 + seed`; and order
stream `random.Random(330000 + seed)`. Only each training example's `points`
were read. Inputs were `point.x + point.y` at the supplied timestamps.
Character IDs were derived from seed and shuffled sequence index. The
planned 320 streams were paired across:

1. `NO_EDGE_CONTROL`: zero active route edges.
2. `DEFAULT_STATIC_EDGE`: `source -> destination`, `w=1.0`, `d=1.0`, `r=0.0`, delay `1.0`.
3. `STATIC_N2_BOUND_SENSITIVITY`: the same edge with only `w=2.0`.

The two-node, edge/routing capacity 1, fan-in/out 1, queue 128, runtime
event budget 1024, settling horizon 4.0, default neutral `E1Config`,
prediction capacity 8 and expiry 4.0, and structural observation/evidence
bounds were declared in `config.json`. No topology mutation or efficacy
endpoint was introduced.

## Evidence and checks

Observed:

- The focused tests exercise the public runtime path, event/transfer identity
  reconciliation, recipient deduplication, candidate order/locality/window,
  character-local observation reset, exact edge conditions, point batching,
  point-only dataset use, negative-control behavior on a small neutral
  fixture, and serialized replay determinism.
- Focused tests: **9 passed**.
- Full repository suite: **929 passed, 1 skipped**.
- The skipped test was `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`,
  skipped because CUDA is unavailable.
- Runner/tests compile successfully; `git diff --check` passed.
- The first full-suite collection attempt initially found missing NumPy and
  Torch in the terminal interpreter. Those packages were installed in the
  configured environment; SciPy was installed after the next collection
  failure. The final complete suite then passed as above. No dependency
  manifest was changed.

Not observed because execution blocked:

- Complete per-character canonical-emission and routed-transfer records.
- Per-condition receiving counts, route depths, accumulator maxima, and
  source-before-destination candidate counts.
- Full 320-stream / 960-execution replay digests or paired N2 sensitivity.
- A valid experiment-wide negative-control conclusion.

The blocked attempt and its limits are recorded in
`artifacts/acp0007-luna34-multi-emitter-bridge/results.json` and
`artifacts/acp0007-luna34-multi-emitter-bridge/summary.json`. The complete
declared design is in
`artifacts/acp0007-luna34-multi-emitter-bridge/config.json`.

## Required return to Luna-0

The smallest unresolved issue is that the accepted public runtime has no
experiment-facing control for its internally derived eligibility-trace
capacity, or bounded overflow behavior that still returns the canonical
character result and trace, while Luna-34 fixes `prediction_capacity=8`.
This handoff requests Luna-0 review of that public-API limitation and does
not implement a workaround. No architecture change is recommended by this
incomplete run; it neither demonstrates nor falsifies the declared bridge
hypotheses. ACP-0007, the Luna-33 verdict, task-efficacy scope, and hardware
claims remain unchanged. No Luna-35 is authorized.
