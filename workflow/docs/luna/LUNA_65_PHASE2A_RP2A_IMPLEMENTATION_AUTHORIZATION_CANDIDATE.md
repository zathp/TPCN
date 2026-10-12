# Luna-65 RP-2A implementation authorization candidate

**Status:** PROPOSED ONLY - IMPLEMENTATION NOT AUTHORIZED.
**Prepared under:** `L65-PHASE2A-RP2-R1-OWNER-DECISION-CLOSURE`
**Proposed separate gate:** `L65-PHASE2A-RP2A-IMPLEMENTATION-STATIC-REVIEW`
**Responsible role:** Luna-65 implementation; independent Luna-11 review;
Luna-0 integrates governance. No agent is dispatched to implement here.

## 1. Exact owner grant proposed, not adopted

> After verified governance publication, authorize ONLY implementation and
> nonexecuting static validation of the two source paths in section 2 against
> the immutable R1/direct dependencies and accepted owner-decision record.
> Freeze the embedded synthetic literal and startup/import manifests, Windows
> FFI/ABI/SD/access masks, command/environments/timing, bounded evidence and
> every cleanup/failure path. Require separate independent A-D static reviews
> of identical final source bytes and publication/fetched identity verification.
> Do not import/run either source, create a token/job/process, execute an outer
> wrapper or compatibility probe, qualify a supervisor or run a fixture.
> RP-2B execution requires a later distinct owner grant.

The owner must separately name the full verified governance publication commit,
the Git blobs/checkouts of all contract dependencies and this candidate before
adopting that grant. No placeholder commit is an authorization.
Current policy acceptance/publication permission does NOT accept this grant.

## 2. Exact proposed file ownership/allowlist

Only new executable sources:

- `scripts/luna65_phase2a_rp2_compatibility_probe.py`
- `scripts/luna65_phase2a_rp2_outer_wrapper.ps1`

Plus one RP-2A implementation handoff and one additive authoritative workflow
entry, reviewed before source publication. No helper module, generated .cs/
.dll/.exe/.pyc, dependency manifest/install, fixture, supervisor, RP-1 source,
neuron/runtime, ACP or historical-record change. Native interop must remain
inside the attended PowerShell wrapper; any required additional file or build
artifact needs a new explicit allowlist decision. No source exists by this
document's creation; do not invent source/literal SHA-256.

## 3. Frozen inputs and precedence

Apply [owner decisions](LUNA_65_PHASE2A_RP2_R1_OWNER_DECISIONS.md) prospectively,
then [R1](LUNA_65_PHASE2A_RP2_OUTER_LAUNCHER_CORRECTIVE_R1.md) for Medium/
outer/token corrections, then unchanged
[direct design](LUNA_65_PHASE2A_RP2_DIRECT_INTERPRETER_DESIGN.md) and referenced
historical RP-2 details only where not superseded. Historical BLOCKED records
remain history, not competing current authority.

| Input | Frozen reviewed checkout identity |
|---|---|
| R1 CRLF SHA-256 | `F9913AC44C268291988F549A110B2EFCC4777139A2BB8BD0DA407DF020FABEFB` |
| R1 Git-clean LF blob | `8abb50dfef732da71cee94b1623c61b3f4f8e49e` |
| Direct candidate SHA-256 | `374AB0328B62966EEA7C1E52E9E9E25BB40D973863177DEC4160D077E1C2A476` |
| Direct Git-clean LF blob | `66356a9328e6fc4dfc28e8b8eb2fdbbfc0cdf15d` |
| Older corrected RP-2 SHA-256 | `E573ADA32D746E6766D21420C845FF6AA09B18107F05523A6F1BE8913EE3A313` |
| Older corrected Git-clean LF blob | `f61847d0c93f59b189142c5544caf9791e32bbe4` |

Exact interpreter for P and L:
`C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe`,
SHA-256 `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`,
Python 3.11.4 AMD64. O host is existing non-elevated Windows PowerShell 5.1;
its exact executable/version/startup/interop binding is a static deliverable
and RP-2B preflight prerequisite, not an arbitrary replacement host.

Raw CRLF identities and Git-clean LF identities differ by normalization.
Preserve exact published blobs and declared checkout materialization; do not
claim a future LF checkout must have the CRLF SHA-256. Any content change
beyond declared newline normalization needs new exact-byte review.

## 4. Mandatory source deliverables

- Explicit ctypes Windows signatures, structure layouts/packing, lengths,
  pointer lifetime, handles, DWORD/BOOL/SIZE_T widths and immediate API error/
  NTSTATUS semantics. No broad exception suppression or successful defaults.
- Native O CreateProcessW suspended admission: ordinary NULL process/thread
  SDs; pre-resume actual SD/token/image/PID+creation-time/rights readback;
  retain process/thread authority 0x00121401/0x00120042, two Medium capture
  writes only; Medium three-variable block. No existing SD edits.
- P CreateRestrictedToken from exact own primary source mask 0x2008B;
  derived handle SAME rights; Low IL set only on derived token; mandatory
  policy 3 readback without repair; B01 full privilege/name/attribute checks,
  frozen groups/no restricting SIDs, no source privilege adjustment.
- Token-object SD owner/group/DACL/label readback and drift checks distinct
  from contained fields; no audit-SACL/new privileges or inferred token DACL.
- Low one CreateProcessAsUserW with exact X-L descriptors, HANDLE_LIST
  exactly three P-L writes, JOB_LIST sole job, frozen flags/stdin NULL,
  exact four-variable environment/cwd; pre-resume admission; no fallback.
- One fixed embedded ASCII synthetic literal implementing only the reviewed
  specification; exact quoted argv, nonce/schema/READY-END/order/bytes and
  module-origin/content manifest. Freeze complete Medium/Low startup and
  import/DLL/.pth/hooks/user-site/cwd/transitive pytest closure/absences using
  static bounded inspection. No target imports to discover closure, package
  installs, -S/-I/PYTHONPATH workaround or removed pytest import.
- U1/U2/U3 independently inspectable sections, PSS finite checkpoints,
  duplicate/compare/object-basic rights ABI and limitations, runtime opens
  distinguished from inherited objects; no dump/global census/VA clone.
- GetTickCount64 common epoch and validated O0/P0 metadata; 10 s active,
  <=5 s cleanup and 20 s outer; one invocation/Low attempt, zero retries.
  64 MiB job charge, eight-process backstop, five-second job user-time, no
  breakaway/UI limits, effective configuration readback. No stress fixture.
- O sole evidence-file writer; P byte-preserving encoded relay, bounded
  readers/buffers, exact stream recovery, all simultaneous representations
  <=1 MiB with 131,072 finalization reserve/917,504 payload, reserve-before-
  write/high-water/final hashes/reparse/leaf rules; no uncounted temp files.
- P sole nonduplicated job; all write observation duplicates close before
  EOF, worker cancellation/waits, snapshot/token/pipe/thread/process closure,
  job last. O at most one retained-handle TerminateProcess, bounded wait/EOF.
  No name/PID-only kill or guarantee inferred from termination requests.
- Full fault/race precedence, explicit no-child vs unknown-create states.
  Missing Low cessation => RP2_UNKNOWN_FAIL_CLOSED, explicit operator alert
  that containment is unresolved/Low may survive, never RP2_PASS or automatic
  downstream progression. No silent continuation or recovery workaround.

## 5. Allowed NONEXECUTING checks after a separate RP-2A grant

Read files, hashes, Git diff/attributes and editor diagnostics; static
AST/syntax parsing of source TEXT without import, bytecode or target execution.
PowerShell Parser.ParseFile/ParseInput only, never invoke/dot-source wrapper
or execute Add-Type/native interop. FFI/SD/ABI/control-flow/ownership review
against documented APIs without calling Windows token/job/process functions.
Any parser tool runtime itself must be explicitly bound and never load target
code; no pytest, compileall, py_compile artifact, dependency install, probe
--help/self-test or "dry-run" that imports/launches target source.
No static test may silently turn into a fixture/API-mechanism execution.

## 6. Independent implementation review and stop conditions

A: exact token/SD/access masks and handle ownership. B: direct image/literal/
closure/environment/three Low handles/finite U1-U3 evidence. C: O/P timing,
single-writer accounting, job ownership, fault races, all cleanup paths and
explicit UNKNOWN operator notification. D: exact identities/source allowlist,
owner decisions/scientific isolation/publication/authorization boundaries.

All four inspect the SAME final probe/wrapper/literal/manifest identities.
Implementation author must not approve its own work. Freeze source hashes/
blobs, record passed/failed/not-run checks and source/literal dependencies in
handoff. Static PASS does not demonstrate host feasibility or execution.
If closure/ABI/ownership cannot be bound, return BLOCKED; no new privileges,
environment widening, helper/source expansion or execution as a diagnostic.

After owner-authorized implementation, reviewed source publication/fetch
verification is separate from RP-2B. RP-2B must later name full source commit/
hashes/literal/closure, exact outer command/host, run ID, fresh evidence path/
preflight/operator/stop procedure and accepted limits. No RP-2 run now.
Production venv compatibility, RP-3, supervisor/fixtures/full Spiral/Luna-64
remain blocked/not authorized as before; Luna-63C remains frozen.
