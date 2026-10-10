# Luna-63C Stage-A — Lane E N4 audit, 2026-10-10

**Disposition: E BLOCKED — N4-B FROZEN INVENTORY INCOMPLETE.** The independent
N4-A checks pass for every applicable published W checkpoint. N4-B remains
blocked because the pinned T publication has 182 unresolved scheduled-event
identities. E does not replace their missing times or ordinals.

## Scope and immutable inputs

- Branch/worktree: `experiment/luna63c-stage-a-E`,
  `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna63c-E`, created from the
  published T commit `0a8c34b7e6febf681917d915082a8559eea998f7`.
- Source branch HEAD pin: `19caa49d7620062c06ad74d19528e47725f86b37`.
- Fixture publication: `583148e2812b93d519a3dc2821944d08446497b7`.
- W COMPLETE publication: `17907c67d52cc338249b66f28c3179cd97572c6e`;
  W matrix SHA-256
  `0B5AB09AE5E4A29AD951B00563C64F5D445D0665B332154C9D40F93335F90D9F`.
- T publication: `0a8c34b7e6febf681917d915082a8559eea998f7`; the committed
  manifest and handoff both report **T BLOCKED — N3 NOT CLOSED**, 9/191
  certified and 182/191 blocked, including all 119 C7 event identities
  (9 certified, 110 blocked).
- Frozen inputs: `fixtures.json` SHA-256
  `AF81F3390274B2D565F90CBF12C116C78F45C5DF65D6C28BA88194E9DF2F70FB`,
  blob `8c4f9d20dda217d71ef1bcbb4fdefd0e3507ed92`; `FIXTURE_FREEZE.md`
  SHA-256 `B3BB25D65A8344363DF17F2A6FF3085034FDC431605B6FBA729499D512BE667F`,
  blob `fc3d883e72ec3062e07cc453927ee76cba4aa561`.
- N4 schema commit `9cc92adb56e388d8675d538410b319fd8d8841a5`;
  arithmetic governance `87179ba2f5da13da7bc70727e72c000de924ed80`;
  reviewed design `3e7d31b9a527e908b21abee3766906084e7cd082`.
- Artifact-pinned line-ending materialization was checked against Git blobs;
  checkout bytes were not substituted for the frozen object identities.

No parent untracked historical E artifact or W/T helper calculation was used as
an arithmetic authority. The published W/T JSON is read-only input. The
read-only native dependency materialization is the existing
`C:\Users\Patrick\Documents\ActiveCode\TPCN\experiments\luna63c\certificate\lane-w\.engine`;
it was neither copied nor modified by E.

## Independently reproduced N4-A evidence

The standalone E auditor imports the already-available gmpy2 binding and
recomputes the frozen analytic quantities with its own directed-MPFR interval
operations. The actual environment was CPython 3.11.4, gmpy2 2.3.2, MPFR
4.2.2, GMP 6.3.0, Windows AMD64. Loaded extension SHA-256:
`632D398D77023696549483852FB947B2627E6F7B88C4A42815A1A4977BEF30B5`;
the MPFR/GMP DLL identities and hashes are recorded in `lane-e/manifest.json`
and matched against the published W environment record. MPFR RNDD/RNDU
constants were read from the binding; host `libm` was not used for scientific
transcendentals.

- All 90 serialized rational interval pairs in W were rechecked against
  independently recomputed outward MPFR enclosures. The 36 corresponding
  non-root-endpoint quantities at 256/512 bits overlap. Root endpoint
  surfaces are checked separately at each precision because the bisection
  endpoint itself changes with refinement.
- Both independent root paths (C4 and C6), upward and re-arm roots, were
  checked: strict endpoint signs, proper monotone bracket, nested refinement,
  exact interval width after 64 bisections at each precision, and no more than
  128 bisections per root. Every root's 256/512 classification agrees.
- Directed enclosures were recomputed for `pi`, `sqrt(2)`, `g`, `q`, `theta`,
  A=1/A=4 quiet times, the upper-q-neighbor quiet time, lifetime, and all
  frozen flow/root/quiet-state coordinates. Exact symbolic checks cover the
  neutral fixed point, stable-focus eigenvalues, invariant disk, HOLD, C2
  tangency/no upward crossing, A4 rising/re-arm roots, quiet/terminal timing,
  and C5 exact HOLD offsets.
- The strict A=1 ideal comparison margin `exp(-2) < theta/4` was independently
  enclosed at 256 and 512 bits. This certifies only the frozen ideal-model
  margin and strict L2 rule; **no absent Stage-B candidate was evaluated**.
- The 100 distinct W checkpoints, all proof references, and all 15
  observation-only identities map to frozen inventory. The observation rows
  remain non-events. No 1024-bit escalation was needed.

## N4 coverage matrix

`experiments/luna63c/certificate/lane-e/coverage_matrix.json` contains 1,905
per-row obligation records, including every W checkpoint, each of the 15
observation-only checkpoints, every one of the 191 T event identities, and
every applicable N4-A/N4-B obligation. The machine-readable records preserve
each T blocked event's exact reason codes, rather than extrapolating from
representative cases.

| Obligation | Applicable rows | PASS | BLOCKED | N/A |
|---|---:|---:|---:|---:|
| N4-A1 | 100 | 100 | 0 | 0 |
| N4-A2 | 100 | 100 | 0 | 0 |
| N4-A3 | 59 | 59 | 0 | 0 |
| N4-A4 | 59 | 59 | 0 | 0 |
| N4-A5 | 86 | 86 | 0 | 0 |
| N4-A6 | 49 | 49 | 0 | 0 |
| N4-A7 | 115 | 115 | 0 | 0 |
| N4-B1 | 191 | 9 | 182 | 0 |
| N4-B2 | 191 | 9 | 182 | 0 |
| N4-B3 | 46 | 1 | 45 | 145 |
| N4-B4 | 191 | 9 | 182 | 0 |
| N4-B5 | 191 | 9 | 182 | 0 |
| N4-B6 | 182 | 9 | 173 | 9 |
| N4-B7 | 191 | 9 | 182 | 0 |

The nine converted T identities are the near-clock limit case (last accepted
origin, expiry-record creation, and successor origin) and the positive
sub-ULP case (STORE, expiry-record creation, same-time RECALL, quiet-record
creation, quiet event, and expiry invalidation).

For those rows E independently used exact `Fraction` comparisons and an IEEE
binary64-bit-order search for least ceilings, not the T conversion helper and
not a `nextafter` fallback. The lifetime endpoints map to the inclusive
`2^20` clock at the last-in-domain STORE origin; the successor origin's
expiry lower bound exceeds the domain. The positive quiet delay is strictly
positive and below the origin ULP, both endpoints map to the successor, and
the exact predecessor is the cause timestamp. The quiet and expiry tie-group
ordinals, causal identities, and 0/1/2-TU HOLD active-time convention are
recorded and checked. Exact dyadic timestamp units and the positive
`2^-33 TU = 2^1041` sub-ULP schedule delta were reconstructed with GMP
integers.

The other 182 IDs stay blocked. Their manifest reason counts are:

| Exact T blocker code | Rows carrying the code |
|---|---:|
| `ABSOLUTE_ORIGIN_t_store_UNFROZEN` | 85 |
| `COALESCENCE_WITNESS_t_store_AND_t_late_NOT_FROZEN` | 6 |
| `EXPIRY_COALESCENCE_PACKET_CHOICE_DEPENDS_ON_UNFROZEN_t_store` | 10 |
| `EXTERNAL_INPUT_TIME_UNSPECIFIED` | 80 |
| `INVALID_TIMESTAMP_ENVELOPE_NOT_FROZEN` | 12 |
| `NO_TIMESTAMP_BY_RULE_PRECEDENCE_DEPENDS_ON_BLOCKED_INSTANCE_SCHEDULE` | 2 |
| `PRECEDING_STORE_TIME_t_store_UNSPECIFIED` | 12 |
| `RELEASE_ORIGIN_NOT_FROZEN_NUMERICALLY` | 3 |
| `RESET_TIME_ONLY_CONSTRAINED_TO_AN_OPEN_INTERVAL` | 1 |
| `s_pause_AND_RESUME_TIME_ONLY_CONSTRAINED_TO_INTERVALS` | 3 |

Counts are reason occurrences; a row may carry multiple reasons. The matrix
lists every blocked `event_id`, every applicable blocked obligation, and its
exact source reason. E does not pick input times or ordinals, close T/N3,
claim global N4/N3 closure, or convert convention demonstrations into
coverage.

## Historical labels, tests, and strict stop

The pinned repository records that no authoritative E1–E14 definitions were
found; those labels were not reconstructed or guessed. Instead, the matrix
maps the actual numbered Stage-A certificate clauses 1–12 in
`.github/agents/luna-63c-mechanism.agent.md` to their corresponding real
N4-A1…A7/N4-B1…B7 requirements.

Validation:

- `python experiments\luna63c\certificate\lane-e\test_audit.py` — 5 tests
  passed.
- `python experiments\luna63c\certificate\lane-e\audit.py --write` — matrix
  and manifest generated deterministically.
- `python experiments\luna63c\certificate\lane-e\audit.py` — deterministic
  reserialization/check passed (W 100, T 191, matrix 1,905, T blocked 182).
- `git -c core.whitespace=cr-at-eol diff --check` — run before publication.
- No dependencies installed; no architecture/ACP/A01–A15/field/fixture/cap
  changes.

No Lane S/N5, Stage B, runtime/candidate implementation, or C0–C7 scientific
mechanism execution ran. E stops here because T is incomplete.

## E artifact hashes

| File | SHA-256 |
|---|---|
| `experiments/luna63c/certificate/lane-e/audit.py` | `5D710BF45C625BCACA974F374AD1C676396C4159477DFBC82CCDC8C47F3BFA7C` |
| `experiments/luna63c/certificate/lane-e/test_audit.py` | `AF58AF122CC9087E2A608D689261E98FAF34B8A94815E4579579772CF09E76B5` |
| `experiments/luna63c/certificate/lane-e/coverage_matrix.json` | `D1A7CE384D10B42EDA08DE82E29D3E0257A8EB752CF8C4B7E164B6037F0BB436` |
| `experiments/luna63c/certificate/lane-e/manifest.json` | `4EFBEAC456EA5FA8EE1FD88C7A9B7AE2284AAC3BFC8B574990DC7BBA79F2244B` |
