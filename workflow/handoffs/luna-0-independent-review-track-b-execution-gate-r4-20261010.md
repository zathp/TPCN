# Independent review — Luna-64 Track B execution gate R4.3

**GATE:** `L64-TB-GATE-20261010-R4`  
**REVIEWED PROTOCOL:** `4.3.0-draft`  
**REVIEW VERDICT:** **BLOCKED — not ready for owner authorization**  
**REVIEWED MANIFEST SHA-256:** `6C665DCD843CA524F59967CB46F72692EF56EEA6A712699059737579EC9D04C4`  
**SOURCE BASELINE:** `73aaa50f97ceab322907875ae4dcf23e7541c3b5`  
**OWNER APPROVAL:** NOT PROVIDED  
**EXECUTION AUTHORIZATION:** NOT GRANTED

This review evaluated the exact uncommitted candidate package whose ten
manifest-listed hashes matched at review time. The package and governing
inputs were not committed or frozen; the manifest explicitly reports
`package_freeze: false`.

## Findings

1. **Immutable publication/freeze is absent — blocking.** The ten candidate
   files and manifest are untracked; the source inventory reports
   `immutable_freeze: false`. The inventory also omitted
   `.github/agents/luna-63c.agent.md` and
   `.github/agents/luna-63c-mechanism.agent.md`. The working-tree
   `LUNA_WORKFLOW.md` said the owner and Luna-0 had “published” the governance
   record, although the governance record and related changes were
   uncommitted.
2. **Pilot replay work and operation bounds are ambiguous — blocking.** The
   proposal says the feasibility pilot tests “replay”, while the protocol
   defines per-event counterfactual omission replay for attribution scores.
   The stated pilot episode/reception/operation arithmetic covered only the
   base workload and did not say whether omission replays were included.
3. **Reward-delay assignment and evaluation reward policy are unspecified —
   blocking.** The protocol lists six delays without mapping them to
   episode, seed, split, or arm. It does not state whether frozen evaluation
   episodes receive correctness rewards.

## Findings that passed

- Raw attribution-specificity arm scores are in `[0,1]`; computed signed
  paired effects are in `[-1,1]`. The classifier compares the N−U and N−R
  differences, and a valid negative comparison is **FAILURE**, not
  **INCONCLUSIVE**.
- Static review found the generator and paired-seed bootstrap encodings,
  estimands, Bonferroni family mapping, interval endpoints, decision
  precedence, and task balancing specified. Arms share physical task
  opportunities; the temporal-disruption arm changes decoder timing while
  retaining physical timing and eligibility ages. Labels and future inputs
  are excluded from decoder input; correctness reward is post-prediction.
- Base-workload arithmetic is internally consistent: 2,592 episodes,
  10,368 receptions, 8,640 decoder receptions, and 18,358,272 counted-op
  ceiling. These are ceilings, not measurements. Runtime, memory peak, and
  throughput remain unverified; the activity-cost proxy is not physical
  energy.
- No Luna-63C contamination or architecture promotion was found. The
  candidate stays within isolated software-experiment scope and is
  compatible with the Luna-64 contract and architecture clauses reviewed.

## Validation performed

- `node experiments/luna64/test-track-b-gate-r4.mjs`: PASS; reproduced three
  PCN transitions, two generator fixtures, two bootstrap fixtures, 19
  verdict fixtures, 15 validator-negative fixtures, and public-CLI
  valid/invalid cases.
- Node syntax checks for the candidate JavaScript files: PASS.
- Independently checked all ten package hashes and inventory-listed source
  hashes / Git identities: matched at review time.
- No pilot, benchmark, training, branch/worktree creation, or file edit was
  performed. These checks do not establish full 100,000-replicate execution,
  pilot feasibility, or efficacy.

## Follow-up review of candidate corrections

The independent follow-up review examined the corrected candidate manifest
with SHA-256
`FAA6A200A13A1A78AF06EE93619650D04B082A2CC906226291D40FED119F34C6`.
All ten listed package hashes matched at that review time. The reviewer
verified that the replay, doubled workload arithmetic, reward-delay policy,
EVAL reward policy, Luna-63C inventory entries, and working-tree wording
corrections described above were present and internally consistent. The
follow-up found no 63C contamination or architecture promotion.

The follow-up remains **BLOCKED solely on mutable/uncommitted provenance**:
the manifest still declared `package_freeze: false` and the inventory
declared `immutable_freeze: false`. That finding does not establish review
of later-modified candidate bytes; any further change requires a fresh
hash-verified review of the final candidate.

## Disposition and required next step

The latest candidate remains **BLOCKED pending final exact-byte review and an
immutable publication/freeze**. Owner approval was not provided, and
pilot/execution authorization was not granted.

The final candidate must be regenerated and independently reviewed by exact
manifest hash. Until an owner-approved publication/freeze is committed and
reverified, this package is not immutable or ready for owner authorization.

After the `983D41E329D07D4FAD882E50C674D644A9B14F751686AED276F0B7AF0DA1F11D`
follow-up review, the replay-digest description was normalized from prose to
explicit outer-record and event-record field orders. The current manifest
therefore differs from that reviewed hash and requires its own fresh
hash-verified review; this documentation records the prior review and is not
an input to the candidate manifest.

The final candidate review verified manifest SHA-256
`62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
All ten package hashes matched. The reviewer verified the structured replay
digest definition and validator equality check, generated-schema identity,
32-entry governing-input inventory including both Luna-63C contracts, and
the test run with 20 CLI-negative fixtures. No additional candidate issue
or semantic contradiction was found. The verdict remains **BLOCKED solely
by mutable/uncommitted provenance**: package and inventory still declared
their freeze flags false. No owner approval or execution authorization was
granted; no experiment or branch was created. This review is evidence of
the working-tree candidate only, not the later Git-backed post-publication
verification.

No implementation, experiment, execution worktree, production change,
Luna-63C modification, or architecture promotion is authorized by this
review.
