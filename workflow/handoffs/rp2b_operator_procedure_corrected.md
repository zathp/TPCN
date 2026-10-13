# RP-2B Operator Procedure — Corrected, Non-Executable, Not Authorized

**Revision:** Corrective R1 — 2026-10-12  
**Status:** Static governance artifact only. **No execution, preflight, test, import, compilation, or runtime action is authorized by this document.** RP-2B remains **BLOCKED — CORRECTION REQUIRED**; execution and downstream qualification remain **NOT AUTHORIZED**.

This procedure intentionally contains no shell, PowerShell, Python, or other executable command; no invocation template; no operational checklist to perform now; and no instruction that can launch a future phase from Phase 0. Do not derive commands or fill placeholders from source, Lane D, or this document. The prior Lane D report remains untouched and its command/process-name termination advice is rejected (see `rp2b_lane_d_corrected.md`).

## Unresolved bindings — placeholders, not defaults

Each value below is unresolved. A future owner must provide and approve the exact binding in a separate, immutable grant; placeholders must not be populated by an operator or inferred from the historical candidate.

| Binding | Required value |
|---|---|
| Separate owner execution grant | `<UNRESOLVED: grant identifier, date, owner, scope, exact authorized actions, limits, expiry and review record>` |
| Reviewed revision | `<UNRESOLVED: exact fetched commit/tree and clean/dirty policy in the future grant>` |
| Source and checkout identities | `<UNRESOLVED: grant-bound probe/wrapper paths, checkout hashes, Git object IDs, and any changed successor identities>` |
| Host and environment | `<UNRESOLVED: actual attended host, OS/build, shell and executable identity, architecture, session, user/token/integrity, environment and route>` |
| Operator and supervision | `<UNRESOLVED: named attending operator, contact/escalation path, observation method and supervision boundary>` |
| Exact command and arguments | `<UNRESOLVED: supplied verbatim and explicitly approved by a separate owner grant; never derive here>` |
| Run identifier | `<UNRESOLVED: exact owner-approved unique run ID and grammar>` |
| Evidence destination | `<UNRESOLVED: exact owner-approved fresh destination and approved route/containment checks>` |
| Resource contract | `<UNRESOLVED: written owner reconciliation of 256 MiB/120-second request with frozen RP-2 64 MiB/10-5-20 design, or separately reviewed successor contract/source>` |
| Evidence budget proof | `<UNRESOLVED: independently reviewed exact-schema maximum-size/all-representation proof under unchanged 1 MiB cap, including console and failure/finalization paths>` |
| Stop/abort and classification | `<UNRESOLVED: grant-bound stop authority, monitoring/overrun semantics, canonical result rules, and operator alert procedure>` |
| Retention and reviewer | `<UNRESOLVED: evidence retention/custody duration, integrity controls, independent reviewer, and no-delete/no-alter rule>` |

The current manifest candidate itself remains blocked and leaves these runtime values unresolved (`rp2b_authorization_manifest_candidate.json`, `unresolved_values`, `blocking_findings`, `authorization`). It is not the grant.

## Phase 0 — Static-only review boundary (this cycle)

**Allowed scope:** read the frozen artifacts and source text; compare their recorded identities, requirements, and claims; write only the two specifically authorized correction documents. Do not perform a preflight or prepare an invocation. Do not interact with a target host, process list, interpreter, OS API, filesystem route, or evidence destination. Do not create an evidence leaf or runtime artifact.

**Stop gate:** this phase ends with the static disposition **BLOCKED — CORRECTION REQUIRED**. It does not start, schedule, or trigger Phase 1, Phase 2, or Phase 3. There is no action the operator may perform now to “continue.”

Blockers include the unresolved resource-policy conflict, absent worst-case evidence-fit proof, corrected operator/provenance material needing independent review, unresolved host/run/command/destination/grant, and outstanding runtime qualification (`rp2b_luna0_independent_review.md` §§1–4, 6; `rp2b_authorization_readiness.md` §§B1–B4).

## Phase 1 — Future authorized attended preflight (unavailable this cycle)

This is a description of a **future gate only**, not permission or a procedure to execute now. It remains unavailable until all Phase 0 blockers close, a separate written owner grant explicitly authorizes the exact attended preflight, and an independent reviewer accepts the exact grant-bound materials. No such grant is present in this package.

If separately authorized in a future cycle, the grant must first specify the exact static identity and destination checks, their approved method, host/operator binding, stop conditions and evidence handling. Mismatch, ambiguity, missing observation, or identity drift must stop the process before any launch; there is no repair, substitution, retry, permission change, or fallback. This document provides none of those checks as runnable instructions.

Unresolved for that separate decision: `<GRANT>`, `<HOST>`, `<OPERATOR>`, `<REVISION>`, `<SOURCE_IDENTITIES>`, `<APPROVED_PREFLIGHT_SCOPE>`, `<RUN_ID>`, `<EVIDENCE_DESTINATION>`, `<RESOURCE_PROFILE>`, `<STOP_RULE>`, and `<RETENTION/REVIEW>`.

## Phase 2 — Explicitly prohibited this cycle

**RP-2B invocation is prohibited under this package.** No command or other action may launch the wrapper, probe, interpreter, child process, test, compilation, native API operation, or runtime preflight. Do not complete or copy Lane D's command; do not invoke a future phase from Phase 0 or Phase 1; do not perform process-name/PID enumeration or termination; do not manually kill an outer process or child; do not create the evidence destination; and do not retry.

Only a new, separate owner decision and independently reviewed successor authorization package could change this prohibition for a future cycle. A placeholder, proposed manifest field, static source branch, or this procedure cannot grant that authority.

## Phase 3 — Post-run verification (unavailable until an authorized run)

There is no run in this correction, so no run evidence exists to verify. This phase is unavailable unless a distinct future owner grant authorizes a run and that run is actually performed under its exact reviewed conditions. This document authorizes no post-run inspection, evidence movement, cleanup, deletion, or classification now.

If a future authorized run occurs, required evidence and its custody, integrity checks, independent review, and canonical outcome handling must come from that grant and accepted successor procedure. Missing required Low cessation/EOF/cleanup evidence remains `RP2_UNKNOWN_FAIL_CLOSED`, requires an operator alert that containment is unresolved and a Low child/descendant may still be active, and blocks retry and downstream progression. A termination request, Medium exit, job membership, or process-name check is not proof of Low/tree cessation (frozen restricted-token contract §6; owner decision D-RP2-OUTER-1; `outer_wrapper.ps1:83–85, 985–1001`; `rp2b_luna0_independent_review.md` §6).

## Governance and preservation

- RP-2B execution: **NOT AUTHORIZED**.
- Downstream qualification: **NOT AUTHORIZED**.
- No preflight or invocation is supplied or approved here.
- No historical or existing readiness artifact is superseded or overwritten.
- The historical parameter-binding incident remains disclosed with its original forensic limit; it is not proof that no side effect occurred (`luna-0-luna65-rp2a-implementation-review-20261012.md`, “Static-validation boundary”; `rp2b_luna0_independent_review.md` §4).
- The current source identity establishes static provenance only. The separate resource-policy resolution and exact maximum evidence-fit proof remain prerequisite blockers.

Artifacts created for this correction: `workflow/handoffs/rp2b_lane_d_corrected.md` and `workflow/handoffs/rp2b_operator_procedure_corrected.md`. No other repository file was changed.
