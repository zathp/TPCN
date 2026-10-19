# Luna-71B-C4.2-J — PPC-11 v1-to-v2 contract difference matrix

**Status:** Pre-implementation contract gate; candidate only.  
**Owner selections:** OD-J-1 through OD-J-6 in the project-owner C4.2-J
authorization.  
**Frozen baseline:** Published C4.1 PPC-11 at
`11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`; manifest SHA-256
`2f18d694784a6a583b0a7c01e6cc89f1313c2d65c7c6b5346a7cd4d993d3f1fa`.
The authoritative documents are `workflow/handoffs/luna71b-c4.1/02-ppc11-reconstituted-contract.md`
and `workflow/handoffs/luna71b-c4.1/05-paired-trace-schema-and-comparison.md`.

**I design identity:** Final manifest SHA-256
`1cc1f19b288c20601cfa7853382d0aff4f5b5392afbc8cc185ef0752b861b775`;
preserved Luna-0-audited candidate SHA-256
`c7deff6e407f5e3f8f19ace657bc3616d101420b2552a01303229fa078918b4c`.
All nine listed I documents match the final manifest's byte counts and raw
SHA-256 values. This matrix must be independently reviewed with the exact
v2 candidate before any v2-dependent implementation.

## Clause-by-clause matrix

| Area / v1 clause | Frozen v1 requirement | Proposed v2 delta | Classification | OD-J disposition / implementation boundary |
|---|---|---|---|---|
| Version identity | `ppc11-paired-trace-1`; one version per record; exact closed schema | New literal `ppc11-paired-trace-2`; version-specific parser and implementation identity | Additive version boundary | OD-J-1 permits v2 candidate. V1 remains immutable; mixed versions reject; no migration or projection. |
| Envelope and identity | Same source/runtime/fixture/exposure/parameter identities, side/run and contiguous record index | Preserve all v1 fields/meanings and require exact v2 implementation identity | Additive identity evidence | Authorized only as fail-closed diagnostic/preflight evidence. Does not claim historical R6 identity or replace missing hashes. |
| Number encoding and ordering | Exact typed numbers/bits, source order, no JSON model floats, no sorting/projection | Preserve the v1 encodings and ordering; tagged evidence values are added | No semantic change | Retain byte-exact values and P01-P11 comparison objectives. |
| Evidence-state algebra | Missing required data is incomplete; no missing-as-zero | Explicit `SOURCE_OBSERVED`, `DERIVED`, `NOT_APPLICABLE`, `UNAVAILABLE`, `COMPLETE_UNEXERCISED`, and `SOURCE_PATH_ABSENT` where applicable | Additive observability and terminology clarification | Allowed only if each state is source-grounded and cannot satisfy a required transition by itself. `UNOBSERVED` is used for P11 causes that cannot be observed. |
| P01 input events | Exact ordered event type, typed payload, timestamp, input order, channel and model-visible identity | No objective change; optional exact source locators | Additive evidence only | OD-J-1 and OD-J-6 allow passive fields; no event identity or input change. |
| P02 scheduler | Exact enqueue/schedule/dequeue/process order and source tie key | Capture exact source priority/tie key and admission reference where already exposed | Additive evidence / source-semantics clarification | No scheduling, sequence assignment, queue admission, or tie-break changes. Compare the existing P02 objective exactly. |
| P03 symbol prediction | Creation/identity, expected symbol, create/due, match, expiry, settlement/disposition | Preserve v1 `prediction_create` and its required `expected_symbol` for symbol-bearing predictions; add explicit source/derived evidence and prediction kind | Additive provenance | OD-J-2 explicitly permits derived values only with scalar, mapping identity/revision, value and provenance. A derived symbol is never called source-observed. |
| P03 mapping | V1 does not distinguish source-observed from derived symbol | `next-symbol-sign-v1`: `A` iff source scalar `>= 0.0`, else `B` | Clarification with provenance; acceptance depends on exact review | Implement only if Luna-0 independently verifies the source equation and the exact mapping/source revision is bound in the candidate. Preserve original scalar bits. |
| P03 nonsymbol prediction | V1 creation requires a nonempty expected symbol | Add `prediction_create_non_symbol` with source kind and explicit `NOT_APPLICABLE`; no fabricated symbol | Applicability change, expressly selected | OD-J-2 authorizes nonsymbol completion representation where source semantics establish it. It cannot stand in for settlement. |
| P03 settlement | Capture actual match/expiry/settlement; absent evidence is incomplete | Capture only source-reached settlement transitions; record missing source path as `SOURCE_PATH_ABSENT`/incomplete | Additive capture; no new model transition | OD-J-2 and OD-J-6 prohibit fabricated settlement or any new settlement behavior. P03 remains incomplete where source lacks the transition. |
| P04 omission | Origin prediction, omitted symbol/time, route, payload/event, delivery | Link pending prediction, external deadline, error, existing event/lineage, each route attempt, P02 admission/rejection, delivery/integration and observed duplicate/rejection result | Additive passive evidence; outcome decomposition clarification | OD-J-3 authorizes the minimum passive hooks. No label/evaluation access, new model ID, autonomous silence detector, route retry, or queue behavior change. |
| P04 cause | V1 needs delivery/outcome; absent evidence blocks | Capture actual cause only where source exposes it; otherwise `UNOBSERVED`/`UNAVAILABLE` | Clarification of evidence state | Do not infer internal route or rejection causes from generic exception or absent output. |
| P05 readout feature | Exact decision-time scalar bits | No change | None | Preserve v1 requirement and ordering. |
| P06 readout competition | All four affine drives, activations, candidates/winner, ties and tie-break | No change | None | Preserve exact bits and order; no readout alteration. |
| P07 eligibility | Creation/value/owner/expiry/consumption/capacity/admission/rejection | Optional source-state locators only | Additive evidence only | No eligibility, feedback, capacity or update behavior change. |
| P08 feedback | Identity/origin/schedule/due/application/order/sign/magnitude/duplicate/rejection | Optional source-state locators only | Additive evidence only | No feedback or rejection behavior change. |
| P09 parameters | Initial identity and every ordered exact-bit transition/cause/final state | No reduction; optional existing event reference | Additive evidence only | No parameter, RNG, or learning change. |
| P10 output | Exact predicted class/time and every model-visible emission | No change | None | Preserve exact order, identity and content. |
| P11 Queue/admission | Occupancy trajectory, each admission, processed count, drops, overflow and failure result; C4.1 also requires the actual terminal boundary, timestamp, queue state and ordered pending keys | Capture actual operation and exception/failure identity where exposed; retain the already-required terminal boundary/queue evidence; priority remains captured and compared under P02 | Operation/cause additions are non-gating diagnostics; C4.1 terminal evidence remains mandatory | OD-J-4 authorizes passive capture. An unavailable new cause is `UNOBSERVED`; missing required C4.1 terminal evidence remains P11 INCOMPLETE. Never duplicate/redefine P02 admission outcomes or invent source values. No scheduler, queue, operation order, or termination changes. |
| P11 comparator and stops | Exact v1 P11 equality, first failure stop/alignment rules in frozen contract | Preserve the exact v1 P11 comparator and stop/adjudication rules; report added operation/cause/boundary diagnostics separately | No comparison or stop change | No new terminal-status enum, failure-matching category, stop condition, or parity gate from diagnostic fields. A substantive comparator change requires a separate owner decision. |
| Branch register | Frozen v1 conditional evidence states and outcomes; nine historical branches remain NOT_EVIDENCED | Retain v1 states; add v2 evidence locators without converting absence to zero | Additive evidence only | No branch is forced or relabeled. Keep historical identities and outcomes intact. |
| Source/runtime/fixture preflight | Exact source, runtime, fixture and independent parameter identities before comparison | Version-specific preflight rejects wrong contract/source identity and mixed schema | Additive guard | Keep historical expected identities unchanged; preserve 43fb…/0ad1… as unresolved. C4.2-N is separate lineage, never R6. |
| Comparison and reporting | All P01-P11 retained; exact, ordered, fail-closed; no projection | V2 fields appear in versioned reports with their evidence state and provenance | Additive reporting; acceptance effects as above | Every original objective remains. No arbitrary migration, silent defaults, broad projection, or neural inference. |

## Explicit exclusions

The I proposal's descriptions are not blanket authorization. The v2 candidate
does **not** authorize:

1. new prediction/settlement, omission, scheduler, route, queue, readout,
   feedback, eligibility, parameter, or RNG behavior;
2. model-visible diagnostic identities or labels in computation;
3. new autonomous silence detection, deadline semantics, route retries, or
   queue-admission semantics;
4. inferred failure causes, synthetic settlement/terminal records, or
   replacing `UNOBSERVED` with a guessed taxonomy;
5. altered v1 comparisons, migration, projection, or changed comparator stop
   behavior; or
6. treating the unavailable historical 43fb… and 0ad1… preimages as
   recovered, incorrect, waived, or superseded.

## Gate disposition

The v1 contract remains frozen. Luna-0's final independent review found the
exact v2 candidate and reviewed source facts suitable for limited experimental
use, subject to formal owner adoption. The candidate is not adopted by this
handoff. The review confirmed the mapping identity/revision, selected P03
applicability distinction, passive-only P04 lineage/outcome observation, and
non-gating P11 additions without changing frozen v1 comparison semantics. If
a substantive change outside OD-J-1 through OD-J-6 becomes essential, stop
that part pending a separate owner decision.
