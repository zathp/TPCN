# Luna-63C N4 certification requirements

**Status: N4 CERTIFICATION REQUIREMENT SCHEMA FROZEN.**

This document defines verification obligations for the already-authorized
Luna-63C reference arithmetic profile. It is not a numerical certificate,
does not close N4, and does not change the reviewed scientific design,
fixtures, equations, parameters, event semantics, or resource limits.

## Authority and scope

The governing scientific sources are the reviewed
[Luna-63C design](LUNA_63C_NONLINEAR_EXCURSION_DESIGN.md), its pinned
design/review identity `3e7d31b9a527e908b21abee3766906084e7cd082`, the
[mechanism execution contract](../../../.github/agents/luna-63c-mechanism.agent.md),
and the [reference-arithmetic governance decision](../../handoffs/luna-0-luna63c-reference-arithmetic-governance-20261010.md)
at commit `87179ba2f5da13da7bc70727e72c000de924ed80`.

The arithmetic profile remains MPFR C API 4.2.2 with GMP 6.3.0; outward
interval rounding; exact binary64 fixture/timestamp imports; exact active-time
accumulation in integer multiples of `2^-1074`; required 256-bit and 512-bit
checks; escalation to 1024 bits only when unresolved or inconsistent; at most
128 bisections per root; and no host `libm` for scientific transcendental
reference values. The profile itself is not evidence that any obligation
passes.

The repository-defined fixture identities remain C0 neutral/no STORE, C1
neutral RECALL, C2 entry/subthreshold boundaries and tangency, C3
supra-threshold HOLD, C4 supra-threshold release, C5 unequal-HOLD replay, C6
ungated reference, and C7 lifecycle/time edge cases. These obligations do not
relabel or extend those fixtures.

Earlier requests referred to `E1–E14`, but no authoritative definitions with
those labels were found in the pinned repository sources. Those labels are
superseded for this certificate chain by the distinct verification-only
identifiers `N4-A1` through `N4-A7` and `N4-B1` through `N4-B7`. No
requirement is inferred from the old labels.

## N4-A — certified reference arithmetic

N4-A concerns the reference arithmetic for the reviewed mathematical state,
roots, event surfaces, and terminal classifications. It does not certify a
future candidate implementation or relax the independent-oracle requirement.

### N4-A1 — Reference environment identity

Identify and verify the numerical reference environment used for certificate
computations. Record MPFR and GMP versions, arithmetic precision, rounding
modes, and relevant platform, ABI, library, and build/runtime identity where
material. State any unavailable identity information explicitly.

**Pass:** the actual computation environment is reproducibly identified and
matches the authorized profile. A wrapper package version alone is
insufficient evidence of the loaded MPFR/GMP versions.

### N4-A2 — Outward interval construction

For every certified interval, document the interval operation and its
containment basis. Lower endpoints use directed rounding toward negative
infinity where required; upper endpoints use directed rounding toward positive
infinity where required. Exact inputs must be imported without silently
rounding away their exact value.

**Pass:** every reference interval defensibly contains the mathematical
quantity it represents. Two ordinary round-to-nearest calculations are not
an outward interval proof.

### N4-A3 — Root and transcendental enclosures

For every root or transcendental quantity used in a scientific classification,
record its defining equation, interval/bracket, existence evidence, uniqueness
or monotonicity argument where applicable, enclosure width, and bounded
refinement work. Record endpoint signs or other proof obligations required by
the reviewed design.

**Pass:** the enclosure is tight enough to support every dependent
classification and required event-time conversion. This is the arithmetic
method's obligation; N1 witness completeness remains a separate gate.

### N4-A4 — Precision convergence and escalation

Evaluate every frozen scientific assertion at both 256 and 512 bits. Require
overlapping certified enclosures, the same resolved qualitative
classification, and the same scheduled binary64 timestamp whenever timing is
involved. If either result is unresolved or the two results disagree, refine
at 1024 bits and require overlap and resolved agreement there.

**Pass:** the assertion resolves under this protocol. If it does not resolve
at the authorized cap, mark it blocked; do not substitute midpoint agreement
or add unapproved precision.

### N4-A5 — Scientific boundary classification

Use the certified interval arithmetic and the reviewed analytic rules to
classify each relevant boundary, including strict subthreshold behavior,
directional crossing, exact tangency, terminal/quiet inclusion, and any
expiry-related mathematical boundary. Preserve exact equalities where the
design establishes them; do not manufacture a numerical margin for exact
tangency.

**Pass:** numerical uncertainty cannot change the reviewed classification.
For C2, the exact `A=2` tangency is not an upward directional crossing.

### N4-A6 — Terminal and quiet certification

For every fixture that requires a quiet or terminal conclusion, record the
mathematical basis: an interval wholly inside the reviewed terminal region,
an exact analytic terminal condition, or a certified root/time establishing
the transition. A finite observation window with no further simulated
activity is not sufficient.

**Pass:** quiet/terminal status follows from the reviewed mathematics and
certified evidence.

### N4-A7 — Complete fixture/checkpoint coverage

Map every mathematical-reference checkpoint in the subsequently frozen C0–C7
fixture inventory to the applicable N4-A evidence and its source artifact.

**Pass:** no required reference-arithmetic checkpoint is unspecified,
implicitly deferred to certificate-time invention, omitted, or delegated to
Stage B. This obligation cannot be evaluated as complete before the fixture
inventory is frozen.

## N4-B — binary64 event-time interface

N4-B covers only the interface from certified mathematical event times to
the binary64 event clock and the associated ordering semantics. Scientific
state remains in the governed reference arithmetic.

### N4-B1 — Exact active-time accounting

Interpret binary64 event timestamps as exact dyadic values and accumulate
released active-time durations as signed integer multiples of `2^-1074`
using GMP integer arithmetic. HOLD contributes no active duration. Do not use
rounded binary64 duration accumulation as the governing operation.

**Pass:** every active-time quantity used by the certificate is exactly
reconstructible from the governed timestamps and respects the reviewed clock
domain.

### N4-B2 — Real-time interval to binary64 ceiling

For every certified real-time interval `[t_L,t_U]`, determine the least
finite binary64 value greater than or equal to each endpoint.

**Pass:** both endpoints have the same ceiling, uniquely determining the
represented event timestamp. If their ceilings differ, that event remains
uncertified; do not guess or clamp.

### N4-B3 — Strict-future guarantee

For every positive causal delay, certify that the represented event timestamp
is strictly later than the actually processed cause timestamp. Resolve
positive sub-ULP delays in reference arithmetic before conversion.
`nextafter` may identify the uniquely certified ceiling but is not a fallback.

**Pass:** no positive causal delay collapses to the already-processed
timestamp.

### N4-B4 — Clock-domain and causal-order compliance

For each scheduled event, record its exact time source, event/cause identity,
clock domain, causal predecessor, and required order. Apply the reviewed
inclusive clock domain and event-order rules.

**Pass:** no scheduled event precedes its cause or violates the reviewed
clock-domain or causal-order constraints.

### N4-B5 — Equal-time precedence

For each relevant pair or group of events that share a represented
binary64 timestamp, record the participating event identities, shared time,
governed precedence class, and resulting ordinal relation. Apply the reviewed
internal-before-external rule, external delivery ordering, expiry precedence,
and the permitted re-arm-before-quiet tie as applicable.

**Pass:** every relevant equal-time ordering is determined by governed
semantics, not insertion order, dictionary order, or implementation accident.

### N4-B6 — Expiry and lifecycle boundary mapping

For lifecycle boundaries in the frozen fixtures, certify the expiry time,
timer/lifecycle boundary, output/expiry relation or coalescence, ingress
closure and terminal transition as applicable, using reviewed precedence.

**Pass:** lifecycle classification does not depend on accidental binary64
rounding or unspecified ordering. Runtime enforcement remains N6/Stage B and
is not established by this arithmetic certificate.

### N4-B7 — Complete scheduled-event coverage

Map every order-relevant event in the frozen C0–C7 inventory to its exact or
mathematical time source, certified binary64 mapping, strict-future result
where applicable, precedence treatment, and expected ordinal rule. The
fixture inventory freezes event identities and ordinal dependencies; N3/N4-B
certifies and materializes resulting times and ordinals.

**Pass:** no event needed for scientific interpretation remains unmapped.
The required mapping covers all scheduled events, not merely selected
boundary examples.

## Gate boundaries and fixture-freeze mapping

| Fixture | Required N4 mapping focus (not a fixture expansion) |
|---|---|
| C0 — neutral/no STORE | Neutral reference state and no unintended motion/output; any applicable lifecycle or event-time assertions. |
| C1 — neutral RECALL | Neutral-state classification, no RECALL-induced crossing, gate/event timestamps, and terminal behavior. |
| C2 — entry/subthreshold boundaries and tangency | N4-A3/A4/A5, N4-A6 where quiet/terminal applies, and applicable N4-B mappings; preserve exact tangency. |
| C3 — supra-threshold HOLD | Held-state assertions, output suppression, and applicable timer/expiry/lifecycle mappings. |
| C4 — supra-threshold release | Certified crossing and classification, crossing/output times, and quiet/terminal state. |
| C5 — unequal-HOLD replay | Active-time relation/equivalence, each associated schedule, hold-dependent absolute-time shifts, and terminal/output relation. |
| C6 — ungated reference | Independent mapping of the reviewed reference fixture; do not infer coverage by copying C4. |
| C7 — lifecycle/time edge cases | Applicable sub-ULP delays, ceilings, expiry/coalescence, equal-time precedence, and ingress/lifecycle boundaries, restricted to cases already in the reviewed design. |

This table describes which obligations a future fixture-freeze artifact must
map. It does not supply fixture inputs, numeric checkpoints, event schedules,
timestamps, computed ordinals, or certificate results.

### Relationship to other gates

| Gate | Boundary |
|---|---|
| N1 | Mathematical witness/enclosure completeness. N4-A3 and N4-A5 consume relevant N1 evidence; they do not close N1. |
| N3 | Complete event-time mapping and ordering. N4-B certifies the arithmetic and binary64 interface for that mapping; it does not replace N3. |
| N4 | N4-A and N4-B are separate certificate gates. This schema defines their proof obligations only and closes neither. |
| N5 | Immutable synthesized C0–C7 numeric expectation table. It consumes completed N1/N3/N4 evidence and adds no new mathematics. |
| N6 | Runtime enforcement of the reviewed semantics; Stage B only. N4 does not establish N6. |

## Required fixture-freeze mapping fields

After independent review of this schema, the fixture-freeze artifact must
map each fixture/checkpoint/event to at least:

| Field | Meaning |
|---|---|
| `fixture_id` | Repository-defined C0–C7 identity. |
| `checkpoint_id` | Stable identity of a mathematical or timing checkpoint. |
| `event_id` | Stable semantic identity when the checkpoint is an event. |
| `n1_witness` | Required N1 witness identity or explicit not-applicable rationale. |
| `n3_event_mapping` | Required N3 mapping identity or explicit not-applicable rationale. |
| `n4_a_requirements` | Applicable N4-A1…A7 obligations. |
| `n4_b_requirements` | Applicable N4-B1…B7 obligations. |
| `time_source` | Frozen exact or mathematical source, if applicable; not its computed result. |
| `ordinal_dependency` | Frozen precedence/ordinal rule dependencies; not a numerically derived ordinal. |

The freeze defines what later evidence must cover. It must not run numerical
certification or the scientific fixture.

## Status and next gate

Disposition: **N4 CERTIFICATION REQUIREMENT SCHEMA FROZEN.** N4 itself remains
open and blocked until complete evidence satisfies every applicable
obligation. The C0–C7 scientific definitions, equations, parameters,
thresholds, event semantics, arithmetic profile, and `16+1+24+1=42` accounting
are unchanged.

Next: independent Luna-0 review of this schema for contract fidelity and
sufficiency. Only after an independent PASS may the separately bounded C0–C7
fixture-freeze prerequisite proceed. W/T/E numerical completion remains
behind that fixture freeze and its independent PASS; Lane S/N5 and Stage B
remain blocked.
