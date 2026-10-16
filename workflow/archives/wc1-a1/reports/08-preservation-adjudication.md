# WC1-A1 - Preservation adjudication

## Overall disposition

**BLOCKED - four-commit identity inventory verified, but complete four-commit preservation is not achieved.** Three targets have an independently reviewed, self-contained bundle and isolated recovery; the fourth (`430b60ed...`) is absent from the candidate and its tree dependency has conflicting storage-versus-lookup evidence. No source-repository protective refs were created.

## Gate results

| Gate | Disposition | Evidence |
|---|---|---|
| Four-commit identity | VERIFIED | Current ref/reflog graph reproduces all four full commit, tree and parent identities. |
| Four-target bundle recoverability | BLOCKED | Bundle contains/recoverably restores 3/4 targets; `430b60ed...` is not in it. Candidate is partial, not a complete four-target backup. |
| Independent preservation review | BLOCKED | Luna-0 independently reviewed the bundle and original state; confirmed three-target success and required no refs because the fourth is incomplete. |
| Local protection refs | NOT CREATED | Full-candidate acceptance condition was not met. Existing refs were not replaced or deleted. |
| Missing-tree diagnosis | EFFECTIVE AVAILABILITY UNRESOLVED | Physical object-store absence and fsck complaint are confirmed; direct `cat-file` returns the canonical zero-byte empty tree. The reviewed bundle/recovery repo do not contain `430b60ed...`. |
| Repository object integrity | BLOCKED | Reflog-inclusive `git fsck --full --unreachable` exits 2 with the missing tree diagnostic. No other missing/corrupt diagnostic was found. |
| Off-machine preservation | NOT AUTHORIZED / NOT PERFORMED | No remote or external storage copy was made. |
| Worktree removal | NOT AUTHORIZED / NOT PERFORMED | No worktree was removed. |
| Neural execution / Track B changes | NOT AUTHORIZED / NOT PERFORMED | No experiment, source change, training or inference was run. |
| RP-2B | BLOCKED / BOUND INCOMPLETE | This repository-preservation gate did not change or infer scientific evidence. |

## Repository and evidence preservation

The original checkout remains on `governance/luna71b-c4-1-ppc11-freeze` at `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`; its pre-existing untracked `_worktrees/` and workflow handoff directories remain. No source-repository ref was created, and no branch, reflog or worktree was changed or deleted. The temporary staging and recovery repositories were outside the TPCN worktrees and were removed after verification; their staging refs were not protective refs in the source repository.

The historical `43fb...` source-manifest and `0ad1...` test-index preimages remain unresolved. Their recovery is not inferred from the preserved commits. Published PPC-11, proposed PPC-11 V2, C4.2-I/J evidence, GN/H source variants, fixture identities, and Luna-64/RP-2B governance were not changed.

## Narrow next action

If a complete four-target preservation is still required, obtain a separate owner decision for investigating exact recovery or authorized repair of the empty-tree storage gap. Then rebuild and independently verify a candidate that recovers all four exact commit IDs and histories before creating any source-repository protection refs. No such recovery or repair is authorized by WC1-A1 as executed.