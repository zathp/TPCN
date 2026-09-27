Luna-12 Completion Handoff

```yaml
tpcn_handoff:
  agent: Luna-12 Visualization Contract and CPU Reference Exporter
  task_id: visualization-contract-luna-12
  component: downstream visualization format and CPU reference path
  status: complete
  contract_version: "1.0"
  branch: main
  base_revision: 1cf40659d1ff05e71c2f2cc5e730633805b7129f
  result_revision: uncommitted
  architecture_invariants_touched: [A01, A03, A04, A07, A08, A15]
  preserves:
    - canonical TPCN computation and event semantics
    - classifier, reward, topology, timestamp, and queue state
    - optional visualization and downstream-only observation
  architecture_change: false
  proposal: null
  files_changed:
    - tpcn/visualization.py
    - tpcn/__init__.py
    - tpcn/energy_utility.py
    - tests/test_visualization.py
    - workflow/docs/luna/VISUALIZATION_CONTRACT.md
    - workflow/README.md
    - workflow/handoffs/visualization-contract-Luna-12.md
  tests_added:
    - tests/test_visualization.py: 13 focused tests
  tests_passing:
    - focused visualization suite: 13 passed
    - focused visualization/energy/Luna-11 checks: 28 passed, 2 stale strict-xfail XPASS
    - full regression: 116 passed, 2 stale strict-xfail XPASS (pytest exit 1)
    - python -m compileall -q tpcn tests
    - git diff --check
    - workspace diagnostics for touched files: no errors
  tests_failed:
    - full pytest exit is nonzero because two pre-existing Luna-7 tests are strict xfail markers around behaviors that are now fixed in the current classifier
  tests_not_run:
    - GPU, ModelSim, FPGA, VGA, Ethernet, and hardware equivalence: outside Luna-12
    - dataset benchmarking: outside this observability milestone
  assumptions:
    - owner-supplied Luna-11 pass is the authorization premise; the stale Luna-11 handoff remains preserved
    - visualization callers provide only separately authorized observable state
  unresolved:
    - Luna-0 should reconcile the two stale strict-xfail markers with the current Luna-7 implementation
  recommended_next_agent:
    - Luna-0 review and gate decision
```

## Outcome and owned scope

Luna-12 defines and implements TPCV version 1, a compact big-endian binary
snapshot format with deterministic sorted records, bounded UTF-8 identifiers,
fixed-width numeric fields, explicit incomplete captures, and strict parser
validation. The CPU path consists of `VisualizationSnapshot`, immutable neuron
and connection records, `export_snapshot`, `parse_snapshot`,
`SnapshotCollector`, and `ReferenceVisualizer`.

The exporter is pull-based and downstream-only. It does not inject events,
consume queues, call classifier/reward code, change topology, or mutate source
objects. The focused workload test compared disabled, every-step, and
intermittent capture and found identical neuron state, activation, processed
counts, local timestamps, queue contents, and topology edges.

Classifier labels, reward messages, queue contents, and hidden global state are
not represented. The current topology exposes propagation delay but no edge
strength, so no synthetic strength is serialized. Optional coordinates are
supported as diagnostic metadata but are not required by the core.

## Architecture evidence

- A01/A03: timestamps are explicit snapshot metadata; export does not create
  neural ticks or route events.
- A04/A08: record counts, identifiers, numeric fields, and collector capacity
  are bounded with rejection rather than wraparound or truncation.
- A07: no labels, rewards, or unrestricted global state are pulled implicitly.
- A15: the fixed-width, big-endian, hexadecimal-friendly layout is suitable as
  a reference for later CPU/GPU/simulation/FPGA adapters.

No computational architecture clause changed and no ACP is required.

## Format summary

Header: `TPCV`, version `1`, flags, reserved fields, epoch, timestamp, neuron
count, connection count, and body length. All integers and doubles are
big-endian. Neuron records carry identifier, active flag, state, activation,
processed-event count, and optional signed 32-bit position. Connection records
carry source, destination, and propagation delay. Records are sorted by stable
identifiers. The CPU reference bounds complete snapshots to 1 MiB and accepts
empty snapshots; malformed, unsupported, reserved, truncated, over-limit, and
framing-invalid input is rejected.

The full contract is in [VISUALIZATION_CONTRACT.md](../docs/luna/VISUALIZATION_CONTRACT.md).

## Validation record

| Command or procedure | Revision / environment | Observed result |
|---|---|---|
| Baseline | `1cf40659d1ff05e71c2f2cc5e730633805b7129f`, Windows PowerShell, Python 3.10.8 | recorded; unrelated pre-existing workflow edits preserved |
| `python -m pytest -q tests/test_visualization.py` | same environment | 13 passed |
| focused visualization, energy, Luna-11 suite | same environment | 28 passed; 2 strict-xfail XPASS |
| `python -m pytest -q` | same environment | 116 passed; 2 strict-xfail XPASS, exit 1 |
| `python -m compileall -q tpcn tests` | same environment | passed |
| `git diff --check` | same worktree | passed |
| workspace diagnostics | touched implementation/tests/docs | no errors reported for touched code files |

## Assumptions, limitations and unresolved issues

The full regression status is not a clean pytest pass solely because existing
strict-xfail markers have become stale; Luna-12 did not change classifier
behavior. The current checkout also required minimal package export/API
repairs (`tpcn/__init__.py` and `RewardMessage.to_reward_signal`) to collect
the established regression tests. No GPU, simulation, FPGA, display, transport,
dataset, or hardware equivalence claim is made.

## Reproduction and rollback

Run the commands in the validation table from the repository root. The exact
baseline revision is recorded above. Revert only the Luna-12 files if needed;
preserve the unrelated pre-existing worktree changes listed by `git status`.

## Next assignment

Return control to Luna-0. Luna-0 may review this evidence and decide whether the
Luna-12 gate passes. Luna-13 may rely on the TPCV-1 parser and logical record
contract only after explicit Luna-0 authorization. Luna-14 may likewise rely on
the format for a later ModelSim/FPGA bridge. Neither milestone is authorized by
this handoff, and no subsequent milestone is promoted automatically.

## Required completion evidence

Record the canonical format, parser/exporter interfaces, deterministic and bounded serialization, malformed/version/empty-state behavior, capture-on/off invariance, exact commands and environment, and all unrun checks using the handoff template.
