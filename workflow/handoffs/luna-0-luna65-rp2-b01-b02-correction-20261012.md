# Luna-0 Luna-65 RP-2 B01/B02 Corrective Contract Review

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "RP-2 B01/B02 corrective governance review"
  task_id: "L65-PHASE2A-RP2-B01-B02-CORRECTION"
  component: "Luna-65 Phase 2A RP-2 contract"
  status: "blocked"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "45121227d96c6fa13357c6bdf5fba0d99d8d7352"
  result_revision: "uncommitted; BLOCKED; no publication"
  dependencies: ["Frozen R7 profile", "Preserved unpublished RP-2 BLOCKED preparation"]
  owner: "Project owner"
  classification: ["governance-only", "design", "independent exact-byte review"]
  hypothesis: "Exact token and descriptor/launcher semantics can support a reviewed bounded compatibility contract without silent profile changes."
  counter_hypothesis: "Frozen interpreter behavior or descriptor constraints require unaccepted policy changes."
  interfaces_relied_on: ["Microsoft Windows security/process API documentation", "Public CPython v3.11.4 launcher source; not proven local binary correspondence"]
  label_information_boundary: ["No TPCN, datasets, E2 counters, training, fixtures or scientific workload"]
  timing_assumptions: ["Proposed 10 s active; <=5 s cleanup; 20 s attended outer; no measured or hard real-time qualification"]
  reset_boundaries: ["No RP-2 invocation consumed", "RP-1 consumed; no retry; original verdict preserved"]
  resource_bounds: ["Unchanged proposed 64 MiB job charge, 8-process backstop, 5 s job user-time backstop, 1 MiB retained output"]
  authorized_scope: ["Governance/design correction", "Four independent exact-byte reviews", "Conditional publication only after decisions/reviews PASS"]
  unauthorized_scope: ["RP-2A implementation", "RP-2B execution", "RP-3", "Supervisor work/qualification", "Capacity fixtures", "Windows security changes"]
  controls: ["Baseline and prior draft hash verification", "Exact snapshot of prior contract/handoff/workflow", "Freeze corrected contract for A-D", "No owner approval inferred"]
  measurements: ["File identities and ancestry only; no runtime compatibility or enforcement evidence"]
  information_boundary_check: ["Documentation/public source inspection only; no probe or Python workload"]
  hardware_mapping: ["Not applicable; no hardware realization/equivalence claim"]
  architecture_invariants_touched: []
  preserves: ["B-min selection", "Historical RP2 BLOCKED reviews", "RP1_CONTRACT_DEFECT", "All execution prohibitions", "Untracked supervisor and authorization records"]
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md"
    - "workflow/handoffs/luna-0-luna65-rp2-b01-b02-correction-20261012.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All token/job/process/host compatibility tests", "All fixtures, benchmarks and supervisor qualification"]
  assumptions: ["Public launcher source is design evidence, not verified local binary behavior"]
  unresolved: ["B01 affirmative owner acceptance", "B02 full-chain descriptor/access decision", "Intermediate launcher environment/inheritance/internal-job policy decisions", "Binary/source behavior binding and exact later static source deliverables"]
  recommended_next_agent: ["Luna-0: obtain explicit profile decisions and re-review any changed exact candidate; no implementation or execution"]
```

## Outcome and provenance

**OBSERVED:** HEAD remains `45121227d96c6fa13357c6bdf5fba0d99d8d7352`,
branch as above. Prior contract checkout SHA-256 matched
`840D06F6F28ABA6CDF285C375A9CB6E8882A6BAEF4BF74A8B4A9986E9F0D1099`.
Before editing, exact contract, preparation handoff and workflow snapshots
were retained under the session artifact directory `rp2-before-b01-b02`.
The previous preparation handoff and review record were not rewritten.
Contract sections 1-9 retain preceding requirements/reviews, with an explicit
heading pointer to governing section 10; section 10 adds the corrective design.

**INFERRED:** API/public-source analysis supports the proposed B01 enablement
invariant but identifies full-chain descriptor and launcher-policy questions.
This is not measured Windows incompatibility. The selected B-min architecture
and its protection requirements were not silently changed.

No source was created, imported or executed. No token, job, child process,
probe or security configuration operation was performed. No files staged,
committed, pushed or fetched for this correction.

## B01 owner-decision status

Microsoft documents DISABLE_MAX_PRIVILEGE as disabling all privileges except
SeChangeNotifyPrivilege and ignoring privilege-deletion parameters when that
flag is set. Presence is not enablement; deletion is not guaranteed.

Proposed replacement: SeChangeNotifyPrivilege is the only enabled privilege;
other entries may remain disabled; full LUID/name/attribute readback required;
unexpected enabled privilege is failure. The source token must already have
ChangeNotify enabled; the constructor is not assumed to enable it.

**AWAITING OWNER APPROVAL.** This task asks for design/review, not affirmative
acceptance. The historical only-entry invariant remains unamended. No token
repair, new privileges, alternate launch API or elevation is authorized.

## B02 descriptor/access design

The exact matrix and candidate root SDDL are in contract section 10.2.
Root is the Low venv launcher, not an additional synthetic process. Candidate
root process/thread descriptors have owner U, protected DACL with zero allow
ACEs and one OWNER RIGHTS deny READ_CONTROL|WRITE_DAC, Low NO_WRITE_UP label.
Parent relies on full creation-returned handles; they are not inherited.
The candidate is not a proven viable launcher descriptor or a selected policy.

Public stock venv code creates a distinct base process via internal
CreateProcessW with NULL process/thread security attributes. Owner and DACL
come from the venv token; actual default DACL/label is not invented here.
Full-access base process/thread handles are initially held by the venv, not
returned to the Medium probe. Its thread handle is closed by the launcher;
the process handle is retained for wait/exit. Proposed Medium base observation
union 0x00121440 must be acquired and read back without new grants/privileges.

**B02 UNRESOLVED for the full frozen chain.** Directly specified root security
does not prove descriptor control of the base descendant. A shared-user default
ACL observation path conflicts with a literal chain-wide prohibition on
workload-principal grants; a root-only scope exception is proposed, not adopted.
The actual default owner/DACL/label and binary behavior remain future static
bindings, not measured or permission-assumed evidence.

Reviewer interpretation limits: lane A used broad impossibility language and
asserted a default user allow ACE without a newly observed TokenDefaultDacl.
No such default-DACL readback occurred in this gate. Also, a retained root
PROCESS_ALL_ACCESS handle already includes DUP_HANDLE: reopening that root
is not inherently required to duplicate a venv-held base handle. A narrowly
specified handle-transfer/inspection design might be investigated under
separate governance review; it was not selected or independently proven here.
The integration adopts the demonstrated missing full-chain descriptor/access
plan, not a universal theorem that all alternative access designs are impossible.
Neither that alternative nor owner-authority DACL repair is authorized by this
candidate. No new ACE is invented to produce a PASS.

## Venv topology and remaining policy decisions

Public CPython v3.11.4 build compiles PC/launcher.c with VENV_REDIRECT:

1. Medium probe -> suspended Low venv root -> distinct Low base image/PID.
2. Base argv[0] maps to base path while the synthetic argument tail is fixed;
   sys.executable may still refer to the venv and is not image proof.
3. Launcher inserts __PYVENV_LAUNCHER__ into the intermediate environment.
   Root has four supplied variables; every-stage four-variable identity cannot
   be assumed. Exact internal-variable handling needs owner/static review.
4. Stdout/stderr are duplicated as inheritable same-access objects; numeric
   equality is required only at root. Ledger forwarding must be independently
   evidenced at base, not inferred from successful stdout.
5. Root->base uses generic inheritance, not another explicit HANDLE_LIST.
6. Launcher creates its own internal kill-on-close/SILENT_BREAKAWAY_OK job
   and does not check its assignment result. Outer job limits/membership are
   separately required; no loosening or nested-job success is presumed.

These are public-source findings only; the local hash-bound launcher is not
yet linked reproducibly to those sources. No host execution was used to close
that provenance gap.

## Fresh independent exact-byte review

All four separate Luna-11 reviews verified the same final contract:

| Representation | Exact identity |
|---|---|
| Raw checkout SHA-256 | `E573ADA32D746E6766D21420C845FF6AA09B18107F05523A6F1BE8913EE3A313` |
| LF-normalized SHA-256 | `B8B0DE27BD833396DF87990B1A088F3453AEE40796F2ACB81CBFD752BBB150AC` |
| Raw CRLF blob | `489707e18bf422c370678a1433aad983fd14e552` |
| Git-clean LF blob | `f61847d0c93f59b189142c5544caf9791e32bbe4` |

| Lane | Verdict | Independent disposition |
|---|---|---|
| A Token/descriptors | BLOCKED | B01 technical amendment sound but unaccepted; full-chain B02 and stock-launcher exceptions unresolved. Candidate root handle plan does not establish descendant compliance. |
| B Interpreter/inheritance | BLOCKED | Prior startup closure, literal binding, topology, object-vs-value mapping, READY/inventory/EOF design clarified; intermediate environment, default descriptors, generic inheritance and internal-job policies still need decisions/binding. |
| C Cleanup/evidence/resources | PASS, lane only | Independently accepted startup-content obligations, normal/failure/no-child deadlines, bounded readers/cancellation, candidate limits, all-file high-water/reserve accounting and fail-closed precedence. No runtime qualification. |
| D Governance/provenance | PASS, lane only | Exact baseline/candidate/prior snapshots and protected records verified; proposed decisions not treated accepted; authority/scientific boundaries preserved. |

**Integrated verdict: BLOCKED — RP-2 CONTRACT INCOMPLETE.**
Technical review is not wholly PASS: descriptor/policy completeness remains
open even apart from B01 acceptance. C/D PASS are lane-only design/governance
results, never proof of Windows or neural architecture invariants.
The contract was not edited after the final review identity freeze.

## Validation record

| Procedure | Actual result |
|---|---|
| HEAD/branch/prior SHA-256 and empty index | Verified before design edits |
| Exact prior draft/handoff/workflow snapshots | Preserved before correction; reviewed by D |
| Microsoft API and public CPython source inspection | Documentation/design findings only |
| Four independent candidate hash checks | All matched the raw/LF/Git-clean identity above |
| CRLF-aware diff and protected-file checks | Recorded in final session validation; no executable tests |
| Runtime APIs, source implementation, fixtures/benchmark | NOT RUN / NOT AUTHORIZED |

## Publication and next bounded assignment

No publication identity. Proposed future corrective governance allowlist:
contract, this corrective handoff, authoritative workflow entry. The original
preparation handoff remains unchanged, and unrelated untracked supervisor and
S1-B authorization record stay excluded. The current candidate remains local.

Next owner prerequisite is affirmative B01 amendment acceptance, plus an
explicit disposition of the full-chain B02 and stock-launcher environment/
inheritance/internal-job policy issues. Then Luna-0 prepares an exact resolved
design for renewed review of any changed bytes. Before RP-2A: all necessary
policy decisions, complete descriptor/access plan, binary/source behavior
binding obligations, integrated exact-byte A-D PASS and governance publication
verified against fetched remote, then a new explicit owner source allowlist
authorization. RP-2A may freeze literal/import closure/ABI/schema and inspectable
cleanup/accounting source; it cannot execute. RP-2B needs a later distinct
execution authorization.

RP-1 consumed/no retry, historical RP1_CONTRACT_DEFECT; RP-2 implementation/
execution, RP-3, supervisor/qualification and Phase 2A/2B fixtures NOT AUTHORIZED;
full Spiral and Luna-64 corrective execution BLOCKED; Luna-63C FROZEN.
