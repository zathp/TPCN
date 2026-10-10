# Luna-63C Stage-A Lane W — mathematical witnesses / N1

**Disposition: LANE W COMPLETE.** This result covers only the W mathematical
witnesses assigned for the frozen C0–C7 inventory. The remaining T/E event
conversion and ordinal work is separately marked **BLOCKED / NOT RUN**. This
is not a complete Stage-A certificate, N1/N3/N4 closure, Lane-S/N5 result,
Stage-B authorization, or scientific experiment.

## Isolation, baseline, and immutable authorities

| Item | Identity |
|---|---|
| Worktree | `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna63c-W` |
| Branch | `experiment/luna63c-stage-a-W` |
| Starting HEAD and fetched source branch | `19caa49d7620062c06ad74d19528e47725f86b37` |
| Source branch | `experiment/luna63c-stage-a-certificate` |
| Fixture publication ancestor | `583148e2812b93d519a3dc2821944d08446497b7` |
| N4 requirements revision | `9cc92adb56e388d8675d538410b319fd8d8841a5` |
| Arithmetic governance revision | `87179ba2f5da13da7bc70727e72c000de924ed80` |
| Reviewed design revision | `3e7d31b9a527e908b21abee3766906084e7cd082` |

Only `experiments/luna63c/certificate/lane-w/**` and this handoff are owned
by this lane. No prior untracked lane artifact was copied, edited, promoted,
or used as certificate authority. The earlier read-only `lane-w/.engine`
directory in the parent worktree was used solely as a dependency source:
it was neither modified nor copied. No parent-worktree files were changed.

### Fixture source integrity

The immutable publication commit and the current HEAD path blobs were checked
against both Git object IDs and SHA-256 over the canonical committed blob
bytes:

| Source | Git blob | Canonical raw SHA-256 |
|---|---|---|
| `experiments/luna63c/fixture-freeze/fixtures.json` | `8c4f9d20dda217d71ef1bcbb4fdefd0e3507ed92` | `AF81F3390274B2D565F90CBF12C116C78F45C5DF65D6C28BA88194E9DF2F70FB` |
| `experiments/luna63c/fixture-freeze/FIXTURE_FREEZE.md` | `fc3d883e72ec3062e07cc453927ee76cba4aa561` | `B3BB25D65A8344363DF17F2A6FF3085034FDC431605B6FBA729499D512BE667F` |

The worktree has `core.autocrlf=true`. Consequently the JSON checkout's raw
CRLF-materialized SHA-256 is
`9148A66EA75B21A21701CA2D4CCDA4B21C01C0EA5CF08160E71B28327340069D`;
normalizing its CRLF pairs to the canonical LF blob reproduces the pinned
`AF81...70FB` hash. The Markdown checkout raw hash equals its canonical
`B3BB...667F` hash. The checker verifies both canonical blob hashes, pinned
blob identities, publication ancestry, and checkout materialization before
building the matrix and manifest.

A lane-local `.gitattributes` pins the Python and JSON artifacts to LF in
Git checkouts. This keeps the generator's byte-exact deterministic
serialization and source-program hash check reproducible when
`core.autocrlf=true`; it does not change the immutable fixture sources.

## Governed arithmetic environment

The calculation ran under CPython 3.11.4, 64-bit Windows AMD64, MSVC 1934,
with the gmpy2 2.3.2 binding. The loaded native libraries reported **MPFR
4.2.2** and **GMP 6.3.0**, matching the governed versions. The manifest records
the actual extension/DLL paths and SHA-256 identities. gmpy2 invokes the
MPFR C API; all scientific transcendental results in this lane used MPFR
directed operations, not host `libm`.

Lower and upper interval endpoints use MPFR round-toward-negative-infinity
(RNDD / `gmpy2.RoundDown`) and round-toward-positive-infinity (RNDU /
`gmpy2.RoundUp`). Every stored endpoint is serialized as its exact rational
value. Every numerical assertion is checked at 256 and 512 bits; the
enclosures overlap and qualitative classifications agree. No 1024-bit
escalation was required. Each non-symbolic root used 64 bisections at each
precision, 128 total per root, within the cap. A directed-rounding `exp(1)`
and `pi` smoke test verified distinct lower/upper bounds.

The exact q-neighbor fixture magnitudes were independently resolved from
their frozen definitions (not used as event times):

| Definition | Exact binary64 hex | Bits |
|---|---|---|
| Greatest binary64 strictly below `q` | `0x1.4a226c87ef13fp-2` | `0x3fd4a226c87ef13f` |
| Least binary64 strictly above `q` | `0x1.4a226c87ef140p-2` | `0x3fd4a226c87ef140` |

The 256- and 512-bit q enclosures are strictly between these adjacent
dyadics. Exact binary64 input imports are used for the neighbor comparisons.

## Fixture-driven coverage reconciliation

`experiments/luna63c/certificate/lane-w/coverage_matrix.json` contains **100
W rows: 100 CERTIFIED, 0 BLOCKED**. The frozen-source plan reconciles as:

| Fixture | W rows | Source-derived coverage |
|---|---:|---|
| C0 | 1 | Published initial-state checkpoint |
| C1 | 2 | Both neutral RECALL state checkpoints |
| C2 | 22 | All seven magnitude cases with frozen polarities; all eight A=1 P/N checkpoints; strict ideal A=1 margin |
| C3 | 5 | Stored state, each HOLD duration 0/1/2, and expiry mathematical source |
| C4 | 8 | A=4 state, upward root/state, re-arm root/state, quiet state/root, expiry, terminal clear |
| C5 | 18 | Each H0/H1/H2 instance: HOLD, matched full-state flow, upward root, re-arm, quiet/terminal, expiry |
| C6 | 8 | Separate ungated oracle: initial state, independently solved upward/re-arm roots and states, quiet root/state, terminal |
| C7 | 36 | All 14 published subcases, including four individually expanded timestamp-invalid variants |
| **Total** | **100** | All planned W rows present; no fixture or checkpoint added |

The machine-readable plan records the per-case reconciliation and enforces
unique row keys. Every W row is `CERTIFIED` with its mathematical identity,
proof reference, and applicable N4-A mapping. Exact identities are labeled
`EXACT_SYMBOLIC`; numerical enclosures use `MPFR_OUTWARD_INTERVAL`.

### Key mathematical results

- **C2 A=1:** both polarities have complete two-coordinate independent oracle
  enclosures at exactly `s={0,1/2,1,2}` TU. At 0, 1/2, and 1 the ideal
  candidate has not yet reached quiet and is analytically the same flow. At
  2, quiet has already cleared the ideal model state; the unreset oracle
  norm/discrepancy is exactly `exp(-2)`. The strict mathematical margin
  `exp(-2) < theta/4` is proved from `pi < 22/7`,
  `e^(6/5) > 73/25`, `(73/25)^2 > 8`, and `2-pi/4 > 6/5`.
  `theta/4` remains only the owner-frozen later candidate acceptance ceiling.
  **No Stage-B candidate comparison was performed.**
- **C2 A=2:** for each polarity the first-lobe peak at `s=pi/4` is exactly
  `p*y=theta`, the derivative is exactly zero, and the second derivative is
  strictly negative. This is exact tangency, not a crossing; later positive
  lobes are smaller.
- **C3:** `R=0` gives exact identity flow and zero active-time advance; the
  full held state is `(4,0)` for all three frozen durations, with norm
  squared 16. No release schedule was added.
- **C4/C5:** MPFR brackets, strict endpoint signs, monotonicity, existence,
  uniqueness, root-state enclosures, and 256/512 consistency are recorded.
  The C4 upward root solves `4 exp(-s) sin(s)=theta`; the unique downward
  re-arm root solves `4 exp(-s) sin(s)=q`. The exact quiet root is
  `ln(4/q)`, with radius derivative `-r<0`; `T_life=3+ln(4/q)`. C5's
  HOLD values `{0,1,2}` add exact real-time offsets but no active time.
- **C6:** the ungated reference roots were recalculated in a separate scalar
  enclosure/bisection path with distinct starting brackets, without using a
  C4 root result as input. Its independently calculated brackets overlap
  the C4 brackets, and its quiet root and full root/quiet state enclosures
  are also recorded.
- **C7:** every frozen subcase points to its required mathematical source:
  A=4 upward/re-arm roots, pause-before-root constraints, exact HOLD state,
  `T_q`, `T_life`, the quiet-before-expiry relation under the frozen
  start-by-H condition, q-upper-neighbor positive quiet delay, and the
  explicit no-settlement/closed-ingress mathematical transitions. Distinct
  real/represented event-time relations are not claimed by W.

For all computed roots the matrix records defining functions, brackets,
endpoint sign enclosures, existence/uniqueness arguments, monotonicity,
iterations, exact bracket widths, and overlapping 256/512 results. The
absolute rational endpoints and state enclosures are in the JSON artifact,
not rounded decimal approximations.

## Explicitly blocked work reserved to T/E

The manifest records eight separate **BLOCKED** non-W reservations: C1–C7
time/ordinal materialization plus a C7 frozen-schedule coverage reservation.
No binary64 event input time, absolute root time, timestamp ceiling,
strict-future/ULP conclusion, expiry coalescence, event schedule, or final
ordinal was computed. C7 schedule feasibility conditions that depend on
those values remain unproved here. The mathematical source witnesses are
provided; T/E must independently materialize the event-time interface.

No Lane T, Lane E, Lane S/N5, Stage B, runtime implementation, candidate
evaluation, C0–C7 scientific fixture execution, architecture/ACP/A01–A15
change, field/fixture/cap change, or experiment was run.

## Artifacts and validation

Owned files:

- `experiments/luna63c/certificate/lane-w/certificate.py`
- `experiments/luna63c/certificate/lane-w/test_certificate.py`
- `experiments/luna63c/certificate/lane-w/coverage_matrix.json`
- `experiments/luna63c/certificate/lane-w/manifest.json`
- `experiments/luna63c/certificate/lane-w/.gitattributes`
- this handoff

Focused validation passed:

1. `python -m unittest -v test_certificate` — 7 tests passed, covering the
   100-row source reconciliation, both A=1 polarities/checkpoints, exact
   tangency, root sign/overlap and 128-bisection limits, T/E separation, and
   deterministic JSON/manifest hashes.
2. `python certificate.py --check` — deterministic full matrix regeneration,
   complete manifest re-creation, and hash verification passed.
3. `python certificate.py --write` — generated deterministic serialization;
   matrix SHA-256 is recorded in `manifest.json`.
4. Before publication, immutable fixture blob IDs/raw SHA-256 pins were
   rechecked and CRLF-aware `git -c core.whitespace=cr-at-eol diff --check`
   passed.

The manifest binds the matrix/program hashes, actual arithmetic environment,
fixture pins, and reconciled row counts. This handoff reports Lane-W only;
the full certificate remains incomplete until the separately authorized
T/E obligations and later gates are completed.
