# Luna-47E predeclared analysis criteria — revision 1

Authorization checkout: `789dda5988daf72f375d9713bd76a6da2b9e8b34`.
Production/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Declared 2026-10-06, before classification or matrix construction. Initial
manufacturer URL probes are discovery only, not positive findings.

## Classification rules

- **SUPPORTED**: the primitive has an identified commercial implementation,
  manufacturer limits and an independently observed distributor stock/ordering
  indication for the exact part. This means documentary primitive support,
  never circuit validation or TPCN equivalence.
- **PARTIALLY SUPPORTED**: constituent parts are documented/obtainable but the
  primitive requires an unvalidated composition, calibration or digital control.
- **NOT SUPPORTED**: a proposed realization contradicts documented limits.
- **BLOCKED**: capability or purchase evidence cannot be verified.
- Overall: PARTIALLY SUPPORTED when plausible discrete compositions exist but
  FPAA availability, system semantics or owner access remains unresolved.

## Fixed scope and controls

Eight required primitive families only. No search over neuron parameters or
interpretation of unreviewed Luna-47 lanes. Public sources only; no delegation,
purchase, build, simulation, production change, ACP or architecture promotion.
No claimed country access: owner region, budget, inventory and lead-time
constraints are unknown and owner-specific availability is BLOCKED.

For each exact candidate retain manufacturer, function, electrical limits,
configuration, resolution/time constraints, tolerance, package/accessories,
source identity/URL/retrieval time, public price/stock/lead-time or explicit
unknown. Distributor evidence and manufacturer capability are separate.
Unavailable pages and negative evidence are retained, not replaced by inference.
FPAA requires verified purchasability and documented integrator/OTA resources;
an old capability claim or a distributor search alone is insufficient.

## Analytical assumptions, not hardware specification

Illustrative low-voltage bench envelope: 5 V analog, 2.5 V signal reference;
state limited to a proposed +/-1 V about reference. Reference/buffering/reset,
rail clamps, finite pulse budgets and signed-event encoding remain design gaps.
Choose illustrative R=10 kohm to 100 kohm, C=100 nF: tau=1 to 10 ms.
These are hand calculations, not validated circuit ranges. No logical-time to
seconds conversion is adopted; retained Luna-46 tau=80 logical units is context
only. Ideal RC decay does not by itself implement event-time WEMA normalization.

## Verification / stop

Validate JSON structure, exact eight-family coverage, references, source hashes,
retrieval dates, explicit owner block, baseline identity and owned-path diff.
Hash retained Luna-46 artifact without recomputing or changing its MIXED result.
Record calculations and uncertainty without inventing measurements.
Publish evidence and handoff with required coauthor trailer; verify remote parity
and clean worktree; stop for independent Luna-0 review.
