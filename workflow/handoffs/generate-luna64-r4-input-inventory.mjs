import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const outputPath = path.join(root, "workflow/handoffs/luna-0-track-b-execution-gate-r4-input-inventory-20261010.json");
const paths = [
  ".github/agents/luna-64.agent.md",
  "workflow/ARCHITECTURE_CONTRACT.md",
  "workflow/ARCHITECTURE_CHANGELOG.md",
  "workflow/docs/luna/LUNA_WORKFLOW.md",
  "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md",
  "workflow/docs/architecture_proposals/ACP-0008.md",
  ".github/agents/luna-63c.agent.md",
  ".github/agents/luna-63c-mechanism.agent.md",
  "workflow/handoffs/luna-0-luna63c-mechanism-authorization-20261009.md",
  "workflow/handoffs/luna-0-track-b-governance-authorization-20261010.md",
  "workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010.md",
  "workflow/handoffs/luna-0-independent-review-track-b-execution-gate-20261010.md",
  "workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010-R1.md",
  "workflow/handoffs/luna-0-independent-review-track-b-execution-gate-r1-20261010.md",
  "workflow/handoffs/luna-0-track-b-execution-gate-r1-manifest-20261010.json",
  "workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010-R2.md",
  "workflow/handoffs/luna-0-independent-review-track-b-execution-gate-r2-20261010.md",
  "workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010-R3.md",
  "workflow/handoffs/luna-0-independent-review-track-b-execution-gate-r3-20261010.md",
  "workflow/handoffs/luna-0-track-b-execution-gate-r3-manifest-20261010.json",
  "experiments/luna64/luna64-track-b-protocol-r3.json",
  "experiments/luna64/luna64-track-b-protocol-r3.schema.json",
  "experiments/luna64/luna64-track-b-golden-r3.json",
  "experiments/luna64/luna64-track-b-consistency-r3.json",
  "experiments/luna64/validate-track-b-gate-r3.mjs",
  "workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010-R4.md",
  "experiments/luna64/luna64-track-b-protocol-r4.json",
  "experiments/luna64/luna64-track-b-protocol-r4.schema.json",
  "experiments/luna64/luna64-track-b-golden-r4.json",
  "experiments/luna64/generate-track-b-gate-r4-schema.mjs",
  "experiments/luna64/validate-track-b-gate-r4.mjs",
  "experiments/luna64/test-track-b-gate-r4.mjs"
];

function git(...args) {
  const result = spawnSync("git", args, { cwd: root, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`git ${args.join(" ")} failed: ${result.stderr.trim()}`);
  return result.stdout.trim();
}

const entries = [];
for (const relativePath of paths) {
  const bytes = await readFile(path.join(root, relativePath));
  const blobOid = git("hash-object", "--", relativePath);
  const committed = spawnSync("git", ["cat-file", "-e", `HEAD:${relativePath}`], { cwd: root, encoding: "utf8" }).status === 0;
  const status = git("status", "--short", "--", relativePath) || "clean";
  entries.push({
    path: relativePath,
    raw_sha256: createHash("sha256").update(bytes).digest("hex").toUpperCase(),
    git_blob_oid: blobOid,
    present_in_head: committed,
    worktree_status: status
  });
}

const inventory = {
  inventory_schema: "LUNA64-TRACK-B-R4-INPUT-INVENTORY",
  gate_id: "L64-TB-GATE-20261010-R4",
  source_baseline: git("rev-parse", "HEAD"),
  source_branch: git("branch", "--show-current"),
  worktree_clean: git("status", "--porcelain") === "",
  immutable_freeze: false,
  reason: "Working-tree inputs include modified or untracked governing files; hashes identify current bytes only and do not establish an approved committed freeze.",
  entries
};
await writeFile(outputPath, `${JSON.stringify(inventory, null, 2)}\n`, "utf8");
console.log(`Wrote ${path.relative(root, outputPath)} with ${entries.length} exact-byte entries`);
