# Luna-0 RP-2B Corrective Review R2 — Final Exact-Byte Independent Review

**Review date:** 2026-10-12  
**Reviewed branch:** `governance/luna64-r4.3-freeze-20261010`  
**Reviewed `HEAD` / fetched branch origin:** `96fb4aec100578db6939136b4ed7985478f18bb8`  
**Scope:** final static/exact-byte review of the corrected RP-2B readiness package, including the Lane C correction requested in Luna-0 R1.  
**Narrow review result:** **PASS — R1 Lane C corrections are accepted as static corrections; identity checks match.**  
**Integrated RP-2B readiness:** **BLOCKED — resource decision and evidence-fit gates remain open.**  
**RP-2B execution / downstream qualification:** **NOT AUTHORIZED.**  
**Publication:** **NOT AUTHORIZED / NOT PERFORMED.**

This is an independent static adjudication, not execution permission, runtime
qualification, publication approval, owner policy selection, contract
amendment, or architecture change. It used only read-only source/document
inspection, Git identity/status inspection, and SHA-256 calculation. No
candidate was edited. This is the only file created by this review.

## 1. Baseline, exact bytes, and preservation

The current branch is the requested branch. `HEAD` and
`origin/governance/luna64-r4.3-freeze-20261010` both resolve to
`96fb4aec100578db6939136b4ed7985478f18bb8`; `HEAD^` is
`f47c48a947e48867c629817fa1031cb93729e440`. At review start, tracked and
index diffs were empty (`git diff --quiet` and `git diff --cached --quiet`
both returned 0). This is not a clean-worktree claim: the previously present
review package and two protected files were untracked.

### Source and literal identities

| Item | Raw checkout SHA-256 / identity | Result |
|---|---|---|
| Probe `scripts/luna65_phase2a_rp2_compatibility_probe.py` | `B8F669C68ED5768E4126FFA87E855002A5E7E5E116999E81E4AAE1CA69CE2427`; `HEAD` blob `e76c2abf728072315c779da990cf9a5e445f1a00` | Match |
| Outer wrapper `scripts/luna65_phase2a_rp2_outer_wrapper.ps1` | `F7C39C0FC849F61AFFF71A07AC8DCC7BDBEBA91D9971B44BCCF96B0C01ABE2A7`; `HEAD` blob `3c29b21952e08100da2779c1a7fb02dcc930acdf` | Match |
| Embedded `SYNTHETIC_LITERAL` | 6,583 ASCII bytes after source newline normalization and `.lstrip()` semantics; SHA-256 `D9EC540BCEA9326C67A791DA6C59FC11357C00396B707EEB9FE278FCD08BF2A0` | Match |

The literal was re-extracted as delimited source text only, normalized to
Python universal-newline behavior, stripped at the leading-whitespace
boundary, encoded as ASCII and hashed. The source was not evaluated,
compiled, imported or invoked.

### All six historical RP-2A source-tree entries

The current `HEAD` tree contains all six allowlisted entries with the
following exact Git blobs:

| Path | `HEAD` blob |
|---|---|
| `scripts/luna65_phase2a_rp2_compatibility_probe.py` | `e76c2abf728072315c779da990cf9a5e445f1a00` |
| `scripts/luna65_phase2a_rp2_outer_wrapper.ps1` | `3c29b21952e08100da2779c1a7fb02dcc930acdf` |
| `workflow/docs/luna/LUNA_65_PHASE2A_RP2A_CORRECTIVE_R1_TRACEABILITY.md` | `646548764258ff252ffd6a386461a60671885dba` |
| `workflow/handoffs/luna-0-luna65-rp2a-corrective-r1-20261012.md` | `9e7cc656224d400030e9c50f98b058f46bc780fd` |
| `workflow/handoffs/luna-0-luna65-rp2a-implementation-review-20261012.md` | `cf4f267ae9deb95a7290baee3b8a66e4bb23079c` |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `4b5639effead056f54f815814bbeeb42e7dba07b` |

These are the historical six paths only. None of the RP-2B corrective
artifacts below is included in that allowlist. The protected, pre-existing
untracked files still match their recorded raw identities:

| Protected untracked path | SHA-256 |
|---|---|
| `scripts/luna65_phase2a_supervisor.py` | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` |
| `workflow/handoffs/luna-0-luna65-s1b-final-execution-authorization-record-20261012.md` | `BB9134CB7FF1813D495575FA80F912EEFB6E6A7C7A86F720CDAD829CAC925451` |

Neither protected file was edited, staged or included in the proposed
publication scope.

## 2. Corrected manifest and exact artifact identities

The corrected manifest's current raw checkout SHA-256 is
`7A63491699A6BE2D3FB5174634126DA24AED38CF0DAD696FCF0544FA873B2D60`.
Its source digests/blobs, six-tree inventory, governing-input identities,
readiness-input hashes, protected-file hashes, and nine correction-artifact
hash entries were compared with the current checkout. All 22 governing and
original-readiness checkout hashes match its declarations; all nine
correction-artifact hashes below match as well. Manifest status is consistent
with a blocked package: no owner resource option is selected, no worst-case
fit is asserted, `total_max_bytes` is null, and execution, downstream
qualification and publication are false. Its R1/pending-review statements
are retained as the manifest's pre-R2 snapshot, not silently rewritten by
this review.

Raw checkout SHA-256 identities:

| Corrective artifact | SHA-256 |
|---|---|
| `workflow/handoffs/rp2b_resource_reconciliation.md` | `7305637DC037CFAA8E8E463730BE1B960FFE545F06B291CEE5F0D8B1EC61F9D6` |
| `workflow/handoffs/rp2b_resource_owner_decision_candidate.md` | `374B5843C4EEE67D05DC3A0DBD9972E9419E7889A8AD9AE8DB541044AC3244C6` |
| `workflow/handoffs/rp2b_lane_c_corrected.md` | `29D2700838F6D2D8D9048A6D0F2D88274B29F1F0F61E23349AC0574057FC0BD6` |
| `workflow/handoffs/rp2b_race_classification_corrected.md` | `C0C014888F31BE9957BD3148D351BB686F696A5975DDF1C96908622FD466C4B5` |
| `workflow/handoffs/rp2b_lane_d_corrected.md` | `4E660BCDB13E553C14591BDC30DF7DEB0221253BDD5000ED8BC15DC65A458894` |
| `workflow/handoffs/rp2b_operator_procedure_corrected.md` | `9032D8016C339F71016FA4029CEC73088055539636923E46EEF76C1CB88DA30D` |
| `workflow/handoffs/rp2b_evidence_worst_case_bound.md` | `44F444046C958AAABED9246B012CD0A2C74A8E95D45B4E108594DC9F97F4FE4C` |
| `workflow/handoffs/rp2b_corrective_reconciliation_matrix.md` | `7738337F1497608DF28A756B03502EC0188786A3DE97A016831AB4E195084102` |
| Prior Luna-0 R1 review input, `workflow/handoffs/rp2b_luna0_corrective_review_r1.md` | `688B3644C5B6009964F3A20278CD3AA84028C8CB8A9B0C1C999FD876024FB91A` |

The R2 review's own SHA-256 is intentionally not embedded in this document;
it is reported separately in the tool result to avoid a self-hash cycle.

## 3. Independent findings

### B1 — Resource reconciliation: BLOCKED; no owner decision

The frozen RP-2 profile remains 64 MiB Job Object job-memory charge, an
8-process backstop, 5-second job user-time backstop, 10-second active window,
up to 5 seconds cleanup, 20-second outer deadline, zero retries and a 1 MiB
logical evidence cap. Resource Policy R2's 256 MiB and 120-second CPU/wall
design is Phase 2A-only; it does not amend RP-2B. Job charge, aggregate
private commit, working set, job user time, aggregate user-plus-kernel CPU,
elapsed wall and confirmed cessation are distinct measures.

The resource decision candidate records **NONE** for owner selection.
Option C is a current review recommendation only, not an owner decision.
No policy amendment or source-compliance claim is established. Keep B1
**BLOCKED** pending explicit owner selection or a separately authorized and
independently reviewed RP-2B contract/source change.

### C1 / N2 — Lane C and race matrix correction: accepted, static scope only

The required R1 correction is present in both Lane C and the race matrix:

1. The probe's `BASELINE` value, `f47c48a947e48867c629817fa1031cb93729e440`,
   equals the reviewed source commit's actual parent (`HEAD^`) and the RP-2A
   corrective handoff's `base_revision`. It is source-base provenance, not a
   mismatch with reviewed `HEAD` `96fb4aec100578db6939136b4ed7985478f18bb8`.
   Source identity remains separately bound by the manifest's source
   checkout hash and Git blob.
2. D-RP2-DIRECT-1 accepts the hash-bound direct-base executable for
   diagnostic **design only**. Corrected Lane C no longer calls that choice
   an unresolved venv-topology contradiction. The decision is not a frozen
   contract amendment, runtime/source-to-binary compatibility result or
   RP-2B grant. A future grant must bind the accepted design and exact
   source/literal/interpreter identities.

The related handle-inheritance qualification is also corrected: direct
`HANDLE_LIST` controls apply at the described creation boundary; they do not
establish chain-wide inheritance or runtime semantics. Direct-base design
acceptance does not prove behavior beyond that boundary.

The race matrix covers active timeout and cessation ordering; cleanup after
apparent/confirmed cessation; truncation/accounting loss during termination
and drain; process/job/worker termination or join failures; missing Low and
Medium evidence; finalization failures; and contradictory observers. Its
non-negotiable rule is correct: if required Low cessation evidence is
missing or unreliable, return `RP2_UNKNOWN_FAIL_CLOSED` and issue the
unresolved-containment operator alert. Medium P signal/EOF, job membership,
or a successful termination request cannot substitute for Low cessation.
This is a conditional classification rule, not an observed runtime result.

No new Lane C source/profile defect was found in the corrected text. The
original Lane C PASS remains rejected as sufficient evidence; static
correction does not certify ABI, Windows behavior, worker cancellation,
deadlines, isolation or cessation.

### D1 — Lane D and operator procedure: static correction accepted; no readiness grant

The corrected Lane D withdraws the prior PASS, preserves the incident's
forensic uncertainty, corrects provenance and classification assertions,
and does not reuse the prior unsafe command or process-name/PID termination
guidance. The corrected procedure is non-executable: it contains no command
or invocation template, leaves host/run/destination/grant fields unresolved,
ends Phase 0 blocked, and explicitly prohibits this-cycle preflight and
execution. It does not authorize a future phase or establish operator-alert
delivery. The historical Lane D report remains discredited and unchanged.

### E1 / N1 — Worst-case evidence fit: BLOCKED; no finite supported TOTAL_MAX

**Independent decision:** the reviewed evidence does not establish a finite,
defensible `TOTAL_MAX <= 1,048,576` bytes for all mandatory evidence and
simultaneous retained representations. Do not treat the write-time cap as
proof that every required record fits.

The source establishes constants and local controls: total 1,048,576 bytes,
payload 917,504 bytes, finalization reserve 131,072 bytes, 393,216-byte
probe reservation, individual record ceilings and source counters. These are
not a complete schema-level maximum. Mandatory O record/event counts and
complete encoded field maxima are not jointly specified; relay and copied
section/decoded files create simultaneous representations; `report.json`
growth and failure/finalization cases have no complete maximum derivation.
The capped failure counters and write guards do not establish that a
complete required success or failure record set fits.

The outer wrapper's unresolved-containment alert, controller-error
diagnostic, final verdict/report digest line, and finalization-error output
are written directly to `Console.Error`/`Console.WriteLine`, not through
`Write-Artifact`/`Charge`. Some individual strings/fields are source-capped,
but no complete capture, retention or aggregate-size boundary for console
and host transcript output is specified. External authorization,
provenance and operator/host binding also have no jointly bounded schema
or explicit in/out-of-cap definition. Even if those items were deemed
outside the 1 MiB run-artifact boundary, the in-boundary complete mandatory
schema/count/representation proof is still absent. Thus no defensible
finite maximum fitting under the unchanged cap can be certified.

The source's failure-finalization path may not write a complete report;
the source then switches to UNKNOWN and writes another console alert/error.
The required alert's runtime delivery and durable retention are not
established. Preserve E1 as **BLOCKED — EVIDENCE FIT NOT ESTABLISHED**;
do not populate `total_max_bytes`, infer fit from counters, discard
mandatory evidence or raise the cap.

### Publication, authority and runtime boundary

Corrective artifacts are outside the exact six-path historical RP-2A
publication allowlist, so this package is not publication-eligible under
that allowlist. The corrected manifest also records publication false.
No owner execution grant or resource selection is present. RP-2B execution
and downstream qualification remain **NOT AUTHORIZED**.

No TPCN A01–A15 clause, computational interface or ACP is changed. The
profile-listed paths
`tpcn-luna-workflow/ARCHITECTURE_CONTRACT.md`,
`tpcn-luna-workflow/ARCHITECTURE_CHANGELOG.md`,
`tpcn-luna-workflow/docs/luna/LUNA_WORKFLOW.md`,
`tpcn-luna-workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`tpcn-luna-workflow/docs/architecture_proposals/README.md`,
`tpcn-luna-workflow/docs/architecture_proposals/ACP-TEMPLATE.md`, and
`tpcn-luna-workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` are absent at those
exact paths. The available repository counterparts under `workflow/`
(architecture contract/changelog, workflow, acceptance criteria, proposal
README/template and handoff template) were consulted. No architecture
decision depends on missing-path contents here; this review makes no new
A01–A15 compliance claim.

## 4. Validation record and limits

| Procedure | Result |
|---|---|
| Branch, `HEAD`, origin branch, parent, tracked diff and staged diff | **PASS:** expected revision/parent; tracked and index diffs empty at review start. |
| Probe/wrapper raw hashes, Git blobs, and all six tree paths/blobs | **PASS:** exact values recorded in §1. |
| Static embedded-literal extraction and SHA-256 | **PASS:** 6,583 ASCII bytes; digest recorded in §1; no source evaluation. |
| Corrected manifest input and correction-artifact hashes | **PASS:** all declared checkout hashes cross-checked; manifest raw SHA recorded in §2. |
| Protected untracked file hashes | **PASS:** both match §1 and remain untouched/unstaged. |
| Lane C/Race, B1, D1, E1, procedure, frozen RP-2 contract, R2 and owner decisions | **Reviewed statically;** dispositions in §3. |
| Probe/wrapper execution or import, compilation, preflight, tests, native APIs, token/job/process/thread creation, runtime qualification | **NOT PERFORMED.** |
| Publication, staging or commit | **NOT PERFORMED.** |

An initial PowerShell digest-helper attempt used a .NET API unavailable in
the installed PowerShell/.NET version and did not produce a hash. The
read-only extraction was then repeated with the available SHA-256
`ComputeHash` API and produced the matching literal byte length/digest above.
No target source was executed.

## 5. Final disposition and next bounded gate

**R2 narrow review:** PASS for the requested exact-byte identity review and
the two Lane C/Race corrections from R1. No additional exact-byte correction
pass is required for those two corrected statements.

**Integrated package:** BLOCKED. B1 still requires an explicit owner
resource-policy decision or separately reviewed amendment. E1 still
requires a complete, independently supportable worst-case evidence-fit
argument under the unchanged 1 MiB cap. These are distinct from this review's
acceptance of the corrected static Lane C wording.

**Next bounded responsibility:** project owner must resolve the resource
profile; resource/evidence owner must specify a complete bounded schema and
all-representation maximum, including the alert/finalization boundary; Luna-0
must independently review any exact successor package. A separate exact
owner grant is required before any future preflight or execution. Until
those gates close, preserve **BLOCKED / NOT AUTHORIZED**.
