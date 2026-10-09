---
name: "Luna-63A Binary Adaptive Decay HOLD RELEASE"
description: "Implement and verify only the isolated, frozen binary adaptive-decay retention probe; no production neuron change, sequence memory, training or integrated recall."
tools: [read, search, edit, execute]
agents: []
---

# Luna-63A — binary adaptive decay mechanism

**AUTHORIZED / NOT EXECUTED.** Authorization is for a future isolated
experimental-model probe, not execution on main. Read
`workflow/handoffs/luna-0-independent-review-luna62-20261009.md` first,
then `workflow/handoffs/luna-0-luna63-mechanism-authorization-20261009.md`.
Luna-62 passed design review with limitations; its FIFO-like proposal is
retained and still ACP-gated. No integrated echo or Luna-64 is authorized.

## Identity, dependencies and ownership

Scientific/governing baseline:
`8123147e04c6044d12023f541cf63130cdbb7dcc`, contract v1.2.
Before execution pin the subsequently published governance commit containing
this exact contract. Do not invent its SHA or execute an uncommitted freeze.
Orchestrator must supply a clean isolated branch/worktree named
`experiment/luna63a-binary-adaptive-decay` (or explicitly recorded equivalent
isolated experiment branch). Do not execute on main or merely isolate a
directory. No branches are created by this governance assignment.

Read contract, changelog, workflow, acceptance criteria, ACP README/template,
handoff template, ACP-0008 and baseline source ranges in the authorization
record. Historical Luna-47A is an impulse accumulator, not a normalized WEMA;
Luna-47D is a synthetic charge-drain model, not a spiral or canonical neuron.
No other lane's implementation/results are inputs.

Only future worker-owned files:

- `experiments/luna63a/__init__.py`
- `experiments/luna63a/model.py`
- `experiments/luna63a/run.py`
- `experiments/luna63a/protocol.json`
- `experiments/luna63a/README.md`
- `tests/test_luna63a_adaptive_decay.py`
- `artifacts/luna63a/results.json`
- `artifacts/luna63a/replay.json`
- `artifacts/luna63a/manifest.json`
- `workflow/handoffs/luna-63a-binary-adaptive-decay-20261009.md`

No other edits: especially no `tpcn/`, existing tests/artifacts, ACP, prior
Luna-62, agent contract or shared index edits. Use the repository handoff
template and fill every field before implementation; classification is
ISOLATED EXPERIMENTAL MODEL, not production TPCN.

## Hypothesis and exact intervention

HYPOTHESIZED: a bounded signed local scalar can wait unchanged under zero
leak and resume its ordinary analytic exponential decay on release.
Counter-hypothesis: hold changes state, switch applies the new gate
retroactively, release fails its oracle, expiry is bypassed, or cue writes
state/output. Support answers only **can the state wait?**

One scalar `z`, local `last_time`, binary gate `R`, finite expiry/status and
bounded event counter. No fast/output state, peak hold, predictor, network,
sequence slots, decoder, output threshold, discharge, learning or routing.
No production imports in model/run/oracle. It is a retention component,
not a full ACP-0008 neuron.

Freeze these dimensionless analytic constants; no search or alternative arm:

```text
lambda_0 = 1/8 = 0.125
R in {0,1}; lambda_eff = lambda_0 * R
z_max = 4
preload z0 in {-3/4, 0, +3/4}, set only at fresh initialization t0=0
absolute TTL = 64 from initialization (never renewed)
allowed timestamp domain [0,65] for the explicit post-expiry probe only
at most 32 processed local events per instance; one due expiry event
one active generation/instance; no automatic reuse or wrap
```

For a valid event at t < 64:

```text
dt = t - last_time                 # reject late/nonfinite timestamps
z_pre = z * exp(-lambda_0 * R_old * dt)
z = z_pre; last_time = t
if event is a gate cue: R = cue    # binary validation; NO z write
if event is observation: no further computation/state change
```

Use exact zero-leak identity (`z_pre=z`) for R_old=0; do not store floating
infinity or compute `1/0`. Normal decay is the exponential recurrence
present at `excursion_neuron.py:725-735`, not the full neuron's discharge rule.
Gate-switch settles the elapsed interval under the **prior** gate, then
changes the gate for strictly subsequent elapsed time. Repeated same-gate
cues and equal-time cues have no extra effect; valid same-time observations
use insertion order and dt=0. No batch may reorder cues.

Before any cue or observation at `t >= 64`, take terminal expiry:
invalidate/clear z, mark EXPIRED, cancel due expiry and reject cue application.
The expiry row records retained pre-clear value and explicit reason.
Equality expires even if the cue is dequeued before the local expiry event.
After expiry, no state revival/preload/normal evolution; the t=65 probe only
reports terminal status. Reset means a new independent fresh instance,
not ID reuse. Expiry is the only permitted post-initialization direct clear.
Overflow/invalid input faults visibly; never truncate into success.

## Frozen matrix, unequal schedules and controls

All event times are exact binary-representable fractions; serialize their
rational identities as well as float values. No random seed/no noise.
Every row runs for all three z0 values, independently, with fresh state.

| Family | Initial gate; frozen event schedule |
|---|---|
| A1 fixed normal | R=1; observations at 1/4, 7/4, 4, 8, 32, 36 |
| A2 exact HOLD | R=0; observations at 1/4, 7/4, 4, 8, 32, 63 |
| A3/A5 hold then release | R=0; for each H in {2,8,32}, observations at H/8, H/2, H; release cue at H after that observation; observations at H+1/4, H+7/4, H+4 |
| fixed-normal delayed comparator | R=1; for each H in {2,8,32}, same A3 schedule including the R=1 cue |
| prior-gate switch control | R=1; observe at 1/4; HOLD cue at 1; observe at 7/4,4,8; RELEASE cue at 8; observe at 33/4,39/4,12 |
| expiry boundary | R=0; observe at 63; RELEASE cue at 64 offered before due expiry; observe at 64 then 65 |
| duplicate cue control | R=0; observe at 2; two RELEASE cues at 2; observe at 9/4,15/4,6 |

This is 11 schedule variants per preload, **33 frozen instances**. The
z0=0 instances are not separate fitted baselines: all zero-preload instances
must remain zero through every valid gate change. No stored state/RECALL
without preload is thus a primary negative. No continuous/partial gate arm.
Any add-on scientific fixture requires new Luna-0 authorization.

Validation-only negatives (not new scientific arms): nonbinary/bool gate,
NaN/infinity, |preload|>4, negative/late time, >32 events, attempted revival
after expiry. Reject explicitly. Gate cue accepts R only, not a value,
symbol, answer, pointer or desired output.

## Independent oracle and acceptance

Oracle in the focused test must not import model functions or production
code. Compute the closed-form reference from **total time spent in R=1**
since preload: `z_expected=z0*exp(-(1/8)*T_release)` before expiry.
Use independent high-precision standard-library Decimal exponential
(at least 50 decimal digits) and compare binary64 results with
`abs_error <= 1e-12 + 1e-12*abs(expected)`.
Do not fit tolerance from outcomes. Exact HOLD compares identical binary64
bits before/after every hold interval, including negative and zero states.
IDs, rational schedule/ties, gates, expiry and fault status compare exactly.
For split elapsed intervals, the exponential semigroup comparison uses the
same numeric tolerance; observations must not change the mechanism.

Require: normal oracle match, exact hold retention, hold-duration
independence before release, correct resumed recurrence, correct prior-gate
interval (at t=8 switch control retains z0*exp(-1/8)), fixed-normal
loss of nonzero state at long delays, zero-state no creation, TTL equality
preemption, bounds, explicit faults and exact deterministic replay in the
recorded environment. Replay repeats all 33 instances independently.
Same-platform canonical JSON outcome bytes/digests must match, excluding
separately stored run/provenance labels. Cross-platform libm identity is
not presumed.

Anti-command check: inspect cue implementation and trace; cue cannot write
z, a threshold, fast state, `ExcursionEmission` or any output/pending-spike.
No output interface exists; generated output events must be zero by
construction with output dynamics disconnected. This is **NOT evidence
that a connected canonical neuron will recall or emit on release**.

## Departures, regressions, evidence and stop

Explicit isolated semantics depart from ACP-0008's strictly positive,
fixed-per-execution IntegrationConfig decay: lambda_eff=0 in HOLD and a
runtime-local mutable gate instead of immutable effective decay. No frozen
production config is mutated/bypassed. Terminal TTL is a new isolated
wrapper lifetime. A02/A08 permit bounded local elapsed state generally but
do not make these altered neuron semantics accepted core behavior.
A01-A03/A04/A05/A07/A08 are preserved within this one-component scope;
A06/A09-A11 full predictive/energy/credit capabilities are absent from the
assay, not removed from TPCN; A12-A13 remain optional; A14 out of scope;
A15 has only qualitative zero-leak gate/register/expiry mapping, no hardware
equivalence or physical infinite retention.

Before outcomes, publish the identical protocol and focused tests/model
on the isolated branch, pin its pre-outcome commit and unchanged governance
contract Git blob. Do not change equations/criteria after outcomes.
Run focused mechanism/oracle/bounds/replay tests plus unchanged:
`tests/test_event_runtime.py`, `tests/test_excursion_neuron.py`,
`tests/test_e2_multi_excursion.py`,
`tests/test_luna38_excursion_integration_state.py`,
`tests/test_predictive_coding.py`, `tests/test_luna47a_retention.py`,
`tests/test_luna47d_output_model.py`.
Record exact counts/skips/errors and command/interpreter/platform.
Historical source tests are regression evidence, not new lane science.
A full suite is not required for isolated-only edits; production edits are
forbidden, so their perceived necessity is a blocker, not permission.
Integrity/whitespace/scope checks are required. Do not repair historical
failures in this lane or report inherited failures as passes.

Pin starting/governance/pre-outcome/implementation SHAs and Git blobs,
protocol/schedule, raw per-event prior gate/time/state, pre/post state,
expiry/rejections, expected/residual/tolerance, maxima, all 33 identities,
initial/replay digests and every artifact hash. Separate canonical Git
bytes from LF/CRLF checkout bytes; never weaken identity to hide differences.
Oracle/fixtures measure only; they cannot drive computation from expected
results. No lane B/C evidence is consumed.

Report exactly SUPPORTED — ADAPTIVE-TAU HOLD/RELEASE, PARTIALLY SUPPORTED,
NOT SUPPORTED, or BLOCKED with all failures/limitations. Stop after the
completed handoff. Independent Luna-0 must verify intervention/oracle,
controls, source/byte identity, regression state and non-claims before any
successor. Even PASS authorizes no core promotion, ACP acceptance, sequence
memory, task efficacy, integrated echo, Luna-64 or interlane composition.
