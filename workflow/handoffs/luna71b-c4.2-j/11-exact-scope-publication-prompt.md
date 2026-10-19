# Exact-scope publication prompt (not authorized by this handoff)

> **Do not execute unless the project owner separately authorizes publication.**

Please publish only the exact files enumerated by
[`10-artifact-manifest.json`](./10-artifact-manifest.json), plus that manifest
and its detached `10-artifact-manifest.sha256` integrity file. Independently
verify the detached SHA-256 and every listed artifact's byte size and SHA-256.
The manifest is the complete content allowlist; do not add a directory,
wildcard, unlisted temporary file, generated test artifact, or unrelated
worktree content.

Preserve the published C4.1/C4.2 checkpoints, the original H/GN evidence, and
the unavailable historical identities without rewriting them. Do not run
neural training or inference, a paired pilot, or RP-2B. Do not amend or
replace historical artifacts. If any allowlisted file no longer matches the
manifest, stop and request a new reviewed manifest rather than refreshing
hashes in place.

Before acting, return the exact Git paths to be published and proposed
publication mechanism for owner confirmation. This document is a prepared
prompt only and grants no commit, push, merge, or publication authority.
