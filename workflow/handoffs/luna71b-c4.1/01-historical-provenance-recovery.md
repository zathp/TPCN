# Luna-71B-C4.1 Historical Provenance Recovery Assessment

**Disposition:** `RECOVERED_WITH_LIMITATIONS`  
**Prepared:** 2026-10-15  
**Scope:** Documentary recovery, raw-byte hashing, static source/provenance inspection.  
**Authority:** Owner authorization in the C4.1 task request. No source edits, neural execution, paired driver, pilot, commit, push, or publication is authorized.

## Recovery result

All three named C3.1 artifacts were located in the read-only session artifact directory:

`C:\Users\Patrick\.copilot\session-state\339fa321-b273-46ac-b870-d175327b66ac\files`

The prior C4 package was blocked at this provenance gate because those files
were not located during its bounded search. Their current recovery changes
the historical-document availability finding only; it does not establish
capture readiness or retroactively authorize C4 implementation.

| Historical artifact | Bytes | Raw SHA-256 | Reported prefix | Result |
|---|---:|---|---|---|
| `LUNA71B-C-PPC11-C3.1-CORRECTION.md` | 5,967 | `17b566c834c6a726133d3be2f1f59483b3740dc00250a4bd52d4935ff303bf25` | `17b566c8...bf25` | Exact match |
| `LUNA71B-C-PPC11-C3.1-FINAL-REVIEW.md` | 2,768 | `d8989f650ec905a696015b471c11191675668c4002800f1999178351e09ac4dc` | `d8989f65...4dc` | Exact match |
| `LUNA71B-C-PPC11-C3.1-MANIFEST.json` | 2,475 | `99504245b26bb91831d6b3c0e6eead10f83d8b080025d2eeaf4e6291c957017e` | `99504245...017e` | Exact match |

The C3.1 final-review and manifest sidecar files were also present and their
contents name the exact raw SHA-256 values above. The sidecar files' own hashes
are `LUNA71B-C-PPC11-C3.1-FINAL-REVIEW.sha256` (104 bytes,
`df5503e25e85d90f81cda2a3edea8d7608677b488925a574399a130f7652b917`) and
`LUNA71B-C-PPC11-C3.1-MANIFEST.sha256` (101 bytes,
`804b7eaf5d177c2b302ba6bc28b418e39c5f6ba146ec5213abb06116559ad095`).
These are recovered bytes, not reconstructions. Their contents were read
without modification.

## Historical disposition retained

C3.1 reports `INCOMPLETE - CORRECTION REQUIRED` and its final review reports
`PASS WITH LIMITATIONS` for the documentary correction. It establishes neither
source capture completeness nor parity. It records:

- Source-level READY: P01, P04, P05, P10.
- Source-level INCOMPLETE: P02, P03, P06, P07, P08, P09, P11.
- Nine conditional branches: `UNEXERCISED / NOT_EVIDENCED`.
- No reviewed paired driver and no approved diagnostic projection exclusions.
- No authority for paired execution.

C4.1 does not revise those historical dispositions. It supplies a new,
self-contained contract as a possible replacement basis for future,
separately authorized implementation; it does not claim equivalence to C3.1
or erase C3.1's limitations.

The C3.1 final review's three stated limitations also remain part of the
historical record: (D1) the R4 wording differs from the reviewer wording
described in the cause line; (D2) R6 cites `predictive_coding.py:229`, while
the `expire()` call is at line 230; and (D3) traceability from review findings
F1-F8 to corrections R1-R7 is incomplete. These were recorded as having no
effect on C3.1 disposition; C4.1 does not retroactively repair them.

## Other provenance limitations

- The R6 result and manifest raw hashes were independently recomputed from the
  accessible Luna-70 worktree and match the C3.1/C4 records:
  `df54185fcbf02293c24589dbf1fd118c406e6651e1e4744a4ed0119f5715502d`
  and
  `5a28e2950326ce2347760ee128effbd2b38208d5f477242208fb7537f74821fc`.
- The R6 JSON was parsed as static evidence. Its seed-17 train, validation,
  and test content/input-only digests match the six full-split values in the
  recovered paired-pilot plan. The R6 parameter digest
  `5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a`
  appears for arms A-D on seeds 17, 29, and 43; it remains seed-independent
  and does not by itself prove seed identity or loaded historical bytes.
- Both Luna-70 and Luna-71B worktrees report baseline
  `f117ce51e7a805564e37252d3b5c99bda163ce57`. C4 worktree artifacts were
  read-only inputs and were not changed.
- The historical Luna-71A package remains unavailable.
- The recorded initial-parameter digest is seed-independent and does not by
  itself prove seed identity or historical loaded bytes.
- Historical source-to-run lineage is not independently established.

The exact source identities and these limitations are expanded in
[`04-source-identity-inventory.md`](./04-source-identity-inventory.md).
