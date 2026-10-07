# Luna-47E: bench-buildable primitive evidence

**Overall verdict: PARTIALLY SUPPORTED.** This is a completed documentary
investigation, not a completed hardware implementation. Ordinary components
make several primitives commercially plausible. Composed WEMA, rectifier,
window and bounded-event circuits remain unvalidated. Independent FPAA stock,
software access, complete board specifications and **all owner-specific access
are BLOCKED**. No architecture, BOM or configuration is selected for production.

## Authority and evidence scope

The lane began clean on `copilot/luna47e-investigation` at common authorization
`789dda5988daf72f375d9713bd76a6da2b9e8b34`. Production/evidence remains
`2cef8ea4b37a4ae586e3f383511cba63c9268ddc`. Read sources are the committed
Luna-47E agent contract, architecture contract v1.2, changelog, authoritative
workflow, acceptance criteria, ACP process/template, handoff template, common
Luna-0 authorization, and retained Luna-46 handoffs/corrective artifact.
Other Luna-47 lanes were not inspected, delegated to or used.

[Criteria](criteria.md) were written before classification/matrix construction,
after initial URL discovery probes. They define documentary SUPPORTED,
PARTIALLY SUPPORTED, NOT SUPPORTED and BLOCKED; no statement means equivalence.
The [matrix](../../artifacts/luna47e/primitive-matrix.json) supplies exact
parts, electrical limits, configuration and package/accessory gaps, stock
tiers, references, configuration identity, hashes and negative results.

## Practical mappings

| Ideal primitive | Commercial FPAA capability / remaining gate | Ordinary discrete fallback | Documentary verdict |
|---|---|---|---|
| Leaky integrator / event WEMA, adjustable tau | Okika AN231E04-QFNSP: documented switched-capacitor CABs and boxcar integration. Boxcar is **not** proof of leaky event-time WEMA; CAM tau range/grid unverified. | TLV9062IDR summing integrator, B32529C1104J289 100 nF, MFR-25FBF52-100K leakage/guard resistor, MCP41010-I/P for limited adjustment. Signed bounded charge deposition, normalization and reset still need definition. | PARTIALLY SUPPORTED |
| Programmable R / conductance | AN231E04 clock/cap ratios can realize SC processing, not an ideal two-terminal voltage-controlled resistor or exposed OTA. | MCP41010-I/P, 10 kohm, 256 positions, SPI; 0..VDD terminals, +/-1 mA wiper limit, 20% absolute resistance spread. Resistor banks/DAC-biased active stages remain alternatives, not verified compositions. | SUPPORTED for finite-step digi-pot |
| Capacitor | AN231E04 matched programmable capacitor banks; physical values/code mapping not established. | TDK B32529C1104J289, 100 nF +/-5%, 100 VDC, PET, 5 mm through-hole. | SUPPORTED for fixed capacitor |
| Comparator / deadband | Four CAB comparators; on/off hysteresis and finite clock-related delay documented. Selected window CAM unverified. | Two TLV3201AIDBVR plus two references/DACs form a window; intrinsic hysteresis typical 1.2 mV, offset max 4 mV over temperature. | PARTIALLY SUPPORTED for composed window |
| Rectification / absolute value | AN231E04 UM names rectification in the design library, without verified selected transfer limits. | TLV9062IDR + Vishay 1N4148-TAP feedback full-wave rectifier. A diode-only circuit suppresses small signals and is not a precision absolute value. | PARTIALLY SUPPORTED |
| Sum / subtract / accumulate | CAB op-amps, caps and summing library documented; four CABs are finite. | TLV9062IDR + equal/resolved MFR resistors; capacitor plus parallel R supplies persistence/leak. Arbitrary analog fan-in is not ordered event processing. | PARTIALLY SUPPORTED |
| Threshold oscillator / bounded output | Manufacturer's OTC2312 shield CAM library names oscillators; compiled bounded-return/event-count mechanism unverified. | TLV3201 crossing -> LMC555CMX/NOPB one-shot, nominal 1.1RC. RESET/gating, finite count and refractory handling still required. Free-running oscillator alone is NOT SUPPORTED as bounded output. | PARTIALLY SUPPORTED |
| DAC / digital configuration | AN231E04 serial bitstream configuration documented; not a general voltage DAC. Tool/host availability untested. | MCP4921-E/P: SPI 12-bit voltage DAC, external VREF, gain 1/2, LDAC; MCP41010 for finite-step R configuration. | SUPPORTED for individual interfaces |

**Every FPAA realization is independently-purchasable BLOCKED** under the
predeclared criterion, even where manufacturer capability is established.
This is not a finding that all FPAAs are unavailable or cannot implement it.

### FPAA evidence and bench barriers

**OBSERVED:** Okika's present store lists AN231E04-QFNSP, a 10-chip pack at
USD120 with `available=true`, and AN231K04-DUAL2 at USD219 with
`available=true`. The independent DigiKey pages return HTTP403. No independent
stock count/lead-time claim is accepted. Okika's OTC2312 shield is also listed
at USD81.25 and its page names 43 CAMs including comparators and oscillators;
this is a separately identified alternative, not the selected baseline board.
OTC9300L at USD25 is discoverable but is not treated as a substitute whose
primitive limits were verified. Manufacturer orderability is **not**
independent distributor confirmation or a delivery guarantee.

**OBSERVED:** AN231E04 DSv2.2 and manufacturer UM document 4 CABs, 7 IO cells,
switched-capacitor processing, op-amps, comparators, programmable caps and
serial configuration. Supply 3.0..3.6 V, ambient -40..85 C; sample/hold-related
input range VMR +/-1.375 V with VMR 1.5 V is conditional, not universal.
ACLK <=40 MHz, typical 16 MHz, CAB clock divided below 4 MHz.
Comparator and IO specifications depend on route/mode/load.

**INFERRED:** The manufacturer's 0.25 W full-resource chip power ceiling is
roughly 75.8 mA at 3.3 V, not a measured circuit or board current. QFN44 with
exposed pad makes bare-chip breadboarding unrealistic without a PCB. A board
reduces assembly risk but does not resolve missing input-supply, accessories,
interface, software license/download and CAM compile/fit evidence. No exposed
OTA, unbounded conductance range or arbitrarily precise capacitor is assumed.

No installer is executed, no circuit is compiled and no board is ordered.
SC clocks are potentially legal hardware clocks under A01; adopting them as
a mandatory all-neuron update schedule would require separate causal evidence.

### Independently observed ordinary-part offers

Public LCSC HTML, exact manufacturer part numbers and structured offers were
retrieved directly with unauthenticated curl. Prices are the **first quantity
tier**, not the misleading lowest-volume-independent metadata price.
UTC retrievals are October 7; local session date is October 6, UTC-04:00.
Exact per-source UTC timestamps, URLs and response hashes are retained.

| Part | LCSC identity | Public count | USD/part at minimum quoted quantity |
|---|---:|---:|---:|
| TLV9062IDR | C398355 | 168,340 | 0.1220 at 5 |
| TLV3201AIDBVR | C105188 | 32,169 | 0.9820 at 1 |
| MCP41010-I/P | C1539831 | 64 | 3.7835 at 1 |
| MCP4921-E/P | C640392 | 34 | 4.4057 at 1 |
| LMC555CMX/NOPB | C90760 | 610 | 0.2948 at 5 |
| B32529C1104J289 | C15523 | 9,430 | 0.1014 at 5 |
| 1N4148-TAP | C917479 | 18,580 | 0.0483 at 20 |
| MFR-25FBF52-100K | C1364475 | 10,500 | 0.0183 at 50 |

Catalog shipping data for the first six lists `shipImmediately` equal to
reported inventory; this is a distributor assertion, not observed shipment.
Diode/resistor offers indicate InStock. Destination transit, replenishment,
tax/shipping costs, authenticity/lot inspection and owner-specific import
eligibility were not verified. Owner country, budget and existing inventory
are unknown. All owner-specific availability is **BLOCKED**, even if the
public stock looks generous. No total-build budget is invented.

### Electrical and configuration reality

The proposed illustrative envelope is 5 V analog, a buffered 2.5 V reference
and +/-1 V signals about reference. Bare FPAA instead needs 3.3 V domains
and its own documented reference; do **not** connect 5 V signals blindly.
Reference source, MCU/FPGA controller, reset switch, adapters, decouplers,
clamps, connectors, power supply and measurement apparatus are not a verified
complete BOM. SOIC8 op-amp/timer and SOT23-5 comparator need PCB/adapters;
PDIP8 DAC/pot and axial/film passives are mechanically more breadboard-friendly.

The TLV9062 is RRIO, 10 MHz GBW and 6.5 V/us typical slew, but offset is not
zero and its 50 mA short-circuit figure is not a continuous design load.
No shutdown pin exists on this chosen IDR variant. Its typical 538 uA/channel
at 5.5 V implies about 5.92 mW for two unloaded channels at that voltage,
before other circuit costs; **not measured**. Analog static bias persists at
idle. A09 local energy accounting must include that rather than pretending
no events means no hardware power.

MCP41010's 52-ohm typical wiper at 5.5 V and 8..12 kohm total spread prevent
exact programmable R. It resets to midscale, has finite settling and cannot
accept unreferenced bipolar terminal voltages. MCP4921's 12-bit resolution
is not 12-bit absolute accuracy: manufacturer INL can reach +/-12 LSB,
and an external reference must be chosen. The current values called
short-circuit or absolute maximum in the matrix are explicitly **not**
selected operating limits.

Capacitor PET absorption/drift/leakage and board contamination affect memory;
100 nF cannot be naively attached as a capacitive op-amp output load.
TLV9062's ordinary capacitive load specification is 100 pF; the proposed
100 nF state capacitor requires a proper compensated feedback network.
The film capacitor manufacturer PDF was obtained from a distributor mirror
after direct TDK retrieval failed. Its exact ordering code decodes on p7,
including J=5% and 289=ammo pack; it is not an approximate WIMA substitute.

### Hand calculations, not tuning or hardware results

- Fixed 100 kohm, 100 nF -> tau = 10 ms; 1% R and 5% C initial tolerance
  gives 9.405..10.605 ms before temperature, leakage and active errors.
- MCP41010 nominal R step is 10,000/256 = 39.0625 ohm, nominal RC step
  3.90625 us with 100 nF. It does **not** give linear conductance steps.
- A 100 kohm guard in series with that pot nominally gives about
  10.0052..11.00129375 ms using a 52-ohm illustrative wiper. This is **not**
  an implementation of the predeclared generic 1..10 ms RC illustration;
  wider adjustment needs a different verified resistance arrangement.
  The wiper value is typical at 5.5 V, not guaranteed at proposed 5 V.
- 1 V/100 kohm = 10 uA nominal: low-code pot safety cannot be assumed
  without such a separately enforced bound.
- VREF=2.5 V, gain1 -> ideal DAC step = 610.3515625 uV; this is an
  assumed reference calculation, not calibrated threshold resolution.
- LMC555 one-shot with 100 kohm/100 nF -> nominal 11 ms; timer timing
  tolerance and finite event-count/retrigger policy still matter.

No mapping from Luna-46's tau=80 **logical units** to seconds is adopted.
Retained corrective evidence preserves MIXED: 33 retention-limited,
75 drive-limited and 212 no-reception sequences. Primitive capability cannot
repair missing drive or prove efficacy. No retained trace is used as a
hardware fixture, no other lane results are consumed and no circuit behavior
is inferred to match EXCURSION_V1.

## Evidence retention and unavailable results

Five source catalogs preserve successive retrievals without overwriting:

1. `sources-20261006.json`: initial direct store/stock facts; PDF parsing
   failed because pypdf was absent in the explicit interpreter.
2. `sources-20261006-retrieval2.json`: pypdf present; several console
   inspection prints failed under Windows encoding. These are **tooling
   failures**, not negative manufacturer capability. Font encoding warnings
   also required fonttools.
3. `sources-20261006-retrieval3.json`: explicit UTF-8 printing/fonttools,
   successful manufacturer PDF retrieval/inspection. Capacitor mirror needed
   pypdf's AES dependency.
4. `sources-20261006-retrieval4.json`: capacitor mirror parsed with
   cryptography; diode/resistor stocks and Vishay datasheet captured.
5. `sources-20261006-retrieval5.json`: FPAA page currency USD captured;
   Yageo manufacturer resistor document retrieved through distributor mirror.

The capture helper initially installed pypdf through the environment tool,
but it was not visible in the explicit supplied interpreter. It was then
installed explicitly there. Environment-only PDF tools are pypdf 6.19.0,
fonttools 4.66.1 and cryptography 50.0.2 (with cffi/pycparser). No production
dependency manifest was changed.

Raw HTTP/PDF content is hashed in memory. Only limited excerpts/selected
structured offers are retained, not full third-party publications. Hashes
prove identity **if** the same bytes can be obtained again; they cannot prove
an unretained response's content by themselves. Human-reviewed numeric claims
have document/page locators. Offline checking resolves references, stock and
prices but does not independently recertify every electrical specification.

Legacy anadigm.com returns a JavaScript `/lander` stub, not a product page.
DigiKey direct FPAA pages and Microchip product pages return 403. Some
Newark/Mouser web-tool discovery requests failed transport retrieval.
Those preliminary failures and conflicting AI search summaries were not
used as positive capability, price or stock evidence. TDK direct PDF 403 is
retained; the manufacturer-authored mirror is explicitly distinguished.

## Replay and verification

From the specified worktree, with the explicit selected interpreter:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47e'
& 'c:/Users/zathp/Documents/programming/TPCN/.venv/Scripts/python.exe' -m pytest tests/test_luna47e_evidence.py -q
& 'c:/Users/zathp/Documents/programming/TPCN/.venv/Scripts/python.exe' experiments/luna47e/validate.py
git --no-pager diff --check
```

Offline tests/validation need Python/pytest, not PDF dependencies or internet.
They do not import production code. Optional live observation:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47e'
& 'c:/Users/zathp/Documents/programming/TPCN/.venv/Scripts/python.exe' experiments/luna47e/capture_sources.py --output artifacts/luna47e/new-observation.json
```

The destination must be new. Live content need not reproduce retained bytes.
No automatic new observation replaces the matrix. The final validation report
contains lane file hashes; publication is identified by Git commits.

The first test run failed (1 failed,17 passed) because the retained checkout
SHA differed from the canonical Git blob. Diagnosis found one terminal CRLF
versus LF under `core.autocrlf=true`, exact JSON equality, and otherwise
byte-identical content after CRLF normalization. The validator now checks
**both exact hashes separately** and the declared conversion. It does not
alter retained evidence or erase the first failure.

Full production, efficacy, circuit simulation, timing, hardware and equivalence
tests are **not run**. A15 remains an implementation constraint, not certified
hardware portability. Stop after publication for independent Luna-0 review.
