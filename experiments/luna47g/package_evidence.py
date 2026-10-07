"""Post-outcome packaging only: does not change model, draws, gates or verdict."""
from __future__ import annotations

import gzip
import json
from pathlib import Path
import subprocess
import sys

from simulate import ROOT, canonical, sha

TARGET = ROOT / "artifacts/luna47g"


def load_rows(name: str) -> list[dict]:
    return [json.loads(line) for line in gzip.decompress((TARGET / name).read_bytes()).splitlines()]


def derive(rows: list[dict]) -> dict:
    bands = {}
    for name in ("nominal", "selected", "general", "loose", "stress"):
        group = [r for r in rows if r["band"] == name]
        gate_witnesses = {}
        subfailures = {}
        max_state = max_output = max_final = 0.0
        max_events = max_outputs = total_events = total_outputs = 0
        asymmetric = 0
        for row in group:
            result = row["outcome"]
            for gate in result["failed"]:
                gate_witnesses.setdefault(gate, row["id"])
            if any(v["admission_difference"] or v["output_count_difference"]
                   for v in result["asymmetry"].values()):
                asymmetric += 1
            for label in ("positive", "negative"):
                runs = result["runs"][label]
                single, near, far, moderate, extreme = [
                    runs[k] for k in ("single", "near", "far", "moderate", "extreme")]
                flags = {
                    "single_early_output": bool(single["outputs"]),
                    "single_low_peak": single["peak"] < 0.3,
                    "single_not_admitted": single["admitted"] != 1,
                    "near_no_output": not near["outputs"],
                    "near_peak_ratio": near["peak"] < 1.5 * single["peak"],
                    "near_not_both_admitted": near["admitted"] != 2,
                    "far_output": bool(far["outputs"]),
                    "moderate_no_output": not moderate["outputs"],
                    "moderate_multiple_outputs": len(moderate["outputs"]) > 1,
                    "moderate_admission_loss": moderate["admitted"] != 3,
                    "moderate_compression_ratio": abs(sum(o["value"] for o in moderate["outputs"]))
                    > 0.9 * moderate["deposition"],
                    "extreme_fewer_than_two_outputs": len(extreme["outputs"]) < 2,
                    "extreme_no_local_return_output": extreme["return_outputs"] < 1,
                    "extreme_output_sum_exceeds_deposition":
                    abs(sum(o["value"] for o in extreme["outputs"])) > extreme["deposition"],
                }
                for flag, failed in flags.items():
                    key = f"{label}:{flag}"
                    subfailures[key] = subfailures.get(key, 0) + int(failed)
            all_runs = [v for group_ in result["runs"].values() for v in group_.values()]
            all_runs.extend(v for pair in result["zero_offset_controls"].values() for v in pair)
            for run in all_runs:
                max_state = max(max_state, run["peak"])
                max_final = max(max_final, abs(run["final"]))
                max_output = max(max_output, max((abs(o["value"]) for o in run["outputs"]), default=0))
                max_events = max(max_events, run["processed"])
                max_outputs = max(max_outputs, len(run["outputs"]))
                total_events += run["processed"]
                total_outputs += len(run["outputs"])
        bands[name] = dict(first_failure_witnesses=gate_witnesses,
                           signed_subfailure_counts=subfailures,
                           max_abs_state=max_state, max_abs_output=max_output,
                           max_abs_final_state=max_final, max_events_per_fixture=max_events,
                           max_outputs_per_fixture=max_outputs,
                           total_local_events_including_controls=total_events,
                           total_outputs_including_controls=total_outputs,
                           physical_offset_asymmetric_samples=asymmetric)
    return bands


def baseline_failure_evidence() -> dict:
    path = "artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json"
    baseline = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
    blob = subprocess.check_output(["git", "show", f"{baseline}:{path}"], cwd=ROOT)
    raw = (ROOT / path).read_bytes()
    return dict(path=path, baseline_revision=baseline,
                pinned_catalog_sha256="a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e",
                git_blob_sha256=sha(blob), worktree_raw_sha256=sha(raw),
                worktree_lf_normalized_sha256=sha(raw.replace(b"\r\n", b"\n")),
                bytes_differ_only_by_crlf=raw.replace(b"\r\n", b"\n") == blob,
                diagnostic_source_unchanged=subprocess.check_output(
                    ["git", "diff", baseline, "--", "run_luna46_depth_scaling_diagnostic.py",
                     "tests/test_luna46_depth_scaling_diagnostic.py", path], cwd=ROOT) == b"")


def main() -> None:
    if TARGET.resolve() != ROOT.resolve() / "artifacts/luna47g":
        raise ValueError("output directory alias")
    verify = "--verify" in sys.argv[1:]
    manifest = json.loads((TARGET / "manifest.json").read_bytes())
    prov = manifest["provenance"]
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    rows = load_rows("samples.jsonl.gz")
    corners = load_rows("corners.jsonl.gz")
    index = []
    for filename, group in (("samples.jsonl.gz", rows), ("corners.jsonl.gz", corners)):
        for line, row in enumerate(group, 1):
            index.append(dict(id=row["id"], file=filename, line=line,
                              row_sha256=sha(canonical(row)), execution_revision=prov["execution_revision"],
                              authorization_revision=prov["authorization_revision"],
                              production_evidence_revision=prov["production_evidence_revision"],
                              configuration_sha256=prov["configuration_sha256"],
                              fixture_sha256=prov["fixture_sha256"], source_hashes=prov["sources"],
                              numeric_absolute_tolerance=prov["tolerance"],
                              neutral_tolerance=prov["neutral_tolerance"]))
    diagnostics = dict(post_outcome_packaging=True, bands=derive(rows),
                       baseline_regression_failure=baseline_failure_evidence())
    payloads = {"sample-provenance.jsonl.gz": gzip.compress(
        b"".join(canonical(r) for r in index), mtime=0), "diagnostics.json": canonical(diagnostics)}
    package_manifest = dict(packaging_revision=revision, model_manifest_sha256=sha(
        (TARGET / "manifest.json").read_bytes()), script_sha256=sha(Path(__file__).read_bytes()),
                            files={k: dict(sha256=sha(v), bytes=len(v)) for k, v in payloads.items()})
    if verify:
        retained = json.loads((TARGET / "package-manifest.json").read_bytes())
        if retained["script_sha256"] != package_manifest["script_sha256"]:
            raise ValueError("packaging script hash mismatch")
        if retained["model_manifest_sha256"] != package_manifest["model_manifest_sha256"]:
            raise ValueError("model manifest linkage mismatch")
        if retained["files"] != package_manifest["files"]:
            raise ValueError("package file hashes mismatch")
        for name, payload in payloads.items():
            if (TARGET / name).read_bytes() != payload:
                raise ValueError(f"retained payload mismatch: {name}")
        print("Packaging replay: PASS")
    else:
        payloads["package-manifest.json"] = canonical(package_manifest)
        for k in payloads:
            if (TARGET / k).exists() or (TARGET / k).resolve().parent != TARGET.resolve():
                raise ValueError("refusing overwrite/alias")
        for k, v in payloads.items():
            (TARGET / k).write_bytes(v)
        print(json.dumps(diagnostics, indent=2))


if __name__ == "__main__":
    main()
