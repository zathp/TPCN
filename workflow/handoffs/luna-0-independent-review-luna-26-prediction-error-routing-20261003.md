# Luna-0 Independent Review — Luna-26 Prediction-Error Routing

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Adversarial verification of Luna-26 error routing and reconsideration of Luna-22 closure"
  task_id: "luna-0-independent-review-luna-26-prediction-error-routing-20261003"
  component: "ACP-0006 prediction-error routing and Luna-22 closure readiness"
  status: "PASS — Luna-26 corrective routing independently verified; Luna-26 and bounded Luna-22 integration closed"
  contract_version: "ACP-0006 1.1"
  branch: "main"
  base_revision: "c7fc9b7477e8419af2282969b936db3a242e751b (initial adversarial review)"
  implementation_revision: "9f2e5d98e9abfd3702eb55a4af76c41009872abc"
  corrective_starting_revision: "f63e59552bf1f18b8cf1137abdf331f3aa8056f4"
  corrective_implementation_revision: "8a14681fe6a770e75136227c5059bc9c76ae5d46"
  result_revision: "review publication commit recorded in final commit metadata"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT VERIFICATION", "ADVERSARIAL ROUTING REVIEW", "INTEGRATION DECISION"]
  hypothesis: "The hop-local adapter correction fixes multi-hop delivery while satisfying every ACP-0006 path, identity, timing and boundedness invariant."
  counter_hypothesis: "Forwarding from the current node fixes reachability but still enqueues a repeated-node path."
  architecture_change: false
  proposal: null
  architecture_invariants_touched: ["A01", "A03", "A04", "A06", "A07", "A08", "A09", "A11", "A15"]
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md"
    - "workflow/handoffs/luna-0-authorization-luna-26-corrective-route-path-20261003.md"
    - ".github/agents/luna-26.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  review_production_behavior_changed: false
  luna26_verdict: "PASS — corrective route-path behavior independently verified / closed"
  luna22_verdict: "PASS — bounded ACP-0006 first CPU software-reference integration independently verified / closed"
  recommended_next_agent: ["Project owner / Luna-0 to select one bounded downstream compatibility task"]
```

## Final corrective review outcome

**PASS — LUNA-26 ACP-0006 MULTI-HOP PREDICTION-ERROR ROUTING
INDEPENDENTLY VERIFIED / CLOSED.**

**PASS — LUNA-22 ACP-0006 FIRST CPU SOFTWARE-REFERENCE INTEGRATION
INDEPENDENTLY VERIFIED / CLOSED**, limited to the accepted first fixed-topology
`EXCURSION_V1` integration semantics. This does not establish predictive
efficacy, useful delayed-credit learning, downstream migration, structural
plasticity integration, dataset writer-disjointness, hardware equivalence or
physical-energy calibration.

The prior section below records the initial independent finding at
`c7fc9b7`: the first Luna-26 implementation allowed a repeated-node error
path. The same Luna-26 assignment was corrected under the explicit
same-identifier authorization, and the corrective commit
`8a14681fe6a770e75136227c5059bc9c76ae5d46` was independently reviewed here.
The current implementation rejects an edge whose destination is already in
that error event's route path before route-capacity/queue preflight and before
queueing. The actual cycle has no return arrival; a separate legal outgoing
edge from the same node remains routed. No global visited set is used.

**OBSERVED:** In the corrective mixed cycle/fan-out test, the actual
runtime-generated error takes `n0 -> n0 @ 1.00`, `n0 -> n1 @ 1.25`, then the
legal `n1 -> n2 @ 1.85`; `n1 -> n0` is not queued. Each observed route path
contains unique nodes and depth remains below the network-node count.

**OBSERVED:** The independent diamond retains distinct legal path contexts
to `n3`; the first equal-time arrival applies error once and only one
post-convergence `n3 -> n4` continuation is queued. Per-destination
deduplication remains intact.

**OBSERVED:** The optional `exclude_destinations` API parameter defaults to
the existing complete outgoing routing behavior. Filtering is per call,
preserves edge insertion order, and occurs before fan-out capacity checks,
queue pushes, observer callbacks, sequence allocation, sidecar attachment,
event processing and edge-cost accounting. The post-filter legal fan-out
retains atomic queue-capacity preflight.

**INFERRED:** The corrected integration now satisfies ACP-0006 rules 3 and 6
for the tested directed routes without changing default topology behavior,
Model-B transfer, error payload semantics, or the convergence guard. This is
a software-reference integration closure only; it is not an architecture
promotion.

The initial review phase changed no production behavior. This final review
phase also changed no production behavior or tests; only review/governance
records are being updated.

## Revisions and publication lineage

The requested token
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` does **not** resolve to a Git
object in this repository. The valid checkout was clean `main`, with
`HEAD == origin/main == c7fc9b7477e8419af2282969b936db3a242e751b`, subject
`docs: record Luna-26 implementation revision`. This is the publication
revision referred to by the token in the assignment.

Verified code/publication lineage:

```text
e5d31236432ca5301ca5ca4ba8eb699006a55b09
    exact Luna-26 authorized execution baseline
-> 9f2e5d98e9abfd3702eb55a4af76c41009872abc
    Luna-26 implementation: "fix: forward prediction errors hop by hop"
-> c7fc9b7477e8419af2282969b936db3a242e751b
    completion-handoff publication:
    "docs: record Luna-26 implementation revision"
```

Verified prior governance lineage:

```text
42026a9fc3ccc1b1fdc83e0344c79312f2d76b14
    Luna-25 independent-review baseline
-> ffbf5ed3241ea6291955a6e1bba98bd6be27b54a
    Luna-22 closure-readiness review and Luna-26 authorization publication
-> e5d31236432ca5301ca5ca4ba8eb699006a55b09
    exact Luna-26 execution baseline
```

The implementation delta from `e5d3123` to `9f2e5d9` contains exactly
`tpcn/experiment_excursion_runtime.py` and
`tests/test_excursion_integration.py` plus the Luna-26 completion handoff.
The publication delta from `9f2e5d9` to `c7fc9b7` contains only that
completion handoff. No topology, predictor, eligibility, neuron, schema,
benchmark or downstream-consumer implementation was changed.

Corrective-pass lineage:

```text
f63e59552bf1f18b8cf1137abdf331f3aa8056f4
    exact corrective-authorization baseline
-> 8a14681fe6a770e75136227c5059bc9c76ae5d46
    Luna-26 corrective implementation and completion handoff
```

The corrective implementation changed exactly the four authorized
production/test files and its completion handoff, as listed above. The
independent-review publication records the verification and closure decision.

## Accepted contract and critical route-path finding

ACP-0006 rule 3 requires a bounded sidecar with causal roots, route depth and
route path. Each routed edge appends its destination and increments depth
once. It explicitly requires that a node may not be visited twice within one
routed-event path and caps route depth by the finite network node count.
Rule 6 independently requires opaque error forwarding along directed edges
and a bounded `(prediction_id, destination)` duplicate/delivery guard. Both
requirements apply; passing the dedupe test does not waive the route-path
constraint.

The runtime-generated cycle probe uses the actual causal input sequence:

```text
external 1.2 @ t=0
E2 emission and prediction 0.3 @ t=0.5
admitted target 0.4 @ t=1.0
actual error +0.10000000000000003 @ t=1.0
```

With `n0 -> n1 (0.25)` and `n1 -> n0 (0.40)`, the observed prediction-error
trace is:

| Time | Source | Destination | Route depth | Route path | Outcome |
|---:|---|---|---:|---|---|
| 1.00 | n0 | n0 | 0 | `("n0",)` | Local error consumer accepts |
| 1.25 | n0 | n1 | 1 | `("n0", "n1")` | First hop accepts and forwards |
| 1.65 | n1 | n0 | 2 | `("n0", "n1", "n0")` | **Prohibited revisit is enqueued and processed; guard then suppresses local re-application and further forwarding** |

For this two-node graph, depth `2` satisfies the numeric cap `<= 2`, but the
path repeats `n0`; therefore the path invariant fails independently of the
depth bound. The return event does get queued, receives a sequence and
sidecar, increments processed-event accounting and is traced. It is not
legal to characterize this as a PASS merely because it terminates.

The exact production change creates a fresh forwarding anchor with
`source=event.destination`, routes it through `BoundedTopology.route()`, and
attaches the next context as `context.route_path + (routed.destination,)`.
There is no check that the next destination already appears in the path.
The finding is therefore directly attributable to the Luna-26 route-context
construction/forwarding boundary.

## Original-defect reproduction and multi-hop verification

The exact authorization baseline was independently checked in a detached
temporary Git worktree at `e5d31236432ca5301ca5ca4ba8eb699006a55b09`. The
current six new controls were executed against that baseline source:

```text
5 failed, 1 passed
```

The real one-hop fixture showed the old defect as a second `n0 -> n1 @ 1.50`
arrival instead of stopping after `n0 -> n1 @ 1.25`. The two-hop fixture
repeated `n0 -> n1` instead of reaching `n1 -> n2 @ 1.65`. The convergent
paths re-emitted from their old sources instead of continuing from `n1` and
`n2`. The cycle did not produce the expected legal `n1 -> n0` continuation.
The reset case also showed repeated original-source routing; the queue
capacity/fan-out atomicity control passed. The temporary worktree was removed
after the probe; the review checkout remained clean.

On current revision `c7fc9b7`, the focused integration suite verifies:

- One-hop local `n0` followed by `n0 -> n1 @ 1.25`; no reverse delivery.
- Two-hop unequal delays: `n0 -> n0 @ 1.00`, `n0 -> n1 @ 1.25`,
  `n1 -> n2 @ 1.65`.
- Directed reachability: an incoming-only/unreachable node is not traversed.
- Non-identity Model-B edge parameters do not transform the opaque
  `PredictionError`.
- The complete payload (prediction identity, predictor, target, predicted
  and observed values, signed error, timestamps and observation source),
  event ID, lineage ID, causal roots and truncation state are retained.
  `event_id` matches the prediction ID; queue sequence is freshly assigned
  and distinct.
- Instrumented `MultiExcursionNeuron.receive_event()` observes no prediction
  error.
- Equal-time diamond arrivals are deterministically ordered on two executions.
  Both distinct paths arrive at `n3`; the guard applies its local error once
  and only one `n3 -> n4` forwarding occurs.
- Character reset clears the delivery guard.
- **But** the directed cycle control observes the prohibited repeated path
  shown above. This invalidates the Luna-26 PASS gate.

The reset test deliberately restarts sequentially with the same
`character_id="char"`. This is a valid scoped reset control: the character
queue/sidecar/guard are destroyed, then a fresh character-local predictor and
ledger are constructed. It also reuses the deterministic
`namespace:character:predictor:sequence` identity. ACP-0006 scopes these
identities by model instance and character; the fixture does not establish
global uniqueness across reused character identifiers, and this review does
not make that claim. There are no concurrent old/new character queues or
retained per-character guard entries.

## Other adversarial controls

### Queue capacity and sidecar

**PASS:** The two-edge fan-out test raises `QueueCapacityError` with no
partial fan-out. The adapter still calls `BoundedTopology.route()` on the
actual finite queue, whose existing preflight checks complete fan-out before
any push. Each successfully queued routed event receives a sidecar keyed by
its fresh queue sequence. `_process_one` removes the route sidecar and
queued-timestamp entry at consumption; character teardown/reset clears all
sidecar, event-context and delivery-guard state. No queued event can proceed
without sidecar context (`RuntimeError` otherwise).

### Delayed credit

**PASS:** The integrated delayed-credit test reports matched credit with
`reward_delay=0.25` and measured reward update latency `0.25`. The
eligibility regression for duplicate reward IDs passes and confirms replay
does not mutate ledger clock, traces or retained identities. The exact
focused command for these controls reports **2 passed**. Luna-26 did not
change eligibility or reward code.

### Energy/accounting interpretation

The current implementation and ACP-0006 rule 16 consistently distinguish:

- **Processed event cost:** every queued error arrival is processed and
  charged the existing one-unit event-processing proxy, including an arrival
  later suppressed by the destination guard.
- **Edge transfer cost:** each routed edge is charged when its error event is
  queued. A distinct second diamond branch therefore pays its own incoming
  edge transfer even though its arrival is later deduped at `n3`.
- **Local prediction-error cost:** `_meter_observe_error()` runs only after
  the per-destination guard accepts the arrival. It is counted once for each
  accepted destination, not for the duplicate arrival.
- **Local credit:** `EligibilityLedger.apply_signal()` is called only for an
  accepted destination; duplicate convergent arrivals do not apply credit.

This preserves the implementation's existing activity-cost-proxy
interpretation and introduces no energy formula. These units are not joules.

### Label, future-input, reset and identity boundaries

**PASS within existing tests:** The focused and prescribed integration sets
include label-isolation, incremental admission, no-global-timestep,
character-reset, and identity-high-water controls. Prediction/error creation
uses the actual admitted target; no label or unseen suffix is read by routing.
The same-character reset test establishes per-character guard reset only, as
qualified above.

### Dataset efficacy and downstream compatibility

Luna-25's `luna25-v1` result remains a **task-efficacy observation**, not a
Luna-26 or Luna-22 routing failure: zero matched dataset predictions, zero
generated prediction errors and zero matched delayed credit were reported.
Predictive efficacy and useful delayed-credit learning remain **NOT
ESTABLISHED**; no threshold is inferred and no tuning was performed.

The full-suite 24 failures remain the same baseline-classified downstream
compatibility tests:

| Group | Count | Failure identities |
|---|---:|---|
| CPU visualization / TPCV | 3 | `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data` |
| Luna-12B structural integration | 4 | `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated` |
| Luna-12E legacy observables | 2 | `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` |
| Luna-12L temporal scale | 8 | `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`; `[random]`; `[temporal]`; `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch` |
| Spiral benchmark | 1 | `test_control_results_are_deterministic_and_include_required_order_controls` |
| Temporal analysis | 3 | `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` |
| 3D viewer | 3 | `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics` |

Failure identities, owners and construction-time causes match the published
Luna-0 baseline matrix. They are not repaired or promoted to Luna-22
correctness gates.

## Validation record

| Command / procedure | Observed result |
|---|---|
| Exact authorization-baseline counterexample controls in detached `e5d3123` worktree | **FAIL as expected:** 5 failed, 1 passed; old-source repetition and failure to advance hops observed |
| `python -m pytest -q tests/test_excursion_integration.py` | **PASS: 49 passed** |
| Prescribed 12 ACP-0006 regression modules plus `tests/test_excursion_integration.py` | **PASS: 340 passed** |
| Delayed-credit plus duplicate-reward idempotency tests | **PASS: 2 passed** |
| `python -m pytest -q -rs` | **FAIL: 24 failed, 802 passed, 1 skipped**; all 24 are the classified downstream failures |
| `python -m pytest --collect-only -q` | **PASS: 827 collected** |
| Test-integrity diff from authorization baseline | **PASS:** 6 test functions added; 0 removed; no xfail conversion, unconditional skip or explicit deselection |
| `python -m compileall -q tpcn tests` | **PASS** |
| Diagnostics for runtime and integration test files | **PASS: no errors reported** |
| `git diff --check` | **PASS** |
| Hardware equivalence / physical-energy calibration | **NOT RUN / NOT AUTHORIZED** |

## Initial clause verdicts at `c7fc9b7` (superseded by final table below)

| Clause | Verdict | Evidence |
|---|---|---|
| A01 | **PASS** | No global tick, polling interval or wall-clock neural time added. |
| A03 | **FAIL for this route path** | Edge delays and causal queue times are finite and ordered, but the cycle enqueues a repeated node path. |
| A04 / A08 | **BOUNDED, BUT PATH-CORRECTNESS FAIL** | Topology, queue, event budget, sidecar, route depth and delivery guard are finite; the bounded return event still violates the explicit no-revisit invariant. |
| A06 | **FAIL — Luna-22 remains blocked** | Real local prediction/error and valid two-hop propagation work, but cycle routing does not satisfy accepted rule 3. |
| A07 | **PASS in applicable controls** | Incremental input admission and label-isolation tests pass; no label/future data enters routing. |
| A09 | **PASS for proxy accounting interpretation** | Event, edge and accepted local error costs retain existing finite activity-proxy semantics; no joule claim. |
| A11 | **PASS for existing delayed-credit controls** | Positive-delay reward matches and duplicate reward identity is idempotent; no learning-efficacy claim. |
| A15 | **PASS as software-reference-only scope** | CPU reference only; no backend/hardware equivalence claim. |

## Initial verdict and corrective authorization (superseded below)

**Luna-26 verdict:** `BLOCKED — LUNA-26 VIOLATES ACP-0006 ROUTE-PATH
NO-REVISIT INVARIANT`.

**Luna-22 verdict:** `IMPLEMENTED / BLOCKED / NOT CLOSED`. The prior
multi-hop reachability blocker has been corrected, but the independent review
found this additional applicable ACP-0006 rule-3 defect. No closure claim is
made.

The exact bounded corrective assignment is published separately at
`workflow/handoffs/luna-0-authorization-luna-26-corrective-route-path-20261003.md`.
This remains Luna-26, not Luna-27. It authorizes a minimal optional
destination-exclusion filter in `BoundedTopology.route()` because the current
API always routes its complete outgoing fan-out and cannot omit only
previously visited destinations while preserving atomic queue preflight.
Default topology routing behavior and Model-B transfer must remain unchanged.
The adapter must pass the current event's `route_path` as exclusions so only
edges that revisit this same path are omitted before queueing. The existing
per-destination guard remains required for convergent duplicate arrivals.

Luna-0 must independently review the corrective implementation before
reconsidering Luna-22 closure. Downstream compatibility work remains
separately scoped; efficacy and hardware equivalence remain unestablished.

## Supplemental independent review of corrective revision `8a14681`

Review of the corrective pass began at clean `main` / `origin/main`
`8a14681fe6a770e75136227c5059bc9c76ae5d46`, exactly the implementation
revision identified by the Luna-26 corrective handoff. The implementation
delta from authorization base `f63e59552bf1f18b8cf1137abdf331f3aa8056f4`
contains only:

- `tpcn/topology.py`
- `tpcn/experiment_excursion_runtime.py`
- `tests/test_topology.py`
- `tests/test_excursion_integration.py`
- `workflow/handoffs/luna-26-corrective-route-path-20261003.md`

No ACP/A01-A15 text, predictor, ledger, neuron, dataset, or downstream
consumer behavior changed.

**OBSERVED:** In the real-error cycle-plus-legal-fan-out control, the queued
error arrivals are only `n0 -> n0 @ 1.00`, `n0 -> n1 @ 1.25`, and
`n1 -> n2 @ 1.85`. No `n1 -> n0` return event exists. Their route paths are
`("n0",)`, `("n0", "n1")`, and `("n0", "n1", "n2")`, respectively; each path
contains unique nodes and route depth is less than the three-node network
size. The test observes sidecar attachment only for these queued errors,
unchanged error identity/payload and causal roots, no neuron delivery, and
edge/error cost equal to actual routed edges and accepted local consumers.

**OBSERVED:** The API test confirms the optional exclusions remove only
visited destinations, preserve deterministic edge insertion order for legal
fan-out, do not call the route observer for excluded edges, and do not
consume queue sequence numbers when all edges are excluded. Capacity failure
of the post-filter legal fan-out remains atomic. The default empty exclusion
preserves existing route behavior.

**OBSERVED:** Independent reruns on `8a14681`:

| Command / procedure | Result |
|---|---|
| Topology and focused integration suites | **60 passed** |
| Prescribed ACP-0006 regression modules plus focused integration | **342 passed** |
| Corrective cycle, diamond, and topology exclusion/capacity controls | **4 passed** |
| Full CPU suite | **24 failed, 804 passed, 1 skipped**; failure identities match the seven pre-classified downstream groups |
| Full test collection | **829 collected** |
| `compileall`, diagnostics for all four changed code/test files, `git diff --check` | **Passed; no diagnostics errors** |

The one skip remains CUDA unavailable. The 24 failures are unchanged
downstream visualization (3), Luna-12B structural integration (4), Luna-12E
legacy observables (2), Luna-12L temporal scale (8), spiral benchmark (1),
temporal analysis (3), and 3D viewer (3). They are not Luna-22 core
correctness blockers under the reviewed contract. Luna-25's zero dataset
prediction matches/errors/credit remain task-efficacy observations;
predictive efficacy and useful delayed-credit learning remain
**NOT ESTABLISHED**. Hardware equivalence and energy calibration remain
not run/not authorized.

### Final architecture and closure verdicts

| Scope / clause | Final verdict | Basis |
|---|---|---|
| Luna-26 corrective route | **PASS / INDEPENDENTLY VERIFIED / CLOSED** | Hop-local forwarding reaches directed multi-hop targets; revisits are filtered before routing preflight and queue admission; legal path-local fan-out and convergence are retained. |
| A01 | **PASS** | No global tick, polling timestep, or wall-clock neural time was introduced. |
| A03 | **PASS for tested routes** | Positive finite per-edge delays, causal event order, no repeated node per error path, and finite route-depth bound. |
| A04 / A08 | **PASS for this correction** | Finite topology, filtered atomic fan-out, bounded queue/event/sidecar/delivery state, deterministic convergence and cycle handling. |
| A06 | **PASS for ACP-0006 correctness** | Actual emission -> prediction -> later admitted observation -> nonzero error; one-hop, unequal-delay multi-hop, directed reachability, opaque forwarding and no-neuron-delivery controls pass. This is not an efficacy claim. |
| A07 | **PASS in applicable controls** | Label isolation and incremental admission remain unchanged and pass; no future input enters routing. |
| A09 | **PASS for proxy accounting** | Processed-event, actual-edge and unique accepted local-error costs are consistently accounted; proxy units are not joules. |
| A11 | **PASS for delayed-credit mechanics** | Positive-delay reward attribution and duplicate reward idempotency pass; useful learning remains unestablished. |
| A15 | **PASS as CPU software-reference scope** | No backend or hardware equivalence claim. |
| Luna-22 | **PASS / INDEPENDENTLY VERIFIED / CLOSED** | The last identified core blocker (ACP-0006 error forwarding) is corrected; prior Luna-0 closure-readiness review classified other owned correctness gates as passed. This is bounded to the accepted first fixed-topology `EXCURSION_V1` CPU integration. |

Luna-22 closure does **not** establish task efficacy, useful delayed-credit
learning, downstream consumer migration, E2 structural plasticity,
reconstruction of the historical Luna-22 split, writer-disjointness,
hardware equivalence, calibrated physical energy, or repository-wide
architecture completion. Luna-23, Luna-24 and Luna-25 remain independently
closed in their previously stated bounded scopes. ACP-0006 and A01-A15 are
unchanged.

The next governance action is not an implementation authorization: the
project owner / Luna-0 may select one bounded downstream compatibility
semantic unit. The 24 downstream test failures remain a separate backlog.
