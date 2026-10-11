import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { classifyOutcome, validateText } from "./validate-track-b-gate-r4.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const protocolPath = path.join(root, "experiments/luna64/luna64-track-b-protocol-r4.json");
const schemaPath = path.join(root, "experiments/luna64/luna64-track-b-protocol-r4.schema.json");
const goldenPath = path.join(root, "experiments/luna64/luna64-track-b-golden-r4.json");
const validatorPath = path.join(root, "experiments/luna64/validate-track-b-gate-r4.mjs");
const protocolText = await readFile(protocolPath, "utf8");
const schemaText = await readFile(schemaPath, "utf8");
const golden = JSON.parse(await readFile(goldenPath, "utf8"));
const tempDir = await mkdtemp(path.join(os.tmpdir(), "luna64-r4-validator-"));

try {
  const protocol = validateText(protocolText, schemaText);
  assert.equal(protocol.gate_id, golden.gate_id);
  const delaySchedule = protocol.reward_lifecycle.delay_ticks;
  assert.deepEqual(
    Array.from({ length: 12 }, (_, ordinal) => delaySchedule[ordinal % delaySchedule.length]),
    [0, 1000000, 8000000, 9000000, 15000000, 16000000, 0, 1000000, 8000000, 9000000, 15000000, 16000000]
  );
  assert.match(protocol.reward_lifecycle.delay_assignment, /EVAL emits no correctness reward/);

  for (const fixture of golden.math.generator) {
    const key = `L64-R4.3|${fixture.seed}|${fixture.split}|${fixture.block}|${fixture.draw_name}|${fixture.counter}`;
    const digest = createHash("sha256").update(key, "utf8").digest("hex");
    const index = Number(BigInt(`0x${digest}`) % 3n);
    const support = ["-0.0625", "0", "0.0625"];
    assert.equal(digest, fixture.digest);
    assert.equal(index, fixture.support_index);
    assert.equal(support[index], fixture.expected_value);
  }

  for (const fixture of golden.math.temporal_disruption) {
    const expectedDecoderGap = fixture.block_index % 2 === 1
      ? 10000000 - fixture.physical_gap_ticks
      : fixture.physical_gap_ticks;
    assert.equal(expectedDecoderGap, fixture.expected_decoder_gap_ticks);
    assert.equal(fixture.physical_gap_ticks, fixture.expected_physical_gap_ticks);
  }
  for (const fixture of golden.math.attribution_specificity) {
    const denominator = fixture.event_credit_masses.reduce((sum, mass) => sum + mass, 0);
    if (fixture.expected_inconclusive) {
      assert.equal(denominator, 0);
      continue;
    }
    const numerator = fixture.event_credit_masses.reduce((sum, mass, index) =>
      sum + (fixture.event_logit_changes[index] > 0.000001 ? mass : 0), 0);
    assert.ok(Math.abs(denominator - fixture.expected_denominator) <= 1e-15);
    assert.ok(Math.abs(numerator / denominator - fixture.expected_score) <= 1e-15);
  }
  for (const item of golden.math.eligibility.kernel_values) {
    const actual = item.age_tu > 8 ? 0 : Math.exp(-item.age_tu / 2);
    assert.ok(Math.abs(actual - item.expected) <= 1e-15, `eligibility kernel at age ${item.age_tu}`);
  }
  for (const item of golden.math.eligibility.equal_strength_distinct_timing.events) {
    const actual = Math.exp(-item.age_tu / 2) * item.local_support_g;
    const expected = golden.math.eligibility.equal_strength_distinct_timing.expected_contribution_weights[
      golden.math.eligibility.equal_strength_distinct_timing.events.indexOf(item)
    ];
    assert.ok(Math.abs(actual - expected) <= 1e-15, `equal-strength temporal credit ${item.id}`);
  }
  for (const item of golden.math.eligibility.equal_timing_distinct_contribution.events) {
    const actual = Math.exp(-item.age_tu / 2) * item.local_support_g;
    const expected = golden.math.eligibility.equal_timing_distinct_contribution.expected_contribution_weights[
      golden.math.eligibility.equal_timing_distinct_contribution.events.indexOf(item)
    ];
    assert.ok(Math.abs(actual - expected) <= 1e-15, `equal-time contribution credit ${item.id}`);
  }
  assert.deepEqual(
    golden.math.eligibility.nearby_distractor_vs_distant_informative.events.map(
      event => Math.exp(-event.age_tu / 2) * event.local_support_g
    ),
    golden.math.eligibility.nearby_distractor_vs_distant_informative.expected_absolute_weights
  );
  assert.equal(golden.math.eligibility.zero_reward.reward * golden.math.eligibility.zero_reward.eligibility[0], 0);
  assert.equal(
    golden.math.eligibility.duplicate_reward.first_delivery_id,
    golden.math.eligibility.duplicate_reward.duplicate_delivery_id
  );

  const pcn = golden.math.pcn_multievent;
  let z = pcn.initial_state.z;
  let previousTick = pcn.initial_state.tick;
  const weights = pcn.readout.w;
  const V = Array.from({ length: 8 }, (_, i) =>
    Array.from({ length: 4 }, (_, j) => i === j ? 0.25 : i === j + 4 ? 0.125 : 0));
  const c = Array(8).fill(0);
  const channels = { A: 0, B: 1, N: 2, D: 3 };
  for (let index = 0; index < pcn.events.length; index++) {
    const event = pcn.events[index];
    const expected = pcn.expected_transitions[index];
    const dt = (event.tick - previousTick) / 1e6;
    const z0 = z.map(value => Math.exp(-dt / 2) * value);
    assert.ok(z0.every((value, j) => Math.abs(value - expected.z0[j]) < 1e-14), `PCN z0 ${event.id}`);
    let latent = [...z0];
    const x = Array(8).fill(0);
    x[channels[event.symbol]] = event.amplitude;
    for (let iteration = 0; iteration < 4; iteration++) {
      const prediction = V.map((row, i) => Math.tanh(row.reduce((sum, value, j) => sum + value * latent[j], c[i])));
      const q = x.map((value, i) => (value - prediction[i]) * (1 - prediction[i] ** 2));
      const gradient = latent.map((value, j) =>
        -V.reduce((sum, row, i) => sum + row[j] * q[i], 0) + (value - z0[j]));
      latent = latent.map((value, j) => Math.max(-1, Math.min(1, value - 0.0625 * gradient[j])));
    }
    const prediction = V.map((row, i) => Math.tanh(row.reduce((sum, value, j) => sum + value * latent[j], c[i])));
    const epsilon = x.map((value, i) => value - prediction[i]);
    const logit = weights.reduce((sum, value, j) => sum + value * latent[j], pcn.readout.b);
    assert.ok(latent.every((value, j) => Math.abs(value - expected.z_after[j]) < 1e-14), `PCN latent ${event.id}`);
    assert.ok(Math.abs(logit - expected.logit) < 1e-14, `PCN readout ${event.id}`);
    assert.ok(epsilon.every((value, j) => Math.abs(value - expected.epsilon_final[j]) < 1e-14), `PCN error ${event.id}`);
    const q = epsilon.map((value, i) => value * (1 - prediction[i] ** 2));
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 4; j++) V[i][j] = Math.max(-1, Math.min(1, V[i][j] + 0.001 * q[i] * latent[j]));
      c[i] = Math.max(-1, Math.min(1, c[i] + 0.001 * q[i]));
    }
    z = latent;
    previousTick = event.tick;
  }

  function bootstrap(seedEffects, comparisonId) {
    const replicates = 257;
    const means = [];
    for (let replicate = 0; replicate < replicates; replicate++) {
      let total = 0;
      for (let draw = 0; draw < seedEffects.length; draw++) {
        const key = `L64-R4.3-BOOT|4.3.0-draft|L64-TB-GATE-20261010-R4|640000|${comparisonId}|${replicate}|${draw}`;
        const digest = createHash("sha256").update(key, "utf8").digest("hex");
        const index = Number(BigInt(`0x${digest}`) % BigInt(seedEffects.length));
        total += seedEffects[index];
      }
      means.push(total / seedEffects.length);
    }
    means.sort((a, b) => a - b);
    return [
      means[Math.ceil(0.0125 * replicates) - 1],
      means[Math.ceil(0.9875 * replicates) - 1]
    ];
  }
  for (const fixture of [golden.statistics.positive, golden.statistics.zero_degenerate]) {
    assert.deepEqual(bootstrap(fixture.seed_effects, fixture.comparison_id), fixture.interval);
    assert.equal(fixture.seed_effects.reduce((sum, value) => sum + value, 0) / fixture.seed_effects.length, fixture.expected_mean);
  }
  for (const fixture of golden.statistics.verdict_cases) {
    assert.equal(classifyOutcome(fixture), fixture.expected, `statistical verdict ${fixture.id}`);
  }
  assert.equal(classifyOutcome({
    valid: true,
    accuracy: Infinity,
    mean_effect: 0.1,
    lower_ci_primary: 0.01,
    lower_ci_attribution: 0.01,
    specificity_n: 0.3,
    specificity_u: 0.2,
    specificity_r: 0.2,
    ops_ratio: 1,
    memory_ratio: 1,
    disruption_accuracy: 0.5
  }), "INCONCLUSIVE");

  let rejected = 0;
  const cliProtocolPath = path.join(tempDir, "negative-protocol.json");
  for (const fixture of golden.validator_negative_cases) {
    let text = fixture.raw_json;
    if (fixture.id === "excessive_nesting") text = `${"[".repeat(65)}0${"]".repeat(65)}`;
    if (fixture.mutation) {
      const mutated = JSON.parse(protocolText);
      const segments = fixture.mutation.path.split(".");
      const leaf = segments.pop();
      const parent = segments.reduce((value, segment) => Array.isArray(value) ? value[Number(segment)] : value[segment], mutated);
      if (fixture.mutation.op === "delete") delete parent[leaf];
      else parent[Array.isArray(parent) ? Number(leaf) : leaf] = fixture.mutation.value;
      text = JSON.stringify(mutated);
    }
    if (fixture.id === "duplicate_top_level" || fixture.id === "duplicate_nested") {
      assert.throws(() => validateText(text, schemaText), /duplicate object key/);
    } else if (fixture.id === "malformed_json") {
      assert.throws(() => validateText(text, schemaText), /invalid JSON grammar/);
    } else if (fixture.id === "trailing_data") {
      assert.throws(() => validateText(text, schemaText), /trailing data/);
    } else if (fixture.id === "excessive_nesting") {
      assert.throws(() => validateText(text, schemaText), /nesting depth over 64/);
    } else if (fixture.id === "nonfinite_number") {
      assert.throws(() => validateText(text, schemaText), /nonfinite JSON number/);
    } else {
      assert.throws(() => validateText(text, schemaText), /(?:additionalProperties|required property|type mismatch|safe integer|timebase|capacity|expiry|arm identity|protocol revision|const mismatch|pilot episode arithmetic|pilot replay scope|reward delay assignment)/);
    }
    await writeFile(cliProtocolPath, text);
    const cliNegative = spawnSync(process.execPath, [
      validatorPath, "--protocol", cliProtocolPath, "--schema", schemaPath
    ], { encoding: "utf8" });
    assert.equal(cliNegative.status, 1, `public CLI accepted ${fixture.id}`);
    assert.ok(cliNegative.stderr.length > 0, `public CLI emitted no diagnostic for ${fixture.id}`);
    rejected++;
  }

  await writeFile(cliProtocolPath, protocolText);
  const cliValid = spawnSync(process.execPath, [validatorPath, "--protocol", cliProtocolPath, "--schema", schemaPath, "--golden", goldenPath], { encoding: "utf8" });
  assert.equal(cliValid.status, 0, cliValid.stderr);
  assert.match(cliValid.stdout, /"status":"VALID"/);
  const duplicatePath = path.join(tempDir, "duplicate.json");
  await writeFile(duplicatePath, "{\"gate_id\":\"A\",\"gate_id\":\"B\"}");
  const cliInvalid = spawnSync(process.execPath, [validatorPath, "--protocol", duplicatePath, "--schema", schemaPath], { encoding: "utf8" });
  assert.equal(cliInvalid.status, 1);
  assert.match(cliInvalid.stderr, /duplicate object key/);
  const permissiveSchemaPath = path.join(tempDir, "permissive-schema.json");
  await writeFile(permissiveSchemaPath, "{}");
  const permissiveSchemaCli = spawnSync(process.execPath, [
    validatorPath, "--protocol", cliProtocolPath, "--schema", permissiveSchemaPath
  ], { encoding: "utf8" });
  assert.equal(permissiveSchemaCli.status, 1);
  assert.match(permissiveSchemaCli.stderr, /protocol-derived R4 schema/);
  const unsupportedSchema = JSON.parse(schemaText);
  unsupportedSchema["x-unknown-keyword"] = true;
  assert.throws(() => validateText(protocolText, JSON.stringify(unsupportedSchema)), /unknown schema keyword/);
  const prototypeKeyText = protocolText.replace(
    "\"gate_id\":",
    "\"__proto__\":{\"gate_id\":\"bypass\"},\"gate_id\":"
  );
  assert.throws(() => validateText(prototypeKeyText, schemaText), /additionalProperties/);

  console.log(JSON.stringify({
    status: "PASS",
    gate_id: protocol.gate_id,
    pcn_events_reproduced: pcn.events.length,
    generator_fixtures_reproduced: golden.math.generator.length,
    bootstrap_fixtures_reproduced: 2,
    verdict_fixtures: golden.statistics.verdict_cases.length,
    validator_negative_fixtures: rejected,
    public_cli_valid_and_invalid: true
  }, null, 2));
} finally {
  await rm(tempDir, { recursive: true, force: true });
}
