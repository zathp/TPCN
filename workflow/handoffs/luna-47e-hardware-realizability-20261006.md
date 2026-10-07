---
tpcn_handoff:
  agent: "Luna-47E evidence worker; independent Luna-0 review pending"
  luna_identifier: "Luna-47E"
  descriptive_name: "Bench-buildable FPAA / discrete realizability"
  task_id: "luna-47e-hardware-realizability-20261006"
  component: "Public component evidence and primitive mapping only"
  status: "complete - PARTIALLY SUPPORTED; owner access and independent FPAA access BLOCKED"
  contract_version: "1.2"
  branch: "copilot/luna47e-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  production_evidence_baseline: "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
  evidence_revision: "d19b2064ce846e6c564d1e34cd306b4ca0f3d036"
  result_revision: "Publication commit containing this handoff and validation record; exact hash returned to caller after push."
  dependencies:
    - "Common published Luna-0 authorization at base_revision"
    - "Committed Luna-47E agent contract, architecture contract/changelog, authoritative workflow, acceptance, ACP process/template and handoff template"
    - "Retained Luna-46 corrective handoff and baseline artifact; context only"
  owner: "Project owner; region, inventory, budget and supply constraints not supplied"
  classification:
    - "OFFLINE ANALYSIS / PUBLIC DOCUMENTARY EVIDENCE"
    - "PARTIALLY SUPPORTED"
    - "owner-specific availability BLOCKED"
    - "independent FPAA purchasing BLOCKED"
    - "not hardware validation, efficacy or equivalence"
    - "independent Luna-0 review pending"
  hypothesis: "Identified commercial parts provide realistic constituent primitive mappings without ideal or research-only devices."
  counter_hypothesis: "Unavailable products, missing limits/tooling, or required unvalidated compositions prevent a complete bench-ready mapping."
  interfaces_relied_on:
    - "Public unauthenticated manufacturer/store/distributor HTTPS GETs"
    - "Manufacturer PDFs, including clearly identified distributor mirrors"
    - "Lane-only matrix/capture/validation schemas; no TPCN runtime imports or changes"
  label_information_boundary:
    - "No dataset or task labels used; all results remain downstream documentary evidence."
    - "No retained diagnostic metric becomes a neural input or hardware parameter selection."
  timing_assumptions:
    - "Retrieval date is 2026-10-07 UTC / 2026-10-06 local UTC-04:00; per-source exact timestamps retained."
    - "No logical-time-to-seconds mapping adopted; Luna-46 tau80 is context only."
    - "RC, DAC and timer calculations are ideal hand calculations, not measured timing."
  reset_boundaries:
    - "No physical or simulated state executed."
    - "Character reset/discharge, pending pulse cancellation and reinitialization remain unimplemented bench design requirements."
  resource_bounds:
    - "Eight primitive families, ten matrix components, eight independent exact-part discrete offers."
    - "Five catalogs, sixty source observations; bounded capture12 MB/GET and60-second curl timeout."
    - "Finite4-CAB FPAA and finite-step digi-pot/DAC resources; no unlimited fan-in or events assumed."
  authorized_scope:
    - "Predeclare criteria; research public capability/purchasability; retain unavailable outcomes."
    - "Write lane-owned matrix, evidence catalogs, provenance, offline checks and this handoff."
    - "Commit and push isolated branch, verify clean remote parity, then stop."
  unauthorized_scope:
    - "No purchase, hardware build, circuit simulation/validation, hardware equivalence or architecture selection/promotion."
    - "No production, runtime, neuron, routing, topology, governance or other lane changes."
    - "No other lane visibility, delegation, merge, successor, ACP or Luna-48."
  controls:
    - "Criteria revision1 and exact SHA declared before matrix interpretation."
    - "Manufacturer capability separated from independent distributor evidence."
    - "Exact MPN, stock and first quantity-tier price checked against captured structured offer."
    - "Every source reference resolves to a dated catalog record with URL/status; successful raw response bytes hashed in memory."
    - "All owner-specific access remains BLOCKED; no assumed purchasing region or budget."
    - "Retained context exact checkout and Git-blob SHA256 checked separately with declared terminalCRLF materialization."
    - "Mutation tests reject unsupported owner, stock, price, source, baseline, calculation and hardware claims."
  measurements:
    - "Public offer counts/prices, document electrical limits, retrieval statuses and hashes; no physical quantities measured."
    - "Offline matrix coverage10 components/8 families;8 exact independent offers."
    - "Analytical RC tolerance, digi-pot step, DAC ideal resolution, nominal current and one-shot width."
  information_boundary_check:
    - "PASS: downstream-only public evidence; no labels, future sequence data, global neural state or production imports."
  hardware_mapping:
    - "AN231E04-QFNSP capability documented; manufacturer store orderability observed, independent FPAA access BLOCKED."
    - "TLV9062IDR,TLV3201AIDBVR,MCP41010-I/P,MCP4921-E/P,LMC555CMX/NOPB,B32529C1104J289,1N4148-TAP,MFR-25FBF52-100K exact public distributor offers retained."
    - "Composed integrator/WEMA,deadband,rectifier,sum/accumulation and bounded-event output not validated."
  architecture_invariants_touched:
    - "A15 primary realizability analysis boundary; no equivalence established."
    - "A01-A04,A08,A09 constraints analyzed but not changed or experimentally certified."
  preserves:
    - "A01-A15, architecture contract1.2 and all ACP statuses unchanged"
    - "Luna-46 MIXED; no repaired-drive/retention efficacy inference"
    - "Production/evidence baseline unchanged"
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna47e/criteria.md"
    - "experiments/luna47e/README.md"
    - "experiments/luna47e/capture_sources.py"
    - "experiments/luna47e/validate.py"
    - "artifacts/luna47e/primitive-matrix.json"
    - "artifacts/luna47e/sources-20261006.json"
    - "artifacts/luna47e/sources-20261006-retrieval2.json"
    - "artifacts/luna47e/sources-20261006-retrieval3.json"
    - "artifacts/luna47e/sources-20261006-retrieval4.json"
    - "artifacts/luna47e/sources-20261006-retrieval5.json"
    - "artifacts/luna47e/validation-20261006.json"
    - "tests/test_luna47e_evidence.py"
    - "workflow/handoffs/luna-47e-hardware-realizability-20261006.md"
  tests_added:
    - "18 offline evidence/mutation/ownership tests, no production imports"
  tests_passing:
    - "Focused pytest:18 passed"
    - "Matrix/source/offer/reference/hash/hand-calculation validator:PASS"
    - "Editor problems check:no errors found in lane Python files"
    - "Owned-path staging and Git whitespace checks:PASS"
  tests_failed:
    - "Initial focused run:1 failed,17 passed; baseline hash mismatch due solely to terminalCRLF checkout vsLF Git blob. Preserved, diagnosed, corrected validation policy; evidence unchanged."
  tests_not_run:
    - "VS Code runTests found no tests for the isolated worktree; explicit pytest fallback used."
    - "Full production/application suite:NOT RUN, outside evidence-only scope."
    - "Circuit, physical hardware, equivalence, efficacy, routing/timing and energy calibration:NOT RUN."
    - "Checkout, purchase, installer or FPAA CAM compile/fit:NOT RUN."
  assumptions:
    - "Public stock and available=true are supplier statements, not guarantees or completed purchases."
    - "Proposed5 V analog/2.5 V reference/+/-1 V envelope is an illustration, not an approved circuit."
    - "Raw documents are not redistributed; hashes support identity checks only if the same bytes can be retrieved."
  unresolved:
    - "Owner region/budget/inventory/supply constraints"
    - "Independent FPAA availability and software/license/board/accessory verification"
    - "Complete controller/reference/reset/deposition/gating/PCB BOM and schematic"
    - "Physical drift, mismatch, noise, stability, signed encoding, finite budgets and causal event order"
    - "No hardware portability or system efficacy gate closed"
  recommended_next_agent:
    - "Independent Luna-0 review of pushed evidence/handoff only; no successor or build authorized."
---

# Luna-47E completed evidence handoff

## Outcome and owned scope

**OBSERVED:** Completed analysis-only work in the explicitly supplied isolated
worktree and branch from the published authorization revision. All changed
paths are in the permitted lane directories/test prefix or this handoff.
There is no production/governance change, delegation, other-lane consumption,
merge, purchase, build, simulation or successor execution.

**Verdict: PARTIALLY SUPPORTED.** Individually documented finite-step
programmable resistance, fixed capacitance and DAC/configuration interfaces
are SUPPORTED at the documentary primitive level. Composed analog integration,
deadband, rectification, accumulation and bounded output are PARTIALLY
SUPPORTED. Independent FPAA purchasability and owner-specific access are
BLOCKED. This does not select a production architecture or establish A15
hardware equivalence.

Primary artifacts:

- [Detailed analysis and reproduction](../../experiments/luna47e/README.md)
- [Predeclared criteria](../../experiments/luna47e/criteria.md)
- [Machine-readable primitive/component matrix](../../artifacts/luna47e/primitive-matrix.json)
- [Initial source observations](../../artifacts/luna47e/sources-20261006.json)
- [Second observations / preserved tooling failures](../../artifacts/luna47e/sources-20261006-retrieval2.json)
- [Manufacturer datasheet observations](../../artifacts/luna47e/sources-20261006-retrieval3.json)
- [Capacitor mirror and accessories](../../artifacts/luna47e/sources-20261006-retrieval4.json)
- [Currency and resistor mirror](../../artifacts/luna47e/sources-20261006-retrieval5.json)
- [Offline validation and lane integrity inventory](../../artifacts/luna47e/validation-20261006.json)

## Findings by primitive

| Primitive | Practical mapping | Result |
|---|---|---|
| Leaky integrator/WEMA | AN231E04 documented SC/boxcar resources, exact leaky CAM limits unresolved; discrete TLV9062 + TDK100 nF + Yageo100 kohm + MCP41010 finite adjustment | PARTIALLY SUPPORTED; RC alone is not event-time normalized WEMA |
| Programmable R/conductance | MCP41010-I/P,256 positions,10 kohm; current/voltage/wiper limits explicit | SUPPORTED for bounded digi-pot, not ideal continuous bipolar VCR |
| Capacitor | B32529C1104J289,100 nF5%,100 VDC,PET,5 mm | SUPPORTED fixed capacitor; memory precision unvalidated |
| Comparator/deadband | TwoTLV3201AIDBVR + threshold references/DACs | PARTIALLY SUPPORTED window; individual comparator documented |
| Rectification/absolute value | TLV9062 +1N4148-TAP precision feedback composition | PARTIALLY SUPPORTED; diode-only low-signal mapping rejected |
| Sum/subtract/accumulate | TLV9062 + fixed resistor arms + capacitor/leak | PARTIALLY SUPPORTED; ordered events not an unordered analog sum |
| Threshold/bounded output | Comparator -> LMC555CMX/NOPB one-shot plus reset/gate/budget | PARTIALLY SUPPORTED; free-running oscillator alone not bounded |
| DAC/configuration | MCP4921-E/P12-bit SPI/LDAC voltageDAC, MCP41010 SPI, FPAA serial bitstream | SUPPORTED discrete interfaces; FPAA tools/access unresolved |

**OBSERVED:** Okika's manufacturer store has AN231E04-QFNSP10-pack USD120,
AN231K04-DUAL2 USD219, `available=true`; unknown stock quantity/lead-time.
DSv2.2/UM establish finite CAB op-amp/comparator/switched-capacitor resources,
not an exposed OTA. Independent DigiKey FPAA pages return403. No search
summary stock claim is promoted to verified evidence. Legacy Anadigm product
page is a redirect stub. Direct Microchip/TDK pages were unavailable; successful
manufacturer PDFs or clearly identified manufacturer-document mirrors supply
capability instead.

**OBSERVED:** Eight exact ordinary-part public distributor offers are retained:
TLV9062IDR168340,TLV3201AIDBVR32169,MCP41010-I/P64,MCP4921-E/P34,
LMC555CMX/NOPB610,B32529C1104J2899430,1N4148-TAP18580 and
MFR-25FBF52-100K10500 units. The matrix/README give precise quantity-tier
prices and sources. Those figures are dated observations, not audited
inventory, delivery guarantees or evidence of owner access.

**INFERRED:** Ordinary low-voltage circuits are realistic candidates for
bench investigation, but the selected evidence is not a complete tested
bench-ready system. Missing controller/reference/reset/gate/PCB selection,
FPAA board/tool limits and calibration block any stronger claim.

**HYPOTHESIZED, NOT TESTED:** A future separately authorized hybrid controller
and analog primitive assembly could enforce causal finite event handling.
This lane neither proposes nor authorizes that system or any follow-up.

## Architecture evidence

| Clause | Analysis boundary / unresolved evidence |
|---|---|
| A15 | Specific commercially documented parts and public offers replace ideal/research-only assumptions. Hardware equivalence remains untested. |
| A01 | SC/configuration clocks are implementation clocks, not an authorized mandatory neural tick. Analog idle bias is not zero computation energy. |
| A02 | RC charge can provide persistent local state; time units, deposition, event-order response and reset require separate fixtures. |
| A03 | Comparator, DAC and SC delays are finite; no verified causal routing/timestamp equivalence is claimed. Analog simultaneous summation cannot silently discard event order. |
| A04 | Four CABs, finite IO,256 pot positions and4096 DAC codes are finite resources; no complete fan-in/out or queue implementation is established. |
| A08 | Saturation/clamps alone do not enforce finite event count or safe recurrent routing. Output gates/budgets/refractory/reset remain unimplemented. |
| A09 | Bias, leakage, clock and digital configuration cost require local hardware accounting and calibration. Manufacturer current values and hand estimates are not joule measurements. |

No clause, ACP, accepted production configuration or Luna-46 result changes.
Luna-46 corrective artifact remains MIXED, not evidence that circuit
availability would fix its75 drive-limited/212 no-reception sequences.

## Validation record

Environment: Windows10 build19045, selected CPython3.11.5, curl, git;
PDF inspection pypdf6.19.0/fonttools4.66.1/cryptography50.0.2 installed only in
the interpreter environment. No project dependency file changed.

| Procedure | Actual result | Evidence |
|---|---|---|
| Clean initial branch/HEAD inspection | Specified branch at789dda5, clean | Git command output |
| Predeclaration before classifications | Criteria SHAe7dfd7bb… retained | Criteria + matrix |
| Public capture | 60 dated observations in5 catalogs; unavailable states retained | Source catalogs |
| VS Code focused runTests | No discovered tests; explicit terminal fallback used | Tool result |
| Initial pytest | 1 failed,17 passed: canonical/checkout hash assumption wrong | Preserved narrative; exact diagnosis below |
| Corrected focused pytest | 18 passed | Explicit selected interpreter command; final record |
| Offline validate.py | PASS:8 families,10 components,8 independent exact-part offers; references, baselines, prices, calculations checked | validation-20261006.json |
| Editor problems | No lane Python errors reported | Tool result |
| Lane-only staging / git diff --check | PASS | Git command output |
| Full suite / hardware / circuit / efficacy | NOT RUN | Outside scope |
| Publication push/remote parity/clean | Required final gate; exact commit and observed result returned to caller after publication | Final caller response, origin ref |

Retained context integrity (no mutation):

- Checkout SHA256:
  `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e`
- Canonical Git blob at production baseline SHA256:
  `54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51`
- Difference: one terminalCRLF in checkout versusLF in Git blob under
  `core.autocrlf=true`; checkout normalization is otherwise exactly byte equal.
  Both hashes and this conversion are independently checked, not replaced
  with loose JSON comparison.

The offline checker validates record consistency and provenance, not electrical
correctness, physical circuit stability or supplier authenticity. PDF numeric
claims were read with document/page locators; limited extracts and response
hashes are retained rather than redistributing entire publications.

## Benchmark and resource results

Dataset, split, class accuracy, prediction loss, event/activation counts,
physical energy, connectivity utilization, latency and utility: **not
applicable / not measured**. There is no neural experiment in this lane.
IllustrativeRC100 kohm*100 nF=10 ms,1%/5% tolerance9.405..10.605 ms;
DAC2.5 V/4096=610.3515625 uV; one-shot nominal11 ms. These are hand
calculations with explicit assumptions, not parameter tuning or hardware
measurements. Logicaltau80 is not assigned seconds.

## Assumptions, limitations and unresolved gates

1. Owner region, budget, stock and supply constraints are unknown:
   owner-specific procurement **BLOCKED**. No purchase authorized.
2. FPAA manufacturer orderability is not independent stock verification:
   FPAA procurement criterion **BLOCKED**. Tool installation/license/CAM
   fit, selected board supplies/accessories and precision limits unresolved.
3. Controller/reference/deposition/reset/output gating, finite causal event
   routing, signed encoding, saturation, tolerance/noise/thermal behavior and
   local energy model have no executed evidence.
4. Supplier data changes. Live recapture cannot be expected to reproduce
   old response bytes; catalog hashes do not by themselves reconstruct
   unretained raw sources. Initial PDF failures were tooling/encoding issues,
   not claims that devices lack the functions.
5. No varactor, MEMS, exotic memristor, custom ASIC or unverified idealOTA is
   assumed. Alternatives have no demonstrated baseline prototyping advantage.

## Reproduction, rollback and next assignment

Run the explicit worktree/interpreter commands in the linked README.
Offline validation needs no network and imports no production code.
Optional recapture writes only a **new** lane artifact; it cannot overwrite
published catalogs. Keep original observations and dates.

Safe restoration point is common authorization789dda5988daf72f375d9713bd76a6da2b9e8b34.
Any rollback is confined to this lane's commits; no shared changes or other
worktrees are involved. Publication consists of the pinned evidence commit
plus the containing handoff/validation commit, both with the requested
Copilot coauthor trailer.

**Stop after the pushed handoff.** Only independent Luna-0 review of these
published inputs is appropriate. Integration, purchase/build, production
selection, merge, successor dispatch and Luna-48 remain unauthorized.
