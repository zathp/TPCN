import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildSchema } from "./generate-track-b-gate-r4-schema.mjs";

const ALLOWED_SCHEMA_KEYWORDS = new Set([
  "$schema", "$id", "$defs", "title", "description", "type", "properties",
  "required", "additionalProperties", "items", "enum", "const", "minimum",
  "maximum", "minLength", "maxLength", "anyOf"
]);
const PROTOCOL_REVISION = "4.3.0-draft";
const ARM_PARAMETER_COUNTS = new Map([
  ["A_COST_ONLY", 0],
  ["U_UNIFORM_PC", 45],
  ["R_RECENCY_PC", 45],
  ["L_LINEAR_TEMPORAL", 45],
  ["N_NONLINEAR_LOCAL", 45],
  ["X_TEMPORAL_DISRUPTION", 45]
]);

class StrictJsonParser {
  constructor(text) {
    this.text = text;
    this.offset = 0;
  }

  parse() {
    this.skipWhitespace();
    const result = this.value(0);
    this.skipWhitespace();
    if (this.offset !== this.text.length) this.fail("trailing data");
    return result;
  }

  value(depth) {
    if (depth > 64) this.fail("nesting depth over 64");
    this.skipWhitespace();
    const char = this.text[this.offset];
    if (this.text.startsWith("NaN", this.offset) ||
        this.text.startsWith("Infinity", this.offset) ||
        this.text.startsWith("-Infinity", this.offset)) this.fail("nonfinite JSON number");
    if (char === "{") return this.object(depth + 1);
    if (char === "[") return this.array(depth + 1);
    if (char === "\"") return this.string();
    if (char === "t" && this.text.startsWith("true", this.offset)) {
      this.offset += 4;
      return true;
    }
    if (char === "f" && this.text.startsWith("false", this.offset)) {
      this.offset += 5;
      return false;
    }
    if (char === "n" && this.text.startsWith("null", this.offset)) {
      this.offset += 4;
      return null;
    }
    if (char === "-" || (char >= "0" && char <= "9")) return this.number();
    this.fail("invalid JSON grammar");
  }

  object(depth) {
    this.offset++;
    this.skipWhitespace();
    const output = Object.create(null);
    const seen = new Set();
    if (this.text[this.offset] === "}") {
      this.offset++;
      return output;
    }
    while (true) {
      this.skipWhitespace();
      if (this.text[this.offset] !== "\"") this.fail("object key must be a string");
      const key = this.string();
      if (seen.has(key)) this.fail(`duplicate object key ${JSON.stringify(key)}`);
      seen.add(key);
      this.skipWhitespace();
      if (this.text[this.offset++] !== ":") this.fail("expected colon after object key");
      output[key] = this.value(depth);
      this.skipWhitespace();
      const separator = this.text[this.offset++];
      if (separator === "}") return output;
      if (separator !== ",") this.fail("expected comma or object end");
    }
  }

  array(depth) {
    this.offset++;
    this.skipWhitespace();
    const output = [];
    if (this.text[this.offset] === "]") {
      this.offset++;
      return output;
    }
    while (true) {
      output.push(this.value(depth));
      this.skipWhitespace();
      const separator = this.text[this.offset++];
      if (separator === "]") return output;
      if (separator !== ",") this.fail("expected comma or array end");
    }
  }

  string() {
    const start = this.offset++;
    while (this.offset < this.text.length) {
      const char = this.text[this.offset++];
      if (char === "\"") return JSON.parse(this.text.slice(start, this.offset));
      if (char === "\\") {
        if (this.offset >= this.text.length) this.fail("unterminated string escape");
        this.offset++;
      } else if (char.charCodeAt(0) < 0x20) {
        this.fail("unescaped control character in string");
      }
    }
    this.fail("unterminated string");
  }

  number() {
    const match = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/.exec(this.text.slice(this.offset));
    if (!match) this.fail("invalid JSON number");
    this.offset += match[0].length;
    const result = Number(match[0]);
    if (!Number.isFinite(result)) this.fail("nonfinite JSON number");
    return result;
  }

  skipWhitespace() {
    while (this.text[this.offset] === " " || this.text[this.offset] === "\t" ||
           this.text[this.offset] === "\r" || this.text[this.offset] === "\n") this.offset++;
  }

  fail(message) {
    throw new Error(`${message} at byte offset ${this.offset}`);
  }
}

function schemaConfigurationCheck(schema, at = "$") {
  if (!schema || typeof schema !== "object" || Array.isArray(schema)) {
    throw new Error(`schema configuration must be an object at ${at}`);
  }
  for (const [key, value] of Object.entries(schema)) {
    if (!ALLOWED_SCHEMA_KEYWORDS.has(key)) throw new Error(`unknown schema keyword ${key} at ${at}`);
    if (key === "properties" && value && typeof value === "object") {
      for (const [name, child] of Object.entries(value)) schemaConfigurationCheck(child, `${at}.properties.${name}`);
    } else if (key === "items" || key === "anyOf") {
      for (const [index, child] of (Array.isArray(value) ? value : [value]).entries()) {
        schemaConfigurationCheck(child, `${at}.${key}.${index}`);
      }
    }
  }
}

function equalJson(left, right) {
  if (Object.is(left, right)) return true;
  if (Array.isArray(left) || Array.isArray(right)) {
    return Array.isArray(left) && Array.isArray(right) &&
      left.length === right.length && left.every((value, index) => equalJson(value, right[index]));
  }
  if (!left || !right || typeof left !== "object" || typeof right !== "object") return false;
  const leftKeys = Object.keys(left).sort();
  const rightKeys = Object.keys(right).sort();
  return leftKeys.length === rightKeys.length &&
    leftKeys.every((key, index) => key === rightKeys[index] && equalJson(left[key], right[key]));
}

function validateAgainstSchema(value, schema, at = "$") {
  if (schema.const !== undefined && value !== schema.const) {
    throw new Error(`const mismatch at ${at}`);
  }
  if (schema.enum && !schema.enum.some(candidate => Object.is(candidate, value))) {
    throw new Error(`enum mismatch at ${at}`);
  }
  if (schema.anyOf) {
    const errors = [];
    for (const candidate of schema.anyOf) {
      try {
        validateAgainstSchema(value, candidate, at);
        return;
      } catch (error) {
        errors.push(error.message);
      }
    }
    throw new Error(`anyOf mismatch at ${at}: ${errors.join("; ")}`);
  }

  const type = schema.type;
  const typeMatches = type === undefined ||
    (type === "object" && value !== null && typeof value === "object" && !Array.isArray(value)) ||
    (type === "array" && Array.isArray(value)) ||
    (type === "integer" && typeof value === "number" && Number.isSafeInteger(value)) ||
    (type === "number" && typeof value === "number" && Number.isFinite(value)) ||
    (type === "string" && typeof value === "string") ||
    (type === "boolean" && typeof value === "boolean") ||
    (type === "null" && value === null);
  if (!typeMatches) throw new Error(`type mismatch at ${at}; expected ${type}`);

  if (typeof value === "number") {
    if (schema.minimum !== undefined && value < schema.minimum) throw new Error(`minimum violation at ${at}`);
    if (schema.maximum !== undefined && value > schema.maximum) throw new Error(`maximum violation at ${at}`);
  }
  if (typeof value === "string") {
    if (schema.minLength !== undefined && value.length < schema.minLength) throw new Error(`minLength violation at ${at}`);
    if (schema.maxLength !== undefined && value.length > schema.maxLength) throw new Error(`maxLength violation at ${at}`);
  }
  if (Array.isArray(value) && schema.items) {
    value.forEach((item, index) => validateAgainstSchema(item, schema.items, `${at}[${index}]`));
  }
  if (type === "object") {
    for (const required of schema.required ?? []) {
      if (!Object.hasOwn(value, required)) throw new Error(`required property missing at ${at}.${required}`);
    }
    for (const key of Object.keys(value)) {
      if (!Object.hasOwn(schema.properties ?? {}, key) && schema.additionalProperties === false) {
        throw new Error(`additionalProperties violation at ${at}.${key}`);
      }
      const propertySchema = schema.properties?.[key];
      if (propertySchema) validateAgainstSchema(value[key], propertySchema, `${at}.${key}`);
    }
  }
}

function semanticChecks(protocol) {
  if (protocol.schema !== "LUNA64-TRACK-B-PROTOCOL-R4") throw new Error("protocol schema identity mismatch");
  if (protocol.schema_revision !== 1 || protocol.protocol_revision !== PROTOCOL_REVISION) {
    throw new Error("protocol revision mismatch");
  }
  if (protocol.gate_id !== "L64-TB-GATE-20261010-R4") throw new Error("gate identity mismatch");
  if (protocol.timebase.ticks_per_tu !== 1000000 || protocol.timebase.tu_per_tick !== "0.000001") {
    throw new Error("timebase ticks_per_tu/tu_per_tick mismatch");
  }
  if (protocol.eligibility.capacity !== 8 || !Number.isSafeInteger(protocol.eligibility.capacity) ||
      protocol.eligibility.capacity < 1) {
    throw new Error("eligibility capacity must be a positive safe integer no greater than the declared maximum");
  }
  if (protocol.eligibility.horizon_ticks !== 8000000) throw new Error("eligibility horizon mismatch");
  const reward = protocol.reward_lifecycle;
  if (reward.deadline_ticks_after_activation !== 16000000 ||
      reward.expiry_tick_after_activation !== reward.deadline_ticks_after_activation + 1) {
    throw new Error("reward expiry must equal deadline plus one tick");
  }
  if (!Array.isArray(protocol.arms) || protocol.arms.length !== ARM_PARAMETER_COUNTS.size) {
    throw new Error("arm inventory must contain exactly the allowlisted arm identities");
  }
  const seen = new Set();
  for (const arm of protocol.arms) {
    if (!ARM_PARAMETER_COUNTS.has(arm.id) || seen.has(arm.id)) throw new Error(`arm identity invalid or repeated: ${arm.id}`);
    seen.add(arm.id);
    if (arm.parameters !== ARM_PARAMETER_COUNTS.get(arm.id)) throw new Error(`arm parameter count mismatch: ${arm.id}`);
  }
  if (seen.size !== ARM_PARAMETER_COUNTS.size) throw new Error("arm inventory is incomplete");
  if (protocol.resources.maximum_total_episodes !==
      protocol.resources.pilot_arms * protocol.resources.pilot_seeds *
      (protocol.resources.training_episodes_per_arm_seed + protocol.resources.evaluation_workload_episodes_per_arm_seed) *
      protocol.resources.pilot_execution_passes) {
    throw new Error("pilot episode arithmetic mismatch");
  }
  if (protocol.resources.maximum_total_input_receptions !==
      protocol.resources.maximum_total_episodes * protocol.resources.maximum_input_events_per_episode) {
    throw new Error("pilot reception arithmetic mismatch");
  }
  if (protocol.resources.pilot_seed_ids.length !== protocol.resources.pilot_seeds ||
      new Set(protocol.resources.pilot_seed_ids).size !== protocol.resources.pilot_seeds ||
      protocol.resources.pilot_seed_ids.some(seed => !protocol.task.generator.seeds.includes(seed))) {
    throw new Error("pilot seed IDs must be a unique subset of the frozen task seeds");
  }
  const decoderArms = protocol.resources.pilot_arms - 1;
  const pcnEpisodes = decoderArms * protocol.resources.pilot_seeds *
    (protocol.resources.training_episodes_per_arm_seed + protocol.resources.evaluation_workload_episodes_per_arm_seed) *
    protocol.resources.pilot_execution_passes;
  const pcnReceptions = pcnEpisodes * protocol.resources.maximum_input_events_per_episode;
  if (protocol.resources.maximum_pcn_workload_episodes !== pcnEpisodes ||
      protocol.resources.maximum_pcn_input_receptions !== pcnReceptions) {
    throw new Error("PCN workload arithmetic mismatch");
  }
  const opsUpper = pcnReceptions * protocol.resources.maximum_counted_ops_per_pcn_event +
    protocol.resources.maximum_total_episodes * protocol.resources.maximum_episode_overhead_ops;
  if (protocol.resources.analytical_total_counted_ops_lower !== 0 ||
      protocol.resources.analytical_total_counted_ops_upper !== opsUpper) {
    throw new Error("analytical operation bounds mismatch");
  }
  if (protocol.resources.pilot_execution_passes !== 2 ||
      protocol.resources.counterfactual_omission_replay_passes_in_pilot !== 0 ||
      !protocol.statistics.attribution_specificity.replay.includes("expressly excluded from the feasibility-only pilot") ||
      !protocol.resources.execution_passes.includes("reset the entire run to initial model parameters") ||
      !equalJson(protocol.resources.replay_digest, {
        algorithm: "SHA-256",
        encoding: "UTF-8 without BOM; compact JSON Lines; one episode object followed by LF; ECMAScript JSON.stringify with no replacer or whitespace",
        episode_record_fields_in_order: ["global_ordinal", "seed", "split", "arm_id", "input_event_records", "prediction", "trained_parameter_sha256", "counted_scalar_ops", "tanh_calls", "exp_calls", "eligibility_bytes_peak", "model_bytes_peak"],
        episode_record_order: "seed ascending, protocol arms array order, split TRAIN then EVAL, split_local_ordinal ascending",
        input_event_record_fields_in_order: ["event_id", "physical_timestamp_ticks", "decoder_timestamp_ticks", "channel_index", "amplitude"],
        input_event_record_order: "canonical event order from timebase.equal_time_order",
        number_serialization: "ECMAScript JSON.stringify",
        equal_pass_digests_required: true
      })) {
    throw new Error("pilot replay scope or execution-pass contract mismatch");
  }
  const rewardDelays = protocol.reward_lifecycle.delay_ticks;
  if (!Array.isArray(rewardDelays) ||
      !equalJson(rewardDelays, [0, 1000000, 8000000, 9000000, 15000000, 16000000]) ||
      protocol.task.generator.training_episodes_per_seed_arm % rewardDelays.length !== 0 ||
      !protocol.reward_lifecycle.delay_assignment.includes("split_local_ordinal mod delay_ticks.length") ||
      !protocol.reward_lifecycle.delay_assignment.includes("EVAL emits no correctness reward") ||
      !protocol.task.controls.reward_delay_assignment.includes("same split-local ordinal")) {
    throw new Error("reward delay assignment or evaluation reward policy mismatch");
  }
  if (protocol.resources.pilot_authorized !== false || protocol.status.pilot_authorized !== false ||
      protocol.status.execution_performed !== false || protocol.status.architecture_promotion_authorized !== false) {
    throw new Error("R4 must remain an unauthorized, unexecuted candidate");
  }
}

export function validateText(text, schemaText) {
  const value = new StrictJsonParser(text).parse();
  const schema = new StrictJsonParser(schemaText).parse();
  schemaConfigurationCheck(schema);
  validateAgainstSchema(value, schema);
  semanticChecks(value);
  if (!equalJson(schema, buildSchema(value))) {
    throw new Error("schema does not exactly match the protocol-derived R4 schema");
  }
  return value;
}

export function classifyOutcome(result) {
  if (!result.valid || result.missing_seed || result.aborted_seed ||
      result.empty_attribution || result.cost_available === false || result.nonfinite) {
    return "INCONCLUSIVE";
  }
  const requiredNumeric = [
    result.accuracy, result.mean_effect, result.lower_ci_primary, result.lower_ci_attribution,
    result.specificity_n, result.specificity_u, result.specificity_r,
    result.ops_ratio, result.memory_ratio, result.disruption_accuracy
  ];
  if (!requiredNumeric.every(Number.isFinite)) return "INCONCLUSIVE";
  if (result.accuracy < 0 || result.accuracy > 1 ||
      result.mean_effect < -1 || result.mean_effect > 1 ||
      result.lower_ci_primary < -1 || result.lower_ci_primary > 1 ||
      result.lower_ci_attribution < -1 || result.lower_ci_attribution > 1 ||
      result.specificity_n < 0 || result.specificity_n > 1 ||
      result.specificity_u < 0 || result.specificity_u > 1 ||
      result.specificity_r < 0 || result.specificity_r > 1 ||
      result.ops_ratio < 0 || result.memory_ratio < 0 ||
      result.disruption_accuracy < 0 || result.disruption_accuracy > 1) {
    return "INCONCLUSIVE";
  }
  const success =
    result.accuracy >= 0.70 &&
    result.mean_effect >= 0.05 &&
    result.lower_ci_primary > 0 &&
    result.lower_ci_attribution > 0 &&
    result.specificity_n - result.specificity_u >= 0.10 &&
    result.specificity_n - result.specificity_r >= 0.10 &&
    result.ops_ratio <= 2.0 &&
    result.memory_ratio <= 2.0 &&
    result.disruption_accuracy <= 0.55;
  return success ? "SUCCESS" : "FAILURE";
}

async function main(args) {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
  const protocolPath = args[args.indexOf("--protocol") + 1] ??
    path.join(root, "experiments/luna64/luna64-track-b-protocol-r4.json");
  const schemaPath = args[args.indexOf("--schema") + 1] ??
    path.join(root, "experiments/luna64/luna64-track-b-protocol-r4.schema.json");
  const protocolText = await readFile(protocolPath, "utf8");
  const schemaText = await readFile(schemaPath, "utf8");
  const protocol = validateText(protocolText, schemaText);
  const goldenIndex = args.indexOf("--golden");
  if (goldenIndex >= 0) {
    const goldenPath = args[goldenIndex + 1];
    const golden = new StrictJsonParser(await readFile(goldenPath, "utf8")).parse();
    if (golden.gate_id !== protocol.gate_id || golden.protocol_path !== "experiments/luna64/luna64-track-b-protocol-r4.json") {
      throw new Error("golden fixture identity does not match protocol");
    }
  }
  process.stdout.write(JSON.stringify({ status: "VALID", gate_id: protocol.gate_id, protocol_revision: protocol.protocol_revision }) + "\n");
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2)).catch(error => {
    process.stderr.write(`INVALID: ${error.message}\n`);
    process.exitCode = 1;
  });
}
