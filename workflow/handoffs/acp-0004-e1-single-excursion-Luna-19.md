# Luna-19 ACP-0004 E1 Completion Handoff

```yaml
tpcn_handoff:
  agent: Luna-19
  luna_identifier: "Luna-19"
  descriptive_name: "ACP-0004 E1 Canonical Single-Excursion Reference"
  task_id: "ACP-0004-E1"
  component: "static leaky accumulator and single-excursion software reference"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "03302de7121f0dfe340cfd2d87d351ff8d7380a6"
  result_revision: "uncommitted working tree after validation"
  dependencies:
    - "ACP-0004 accepted for staged implementation"
    - "Luna-1 event runtime"
    - "ACP-0002 N2 static Model-B edge transfer"
  owner: "Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "A bounded local leaky accumulator can implement one deterministic ordinary excursion per episode without a global neural timestep or M execution."
  counter_hypothesis: "Focused E1 or affected runtime regressions show an ordering, bound, identity, cancellation, or Model-B compatibility failure."
  interfaces_relied_on:
    - "Event"
    - "EventQueue"
    - "EventType"
    - "BoundedTopology.route"
  label_information_boundary:
    - "No labels, future inputs, evaluation state, prediction state, reward state, or learning state enters E1 computation."
  timing_assumptions:
    - "Nonnegative logical timestamps and monotonic local time."
    - "Internal E1 delays are finite and positive."
    - "Equal-time external events precede internal events, then queue sequence orders ties."
  reset_boundaries:
    - "reset() clears character-local state, pending work, provenance, emissions, and boundary reports while retaining monotonic identity counters."
  resource_bounds:
    - "Signed accumulator is clipped to [-x_max, x_max]."
    - "One valid pending internal event exists per neuron."
    - "Provenance capacity is 1..64 with oldest eviction and explicit truncation."
    - "Event processing, generation, output, and diagnostic collections use finite budgets."
  authorized_scope:
    - "E1 modes N, S_PENDING, and S_RETURN."
    - "Analytic local decay, ordinary admission, one emission, and analytic re-arm."
    - "M-boundary detection/reporting without M execution."
    - "Focused E1 tests and handoff."
  unauthorized_scope:
    - "M_ACTIVE, M_EMIT, M_REARM, multi-excursion discharge, and oscillator behavior."
    - "IR-2, backends, approximation, calibration, hardware equivalence, learning, and reward redesign."
    - "ACP-0002 N3, Luna-13F reopening, and Luna-13G."
  controls:
    - "Existing TPCNNeuron behavior remains covered by its existing focused tests."
    - "Existing EventQueue, topology, and Model-B tests remain regression controls."
    - "Serial and batched ready-event delivery use the same ordered queue."
  measurements:
    - "Input contribution count versus emitted excursion count."
    - "Emission timestamps, payloads, event identities, lineages, state bounds, and provenance bounds."
  information_boundary_check:
    - "E1 receives only addressed numeric events and local pending-event state."
  hardware_mapping:
    - "The implementation uses bounded scalar state and logical events only; no hardware equivalence or backend claim is made."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A11", "A15"]
  preserves:
    - "A01-A15"
    - "ACP-0002 N2 Model-B transfer semantics"
    - "ACP-0003 H1 and TPCN-IR-1"
    - "Existing predictive coding, reward, eligibility, structural-plasticity, visualization, classifier, and label-isolation boundaries"
  architecture_change: false
  proposal: "ACP-0004"
  files_changed:
    - "tpcn/event_runtime.py"
    - "tpcn/excursion_neuron.py"
    - "tpcn/topology.py"
    - "tpcn/__init__.py"
    - "tests/test_excursion_neuron.py"
    - "workflow/handoffs/acp-0004-e1-single-excursion-Luna-19.md"
  tests_added:
    - "tests/test_excursion_neuron.py"
  tests_passing:
    - "python -m pytest -q tests/test_excursion_neuron.py tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py: 54 passed"
    - "python -m pytest -q: 589 passed, 1 skipped"
    - "python -m compileall -q tpcn tests: passed"
    - "git diff --check: passed"
  tests_failed: []
  tests_not_run:
    - "M behavior, IR-2, ACP-0003 H2, GPU/FPGA/FPAA, approximation, calibration, hardware equivalence, learning, and reward redesign: unauthorized/not applicable"
  assumptions:
    - "EventQueue remains the shared scheduler; stale records are invalidated rather than removed."
    - "EventType.EXCURSION is a routed numeric Model-B source event."
  unresolved:
    - "Luna-0 must independently review and accept or reject this staged implementation."
  recommended_next_agent:
    - "Luna-0: independently verify E1 and integration readiness."
```

## Outcome and owned scope

**OBSERVED:** E1 is implemented as `SingleExcursionNeuron` in
`[tpcn/excursion_neuron.py](../../tpcn/excursion_neuron.py)`. It stores only
bounded signed `x`, a local timestamp, the three authorized E1 modes, one
pending internal event, generation/episode/lineage bookkeeping, captured
polarity, bounded `m_peak`, and bounded provenance.

The reference configuration is `lambda=1`, `X_max=8`, `theta_R=0.25`,
`theta_E=1`, `theta_hold=1.5`, `theta_M=4`, `Delta_t_E=0.5`,
`A_min=0.25`, `A_max=1`, and `P=16`. Configurations validate finite accepted
threshold ordering, positive decay and delay, bounded provenance capacity
`P <= 64`, and a finite event budget.

**OBSERVED:** Local exponential decay is applied only when an addressed
external or valid internal event is processed. Admission captures the sign and
allocates one ordinary episode. A valid `S_EMIT` creates exactly one digital
`EventType.EXCURSION` record. The amplitude map is the accepted bounded,
monotone, saturating map. `S_RETURN` schedules one finite analytic re-arm and
does not admit a second ordinary excursion before returning to `N`.

**OBSERVED:** `EventQueue` now orders external events before internal events at
equal timestamps, preserving sequence order within each priority. Internal
records carry episode, generation, kind, timestamp, and queue identity checks.
Cancellation invalidates the generation; stale queued records are no-ops.
`EventType.EXCURSION` is routed by the existing Model-B edge transfer without
changing `w`, `d`, `r`, or propagation delay semantics.

**OBSERVED:** Reaching `|x| >= theta_M` records a bounded boundary report,
cancels pending ordinary work, emits no ordinary excursion, and halts further
external E1 computation. M behavior is not implemented.

## Architecture evidence

- **A01/A02:** Irregular timestamps use only the addressed neuron's local
  timestamp and analytic decay. No global neural tick or polling loop exists.
- **A03/A04:** Excursion outputs are ordinary queued logical events and Model-B
  routing retains finite edge delay and bounded queue behavior.
- **A05:** No spatial reservoir or spatial feature was introduced.
- **A06/A07:** No predictive-learning or nonlocal information path was added.
- **A08:** State, pending work, generation, provenance, emissions, and boundary
  reports are bounded; finite event-budget exhaustion is explicit.
- **A09/A10:** Contribution/output compression is observable but is not claimed
  as physical energy savings or a utility decision.
- **A11:** Provenance is bounded and exposes truncation after oldest eviction.
- **A12/A13/A14:** No pathway, gate, or structural-plasticity behavior changed.
- **A15:** The implementation is a hardware-neutral software reference; no
  backend, approximation, calibration, or hardware equivalence is claimed.

No architecture contract text changed. ACP-0004 remains accepted for staged
implementation, and only E1 was implemented.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_excursion_neuron.py tests/test_event_runtime.py tests/test_canonical_event_neuron.py tests/test_topology.py` | Windows, Python environment, deterministic queue order | **PASS — 54 passed** | focused E1 and affected runtime/topology controls |
| `python -m compileall -q tpcn tests` | Windows, Python environment | **PASS** | package/test compilation |
| `git diff --check` | starting revision `03302de7121f0dfe340cfd2d87d351ff8d7380a6` | **PASS** | changed-file whitespace check |
| `python -m pytest -q` | starting revision and final working tree | **PASS — 589 passed, 1 skipped** | full CPU suite; no hardware or backend claims |

## Benchmark and resource results

The deterministic compression fixture uses `+0.4@0`, `+0.4@0.1`,
`+0.4@0.2`: three input contributions produce one ordinary excursion at
`0.7`. The leakage control uses the same values at `0`, `5`, and `10` and
produces no excursion. Classification, prediction loss, calibrated energy,
hardware latency, and dataset metrics are not applicable to E1.

## Assumptions, limitations and unresolved issues

The existing `TPCNNeuron` remains an explicitly separate legacy/minimal
continuous-activation reference. E1 does not add a second unlabeled stream to
that class. E1 does not implement M behavior, IR-2, learning, prediction,
reward, structural adaptation, or hardware execution.

## Reproduction and rollback

From the repository root, run the validation commands in the table above and
the full CPU suite. The work is currently uncommitted on `main` at the
recorded baseline. Removing only the six files listed under `files_changed`
restores the pre-Luna-19 state while preserving unrelated work.

## Next assignment

Return to Luna-0 for independent verification. Luna-0 must review the focused
and regression evidence before any integration decision. M/E2, IR-2, H2,
ACP-0002 N3, Luna-13F reopening, Luna-13G, and backend work remain
unauthorized.
