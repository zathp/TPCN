# Luna-47A fixed protocol — declared before outcome generation

## Identity, classification and boundaries

Worker: Luna-47A; owner: project owner; contract 1.2; branch
`copilot/luna47a-investigation`. Authorization/base checkout:
`789dda5988daf72f375d9713bd76a6da2b9e8b34`; production/evidence baseline:
`2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Classification: offline experimental-model mechanism investigation.
Dependencies: reviewed Luna-46 corrected evidence and reviewed Luna-44/45
raw captures, not another Luna-47 lane. No architecture change or ACP.

HYPOTHESIS: a finite event-time retention rate can make some of the
Luna-46 retention-limited signed streams cross the unchanged threshold.
COUNTER-HYPOTHESIS: neither fixed finite-rate variant crosses those streams.
Drive-limited negatives must remain explicit. Preserve Luna-46 **MIXED** and
its exact category priority; never reclassify the historical diagnostic.

Owned paths: `experiments/luna47a/`, `artifacts/luna47a/`,
`tests/test_luna47a_*.py`, and the named Luna-47A handoff. No core, governance,
fixture, input, gain, weight, threshold, topology, output or routing edits.
No efficacy, hardware, parameter search, integration or successor.

## Three stages and equation

1. Baseline estimation: frozen zero reference `b=0`, no fitting or adaptive
   estimator. Retained signed routed payloads already use the frozen model.
2. Qualification: identity `q(u)=u`; **all** successful signed receptions,
   including zero/opposing values, pass unchanged. No new noise gate.
   "Meaningful" here means the frozen admitted stream, not verified signal
   versus noise truth. No future points, labels or statistics enter state.
3. Accumulation: one signed binary64 scalar, initial state `a=0`.

Between exact event timestamps, `da/dt=-lambda*a`, evaluated analytically.
At reception `i`:

```
dt = t_i - prior_clock
rho = exp(-lambda * dt)
retained = rho * a_previous
unclipped = retained + q(u_i)
a_after = min(4, max(-4, unclipped))
margin = abs(a_after) - 1
```

Baseline component: `lambda=0.0125`, `tau=80`.
Two and only two experimental variants:
`lambda=0.00125`, `tau=800` (tenfold retention) and
`lambda=0.000125`, `tau=8000` (hundredfold retention).
These decade multipliers are fixed illustrative finite retention contrasts,
not selected from critical roots or outcomes. Input gain remains exactly 1.
Offline signed zero-decay prefixes are the retained Luna-46 reference only,
never counted as finite-rate success. No normalized moving-average input
coefficient is used: this is an equivalent continuous-time leaky **impulse
accumulator**, not a claim about a particular normalized WEMA implementation.

Threshold is exactly `abs(a)>=1`; equality crosses, with no rounding/tolerance.
No output or discharge occurs in this isolated component, including after
crossing. Thus a crossing is representability, **not** canonical emission.
Production discharge is absent in the target baseline; if evidence shows
discharge/clipping/direct admission or a recurrence mismatch, BLOCKED.
Cap=4 is the unchanged frozen state bound. Clipping is measured, and a
clipped target trajectory cannot count as support.

Units: frozen logical-time units and routed-payload/state units, not seconds,
volts, joules or neural ticks. Reset scalar and clock to zero per character.
Retain every actual destination update, including intervening non-reception
updates with deposition zero; the first interval uses its retained prior
clock. Reject missing continuity; never synthesize an arrival. Equal-time
events retain queue-sequence order, with zero elapsed time. No global step
or discrete approximation. Analytic relaxation semigroup tests compare
split intervals to their continuous-time target.

Supported numerical domain: finite `0 <= time <= 1e12`, monotonic timestamps,
finite `abs(payload)<=1e6`, at most 4096 updates per stream; state in [-4,4].
Fixed rates are positive. Exponential underflow to zero at extreme spacing
is legal, explicitly tested; input addition cannot overflow this domain.
At most 320 primary and 320 historical streams, 100 MiB per source file.
Unsupported/nonfinite values, excess events, duplicate identities, unordered
events or invalid rates are rejected, not clipped into the accepted domain.

## Evidence, replay and tolerances

Read only the corrected Luna-46 file:
`artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`,
2337377 bytes, SHA-256
`0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e`.
Require committed baseline bytes, internal digest, exact MIXED disposition,
320 sequence identities and exact category inventory (212 no reception,
33 retention-limited, 75 drive-limited, 0 other; 235 receptions).
Use the **reviewed, unchanged** Luna-46 integrity, raw reconciliation and
recurrence functions, not its branch-specific execution entry point.
Verify all 33 pinned source identities/catalog entries and frozen fixture,
configurations and retained source Git pins before interpreting results.
All six Luna-45 initial/replay phase digests must pass.

Pre-outcome environmental observation: the unchanged Luna-46 integrity test
failed because this Windows checkout materializes the catalog as 7122 bytes,
SHA-256 `5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80`,
versus its reviewed Git blob of 7121 bytes, SHA-256
`a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.
Replacing CRLF with LF proves exact equality; `core.autocrlf=true`.
This is documented **before new mechanism outcomes**, not a result-driven
tolerance. The authoritative input source is therefore exact Git blobs at
the production/evidence baseline. Materialize only the required reviewed
evidence into ignored, lane-owned `experiments/luna47a/_evidence/` for the
unchanged verifier; do not modify or normalize the historical files.
Record physical checkout hashes and Git hashes separately. Reject any
checkout difference not explained exactly by LF/CRLF materialization.
Exact pinned lengths/hashes still apply to the authoritative blob bytes.
Record pre/post physical checkout hashes to prove no historical edit.
The original regression remains a reported failure, not a passing test.
This isolated read adapter is not a production or governance correction.

For each calibrated initial/replay character, independently reconcile both
raw routes one-to-one and verify relay emission origins/fixed Model-B
transfer, destination coverage/configuration and trajectory/trace boundaries.
Reconstruct all Luna-46 sequence measurements and require exact canonical
equality to the reviewed corrected sequence evidence. No fitting to residuals.
Retain source identities, raw enqueue/reception rows, exact update boundaries,
sequence/fixture/raw/input identities and frozen configuration in inputs.json.
Run variants independently over both phases; require exact analytical bytes.

Equation tolerances only:
`64*sys.float_info.epsilon*max(1,abs(observed),abs(expected))`.
Retained input bits, timestamp subtraction, queue ordering, hashes, category,
threshold crossing and replay canonical bytes are **exact**.
Every equation comparison retains expected/observed/residual/bound.
Use Python math.exp binary64; cross-platform libm equality is not promised.
There is no discrete-WEMA approximation requiring another tolerance.

Per event retain previous/pre-event/post-event signed state, exact timestamp,
prior timestamp, elapsed time, decay factor, signed/absolute decay loss,
payload, unclipped value, clipping flag, threshold margin/crossing and
baseline difference. Per sequence retain first crossing, extrema, maximum
absolute state and original category. Keep all no-reception/negative rows.
Report rescued and unrescued retention IDs and remaining drive-limited IDs.
Track representability against original signed zero-decay crossing reference.

Historical compatibility: also replay the reviewed Luna-44 calibrated
**source-to-relay** raw reception streams (320 characters), with the same
three isolated no-output accumulators, preserving exact timestamps/order.
Report changed state/crossing decisions and cap use outside the target
diagnostic, rather than assuming longer retention is behavior-preserving.
This historical comparison is a **component counterfactual**, not a replay
of the full historical neuron (which has discharge/output); no claim of
preserved historical emissions or efficacy is permitted. Production
historical records/configuration remain byte-identical. Fixed synthetic
controls additionally expose cancellation, isolated impulse decay,
same-time accumulation, sparse drive and long-gap forgetting.

## Fixed verdict criteria

Integrity, recurrence, exact replay, event-domain/boundedness tests and
absence of target clipping are prerequisite gates. A new applicable failure,
empty reception/retention denominator or corrupt/incomplete evidence yields
**BLOCKED**. Known baseline Windows fixture-materialization failures must
be reported without changing assertions; they do not erase valid retained
evidence. Preserve all negatives even if a variant succeeds.

- **SUPPORTED**: at least one fixed finite-rate variant crosses all 33
  original retention-limited streams, and both variants leave all 75
  original drive-limited streams non-crossing, with all prerequisite gates.
- **PARTIALLY SUPPORTED**: at least one retention-limited stream crosses,
  but neither single variant crosses all 33, with the same gates and all 75
  drive-limited streams remaining non-crossing (even if their union is 33).
- **NOT SUPPORTED**: zero retention-limited rescues, gates otherwise pass.
- **BLOCKED**: any failed prerequisite, or drive-limited crossing.

Report per-variant counts separately; union does not select a new rate or
prove one finite rate fixes every stream. Broader scientific verdict stays
Luna-46 MIXED regardless of this narrower mechanism result.

## Validation, promotion boundary and rollback

Commit this protocol, runner and synthetic tests before retained execution.
Focused tests: declared recurrence, exact threshold, signed cancellation,
ties/order sensitivity, intervening zero deposition, reset, domain/cap,
extreme time/payload, continuous-time semigroup, deterministic replay,
criteria boundaries and tamper/path rejection. Regression: reviewed Luna-46
suite, ACP-0008 neuron/runtime/topology and Luna-44/45 retained verification.
No task-efficacy experiment or full training run.
Record actual commands/exits, environment, code/protocol/config hashes and
numerical bounds in artifacts and completed handoff; "not run" for omissions.
Bundle writes only new files under canonical `artifacts/luna47a/`; reject
aliases escaping the worktree. Replay verifies input/result canonical bytes
and hashes without overwriting. Record pre/post retained integrity.

A01/A02: analytic event time, not a global clock. A06: prediction remains
production behavior, not tested/replaced by this component. A08: finite
state/events/domain. A15: no hardware equivalence assertion. A07: statistics
remain downstream. No amendment/departure from production architecture.
Rollback removes only this lane's additions; restore authorization checkout.
Next role: independent Luna-0 review of the pushed handoff, not a successor
or self-approval. Stop after push and remote/clean verification.
