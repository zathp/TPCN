# WC1-A3-P - Exact publication inventory

This inventory classifies every file in the 23-entry WC1-A3 preservation
manifest before staging. Publication is a curated subset; the manifest-listed
bundle is not eligible for Git publication. No raw evidence file has been
silently edited. Two reports with machine-local absolute paths were replaced
by separately identified sanitized derivatives.

| # | Original archive artifact | Original bytes | Original SHA-256 | Classification | Publication action |
|---:|---|---:|---|---|---|
| 1 | `wc1-a2-four-commits.bundle` | 347,973,854 | `0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887` | Binary bundle | **EXCLUDED**; do not publish in Git |
| 2 | `01-source-read-only-verification.txt` | 75,113 | `fb0d40475afe98b9a7b5e7d162df5e61a85c716ef51f1e5def231b5df73db7e8` | Raw command transcript | **EXCLUDED**; machine-local paths and verbose fsck output; findings summarized in A2 adjudication |
| 3 | `02-isolated-recovery-and-bundle-build.txt` | 1,526 | `100fc060bfa822af7bc2aed54c17f3e2134d962ee67d523db4be8c181e505824` | Failed-attempt transcript | **EXCLUDED**; setup failure, no additional preservation evidence |
| 4 | `02b-isolated-recovery-and-bundle-build.txt` | 927 | `d82c19dd8b9d9a75658cce9fbbfce506518bec5e46fc500168e1b0f03d30fe66` | Failed-attempt transcript | **EXCLUDED**; command-wrapper failure, no additional preservation evidence |
| 5 | `02c-isolated-recovery-and-bundle-build.txt` | 13,823 | `90cb9962fd866f425fccc7eb890f983dd7ed9df3f775522460c16cdd3d6d2d26` | Raw build transcript | **EXCLUDED**; machine-local paths; result summarized in A2 adjudication |
| 6 | `03-bundle-restoration-verification.txt` | 11,131 | `ae2958375c54c956596b3731772d2859918951d4f769e03327a95159198d60ff` | Raw recovery transcript | **EXCLUDED**; machine-local paths; independent review and adjudication retain outcome |
| 7 | `04-source-postcheck.txt` | 33,082 | `45e89015346371a698155004eb1def0abab85c408c885f71f0fd16cd80a4f0ef` | Raw worktree transcript | **EXCLUDED**; contains machine-local worktree paths |
| 8 | `05-independent-review.md` | 3,374 | `1c39f841aabb07d1b08307136a9ea48c238db82473311397458a181ee864f5f5` | Documentary review | **INCLUDED unchanged** as `WC1-A2-independent-review.md` |
| 9 | `06-final-adjudication.md` | 4,788 | `35e1f822a4203368b4bc27a6e3f602344ea6d3954a8c34addd14c4ead7875a9c` | Documentary adjudication | **INCLUDED as sanitized derivative** `WC1-A2-final-adjudication.md`; absolute paths omitted; source bytes unchanged locally |
| 10 | `07-follow-up-authorization-request.md` | 2,353 | `68361c31abfed076caa8190e9a0998feb1cd07edff93e5fa04afb9bb9097c728` | Superseded authorization request | **EXCLUDED**; superseded by WC1-A3-P scope |
| 11 | `object-closure.txt` | 20,907 | `94ecd65fed4e59caf9685017716f977bc7de9c784989af877bf01a932f5a68cc` | Object listing | **EXCLUDED**; raw closure is not necessary for documentary publication; digest and count retained in adjudication |
| 12 | `01-preflight-source-dependencies.txt` | 736,097 | `10b5df9ff74ae4bafa02d9d5c97d056df3f843cb2a4f41a4b1484eb8442400f4` | Raw object enumeration | **EXCLUDED**; machine-specific verbose physical object listing |
| 13 | `02-precopy-bundle-verification.txt` | 3,390 | `018b3dd36e720c69af8c477f588f6d5411239c846ebf76c8d94a42ec8f4b2ebb` | Failed refspec transcript | **EXCLUDED**; failed attempt without state change |
| 14 | `02b-precopy-bundle-verification.txt` | 10,072 | `64c820ea50f2f078e421412d0c3a2f07bdfeb3d782171a929061d9bc4ec961eb` | Raw recovery transcript | **EXCLUDED**; machine-local paths; outcome retained in A3 report and final review |
| 15 | `03-repository-local-copy-recovery.txt` | 8,718 | `ca875bf4b2229229d8850f013bf89a1e2a1c2c90f000f1d98bcf361dd31ec5af` | Raw recovery transcript | **EXCLUDED**; machine-local paths; outcome retained in A3 report and review |
| 16 | `04-source-protection-refs.txt` | 2,770 | `c2904b1f36772be74360012b98b41d48002b4d56b761bccac2ac9714f4e24cbd` | Failed transaction transcript | **EXCLUDED**; failed syntax attempt, no ref changes |
| 17 | `04b-source-protection-refs.txt` | 1,495 | `1068a38d225c606c560a0ce9954f0c21afafdb7c30367b391f3f294c9bebffe9` | Failed transaction transcript | **EXCLUDED**; failed syntax attempt, no ref changes |
| 18 | `04c-source-protection-refs.txt` | 282,846 | `2687481a2becc96511f0340778d8edc93a1ac0128e4385a15e1d0fb56cc30651` | Raw ref/fsck transcript | **EXCLUDED**; verbose machine-specific dangling-object output |
| 19 | `05-source-postcheck.txt` | 9,783 | `ca4842b28028814bb5d5882608a86319c8a82b82c94353999a78b4cf5772c3b0` | Raw worktree transcript | **EXCLUDED**; contains machine-local paths and full worktree inventory |
| 20 | `independent-final-review.md` | 3,001 | `97e9a978c77f4403629006548716cf7bae7b30e7ebf1ed9c0d1c1dbbc4a67b00` | Independent review | **INCLUDED unchanged** |
| 21 | `preliminary-ref-acceptance.md` | 2,155 | `c9a4b9a4f2e819665d9d6514d1b879da8ab511a18af1ea3b86e779b0cdf0237f` | Independent gate decision | **INCLUDED unchanged** |
| 22 | `WC1-A3-preservation-report.md` | 5,678 | `40fa0fc0a2ab0847d638c1998393d95928561e82e5f6f45b9b40c8932ede3178` | Documentary report | **INCLUDED as sanitized derivative** of same name; removes machine-local absolute paths |
| 23 | `wc1-a2-four-commits.bundle.sha256` | 94 | `a856b66abad52b65a7f7bd1a7113eb5d97d2d58cdfe5eb0adb2f8f24d891e7f8` | Bundle integrity metadata | **INCLUDED unchanged**; contains only bundle filename and SHA-256 |

The current WC1-A3 manifest itself (15,114 bytes,
`53af9adcb642d9ec71c2c3ca56eac73558505ed0fa3d964158bd523739f15cac`) and its
100-byte checksum sidecar
(`5f4f729e25c4e893ff7d4f39ebd9f1b7b1b4233b10fd194aaf936c2ae5de4383`) are
verified source identities, but their local absolute storage paths are not
published. A distinct publication manifest records the original identity,
curated inventory, sanitized-derivative parent hashes, and publication-relative
locations.

Explicitly not copied into this publication tree: the complete or previous
partial bundle binaries, restoration repositories/object databases, local
experiment worktrees, unrelated historical source copies, and any untracked
experiment implementations.

