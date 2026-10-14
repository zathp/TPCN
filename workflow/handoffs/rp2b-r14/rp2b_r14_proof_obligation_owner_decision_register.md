# RP-2B R14 — Proof-Obligation and Owner-Decision Register

**Status:** Static register; no new owner decisions or result semantics
adopted. The R14 prompt grants documentary review only.

## Owner policy directions

| Decision | Selected policy direction | Still not decided/adopted |
|---|---|---|
| OD-1 | All existing evidence families remain mandatory. | No family-level inventory details, widths, counts, optionality, or derived-representation exception supplied. |
| OD-2 | Preserve full-copy and recovery obligations. | No item-specific exclusion, reference substitution, or complete retention boundary supplied. |
| OD-3 | Sink A / Alert 1; existing-sink fail-closed limitation and attempt-level alert; preserve existing operator warning. | No independent observer/sink, receipt/durability guarantee, or complete attempt-evidence rule supplied. |
| OD-4 | Defer unresolved admission/refusal and incomplete-terminal decisions. | No universal result/precedence for novel candidate-limit, admission, reserve, partial-terminal, or alert-failure cases. |
| OD-5 | Preserve accepted Low bytes, grammar, ordering, framing, reconstruction and EOF behavior. | No new limits, encoding, accepted-set change, or recovery alteration selected. |
| OD-6 | Reaffirm frozen RP-2 profile for RP-2B. | No feasibility, capacity, host enforcement, or runtime qualification established. Phase 2A R2 remains inapplicable. |

## Proof obligations

| ID | Obligation | Status | Minimum closure evidence | Owner/policy dependency |
|---|---|---|---|---|
| P1 | Complete versioned mandatory-family inventory | **OPEN** | Every existing producer, field/schema, requiredness, count, width/escaping, conditional presence and canonical form reconciled. | OD-1/A means do not omit or invent details. |
| P2 | Finite `N_LOW` and `T_LOW` for all attempts | **UNSUPPORTED** | Whole-attempt count/byte proof covering startup, diagnostics, normal, malformed, EOF, partial and failure paths. | Must preserve OD-5/A; OD-4/C blocks unmapped new refusal. |
| P3 | Exact `LOW_BYTES` framing/transport bound | **PARTIAL** | Derive payload/framing/sequence/tick widths and prove complete source-enforced total, including failed/short writes. | No grammar or accepted-set change. |
| P4 | Full-copy and recovery accounting | **OPEN** | All raw/encoded/decoded/report/U copies, custody and required lifetimes. | OD-2/A disallows reference substitution/exclusions by inference. |
| P5 | Simultaneous-copy and transient lifetime peak | **OPEN** | Time-indexed concurrency/ownership graph including native buffers, snapshots, worker storage and serialization temporaries. | All existing mandatory copies remain included. |
| P6 | Partial-write/prefix/uncertainty accounting | **OPEN** | API-level accepted-prefix, uncertain state, chunk ownership, flush/close/hash/custody under failures. | No retries/fallback channel inferred. |
| P7 | Console/operator/governance material boundary | **OPEN** | Contract-required material, capture/durability boundary, schema, bounds and custody distinguished. | Preserve OD-2/A and OD-3 warning/Alert1. |
| P8 | Mandatory terminal evidence family maxima | **OPEN** | Joint per-path serialized maxima for P FINAL, O final, failures, cleanup, report, warning and all copies. | OD-1/A; OD-3/A; no new family omitted. |
| P9 | 131,072-byte reserve sufficiency | **NOT PROVEN** | Proof reserve is large enough for all jointly reachable required terminal records and cannot be consumed by payload. | No value inferred from constant or memory allowance. |
| P10 | Terminal admission/reachability | **NOT PROVEN** | State machine proves required terminal evidence can be admitted under existing behavior, or accurately records incompleteness. | Novel refusal/result mapping deferred under OD-4/C. |
| P11 | Sink failure and alert attempt evidence | **PARTIAL** | Trace writes/attempt and distinguish attempt, successful return, delivery, observation and persistence; assess actual available artifacts and later write outcomes. An individual failed write does not establish total sink unavailability. | Sink A / Alert1; D-RP2-OUTER-1 warning retained. |
| P12 | Frozen-profile resource feasibility | **UNDETERMINED** | Static bound/profile compatibility; any OS/runtime guarantees need separately authorized evidence. | OD-6/R-A; do not import Phase 2A R2. |
| P13 | P/O interface completeness | **INCOMPLETE** | Complete all external callers, producers, error/cleanup paths, writer/reader ownership, P→O contract and dependent files. | P/O remain candidate only. |
| P14 | Semantic preservation of candidate changes | **NOT PROVEN** | Exact old/new accepted-set and byte/output/result comparison for a frozen diff. | Any new rejection alters accepted behavior unless proven already disallowed. |
| P15 | Category I source allowlist | **NOT APPROVED** | Independent proof of complete patch surface, semantics, dependencies, exact diff and rollback. | R14 expressly cannot grant source allowlist. |
| P16 | Candidate O report/process-result consistency after finalization exceptions | **DISCREPANCY OBSERVED** | Establish contractual treatment and whether any later authorized correction is needed; candidate O can write the report at O:1033, then force the in-process verdict to UNKNOWN at O:1038 on a later finalization exception, without rewriting the report. | Source behavior is not contract approval; no correction or replacement outcome authorized. |
| P17 | Alert exception continuation | **UNGUARDED CALL SITES OBSERVED** | Determine by separately authorized future review whether exception-safe continuation and completion evidence are required; O:83–85 writes directly to stderr, and calls at O:1001/O:1038 do not guarantee continuation if it throws. | Attempt does not prove delivery; no alert-specific result adopted. |

## Values and established classifications

```text
frozen_total_max_bytes: null
proposed_total_max_bytes: null
proposed_headroom_bytes: null
```

Keep `RP2_UNKNOWN_FAIL_CLOSED` when required Low cessation evidence is
missing. Do not map an unadopted candidate-limit breach automatically to
`RP2_FAIL`. An alert attempt is not proof of delivery or persistence. On
total unavailability of the sole sink, persistence of its own failure record
cannot be guaranteed; an individual write failure alone does not establish
total sink unavailability. No numeric maximum, terminal reserve, headroom,
or fit is established by this register.

## Authority boundary

R14 authorizes only read-only review and session-state documentary
deliverables. It does not authorize source/contract changes, tests/imports/
compilation/preflight, runtime execution, a source allowlist, implementation,
staging, commit, push, merge, or publication.
