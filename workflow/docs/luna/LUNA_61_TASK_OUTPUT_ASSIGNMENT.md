# Luna-61 — Delayed symbolic event-sequence echo design

**Status:** design prerequisite complete; independent Luna-0 review pending.
**Execution boundary:** documentation only. No task data, trials, scores,
training, runtime changes or efficacy results were produced.

## Decision summary

**Disposition: SEQUENCE-ECHO REQUIRES RECALL-GATING ARCHITECTURE DECISION.**

The task is independently definable: truth is the externally presented
LISTEN sequence, and a correct recall is exactly that sequence after the
RECALL cue. Event-driven input and canonical emissions provide useful
interfaces, but the inspected software reference has no symbolic sequence
buffer, sequence-position state, or cue-controlled replay mechanism.
Observed scalar state, bounded event provenance and recurrent routing do not
establish that arbitrary ordered symbols can be retained and emitted later.
The architecture's local state and recurrence provisions permit temporal
computation; they are not evidence that this task behavior is already
implemented or configured.

An evaluator could mechanically score a fixed output stream, but in the
absence of a predeclared input-to-output identity circuit and cue-responsive
sequence mechanism, a fixed/no-training task result would be technically
scoreable but arbitrary. No fixed evaluation is authorized.

The smallest next *decision* is an owner/Luna-0 architecture-boundary
decision on whether a bounded local sequence-memory and cue-gated replay
mechanism is an acceptable TPCN component, or whether the task must remain
blocked. This design does not specify or authorize its implementation.
Symbol-channel input adaptation, output identity mapping/collection and a
frozen deterministic fixture are subsequent prerequisites, not bundled
architecture changes. Training and task-level sequence credit are later,
separate governance questions.

## Task definition and information boundary

A trial has four logical phases:

1. **LISTEN:** Present an externally defined ordered sequence of symbolic
   input events. The network receives each symbol only when that event
   occurs. The LISTEN sequence is external task truth; it is never separately
   supplied as an answer or target to neural computation.
2. **DELAY:** After the final LISTEN symbol, wait a variable event-driven
   interval. Conditions may have no events, neutral timing events, or
   distractors. The expected recall remains the original LISTEN sequence.
3. **RECALL:** Present one explicit recall cue. This opens the task-output
   phase. Any designated sequence-output event before the cue is premature;
   the evaluator scores it and cannot suppress or delay it.
4. **RECALL OUTPUT:** The system should emit the original LISTEN sequence,
   preserving symbol identity, multiplicity and order.

Example: input `A -> C -> B -> D`; expected output `A -> C -> B -> D`.
Truth is determined before and independently of network execution. No trial
may be relabelled, selected, or omitted because of its output.

This is a symbolic temporal-recall task, not speech/audio processing,
classification, or a claim of human-like memory. There is no task training,
teacher forcing, reward or efficacy in this design.

## Proposed external event representation

**Proposed vocabulary:** `A, B, C, D`, subject to future task-contract
acceptance. Use fixed conceptual input identities `IN_A`, `IN_B`, `IN_C`,
`IN_D`, and `IN_RECALL`. These are design names, not current code channels.

`Event.source` and `Event.destination` are identifiers, but the excursion
neuron's external-event computation uses the numeric payload and does not
interpret source text as symbol meaning. The runtime's current convenience
input path admits numeric contributions to one configured `input_destination`.
Consequently:

- Distinct addressed input nodes can, in principle, provide identity without
  overloading signal magnitude or inventing payload-coded symbols.
- The current task input driver does not expose this multi-port symbolic
  interface; a bounded input-adapter/routing configuration would be needed.
- A future mapping from symbols to input destinations must be fixed before
  task trials. Symbol inputs should have matched numeric contribution and
  timing policies so magnitude or duration does not become an accidental
  symbol code.
- A generic `CONTROL` event exists, but the neuron treats every non-`INTERNAL`
  event as a numeric external contribution. `CONTROL` is not a RECALL
  semantic or a neural gate today. A distinct cue input identity can be
  delivered as an event; cue-responsive behavior is not thereby supplied.

Use a dedicated `IN_DISTRACTOR` identity as the simplest first distractor
stratum, explicitly outside the four-symbol target vocabulary. The
independently specified target remains LISTEN only. A later, separately
governed interference condition may present ordinary vocabulary symbols
during DELAY that are explicitly absent from the target sequence; this is
more demanding and must not be conflated with the initial dedicated-channel
control. A neutral timing event, if used, also needs a predeclared identity
and payload policy; no claim is made that a zero payload has useful timing
semantics in the current neuron.

**Input classification:** `EXISTING INPUT IDENTITY SUFFICIENT` in the
architectural sense that event addressing/topology can distinguish nodes;
the existing single-destination numeric task driver is insufficient and
requires an input-interface/configuration prerequisite. This does not imply
the network can store or recall the symbols.

## Architecture evidence and viability

Evidence is tied to clean baseline
`ae4f183bd9ffa8ecaae082087aba32cab9d72fe3`.

| Concern | OBSERVED repository behavior | Design assessment |
|---|---|---|
| Event identity and time | `Event` has source, destination, event type, payload, timestamp, optional identity and queue sequence. `EventQueue` is finite, orders by timestamp and deterministic queue sequence, and queues propagated events at finite delay. | Appropriate external event and ordering substrate; no sequence semantics are implied. |
| Symbol input | The generic event can address distinct nodes. `MultiExcursionNeuron.receive_event` treats `INTERNAL` specially and otherwise requires a real numeric contribution; it records event identity as bounded provenance. The integrated character runtime admits timestamp/value pairs to one configured input destination. | Separate addressed symbol nodes are a viable interface-level encoding; a task-specific input adapter is required. Source labels alone do not become neuron-visible symbol state. |
| Local temporal state | The excursion neuron has bounded scalar `x`, optional ACP-0008 scalar `z`, mode/episode/pending-event state and analytic elapsed-time decay. | Supports event-time persistence and dynamics, not a general ordered token store. ACP-0008 is opt-in experimental state and supplies no symbol identity or replay. |
| Provenance | Provenance entries retain input event ID, timestamp and numeric contribution in a finite deque and can truncate. They are diagnostic/episode bookkeeping, not used as a recall buffer or output-generation rule. | Must not be mistaken for symbolic working memory; capacity and content do not implement recall. |
| Recall cue | `EventType.CONTROL` is defined, but external neuron handling is numeric and event-category-agnostic except for `INTERNAL`. | The cue can be represented as an addressed event, but no cue-specific state transition, release gate or replay is present. |
| Output identity | `ExcursionEmission` carries canonical event ID, source-local sequence, source neuron ID, logical timestamp, numeric payload, lineage and episode identity. | A fixed source-to-symbol map could expose identities through distinct output nodes without coding symbol identity in amplitude. No such multi-symbol task mapping is currently governed. |
| Repeated output | E2 M-excursions can produce repeated emissions in one lineage while state remains above its threshold, with finite event/rearm behavior. | Repeated emissions are a primitive capability, not evidence they reproduce an arbitrary stored symbol sequence. |
| Cross-source ordering | The runtime processes a globally queued stream with deterministic same-time ordering; the emission observer is called in actual processing order. Per-neuron `ExcursionEmission.sequence` is source-local, not a global sequence number. | A future observer must assign a monotonically increasing capture ordinal in actual callback order. Sorting by timestamp alone or comparing local source sequences cannot resolve equal-time cross-source outputs. |
| Existing readout | The streaming A-Z classifier consumes signed numeric activity events, accumulates class scores, and returns one class at character finalization. | It is not a time-indexed sequence generator; repurposing it would conflate classification and recall and does not establish repeated ordered outputs. |
| Prediction | ACP-0006 prediction targets a later numeric observation at a configured numeric input port. | It is not symbolic sequence prediction or recall. |
| Credit | Eligibility is recorded for actual excursions; a reward/error addresses a trace or prediction ID. The integrated outer readout reward attributes to the first readout-source emission and is unmatched if there was none. | Existing semantics cannot credit an absent symbol or sequence omission, and do not assign an ordered multi-emission task loss. |

### Input identity, ordered storage and delay retention

Four identities can be expressed at the external event/topology boundary by
addressing four distinct input nodes. In the current integrated path, the
public input batch is numeric and directed to a single configured node; no
symbol-valued payload is accepted by the canonical excursion neuron.
Therefore identity is interface-representable, not already end-to-end task
supported.

The neuron stores scalar decaying state, optional scalar slow state, mode and
bounded provenance. It does not maintain a typed sequence, position pointer,
stack/FIFO, token identity array, or replay cursor. Provenance is finite
bookkeeping and may truncate; it does not feed the emission decision as a
symbolic sequence. A bounded recurrent topology can create delayed causal
paths and A02 allows persistent local temporal state, but no inspected
configured topology establishes preservation of both identity and order for
variable sequences or repeated symbols.

**Evidence strength:** event timing, finite propagation and scalar retention
are observed existing capabilities; ordered symbolic storage through delay
is not observed. Mechanism retention results from Luna-53–58 cannot be
promoted to symbolic sequence memory.

### RECALL cue and gating

An input event can carry a distinct external cue identity, and finite causal
routing can propagate it. Current neuron computation does not give `CONTROL`
or any other non-internal event special recall behavior; the payload is
numeric. No existing pathway has a governed rule “retain symbols, remain
silent, then on RECALL emit the stored sequence.” The evaluator cannot provide
that behavior by filtering premature events.

**Recall-gating classification: `RECALL GATING REQUIRES NEW ARCHITECTURE
PRIMITIVE` / owner architecture decision.** This is a statement about the
absence of an existing configured symbolic sequence store-and-release
mechanism, not a proof that no bounded recurrent circuit could ever encode a
finite task. A proposed mechanism must preserve A01 event causality, A02
local elapsed-time state, A03 finite propagation, A04/A08 finite topology,
state and event budgets, A07 locality and A15 hardware independence.
Luna-61 does not define its state model or authorize an ACP/implementation.

The current native predictor does not implement a recall trigger: it creates
numeric predictions from configured emissions and matches later numeric
observations. Existing excursion emission thresholds and rearm events are
also not conditioned on a `RECALL` identity. Merely injecting a control-type
event is not evidence of cue-gated emission.

## Output representation analysis

| Design | Existing primitives? | Repeated symbols? | Ordered sequence? | New semantics/prerequisite | Assessment |
|---|---|---|---|---|---|
| **A. One output source per symbol** (`OUT_A` … `OUT_D`) | Canonical emissions already expose source neuron identity, ID, local sequence and time; current configured readout sources are aggregated into a numeric classifier, not distinct symbols. | A source can emit repeatedly, including E2 multiple excursions, subject to its dynamics and finite bounds. | Actual global processing/capture order can be recorded; source-local sequence alone does not order different sources at equal time. | Predeclared source-to-symbol mapping, multi-source output observer/adapter, and a neural sequence-recall/gating mechanism. | **Rank 1 / preferred if later authorized.** Highest compatibility with event semantics, explicit identity, event provenance, label isolation and hardware channel mapping; lowest output-semantic novelty. It still lacks the required memory/gating mechanism. |
| **B. One source with payload-coded identity** | Payload currently represents numeric excursion magnitude/polarity; Model-B transfer transforms numeric signals. | Potentially, if a new symbol coding were defined. | Would need event ordering as above. | New governed payload schema and transfer/preservation semantics; may confound symbol with amplitude/energy. | **Rank 3 / not recommended absent architecture decision.** Fewer sources but new output semantics, decoder and payload-audit/hardware burden. |
| **C. Existing classifier-style readout** | Existing A-Z classifier consumes numeric emissions and finalizes one class per character. | It does not emit one symbol for each recall position. | It aggregates activity rather than producing an ordered output event stream. | Would require substantial readout behavior changes and entangles classification semantics. | **Rank 2 / unsuitable as-is.** More reuse in name than behavior; not an ordered task-output primitive. |

Option A is a design preference only, based on current event semantics. If
ever adopted, mapping `IN_A -> OUT_A` etc. must be fixed as a task
specification before trials, independently of labels or performance. The
neural mechanism must actually cause those output-source emissions after the
cue; the evaluator must not synthesize or relabel them.

**Multi-symbol output classification:** existing canonical source identity
can express distinct symbols if distinct output nodes and a fixed
source-to-symbol map are provided. That task mapping, multi-source observer
record and input/output wiring are not currently configured for sequence
recall, so an interface/configuration prerequisite remains. No new
payload-coded neural symbol field is justified by the inspected interfaces.

Minimum future output record:

| Field | Source |
|---|---|
| trial ID and recall-window ID | Frozen external trial controller |
| symbol identity | Fixed map from output source ID to symbol |
| canonical event ID, source ID, source-local sequence and timestamp | Actual immutable `ExcursionEmission` |
| capture ordinal | Bounded downstream observer counter, incremented in actual global emission callback order |
| output ordinal | Derived from capture order among designated outputs during the recall window |

Truth and expected output are not fields in the neural output record. Distinct
timestamps order by logical time. Equal-timestamp events use actual canonical
queue/observer order; do not infer a global order from each source's local
sequence. If concurrent outputs cannot be observed in canonical processing
order in a future backend, simultaneous cross-symbol outputs are ambiguous
and that backend/interface must define a deterministic ordering before use;
no artificial time step may be inserted by the evaluator.

Luna-60 remains a valid binary evaluator primitive and is unchanged. Its one
affirmative `destination` -> `target-before-deadline` record cannot represent
symbol identity at each ordered output position. Recommend a **generalized
sibling sequence-output interface** rather than changing Luna-60's binary
contract.

## Recall close, silence and scoring proposal

### Close rule

Use a **predeclared finite logical deadline relative to the RECALL cue** as
the external evaluator close rule. It does not depend on the expected output
length or the number of outputs, and the evaluator does not inject a
`RECALL_END` event into the network. The future task contract must choose
one finite duration before any task trials; Luna-61 selects no numeric value.
The runtime must provide an external completion watermark proving all due
events through the inclusive close time were processed. Budget exhaustion or
unresolved due work makes the trial incomplete/censored, never correct
silence. Work pending beyond the deadline is reported/discarded under an
explicit reset policy; no global tick or unlimited wait is allowed.

At the exact RECALL timestamp, canonical queue order decides whether an
emission preceded or followed the cue. An output before the cue is premature
even when timestamp-equal but ordered before it; after-cue outputs are
eligible. At the deadline, an output is included only if canonical ordering
places it at or before the inclusive close boundary.

Compared alternatives:

- **Explicit `RECALL_END`:** finite and event-driven, but adds another
  network-facing cue whose semantics and possible effect on recall need
  governance; it does not by itself define how long output was allowed.
- **Cue-relative finite deadline (recommended):** one evaluator-only
  duration, fixed before trials and independent of expected output length;
  compatible with event-time completion watermarks. Its value remains
  unselected.
- **Expected output length plus timeout:** may stop collection early, but
  makes evaluator termination depend on the externally held answer length,
  adds complexity for extra outputs and can risk answer leakage. Do not use
  it for the first design.

The deadline is an evaluator window, not a neural timestep. A later task
contract must also freeze how events beyond the close are handled at reset
so they cannot leak into the next trial.
The evaluator creates no silence event, reward, eligibility trace or neural
input before RECALL.

### Primary metric

For complete trials with expected sequence length greater than zero:

`exact_sequence_accuracy = exact_matches / complete_recall_trials`

An exact match requires identical output/target length, symbol at every
position identical, identical order and multiplicity, and no premature
designated output. A censored/incomplete trial has no accuracy cell; report
its count and reason and the complete-trial denominator. Do not silently
exclude budget failures and imply silence correctness.

### Secondary metrics (reported separately)

- **Symbol accuracy:** exact aligned target-symbol matches divided by target
  length, using the deterministic edit alignment below; no combined score.
- **Insertions/deletions/substitutions/order errors:** compute unit-cost
  Levenshtein alignment for insertion, deletion and substitution counts,
  with traceback tie-break `exact match`, then `substitution`, `deletion`,
  `insertion`. Levenshtein alone does not identify a transposition as one
  operation. Additionally compute unit-cost adjacent-transposition
  Optimal String Alignment distance, with traceback tie-break
  `exact match`, `transposition`, `substitution`, `deletion`, `insertion`.
  Report both the Levenshtein counts and OSA transposition count; label
  repeated-symbol alignments by this fixed algorithm rather than guessing
  intended edits. The OSA count is diagnostic and does not replace the
  exact-match primary metric.
- **Longest exact prefix:** number of leading positions matching before the
  first mismatch or end of either sequence.
- **Recall latency:** first eligible output time minus RECALL time; N/A if no
  eligible output.
- **Inter-output timing:** differences in logical time for consecutive
  eligible output events, including zero where canonically ordered
  equal-time events occur; report sample counts.
- **Premature outputs:** event and trial counts before RECALL, by LISTEN or
  DELAY phase; any such event fails exact sequence accuracy.
- **Extra outputs:** edit-alignment insertions. Repeated same-symbol outputs
  are not called duplicates merely because symbols repeat; they may be
  correct target multiplicity.
- **Duplicate capture:** repeated observation of the same canonical event
  identity is an interface integrity/duplicate-capture count, separate from
  task insertions.
- **Total output events:** actual designated canonical events by phase.
- **Energy/event proxy:** only if a later contract specifies a governed
  measure, units and limitations; no proxy value is selected here.

## Controls, candidate population and staged progression

**Smallest interpretable candidate first population (not frozen):** four
symbols and all 16 ordered length-2 sequences. This includes all four
repeated pairs (`A A`, `B B`, `C C`, `D D`) and every reversed pair, with a
predeclared short/long delay assignment crossed independently of sequence
identity. No distractors in the first stage. Replication count, actual delay
values, execution budget and comparator remain unselected. This candidate
tests identity, two-symbol order, repetition and waiting with a compact
balanced composition; it does not establish longer capacity.

Repeated-symbol and order-confusable controls address different shortcuts:

- `A A B` versus `A B A` has the same symbol set and counts but different
  order, so set membership and aggregate counts are insufficient.
- `A B C` versus `D B C` shares the final symbol (and suffix `B C`) but
  differs at the first position; a last-symbol-only state cannot distinguish
  the expected outputs.
- `A A B C` versus `A B A C` has matched counts and same first/last symbols,
  but different internal order.
- `A A` versus `A` (where a separately governed length-1 control is later
  included) distinguishes multiplicity from set membership. Length-1 is not
  part of the proposed first population, which begins at length 2.

Then consider, only after separate authorization:

1. Lengths 2-4, repeated symbols, matched-count order-confusable sequences
   such as `A B C`, `C B A`, `A A B C`, and `A B A C`.
2. Multiple predeclared event-driven delays, crossed/blocked across lengths
   rather than deterministically determined by length.
3. A dedicated distractor-channel DELAY stratum that is absent from LISTEN
   truth; later, ordinary vocabulary distractor symbols not in the target
   as a distinct harder condition.
4. Progressively longer sequences for an observed capacity curve and a
   separately reported maximum reliable recall length. Reliability
   threshold and population must be defined before observing performance.
5. Novel sequence-combination generalization. If any training or calibration
   is later approved, keep exact LISTEN sequences and their reverse/order-
   confusable mates within one partition; hold out novel combinations,
   repeated-symbol forms and order variants with composition balanced.
   Treat length generalization as a distinct held-out axis, not proof from
   novel combinations alone.
6. Phoneme-like symbolic inputs only in a later governed task, and real
   speech/audio front end only after separate acoustic-interface work.

All stages after design are **NOT AUTHORIZED**. Do not use fixed binary
target/deadline populations, Luna-12J labels, Luna-13C target arrivals, or
output-conditioned examples as sequence truth.

### Development fixture versus scientific fixture

Hand-authored miniature unit fixtures may later test record mapping and
metric edge cases; they are not a scientific population or held-out benchmark.
A scientific fixture must be independently specified, frozen, and pinned
before execution, including vocabulary, trial IDs, exact LISTEN sequences
and lengths, phase boundaries, event timestamps, delay/distractor schedules,
RECALL and close semantics, expected outputs, generator source revision and
Git blob/hash, deterministic seed if used, serialized event records and
train/calibration/test assignment. Preserve canonical LF/CRLF materialization
identity where applicable. Do not generate or publish any fixture here.

## Fixed behavior, training and credit

**Fixed evaluation classification: `FIXED SEQUENCE-ECHO EVALUATION
TECHNICALLY SCOREABLE BUT ARBITRARY`.** The external evaluator can compare
two sequences, but the repository does not provide a predeclared
symbol-to-output map plus a neural store/wait/recall sequence mechanism.
Choosing one after observing a result would be selection leakage. A future
fixed baseline could become interpretable only after its mapping, topology,
configuration, reset and recall behavior are independently justified and
frozen; this is not such authorization.

**Training viability:** existing learning components do not establish
trainability for this task. A canonical output emission has an identity and
can create an actual-emission eligibility trace. An actual wrong or
premature emission therefore has an event identity that a future governed
reward could address. But:

- a missing expected symbol or entirely silent sequence has no emission ID
  and no eligibility trace;
- correct silence before RECALL likewise has no event identity and needs no
  evaluation-time silence event;
- current local predictor targets numeric future input, not symbolic output
  sequence position;
- current integrated outer reward is attributed to the first readout
  emission (or unmatched when there is none); it does not score each
  symbol, order, insertion, deletion, or sequence completion;
- misordered outputs exist as emitted identities but require a governed
  alignment/position-to-credit assignment; current first-emission reward
  does not express it.

Future training may require task/recall-window identity, expected output
position, sequence-level opportunity/eligibility, and a principled
missing-output/omission representation. These are unresolved governance and
architecture questions. Do not create reward for correct symbols, penalties,
omission identity, sequence reward, teacher forcing, or supervised output
learning under Luna-61.

## Historical fixture suitability

- **Luna-12J (`tpcn/temporal_efficacy.py`):** fixed `a-first`/`b-first`
  examples reverse two numeric signed events and read a scalar target state
  to classify order. This is useful evidence that order-sensitive scalar
  fixture design exists, not a multi-symbol recall task, cue-gated replay,
  repeated-symbol buffer, or designated sequence output.
- **Luna-13C (`tpcn/causal_utility.py`, `tests/test_luna13c_causal_utility.py`):
  fixed external `on_time`/`late` targets are compared with the second
  target-arrival deadline decision under graph interventions. This is a
  small topology-utility/causal fixture, not a LISTEN sequence target or
  output-symbol stream.
- **Luna-60:** implementation and independent review remain valid for one
  affirmative binary `destination` output channel. It preserves event
  identity/time but cannot encode a sequence of distinct symbol identities
  by itself. Preserve it unchanged; a generalized sibling sequence-output
  observer/evaluator is preferable.
- **Luna-53–58:** mechanism studies of destination/relay integration,
  retention and discharge are not symbolic sequence truth, ordered storage,
  or RECALL behavior.

These assessments are conceptual read-only source inspections; no fixture
or runner was executed.

## Architecture impact and smallest next prerequisite

| Clause | Relevance / evidence | Status |
|---|---|---|
| A01 | External phases and output are events; evaluator must not add a global tick. | Preserved; no task runtime implemented. |
| A02 | Local state can persist/evolve with elapsed time, but observed scalar state is not an ordered symbol store. | Relevant; no conclusion that current state suffices. |
| A03 | Finite propagation and timestamps support causal delays and deterministic routing. | Preserved; no instant recall route. |
| A04 | Finite nodes/fan-in/out/resources bound any future input/output map and memory. | Relevant resource constraint. |
| A05 | No spatial reservoir is needed or proposed. | Preserved. |
| A06 | Existing prediction is numeric and cannot substitute for symbolic recall. | Preserved; no predictor change. |
| A07 | Expected sequence remains external evaluation truth; any learning/config initialization must not leak future answer. | Preserved; no learning. |
| A08 | Any future buffer/recurrent replay must be finite in state, queue, event and path budgets. | Relevant future acceptance gate. |
| A09-A10 | Energy is not scored or optimized here; later proxy requires governed units. | Not calibrated/changed. |
| A11 | Existing delayed credit supports actual addressed traces, not missing sequence positions. | Limitation documented; no credit change. |
| A12-A13 | Multiple pathways and explicit gating are optional, not assumed required. | Preserved. |
| A14 | Structural plasticity is neither required nor presumed to create sequence memory. | Not evaluated or changed. |
| A15 | Source IDs, bounded state and event timestamps are hardware-plausible abstractions, but no implementation/equivalence is assessed. | No hardware claim. |

**Smallest recommended next prerequisite:** project-owner/Luna-0 decision on
whether a bounded local sequence-memory plus RECALL-gated replay mechanism
may be designed within TPCN, including locality/reset/resource constraints
and whether it is an A02/A08-compatible configuration or a new architecture
primitive requiring ACP governance. Do not bundle its implementation with an
output adapter or task fixture. A separate output-interface/fixture
prerequisite follows only if that boundary is accepted.

No successor is authorized by this design. No Luna-62 is created.

## Architecture boundary and hardware relevance

The identity channels, output source IDs and finite timestamped records are
interface/routing configuration concepts; they do not by themselves change
neuron dynamics. A bounded input adapter and a downstream multi-symbol output
collector are interface-level prerequisites. A static one-source-per-symbol
map is a routing/configuration prerequisite if legal nodes and capacities
are independently frozen.

The missing store/order/replay-on-cue behavior is different: current
computation has no sequence-token store or recall gate. Placing a hidden
sequence list in the evaluator or task driver and replaying it would move the
answer outside TPCN and invalidate the challenge. A task-specific learning
rule alone cannot fix this representational gap, and current reward does not
provide sequence-position or omission credit. Therefore the immediate gap is
an **architecture primitive decision**, not a training decision.

In principle, source/channel identity, timestamps, local routing and an
explicitly bounded local sequence state are compatible with event-driven
FPGA/FPAA-style realization. A source-per-symbol design avoids a centralized
payload decoder. This is conceptual compatibility only: no cell/area/timing
budget, analog tolerance, mapped design or hardware equivalence was assessed.

### Required component matrix

| Component | Existing support | Gap | Smallest prerequisite | Architecture impact |
|---|---|---|---|---|
| Symbolic input identity | Generic events address named nodes; the neuron processes numeric payload locally. | Current task driver sends scalar values to one configured input destination. | Predeclare `IN_A`…`IN_D` node map and bounded multi-port input adapter. | Interface/routing configuration; no new payload code. |
| Ordered retention | Scalar local state, timestamps, bounded provenance and finite recurrent routing. | No typed sequence, multiplicity store or position state; provenance does not drive recall. | Owner decision on bounded local sequence-memory representation and reset/resource invariants. | Potential architecture primitive; design/ACP boundary must be decided. |
| Variable delay | Local elapsed time, exponential decay and delayed finite events. | No demonstrated preservation of ordered symbols across variable delay. | After memory decision, freeze delay strata independent of sequence length. | A01-A03 timing configuration plus memory-state decision. |
| RECALL cue input | Generic addressed event and `CONTROL` type exist. | Neuron treats non-internal events as numeric contribution; no cue meaning. | Predeclare cue input identity and causal route. | Interface/configuration only if used as input; not a gate itself. |
| Recall gating | Threshold emissions, pending events and rearm exist. | They are not conditioned on RECALL and do not release a stored sequence. | Owner/Luna-0 architecture decision for cue-triggered bounded release. | New task-relevant state transition/primitive unless an existing lawful circuit is specified. |
| Multi-symbol output | Canonical emissions carry source identity and timestamp. | No symbol-source mapping or sequence-output observer. | Freeze one source per symbol and a truth-blind output record/collector. | Downstream interface/routing configuration; avoid new payload semantics. |
| Ordered repeated outputs | E2 can emit repeated canonical events; runtime queue ordering is deterministic. | Source-local sequence does not globally order simultaneous distinct sources; no target-position scheduler. | Observer assigns capture ordinal; memory/gating mechanism produces actual order. | Interface tie-order plus sequence primitive. |
| Evaluator | Luna-60 has a bounded binary event-time evaluator. | It scores one affirmative channel, not sequence symbols/edit operations. | Generalized sibling sequence evaluator after output contract is separately authorized. | Downstream-only; do not break Luna-60 binary contract. |
| Fixed evaluation | External LISTEN sequence provides independent truth. | No independently justified input/output map or recall behavior in current setup. | Freeze behavior/map only after architecture viability; otherwise do not run fixed task. | Scientific interpretation gate, not an implementation primitive. |
| Training | Eligibility/reward can address actual emission traces; numeric prediction is local. | No symbol-position/sequence loss, no trainable recall mechanism established. | Separate future training design after behavior/output are defined. | Learning prerequisite; preserve A07 locality. |
| Omission/misorder credit | Emitted events have IDs; reward can address a trace. | Missing symbols have no trace; first-readout reward does not assign position/order; silence has no identity. | Govern task-level sequence opportunity/alignment/omission semantics if learning is later needed. | New credit/governance concept; not authorized here. |

**Architecture-boundary classification:** input mapping and a
source-per-symbol collector are interface/routing prerequisites; task
outcome learning is a separate learning/credit prerequisite; bounded ordered
memory and cue-triggered replay are the architecture-primitive decision.
These are causally ordered and must not be bundled into one implementation
dispatch.

## Evidence and limits

**OBSERVED:** source interfaces at the pinned baseline show numeric
excursion-neuron contributions, bounded scalar state/provenance, canonical
source-ID emissions, finite deterministic event routing, one-destination
numeric task input, classifier aggregation, numeric prediction, and
actual-emission eligibility/reward boundaries.

**INFERRED:** these existing primitives can support task input addressing
and source-coded external output records, but they do not by themselves
provide symbol-preserving ordered storage and cue-triggered replay.

**HYPOTHESIZED:** a bounded local sequence-state mechanism may be designable
within the architecture if an owner decision permits it; no behavior or
hardware realizability is demonstrated.

| Procedure | Result |
|---|---|
| Fetch, branch/HEAD/origin/status and amendment ancestry | **PASS** at `ae4f183bd9ffa8ecaae082087aba32cab9d72fe3`; clean `main`, amendment is ancestor. |
| Read amended Luna-61 contract, governance handoff, workflow/changelog and Luna-60 interface records | **PASS**; current selected task is symbolic echo, binary task retained as historical. |
| Read-only inspection of event/neuron/runtime/topology/classifier/predictor/credit and Luna-12J/Luna-13C code | **PASS** for design evidence. |
| Task data generation, fixtures, runners, simulation, training, scores, efficacy, hardware validation | **NOT RUN / NOT AUTHORIZED.** |
| Tests | **NOT RUN / NOT APPLICABLE** to documentation-only design. |

## Final disposition

**SEQUENCE-ECHO REQUIRES RECALL-GATING ARCHITECTURE DECISION.**
