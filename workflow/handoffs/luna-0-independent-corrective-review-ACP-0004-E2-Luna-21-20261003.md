# Luna-0 Independent Corrective Review — ACP-0004 E2 / Luna-21

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent corrective review and closure of Luna-21 E2"
  task_id: "luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003"
  component: "ACP-0004 E2 runtime and TPCN-IR-2 revision 1 reconstruction"
  status: "complete; independently verified and closed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "3fb6d8c5128277bc8ecc5b2beea7288c214b772d"
  result_revision: "review publication commit; exact pushed tip is reported in the session result"
  dependencies:
    - "Luna-21 corrective implementation published"
    - "ACP-0004 E1 independently closed"
    - "ACP-0005 / TPCN-IR-2 revision 1 independently closed"
    - "ACP-0002 N2 Model-B independently closed"
  owner: "Project owner / Luna-0 architecture authority"
  classification: ["INDEPENDENT REVIEW", "ARCHITECTURE CONFORMANCE VERIFICATION", "ADVERSARIAL VERIFICATION"]
  hypothesis: "The corrective IR-2 validation closes the identified identity, boundedness and strict-future defects while preserving E1, E2 runtime behavior, N2 and schema revision 1."
  counter_hypothesis: "Independent replay exposes an identity reuse, budget bypass, causal reconstruction defect, regression or architecture departure."
  interfaces_relied_on:
    - "IR2Neuron / TPCNIR2 revision-1 parsing and serialization"
    - "neuron_from_ir2 E1-only and neuron_from_ir2_e2 E2 capability boundaries"
    - "SingleExcursionNeuron / MultiExcursionNeuron local event runtime"
    - "EventQueue destination-local external-before-internal ordering"
    - "BoundedTopology Model-B transfer"
  label_information_boundary:
    - "No task labels, evaluation state, learning, reward or global orchestration state were introduced."
  timing_assumptions:
    - "Local logical timestamps and analytic elapsed-time decay."
    - "Pending internal work entering E2 reconstruction must be strictly later than local time."
    - "Equal-time external-before-internal ordering is destination-local and unchanged."
  reset_boundaries:
    - "Reconstruction is distinct from reset and preserves character-local state, counters, provenance and pending validity."
  resource_bounds:
    - "All seven transferable execution counters are bounded by event_budget."
    - "One valid pending event, finite event budget, bounded topology and provenance capacity remain unchanged."
  authorized_scope:
    - "Independently reproduce and verify the bounded Luna-21 correction."
    - "Make a narrowly scoped review-owned regression/oracle correction."
    - "Synchronize workflow/changelog and publish the independent review."
  unauthorized_scope:
    - "Production implementation changes, successor Luna execution, H2, N3, learning, backends, hardware, calibration, hardware equivalence, IR-3 and A01-A15 amendments."
  controls:
    - "Closed E1 behavior and historical E1-only IR-2 reconstruction."
    - "E2 runtime dynamics and reset semantics."
    - "TPCN-IR-2 schema revision 1."
    - "ACP-0002 N2 Model-B transfer and event ordering."
  measurements:
    - "Original-blocker reproductions, identity/counter boundaries, E1/E2 compatibility, continuation traces, provenance round trips and regression counts."
  information_boundary_check:
    - "All corrective checks concern serialized local state; no evaluation or global state enters neuron computation."
  hardware_mapping:
    - "None; software-reference evidence only."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A11", "A15"]
  preserves:
    - "A01-A15"
    - "ACP-0004 staged architecture status and closed E1 behavior"
    - "ACP-0005 / TPCN-IR-2 schema revision 1"
    - "ACP-0002 N2 Model-B"
    - "Luna-17 reservation and Luna-13F closure"
  architecture_change: false
  proposal: "ACP-0004"
  files_changed:
    - "tests/test_e2_ir2.py"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003.md"
  files_reviewed:
    - ".github/agents/luna-0.agent.md"
    - ".github/agents/luna-21.agent.md"
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md"
    - "workflow/docs/architecture_proposals/README.md"
    - "workflow/docs/architecture_proposals/ACP-TEMPLATE.md"
    - "workflow/docs/architecture_proposals/ACP-0002.md"
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0005.md"
    - "workflow/handoffs/luna-0-independent-review-ACP-0004-E2-Luna-21-20261003.md"
    - "workflow/handoffs/luna-21-ir2-corrective-20261003.md"
    - "workflow/handoffs/luna-21-e2-multi-excursion-20261003.md"
    - "tpcn/ir2.py"
    - "tests/test_ir2.py"
    - "tests/test_e2_ir2.py"
    - "tpcn/excursion_neuron.py"
    - "tpcn/event_runtime.py"
    - "tpcn/topology.py"
    - "tpcn/__init__.py"
    - "tests/test_excursion_neuron.py"
    - "tests/test_e2_multi_excursion.py"
    - "tests/test_acp0002_n2.py"
    - "tests/test_event_runtime.py"
    - "tests/test_topology.py"
  tests_added:
    - "Strengthened test_e2_reconstruction_restores_counters_and_continues_with_unique_ids in tests/test_e2_ir2.py."
  tests_passing:
    - "Prior-revision independent repros: all three original production blockers reproduced."
    - "Independent S_PENDING/S_RETURN/M_ACTIVE high-water probes: all six malformed pairs rejected; valid equality remains accepted."
    - "Independent 4-mode x 7-counter x 3-boundary probe: budget-1 and budget accepted; budget+1 rejected."
    - "Independent strict-future probes: earlier rejected, equal rejected by E2 capability, later accepted, including optional-M-absent JSON round trip."
    - "E1 equal-time pending control and E1-only M_ACTIVE rejection."
    - "Bounded REFRACTORY continuation: original and reconstructed traces equal; nonempty outputs/transitions; final N/no pending."
    - "Review-owned counter-continuation oracle: 13 outputs; IDs differ from prior emission; sequences increase from prior 1 to subsequent 2; final N/no pending."
    - "Exact-capacity and overflow provenance round trips preserve fields and truncation."
    - "Full-state E2 reconstruction probe preserves state, configuration, counters, pending tuple, provenance and truncation without duplicate scheduling."
    - "Focused E2 runtime and E2 IR-2: 45 passed."
    - "E1 and IR-2 regression pair: 156 passed."
    - "N2 and event-runtime regressions: 254 passed."
    - "Topology: 9 passed."
    - "Final IR-2 and E2 IR-2: 116 passed."
    - "Full CPU suite: 768 passed, 1 skipped, 0 failed."
    - "compileall and git diff --check passed."
  tests_failed: []
  tests_not_run:
    - "GPU/FPGA/FPAA implementations, ModelSim, hardware equivalence, calibration, H2, N3, learning/benchmark evaluations and IR-3; these are unauthorized or outside this closure."
  assumptions:
    - "The repository's actual Git SHA at review start is authoritative; the external non-Git identifier in the request is not a repository revision."
    - "Zero-valued episode/lineage identities remain schema-legal because ACP-0004/ACP-0005 do not require one-based IDs; high-water validation still prevents reuse."
  unresolved: []
  recommended_next_agent:
    - "None assigned; future dependency planning must follow the updated authoritative workflow."
```

## Synchronization and revision lineage

**OBSERVED:** `git fetch origin` completed before review. The actual published
baseline was clean `main` with `HEAD == origin/main ==
3fb6d8c5128277bc8ecc5b2beea7288c214b772d`, subject
`Document Luna-21 IR-2 correction`. The request also supplied an opaque
non-Git identifier as an expected baseline; it is not a repository object
identifier and was not substituted for the actual published commit.

The required ancestry is present:

- Prior blocking Luna-0 review: `a9077997740ccdc374c7ad89deef122112967369`.
- Corrective implementation: `ac2e822e5c7656d649c6e77f62024c6d6e4cf72f`.
- Corrective handoff and synchronized review baseline:
  `3fb6d8c5128277bc8ecc5b2beea7288c214b772d`.

The corrective production diff from the blocking review to implementation
contains only `tpcn/ir2.py`, `tests/test_ir2.py`, and `tests/test_e2_ir2.py`.
The review changed no production code. Review-owned changes are limited to
the unique-ID continuation test oracle and this handoff plus workflow/changelog
synchronization.

## Original blocking cases independently reproduced

The exact prior blocking revision was checked out in a temporary detached
worktree, then removed after the probes:

1. **OBSERVED — identity/high-water blocker:** a record with
   `S_PENDING`, ordinary episode and lineage IDs `2`, and corresponding
   high-water counters `1` passed construction and E2 reconstruction.
   Promoting it to M allocated `multi_episode_id == 2`, reusing the active
   ordinary episode identity.
2. **OBSERVED — counter-budget blocker:** an `N` record with
   `next_event_identity == 2` and `event_budget == 1` survived a
   `TPCNIR2` JSON round trip.
3. **OBSERVED — equal-time E2 blocker:** an ordinary `S_PENDING/S_EMIT`
   record with all optional M settings absent and pending time equal to local
   time reconstructed through `neuron_from_ir2_e2`; `process_pending()` then
   emitted at that same timestamp.

The correction was reviewed from the published source, not accepted on test
counts alone.

## Corrective boundary evidence

### Active identities and high-water counters

Independent malformed records were built for each relevant pair and fed
through `IR2Neuron.from_dict`:

| Mode | Malformed active identity | Observed |
|---|---|---|
| `S_PENDING` | ordinary episode above `next_episode_identity` | rejected at high-water validation |
| `S_PENDING` | lineage above `next_lineage_identity` | rejected at high-water validation |
| `S_RETURN` | ordinary episode above `next_episode_identity` | rejected at high-water validation |
| `S_RETURN` | lineage above `next_lineage_identity` | rejected at high-water validation |
| `M_ACTIVE` | multi episode above `next_episode_identity` | rejected at high-water validation |
| `M_ACTIVE` | lineage above `next_lineage_identity` | rejected at high-water validation |

**OBSERVED:** Valid equality boundaries remain accepted. Independently
reconstructing `S_PENDING` with ordinary ID equal to its high-water and
promoting to M allocated ID `2` after prior ordinary ID `1`, retaining
lineage `1`. The regression suite also verifies identity equality in all
four modes. No identity was reused.

### Event budget and modes

**OBSERVED:** The shared `IR2Neuron` construction validation bounds
`generation_token`, `next_event_identity`, `next_episode_identity`,
`next_lineage_identity`, `next_input_identity`, `processed_event_count`, and
`input_contribution_count` for `N`, `S_PENDING`, `S_RETURN`, and `M_ACTIVE`.
An independent `4 modes × 7 counters × 3 values` probe accepted
`event_budget - 1` and `event_budget`, and rejected `event_budget + 1` for
every cell.

The same shared bound applies to `TANH_LEGACY`. An over-budget legacy
counter is rejected. The explicit IR-1-to-IR-2 legacy upgrade remains
accepted and emits schema revision 1 with valid counters. This is consistent
with ACP-0005's bounded-transferable-counter requirement and causes no
observed valid-upgrade regression.

### Strict-future boundary and E1 compatibility

For ordinary `S_PENDING/S_EMIT` with absent optional M settings, independent
dict/record/JSON reconstruction established:

- Pending time earlier than local time: rejected by IR-2 validation.
- Pending time equal to local time: valid historical ordinary IR-2 data,
  but `neuron_from_ir2_e2` rejects it at the E2 capability boundary.
- Pending time later than local time: accepted through E2 reconstruction.

Explicit-M ordinary records and `M_ACTIVE/M_REARM` records were also tested:
equal-time pending work is rejected; future pending work survives JSON and
restores. The E2 adapter checks this boundary for every record with pending
work, including records without optional M settings.

**OBSERVED:** `neuron_from_ir2` still accepts and executes an otherwise-valid
equal-time ordinary record with absent optional M settings at that timestamp.
It still raises `IR2UnsupportedRuntimeError` for `M_ACTIVE`. The E1-only
serializer continues to reject a `MultiExcursionNeuron` in favor of the
explicit E2 serializer. Schema revision remains 1.

### Continuation and unique-ID fixture

The corrective REFRACTORY test begins with a prior M emission and its valid
`M_REARM`. It processes pending work repeatedly under `event_budget`, compares
the complete output and transition traces for the original and reconstructed
neurons, and requires final `N` with no pending event. The traces are
nonempty and equal. They cover emission ID/sequence, timestamp, payload,
episode and lineage; local state/time, mode/phase, pending validity tuple;
identity/work counters; provenance/truncation; and final state.

**OBSERVED:** The separate test
`test_e2_reconstruction_restores_counters_and_continues_with_unique_ids`
was still vacuous because it drained a newly empty queue and used `all(...)`
assertions that passed for empty output. Luna-0 classified it as a
**FIXTURE / ORACLE DEFECT**, not a production defect, and corrected that
test only. It now calls the same finite direct-pending continuation helper,
requires actual outputs and transitions, requires every post-reconstruction
event ID to differ from the prior output and every sequence to exceed the
prior sequence, and requires termination at `N`.

Independent execution observed 13 later outputs and 26 state transitions
for the unchanged fixture configuration; the first later output used event
ID `n:excursion:2` and sequence `2`, after prior ID `n:excursion:1` and
sequence `1`. Both the corrected test and REFRACTORY equivalence test pass.

### Zero identities and pending generation

**OBSERVED:** Runtime allocators start at zero and increment before assigning
ordinary, M and lineage IDs. IR-2 `_id` accepts nonnegative integer IDs;
pending-event episode IDs use the stricter positive-integer validator.
Consequently `multi_episode_id == 0` cannot satisfy an M pending-event
ownership tuple; `S_PENDING` likewise has a positive pending episode ID.
Lineage zero is accepted in an otherwise-valid active record, and a
no-pending `S_RETURN` can serialize ordinary ID zero.

**INFERRED:** Neither ACP-0004 nor ACP-0005 normatively requires one-based
episode or lineage IDs. The schema's nonnegative identifier domain and
monotonic high-water semantics allow a zero-based producer; restoring
high-water zero causes future allocation to advance to one, not reuse the
active identity. No architectural basis for adding a new positive-ID
restriction was found, so this is not classified as an implementation or
validation defect.

**OBSERVED:** A pending internal event cannot have generation zero:
`IR2PendingInternal` requires a positive generation. The canonical runtime
scheduler likewise increments generation before installing valid pending
work. This is consistent and needs no correction.

## State/provenance and architecture preservation

An independent full-state M_ACTIVE JSON reconstruction probe verified
preservation of accumulator and local time; mode/phase; ordinary/M/lineage
IDs and polarity; `m_peak`; exact pending owner/kind/time/episode/generation/
queue sequence; all seven transferable counters; all E1/E2 configuration
values; provenance fields and order; truncation and unassigned-provenance
state. Reconstruction scheduled no duplicate event and produced no output.

Exact-capacity and overflow provenance round trips preserved causal event
IDs, timestamps, signed contributions, ownership, order and sticky
truncation. The existing E2 M-to-final-S tests continue to verify new
ordinary episode identity, continuous lineage, provenance re-ownership and
truncation. No production runtime file changed in the corrective diff.

**OBSERVED:** The unchanged E2 regression suite covers theta-M equality and
just-below behavior, sign at M emission, bounded discharge and finite
return, external sign reversal in both phases, external-before-internal
equal-time cancellation, final-S identity, direct M-to-N, reset/stale work,
and one valid pending internal event. Runtime and protected regression
surfaces are unchanged from the prior implementation.

**OBSERVED:** ACP-0002 N2 still computes
`z = tanh(w * a)` then `v = d * z + (1 - d) * r`, routes via the finite
delayed queue, and preserves E2 excursion payload semantics. The E2
correction does not modify topology, Model-B or event ordering.

A01-A15 remain unchanged: local event execution/time, finite causal
propagation, bounded topology/state/work/provenance, hardware-neutral
canonical semantics, and all other contract clauses are preserved. No
global polling, unbounded replay/history, wraparound, schema fork, backend
canonical state or architecture promotion was introduced.

## Validation record

All commands ran on Windows from the repository root with Python 3.11.5.

| Command | Result |
|---|---|
| `python -m pytest -q tests/test_e2_multi_excursion.py tests/test_e2_ir2.py` | PASS — 45 passed |
| `python -m pytest -q tests/test_excursion_neuron.py tests/test_ir2.py` | PASS — 156 passed |
| `python -m pytest -q tests/test_acp0002_n2.py tests/test_event_runtime.py` | PASS — 254 passed |
| `python -m pytest -q tests/test_topology.py` | PASS — 9 passed |
| `python -m pytest -q tests/test_ir2.py tests/test_e2_ir2.py` | PASS — 116 passed |
| `python -m pytest -q -rs` | PASS — 768 passed, 1 skipped |
| `python -m compileall -q tpcn tests` | PASS |
| `git diff --check` | PASS |

The only skip is
`tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`
(`CUDA is unavailable`). It is unrelated to the CPU software-reference
correction. GPU/FPGA/FPAA, ModelSim, hardware equivalence, calibration,
H2/N3, IR-3 and learning/benchmark work was not run; it is unauthorized or
outside this closure.

## Verdict and governance

**TERMINAL VERDICT: PASS — LUNA-21 ACP-0004 E2 IMPLEMENTATION AND IR-2
CORRECTION INDEPENDENTLY VERIFIED AND CLOSED.**

The earlier `BLOCKED` changelog entry and review handoff remain as historical
evidence. The workflow now records the later independent closure. ACP-0004
remains staged, ACP-0005 schema revision 1 remains unchanged, and A01-A15
remain unchanged. This is not integration readiness, hardware validation or
architecture promotion.

No successor Luna is authorized or assigned. Any later dependency planning
must follow the updated authoritative workflow.

**NOT TESTED:** Hardware/backend equivalence, calibration, learning
benchmarks, H2, N3 and IR-3.
