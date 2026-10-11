import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { appendFileSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { performance } from "node:perf_hooks";
import { once } from "node:events";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const OUT = path.join(HERE, "pilot-20261010");
const PROTOCOL_PATH = path.join(HERE, "luna64-track-b-protocol-r4.json");
const SCHEMA_PATH = path.join(HERE, "luna64-track-b-protocol-r4.schema.json");
const GOLDEN_PATH = path.join(HERE, "luna64-track-b-golden-r4.json");
const AUTH_PATH = path.join(ROOT, "workflow/handoffs/luna-0-authorization-luna64-r4.3-bounded-pilot-20261010.md");
const FREEZE = "64a214e310de3b982b90a8ad215598bc1e9f8b1c";
const BASELINE = "bc338a48bc05f7e15c4cb84636a979294b88e093";
const BRANCH = "experiment/luna64-track-b-r4.3-pilot-20261010";
const SEEDS = [6401, 6402, 6403];
const DELTA_NU_SUPPORT = [-0.0625, 0, 0.0625];
const DELAY_TICKS = [0, 1000000, 8000000, 9000000, 15000000, 16000000];
const HORIZON_TICKS = 8000000;
const TAU_TICKS = 2000000;
const REWARD_DEADLINE_TICKS = 16000000;
const MAX_EPISODES = 5184;
const MAX_RECEPTIONS = 20736;
const MAX_PCN_EPISODES = 4320;
const MAX_PCN_RECEPTIONS = 17280;
const MAX_TOTAL_OPS = 36716544;
const MAX_OPS_PER_EVENT = 2048;
const MAX_EPISODE_OVERHEAD_OPS = 256;
const MAX_CPU_SECONDS = 900;
const MAX_WALL_SECONDS = 1200;
const MAX_RSS_BYTES = 536870912;
const MAX_ARTIFACT_BYTES = 26214400;
const MAX_HISTORY = 4;
const MAX_ELIGIBILITY = 8;
const FIXED_HEAD_HASH = hash(Buffer.from("[]", "utf8"));
let activeRun = null;

function hash(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function shaFile(file) {
  return hash(readFileSync(file));
}

function gitText(...args) {
  const result = spawnSync("git", args, { cwd: ROOT, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`git ${args.join(" ")} failed: ${result.stderr}`);
  return result.stdout.trim();
}

function assertExecutionIdentity() {
  const ancestry = spawnSync("git", ["merge-base", "--is-ancestor", BASELINE, "HEAD"], {
    cwd: ROOT,
    encoding: "utf8"
  });
  assert.equal(ancestry.status, 0, "authorized baseline is not an ancestor of the execution revision");
  assert.equal(gitText("branch", "--show-current"), BRANCH, "execution branch changed");
  assert.ok(os.platform() === "win32", "R4.3 pilot is authorized for the verified Windows worktree only");
  assert.ok(os.arch() === "x64", `unexpected process architecture ${os.arch()}`);
}

class Meter {
  constructor(global) {
    this.global = global;
    this.episodeOps = 0;
    this.eventOps = 0;
    this.eventOpsSum = 0;
    this.eventActive = false;
    this.eventOpsMax = 0;
    this.tanhCalls = 0;
    this.expCalls = 0;
    this.parameterReads = 0;
    this.parameterWrites = 0;
    this.stateReads = 0;
    this.stateWrites = 0;
    this.rewardRecordsCreated = 0;
    this.rewardRecordsSettled = 0;
    this.duplicateRewards = 0;
    this.inputCharges = 0;
    this.eligibilityBytesPeak = 0;
    this.modelBytesPeak = 0;
  }

  op(count = 1) {
    if (this.eventActive) {
      this.eventOps += count;
      this.eventOpsMax = Math.max(this.eventOpsMax, this.eventOps);
      if (this.eventOps > MAX_OPS_PER_EVENT) throw new Error("ABORT: per-decoder-event scalar operation cap exceeded");
    } else {
      this.episodeOps += count;
      if (this.episodeOps > MAX_EPISODE_OVERHEAD_OPS) throw new Error("ABORT: episode-level scalar operation cap exceeded");
    }
    this.global.scalarArithmeticComparisonOps += count;
    if (this.global.scalarArithmeticComparisonOps > MAX_TOTAL_OPS) {
      throw new Error("ABORT: aggregate scalar operation cap exceeded");
    }
  }

  add(a, b) { this.op(); return a + b; }
  sub(a, b) { this.op(); return a - b; }
  mul(a, b) { this.op(); return a * b; }
  div(a, b) { this.op(); return a / b; }
  lt(a, b) { this.op(); return a < b; }
  gt(a, b) { this.op(); return a > b; }
  lte(a, b) { this.op(); return a <= b; }
  gte(a, b) { this.op(); return a >= b; }
  eq(a, b) { this.op(); return a === b; }

  clip(value, lo, hi) {
    if (this.lt(value, lo)) return lo;
    if (this.gt(value, hi)) return hi;
    return value;
  }

  beginEvent() {
    if (this.eventActive) throw new Error("nested decoder-event operation counter");
    this.eventActive = true;
    this.eventOps = 0;
  }

  endEvent() {
    if (!this.eventActive) throw new Error("decoder-event operation counter was not active");
    this.eventActive = false;
    this.eventOpsSum += this.eventOps;
    this.eventOpsMax = Math.max(this.eventOpsMax, this.eventOps);
    this.global.maximumEventOps = Math.max(this.global.maximumEventOps, this.eventOps);
  }

  exp(x) {
    this.expCalls++;
    this.global.expCalls++;
    return Math.exp(x);
  }

  tanh(x) {
    this.tanhCalls++;
    this.global.tanhCalls++;
    return Math.tanh(x);
  }

  snapshot() {
    return {
      counted_scalar_ops: this.episodeOps + this.eventOpsSum,
      tanh_calls: this.tanhCalls,
      exp_calls: this.expCalls,
      parameter_reads: this.parameterReads,
      parameter_writes: this.parameterWrites,
      state_reads: this.stateReads,
      state_writes: this.stateWrites,
      reward_records_created: this.rewardRecordsCreated,
      reward_records_settled: this.rewardRecordsSettled,
      duplicate_rewards: this.duplicateRewards,
      input_event_cost_charges: this.inputCharges,
      eligibility_bytes_peak: this.eligibilityBytesPeak,
      model_bytes_peak: this.modelBytesPeak,
      maximum_counted_ops_single_event: this.eventOpsMax
    };
  }
}

function digestDraw(seed, split, block, drawName) {
  const key = `L64-R4.3|${seed}|${split}|${block}|${drawName}|0`;
  const digest = createHash("sha256").update(key, "utf8").digest();
  const index = Number(BigInt(`0x${digest.toString("hex")}`) % 3n);
  return { key, digest: digest.toString("hex"), index, value: DELTA_NU_SUPPORT[index] };
}

function makeEvents(seed, split, globalOrdinal, splitLocalOrdinal, armId) {
  const block = Math.floor(splitLocalOrdinal / 8);
  const delta = digestDraw(seed, split, block, "DELTA").value;
  const nu = digestDraw(seed, split, block, "NU").value;
  const cell = splitLocalOrdinal % 8;
  const orderBit = Math.floor(cell / 4);
  const gapBit = Math.floor(cell / 2) % 2;
  const target = orderBit === gapBit ? 1 : 0;
  const gapTicks = gapBit === 0 ? 4000000 : 6000000;
  const first = orderBit === 0 ? "A" : "B";
  const second = orderBit === 0 ? "B" : "A";
  const amplitude = symbol => {
    if (symbol === "A") return 1 + delta;
    if (symbol === "B") return 1 - delta;
    if (symbol === "N") return 0.25 + nu;
    return 0.25 - nu;
  };
  const eventSymbols = [
    { symbol: first, physical: 0, decoder: 0 },
    { symbol: second, physical: gapTicks, decoder: gapTicks },
    { symbol: "N", physical: gapTicks + 1000000, decoder: gapTicks + 1000000 },
    { symbol: "D", physical: gapTicks + 2000000, decoder: gapTicks + 2000000 }
  ];
  if (armId === "X_TEMPORAL_DISRUPTION" && block % 2 === 1) {
    const decoderGap = 10000000 - gapTicks;
    eventSymbols[1].decoder = decoderGap;
    eventSymbols[2].decoder = decoderGap + 1000000;
    eventSymbols[3].decoder = decoderGap + 2000000;
  }
  return {
    target,
    records: eventSymbols.map((event, index) => ({
      event_id: `L64-R4.3/${seed}/${split}/${globalOrdinal}/${event.symbol}/${index}`,
      physical_timestamp_ticks: event.physical,
      decoder_timestamp_ticks: event.decoder,
      channel_index: ["A", "B", "N", "D"].indexOf(event.symbol),
      amplitude: amplitude(event.symbol)
    }))
  };
}

function buildWorkload(protocol) {
  assert.deepEqual(protocol.resources.pilot_seed_ids, SEEDS);
  const lines = [];
  for (const seed of SEEDS) {
    for (const arm of protocol.arms) {
      for (const split of ["TRAIN", "EVAL"]) {
        const n = split === "TRAIN" ? protocol.resources.training_episodes_per_arm_seed :
          protocol.resources.evaluation_workload_episodes_per_arm_seed;
        for (let splitLocalOrdinal = 0; splitLocalOrdinal < n; splitLocalOrdinal++) {
          const globalOrdinal = split === "TRAIN" ? splitLocalOrdinal : 96 + splitLocalOrdinal;
          const { records, target } = makeEvents(seed, split, globalOrdinal, splitLocalOrdinal, arm.id);
          const row = {
            global_ordinal: globalOrdinal,
            seed,
            split,
            split_local_ordinal: splitLocalOrdinal,
            arm_id: arm.id,
            input_event_records: records
          };
          if (split === "TRAIN") {
            row.train_oracle_target = target;
            row.reward_delay_ticks = DELAY_TICKS[splitLocalOrdinal % DELAY_TICKS.length];
          }
          lines.push(`${JSON.stringify(row)}\n`);
        }
      }
    }
  }
  assert.equal(lines.length, 2592);
  return Buffer.from(lines.join(""), "utf8");
}

function initialParameters(armId) {
  if (armId === "A_COST_ONLY") return null;
  const V = Array.from({ length: 8 }, (_, i) =>
    Array.from({ length: 4 }, (_, j) => i === j ? 0.25 : i === j + 4 ? 0.125 : 0));
  return {
    V,
    c: Array(8).fill(0),
    w: [0.01, -0.02, 0.015, 0.005],
    b: 0
  };
}

function createModel(armId, meter = null) {
  const params = initialParameters(armId);
  return {
    armId,
    params,
    z: [0, 0, 0, 0],
    previousDecoderTick: 0,
    history: [],
    credit: null,
    learningEnabled: true,
    meter
  };
}

function parameterHash(model) {
  if (!model.params) return FIXED_HEAD_HASH;
  const flattened = [
    ...model.params.V.flat(),
    ...model.params.c,
    ...model.params.w,
    model.params.b
  ];
  return hash(Buffer.from(JSON.stringify(flattened), "utf8"));
}

function modelByteSize(model) {
  return model.params ? 45 * 8 + 4 * 8 + 8 : 0;
}

function logit(model, z, meter) {
  let total = 0;
  for (let j = 0; j < 4; j++) {
    meter.parameterReads++;
    meter.stateReads++;
    total = meter.add(total, meter.mul(model.params.w[j], z[j]));
  }
  meter.parameterReads++;
  return meter.add(total, model.params.b);
}

function forward(model, z, nonlinear, meter) {
  const output = Array(8);
  for (let i = 0; i < 8; i++) {
    let u = 0;
    for (let j = 0; j < 4; j++) {
      meter.parameterReads++;
      meter.stateReads++;
      u = meter.add(u, meter.mul(model.params.V[i][j], z[j]));
    }
    meter.parameterReads++;
    u = meter.add(u, model.params.c[i]);
    output[i] = nonlinear ? meter.tanh(u) : u;
  }
  return output;
}

function decoderInput(record) {
  const x = Array(8).fill(0);
  x[record.channel_index] = record.amplitude;
  return x;
}

function applyPcnEvent(model, event, meter) {
  const p = model.params;
  const nonlinear = model.armId !== "L_LINEAR_TEMPORAL";
  const before = logit(model, model.z, meter);
  const dt = meter.sub(event.decoder_timestamp_ticks, model.previousDecoderTick);
  if (meter.lt(dt, 0)) throw new Error("ABORT: nonmonotone decoder timestamp");
  const decay = meter.exp(-meter.div(meter.div(dt, 1000000), 2));
  const z0 = model.z.map(value => meter.clip(meter.mul(decay, value), -1, 1));
  const x = decoderInput(event);
  let z = [...z0];
  for (let iteration = 0; iteration < 4; iteration++) {
    const prediction = forward(model, z, nonlinear, meter);
    const epsilon = x.map((value, i) => meter.sub(value, prediction[i]));
    const q = epsilon.map((value, i) => nonlinear ?
      meter.mul(value, meter.sub(1, meter.mul(prediction[i], prediction[i]))) : value);
    const gradient = Array(4);
    for (let j = 0; j < 4; j++) {
      let transposeProduct = 0;
      for (let i = 0; i < 8; i++) {
        meter.parameterReads++;
        transposeProduct = meter.add(transposeProduct, meter.mul(p.V[i][j], q[i]));
      }
      const priorDifference = meter.sub(z[j], z0[j]);
      gradient[j] = meter.add(-transposeProduct, priorDifference);
    }
    z = z.map((value, j) => meter.clip(
      meter.sub(value, meter.mul(0.0625, gradient[j])), -1, 1
    ));
  }
  const prediction = forward(model, z, nonlinear, meter);
  const epsilon = x.map((value, i) => meter.sub(value, prediction[i]));
  const q = epsilon.map((value, i) => nonlinear ?
    meter.mul(value, meter.sub(1, meter.mul(prediction[i], prediction[i]))) : value);
  if (model.learningEnabled) {
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 4; j++) {
        const gradient = -meter.mul(q[i], z[j]);
        meter.parameterReads++;
        p.V[i][j] = meter.clip(meter.sub(p.V[i][j], meter.mul(0.001, gradient)), -1, 1);
        meter.parameterWrites++;
      }
      const gradientC = -q[i];
      meter.parameterReads++;
      p.c[i] = meter.clip(meter.sub(p.c[i], meter.mul(0.001, gradientC)), -1, 1);
      meter.parameterWrites++;
    }
  }
  const after = logit(model, z, meter);
  model.z = z;
  model.previousDecoderTick = event.decoder_timestamp_ticks;
  model.meter.stateWrites += 5;
  return { ell: after, ellBefore: before, z: [...z] };
}

function captureEligibility(model, prediction, activationTick, meter, rewardId) {
  if (model.history.length > MAX_ELIGIBILITY) throw new Error("ABORT: eligibility capacity overflow");
  const sign = meter.eq(prediction, 1) ? 1 : -1;
  const eligible = [];
  for (const event of model.history) {
    const age = meter.sub(activationTick, event.physical_timestamp_ticks);
    if (meter.lt(age, 0)) throw new Error("ABORT: event is later than activation");
    if (meter.lte(age, HORIZON_TICKS)) {
      const kernel = meter.exp(-meter.div(age, TAU_TICKS));
      const deltaLogit = meter.sub(event.ell, event.ellBefore);
      const g = meter.clip(meter.mul(sign, deltaLogit), -1, 1);
      eligible.push({ event, age, kernel, g });
    }
  }
  if (eligible.length > MAX_ELIGIBILITY) throw new Error("ABORT: eligibility record cap exceeded");
  let kernelSum = 0;
  for (const item of eligible) kernelSum = meter.add(kernelSum, item.kernel);
  const vector = Array(5).fill(0);
  for (const item of eligible) {
    let q;
    if (model.armId === "U_UNIFORM_PC") q = meter.div(1, eligible.length || 1);
    else if (model.armId === "R_RECENCY_PC") {
      const denominator = meter.gt(kernelSum, 1) ? kernelSum : 1;
      q = meter.div(item.kernel, denominator);
    }
    else q = meter.mul(item.kernel, item.g);
    const features = [...item.event.z, 1];
    for (let j = 0; j < 5; j++) {
      const contribution = meter.mul(q, meter.mul(sign, features[j]));
      vector[j] = meter.add(vector[j], contribution);
    }
  }
  for (let j = 0; j < vector.length; j++) vector[j] = meter.clip(vector[j], -4, 4);
  if (model.params) {
    model.credit = {
      rewardId,
      vector,
      readoutSnapshot: [...model.params.w, model.params.b],
      capturedAtTick: activationTick
    };
    meter.parameterReads += 5;
    const bytes = eligible.reduce((sum, item) =>
      sum + 144 + Buffer.byteLength(item.event.event_id, "utf8"), 0) +
      40 + Buffer.byteLength(rewardId, "utf8");
    meter.eligibilityBytesPeak = Math.max(meter.eligibilityBytesPeak, bytes);
  }
}

function inputCharge(meter, global) {
  meter.inputCharges++;
  global.inputEventCostCharges++;
  if (global.inputReceptions > MAX_RECEPTIONS) throw new Error("ABORT: input reception cap exceeded");
}

function applyRewardOnce(model, record, settledIds, meter) {
  if (settledIds.has(record.id)) {
    meter.duplicateRewards++;
    meter.global.duplicateRewards++;
    return false;
  }
  settledIds.add(record.id);
  meter.rewardRecordsSettled++;
  meter.global.rewardRecordsSettled++;
  if (model.params && model.credit) {
    const reward = record.reward;
    for (let j = 0; j < 5; j++) {
      const before = j < 4 ? model.params.w[j] : model.params.b;
      const delta = meter.mul(0.01, meter.mul(reward, model.credit.vector[j]));
      const updated = meter.clip(meter.add(before, delta), -1, 1);
      if (j < 4) model.params.w[j] = updated;
      else model.params.b = updated;
      meter.parameterWrites++;
      meter.parameterReads++;
    }
  }
  return true;
}

function evaluateReadout(model, z, meter) {
  if (!model.params) return 0;
  const ell = logit(model, z, meter);
  const probability = meter.div(1, meter.add(1, meter.exp(-ell)));
  return meter.gt(probability, 0.5) ? 1 : 0;
}

function currentRss() {
  return process.memoryUsage.rss();
}

function checkResources(global, startedAt, cpuStart, artifactBytes) {
  const wall = (performance.now() - startedAt) / 1000;
  const usage = process.cpuUsage(cpuStart);
  const cpu = (usage.user + usage.system) / 1e6;
  global.peakWorkingSetBytes = Math.max(global.peakWorkingSetBytes, currentRss());
  if (cpu > MAX_CPU_SECONDS) throw new Error("ABORT: CPU time cap exceeded");
  if (wall > MAX_WALL_SECONDS) throw new Error("ABORT: wall time cap exceeded");
  if (global.peakWorkingSetBytes > MAX_RSS_BYTES) throw new Error("ABORT: process working-set cap exceeded");
  if (artifactBytes > MAX_ARTIFACT_BYTES) throw new Error("ABORT: aggregate artifact cap exceeded");
}

function artifactBytes() {
  let total = 0;
  try {
    for (const entry of (awaitlessReadDir(OUT))) {
      if (entry.isFile()) total += statSync(path.join(OUT, entry.name)).size;
    }
  } catch { /* output directory has not been created yet */ }
  return total;
}

function awaitlessReadDir(dir) {
  const fs = requireFs();
  return fs.readdirSync(dir, { withFileTypes: true });
}

function requireFs() {
  return importFs;
}

import * as importFs from "node:fs";

function parameterAndStateMetrics(model, meter) {
  meter.modelBytesPeak = Math.max(meter.modelBytesPeak, modelByteSize(model));
}

function nextPassModels(protocol, global) {
  const models = new Map();
  for (const seed of SEEDS) {
    for (const arm of protocol.arms) {
      const meter = new Meter(global);
      const model = createModel(arm.id, meter);
      parameterAndStateMetrics(model, meter);
      models.set(`${seed}/${arm.id}`, { model, meter });
    }
  }
  return models;
}

function assertNoEvalLabel(episode) {
  if (episode.split === "EVAL" &&
      (Object.hasOwn(episode, "train_oracle_target") || Object.hasOwn(episode, "reward_delay_ticks"))) {
    throw new Error("ABORT: evaluator truth or reward schedule leaked into EVAL workload");
  }
}

function runOneEpisode(episode, holder, global, frozenHash) {
  assertNoEvalLabel(episode);
  const { model, meter } = holder;
  meter.episodeOps = 0;
  meter.eventOpsSum = 0;
  meter.eventOpsMax = 0;
  meter.tanhCalls = 0;
  meter.expCalls = 0;
  meter.parameterReads = 0;
  meter.parameterWrites = 0;
  meter.stateReads = 0;
  meter.stateWrites = 0;
  meter.rewardRecordsCreated = 0;
  meter.rewardRecordsSettled = 0;
  meter.duplicateRewards = 0;
  meter.inputCharges = 0;
  meter.eligibilityBytesPeak = 0;
  meter.modelBytesPeak = 0;
  model.z = [0, 0, 0, 0];
  model.previousDecoderTick = 0;
  model.history = [];
  model.credit = null;
  model.learningEnabled = episode.split === "TRAIN";
  parameterAndStateMetrics(model, meter);
  const startParameters = parameterHash(model);
  if (episode.split === "EVAL" && startParameters !== frozenHash) {
    throw new Error("ABORT: evaluation parameters differ from frozen training parameters");
  }
  let prediction = 0;
  let activationTick = 0;
  const rewardId = `L64-R4.3/${episode.seed}/${episode.arm_id}/${episode.global_ordinal}/reward`;
  for (let index = 0; index < episode.input_event_records.length; index++) {
    const event = episode.input_event_records[index];
    if (index >= 4 || model.history.length >= MAX_HISTORY) {
      throw new Error("ABORT: event history overflow; no eviction or truncation permitted");
    }
    if (global.inputReceptions >= MAX_RECEPTIONS) throw new Error("ABORT: input reception cap would be exceeded");
    global.inputReceptions++;
    global.episodesInputReceptions++;
    inputCharge(meter, global);
    meter.beginEvent();
    if (index === 3) activationTick = event.physical_timestamp_ticks;
    let transition;
    if (model.params) {
      transition = applyPcnEvent(model, event, meter);
      model.history.push({
        event_id: event.event_id,
        physical_timestamp_ticks: event.physical_timestamp_ticks,
        decoder_timestamp_ticks: event.decoder_timestamp_ticks,
        channel_index: event.channel_index,
        amplitude: event.amplitude,
        ell: transition.ell,
        ellBefore: transition.ellBefore,
        z: transition.z,
        readoutSnapshot: [...model.params.w, model.params.b]
      });
      meter.parameterReads += 5;
      if (index === 3) {
        prediction = evaluateReadout(model, transition.z, meter);
        captureEligibility(model, prediction, activationTick, meter, rewardId);
      }
    }
    meter.endEvent();
  }
  if (episode.split === "TRAIN") {
    const truth = episode.train_oracle_target;
    if (truth !== 0 && truth !== 1) throw new Error("ABORT: invalid TRAIN-only oracle target");
    const reward = meter.eq(prediction, truth) ? 1 : -1;
    const delay = episode.reward_delay_ticks;
    if (!DELAY_TICKS.includes(delay)) throw new Error("ABORT: non-protocol reward delay");
    const dueTick = meter.add(activationTick, delay);
    if (meter.gt(meter.sub(dueTick, activationTick), REWARD_DEADLINE_TICKS)) {
      throw new Error("ABORT: reward deadline exceeded");
    }
    meter.rewardRecordsCreated++;
    global.rewardRecordsCreated++;
    const settled = new Set();
    meter.global = global;
    const rewardRecord = { id: rewardId, reward, dueTick };
    if (meter.lt(dueTick, activationTick) || !applyRewardOnce(model, rewardRecord, settled, meter)) {
      throw new Error("ABORT: invalid or duplicate first reward delivery");
    }
    if (!meter.eq(settled.size, 1)) throw new Error("ABORT: reward was not settled exactly once");
  } else {
    if (model.credit && model.learningEnabled) throw new Error("ABORT: EVAL learner update was enabled");
    meter.global = global;
  }
  const finalHash = parameterHash(model);
  if (episode.split === "EVAL" && finalHash !== frozenHash) {
    throw new Error("ABORT: EVAL changed trained parameters");
  }
  if (model.params) {
    model.z = [0, 0, 0, 0];
    model.history = [];
    model.credit = null;
  }
  global.episodes++;
  if (global.episodes > MAX_EPISODES) throw new Error("ABORT: episode cap exceeded");
  meter.global.parameterReads += meter.parameterReads;
  meter.global.parameterWrites += meter.parameterWrites;
  meter.global.stateReads += meter.stateReads;
  meter.global.stateWrites += meter.stateWrites;
  meter.global.eligibilityBytesPeak = Math.max(meter.global.eligibilityBytesPeak, meter.eligibilityBytesPeak);
  meter.global.modelBytesPeak = Math.max(meter.global.modelBytesPeak, meter.modelBytesPeak);
  meter.global.maximumEpisodeOverheadOps = Math.max(
    meter.global.maximumEpisodeOverheadOps, meter.episodeOps
  );
  return {
    global_ordinal: episode.global_ordinal,
    seed: episode.seed,
    split: episode.split,
    arm_id: episode.arm_id,
    input_event_records: episode.input_event_records,
    prediction,
    trained_parameter_sha256: finalHash,
    counted_scalar_ops: meter.episodeOps + meter.eventOpsSum,
    tanh_calls: meter.tanhCalls,
    exp_calls: meter.expCalls,
    eligibility_bytes_peak: meter.eligibilityBytesPeak,
    model_bytes_peak: meter.modelBytesPeak
  };
}

function newGlobal() {
  return {
    episodes: 0,
    inputReceptions: 0,
    episodesInputReceptions: 0,
    pcnEpisodes: 0,
    pcnInputReceptions: 0,
    scalarArithmeticComparisonOps: 0,
    tanhCalls: 0,
    expCalls: 0,
    inputEventCostCharges: 0,
    rewardRecordsCreated: 0,
    rewardRecordsSettled: 0,
    duplicateRewards: 0,
    peakWorkingSetBytes: currentRss(),
    maximumEventOps: 0,
    maximumEpisodeOverheadOps: 0,
    parameterReads: 0,
    parameterWrites: 0,
    stateReads: 0,
    stateWrites: 0,
    eligibilityBytesPeak: 0,
    modelBytesPeak: 0,
    maximumEpisodeOverheadOps: 0
  };
}

function ensureEmptyOutput() {
  mkdirSync(OUT, { recursive: true });
  const fs = importFs;
  if (fs.readdirSync(OUT).length !== 0) {
    throw new Error("ABORT: pilot output directory is not empty; no restart or replacement is permitted");
  }
}

async function waitForAffinityGate() {
  if (!process.stdin.isTTY) {
    const [chunk] = await once(process.stdin, "data");
    if (String(chunk).trim() !== "GO") throw new Error("ABORT: missing one-core affinity gate");
    return;
  }
  throw new Error("ABORT: execution requires the verified Windows one-core launcher");
}

function recordHeader(protocol, inputHash, config) {
  return {
    schema: "LUNA64-R4.3-BOUNDED-FEASIBILITY-PILOT",
    pilot_type: "feasibility_only",
    efficacy_scored: false,
    architecture_promotion: false,
    exact_revision: gitText("rev-parse", "HEAD"),
    branch: gitText("branch", "--show-current"),
    authorized_baseline: BASELINE,
    frozen_content_commit: FREEZE,
    protocol_revision: protocol.protocol_revision,
    protocol_sha256: shaFile(PROTOCOL_PATH),
    schema_sha256: shaFile(SCHEMA_PATH),
    golden_sha256: shaFile(GOLDEN_PATH),
    input_workload_sha256: inputHash,
    configuration: config
  };
}

function writeJson(file, value) {
  writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function validateCounts(global) {
  assert.equal(global.episodes, MAX_EPISODES);
  assert.equal(global.inputReceptions, MAX_RECEPTIONS);
  assert.equal(global.pcnEpisodes, MAX_PCN_EPISODES);
  assert.equal(global.pcnInputReceptions, MAX_PCN_RECEPTIONS);
  assert.equal(global.inputEventCostCharges, MAX_RECEPTIONS);
  assert.equal(global.duplicateRewards, 0);
  assert.equal(global.rewardRecordsCreated, 6 * 3 * 96 * 2);
  assert.equal(global.rewardRecordsSettled, global.rewardRecordsCreated);
  assert.ok(global.scalarArithmeticComparisonOps <= MAX_TOTAL_OPS);
}

async function runPilot() {
  await waitForAffinityGate();
  assertExecutionIdentity();
  const protocol = JSON.parse(readFileSync(PROTOCOL_PATH, "utf8"));
  const schema = JSON.parse(readFileSync(SCHEMA_PATH, "utf8"));
  const golden = JSON.parse(readFileSync(GOLDEN_PATH, "utf8"));
  const authText = readFileSync(AUTH_PATH, "utf8");
  assert.match(authText, /authorized; execution pending publication and isolated dispatch/);
  assert.equal(protocol.protocol_revision, "4.3.0-draft");
  assert.equal(schema.protocol_revision, undefined);
  assert.equal(golden.gate_id, protocol.gate_id);
  assert.equal(protocol.resources.maximum_total_episodes, MAX_EPISODES);
  assert.equal(protocol.resources.maximum_total_input_receptions, MAX_RECEPTIONS);
  ensureEmptyOutput();
  const startedAt = performance.now();
  const cpuStart = process.cpuUsage();
  const global = newGlobal();
  activeRun = { global, startedAt, cpuStart };
  const inputBytes = buildWorkload(protocol);
  const inputHash = hash(inputBytes);
  const inputPath = path.join(OUT, "input-workload.jsonl");
  writeFileSync(inputPath, inputBytes);
  const config = {
    seeds: SEEDS,
    arms: protocol.arms.map(arm => arm.id),
    training_episodes_per_arm_seed: 96,
    evaluation_workload_episodes_per_arm_seed: 48,
    passes: 2,
    episodes_per_pass: 2592,
    total_episodes: 5184,
    input_receptions_per_episode: 4,
    total_input_receptions: 20736,
    total_pcn_workload_episodes: 4320,
    total_pcn_input_receptions: 17280,
    reward_delays_ticks: DELAY_TICKS,
    omission_replay_passes: 0,
    efficacy_scoring: false,
    protocol_gate: protocol.gate_id,
    protocol_revision: protocol.protocol_revision,
    protocol_sha256: shaFile(PROTOCOL_PATH),
    schema_sha256: shaFile(SCHEMA_PATH),
    golden_sha256: shaFile(GOLDEN_PATH),
    authorization_sha256: shaFile(AUTH_PATH),
    freeze_manifest_sha256: "62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B",
    limit: {
      logical_cpus: 1,
      cpu_seconds: MAX_CPU_SECONDS,
      wall_seconds: MAX_WALL_SECONDS,
      working_set_bytes: MAX_RSS_BYTES,
      aggregate_artifact_bytes: MAX_ARTIFACT_BYTES,
      total_scalar_ops: MAX_TOTAL_OPS,
      scalar_ops_per_decoder_event: MAX_OPS_PER_EVENT,
      scalar_ops_episode_overhead: MAX_EPISODE_OVERHEAD_OPS
    },
    timing: "physical event time for eligibility and reward; decoder time only for PCN elapsed-time; no global neural timestep",
    event_cost: "one activity-cost-proxy unit charged immediately per input reception; reward charge zero",
    eval_boundary: "no target in EVAL input; no correctness reward, settlement, or parameter update",
    operation_counter: "executed scalar add/subtract/multiply/divide/comparison in decoder, eligibility, reward, and lifecycle arithmetic; excludes indexing, loop control, memory access, hashing, serialization, tanh, exp"
  };
  const header = recordHeader(protocol, inputHash, config);
  writeJson(path.join(OUT, "configuration.json"), header);
  const inputsForBothPasses = readFileSync(inputPath);
  if (!inputBytes.equals(inputsForBothPasses) || hash(inputsForBothPasses) !== inputHash) {
    throw new Error("ABORT: initial input workload byte verification failed");
  }
  let passDigests = [];
  const passSummaries = [];
  for (let passIndex = 0; passIndex < 2; passIndex++) {
    const passNo = passIndex + 1;
    const currentInputBytes = passIndex === 0 ? inputsForBothPasses : readFileSync(inputPath);
    if (!currentInputBytes.equals(inputsForBothPasses) || hash(currentInputBytes) !== inputHash) {
      throw new Error("ABORT: replay input bytes differ; no replacement is permitted");
    }
    const globalBeforePass = global.episodes;
    const models = nextPassModels(protocol, global);
    const frozenEvaluationHashes = new Map();
    const recordsFile = path.join(OUT, `pass-${passNo}-episodes.jsonl`);
    writeFileSync(recordsFile, "");
    const digest = createHash("sha256");
    const rows = currentInputBytes.toString("utf8").split("\n").filter(Boolean);
    if (rows.length !== 2592) throw new Error("ABORT: workload episode count mismatch");
    let passCount = 0;
    const perArmSeed = new Map();
    for (const line of rows) {
      const episode = JSON.parse(line);
      const holder = models.get(`${episode.seed}/${episode.arm_id}`);
      if (!holder) throw new Error("ABORT: workload path/arm mismatch");
      if (episode.split === "EVAL" && !frozenEvaluationHashes.has(`${episode.seed}/${episode.arm_id}`)) {
        frozenEvaluationHashes.set(`${episode.seed}/${episode.arm_id}`, parameterHash(holder.model));
      }
      const frozenHash = frozenEvaluationHashes.get(`${episode.seed}/${episode.arm_id}`);
      const beforeReceipts = global.inputReceptions;
      const result = runOneEpisode(episode, holder, global, frozenHash);
      if (episode.arm_id !== "A_COST_ONLY") {
        global.pcnEpisodes++;
        global.pcnInputReceptions += episode.input_event_records.length;
        if (global.pcnEpisodes > MAX_PCN_EPISODES || global.pcnInputReceptions > MAX_PCN_RECEPTIONS) {
          throw new Error("ABORT: PCN workload cap exceeded");
        }
      }
      if (global.inputReceptions - beforeReceipts !== 4) throw new Error("ABORT: input reception accounting mismatch");
      const outputLine = `${JSON.stringify(result)}\n`;
      appendFileSync(recordsFile, outputLine, "utf8");
      digest.update(outputLine, "utf8");
      passCount++;
      const key = `${episode.seed}/${episode.arm_id}`;
      if (!perArmSeed.has(key)) perArmSeed.set(key, {
        seed: episode.seed,
        arm_id: episode.arm_id,
        episodes: 0,
        train_episodes: 0,
        eval_episodes: 0,
        input_receptions: 0,
        counted_scalar_ops: 0,
        max_event_operations: 0,
        reward_records_created: 0,
        reward_records_settled: 0,
        eval_parameter_hashes: [],
        prediction_ones: 0,
        parameter_reads: 0,
        parameter_writes: 0,
        state_reads: 0,
        state_writes: 0,
        maximum_episode_overhead_operations: 0,
        eligibility_bytes_peak: 0,
        model_bytes_peak: 0
      });
      const group = perArmSeed.get(key);
      group.episodes++;
      group.input_receptions += 4;
      group.counted_scalar_ops += result.counted_scalar_ops;
      group.prediction_ones += result.prediction;
      group.parameter_reads += holder.meter.parameterReads;
      group.parameter_writes += holder.meter.parameterWrites;
      group.state_reads += holder.meter.stateReads;
      group.state_writes += holder.meter.stateWrites;
      group.max_event_operations = Math.max(group.max_event_operations, holder.meter.eventOpsMax);
      group.maximum_episode_overhead_operations = Math.max(
        group.maximum_episode_overhead_operations, holder.meter.episodeOps
      );
      group.eligibility_bytes_peak = Math.max(group.eligibility_bytes_peak, holder.meter.eligibilityBytesPeak);
      group.model_bytes_peak = Math.max(group.model_bytes_peak, holder.meter.modelBytesPeak);
      if (episode.split === "TRAIN") {
        group.train_episodes++;
        group.reward_records_created++;
        group.reward_records_settled++;
      } else {
        group.eval_episodes++;
        group.eval_parameter_hashes.push(result.trained_parameter_sha256);
      }
      if (passCount % 16 === 0) checkResources(global, startedAt, cpuStart, artifactBytes());
    }
    const passDigest = digest.digest("hex");
    if (passCount !== 2592 || global.episodes - globalBeforePass !== 2592) {
      throw new Error("ABORT: pass episode count mismatch");
    }
    for (const [key, holder] of models) {
      const evalHash = frozenEvaluationHashes.get(key);
      if (!evalHash) throw new Error(`ABORT: missing evaluation parameter checkpoint for ${key}`);
      if (parameterHash(holder.model) !== evalHash) throw new Error(`ABORT: evaluation parameters changed for ${key}`);
      const group = perArmSeed.get(key);
      if (group.eval_parameter_hashes.some(value => value !== evalHash)) {
        throw new Error(`ABORT: evaluation output parameter hash mismatch for ${key}`);
      }
    }
    passDigests.push(passDigest);
    const passSummary = {
      pass: passNo,
      episodes: passCount,
      input_receptions: 10368,
      digest_algorithm: "SHA-256",
      canonical_output_digest: passDigest,
      input_workload_sha256: inputHash,
      matched_models_reset_to_initial_parameters: true,
      evaluation_updates: 0,
      evaluation_reward_records: 0,
      omission_replay_passes: 0,
      per_arm_seed: [...perArmSeed.values()].sort((a, b) =>
        a.seed - b.seed || protocol.arms.findIndex(x => x.id === a.arm_id) -
          protocol.arms.findIndex(x => x.id === b.arm_id))
    };
    passSummaries.push(passSummary);
    writeJson(path.join(OUT, `pass-${passNo}-summary.json`), passSummary);
    checkResources(global, startedAt, cpuStart, artifactBytes());
    if (passNo === 2 && passDigests[0] !== passDigests[1]) {
      throw new Error("ABORT: canonical replay digests differ");
    }
  }
  validateCounts(global);
  const usage = process.cpuUsage(cpuStart);
  const finishedAt = performance.now();
  global.peakWorkingSetBytes = Math.max(global.peakWorkingSetBytes, currentRss());
  const totalArtifactBytes = artifactBytes();
  checkResources(global, startedAt, cpuStart, totalArtifactBytes);
  const summary = {
    status: "COMPLETED_BOUNDED_FEASIBILITY_PILOT",
    scientific_verdict: "NOT_ASSESSED",
    efficacy_scored: false,
    pilot_pooling_permitted: false,
    architecture_promotion: false,
    exact_revision: gitText("rev-parse", "HEAD"),
    branch: gitText("branch", "--show-current"),
    configuration: header,
    pass_summaries: passSummaries,
    canonical_digests_match: passDigests.length === 2 && passDigests[0] === passDigests[1],
    canonical_digests: passDigests,
    aggregate_counts: global,
    measured_resources: {
      cpu_seconds: (usage.user + usage.system) / 1e6,
      wall_seconds: (finishedAt - startedAt) / 1000,
      process_rss_peak_bytes: global.peakWorkingSetBytes,
      artifact_bytes_before_summary: totalArtifactBytes,
      artifact_cap_bytes: MAX_ARTIFACT_BYTES,
      one_core_affinity: "enforced externally with Windows SetProcessAffinityMask; verified child mask 0x1 before GO"
    },
    abort: null,
    omitted_analysis: [
      "No accuracy, specificity, efficacy, success/failure, or cost-benefit verdict was calculated.",
      "No counterfactual omission replay was run.",
      "No outcome was pooled into future efficacy data."
    ]
  };
  writeJson(path.join(OUT, "run-summary.json"), summary);
  const finalBytes = artifactBytes();
  if (finalBytes > MAX_ARTIFACT_BYTES) throw new Error("ABORT: artifact cap exceeded after final summary");
  summary.measured_resources.artifact_bytes_total = finalBytes;
  writeJson(path.join(OUT, "run-summary.json"), summary);
  process.stdout.write(`${JSON.stringify({ status: summary.status, episodes: global.episodes,
    input_receptions: global.inputReceptions, scalar_ops: global.scalarArithmeticComparisonOps,
    cpu_seconds: summary.measured_resources.cpu_seconds, wall_seconds: summary.measured_resources.wall_seconds,
    working_set_peak_bytes: global.peakWorkingSetBytes, artifact_bytes: artifactBytes(),
    digests_match: summary.canonical_digests_match }, null, 2)}\n`);
}

async function main() {
  try {
    await runPilot();
  } catch (error) {
    const message = String(error?.stack || error);
    try {
      if (!importFs.existsSync(OUT)) mkdirSync(OUT, { recursive: true });
      const entries = importFs.readdirSync(OUT);
      if (entries.length === 0 || !importFs.existsSync(path.join(OUT, "abort-status.json"))) {
        const usage = activeRun ? process.cpuUsage(activeRun.cpuStart) : { user: 0, system: 0 };
        const status = {
          status: "ABORTED",
          scientific_verdict: "NOT_ASSESSED",
          efficacy_scored: false,
          abort: message,
          exact_revision: (() => { try { return gitText("rev-parse", "HEAD"); } catch { return null; } })(),
          branch: (() => { try { return gitText("branch", "--show-current"); } catch { return null; } })(),
          partial_counts: activeRun?.global ?? null,
          measured_cpu_seconds: (usage.user + usage.system) / 1e6,
          measured_wall_seconds: activeRun ? (performance.now() - activeRun.startedAt) / 1000 : 0,
          retained_partial_files: entries,
          retained_partial_artifact_bytes: artifactBytes()
        };
        if (!importFs.existsSync(path.join(OUT, "abort-status.json"))) {
          writeJson(path.join(OUT, "abort-status.json"), status);
        }
        process.stderr.write(`${JSON.stringify(status, null, 2)}\n`);
      } else {
        process.stderr.write(`ABORT: existing abort-status.json preserved; ${message}\n`);
      }
    } catch (writeError) {
      process.stderr.write(`ABORT STATUS WRITE FAILED: ${String(writeError)}\n`);
    }
    process.exitCode = 2;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main();
}

export {
  DELAY_TICKS,
  Meter,
  applyRewardOnce,
  buildWorkload,
  captureEligibility,
  createModel,
  digestDraw,
  inputCharge,
  initialParameters,
  makeEvents,
  parameterHash
};
