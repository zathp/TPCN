# Luna-71B-C4.2-J — Pre-correction Luna-0 review

**Review disposition:** BLOCKED. This records the first independent review
of the implementation bytes before the corrective pass. It is not approval
of later changes.

**Reviewed baseline:** J detached HEAD `e91818a5c974282e848dc43e52d3c0a534dcbf45`,
tree `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749`. No files were edited and no
tests or neural code were run by the reviewer. The reviewer confirmed all 80
J source-copy files and 12 PPC-11 implementation files against their
manifests, but could not independently verify the claimed 125-file H GN
inventory because `experiments/luna71b_c4_2/gn/gn-artifact-manifest.json`
was absent from J.

## Ranked findings

1. **End-to-end v2 path missing.** No production path constructed and bound
   `TraceWriterV2` plus `SourceCaptureV2` for both sides, dispatched the
   pair, and passed the traces to the v2 comparator. Existing source hooks
   and direct synthetic method tests did not establish integrated capture.
   The existing driver explicitly reports full-context dispatch as
   unimplemented.
2. **Comparator completeness was insufficient.** It treated a P03 match as
   resolving settlement, did not promote relevant `capture_gap` records to
   incomplete status, did not require route-result evidence for routed P04
   events, and did not enforce every mandatory terminal-evidence condition
   in the v2 candidate. The correction must preserve the owner-selected
   non-gating status of new P11 operation/cause diagnostics and the frozen
   C4.1 comparator semantics.
3. **Capture failures could affect execution.** `SourceCaptureV2.emit`
   synchronously called the writer; observer errors propagated through the
   execution path. The candidate requires writer failures to be reported by
   an independent supervisor/sidecar while preserving source result,
   exception, queue mutation, order, and termination.
4. **Trace comparison was not bound to preflight identities.** Syntactically
   valid trace source/runtime identities were not checked against the
   verified per-side J manifests before comparison.
5. **Derived-symbol validation was not fail-closed.** The validator accepted
   noncanonical mapping metadata and did not recompute the mapping or require
   the recorded scalar bits to match `predicted_value`.
6. **Provenance and v1 boundary claims needed qualification.** The GN
   artifact manifest was absent from J. The PPC-11 v1 contract/schema
   remained separately versioned, but the H-corrected `capture.py` and
   `driver.py` bytes differed from published C4.2 and were not the original
   C4.2 implementation bytes.

## Owner-policy and readiness findings

- OD-J-1: version separation was present in the schema design, but no
  end-to-end v2 execution/comparison path existed.
- OD-J-2: source mapping and nonsymbol representation were present, but
  derivation and settlement validation were incomplete.
- OD-J-3: passive omission hooks and a synthetic P02 linkage test existed;
  route-result completeness and runtime passivity were not established.
- OD-J-4: operation/failure and terminal capture fields existed, but
  mandatory terminal evidence and capture-failure isolation were unresolved.
- OD-J-5: unavailable historical preimages remained explicitly unresolved;
  no recovery or waiver was claimed.
- OD-J-6: the candidate prohibited fabricated outcomes, but the comparator
  did not reliably turn capture gaps into incomplete status.

The reviewer reported the v2 implementation/comparator as **BLOCKED**,
end-to-end static capture completeness **NOT ESTABLISHED**, and runtime
behavioral parity **NOT TESTED**. Neural execution and pilot remained
unauthorized. This record preserves the initial findings; a separate
post-correction review is required for the final bytes.

## Later clarification and correction boundary

In a same-review clarification, Luna-0 narrowed the P11 finding: the presence
of non-gating `execution_terminal` diagnostics is not itself a P11 gate.
Existing `terminal_state` fields and exact comparison remain the baseline.
The concrete issue was a null or stale `terminal_state.timestamp` at a
queue-failure boundary before any dequeue/process. The J corrective pass now
uses the observed failed/active event timestamp when available without
inventing a value or adding a new parity objective.

The corrective pass also supplied the missing J-side GN manifest,
implemented a synthetic-only injected v2 pair path, bound trace identities
to J preflight, corrected fail-closed completeness and derived-symbol
validation, and isolated capture-writer failures. Three obsolete P04 gaps
were suppressed only for the v2 source hooks that now capture the pending
prediction symbol, duplicate rejection, and existing lineage. Genuine P03
settlement and anomalous P04 route/admission gaps remain incomplete. These
corrections do not alter the historical review disposition; exact final bytes
require the separate post-correction review.
