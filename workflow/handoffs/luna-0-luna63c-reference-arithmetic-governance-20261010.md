# Luna-0 — Luna-63C reference arithmetic governance

**Disposition: REFERENCE ARITHMETIC PROFILE AUTHORIZED.**

This is a narrow arithmetic-semantics decision for the already-authorized,
isolated Luna-63C mechanism experiment. It does not authorize certificate
synthesis, Stage-B implementation, C0–C7 execution, architecture promotion,
or hardware conformance.

## Verified baseline and authorities

Before review, `origin` was fetched. The certificate branch was clean at
`e10aad9dd2b4a3fbfd708ac656e89ace2cf20293`, equal to
`origin/experiment/luna63c-stage-a-certificate`. `main` was clean and equal
to `origin/main` at `73aaa50f97ceab322907875ae4dcf23e7541c3b5`.

Reviewed design SHA: `3e7d31b9a527e908b21abee3766906084e7cd082`.
Latest design handoff SHA: `a303ebb835b72fdd01c86df478431b8638aacbb4`.
Latest published certificate SHA: `e10aad9dd2b4a3fbfd708ac656e89ace2cf20293`.
Its independent certificate disposition remains
**BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE**.

The pinned design specifies the exact flow
`X(s)=exp(-s) Rot(s) X(0)`, binary gate semantics, root/terminal rules,
interval-based mathematical reference requirements, and binary64 event-time
ceiling/strict-future rules. The committed `.github/agents/luna-63c-mechanism.agent.md`
also requires an independent certificate oracle and the A=1
`||X_candidate-X_oracle||_2 < theta/4` comparison. Neither source requires
binary64 continuous-state arithmetic. The explicit use of binary64 is at the
event-time boundary. Thus the requested profile clarifies implementation
representation inside the existing isolated authorization; it does not
change the scientific intervention or event contract.

## Arithmetic evidence considered

The read-only W/T/E analyses remain findings, not a completed certificate:

- correctly rounded transcendental results followed by ordinary binary64
  coordinate arithmetic can, for a stipulated minimum-subnormal active time,
  yield stored coordinates whose exact squared norm is slightly greater than
  16;
- naive binary64 duration accumulation can discard `2^-54` when added to 1;
- directed/inward coordinate projection was not established as
  semantics-preserving and is not adopted.

Independent Luna-0 review confirmed these arithmetic examples under their
stated assumptions, while explicitly finding that they are not observed
Stage-B failures or violations of the reviewed mathematical design. They
demonstrate why unrestricted binary64 state/time arithmetic must not silently
serve as the scientific reference.

## Authorized Stage-B reference arithmetic profile

1. **Implementation identity:** MPFR C API 4.2.2 with GMP 6.3.0. These
   versions are pinned for the isolated reference implementation. Host
   `libm` is not used for scientific transcendental values.
2. **State representation:** continuous coordinates and reference
   quantities are outward-rounded MPFR intervals, not binary64 coordinates.
   Exact fixture binary64 values are imported exactly. The reviewed analytic
   field and all parameters remain unchanged.
3. **Rounding:** interval lower endpoints use MPFR round-toward-negative
   infinity; upper endpoints use round-toward-positive infinity. Arithmetic
   and `sqrt`, `exp`, `sin`, `cos`, `log`, and `pi` use MPFR with those modes.
   Non-finite or unsupported operations fail closed.
4. **Precision and convergence:** evaluate every required frozen assertion
   at both 256 and 512 bits. Require overlapping enclosures and identical
   resolved classifications and scheduled binary64 timestamps. If either
   precision is unresolved or results disagree, refine at 1024 bits and
   require overlap and resolved agreement. No greater precision or more than
   128 bisections per root is allowed. Midpoint agreement alone is
   insufficient.
5. **Active time:** convert binary64 event timestamps to exact dyadic
   integers in `2^-1074` units and accumulate released durations exactly with
   GMP integers. The cumulative duration is bounded by the inclusive
   `[0,2^20]` clock domain; no rounded binary64 addition defines active time.
6. **Flow evaluation:** evaluate the reviewed semigroup at certified active
   time using MPFR interval operations. Do not quantize continuous-state
   updates to binary64. Certify the disk invariant on the reference interval,
   not on separately rounded coordinates.
7. **Scientific decisions:** crossing existence, direction, tangency, quiet,
   and terminal classification follow the reviewed analytic rules and
   certified intervals; a rounded coordinate never redefines a crossing.
   Root and event-time intervals must resolve all required signs, common
   ceilings, and ordering, or the certificate stays blocked.
8. **Event-time interface:** map a certified real-time interval to binary64
   only when both endpoints have the same least binary64 ceiling. Require
   strict future for every positive causal delay, clock-domain membership,
   strict causal order, and output-before-expiry. A positive sub-ULP delay is
   evaluated at reference precision before conversion. `nextafter` is only a
   candidate for the uniquely certified ceiling.
9. **Output:** the canonical payload `p·1` remains exact. Event time is the
   only state/trajectory boundary quantized to binary64 by this profile.
10. **Independence:** the Stage-A certificate oracle must be separately
    implemented and must not share propagation, root, threshold, conversion,
    timer, or lifecycle code with the future Stage-B reference
    implementation.

N4 is now partitioned into **N4-A**, certified enclosure of the reviewed
state, roots, and event times, and **N4-B**, preservation of event-time ceiling,
strict-future, domain, causal order, and expiry rules at the binary64 queue
boundary. This authorization does not establish either part; both require
independent numerical evidence in the Stage-A certificate. Candidate/oracle
state comparisons, including the strict A=1 bound, remain mandatory and must
be independently verifiable.

## Deferred and unchanged scope

- **N1/N3/N4/N5:** remain open; v2 remains blocked.
- **N6:** runtime enforcement remains Stage-B-only.
- **W/T/E:** authorized to resume independent certificate preparation under
  this profile. Lane S/N5 synthesis must wait for complete, publishable W/T/E
  outputs and may add no new mathematics.
- **Stage B:** remains unauthorized until certificate publication and
  independent Luna-0 **PASS** on immutable hashes.
- **Binary64-state and fixed-point conformance:** deferred to later isolated
  conformance work; no claim is made here.
- **A01–A15, ACP-0008, production defaults, field equations, parameters,
  thresholds, event surfaces, C0–C7 semantics, and 16+1+24+1=42 accounting:**
  unchanged.
- **WEMA/input-spike interpretation:** not part of Luna-63C and not changed.

## Validation and next assignment

| Check | Result |
|---|---|
| Fetch and baseline identity | PASS; certificate branch `e10aad9…`, main `73aaa50…` |
| Initial worktree/index | Clean |
| Design/contract semantic review | Read-only; no binary64 state-arithmetic mandate found |
| W/T/E certificate calculations | Not run in this governance pass |
| N5 synthesis | Not run |
| Stage-B implementation and C0–C7 scientific execution | Not run |
| Tests/build | Not run; documentation/governance scope |
| Architecture/ACP change | None |

Next assignment: independent W/T/E certificate preparation against this exact
arithmetic profile, stopping with blocked dispositions for any unresolved
interval, event mapping, or comparison rule. Then, and only after complete
lane results, Lane S may synthesize N5. Stage B stays locked pending the
subsequent independent Luna-0 certificate PASS.
