"""Post-outcome integrity checks; no alteration of preregistered gates."""
import gzip
import hashlib
import json
from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "artifacts/luna47g"


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def test_per_sample_provenance_linkage():
    manifest = json.loads((TARGET / "manifest.json").read_bytes())
    prov = manifest["provenance"]
    index = [json.loads(line) for line in
             gzip.decompress((TARGET / "sample-provenance.jsonl.gz").read_bytes()).splitlines()]
    assert len(index) == 4008
    files = {name: gzip.decompress((TARGET / name).read_bytes()).splitlines()
             for name in ("samples.jsonl.gz", "corners.jsonl.gz")}
    ids = set()
    for entry in index:
        row = json.loads(files[entry["file"]][entry["line"] - 1])
        assert entry["id"] == row["id"] and entry["id"] not in ids
        ids.add(entry["id"])
        assert hashlib.sha256(canonical(row)).hexdigest() == entry["row_sha256"]
        assert entry["execution_revision"] == prov["execution_revision"]
        assert entry["source_hashes"] == prov["sources"]
        assert entry["configuration_sha256"] == prov["configuration_sha256"]
        assert entry["fixture_sha256"] == prov["fixture_sha256"]
        assert entry["numeric_absolute_tolerance"] == 1e-12
        assert entry["neutral_tolerance"] == 1e-6


def test_package_hashes():
    manifest = json.loads((TARGET / "package-manifest.json").read_bytes())
    assert manifest["model_manifest_sha256"] == hashlib.sha256(
        (TARGET / "manifest.json").read_bytes()).hexdigest()
    for name, entry in manifest["files"].items():
        data = (TARGET / name).read_bytes()
        assert entry["sha256"] == hashlib.sha256(data).hexdigest()
        assert entry["bytes"] == len(data)


def test_controlled_corners_reconcile():
    rows = [json.loads(line) for line in
            gzip.decompress((TARGET / "corners.jsonl.gz").read_bytes()).splitlines()]
    summary = json.loads((TARGET / "summary.json").read_bytes())
    assert len(rows) == 168 and len(summary["interactions"]) == 42
    for entry in summary["interactions"]:
        group = [r for r in rows if r["band"] == entry["band"] and r["pair"] == entry["pair"]]
        assert len(group) == 4
        flags = {",".join(map(str, r["directions"])): int(not r["outcome"]["pass_"]) for r in group}
        assert flags == entry["failures"]
        assert flags["1,1"] - flags["1,-1"] - flags["-1,1"] + flags["-1,-1"] == entry["difference_in_differences"]
        assert all(r["noise_units"] == group[0]["noise_units"] for r in group)
