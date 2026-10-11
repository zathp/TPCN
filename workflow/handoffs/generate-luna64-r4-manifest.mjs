import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const outputPath = path.join(root, "workflow/handoffs/luna-0-track-b-execution-gate-r4-manifest-20261010.json");
const paths = [
  "workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010-R4.md",
  "experiments/luna64/luna64-track-b-protocol-r4.json",
  "experiments/luna64/luna64-track-b-protocol-r4.schema.json",
  "experiments/luna64/luna64-track-b-golden-r4.json",
  "experiments/luna64/generate-track-b-gate-r4-schema.mjs",
  "experiments/luna64/validate-track-b-gate-r4.mjs",
  "experiments/luna64/test-track-b-gate-r4.mjs",
  "workflow/handoffs/generate-luna64-r4-input-inventory.mjs",
  "workflow/handoffs/generate-luna64-r4-manifest.mjs",
  "workflow/handoffs/luna-0-track-b-execution-gate-r4-input-inventory-20261010.json"
];

function git(...args) {
  const result = spawnSync("git", args, { cwd: root, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`git ${args.join(" ")} failed: ${result.stderr.trim()}`);
  return result.stdout.trim();
}

const files = [];
for (const relativePath of paths) {
  const bytes = await readFile(path.join(root, relativePath));
  files.push({
    path: relativePath,
    sha256: createHash("sha256").update(bytes).digest("hex").toUpperCase(),
    git_blob_oid: git("hash-object", "--", relativePath),
    present_in_head: spawnSync("git", ["cat-file", "-e", `HEAD:${relativePath}`], { cwd: root }).status === 0,
    worktree_status: git("status", "--short", "--", relativePath) || "clean"
  });
}
const manifest = {
  manifest_schema: "LUNA64-TRACK-B-R4-MANIFEST",
  gate_id: "L64-TB-GATE-20261010-R4",
  source_baseline: git("rev-parse", "HEAD"),
  source_branch: git("branch", "--show-current"),
  package_freeze: false,
  review_status: "pending",
  owner_approval: "not_provided",
  pilot_authorized: false,
  execution_performed: false,
  files
};
await writeFile(outputPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
console.log(`Wrote ${path.relative(root, outputPath)} with ${files.length} exact-byte package entries`);
