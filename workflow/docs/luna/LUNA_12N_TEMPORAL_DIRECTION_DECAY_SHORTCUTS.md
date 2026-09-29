# Luna-12N - Temporal Direction and Intrinsic-Decay-Gated Shortcut Verification

This is a creation-only `EXPERIMENT` and `VERIFICATION` milestone. It does
not execute without a separate explicit execution assignment, promote A14,
change the architecture contract, accept hardware, redesign classification or
authorize a successor Luna.

```yaml
luna:
  identifier: Luna-12N
  name: Temporal Direction and Intrinsic-Decay-Gated Shortcut Verification
  task_id: temporal-direction-intrinsic-decay-shortcut-verification-luna-12n
  classification: [EXPERIMENT, VERIFICATION]
  baseline_revision: "0d91207ec5db0ab8011e0fc020cc9e4e20915428"
  dependencies: [Luna-12M, Luna-12K, corrected Luna-12L, Luna-12J, Luna-12I, Luna-12H, Luna-12E, Luna-4, Luna-10]
  owner: "Luna-0 Architecture Guardian pending experiment-owner assignment"
  production_code_authorized: "only the smallest demonstrated exposure fix; otherwise experiment components"
```

## Evidence boundary and question

The creation begins at repository HEAD `0d91207ec5db0ab8011e0fc020cc9e4e20915428`,
with a clean working tree. Luna-12N is unused at this baseline. The evidence
boundary is:

- **12H:** intrinsic temporal state and unequal-delay semantics are valid.
- **12I:** local temporal association can form bounded convergent structure.
- **12J:** temporal structural changes can alter real routed computation.
- **12K:** equal exposure and capacity pressure can produce a genuinely shorter
  causal route.
- **Corrected 12L:** the current policy did not demonstrate robust four-class or
  scale benefit; this does not disprove shortcut formation.
- **12M:** corrected `TPCN-EDGE-2` instrumentation exposes edge identity and
  lifecycle, phase-scoped traffic, candidates and rejection records, decay
  context, pruning observations, replay determinism and ON/OFF non-interference.
  Replacement attribution and hardware export remain unavailable.

The research question is:

> Can locally available connection direction and intrinsic neuron decay improve
the fraction of bounded structural mutations that create genuinely used
causal shortcuts, without global topology information?

The motivating ambiguity is explicit: a temporal association can connect a node
on one path to the end of another without reducing source-to-target causal
distance. A two-hop partial path joined to the end of a three-hop route can
merely create another three-hop route. Edge existence is therefore not a
shortcut result.

## Hypotheses and falsifiers

**H1 - direction:** candidate edge orientation affects the probability that a
mutation reduces real causal path delay. It is falsified if legal earlier-to-
later and later-to-earlier interventions are equivalent or the tested reversal
is worse under matched opportunity.

**H2 - intrinsic decay:** associations separated by meaningful local intrinsic
decay are more likely to span intervening computation and form real shortcuts
than nearly adjacent associations. It is falsified if decay-relative variants
are equivalent or worse, or if any observed difference requires a fixed global
time threshold.

**H3 - combined:** appropriate direction plus decay-relative preference
increases used shortcut yield under equal opportunity and bounded resources. It
is falsified if the combined condition does not improve used yield, or if the
apparent improvement is caused by unequal exposure, traffic-unmeasured graph
change, or nonlocal information.

Negative, unstable and small-fixture results are valid results. No hypothesis
is assumed true.

## Policy matrix and controls

Declare the policy settings before inspecting outcomes:

| Policy | Direction | Decay preference |
|---|---|---|
| current temporal association | current legal orientation | none |
| reversed temporal association | reversed legal orientation, same pair where legal | none |
| decay-aware temporal association | current legal orientation | local intrinsic-decay-relative |
| combined direction + decay-aware | reversed legal orientation, same pair where legal | local intrinsic-decay-relative |
| random legal growth | seeded random legal orientation | none |
| fixed topology | no growth | not applicable |

If literal reversal is illegal for a candidate pair, retain the direction
question with a declared equivalent legal orientation comparison and record the
reason. Do not silently remove the condition. Adaptive policies must receive
the same or closely comparable candidate set, candidate exposure, candidates
considered, growth attempts, workload, epochs/replays, seed set, edge/fan-in/
fan-out/candidate capacities, replacement/pruning budget and event budget.
Record every mismatch.

Use seeds `0, 1, 2, 3, 4` by default. Any additional seed or decay setting
must be declared before outcome inspection. Compare a small predeclared set of
relative regimes (for example weak, moderate and strong residual separation)
derived from the current neuron's declared dynamics; do not seed-search or
tune a threshold after seeing results. Absolute time cutoffs are diagnostic
controls only, never the principal policy.

## Locality and architecture boundary

Preserve A01 event-driven computation, A02 local intrinsic state, A03 finite
propagation and unequal delays, A04 bounded topology, A06 predictive coding,
A07 local information boundaries, A08 bounded dynamics, A09/A10 local energy
and utility semantics, A11 delayed credit, A14 bounded structural plasticity
and A15 hardware independence. No ACP is required.

Legal policy inputs are local event timestamps, local elapsed time, the source
neuron's decay parameter or residual state, local candidate evidence and edge
state already legal under A14. A reference quantity may be `D = exp(-lambda *
delta_t)`, where `lambda` and `delta_t` are local. Forbidden inputs are global
shortest paths, hop counts in runtime learning, labels, task accuracy,
whole-network energy, offline shortcut classifications, future events,
centrality and global topology summaries. Global path analysis is permitted
only in offline evaluation.

Labels remain external readout/evaluation metadata and cannot enter events,
payloads, IDs, predictor state, routing, structural evidence, eligibility or
energy computation. Do not alter pruning rules, edge protection periods,
persistent strength, utility or eligibility. Those persistent edge states are
not present and must remain absent. Do not add protected edges, a permanent
threshold, genetic hyperparameters, a local micro-network or a classifier
redesign.

All nodes, edges, candidates, histories, queues, event/lineage paths, mutation
attempts and analysis buffers are finite. Positive finite edge delays, reset
boundaries, equal-time ordering, late-event handling and event budgets must be
declared before execution. Hardware mapping is limited to finite counters,
local decay arithmetic and bounded records; no hardware equivalence is claimed.

## Measurement contract

Use corrected Luna-12M `TPCN-EDGE-2` records as the measurement basis:

- endpoint-plus-generation edge identity and lifecycle transitions;
- candidate proposed/considered/accepted/rejected records and exact reasons;
- creation/removal/pruning information, with unavailable timestamps explicit;
- phase-scoped old-route, new-edge and new-route traffic;
- edge first/last use, routed counts and emission/arrival timestamps;
- local decay context, including `delta_t`, decay rate, pre/residual/post state
  and derived factor; and
- replay digests and instrumentation ON/OFF equality.

Do not replace measured route traffic with fixture constants. If a quantity is
not established, report `not established`. Replacement attribution, hardware
export, traffic crossover and dominance may remain unavailable.

For each accepted mutation, measure old-route traffic before and after growth,
new-edge and new-route traffic after growth, and old-route traffic after
shortcut removal. Where supported, report route coexistence, dominance,
traffic crossover, time to first use, time to last use and later pruning.

Record both hop-count delta and causal timing: cumulative-delay delta and
arrival-time delta. Causal delay is primary because unequal propagation delays
are legal. Also record prediction loss, prediction-error activity, proxy energy
with units/calibration status, event and activation counts, edge count and
utilization, candidate exposure/counts, attempts, accepted edges, rejection
reasons, fan-in/out limits, replacement/pruning observations, workload and
seeds.

## Shortcut outcomes and primary metric

Classify accepted mutations offline, without feeding classifications back into
learning:

- unused new edge;
- used but no causal compression;
- static shortcut but unused;
- used shortcut;
- shortcut coexists with old route;
- shortcut dominates old route;
- old route remains dominant; and
- shortcut later pruned.

A **static shortcut** is a graph/path property established offline. A **used
shortcut** must have both (1) reduced measured cumulative causal path delay
(and record hop and arrival-time deltas) and (2) actual routed traffic on the
new edge/new route.

```text
static_shortcut_yield = accepted mutations classified as static shortcuts /
                        accepted structural mutations

used_shortcut_yield = accepted mutations that reduce measured causal path delay
                      and carry routed traffic /
                      accepted structural mutations
```

Report zero accepted mutations explicitly as undefined/not applicable rather
than silently treating the ratio as a win.

## Causal intervention

For representative learned shortcuts, run the identical input with the
shortcut present and with it removed or disabled. Compare route traces,
cumulative delay, hop count, arrival timestamps, downstream state/output,
prediction and error, event/activation counts and proxy energy/resource
metrics. The intervention must establish, as far as the fixture permits:

```text
local evidence -> structural choice -> real topology change
-> real traffic -> changed causal route -> changed downstream computation
```

A graph-only difference is insufficient. If removal does not change the routed
trace or downstream computation, the mutation is not causal shortcut evidence.

## Required focused tests and artifact

Focused tests must cover:

1. current-direction policy remains unchanged;
2. reversed orientation uses the intended candidate pair or declared legal equivalent;
3. decay-aware selection uses local neuron decay, not a global time threshold alone;
4. same seed reproduces candidate decisions;
5. adaptive policies have equal/comparable candidate opportunity;
6. labels, future information and global topology do not leak into decisions;
7. static shortcut detection is separate from used shortcut detection;
8. phase-scoped traffic comes from 12M instrumentation;
9. a used shortcut reduces measured causal delay;
10. an unused shortcut is excluded from used yield;
11. shortcut removal changes/restores routed trace as expected;
12. unequal edge delays are handled correctly;
13. energy and prediction metrics remain comparable; and
14. pruning semantics are unchanged.

Each machine-readable result must include baseline revision, policy, direction
mode, decay mode and predeclared parameters, seed, workload/configuration,
candidate exposure/counts, attempts, accepted edges, rejection reasons, static
and used shortcut counts/yields, old/new route traffic, hop/delay/arrival deltas,
prediction loss, proxy energy and units, event count, edge utilization,
causal-intervention result, and validation status. Keep raw 12M records
separate from offline taxonomy and summaries.

## Gates and dependency

- **PASS:** equal-opportunity controlled evidence increases used causal
  shortcut yield for direction and/or decay-aware selection, with causal
  intervention confirming the effect. This does not promote A14.
- **PASS WITH FOLLOW-UP:** used yield improves but a bounded issue remains,
  such as energy overhead, prediction degradation, premature pruning, route
  coexistence ambiguity or small-fixture limitation.
- **NOT SUPPORTED:** controlled variants do not improve used shortcut formation
  or useful routing in the tested scope.
- **INCONCLUSIVE:** valid execution cannot distinguish the variants.
- **BLOCKED:** instrumentation, locality, fairness, determinism or causal
  intervention is invalid.

```text
Luna-12M
instrumentation PASS WITH FOLLOW-UP
    |
    v
Luna-12N  Temporal Direction + Intrinsic-Decay-Gated Shortcut Verification
    |
    v
Luna-0 review
```

No successor Luna is authorized. The back-burner hypothesis that a used edge
may need a bounded local evaluation/protection interval before pruning is
recorded only for future consideration if 12N produces direct premature-
removal evidence. Future inherited/genetic neuron hyperparameters are also
recorded as out of scope and are not implemented here.

## Creation and completion boundary

Owned files are the 12N agent brief, this specification, the 12N handoff,
experiment components/tests/artifacts explicitly assigned at execution, and
only the smallest demonstrated measurement exposure fix. No changes to
`ARCHITECTURE_CONTRACT.md`, pruning semantics or core architecture are
authorized. The execution handoff must separate `OBSERVED`, `INFERRED` and
`HYPOTHESIZED`, and passed, failed, not-run and not-applicable checks.

Creation validation requires: unused-namespace verification; 12M evidence-gate
verification; confirmation that 12M remains the measurement basis; no contract
change; agreement among agent/spec/handoff; documentation/static checks; and
`git diff --check`. Execution is not performed by this creation milestone.
