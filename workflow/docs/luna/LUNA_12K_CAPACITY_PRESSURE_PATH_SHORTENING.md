# Luna-12K - Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification

This specification defines a controlled follow-up experiment to Luna-12J. It
is `EXPERIMENT` and `VERIFICATION` work. It does not promote the Luna-12I
mechanism into A14, change the architecture contract, or authorize Luna-12L or
later work.

```yaml
luna:
  identifier: Luna-12K
  name: Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification
  task_id: capacity-pressure-equal-exposure-path-shortening-luna-12k
  baseline_revision: "e0f308f5aa76cdf41578f0574a2135b9bb0b256d"
  dependencies: [Luna-12J, Luna-12I, Luna-12H, Luna-12E, Luna-4, Luna-10]
  owner: "Luna-0 Architecture Guardian pending experiment-owner assignment"
  classification: [EXPERIMENT, VERIFICATION]
  production_code_authorized: "only the smallest demonstrated measurement exposure fix"
```

## Authorization and purpose

The Luna-12J handoff records `partially supported` with gate `PASS WITH
FOLLOW-UP`. It specifically calls for equal candidate exposure, a larger
bounded competing-path workload, explicit capacity/rejection pressure and a
meaningful path-shortening intervention. Luna-12K is the formal response to
that bounded follow-up. Creation is authorized by the current Luna-0 dispatch;
do not execute Luna-12K during creation. Execution requires the explicit
execution assignment recorded in the 12K handoff.

Luna-12K must answer:

> When connectivity is scarce, does temporal-associative evidence allocate
> bounded topology more effectively than temporally uninformed growth?

Do not reduce this question to whether a policy creates more fan-in. Useful
allocation requires evidence such as higher active-edge utilization, lower
prediction error, equal performance with fewer edges, shorter useful causal
paths, better behavior at the same edge budget, or lower routed/resource cost.

## Primary hypothesis and falsifier

**Hypothesis:** Under equal candidate exposure and bounded topology pressure,
temporal-associative structural growth preferentially allocates scarce
connection capacity toward useful causal convergence and can create shortcuts
that measurably reduce meaningful propagation path length or delay compared
with temporally uninformed controls.

The hypothesis is falsified in the tested scope if equalized controls match or
exceed useful convergence or path shortening, temporal evidence does not alter
candidate preference, capacity pressure is not reached, a selected shortcut
does not change routed computation, or the result disappears under reversed or
timing-destroyed evidence. The result must be one of `supported`, `partially
supported`, `not supported`, `inconclusive`, or `blocked`.

## Required controls

At minimum compare:

1. fixed topology;
2. pre-12I structural-growth policy;
3. random legal growth;
4. Luna-12I temporal-associative growth; and
5. reversed, shuffled or timing-destroyed temporal evidence.

An oracle-like diagnostic selector may be included only as a non-architectural
upper-bound reference. It is never a legal TPCN learning mechanism.

All compared adaptive policies must receive equivalent opportunity to consider
legal candidates. Equalize, where practical, the candidate set and count,
mutation opportunities, growth attempts, edge budget, fan-in limit, fan-out
limit, pruning/replacement budget, epochs/trials, event workload and seed set.
Candidate exposure must be measured as `exposed`, `considered` and `selected`
counts. If exact equality is impossible, record the mismatch and quantify or
bound its effect. The temporal policy must not receive extra useful candidates
or computation.

## Deterministic capacity-pressure fixture

Construct a bounded deterministic fixture with multiple legal candidates that
compete for finite resources. At least one candidate must be temporally
relevant, one temporally irrelevant, and all selected candidates must be
structurally legal before admission. The workload must reach meaningful
pressure on at least one declared destination fan-in, source fan-out, global
edge capacity, candidate capacity or replacement/pruning budget. Record the
precise rejection reason for every failed admission, including duplicate,
source fan-out full, destination fan-in full, global edge capacity, candidate
unavailable, locality restriction, utility rejection, replacement rejection or
another declared cause.

Include a functional existing long path, for example:

```text
source -> n1 -> n2 -> target
```

The path must have explicit positive finite delays and be exercised before
shortcut growth. A legal shorter candidate such as `source -> target` must be
initially absent, must use ordinary event semantics, and must compete for the
same bounded resources. The graph may differ from this example, but the long
path must be functional, the shortcut must be legal, and both must be in the
actual routed topology rather than an auxiliary visualization graph.

Declare finite bounds for nodes, edges, fan-in/out, candidate lists, event and
queue budgets, observation history, lineage/path depth, mutation attempts,
pruning/replacement, state, and all analysis buffers. Declare time units,
equal-time ordering, reset boundaries, late-event handling and positive edge
delays before execution.

## Path-shortening intervention

Measure the same event stream before growth, after shortcut formation and after
removing or disabling the shortcut. Record:

- hop count and cumulative causal propagation delay;
- each relevant arrival timestamp and tie order;
- routed event count and neuron activations;
- downstream state/output and prediction/error behavior;
- energy/resource proxy, units and utility;
- edge budget, active-edge utilization and capacity/rejection outcomes.

The required causal chain is:

```text
local temporal evidence
    -> shortcut selected
    -> legal shorter real causal path
    -> changed arrival timing and/or routed work
    -> changed downstream state or output
```

Removing the shortcut must restore the longer-path behavior or otherwise
remove its causal contribution. Determine whether the shortcut displaces
another useful edge under pressure. Graph-distance reduction without a change
in routed computation is insufficient.

The handoff must answer directly:

1. Did temporal growth select a real shorter path?
2. Was it formed from legal local evidence?
3. Did it reduce cumulative causal delay and/or routed work?
4. Did it alter downstream neural state or output?
5. Did removing it reverse the effect?
6. Did the benefit survive equal candidate exposure?
7. Did it crowd out another useful edge under capacity pressure?

## Measurements and information boundaries

Record, per condition and declared seed:

- task accuracy/class separation, prediction loss and prediction-error events;
- candidate edges exposed, considered and selected;
- growth attempts, accepted additions, rejection reasons, pruning/replacement;
- fan-in/out distributions, saturation, global edge utilization and active-edge utilization;
- convergent fan-in motifs, duplicate proposals, edge churn and stabilization;
- hop count, cumulative path delay, arrival timestamps and path-shortening frequency;
- routed events, neuron activations, energy/resource proxy and utility;
- same-seed candidate-selection, topology and replay determinism.

Labels remain outside canonical events, predictor state, routing, topology
evidence, structural-learning evidence, eligibility and energy computation.
Structural evidence may use only causally/local available event relationships.
Global evaluation and orchestration may measure results but cannot become
runtime neural or structural inputs. No future event, label, global topology
statistic, evaluation metric, wall-clock value or unrestricted trainer state
may influence a canonical decision.

## Invariants and exclusions

Preserve A01 event-driven computation, A02 intrinsic temporal state, A03
finite propagation and unequal delays, A04 bounded topology, A06 predictive
coding, A07 locality/information boundaries, A08 bounded recurrence, A09/A10
local energy and utility semantics, A11 delayed credit, A14 bounded structural
plasticity and A15 hardware independence.

Do not amend `ARCHITECTURE_CONTRACT.md`, mandate a temporal-association rule,
redesign Luna-12I because results are weak, add unbounded topology, introduce
a global neural timestep, claim real-data or hardware acceptance, or authorize
another milestone. Minimal production changes are allowed only to expose an
existing legal configuration or measurement and must be justified in the
handoff.

## Required focused tests and validation

Focused tests must establish:

1. equal candidate exposure between adaptive conditions;
2. identical topology and resource bounds;
3. no label or future-information leakage;
4. same-seed candidate and topology determinism;
5. actual capacity pressure with recorded rejection reasons;
6. functional pre-existing long path;
7. legal shortcut formation when temporal evidence supports it;
8. changed real routed computation after shortcut formation;
9. removal of the shortcut removes its causal contribution; and
10. reversed/destroyed temporal evidence changes shortcut preference as predicted.

Run and classify separately as `passed`, `failed`, `not run` or `not
applicable`: focused 12K tests; 12J, 12I and 12H tests; relevant 12E routing
tests; affected structural-plasticity and classifier/readout regressions; full
`pytest`; compile/static validation; workspace diagnostics; and `git diff
--check`. Keep all declared seeds, including unfavorable outcomes. Do not
search seeds until a favorable result appears.

## Evidence and gates

The completion handoff must distinguish:

- **OBSERVED:** directly measured fixture, topology, route, state, resource or
  validation result;
- **INFERRED:** interpretation supported by those observations; and
- **HYPOTHESIZED:** untested scale, generalization or mechanism claims.

**PASS:** Equal-exposure controlled evidence shows more useful allocation than
controls under real capacity pressure and demonstrates path-shortening
causality. This still returns to Luna-0 and does not promote A14.

**PASS WITH FOLLOW-UP:** The mechanism remains promising but one bounded issue
remains, such as limited seeds, synthetic-only benefit, energy uncertainty,
capacity-regime sensitivity or insufficient topology scale.

**INCONCLUSIVE:** The valid experiment cannot distinguish the policies.

**NOT SUPPORTED:** Controlled evidence does not support the hypothesis in the
tested scope.

**BLOCKED:** A defect, invalid comparison, information leak, nondeterminism,
broken path semantics or missing dependency prevents valid evaluation.

No gate authorizes Luna-12L or later work. Any positive result returns to
Luna-0 for a separate architecture decision and any required ACP.

## Dependency graph

```text
Luna-12I
    |
    v
Luna-12J  PASS WITH FOLLOW-UP
    |
    v
Luna-12K  Capacity Pressure / Equal Exposure / Path Shortening
    |
    v
Luna-0 review

Luna-13 and Luna-14 remain independent siblings.
```
