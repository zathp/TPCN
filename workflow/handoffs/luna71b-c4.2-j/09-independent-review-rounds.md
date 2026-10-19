# Luna-71B-C4.2-J — Independent Luna-0 review rounds

## Review 1 — corrected J candidate before additional findings

**Disposition: BLOCKED.** This read-only review inspected the exact J
implementation report with SHA-256
`16ea9611a867d32eea6e05c0d5278e55f27128d0b790abcafe5f0aefaa25409b`
(18,571 bytes), implementation manifest SHA-256
`25b23d1dfa3dfb3f426021f5dc4446f4d6b78ea053fd77d2ebc133ee1fa90fd1`,
and J source manifest SHA-256
`605a730361da6252173d5466e11fa412ffdecca45c26ffabc31ca384b23d2ec0`.
J remained detached at published C4.2 commit
`e91818a5c974282e848dc43e52d3c0a534dcbf45`, tree
`f14f23f0eb00e8b4aa8946e34acc71ab46ab5749`. The reviewer made no file
changes and ran no neural code. Its independent identity preflight passed
and verified 125 GN artifacts.

### Ranked findings

1. **P03 lifecycle coverage was not evidence-bound.** The schema allowed
   `COMPLETE_UNEXERCISED` based on a caller-provided source-point claim, and
   the comparator could treat that state as resolving an unsettled prediction
   without proof of a verified completed exposure boundary.
2. **Compared traces were not bound to actual fixture inputs.** Fixture and
   initial-parameter hashes appeared in the pair result, but trace completion
   and comparison did not consume a sidecar or otherwise bind P01 input
   records to those exact frozen inputs.
3. **Source locators were function-scoped, not exact-callsite-bound.** The
   checked source hash, path, role, function, and AST span rejected external
   locations but permitted an arbitrary line inside the function.
4. **Process-control exceptions were caught as observer failures.**
   `BaseException` handling could swallow or delay `KeyboardInterrupt` or
   `SystemExit`, so passive failure isolation was broader than established.
5. **Parent handoff identities and test counts were stale.** The parent
   provenance and validation documents still referenced earlier J manifest
   identities and a 26-test count while corrected J reported 28 tests.

### Other reviewed dimensions

- OD-J-1 version separation and frozen v1 contract/schema boundary were
  statically conformant; pre-existing H identity-pinned overlays in
  `capture.py` and `driver.py` mean the whole C4.2 implementation is not
  byte-identical to published C4.2.
- OD-J-2 was partial due to the P03 coverage issue; derived symbol mapping
  and nonsymbol completion representation were otherwise supported.
- OD-J-3 conformed at static/synthetic level for pending-prediction
  provenance and label isolation; actual anomalous route/admission paths
  remain incomplete, and runtime passivity was not established.
- OD-J-4 was mostly conformant at static/synthetic level; mandatory v1
  terminal state remained gating and new diagnostics remained non-gating,
  subject to process-control exception handling.
- OD-J-5 preserved unavailable historical `43fb…` and `0ad1…` preimages as
  unresolved; historical R6 readiness remains blocked.
- OD-J-6 was partial because unsupported P03 coverage and missing
  trace-to-fixture binding prevented a full fail-closed conclusion.
- Runtime parity was **NOT TESTED**. The J suite's 28-pass result, GN
  authorized-H 14-pass result, and C4.2 three preflight blocks were reported
  by the implementation handoff, not rerun by this reviewer. The reviewer
  did not rerun tests because the test class setup removes the generated J
  artifact directory.

## Corrective status

The five findings above block adoption and static readiness until corrected
and independently reviewed. A bounded J-only corrective pass is authorized
by the owner scope: evidence-bound lifecycle coverage, fixture/input
binding, exact callsite validation, process-control exception preservation,
and reconciliation of parent handoff identities/results. It must not change
the contract or neural behavior, run a real-source pair, or execute training,
inference, or a pilot.

**Final independent review:** pending a fresh read-only review of the exact
corrected code and updated artifact manifest. Review 1 remains preserved as
BLOCKED and is not approval of later bytes.

## Review 2 — corrected J after final-review implementation pass

**Disposition: PASS WITH FINDINGS.** Read-only review of J report
`CORRECTIVE-PROVENANCE.md` (23,093 bytes, SHA-256
`90ed7b2f15fcc2738cb9b832c4899afd54654b58e35cce76ac73673ee1053a2e`),
implementation manifest SHA-256
`52892efc319dfa35ce3dbdedf25b16d4e03c70d5b4d34530cc37d126d7571463`,
and source manifest SHA-256
`605a730361da6252173d5466e11fa412ffdecca45c26ffabc31ca384b23d2ec0`.
J remained detached at the published C4.2 commit/tree. The reviewer verified
the identity preflight and 125 GN inventory. No neural code or tests were
run by the reviewer.

### Findings and disposition

1. **High — P03 settlement was not linked to its source lifecycle evidence.**
   V2 accepted a `prediction_settle` row by prediction ID alone, although
   the candidate requires the settlement source disposition and triggering
   record reference. A fabricated, dangling, or mismatched settlement could
   clear a missing-settlement gap. Correct this in J v2 only; do not change
   v1 or synthesize source transitions. Static PPC-11 remains not ready.
2. **Medium — stale parent handoff identities/status.** The review found
   outdated `driver_v2.py`, corrective-report, test-count, and pending-review
   references in documents 03, 08, and 09. Reconcile them to final corrected
   bytes while preserving earlier review records.
3. **Low — P11 non-gating diagnostic type validation.** Validate typed
   integer ranges and structures for processed count, occupancy/capacity,
   ordered pending entries, and queue snapshot. Keep these new diagnostics
   non-gating for parity.

### Assessment

- **V2 contract candidate:** suitable for limited experimental use as a
  versioned PPC-11 candidate, subject to explicit owner adoption; v1 remains
  immutable. This does not approve the current J implementation for a
  real-source pair or pilot.
- Trace-to-fixture binding, exact source callsites, unsupported
  `COMPLETE_UNEXERCISED` rejection, and process-control exception propagation
  were independently confirmed as corrected.
- P03 remains **INCOMPLETE** due to source settlement coverage and the
  settlement-linkage issue. P04 remains **INCOMPLETE** on anomalous
  route/admission paths. P11 passes at static/synthetic level only.
- J synthetic suite was reported as 32 passed, not rerun; authorized H/GN
  14 passed, detached-J GN blocked by branch preflight; C4.2 has 31 passes
  and 3 blocked checks at missing frozen-pilot-plan preflight (13 subtests
  passed). Runtime parity is **NOT TESTED**.
- The required A01–A15 source documents were not present at the paths
  expected by the reviewer; no general architecture-conformance or
  promotion determination is made.

The owner-authorized J-only corrective pass has now:

- added source-trigger references to v2 settlement records and fail-closed
  same-prediction, earlier-record, disposition, outcome, and timestamp checks;
- made unavailable source-order triggers explicit P03 gaps rather than
  accepting unlinked settlement or reordering/synthesizing events;
- added typed/range validation for P11 diagnostic counts, queue snapshots,
  pending entries, and capacity/occupancy while retaining non-gating parity;
- rerun the J synthetic/static suite (**35 passed**) and verified preflight
  plus all 125 GN artifact identities.

The latest corrected report is 28,655 bytes, SHA-256
`3ac6e6f3b57f21e208066757c6d3f671ae58326db7365d7e62f2303927168b13`;
implementation manifest SHA-256
`5625a596ed8a134de0fce0ebaa79eaae6749b9f6f4672f65d606d3d63326540e`.
P03 remains incomplete for the source-order path and readout predictions;
P04 remains incomplete on anomalous route/admission paths.

Review 2 remains preserved with its original PASS WITH FINDINGS disposition.
A third, fresh independent review of these exact corrected bytes and the
reconciled final handoff is required before declaring the J implementation
review-complete. The contract candidate is independently suitable for limited
experimental use subject to formal owner adoption; neither adoption nor
static PPC-11 readiness is claimed.

## Review 3 — exact corrected implementation and complete manifest

**Disposition: PASS WITH FINDINGS.** The independent reviewer inspected the
corrected J code and documentary package read-only. The 232-entry artifact
manifest matched every listed byte size and SHA-256; its 55,286-byte raw
identity is SHA-256
`92bb6b3e55cd3237311f9825aac430cb5b31a33bb66b34c028e85c8cab9c9648`,
matching its detached checksum. J remained detached at the published C4.2
commit/tree. The report (28,655 bytes, SHA-256
`3ac6e6f3b57f21e208066757c6d3f671ae58326db7365d7e62f2303927168b13`),
implementation manifest (`5625a596ed8a134de0fce0ebaa79eaae6749b9f6f4672f65d606d3d63326540e`),
and source manifest (`605a730361da6252173d5466e11fa412ffdecca45c26ffabc31ca384b23d2ec0`)
were verified. Read-only preflight returned
`PREFLIGHT_VERIFIED_NO_NEURAL_EXECUTION` and verified 125/125 GN artifacts.
The reviewer did not run tests, neural code, a real-source pair, or a pilot.

### Independent findings and disposition

- **P03 — INCOMPLETE.** The new settlement trigger linkage is fail-closed:
  same prediction, earlier record, compatible lifecycle outcome/disposition,
  and exact timestamp are required. The source match callback emits
  settlement before the caller's v2 match record, so capture records a gap.
  Expiry can be linked because its trigger precedes settlement. Completion/
  readout settlement coverage also remains incomplete. No transition was
  reordered or synthesized.
- **P04 — INCOMPLETE.** Label-isolated pending-prediction provenance and
  normal-path route evidence are represented; anomalous route/admission
  cases still lack complete source evidence.
- **P11 — COMPLETE at static/synthetic level only.** Mandatory v1 terminal
  state and priority comparison remain gating. Added diagnostic types/ranges
  are validated while differences/absence remain non-gating for parity.
- **V2 contract candidate:** suitable for limited experimental use subject to
  formal owner adoption; adoption has not occurred and v1 remains frozen.
- **Historical identity:** PARTIAL; the `43fb…` and `0ad1…` preimages remain
  unresolved. The new C4.2-N fixture is not historical R6 evidence.
- **Runtime parity:** NOT TESTED. Static PPC-11 readiness remains incomplete;
  pilot/RP-2B remains blocked.
- J 35-test, authorized H/GN 14-test, detached-J GN block, and C4.2
  31-pass/3-blocked/13-subtest results are reported from the implementation
  handoff and were not independently rerun.
- No new implementation blocker was found beyond the stated P03/P04 gaps.
  No architecture promotion or general ACP/A01–A15 conformance determination
  is made.

Review 3 closes the independent-review requirement for the exact corrected
J implementation and its reviewed package. It does not close source-capture
gaps, establish runtime parity, or authorize owner adoption, publication, or
execution.
