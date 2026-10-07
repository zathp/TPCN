"""Independently validate byte/source claims and retained 33-input inventory."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
report = {"retained_inputs": [], "manifest_checks": []}


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT)


def sha(value):
    return hashlib.sha256(value).hexdigest()


def load(letter, name):
    return json.loads((ROOT.parent / f"luna47{letter}" / "artifacts" /
                       f"luna47{letter}" / name).read_bytes())


def require(condition, description):
    if not condition:
        raise AssertionError(description)


inputs = load("a", "inputs.json")
for path, pin in inputs["integrity"]["inputs"].items():
    path = path.replace("\\", "/")
    data = git("show", f"{BASE}:{path}")
    require(sha(data) == pin["file_sha256"], "retained input SHA " + path)
    require(len(data) == pin["byte_length"], "retained input length " + path)
    row = dict(path=path, baseline_git_blob=git(
        "rev-parse", f"{BASE}:{path}").decode().strip(),
        consumed_sha256=sha(data), consumed_bytes=len(data), materializations={})
    for letter in "abcdefg":
        lane = ROOT.parent / f"luna47{letter}"
        physical = (lane / path).read_bytes()
        require(physical == data or physical == data.replace(b"\n", b"\r\n"),
                "unexplained materialization " + letter + ":" + path)
        row["materializations"][letter] = dict(
            file_sha256=sha(physical), file_bytes=len(physical),
            exact=physical == data, exact_LF_to_CRLF=physical != data)
    report["retained_inputs"].append(row)
require(len(report["retained_inputs"]) == 33, "33 retained inputs")


def file_pin(letter, name, expected, length=None):
    data = (ROOT.parent / f"luna47{letter}" / "artifacts" /
            f"luna47{letter}" / name).read_bytes()
    require(sha(data) == expected, f"{letter} manifest physical SHA {name}")
    if length is not None:
        require(len(data) == length, f"{letter} manifest physical length {name}")
    report["manifest_checks"].append(dict(lane=letter, path=name, file_sha256=sha(data)))


for name, pin in load("a", "manifest.json")["files"].items():
    file_pin("a", name, pin["sha256"], pin["byte_length"])
for name, expected in load("c", "manifest.json")["files_sha256"].items():
    file_pin("c", name, expected)
for name, pin in load("g", "manifest.json")["files"].items():
    file_pin("g", name, pin["sha256"], pin["bytes"])
for name, pin in load("g", "package-manifest.json")["files"].items():
    file_pin("g", name, pin["sha256"], pin["bytes"])
file_pin("g", "manifest.json", load("g", "package-manifest.json")["model_manifest_sha256"])

for letter, sources in (
    ("a", load("a", "manifest.json")["code"]["files"]),
    ("b", load("b", "results.json")["source_hashes"]),
    ("c", load("c", "replay.json")["provenance"]["source_sha256_lf"]),
    ("g", load("g", "manifest.json")["provenance"]["sources"]),
):
    lane = ROOT.parent / f"luna47{letter}"
    for path, pin in sources.items():
        data = (lane / path).read_bytes()
        blob = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=lane)
        if letter == "a":
            expected, raw_expected = pin["git_sha256"], pin["working_sha256"]
        elif letter == "b":
            expected, raw_expected = pin["committed_sha256"], pin["worktree_sha256"]
        elif letter == "c":
            expected, raw_expected = pin, None
        else:
            expected, raw_expected = pin["git_blob_sha256"], pin["raw_sha256"]
        require(sha(blob) == expected, f"{letter} source blob {path}")
        if raw_expected:
            require(sha(data) == raw_expected, f"{letter} raw execution source {path}")
        report["manifest_checks"].append(dict(lane=letter, source=path,
                                               git_sha256=sha(blob), file_sha256=sha(data)))
for pin in load("d", "evidence.json")["provenance"]["sources"]:
    lane = ROOT.parent / "luna47d"
    data = (lane / pin["path"]).read_bytes()
    require(sha(data.replace(b"\r\n", b"\n")) == pin["sha256_lf"], "D source LF SHA")
    require(subprocess.check_output(["git", "rev-parse", f"HEAD:{pin['path']}"], cwd=lane
                                   ).decode().strip() == pin["git_blob"], "D source Git blob")
report["status"] = "PASS"
(OUT / "independent-manifest-verification.json").write_text(
    json.dumps(report, indent=2)+"\n", encoding="utf-8")
print("PASS", len(report["retained_inputs"]), "retained input identities;",
      len(report["manifest_checks"]), "manifest/source checks")
