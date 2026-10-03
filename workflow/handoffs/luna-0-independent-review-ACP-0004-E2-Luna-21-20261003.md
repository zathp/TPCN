# Luna-0 Independent Review — ACP-0004 E2 / Luna-21

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of ACP-0004 E2 multi-excursion runtime"
  task_id: "luna-0-independent-review-ACP-0004-E2-Luna-21-20261003"
  component: "E2 runtime, IR-2 E2 reconstruction, and independent closure gate"
  status: "blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "5d0171f46b90664b1a6aca5709cc2f07f19b7f4e"
  result_revision: "review documentation publication; exact pushed tip is reported in the session result"
  dependencies:
    - "ACP-0004 E1 independently closed"
    - "ACP-0005 TPCN-IR-2 revision 1 independently closed"
    - "Luna-21 implementation and completion handoff published"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT REVIEW", "ARCHITECTURE CONFORMANCE VERIFICATION", "ADVERSARIAL VERIFICATION"]
  hypothesis: "Luna-21 satisfies the authorized ACP-0004 E2 state machine and ACP-0005 IR-2 boundary without changing closed behavior."
  counter_hypothesis: "Adversarial state reconstruction exposes a causal, boundedness, identity, or compatibility defect."
  interfaces_relied_on:
    - "SingleExcursionNeuron and MultiExcursionNeuron"
    - "EventQueue destination-local external-before-internal ordering"
    - "TPCN-IR-2 schema revision 1 and E1/E2 adapters"
    - "ACP-0002 N2 Model-B transfer"
  label_information_boundary:
    - "No labels, evaluation state, learning, reward, or global task state is introduced."
  timing_assumptions:
    - "Local timestamps and analytic elapsed-time decay."
    - "Finite positive propagation and internal delays."
    - "Same-destination external-before-internal ordering at equal timestamps."
  reset_boundaries:
    - "E2 reset clears character-local state and pending validity while retaining output, shared episode, lineage, and automatic-input high-water counters."
  resource_bounds:
    - "Bounded x, finite mode/phase state, one valid pending event, bounded provenance, finite counters and event budget."
  authorized_scope:
    - "Independent review of the published Luna-21 implementation and evidence."
    - "Workflow/changelog synchronization and a bounded corrective gate."
  unauthorized_scope:
    - "Production implementation changes, successor Luna execution, H2, N3, learning, backend or hardware work, calibration, hardware equivalence, IR-3, and A01-A15 amendments."
  controls:
    - "Closed E1 runtime and E1-only IR-2 adapter."
    - "Accepted TPCN-IR-2 schema revision 1."
    - "Closed ACP-0002 N2 Model-B transfer."
  measurements:
    - "Threshold transitions, finite return, output and episode identities, provenance, reset, pending-event ordering, IR-2 continuation and regression counts."
  information_boundary_check:
    - "All reviewed E2 transitions use local state, local time, the delivered event, and bounded causal provenance."
  hardware_mapping:
    - "None; this review makes no backend or hardware equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A11", "A15"]
  preserves:
    - "A01-A15"
    - "ACP-0004 staged status and closed E1 behavior"
    - "ACP-0005 / TPCN-IR-2 schema revision 1"
    - "ACP-0002 N2 Model-B"
    - "Luna-17 reserved status and Luna-13F closed status"
  architecture_change: false
  proposal: "ACP-0004"
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-ACP-0004-E2-Luna-21-20261003.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Focused E2 runtime and E2 IR-2: 44 passed."
    - "Closed E1 and IR-2 regression pair: 57 passed; Luna-21 handoff claimed 41."
    - "ACP-0002 N2 and event runtime: 254 passed."
    - "Topology: 9 passed."
    - "Full CPU suite: 668 passed, 1 skipped, 0 failed."
    - "compileall and pre-review git diff --check passed."
    - "Independent bounded M continuation comparison: 13 outputs and 26 transitions matched; final N state."
    - "Independent positive/negative finite-return recurrence and decay-before-emission probes passed."
    - "Runtime budget probes: processed events, generation, output, episode, lineage, and automatic-input identities reached budget without wrapping and rejected the next allocation."
    - "Wrong payload-neuron internal delivery was a state/output no-op."
  tests_failed:
    - "Adversarial IR-2 validation gate: an ordinary S record with a high-water mark below its active episode/lineage ID survives parse and reconstruction, then reuses the ordinary episode ID on M promotion."
    - "Adversarial IR-2 validation gate: ordinary-mode identity counters above event_budget survive schema construction and JSON round trip."
    - "Adversarial E2 reconstruction gate: with all optional M settings absent, a pending internal event at local_last_update_time survives construction and executes at that same time."
    - "Existing REFRACTORY continuation test does not exercise its restored pending event because it drains newly empty queues; its empty-vs-empty output comparison is not continuation evidence."
  tests_not_run:
    - "GPU/FPGA/FPAA, ModelSim, hardware equivalence, calibration, learning benchmarks, H2, N3, and IR-3; unauthorized or not applicable."
  assumptions:
    - "E2 adapter defaults for absent optional M settings are as documented in the Luna-21 completion handoff; the corrective gate must keep this explicit and must not weaken E1-only behavior."
  unresolved:
    - "Shared IR-2 cross-field validation must enforce identity high-water and budget invariants across all modes."
    - "E2-capable reconstruction must not accept an equal-time pending internal transition."
    - "The committed post-emission continuation regression must actually execute reconstructed pending work."
  recommended_next_agent:
    - "Project owner / Luna-0: dispatch a bounded correction within the existing Luna-21 scope; do not create a successor Luna."
```

## Outcome and synchronized baseline

**OBSERVED:** The request was an independent implementation review, not a new
implementation assignment. `origin/main` was fetched before review. The review
started at clean `main`, with `HEAD == origin/main ==
5d0171f46b90664b1a6aca5709cc2f07f19b7f4e`; no later commits were present.
The authorized starting revision
`0d26c3d6bd253ce3be1a3877ec5f2fcb0cf62868`, implementation/fixture revision
`bfc866be053f9692382d1be5e048f5b4d280e5f6`, and completion-handoff revision
`5d0171f46b90664b1a6aca5709cc2f07f19b7f4e` exist in the required ancestry.
The implementation revision's subject is `Complete E2 boundary and
provenance fixtures`; the current baseline subject is `Record Luna-21 E2
implementation handoff`.

**OBSERVED:** The implementation delta contains only the authorized runtime,
IR-2 adapter/export and test files:

- `tpcn/excursion_neuron.py`
- `tpcn/ir2.py`
- `tpcn/__init__.py`
- `tests/test_e2_multi_excursion.py`
- `tests/test_e2_ir2.py`
- `tests/test_ir2.py`

No learning, reward, prediction redesign, structural plasticity, GPU/CUDA,
FPGA/VHDL, FPAA, calibration, hardware equivalence, IR-3, or A01-A15 change
was observed.

**OBSERVED:** The review read the Luna-0 and Luna-21 agent contracts,
architecture contract/changelog, Luna workflow and acceptance criteria,
handoff template, architecture proposal index/template, ACP-0002, ACP-0004,
ACP-0005, Luna-21 authorization/dispatch/completion handoffs, and the closed
Luna-19 E1 and Luna-20 IR-2 evidence. ACP-0004 remains accepted for staged
implementation. A01-A15, E1 closure, IR-2 schema revision 1, N2 closure, and
the hardware reservations remain unchanged.

## Exact implementation and tests inspected

Implementation:

- `tpcn/excursion_neuron.py`: E1 boundary behavior, shared event validation,
  `MultiExcursionNeuron` transitions, admission, discharge, re-arm,
  final-S ownership, reset and counters.
- `tpcn/ir2.py`: `IR2Neuron` validation, JSON round trip, E1-only adapter,
  E2 serialization and E2 reconstruction.
- `tpcn/__init__.py`: additive public exports.
- `tpcn/event_runtime.py`: priority ordering, queue sequencing and finite
  queue semantics.
- `tpcn/topology.py`: bounded Model-B fan-out and finite delayed routing.

Tests:

- `tests/test_e2_multi_excursion.py`
- `tests/test_e2_ir2.py`
- `tests/test_excursion_neuron.py`
- `tests/test_ir2.py`
- `tests/test_acp0002_n2.py`
- `tests/test_event_runtime.py`
- `tests/test_topology.py`

## Validation record

Executed on Python 3.11.5 at review baseline `5d0171f...`:

| Command / procedure | Observed result |
|---|---|
| `python -m pytest -q tests/test_e2_multi_excursion.py tests/test_e2_ir2.py` | **PASS — 44 passed, 0 failed, 0 skipped** |
| `python -m pytest -q tests/test_excursion_neuron.py tests/test_ir2.py` | **PASS — 57 passed, 0 failed, 0 skipped**; Luna-21 handoff states 41 for this command. |
| `python -m pytest -q tests/test_acp0002_n2.py tests/test_event_runtime.py` | **PASS — 254 passed, 0 failed, 0 skipped** |
| `python -m pytest -q tests/test_topology.py` | **PASS — 9 passed, 0 failed, 0 skipped** |
| `python -m pytest -q` | **PASS — 668 passed, 0 failed, 1 skipped** |
| `python -m compileall -q tpcn tests` | **PASS** |
| `git diff --check` before review edits | **PASS** |
| Pylance diagnostics for `tpcn/excursion_neuron.py` | **PASS — no diagnostics returned** |

All ordinary requested test commands passed. The independent IR-2 probes below
are contrary evidence and block closure; they were not fixes or committed
production changes.

## Independent adversarial evidence

### E2 state machine, thresholds, output and decay

**OBSERVED:** Independent actual-input probes for
`nextafter(theta_M, -inf)`, exact `theta_M`, and
`nextafter(theta_M, +inf)` produced `S_PENDING`, `M_ACTIVE`, and `M_ACTIVE`,
respectively. Existing fixtures independently exercise `theta_E`,
`theta_hold`, M emission and re-arm boundaries. A high-decay M input that
fell from `4.0` to `1.4715177646857693` before `M_EMIT` produced no M event
and entered `S_PENDING` with one pending `S_EMIT`.

**OBSERVED:** The implementation emits `sign(x_emit) * A_max`, discharges
without crossing zero, and retains one valid M event for the active phase.
External inputs in ARMED/REFRACTORY and same-time external-before-internal
cases pass the focused tests; already emitted output objects are not rewritten.

### Finite return, local ordering and stale events

**OBSERVED:** An independent recurrence, run against actual positive and
negative states at `theta_M`, intermediate magnitude 6, and `X_max`, matched
actual M output counts exactly: `3`, `5`, and `7`, respectively. All cases
terminated at `N`; output polarity mirrored the input. This verifies the
finite-return behavior beyond merely repeating the test's `ceil` expression.
Configured positive delays that cannot advance floating-point time raise
explicitly.

**OBSERVED:** `EventQueue` scans equal-time events and selects an external
event ahead of an internal event only for the same destination, with queue
sequence deciding otherwise. Its sequence assignment and comparison are
independent of the E2 test insertion order. The exact-time E2 fixtures pass.

**OBSERVED:** `_receive_internal` charges the inherited execution budget before
validating stale work, then checks the valid slot plus source, payload neuron,
episode, generation, kind, timestamp, sequence and phase. Stale and duplicate
delivery tests are no-ops for neuron state/output. This pre-validation budget
charge is inherited closed E1 behavior and was not classified as an E2 defect.

### Identity, provenance and reset

**OBSERVED:** In-memory M admission and final residual S use the shared
monotonic episode counter, preserve one lineage, and avoid allocating an
ordinary episode on direct M-to-N. The M-to-final-S provenance transition
changes episode ownership while preserving event ID, timestamp, signed
contribution, order and lineage; truncation remains sticky. Capacity and
capacity-plus-one behavior are covered. Reset from ARMED and REFRACTORY clears
character-local state and stale queued events while retaining identity
high-water values.

**BLOCKER — IR-2 RECONSTRUCTION DEFECT:** The same guarantees do not hold for
all validated serialized ordinary states. An independently constructed
`S_PENDING` record with `ordinary_episode_id = lineage_id = 2`,
`next_episode_identity = next_lineage_identity = 1`, a matching pending
`S_EMIT`, and optional M configuration absent passed `IR2Neuron`
construction, JSON round trip, and `neuron_from_ir2_e2`. An above-threshold
input then produced `multi_episode_id == 2`, colliding with the prior ordinary
episode ID. `_validate_cross_fields` enforces high-water relationships only
inside the `M_ACTIVE` branch; it omits them for S_PENDING/S_RETURN.

**BLOCKER — IR-2 RECONSTRUCTION DEFECT:** An ordinary S_PENDING record with
`next_event_identity = 5` and `event_budget = 4` also survived construction,
serialization and parse. Counter-budget validation is likewise inside the
M_ACTIVE branch, so ordinary records can transfer an impossible high-water
state. Generation, lineage, episode, input and event counters need consistent
mode-independent bounds wherever their semantics apply.

**BLOCKER — IR-2 RECONSTRUCTION DEFECT:** When all optional M settings are
`None`, an S_PENDING record whose pending timestamp equals the local timestamp
passes validated construction. `neuron_from_ir2_e2` supplies E2 defaults and
`process_pending()` can emit at that same timestamp. E2-produced records with
explicit M settings reject equality, but the E2 capability path also accepts
E1-only records with omitted M settings. That path must not allow an
equal-time transition to bypass the positive-delay execution rule.

The defaulting of absent optional M settings is documented as a Luna-21
handoff assumption and the correction must retain any owner-approved meaning
for it. No schema revision or E1 adapter change is requested by this review.

### IR-2 continuation fixture

**FIXTURE / ORACLE DEFECT:** The committed
`test_refractory_round_trip_continues_after_a_prior_m_emission` reconstructs
the REFRACTORY state, creates new empty queues for both original and restored
neurons, and drains only those queues. The neuron pending slot is not inserted
into either queue, so `actual == expected == []` can pass without executing
`M_REARM`.

**OBSERVED independent continuation:** I instead repeatedly executed
`process_pending()` on both the original and reconstructed REFRACTORY states,
with a finite `event_budget` guard. The runs matched on 13 subsequent output
records, 26 transition snapshots, pending kind/time/generation, state, mode,
episode and lineage IDs, provenance and truncation, counters, and final `N`
state with no pending event. Runtime continuation therefore passed this
independent procedure; the checked-in regression still needs correction
before it can serve as durable evidence.

### E1, Model-B, bounds and scope

**OBSERVED:** `SingleExcursionNeuron` remains E1-only: M threshold behavior
continues to report/raise the closed boundary rather than executing M output.
`neuron_from_ir2` remains E1-only and rejects M_ACTIVE. `E1Neuron` and
`CanonicalExcursionNeuron` still refer to `SingleExcursionNeuron`. E2 API
exports are additive. The E1, IR-2, N2, event-runtime and full-suite runs
passed.

**OBSERVED:** Non-default Model-B fan-out used signed `w`, nontrivial `d` and
`r`, and delays `0.2`/`0.4`; the routed payloads matched
`d*tanh(w*p_exc) + (1-d)*r`, arrival timestamps were `0.21`/`0.41`, and both
events preserved the output event ID and lineage. The ACP-0002 N2 suite passed.

**OBSERVED:** Runtime bookkeeping is bounded by the configured provenance,
emission/report and queue capacities, one pending slot, and bounded identity
allocation that raises before wrap/reuse. No new cancellation table or
unbounded history was found. IR-2's inconsistent ordinary-mode counter
acceptance nevertheless violates transferable bounded-counter invariants.

**OBSERVED:** No unauthorized feature or architecture change was found. No
backend, hardware, calibration, learning or cross-hardware equivalence claim
was tested or inferred.

## Bounded corrective gate and verdict

The shared IR-2 validated-construction/parsing path and E2 adapter boundary
must be corrected to:

1. enforce active ordinary and M episode/lineage IDs do not exceed their
   serialized high-water counters;
2. reject every execution counter beyond `event_budget` in each supported
   mode, including ordinary E2-capable records;
3. reject pending internal events at or before local time on every record
   that can be reconstructed through the E2 capability, including records
   with absent optional M settings, without changing valid E1-only behavior;
4. replace the empty-queue REFRACTORY round-trip comparison with a bounded
   test that executes restored pending work and compares emissions,
   transitions, final state, counters, provenance and truncation.

The correction belongs to the existing Luna-21 authorized scope; it is not a
new Luna assignment. Keep E1 closure, TPCN-IR-2 schema revision 1, ACP-0002
N2, A01-A15, and all existing governance prohibitions intact. No production
code or test fixture was changed during this review.

**TERMINAL VERDICT: BLOCKED — IR-2 RECONSTRUCTION DEFECT.**

The workflow records Luna-21 as implemented but not independently closed.
The changelog records this review and the bounded gate. No successor
implementation is executed or authorized by this handoff.
