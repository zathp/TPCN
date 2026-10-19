# Luna-71B-C4.2-J — Final readiness adjudication

**Adjudication scope:** The bounded C4.2-J candidate and its static/synthetic
evidence only. Published C4.1 PPC-11 v1, published C4.2, historical H/GN
evidence, and C4.2-I artifacts remain unchanged. No neural execution,
training, inference, or paired pilot was performed or authorized.

## Identity basis

- Published C4.2: commit
  `e91818a5c974282e848dc43e52d3c0a534dcbf45`, tree
  `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749`.
- Published C4.1 PPC-11: commit
  `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`, manifest SHA-256
  `2f18d694784a6a583b0a7c01e6cc89f1313c2d65c7c6b5346a7cd4d993d3f1fa`.
- J is an isolated, uncommitted worktree at
  `C:\Users\Patrick\Documents\ActiveCode\TPCN\_worktrees\luna71b-c4-2-j`,
  detached at the published C4.2 commit. Its corrected implementation
  provenance report is 28,655 bytes, SHA-256
  `3ac6e6f3b57f21e208066757c6d3f671ae58326db7365d7e62f2303927168b13`.
- The J source manifest, implementation manifest, GN artifact manifest, and
  new fixture identities are itemized in
  [`03-implementation-provenance.md`](./03-implementation-provenance.md),
  [`04-focused-validation-and-regression-disposition.md`](./04-focused-validation-and-regression-disposition.md),
  and the artifact manifest delivered with this handoff.

## Gate results

| Gate | Result | Basis |
|---|---|---|
| V2 candidate / experimental adoption | **INDEPENDENTLY SUITABLE FOR LIMITED EXPERIMENTAL USE; FORMAL ADOPTION PENDING** | Luna-0 review 2 found the versioned candidate suitable as a constrained experimental contract, subject to owner adoption. V1 remains frozen. |
| P03 capture | **INCOMPLETE** | Settlement rows must reference an earlier same-prediction match/expiry with matching disposition/time. The source match callback emits settlement before the v2-observed match, so that path remains a gap; readout predictions also lack full settlement coverage. No transition was synthesized or reordered. |
| P04 capture | **INCOMPLETE** | Pending-prediction target, label isolation, source lineage and normal route/delivery evidence are represented. Anomalous route/admission evidence is not complete for all source paths. |
| P11 capture | **COMPLETE at static/synthetic level** | Existing mandatory v1 terminal state and exact priority remain gating and are captured/tested; additional operation/cause diagnostics are non-gating. Runtime parity is not inferred. |
| Historical identity | **PARTIAL / historical R6 BLOCKED** | The `43fb…` source-manifest and `0ad1…` test-index preimages remain unavailable; no historical evidence was rewritten or waived. |
| New fixture identity | **VERIFIED** | C4.2-N fixture has independent manifest, event-payload, and initial-parameter hashes; it is not an R6 reproduction. |
| Initial parameters | **VERIFIED** | Exact 112-byte payload SHA-256 is recorded in the provenance and validation reports. |
| Paired driver | **COMPLETE for injected synthetic backend only** | The v2 bilateral driver performs identity-bound preflight/dispatch/comparison using injected test doubles. No real-source neural pair ran. |
| Focused synthetic/static validation | **PASS** | Final J synthetic/static suite: 35 passed in 314.847s. Authorized H/GN suite: 14 passed. J's detached GN attempt remains blocked by branch preflight. Three C4.2 tests remain blocked by the absent frozen pilot plan; expected identities were not changed. |
| Static PPC-11 readiness | **INCOMPLETE** | P03 and P04 capture gaps prevent READY. |
| Independent Luna-0 review | **PASS WITH FINDINGS** | Review 3 independently checked the corrected J code, current provenance, complete 232-entry artifact manifest, and read-only identity preflight. No new implementation blocker was found beyond P03/P04. |
| Runtime parity | **NOT TESTED** | No neural runner or real paired execution occurred. |
| Neural execution | **NOT AUTHORIZED; NOT PERFORMED** | Explicit scope boundary. |
| Pilot execution | **NOT AUTHORIZED; NOT PERFORMED** | Explicit scope boundary. |
| RP-2B | **BLOCKED / BOUND INCOMPLETE** | No execution authorization; prerequisite capture and historical identity gates remain unresolved. |

## Final disposition

The V2 candidate is **independently suitable for limited experimental use,
subject to formal owner adoption**; adoption has not been declared here.
The J implementation is **not READY for static PPC-11**. P03 remains
incomplete where source ordering does not expose an earlier trigger and on
readout paths without settlement. P04 remains incomplete on anomalous
route/admission paths. Historical R6 identity is PARTIAL/BLOCKED, and runtime
parity is NOT TESTED. The new fixture is a separate verified lineage and does
not repair historical R6 provenance.

No commit, push, merge, publication, neural execution, inference, training,
pilot, Track B/RP-2B modification, or architecture promotion occurred. Any
future publication requires a separate explicit authorization and must use
the exact final artifact allowlist; this handoff does not publish the
untracked J worktree.

The narrowest next owner action is to decide whether to formally adopt the V2
candidate for constrained experimental use. Closing any remaining P03/P04
source gaps would require a separately bounded passive-observation task; if a
transition is unavailable without changing model behavior, leave it blocked
rather than adding synthetic settlement, reordering source events, or
inferring an outcome. Real-source paired execution, neural execution, and
pilot/RP-2B remain separate authorization gates.
