# WC1-A3 - Luna-0 preliminary source-ref acceptance

**Reviewer:** Luna-0 Architecture Guardian  
**Scope:** Read-only independent acceptance gate before source-ref creation  
**Source baseline:** `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`, branch
`governance/luna71b-c4-1-ppc11-freeze`

## Decision

**ACCEPT three refs; REJECT one.** This is preliminary acceptance for ref
creation only, not the final WC1-A3 review. No refs were created by the
reviewer.

| Proposed ref | Decision | Basis |
|---|---|---|
| `refs/preservation/wc1-a3/430b60ed3684dde1d4f618d2e4c8d23410d81928` | REJECT | Required empty tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904` is absent from physical object enumeration; scoped `git fsck --full --strict` exits 2. Do not create a healthy-looking source ref. |
| `refs/preservation/wc1-a3/77938eb04aa058246e19267326747101664cf777` | ACCEPT | Complete 220-object closure, all physically enumerated; scoped strict full fsck exits 0. |
| `refs/preservation/wc1-a3/6db1e4754851cf86389ef6c7b562a6f7606cfacc` | ACCEPT | Complete 223-object closure including parent `77938eb04aa058246e19267326747101664cf777`; scoped strict full fsck exits 0. |
| `refs/preservation/wc1-a3/b85eb31e7801c1c8c3ee48968978cfe40a5d8aef` | ACCEPT | Complete 223-object closure including parent `bcb76a40778d235806cf863dd2a9b753937dabcf`; scoped strict full fsck exits 0. |

For each target the reviewer checked the commit/tree/parent identities,
`rev-list --objects --missing=print`, physical object enumeration against
7,488 objects, and scoped strict fsck. `rev-list` emitted no missing marker
for the first commit, but physical enumeration and fsck independently show its
empty tree missing.

No refs already contained any target. The A2 bundle has the expected four
refs, size 347,973,854 bytes, SHA-256
`0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`,
complete history, no prerequisite-only dependency, and independently recorded
successful recovery.

The reviewer made no source changes. The full reviewer response is preserved
in the A3 handoff/evidence record; the final review is a separate gate.

