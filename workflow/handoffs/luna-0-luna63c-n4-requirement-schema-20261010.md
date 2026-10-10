# Luna-0 — Luna-63C N4 certification requirement schema

**Disposition: N4 CERTIFICATION REQUIREMENT SCHEMA FROZEN.**
This freezes verification obligations only. N4 remains open; the independent
review gate is pending.

## Identity and authoritative inputs

| Item | Verified identity |
|---|---|
| Branch | `experiment/luna63c-stage-a-certificate` |
| Starting HEAD | `87179ba2f5da13da7bc70727e72c000de924ed80` |
| Fetched branch | `origin/experiment/luna63c-stage-a-certificate` at the same SHA |
| `origin/main` | `73aaa50f97ceab322907875ae4dcf23e7541c3b5` |
| Reviewed design revision | `3e7d31b9a527e908b21abee3766906084e7cd082` |
| Latest design handoff revision | `a303ebb835b72fdd01c86df478431b8638aacbb4` |
| Arithmetic-profile governance revision | `87179ba2f5da13da7bc70727e72c000de924ed80` |
| Latest published v2 certificate revision | `e10aad9dd2b4a3fbfd708ac656e89ace2cf20293` |

The design, execution contract, governance decision, v2 report, workflow,
changelog, and current untracked W/T/E handoffs were inspected. No prior
fixture-freeze blocked handoff exists in the repository at this baseline;
the prior blocked disposition is preserved in session history and the current
W/T/E reports. Existing untracked W/T/E files were left untouched and are not
treated as committed authority.

Repository search of the pinned source tree found no authoritative E1–E14
definitions. The separate ACP E1 terminology is unrelated. This governance
record therefore replaces the undefined requirement labels for this
certificate chain rather than reconstructing them.

## Frozen obligations

The dedicated
[N4 requirements artifact](../docs/luna/LUNA_63C_N4_CERTIFICATION_REQUIREMENTS.md)
freezes these fourteen verification-only obligations:

| ID | Definition |
|---|---|
| N4-A1 | Reproducibly identify and verify the reference environment against the MPFR/GMP profile. |
| N4-A2 | Construct every certified interval with directed outward rounding and a documented containment basis. |
| N4-A3 | Rigorously enclose every classification-relevant root/transcendental value with defining equation, bracket/proof, uniqueness/monotonicity where applicable, width, and bounded work. |
| N4-A4 | Check all frozen assertions at 256 and 512 bits; require overlap/classification/timestamp agreement, escalate unresolved or inconsistent cases to 1024, otherwise block. |
| N4-A5 | Resolve each scientific boundary by certified mathematics, preserving exact tangency and reviewed crossing/terminal/expiry classification. |
| N4-A6 | Certify required quiet/terminal conclusions by analytic condition, containing interval, or certified transition root/time—not observation-window silence. |
| N4-A7 | Cover every frozen mathematical fixture checkpoint with mapped N4-A evidence; no omitted or deferred-to-Stage-B checkpoint. |
| N4-B1 | Accumulate released active time exactly in GMP integer multiples of `2^-1074`; no governing rounded binary64 sum. |
| N4-B2 | Map every certified event-time interval to one uniquely proven least-binary64 ceiling shared by both endpoints. |
| N4-B3 | Prove every positive causal delay is strictly after its processed cause, resolving sub-ULP cases before conversion. |
| N4-B4 | Establish event time source, cause, clock-domain membership, and required causal order for every scheduled event. |
| N4-B5 | Materialize governed deterministic precedence for every relevant equal-represented-time group. |
| N4-B6 | Certify expiry/lifecycle mapping and precedence, including coalescence where applicable; runtime enforcement remains N6. |
| N4-B7 | Cover every order-relevant frozen fixture event with time source, binary64 mapping, strict-future result where applicable, precedence, and expected ordinal rule. |

N4-A1–A7 and N4-B1–B7 are verification requirements, not scientific
semantics. The complete definitions, pass conditions, fixture mapping focus,
gate boundaries, and required fixture-freeze mapping fields are authoritative
in the linked requirements artifact.

## Gate relationships and preserved scope

- **N1:** mathematical witness/enclosure completeness. N4-A3/A5 consume
  relevant N1 evidence but do not close N1.
- **N3:** complete event-time mapping/ordering. N4-B certifies the arithmetic
  interface for N3 but does not replace or close N3.
- **N5:** immutable synthesized C0–C7 numeric expectation table; consumes
  completed N1/N3/N4 evidence and adds no new mathematics.
- **N6:** future runtime enforcement, Stage B only; not established by N4.

The repository-defined identities remain C0 neutral/no STORE, C1 neutral
RECALL, C2 entry/subthreshold boundaries and tangency, C3 supra-threshold
HOLD, C4 supra-threshold release, C5 unequal-HOLD replay, C6 ungated
reference, and C7 lifecycle/time edge cases. No equations, parameters,
fixture values, event semantics, `16+1+24+1=42` accounting, or arithmetic
profile changed.

## Changes and validation

Changed:

- `workflow/docs/luna/LUNA_63C_N4_CERTIFICATION_REQUIREMENTS.md`
- `.github/agents/luna-63c-mechanism.agent.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- this handoff

No numerical certification, Stage B, scientific fixture, W/T/E lane, or
Lane S/N5 work was run or resumed. No architecture clause or ACP changed.
No separate executable tests apply to this documentation-only schema.

The schema was checked against the arithmetic governance decision and
execution contract. `git diff --check` and independent Luna-0 review are
required before this handoff is final. Publication and remote verification
are recorded in the completion addendum below.

## Independent review and next gate

An independent Luna-0 review must verify requirement/profile compatibility,
unchanged fixture/scientific semantics, gate boundaries, and sufficiency for
the fixture-freeze mapping. Until that review returns PASS, the fixture-freeze
prerequisite does not resume. After PASS, a separately bounded C0–C7
fixture-freeze assignment may proceed; W/T/E resume only after that freeze
receives its own independent PASS.

Lane S/N5 remains blocked. Stage B remains blocked. No scientific fixture has
been executed.

## Publication completion addendum

Pending publication.
