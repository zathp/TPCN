"""Run the authorized Luna-44 ACP-0008 canonical-fixture rebaseline.

This runner consumes only the committed Luna-44 fixture. It deliberately does
not import the fixture builder or any spiral/dataset generator.

Routed EXCURSION evidence is captured independently at queue admission and
successful neuron consumption, then retained in separate initial/replay JSON
artifacts. The receiver timestamp is the destination's logical clock, not wall
time. Instrumentation does not modify routing or neuron computation.
"""

from __future__ import annotations

from contextlib import ExitStack
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import math
import platform
import struct
import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest import mock

from tpcn.eligibility import EligibilityCapacityError, EligibilityLedger
from tpcn.event_runtime import Event, EventQueue, EventType, QueueCapacityError
from tpcn.excursion_neuron import (
    E1Config,
    IntegrationConfig,
    MultiExcursionNeuron,
)
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.predictive_coding import LocalPredictor
from tpcn.topology import BoundedTopology, Edge, TopologyCapacityError
from scripts.verify_luna44_canonical_fixture import (
    FixtureVerificationError,
    verify_fixture as verify_committed_fixture_provenance,
)


AUTHORIZATION_REVISION = "ff4bf51dcaab2e7b66f0409f4d63a33649c3e104"
AUTHORIZATION_HANDOFF_SHA256 = "a2baf6e0f6fefae6ec5e108688de965940242d34f109b1143c3f6909699cbe40"
FIXTURE_REVISION = "6413cffe6982bccc6698af6bebfae51f04e71dd9"
FIXTURE_PROVENANCE_REVISION = "86e5a2f389af06b06bf04a614edaed88e0847902"
FIXTURE_SHA256 = "6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305"
FIXTURE_FILE_SHA256 = "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629"
FIXTURE_PROVENANCE_SHA256 = "6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22"
FIXTURE_PROVENANCE_GIT_BLOB = "eb9179abae7eed10891e6022832f16735111b220"
FIXTURE_GENERATOR_REVISION = "a79494cd66be28fd291ed11eddd62d342f457cfd"
FIXTURE_GENERATOR_SHA256 = "17e581cf702fae1f56889472a967d2e8e5fec37cc041edba8247da14a0a8b5db"
FIXTURE_POINT_GENERATOR_SHA256 = "2ffb1b5ebb23f016436043118bc675eddaa14bfd923129359fe61a12df94d9f0"
FIXTURE_GENERATION_EXECUTION_REVISION = "9226316be4935236ba3f6f511b4abfe8f23af278"
AUTHORIZATION_HANDOFF_PATH = Path(
    "workflow/handoffs/luna-0-authorization-luna44-canonical-fixture-rebaseline-20261005.md"
)
SEEDS = tuple(range(5))
SEQUENCES_PER_SEED = 64
TOTAL_SEQUENCES = 320
TOTAL_POINTS = 5164
ARMS = ("DISABLED", "DEFAULT", "CALIBRATED")
CALIBRATED_DECAY_RATE_Z = 0.0125
DEFAULT_DECAY_RATE_Z = 0.1
FLOAT_TOLERANCE_MULTIPLIER = 64.0
NODES = ("source", "relay", "destination")
QUEUE_CAPACITY = 128
RUNTIME_EVENT_BUDGET = 1024
MAX_ACTIVITY_EVENTS = 1024
SETTLING_HORIZON = 4.0
PREDICTION_CAPACITY = 8
PREDICTION_EXPIRY = 4.0
ELIGIBILITY_CAPACITY = 1024
NEURON_EVENT_BUDGET = 4096
ARTIFACT_DIRECTORY = Path("artifacts/luna44-acp0008-canonical-fixture-rebaseline")
FIXTURE_PATH = Path("artifacts/luna44-canonical-fixture/fixture.json")
FIXTURE_PROVENANCE_PATH = Path("artifacts/luna44-canonical-fixture/provenance.json")
FIXTURE_PROVENANCE_GIT_PATH = FIXTURE_PROVENANCE_PATH.as_posix()
FLOAT_POLICY_FORMULA = (
    "64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))"
)
EXPECTED_SPIRAL_CONFIG = {
    "min_points": 12,
    "max_points": 20,
    "min_duration": 240.0,
    "max_duration": 320.0,
    "min_scale": 0.8,
    "max_scale": 1.2,
    "min_angular_speed": 1.7,
    "max_angular_speed": 2.5,
    "min_radial_growth": 0.7,
    "max_radial_growth": 1.1,
    "max_rotation": 6.283185307179586,
    "max_translation": 1.0,
    "max_timing_jitter": 0.08,
    "max_coordinate_noise": 0.025,
    "max_radial_jitter": 0.04,
}


class ProvenanceError(RuntimeError):
    def __init__(self, message: str, provenance: dict[str, Any]) -> None:
        super().__init__(message)
        self.provenance = provenance


class RoutingEvidenceError(RuntimeError):
    def __init__(self, capture: dict[str, Any]) -> None:
        super().__init__("canonical emission/transfer/reception provenance did not reconcile")
        self.capture = capture


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite value cannot be serialized")
        return value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise TypeError(f"cannot serialize {type(value).__name__}")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        _jsonable(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _artifact_digest(value: dict[str, Any]) -> str:
    payload = dict(value)
    payload.pop("artifact_digest", None)
    return _digest(payload)


def _seal_artifact(value: dict[str, Any]) -> dict[str, Any]:
    artifact = dict(value)
    artifact["artifact_digest"] = _artifact_digest(artifact)
    return artifact


def _replay_envelope_digest(record_digests: list[str], config_digest: str) -> str:
    return _digest(
        {
            "fixture_sha256": FIXTURE_SHA256,
            "config_digest": config_digest,
            "ordered_record_digests": record_digests,
        }
    )


def _bits(value: float) -> str:
    return struct.pack(">d", float(value)).hex()


def _float_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("fixture floats must be finite")
    return {"decimal": repr(number), "hex": number.hex()}


def _float_tolerance(observed: float, expected: float) -> float:
    return (
        FLOAT_TOLERANCE_MULTIPLIER
        * sys.float_info.epsilon
        * max(1.0, abs(observed), abs(expected))
    )


def _float_check(observed: float, expected: float) -> dict[str, Any]:
    tolerance = _float_tolerance(observed, expected)
    difference = abs(observed - expected)
    return {
        "observed": observed,
        "expected": expected,
        "error": difference,
        "bound": tolerance,
        "absolute_error": difference,
        "tolerance": tolerance,
        "tolerance_formula": FLOAT_POLICY_FORMULA,
        "matches": difference <= tolerance,
    }


def _raw_row(point: dict[str, Any]) -> dict[str, Any]:
    return {
        "seed": point["seed"],
        "sequence_index": point["sequence_index"],
        "stream_id": point["stream_id"],
        "point_index": point["point_index"],
        "batch_ordinal": point["batch_ordinal"],
        "x_bits_be": _bits(float.fromhex(point["x"]["hex"])),
        "y_bits_be": _bits(float.fromhex(point["y"]["hex"])),
        "t_bits_be": _bits(float.fromhex(point["t"]["hex"])),
    }


def _sequence_raw_rows(sequence: dict[str, Any]) -> list[dict[str, Any]]:
    return [_raw_row(point) for point in sequence["points"]]


def _validate_sequence(sequence: dict[str, Any]) -> None:
    seed = sequence["seed"]
    sequence_index = sequence["sequence_index"]
    stream_id = sequence["stream_id"]
    points = sequence["points"]
    if stream_id != f"c{seed:02d}-{sequence_index:03d}":
        raise ValueError(f"invalid stream identity {stream_id!r}")
    if sequence["point_count"] != len(points) or not points:
        raise ValueError(f"invalid point count for {stream_id}")
    previous_timestamp: float | None = None
    batch_ordinal = -1
    for point_index, point in enumerate(points):
        if (
            point["seed"] != seed
            or point["sequence_index"] != sequence_index
            or point["stream_id"] != stream_id
            or point["point_index"] != point_index
        ):
            raise ValueError(f"point identity/order mismatch in {stream_id}")
        values: dict[str, float] = {}
        for name in ("x", "y", "t", "audit_x_plus_y"):
            encoded = point[name]
            decimal_value = float(encoded["decimal"])
            hex_value = float.fromhex(encoded["hex"])
            if not math.isfinite(decimal_value) or _bits(decimal_value) != _bits(hex_value):
                raise ValueError(f"decimal/hex binary64 mismatch in {stream_id}:{point_index}:{name}")
            values[name] = hex_value
        timestamp = values["t"]
        if previous_timestamp is None or timestamp != previous_timestamp:
            if previous_timestamp is not None and timestamp < previous_timestamp:
                raise ValueError(f"timestamp order decreases in {stream_id}")
            batch_ordinal += 1
        if point["batch_ordinal"] != batch_ordinal:
            raise ValueError(f"same-time batch ordinal mismatch in {stream_id}:{point_index}")
        if not _float_check(values["x"] + values["y"], values["audit_x_plus_y"])["matches"]:
            raise ValueError(f"derived audit value mismatch in {stream_id}:{point_index}")
        previous_timestamp = timestamp
    if _digest(_sequence_raw_rows(sequence)) != sequence["source_sha256"]:
        raise ValueError(f"per-sequence raw source digest mismatch in {stream_id}")


def _validate_materialization_provenance(
    provenance: dict[str, Any],
    fixture_bytes: bytes,
    fixture: dict[str, Any],
    rows: list[dict[str, Any]],
) -> None:
    materializations = provenance.get("materializations")
    if not isinstance(materializations, list) or len(materializations) != 2:
        raise ValueError("fixture provenance must contain two independent materializations")
    invocation_ids = [item.get("invocation_id") for item in materializations]
    process_ids = [item.get("process_id") for item in materializations]
    output_directories = [item.get("output_directory") for item in materializations]
    if (
        any(not isinstance(value, str) or not value for value in invocation_ids)
        or any(not isinstance(value, int) or isinstance(value, bool) for value in process_ids)
        or any(not isinstance(value, str) or not value for value in output_directories)
        or len(set(invocation_ids)) != 2
        or len(set(process_ids)) != 2
        or len(set(output_directories)) != 2
    ):
        raise ValueError("fixture materialization records are duplicated or not independent")
    materializer_hashes = [
        item.get("materializer_source_sha256") for item in materializations
    ]
    if (
        any(
            not isinstance(value, str)
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
            for value in materializer_hashes
        )
        or len(set(materializer_hashes)) != 1
    ):
        raise ValueError("fixture materialization source identities differ or are invalid")
    for item in materializations:
        if (
            item.get("generator_revision") != FIXTURE_GENERATOR_REVISION
            or item.get("generation_execution_revision")
            != FIXTURE_GENERATOR_REVISION
            or not item.get("started_at_utc")
            or not item.get("completed_at_utc")
            or not item.get("environment_identity")
        ):
            raise ValueError("fixture materialization identity or environment is invalid")
        if (
            item.get("fixture_file_sha256") != hashlib.sha256(fixture_bytes).hexdigest()
            or item.get("semantic_fixture_digest")
            != provenance.get("canonical_fixture_sha256")
            or item.get("byte_length") != len(fixture_bytes)
            or item.get("record_count") != len(fixture["sequences"])
            or item.get("ordered_point_count") != len(rows)
        ):
            raise ValueError("fixture materialization measurements differ from committed fixture")
        order_digest = _digest(
            [
                [
                    row["seed"],
                    row["sequence_index"],
                    row["stream_id"],
                    row["point_index"],
                ]
                for row in rows
            ]
        )
        bits_digest = _digest(
            [[row["x_bits_be"], row["y_bits_be"], row["t_bits_be"]] for row in rows]
        )
        if (
            item.get("seed_sequence_point_order_sha256") != order_digest
            or item.get("exact_xyz_bits_sha256") != bits_digest
        ):
            raise ValueError("fixture materialization ordering or point bits differ")
    if (
        materializations[0]["environment_identity"]
        != materializations[1]["environment_identity"]
    ):
        raise ValueError("fixture materializations were generated in different environments")
    original_publication = provenance.get("original_publication_materialization", {})
    if (
        original_publication.get("independent_repeat_evidence_retained") is not False
        or original_publication.get("original_independent_materialization_count")
        != "not established by retained evidence"
    ):
        raise ValueError("original publication determinism evidence is unsupported")
    verification = provenance.get(
        "post_publication_independent_materialization_verification", {}
    )
    if (
        verification.get("verified_after_original_publication") is not True
        or verification.get("invocation_ids") != invocation_ids
        or verification.get("materializer_sha256") != materializer_hashes[0]
        or verification.get("materializer_revision") != "10994419cec3646d30d965372f88d10605d83d57"
    ):
        raise ValueError("post-publication materialization verification is incomplete")
    comparison = provenance.get("materialization_comparison", {})
    if (
        comparison.get("independent_invocations") is not True
        or comparison.get("fixture_bytes_equal") is not True
        or comparison.get("file_sha256_equal") is not True
        or comparison.get("semantic_digest_equal") is not True
        or comparison.get("sequence_point_order_equal") is not True
        or comparison.get("point_by_point_exact_equal") is not True
        or comparison.get("statement")
        != "Post-publication independent fixture materialization verification produced identical canonical fixture bytes/digests under the declared environment."
        or comparison.get("scope")
        != "Repeated materialization was verified only in the recorded environment; this does not establish cross-platform or environment-independent determinism."
    ):
        raise ValueError("fixture determinism comparison is incomplete or failed")


def load_fixture(
    fixture_path: Path = FIXTURE_PATH,
    provenance_path: Path = FIXTURE_PROVENANCE_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate and load retained fixture files without importing a generator."""
    if provenance_path != FIXTURE_PROVENANCE_PATH:
        raise ValueError("fixture provenance path differs from the pinned path")
    fixture_bytes = fixture_path.read_bytes()
    fixture_file_sha256 = hashlib.sha256(fixture_bytes).hexdigest()
    fixture = json.loads(fixture_bytes.decode("utf-8"))
    provenance_bytes = provenance_path.read_bytes()
    committed_provenance_path = (
        f"{FIXTURE_PROVENANCE_REVISION}:{FIXTURE_PROVENANCE_GIT_PATH}"
    )
    committed_provenance_blob = _git_output("rev-parse", committed_provenance_path)
    if committed_provenance_blob != FIXTURE_PROVENANCE_GIT_BLOB:
        raise ValueError("fixture provenance Git blob differs from the pinned provenance revision")
    committed_provenance_bytes = subprocess.run(
        ["git", "cat-file", "blob", committed_provenance_blob],
        check=True,
        capture_output=True,
    ).stdout
    if provenance_bytes != committed_provenance_bytes:
        raise ValueError("fixture provenance differs from the committed provenance-revision blob")
    provenance_sha256 = hashlib.sha256(provenance_bytes).hexdigest()
    if provenance_sha256 != FIXTURE_PROVENANCE_SHA256:
        raise ValueError("fixture provenance full-file SHA-256 does not match the pinned value")
    fixture_provenance = json.loads(provenance_bytes.decode("utf-8"))
    try:
        verify_committed_fixture_provenance(
            provenance_path,
            fixture_path,
            Path.cwd(),
            expected_manifest_sha256=FIXTURE_PROVENANCE_SHA256,
        )
    except FixtureVerificationError as error:
        raise ValueError(f"independent fixture provenance verification failed: {error}") from error
    if fixture.get("schema") != "TPCN-LUNA44-CANONICAL-POINT-FIXTURE-1":
        raise ValueError("unexpected canonical fixture schema")
    if fixture_provenance.get("schema") != "TPCN-LUNA44-CANONICAL-FIXTURE-PROVENANCE-1":
        raise ValueError("unexpected fixture provenance schema")
    generator = fixture_provenance["generator"]
    sequence_builder = generator["sequence_builder"]
    point_generator = generator["point_generator"]
    if generator["source_repository_revision"] != FIXTURE_GENERATOR_REVISION:
        raise ValueError("fixture generator source revision is not the authorized baseline")
    if (
        sequence_builder.get("module") != "run_luna34_excursion_v1_multi_emitter_bridge"
        or sequence_builder.get("function") != "_training_point_sequences"
        or sequence_builder.get("source_sha256") != FIXTURE_GENERATOR_SHA256
        or point_generator.get("module") != "tpcn.spiral_benchmark"
        or point_generator.get("function") != "make_spiral_dataset"
        or point_generator.get("source_sha256") != FIXTURE_POINT_GENERATOR_SHA256
    ):
        raise ValueError("fixture generator source identity is not the authorized baseline")
    if fixture_provenance.get("generation_execution_revision") != FIXTURE_GENERATION_EXECUTION_REVISION:
        raise ValueError("fixture generation execution revision is not the recorded baseline")
    if fixture_provenance.get("fixture_json_sha256") != FIXTURE_FILE_SHA256:
        raise ValueError("fixture provenance full-file SHA-256 is not the pinned value")
    if fixture_file_sha256 != fixture_provenance["fixture_json_sha256"]:
        raise ValueError("fixture JSON full-file SHA-256 differs from provenance")
    generation_parameters = generator["point_generation_parameters"]
    if (
        generation_parameters.get("examples_per_class") != 16
        or generation_parameters.get("train_seed") != "12007 + seed"
        or generation_parameters.get("evaluation_seed")
        != "22017 + seed; evaluation points are not consumed"
        or generation_parameters.get("ordering")
        != "random.Random(330000 + seed).shuffle(point_sequences)"
    ):
        raise ValueError("fixture point generation parameters differ from provenance contract")
    if generation_parameters.get("spiral_config") != EXPECTED_SPIRAL_CONFIG:
        raise ValueError("fixture generator configuration differs from provenance contract")
    if "not read" not in fixture_provenance.get("data_access_boundary", ""):
        raise ValueError("fixture provenance does not preserve the label/evaluation boundary")
    runtime_provenance = fixture_provenance.get("runtime", {})
    if not all(
        runtime_provenance.get(name)
        for name in ("python_version", "python_implementation", "platform", "library_versions")
    ):
        raise ValueError("fixture runtime provenance is incomplete")
    if (
        "exact big-endian IEEE-754 binary64 hex" not in fixture["canonical_identity"]
        or "Audit values and neural outputs are excluded" not in fixture["canonical_identity"]
    ):
        raise ValueError("fixture does not declare the pinned raw-only canonical identity")
    sequences = fixture["sequences"]
    if len(sequences) != TOTAL_SEQUENCES:
        raise ValueError(f"expected {TOTAL_SEQUENCES} fixture sequences")
    expected_order = [
        (seed, sequence_index, f"c{seed:02d}-{sequence_index:03d}")
        for seed in SEEDS
        for sequence_index in range(SEQUENCES_PER_SEED)
    ]
    observed_order = [
        (item["seed"], item["sequence_index"], item["stream_id"])
        for item in sequences
    ]
    if observed_order != expected_order:
        raise ValueError("fixture seed/sequence ordering is invalid")
    for sequence in sequences:
        _validate_sequence(sequence)
        audit_bits = [
            _bits(float.fromhex(point["audit_x_plus_y"]["hex"]))
            for point in sequence["points"]
        ]
        if _digest(audit_bits) != sequence["derived_audit_sha256"]:
            raise ValueError(f"derived audit digest mismatch in {sequence['stream_id']}")
    rows = [
        row
        for sequence in sequences
        for row in _sequence_raw_rows(sequence)
    ]
    digest = _digest(rows)
    point_count = len(rows)
    if point_count != TOTAL_POINTS:
        raise ValueError(f"expected {TOTAL_POINTS} fixture points, got {point_count}")
    _validate_materialization_provenance(fixture_provenance, fixture_bytes, fixture, rows)
    if digest != FIXTURE_SHA256 or digest != fixture_provenance["canonical_fixture_sha256"]:
        raise ValueError("canonical fixture digest does not match the pinned identity")
    if fixture_provenance["sequence_order"] != [item[2] for item in expected_order]:
        raise ValueError("fixture provenance sequence order differs from retained fixture")
    if fixture_provenance["seeds"] != list(SEEDS):
        raise ValueError("fixture provenance seed values differ from retained fixture")
    if fixture_provenance["sequences_per_seed"] != SEQUENCES_PER_SEED:
        raise ValueError("fixture provenance sequence count differs from retained fixture")
    if fixture_provenance["canonical_row_count"] != TOTAL_POINTS:
        raise ValueError("fixture provenance point count differs from retained fixture")
    point_counts = fixture_provenance["point_counts"]
    if [
        (item["stream_id"], item["point_count"])
        for item in point_counts
    ] != [(item["stream_id"], item["point_count"]) for item in sequences]:
        raise ValueError("fixture provenance point counts differ from retained fixture")
    return fixture, fixture_provenance


def experiment_config() -> dict[str, Any]:
    return {
        "schema": "TPCN-LUNA44-ACP0008-CANONICAL-FIXTURE-REBASELINE-1",
        "authorization_revision": AUTHORIZATION_REVISION,
        "authorization_handoff_sha256": AUTHORIZATION_HANDOFF_SHA256,
        "fixture": {
            "revision": FIXTURE_REVISION,
            "canonical_sha256": FIXTURE_SHA256,
            "file_sha256": FIXTURE_FILE_SHA256,
            "provenance_manifest_path": FIXTURE_PROVENANCE_PATH.as_posix(),
            "provenance_manifest_revision": FIXTURE_PROVENANCE_REVISION,
            "provenance_manifest_sha256": FIXTURE_PROVENANCE_SHA256,
            "provenance_manifest_git_blob": FIXTURE_PROVENANCE_GIT_BLOB,
            "seeds": list(SEEDS),
            "sequences_per_seed": SEQUENCES_PER_SEED,
            "total_sequences": TOTAL_SEQUENCES,
            "total_points": TOTAL_POINTS,
            "generator_source_revision": FIXTURE_GENERATOR_REVISION,
            "generator_source_sha256": FIXTURE_GENERATOR_SHA256,
            "point_generator_source_sha256": FIXTURE_POINT_GENERATOR_SHA256,
            "input_fields": ["x", "y", "t"],
            "audit_field_excluded_from_identity": "audit_x_plus_y",
        },
        "floating_point_policy": {
            "formula": FLOAT_POLICY_FORMULA,
            "multiplier": FLOAT_TOLERANCE_MULTIPLIER,
            "epsilon": sys.float_info.epsilon,
            "raw_identity": "exact big-endian IEEE-754 binary64 bits",
            "derived_input": "recompute float(x) + float(y) independently per arm and replay",
            "decimal_hex": "decimal and float.hex() must decode to bitwise-identical binary64",
            "numerical_checks": {
                "ordinary_emission": (
                    "polarity * (a_min + (a_max-a_min) * "
                    "clamp((m_peak-theta_e)/(theta_m-theta_e), 0, 1))"
                ),
                "model_b_payload": "math.tanh(canonical_emission.payload)",
                "edge_arrival": (
                    "transfer.timestamp ~= emission.timestamp + 1.0 under formula; "
                    "transfer.timestamp > emission.timestamp exactly"
                ),
                "relay_dt": (
                    "trace.elapsed equals captured event timestamp minus captured "
                    "prior relay neuron clock exactly"
                ),
                "relay_decay": (
                    "x_decay=clip(x_before*exp(-decay_rate*dt)); "
                    "z_decay=z_before*exp(-decay_rate_z*dt)"
                ),
                "relay_input": (
                    "x_input=clip(x_decay+input); integrate z only when "
                    "mode_before=N and abs(x_input)<theta_e"
                ),
                "relay_discharge": (
                    "when integrated, abs(z_input)>=theta_z, and "
                    "x_input*z_input>=0, discharge sign(z_input)*theta_z; "
                    "compare post-discharge x/z"
                ),
                "relay_classification": (
                    "integrated_discharge iff independent recurrence admits an "
                    "ordinary episode with nonzero integrated discharge"
                ),
                "exact_criteria": [
                    "raw identities, route event IDs/endpoints/path/lineage, batching, event order, and replay digests",
                    "strict-future edge arrival and exact captured dt",
                ],
                "tolerance_criteria": [
                    "ordinary emission payload reconstruction",
                    "Model-B payload and one-unit route arrival timestamps",
                    "relay state recurrence fields",
                ],
            },
        },
        "arms": {
            "DISABLED": {"relay_integration": None},
            "DEFAULT": {"relay_decay_rate_z": DEFAULT_DECAY_RATE_Z},
            "CALIBRATED": {"relay_decay_rate_z": CALIBRATED_DECAY_RATE_Z},
            "comparison_boundary": (
                "Only relay ACP-0008 integration differs; source and destination "
                "integration are disabled for every arm."
            ),
        },
        "neuron_configurations": {
            arm: {
                node: asdict(_e1_config(arm, node))
                for node in NODES
            }
            for arm in ARMS
        },
        "topology": {
            "nodes": list(NODES),
            "edges": [
                {"source": "source", "destination": "relay", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
                {"source": "relay", "destination": "destination", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
            ],
            "fan_in_limit": 2,
            "fan_out_limit": 2,
            "edge_capacity": 3,
            "routing_capacity": 3,
        },
        "runtime": {
            "neuron_event_budget": NEURON_EVENT_BUDGET,
            "queue_capacity": QUEUE_CAPACITY,
            "runtime_event_budget": RUNTIME_EVENT_BUDGET,
            "max_activity_events": MAX_ACTIVITY_EVENTS,
            "settling_horizon": SETTLING_HORIZON,
            "prediction_capacity": PREDICTION_CAPACITY,
            "prediction_expiry": PREDICTION_EXPIRY,
            "eligibility_capacity_per_ledger": ELIGIBILITY_CAPACITY,
            "neutral_reward": 0.0,
        },
        "execution": {
            "runs_per_arm": 2,
            "second_run": "full deterministic replay from fresh per-sequence state",
            "destination_condition_comparison": False,
        },
        "control_interpretation": (
            "Compare the observed per-arm relay integrated/direct emission counts "
            "for DEFAULT versus CALIBRATED and DISABLED; record a distinction only "
            "when values differ. No difference is required, and no historical count "
            "is a target."
        ),
        "verdict_rules": {
            "supported": (
                "Valid provenance, causal routing, resource bounds, and replay; "
                "calibrated integrated relay emissions reconcile to ordinary onward transfer."
            ),
            "not_supported": (
                "Valid fixture and execution contract, but no calibrated integrated "
                "relay mechanism in this new baseline."
            ),
            "blocked": "Provenance, capacity, replay, or causal/publication blocker.",
        },
    }


def _git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def _available_execution_revision() -> str:
    try:
        return _git_output("rev-parse", "HEAD")
    except Exception:
        return "unavailable"


def _runner_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _authorization_handoff_sha256() -> str:
    committed_path = f"{AUTHORIZATION_REVISION}:{AUTHORIZATION_HANDOFF_PATH.as_posix()}"
    handoff_bytes = subprocess.run(
        ["git", "show", committed_path],
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(handoff_bytes).hexdigest()


def _collect_execution_provenance() -> dict[str, Any]:
    head = _available_execution_revision()
    problems = []
    if head == "unavailable":
        problems.append("git could not return the execution HEAD")
    try:
        branch = _git_output("branch", "--show-current")
        status = _git_output("status", "--porcelain", "--untracked-files=all")
    except Exception as error:
        branch = ""
        status = ""
        problems.append(f"git environment query failed: {type(error).__name__}: {error}")
    try:
        authorization_merge_base = _git_output(
            "merge-base", AUTHORIZATION_REVISION, head
        )
        fixture_merge_base = _git_output("merge-base", FIXTURE_REVISION, head)
    except Exception as error:
        authorization_merge_base = "unavailable"
        fixture_merge_base = "unavailable"
        problems.append(f"ancestor verification failed: {type(error).__name__}: {error}")
    try:
        observed_handoff_sha256 = _authorization_handoff_sha256()
    except Exception as error:
        observed_handoff_sha256 = "unavailable"
        problems.append(f"authorization handoff unavailable: {type(error).__name__}: {error}")
    provenance = {
        "authorization_revision": AUTHORIZATION_REVISION,
        "authorization_handoff_sha256": observed_handoff_sha256,
        "authorization_merge_base": authorization_merge_base,
        "fixture_revision": FIXTURE_REVISION,
        "fixture_merge_base": fixture_merge_base,
        "branch": branch,
        "head": head,
        "execution_revision": head,
        "git_status_porcelain": [] if not status else status.splitlines(),
        "runner_file": Path(__file__).name,
        "runner_sha256": _runner_sha256(),
        "python": sys.version,
        "python_implementation": sys.implementation.name,
        "platform": platform.platform(),
        "float_info": {
            name: getattr(sys.float_info, name)
            for name in (
                "epsilon", "dig", "mant_dig", "max", "max_10_exp", "max_exp",
                "min", "min_10_exp", "min_exp", "radix", "rounds",
            )
        },
        "floating_point_tolerance_rule": {
            "formula": FLOAT_POLICY_FORMULA,
            "multiplier": FLOAT_TOLERANCE_MULTIPLIER,
            "epsilon": sys.float_info.epsilon,
        },
    }
    if observed_handoff_sha256 != AUTHORIZATION_HANDOFF_SHA256:
        problems.append("authorization handoff hash differs from pinned authorization")
    if authorization_merge_base != AUTHORIZATION_REVISION:
        problems.append("authorization revision is not an ancestor")
    if fixture_merge_base != FIXTURE_REVISION:
        problems.append("fixture revision is not an ancestor")
    if status:
        problems.append("worktree is not clean")
    if problems:
        provenance["validation_problems"] = problems
        raise ProvenanceError("; ".join(problems), provenance)
    return provenance


def _topology() -> BoundedTopology:
    return BoundedTopology.from_edges(
        NODES,
        (
            Edge("source", "relay", 1.0, edge_weight=1.0, divider_strength=1.0, reference=0.0),
            Edge("relay", "destination", 1.0, edge_weight=1.0, divider_strength=1.0, reference=0.0),
        ),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=3,
        routing_capacity=3,
    )


def _relay_integration(arm: str) -> IntegrationConfig | None:
    if arm == "DISABLED":
        return None
    if arm == "DEFAULT":
        return IntegrationConfig()
    if arm == "CALIBRATED":
        return IntegrationConfig(decay_rate_z=CALIBRATED_DECAY_RATE_Z)
    raise ValueError(f"unknown condition {arm!r}")


def _e1_config(arm: str, node: str) -> E1Config:
    return E1Config(
        event_budget=NEURON_EVENT_BUDGET,
        integration=_relay_integration(arm) if node == "relay" else None,
    )


def _environment_record(provenance: dict[str, Any]) -> dict[str, Any]:
    return {
        "python": provenance.get("python", sys.version),
        "python_implementation": provenance.get(
            "python_implementation", sys.implementation.name
        ),
        "platform": provenance.get("platform", platform.platform()),
        "float_info": provenance.get(
            "float_info",
            {
                name: getattr(sys.float_info, name)
                for name in (
                    "epsilon", "dig", "mant_dig", "max", "max_10_exp", "max_exp",
                    "min", "min_10_exp", "min_exp", "radix", "rounds",
                )
            },
        ),
    }


def _artifact_metadata(
    provenance: dict[str, Any],
    fixture_source_provenance: dict[str, Any],
    config_digest: str,
) -> dict[str, Any]:
    execution_revision = provenance.get("execution_revision") or "unavailable"
    return {
        "authorization_revision": AUTHORIZATION_REVISION,
        "authorization_handoff_sha256": AUTHORIZATION_HANDOFF_SHA256,
        "fixture_revision": FIXTURE_REVISION,
        "fixture_sha256": FIXTURE_SHA256,
        "runner_revision": execution_revision,
        "execution_revision": execution_revision,
        "runner_sha256": provenance.get("runner_sha256", _runner_sha256()),
        "config_digest": config_digest,
        "fixture_source_provenance": fixture_source_provenance,
        "source_generator_provenance": fixture_source_provenance.get("generator", {}),
        "environment": _environment_record(provenance),
        "provenance": provenance,
    }


def _trace_record(item: tuple[Any, ...]) -> dict[str, Any]:
    if len(item) == 12:
        names = (
            "timestamp", "source", "destination", "event_type", "payload",
            "sequence", "event_id", "lineage_id", "causal_roots", "route_depth",
            "route_path", "roots_truncated",
        )
    elif len(item) == 11 and item[3] == "excursion_emission":
        names = (
            "timestamp", "source", "destination", "event_type", "payload",
            "event_id", "sequence", "episode_id", "lineage_id",
            "causal_roots", "roots_truncated",
        )
    else:
        raise ValueError(f"unrecognized runtime trace row with {len(item)} fields")
    return {key: _jsonable(value) for key, value in zip(names, item)}


def _reconcile_route_events(
    enqueued_events: list[dict[str, Any]],
    reception_events: list[dict[str, Any]],
) -> dict[str, Any]:
    enqueued_by_sequence: dict[int, list[dict[str, Any]]] = {}
    reception_by_sequence: dict[int, list[dict[str, Any]]] = {}
    for item in enqueued_events:
        enqueued_by_sequence.setdefault(item["queue_sequence"], []).append(item)
    for item in reception_events:
        reception_by_sequence.setdefault(item["queue_sequence"], []).append(item)

    checks = []
    matched_count = 0
    payload_mismatch_count = 0
    timing_mismatch_count = 0
    route_path_mismatch_count = 0
    identity_mismatch_count = 0
    provenance_mismatch_count = 0
    event_id_mismatch_count = 0
    for queue_sequence, enqueued_rows in enqueued_by_sequence.items():
        received_rows = reception_by_sequence.get(queue_sequence, [])
        if len(enqueued_rows) != 1 or len(received_rows) != 1:
            checks.append(
                {
                    "event_id": enqueued_rows[0]["event_id"],
                    "queue_sequence": queue_sequence,
                    "matches": False,
                    "enqueue_count": len(enqueued_rows),
                    "reception_count": len(received_rows),
                    "reason": "queue admission identity is not one-to-one",
                }
            )
            continue

        enqueued = enqueued_rows[0]
        received = received_rows[0]
        identity_matches = (
            enqueued["event_id"] == received["event_id"]
            and enqueued["queue_sequence"] == received["queue_sequence"]
            and enqueued["source"] == received["source"]
            and enqueued["destination"] == received["receiver_node"]
            and enqueued["destination"] == received["destination"]
        )
        timing_matches = _bits(
            float(enqueued["scheduled_delivery_timestamp"])
        ) == _bits(float(received["reception_timestamp"])) and (
            _bits(float(received["scheduled_delivery_timestamp"]))
            == _bits(float(enqueued["scheduled_delivery_timestamp"]))
            and float(enqueued["enqueue_timestamp"])
            < float(enqueued["scheduled_delivery_timestamp"])
        )
        payload_matches = (
            enqueued["payload_bits"] == received["payload_bits"]
            == _bits(float(enqueued["payload"]))
            == _bits(float(received["payload"]))
        )
        route_path_matches = (
            enqueued["route_path"] == received["route_path"]
            and enqueued["route_depth"] == received["route_depth"]
        )
        provenance_matches = (
            enqueued["event_type"] == received["event_type"]
            and enqueued["lineage_id"] == received["lineage_id"]
            and enqueued["causal_roots"] == received["causal_roots"]
            and enqueued["originating_emission_id"]
            == received["originating_emission_id"]
            and enqueued["roots_truncated"] == received["roots_truncated"]
        )
        identity_matches &= enqueued["source"] == received["source"]
        event_id_mismatch_count += enqueued["event_id"] != received["event_id"]
        payload_mismatch_count += not payload_matches
        timing_mismatch_count += not timing_matches
        route_path_mismatch_count += not route_path_matches
        identity_mismatch_count += not identity_matches
        provenance_mismatch_count += not provenance_matches
        matches = (
            identity_matches
            and timing_matches
            and payload_matches
            and route_path_matches
            and provenance_matches
        )
        matched_count += matches
        checks.append(
            {
                "event_id": enqueued["event_id"],
                "reception_event_id": received["event_id"],
                "queue_sequence": queue_sequence,
                "matches": matches,
                "identity_matches": identity_matches,
                "enqueue_source": enqueued["source"],
                "reception_source": received["source"],
                "queue_sequence_matches": (
                    enqueued["queue_sequence"] == received["queue_sequence"]
                ),
                "timing_matches": timing_matches,
                "payload_bits_match": payload_matches,
                "route_path_matches": route_path_matches,
                "provenance_matches": provenance_matches,
                "scheduled_delivery_timestamp": enqueued[
                    "scheduled_delivery_timestamp"
                ],
                "reception_timestamp": received["reception_timestamp"],
                "enqueue_payload_bits": enqueued["payload_bits"],
                "reception_payload_bits": received["payload_bits"],
                "enqueue_route_path": enqueued["route_path"],
                "reception_route_path": received["route_path"],
            }
        )

    duplicate_count = sum(
        max(0, len(rows) - 1) for rows in reception_by_sequence.values()
    )
    orphan_reception_count = sum(
        len(rows)
        for queue_sequence, rows in reception_by_sequence.items()
        if queue_sequence not in enqueued_by_sequence
    )
    unmatched_enqueue_count = sum(
        len(rows) for rows in enqueued_by_sequence.values()
    ) - matched_count
    duplicate_enqueue_count = sum(
        max(0, len(rows) - 1) for rows in enqueued_by_sequence.values()
    )
    for queue_sequence, rows in reception_by_sequence.items():
        if queue_sequence not in enqueued_by_sequence:
            checks.append({
                "queue_sequence": queue_sequence,
                "event_id": rows[0]["event_id"],
                "matches": False,
                "enqueue_count": 0,
                "reception_count": len(rows),
                "reason": "orphan reception",
            })
    mismatch_count = (
        payload_mismatch_count
        + timing_mismatch_count
        + route_path_mismatch_count
        + identity_mismatch_count
        + provenance_mismatch_count
        + event_id_mismatch_count
    )
    reconciles = (
        not unmatched_enqueue_count
        and not orphan_reception_count
        and not duplicate_count
        and not mismatch_count
        and matched_count == len(enqueued_events) == len(reception_events)
    )
    return {
        "enqueued_count": len(enqueued_events),
        "received_count": len(reception_events),
        "matched_count": matched_count,
        "unmatched_enqueue_count": unmatched_enqueue_count,
        "orphan_reception_count": orphan_reception_count,
        "duplicate_count": duplicate_count,
        "duplicate_reception_count": duplicate_count,
        "duplicate_enqueue_count": duplicate_enqueue_count,
        "payload_mismatch_count": payload_mismatch_count,
        "timing_mismatch_count": timing_mismatch_count,
        "route_path_mismatch_count": route_path_mismatch_count,
        "identity_mismatch_count": identity_mismatch_count,
        "provenance_mismatch_count": provenance_mismatch_count,
        "event_id_mismatch_count": event_id_mismatch_count,
        "mismatch_count": mismatch_count,
        "reconciles": reconciles,
        "payload_identity_policy": (
            "exact IEEE-754 binary64 bits; routing transformation occurs before "
            "enqueue and is not applied again at reception"
        ),
        "checks": checks,
    }


def _emission_record(emission: Any) -> dict[str, Any]:
    return {
        "event_id": emission.event_id,
        "sequence": emission.sequence,
        "source": emission.source,
        "timestamp": float(emission.timestamp),
        "payload": float(emission.payload),
        "lineage_id": emission.lineage_id,
        "episode_id": emission.episode_id,
    }


def _canonical_emission_checks(
    emissions: list[dict[str, Any]],
    config: E1Config,
) -> list[dict[str, Any]]:
    checks = []
    for emission in emissions:
        peak = float(emission["m_peak"])
        polarity = emission["polarity"]
        if polarity not in (-1, 1):
            checks.append(
                {
                    "event_id": emission["event_id"],
                    "m_peak": peak,
                    "matches": False,
                    "reason": "missing captured ordinary polarity",
                }
            )
            continue
        fraction = max(
            0.0,
            min(
                1.0,
                (peak - config.theta_e) / (config.theta_m - config.theta_e),
            ),
        )
        amplitude = config.a_min + (config.a_max - config.a_min) * fraction
        expected = float(polarity) * amplitude
        check = _float_check(float(emission["payload"]), expected)
        checks.append(
            {
                "event_id": emission["event_id"],
                "m_peak": peak,
                "polarity": polarity,
                "observed_payload": float(emission["payload"]),
                "expected_payload": expected,
                **check,
            }
        )
    return checks


def _relay_recurrence_checks(
    relay_trace: list[dict[str, Any]],
    relay_state_trajectory: list[dict[str, Any]],
    config: E1Config,
) -> list[dict[str, Any]]:
    integration = config.integration
    if integration is None:
        if relay_trace:
            raise RuntimeError("disabled relay unexpectedly produced integration traces")
        return []
    relay_external_events = [
        item
        for item in relay_state_trajectory
        if item["event_type"] == EventType.EXCURSION.value
    ]
    if len(relay_external_events) != len(relay_trace):
        raise RuntimeError("relay state captures do not align with integration traces")
    checks = []
    for entry, captured in zip(relay_trace, relay_external_events):
        timestamp = float(captured["timestamp"])
        prior_clock = float(captured["prior_clock"])
        dt_expected = timestamp - prior_clock
        dt_observed = float(entry["elapsed"])
        dt_check = _float_check(dt_observed, dt_expected)
        dt_check["exact_match"] = _bits(dt_observed) == _bits(dt_expected)
        dt_check["timestamp"] = timestamp
        dt_check["prior_clock"] = prior_clock

        x_before = float(captured["x_before"])
        z_before = (
            0.0
            if captured["z_before"] is None
            else float(captured["z_before"])
        )
        input_value = float(captured["payload"])
        mode_before = captured["mode_before"]

        def clip_x(value: float) -> float:
            return max(-config.x_max, min(config.x_max, value))

        expected_x_decay = clip_x(
            x_before * math.exp(-config.decay_rate * dt_expected)
        )
        expected_z_decay = (
            z_before
            if integration is None
            else z_before * math.exp(-integration.decay_rate_z * dt_expected)
        )
        expected_x_input = clip_x(expected_x_decay + input_value)
        should_integrate = (
            integration is not None
            and mode_before == "N"
            and abs(expected_x_input) < config.theta_e
        )
        expected_z_input = expected_z_decay
        if should_integrate:
            assert integration is not None
            expected_z_input = max(
                -integration.z_max,
                min(
                    integration.z_max,
                    expected_z_decay + integration.input_gain * input_value,
                ),
            )
        expected_discharge = 0.0
        if (
            should_integrate
            and integration is not None
            and abs(expected_z_input) >= integration.discharge_quantum
            and expected_x_input * expected_z_input >= 0.0
        ):
            expected_discharge = math.copysign(
                integration.discharge_quantum, expected_z_input
            )
        expected_x_post = clip_x(expected_x_input + expected_discharge)
        expected_z_post = expected_z_input - expected_discharge
        expected_admitted = (
            mode_before == "N"
            and config.theta_e <= abs(expected_x_post) < config.theta_m
        )
        observed_admitted = entry["admitted_episode_id"] is not None
        expected_classification = (
            "integrated_discharge"
            if expected_admitted and expected_discharge != 0.0
            else "direct"
            if expected_admitted
            else "none"
        )
        checks.append(
            {
                "event_id": captured["event_id"],
                "trace_emission_id": entry.get("emission_id"),
                "timestamp": timestamp,
                "input_value": input_value,
                "dt": dt_check,
                "timestamp_matches_trace": _bits(timestamp) == _bits(float(entry["timestamp"])),
                "input_matches_trace": _bits(input_value) == _bits(float(entry["input_value"])),
                "mode_matches_trace": mode_before == entry["mode_before"],
                "x_before_decay": _float_check(
                    float(entry["x_before_decay"]), x_before
                ),
                "z_before_decay": _float_check(
                    float(entry["z_before_decay"]), z_before
                ),
                "x_after_decay": _float_check(
                    float(entry["x_after_decay"]), expected_x_decay
                ),
                "z_after_decay": _float_check(
                    float(entry["z_after_decay"]), expected_z_decay
                ),
                "x_after_input": _float_check(
                    float(entry["x_after_input"]), expected_x_input
                ),
                "z_after_input": _float_check(
                    float(entry["z_after_input"]), expected_z_input
                ),
                "integrated": bool(entry["integrated"]) == should_integrate,
                "discharge_amount": _float_check(
                    float(entry["discharge_amount"]), expected_discharge
                ),
                "x_post_discharge": _float_check(
                    float(entry["x_post_discharge"]), expected_x_post
                ),
                "z_post_discharge": _float_check(
                    float(entry["z_post_discharge"]), expected_z_post
                ),
                "crossed_theta_e": bool(entry["crossed_theta_e"])
                == (abs(expected_x_post) >= config.theta_e),
                "admitted_episode": observed_admitted == expected_admitted,
                "expected_classification": expected_classification,
                "observed_classification": entry["classification"],
                "classification_matches": (
                    entry["classification"] == expected_classification
                ),
            }
        )
        checks[-1]["matches"] = (
            checks[-1]["dt"]["exact_match"]
            and checks[-1]["timestamp_matches_trace"]
            and checks[-1]["input_matches_trace"]
            and checks[-1]["mode_matches_trace"]
            and checks[-1]["integrated"]
            and checks[-1]["crossed_theta_e"]
            and checks[-1]["admitted_episode"]
            and checks[-1]["classification_matches"]
            and all(
                checks[-1][name]["matches"]
                for name in (
                    "x_before_decay",
                    "z_before_decay",
                    "x_after_decay",
                    "z_after_decay",
                    "x_after_input",
                    "z_after_input",
                    "discharge_amount",
                    "x_post_discharge",
                    "z_post_discharge",
                )
            )
        )
    return checks


def _classify_relay_emissions(
    relay_emissions: list[dict[str, Any]],
    relay_integration_trace: list[dict[str, Any]],
    recurrence_checks: list[dict[str, Any]],
    *,
    integration_enabled: bool,
) -> list[dict[str, Any]]:
    checks_by_emission = {
        item["trace_emission_id"]: item
        for item in recurrence_checks
        if item.get("trace_emission_id") is not None
    }
    del relay_integration_trace
    classified = []
    for emission in relay_emissions:
        recurrence = checks_by_emission.get(emission["event_id"])
        category = (
            "integration-mediated"
            if recurrence is not None
            and recurrence["expected_classification"] == "integrated_discharge"
            else "direct"
        )
        classified.append(
            {
                **emission,
                "classification": category,
                "integration_trace_check": recurrence,
                "classification_matches": (
                    recurrence is not None
                    and recurrence["matches"]
                    if integration_enabled
                    else recurrence is None or recurrence["matches"]
                ),
            }
        )
    return classified


class _ResourceAudit:
    def __init__(self) -> None:
        self.ledgers: dict[str, dict[str, int]] = {}
        self.eligibility_peak = 0
        self.prediction_peak = 0

    def register(self, ledger: EligibilityLedger) -> None:
        self.ledgers[ledger.ledger_id] = {
            "capacity": ledger.max_traces,
            "peak": len(ledger.traces),
        }

    def observe_ledger(self, ledger: EligibilityLedger) -> None:
        item = self.ledgers[ledger.ledger_id]
        item["peak"] = max(item["peak"], len(ledger.traces))
        self.eligibility_peak = max(self.eligibility_peak, item["peak"])


def _run_character(*, arm: str, sequence: dict[str, Any]) -> dict[str, Any]:
    """Execute one isolated retained-fixture sequence under one fixed arm."""
    _validate_sequence(sequence)
    seed = sequence["seed"]
    sequence_index = sequence["sequence_index"]
    stream_id = sequence["stream_id"]
    point_inputs = []
    contributions_by_batch: dict[int, list[tuple[float, float]]] = {}
    raw_identity = _sequence_raw_rows(sequence)
    for point in sequence["points"]:
        x = float.fromhex(point["x"]["hex"])
        y = float.fromhex(point["y"]["hex"])
        timestamp = float.fromhex(point["t"]["hex"])
        derived = float(x) + float(y)
        audit = float.fromhex(point["audit_x_plus_y"]["hex"])
        check = _float_check(derived, audit)
        if not check["matches"]:
            raise ValueError(f"derived input does not match retained audit for {stream_id}")
        point_inputs.append(
            {
                "seed": seed,
                "sequence_index": sequence_index,
                "stream_id": stream_id,
                "point_index": point["point_index"],
                "batch_ordinal": point["batch_ordinal"],
                "x": point["x"],
                "y": point["y"],
                "t": point["t"],
                "audit_x_plus_y": point["audit_x_plus_y"],
                "computed_source_value": _float_record(derived),
                "audit_comparison": check,
            }
        )
        contributions_by_batch.setdefault(point["batch_ordinal"], []).append(
            (timestamp, derived)
        )
    batch_values = tuple(
        tuple(contributions_by_batch[index])
        for index in range(len(contributions_by_batch))
    )
    input_digest = _digest(
        {
            "fixture_sequence_sha256": sequence["source_sha256"],
            "point_inputs": point_inputs,
        }
    )

    node_configs = {node: _e1_config(arm, node) for node in NODES}
    integration_configuration = {
        node: node_configs[node].integration for node in NODES
    }
    neurons = tuple(
        MultiExcursionNeuron(node, config=node_configs[node])
        for node in NODES
    )
    topology = _topology()
    character_id = stream_id
    namespace = f"luna44-{arm.lower()}-seed-{seed}"
    runtime = ExcursionCharacterRuntime(
        neurons,
        topology,
        queue_capacity=QUEUE_CAPACITY,
        event_budget=RUNTIME_EVENT_BUDGET,
        settling_horizon=SETTLING_HORIZON,
        prediction_capacity=PREDICTION_CAPACITY,
        prediction_expiry=PREDICTION_EXPIRY,
        max_activity_events=MAX_ACTIVITY_EVENTS,
        namespace=namespace,
        eligibility_capacity=ELIGIBILITY_CAPACITY,
    )
    audit = _ResourceAudit()
    snapshots: dict[str, dict[str, Any]] = {}
    relay_state_trajectory: list[dict[str, Any]] = []
    emission_peaks: dict[str, dict[str, Any]] = {}
    enqueue_events: list[dict[str, Any]] = []
    reception_events: list[dict[str, Any]] = []
    enqueue_by_sequence: dict[int, dict[str, Any]] = {}
    active_receiver_context: Any = None
    original_reset = MultiExcursionNeuron.reset
    original_receive_event = MultiExcursionNeuron.receive_event
    original_emit_ordinary = MultiExcursionNeuron._emit_ordinary
    original_handle_m_internal = MultiExcursionNeuron._handle_m_internal
    original_push_propagated = EventQueue.push_propagated
    original_attach = ExcursionCharacterRuntime._attach
    original_process_one = ExcursionCharacterRuntime._process_one
    original_ledger_init = EligibilityLedger.__init__
    original_record_activity = EligibilityLedger.record_activity
    original_create_prediction = LocalPredictor.create_prediction

    def capture_reset(neuron: MultiExcursionNeuron, *, timestamp: float = 0.0) -> None:
        snapshots[neuron.neuron_id] = {
            "emissions": [_emission_record(item) for item in neuron.emissions],
            "integration_trace": [_jsonable(item) for item in neuron.integration_trace],
            "x": float(neuron.state),
            "z": None if neuron.integration_state is None else float(neuron.integration_state),
            "processed_events": neuron.processed_event_count,
            "last_update_timestamp": float(neuron.last_update_timestamp),
        }
        original_reset(neuron, timestamp=timestamp)

    def capture_receive(
        neuron: MultiExcursionNeuron,
        event: Event,
        queue: Any = None,
    ) -> Any:
        before_x = float(neuron.state)
        before_z = None if neuron.integration_state is None else float(neuron.integration_state)
        prior_clock = float(neuron.clock.timestamp)
        processed_before = neuron.processed_event_count
        mode_before = neuron.mode.value
        result = original_receive_event(neuron, event, queue)
        if event.event_type == EventType.EXCURSION:
            if neuron.processed_event_count != processed_before + 1:
                raise RuntimeError("receiver did not process the routed event")
            context = active_receiver_context
            if context is None:
                raise RuntimeError("receiver event has no independently captured route context")
            reception_events.append(
                {
                    "event_id": event.event_id,
                    "queue_sequence": event.sequence,
                    "source": event.source,
                    "destination": event.destination,
                    "receiver_node": neuron.neuron_id,
                    "event_type": _jsonable(event.event_type),
                    "scheduled_delivery_timestamp": float(event.timestamp),
                    "reception_timestamp": float(neuron.clock.timestamp),
                    "payload": float(event.payload),
                    "payload_bits": _bits(float(event.payload)),
                    "route_path": list(context.route_path),
                    "route_depth": context.route_depth,
                    "lineage_id": event.lineage_id,
                    "causal_roots": list(context.causal_roots),
                    "roots_truncated": context.roots_truncated,
                    "originating_emission_id": event.event_id,
                    "receiver_state_transition": {
                        "event_sequence": event.sequence,
                        "processed_events_before": processed_before,
                        "processed_events_after": neuron.processed_event_count,
                        "x_before": before_x,
                        "x_after": float(neuron.state),
                        "z_before": before_z,
                        "z_after": (
                            None
                            if neuron.integration_state is None
                            else float(neuron.integration_state)
                        ),
                    },
                }
            )
        if neuron.neuron_id == "relay":
            relay_state_trajectory.append(
                {
                    "timestamp": float(event.timestamp),
                    "event_id": event.event_id,
                    "event_type": _jsonable(event.event_type),
                    "payload": _jsonable(event.payload),
                    "prior_clock": prior_clock,
                    "mode_before": mode_before,
                    "x_before": before_x,
                    "z_before": before_z,
                    "x_after": float(neuron.state),
                    "z_after": (
                        None
                        if neuron.integration_state is None
                        else float(neuron.integration_state)
                    ),
                    "mode_after": neuron.mode.value,
                }
            )
        return result

    def capture_enqueue(
        queue: EventQueue[Event],
        emission_time: Any,
        source: str,
        destination: str,
        event_type: Any,
        payload: Any,
        delay: Any,
        **kwargs: Any,
    ) -> Event:
        queued = original_push_propagated(
            queue, emission_time, source, destination, event_type, payload, delay,
            **kwargs,
        )
        if queue is runtime.queue and queued.event_type == EventType.EXCURSION:
            row = {
                "event_id": queued.event_id,
                "queue_sequence": queued.sequence,
                "source": queued.source,
                "destination": queued.destination,
                "event_type": _jsonable(queued.event_type),
                "enqueue_timestamp": float(emission_time),
                "scheduled_delivery_timestamp": float(queued.timestamp),
                "timestamp": float(queued.timestamp),
                "payload": float(queued.payload),
                "payload_bits": _bits(float(queued.payload)),
                "lineage_id": queued.lineage_id,
                "originating_emission_id": kwargs.get("event_id"),
            }
            enqueue_events.append(row)
            enqueue_by_sequence[queued.sequence] = row
        return queued

    def capture_attach(
        character_runtime: ExcursionCharacterRuntime,
        queued: Event,
        context: Any,
    ) -> None:
        original_attach(character_runtime, queued, context)
        if character_runtime is runtime and queued.event_type == EventType.EXCURSION:
            row = enqueue_by_sequence[queued.sequence]
            row.update({
                "route_path": list(context.route_path),
                "route_depth": context.route_depth,
                "causal_roots": list(context.causal_roots),
                "roots_truncated": context.roots_truncated,
            })

    def capture_process_one(
        character_runtime: ExcursionCharacterRuntime,
        event: Event,
    ) -> None:
        nonlocal active_receiver_context
        previous_context = active_receiver_context
        active_receiver_context = character_runtime._sidecar.get(event.sequence)
        try:
            original_process_one(character_runtime, event)
        finally:
            active_receiver_context = previous_context

    def capture_ordinary_emit(neuron: MultiExcursionNeuron, queue: Any = None) -> Any:
        peak = max(float(neuron.m_peak), abs(float(neuron.state)))
        polarity = neuron.captured_polarity
        emission = original_emit_ordinary(neuron, queue)
        if emission is not None:
            emission_peaks[emission.event_id] = {
                "m_peak": peak,
                "polarity": polarity,
            }
        return emission

    def capture_m_internal(
        neuron: MultiExcursionNeuron,
        kind: Any,
        queue: Any = None,
    ) -> Any:
        peak = max(float(neuron.m_peak), abs(float(neuron.state)))
        polarity = neuron.captured_polarity
        if polarity is None:
            polarity = 1 if neuron.state >= 0.0 else -1
        emission = original_handle_m_internal(neuron, kind, queue)
        if emission is not None:
            emission_peaks[emission.event_id] = {
                "m_peak": peak,
                "polarity": polarity,
            }
        return emission

    def ledger_init(ledger: EligibilityLedger, *args: Any, **kwargs: Any) -> None:
        original_ledger_init(ledger, *args, **kwargs)
        audit.register(ledger)

    def record_activity(ledger: EligibilityLedger, event: Event) -> Any:
        result = original_record_activity(ledger, event)
        audit.observe_ledger(ledger)
        return result

    def create_prediction(
        predictor: LocalPredictor,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        prediction = original_create_prediction(predictor, *args, **kwargs)
        audit.prediction_peak = max(audit.prediction_peak, predictor.outstanding_count)
        return prediction

    try:
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(MultiExcursionNeuron, "reset", capture_reset))
            stack.enter_context(
                mock.patch.object(MultiExcursionNeuron, "receive_event", capture_receive)
            )
            stack.enter_context(
                mock.patch.object(EventQueue, "push_propagated", capture_enqueue)
            )
            stack.enter_context(
                mock.patch.object(ExcursionCharacterRuntime, "_attach", capture_attach)
            )
            stack.enter_context(
                mock.patch.object(
                    ExcursionCharacterRuntime,
                    "_process_one",
                    capture_process_one,
                )
            )
            stack.enter_context(
                mock.patch.object(MultiExcursionNeuron, "_emit_ordinary", capture_ordinary_emit)
            )
            stack.enter_context(
                mock.patch.object(
                    MultiExcursionNeuron,
                    "_handle_m_internal",
                    capture_m_internal,
                )
            )
            stack.enter_context(mock.patch.object(EligibilityLedger, "__init__", ledger_init))
            stack.enter_context(
                mock.patch.object(EligibilityLedger, "record_activity", record_activity)
            )
            stack.enter_context(
                mock.patch.object(LocalPredictor, "create_prediction", create_prediction)
            )
            runtime.start_character(
                character_id,
                sequence_index,
                timestamp=0.0,
                predictor_source="source",
                readout_sources=NODES,
                input_destination="source",
            )
            for batch in batch_values:
                runtime.admit_external_batch(batch)
            last_timestamp = batch_values[-1][-1][0] if batch_values else 0.0
            runtime_result = runtime.end_character(
                last_external_timestamp=last_timestamp,
                reward=0.0,
                reward_delay=0.0,
                reward_message_id=f"luna44-neutral-{character_id}",
            )
    except (EligibilityCapacityError, QueueCapacityError, TopologyCapacityError, BufferError):
        raise

    if set(snapshots) != set(NODES):
        raise RuntimeError("runtime teardown did not expose all neuron snapshots")
    for snapshot in snapshots.values():
        enriched = []
        for emission in snapshot["emissions"]:
            observed_peak = emission_peaks.get(emission["event_id"])
            if observed_peak is None:
                raise RuntimeError(f"emission peak missing for {emission['event_id']}")
            enriched.append({**emission, **observed_peak})
        snapshot["emissions"] = enriched
    execution = runtime_result.execution
    if (
        not execution.completed
        or execution.budget_exhausted
        or execution.pending_event_count != 0
        or runtime_result.incomplete_settling
    ):
        raise RuntimeError("runtime failed the declared bounded settling contract")
    if execution.processed_event_count > RUNTIME_EVENT_BUDGET:
        raise RuntimeError("runtime event budget exceeded")
    if (
        runtime_result.peak_queue_occupancy > QUEUE_CAPACITY
        or any(
            snapshot["processed_events"] > NEURON_EVENT_BUDGET
            or abs(snapshot["x"]) > 8.0
            or (snapshot["z"] is not None and abs(snapshot["z"]) > 4.0)
            for snapshot in snapshots.values()
        )
    ):
        raise RuntimeError("neuron state or event budget exceeded")
    if len(audit.ledgers) != len(NODES):
        raise RuntimeError("runtime did not create exactly one eligibility ledger per node")
    if any(
        item["capacity"] != ELIGIBILITY_CAPACITY
        or item["peak"] >= item["capacity"]
        for item in audit.ledgers.values()
    ):
        raise RuntimeError("eligibility ledger capacity contract failed")
    if audit.prediction_peak > PREDICTION_CAPACITY:
        raise RuntimeError("prediction capacity exceeded")

    trace_records = [_trace_record(item) for item in runtime_result.trace]
    source_emissions = snapshots["source"]["emissions"]
    relay_emissions = snapshots["relay"]["emissions"]
    destination_emissions = snapshots["destination"]["emissions"]
    relay_trace = snapshots["relay"]["integration_trace"]
    canonical_emission_checks = {
        node: _canonical_emission_checks(
            snapshots[node]["emissions"],
            node_configs[node],
        )
        for node in NODES
    }
    relay_recurrence_checks = _relay_recurrence_checks(
        relay_trace,
        relay_state_trajectory,
        node_configs["relay"],
    )
    classified_relay_emissions = _classify_relay_emissions(
        relay_emissions,
        relay_trace,
        relay_recurrence_checks,
        integration_enabled=integration_configuration["relay"] is not None,
    )
    transfers = enqueue_events
    source_transfers = [
        item for item in transfers
        if item["source"] == "source" and item["destination"] == "relay"
    ]
    relay_transfers = [
        item for item in transfers
        if item["source"] == "relay" and item["destination"] == "destination"
    ]
    source_receptions = [
        item for item in reception_events if item["receiver_node"] == "relay"
    ]
    destination_receptions = [
        item for item in reception_events if item["receiver_node"] == "destination"
    ]
    source_route_reconciliation = _reconcile_route_events(
        source_transfers,
        source_receptions,
    )
    onward_route_reconciliation = _reconcile_route_events(
        relay_transfers,
        destination_receptions,
    )
    all_route_reconciliation = _reconcile_route_events(enqueue_events, reception_events)
    expected_emissions = source_emissions + relay_emissions
    emission_by_id = {item["event_id"]: item for item in expected_emissions}
    transfer_checks = []
    for transfer in transfers:
        emission = emission_by_id.get(transfer["event_id"])
        if emission is None:
            transfer_checks.append(
                {
                    "event_id": transfer["event_id"],
                    "identity_matches": False,
                    "arrival_timestamp_check": None,
                    "model_b_check": None,
                    "strict_future": False,
                    "matches": False,
                    "reason": "orphan transfer",
                }
            )
            continue
        expected_edge = (emission["source"], "relay" if emission["source"] == "source" else "destination")
        expected_path = list(expected_edge)
        expected_timestamp = float(emission["timestamp"]) + 1.0
        arrival_check = _float_check(float(transfer["timestamp"]), expected_timestamp)
        strict_future = float(transfer["timestamp"]) > float(emission["timestamp"])
        identity_matches = (
            transfer["event_id"] == emission["event_id"]
            and transfer["source"] == expected_edge[0]
            and transfer["destination"] == expected_edge[1]
            and transfer["event_type"] == EventType.EXCURSION.value
            and transfer["route_path"] == expected_path
            and transfer["route_depth"] == 1
            and transfer["lineage_id"] == emission["lineage_id"]
        )
        expected_payload = math.tanh(float(emission["payload"]))
        model_b_check = _float_check(float(transfer["payload"]), expected_payload)
        transfer_checks.append(
            {
                "event_id": transfer["event_id"],
                "source": transfer["source"],
                "destination": transfer["destination"],
                "route_path": transfer["route_path"],
                "arrival_timestamp_observed": transfer["timestamp"],
                "arrival_timestamp_expected": expected_timestamp,
                "arrival_timestamp_check": arrival_check,
                "strict_future": strict_future,
                "identity_matches": identity_matches,
                "payload": transfer["payload"],
                "expected_model_b_payload": expected_payload,
                "model_b_check": model_b_check,
                "matches": (
                    identity_matches
                    and arrival_check["matches"]
                    and strict_future
                    and model_b_check["matches"]
                ),
            }
        )
    by_transfer_id = {
        item["event_id"]: item
        for item in transfer_checks
    }
    onward_checks = []
    for emission in classified_relay_emissions:
        transfer_check = by_transfer_id.get(emission["event_id"])
        valid_route = (
            transfer_check is not None
            and transfer_check["source"] == "relay"
            and transfer_check["destination"] == "destination"
            and transfer_check["matches"]
            and emission["classification_matches"]
        )
        onward_checks.append(
            {
                "event_id": emission["event_id"],
                "classification": emission["classification"],
                "onward_transfer_check": transfer_check,
                "matches": valid_route,
            }
        )
    source_reception_check_by_id = {
        item["event_id"]: item
        for item in source_route_reconciliation["checks"]
    }
    source_reception_checks = [
        {
            "event_id": emission["event_id"],
            "reception": next(
                (
                    item
                    for item in source_receptions
                    if item["event_id"] == emission["event_id"]
                ),
                None,
            ),
            "route_reconciliation": source_reception_check_by_id.get(
                emission["event_id"]
            ),
            "matches": (
                source_reception_check_by_id.get(
                    emission["event_id"], {}
                ).get("matches", False)
                and by_transfer_id.get(emission["event_id"], {}).get(
                    "matches", False
                )
            ),
        }
        for emission in source_emissions
    ]
    route_count_matches = (
        len(source_transfers) == len(source_emissions)
        and len(relay_transfers) == len(relay_emissions)
        and len(transfers) == len(expected_emissions)
        and len({item["event_id"] for item in transfers}) == len(transfers)
        and source_route_reconciliation["reconciles"]
        and onward_route_reconciliation["reconciles"]
        and all_route_reconciliation["reconciles"]
    )
    causality_reconciles = (
        route_count_matches
        and all(item["matches"] for item in transfer_checks)
        and all(item["matches"] for item in onward_checks)
        and all(item["matches"] for item in source_reception_checks)
        and all(item["matches"] for item in canonical_emission_checks["source"])
        and all(
            all(item["matches"] for item in checks)
            for checks in canonical_emission_checks.values()
        )
        and all(item["matches"] for item in relay_recurrence_checks)
        and all(item["classification_matches"] for item in classified_relay_emissions)
    )
    if not causality_reconciles:
        raise RoutingEvidenceError({
            "seed": seed,
            "sequence_index": sequence_index,
            "stream_id": stream_id,
            "routing_enqueue_events": enqueue_events,
            "receiver_reception_events": reception_events,
            "routing_capture_status": "reconciliation_failed",
            "routing_reconciliation": all_route_reconciliation,
        })
    signed_z_values = [
        float(entry[key])
        for entry in relay_trace
        for key in ("z_before_decay", "z_after_decay", "z_after_input", "z_post_discharge")
        if entry.get(key) is not None
    ]
    signed_z_values.extend(
        float(captured[key])
        for captured in relay_state_trajectory
        for key in ("z_before", "z_after")
        if captured.get(key) is not None
    )
    activity_count = (
        len(source_emissions) + len(relay_emissions) + len(destination_emissions)
    )
    if activity_count > MAX_ACTIVITY_EVENTS or runtime_result.emission_count != activity_count:
        raise RuntimeError("canonical readout activity count exceeded or failed reconciliation")
    record = {
        "arm": arm,
        "decay_rate_z": (
            CALIBRATED_DECAY_RATE_Z if arm == "CALIBRATED"
            else DEFAULT_DECAY_RATE_Z if arm == "DEFAULT"
            else None
        ),
        "integration_configuration": {
            node: (
                None
                if integration_configuration[node] is None
                else {
                    "decay_rate_z": integration_configuration[node].decay_rate_z,
                    "input_gain": integration_configuration[node].input_gain,
                    "discharge_quantum": integration_configuration[node].discharge_quantum,
                    "z_max": integration_configuration[node].z_max,
                }
            )
            for node in NODES
        },
        "neuron_configuration": {
            node: asdict(node_configs[node])
            for node in NODES
        },
        "seed": seed,
        "sequence_index": sequence_index,
        "stream_id": stream_id,
        "fixture_sequence_sha256": sequence["source_sha256"],
        "raw_identity": raw_identity,
        "raw_identity_sha256": _digest(raw_identity),
        "point_inputs": point_inputs,
        "input_digest": input_digest,
        "input_batches": batch_values,
        "source_emissions": source_emissions,
        "relay_emissions": classified_relay_emissions,
        "destination_emissions": destination_emissions,
        "relay_state_trajectory": relay_state_trajectory,
        "relay_integration_trace": relay_trace,
        "relay_recurrence_checks": relay_recurrence_checks,
        "relay_recurrence_reconciles": all(
            item["matches"] for item in relay_recurrence_checks
        ),
        "canonical_emission_checks": canonical_emission_checks,
        "routed_signal_transfers": transfers,
        "routing_enqueue_events": enqueue_events,
        "receiver_reception_events": reception_events,
        "routing_capture_sources": {
            "enqueue": (
                "EventQueue.push_propagated after successful queue admission; "
                "route context from successful ExcursionCharacterRuntime._attach"
            ),
            "reception": (
                "events successfully consumed by MultiExcursionNeuron.receive_event"
            ),
        },
        "routing_stream_digests": {
            "enqueue": _digest(enqueue_events),
            "reception": _digest(reception_events),
        },
        "source_to_relay_receptions": source_receptions,
        "destination_receptions": destination_receptions,
        "routing_reconciliation": {
            "all_routes": all_route_reconciliation,
            "source_to_relay": source_route_reconciliation,
            "relay_to_destination": onward_route_reconciliation,
            "reconciles": (
                source_route_reconciliation["reconciles"]
                and onward_route_reconciliation["reconciles"]
                and all_route_reconciliation["reconciles"]
            ),
        },
        "transfer_checks": transfer_checks,
        "source_reception_checks": source_reception_checks,
        "relay_onward_transfer_checks": onward_checks,
        "runtime_events": trace_records,
        "resource_high_water": {
            "queue_capacity": QUEUE_CAPACITY,
            "queue_peak": runtime_result.peak_queue_occupancy,
            "runtime_event_budget": RUNTIME_EVENT_BUDGET,
            "processed_events": execution.processed_event_count,
            "pending_events": execution.pending_event_count,
            "per_neuron_event_budget": NEURON_EVENT_BUDGET,
            "neuron_processed_events": {
                node: snapshots[node]["processed_events"] for node in NODES
            },
            "max_activity_events": MAX_ACTIVITY_EVENTS,
            "activity_count": activity_count,
            "activity_high_water": activity_count,
            "prediction_capacity": PREDICTION_CAPACITY,
            "prediction_peak": audit.prediction_peak,
            "eligibility_capacity_per_ledger": ELIGIBILITY_CAPACITY,
            "eligibility_ledgers": [
                {"ledger_id": key, **value}
                for key, value in sorted(audit.ledgers.items())
            ],
            "eligibility_peak": audit.eligibility_peak,
            "topology_edge_capacity": 3,
            "topology_routing_capacity": 3,
            "observed_route_transfers": len(transfers),
            "observed_receiver_receptions": len(reception_events),
        },
        "settling": {
            "completed": execution.completed,
            "termination_reason": execution.termination_reason,
            "last_event_timestamp": execution.last_event_timestamp,
            "horizon": last_timestamp + SETTLING_HORIZON,
        },
        "state_at_teardown": snapshots,
        "counts": {
            "source_inputs": len(point_inputs),
            "source_emissions": len(source_emissions),
            "source_to_relay_transfers": len(source_transfers),
            "source_to_relay_receptions": len(source_receptions),
            "source_to_relay_enqueued": source_route_reconciliation["enqueued_count"],
            "source_to_relay_received": source_route_reconciliation["received_count"],
            "source_to_relay_matched": source_route_reconciliation["matched_count"],
            "source_to_relay_unmatched_enqueue": source_route_reconciliation[
                "unmatched_enqueue_count"
            ],
            "source_to_relay_orphan_reception": source_route_reconciliation[
                "orphan_reception_count"
            ],
            "source_to_relay_duplicate_reception": source_route_reconciliation[
                "duplicate_count"
            ],
            "source_to_relay_payload_mismatches": source_route_reconciliation[
                "payload_mismatch_count"
            ],
            "source_to_relay_timing_mismatches": source_route_reconciliation[
                "timing_mismatch_count"
            ],
            "source_to_relay_route_path_mismatches": source_route_reconciliation[
                "route_path_mismatch_count"
            ],
            "source_to_relay_identity_mismatches": source_route_reconciliation[
                "identity_mismatch_count"
            ],
            "source_to_relay_provenance_mismatches": source_route_reconciliation[
                "provenance_mismatch_count"
            ],
            "source_to_relay_event_id_mismatches": source_route_reconciliation[
                "event_id_mismatch_count"
            ],
            "relay_emissions": len(classified_relay_emissions),
            "relay_integrated_emissions": sum(
                item["classification"] == "integration-mediated"
                for item in classified_relay_emissions
            ),
            "relay_direct_emissions": sum(
                item["classification"] == "direct"
                for item in classified_relay_emissions
            ),
            "relay_to_destination_transfers": len(relay_transfers),
            "destination_receptions": len(destination_receptions),
            "relay_to_destination_enqueued": onward_route_reconciliation[
                "enqueued_count"
            ],
            "relay_to_destination_received": onward_route_reconciliation[
                "received_count"
            ],
            "relay_to_destination_matched": onward_route_reconciliation[
                "matched_count"
            ],
            "relay_to_destination_unmatched_enqueue": onward_route_reconciliation[
                "unmatched_enqueue_count"
            ],
            "relay_to_destination_orphan_reception": onward_route_reconciliation[
                "orphan_reception_count"
            ],
            "relay_to_destination_duplicate_reception": onward_route_reconciliation[
                "duplicate_count"
            ],
            "relay_to_destination_payload_mismatches": onward_route_reconciliation[
                "payload_mismatch_count"
            ],
            "relay_to_destination_timing_mismatches": onward_route_reconciliation[
                "timing_mismatch_count"
            ],
            "relay_to_destination_route_path_mismatches": onward_route_reconciliation[
                "route_path_mismatch_count"
            ],
            "relay_to_destination_identity_mismatches": onward_route_reconciliation[
                "identity_mismatch_count"
            ],
            "relay_to_destination_provenance_mismatches": onward_route_reconciliation[
                "provenance_mismatch_count"
            ],
            "relay_to_destination_event_id_mismatches": onward_route_reconciliation[
                "event_id_mismatch_count"
            ],
            "destination_emissions": len(destination_emissions),
            "activity_count": activity_count,
            "max_relay_z": max(signed_z_values, default=0.0),
            "max_abs_relay_z": max(
                (abs(value) for value in signed_z_values),
                default=0.0,
            ),
            "relay_max_abs_z": max(
                (abs(value) for value in signed_z_values),
                default=0.0,
            ),
        },
        "causality_reconciles": causality_reconciles,
    }
    record["record_digest"] = _digest(record)
    return record


def _aggregate_arm(records: list[dict[str, Any]]) -> dict[str, Any]:
    def count(name: str) -> int:
        return sum(record["counts"][name] for record in records)

    routing_reconciliation = {}
    for hop in ("all_routes", "source_to_relay", "relay_to_destination"):
        routing_reconciliation[hop] = {
            name: sum(
                record["routing_reconciliation"][hop][name]
                for record in records
            )
            for name in (
                "enqueued_count",
                "received_count",
                "matched_count",
                "unmatched_enqueue_count",
                "orphan_reception_count",
                "duplicate_count",
                "duplicate_reception_count",
                "duplicate_enqueue_count",
                "payload_mismatch_count",
                "timing_mismatch_count",
                "route_path_mismatch_count",
                "identity_mismatch_count",
                "provenance_mismatch_count",
                "event_id_mismatch_count",
                "mismatch_count",
            )
        }
        routing_reconciliation[hop]["reconciles"] = all(
            record["routing_reconciliation"][hop]["reconciles"]
            for record in records
        )
    routing_reconciliation["reconciles"] = all(
        routing_reconciliation[hop]["reconciles"]
        for hop in ("all_routes", "source_to_relay", "relay_to_destination")
    )
    return {
        "sequences": len(records),
        "routing_reconciliation": routing_reconciliation,
        "source_inputs": count("source_inputs"),
        "source_emissions": count("source_emissions"),
        "source_to_relay_transfers": count("source_to_relay_transfers"),
        "source_to_relay_receptions": count("source_to_relay_receptions"),
        "relay_emissions": count("relay_emissions"),
        "relay_integrated_emissions": count("relay_integrated_emissions"),
        "relay_direct_emissions": count("relay_direct_emissions"),
        "relay_to_destination_transfers": count("relay_to_destination_transfers"),
        "destination_receptions": count("destination_receptions"),
        "destination_emissions": count("destination_emissions"),
        "activity_count": count("activity_count"),
        "max_relay_z": max(
            (item["counts"]["max_relay_z"] for item in records), default=0.0
        ),
        "max_abs_relay_z": max(
            (item["counts"]["max_abs_relay_z"] for item in records), default=0.0
        ),
        "all_causality_checks_pass": all(
            item["causality_reconciles"] for item in records
        ),
        "all_recurrence_checks_pass": all(
            item["relay_recurrence_reconciles"] for item in records
        ),
        "resource_high_water": {
            "queue_peak": max(
                (item["resource_high_water"]["queue_peak"] for item in records),
                default=0,
            ),
            "runtime_event_peak": max(
                (item["resource_high_water"]["processed_events"] for item in records),
                default=0,
            ),
            "neuron_event_peak": max(
                (
                    max(item["resource_high_water"]["neuron_processed_events"].values())
                    for item in records
                ),
                default=0,
            ),
            "prediction_peak": max(
                (item["resource_high_water"]["prediction_peak"] for item in records),
                default=0,
            ),
            "eligibility_peak": max(
                (item["resource_high_water"]["eligibility_peak"] for item in records),
                default=0,
            ),
            "activity_peak": max(
                (item["resource_high_water"]["activity_high_water"] for item in records),
                default=0,
            ),
        },
    }


def _observed_control_distinctions(
    summaries: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    per_arm_counts = {
        arm: {
            "relay_integrated_emissions": summaries[arm]["relay_integrated_emissions"],
            "relay_direct_emissions": summaries[arm]["relay_direct_emissions"],
        }
        for arm in ARMS
    }
    comparisons = []
    for left, right in (
        ("DEFAULT", "CALIBRATED"),
        ("DEFAULT", "DISABLED"),
        ("CALIBRATED", "DISABLED"),
    ):
        if per_arm_counts[left] != per_arm_counts[right]:
            comparisons.append(
                {
                    "left_arm": left,
                    "right_arm": right,
                    "left_counts": per_arm_counts[left],
                    "right_counts": per_arm_counts[right],
                }
            )
    if not comparisons:
        return None
    return {
        "basis": "actual per-arm integrated/direct relay emission counts",
        "per_arm_counts": per_arm_counts,
        "observed_differences": comparisons,
    }


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_bytes(value) + b"\n")


def _persist_routing_evidence(
    output_directory: Path,
    metadata: dict[str, Any],
    initial: dict[str, list[dict[str, Any]]],
    replay: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Persist independent captures, verifying bytes and replay stream digests."""
    manifest: dict[str, Any] = {"artifacts": {}, "streams": {}}
    for stream, field in (
        ("enqueue", "routing_enqueue_events"),
        ("reception", "receiver_reception_events"),
    ):
        captures = {}
        for phase, runs in (("initial", initial), ("replay", replay)):
            per_arm = {
                arm: [
                    {
                        "seed": record["seed"],
                        "sequence_index": record["sequence_index"],
                        "stream_id": record["stream_id"],
                        "capture_status": record.get("routing_capture_status", "completed"),
                        "events": record[field],
                        "stream_digest": _digest(record[field]),
                    }
                    for record in runs[arm]
                ]
                for arm in ARMS
            }
            captures[phase] = per_arm
            filename = f"routing-{phase}-{stream}.json"
            artifact = _seal_artifact({
                **metadata,
                "schema": "TPCN-LUNA44-ROUTING-RAW-1",
                "phase": phase,
                "capture_stream": stream,
                "event_scope": "routed EXCURSION events only",
                "timestamp_policy": "exact binary64 logical time; no wall clock",
                "identity_key": "arm, seed, sequence_index, queue_sequence",
                "per_arm": per_arm,
                "streams_digest": _digest(per_arm),
            })
            path = output_directory / filename
            _write_json(path, artifact)
            persisted = path.read_bytes()
            if persisted != _canonical_bytes(artifact) + b"\n":
                raise RuntimeError(f"raw routing artifact persistence mismatch: {filename}")
            manifest["artifacts"][f"{phase}_{stream}"] = {
                "path": filename,
                "file_sha256": hashlib.sha256(persisted).hexdigest(),
                "artifact_digest": artifact["artifact_digest"],
                "streams_digest": artifact["streams_digest"],
            }
        manifest["streams"][stream] = {
            "initial_digest": _digest(captures["initial"]),
            "replay_digest": _digest(captures["replay"]),
            "equal": captures["initial"] == captures["replay"],
        }
    manifest["replay_equal"] = all(
        item["equal"] for item in manifest["streams"].values()
    )
    return manifest


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Execute all fixture streams and full per-arm deterministic replays."""
    config = experiment_config()
    config_digest = _digest(config)
    output_directory.mkdir(parents=True, exist_ok=False)
    run_records: dict[str, list[dict[str, Any]]] = {arm: [] for arm in ARMS}
    replay_records: dict[str, list[dict[str, Any]]] = {arm: [] for arm in ARMS}
    fixture: dict[str, Any] | None = None
    fixture_source_provenance: dict[str, Any] = {}
    provenance: dict[str, Any]
    stop_reason: str | None = None
    fixture_error: str | None = None
    failed_routing_capture: dict[str, Any] | None = None
    execution_phase = "initial"
    try:
        fixture, fixture_source_provenance = load_fixture()
    except Exception as error:
        fixture_error = f"{type(error).__name__}: {error}"
        stop_reason = f"fixture validation blocker: {fixture_error}"
    try:
        provenance = _collect_execution_provenance()
    except ProvenanceError as error:
        provenance = error.provenance
        message = f"provenance blocker: {error}"
        stop_reason = message if stop_reason is None else f"{stop_reason}; {message}"
    except Exception as error:
        execution_revision = _available_execution_revision()
        provenance = {
            "authorization_revision": AUTHORIZATION_REVISION,
            "authorization_handoff_sha256": AUTHORIZATION_HANDOFF_SHA256,
            "fixture_revision": FIXTURE_REVISION,
            "head": execution_revision,
            "execution_revision": execution_revision,
            "runner_sha256": _runner_sha256(),
            "provenance_error": f"{type(error).__name__}: {error}",
        }
        message = f"provenance blocker: {type(error).__name__}: {error}"
        stop_reason = message if stop_reason is None else f"{stop_reason}; {message}"
    provenance["config_digest"] = config_digest
    provenance["fixture_sha256"] = FIXTURE_SHA256
    if stop_reason is None and fixture is not None:
        try:
            for arm in ARMS:
                execution_phase = "initial"
                for sequence in fixture["sequences"]:
                    run_records[arm].append(_run_character(arm=arm, sequence=sequence))
                execution_phase = "replay"
                for sequence in fixture["sequences"]:
                    replay_records[arm].append(_run_character(arm=arm, sequence=sequence))
        except Exception as error:
            stop_reason = f"execution blocker: {type(error).__name__}: {error}"
            if isinstance(error, RoutingEvidenceError):
                failed_routing_capture = {
                    "phase": execution_phase,
                    "arm": arm,
                    **error.capture,
                }
    if stop_reason is None:
        try:
            observed_head = _git_output("rev-parse", "HEAD")
            observed_runner_sha256 = _runner_sha256()
            if observed_head != provenance["execution_revision"]:
                raise RuntimeError("execution revision changed during experiment")
            if observed_runner_sha256 != provenance["runner_sha256"]:
                raise RuntimeError("runner source changed during experiment")
        except Exception as error:
            stop_reason = f"provenance drift blocker: {type(error).__name__}: {error}"

    artifact_metadata = _artifact_metadata(
        provenance, fixture_source_provenance, config_digest,
    )
    routing_initial = {arm: list(records) for arm, records in run_records.items()}
    routing_replay = {arm: list(records) for arm, records in replay_records.items()}
    if failed_routing_capture is not None:
        captures = (
            routing_initial if failed_routing_capture["phase"] == "initial"
            else routing_replay
        )
        captures[failed_routing_capture["arm"]].append(failed_routing_capture)
    routing_evidence = _persist_routing_evidence(
        output_directory, artifact_metadata, routing_initial, routing_replay,
    )
    if failed_routing_capture is not None:
        routing_evidence["failed_capture"] = {
            key: failed_routing_capture[key]
            for key in ("phase", "arm", "seed", "sequence_index", "stream_id",
                        "routing_reconciliation")
        }
    replay_summary = {}
    replay_ok = stop_reason is None
    replay_ok &= routing_evidence["replay_equal"]
    for arm in ARMS:
        first_digests = [item["record_digest"] for item in run_records[arm]]
        replay_digests = [item["record_digest"] for item in replay_records[arm]]
        equal = (
            len(first_digests) == TOTAL_SEQUENCES
            and len(replay_digests) == TOTAL_SEQUENCES
            and first_digests == replay_digests
        )
        replay_ok &= equal
        replay_summary[arm] = {
            "initial_digest": _replay_envelope_digest(first_digests, config_digest),
            "replay_digest": _replay_envelope_digest(replay_digests, config_digest),
            "equal": equal,
            "sequences_replayed": len(replay_digests),
            "initial_record_digests": first_digests,
            "replay_record_digests": replay_digests,
        }

    invariance = True
    if stop_reason is None:
        for seq_index in range(TOTAL_SEQUENCES):
            baseline = run_records["DISABLED"][seq_index]
            baseline_points = baseline["point_inputs"]
            baseline_raw = baseline["raw_identity"]
            for arm in ARMS:
                candidate = run_records[arm][seq_index]
                invariance &= candidate["raw_identity"] == baseline_raw
                invariance &= candidate["point_inputs"] == baseline_points
                invariance &= candidate["input_batches"] == run_records["DISABLED"][seq_index]["input_batches"]
                replay = replay_records[arm][seq_index]
                invariance &= replay["raw_identity"] == baseline_raw
                invariance &= replay["point_inputs"] == baseline_points
                invariance &= replay["input_batches"] == run_records["DISABLED"][seq_index]["input_batches"]
    replay_ok &= invariance
    summaries = {
        arm: _aggregate_arm(run_records[arm])
        for arm in ARMS
    }
    complete_all_arms = all(len(run_records[arm]) == TOTAL_SEQUENCES for arm in ARMS)
    calibrated_supported = (
        complete_all_arms
        and summaries["CALIBRATED"]["relay_integrated_emissions"] > 0
        and summaries["CALIBRATED"]["relay_integrated_emissions"]
        <= summaries["CALIBRATED"]["relay_to_destination_transfers"]
    )
    causal_ok = all(
        item["all_causality_checks_pass"] and item["all_recurrence_checks_pass"]
        for item in summaries.values()
    )
    resource_ok = stop_reason is None
    if not replay_ok and stop_reason is None:
        stop_reason = "deterministic replay or paired fixture identity blocker"
    if not causal_ok and stop_reason is None:
        stop_reason = "causal transfer/reception reconciliation blocker"
    if stop_reason is not None or not replay_ok or not causal_ok or not resource_ok:
        status = "BLOCKED"
        verdict = "BLOCKED"
    elif calibrated_supported:
        status = "PASS"
        verdict = "SUPPORTED"
    else:
        status = "PASS"
        verdict = "NOT SUPPORTED IN THIS NEW BASELINE"
    control_distinction = (
        _observed_control_distinctions(summaries)
        if complete_all_arms
        else None
    )
    summary_body = {
        **artifact_metadata,
        "schema": "TPCN-LUNA44-ACP0008-CANONICAL-FIXTURE-SUMMARY-1",
        "status": status,
        "verdict": verdict,
        "stop_reason": stop_reason,
        "authorization_revision": AUTHORIZATION_REVISION,
        "fixture_revision": FIXTURE_REVISION,
        "fixture_sha256": FIXTURE_SHA256,
        "config_digest": config_digest,
        "provenance": provenance,
        "fixture_source_provenance": fixture_source_provenance,
        "sequence_count": 0 if fixture is None else len(fixture["sequences"]),
        "point_count": (
            0
            if fixture is None
            else sum(item["point_count"] for item in fixture["sequences"])
        ),
        "per_arm": summaries,
        "relay_z_summary": {
            arm: {
                "max_relay_z": summaries[arm]["max_relay_z"],
                "max_abs_relay_z": summaries[arm]["max_abs_relay_z"],
            }
            for arm in ARMS
        },
        "replay": replay_summary,
        "routing_raw_evidence": routing_evidence,
        "replay_equal": replay_ok,
        "paired_raw_identity_and_input_invariance": invariance,
        "causality_reconciles": causal_ok,
        "resource_bounds_pass": resource_ok,
        "calibrated_mechanism_supported": calibrated_supported,
        "destination_condition_comparison": False,
    }
    if control_distinction is not None:
        summary_body["observed_control_distinction"] = control_distinction
    summary = _seal_artifact(summary_body)
    results = _seal_artifact({
        **artifact_metadata,
        "schema": "TPCN-LUNA44-ACP0008-CANONICAL-FIXTURE-RESULTS-1",
        "config_digest": config_digest,
        "fixture_sha256": FIXTURE_SHA256,
        "provenance": provenance,
        "fixture_validation": {
            "valid": fixture is not None,
            "error": fixture_error,
            "canonical_sha256": FIXTURE_SHA256,
            "sequences": 0 if fixture is None else len(fixture["sequences"]),
            "points": (
                0
                if fixture is None
                else sum(item["point_count"] for item in fixture["sequences"])
            ),
        },
        "runs": run_records,
        "routing_raw_evidence": routing_evidence,
    })
    replay_artifact = _seal_artifact({
        **artifact_metadata,
        "schema": "TPCN-LUNA44-ACP0008-CANONICAL-FIXTURE-REPLAY-1",
        "fixture_sha256": FIXTURE_SHA256,
        "config_digest": config_digest,
        "routing_raw_evidence": routing_evidence,
        "digest_envelope": {
            "algorithm": "sha256",
            "canonicalization": "sorted-key compact UTF-8 JSON",
            "fields": ["fixture_sha256", "config_digest", "ordered_record_digests"],
            "record_order": "fixture sequence order",
        },
        "per_arm": {
            arm: {
                **replay_summary[arm],
                "records": replay_records[arm],
            }
            for arm in ARMS
        },
    })
    config_artifact = _seal_artifact({
        **artifact_metadata,
        "schema": "TPCN-LUNA44-ACP0008-CANONICAL-FIXTURE-CONFIG-1",
        "experiment": config,
        "config_digest": config_digest,
        "source_provenance": fixture_source_provenance,
        "execution_provenance": provenance,
    })
    _write_json(output_directory / "config.json", config_artifact)
    _write_json(output_directory / "results.json", results)
    _write_json(output_directory / "summary.json", summary)
    _write_json(output_directory / "replay.json", replay_artifact)
    return results, summary


def main() -> None:
    results, summary = run_experiment()
    print(
        json.dumps(
            {
                "status": summary["status"],
                "verdict": summary["verdict"],
                "fixture_sha256": results["fixture_sha256"],
                "config_digest": results["config_digest"],
                "sequences": summary["sequence_count"],
                "points": summary["point_count"],
                "output_directory": str(ARTIFACT_DIRECTORY),
                "stop_reason": summary["stop_reason"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
