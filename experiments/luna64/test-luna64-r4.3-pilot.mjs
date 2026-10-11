import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import {
  Meter,
  applyRewardOnce,
  buildWorkload,
  createModel,
  digestDraw,
  inputCharge,
  makeEvents,
  parameterHash
} from "./run-luna64-r4.3-pilot.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const protocol = JSON.parse(readFileSync(path.join(HERE, "luna64-track-b-protocol-r4.json"), "utf8"));
const golden = JSON.parse(readFileSync(path.join(HERE, "luna64-track-b-golden-r4.json"), "utf8"));

assert.deepEqual(protocol.resources.pilot_seed_ids, [6401, 6402, 6403]);
assert.equal(protocol.resources.pilot_execution_passes, 2);
assert.equal(protocol.resources.maximum_total_episodes, 5184);

for (const fixture of golden.math.generator) {
  const split = fixture.split;
  const actual = digestDraw(fixture.seed, split, fixture.block, fixture.draw_name);
  assert.equal(actual.key, `L64-R4.3|${fixture.seed}|${split}|${fixture.block}|${fixture.draw_name}|0`);
  assert.equal(actual.digest, fixture.digest);
  assert.equal(actual.index, fixture.support_index);
  assert.equal(actual.value, Number(fixture.expected_value));
}

const stable = makeEvents(6401, "TRAIN", 8, 8, "N_NONLINEAR_LOCAL");
const disrupted = makeEvents(6401, "TRAIN", 8, 8, "X_TEMPORAL_DISRUPTION");
assert.equal(stable.records.length, 4);
assert.equal(disrupted.records.length, 4);
assert.equal(stable.target, disrupted.target);
for (let i = 0; i < 4; i++) {
  assert.equal(stable.records[i].event_id, disrupted.records[i].event_id);
  assert.equal(stable.records[i].physical_timestamp_ticks, disrupted.records[i].physical_timestamp_ticks);
  assert.equal(stable.records[i].channel_index, disrupted.records[i].channel_index);
  assert.equal(stable.records[i].amplitude, disrupted.records[i].amplitude);
}
assert.notEqual(stable.records[1].decoder_timestamp_ticks, disrupted.records[1].decoder_timestamp_ticks);
assert.equal(disrupted.records[2].decoder_timestamp_ticks, disrupted.records[1].decoder_timestamp_ticks + 1000000);

const workload = buildWorkload(protocol);
const rows = workload.toString("utf8").trimEnd().split("\n").map(line => JSON.parse(line));
assert.equal(rows.length, 2592);
assert.equal(rows[0].seed, 6401);
assert.equal(rows[0].arm_id, protocol.arms[0].id);
assert.equal(rows[0].split, "TRAIN");
assert.equal(rows[96].split, "EVAL");
for (const row of rows.filter(item => item.split === "EVAL")) {
  assert.equal(Object.hasOwn(row, "train_oracle_target"), false);
  assert.equal(Object.hasOwn(row, "reward_delay_ticks"), false);
}
assert.equal(rows.filter(item => item.split === "TRAIN").length, 1728);
assert.equal(rows.filter(item => item.split === "EVAL").length, 864);
const allowedOutputFields = [
  "global_ordinal", "seed", "split", "arm_id", "input_event_records", "prediction",
  "trained_parameter_sha256", "counted_scalar_ops", "tanh_calls", "exp_calls",
  "eligibility_bytes_peak", "model_bytes_peak"
];
assert.deepEqual(allowedOutputFields, protocol.resources.replay_digest.episode_record_fields_in_order);

const global = {
  scalarArithmeticComparisonOps: 0,
  expCalls: 0,
  tanhCalls: 0,
  inputEventCostCharges: 0,
  inputReceptions: 1,
  maximumEventOps: 0,
  rewardRecordsSettled: 0,
  duplicateRewards: 0
};
const meter = new Meter(global);
inputCharge(meter, global);
assert.equal(meter.inputCharges, 1);
assert.equal(global.inputEventCostCharges, 1);
assert.equal(global.inputReceptions, 1);

const eventCapGlobal = { scalarArithmeticComparisonOps: 0, expCalls: 0, tanhCalls: 0, maximumEventOps: 0 };
const eventCapMeter = new Meter(eventCapGlobal);
eventCapMeter.beginEvent();
assert.throws(() => {
  for (let i = 0; i < 2049; i++) eventCapMeter.add(0, 0);
}, /per-decoder-event scalar operation cap exceeded/);

const episodeCapGlobal = { scalarArithmeticComparisonOps: 0, expCalls: 0, tanhCalls: 0, maximumEventOps: 0 };
const episodeCapMeter = new Meter(episodeCapGlobal);
assert.throws(() => {
  for (let i = 0; i < 257; i++) episodeCapMeter.add(0, 0);
}, /episode-level scalar operation cap exceeded/);

const rewardGlobal = {
  scalarArithmeticComparisonOps: 0,
  expCalls: 0,
  tanhCalls: 0,
  maximumEventOps: 0,
  rewardRecordsSettled: 0,
  duplicateRewards: 0
};
const rewardMeter = new Meter(rewardGlobal);
const model = createModel("N_NONLINEAR_LOCAL", rewardMeter);
model.credit = { vector: [1, -1, 0.5, 0.25, -0.5] };
const beforeReward = parameterHash(model);
const seen = new Set();
const delivery = { id: "stable-test-reward-id", reward: 1 };
assert.equal(applyRewardOnce(model, delivery, seen, rewardMeter), true);
const afterFirst = parameterHash(model);
assert.notEqual(afterFirst, beforeReward);
assert.equal(applyRewardOnce(model, delivery, seen, rewardMeter), false);
assert.equal(parameterHash(model), afterFirst);
assert.equal(rewardMeter.rewardRecordsSettled, 1);
assert.equal(rewardMeter.duplicateRewards, 1);
assert.equal(rewardGlobal.duplicateRewards, 1);

const freshA = createModel("N_NONLINEAR_LOCAL");
const freshB = createModel("N_NONLINEAR_LOCAL");
assert.equal(parameterHash(freshA), parameterHash(freshB), "reset must restore initial model parameters");
assert.equal(parameterHash(createModel("A_COST_ONLY")), parameterHash(createModel("A_COST_ONLY")));

console.log(JSON.stringify({
  status: "PASS",
  generator_goldens: golden.math.generator.length,
  workload_records_checked: rows.length,
  eval_truth_leakage: false,
  temporal_disruption_mapping: "PASS",
  input_charge_identity: "PASS",
  duplicate_reward_idempotence: "PASS",
  operation_caps: "PASS",
  reset_parameter_identity: "PASS"
}, null, 2));
