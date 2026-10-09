# Luna-62 — Bounded sequence-memory architecture proposal

Date: 2026-10-09. Documentation/design only; no mechanism executed.

**Disposition: BOUNDED SEQUENCE-MEMORY ARCHITECTURE PROPOSED — ACP REQUIRED**

Recommendation is not adoption. Independent Luna-0 review of these exact two
deliverables is the next gate, before any ACP or implementation decision.
No ACP is drafted here; no Luna-63 or other successor is authorized.

## 1. Authority, evidence discipline and verification limits

The entire assigned `.github/agents/luna-62.agent.md` and the 1,343-line
read-only user attachment were read in sections. The committed contract
prevails. The committed contract permits edits only to this report and
`workflow/handoffs/luna-62-sequence-memory-architecture.md`. The owner
authorizes publication of those documents by the parent orchestrator, but
not workflow/changelog edits outside the contract's two-file ownership.

Authoritative starting baseline:
`362282e1871fc46037d83bed4ed99d66fb5e796b`, clean fetched `main == origin/main`.
**OBSERVED by the parent orchestrator:** `git fetch origin`, ref comparison
and worktree status establish clean synchronized `main` at that exact SHA.
The worker performed read-only source inspection and authored the two
documents; the parent performed Git object, scope and whitespace checks.

Actual authorization identity supplied by the caller:
`084033b03968c256dc47c8d24fbafa56f085b729`.
**OBSERVED corroboration:** `.git/logs/refs/heads/main:57-58` records that
authorization followed by the starting publication. The existing Luna-0
authorization handoff instead writes
`084033b3b69ad821fb71326ec1507125cd43a9c5`. The discrepancy is recorded
additively in the new handoff; neither historical record is changed.
The parent ran `git cat-file -e '<SHA>^{commit}'` for both identities:
the actual commit resolves (exit 0), while the recorded identity fails
resolution (exit 128) in this fetched checkout. Ancestry of the actual
authorization commit is verified. The historical handoff remains unchanged.

Preserve the prior review caveat:
**Luna-61 design publication: ancestry verified in the preceding governance
record; independent PASS: conversation-provided, not tracked-verified.**
Luna-0's authorization handoff explicitly records this limitation.
The local reflog corroborates design/publication identities
`79aa0a053061e545669cea71aa8342a52f0e533e` and
`694b34e0e80af21f89547d1124315ef8913fce35` at lines 55-56.
The parent also verified Luna-61 publication ancestry (exit 0). No separate
tracked independent Luna-61 PASS artifact was located in this assignment.
This does not reopen Luna-61.

Throughout: **OBSERVED** means read source/document content; **INFERRED**
means interpretation of those interfaces; **HYPOTHESIZED** means proposed,
unimplemented behavior. No static source inspection is a passing runtime test.

### Evidence register

Line references below refer to the inspected files. The parent resolved
their exact Git blobs with `git ls-tree HEAD` at the starting baseline.
The following six pins also match the historical pins reported by Luna-61
at `ae4f183bd9ffa8ecaae082087aba32cab9d72fe3`.

| File | Verified starting-baseline Git blob | Inspected current evidence |
|---|---|---|
| `tpcn/event_runtime.py` | `f4aacb5d782f19e30fd9e562d56d62faefa9002f` | 26-88: categories/identity; 91-180: local clock, bounded queue and destination-local external-before-internal ties; 181-300: propagation and bounded execution |
| `tpcn/excursion_neuron.py` | `c0bdece6b15009db4e2b7d69c3242be174b5de80` | 60-160: optional integration/configuration; 225-350: provenance, pending work, canonical emission and scalar state; 371-499: reset and numeric external handling; 530-660: pending validation and ordinary emission; 678-782: scheduling/decay/provenance; 847-1090: E2 identity limits, positive representable scheduling, M replay-like excursions and return |
| `tpcn/experiment_excursion_runtime.py` | `b4e074f0139f3fcfb59189c8313c934c551d6bcb` | 44-170: sidecar and finite capacities; 272-390: character start/reset; 422-524: scalar admission/watermark; 525-671: emission consumption, observer, prediction, eligibility, readout, routing; 739-875: settling, first-readout reward and destruction |
| `tpcn/topology.py` | `98035a7657ec94d6e43fdcc0a648711284514907` | 28-107: finite positive delays and budgets; 175-285: admission and complete-fanout capacity preflight, Model-B transfer and preserved identity |
| `tpcn/eligibility.py` | `57b9f186c1332de6a9fc2759237184fb809ad4f5` | 34-139: activity/reward IDs and bounded ledger; 145-230: decay, activity accumulation, matching, bounded reward retry deduplication |
| `tpcn/streaming_classifier.py` | `99472550cd2c1a734eeba86b0047688b0fbea8e8` | Historical pin only; classifier use directly inspected at runtime 609-631 and 771-783; not separately reread here |

Additional actual source reads:
`tpcn/predictive_coding.py:1-300` (numeric keyed prediction, consumption on
observation, expiry and error); `tpcn/canonical_neuron.py:1-155`
(legacy bounded scalar dynamics, not a new sequence mechanism);
`tpcn/energy_utility.py:1-150` (local proxy units and stable reward identity);
`experiments/task_output_interface.py:1-160` (downstream binary mapping,
finite metadata bounds; no scheduling).
The parent resolved these additional pins:

| Source | Starting-baseline Git blob |
|---|---|
| `tpcn/predictive_coding.py` | `8c391703bb2361c77fc768407eb343da73677166` |
| `tpcn/canonical_neuron.py` | `b403fbc8c07d13600c6476e92652873707acea28` |
| `tpcn/energy_utility.py` | `3e563c31f2ac564e608b8c9487989f17ef5eea96` |
| `experiments/task_output_interface.py` | `52a0cec30e9d0e5bb5070d95c407f92db2289a77` |
| `.github/agents/luna-62.agent.md` | `e7d5d63792bc4b1cc12c7865d9a90c706fe54040` |
| `workflow/ARCHITECTURE_CONTRACT.md` | `3afc85f86dbc6992e01cb7ca26ebadfb49c09cab` |

Governing ACP and workflow source identities are pinned in the handoff.

Governing reads: full architecture contract v1.2/A01-A15; current relevant
Luna-62/61/60 status sections of changelog and Luna workflow; acceptance
criteria; ACP process README and template; full agent handoff template;
complete Luna-61 contract, design and handoff; Luna-62 authorization;
Luna-60 contract/interface/completion and owner/task-output governance.
Applicable ACP evidence: ACP-0002 Model-B transfer, ACP-0004 canonical
state/emission semantics, ACP-0005 IR-2 scope, ACP-0006 §§1-17,
ACP-0007 bounded opt-in structural observation, and complete ACP-0008
opt-in slow state. Historical ACP problem statements are not descriptions
of today's implementation. Legacy examples do not amend the contract.

No requested named governing artifact was missing in the reads. There is no
known exact repository path for a separate Luna-61 independent PASS record;
its absence was reported by prior governance, not exhaustively searched or
proved in this session. The parent completed the source identity and
documentation command checks; none is a behavioral or scientific result.

## 2. Architecture gap and question

**OBSERVED:** Luna-61 defines truth independently as the externally presented
LISTEN sequence, including repetitions, and prefers one canonical output
source per symbol. Its central missing behavior is
`LISTEN -> silent DELAY -> genuine RECALL -> ordered output`.
Current runtime accepts scalar contributions at one configured destination.
Non-INTERNAL events, including CONTROL, are numeric contributions to the
excursion neuron, not recognized recall commands. Scalar `x`, optional `z`,
mode and one valid pending internal event do not constitute an explicit
symbol/position store. E2 can emit multiple excursions, but a repeated
excursion is not evidence of the right repeated symbol at the right position.

**OBSERVED:** bounded provenance records event IDs/contributions and
episode/lineage information; it can truncate. It does not decode symbols or
select successive recalled occurrences. Runtime causal-root/path metadata
can affect bounded routing and error delivery; such guards are computational
scheduler state, but they still do not supply symbolic storage/replay.
Do not globally label every sidecar field “non-computational.”

**INFERRED:** generic event addressing, canonical output identities,
deterministic queue ordering and finite propagation are useful substrates.
They establish neither arbitrary bounded sequence retention nor recall.
A02 temporal noncommutativity is weaker than lossless bounded symbolic
sequence memory; recurrence alone also proves neither.

**HYPOTHESIZED leading answer:** `A -> C -> B` would physically reside in
three occupied registers/local RAM entries within a bounded computational
memory cluster: occurrence 0 stores A, 1 stores C, 2 stores B; occupied
successor relations are 0 -> 1 -> 2 -> none. During HOLD these registers
retain exact discrete codes, with an absolute finite expiry. An answer-free
RECALL arriving at that cluster in HOLD creates one token at occurrence 0.
Actual canonical emission of A, followed by output quiet confirmation,
permits the token to reach occurrence 1, then similarly occurrence 2.
The tail consumes the token and initiates cleanup. This is a specified
digital memory primitive, not a claim about existing neuron dynamics.

## 3. Boundary and candidate representations

The oracle alone may retain external LISTEN truth for evaluation. It never
supplies a pointer, symbol, length, next-step decision or completion command
to this computation. Task software must not keep a replayable answer list,
external answer FIFO, fixture feedback path or clocked shift register as
the neural solution. A trial/generation identity must not encode the answer.

Every exact representation must distinguish all ordered strings through K.
At length K the information lower bound is `K log2(V)` bits, excluding
length/phase/identity/safety overhead. Fewer scalar coordinates are not
automatically smaller once required precision, decoding and noise are counted.
No proof of globally smallest circuit is offered.

| Family | Representation M, length/head/end, and causal progression |
|---|---|
| Chained local memory cells | K indexed cells, each occupied with a symbol code; occupied prefix gives length/head/tail. Write token occupies next stage; RECALL reaches head; local emission completion activates successor. Separate occurrences preserve repetition. Functionally FIFO-like; allocation and completion still need explicit machinery. |
| Event-linked sequence chain | K computational records `(occurrence, symbol, successor)` plus head/tail/count; append on admitted event, replay token walks successors after completion. Original event IDs may accompany records but provenance itself is not reused as storage. Explicit linked queue; strongest inspectability, new computation. |
| Distributed temporal-state trajectory | Candidate bounded vector `h <- clip(Phi_dt(h) + B_symbol(h))`; M is h and a cue-gated decoder/trajectory. Length/end would need separate latent encodings. Noncommuting operators could separate AB/BA, but exact AA, arbitrary strings, delay invariance and replay decoding have no specified finite-precision mechanism here. Underdefined, not accepted as exact memory. |
| Local token/ring replay | K occupied ring slots, head/tail/count and one token; writes advance tail, RECALL enables head, completed output advances token until retained count/tail. Repeated symbols occupy different slots. Bounded asynchronous circular FIFO, with wrap/cycle and stale-token hazards. |
| Recurrent neural replay | Candidate bounded recurrent state h, event-triggered write operator, HOLD gate, RECALL release operator and positive-delay recurrent emission events; length/end must be latent or explicit. A concrete position-by-symbol one-hot h would use K*V states and collapse to chained cells with recurrence. A smaller emergent decoder is not specified; recurrence alone is weak evidence. |
| Conventional bounded FIFO reference | Array of K symbol codes, head/tail/count; enqueue during LISTEN, dequeue only after RECALL, terminate at empty. Fully specified engineering reference; oracle copy is external evaluation only. External FIFO replay cannot count as TPCN memory. |
| **Leading hybrid: local computational chain + replay token + isolated canonical output bank** | Fixed K local occurrence cells, occupied-prefix successor chain, bounded ingress arbiter and phase FSM, single token, V canonical output neurons, new computational emission/quiet bridge. Digital identity/order, existing scalar dynamics only for output transduction; optional analog evidence/gating later. |

### Complete qualitative capability/scaling comparison

“Specified” means design-level, not demonstrated. U = underdefined.
V = vocabulary size; K = `K_sequence`. Link/ID words have declared finite widths.

| Family | Identity | Multiplicity | Order | Variable delay / silence | Cue gating / sequential release | Event-driven | Bound/locality | FPGA | Analog/hybrid | State and routes scaling | Main risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Chained cells | code per cell | distinct cells | stage order | digital hold/TTL; gate required | head cue; needs emission completion | yes, local events | K; local neighbor links, ingress arbitration | registers/FSM good | digital slots; analog output possible | O(K log V) bits + O(K) flags/IDs; O(K+V) routed fabric or O(KV) direct symbol wires | actually FIFO; output coupling unspecified without bridge |
| Event-linked chain | code per record | occurrence IDs | successor invariant | exact digital hold to TTL; write/output gates | token follows completed emission | yes | K entries, local links; allocator can centralize | RAM/links/FSM good | digital links with analog transducers | O(K(log V+log K+b_ID)) bits; O(K) links; O(K+V) routed / O(KV) direct | treating audit history as computation; corrupted pointers |
| Distributed trajectory | possible in h, U decoder | U | noncommutativity insufficient | decay/noise changes code; U silence gate | U decoder, end and release | possible | bounded vector dimension D, locality depends on coupling | quantized vector/decoder expensive unknown | dynamics plausible, exact code fragile | O(D*b_precision) state; up to O(D^2+DV) routes; necessary D/precision vs K,V unproved | collisions, repeated inputs, retention and inversion |
| Token/ring | slot code | separate slots | ring head/count | digital TTL; output disabled | cue token; handshake per visit | yes | K ring stages; bounded wrap guard | excellent asynchronous FSM | digital ring; analog threshold/drive | O(K log V + K*b_ID + log K) state; O(K+V) routed / O(KV) direct | loop/wrap/stale token; FIFO similarity |
| Recurrent replay | U unless explicit position states | U unless occurrence states | U learned trajectory | attractor/HOLD retention unproved | recurrence/release/end U | possible due local events | finite N/events required | sparse recurrent machine possible, cost unknown | strongest dynamical promise, robustness unproved | explicit positional version O(KV) states/routes; generic N,b and dense O(N^2+NV) routes, K relation unknown | claims from recurrence without representation |
| FIFO reference | exact code | one enqueue each | enqueue order | digital TTL/gate | cue-enabled dequeue | asynchronous possible; global tick not necessary | K, usually central bounded port | excellent RAM/FSM | digital reference, analog peripheral only | O(K log V + log K) bits plus identity guards; O(V) ports/routed control | peripheral replay proves memory device, not neural capability |
| **Leading hybrid** | exact cell code | one cell per admitted root | occupied prefix | no decay of code; finite TTL; silent bank | genuine cue; **actual emission + quiet** gates next token | yes, no polling | one bounded local cluster, K,V and tree degree budgets | registers/RAM, token, routing trees, output FSM | digital exact order; analog accumulation/output under later tolerance contract | O(K(log V+log K+b_ID)+V*b_neuron+K visited bits); O(K+V) bounded-degree control fabric or O(KV) direct crossbar | new completion bridge, subsystem/peripheral status, exact-output assumptions |

### Scientific integration ranking and selection

From most dynamical integration to least: distributed trajectory and genuinely
emergent recurrent replay (tied aspiration, weakest specification);
chained predictive-neuron cells (integration unproved); hybrid/explicit
event-linked chain and local ring (general computational primitive, presently
peripheral subsystem); external conventional FIFO (reference only).
The explicit positional recurrent version is not scientifically “purer”
than a chain merely because its edges are recurrent.

For a first falsifiable design, rank correctness/specifiability, boundedness,
causal auditability, repetitions and exact order ahead of novelty:
**leading hybrid first**; plain chained cells/event-linked chain and ring
next (closely related engineering decompositions); trajectory/emergent
recurrent replay last until a decoder/termination mechanism exists.
The FIFO remains the simplicity reference, not a second recommendation.
For every explicit-slot candidate, full capacity must reject the next
distinct occurrence with a sticky overflow status; prefix replay, if proposed
as a diagnostic alternative, cannot masquerade as complete recall. Finite
expiry and bounded reset apply equally to chained cells, event-linked
records, ring slots and the FIFO reference. Distributed/recurrent candidates
have no proven exact representational capacity or collision detector here;
their overflow, expiry-safe decoding and reset guarantees remain
underdefined, not implicitly satisfied by clipping a state vector.

The hybrid's local identity/events and potential later prediction interaction
make it inspectable, not inherently neural. Future learning compatibility is
possible at interfaces, not evidence favoring a trained system.

Alternatives do not require stopping for an owner choice now: only the
explicit discrete family is sufficiently specifiable for the proposed
small mechanism boundary. Whether such a peripheral computational memory
is scientifically acceptable TPCN is for independent review and architecture
authority. No unresolved philosophical choice is resolved by implementation.

## 4. One leading candidate: bounded local computational chain

**All behavior in §§4-8 is HYPOTHESIZED, new design semantics.**
Scope: one active sequence in one finite local cluster; no concurrent trials,
multi-sequence address space, distractor learning or live checkpoint.

### Components and complete state classification

Fixed cells numbered 0 through K-1 avoid a dynamic allocator. A local arbiter
serializes append transactions. Cell placement and bounded routing are
configuration, not spatial-reservoir computation. “Local” includes only
this declared finite neighborhood, not unrestricted global scans.

| Field/component | Class | Why retained / bound |
|---|---|---|
| Per-cell `valid`, symbol code s in `[0,V)`, generation g, occurrence ordinal i, committed/consumed status | Computational | Determines whether/what can replay; K cells, finite widths |
| `next_valid`/successor index or tail sentinel | Computational | Determines next occurrence; fixed adjacent slot i+1 only, or none; checked against committed length |
| Arbiter phase `READY, LISTEN, CLOSING, HOLD, REPLAY, CLEANUP, FAULT_LOCKED` | Computational | Controls admissions/release/reset; finite enum |
| Committed occupancy n, head, tail, reserved next slot and one in-flight append descriptor `(root ID, symbol, i,g,subphase)` | Computational | Writes and completion; n<=K, at most one transaction; finite write/link/commit subphase; the descriptor is internal computational staging, not task buffer |
| Admission guard root IDs and their symbol-content consistency | Computational | Prevents fanout/retry double storage; bounded by K accepted roots plus one rejected-root latch; exhaustion faults, no eviction within generation |
| Replay token `(g,i,step,request ID)`, visited bitmap, completed count r | Computational | Controls future release/cycle bounds; one token, K bits, r<=n<=K |
| Pending request/source/episode binding, accepted emitted-ID guard, `seen_emission`, `seen_quiet`, per-step timeout | Computational | Completion deduplication and progression; one outstanding request/emission at a time |
| Local clock, absolute generation expiry, cleanup deadline, timer IDs, finite event/queue/route budgets | Computational | Expiry/cancellation and progress limits; finite time/ID/counter widths, no wrap in active generation |
| Generation counter and exhausted/wrap-lock flag; ingress-closed/drain/quiet state | Computational | Prevents stale generation effects and unsafe reuse; finite declared namespace |
| Output neurons' x/mode/pending/episode/generation/high-water IDs and optional z if separately enabled | Computational | Canonical output dynamics; existing E2 bounds; leading design keeps integration disabled |
| Symbol-to-output/source map, legal ports/routes, delay bounds, K,V, event budgets, ID widths | Computational configuration | Fixed independently; no answer lookup table; bounded nodes/degrees |
| Original LISTEN root ID used by admission deduplication | Computational | Identity guard affects admission, even if also copied for audit |
| Original timestamp/payload copy, origin-source audit copy, explanatory causal ancestry edges, trace of occurrence-to-output IDs | Provenance-only | Bounded audit sink; not used to choose symbol/order/timing or success; full sink cannot stall computation |
| Actual output ID used in completion guard | Computational | Acknowledgment deduplication; its separate audit copy is provenance-only |
| Observer capture ordinal and symbol record derived from actual source | Provenance/output observation | Downstream order evidence; never a replay cursor or next-step command |
| External truth sequence, expected count, evaluator deadline, edit alignment, scores and trial metadata | Evaluator-only | Independent oracle; no feedback route; does not count as memory |

No other retained sequence field is implicit. If future ancestry, audit
timestamps or observer state causally alter replay, they must be reclassified
as computation and reviewed; calling a field metadata does not exempt it.

### Conceptual messages (not new code/EventType definitions)

`OPEN`, `SYMBOL`, `WRITE`, `WRITE_COMMITTED`, `LINK_INSTALL`,
`LINK_INSTALLED`, `CLOSE_LISTEN`,
`RECALL`, `VISIT`, `OUTPUT_REQUEST`, `EMISSION_COMMITTED`,
`OUTPUT_QUIET`, `EXPIRE`, `STEP_TIMEOUT`, `RESET`, `CLEANUP_STEP`,
`DRAIN_CONFIRMED`, `READY_NOTICE`, `FAULT_NOTICE`.
These are proposed typed event-local transitions, routed with finite positive
delay where crossing components. Generic CONTROL can transport a record
to a new handler; today's numeric neuron handler cannot interpret it.
No control record or symbol code is passed as an excursion payload.

`EMISSION_COMMITTED` and `OUTPUT_QUIET` are **not existing canonical ACKs**.
They require a new reviewed computational bridge, separate from the read-only
Luna-60 observer. The bridge responds only to actual local output processing,
not evaluator success, expected length or collected answer. This addition
is a material part of the ACP prerequisite.

### Input acquisition, arbitration and write

1. READY has zero occupancy, no valid entries/token/append, drained scoped
   control channels and a quiet output bank. Answer-free OPEN establishes a
   fresh generation, LISTEN and an absolute finite expiry `t_open + T_TTL`.
   No generation is opened from evaluator completion.
2. SYMBOL is accepted only through one declared ordered local ingress.
   The symbol is a fixed port/source code, not a decoded numeric magnitude.
   Each independent original occurrence needs a stable, finite root ID;
   missing IDs, conflicting same-ID symbol content and out-of-domain codes
   fail explicitly. Two A presentations have different root IDs.
3. Order is **ingress admission order**, using timestamp plus canonical
   eligible queue order at that ingress. External LISTEN truth must map
   to that order. Equal-time symbols are all causally available before
   processing; tie order is fixed at admission. Unequal per-symbol paths
   can reorder arrivals: do not claim root timestamps repair this. The
   first boundary requires a single ordered ingress or equal-delay paths
   with a declared order-preserving transport. No evaluator reorder service.
4. Local arbiter reserves index n and sends WRITE to that cell. There is
   one outstanding append; later offered symbols receive explicit BUSY
   backpressure or bounded rejection, never a hidden task replay backlog.
   A future transport must establish the accepted-through watermark before
   releasing later input; it must not jump past unseen events. In the
   smallest boundary, offer the next occurrence only after local commit.
5. The cell retains its descriptor with a tail sentinel and sends
   WRITE_COMMITTED. For a nonempty prefix, the arbiter then sends
   LINK_INSTALL to the old tail, which verifies the transaction/generation,
   installs its adjacent successor and returns LINK_INSTALLED. Only after
   both acknowledgments does the arbiter publish committed occupancy n+1
   and the new tail; the first cell needs no old-tail link handshake.
   The cell's provisional validity is not replayable: HOLD cannot be entered
   with an append subphase outstanding. A partial link/write failure or
   transaction timeout invalidates the whole generation, not just the new
   cell. Arbiter/cell handshakes have finite timestamps, queue reservations
   and budgets. Cross-cell changes occur through events, not instantaneous
   writes to distant neurons.
6. Root-ID duplicates during LISTEN are computational no-ops after consistent
   content validation, including convergent fanout copies with different
   queue sequences. Fanout creates edge deliveries, not new occurrences.
   A duplicate of the currently reserved root shares that one transaction;
   it neither sends a second WRITE nor reports completion before commit.
   Accepted IDs remain guarded for the entire generation. Duplicate storms
   still consume event budget and can fault. During other phases a symbol,
   including an old duplicate, cannot write; its bounded rejection is explicit.

The arbiter has centralized control **within a bounded local cluster**,
not a global network controller. This trades biological distribution for
determinism. V input ports or K cells cannot directly exceed degree limits:
bounded-degree routing trees may be needed; all intermediate nodes/events
and route lengths must be budgeted. Internal input staging is declared
computational memory, not free adapter state.

### Close/HOLD, distractors and expiry

No event tells the system that “the last symbol happened” unless such an
event is supplied or a declared local protocol detects it. Silence alone
does not close LISTEN. Recommend an answer-free **CLOSE_LISTEN** cue after
committed input: it carries no answer, length or expected count. It is not
Luna-61's evaluator recall-close event and is not silently added to that task.
Its new network-facing phase meaning requires explicit architecture/task
approval. Luna-61 excludes hidden phase labels; this proposal exposes, rather
than hides, the additional control requirement. Without an approved close
protocol, phase-gated storage with vocabulary distractors is incomplete.

CLOSE_LISTEN disables new admissions, waits for the one reserved append to
commit, then establishes HOLD after bounded local link/count validation.
No pending-close symbol is admitted. HOLD's symbol codes/links do not decay;
elapsed time changes expiry validity only. No output request is legal.
Neutral/dedicated distractor channels route elsewhere or are explicitly
ignored by the memory gate. Vocabulary arrivals outside LISTEN cannot
overwrite a cell; they receive a bounded phase-rejection notice.

T_TTL is a fixed finite architectural lifetime for the **whole generation**,
including LISTEN/HOLD/REPLAY, not renewed by symbols, distractors or RECALL.
EXPIRE is scheduled locally at OPEN; handlers also check `t >= expiry`
before mutating, so same-time external-before-internal ordering cannot
extend life. Equality expires. Expiry faults/aborts and starts cleanup.
If execution stops, expired bits may physically remain until resumed, but
cannot compute after the deadline; re-arm requires actual cleanup.
Variable/longer delays are admissible only while the full replay can meet
this finite envelope. This is not indefinite retention.

### Genuine RECALL and output-dependent progression

RECALL carries only “begin recall,” arrives via a fixed bounded cue route,
and is accepted only in HOLD before expiry. It has no answer pointer,
symbol, output count, expected length or evaluator state. In LISTEN or
CLOSING it produces a bounded EARLY_RECALL rejection; it is not held for
later automatic release. In REPLAY, duplicate cues do not create tokens.
In empty HOLD, it produces EMPTY completion/control notice and cleanup,
with zero designated symbol emissions, not a synthetic symbol.

Accepted RECALL changes HOLD to REPLAY, freezes actual committed n and
creates the sole token at head 0. It schedules VISIT strictly in the future.
VISIT verifies generation, expected adjacent index, occupied/committed cell,
not-yet-visited bit, r<n and legal successor. It then binds one request to
that occurrence and routes OUTPUT_REQUEST toward fixed `OUT_s`.

The output bank is reserved for this subsystem in the smallest boundary:
V isolated `MultiExcursionNeuron` sources with no ordinary recurrent drive.
A local bridge converts the request into one predeclared numeric contribution
only when the addressed output neuron is quiet (N, no pending work, no active
episode, residual within a declared safe bound). A legal fixed drive must
analytically remain in the ordinary S-admission range for all allowed quiet
residuals: `theta_E <= |x + v| < theta_M`. Positive polarity and the same
policy across symbols avoid amplitude as identity. No numeric drive is
chosen from task performance here. If routed through Model-B, validate the
**post-transfer** contribution, not the pre-transfer value. This lawful-drive
configuration is a future prerequisite, not a forced emission guarantee.

Exactly one actual ordinary canonical emission must result. The computational
bridge binds the actual returned emission's source/episode/ID to the pending
request and sends EMISSION_COMMITTED back with finite delay. It does not
manufacture `ExcursionEmission`, reinterpret accumulator state as output,
or use the existing downstream observer to authorize computation.
An unmatched/second emission is an explicit fault, still visible to the
downstream observer; the evaluator cannot hide it.

The bridge also processes the output neuron's locally scheduled rearm work.
Only a verified transition to N with no pending event/active episode and
safe residual permits OUTPUT_QUIET for that request. This is a proposed
local transition bridge, **not an existing rearm callback/ACK API**.
Token advancement requires both correctly bound actual emission and quiet
confirmation; either arrival order is allowed, duplicates are idempotent.
If OUTPUT_QUIET arrives before EMISSION_COMMITTED, latch it and wait within
the same step timeout; message arrival order is not proof of omission.
The local output bridge may issue a successful quiet confirmation only after
it has itself recorded the request's actual emission. A locally quiet output
that never emitted reports failure instead; no token advancement.

Once both are accepted, mark the occurrence completed, increment r, and
consume its pending request. If successor exists, send VISIT to it with a
strict positive representable delay. At tail require r=n, consume token and
start cleanup. No expected output length, evaluator clock or observed answer
chooses the successor. n is computed from accepted writes, not supplied truth.
Waiting for quiet makes AA possible without merging both A drives into one
S episode, and prevents an M oscillation being mistaken for multiplicity.

### Failure, timing and budgets

There is no timer-only advancement. Missing emission, suppression, wrong
source/episode, unexpected extra emission, missing quiet, failed output
drive, queue overflow or a broken completion bridge causes timeout/fault.
No skip, retry emission, fabricated success or next-symbol release.
One finite STEP_TIMEOUT per outstanding request is fixed analytically from
declared route/emission/rearm bounds, not measured performance.
Failure may leave an emitted correct prefix; it is not successful memory.

Compare timing choices: same-time cascades obscure across-source order;
a local oscillator adds unnecessary state; state-dependent delays are lawful
but harder to bound. Recommend positive parameterized local handshake delays
for the future mechanism boundary. E2's existing rearm uses elapsed-time
decay; the bridge follows those events, not periodic polling.

For each scheduled transition at t require finite representable t' with
`t' > t`, including WRITE/commit, RECALL-to-VISIT, request/drive, canonical
emission, completion/quiet propagation, next VISIT and cleanup propagation.
Positive mathematical delay is insufficient if float addition rounds to t.
Reference design must validate the sum or use an explicitly declared
next-representable-time policy; no silent zero-delay fallback. Overflow to
infinity or exceeding expiry faults. FPGA time quantum/counter exhaustion
must have separately reviewed finite semantics. E2's narrow nextafter
S_REARM correction (`excursion_neuron.py:913-932`) is not a general bridge API.

Strict replay emission times follow `t_emit(i+1) > t_emit(i)` because the
next request follows actual emission and quiet completion over finite paths.
This avoids relying on incomparable source-local sequence counters.
Unrelated equal-time events still obey canonical queue ordering; only the
memory-generated order is claimed. No task-performance timing selection.

K alone does not bound duplicate/control storms. Declare finite per-generation
processed-event, queued-event, admission, route-depth and timer budgets,
including all intermediate tree nodes, output internal rearm events and
cleanup. Reserve control capacity for expiry/abort or use a separately bounded
fault latch/channel. Budget exhaustion is explicit incomplete/fault, never
quiet success. A failed cleanup budget keeps FAULT_LOCKED, not READY.

## 5. Formal invariants and hand-worked declarative examples

Let accepted distinct ingress occurrences be `e_0,...,e_(n-1)` with symbol
map sigma; the notation is explanatory, **not a software answer list**.
At successful HOLD:

- `0 <= n <= K`; precisely cells `[0,n)` are valid for current g.
- Cell i stores `sigma(e_i)` and occurrence `(g,i)`; each accepted root
  maps to exactly one such occurrence.
- Head=0 when n>0, tail=n-1; successor(i)=i+1 iff i<n-1, otherwise none.
  No predecessor field is necessary; adding an audit predecessor is
  provenance-only unless subsequently used by the computation.
- Phase gates imply zero designated replay output in LISTEN/CLOSING/HOLD.
  This is a required future property, not an evaluator output filter.

At successful replay prefix r:

- `0 <= r <= n`; exactly occurrences `[0,r)` have one matched actual
  canonical output each, with strictly increasing source emission times.
- The symbol at replay position j equals cell j's retained symbol.
- One token/pending request exists at r if r<n; no completed cell revisits.
- Distinct occurrences retain distinct request/output identities even
  when their symbols match. Fanout copies of one output ID are one emission.
- Tail completes only after r=n with the final actual emission and quiet;
  count/link inconsistency is a fault, not early success.

Inductive design argument: ordered append preserves the occupied-prefix
relation; HOLD makes no symbol/link writes; cue selects only head; each
completed output permits only the adjacent unvisited successor. Thus the
design would preserve order/multiplicity if the unimplemented write,
transport, bridge, quiet and isolation requirements hold.

The following are **hand-worked declarative examples**, not generated
fixtures, runtime traces, executed tests or observed outputs:

| Input | Hypothesized computational HOLD state | Hypothesized successful cue-dependent release |
|---|---|---|
| AB | `(g,0,A)->(g,1,B)->none`, n=2 | RECALL -> request 0 -> actual OUT_A/quiet -> request 1 -> actual OUT_B/quiet -> cleanup |
| BA | `(g,0,B)->(g,1,A)->none`, n=2 | OUT_B then OUT_A; differs from AB in computational codes, not only audit history |
| AA | `(g,0,A)->(g,1,A)->none`, n=2, distinct roots/requests | two separate OUT_A IDs and episodes after quiet/rearm, not one fanout emission |
| ABA | `(g,0,A)->(g,1,B)->(g,2,A)->none`, n=3 | OUT_A, OUT_B, OUT_A; first and last A are independently retained occurrences |
| ACB | `(g,0,A)->(g,1,C)->(g,2,B)->none`, n=3 | OUT_A, OUT_C, OUT_B only after RECALL; not possible at K=2 without overflow |

A single A uses one cell/request/output, not AA's two. The original LISTEN
root identity, occurrence `(g,i)`, request identity and canonical output
identity are distinct. The output's episode/lineage IDs remain neuron-owned;
do not overwrite them with a memory generation. A bounded separate mapping
relates them for audit and the pending computational completion check.

## 6. Capacity, overflow, end, cleanup and generation isolation

`K_sequence=K` is a symbolic finite occurrence capacity, not unique-symbol
capacity or a demonstrated reliable recall length. Candidate capacities:
2 suffices for AB/BA/AA; 4 admits ABA/ACB and length four; 8 increases slots,
link/visited/identity state, write/replay work and routing pressure. No
production value is selected and none is tuned from performance.

| Overflow option | Tradeoff |
|---|---|
| Reject K+1 and latch overflow, invalidate generation (**leading design**) | Never presents a retained prefix as successful full memory; loses otherwise valid prefix replay, simplest honest failure |
| Reject new symbol but allow explicit incomplete-prefix replay | Useful engineering diagnostic; must carry persistent failure status and cannot claim exact LISTEN recall |
| Explicit truncation with sticky flag | Deterministic but tests truncation, not full memory; keep condition visible |
| Backpressure until space | During HOLD-before-replay no space frees; indefinite wait is invalid. Would require a new streaming protocol, not this echo boundary |
| Overwrite oldest | Changes truth/order, destroys occurrences; silent overwrite rejected |

Leading behavior: no K+1 write, sticky CAPACITY_OVERFLOW fault, disable
RECALL and enter cleanup. A bounded control notice is non-symbol output
and not task success. If its channel is full, the latched failure remains
observable; resource fault cannot become silent success.

End alternatives: tail/no-successor is structurally local and independent of
oracle length; bounded count n is computational actual occupancy and useful
for safety; EOS takes capacity or requires a new semantic marker and can
be confused with a recalled symbol. Recommend tail/no-successor as primary
end, **cross-checked with actual n/r**. No output EOS symbol is needed.
The network's completion is distinct from Luna-61's fixed cue-relative
evaluator deadline; completion must not shorten the evaluator's window or
hide late extras. Evaluator truth length never tells the network to stop.

Cycle/broken-link safety: fixed adjacent successor indices prohibit cycles
by construction; HOLD validation checks each of at most K cells. At replay,
range/generation/valid/expected-index checks and a K-bit visited bitmap
detect corruption before requesting a repeated occurrence. Step count may
not exceed frozen n or K. Early sentinel, missing head/tail, duplicate
successor or successor outside occupied prefix faults. A finite TTL and
event budget independently bound a malicious/stale control-event storm.

Cleanup, on success, reset, expiry or fault:

1. Close ingress and disable all new writes/output requests; revoke token,
   append and completion bindings; latch outcome. RESET is an answer-free
   abort cue, never evaluator answer-dependent completion.
2. Cancel/invalidate this generation's local timers and control messages.
   Clear each of K slots/guards via bounded local CLEANUP_STEP events or a
   declared local RAM clear FSM; no global neural tick is needed. At most
   K cell visits, with fixed finite routing/ack overhead.
3. Quiesce/reset **only the reserved output bank** and invalidate its pending
   work through a reviewed local reset boundary. Existing whole-character
   destruction is not silently reused as a live selective flush.
   In-flight drives, completions, rearm and routed descendants must be
   accounted for, dropped with explicit counts or drained within the
   predeclared finite transit envelope.
4. If an old canonical output is already irrevocably committed, it remains
   observable. A late output during abort/cleanup is a failure observation;
   the evaluator cannot erase it. Completion of cleanup requires no pending
   drive/valid internal output work, each reserved neuron quiet, empty
   generation channels and zero occupied cells/guards. Failure to prove this
   by the cleanup deadline yields FAULT_LOCKED; no next sequence.
5. DRAIN_CONFIRMED is an internal transport/quiescence fact, not an evaluator
   report. Only then READY_NOTICE/re-arm. A later OPEN must obey this
   local ready protocol. READY implies zero occupancy and no valid prior
   token, request, append, output or in-flight event capable of acting.

Generation g uses a finite namespace; token/cell/request/control handlers
reject mismatched g. A generation tag alone is not safe on wrap.
Do not wrap automatically: lock on namespace exhaustion. Reuse requires
closed producer ports, a proven finite transit bound, drained/reset scoped
queues and emitters, and an explicit quiescent instance restart with a
fresh namespace or safe zero-in-flight wrap proof. If no such proof exists,
reuse is prohibited. Existing E2 high-water counters survive reset and
explicitly exhaust; do not reset them to fabricate fresh identities.
Delayed old ingress/control messages must be gated or drained at their
producer too, not merely removed from the consumer's queue.

The cleanup/drain protocol itself is new material semantics. No unlimited
waiting, unbounded ID retention or software-only infinite generation integer
is required by this design. Ordinary network events unrelated to this scope
must not be flushed; isolation is a prerequisite to this proposal's success.

## 7. Separate sequence capability accounting

| Capability | Leading candidate answer / limitation |
|---|---|
| Identity | Fixed addressed input code stored per computational cell; output fixed source map |
| Store | One admitted distinct root -> one committed occurrence via local write handshake |
| Order | Occupied-prefix adjacent successor invariant; only admission order, not path-reordered original order |
| Multiplicity | Separate cells/requests for identical symbols; output quiet prevents episode merging |
| Variable delay | Exact digital retention until absolute finite TTL; no indefinite retention claim |
| Silence while storing | Output gate/bank isolation; no request before RECALL, no observer suppression |
| Cue detection | New dedicated local handler; generic current CONTROL is insufficient |
| Replay gating | HOLD -> REPLAY only on genuine answer-free cue; early/duplicate cue bounded rejection/no-op |
| Sequential release | Actual matching emission plus quiet -> next VISIT; no time-only advancement |
| Output identity | Existing canonical source/event/episode/lineage retained; proposed separate binding |
| Completion | Tail and actual completed count agree; final emission/quiet consumes token |
| Finite capacity | K occurrence cells plus all explicit queue/event/ID/route budgets |
| Overflow | Sticky failure, reject K+1, no recall of a “successful” truncated prefix |
| Reset/re-arm | Bounded scoped cleanup, bank quiet and ingress/transport drain before READY |
| Ordinary interaction | Separate experimental subsystem; sharing bank or mutation is excluded initially |

## 8. Ordinary computation, FIFO role, prediction and credit boundaries

Classification: **separate experimental computational memory subsystem**,
not integration into predictive neurons and not generalized TPCN capability.
The digital chain is essentially a bounded asynchronous FIFO implemented
with local occurrence cells and a token. It is not a neural attractor.
That conclusion applies even though every transition is event-local.
An external answer FIFO would test task software replay instead of network
storage, so cannot satisfy the information boundary.

The scientific claim a later explicit internal chain could test is narrow:
TPCN-associated computational events can write a bounded local exact
identity/order store, maintain silent finite retention, and causally release
it into actual canonical emissions upon a cue. It would **not** show that
the current predictive dynamics learned or naturally provide memory.
Its engineering advantage is an inspectable baseline against which a later
dynamical mechanism could be compared, not the word “neural.”

Ordinary scalar activity, Model-B numeric transfer, predictor, eligibility,
reward and topology remain unchanged. No memory symbol code is routed as
numeric excitation or PredictionError. Memory control lives in an explicitly
bounded plane and cannot parasitize ACP-0007 observation or audit provenance.
Output sources are not classifier aggregates. If later ordinary activity
shares output nodes, it can trigger/merge/multiply excursions: such integration
needs new isolation, conflict and prediction semantics; initial design
does not assume it works. Structural mutation during an active generation
is excluded, so stored links cannot be retroactively rewired.

**Prediction queues must not be reused.** `LocalPredictor` retains keyed
numeric predictions, matches oldest eligible prediction on a later observed
numeric value, removes the matched record and computes observed-predicted
error (`predictive_coding.py:133-176,207-268`). It has no arbitrary symbolic
enqueue, HOLD, answer-free release, replay cursor or tail completion rule.
Using its records as a second FIFO changes ownership/expiry/error semantics
and does not solve recall by “reuse.” The event scheduler is also not a
persistent answer buffer; queue lifetime/time ordering is for pending causal
work, not stored sequences waiting for an unspecified cue.

Future possibilities only: recalled occurrences might drive delayed
expectations; actual subsequent observations could produce explicit mismatch
events; local learned input routing, cue discrimination, output coupling,
retention/gate parameters and prediction association are trainable surfaces.
No training design, teacher forcing, task credit, reward/penalty rule or
parameter selection is specified. Exact identity/order correctness initially
comes from the digital primitive, not learning.

Credit identities must remain distinct:

- Original LISTEN root: causally presented input identity, not a rewarded
  output. Deduplication prevents convergent copies writing extra cells.
- Memory occurrence `(g,i)`: computational storage/token identity, **not**
  an eligibility trace or native prediction ID.
- Replay canonical event: fresh actual neuron-owned output ID; a future
  authorized actual-emission ledger may address its existing trace.
- Routed fanout: same canonical output ID/lineage on every edge, separate
  arrival/queue sequence; do not create extra emission credit per copy.
- Repeated A: two output IDs because two actual emissions, not same-ID
  retries; bounded reward `message_id` deduplication is separate from
  symbol repetition and from occurrence deduplication.

Current activity recording can accumulate repeated trace-ID activities;
reward retry deduplication only guarantees bounded at-most-once application
for a stable message ID within one ledger window
(`eligibility.py:159-230`, A11). Multiple independent reward IDs and
multi-ledger copies are not global exactly-once credit. No automatic credit
transfer from replay to original roots, no per-edge duplicate reward and
no silent changes to error-delivery guards are proposed.
The runtime's observer runs before prediction/eligibility/routing consumption;
an observer notification is not an atomic success transaction across all
those consumers (`experiment_excursion_runtime.py:576-669`).

Preserve the missing-output/silence limitation: no actual emitted ID means
no existing emission eligibility for omission or correct silence. A memory
occurrence might someday represent an expected-output opportunity, but that
is a **future architectural possibility — not authorized**, not a trace
created here. Existing first-readout reward cannot align ordered sequence
loss or fabricate omission credit. Prediction/error/reward tests were not run.

## 9. Hardware and continuous-state concepts

FPGA qualitative mapping: K finite symbol/valid/generation/guard entries in
registers or small RAM; K visited bits; bounded head/count/request registers;
local phase/write/token/cleanup FSMs; timestamp comparisons; finite queues
and degree-limited routing trees; V ordinary output-neuron state machines.
Control routing may cost more than the symbol bits for tiny V,K. A direct
cell-to-symbol matrix costs O(KV) routes; routed addressing reduces static
fabric toward O(K+V) but adds hops, arbitration/queue cost and latency.
A centralized local RAM is physically simpler but less distributed; it
still must be explicitly owned computational state, not a task answer list.
No area, power, frequency or latency measurement/equivalence is claimed.

Single corrupted symbol/link can destroy exact recall. Range/index/generation,
visited/count/tail checks catch some corruption and bound consequences;
valid-but-wrong symbol corruption can evade them. This is not ECC, recovery
or fault-tolerant correctness. Failure latches should prevent endless token
circulation; no hardware fault test occurred.

FPAA/analog: local accumulation, decay, threshold admission, cue evidence
and excursion waveform generation are plausible analog responsibilities.
Exact occurrence IDs, arbitrary symbol order, repeated-symbol indexing,
tail/count checks, deduplication and safe generation wrap are better assigned
to bounded digital/event logic in a hybrid. An all-FPAA exact linked queue
mapping is not supplied. Under A15, pure-analog portability/precision remains
an architecture-review question, not a solved equivalence claim. A hybrid
division is plausible but does not by itself close every A15 realization.

WEMA could retain continuous evidence for cue confidence/readiness or local
activation; peak-hold/spike capture could retain magnitude/polarity or help a
later analog emission detector. Neither alone encodes AB versus BA and AA
versus A with arbitrary bounded replay. If continuous detectors control the
bridge, noise, spurious/dropped excursions, thresholds and event conversion
need a separately declared approximation contract. Initial exact reference
uses actual returned digital canonical emissions; it does not infer ACKs
from peaks or a timer. ACP-0008's optional z is evidence integration, not a
symbolic sequence memory, and remains opt-in/disabled by default.

## 10. Future falsification boundary — none executed

Future deterministic tests must inspect **computational** cells/gates/token,
not just audit ancestry, and preserve negative/fault outcomes. Fix all
configuration, identities, timings and budgets before execution; no
performance-derived choice. The independent oracle must have no scheduler,
memory, bridge or next-step write access.

| Future test/control | Required observation / result that falsifies the proposal |
|---|---|
| Separate A and B | Different retained codes and correct fixed source identity; amplitude-only identity fails boundary |
| AB versus BA | Computational occupied-cell contents differ with matched counts; genuine cue yields respective strict order. Only different provenance with identical effective state fails |
| A versus AA | One versus two committed occurrences and independent request/canonical output IDs; one output or fanout-copy counting fails multiplicity |
| ABA, later K>=3 | Two independently replayable A cells around B; unique-symbol set/count strategy fails |
| ACB, later V>=3 and K>=3 | A/C/B in that order after cue, silent during hold; initial K=2 must overflow, never appear successful |
| No RECALL, early and duplicate RECALL | No designated output without accepted HOLD cue; early rejected, duplicate does not create token or outputs |
| CLOSE/HOLD | No silence-derived close; CLOSE waits for pending commit; symbol after CLOSE cannot write; absent close cannot quietly recall |
| Variable/longer delay | Multiple predeclared delays below expiry retain same codes/order; expiry equality and beyond abort, no immortal memory |
| Neutral/dedicated and later vocabulary distractors | HOLD state unchanged except elapsed validity; no distractor overwrites or supplies answer |
| Capacity/overflow | Exactly K commits; K+1 faults/latches and suppresses replay according to policy; no silent overwrite/truncation success |
| Atomic fanout/convergent duplicates | One root -> one occurrence despite multiple queue copies; conflicting same-ID symbol fails; AA distinct roots stays two |
| Causal progression intervention | Removing first completion/quiet path prevents second request; removing cue path prevents first; timer alone never advances |
| Failed output and premature output | Suppressed/wrong/extra emission or missing quiet faults, no skip/retry; genuine pre-cue output remains visible failure |
| Strict representable timing | Near precision boundary reject/declared next-representable policy; each causal edge/replay emission strictly future, no infinity or same-time loop |
| Empty memory, symbol during REPLAY, repeated reset | Empty recall emits no symbol; wrong-phase writes rejected; reset aborts and only drained quiet state re-arms |
| Missing/broken head/tail/successor, corruption/cycle | Bounded validation/visited/count fault before repeated visit; no unbounded replay even on malformed links |
| Stale generation, delayed drives/completions and wrap exhaustion | Old events cannot act in new generation; no auto-wrap; unverifiable drain locks re-arm |
| Queue/event/cleanup exhaustion | Explicit incomplete/fault; no ready/success claim or disappearing late canonical output |
| Identical history repeat and truth-swapped oracle | Same computational state/actual trace; changing evaluator truth affects scores only, not admissions/replay |
| Observer on/off or full audit sink | Same computation, output times, IDs and budgets; audit cannot backpressure or select replay |
| Ordinary runtime non-interference outside scope | Existing predictor/error/ledger/reward/topology semantics remain unchanged; isolation boundaries demonstrable |

Smallest future mechanism-only boundary for consideration **after review,
ACP and separate authorization**: V=2 (`A,B`), K=2, one ordered ingress,
one local arbiter, two occurrence cells, one token, explicit OPEN/CLOSE/RECALL,
two isolated canonical output sources and the proposed computational bridge.
No training, distractors initially, classifier, task efficacy or reward.
Declarative targets A, B, AA, AB, BA establish identity/order/multiplicity;
empty, early/duplicate cue, K+1 and reset controls establish bounds.
Exact event/state traces, including output quiet and cancellation, would be
required. No fixture, data or trace was generated here. ACB belongs to a
later separately authorized K>=3,V>=3 boundary, not an impossible K=2 trial.
Logical numeric delays, TTL, budgets and lawful output drive are unfrozen.

## 11. A01-A15 and ACP assessment

| Clause | Compatible design intent / tension / future gate |
|---|---|
| A01 | Every transition has a causal input or locally scheduled due event; no global neural tick/polling. New control handlers need governance |
| A02 | Finite persistent local discrete state plus local elapsed expiry is permitted in principle; it is new state beyond canonical x/z and not already established memory |
| A03 | Positive finite representable intercomponent delay; ordered ingress and unequal-path effects explicitly bounded; no instantaneous remote link/ACK |
| A04 | K,V, cluster nodes, fan-in/out, queues, trees/routes and simultaneous requests finite; do not assume a V- or K-wide port fits existing degree limits |
| A05 | No spatial reservoir; placement implements proximity only |
| A06 | Memory is not predictive coding; existing numeric prediction/error remains fundamental and unchanged. Generalized predictive integration is unproven, not replaced by echo success |
| A07 | Local bounded acquisition/bridge; expected symbols/length and evaluator completion excluded; no training/global-state inputs |
| A08 | Token/visited/count/TTL/event budgets, representable time, explicit overflow and fail-locked reset; hardware ID/time widths and drain proof necessary |
| A09 | Local writes/reads/control/output activity could be metered later; no new accounting formula or physical energy measurement |
| A10 | No optimization for silence/low activity, no usefulness claim; fault/no-output is not efficiency success |
| A11 | Actual-emission-only eligibility and bounded reward retry scope preserved; occurrence IDs are not omission credit |
| A12 | No ten-pathway requirement; optionality preserved |
| A13 | This subsystem needs a phase/release gate; explicit learned gates are not imposed as a universal core requirement |
| A14 | Fixed memory wiring during active generation; no new evidence scorer or mutation. Future structural learning must respect local bounds and in-flight handling |
| A15 | Qualitative software/FPGA/hybrid feasibility; exact all-analog mapping and precision unresolved; no hardware equivalence or complete portability assertion |

Compatible interface/configuration work could include fixed source-to-symbol
mapping and a truth-blind sibling downstream collector, subject to separate
authorization. It cannot supply the missing memory. Current canonical
emissions and Model-B equations must not be altered or bypassed.

**An ACP is required before implementing this candidate:** persistent
order-bearing cells, occurrence/dedup state, CLOSE/HOLD/RECALL transitions,
token progression, computational emission/quiet bridge, scoped flush and
generation reuse materially extend existing state/event/composition
semantics. A02's permission for state is not authorization to introduce
this subsystem as an ordinary implementation detail. ACP-0008 similarly
classifies additional persistent state as architecture change; ACP-0006
shows that new composition boundaries may require an ACP even with
unchanged A01-A15 equations.

No existing ACP is amended, accepted, reopened or changed in status.
ACP-0007's non-interfering structural-observation plane is not repurposed
as the computational replay bridge. IR-2 is not a live memory checkpoint:
new cells/tokens/in-flight state cannot be silently serialized into it.
This report is the authorized design deliverable, **not an ACP draft**.
Future architecture authority must decide subsystem acceptance, additional
close cue, emission/quiet/reset ownership and A15 interpretation. Until then,
no mechanism implementation is authorized.

## 12. Non-claims, validation and disposition

Design alone establishes **no implemented or demonstrated recall ability,
task efficacy, measured capacity, generalization, learning, biological
memory, predictive-coding integration, calibrated energy or hardware
equivalence**. It does not prove mathematical minimality. Declarative examples
and proposed tests are not fixtures or measurements. No tests, code execution,
runtime, trials, data generation, simulation, scoring, training or hardware
validation occurred. The parent owns documentation publication; no ACP or
successor was created.

Read-only compatibility evidence supports proposing one explicit local
FIFO-like computational mechanism without claiming existing dynamics solve
the task. No inspected evidence materially contradicts Luna-61. Output
bridge/quiet/isolation and ingress/close/drain semantics are reviewable
design requirements, not present APIs or assumed successes.

Documentation validation performed: cross-check of candidate capabilities,
classification and clause boundaries against the inspected sources; manual
internal consistency and owned-path checks. The parent verified baseline
and authorization commit objects/ancestry, current source blobs, exactly
two new owned paths, and whitespace with `git diff --check` plus both
untracked-file `git diff --no-index --check` calls. No whitespace diagnostics
were emitted. These documentation checks are not mechanism tests.
The companion handoff records exact results and the authorization-pin erratum.

**BOUNDED SEQUENCE-MEMORY ARCHITECTURE PROPOSED — ACP REQUIRED**

Stop after documentation publication; then **independent Luna-0 review**
of these exact two deliverables. No independent review is conducted in Luna-62,
and no implementation, task study, training or Luna-63 follows automatically.
