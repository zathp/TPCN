# Luna-65 Phase 2A S1-A Synthetic Ledger-Sizing Implementation Authorization Review

Gate: `L65-PHASE2A-S1A-IMPLEMENTATION-AUTHORIZATION-REVIEW`
Author: Luna-0. Status: PROPOSAL FOR OWNER DECISION. Nothing in this document is owner-accepted.

This document prepares an owner-authorization request only. It does not authorize writing the sizing script, running any check on it, executing it, implementing or qualifying the supervisor, running fixtures, or any benchmark.

## 1. Verified provenance (read-only)

| Item | Identity |
| --- | --- |
| Branch / HEAD / origin | `governance/luna64-r4.3-freeze-20261010` / `fe7398d1b88741afc83a15733205fedb24588a26` (equal) |
| Preimplementation package | `workflow/docs/luna/LUNA_65_PHASE2A_R7_PREIMPLEMENTATION_READINESS.md`, blob `c4d93f77cecc1a388fa44fe234295aba01018d6d`, CRLF-worktree SHA-256 `D3F28DEEC73A53EFD4A470F7D90BC670E5A6F32593258B16F74F493683DE363C` |
| R7 profile contract (frozen) | `workflow/docs/luna/LUNA_65_PHASE2A_R7_OWNER_DECISIONS_AND_PROFILES.md`, blob `0759087811610f40c73de91d8662c28d8ebce54d`, contract SHA-256 `9CA2E34DCC1F35BA72156B86C889365C2EB6873979E7863248594AF214169B73` |
| Capacity contract (schema authority) | `workflow/docs/luna/LUNA_65_PHASE2_CAPACITY.md`, blob `4073b4035b4629e306822ce4d8b2a307aa6c233f`, CRLF-worktree SHA-256 `234043BC7963AE603C1AC0E419691DE60D14760405614E6C1057BAA8F0D971DE` |
| Workflow | `workflow/docs/luna/LUNA_WORKFLOW.md`, blob `e1cc3769e06c30c7450f4c769138d64d35388de9` |
| Supervisor scaffold | `scripts/luna65_phase2a_supervisor.py`, untracked, unchanged, SHA-256 `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` |
| `scripts/luna65_phase2a_ledger_sizing.py` | ABSENT |
| `tests/test_luna65_capacity_direct.py` | ABSENT (no hash is fabricated) |

Worktree contains only the untracked scaffold. Historical records are untouched. Hash forms: the repository applies `text=auto`; review hashes above are CRLF-worktree hashes, blobs are LF. Authorizations bind to the Git blob ID plus the LF-normalized SHA-256.

The preimplementation package (D3F28DEE) passed all four independent lanes, but its Decision A (`FITS_WORST`) is a request for an owner amendment and is NOT accepted.

## 2. S1 result-gate reconciliation

### 2.1 Published gate and its inconsistency

R7 contract section 9 (`L65-PHASE2A-LEDGER-SIZING-S1`) requires exactly 8,196 records (four counters x 2,049 probes), two profiles (nominal and width-bound), an in-process double-generation determinism check, and classifications `FITS_WORST_AND_NOMINAL`, `FITS_NOMINAL_ONLY`, `EXCEEDS_BOTH`, `GENERATOR_FAILURE`. Two profiles, or any double generation, produce at least 16,392 records, which contradicts the 8,196 ceiling. The published text is internally inconsistent as written; it cannot be executed literally.

### 2.2 Can one deterministic profile establish both nominal and worst-case fit within 8,196 records?

No. Nominal and worst-case are different quantities computed from different record contents. One 8,196-record generation yields exactly one constructed sample. Establishing both requires a second generation (>= 16,392 records), which exceeds the ceiling. A single profile cannot be relabelled as both.

### 2.3 Four quantities that must stay distinct

1. **Analytical maximum size**: arithmetic from schema field widths (uncompressed JSONL length bound). Compression is not guaranteed to shrink data; a gzip stored-block fallback is bounded only by uncompressed length plus per-block and header/trailer overhead. At the uncompressed scale of this ledger that bound is expected to exceed the 786,432-byte ledger allocation. No compression guarantee is claimed.
2. **Constructed worst-case sample**: the width-bound profile (maximal-width, high-entropy field values). Compressed size is not monotone in width, so it is a stress sample, not a proven upper bound.
3. **Nominal expected size**: would need oracle-valued records (requires `math.exp`, outside the import allowlist) and its own 8,196-record run. Not produced under the recommended option.
4. **Actually observed compressed size**: the single measurement S1-B would record. It is an observation about one constructed sample only.

The real Phase 2A writer retains runtime reserve-before-write accounting against the 1,048,576-byte hard cap, so the cap is protected at runtime irrespective of sizing. Sizing is a feasibility and parameter signal and not proof for real runs.

### 2.4 Owner decision D-S1-1 (not accepted; owner must choose)

- **Option 1 (recommended)**: Amend the S1 gate to one width-bound profile generated once (<= 8,196 records), no double-generation, no nominal profile. Classifications `FITS_WORST` (observed compressed bytes within the ledger allocation minus finalization margin), `EXCEEDS_WORST`, `GENERATOR_FAILURE`. Determinism is addressed by closed-form construction and a manifest hash, verified by independent re-derivation of the manifest during review rather than by in-run regeneration. No nominal result is claimed; the result states only the observed fit of the constructed sample.
- **Option 2**: Authorize a separate nominal run (with a separately reviewed `exp` import decision) or raise the sizing record ceiling to cover two profiles.
- **Option 3**: Retain the published gate and raise the ceiling explicitly (e.g. to a stated number >= 32,784 records) with revised CPU/wall/output ceilings.

Until the owner chooses, S1-A authorization is conditioned on D-S1-1; with no choice, implementation remains blocked.

## 3. S1-A frozen scope (conditional on D-S1-1 Option 1)

Single-file allowlist: `scripts/luna65_phase2a_ledger_sizing.py` (currently absent; to be created only after owner authorization). No other file may be created, modified, staged or deleted by S1-A. The scaffold, tests, `src`, contracts, and workflow are out of the allowlist.

### 3.1 Implementation obligations

- O1 Deterministic closed-form construction; a fixed integer arithmetic recurrence (e.g. an LCG with constants stated in source) supplies high-entropy digits. No randomness module, clock-derived values, environment values, or hash-seed dependence.
- O2 Schema fidelity: every row carries exactly the fields and value rules of the Phase 2A JSONL schema table (except only the checkpoint `x`/timestamp sizing-only exception, if and only if the owner selects D-S1-2 Option 1; see O6) in `LUNA_65_PHASE2_CAPACITY.md` (blob `4073b403...`): `schema_version` `luna65-phase2a-probe-v1`; `fixture_version` `l65-phase2a-v1`; `counter_under_test` in {input, episode, lineage, output_event}; `probe_index` 1..2049; `initial_state_id` `l65-phase2a-<counter>-fresh-zero-v1`; `neuron_id` `l65-capacity-node`; `counter_snapshot_before/after` with lexically ordered keys episode, input, lineage, output_event; `target_counter_delta` 1 for allocation and 0 for rejection; `coupled_counter_deltas` including zeros; `preparation_counter_deltas` output_event only; `exception` null or `{type, message}` with the published type and per-counter message; `expected_outcome` `allocated` for 1..2048 and `capacity_rejected` for 2049; `observed_outcome`, `completion_status`, `state_checkpoint`, `post_rearm_checkpoint`. The implementer and reviewers must compare the source field-by-field against the published text; this summary is not the authority.
- O3 `allocated_identity`: input and output_event use the published emitted/provenance ID strings (input `l65-capacity-node:input:<ordinal>` ordinal 0..2047; output `l65-capacity-node:excursion:<ordinal 1..2048>`); episode and lineage use the integer newly allocated counter value; null on the rejection probe. Admission event IDs follow the published `l65-phase2a-episode-<ordinal:04d>` and `l65-phase2a-lineage-<ordinal:04d>` patterns.
- O4 Identity boundaries: probes 1..2048 allocate and probe 2049 is a capacity rejection for every counter; counter snapshots are synthetic integers emitted by construction, never read from live E2 counters.
- O5 Total records <= 8,196, exactly four counters x 2,049, in order input, episode, lineage, output_event; generated once.
- O6 Serialization: `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=True, allow_nan=False)` plus exactly one LF per record; lossless. Values constrained by the published schema (probe_index, counter snapshots, target/coupled/preparation deltas including required zeros, expected/observed outcomes, fixed strings) retain their exact required values and are never inflated. Checkpoint `x` and timestamp values are a recognized conflict between two published texts: R7 section 9 requires the width-bound profile to use a maximum-length finite binary64 `repr` for every `x`/timestamp, while the capacity contract scenarios prescribe exact values (e.g. `1.0`, `4.0`, `0.0`, and the output recurrence). This is owner decision D-S1-2 (not accepted): **Option 1 (recommended)**: the width-bound sizing records are synthetic sizing samples, not fixture evidence; checkpoint `x`/timestamp values are replaced by deterministic maximum-length finite binary64 literals per R7 section 9 (conservative stress), all other constrained fields stay exact, and the manifest states that checkpoint numerics are substituted. Option 1 is an explicit, bounded sizing-only exception to O2 and to the capacity-contract scenario checkpoint-value rules; it applies to checkpoint `x`/timestamp numerics only and to no other field. **Option 2**: checkpoint `x`/timestamps keep the exact published scenario values for all four counters and all 8,196 records (no placeholder and no exclusion of any output row); output-scenario recurrence values must be either (a) fixed precomputed binary64 literals independently verified against the published recurrence before implementation, or (b) computed via a separately owner-authorized `math.exp` import amendment to the import allowlist. No numeric width stress is claimed under Option 2. Without a D-S1-2 choice, O6 numerics are unresolved and implementation stays blocked. Identity strings and ordinals (O3) always retain their exact published values under both options; no identity-string width stress is applied (this narrows R7 section 9's "identity strings at maximum length", and is disclosed here as a recommended owner-visible deviation under D-S1-2). Under Option 1 the manifest discloses that only checkpoint `x`/timestamp numerics are substituted. JSON `null` appears only as published: on a successful allocation probe `exception` is null and `allocated_identity` is non-null; on the rejection probe `allocated_identity` is null and `exception` is the published object; checkpoint nulls only where published. Implementers compare field-by-field against the published schema. No NaN or infinity.
- O7 Compression: gzip level 9, `mtime=0`, no filename, via a byte-counting sink; standard-library gzip/zlib version recorded in the manifest. The `.gz` file is written only if it fits the allocation.
- O8 Output accounting: uncompressed bytes, record count per counter, compressed bytes, finalization margin (deflate end block plus 8-byte trailer), allocation 786,432, and aggregate retained-artifact bytes (`sizing.json`, `sha256.json`, optional `.gz`) <= 1,048,576, all reported.
- O9 Manifest: generator identity (script path, schema/fixture versions, profile name, LCG constants), Python version, zlib version, SHA-256 of the JSONL stream, record counts, byte counts, classification, no host paths beyond the declared output directory.
- O10 Classifications `FITS_WORST`, `EXCEEDS_WORST`, `GENERATOR_FAILURE`; any exception, count mismatch, or output-budget breach is `GENERATOR_FAILURE`.
- O11 Import allowlist: `json`, `gzip`, `zlib`, `hashlib`, `sys`, `os` (path joining only), `time` (monotonic guard only), `io`, `pathlib`. No `math`, `ctypes`, TPCN import, `neuron_to_ir2_e2`, neuron/E2 counters, subprocess, network, environment reads, or Spiral data.
- O12 Scientific isolation: no Spiral data, training, scoring, or network fixture; no use of results to claim task efficacy.
- O13 Writing the file must not execute it; S1-A must not generate or execute the full ledger.

### 3.2 Permitted nonexecuting static checks (only if a later owner authorization permits them; none performed under this dispatch)

1. Source inspection against the published schema, field by field.
2. SHA-256 and Git blob computation of the file.
3. Whitespace and line-ending validation (no trailing whitespace, consistent CRLF/LF per repository policy).
4. AST-based import-allowlist inspection and forbidden-API absence inspection (parsing only, no execution of the module).
5. Python compilation (`py_compile`-style) only if the owner expressly permits; it does not execute module code, but must write no bytecode into the repository (`-B` and temporary output, or an in-memory `compile()`).
6. Verification that `git status` shows only the one allowlisted file as new.

Explicitly not permitted: importing or running the script, running pytest, generating any record, writing evidence, or measuring size.

## 4. S1-B boundary (separate authorization; not authorized)

S1-A implements and statically reviews the generator. S1-B would be a separately authorized single attended synthetic execution:

- One invocation, zero retries, <= 8,196 synthetic records total.
- 30 CPU seconds, 30 seconds workload wall time, 45 seconds outer attended supervision, 1 MiB retained output.
- Memory is unmeasured; 128 MiB is a design target only.
- These limits are not qualified enforcement. The qualified supervisor does not exist; the outer wrapper is an attended best-effort stop. Residual risks: no memory or CPU enforcement, no process control, no token/integrity restriction, no breakaway guarantee.
- Command proposal (not authorized): `.\.venv\Scripts\python.exe -B scripts\luna65_phase2a_ledger_sizing.py --output-dir "$env:LOCALAPPDATA\TPCN\evidence\luna65\phase2a-sizing\<run-id>"` with `PYTHONHASHSEED=0`.
- S1-B prerequisites: owner decision D-S1-1; accepted S1-A with a fixed file SHA-256/blob; owner acceptance of the unsupervised execution boundary (D-R7P-1); independent read-only evidence verifier other than the executor; a pre-created empty destination; no access to live E2 counters.

## 5. Exact owner authorization text (proposed; effective only if the owner adopts it)

"I choose D-S1-1 Option 1 and D-S1-2 Option [1 or 2 — owner to state]. I authorize Luna to create exactly one file, `scripts/luna65_phase2a_ledger_sizing.py`, at base commit `fe7398d1b88741afc83a15733205fedb24588a26`, implementing obligations O1-O13 of the S1-A authorization review package (blob and SHA-256 recorded at its publication), and to perform only the nonexecuting static checks listed in section 3.2 items 1-4 and 6 [and 5 if I so state]. This does not authorize executing, importing, or running the script, generating any ledger, S1-B, supervisor implementation or qualification, capacity fixtures, Spiral benchmarks, or any change to any other file."

## 6. Authorization state

- Supervisor implementation: NOT AUTHORIZED.
- S1-A generator writing: NOT AUTHORIZED (request prepared only).
- S1-B / synthetic sizing execution: NOT AUTHORIZED.
- Supervisor qualification: NOT AUTHORIZED.
- Phase 2A/2B fixtures: NOT AUTHORIZED.
- Full Spiral benchmark: BLOCKED.
- Luna-64 corrective execution: BLOCKED.
- Luna-63C: FROZEN.
