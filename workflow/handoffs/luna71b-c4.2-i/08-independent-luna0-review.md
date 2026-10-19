# Luna-71B-C4.2-I — Independent Luna-0 design review

## Final review disposition

**PASS WITH FINDINGS — documentary design only.** The initial independent
review identified design clarifications and approval boundaries. The
author-authorized documentary corrections were made, and an independent
Luna-0 correction check verified closure of those specified findings against
the revised documents. This is not schema adoption, implementation
authorization, neural parity, pilot readiness, or publication approval.

## Reviewed baselines and exact candidate

* C4.1 baseline: branch `governance/luna71b-c4-1-ppc11-freeze`, HEAD
  `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`; authoritative PPC-11 manifest
  SHA-256 `2f18d694784a6a583b0a7c01e6cc89f1313c2d65c7c6b5346a7cd4d993d3f1fa`.
* H candidate: branch `governance/luna71b-c4-2-h-corrections`, HEAD
  `e91818a5c974282e848dc43e52d3c0a534dcbf45`, tree
  `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749`. The H tree is dirty; H source,
  fixture and identity manifests—not HEAD alone—identify the candidate.
* Revised I files reviewed by the correction checker:

| File | Bytes | SHA-256 |
|---|---:|---|
| `01-p03-semantic-gap-analysis.md` | 8,716 | `43b93d054d65f683bdd78149466f426c614d0305429fd09c0a610877058a731d` |
| `02-p04-lineage-and-route-outcomes.md` | 7,971 | `aaf42b71118deafb93bc052a49c2289603fd4b039045afb37928ab8ddfd1df71` |
| `03-p11-failure-attribution.md` | 6,815 | `bc84f25a61daba181a5abed77b29812788fbc70738f7ddfd2af33fd3c86058ac` |
| `04-proposed-versioned-trace-schema.md` | 17,985 | `d756d35037a5412c691024c3a7479cebfe9ec5ff985f0cc47c53e30f8542245f` |
| `05-ppc11-compatibility-matrix.md` | 8,294 | `d1c4f03d7389ac005a5f59ec48754503b8959dcdb8cbe0f6f8849449beb8c8f1` |
| `06-historical-identity-disposition.md` | 6,557 | `c60752ef2a3715d710dc2ea0b950519cd49d8210aa87e16fa3412817e3ad0d70` |
| `07-regression-and-provenance-assessment.md` | 9,519 | `7a0dcdde95f307a544337d36973f22da293a80de50d8ade70122438da61f398f` |

The initial review was against an earlier candidate revision; it is preserved
as historical review evidence here, not retroactively represented as a review
of the revised hashes above.

| File | Initial review bytes | Initial review SHA-256 |
|---|---:|---|
| `01-p03-semantic-gap-analysis.md` | 8,716 | `43b93d054d65f683bdd78149466f426c614d0305429fd09c0a610877058a731d` |
| `02-p04-lineage-and-route-outcomes.md` | 7,587 | `93863f19a90088e2f7cc19b3d8c96f8cd512883f18a80bae37072bde005e5d68` |
| `03-p11-failure-attribution.md` | 6,815 | `bc84f25a61daba181a5abed77b29812788fbc70738f7ddfd2af33fd3c86058ac` |
| `04-proposed-versioned-trace-schema.md` | 16,711 | `04a38aeb032138f4c26766888deba56c4d67be5582fcc4c3f3fa2a7b3249767a` |
| `05-ppc11-compatibility-matrix.md` | 7,764 | `75b797c2849540b2b9caee20d92e59f6781a7db42605aac41d44d6b621583072` |
| `06-historical-identity-disposition.md` | 6,557 | `c60752ef2a3715d710dc2ea0b950519cd49d8210aa87e16fa3412817e3ad0d70` |
| `07-regression-and-provenance-assessment.md` | 9,283 | `a5149ad047d7032027c9570ae489066eb29c0e023295dcf7ce927b5870fa03f6` |

The correction check matched the revised hashes above. The exact inventory reviewed by Luna-0 is preserved as
[`10-review-inventory-candidate.json`](./10-review-inventory-candidate.json)
with detached checksum
[`10-review-inventory-candidate.sha256`](./10-review-inventory-candidate.sha256).
It was 98,884 bytes with SHA-256
`c7deff6e407f5e3f8f19ace657bc3616d101420b2552a01303229fa078918b4c`; its
candidate-path sidecar is 101 bytes with SHA-256
`a4960ffe700a127e891a163f71099b87c7e689ff5ee40b6642877f7044e0711d`.
The exact 92-byte audit-time sidecar is separately preserved as
[`10-review-inventory-audit-sidecar.sha256`](./10-review-inventory-audit-sidecar.sha256);
its SHA-256 is
`21d0be4cc216aa6ada648bf79c2109a93eec82617371d2bdeabcb1acb216abe1` and it
retains the original `10-artifact-manifest.json` filename it bound at audit
time.
The final
[`10-artifact-manifest.json`](./10-artifact-manifest.json) is regenerated to
bind the final review and adjudication bytes; it is parent-validated, not
represented as independently reviewed by Luna-0.

## Initial independent review findings and disposition

The first Luna-0 review returned **PASS WITH FINDINGS** and confirmed that the
proposal was design-only, maintained explicit owner gates, and did not claim
parity/readiness. Findings:

| Finding | Initial issue | Correction and independent disposition |
|---|---|---|
| F1 — P11 terminal comparison completeness | The terminal comparator did not enumerate every frozen P11 field and every added terminal field. | `04` §§7–8 and `05` explicitly require exact comparison of all frozen P11 observations and every added terminal field, with no terminal projection. Correction check: **CLOSED**. |
| F2 — P04 stage outcomes | Route production, queue admission, and destination delivery could be read as one outcome. | `02` and `04` §6 define separate route-construction, P02-only admission (referenced by `record_index`), and delivery/integration records. `ADMITTED` belongs only to the P02 admission record. Correction check: **CLOSED**. |
| F3 — future owner adoption | P03 non-symbol creation, `NOT_APPLICABLE`, the derived symbol rule, and P11 failure comparison change acceptance details. | Retained as an explicit pending owner decision in `04` and `05`; not “closed” by technical review. |
| F4 — artifact-manifest locator | The I inventory had no exact path in the design document. | `07` names the I manifest and detached checksum paths; the correction check confirms explicit paths. The manifest was not present at the time of that correction check and is produced as a separate artifact after it. |

## Correction-check findings

The second independent Luna-0 check verified:

* v1's required non-empty `expected_symbol` remains unchanged for the v1
  record and symbol-bearing v2 record;
* v2 adds a separate non-symbol creation record with explicit
  `NOT_APPLICABLE`, and discloses that this changes P03 applicability and
  requires owner acceptance;
* completion `NOT_APPLICABLE` does not convert the absent completion
  settlement path into a successful transition;
* the exact P11 and P04 corrections above appear in the revised candidate; and
* the manifest location is explicit, with no placeholder path.

No source, tests, neural runner, training, inference, or pilot were executed.
The reported H test results remain H evidence, not tests run by either
reviewer.

## Review limitations and required owner decisions

The initial reviewer confirmed the H manifest identities and group-level
provenance descriptions, but did not independently recompute each auxiliary
file identity. A separate bounded Luna-0 inventory audit then verified all
125 H GN artifact entries and all 80 source-copy entries against raw bytes,
sizes, and manifests, with zero mismatches. It confirmed 69 verified source
dependencies, six reviewed implementation artifacts, and five auxiliary
tools; it separately verified the exact pilot-plan copy match and confirmed
that it is not a committed object. The checked manifest at that time was
98,884 bytes, SHA-256 `c7deff6e407f5e3f8f19ace657bc3616d101420b2552a01303229fa078918b4c`;
the sidecar was 92 bytes, SHA-256
`21d0be4cc216aa6ada648bf79c2109a93eec82617371d2bdeabcb1acb216abe1`.
The final manifest is regenerated only to bind the exact final I review and
adjudication document bytes. The parent revalidates the final inventory after
that update. No neural/test execution is part of either audit.

The actual repository carries architecture and workflow authorities under
`workflow/` (`ARCHITECTURE_CONTRACT.md`, `README.md`, `docs/luna/`,
`docs/architecture/`, and `docs/architecture_proposals/`); the agent-profile
alias directory `tpcn-luna-workflow/` is not present. The applicable C4.1
handoff/contract is present and remains authoritative. No architecture clause
or ACP is changed by this documentary trace-schema design.

The reviewers explicitly leave adoption to the owner. Required future
decisions are listed in
[`09-final-adjudication.md`](./09-final-adjudication.md), including the
versioned contract, P03 derivation/non-symbol acceptance, P04 passive
instrumentation, P11 failure comparison, and any later C4.2-N qualification.

## Final disposition

The documentary schema design is **REVIEWED — PASS WITH FINDINGS**; the
specified F1/F2/F4 wording corrections are independently confirmed closed.
F3 and all substantive acceptance changes remain pending owner decision. This
review does not establish implementation readiness, neural parity, or pilot
authorization.
