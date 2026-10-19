# Luna-71B-C4.2-I — Historical identity disposition

**Disposition:** **PARTIAL / BLOCKED** for historical C4.2 identity reconciliation.  
**Method:** Compare exact bytes, Git objects, checkout materialization, and recorded revisions. No historical preimage is inferred or rewritten.

## Identities with exact available bytes

| Artifact/identity | Full SHA-256 | Size | Git identity / revision | Classification |
|---|---|---:|---|---|
| Published C4.2 source manifest, `experiments/luna71b_c4_2/reports/source-manifest.json` | `d3edfd73c4ac9f183f145d49fac4d01e8ca5aaf552f681ddd2bdd253dbccf5a7` | 14,826 LF blob bytes | Git blob SHA-1 `85f1f2c79f69ee675fa8ab600be74bbf2469a3cc`; C4.2 commit `e91818a5c974282e848dc43e52d3c0a534dcbf45`, tree `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749` | **RECOVERED**; committed source-manifest bytes |
| Same manifest, current Windows checkout | `84070d2a414dc037611e842e71faf4fab66736e8a38a1f59465c2584a69ae383` | 15,266 CRLF bytes | Same committed blob/path; conversion adds 440 CR bytes | **RECOVERED** materialization of the same manifest. LF/CRLF explains `d3ed…` versus `84070…` only. |
| Published C4.2 test source, `tests/test_luna71b_c4_2.py`, LF blob | `a02fd154e7d7d25866418f8d3990586c0a8151a493016e90814451ddd6a8535b` | 45,169 LF blob bytes | Git blob SHA-1 `4758d9a45f7aaecf487c57e489717dd8750e2df1`; C4.2 commit/tree above | **RECOVERED**; committed test bytes |
| Same test, current Windows checkout | `d7c4c90bf4ed7cc1871b835b5f620132cfcb14f6fba6ca83d485f57d49251c83` | 45,985 CRLF bytes | Same committed blob/path; 816 added CR bytes | **RECOVERED** materialization of the same test. It is not the H GN test file. |

The two current H references are different artifacts and are not evidence
that either historical reference below is correct. The canonical LF blob SHA
and raw CRLF checkout SHA are distinct raw-byte identities, not interchangeable
hashes.

## Unavailable historical references

| Historical reference | Full SHA-256 | Exact bytes / size / Git object / revision | Classification |
|---|---|---|---|
| Historical source-manifest reference cited by correction records | `43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719` | Exact preimage, byte size, Git blob and source revision not recovered | **UNRESOLVED**. Not declared incorrect or superseded. |
| Historical test-index reference cited by correction records | `0ad1d9e1e407393b797ace9b04be6a6cd30de45ad00b898e493ffc41b4752697` | Exact preimage, byte size, Git object, and what exact index bytes were hashed are not recovered | **UNRESOLVED**. Not equated with the test source file or manifest. |

No evidence distinguishes a different historical revision, changed manifest
contents/inventory, superseded index, mistaken reference, or another cause
for these two values. Therefore neither is classified `INCORRECT REFERENCE`.
The LF/CRLF cause is independently demonstrated for the `d3ed…` /
`84070…` pair and does not resolve `43fb…` or `0ad1…`.

## Historical pilot-plan copy and new C4.2-N lineage

The untracked H copy
`experiments/luna71b_c4_2/inputs/L71B-C-paired-pilot-plan.json` is 133,178
bytes, raw SHA-256
`60cde6b4929be4408fcecdcf3ac7104d5cb7b3365d94d55b568431e54fb5bc3f`.
Its bytes match the exact file at
`TPCN-luna71b/artifacts/luna71b/L71B-C-paired-pilot-plan.json` (133,178
bytes, same SHA-256) and the recovered C4.1 source-identity inventory. The
source worktree is branch `experiment/luna71b-instrumented-learning`,
HEAD `f117ce51e7a805564e37252d3b5c99bda163ce57`; the plan itself is
untracked there, so no committed Git object or revision binding exists. The
H copy is thus an exact-content copy of a recovered plan, but its copy-time
provenance and any use by H are not established.

The new fixture `L71B-C4.2-N-FOURCLASS-SEED17-V1` remains a separate
experimental identity:

* fixture manifest: 2,368 bytes, SHA-256
  `839e58df80da69cdf7b63618afc9626b85a9aa9817885931189c58a6f9658f40`;
* event payload identity: 39,796 bytes, SHA-256
  `520b1cedfeefe8b285d02dba7d26583f6581ac29cd82dc8571a4b9ba5ed4970e`;
* initial parameters: 112 bytes, SHA-256
  `5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a`.

The matching old plan copy does not turn this new fixture into the historical
R6 fixture, establish that the H driver consumed the plan, or recover the
`43fb…` / `0ad1…` preimages.

## Separate lineage proposal

Any future C4.2-N qualification should bind a new lineage without R6
substitution:

1. exact source revision and commit/tree plus full per-file raw source
   manifest; uncommitted H bytes require separate hashes;
2. schema/contract version and independent implementation identity manifests;
3. builder/preprocessor source identity and invocation/seed metadata;
4. exact config and runtime/dependency manifests;
5. fixture ID, manifest, each split payload, and initial-parameter bytes;
6. per-side run IDs and raw trace identities if execution is separately
   authorized; and
7. explicit `NEW_C4.2_N_LINEAGE`, with an explicit non-claim of historical R6
   equivalence.

This lineage may support a future separately authorized C4.2-N parity
question; it cannot satisfy a C4.1 historical reproduction obligation or
waive a frozen C4.1 requirement.

## Published C4.1 dependencies that remain mandatory

Under PPC-11 C4.1 §1, any claim to reproduce its frozen R6 pairing still
requires the exact historical preparation artifacts and all six train,
validation, and test full-split identities, plus independently identified
source/runtime and initial-parameter manifests. Counts or a replacement
fixture are not substitutes. The C4.1 text does not name the `43fb…` or
`0ad1…` digests as standalone acceptance fields; those are unresolved
references in later correction evidence. Their missing preimages are therefore
not silently declared a C4.1 waiver or a known C4.1 blocker by digest alone.
If either is offered as evidence for a required C4.1 source/test lineage, that
claim remains blocked until its bytes and role are established. Independently,
the historical split/source-to-run lineage requirements of C4.1 remain
mandatory and are not satisfied by C4.2-N.

## Conclusion

Disposition is **PARTIAL / BLOCKED**. The two historical references remain
unresolved. No historical artifact was changed, substituted, or declared
incorrect. A future C4.2-N lineage can be independent, but cannot retroactively
authenticate R6 or satisfy PPC-11 C4.1.
