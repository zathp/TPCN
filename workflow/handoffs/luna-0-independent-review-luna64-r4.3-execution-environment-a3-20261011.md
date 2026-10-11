# Luna-0 - Integrated Independent Review: Luna-64 A3

**Identifier:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A3`

**Final verdict:** **BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE**

**Architecture decision:** **NO QUALIFIED EXECUTION ENVIRONMENT**

**Date:** 2026-10-11

Four separate read-only Luna-0 Architecture Guardian reviewers, none of whom
authored the decision package, returned the final verdict above. This record
integrates their evidence, limitations and clarifications. No selected
architecture, infrastructure setup, qualification, corrective execution or
scientific rerun is approved.

## 1. Exact reviewed package and publication baseline

Baseline: `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c`, the published A2
governance commit. Local and remote governance refs matched that revision at
reconnaissance. Reviewers checked local Git objects; their reviews are not
separate fresh remote audits.

| Artifact | Reviewed CRLF checkout SHA-256 | Canonical LF Git-content SHA-256 |
|---|---|---|
| [A3 decision](luna-0-luna64-r4.3-execution-environment-a3-20261011.md) | `C5CB582C54ECEEAFC48256439FF034351DAD1776BD0D911CE45FFF2DA48FC66B` | `B0E357C52DF1A37ED4585A27D3DE3FAD6D54D3B6011189B5DA004A5DEFAABEFE` |
| [A3 platform evidence](luna64-r4.3-execution-environment-a3-evidence-20261011.json) | `F8685013351DB94848AE7A27CE0659A0EB4596F8255B12F5A95053F30A605FB7` | `52F1946DA40A4E90D85ADCA42F0E83C1F851E7B8173C84F1CCE95763DE38186E` |

All four reviewers confirmed these identities. The two reviewed files remain
unchanged after review. The workflow entry and this integrated review are
publication closure, not part of the pinned architectural proposal review.
The workflow appeared as an orchestrator-owned unstaged change during review;
reviewers accurately did not claim to validate it.

## 2. Independent reviewer records

### Resource enforcement and OS semantics

Reviewer `81101993-27f2-4f61-8f37-cd071b6ac9fd`.
Verdict: **BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE**.

Independently checked Windows metadata, frozen CLI-call count and official
Microsoft/Linux documentation. Confirmed hard-working-set maximum flag is
real, and the conditional arithmetic `4 * 134217728 = 536870912` is valid
only with continuous complete membership, hard limits and bootstrap coverage.
No before-allocation or inherited-hard-flag proof exists. Job commitment,
active count and affinity are documented controls, not proof of the original
aggregate working-set/strict time policy.

Native job CPU limits are periodically checked user-time limits. Full user
and kernel accounting, including terminated job members, is measurement;
nested aggregates must not be double-counted. No finite worst-case watchdog
observation-to-cessation delay is established.

Official pages were freshly retrieved using curl with certificate revocation
checking disabled. No revocation-validation or runtime-enforcement claim is
made. The reviewer did not repeat the complete scientific inventory.

### Bootstrap containment and failure behavior

Reviewer `a60737a4-f3ec-46e4-8376-3072136cab8a`.
Verdict: **BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE**.

Independently queried platform metadata and retrieved official Microsoft
assignment, process-creation, job, termination, Hyper-V and WSL documentation.
Fresh web retrieval succeeded without disabling revocation checks; retained
orchestrator captures still carry their separately disclosed retrieval limit.

Confirmed creator/self-assignment cannot retroactively cover startup; suspended
creation does not prove zero earlier allocation. Active process limits do not
deny out-of-job broker work. Last-job-handle close addresses some crash paths,
not living hangs or leaked/inherited/reopened handles. No approved external
controller scope, complete guest/host boundary or bounded surviving failure
writer exists. Reserved evidence bytes are accounting intent, not guaranteed
retention after abrupt termination.

The reviewer did not repeat the full scientific inventory or CLI-call count.
No process containment, VM boot or shutdown experiment was conducted.

### Scientific protocol and frozen-test compatibility

Reviewer `36364464-6c06-4ff1-a619-c3a6a565cd68`.
Verdict: **BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE**.

Static inspection confirmed 20 negative validator CLI calls plus three
additional calls: 23 planned serial descendants in a complete successful pass,
not observed execution and not extra primary-test invocations. Early failure
may prevent later calls. No-descendants execution cannot preserve CLI
exit-status/stdio assertions; importing modules or using threads is not an
equivalent replacement for the three frozen commands.

The frozen test writes under `os.tmpdir()` and abrupt termination can bypass
its `finally` cleanup. Temp input files, captured stdio and final logs require
explicit storage scope; deletion does not excuse unaccounted peak usage.
Both new corrective tests remain absent; compatibility is unverified.

The original runner guards Windows/x64. Cross-OS execution changes that
assumption and needs separate review even with unchanged equations.
Scientific equations, reward/eligibility/deadline/order identities, six arms,
statistical and cost criteria, TRAIN/EVAL separation and Luna-63C isolation
are preserved specifications, not newly passing implementation results.
Retained source confirms immediate settlement after calculating `dueTick`;
matching historical pass hashes do not repair that defect or prove efficacy.

The reviewer checked platform metadata and retained official-document captures;
no fresh documentation fetch or runtime workload occurred.

### Governance and authorization boundaries

Reviewer `ca7d649a-afe5-4f6b-b246-b506e4dfb988`.
Verdict: **BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE**.

Independently verified predecessor ancestry, ten raw frozen-package identities,
32 inventory freeze identities using Stage-B mappings, corrective tree and
markers, static CLI calls, platform metadata and relevant Microsoft sources.
Parent authority is preserved, not expanded. A1/A2 blocked dispositions are
retained; A2 exact-review/publication discrepancy is correctly disclosed.
Reconstruction does not establish possession of the original reviewed artifact
or approval of published bytes.

The provisional qualification allowance is unapproved, unselected and
non-executable. It cannot exempt its own launcher/controller/time/storage
boundary or borrow authority from the unused parent allowance. Feature/quota
states remain unknown, not disabled. No universal absence of other users'
or remote infrastructure is inferred.

## 3. Authoritative identity clarifications

The owner-approved parent hash
`8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369`
is the exact CRLF materialization identity. Its LF Git-content SHA-256 at
`439c0c930489ed032dc10950bbd51fe3f153d05a` is
`AB6DE19AF19E880F2294020A4F9B80E6F7D34E70C31E17A32577960A9127BB60`.
This distinction does not invalidate the owner-approved materialization or
expand it. Authorization commit remains
`0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`.

A1 publication `d20aab249e42575ccc571c9c72153a3bb4b412db` retains the
BLOCKED verdict; its earlier reviewed draft is not its final publication hash.

A2 publication `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c` proposal blob
`86e18e4385bd4507c4290fdd3713d48b91198da9` has LF SHA-256
`9FAF922016726FBB5B1EAEBBC8B9488A293E99FC830738E02F3A9A9CD7D958AD`
and checkout SHA-256
`05C401518A74B1957697E6F12C8877E4D9F8F734A4A7B1432CDF3C9520AE835A`.
Neither is the recorded reviewed proposal hash
`E00B75004D3085EFDA60D7163D57153F2FCB2D089162574358794BBA54145591`.
CRLF reconstruction plus two spaces on header lines 3-9 reproduces that hash;
the difference is not normalization alone. A2 remains unmodified and blocked.

Original content freeze `64a214e310de3b982b90a8ad215598bc1e9f8b1c`,
governance closure `ea1b10456cbf4ca726e473076d239a4f6e53b9c7`,
manifest hash `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`
and pilot closure `515dde66f37ca67c44a39f02e13f2e59b2f10d1d` are preserved.

## 4. Binding review clarifications for any successor

These refine the blocked analysis, not release an execution specification:

1. A successful termination API return is not verified cessation.
   [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
   is asynchronous when called externally; pending I/O must complete or be
   cancelled. [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)
   does not create a documented precise cessation deadline. A successor must
   reconcile exit/completion or report incomplete, not equate a request with a
   strict CPU/wall bound.
2. [Stop-VM](https://learn.microsoft.com/en-us/powershell/module/hyper-v/stop-vm?view=windowsserver2025-ps)
   `-Force` may allow five minutes for guest shutdown and is not equivalent to
   `-TurnOff`. Abrupt power-off risks evidence loss; neither establishes a
   documented host-side completion bound here. No shutdown command was run.
3. [NTFS quota limits](https://learn.microsoft.com/en-us/windows/win32/fileio/disk-quota-limits)
   charge file-owner SID data-stream lengths, not allocated-cluster usage or
   simply a directory's ordinary file lengths. Compression, alternate streams,
   ownership, excluded metadata, other volumes and temporary/log destinations
   need exact policy. The proposal's generic requirement to define quota
   accounting is resolved by this clarification; no quota was configured.
4. The validator imports `buildSchema` from the frozen schema-generator module.
   The import does not execute its guarded CLI write path or a benchmark
   generator. A future allowlist must preserve that dependency, rather than
   deny every module whose name contains "generate".
5. The 23-call figure is planned source behavior of a complete successful first
   test, not measured descendant completeness. Future test compatibility and
   resource accounting must retain those calls and their temporary writes.

## 5. Final resource and authorization disposition

No current candidate satisfies complete pre-start memory coverage, strict
aggregate user-plus-kernel CPU and monotonic wall cessation, completely
mediated artifact bounds, independently bounded failure cleanup, and frozen
test compatibility. OS/API support and hardware virtualization capability are
not installed infrastructure, runtime qualification, or 512 MiB guest viability.

The parent budget is unchanged and retained as unused: one supervisor
invocation, three primary tests, zero retries, 512 combined synthetic records,
one logical CPU, 120 CPU seconds, 180 wall seconds, 536870912-byte aggregate
peak working set, 5242880 artifact bytes. Marker/artifact absence is retained
evidence, not proof that no unrecorded external process ever ran.

The provisional future qualification request is distinct: one invocation,
16 resource cases, 128 combined records, four active processes including
launcher/controller, one logical CPU, 120 aggregate user-plus-kernel seconds,
180 wall seconds, conditional 536870912-byte commitment with fully declared
outer scope, 5242880 artifact bytes with 65536 reserved inside the cap, zero
retries. It remains non-executable and unapproved. A candidate-specific gate
must first resolve its own containment and cutoff dependencies; success would
not automatically authorize corrective execution.

**BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE.**

The original pilot remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**,
not a scientific efficacy result; 5,184 episodes / 20,736 receptions remain
exhausted. Scientific rerun is disabled. Parent owner approval and reject-only
second-origin policy survive unchanged, but corrective execution is blocked.
No A3 owner approval, infrastructure setup, qualification, production/core,
ACP, architecture promotion or Luna-63C modification is authorized.

## 6. Validation, publication and next role

Actual validation: hashes, local Git-object ancestry, public-document inspection,
read-only platform metadata, static source/golden inspection, JSON parsing
and governance diff checks. All supervisor qualification, corrective tests,
VM/container/distro starts, scientific reproduction and efficacy measurements
are **NOT RUN**. Reviewers made no edits and did not delegate.

The publication commit contains this review, the two unchanged reviewed
artifacts and the authoritative workflow closure; its exact commit and
Git-content hashes are reported after commit/remote verification, avoiding a
self-referential hash or containing-commit claim.

Next role is Luna-0, only if separately requested: identify a specific
administrator-controlled environment and independently review a complete
resource policy, executable/descendant compatibility, bootstrap, cutoff and
storage boundaries before requesting owner approval. No follow-up invocation,
installation or experiment is automatic. Integration remains blocked.
