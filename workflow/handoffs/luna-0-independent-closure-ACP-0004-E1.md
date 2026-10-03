# Luna-0 Independent Closure — ACP-0004 E1

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "ACP-0004 E1 Independent Verification and Closure"
  task_id: "ACP-0004-E1-independent-closure"
  component: "independent review of the canonical single-excursion reference"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "f0a5977db1a56ac559262e52413f31ebf15092f5"
  result_revision: "Luna-0 review publication commit"
  dependencies:
    - "ACP-0004 accepted for staged implementation"
    - "Luna-19 E1 implementation at f0a5977db1a56ac559262e52413f31ebf15092f5"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["VERIFICATION", "ARCHITECTURE-PROMOTION"]
  hypothesis: "The published E1 implementation is a bounded, deterministic, hardware-neutral single-excursion reference that preserves A01-A15 and prior Model-B/runtime behavior."
  counter_hypothesis: "Adversarial execution finds a semantic, ordering, identity, bound, reset, provenance, or regression failure that prevents independent closure."
  interfaces_relied_on:
    - "Event"
    - "EventQueue"
    - "SingleExcursionNeuron"
    - "BoundedTopology.route"
    - "ACP-0002 N2 Model-B transfer"
  label_information_boundary:
    - "No labels, future inputs, evaluation state, learning, prediction, reward, or global statistics enter E1."
  timing_assumptions:
    - "Logical timestamps are nonnegative and destination-local clocks are monotonic."
    - "Equal-time external-before-internal ordering is destination-local; unrelated destinations retain queue sequence ordering."
  reset_boundaries:
    - "reset() clears character-local state and provenance while retaining event, episode, and lineage identity counters."
  resource_bounds:
    - "Accumulator, pending internal event, generations, provenance, emissions, reports, and processing use finite declared bounds."
  authorized_scope:
    - "Independent verification and directly required surgical fixes for E1 closure."
    - "Governance handoff, stale metadata correction, and changelog entry."
  unauthorized_scope:
    - "M/multi-excursion execution, IR-2, H2, N3, backends, hardware equivalence, learning redesign, and new architecture authorization."
  controls:
    - "Published revision f0a5977."
    - "Existing event-runtime, canonical-neuron, topology, ACP-0002, predictive, eligibility, utility, structural, visualization, IR, and classifier tests."
    - "Serial/batched queues, stale-event, reset, provenance, and fan-out adversarial fixtures."
  measurements:
    - "Configuration rejection cases, compression ratio, leakage control, amplitude/polarity, event ordering, re-arm termination, identity/lineage, provenance ownership, and regression counts."
  information_boundary_check:
    - "E1 state transitions consume only addressed local events and bounded local bookkeeping."
  hardware_mapping:
    - "No hardware equivalence is claimed; the reference remains backend-neutral."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A11", "A15"]
  preserves:
    - "A01-A15"
    - "ACP-0002 N2 Model-B edge transfer"
    - "ACP-0003 H1/TPCN-IR-1"
    - "Prediction, reward, eligibility, structural-plasticity, visualization, classifier, and label-isolation behavior outside E1"
  architecture_change: false
  proposal: "ACP-0004"
  files_changed:
    - "tpcn/event_runtime.py"
    - "tpcn/excursion_neuron.py"
    - "tests/test_excursion_neuron.py"
    - "workflow/handoffs/acp-0004-e1-single-excursion-Luna-19.md"
    - "workflow/handoffs/luna-0-independent-closure-ACP-0004-E1.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "Adversarial E1 and runtime review cases in tests/test_excursion_neuron.py"
  tests_passing:
    - "59 focused E1/runtime tests"
    - "429 review regression tests"
    - "612 full CPU tests, 1 skipped"
  tests_failed: []
  tests_not_run:
    - "M, IR-2, H2, N3, GPU/FPGA/FPAA, approximation, calibration, hardware equivalence, and learning redesign: unauthorized/not applicable"
  assumptions:
    - "Episode/lineage ownership is the required E1 provenance boundary; completed episode records may remain bounded until a later episode admission filters them."
    - "ULP-scale adjustment at a valid analytic re-arm is numerical roundoff handling, not fuzzy external threshold semantics."
  unresolved:
    - "The next stage must be separately authorized; this closure does not select E2/M or IR-2."
  recommended_next_agent:
    - "Project owner / Luna-0: decide whether to authorize a separate IR-2 or E2 dependency study."
```

## Review outcome

**OBSERVED:** Publication provenance was verified at commit
`f0a5977db1a56ac559262e52413f31ebf15092f5`, branch `main`, with
`HEAD == origin/main` and a clean tree before review edits. The publication
contained only the six E1 implementation/test/handoff files and no M, IR-2,
backend, learning, or architecture-contract changes.

**OBSERVED:** The original Luna-19 handoff contained stale “uncommitted”
result/reproduction wording. It is corrected as part of this review while
preserving the historical implementation evidence.

**OBSERVED:** `E1Config` rejects non-finite values, bool numerics, invalid
threshold ordering, non-positive decay/delay, invalid amplitude bounds,
provenance capacities outside `1..64`, and invalid event budgets.

**OBSERVED:** Accumulation applies local elapsed-time exponential decay before
signed contribution integration and state clipping. The canonical close-input
fixture produces three contributions and one excursion (`C_E = 3/1`); widely
spaced contributions produce no excursion.

**OBSERVED:** Admission is inclusive at `theta_E`, excludes `theta_M`, captures
polarity, creates one episode/lineage, and schedules one `S_EMIT`. Ordinary
episodes cannot emit a second excursion while pending or returning. Exact
amplitude, negative polarity, opposite-sign input, threshold, and M-boundary
cases pass.

**OBSERVED:** Equal-time ordering is destination-local. Same-destination
external events precede internal events; unrelated destinations retain the
existing sequence ordering. Serial and batched execution agree.

**OBSERVED:** Generation and episode identity prevent stale `S_EMIT` and
`S_REARM` records, including pre-reset records, from becoming valid. A valid
analytic re-arm terminates without a micro-rearm loop; ULP-scale correction is
applied only at a valid internal re-arm boundary.

**OBSERVED:** Provenance entries carry episode/lineage ownership. Completed
episode records do not contaminate a newly admitted episode; truncation is
computed for the active pre-admission/episode contributor set.

**OBSERVED:** Excursion fan-out preserves causal `event_id` and `lineage_id`
while assigning distinct queue sequences and applying independent Model-B
`w`, `d`, `r`, and delay values. No legacy continuously recomputed activation
is emitted by E1.

## Validation record

| Command or procedure | Observed result |
|---|---|
| `python -m pytest -q tests/test_excursion_neuron.py tests/test_event_runtime.py` | **PASS — 59 passed** |
| Review regression bundle including E1, runtime, canonical neuron, topology, ACP-0002 N1/N2, prediction, eligibility, utility, structural, visualization, IR, and classifier tests | **PASS — 429 passed** |
| `python -m compileall -q tpcn tests` | **PASS** |
| `git diff --check` | **PASS** |
| Full CPU suite | **PASS — 612 passed, 1 skipped** |

## A01-A15 and authorization gate

**PASS — A01-A15 unchanged and preserved.** E1 uses local event-driven state,
finite propagation, bounded topology/runtime resources, local-only inputs,
bounded dynamics, explicit bounded provenance, and hardware-neutral logical
records. Predictive coding, delayed reward, structural plasticity, gates, and
energy utility remain outside E1 and their existing tests pass.

M/multi-excursion behavior is not implemented. TPCN-IR-2, ACP-0003 H2,
ACP-0002 N3, GPU/FPGA/FPAA work, approximation, calibration, Luna-13F
reopening, and Luna-13G remain unauthorized.

## Closure decision

**PASS — ACP-0004 E1 CANONICAL SINGLE-EXCURSION REFERENCE INDEPENDENTLY
VERIFIED AND CLOSED**

This closure covers E1 only. It does not accept or authorize E2, M, IR-2,
backends, hardware equivalence, or learning changes.

## Next-stage recommendation

Do not jump directly from E1 closure to M/E2. The safer dependency is a
separately reviewed `TPCN-IR-2` schema for excursion state and bounded
pending/provenance representation, followed by a separately authorized E2/M
implementation. An alternative E2-before-IR-2 path would leave the canonical
serialization boundary unresolved and is not recommended. This is a
recommendation, not authorization.
