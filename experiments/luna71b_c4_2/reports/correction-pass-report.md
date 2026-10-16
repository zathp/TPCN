# Luna-71B-C4.2 bounded correction pass

## Disposition and authority

**PASS — bounded correction review; PPC-11 remains INCOMPLETE and is not
pilot-eligible.** This pass corrects bounded source/test defects; it does not
establish PPC-11 readiness, bilateral parity, efficacy, or architecture
conformance. The fresh same-byte Luna-0 review passed only the bounded
correction review.

Scope: `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna71b-c4-2`,
branch `experiment/luna71b-c4-2-bilateral-capture`, baseline HEAD
`11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`. C4.1 remains binding.
Both required contract/schema documents were read before edits. Only this
worktree's C4.2 modules, copied event runtimes, focused test and related
reports were changed. The active checkout and historical worktrees were not
modified. No package installation, neural training, inference, pilot, dataset
regeneration, commit, push, merge, or publication occurred.

## Preserved initial findings

`initial-implementation-report.md` is unchanged and remains a historical
initial report, not the correction disposition. The independent initial
Luna-0 review artifact was read without modification:

`C:\Users\Patrick\AppData\Local\Temp\1792100641526-copilot-tool-output-eda14f4350e843b4b2e7cbbacf74800b.txt`

Raw SHA-256:
`5bf00388011aca1d914c20dac97791bf47d727b72ece12fada90bf58c5503737`.
Its original disposition was **INCOMPLETE — CORRECTION REQUIRED**. All seven
initial blocking findings are retained here:

1. Family presence alone could admit incomplete cardinalities; branch counts,
   fixture identity and initial parameter manifests were insufficiently checked.
2. Peer completion could release unmatched events; identity and online
   first-mismatch stopping were not enforced.
3. Processed counts preceded handler completion and failure snapshots named
   attempted rather than last completed operations/times.
4. Disabled capture computed tie metadata; enabled tie causes were inaccurate.
5. Required lifecycle and bilateral source evidence remained unavailable.
6. The arbitrary callback driver did not bind actual model/source/trace
   contexts; cache identity was not verified.
7. Cleanly truncated files were indistinguishable from complete trace files.

The initial source-manifest SHA-256 was
`aaf18de03069111fd5872bfb98e6c4ebeb6fc8ac7b02108f84440eb907a86360`.
The initial inventory and matrix are retained below their correction addenda.
These historical findings have not been independently closed by this pass.

## Implemented corrections

### Schema and comparator

- Every family field is checked for its schema-specific string, boolean,
  ordered-list, source-map or tagged numeric representation. Model-visible
  raw JSON numbers and untagged source objects are rejected. Fixed-width
  integer encodings validate exact width and lowercase hexadecimal.
  Source revision requires the commit plus source-manifest digest.
- Positive branch counts must equal occurrence-list length; occurrence
  objects must be typed source maps. Comparator evidence must link the
  occurrences to matching captured family records, including duplicate/tie
  predicates. Inconsistent branch claims become evidence unavailable.
- Input IDs/orders and scheduler links, schedule/admission cardinalities,
  decision/feature identities, exactly four class drives and activations,
  feature-to-drive/pre-transfer links and tie-result consistency are checked.
  Known lifecycle creation links and processed-event accounting are checked.
  Parameter transition order and old/new chains connect initial/final state.
- Parameter manifest SHA-256 is recomputed from the captured Python source
  values using the copied source's canonical manifest serialization. Decoding
  f64 bits for that hash is not a parity projection or tolerance: comparison
  still uses complete typed wire values. Unsupported manifest source types
  or mismatched digests remain incomplete.
- No copied artifact provides frozen event payloads. A caller's fixture hash,
  even a syntactically valid SHA-256, cannot establish that binding. The
  comparator explicitly retains a P01 fixture-identity gap and cannot report
  overall READY from these inputs. It still reports actual observed
  mismatches as CONTRADICTED.

### Gate, runtime and dispatch

- Next-event rendezvous compares the event anchor, type, payload, timestamp
  and sequence/priority evidence before either handler runs. Absent identity,
  identity mismatch, peer finish or unequal event counts stop/release both
  sides; completion does not authorize unmatched processing.
- Handler completion now precedes `process` and `event_processed` emission.
  Failed handlers do not increment completed counts. Queue failure preserves
  the last completed P02 operation; scheduling a future event does not move
  the current event-loop clock to that future time. Terminal capture is
  idempotent and covers stopped peers at their actual finish boundary.
- Without an observer the dequeue path does not call or scan tie metadata.
  Enabled dequeue capture reports when an earlier same-time internal event
  was actually excluded by the external-before-internal policy. Schedule
  records have null selection cause because selection has not happened.
- `run_authorized_pair` is a preflight-only compatibility API. Even after
  successful preflight and a grant it refuses callback dispatch. Actual
  model construction, source loading/cache identity, trace binding and online
  full-stream comparison are unimplemented and must not be represented as
  enforced. The gate's next-event identity check is not a full PPC-11 online
  comparator.

### File-completion protocol

The record schema version remains `ppc11-paired-trace-1`; no new record family
or envelope field was invented. Successful nonempty writer close creates
`<trace>.complete.json` exclusively, with format `ppc11-file-completion-1`,
raw trace SHA-256, bytes, record count and exact stream identity. The sidecar
is canonical JSON, bounded by the existing line-size limit, and checked by
the parser against independently read bytes and records. Missing, altered,
oversized or stale markers fail closed. Exceptional context-manager exit
leaves no completion marker. Older markerless files fail closed, not ready.
Any record failure also prevents completion certification, even if its
exception was caught by a caller. Existing completion markers are never
overwritten, and marker writes themselves have an explicit byte bound.
This backward-compatible wire sidecar establishes physical file completion
only; it does not certify semantic capture or successful neural execution.

## Changed-file list

Relative to this isolated worktree:

- `experiments\luna71b_c4_2\ppc11\schema.py`
- `experiments\luna71b_c4_2\ppc11\trace.py`
- `experiments\luna71b_c4_2\ppc11\capture.py`
- `experiments\luna71b_c4_2\ppc11\compare.py`
- `experiments\luna71b_c4_2\ppc11\pairing.py`
- `experiments\luna71b_c4_2\ppc11\driver.py`
- `experiments\luna71b_c4_2\variants\original\tpcn\event_runtime.py`
- `experiments\luna71b_c4_2\variants\instrumented\tpcn\event_runtime.py`
- `tests\test_luna71b_c4_2.py`
- `experiments\luna71b_c4_2\reports\source-manifest.json`
- `experiments\luna71b_c4_2\reports\source-and-provenance-inventory.md`
- `experiments\luna71b_c4_2\reports\p01-p11-coverage-matrix.md`
- `experiments\luna71b_c4_2\reports\correction-pass-report.md`
- `experiments\luna71b_c4_2\reports\correction-evidence-hashes.json`

## Validation

Command run from the isolated worktree, using the configured Python 3.11.4:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& C:\Users\Patrick\Documents\ActiveCode\TPCN\.venv-1\Scripts\python.exe tests\test_luna71b_c4_2.py
```

Observed output:

```text
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.605s

OK
```

The suite covers wrong P01 timestamp/order and other family types, integer
tags, branch count/record consistency, four-class/decision cardinalities,
input/scheduler linkage, parameter digest recomputation, refusal of unbound
fixture identities, missing/altered completion markers and clean truncation,
exceptional writer exit and caught record failures, bounded threaded mismatch/peer-finish/unequal-queue
termination, callback refusal even after mocked successful preflight,
disabled metadata no-op, special tie policy, successful/failing handlers and
queue failure. Existing exact bit mismatch, ordering, branch and preflight
tests remain included.

An additional bounded repetition ran the three threaded identity-mismatch,
peer-completion and unequal-queue tests 20 times each: **60 PASS**, with all
threads terminating within the test timeouts.

Only copied event-runtime primitives were loaded under synthetic module
names; no neuron/model/runner source was loaded or run. Generated artifacts
were bounded under the C4.2 directory and removed by test cleanup. Existing
bytecode caches were left untouched; bytecode writing was disabled. Editor
problem checks reported no errors for all nine edited Python files.
Pylance signature checks found no indexed call sites; runtime tests, not that
empty result, provide the callback/signature evidence.

## Current identities and unresolved gates

Current source-manifest SHA-256:
`43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719`.
All 87 listed source/implementation hashes were verified against the corrected
files. Both copied event runtimes are identical:
`e16a48af25657e5a45773248adbed37dd41782f4ef51fba9fd1e2cda013617fd`.
Focused test SHA-256:
`0ad1d9e1e407393b797ace9b04be6a6cd30de45ad00b898e493ffc41b4752697`.
Report and test hashes are retained in `correction-evidence-hashes.json`.

P03 expiry/settlement, P04 omitted-symbol and complete omission lifecycle,
P07 eligibility expiry/capacity outcomes, P08 feedback duplicate/rejection
and schedule provenance, P09 complete source transitions, and actual P11
bilateral source stop evidence remain **INCOMPLETE**. No label information
was inferred. Score-tie source evidence, frozen fixture payload identity,
runtime non-interference, full-context dispatch, online full-stream stopping,
and bilateral neural source traces remain absent/unverified. No frozen
pilot was broadened and no PPC-11 criterion was relaxed.

## Follow-up independent review and bounded fixes

The fresh same-byte Luna-0 review returned **FAIL for the C4.2 correction
review**. It independently verified the source/report hashes and 30-test
synthetic suite, but found three additional defects:

1. Preflight produced `COMMIT+working-tree-sha256:<digest>` while the trace
   schema accepts `COMMIT+sha256:<digest>`.
2. P08 `application_order` reused the current event process order, so multiple
   feedback applications within one event could share an order.
3. Fixture-manifest validation checked required keys and plan identity but
   did not validate the schema tag.

The first two defects are corrected in the PPC-11 driver and capture sink. The
fixture manifest now requires the explicit
`luna71b-c4.2-fixture-payload-manifest-1` schema tag. Synthetic regressions
exercise each defect, including directly validating the preflight-generated
revision with the trace schema and recording two feedback applications within
one event. The frozen fixture payload manifest remains absent; defining its
tag does not create or authorize fixture data.

The refreshed focused suite passes **33 tests**. The previous 60 repeated
threaded regressions apply to the prior correction bytes; they were not
repeated for these three focused changes. The current source manifest and
evidence-hash index must be checked against the finalized report and test
bytes after this addendum.

The independent reviewer found the work **not eligible** for separate
smoke-pilot authorization. P01 fixture identity and required lifecycle/source
evidence remain incomplete. A fresh same-byte review then passed the three
focused corrections, but did not close those gates or approve PPC-11
readiness. See `final-independent-review.md`. No neural training/inference/
pilot, fixture regeneration, commit, push, merge, or publication occurred.
