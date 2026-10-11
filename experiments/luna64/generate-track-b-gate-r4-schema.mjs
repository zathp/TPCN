import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const protocolPath = path.join(root, "experiments/luna64/luna64-track-b-protocol-r4.json");
const schemaPath = path.join(root, "experiments/luna64/luna64-track-b-protocol-r4.schema.json");
function infer(value) {
  if (Array.isArray(value)) {
    const itemSchemas = value.map(infer);
    if (itemSchemas.length === 0) return { type: "array" };
    return { type: "array", items: merge(itemSchemas) };
  }
  if (value === null) return { type: "null" };
  if (typeof value === "object") {
    const properties = Object.fromEntries(Object.entries(value).map(([key, item]) => [key, infer(item)]));
    return {
      type: "object",
      properties,
      required: Object.keys(properties),
      additionalProperties: false
    };
  }
  if (typeof value === "number") return { type: Number.isInteger(value) ? "integer" : "number" };
  return { type: typeof value };
}

function merge(schemas) {
  const serialized = new Map(schemas.map(schema => [JSON.stringify(schema), schema]));
  if (serialized.size === 1) return schemas[0];
  const types = [...new Set(schemas.map(schema => schema.type))];
  if (types.length === 1 && types[0] === "object") {
    const keys = [...new Set(schemas.flatMap(schema => Object.keys(schema.properties)))];
    const properties = Object.fromEntries(keys.map(key => {
      const present = schemas.flatMap(schema => key in schema.properties ? [schema.properties[key]] : []);
      return [key, merge(present)];
    }));
    return {
      type: "object",
      properties,
      required: keys.filter(key => schemas.every(schema => key in schema.properties)),
      additionalProperties: false
    };
  }
  if (types.length === 1 && types[0] === "integer") return { type: "integer" };
  if (types.length <= 2 && types.includes("integer") && types.includes("number")) return { type: "number" };
  return { anyOf: schemas };
}

export function buildSchema(protocol) {
  const schema = {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    $id: "https://tpcn.invalid/schemas/luna64-track-b-r4.json",
    title: "Luna-64 Track B R4 strict protocol",
    ...infer(protocol)
  };
  const consts = [
    ["schema", protocol.schema],
    ["schema_revision", protocol.schema_revision],
    ["gate_id", protocol.gate_id],
    ["protocol_revision", protocol.protocol_revision],
    ["timebase.ticks_per_tu", protocol.timebase.ticks_per_tu],
    ["eligibility.horizon_ticks", protocol.eligibility.horizon_ticks],
    ["eligibility.capacity", protocol.eligibility.capacity],
    ["reward_lifecycle.deadline_ticks_after_activation", protocol.reward_lifecycle.deadline_ticks_after_activation],
    ["reward_lifecycle.expiry_tick_after_activation", protocol.reward_lifecycle.expiry_tick_after_activation]
  ];
  for (const [dottedPath, value] of consts) {
    const target = dottedPath.split(".").reduce((node, key) => node.properties[key], schema);
    target.const = value;
  }
  return schema;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const protocol = JSON.parse(await readFile(protocolPath, "utf8"));
  const schema = buildSchema(protocol);
  await writeFile(schemaPath, `${JSON.stringify(schema, null, 2)}\n`, "utf8");
  console.log(`Wrote ${path.relative(root, schemaPath)} from ${path.relative(root, protocolPath)}`);
}
