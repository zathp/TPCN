# RP-2B R14-C — P/O Interface and Semantic-Preservation Assessment

**Disposition: BLOCKED — complete interface scope not established.**
P and O remain candidate source locations, not an approved Category I
allowlist. This is read-only source analysis; no program was executed or
imported.

## Baseline and identity

Branch `governance/luna64-r4.3-freeze-20261010`; HEAD
`f117ce51e7a805564e37252d3b5c99bda163ce57`.

| Alias | Path | SHA-256 |
|---|---|---|
| P | `scripts/luna65_phase2a_rp2_compatibility_probe.py` | `B8F669C68ED5768E4126FFA87E855002A5E7E5E116999E81E4AAE1CA69CE2427` |
| O | `scripts/luna65_phase2a_rp2_outer_wrapper.ps1` | `F7C39C0FC849F61AFFF71A07AC8DCC7BDBEBA91D9971B44BCCF96B0C01ABE2A7` |

R13 policy directions retained: mandatory families; full-copy/recovery
duties; Sink A / Alert 1 and existing operator warning; OD-4 deferral;
unchanged bytes/ordering; frozen RP-2 profile.

## Interface map

| Boundary | Source references | Input/output and behavior | Unresolved interface |
|---|---|---|---|
| Attended operator → O | O parameters, lines 4–28; startup around 790+ | O accepts RunId, EvidenceLeaf and reviewed source hashes, validates route and dependencies. | Full caller, attended procedure, host evidence/custody and operator-record boundary are outside P/O. |
| O → P Medium process | O process/pipe setup and creation around 800–940; P `main` 1743+ | O launches pinned Python with P, `--rp2`, fixed nonce, decimal O0 and 20,000; supplies three environment variables and captures stdout/stderr separately. | Full launch failure, external host/operator state and all cleanup interactions require cross-call review. |
| P → embedded Low producer | P literal 84–231, `environment` 695, `Controller.create` 1241 | P constructs `-B -c` with restricted token and three inherited stdout/stderr/ledger write handles. Low receives fixed Python variables, SYSTEMROOT and ledger handle. | Embedded literal is only one producer; interpreter startup/import/error diagnostics may add output. |
| Low output → P | Embedded emit 208–231; `NativeReader.read_loop` 1717; `Controller.drain` 1340 | Low writes compact sorted ASCII JSON + LF on three independent streams; READY then END per stream. P reads 4 KiB chunks, buffers incomplete lines and parses records. | No global chronology across streams; interruption and partial writes lack prefix/custody proof. |
| P parse → relay | `Controller.accept_line` 1293; `drain` 1340; `emit` 916 | P checks ASCII/length/schema/nonce/PID/stream/phase and emits sequenced `LOW_BYTES` hex relay records. | Record thresholds and sequence checks are local predicates, not a complete all-attempt transport maximum. |
| O relay ingress → evidence | `Drain-Medium` 724; `Receive-Relay` 655; `Write-Artifact` 632; `Validate-LowStreams` 697 | O records Medium stdout/stderr, validates relay schema/sequence and decodes hex into three original Low files; U1/U2/U3 lines are also retained. | O line/decoder/copy lifetime, prefix uncertainty, replay handling and all-path retained-byte reconciliation remain incomplete. |
| Evidence / terminal output | `Record-O`/`Json-Bytes` 645–654; finalization 998–1042; `Alert-Unresolved` 83–85 | O writes outer JSONL, Low originals, Medium captures, U-section copies and final report; console summary and unresolved warning are emitted separately. | Console/evidence boundary, sink/custody and attempt-vs-delivery evidence remain open. |

## Byte, ordering, grammar, EOF and sequence observations

Low writes READY then END per stream, but three pipes provide no global
cross-stream chronology. P relay sequence reflects its read/drain traversal,
not original global write order. O preserves bytes/order within reconstructed
streams and Medium stdout relay-line order, not global Low inter-stream
chronology.

Framing is LF-based. The producer's 16,384-byte cap includes LF; P's parser
cap is on the line without LF; O has a separate line-buffer predicate. P
rejects a nonempty truncated buffer at EOF. O's complete-path validator
checks ASCII, LF framing, stream order and counts. These predicates do not
yet define one proven acceptance boundary.

Successful complete relay/decode can preserve per-stream bytes. It does not
prove byte/custody reconciliation under every interruption/partial-write
path or prove a future change preserves the accepted set.

## Admission, ownership, error paths

P refusal points include Low schema/identity/phase checks, partial-line and
reader caps, metadata/parse reservations, relay record/aggregate/
representation guards, and embedded producer write/record checks. O refusal
points include line/ASCII/sequence/P0 checks, Low-bytes encoding/length/hex
validation, metadata/record checks, payload/final `Charge`, path checks,
final byte reconciliation and independent Low-grammar validation.

P retains reader chunks, pending/partial lines, parsed observations,
metadata and relay serialization. O holds reader buffers, copied raw chunks,
partial lines, decoded objects, hex and Low raw bytes, files and metadata.
`Charge`/`Retain-O` and P reservations do not prove all simultaneous
lifetimes. O increments persisted lengths only after `FileStream.Write`
returns; uncertain partial writes are not fully accounted. P removes a
pending chunk before relay emission; if emission fails, later pending/line
discard counts may not account for that chunk. O may re-drain a published
chunk if failure occurs before reader count clearing; exactly-once/prefix
custody is not established.

P and O have existing failure classifications and precedence; a new refusal
can change result or terminal reachability. Under OD-4/C, do not assign a
new result to an unmapped refusal or incomplete terminal condition.

### Candidate O finalization and alert exception paths

O:998–1007 selects `$Verdict` before finalization. O:1009–1037 writes,
flushes/closes, hashes, and prints the report summary. An exception in that
finalization block enters O:1038, which unconditionally changes the
in-process verdict to `RP2_UNKNOWN_FAIL_CLOSED` and invokes
`Alert-Unresolved`, regardless of previously established cessation.
`report.json` is written at O:1033 before the subsequent flush/close/hash/
console operations; a later exception can therefore leave an already-written
report with an earlier verdict while process state becomes UNKNOWN, without
rewriting that report.

`Alert-Unresolved` directly calls `[Console]::Error.WriteLine` at O:83–85.
Calls at O:1001 and O:1038 have no enclosing handler that guarantees
continuation if that call throws. Attempt, successful return, delivery,
observation and durable retention are distinct. An alert exception may
interrupt subsequent report finalization or disposal; completed cleanup is
not guaranteed by the call site.

These are observed candidate-source behaviors, not proof of contractual
equivalence. The contract separately states confirmed cessation with
incomplete finalization is at least PARTIAL, while known contradictions
retain their classification (C:312–313, 359–366, 631). Reconciliation is
required; no source repair or replacement result is authorized under OD-4/C.

## Semantic-preservation result

Pure internal bookkeeping might preserve behavior in principle only if it
adds no refusal, timing-sensitive branch, altered output, result change, or
new simultaneous representation. This is not demonstrated by existing
source evidence. A new cap or guard may reject formerly accepted Low input;
that is an accepted-set change and cannot be characterized as harmless merely
because it is called validation or a memory-safety check.

P/O depend on Windows process/token/job/pipe/handle/thread/filesystem APIs,
pinned Python/PowerShell/.NET images, dependency closures, attended console
and external evidence filesystem. Full caller, sink/custody environment,
every producer/result/failure/cleanup path, native buffer/pipe lifetimes,
terminal admission and P→O interface sufficiency are not closed.

**SOURCE ALLOWLIST: BLOCKED / NOT APPROVED.** P/O remain candidates only.
No exact correction diff, all-call-site map, accepted-set proof or
independently complete source scope has been established.
