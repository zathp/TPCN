import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const files = {
  protocol: "experiments/luna64/luna64-track-b-protocol-r3.json",
  schema: "experiments/luna64/luna64-track-b-protocol-r3.schema.json",
  golden: "experiments/luna64/luna64-track-b-golden-r3.json",
  proposal: "workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010-R3.md",
  validator: "experiments/luna64/validate-track-b-gate-r3.mjs",
};
const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, files[name]), "utf8"));
const protocol = readJson("protocol");
const schema = readJson("schema");
const golden = readJson("golden");
const checks = [];

function assertCheck(id, condition, detail) {
  if (!condition) throw new Error(`${id}: ${detail}`);
  checks.push({ id, status: "PASS", detail });
}

function validate(schemaNode, value, at) {
  if (schemaNode.anyOf) {
    if (!schemaNode.anyOf.some((candidate) => {
      try {
        validate(candidate, value, at);
        return true;
      } catch {
        return false;
      }
    })) throw new Error(`${at}: no anyOf schema matched`);
    return;
  }
  const type = schemaNode.type;
  const matches = type === "object"
    ? value !== null && typeof value === "object" && !Array.isArray(value)
    : type === "array"
      ? Array.isArray(value)
      : type === "integer"
        ? Number.isInteger(value)
        : type === "number"
          ? typeof value === "number" && Number.isFinite(value)
          : type === "null"
            ? value === null
            : typeof value === type;
  if (!matches) throw new Error(`${at}: expected ${type}`);
  if (type === "object") {
    for (const key of schemaNode.required ?? []) {
      if (!Object.hasOwn(value, key)) throw new Error(`${at}.${key}: missing required key`);
    }
    for (const key of Object.keys(value)) {
      if (!Object.hasOwn(schemaNode.properties ?? {}, key) && schemaNode.additionalProperties === false) {
        throw new Error(`${at}.${key}: unexpected key`);
      }
    }
    for (const [key, childSchema] of Object.entries(schemaNode.properties ?? {})) {
      if (Object.hasOwn(value, key)) validate(childSchema, value[key], `${at}.${key}`);
    }
  }
  if (type === "array") {
    value.forEach((item, index) => validate(schemaNode.items, item, `${at}[${index}]`));
  }
}

validate(schema, protocol, "$");
assertCheck("strict-schema", true, "Protocol matches recursively strict required-key/type schema.");
const withUnknownKey = { ...protocol, unknown_probe: true };
let unknownKeyRejected = false;
try {
  validate(schema, withUnknownKey, "$");
} catch {
  unknownKeyRejected = true;
}
assertCheck("unknown-key-rejection", unknownKeyRejected, "Schema rejects a synthetic unknown root key.");
assertCheck(
  "artifact-identity",
  protocol.gate_id === golden.gate_id
    && protocol.provenance.golden_fixture_path === files.golden
    && golden.protocol_path === files.protocol
    && protocol.provenance.source_baseline === "73aaa50f97ceab322907875ae4dcf23e7541c3b5",
  "Gate ID, reciprocal artifact paths, and source baseline agree.",
);
assertCheck(
  "timebase-reciprocal",
  protocol.timebase.ticks_per_tu === 1_000_000
    && protocol.timebase.tu_per_tick_decimal === "0.000001",
  "1 TU is 1,000,000 ticks; 1 tick is 10^-6 TU.",
);
assertCheck(
  "arm-e-permutation-definition",
  protocol.rng.arm_e_permutation_bit.includes("split_code=0 for train, 1 for evaluation")
    && protocol.arm_e.permutation_source.includes("primary floor(cell/2) mod 2")
    && protocol.arm_e.permutation_source.includes("seed index and split_code"),
  "Arm E uses the deterministic balanced cell/seed/split formula, not a random draw.",
);

const training = { positive: 0, negative: 0, cells: Array(4).fill(0) };
for (let ordinal = 0; ordinal < 10_000; ordinal += 1) {
  const cell = ordinal % 16;
  const order = Math.floor(cell / 8);
  const gap = Math.floor(cell / 4) % 2;
  const target = Number(order === gap);
  training[target ? "positive" : "negative"] += 1;
  training.cells[order * 2 + gap] += 1;
}
assertCheck(
  "training-cell-balance",
  training.positive === 5_000 && training.negative === 5_000 && training.cells.every((n) => n === 2_500),
  JSON.stringify(training),
);

const evaluation = {
  positive: 0,
  negative: 0,
  cells: Array(4).fill(0),
  permutations: Array.from({ length: 4 }, () => [0, 0]),
};
for (let ordinal = 0; ordinal < 1_200; ordinal += 1) {
  const cell = ordinal % 16;
  const order = Math.floor(cell / 8);
  const gap = Math.floor(cell / 4) % 2;
  const target = Number(order === gap);
  const permutation = (Math.floor(cell / 2) % 2 + 1) % 2;
  evaluation[target ? "positive" : "negative"] += 1;
  evaluation.cells[order * 2 + gap] += 1;
  evaluation.permutations[order * 2 + gap][permutation] += 1;
}
assertCheck(
  "evaluation-primary-balance",
  evaluation.positive === 600
    && evaluation.negative === 600
    && evaluation.cells.every((n) => n === 300)
    && evaluation.permutations.every(([identity, swap]) => identity === 150 && swap === 150),
  JSON.stringify(evaluation),
);

const uncorrelated = Array.from({ length: 2 }, () =>
  Array.from({ length: 2 }, () =>
    Array.from({ length: 2 }, () => [0, 0])));
for (let ordinal = 0; ordinal < 400; ordinal += 1) {
  const cell = ordinal % 16;
  const order = Math.floor(cell / 8);
  const gap = Math.floor(cell / 4) % 2;
  const target = Math.floor(cell / 2) % 2;
  const permutation = (cell % 2 + 1) % 2;
  uncorrelated[order][gap][target][permutation] += 1;
}
assertCheck(
  "uncorrelated-control-balance",
  uncorrelated.flat(3).every((n) => n === 25),
  "Each order × gap × target × permutation cell occurs 25 times.",
);

const delayClassCounts = Array.from({ length: 7 }, () => [0, 0]);
for (let block = 0; block < 625; block += 1) {
  for (let cell = 0; cell < 16; cell += 1) {
    const target = Number(Math.floor(cell / 8) === Math.floor(cell / 4) % 2);
    delayClassCounts[block % 7][target] += 1;
  }
}
assertCheck(
  "reward-delay-class-balance",
  delayClassCounts.every(([negative, positive]) => negative === positive),
  JSON.stringify(delayClassCounts),
);

for (const [hashKey, drawName] of [
  ["amplitude_delta_sha256", "amplitude_delta"],
  ["nuisance_nu_sha256", "nuisance_nu"],
]) {
  const expectedHash = golden.fixtures[0].draws[hashKey];
  const expectedIndex = golden.fixtures[0].draws[`${drawName}_index`];
  const actualHash = crypto.createHash("sha256")
    .update(`L64-R3|6401|train|0|${drawName}|0`, "utf8")
    .digest("hex")
    .toUpperCase();
  const actualIndex = Number(BigInt(`0x${actualHash}`) % 3n);
  assertCheck(
    `golden-${drawName}-draw`,
    actualHash === expectedHash && actualIndex === expectedIndex,
    `SHA-256=${actualHash}; mapped index=${actualIndex}.`,
  );
}

const sequence = protocol.task.sequence;
const lifecycle = protocol.event_lifecycle;
assertCheck(
  "duration-and-cleanup",
  sequence.gap_values_ticks.every((gap) => gap + 2_000_000 <= sequence.maximum_logical_duration_ticks)
    && lifecycle.max_episode_physical_lifetime_ticks === sequence.maximum_logical_duration_ticks + 16_000_000 + 1,
  "Latest input is at or before 5,000,000 ticks; fixed cleanup is deadline+1 at 21,000,001.",
);
assertCheck(
  "eligibility-and-reward-boundaries",
  protocol.learning.eligibility.lifetime_ticks === 8_000_000
    && lifecycle.settlement_deadline === "activation_tick + 16000000 ticks inclusive"
    && lifecycle.expiry_tick === "settlement_deadline + 1 tick",
  "8-TU eligibility capture is distinct from the inclusive 16-TU reward deadline and +1-tick expiry.",
);
assertCheck(
  "overflow-fixture",
  protocol.task.controls.overflow_control.attempted_eligibility_entries === 9
    && protocol.task.controls.overflow_control.eligibility_capacity === 8
    && protocol.task.controls.overflow_control.injection.includes("not nine task input receptions")
    && golden.resource_boundary_fixtures.overflow_probe.expected === protocol.task.controls.overflow_control.expected,
  "Ledger-only overflow fixture agrees with golden data and does not exceed the four-input task limit.",
);
assertCheck(
  "operation-ceilings",
  protocol.resources.maximum_per_event_scalar_arithmetic_comparison_ops === 2_048
    && protocol.resources.maximum_per_event_tanh_calls === 48
    && protocol.resources.maximum_per_event_exp_calls === 2
    && protocol.resources.maximum_episode_scalar_arithmetic_comparison_ops === 4 * 2_048 + 256,
  "Per-event ceiling covers final sigmoid (at most two exp calls); episode ceiling is 8,448.",
);
assertCheck(
  "computational-unit-ceiling",
  protocol.resources.maximum_computational_units_any_arm === 32
    && Object.values(protocol.resources.computational_units_by_arm).every((units) => units <= 32)
    && JSON.stringify(Object.values(protocol.resources.computational_units_by_arm)) === JSON.stringify([1, 5, 9, 13, 13]),
  "Persistent model-unit counts are A/B/C/D/E = 1/5/9/13/13, within 32; parameters and bounded scratch are separate.",
);

const V = Array.from({ length: 8 }, (_, i) =>
  Array.from({ length: 4 }, (_, j) => (i === j ? 0.25 : i === j + 4 ? 0.125 : 0)));
const pcnFixture = golden.fixtures.find((fixture) => fixture.id === "pcn-one-event-inference-and-gradient");
let z = [0, 0, 0, 0];
const z0 = [0, 0, 0, 0];
const c = Array(8).fill(0);
const x = pcnFixture.input.x;
for (let iteration = 0; iteration < 4; iteration += 1) {
  const prediction = V.map((row, i) => Math.tanh(row.reduce((sum, value, j) => sum + value * z[j], c[i])));
  const q = x.map((value, i) => (value - prediction[i]) * (1 - prediction[i] ** 2));
  const gradient = z.map((value, j) =>
    -V.reduce((sum, row, i) => sum + row[j] * q[i], 0) + value - z0[j]);
  z = z.map((value, j) => Math.max(-1, Math.min(1, value - 0.0625 * gradient[j])));
}
const prediction = V.map((row, i) => Math.tanh(row.reduce((sum, value, j) => sum + value * z[j], c[i])));
const objective = 0.5 * x.reduce((sum, value, i) => sum + (value - prediction[i]) ** 2, 0)
  + 0.5 * z.reduce((sum, value, j) => sum + (value - z0[j]) ** 2, 0);
assertCheck(
  "pcn-one-event-golden",
  Math.abs(z[0] - pcnFixture.inference_latent_after_each_step[3][0]) < 1e-14
    && Math.abs(prediction[0] - pcnFixture.expected_prediction.xhat[0]) < 1e-14
    && Math.abs(objective - pcnFixture.expected_prediction.objective) < 1e-14,
  `final latent=${z[0]}; xhat[0]=${prediction[0]}; objective=${objective}.`,
);

const gradientFixture = golden.gradient_verification;
const { z: zInterior, z0: zReference, x: xInterior } = gradientFixture.interior_fixture;
function objectiveAt(latent, weights, bias) {
  const estimate = weights.map((row, i) =>
    Math.tanh(row.reduce((sum, value, j) => sum + value * latent[j], bias[i])));
  return 0.5 * xInterior.reduce((sum, value, i) => sum + (value - estimate[i]) ** 2, 0)
    + 0.5 * latent.reduce((sum, value, j) => sum + (value - zReference[j]) ** 2, 0);
}
const estimate = V.map((row, i) =>
  Math.tanh(row.reduce((sum, value, j) => sum + value * zInterior[j], c[i])));
const q = xInterior.map((value, i) => (value - estimate[i]) * (1 - estimate[i] ** 2));
const latentGradient = zInterior.map((value, j) =>
  -V.reduce((sum, row, i) => sum + row[j] * q[i], 0) + value - zReference[j]);
const gradientErrors = gradientFixture.step_sizes.map((step) => {
  let maximum = 0;
  for (let j = 0; j < 4; j += 1) {
    const plus = zInterior.slice();
    const minus = zInterior.slice();
    plus[j] += step;
    minus[j] -= step;
    maximum = Math.max(maximum, Math.abs(
      (objectiveAt(plus, V, c) - objectiveAt(minus, V, c)) / (2 * step) - latentGradient[j],
    ));
  }
  for (let i = 0; i < 8; i += 1) {
    for (let j = 0; j < 4; j += 1) {
      const plus = V.map((row) => row.slice());
      const minus = V.map((row) => row.slice());
      plus[i][j] += step;
      minus[i][j] -= step;
      maximum = Math.max(maximum, Math.abs(
        (objectiveAt(zInterior, plus, c) - objectiveAt(zInterior, minus, c)) / (2 * step)
          + q[i] * zInterior[j],
      ));
    }
  }
  for (let i = 0; i < 8; i += 1) {
    const plus = c.slice();
    const minus = c.slice();
    plus[i] += step;
    minus[i] -= step;
    maximum = Math.max(maximum, Math.abs(
      (objectiveAt(zInterior, V, plus) - objectiveAt(zInterior, V, minus)) / (2 * step) + q[i],
    ));
  }
  return maximum;
});
assertCheck(
  "pcn-gradient-finite-differences",
  gradientErrors.every((error, i) =>
    error <= gradientFixture.tolerance
      && Math.abs(error - gradientFixture.observed_max_absolute_errors[i]) < 1e-8),
  JSON.stringify(gradientErrors),
);

const positiveFixture = golden.fixtures[0];
assertCheck(
  "reward-order-and-event-cost",
  positiveFixture.reward.signed_reward === -1
    && positiveFixture.reward.delivery_ticks === positiveFixture.reward.origin_ticks
    && positiveFixture.event_cost_total === 4
    && positiveFixture.credit.reward_event_energy_charge === 0,
  "Prediction precedes zero-delay reward; four input receptions are charged once; reward delivery costs zero.",
);

const artifacts = {};
for (const [name, relativePath] of Object.entries(files)) {
  artifacts[relativePath] = crypto.createHash("sha256")
    .update(fs.readFileSync(path.join(root, relativePath)))
    .digest("hex")
    .toUpperCase();
}
const report = {
  report_id: "L64-TB-R3-CONSISTENCY-20261010",
  gate_id: protocol.gate_id,
  source_baseline: protocol.provenance.source_baseline,
  status: "PASS_LOCAL_GOVERNANCE_CONSISTENCY_ONLY",
  independent_review: "pending",
  owner_approval: "not_provided",
  execution_authorized: false,
  experiment_or_implementation_performed: false,
  checks,
  artifact_sha256: artifacts,
};
const reportText = `${JSON.stringify(report, null, 2)}\n`;
const reportPath = process.argv[2];
if (reportPath) fs.writeFileSync(path.resolve(root, reportPath), reportText, "utf8");
process.stdout.write(reportText);
