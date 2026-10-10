# Luna-63C corrective reconciliation and publication review

**Disposition before this correction: BLOCKED.** This report records the
bounded correction against the exact uncommitted source snapshot at
`19caa49d7620062c06ad74d19528e47725f86b37`. The prior independent PASS at
`8f5e785bd2e46c0c1cb2afbb77ba53704adef65a` remains limited to that reviewed
nine-file publication; it is not approval of the later source-checkout
bundle.

## Authoritative references and status

The following Git objects were verified locally as commits, and the
corresponding local remote-tracking refs identify the listed lane commits:

| Evidence | Verified commit | Scope |
|---|---|---|
| C0-C7 fixture freeze | `583148e2812b93d519a3dc2821944d08446497b7` | Frozen fixture authority |
| W | `17907c67d52cc338249b66f28c3179cd97572c6e` | 100/100 assigned witness rows; scoped result |
| T | `0a8c34b7e6febf681917d915082a8559eea998f7` | 9/191 mappings certified; 182 blocked; N3 open |
| E | `651f18fdf3c7ae8e32cd210ebc68527f86531e32` | 1,905-row N4 audit evidence |
| Prior reviewed governance publication | `8f5e785bd2e46c0c1cb2afbb77ba53704adef65a` | Exact prior review/publication scope only |

The E coverage matrix at the pinned commit was parsed without executing E:
568 applicable N4-A rows are PASS, with zero N4-A BLOCKED or N/A rows.
N4-B has 55 PASS, 1,128 BLOCKED, and 154 N/A rows. Therefore **applicable
N4-A audit obligations pass; this does not certify a future candidate
implementation; N4-B remains incomplete; overall N4 is not closed**. Global
N1/N3/N4 closure is not established, Lane S/N5 is unauthorized, N6 is
deferred, and Stage B remains blocked.

## Claim reconciliation

| Source-checkout claim at the blocked snapshot | Corrected interpretation and destination |
|---|---|
| Changelog and Luna workflow described N4-A as blocked overall because candidate-comparison/protocol evidence was absent. | The pinned E matrix shows all 568 applicable N4-A audit rows PASS. The corrected [changelog](../../../workflow/ARCHITECTURE_CHANGELOG.md) and [workflow](../../../workflow/docs/luna/LUNA_WORKFLOW.md) explicitly separate audited N4-A evidence from future candidate implementation certification, state N4-B is incomplete, and keep overall N4 open. |
| Decision package, preservation report, publication manifest, and handoff contained variants of “overall N4-A blocked.” | The exact prior approved versions of the decision package, preservation report, manifest, and handoff already state the scoped N4-A pass/N4-B incomplete distinction. They are retained from commit `8f5e785...`; the corrected manifest is refreshed for the new allowlist. The superseded uncommitted source copies remain untouched. |
| Preservation report and sanitized inventory said local W `INVENTORY.md`, `README.md`, and the W handoff failed their local W manifest. | All three normalized local SHA-256 values match the corresponding entries in the local W manifest. Local manifest consistency is separate from comparison to published W. The report and sanitized inventory now say so. |
| The schedule-reconciliation handoff used `0a8c34b7d52cc338249b66f28c3179cd97572c6e`. | `git cat-file -t` fails for that value. The verified T object and `origin/experiment/luna63c-stage-a-T` are `0a8c34b7e6febf681917d915082a8559eea998f7`. The corrected handoff below uses the verified identity. |

The preserved source-checkout copies of the decision package and handoff
remain part of the inventory and are not copied over the prior reviewed
publication. The corrected governance branch retains the accurate reviewed
versions and adds this reconciliation.

## W local-manifest and published-tree reconciliation

All raw local hashes were computed from the preserved source checkout. Local
manifest hashes are LF-normalized SHA-256 values as specified by that
manifest. Git blob IDs below are repository/path-filtered identities.

| Local artifact | Local raw SHA-256 | Local manifest LF SHA-256 | Local Git blob | Published W same-path artifact | Published raw SHA-256 / Git blob | Result |
|---|---|---|---|---|---|---|
| `experiments/luna63c/certificate/lane-w/INVENTORY.md` | `cfd27c3827416b66d663880c86d820f5860bf04face35780681ac4a8d86d60f9` | `918cf5d99794784e2ee256abd953ef6c075b09e5902bdb15b6a75787036df020` | `18790c70bdae2a0b9ed48b617eaacf625b2f45f5` | None; no same-path published W artifact | None | Local manifest PASS; no byte-level published counterpart |
| `experiments/luna63c/certificate/lane-w/README.md` | `b86fb4685f904ae38e7d9bfda4cfcd96bc7a54912acdb94324b72e7670b22000` | `312d99b71fa146fa7b083cd03d2c6cdd1e90e42d8e684a7ce21402a7f0c31f2e` | `4162df9c68db56851d4c8a7b3f907c58b3c450ff` | None; the published W tree has no README | None | Local manifest PASS; no published path comparison |
| `workflow/handoffs/luna63c-stage-a-lane-w-20261010.md` | `6c614cbe8ffda99c5428151af0abc9163a8fedece676c59199ddace08a8ddc78` | `feb81f65bd52b22475f8cf0e2ccc8eef941d29f0703e6c686aee12dd463e9a7e` | `79c45209552bf7b0165599edbc6e36966ea39102` | `workflow/handoffs/luna63c-stage-a-lane-w-20261010.md` | `08ee8d6aaf36985931d5b495bb332187d93ba2cd07ef7b3ba9a24712b79dbd39` / `69a88ad609c514cceff0a275fdfc8afce7109682` | Local manifest PASS; same-path published handoff differs |

For context only, the published W `coverage_matrix.json` has raw SHA-256
`0b5ab09ae5e4a29ad951b00563c64f5d445d0665b332154c9d40f93335f90d9f` and
Git blob `3fa1379959916275ecbb9aaae57fa981aa5931b0`; it is not a
same-path substitute for either local Markdown file. No same-path published
`INVENTORY.md` or `README.md` exists. The reason the local handoff differs is
unknown. No local W file gains certification authority from matching its
local manifest. Preserve all versions; the pinned published W commit is the
authority for its 100 assigned witness rows.

The local W manifest lists ten package artifacts plus the separate W
handoff; its own hash is excluded. All declared local W file hashes were
checked. Correspondence to the published W tree is a distinct test: the
local W manifest and handoff have different published same-path blobs, and
other local-only names have no same-path published object. The local W
manifest blob is `0577664b150965954b56f1105d84cb636bcf7b44`; the published
manifest blob is `47d5488ab150dc154b70c3a27bda6c44271b7fa3`. The local T and E
package manifests' declared file hashes also pass their local checks; their
differences from published trees are not local-manifest failures.

## Full source-checkout inventory and preservation

The pre-edit source inventory is
[`UNCOMMITTED_ARTIFACT_INVENTORY.json`](UNCOMMITTED_ARTIFACT_INVENTORY.json).
It contains relative paths, source states, raw SHA-256, byte size, text-line
count where applicable, category, local-manifest result, and published
same-path/blob comparison for 68 records:

| Category | Count | Disposition |
|---|---:|---|
| A — governance / decision-preparation | 5 | Corrected governance paths may be included only through the allowlist below |
| B — supplemental governance/provenance manifest | 1 | Included only as corrected review metadata |
| C — historical W/T/E data, documents, and handoffs | 20 | Preserve; exclude from authoritative publication |
| D — Python calculation/generation/integrity/test scripts | 12 | Static review only; preserve; exclude from this publication |
| E — exact duplicates already in the approved governance commit | 3 | Already present; do not republish |
| F — local-only snapshot and ignored engine files | 27 | Preserve locally; exclude |

At snapshot HEAD `19caa49d7620062c06ad74d19528e47725f86b37`, the source
checkout had 42 visible changed files (2 modified tracked, 40 untracked),
33,010 text lines and 1,869,818 bytes. The 26 ignored `.engine` files total
4,049,892 bytes; binary payload has no text-line count. The earlier 43,785
line estimate included binary bytes interpreted as text and is superseded.
The original checkout, 40 untracked files, two modified documents, local-only
unredacted reconciliation snapshot, ignored engine payload, and sibling
lane worktrees were not edited, staged, or deleted.

The exact proposed changed-path allowlist is:

1. `workflow/ARCHITECTURE_CHANGELOG.md`
2. `workflow/docs/luna/LUNA_WORKFLOW.md`
3. `experiments/luna63c/certificate/temporal-schedule-decision/PRESERVATION_REPORT.md`
4. `experiments/luna63c/certificate/temporal-schedule-decision/PUBLICATION_ARTIFACT_RECONCILIATION.json`
5. `experiments/luna63c/certificate/temporal-schedule-decision/PUBLICATION_MANIFEST.json`
6. `experiments/luna63c/certificate/temporal-schedule-decision/CORRECTIVE_RECONCILIATION.md`
7. `experiments/luna63c/certificate/temporal-schedule-decision/UNCOMMITTED_ARTIFACT_INVENTORY.json`
8. `workflow/handoffs/luna63c-artifact-reconciliation-correction-20261010.md`

The corrected publication manifest records raw SHA-256, Git blob, class,
source revision, reason, validation, and certification limitations for
eligible artifacts. Its self-hash is intentionally omitted; the reviewer
receives that raw hash separately. No Category C, D, E, or F source artifact
is added or replaced by this allowlist.

## Static review of all 12 untracked Python files

Static review only; no Python script, test, generator, checker, or scientific
calculation was executed. The files total 2,350 source lines. All are
standalone historical Lane E/T/W certificate tools under untracked lane
directories. None is a production neuron, integrated runtime, training path,
or fixture runner. This does not establish their scientific correctness.

| File | Role, inputs and outputs | Paths, variability and writes | Numerical/test scope and disposition |
|---|---|---|---|
| `lane-e/reference.py` | MPFR/GMP C-API interval, exact-time and binary64-ceiling primitives; consumes a caller-supplied DLL directory; returns interval/time structures and engine identity. | Derives its directory from `__file__`; no commit pin. Native library and ABI identity govern repeatability; mutable global engine/precision. No file writes observed; loads DLLs and allocates native state. | Performs directed numerical arithmetic; `test_certificate.py` has 12 methods including ABI/arithmetic probes. Archive only; any later use requires independent ABI/provenance review. |
| `lane-e/certify.py` | Builds the local 372-row E checkpoint table from historical v2 witnesses and local W/T JSON; writes `checkpoints.json` or the CLI-selected output. | Pins baseline `87179ba...`, sibling `.engine` directory, and local output/input paths; optional path overrides. Fixed diagnostic literals; native engine and discovered inputs affect output. | MPFR 256/512 arithmetic, conditional 1024 escalation, roots and conversions. Covered by the local E test file, but historical claims were not rerun. Archive; any execution requires authorization. |
| `lane-e/check.py` | Verifies local hashes, source identities, and DLL identities; default prints status. | Pins `87179ba...`, sibling `.engine`, and owned-file list. `--freeze` rewrites `manifest.json`; default is read-only. | Hash/metadata checks only. E test file covers LF/CRLF identity; a consumed contract identity differs from current checkout, so historical integrity PASS is not transferable. Archive as old integrity tooling. |
| `lane-e/test_certificate.py` | Twelve local ABI, arithmetic, boundary, accumulation, hash-normalization, and table-scope tests; inputs include local checkpoints/W data and native engine. | Uses sibling checkpoint and DLL paths; no random inputs or explicit file writes; imports mutate shared engine precision/state. | Executes MPFR/GMP calculations. Covers only the local older E schema, not published 1,905-row E. Archive; do not run without a separate authorization. |
| `lane-t/convert.py` | Exact-rational/binary64 ceiling and event-time mapping helpers; CLI delegates to `generate.py`. | Fixed clock limit and local generator paths; no commit pin. Helper calls are read-only; CLI delegation can write schedule outputs. Decimal precision is explicitly set. | Exact encoding/rational arithmetic, not a trajectory solver. `test_conversion.py` has 12 methods including comparison against bit search. Archive as unapproved helper. |
| `lane-t/generate.py` | Assembles a restricted 12-row A4 schedule and optional 16 W conversion rows from correction-v2 and local W JSON. | Pins `87179ba...`, fixed input paths/holds; presence of W inputs changes optional outputs. Default CLI rewrites schedule files; `--check` is non-writing. | Exact rational mapping/ceiling arithmetic; no roots solved. Covered by local T test methods, which expect the restricted schema, not the published 191-row ledger. Archive; future execution separately authorized. |
| `lane-t/check.py` | Independent exact bit-search checker for local restricted schedules and W conversions. | Pins baseline and repository-relative inputs; refuses optimized Python. No explicit writes; reads JSON and uses in-memory structures. | Exact rational/encoding/domain/strict-future checks. Covered by local `test_conversion.py`, not complete published T. Archive. |
| `lane-t/integrity.py` | Builds/verifies local artifact and source hashes. | Pins baseline/source files; discovers local files and optional W/handoff inputs. `--write` replaces `manifest.json`; default verifies. | Hashing only. No direct import by the local conversion test file; historic integrity claims were not rerun. Archive as local-only tooling. |
| `lane-t/test_conversion.py` | Twelve conversion, sub-ULP, coalescence, generation, and tamper tests against local schema. | Reads local schedule; uses seeded `random.Random(6303)`; W-mapping test skips if its inputs are absent. No explicit artifact writes; generation is in-memory in the cited tests. | Exact rational/encoding arithmetic. Tests 12-row output, not complete 191-ID T. Archive; future corrective tests require authorized input/schema reconciliation. |
| `lane-w/oracle.py` | Standalone selected mathematical-witness calculator/exporter; reads fixed equations and local `.engine`; emits stdout results. | Pins `87179ba...`, `.engine`, 256/512 precision and fixed proposal literals; mutable global precision; native engine/environment dependence. No explicit file writes. | Directed MPFR interval/transcendental operations and root isolation; computes 82 selected quantities. `test_w.py` exercises this local package. Archive; not published 100-row W evidence. |
| `lane-w/check_w.py` | Local source/manifest identity and boundary checker; optional fresh oracle evaluation. | Uses local manifest paths and pinned source refs; read-only Git calls. Default can invoke numerical recalculation; even integrity-only includes rational boundary checks. No explicit writes. | Hash checks plus interval arithmetic depending on mode. Covered by `test_w.py`; archive, and any fresh evaluation requires authorization. |
| `lane-w/test_w.py` | Twelve local interval, root, boundary, optimized-Python, and integrity tests. | Reads local witnesses; no randomness; alters oracle precision and temporarily monkey-patches methods; launches a child Python process. No explicit artifact writes; imports may create bytecode caches. | Runs MPFR work for local 82-witness package; not current 100-row published W. Archive; future tests require separate authorization. |

The three local test modules each contain 12 test methods. No test outcome is
claimed from this review. W/T/E local manifests' declared artifact hashes
were checked without running their generators; the E DLL byte hashes match
its local declarations. The lane artifacts remain provenance-uncertain
because local self-consistency is not published-source identity.

## Validation and remaining gate

**Performed:** baseline/branch and exact source references verified; E's
1,905-row matrix parsed for applicability/status totals; all source artifact
raw hashes, sizes, states, and text line counts inventoried; local W/T/E
manifest hashes checked; three W provenance comparisons made; malformed T
identifier shown not to resolve and correct T commit resolved; 12 Python
files statically inspected; exact eight-path changed allowlist established.

**Not performed:** no scientific lane tests or generators, numerical
calculations, fixture execution, E re-audit, T correction, N5, N6, Stage B,
or LTRD. The preserved local lane packages are not certified and are not
published. The next assignment is independent Luna-0 review of this exact
allowlisted diff; only a PASS permits this bounded governance publication.
