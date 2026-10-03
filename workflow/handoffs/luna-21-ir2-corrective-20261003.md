# Luna-21 Corrective Handoff — IR-2 Validation and Continuation

```yaml
tpcn_handoff:
  agent: Luna-21
  luna_identifier: "Luna-21"
  descriptive_name: "Corrective IR-2 validation and E2 continuation evidence"
  task_id: "luna-21-ir2-corrective-20261003"
  component: "ACP-0004 E2 reconstruction through TPCN-IR-2 revision 1"
  status: "complete; awaiting independent Luna-0 review"
  contract_version: "1.1"
  branch: "main"
  base_revision: "a9077997740ccdc374c7ad89deef122112967369"
  implementation_revision: "ac2e822e5c7656d649c6e77f62024c6d6e4cf72f"
  dependencies:
    - "Original Luna-21 implementation and completion handoff"
    - "Luna-0 independent review and bounded corrective gate"
    - "ACP-0004 E1 independently closed"
    - "ACP-0005 / TPCN-IR-2 revision 1 independently closed"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "The identified IR-2 reconstruction gaps can be closed within the existing Luna-21 scope without changing E1 dynamics, E2 runtime dynamics, or schema revision 1."
  counter_hypothesis: "Correcting the gaps requires changing the neuron runtime, E1 adapter behavior, or the accepted IR-2 schema."
  authorized_scope:
    - "Bound active identities by their serialized high-water counters."
    - "Bound execution counters by event_budget in every supported IR-2 mode."
    - "Require E2-reconstructed pending internal events to be strictly later than local time."
    - "Replace empty-queue continuation comparison with bounded real continuation."
  preserved:
    - "ACP-0004 E1 behavior and reset semantics"
    - "ACP-0004 E2 neuron dynamics"
    - "TPCN-IR-2 schema revision 1"
    - "ACP-0002 N2 Model-B transfer and event ordering"
    - "A01-A15 and existing architecture boundaries"
  architecture_change: false
  files_changed:
    - "tpcn/ir2.py"
    - "tests/test_ir2.py"
    - "tests/test_e2_ir2.py"
    - "workflow/handoffs/luna-21-ir2-corrective-20261003.md"
  tests_passing:
    - "Focused E2 runtime and E2 IR-2: 45 passed."
    - "E1 and IR-2 regression pair: 156 passed."
    - "N2 and event-runtime regressions: 254 passed."
    - "Topology regression suite: 9 passed."
    - "Full CPU suite: 768 passed, 1 skipped, 0 failed."
    - "Final IR-2 and E2 IR-2 focused rerun: 116 passed."
    - "compileall and git diff --check passed."
  tests_failed: []
  tests_not_run:
    - "GPU/FPGA/FPAA backends, ModelSim, hardware equivalence, calibration, H2, N3, and learning/benchmark evaluations; these remain outside Luna-21 authorization."
  unresolved:
    - "Independent Luna-0 review of the corrective revision and evidence is required."
  recommended_next_agent:
    - "Luna-0: independently verify the corrective revision and determine whether the bounded gate is closed."
```

## Outcome

The published Luna-0 review identified three IR-2 reconstruction risks: an
ordinary active episode or lineage could exceed its serialized identity
high-water counter; ordinary-mode execution counters could exceed the
declared `event_budget`; and an equal-time pending ordinary event could be
accepted by `neuron_from_ir2_e2` when optional M settings were absent. It
also found that the REFRACTORY round-trip test compared after draining an
empty queue rather than executing the reconstructed pending continuation.

The correction moves the event-budget bound into shared IR-2 neuron
validation and enforces it for all modes and execution counters. It validates
ordinary active episode and lineage IDs against their serialized high-water
counters in `S_PENDING` and `S_RETURN`. The E2 reconstruction adapter rejects
pending internal events at or before local time regardless of optional M
settings. The historical `neuron_from_ir2` adapter and the E1 runtime were
not changed.

The bounded REFRACTORY continuation regression now calls `process_pending`
on both original and reconstructed neurons, at most `event_budget` times.
It compares emitted records, each transition and pending tuple, identity and
work counters, provenance and truncation, and final state; both runs must
reach `N` with no pending event.

## Identity, provenance, and reset evidence

- The shared IR-2 high-water checks prevent restoring an active S or M
  identity beyond its serialized monotonic counter. A boundary test confirms
  equality is accepted, and a reconstructed `S_PENDING` admission allocates
  the next distinct M episode while preserving lineage.
- A 4-mode × 7-counter × 3-boundary test matrix covers `N`, `S_PENDING`,
  `S_RETURN`, and `M_ACTIVE`; each counter is checked immediately below,
  equal to, and above `event_budget`.
- The E2 adapter rejects pending times earlier than or equal to local time
  even without serialized optional M configuration, and accepts a strictly
  future pending time. A separate control verifies equal-time historical E1
  reconstruction still behaves as before.
- The E2 round-trip provenance test confirms owner and sticky truncation
  survive serialization. Full reset, episode lifecycle, and runtime
  transition requirements remain covered by the unchanged focused E2 suite.
- Existing E1-only rejection of `M_ACTIVE` remains covered by the IR-2
  tests; schema revision stays at 1.

## Validation record

All commands ran from the repository root with Python 3.11.5
(`C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe`).

| Command | Result |
|---|---|
| `python -m pytest -q tests/test_e2_multi_excursion.py tests/test_e2_ir2.py` | PASS — 45 passed |
| `python -m pytest -q tests/test_excursion_neuron.py tests/test_ir2.py` | PASS — 156 passed |
| `python -m pytest -q tests/test_acp0002_n2.py tests/test_event_runtime.py` | PASS — 254 passed |
| `python -m pytest -q tests/test_topology.py` | PASS — 9 passed |
| `python -m pytest -q` | PASS — 768 passed, 1 skipped |
| `python -m pytest -q tests/test_ir2.py tests/test_e2_ir2.py` | PASS — 116 passed on final focused rerun |
| `python -m compileall -q tpcn tests` | PASS |
| `git diff --check` | PASS |

The full CPU suite had one skip; its test identity was not separately
investigated for this corrective task. No final validation command failed.
Focused Pylance diagnostics reported no errors in the changed files; an
unused `IREvent` import warning remains in `tpcn/ir2.py`.

## Revisions and terminal gate

The corrective work began at clean `main`, with `HEAD` and fetched
`origin/main` both equal to `a9077997740ccdc374c7ad89deef122112967369`.
Implementation and tests are committed as
`ac2e822e5c7656d649c6e77f62024c6d6e4cf72f`. The published handoff is
evidence only.
No E2 architecture promotion, hardware equivalence, learning result, or
successor authorization is claimed.

**Next:** Luna-0 independently reviews the exact corrective revision and
this handoff. Luna-21 stops here pending that review.
