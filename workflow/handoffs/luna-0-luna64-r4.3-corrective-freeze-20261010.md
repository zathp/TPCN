# Luna-0 — Luna-64 R4.3 corrective Git byte-preservation freeze

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 R4.3 corrective byte-preservation freeze"
  task_id: "luna64-r4.3-corrective-freeze"
  component: "Governance publication and Git provenance"
  status: "complete"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "73aaa50f97ceab322907875ae4dcf23e7541c3b5"
  result_revision: "Stage A 64a214e310de3b982b90a8ad215598bc1e9f8b1c; Stage B 3c65f572482211f0c771596fc9852f7e4a1ce994; Stage C is this workflow-closure commit (reported by final remote verification, not self-embedded)."
  dependencies:
    - "Final R4.3 candidate review and manifest"
    - "32-entry R4.3 governing-input inventory"
    - "User authorization for exact-path .gitattributes correction"
    - "Independent precommit and post-publication Luna-0 reviews"
  owner: "Project owner"
  classification: ["GOVERNANCE", "PROVENANCE", "PUBLICATION"]
  hypothesis: "Path-scoped Git attributes can preserve the exact reviewed package bytes in retrievable Git objects without changing candidate content."
  counter_hypothesis: "Git filters or an incomplete allowlist alter the candidate bytes or governing identities."
  interfaces_relied_on:
    - "R4.3 manifest and 32-entry input inventory"
    - "Git index, blob, tree, commit, and remote-ref identities"
  label_information_boundary:
    - "No labels or execution inputs were consumed."
  timing_assumptions:
    - "Not applicable; no experiment ran."
  reset_boundaries:
    - "No neural runtime or experimental state was created."
  resource_bounds:
    - "Governance-only publication; no GPU or hardware dependency."
  authorized_scope:
    - "Publish the reviewed candidate on the authorized governance branch."
    - "Add only the specifically authorized path-scoped byte-preservation attributes."
    - "Create Stage-B attestation and close the authoritative workflow after independent PASS."
  unauthorized_scope:
    - "Luna-64 implementation, pilot, training, evaluation, or efficacy claims."
    - "Luna-63C contract or evidence changes."
    - "Architecture promotion or owner-approval inference."
  controls:
    - "Stage only the exact reviewed publication allowlist."
    - "Compare staged and remote package blob bytes directly."
    - "Use separate independent precommit and post-publication reviewers."
  measurements:
    - "Raw SHA-256, Git blob OID, byte length, checkout-filter round-trip, remote commit identity."
  information_boundary_check:
    - "No experimental labels or future inputs were introduced."
  hardware_mapping:
    - "Not applicable; no hardware or runtime experiment."
  architecture_invariants_touched:
    - "None; A01-A15 preserved."
  preserves:
    - "Original R4.3 manifest SHA-256 and exact ten raw package hashes."
    - "All 32 original governing-input identities."
    - "Luna-63C boundary and all protected certificate content."
    - "No pilot authorization or owner approval."
  architecture_change: false
  proposal: null
  files_changed:
    - ".gitattributes"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna64-r4.3-provenance-attestation-20261010.json"
    - "workflow/handoffs/luna-0-independent-postpublication-review-luna64-r4.3-20261010.md"
    - "workflow/handoffs/luna-0-luna64-r4.3-corrective-freeze-20261010.md"
  tests_added: []
  tests_passing:
    - "Independent precommit staged-byte review: PASS."
    - "Independent remote post-publication review: PASS — IMMUTABLE FREEZE VERIFIED."
    - "Ten remote package raw SHA-256 comparisons and checkout round-trips."
    - "Thirty-two inventory identity reconciliations."
  tests_failed:
    - "Default git diff --check treats preserved CRLF and Markdown hard-break spaces as trailing whitespace; the independent reviewer classified these separately from content identity."
  tests_not_run:
    - "Candidate tests and validators were not rerun during this publication correction."
    - "No pilot, scientific experiment, training, evaluation, or hardware validation."
  assumptions:
    - "Git commit identities are retrievable but not protected from later remote history rewriting."
    - "Twenty-three legacy inventory checkout hashes were confirmed by the exact LF-to-CRLF transform under the verification environment, not a newly created checkout."
  unresolved:
    - "Explicit owner approval of the frozen pilot gate remains required."
    - "Luna-64 execution remains unauthorized."
  recommended_next_agent:
    - "Project owner to decide whether to authorize the exact frozen pilot gate."
```

## Outcome

Resolved the staging discrepancy without changing the reviewed R4.3 candidate.
Git's `text=auto` plus `core.autocrlf=true` had normalized 31 of 35 unique
reviewed/inventory paths during clean-filter evaluation. The eight CRLF R4
package files now use exact-path `-text` rules. The two LF R4 package files
use exact-path `text eol=lf` rules so checkout bytes remain stable.

The reviewed manifest remains byte-for-byte unchanged at SHA-256
`62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
The eight expected old normalized blob IDs and exact published blob IDs are
listed in the [Stage-B provenance attestation](luna-0-luna64-r4.3-provenance-attestation-20261010.json).
No manifest was regenerated or edited to match the corrected Git objects.

## Publication and independent review

- Stage A content freeze: `64a214e310de3b982b90a8ad215598bc1e9f8b1c`,
  parent `73aaa50f97ceab322907875ae4dcf23e7541c3b5`.
- Stage B attestation: `3c65f572482211f0c771596fc9852f7e4a1ce994`.
- Remote ref: `origin/governance/luna64-r4.3-freeze-20261010`.
- Precommit independent review: **PASS**.
- Post-publication independent review:
  **PASS — IMMUTABLE FREEZE VERIFIED**; see the
  [review record](luna-0-independent-postpublication-review-luna64-r4.3-20261010.md).
- The independent review verified all ten package hashes, all 32 inventory
  identities, the exact allowlist, the remote ref, and Luna-63C isolation.

The remote review found that 23 of the 32 inventory raw hashes are reproduced
by LF-to-CRLF materialization under `core.autocrlf=true`, while nine match the
committed Git blob bytes directly. This computed materialization was not
confirmed in a newly created checkout. Exact checkout behavior is pinned for
the ten R4 package paths only. A remote branch is not immutable against later
history rewriting.

## Validation and disposition

The ten package files passed byte-for-byte working/staged and remote blob
comparisons, and checkout-filter round-trips passed. The 32 inventory entries
were reconciled against recorded raw hashes and Git identities; six inventory
Git blob IDs are exact-byte remappings while the remaining 26 retain their
recorded IDs.

The full `git diff --check` reports preserved CRLF and intentional Markdown
hard-break whitespace. With CR at EOL accepted, the independent precommit
review classified the remaining reports as Markdown hard breaks only; no
source bytes were changed to silence these diagnostics.

The workflow status is **R4.3 FROZEN — READY FOR OWNER AUTHORIZATION**. Owner
approval remains **not provided**; Luna-64 pilot execution remains
**not authorized**. No implementation, experiment, training, evaluation,
Luna-63C change, production integration, or architecture promotion occurred.
