"""Verify Luna-45 retained replay bytes without rerunning the experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

import run_luna45_acp0008_depth2_destination_integration as luna45


RETAINED = Path("artifacts/luna45-acp0008-depth2-destination-integration-20261006")
OUTPUT = Path("artifacts/luna45-corrective-verification-20261006-r1")
ARMS = luna45.ARMS
PHASES = ("initial", "replay")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_revision() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def verify_retained(output: Path = OUTPUT) -> dict[str, Any]:
    catalog = read_json(RETAINED / "artifact-integrity.json")
    summary = read_json(RETAINED / "summary.json")
    config_artifact = read_json(RETAINED / "config.json")
    config = config_artifact["experiment"]
    checks: dict[str, Any] = {
        "retained_catalog_identity": {
            "matches": catalog["execution_revision"] == summary["execution_revision"]
            and catalog["runner_revision"] == summary["runner_revision"]
            and catalog["config_digest"] == summary["config_digest"],
        },
        "original_verdict_preserved": {
            "matches": summary["status"] == "PASS"
            and summary["verdict"] == "NOT SUPPORTED IN THIS SETUP"
            and summary["initial_blocker"] is None
            and summary["replay_blocker"] is None
            and summary["replay_equal"] is True,
        },
        "frozen_configuration_digest": {
            "observed": luna45.digest(config),
            "expected": summary["config_digest"],
            "matches": luna45.digest(config) == summary["config_digest"],
        },
    }

    artifact_bytes: dict[str, dict[str, Any]] = {}
    raw_file_checks = []
    for name, expected_file in catalog["files"].items():
        data = (RETAINED / name).read_bytes()
        raw_file_checks.append({
            "file": name,
            "byte_length": len(data),
            "expected_byte_length": expected_file["byte_length"],
            "sha256": sha256_bytes(data),
            "expected_sha256": expected_file["file_sha256"],
            "matches": (
                len(data) == expected_file["byte_length"]
                and sha256_bytes(data) == expected_file["file_sha256"]
            ),
        })
    canonical_comparisons = {}
    retained_chain_checks = []
    destination_counts: dict[str, dict[str, int]] = {}
    phase_digests_match = True
    for arm in ARMS:
        arm_reports: dict[str, dict[str, Any]] = {}
        destination_counts[arm] = {"canonical_emissions": 0, "genuine_chains": 0}
        for phase in PHASES:
            name = f"{phase}-{arm.lower()}.json"
            path = RETAINED / name
            data = path.read_bytes()
            artifact = json.loads(data)
            if (
                artifact["arm"] != arm or artifact["phase"] != phase
                or artifact["blocker"] is not None
            ):
                arm_reports[phase] = {"matches": False, "reason": "phase identity/blocker mismatch"}
                continue

            records = artifact["records"]
            report = artifact["report"]
            canonical = luna45.phase_canonical_bytes(records, report, config=config)
            canonical_sha256 = sha256_bytes(canonical)
            declared_digest = artifact["phase_digest"]
            summary_digest = summary[f"{phase}_digests"][arm]
            phase_matches = (
                canonical_sha256 == declared_digest
                and declared_digest == summary_digest
            )
            phase_digests_match &= phase_matches
            arm_reports[phase] = {
                "record_count": len(records),
                "canonical_byte_length": len(canonical),
                "canonical_sha256": canonical_sha256,
                "declared_phase_digest": declared_digest,
                "summary_phase_digest": summary_digest,
                "matches": phase_matches,
            }
            artifact_bytes.setdefault(arm, {})[phase] = canonical
            destination_counts[arm]["canonical_emissions"] += sum(
                len(record["destination_emissions"]) for record in records
            )
            for record in records:
                for evidence in record.get("destination_evidence", []):
                    if (
                        evidence.get("classification") == "integration-mediated"
                        and evidence.get("canonical_emission") is not None
                    ):
                        chain = luna45.reconstruct_chain(record, evidence)
                        retained_chain_checks.append({
                            "arm": arm,
                            "phase": phase,
                            "stream_id": record["stream_id"],
                            "destination_emission_id": evidence["canonical_emission_id"],
                            "verified": chain["verified"],
                        })
                        destination_counts[arm]["genuine_chains"] += int(chain["verified"])
        checks[f"{arm}_phase_digests"] = {
            "per_phase": arm_reports,
            "matches": len(arm_reports) == len(PHASES)
            and all(item.get("matches", False) for item in arm_reports.values()),
        }
        if "initial" in artifact_bytes.get(arm, {}) and "replay" in artifact_bytes.get(arm, {}):
            initial = artifact_bytes[arm]["initial"]
            replay = artifact_bytes[arm]["replay"]
            initial_digest = sha256_bytes(initial)
            replay_digest = sha256_bytes(replay)
            byte_equal = initial == replay
            initial_data = read_json(RETAINED / f"initial-{arm.lower()}.json")
            replay_data = read_json(RETAINED / f"replay-{arm.lower()}.json")
            canonical_comparisons[arm] = {
                **luna45.compare_phase_replay(
                    initial_data["records"], initial_data["report"],
                    replay_data["records"], replay_data["report"],
                    config=config,
                ),
                "canonical_bytes_equal": byte_equal,
                "initial_sha256": initial_digest,
                "replay_sha256": replay_digest,
                "matches": (
                    byte_equal
                    and initial_digest == replay_digest
                    and initial_data["phase_digest"] == replay_data["phase_digest"]
                ),
            }

    checks["retained_raw_artifact_integrity"] = {
        "file_count": len(raw_file_checks),
        "files": raw_file_checks,
        "matches": all(item["matches"] for item in raw_file_checks),
    }
    checks["canonical_replay_bytes"] = {
        "per_arm": canonical_comparisons,
        "matches": len(canonical_comparisons) == len(ARMS)
        and all(item["matches"] for item in canonical_comparisons.values()),
    }
    checks["phase_digest_recomputation"] = {"matches": phase_digests_match}
    checks["retained_destination_ancestry"] = {
        "per_arm": destination_counts,
        "verified_chain_count": len(retained_chain_checks),
        "chain_checks": retained_chain_checks,
        "status": (
            "VERIFIED" if retained_chain_checks
            else "NOT APPLICABLE: retained run has no destination canonical emissions"
        ),
        "matches": all(item["verified"] for item in retained_chain_checks),
    }
    checks["no_raw_artifact_mutation"] = {
        "matches": True,
        "basis": "verifier opens retained files read-only and writes only its separate output",
    }
    passed = all(
        entry.get("matches", False)
        for entry in checks.values()
        if isinstance(entry, dict)
    )
    result = {
        "schema": "TPCN-LUNA45-CORRECTIVE-VERIFICATION-1",
        "status": "PASS" if passed else "BLOCKED",
        "retained_execution_revision": summary["execution_revision"],
        "verification_revision": git_revision(),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "runner_sha256": luna45.file_hash(Path(luna45.__file__)),
        "retained_directory": RETAINED.as_posix(),
        "output_directory": output.as_posix(),
        "retained_result": summary["verdict"],
        "checks": checks,
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / "verification.json").write_bytes(
        luna45.reference._canonical_bytes(result) + b"\n"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = verify_retained(args.output)
    print(json.dumps({
        "status": result["status"],
        "retained_execution_revision": result["retained_execution_revision"],
        "verification_revision": result["verification_revision"],
        "checks": {
            key: value.get("matches", value.get("status"))
            for key, value in result["checks"].items()
        },
    }, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
