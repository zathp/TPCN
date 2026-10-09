---
name: "Luna-63B Local Interpretation PCN Design Prerequisite"
description: "Design only the missing bounded local spike-interpretation PCN equations and order-state separation protocol; no implementation, simulations, trials or arbitrary network presented as TPCN."
tools: [read, search, edit]
agents: []
---

# Luna-63B — local equations and state-separation prerequisite

**DESIGN PREREQUISITE REQUIRED / DESIGN ONLY AUTHORIZED / NOT EXECUTED.**
No executable PCN or order-memory mechanism is authorized.
Baseline `8123147e04c6044d12023f541cf63130cdbb7dcc`, contract v1.2.
Read the independent Luna-62 review before the separate Luna-63 authorization
handoff, then the governing contract/process/templates and their source pins.
Pin the eventual published governance commit; never invent a contract SHA.
Use a future isolated branch/worktree `experiment/luna63b-local-pcn-design`
or explicitly recorded equivalent, not mutable shared lane artifacts.

## Owned deliverables and bounded question

Only edit:

- `workflow/docs/luna/LUNA_63B_LOCAL_PCN_STATE_DESIGN.md`
- `workflow/handoffs/luna-63b-local-pcn-state-design-20261009.md`

Use the handoff template with every field completed. No agent/index/ACP/
production/test/artifact edits; no generated trials, dataset, runner,
simulation, training, search, scoring, hardware execution or delegation.
No scientific commands. Read-only Git/documentation checks may be
performed by the orchestrator; tools intentionally exclude execute.

Question: is one minimal, explicitly experimental local interpretation
model specifiable whose multidimensional state might retain input order?
HYPOTHESIZED is not OBSERVED. A nonzero state distance is not sequence
decoding, replay or memory capacity. Do not claim arbitrary neural network
output as TPCN evidence. This prerequisite is warranted because:

- `LocalPredictor` is scalar keyed next-observation/error matching, not
  `F_PCN(p, delta_p, z)` with vector retention.
- Historical WEMA equations are indexed smoothing/multiscale weighted sums,
  not a frozen event-time PCN with separated output dynamics.
- No inspected governed polarity-preserving peak-hold/interpretation model
  specifies the proposed local dimensions, coupling and errors.
- ACP-0008 separates scalar x/z but supplies no proposed multidimensional
  order encoder. A02 noncommutativity is weaker than ordered recall.

## Finite design envelope and required equations

At most one candidate, one compartment, two input ports A/B, two encoding
coordinates. Maximum **10 bounded scalar coordinates total** across peak,
delta/last-event, prediction/error and encoding roles; enumerate any reuse.
At most two outstanding local numeric prediction records if needed, one
local timer per declared expiry role (at most three), one active generation,
no recurrent network/topology/FIFO/occurrence links. If insufficient, report
the blocker; do not enlarge the model or add candidates to force success.

State must be explicitly separated:

1. Polarity-preserving peak-held input and event delta: sign convention,
   simultaneous +/- arrivals, overwrite/capture rule, release/expiry and
   bounded event IDs. A/B are fixed causal input ports, not expected answers.
2. Local predictive/interpretation state: write precise fixed equations,
   prediction target/availability/expiry, matching and explicit local error,
   and `F_PCN`'s allowed causal inputs. No trainer/evaluator/global statistics.
   Define whether fixed predictive computation is sufficient; no learning
   trial is authorized and no scalar matcher may be silently relabeled.
3. Two-dimensional retained encoding z: event-time Phi and update operators,
   coupling, clipping, bounds, initial state and finite lifetime/reset.
   Derive whether operators commute; clipping/noise must not be hidden.
4. Output/excursion state: absent/disconnected in this prerequisite.
   No recall cue, emission threshold crossing, decoder or trajectory.

Provide exact equations, finite dimensions/constants/units, time/ID/budget
domains and immutable initialization provenance as a **proposed model**
for independent review. Any added persistent vector/peak/error semantics
must be identified as isolated experimental departures, not amendments to
ACP-0008 or core. Merely calling an arbitrary map PCN is unacceptable;
show how prediction/error causally affects the interpretation, or honestly
report that the model is not a PCN and the prerequisite remains blocked.
Do not infer existence of required equations from prose aspirations.

## Falsifiable protocol to freeze in the design (no trials)

Minimal proposed comparison set: AB versus BA; AAB versus ABA (matched
counts); AA versus A (multiplicity, explicitly count-confounded).
ABC/CBA is outside this two-port envelope, not silently invented.
Declare equal-amplitude polarity controls and exact unequal local event
schedules, a fixed post-LISTEN observation point shared by each matched
pair, finite hold-delay set and expiry. Do not select constants by separation
outcomes. HOLD must be specified independently; do not consume Luna-63A
results or assume its success. No RECALL/replay condition.

Include repeated identical deterministic histories, matched-count
permutations, zero/no-input, total-count/magnitude confounds and a scalar
aggregate accumulator with otherwise matched timing. A leaky scalar can
already distinguish AB/BA due to recency; it is not automatically a
known-insufficient order baseline. Include a commutative/no-leak aggregate
control to expose that distinction. State whether separation is recency,
count, or genuinely persistent noncommuting dynamics; never conflate them.

Specify Euclidean distances, within-sequence replay variation, between-
sequence separation/margin, observation timing sensitivity and survival
through the declared delays. Require exact deterministic state replay in
the stated platform plus independently derived equation tolerances.
Predeclare finite numerical pass/fail tolerances and a nontrivial margin
before any future execution; nonzero roundoff alone is not support.
No noise in this initial design. If future noise is required, a new
authorization must freeze draws, bounds and margin versus variation.

Provide a truth-swapped evaluator/observer-off non-interference plan and
enumerate every computational versus diagnostic field. No external
sequence list/FIFO, evaluator feedback, expected-answer lookup, hidden
order buffer, global timestep or reservoir. Event fixture/oracle sequences
may exist only as presented inputs or measurement, not replay computation.

## Acceptance, governance and stop

Completion means a self-contained, inspectable candidate equation/state
table and **unexecuted** protocol, or an exact missing-equation/blocker
report. Analytical reasoning is permitted; no simulated traces or empirical
claims. Map A01-A08, A12-A15; preserve A06 explicit prediction/error and
A07 locality, bound A08; do not replace A09-A11 energy/credit with this assay.
Discuss qualitative hardware state/precision burden without equivalence.

Future implementation/test ownership is **not granted** here. List
anticipated focused oracle, event/neuron/predictor/peak expiry/state-bounds
regressions as pending; full suite would be required if a separately
authorized future task touched production. Pin all read sources and
governing/design publication revisions and list actual checks, no tests
passing. No results/artifacts from A or C may enter this design.

Disposition: DESIGN PREREQUISITE COMPLETE — INDEPENDENT REVIEW REQUIRED,
or BLOCKED with missing formulation/owner choices. Independent Luna-0
must verify equations, locality, boundedness, predictive interpretation,
controls, provenance and predeclared criteria before separate execution
authorization. Stop; no successor, ACP, canonical mutation, sequence memory,
task efficacy, integrated echo, Luna-64 or architecture promotion.
