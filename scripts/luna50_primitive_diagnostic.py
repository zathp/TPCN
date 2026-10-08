"""Portable primitive trace for the Luna-44 generator's c00-000 point 3."""

from __future__ import annotations

import argparse
import ctypes.util
from datetime import datetime, timezone
import hashlib
import json
import locale
import math
import os
import platform
import random
import struct
import subprocess
import sys
import sysconfig
import uuid
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
FIXTURE = ROOT / "artifacts/luna44-canonical-fixture/fixture.json"
PROVENANCE = ROOT / "artifacts/luna44-canonical-fixture/provenance.json"
EXPECTED_FIXTURE_SHA256 = "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629"
EXPECTED_PROVENANCE_SHA256 = "6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22"
SOURCE_REVISION = "a79494cd66be28fd291ed11eddd62d342f457cfd"
MATERIALIZER_REVISION = "10994419cec3646d30d965372f88d10605d83d57"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def float_record(value: float) -> dict[str, Any]:
    if not math.isfinite(value):
        raise ValueError("binary64 diagnostic requires a finite value")
    packed = struct.pack(">d", value)
    return {"decimal": repr(value), "hex": value.hex(), "bits_be": packed.hex()}


def compare_values(expected: Mapping[str, float], observed: Mapping[str, float]) -> dict[str, Any]:
    fields = sorted(set(expected) | set(observed))
    comparisons = {}
    for field in fields:
        left = expected.get(field)
        right = observed.get(field)
        if left is None or right is None:
            comparisons[field] = {
                "equal": False,
                "expected": left,
                "observed": right,
                "reason": "field absent on one side",
            }
            continue
        if not math.isfinite(left) or not math.isfinite(right):
            raise ValueError("mismatch reporting requires finite values")
        comparisons[field] = {
            "equal": struct.pack(">d", left) == struct.pack(">d", right),
            "expected": float_record(left),
            "observed": float_record(right),
            "absolute_difference": abs(left - right),
        }
    return {
        "fields": comparisons,
        "all_equal": all(item["equal"] for item in comparisons.values()),
        "first_difference": next(
            (name for name in fields if not comparisons[name]["equal"]), None
        ),
    }


def distinct_materializations(records: list[Mapping[str, Any]]) -> bool:
    if len(records) < 2:
        return False
    return all(
        len({record[field] for record in records}) == len(records)
        for field in ("invocation_id", "process_id", "output_directory")
    )


class _DrawRecorder(random.Random):
    def __init__(self, seed: int):
        super().__init__(seed)
        self.raw_uniforms: list[float] = []

    def random(self) -> float:
        value = super().random()
        self.raw_uniforms.append(value)
        return value


class _GaussianTrace:
    def __init__(self, rng: _DrawRecorder):
        self.rng = rng
        self.cached_standard: float | None = None

    def gauss(self, mu: float, sigma: float) -> tuple[float, dict[str, Any]]:
        before = len(self.rng.raw_uniforms)
        cached_before = self.cached_standard
        transform: dict[str, Any]
        if self.cached_standard is not None:
            standard = self.cached_standard
            self.cached_standard = None
            transform = {"cache_hit": True, "standard_normal": float_record(standard)}
        else:
            first = self.rng.random()
            second = self.rng.random()
            angle = 2.0 * math.pi * first
            radius = math.sqrt(-2.0 * math.log(1.0 - second))
            cosine = math.cos(angle)
            sine = math.sin(angle)
            standard = cosine * radius
            self.cached_standard = sine * radius
            transform = {
                "cache_hit": False,
                "uniforms": [float_record(first), float_record(second)],
                "angle": float_record(angle),
                "log_input": float_record(1.0 - second),
                "radius": float_record(radius),
                "cos_input": float_record(angle),
                "cos_output": float_record(cosine),
                "sin_input": float_record(angle),
                "sin_output": float_record(sine),
                "standard_normal": float_record(standard),
                "cached_standard_normal": float_record(self.cached_standard),
            }
        value = mu + sigma * standard
        transform.update(
            {
                "cached_standard_before": (
                    float_record(cached_before) if cached_before is not None else None
                ),
                "cached_standard_after": (
                    float_record(self.cached_standard)
                    if self.cached_standard is not None
                    else None
                ),
                "mu": float_record(mu),
                "sigma": float_record(sigma),
                "result": float_record(value),
                "raw_uniform_draw_range": [before, len(self.rng.raw_uniforms)],
            }
        )
        return value, transform


def _source_inventory(provenance: Mapping[str, Any]) -> list[dict[str, Any]]:
    result = []
    for source in provenance["source_files"]:
        revision = source["revision"]
        path = source["path"]
        committed = subprocess.run(
            ["git", "show", f"{revision}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        checkout = (ROOT / path).read_bytes()
        canonical_hash = sha256(committed)
        if canonical_hash != source["sha256"]:
            raise RuntimeError(f"Git-object source identity mismatch: {path}")
        if revision == SOURCE_REVISION and source["role"] != "materializer":
            if canonical_hash not in (sha256(checkout), sha256(checkout.replace(b"\r\n", b"\n"))):
                raise RuntimeError(f"checkout source is not LF/CRLF-equivalent: {path}")
        result.append(
            {
                "role": source["role"],
                "path": path,
                "revision": revision,
                "git_object": subprocess.run(
                    ["git", "rev-parse", f"{revision}:{path}"],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip(),
                "git_blob_sha256": canonical_hash,
                "checkout_sha256": sha256(checkout),
                "checkout_line_ending_relation": (
                    "exact Git bytes"
                    if checkout == committed
                    else "CRLF-normalized bytes match Git object"
                    if checkout.replace(b"\r\n", b"\n") == committed
                    else "materialized bytes differ"
                ),
            }
        )
    return result


def _executed_source_identity(path: str) -> dict[str, str]:
    source_path = ROOT / path
    return {
        "path": path,
        "resolved_path": str(source_path.resolve()),
        "executed_source_sha256": sha256(source_path.read_bytes()),
    }


def _trace_point_three(example: Any) -> dict[str, Any]:
    metadata = example.metadata
    point_index = 3
    rng = _DrawRecorder(metadata.seed ^ 0x5EED5EED)
    gaussian = _GaussianTrace(rng)
    timing = []
    for _ in range(1, metadata.sample_count):
        timing.append(rng.uniform(-metadata.timing_jitter, metadata.timing_jitter))
    timing_draw_count = len(rng.raw_uniforms)
    rotation_cos = math.cos(float(metadata.rotation))
    rotation_sin = math.sin(float(metadata.rotation))
    point_traces = []
    generated = None
    for index in range(1, point_index + 1):
        draw_start = len(rng.raw_uniforms)
        radial_jitter = rng.uniform(-metadata.radial_jitter, metadata.radial_jitter)
        fraction = index / (metadata.sample_count - 1)
        radial_base = metadata.radial_growth * fraction
        radius = radial_base + radial_jitter
        angle_rate = metadata.angular_speed * fraction
        angle_turns = angle_rate * 2.0
        angle = angle_turns * math.pi
        cosine = math.cos(angle)
        sine = math.sin(angle)
        scaled_radius = float(metadata.scale) * radius
        local_x = scaled_radius * cosine
        handed_scaled_radius = metadata.handedness * float(metadata.scale)
        handed_scaled_radius *= radius
        local_y = handed_scaled_radius * sine
        rot_x_cos = rotation_cos * local_x
        rot_x_sin = rotation_sin * local_y
        rotated_x = rot_x_cos - rot_x_sin
        rot_y_sin = rotation_sin * local_x
        rot_y_cos = rotation_cos * local_y
        rotated_y = rot_y_sin + rot_y_cos
        noise_x, gaussian_x = gaussian.gauss(0.0, float(metadata.coordinate_noise))
        noise_y, gaussian_y = gaussian.gauss(0.0, float(metadata.coordinate_noise))
        pre_offset_x = rotated_x + noise_x
        pre_offset_y = rotated_y + noise_y
        x = metadata.offset_x + pre_offset_x
        y = metadata.offset_y + pre_offset_y
        operations = [
            ("radial_growth * fraction", [metadata.radial_growth, fraction], radial_base),
            ("radial_base + radial_jitter", [radial_base, radial_jitter], radius),
            ("angular_speed * fraction", [metadata.angular_speed, fraction], angle_rate),
            ("angle_rate * 2.0", [angle_rate, 2.0], angle_turns),
            ("angle_turns * pi", [angle_turns, math.pi], angle),
            ("scale * radius", [metadata.scale, radius], scaled_radius),
            ("scaled_radius * cos(angle)", [scaled_radius, cosine], local_x),
            ("handedness * scale * radius", [metadata.handedness, metadata.scale, radius], handed_scaled_radius),
            ("handed_scaled_radius * sin(angle)", [handed_scaled_radius, sine], local_y),
            ("cos(rotation) * local_x", [rotation_cos, local_x], rot_x_cos),
            ("sin(rotation) * local_y", [rotation_sin, local_y], rot_x_sin),
            ("rotated_x_cos - rotated_x_sin", [rot_x_cos, rot_x_sin], rotated_x),
            ("sin(rotation) * local_x", [rotation_sin, local_x], rot_y_sin),
            ("cos(rotation) * local_y", [rotation_cos, local_y], rot_y_cos),
            ("rotated_y_sin + rotated_y_cos", [rot_y_sin, rot_y_cos], rotated_y),
            ("rotated_x + gaussian_x", [rotated_x, noise_x], pre_offset_x),
            ("rotated_y + gaussian_y", [rotated_y, noise_y], pre_offset_y),
            ("offset_x + pre_offset_x", [metadata.offset_x, pre_offset_x], x),
            ("offset_y + pre_offset_y", [metadata.offset_y, pre_offset_y], y),
        ]
        if index == point_index:
            generated = {"x": example.points[index].x, "y": example.points[index].y}
            point_traces.append(
                {
                    "generator_point_index": index,
                    "timestamp": float_record(example.points[index].timestamp),
                    "radial_jitter": float_record(radial_jitter),
                    "angle": float_record(angle),
                    "angle_sin": float_record(sine),
                    "angle_cos": float_record(cosine),
                    "rotation": float_record(metadata.rotation),
                    "rotation_sin": float_record(rotation_sin),
                    "rotation_cos": float_record(rotation_cos),
                    "gaussian_x": gaussian_x,
                    "gaussian_y": gaussian_y,
                    "operations": [
                        {"operation": name, "operands": [float_record(float(v)) for v in operands], "result": float_record(float(value))}
                        for name, operands, value in operations
                    ],
                    "reconstructed": {name: float_record(value) for name, value in {"x": x, "y": y}.items()},
                    "generator_output": {name: float_record(value) for name, value in generated.items()},
                    "raw_uniform_draw_range": [draw_start, len(rng.raw_uniforms)],
                }
            )
    if generated is None or any(
        struct.pack(">d", trace_value) != struct.pack(">d", generated[name])
        for trace_value, name in ((x, "x"), (y, "y"))
    ):
        raise RuntimeError("instrumented Windows control does not reconstruct generator point 3")
    return {
        "stream_id": "c00-000",
        "output_point_index": point_index,
        "generator_point_index": point_index,
        "generator_parameters": {
            name: float_record(value) if isinstance(value, float) else value
            for name, value in {
                "seed": metadata.seed,
                "rotation": metadata.rotation,
                "scale": metadata.scale,
                "offset_x": metadata.offset_x,
                "offset_y": metadata.offset_y,
                "angular_speed": metadata.angular_speed,
                "radial_growth": metadata.radial_growth,
                "timing_jitter": metadata.timing_jitter,
                "coordinate_noise": metadata.coordinate_noise,
                "radial_jitter": metadata.radial_jitter,
                "sample_count": metadata.sample_count,
                "duration": metadata.duration,
                "handedness": metadata.handedness,
            }.items()
        },
        "pre_coordinate_draws": {
            "timing_uniforms": [float_record(value) for value in timing],
            "timing_raw_draw_count": timing_draw_count,
        },
        "raw_random_uniforms_through_target": [float_record(value) for value in rng.raw_uniforms],
        "raw_uniform_draw_count": len(rng.raw_uniforms),
        "point_trace": point_traces[0],
        "instrumented_reconstruction_exact": True,
        "historical_intermediates": "UNAVAILABLE: only final canonical x/y/t bits are retained",
    }


def build_report() -> dict[str, Any]:
    fixture_before = FIXTURE.read_bytes()
    provenance_before = PROVENANCE.read_bytes()
    fixture_hash = sha256(fixture_before)
    provenance_hash = sha256(provenance_before)
    if fixture_hash != EXPECTED_FIXTURE_SHA256:
        raise RuntimeError("canonical fixture identity mismatch")
    if provenance_hash != EXPECTED_PROVENANCE_SHA256:
        raise RuntimeError("canonical provenance identity mismatch")
    fixture = json.loads(fixture_before)
    provenance = json.loads(provenance_before)

    from tpcn.spiral_benchmark import SpiralConfig, make_spiral_dataset

    dataset = make_spiral_dataset(
        examples_per_class=16,
        train_seed=12007,
        evaluation_seed=22017,
        config=SpiralConfig(),
    )
    examples = list(dataset.train)
    random.Random(330000).shuffle(examples)
    target = examples[0]
    if target.points[3].x.hex() == "" or fixture["sequences"][0]["stream_id"] != "c00-000":
        raise RuntimeError("unexpected target sequence identity")
    trace = _trace_point_three(target)

    historical_point = fixture["sequences"][0]["points"][3]
    historical = {
        field: float.fromhex(historical_point[field]["hex"]) for field in ("x", "y", "t")
    }
    observed = {
        "x": target.points[3].x,
        "y": target.points[3].y,
        "t": target.points[3].timestamp,
    }
    serialization = {
        field: {
            "source": float_record(value),
            "json_round_trip": float_record(json.loads(json.dumps(value, allow_nan=False))),
            "round_trip_bits_equal": struct.pack(">d", value)
            == struct.pack(">d", json.loads(json.dumps(value, allow_nan=False))),
        }
        for field, value in observed.items()
    }
    result = {
        "schema": "TPCN-LUNA50-WINDOWS-PRIMITIVE-CONTROL-1",
        "authorization_revision": "b49f6642957ea630598b576c3c57f8862e436a14",
        "starting_revision": "b49f6642957ea630598b576c3c57f8862e436a14",
        "luna49_baseline_field_revision": "be6e2d2df179be842208724d20b00d9497d4e4a4",
        "current_revision": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip(),
        "invocation_id": uuid.uuid4().hex,
        "process_id": os.getpid(),
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment_classification": "UNAVAILABLE",
        "current_runtime_role": "WINDOWS CONTROL ONLY; not exact or near-match Linux",
        "runtime": {
            "os": platform.platform(),
            "architecture": platform.machine(),
            "python_version": sys.version,
            "python_implementation": sys.implementation.name,
            "python_build": platform.python_build(),
            "python_compiler": platform.python_compiler(),
            "sysconfig": {key: sysconfig.get_config_var(key) for key in ("CC", "CONFIG_ARGS", "MULTIARCH")},
            "libc": platform.libc_ver(),
            "libm_lookup": ctypes.util.find_library("m"),
            "locale": locale.setlocale(locale.LC_ALL, None),
            "environment": {
                key: os.environ.get(key)
                for key in ("PYTHONHASHSEED", "PYTHONPATH", "VIRTUAL_ENV", "LANG", "LC_ALL", "TZ")
            },
            "cwd": str(Path.cwd()),
            "cuda_used": False,
        },
        "source_identity": _source_inventory(provenance),
        "executed_source_bytes": [
            _executed_source_identity("scripts/luna50_primitive_diagnostic.py"),
            _executed_source_identity("tpcn/spiral_benchmark.py"),
        ],
        "canonical_before": {
            "fixture_sha256": fixture_hash,
            "provenance_sha256": provenance_hash,
            "fixture_semantic_digest": "6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305",
        },
        "execution": {
            "command": "python scripts/luna50_primitive_diagnostic.py --output artifacts/luna50-historical-runtime-20261008/windows-control.json",
            "generator_source_revision": SOURCE_REVISION,
            "materializer_source_revision": MATERIALIZER_REVISION,
            "materializations": "NOT RUN: historical Linux runtime unavailable; this control does not materialize a fixture",
            "primitive_trace": trace,
            "historical_final_comparison": compare_values(historical, observed),
            "serialization_round_trip": serialization,
            "windows_linux_primitive_comparison": "NOT AVAILABLE: no Linux runtime or remote endpoint",
            "linux_historical_intermediates": "NOT AVAILABLE",
            "cuda": "NOT USED",
        },
    }
    if (sha256(FIXTURE.read_bytes()), sha256(PROVENANCE.read_bytes())) != (
        fixture_hash,
        provenance_hash,
    ):
        raise RuntimeError("canonical fixture or provenance changed during read-only control")
    result["canonical_after"] = {
        "fixture_sha256": sha256(FIXTURE.read_bytes()),
        "provenance_sha256": sha256(PROVENANCE.read_bytes()),
        "unchanged": True,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report()
    destination = args.output if args.output.is_absolute() else ROOT / args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(destination), "fixture_sha256": report["canonical_after"]["fixture_sha256"], "status": report["environment_classification"]}, sort_keys=True))


if __name__ == "__main__":
    main()