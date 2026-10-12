# Luna-0 Independent Review — Luna-64 A6 Owner-Policy Reconciliation R1

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-OWNER-RECONCILIATION-R1`  
**Integrated verdict:** **PASS — R1 READY FOR GOVERNANCE PUBLICATION**  
**A6 technical verdict:** **BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE**  
**Reviewed R1 proposal checkout SHA-256:** `A619E3A4361B712471B8C3A7FD2AA784992ED6B4F5F0E218ED0449B16144319D`  
**Review scope:** Independent read-only review of governance, resource-policy semantics, trust boundaries, and publication provenance. No supervisor, qualification, host/guest control, corrective test, or scientific workload was executed.

## 1. Reviewed boundary and source authority

The review examined the R1 owner-policy reconciliation at the exact checkout
SHA-256 above, its identity manifest, the corresponding workflow entry, the
three immutable A6 candidate artifacts, and the applicable path-specific
Git attributes.

The owner decisions D1-D6 are treated only as decisions supplied by the
repository owner in the 2026-10-11 task conversation. No independent
signature or external owner-authentication artifact was provided. The review
does not infer owner approval from technical feasibility, prior diagnostics,
or reviewer consensus.

The frozen R4.3 manifest SHA-256 remains
`62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
The content-freeze and governance-closure commits remain
`64a214e310de3b982b90a8ad215598bc1e9f8b1c` and
`ea1b10456cbf4ca726e473076d239a4f6e53b9c7`. A5 package/closure commits
remain `12f84a41fe7c91c17c5df8e975fce24efbadf9ad` and
`b758b411e568b41c516228e7d3bdff26058114cc`; A4 package/closure remain
`7bd440565c38dee81ace3606fde3fb686de6a0ef` and
`f86c25844a4863ac57cd6634f364c28bcf2f511f`.

R1 preserves the frozen scientific protocol, original corrective owner
authorization, accepted reject-only malformed second-origin policy,
A1-A5 findings, A6's **BLOCKED** technical verdict, the original pilot
**NOT SUPPORTED** verdict, the unused parent corrective allowance, and
Luna-63C isolation. It authorizes design-only work; it does not authorize
infrastructure changes, qualification execution, corrective execution, or
scientific work.

## 2. Independent review scopes and results

Three reviewers considered distinct bounded scopes and returned PASS on the
final corrected R1 draft:

| Reviewer | Independent scope | Result |
|---|---|---|
| Reviewer A | Owner-decision attribution, predecessor governance, A6/frozen-protocol preservation, authorization and workflow claims | **PASS — no blocking governance issue.** Confirmed the distinct R1 policy-reconciliation result and A6 technical block; clarified that a mistaken closing sentence in the initial review response was a wording error, not a disposition change. |
| Reviewer B | Memory and swap policy, cumulative CPU accounting, wall-stop stages, artifact alternatives, and qualification budget | **PASS — R1 publication only.** Initially identified an undefined CPU accounting start and an inconsistent implied artifact-mediator cost. R1 now defines the fresh-empty-cgroup baseline, measured interval, included/excluded CPU, and the conditional treatment of any separately authorized mediator. Both corrections passed follow-up review. |
| Reviewer C | Trusted boundary, D5 non-network control, D6 infrastructure authority, Git attributes, byte provenance, and publication inventory | **PASS — no blocking boundary/provenance issue.** Confirmed owner-supplied capabilities are not presented as reviewer-executed tests; six path-scoped `-text` rules preserve exact A6/R1 handoff bytes without altering the repository-wide `text=auto` policy. |

The independent reviews are documentary/design reviews. They are not runtime
qualification, independent reproduction of host/guest behavior, or evidence
that any proposed enforcement control works.

## 3. Integrated findings

### Owner-policy reconciliation

The R1 handoff accurately limits each decision:

- **D1:** the Linux cgroup memory substitution is approved for qualification
  design only. The proposed 512 MiB cgroup-accounted limit is explicitly
  distinguished from Windows aggregate peak working set; no runtime
  enforcement is claimed.
- **D2:** `130.1` guest CPU seconds and the `170/171/180`-second stages remain
  unverified targets, not guaranteed deadlines. The CPU accounting boundary,
  clean baseline, start/end samples, in-scope descendants, and exclusions
  are now explicit. Host/PID 1/VM-boot CPU is separately logged and may not
  be silently counted as zero.
- **D3:** simpler artifact alternatives are evaluated first; no FUSE
  filesystem or daemon is selected or authorized by R1. The exact aggregate
  logical high-water-byte requirement is not replaced by allocated-block or
  post-run measurement. If a later authorized artifact mediator is used,
  its CPU must be included or separately budgeted.
- **D4:** the proposed 12-case, 240 guest CPU-second, 600-second wall,
  768 MiB outer-memory, 6 MiB combined-payload/evidence, one-start,
  at-most-one-TurnOff, zero-retry allowance is for planning only. The
  workload CPU scope remains explicitly unconfirmed for execution.
- **D5:** authenticated non-network host/guest control is mandatory and
  unresolved. Disconnected networking, disabled Guest Service Interface,
  host shutdown integration, or Hyper-V feature availability alone are not
  represented as proof of a secure channel.
- **D6:** no infrastructure changes are authorized. The future allowlist
  is expressly a proposal and requires a new exact owner authorization,
  resource budget, and independent prereview.

### Remaining technical blockers

R1 does not resolve the A6 enforcement contract:

1. No authenticated non-network host/guest protocol has been selected or
   qualified.
2. No simpler filesystem mechanism has been shown to enforce the frozen
   aggregate logical high-water-byte limit across all direct temporary-file
   paths, sparse files, and unlink/recreate behavior.
3. The 130.1 CPU-second and 180-second wall targets have no demonstrated
   worst-case termination guarantee. `cpu.max` or a measured trial would
   not establish such a lifetime bound.
4. The 768 MiB outer-memory and 6 MiB combined payload/evidence limits, and
   the excluded PID 1/VM-boot CPU scope, still require exact operational
   measurement definitions and owner confirmation before any execution.
5. The 600-second qualification wall origin is a candidate only; the exact
   12 synthetic case identities and commands are not fixed by R1 and must be
   approved before execution.
6. No qualification case has been run. No infrastructure control has been
   installed or tested.

These are unresolved evidence, implementation, and owner-policy gates; the
review did not establish an engineering impossibility. R1 does not advance
automatically to A7.

## 4. Git and byte-provenance review

Before path-scoped rules were added, Git's `text: auto` clean filter would
have changed the CRLF A6 checkout bytes in the Git objects. R1's six exact
`-text` entries cover the three A6 artifacts and three R1 handoffs. The
repository-wide `* text=auto` rule is unchanged. The A6 raw checkout
SHA-256 identities were rechecked unchanged; their Git-object SHA-1 values
now match the unfiltered object IDs recorded in the R1 manifest.

The modified workflow remains governed by its existing text normalization
rule. Its checkout materialization and Git object are distinct; the
published commit is the canonical workflow identity. No frozen R4.3 file,
A6 content file, or scientific artifact was rewritten to resolve this
provenance issue.

## 5. Validation and execution record

| Check | Observed result | Classification |
|---|---|---|
| Required predecessor commit objects and A5 ancestry | Verified in local Git; A5 package is an ancestor of the recorded baseline | **PASS — repository provenance only** |
| Supplied A6 checkout SHA-256 values | All three match the R1 manifest before and after R1 edits | **PASS — exact checkout bytes** |
| Git raw/filtered object identity for protected A6/R1 artifacts | Matches after exact path-scoped `-text` rules; attributes report `text: unset` for the protected files | **PASS — publication-byte control** |
| R1 manifest JSON parse and planning-only/CPU-scope assertions | Passed | **PASS — document structure only** |
| `git diff --check` | Passed | **PASS — whitespace only** |
| Windows/Ubuntu diagnostics | Owner-supplied; not independently re-executed | **NOT RUN by reviewer** |
| Hyper-V/systemd/cgroup enforcement or authenticated control | Not installed or tested | **NOT RUN** |
| Qualification cases, corrective tests, or scientific workload | Not run | **NOT RUN** |

Passing provenance and document checks do not establish cgroup containment,
memory enforcement, CPU or wall deadlines, artifact enforcement, protocol
efficacy, or scientific benefit.

## 6. Verdict and next bounded action

**PASS — R1 READY FOR GOVERNANCE PUBLICATION.**

This PASS means only that the owner decisions have been faithfully recorded,
the governance boundaries and predecessor findings are preserved, the
proposal is internally consistent for design-only continuation, and the
reviewed handoff bytes have a disclosed publication identity. It is not
**PASS — A6 QUALIFICATION READY**, resource-policy execution approval, or a
scientific verdict.

**A6 remains BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE.** The original pilot
remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not an efficacy
result. The unused corrective allowance is unchanged. Luna-63C remains
isolated and unchanged.

The next bounded step is read-only design and independent prereview to select
an authenticated offline control path, resolve exact aggregate logical-byte
enforcement against the simpler alternatives, specify any remaining
qualification-budget measurement semantics, and confirm the explicit CPU
scope. Any infrastructure change or execution needs a separate exact owner
authorization. No A7 or scientific workload is authorized by this review.
