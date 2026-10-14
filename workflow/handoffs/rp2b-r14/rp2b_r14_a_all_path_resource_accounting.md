# RP-2B R14-A — All-Path Resource Accounting and Bound Ledger

**Disposition: BLOCKED — BOUND INCOMPLETE**

Read-only static accounting review. The source shows local limits and
structural producer counts, but does not establish a complete mandatory
evidence inventory, all-attempt transport maximum, simultaneous live-copy
maximum, terminal sufficiency, or frozen-profile feasibility. This is not a
finding that fit is impossible.

```yaml
frozen_total_max_bytes: null
proposed_total_max_bytes: null
proposed_headroom_bytes: null
N_LOW_all_attempt_max: unsupported
T_LOW_all_attempt_max_bytes: unsupported
```

No source was executed or imported; no tests, compilation, preflight, or
runtime checks were performed.

## Identity and authority

Baseline: branch `governance/luna64-r4.3-freeze-20261010`, HEAD
`f117ce51e7a805564e37252d3b5c99bda163ce57`.

Pinned source identities:

| Alias | Source | SHA-256 |
|---|---|---|
| P | `scripts/luna65_phase2a_rp2_compatibility_probe.py` | `B8F669C68ED5768E4126FFA87E855002A5E7E5E116999E81E4AAE1CA69CE2427` |
| O | `scripts/luna65_phase2a_rp2_outer_wrapper.ps1` | `F7C39C0FC849F61AFFF71A07AC8DCC7BDBEBA91D9971B44BCCF96B0C01ABE2A7` |

Other controlling sources: RP-2 contract C §§4–6,
`workflow/docs/luna/LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md`;
outer launcher L §§4–5,
`workflow/docs/luna/LUNA_65_PHASE2A_RP2_OUTER_LAUNCHER_CORRECTIVE_R1.md`;
direct design D; R1 owner decision closure OD; and Phase 2A R2.
R13 inputs are identified in `rp2b_r13_artifact_manifest.md` (SHA-256
`8A42FA81C618ED3B7E6A6DE30CE83A16A6322C2053E61E57FCDBFD9C0ED440EB`).
The owner-direction record `rp2b_r13_owner_decision_ratification_candidate.md`
(SHA-256 `51273432061A87E554EFD2D5F1F8341030FDA026496D256B31E3F30C1F77A423`)
records the supplied policy direction, not additional owner authority.

Policy boundary retained: OD-1/A mandatory families, OD-2/A full-copy and
recovery duties, OD-3 Sink A / Alert 1, OD-4/C deferred unresolved new
admission/terminal behavior, OD-5/A unchanged accepted bytes/grammar, and
OD-6/R-A frozen RP-2 profile. No new family, exclusion, bound, admission
rule, result, or resource metric is introduced here.

## Accounting boundaries and distinct quantities

| Quantity | Owner / lifetime | What it measures | What it does not establish |
|---|---|---|---|
| 64 MiB Job Object job-memory charge | Windows job containing L and descendants; P configures/observes it (P:1041–1071, 1098–1111) | Frozen job memory accounting/limit | Total P/O process memory, private commit, working set, host memory, serialized bytes, or retained-artifact fit |
| P private bytes / working set | P outside its owned Low job (P:1092–1111) | Distinct observations | A resource cap or evidence-size measurement |
| Python/.NET/native object memory | L, P and O; overlapping runtime/callback/thread/snapshot lifetimes | Object graphs, allocator capacity and native buffers | JSON length or job-memory charge |
| Logical retained representations | Cross-boundary O-led accounting (C:315–330; L:194–213) | Concurrent encoded/raw/decoded/structured/intermediate copies | Physical memory measurement |
| Persistent artifact bytes | O evidence leaf | File bytes, including partial-prefix uncertainty | Same as emitted bytes, successful relay bytes, counters or memory projections |
| Unretained pipe bytes | Three L→P and two P→O pipes | Kernel transport buffering | Retained artifact size; contract still requires read/discard accounting (C:317–318) |

O is the attended outer process; P is the supervised Medium process; L is
the intended Low job member. O cannot independently observe Low cessation
after P loss (L:175–180, 215–225; OD:75–100).

## Identifiable producer families and local bounds

Counts below are structural producer bounds, not evidence that all required
members are emitted, recovered, or retained.

| Family / owner / lifetime | Count and width evidence | Missing proof |
|---|---|---|
| Low explicit READY/END, L→P→O, all streams | At most six explicit writes: one READY and END per stdout/stderr/ledger. Each serialized write including LF is capped at 16,384 bytes (P:185–228). | Does not cover startup/import/error diagnostics or all Low output. READY observations are separately serialized three times; module/path/string widths and pre-serialization object peak lack independent maxima. |
| Low READY/END accepted records | Six phase slots; per-line P cap is 16,384 excluding LF (P:870–873, 1293–1338). O independently validates stream grammar (O:697–722, 998–999). | Producer LF-inclusive, P LF-exclusive, and O buffer predicates differ; no single proved acceptance boundary or whole-stream maximum. |
| Low original files | Up to three files, retained after capture (O:670–684; C:270–277; L:194–204). | Whole-stream byte maxima are not independently enforced. |
| U1 token/descriptor/object-binding records | Normal inspected graph has 14 U1 emission sites, each reached at most once; successfully emitted relay record ≤16 KiB. Token/SD buffers ≤65,536 bytes; several enumerations ≤256 entries (P:443–608, 978–1035, 1413–1476). | SD raw hex can be 131,072 characters before decoded ACEs/JSON; a 64 KiB native input cap does not guarantee 16 KiB serialized fit. Recursive diagnostic values/co-occurrence and pre-serialization peak are not bounded. |
| U2 closure/identity/job/resource | `closure`, `ambient-job`, `job-configured`, `Low-identity`: ≤1 each; each successful record ≤16 KiB (P:1069–1071, 1362–1384, 1413). | `resources` has no established all-path call ceiling; `unexpected-descendant` may repeat in cleanup (P:1073–1113, 1078–1089, 1573–1577). Eight-process backstop is not a family-cardinality bound. |
| U3 inventories/comparisons | With \(n_p,n_s,n_r\le256\): entries \(n_p+n_s+n_r\le768\); completion records ≤3; comparisons ≤512; structural total \(n_p+2n_s+2n_r+3\le1283\) (P:1115–1224, 1404, 1425, 1461). Record cap 16 KiB. | Aggregate relay cap can stop before this structural maximum; inventory and comparison records can coexist; native snapshots/markers/reference lifetimes lack complete memory and byte maxima. |
| Controller and cleanup | P0 ≤1; BEFORE_LOW_ATTEMPT and CREATE_RESULT ≤1 each; NO_LOW_CREATED ≤2 across alternative/cleanup routes; CLEANUP_BEGIN ≤1; each termination request ≤1; FINAL one attempted emission (P:1270–1288, 1362–1369, 1527–1545, 1627–1654). | Branch co-occurrence must be modeled; FINAL can fail serialization/admission/write. P stderr fallback `repr(error)` and NativeWorker error strings are not width-bounded (P:1673–1682, 1783–1787). |
| O records and metadata | `outer.jsonl`: ≤8 successful records in inspected normal graph; seven retained metadata slots, each admitted JSON ≤16 KiB (O:611–620, 649–654, 694, 754–764, 833–925). | Conditional branches and replacement temporaries; count is not a complete terminal or external-governance inventory. |
| O files, indexes and final report | Up to ten named files: two Medium captures, three U files, three Low files, outer JSONL and report (O:632–643, 670–688, 832, 1033). Pre-report index ≤9 entries; report is one attempted write (O:1009–1036). | Report has no separate 16 KiB cap; its JSON/index/summary/hash representations and partial writes lack a complete maximum. The report excludes itself from its index; its hash is printed to console. |
| Console, governance and operator material | Identified O warning, controller/finalization errors, success summary, and P cleanup stderr (O:83–85, 944–947, 1036–1037; P:1783–1787). | Unhandled/startup diagnostics and external operator/review/governance material lack complete inclusion, schema, byte bound, sink and custody. Console output is not durable evidence merely because attempted. |

Failure strings: P bounded-error list caps eight entries and direct strings
to 512 characters, but nested values are not recursively bounded; worker
error strings remain unsliced. O failure list caps eight and direct strings
but not nested structures (P:254–269, 1673–1682; O:622–631).

## `N_LOW`, `T_LOW`, and LOW_BYTES framing

The explicit literal READY/END calls have a finite subset:

```text
N_explicit <= 6
T_explicit <= 6 * 16,384 = 98,304 bytes
```

These are not bounds for all-attempt `N_LOW` or `T_LOW`: imports/startup
precede the capped emitter; diagnostic output can escape the explicit
grammar/caps; a time limit or bounded read buffer does not bound total
emitted bytes; and no whole-attempt Low count/byte counter closes the
failure paths (P:85–89, 208–228, 1706–1740).

For raw chunk length \(n\), stream-name width \(s\), sequence decimal width
\(d_q\), and tick width \(d_t\), successfully serialized `LOW_BYTES` has
width:

\[
B=2n+180+s+d(n)+d_q+d_t.
\]

Here \(1\le n\le4096\), \(s=6\), \(d(n)\le4\), and tick is at most 20
digits; the sequence has no explicit six-digit ceiling (P:916–925,
1340–1349; O:679–683). Example: \(n=1\), sequence 1, tick 0 is 191 bytes.
P's counted-success relay thresholds are 458,752 ordinary and 491,520
reserve-stage bytes, but failed/short writes do not increment `sent`
(P:924–938). Thus no complete submitted/accepted transport bound follows.

## Transport, partial-write, recovery, and copy accounting

| Surface | Local limit | Overlap / unresolved behavior |
|---|---|---|
| L `WriteFile` | Explicit string ≤16,384 | ASCII bytes and native `create_string_buffer` coexist; short/failing write raises without accepted-prefix ledger (P:208–221). |
| L→P pipe | Three 4,096-byte native readers; per-reader pending ≤16,384 | No whole-attempt counter; `buffer.raw`/slicing make transients (P:1706–1740). |
| P assembly/relay | Line checked after extension; record ≤16,384 | Rejected data already allocated; partition/remainder/bytes copies overlap; P pops pending chunk before relay emit, so emit failure can lose the chunk from later accounting (P:1340–1359, 1583–1588). |
| P→O pipe | Two 4,096-byte reader arrays | Backpressure is not a whole-output bound; O copies raw chunk (O:278–318, 512–531, 724–750). |
| O relay/parser | Pending line check 16,384 | `$Line.ToArray()`, ASCII text, parsed object, raw chunk and hex/decode copies overlap (O:655–694, 737–744). |
| O artifact write | Pre-write `Charge` | `FileStream.Write` may fail after uncertain prefix; `Length`/`DiskBytes` increment only after return, so write uncertainty lacks explicit prefix accounting (O:632–643). |
| O drain cleanup | Reader count cleared after write/parse | Exception before clearing can leave chunk published and cleanup re-drains it; no exactly-once/prefix custody proof (O:724–750, 953–954). |
| O flush/close/hash | Final reconciliation | Later length checks detect some drift if reached, but cannot reconstruct accounting after sink failure or prove earlier high-water (O:1009–1037). |

Full-copy disk component for complete reconciled files:
\[
D=R+E+L_b+U+A+F
\]
where R/E are Medium stdout/stderr, \(L_b\) original Low bytes, U separate
U1–U3 JSONL copies, A outer JSONL and F report. For an ideal reconstructed
relay, Low content appears as \(2L_b\) hex characters in R plus \(L_b\)
original bytes; U also appears in R and U. Framing is additional. This
identity is not an all-path bound; malformed, partial or replayed output
requires the actual captured R/E copies. L:194–204 requires independent
recovery of U1–U3 and original Low stream bytes/order.

Simultaneously live representations include: L runtime/observation/JSON/
ASCII/native-write buffers; P reader buffers, pending/popped chunks, hex,
relay dictionary/text/bytes, partial lines, decoded JSON, phase metadata,
snapshots, SD/token raw and decoded forms, callbacks/workers, command and
attributes; O reader buffers, raw copies, line arrays, strings/parsed
objects, hex/decoded Low bytes, U-line copies, files/index, metadata,
runspaces/pipelines, report/index/summary/JSON buffers and hash state.
Unjoined workers or unresolved Low state can outlive cleanup; storage is
intentionally retained rather than freed unsafely (O:984–991; P:1609–1625).

P's metadata formula permits at most 118,784 bytes **in its selected
projection ledger**, calculated as
`393216 - 65536 - 9*16384 - 49152 - 3*4096`. It does not prove Python,
native, or all simultaneous representation size. Likewise, P's 2x and O's
3x projection multipliers do not prove object graph or transient peaks.

## The 131,072-byte finalization constant

C:289, 324–328 and L:206–213 require payload/reserve separation and terminal
accounting. The code does not establish this constant as a sufficient or
reachable reserve:

1. P's reserve-stage relay threshold adds 32,768 bytes; it does not derive
   terminal maxima (P:23–26, 924–925).
2. O final records can use total rather than payload limit (O:604–610), but
   raw Medium capture containing P FINAL must first pass ordinary payload
   admission before O can parse it (O:734–740).
3. Cleanup records and failure families do not all receive terminal
   admission automatically.
4. Several representations are constructed before guards; rejected
   representations already exist.
5. O's `$OMemoryBase=131072` is a transient-memory allowance, not evidence
   that the identically sized artifact reserve fits terminal obligations
   (O:773–775).
6. Final report, FinalP, errors, stop records, concurrent captures,
   serialization copies, partial-write uncertainty, hashing/flush/close,
   console/governance material and deadlines lack a joint maximum and
   reachability proof.

## Symbolic bound and disposition

A complete logical model would require, for every path p and time t:

\[
B(p,t)=D_{\rm known}+W_{\rm uncertain}+L_{\rm retained}+P_{\rm retained}
+O_{\rm retained}+X_{\rm console/governance}.
\]

This includes reconciled files, uncertain persisted prefixes, simultaneous
retained raw/encoded/decoded/structured/intermediate forms for L/P/O, and
required retained external material after its boundary/schema is defined.
Unretained kernel pipes are excluded from artifact bytes but their counters
and retained copies remain obligations. A supported total would require
\(\sup_{p,t}B(p,t)\le1,048,576\) plus a separate terminal admission proof.
Multiple terms remain unsupported, so this expression cannot be populated
as a numeric total or headroom.

**Disposition: BLOCKED — BOUND INCOMPLETE.** Specifically unsupported are
all-attempt `N_LOW`/`T_LOW`, diagnostic transport maxima, complete mandatory
family/schema maxima, partial-write prefix/custody accounting, all
simultaneous-copy/native-worker lifetimes, external console/operator/
governance bounds, 131,072-byte reserve sufficiency/reachability, and
frozen-profile feasibility. This is not a claim of infeasibility. Preserve
`RP2_UNKNOWN_FAIL_CLOSED` for missing required Low cessation; invent no new
admission or result semantics.
