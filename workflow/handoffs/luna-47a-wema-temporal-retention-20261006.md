---
tpcn_handoff:
  agent: "Luna-47A execution worker; independent Luna-0 review pending"
  luna_identifier: "Luna-47A"
  descriptive_name: "WEMA / bounded event-time temporal retention"
  task_id: "luna-47a-wema-temporal-retention-20261006"
  component: "Isolated downstream-only continuous-time leaky impulse accumulator"
  status: "complete - PARTIALLY SUPPORTED; independent review pending"
  contract_version: "1.2"
  branch: "copilot/luna47a-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  production_evidence_baseline: "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
  protocol_implementation_revision: "add3d0ca87b13dd8998b2e99c784c16a0103c9d2"
  preoutcome_pin_correction_revision: "ec5231d7f6d66a709c160666f412dd525b4c9739"
  execution_revision: "ec5231d7f6d66a709c160666f412dd525b4c9739"
  result_revision: "Publication commit containing this handoff and artifacts; exact immutable commit reported after push"
  dependencies:
    - "Committed Luna-47A contract and published Luna-0 authorization"
    - "Reviewed Luna-46 corrected MIXED evidence and unchanged verifier"
    - "Reviewed Luna-44/45 raw captures/configurations and frozen fixture"
  owner: "Project owner"
  classification:
    - "experimental-model mechanism investigation"
    - "PARTIALLY SUPPORTED"
    - "not task efficacy, production integration or hardware evidence"
  hypothesis: "A fixed finite event-time retention rate makes some original retention-limited signed streams cross unchanged theta=1."
  counter_hypothesis: "Neither predeclared finite-rate variant crosses those streams; drive-limited negatives remain below threshold."
  interfaces_relied_on:
    - "Read-only reviewed Luna-46 integrity/reconciliation/recurrence functions"
    - "Exact baseline Git blobs, independent enqueue/reception captures and trajectory boundaries"
    - "No production runner, neuron, output or topology interface is invoked"
  label_information_boundary:
    - "Frozen zero reference; identity qualification; exact signed payloads"
    - "No labels, future points, fitting or offline statistics feed state"
  timing_assumptions:
    - "Exact frozen logical timestamps/queue ordering; analytical exponential relaxation"
    - "No global neural timestep; binary64 equation tolerance only, exact threshold and replay"
  reset_boundaries:
    - "State and clock zero per character; intervening zero-deposition updates retained"
  resource_bounds:
    - "320 primary and 320 historical streams; 4096 updates per stream; 100 MiB per source file"
    - "Signed state [-4,4]; time [0,1e12]; payload magnitude <=1e6"
    - "Exactly three components: baseline tau80, fixed tau800, fixed tau8000"
  authorized_scope:
    - "Bounded isolated retention comparison, exact retained replay and historical component diagnostics"
    - "Own experiments/luna47a, artifacts/luna47a, lane test and this handoff only"
  unauthorized_scope:
    - "No production/core/input-gain/threshold/weight/topology/routing/output/governance edits"
    - "No efficacy, parameter search, promotion, ACP, hardware claim, other-lane consumption or successor"
  controls:
    - "Code/protocol committed and pushed before outcome interpretation; pin correction separately committed before outcomes"
    - "Exact 33-file Git evidence integrity; 34 physical checkout files unchanged"
    - "All six prior phase digests; 1950 raw route pairs per phase; exact reconstructed Luna-46 sequences"
    - "Initial/replay variant equality and raw-evidence-backed saved bundle replay"
  measurements:
    - "235 primary receptions per phase; 108 reception-bearing, 212 no-reception streams"
    - "19/33 retention rescues at tau800; 31/33 at tau8000; union 31"
    - "75/75 drive-limited remain non-crossing in both variants; target clipping zero"
    - "Historical component crossing streams 108/166/167; clipping events 0/121/179"
    - "18 high-precision target checks; six 4096-event extreme-value stress cases"
  information_boundary_check:
    - "PASS: downstream-only, no computation feedback; no other lane consumed"
  hardware_mapping:
    - "NOT RUN; abstract scalar experiment, no hardware equivalence"
  architecture_invariants_touched:
    - "A01/A02 analytic event time; A08 finite bounds; A07 offline-only"
    - "A06 production prediction unchanged, not replaced/tested here; A15 no hardware claim"
    - "No contract amendment and no ACP"
  preserves:
    - "Luna-46 MIXED and exact category inventory"
    - "Luna-42 PASS WITH FOLLOW-UP"
    - "Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED"
    - "Luna-44 reviewed canonical fixture baseline"
    - "Luna-45 NOT SUPPORTED IN THIS SETUP"
    - "ACP-0007 unchanged/disabled; ACP-0008 opt-in, experimental, unpromoted"
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna47a/.gitignore"
    - "experiments/luna47a/__init__.py"
    - "experiments/luna47a/PROTOCOL.md"
    - "experiments/luna47a/run.py"
    - "tests/test_luna47a_retention.py"
    - "artifacts/luna47a/.gitattributes"
    - "artifacts/luna47a/inputs.json"
    - "artifacts/luna47a/results.json"
    - "artifacts/luna47a/manifest.json"
    - "artifacts/luna47a/execution.json"
    - "workflow/handoffs/luna-47a-wema-temporal-retention-20261006.md"
  tests_added:
    - "74 parametrized recurrence/event-time/threshold/sign/order/reset/bounds/replay/integrity checks"
  tests_passing:
    - "Final focused Luna-47A: 74 passed, no failures/skips"
    - "Authoritative Git 33-file verifier and physical immutability: PASS"
    - "Exact raw-evidence-backed bundle replay: PASS"
    - "Applicable regressions: 261 passed with 7 setup errors separately recorded"
    - "Unchanged Luna-46 regression: 166 passed with 1 physical-checkout failure separately recorded"
    - "py_compile and prepublication whitespace checks: PASS"
  tests_failed:
    - "Unchanged Luna-46 physical catalog integrity test: CRLF hash mismatch, before and after lane execution"
    - "Seven unchanged Luna-44 verification setup errors: pinned source materialization under core.autocrlf=true"
    - "First lane attempt exit 2 on misidentified physical-vs-Git Luna-46 pin, before outcomes; corrected without model/criteria change"
  tests_not_run:
    - "Full repository suite"
    - "Task efficacy/training, hardware, production integration, independent Luna-0 review"
  assumptions:
    - "Identity-qualified frozen stream is not verified clean signal/noise truth"
    - "No discharge/output in isolated component; target production baseline has neither discharge nor clipping"
    - "Historical replay is a component counterfactual, not full neuron behavior"
  unresolved:
    - "c01-009 and c02-025 remain below threshold at both fixed finite rates"
    - "Longer retention changes historical component crossings and increases cap occupancy"
    - "Windows physical integrity regression remains failed; exact Git evidence passes, no assertion relaxed"
    - "Cross-platform libm byte identity and concurrent filesystem-alias replacement are not guaranteed"
  recommended_next_agent:
    - "Independent Luna-0 review only; no successor or promotion authorized"
---

# Outcome and owned scope

**OBSERVED: PARTIALLY SUPPORTED**, under the protocol committed before
new accumulator outcomes. The unchanged threshold is exactly `abs(a)>=1`;
gain remains 1, cap remains 4, signed input/order/timestamps remain frozen.
The two fixed continuous-time rates are 0.00125 and 0.000125, contrasted
against the calibrated baseline 0.0125. All use
`a_after=clip(exp(-lambda*dt)*a_previous+u, -4,4)`, without output/discharge.
This is a leaky impulse accumulator equivalent, not a normalized WEMA
implementation or production neuron.

Baseline estimation, qualification and accumulation are explicit separate
stages: frozen zero reference, pass-through qualification, then accumulation.
No input amplitude, weights, threshold, topology, or output changes count
as success. Neither variant is selected/tuned from a critical root.

**OBSERVED:** All 320 sequence identities remain present. Categories stay
212 NO-RECEPTIONS, 33 TEMPORAL-RETENTION-LIMITED, 75 DRIVE-LIMITED,
0 CANCELLATION-LIMITED and 0 ALREADY-CROSSING. This is 108 reception-bearing
streams and 235 successful destination receptions per phase.
**Luna-46 MIXED is unchanged.**

| Component | tau | Retention rescues | Unrescued retention | Drive-limited non-crossing | Target clipping | Max absolute state |
|---|---:|---:|---:|---:|---:|---:|
| Frozen calibrated component | 80 | 0/33 | 33 | 75/75 | 0 | 0.8284450023885981 |
| Fixed finite retention | 800 | 19/33 (57.58%) | 14 | 75/75 | 0 | 1.8322317142926783 |
| Fixed finite retention | 8000 | 31/33 (93.94%) | 2 | 75/75 | 0 | 2.0455741348599523 |

The union is 31, not 33, so **SUPPORTED** criteria are not met.
All gate checks on authoritative Git evidence pass; no target clipping or
drive-limited crossing occurred. Rescue is representability of the signed
state at an unchanged boundary, **not canonical emission or task success**.

**OBSERVED negatives:** `c01-009` and `c02-025` remain below threshold:

| Stream | Max abs state, tau80 | tau800 | tau8000 | Best tau8000 threshold margin |
|---|---:|---:|---:|---:|
| c01-009 | 0.49586530991358674 | 0.9104793466835653 | 0.9959814194483699 | -0.004018580551630069 |
| c02-025 | 0.4838807819657352 | 0.9040541974893042 | 0.9962404925050159 | -0.0037595074949841045 |

Do not round these into crossings. All 75 drive-limited IDs, both negative
retention IDs, and the fourteen tau800 negatives remain in machine-readable
sequence evidence. No cancellation category was available in this dataset;
signed cancellation is separately exercised in fixed synthetic tests.

## Historical compatibility and numerical evidence

**OBSERVED:** Outside the target diagnostic, the 320 reviewed Luna-44
source-to-relay streams contain 1,715 receptions. Applying the same isolated
no-output components changes historical representability:

| Component | Crossing streams | Changed crossing streams vs tau80 | Changed per-event crossing decisions | Changed state events | Cap/clipping events |
|---|---:|---:|---:|---:|---:|
| tau80 | 108 | 0 | 0 | 0 | 0 |
| tau800 | 166 | 58 | 358 | 1,418 | 121 |
| tau8000 | 167 | 59 | 373 | 1,418 | 179 |

**LIMITATION:** These are historical **component counterfactuals**, not
the full historical neuron replay. The retained historical canonical
emission count is 235; it is neither recomputed nor changed. That neuron
has discharge/output behavior absent from this component. Historical cap
use is a negative compatibility observation, not retention success.
No historical emissions, feedback or task behavior are inferred.

Every relevant target reception retains signed before/retained/after state,
dt/rho, both signed boundary margins, absolute threshold margin, clipping,
signed/absolute decay loss, payload and difference from baseline. Both
phases retain raw enqueue/reception rows, exact boundaries, fixture/raw/input
identities and frozen configurations.

**OBSERVED:** 940 baseline before/after component comparisons across the two
phases have maximum residual 0.0. Exact reconstructed Luna-46 sequence
evidence also equals the reviewed corrected artifact, retaining its own
equation comparisons. Equation bounds are
`64*epsilon*max(1,abs(observed),abs(expected))`, epsilon
`2.220446049250313e-16`. Threshold, hashes, raw bits and replay have no
tolerance. Eighteen independent 90-digit Decimal continuous-time targets
have maximum residual `2.7755575615628914e-17`, within the declared bound.

Six stress cases exercise every fixed rate with 4,096 same-time events at
payload ±1e6. All states remain finite and within [-4,4], with 4,096
declared saturation events in each case. A subsequent 1e12-unit gap
analytically underflows rho to zero and yields zero retained state.
Unsupported/nonfinite inputs, missing clock continuity, invalid ordering,
undeclared rates and excess events reject explicitly. Synthetic controls
also expose single-impulse decay, cancellation, ties and long-gap forgetting.
No discrete approximation or neural timestep is used.

## Integrity, byte provenance and preserved failures

**OBSERVED:** This isolated Windows checkout has `core.autocrlf=true`.
Before any new result, the unchanged Luna-46 integrity test failed because
the physical catalog had a CRLF final newline rather than its pinned LF
Git bytes. We preserved that failing assertion and did not modify historical
files or Git configuration.

The lane-owned ignored `_evidence/` adapter materializes **exact** blobs
from production/evidence baseline `2cef8ea...` and runs the unchanged
reviewed verifier against them. It is a local replay cache, not a committed
fixture or evidence replacement. All 33 reviewed source identities,
22-file Luna-45 catalog, source/fixture/configuration pins and six prior
phase digests pass exact checks. Both routes reconcile 1,950 enqueue/
reception pairs per phase: 1,715 source-to-relay and 235 relay-to-destination.
Reconstructed Luna-46 measurements equal the corrected retained sequences
exactly. Five roots-truncated flags are preserved as bounded metadata, not
missing raw captures or complete expanded ancestry.

Twenty-five of 34 physical evidence files differ from their Git blobs;
each difference is explained by exact LF/CRLF equivalence. Their physical
pre/post hashes are unchanged. Pinned Git bytes are still checked with exact
length/hash, not normalized into a relaxed oracle.

**OBSERVED:** The first code/protocol commit `add3d0c...` was pushed before
an outcome attempt. That attempt exited 2 at the Luna-46 file pin: the
original pin was the inspected physical hash rather than the Git blob hash.
No new accumulator outcomes or bundle were produced. A separate
pre-outcome correction `ec5231d...` changes only this pin/provenance record
and verifies it in tests; rates/equations/criteria stay fixed. It was committed
and pushed before the successful run.

| Resource | Exact Git bytes / SHA-256 |
|---|---|
| Corrected retained Luna-46 | 2337376 / `54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51` |
| Untouched physical Luna-46 | 2337377 / `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` |
| inputs.json | 10665778 / `03b5a27700723afa266e63b516c6b3dfbc9a7accc6983d21a4f7a12e4383b185` |
| results.json | 4577293 / `d1cac5065410767a42a35f99b659b4a4377f1b84d300e5cfd3ed304600322cff` |
| manifest.json | SHA-256 `254fd3f1ba3b8893e9e065fd7ab26e0fa3cd422969a8dfe02924c9067203a51f` |
| Protocol Git blob | SHA-256 `6f947a6515b89f72a74a433e6e618c4a3529f53884222b18b1df21c68162a126` |
| Configuration canonical JSON | SHA-256 `d0f5722574594d8335fa67d4ee1f21d68698170fc82cde884a356578b995024f` |

The manifest additionally records execution revision, working and Git code/
protocol/test/verifier hashes, CPython 3.11.5, Windows platform and epsilon.
Lane-owned artifact `.gitattributes` marks generated JSON `-text`, preserving
exact bundle bytes on future Windows checkouts without editing shared Git
settings. The human-written execution log explicitly uses `text eol=lf`.
Initial artifact staging exposed CRLF-as-trailing-whitespace in that log
(diff check exit 2); the owned attribute correction changes no scientific
input/result/manifest bytes. Their staged hashes equal physical hashes.

## Architecture evidence

- **A01/A02:** analytical event-time evolution and exact deterministic
  reception ordering, no global neural update loop or clock.
- **A08:** finite state/event/time/payload bounds and tested saturation/
  extreme-spacing stability.
- **A06:** production predictive coding remains untouched; this component
  does not establish or replace prediction behavior.
- **A07:** labels/statistics remain downstream; qualification is fixed,
  not an adaptive gate consuming evaluation truth.
- **A15:** hardware mapping/precision/physical usefulness **NOT RUN**.

No A01–A15 amendment, architecture promotion, ACP, production parameter,
topology, routing, output or neuron change. All edits are owned additions.
The protocol is the predeclared authority for this narrower investigation.

## Validation record

Every shell call explicitly began with:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47a'
```

`python` below denotes the configured
`C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe`.
Full commands/phases/exits/counts are retained in
`artifacts/luna47a/execution.json`.

| Command | Observed result | Exit |
|---|---|---:|
| `python -m pytest -q tests/test_luna47a_retention.py` before code/pin publication | 73 passed, 1 expected not-yet-generated bundle skip | 0 |
| `python -m experiments.luna47a.run --output artifacts/luna47a` at first protocol commit | BLOCKED on physical-vs-Git pin, no outcome artifact | 2 |
| Same run at corrected committed/pushed `ec5231d...` | PARTIALLY SUPPORTED, integrity gates passed | 0 |
| `python -m experiments.luna47a.run --verify --output artifacts/luna47a` | Exact saved inputs vs raw evidence and result-byte replay PASS | 0 |
| Final `python -m pytest -q tests/test_luna47a_retention.py` | 74 passed, 0 skipped/failed | 0 |
| `python -m pytest -q tests/test_luna46_depth_scaling_diagnostic.py` | 166 passed, 1 physical CRLF integrity failure | 1 |
| Relevant Luna-38/neuron/E2/integration/topology/Luna-45/Luna-44 verification files listed in execution.json | 261 passed, 7 Luna-44 materialization setup errors | 1 |
| `python -m py_compile experiments/luna47a/run.py tests/test_luna47a_retention.py` | PASS | 0 |
| `git diff --check` before code publication | PASS | 0 |
| Final `git diff --cached --check` and `git diff --check` | PASS after owned execution-log attribute correction | 0 |
| Staged JSON/record validation and scientific pin checks | PASS; eleven owned additions, input/result/manifest byte identity | 0 |

**Preserved failures:** The Luna-46 physical-catalog failure was newly
observed in this particular fresh checkout **before** mechanism outcomes;
it is not claimed as an already accepted Luna-46 regression failure
signature. Exact Git verifier passes separately. The seven Luna-44 setup
errors show `authorized generator source differs from the pinned baseline`,
the existing Windows pinned-source materialization issue documented by
the authoritative workflow. Assertions, baseline bytes and configuration
remain unchanged; suites still have exit 1. No baseline waiver is claimed.
Independent Luna-0 must review the source-byte policy and these failures.

Editor test discovery could not see worktree tests; Pylance's user-file
syntax adapter likewise did not recognize this isolated path. Explicit
pytest and py_compile are the executed evidence, not claimed editor passes.
Full repository suite, task efficacy/training, hardware and production
integration were **NOT RUN**. Existing broad-suite failure counts are not
reused as this lane's test results.

## Interpretation, limitations and recommendation

**INFERRED, narrowly:** Within these exact label-free frozen streams, changing
only analytical finite retention makes 31 of 33 zero-decay-representable
retention negatives cross an unchanged boundary. This supports the
isolated temporal-retention mechanism for a subset, not a model recommendation.
Seventy-five drive-limited negatives remain; WEMA retention is not a solution
to absent drive. No finite-rate extrapolation or additional parameter search
was performed for the two remaining negatives.

Longer retention is demonstrably not behavior-preserving for the historical
component streams: more crossings and saturation occur. Qualification is
pass-through, not evidence that noise is filtered. There is no integrated
output, task efficacy, energy benefit, prediction benefit, hardware mapping,
optimal timescale or architecture-promotion claim.

Cross-platform libm bit identity is not guaranteed. Replay is demonstrated
in the captured environment. Filesystem alias checks do not defend against
concurrent parent-alias replacement after validation. Retained truncated
root metadata is not a complete causal ancestry claim.

## Reproduction, rollback and next assignment

On the pushed lane branch, use the explicit Set-Location above, then:

```powershell
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m experiments.luna47a.run --verify --output artifacts/luna47a
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m pytest -q tests/test_luna47a_retention.py
```

For fresh generation, start from a **clean** lane checkout and choose a
new empty owned child, e.g. `--output artifacts/luna47a/reproduction`.
Existing bundle files are never overwritten. Cache can be removed without
changing any committed evidence; it regenerates from exact baseline blobs.
No external dependencies beyond the repository Python test environment
and Git are required. No seed or fit is performed.

Rollback removes only the eleven owned additions listed above; the shared
authorization and production/evidence baseline are untouched.
Publication/ownership/remote/clean checks are performed after this handoff
is committed and returned with exact commit IDs; the publication revision
is the containing Git commit, avoiding a self-referential embedded hash.
Prepublication ownership validation passed for exactly eleven owned additions;
staged input/result/manifest hashes and physical byte equality also passed.

**Next: independent Luna-0 review only.** Review protocol timing, exact Git
byte source policy, preserved failures, signed negative margins, historical
cap effects and replay. This worker does not self-approve integration,
merge any branch, launch another agent, amend governance or authorize a
successor. Stop after the pushed handoff and remote/clean verification.
