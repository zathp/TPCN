# Luna-0 — Owner Authorization: Luna-64 R4.3 Corrective Implementation

**Gate ID:** `L64-TB-R4.3-CORRECTIVE-20261010`  
**Authorization date:** 2026-10-10  
**Authorization source:** explicit repository-owner authorization in the
current task conversation.  
**Authorized gate SHA-256:**
`8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369`.  
**Gate publication revision:** `439c0c930489ed032dc10950bbd51fe3f153d05a`.  
**Independent prereview:** PASS — CORRECTIVE GATE READY FOR OWNER
AUTHORIZATION, reviewed draft SHA-256
`86F30AA80A6979EA6FC27CD57879412554299A616C8B36A6B94BACC1B35A8045`.  
**Authorized scope:** corrective implementation and focused correctness
verification only; no additional scientific experimentation.

## Owner decision

The repository owner explicitly authorizes the bounded corrective
implementation in the exact gate above and explicitly accepts its proposed
**reject-only malformed second-reward-origin policy**.

A second distinct origin must be rejected without changing, replacing,
delaying, resetting, reopening, settling twice, or charging again for the
first origin. The accepted first reward proceeds under the frozen lifecycle,
including when it has already settled at zero delay. No rollback is allowed.
This policy does not grant authority for other unspecified malformed-input
behavior.

## Verified prerequisites

- The published gate file matches the owner-specified SHA-256.
- Its final bytes are in publication commit
  `439c0c930489ed032dc10950bbd51fe3f153d05a`, descended from the closed-pilot
  governance commit `515dde66f37ca67c44a39f02e13f2e59b2f10d1d`.
- The independent prereview returned PASS for the substantive draft hash
  recorded above. Its exact findings and scope are preserved in
  [the independent prereview record](luna-0-independent-review-luna64-r4.3-corrective-gate-20261010.md).
- The original pilot verdict remains **NOT SUPPORTED AS A
  PROTOCOL-COMPLIANT PILOT**, not an efficacy result; its budget is exhausted.
- The frozen R4.3 protocol and original pilot artifacts are protected and
  outside the modification allowlist.
- Luna-63C remains unchanged and isolated.

## Execution boundary

Implementation is limited to the paths and sections in the approved gate.
It must use the isolated corrective branch
`experiment/luna64-r4.3-reward-lifecycle-correction-20261010`, based on
`d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`, preserve the original branch and
artifacts, and reject unrelated worktree changes.

Verification is limited to the single approved supervisor invocation and
its three exact child tests. The following aggregate limits apply to the
whole supervised run: one logical CPU; 120 CPU seconds; 180 wall seconds;
512 MiB working set; 512 combined synthetic fixture/trace records; and
5 MiB artifacts. The one-shot marker, suspended-process affinity gate and
aggregate monitoring are mandatory. Inability to enforce any required
limit is a stop condition. No fourth invocation may be used.

The original pilot runner may be edited only inside the authorized corrective
mechanisms. No frozen protocol/specification, benchmark, scientific arm,
production/core, ACP, or Luna-63C change is authorized. No scientific
benchmark, training/evaluation workload, efficacy analysis, successor pilot,
or rerun is authorized.

After focused verification, the implementation must be committed and pushed
on the isolated corrective branch with bounded evidence. A separate
independent Luna-0 review of the committed change and evidence is required
before governance closure. The original pilot disposition and exhausted
budget remain unchanged regardless of corrective test outcome.
