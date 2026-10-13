# Luna-0 Independent RP-2B Corrective Reconciliation Review R1

**Review date:** 2026-10-12  
**Reviewed revision:** branch `governance/luna64-r4.3-freeze-20261010`,  
`HEAD = origin/governance/luna64-r4.3-freeze-20261010 = 96fb4aec100578db6939136b4ed7985478f18bb8`  
**Overall verdict:** **BLOCKED — CORRECTION REQUIRED**  
**RP-2B execution:** **NOT AUTHORIZED**  
**Downstream qualification:** **NOT AUTHORIZED**  
**Publication:** **NOT AUTHORIZED / NOT PERFORMED**

This is an independent static adjudication, not an execution grant, runtime
qualification, publication approval, contract amendment, or architecture
change. I independently inspected the corrective reports, matrix, source,
frozen RP-2 contract, R2, owner decisions, direct-interpreter design,
authorization materials, and historical six-path allowlist. No candidate was
edited. The only file created by this review is this handoff.

## 1. Identity and boundary

The requested branch and `HEAD` match; the fetched origin ref resolves to the
same commit. The probe and wrapper raw checkout identities and commit-tree
blobs independently match the corrected manifest:

| Source | Checkout SHA-256 | `HEAD` blob |
|---|---|---|
| `scripts/luna65_phase2a_rp2_compatibility_probe.py` | `B8F669C68ED5768E4126FFA87E855002A5E7E5E116999E81E4AAE1CA69CE2427` | `e76c2abf728072315c779da990cf9a5e445f1a00` |
| `scripts/luna65_phase2a_rp2_outer_wrapper.ps1` | `F7C39C0FC849F61AFFF71A07AC8DCC7BDBEBA91D9971B44BCCF96B0C01ABE2A7` | `3c29b21952e08100da2779c1a7fb02dcc930acdf` |

I statically extracted the embedded ASCII `SYNTHETIC_LITERAL`, normalized
source CRLF to Python's logical LF string representation, applied the source
`.lstrip()` behavior, and independently verified **6,583 bytes** and SHA-256
`D9EC540BCEA9326C67A791DA6C59FC11357C00396B707EEB9FE278FCD08BF2A0`.
This is text identity only, not interpreter, quoting, or Windows evidence.

All six historical RP-2A publication paths exist in the exact `HEAD` tree:

| Path | `HEAD` blob |
|---|---|
| `scripts/luna65_phase2a_rp2_compatibility_probe.py` | `e76c2abf728072315c779da990cf9a5e445f1a00` |
| `scripts/luna65_phase2a_rp2_outer_wrapper.ps1` | `3c29b21952e08100da2779c1a7fb02dcc930acdf` |
| `workflow/docs/luna/LUNA_65_PHASE2A_RP2A_CORRECTIVE_R1_TRACEABILITY.md` | `646548764258ff252ffd6a386461a60671885dba` |
| `workflow/handoffs/luna-0-luna65-rp2a-corrective-r1-20261012.md` | `9e7cc656224d400030e9c50f98b058f46bc780fd` |
| `workflow/handoffs/luna-0-luna65-rp2a-implementation-review-20261012.md` | `cf4f267ae9deb95a7290baee3b8a66e4bb23079c` |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `4b5639effead056f54f815814bbeeb42e7dba07b` |

The corrected manifest is valid JSON and its added R7 owner-decision input is
correct: `workflow/docs/luna/LUNA_65_PHASE2A_R7_OWNER_DECISIONS_AND_PROFILES.md`
has checkout SHA-256 `9CA2E34DCC1F35BA72156B86C889365C2EB6873979E7863248594AF214169B73`
and `HEAD` blob `0759087811610f40c73de91d8662c28d8ebce54d`. I cross-checked
the manifest's source identities, all six tree paths/blobs, governing-input
hashes/blobs, prior-readiness input hashes, eight corrective-artifact hashes,
and protected-file hashes against the checkout/tree; all matched. Its current
SHA-256 is:

`C2A053DC7BB1481258FA0AE4D90DD3705432E021FC6F27D18F6FB29E412BFB60`

Manifest authorization and status fields are internally consistent with a
blocked package: execution, downstream qualification, and publication are
false; runtime/preflight/API-object creation are false; staging is `NONE`;
resource owner decision is `NONE`; `total_max_bytes` is null and
`worst_case_fit_established` is false. Option C is explicitly only the
reviewer recommendation, not an owner choice.

Protected pre-existing untracked files independently retain their expected
hashes and remain unstaged:

| Path | SHA-256 |
|---|---|
| `scripts/luna65_phase2a_supervisor.py` | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` |
| `workflow/handoffs/luna-0-luna65-s1b-final-execution-authorization-record-20261012.md` | `BB9134CB7FF1813D495575FA80F912EEFB6E6A7C7A86F720CDAD829CAC925451` |

At review, there were no tracked diffs and no staged changes. Corrective
materials and the protected records are untracked; “no tracked diff” is not a
clean-worktree claim. No source or frozen contract change is present.

## 2. Independent adjudication of B1, C1, D1 and R2

### B1 — resource profile conflict: confirmed blocker

The frozen RP-2 §5/accepted D-RP2-OUTER-1 design is **64 MiB
`JobMemoryLimit` job-memory charge**, 8-process backstop, 5-second
job-user-time backstop, 10-second active period, up to 5 seconds cleanup,
20-second outer limit, zero retries, and 1 MiB logical evidence cap. The
probe source configures the 67,108,864-byte job charge and 50,000,000
100-nanosecond (5-second) job-user-time limit; the wrapper implements the
10/5/20 timing path.

R2 accepts **268,435,456 bytes / 256 MiB**, **120-second aggregate
job-wide user-plus-kernel CPU**, **120-second elapsed wall**, and 1 MiB
retained artifacts for **Phase 2A qualification design only**. R2 §3
explicitly does not amend Phase 2B. These are not equivalent metrics:
Job Object charge is not aggregate live private commit or working set;
job-user-time is not aggregate user-plus-kernel CPU; elapsed wall is not CPU;
termination request is not cessation. The resource reconciliation and
decision candidate correctly preserve the distinction and present A/B/C as
unselected options. No owner choice exists. The manifest's requested and
frozen values agree with these governing inputs.

**Disposition:** B1 remains blocked pending explicit owner selection or a
separately authorized, reviewed RP-2B contract/source amendment. The R2
values must not be silently applied to RP-2B; the existing source must not be
represented as satisfying the requested 256/120 profile.

### C1 — original Lane C: PASS rejected; corrected evidence mostly improves it

The original `rp2b_lane_c_native_race_readiness.md` is materially corrupted:
independent byte inspection found **9 NUL bytes and 16 other
non-whitespace control bytes**. The claim that the AMD64 `PSS_HANDLE_ENTRY`
is 128 bytes is contradicted by the source structure and its explicit
`sizeof(PSS_HANDLE_ENTRY) != 136` guard. The original's claimed 33 native
declarations is also wrong: the wrapper's `$api` list contains 34 entries.
The other categorical ABI, graceful-degradation, chain-wide inheritance,
worker cancellation/join, deadline, and termination claims exceed what
static source inspection can prove. Its original PASS is not accepted.

The corrected Lane C and race matrix appropriately withdraw that PASS,
distinguish source branches from runtime guarantees, and preserve conditional
classification rather than claiming executed outcomes. I verified that the
race matrix explicitly covers timeout/cessation ordering, truncation during
termination/drain, process/job/worker termination failure, missing Low and
Medium evidence, cleanup/finalization after cessation, and contradictory
observers. Its required rule is correct and non-negotiable: **missing or
unreliable required Low cessation evidence remains
`RP2_UNKNOWN_FAIL_CLOSED` with an operator alert**, regardless of Medium
signal/EOF or termination request. Alert delivery/retention is not proven.

**N2 adjudication and required Lane C/race-matrix correction:** their final
“Source/profile/authorization contradiction” row incorrectly treats both
observations as unresolved mismatches:

1. Probe `BASELINE = f47c48a947e48867c629817fa1031cb93729e440` equals the
   reviewed source commit's actual parent (`HEAD^`) and the RP-2A handoff's
   `base_revision`. It is source-base provenance, not a disagreement with
   the manifest's reviewed `HEAD` `96fb4aec100578db6939136b4ed7985478f18bb8`.
   The probe emits this field as `baseline`; source identity is separately
   bound by the wrapper/manifest hash and current revision.
2. The historic RP-2 contract text retains the venv-chain profile, while
   later owner decision D-RP2-DIRECT-1 explicitly accepts the hash-bound
   direct-base executable **for diagnostic design only**. The source's direct
   base choice therefore should not be described as an unadjudicated design
   mismatch. That owner decision is not a contract amendment, source/runtime
   qualification, or RP-2B execution grant. A future grant must explicitly
   bind the accepted direct-base design and exact source/literal identities.

**Precise fix:** replace the final matrix row and the matching Lane C
conclusion with the two qualifications above. Retain a future-grant mismatch
as `RP2_CONTRACT_DEFECT` only if that grant conflicts with its bound design or
source. Do not modify those candidates in this review. This is a remaining
corrective-document defect, not evidence that runtime was tested.

The matrix's “cleanup after apparent cessation” obligation is otherwise
present in the normal-cessation/finalization row and the cleanup/final-artifact
failure row. The report correctly distinguishes confirmed cessation with
incomplete finalization (at least PARTIAL under the frozen text) from unknown
cessation (UNKNOWN); it also calls out the source's conservative finalizer
UNKNOWN behavior as a question rather than presenting it as observed behavior.

### D1 — original Lane D and corrected Lane D: original PASS withdrawn

The original Lane D contains incorrect published LF digests, prior-review
digest and protected-file digests/path; it mislabels the 64 MiB job-memory
charge as working set, uses noncanonical classifications, includes a
run-ready command and `ExecutionPolicy Bypass`, supplies a mismatched
run-ID/leaf convention, and recommends process-name/PID termination. Its
~774 KiB arithmetic is not a reproducible worst-case derivation. Its claim
that the earlier parameter-binding attempt had no process/token/filesystem
side effects exceeds the historical record's forensic limit.

The corrected Lane D audit appropriately withdraws its readiness conclusion,
corrects those identities/labels/classes, preserves the incident's stated
forensic uncertainty, and rejects manual PID/name termination. The successor
four-phase operator procedure contains no command or invocation template,
keeps runtime placeholders unresolved, prohibits this-cycle preflight and
execution, and does not silently continue from Phase 0. This is an acceptable
static correction boundary, **not** authorization/readiness or proof that an
alert can be delivered.

## 3. Evidence ceiling and TOTAL_MAX

The corrected evidence-bound report properly refuses Lane D's “typical”
volume arithmetic and distinguishes files, in-memory/encoded/decoded copies,
probe reservation, console output, and external governance material. The
governing constants are 1,048,576 total bytes, 917,504 payload bytes,
131,072 finalization reserve, and 393,216 probe reservation. Those constants
are ceilings/reservations, not a proof of fit.

Its required formula,
`TOTAL_MAX = max_t [D(t) + M(t) + P(t) + X(t)]`, cannot currently produce a
finite, defensible number: mandatory record/schema maxima and some counts
(including outer records and final report growth) are not fully specified;
complete simultaneous representation bounds are not reconciled; the
mandatory alert and final summary/digest are printed directly to console
outside the charged artifact writer; external authorization/provenance
material has no defined inclusion boundary/schema; and failure/finalization
paths may leave incomplete artifacts. Individual record and write-time
caps do not demonstrate that all mandatory evidence fits. The operator alert
is required, but its delivery and retention cannot be presumed from the
source call to `Console.Error.WriteLine`.

**Disposition:** retain **BLOCKED — EVIDENCE FIT NOT ESTABLISHED**. Do not
fill `total_max_bytes`, infer fit from runtime counters, or raise the 1 MiB
cap. A later proof must bound every required count/field/serialization and
every simultaneously retained representation, including console/finalization
output, under the unchanged cap.

## 4. Corrected manifest and corrective artifact identities

The following raw checkout SHA-256 values were independently recomputed for
the eight corrective artifacts recorded by the corrected manifest. They are
untracked and unchanged by this review:

| Corrective artifact | SHA-256 |
|---|---|
| `workflow/handoffs/rp2b_resource_reconciliation.md` | `7305637DC037CFAA8E8E463730BE1B960FFE545F06B291CEE5F0D8B1EC61F9D6` |
| `workflow/handoffs/rp2b_resource_owner_decision_candidate.md` | `374B5843C4EEE67D05DC3A0DBD9972E9419E7889A8AD9AE8DB541044AC3244C6` |
| `workflow/handoffs/rp2b_lane_c_corrected.md` | `1F27A7C9E579FFA3DAD823ADA252EBC62D7B9439DA340CCF5F8382D18B9BCD8D` |
| `workflow/handoffs/rp2b_race_classification_corrected.md` | `A72799A5BF7430B235D3707C53514C22EB712D2981835E65B22A9C15620175AF` |
| `workflow/handoffs/rp2b_lane_d_corrected.md` | `4E660BCDB13E553C14591BDC30DF7DEB0221253BDD5000ED8BC15DC65A458894` |
| `workflow/handoffs/rp2b_operator_procedure_corrected.md` | `9032D8016C339F71016FA4029CEC73088055539636923E46EEF76C1CB88DA30D` |
| `workflow/handoffs/rp2b_evidence_worst_case_bound.md` | `44F444046C958AAABED9246B012CD0A2C74A8E95D45B4E108594DC9F97F4FE4C` |
| `workflow/handoffs/rp2b_corrective_reconciliation_matrix.md` | `7CC090496513B46F39042BA9992A58071A2B83271DB2E34039478DF621B4934C` |

The current corrected manifest hash is listed in §1. It is valid JSON; its
path/hash/value/authorization claims checked out, including the user's newly
added R7 provenance pair. Its execution/downstream/publication flags remain
false. No option A/B/C is represented as an owner selection; the owner field
is `NONE`. No other candidate file changed during the review.

## 5. Lane dispositions and architecture boundary

| Work item | Independent disposition |
|---|---|
| Lane A | Prior **PASS — static scope only**. No runtime isolation/security qualification follows. |
| Lane B original | **BLOCKED** on the resource/profile conflict. |
| Lane B-R | **BLOCKED — owner decision required**; its A/B/C choices are proposals, none selected by owner. |
| Lane C original | **PASS rejected as sufficient evidence**; report is corrupted and materially overclaims static evidence. |
| Lane C-R / race matrix | Improved and substantially source-cited, but **correction required** for the baseline/direct-design row described in §2. Low-missing UNKNOWN rule and required scenario coverage are preserved. |
| Lane D original | **PASS withdrawn/rejected**. |
| Lane D-R / operator procedure | Corrective audit and four-phase no-command boundary are materially sound as static submissions; they do not close B1/E1 or authorize execution. |
| Lane E-R | **BLOCKED — EVIDENCE FIT NOT ESTABLISHED**. |
| Integrated matrix/package | **BLOCKED — CORRECTION REQUIRED**. |

No A01–A15 clause or computational interface is changed; no ACP is proposed
or accepted. The RP-2 source review is a diagnostic governance question, not
TPCN-core evidence or a hardware-equivalence claim.

## 6. Validation actually performed

| Procedure | Result |
|---|---|
| Read branch, `HEAD`, origin ref, tracked diff, staged diff, status and six-path tree | **PASS:** branch/HEAD/origin match; no tracked or staged changes; six paths/blobs match. |
| Read-only raw SHA-256 for both source files, corrected manifest, eight corrective artifacts, governing inputs and protected files | **PASS:** values recorded above / cross-checked against manifest. |
| Parse corrected manifest as JSON and cross-check its declared source/tree/input/candidate/protected identities and flags | **PASS:** all checked identities/values match; no execution authority. |
| Extract/hash embedded synthetic literal as static text | **PASS:** 6,583 bytes; SHA-256 recorded in §1. |
| Inspect original Lane C byte stream and source `PSS_HANDLE_ENTRY` guard | **PASS:** 9 NUL, 16 other non-whitespace controls; source guard is 136 bytes. |
| Static source inspection of `$api` list and console/finalization/cleanup branches | **PASS:** 34 API declaration tuples; console alert/final lines are outside artifact writer; source paths are not runtime guarantees. |
| Probe/wrapper execution, target import, preflight, tests, native/API call, token/job/process/thread creation, runtime probing, publication, staging or commit | **NOT PERFORMED**, as required. |

No runtime, Windows behavior, cessation, API/ABI operation, operator alert
delivery, resource qualification, or publication success is claimed.

## 7. Next bounded gate

1. **Lane C / document owner:** correct only the final source/profile
   contradiction text in `rp2b_lane_c_corrected.md` and
   `rp2b_race_classification_corrected.md`, distinguishing parent/base
   revision from reviewed `HEAD`, and recognizing D-RP2-DIRECT-1 as accepted
   design-only authority. Preserve all runtime limits and the mandatory Low
   UNKNOWN/alert rule. Freeze new hashes; do not edit source or the contract.
2. **Project owner:** explicitly select the RP-2B resource policy or authorize
   a separately reviewed successor contract/source. The current
   recommendation C is not a decision.
3. **Resource/evidence owner:** establish exact-schema, all-representation
   worst-case fit under the unchanged 1 MiB cap, including console alerts,
   errors and finalization. If any required count/field remains unbounded or
   fit is not proven, remain blocked.
4. **Luna-0:** independently review the exact corrected successor package
   and any owner-authorized change. Only a separate future owner execution
   grant can authorize execution after readiness closes. No invocation,
   wrapper, preflight, test, target import, or runtime probing is authorized
   by this handoff.

**Final disposition: BLOCKED — CORRECTION REQUIRED.**
