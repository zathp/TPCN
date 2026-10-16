from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import math
from typing import Any, Callable

PLAN_SHA256 = "60cde6b4929be4408fcecdcf3ac7104d5cb7b3365d94d55b568431e54fb5bc3f"
CONTRACT_COMMIT = "11b6f52e9aa6725af69bcd3cd098bb2c62e78b76"
EXPECTED_PARAMETER_SHA256 = "5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a"
FIXTURE_MANIFEST_SCHEMA = "luna71b-c4.2-fixture-payload-manifest-1"
IMPLEMENTATION_FILES = {
    "ppc11/__init__.py", "ppc11/capture.py", "ppc11/compare.py",
    "ppc11/driver.py", "ppc11/pairing.py", "ppc11/schema.py", "ppc11/trace.py",
}


class PreflightError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _source_revision(entries: list[dict[str, Any]]) -> str:
    return f"{CONTRACT_COMMIT}+sha256:{_canonical_digest(entries)}"


def _validate_fixture_manifest(fixtures: Any) -> dict[str, Any]:
    if (not isinstance(fixtures, dict)
            or set(fixtures) != {"schema", "plan_sha256", "splits"}
            or fixtures["schema"] != FIXTURE_MANIFEST_SCHEMA
            or fixtures["plan_sha256"] != PLAN_SHA256
            or not isinstance(fixtures["splits"], dict)
            or set(fixtures["splits"]) != {"train", "validation", "test"}):
        raise PreflightError("fixture manifest schema or frozen plan identity mismatch")
    return fixtures


@dataclass(frozen=True)
class Preflight:
    root: Path
    plan_path: Path
    plan_sha256: str
    source_manifest_sha256: str
    runtime_manifest_sha256: dict[str, str]
    source_revision: dict[str, str]
    fixture_payloads: dict[str, Path]
    initial_parameter_sha256: str


def verify_preflight(root: str | Path, *, source_manifest_path: str | Path,
                     fixture_manifest_path: str | Path) -> Preflight:
    """Verify copied source/runtime/plan/fixture identities; never imports model code."""
    base = Path(root).resolve()
    plan_path = base / "inputs" / "L71B-C-paired-pilot-plan.json"
    if not plan_path.is_file():
        raise PreflightError("frozen pilot plan is missing")
    if _sha256(plan_path) != PLAN_SHA256:
        raise PreflightError("frozen pilot plan raw hash mismatch")
    repository_root = base.parents[1]
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repository_root,
                              check=True, capture_output=True, text=True).stdout.strip()
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=repository_root,
                                check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise PreflightError("cannot verify source worktree identity") from error
    if head != CONTRACT_COMMIT or branch != "experiment/luna71b-c4-2-bilateral-capture":
        raise PreflightError("source worktree commit or branch differs from the authorized baseline")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("initial_untrained_parameters", {}).get("canonical_sha256") != EXPECTED_PARAMETER_SHA256:
        raise PreflightError("frozen initial parameter digest mismatch")

    source_manifest = Path(source_manifest_path)
    if not source_manifest.is_absolute():
        source_manifest = base / source_manifest
    if not source_manifest.is_file():
        raise PreflightError("source/runtime identity manifest is missing")
    source_data = json.loads(source_manifest.read_text(encoding="utf-8"))
    if (set(source_data) != {"schema", "contract_commit", "variants", "implementation"}
            or source_data["schema"] != "luna71b-c4.2-source-manifest-2"
            or source_data["contract_commit"] != CONTRACT_COMMIT):
        raise PreflightError("source manifest schema or contract commit mismatch")
    source_digest = _sha256(source_manifest)
    implementation = source_data["implementation"]
    if not isinstance(implementation, list) or {
            entry.get("path") for entry in implementation if isinstance(entry, dict)
    } != IMPLEMENTATION_FILES or len(implementation) != len(IMPLEMENTATION_FILES):
        raise PreflightError("PPC-11 implementation identity entries are missing or malformed")
    for entry in implementation:
        if (set(entry) != {"path", "sha256"} or not isinstance(entry["path"], str)
                or not isinstance(entry["sha256"], str)):
            raise PreflightError("malformed PPC-11 implementation identity entry")
        relative = PurePosixPath(entry["path"])
        implementation_path = base.joinpath(*relative.parts)
        if (relative.as_posix() != entry["path"] or relative.is_absolute()
                or "\\" in entry["path"] or ".." in relative.parts
                or relative.as_posix() not in IMPLEMENTATION_FILES
                or not implementation_path.is_file()
                or _sha256(implementation_path) != entry["sha256"]):
            raise PreflightError(f"PPC-11 implementation identity mismatch: {entry['path']}")
    runtime_hashes: dict[str, str] = {}
    source_revisions: dict[str, str] = {}
    for side in ("original", "instrumented"):
        entries = source_data["variants"].get(side)
        if not isinstance(entries, list) or not entries:
            raise PreflightError(f"{side} source entries are missing")
        variant_root = (base / "variants" / side).resolve()
        expected_paths = {
            path.relative_to(variant_root).as_posix()
            for path in variant_root.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        entry_paths = [entry.get("path") for entry in entries if isinstance(entry, dict)]
        if (len(entry_paths) != len(entries) or not all(isinstance(path, str) for path in entry_paths)
                or len(set(entry_paths)) != len(entry_paths) or set(entry_paths) != expected_paths):
            raise PreflightError(f"{side} source manifest does not enumerate every copied source exactly once")
        runtime_entries = []
        for entry in entries:
            if set(entry) != {"path", "sha256", "runtime"} or not isinstance(entry["runtime"], bool):
                raise PreflightError(f"malformed {side} source entry")
            if not isinstance(entry["path"], str) or not isinstance(entry["sha256"], str):
                raise PreflightError(f"malformed {side} source identity: {entry.get('path')!r}")
            relative = PurePosixPath(entry["path"])
            file_path = (variant_root.joinpath(*relative.parts)).resolve()
            if (relative.as_posix() != entry["path"] or relative.is_absolute()
                    or "\\" in entry["path"] or ".." in relative.parts
                    or file_path != variant_root and variant_root not in file_path.parents):
                raise PreflightError(f"unsafe {side} source path: {entry['path']}")
            expected_runtime = file_path.suffix == ".py" and not file_path.name.startswith("test_")
            if entry["runtime"] != expected_runtime:
                raise PreflightError(f"{side} runtime classification mismatch: {entry['path']}")
            if not file_path.is_file() or _sha256(file_path) != entry["sha256"]:
                raise PreflightError(f"{side} source identity mismatch: {entry['path']}")
            if entry["runtime"]:
                runtime_entries.append({"path": entry["path"], "sha256": entry["sha256"]})
        runtime_hashes[side] = _canonical_digest(runtime_entries)
        source_revisions[side] = _source_revision(entries)

    fixture_manifest = Path(fixture_manifest_path)
    if not fixture_manifest.is_absolute():
        fixture_manifest = base / fixture_manifest
    if not fixture_manifest.is_file():
        raise PreflightError("verified fixture-payload manifest is missing; pilot plan contains IDs/hashes, not event payloads")
    fixtures = _validate_fixture_manifest(json.loads(fixture_manifest.read_text(encoding="utf-8")))
    payloads: dict[str, Path] = {}
    split_plan = plan.get("pilot_protocol", {}).get("splits", {})
    for split, entry in fixtures["splits"].items():
        if set(entry) != {"path", "sha256"}:
            raise PreflightError(f"malformed {split} fixture manifest entry")
        path = base / "inputs" / Path(entry["path"])
        if not path.is_file() or _sha256(path) != entry["sha256"]:
            raise PreflightError(f"verified {split} event payload is missing or mismatched")
        try:
            rows = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise PreflightError(f"invalid {split} payload JSON") from error
        expected_ids = split_plan.get(split, {}).get("execution_order_example_ids")
        expected_hashes = split_plan.get(split, {}).get("execution_order_hashes")
        if not isinstance(expected_ids, list) or len(expected_ids) != 48 or not isinstance(rows, list) or len(rows) != 48:
            raise PreflightError(f"{split} payload must contain the 48 frozen execution-order examples")
        if [row.get("example_id") for row in rows if isinstance(row, dict)] != expected_ids:
            raise PreflightError(f"{split} payload IDs/order differ from frozen execution order")
        for row in rows:
            if (not isinstance(row, dict) or set(row) != {"example_id", "events", "label"}
                    or not isinstance(row["example_id"], str) or not isinstance(row["events"], list)
                    or isinstance(row["label"], bool) or not isinstance(row["label"], int) or row["label"] not in range(4)):
                raise PreflightError(f"malformed {split} example record")
            for event in row["events"]:
                if (not isinstance(event, dict) or set(event) != {"timestamp", "source", "destination", "event_type", "payload", "event_id"}
                        or isinstance(event["timestamp"], bool) or not isinstance(event["timestamp"], (int, float))
                        or not math.isfinite(event["timestamp"])
                        or not all(isinstance(event[key], str) and event[key] for key in ("source", "destination", "event_type"))
                        or isinstance(event["event_id"], bool) or not isinstance(event["event_id"], (str, int))):
                    raise PreflightError(f"malformed event in {split} payload")
        try:
            content_bytes = json.dumps(rows, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
            input_rows = [{key: row[key] for key in ("example_id", "events")} for row in rows]
            input_bytes = json.dumps(input_rows, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
        except (TypeError, ValueError) as error:
            raise PreflightError(f"noncanonical {split} payload values") from error
        content_hash = hashlib.sha256(content_bytes).hexdigest()
        input_hash = hashlib.sha256(input_bytes).hexdigest()
        if expected_hashes is None or content_hash != expected_hashes["content_sha256"] or input_hash != expected_hashes["input_only_sha256"]:
            raise PreflightError(f"{split} payload content/input hashes differ from frozen execution-order hashes")
        payloads[split] = path
    return Preflight(base, plan_path, PLAN_SHA256, source_digest, runtime_hashes,
                     source_revisions, payloads, EXPECTED_PARAMETER_SHA256)


def require_execution_authorization(path: str | Path) -> dict[str, Any]:
    """Require a separate owner grant; this task intentionally supplies none."""
    grant_path = Path(path)
    if not grant_path.is_file():
        raise PreflightError("separate owner neural-execution authorization is missing")
    grant = json.loads(grant_path.read_text(encoding="utf-8"))
    required = {"authorization_id", "scope", "owner", "approved_at", "plan_sha256", "source_manifest_sha256", "fixture_manifest_sha256", "neural_execution_authorized"}
    if set(grant) != required or grant["scope"] != "Luna-71B-C4.2 bilateral neural execution" or grant["neural_execution_authorized"] is not True:
        raise PreflightError("execution authorization is malformed or out of scope")
    if grant["plan_sha256"] != PLAN_SHA256:
        raise PreflightError("execution authorization is bound to another pilot plan")
    return grant


def run_authorized_pair(*, root: str | Path, source_manifest_path: str | Path,
                        fixture_manifest_path: str | Path, authorization_path: str | Path,
                        initial_parameters: dict[str, dict[str, Any]],
                        execute_side: Callable[..., Any]) -> tuple[Any, Any]:
    """Preflight-only compatibility API; full-context neural dispatch is unimplemented."""
    preflight = verify_preflight(root, source_manifest_path=source_manifest_path,
                                 fixture_manifest_path=fixture_manifest_path)
    authorization = require_execution_authorization(authorization_path)
    if authorization["source_manifest_sha256"] != preflight.source_manifest_sha256:
        raise PreflightError("authorization source-manifest identity mismatch")
    fixture_manifest = Path(fixture_manifest_path)
    if not fixture_manifest.is_absolute():
        fixture_manifest = preflight.root / fixture_manifest
    if authorization["fixture_manifest_sha256"] != _sha256(fixture_manifest):
        raise PreflightError("authorization fixture-manifest identity mismatch")
    if set(initial_parameters) != {"original", "instrumented"}:
        raise PreflightError("independent initial parameter snapshots required for both sides")
    for side in ("original", "instrumented"):
        if _canonical_digest(initial_parameters[side]) != preflight.initial_parameter_sha256:
            raise PreflightError(f"{side} initial parameter identity mismatch")
    if not callable(execute_side):
        raise PreflightError("future source execution adapter is missing")
    raise PreflightError("full-context source/model/trace-bound dispatch is unimplemented; callbacks are never executed")
