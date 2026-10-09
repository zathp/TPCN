# Luna-60 — Binary task-output interface prerequisite

**Status:** implementation and Luna-0 review complete; committed-state
publication validation pending.

**Authority and boundary:** this implements only the bounded contract in
`.github/agents/luna-60.agent.md` (published at `b1d8cc16261ea077b9d3b7c7cb24c975e4c721ee`)
and its explicit subsequent assignment. It is a downstream, no-training
interface prerequisite, not a neural-runtime feature, task experiment, or
efficacy result.

## Evidence vocabulary and source pin

- **OBSERVED:** clean `main` and `HEAD` were
  `b1d8cc16261ea077b9d3b7c7cb24c975e4c721ee` before edits. This is the
  implementation base; the authorization's historical source references
  point to `4ffd13f163d7eb95747b45a1d9d23550ee11c39f`.
- **OBSERVED:** re-resolving the three pinned blobs at the assigned checkout
  returned the same objects:

  | Source interface | Assigned-checkout Git blob |
  |---|---|
  | `tpcn/excursion_neuron.py` | `c0bdece6b15009db4e2b7d69c3242be174b5de80` |
  | `tpcn/experiment_excursion_runtime.py` | `b4e074f0139f3fcfb59189c8313c934c551d6bcb` |
  | `experiments/luna54/run.py` | `08a95b44ddec1d2788d9a914b9653f86abd6d151` |

- **OBSERVED:** the frozen emission record carries event ID, sequence,
  source, logical timestamp, payload, lineage, episode and
  `EventType.EXCURSION`. `MultiExcursionNeuron` creates the emission at its
  delayed emission transition. The runtime observes the actual returned
  emission before its existing consumers and finite routing.
- **INFERRED:** no missing neural primitive was found for this external
  mapping. The presence of the `destination` source establishes source
  availability only, not task performance or utility.
- **HYPOTHESIZED:** none. This is not a scientific experiment.

## Implemented schema and mapping

`experiments/task_output_interface.py` is independent of the neural runtime.
`map_emission(emission, window)` is truth-blind and returns `None` for any
source other than `destination` or event type other than `EXCURSION`.
Otherwise, every actual designated-source canonical emission maps
affirmatively, without a payload-sign, amplitude, lineage, state, truth or
performance filter.

Schema revision 1 records:

| Field | Meaning |
|---|---|
| `trial_id`, `evaluation_window_id` | Predeclared, bounded external window identity |
| `channel_id` | Fixed `target-before-deadline` |
| `source_id` | Fixed `destination` |
| `prediction_event_id` | Exact canonical `emission.event_id` |
| `prediction_time` | Exact source `emission.timestamp`, not routed arrival |
| `emission_sequence` | Exact canonical `emission.sequence` |
| `target_type` | Fixed `designated-target-event` |
| `predicts_occurrence` | Always `true`; no synthetic negative record |
| `prediction_id` | Versioned, injective base64-component encoding of `(trial_id, evaluation_window_id, channel_id, prediction_event_id)` |

The record also carries a private SHA-256 digest of the full canonical
emission content solely to detect conflicting re-observation of the same
identity. It is not part of the identity, exposed as a score feature, or
used to decide whether an emission maps. Thus sign/amplitude changes cannot
turn an affirmative output off; a same-identity content conflict fails
clearly rather than silently deduplicating.

`TaskWindow` freezes one trial/window and requires finite
`t_start <= t_evidence <= t_deadline < t_close`, a logical time unit, and
finite emission/identity capacities. The per-trial emission and identity
capacities default to 256, must be positive and cannot exceed hard ceilings
of 4096; identity capacity cannot exceed emission capacity. Identifier bytes
are caller-bounded (at most 256), the task identity is caller-bounded (at
most 2048 bytes), and each mapped identity is checked against that declared
bound. These are implementation resource bounds, not task calibration.

The evaluator accepts mapped task records only. It requires canonical
nondecreasing event time and strictly increasing source sequence, with
sequence resolving equal-time order. Exact identity re-observation is an
idempotent no-op; a differing record/content digest for that identity fails.
Distinct records outside inclusive `[t_start,t_close]` are kept as bounded
observations and counted as out-of-window, never reassigned.

On emission/identity-capacity exhaustion, the evaluator marks overflow and
will finalize as `INCOMPLETE/CENSORED`. It does not raise into, alter, or
backpressure neural execution. Per-trial arrays and identity maps are cleared
at close; reuse requires an explicit reset with a new trial/window identity.
No global registry or cross-trial learned state exists.

## Frozen evaluation behavior

The first distinct task output in inclusive `[t_start,t_close]` is primary.
An early primary remains an incorrect `PREMATURE` output; later distinct
outputs are counted as duplicates and cannot replace it. Evidence and
deadline endpoints are inclusive for positive on-time scoring. An output at
`t_close` is included. No output is manufactured for silence.

| Complete trial | Confusion cell | Subtype |
|---|---|---|
| Positive, first primary in `[t_evidence,t_deadline]` | TP | ON-TIME |
| Positive, first primary `< t_evidence` | FN | PREMATURE |
| Positive, first primary `> t_deadline` and `<= t_close` | FN | LATE |
| Positive, no primary through close | FN | SILENT/MISSED |
| Negative, no primary through close | TN | TRUE-NEGATIVE |
| Negative, any primary in scoring interval | FP | PREMATURE, LATE, or FALSE-POSITIVE timing subtype |

Incomplete observation before close, pending due work, truncation or overflow
has no confusion cell and cannot count as correct silence or a miss.
Finalization is a function of externally supplied completion evidence; it
does not advance the neuron queue or add a deadline/silence event.
The supplied `observed_through` must also cover the timestamps of all
predictions already handed to the evaluator. A recorded later emission paired
with an earlier completion watermark is explicitly censored rather than
silently accepted as complete.

The evaluator validates truth only at finalization. Positive truth may include
the actual target time in `[t_evidence,t_deadline]` when available; if it is
unavailable, the positive/negative confusion outcome is still scored normally.
Negative truth has no target time, and supplying one is rejected. Truth cannot
affect mapped records. A lead time is reported only when nonnegative; its
signed companion remains available for late/negative timing.
`deadline_lead_time = t_deadline - primary_time`;
`target_relative_lead_time = target_time - primary_time` only when both an
actual positive target time and a primary output exist. Target-relative
unsigned and signed values are `None` when the target time is unavailable.
Absent or negative unsigned leads are also `None`. Trial records keep signed
offsets and primary timing. Aggregate metrics report conditional sample
counts. No reward/efficiency penalty formula or optimization is added.

`aggregate_metrics` contributes exactly one cell per complete trial and
excludes all incomplete trials. It reports TP/FN/TN/FP, positive and negative
denominators, balanced accuracy, TPR/FNR/FPR, and separate premature, late,
silent-miss, out-of-window and duplicate counts. A zero denominator yields
Python `None` for the undefined rate; it is never represented as a fabricated
zero or perfect score.

## Fixture coverage and observed verification

`tests/test_luna60_task_output_interface.py` uses handcrafted immutable
emissions only as labeled evaluator-boundary unit fixtures. It also obtains
an actual canonical emission from `MultiExcursionNeuron("destination")`
through the delayed internal event queue, then maps that returned record.
The A–Z classifier is not instantiated or called.

Coverage includes:

- on-time positive, missed positive, correct negative silence, negative
  false positive, premature, late, duplicate and ambiguous-prefix cases;
- evidence/deadline equality and `t_close` equality;
- complete versus censored silence, plus pending/truncated/overflow censoring;
- first premature output followed by an on-time duplicate; first late output
  followed by later late outputs; duplicate cannot alter the primary;
- non-designated source/type filtering and signed-payload independence;
- identical mapped prefix records under truth swap, with evaluation outcomes
  changing only downstream;
- same-ID exact re-observation, conflicting canonical content, collision-safe
  identity construction, equal-time source-sequence ordering, order rejection,
  reset isolation and identifier/window/capacity validation;
- balanced metrics and N/A zero-denominator rates.

**OBSERVED:** adapter-enabled/disabled executions of the real delayed neuron
fixture produced identical canonical emission records and final neuron,
pending-event and queue state. The enabled case added only the external task
record. Routing and native prediction/error/eligibility/reward state were
not exercised and are **N/A**, not claimed as tested.

**OBSERVED:** identical canonical fixture inputs yielded identical task
records when positive and negative truth were swapped. Only external scoring
changed. No neural labels or outcome values enter `map_emission`.

## Order constraint discovered during verification

The requested phrase “first late output followed by an on-time duplicate”
cannot occur for one source under the frozen semantics: a late event has
`prediction_time > t_deadline`; a later canonical emission must have
nondecreasing time, so it cannot be on-time (`<= t_deadline`). The evaluator
preserves the explicit canonical-order and timestamp rules: it counts later
late emissions as duplicates and rejects an out-of-order earlier on-time
record rather than reordering or rescuing the primary.

This is an **INFERRED contract-fixture incompatibility**, not a neural
primitive blocker. **Independent Luna-0 disposition: PASS.** The proposed
late-then-on-time sequence is impossible in a valid same-source canonical
stream with nondecreasing timestamps. Rejecting its inverted-order record as
an invalid-order fixture is the accepted behavior; it is not an unresolved
requirement. The implementation does not weaken canonical ordering to force
that sequence.

## Behavior, architecture and promotion boundary

- **Changed:** four owned files add this downstream adapter, evaluator,
  fixture tests, interface documentation and handoff.
- **Unchanged:** canonical emission generation/identity/time, neuron state,
  runtime event ordering and routing, native numeric prediction/error,
  actual-emission eligibility and existing reward semantics.
- **Preserved:** A01–A08, A11 and A14–A15 behavior; A12/A13 remain optional.
  No architecture-contract clause or ACP is amended.
- **Not claimed:** scientific target construction, task values, data
  population/splits, efficacy, trained learner, benchmark, physical-energy
  result, hardware equivalence or A01–A15 promotion.

Passing these synthetic interface fixtures is not a task study and does not
authorize generator/dataset production, parameter selection, efficacy,
training, reward changes, omission/silence credit, duplicate penalties, ACP
work or architecture promotion. Stop for independent Luna-0 review.
