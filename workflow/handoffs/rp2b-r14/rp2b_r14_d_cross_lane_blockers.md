# RP-2B R14-D — Cross-Lane Dependency and Blocker Reconciliation

**Disposition: BLOCKED — independent technical gates remain open.**
This integration reconciles R14-A/B/C and creates no new result, admission
rule, limit, owner selection, or source authority.

**Baseline:** branch `governance/luna64-r4.3-freeze-20261010`, HEAD
`f117ce51e7a805564e37252d3b5c99bda163ce57`. R14-A is **BLOCKED — BOUND
INCOMPLETE**; R14-B is **PASS WITH FINDINGS** for existing-result
classification only; R14-C is **BLOCKED** for complete interface and
semantic-preservation scope.

## Cross-lane dependencies

| Dependency | Evidence from lanes | Circular or inconsistent assumption to avoid | Responsible lane / next proof or decision | Independently closable now? |
|---|---|---|---|---|
| Resource maxima ↔ admission semantics | A: `N_LOW`/`T_LOW`, family widths and total maxima unsupported. B: new admission/refusal mapping deferred by OD-4/C. | Do not claim finite evidence maximum by assuming a refusal rule that is not adopted; do not adopt a refusal outcome to make an accounting model fit. | A+B: close existing-contract inventory/accounting where derivable; any changed admission semantics require separate owner decision/amendment. | **No** for all-path total; partial source bounds can be documented only. |
| Terminal reserve ↔ reachable finalization | A: 131,072 is not sized/reachable on every path. B: reserve exhaustion and partial terminal write lack universal new exact result. | A fixed reserve cannot be used as its own proof, and capacity admission cannot rely on a terminal result that is not admitted/reachable. | A+B: establish joint terminal obligations, reservation lifecycle, exact path semantics; defer unresolved branch behavior under OD-4/C. | **No**; proof not established. |
| Simultaneous copies ↔ P/O interface | A: raw/hex/decoded/structured copies and worker lifetimes overlap without complete coverage. C: queues, pending chunks, relay strings/bytes, parsed objects, files and report objects cross P/O boundaries. | Do not sum serialized file lengths alone and call it peak; do not assume P/O-only work owns all copies or all lifetimes. | A+C: complete every producer/caller/failure/cleanup transfer and lifetime model; independently reconcile every reservation. | **No**; P/O boundaries not proven complete. |
| Transport ↔ mandatory families | A: six explicit Low READY/END calls are finite, but startup/error diagnostics and whole-attempt transport are not. C: relay predicates differ across producer, P parser and O validator. | Do not promote the explicit literal bounds into `N_LOW`/`T_LOW`; do not omit malformed/partial bytes to fit. | A+C: enumerate all byte producers, pipes, records and failure paths under OD-1/A and OD-5/A; prove exact accepted boundary. | **No** for all-attempt transport. |
| Full copies ↔ 1 MiB retained cap | A: disk identity \(D=R+E+L_b+U+A+F\) omits transient representations and uncertain partial prefixes. B: total cap is 1,048,576, payload cap cannot consume 131,072 finalization amount. | Do not infer feasibility or infeasibility from nominal record sizes, R2 allocations, or disk-only identity. | A: joint path/time peak plus independent terminal-admission proof. OD-2/A preserves all current copies/recovery duties. | **No**; no complete numeric fit result. |
| Sink failure ↔ alert ↔ terminal result | B: evidence-write failure is incomplete; no universal new result for sink failure. C: console warning path is separate from sole durable sink; attempt ≠ delivery; `Alert-Unresolved` exceptions can interrupt follow-on work. | On total unavailability of the sole sink, persistence of its own failure record cannot be guaranteed. An individual write failure alone does not establish total sink unavailability; later write outcomes and extant artifacts must be assessed separately. Do not claim alert attempt upgrades UNKNOWN or invent alert-failure outcome. | B+C: trace attempt path and actual evidence separately; preserve D-RP2-OUTER-1 warning; any novel classification is deferred. | **Partly:** existing warning/UNKNOWN rule is established; proof of attempt/delivery is not. |
| Report write ↔ later finalization failure | B and C: O writes report at O:1033, then flushes/closes/hashes/prints; a later exception enters O:1038 and changes process verdict to UNKNOWN without rewriting the report. | Do not assume persisted report verdict and final in-process verdict remain aligned after a post-report exception. Alert exceptions can also prevent guaranteed subsequent finalization/disposal. | B+C: reconcile source behavior with contractual confirmed-cessation/incomplete-finalization criteria; no source correction or replacement outcome within R14. | **No equivalence established.** |
| Frozen profile ↔ observed feasibility | A: 64 MiB job charge is not combined L/P/O memory or artifact bound; local counters do not prove OS behavior. B: R2 remains Phase 2A only. | Do not substitute job user-time with aggregate CPU, charge with private commit, monitored time with hard cutoff, or requested stop with cessation. | A: static profile-to-source reconciliation; runtime proof would require future separate authorization. | **No** for feasibility/qualification. |

## Blocker register

| Blocker | Evidence / affected requirement | Responsible lane | Next required work or decision | Independently closable? |
|---|---|---|---|---|
| Complete mandatory-family inventory and encoded maxima | A U1/U2/U3/controller/O families are only partially bounded; OD-1/A keeps existing families mandatory. | R14-A | Reconcile every contract-required producer, schema, count, width, conditionality, and co-occurrence. No invented family details. | **Not from current P/O evidence.** |
| All-attempt Low transport maximum | Explicit subset `N_explicit≤6`, `T_explicit≤98,304`; total `N_LOW` and `T_LOW` unsupported. | R14-A / R14-C | Trace diagnostics/startup/EOF/error/write paths and prove enforceable totals without changing OD-5 accepted behavior. | **No.** |
| Partial-write and replay/custody accounting | P popped chunk can leave pending accounting before failed emit; O can re-drain a published chunk after failure. | R14-A / R14-C | Map byte prefixes, chunk ownership and durable reconciliation across every write and cleanup branch. | **No.** |
| Complete simultaneous representation/lifetime peak | P/O projection multipliers omit native/worker/transient forms; L/P/O overlap. | R14-A / R14-C | Time-indexed lifetime/co-occurrence and resource-ledger proof against adopted cap/profile. | **No.** |
| Console/governance/operator retained-material boundary | Operator console is not automatically durable evidence; external governance package schema/bounds unresolved. | R14-A / R14-B | Identify existing required material and custody boundary without inferring exclusions; account only where contract requires. | **No.** |
| Terminal reserve and admission | No joint terminal-family maximum or proof all required terminal paths can be admitted; raw P FINAL must first pass ordinary O payload admission. | R14-A / R14-B | Prove terminal family maxima, reserve isolation and reachable admission for existing semantics. New refusal mapping remains owner-deferred. | **No.** |
| Novel refusal/result precedence | Candidate-limit breach, admission failure, reserve exhaustion, alert failure, and some terminal/write branches lack a universal exact result. | R14-B | Preserve existing mappings; defer affected implementation under OD-4/C. A changed policy needs explicit future owner action. | **No** for novel behaviors. |
| Candidate-source finalization/report divergence | O:998–1007 chooses a verdict; exception in O:1009–1037 forces UNKNOWN at O:1038; report write at O:1033 may precede failure, leaving the report and final in-process verdict divergent. | R14-B / R14-C | Reconcile implemented behavior against C:312–313, 359–366, 631; no source fix or replacement result authorized. | **No**; material discrepancy requires later governance review. |
| Alert exception continuation | `Alert-Unresolved` O:83–85 directly writes console; call sites O:1001 and 1038 do not guarantee continuation if it throws. | R14-B / R14-C | Preserve attempt-only scope; do not claim delivery, completed cleanup, or alert-specific outcome. Further source/contract handling requires separate authorization. | **No**; failure outcome unadopted. |
| P/O semantic interface and complete source scope | Interfaces outside P/O include attended operator, host APIs, sink/custody; caller/producer/failure/cleanup paths incomplete. | R14-C | Complete call graph/interface, exact acceptance-set analysis, and exact proposed diff boundary before any future allowlist review. | **No.** |
| Frozen-profile feasibility | Resource accounting is incomplete; no runtime/OS behavior authorized or evidenced. | R14-A / R14-C | Close static bounds first; any runtime evidence requires separate future authorization. | **No.** |

## Integration result

The lanes do not establish a contradiction among owner-selected policies;
they also do not establish the capacity or terminal properties needed to
implement them. There is circular dependency if finite maxima depend on
unadopted admission limits, or if reserve sufficiency depends on a terminal
result that is not contractually defined. Preserve all null totals/headroom.
P/O remain candidate sources. RP-2B remains **BLOCKED / BOUND INCOMPLETE**.
