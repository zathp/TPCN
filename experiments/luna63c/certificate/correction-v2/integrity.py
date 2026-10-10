"""Read-only correction-v2 blob integrity checks; no model evaluation."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PREFIX = "experiments/luna63c/certificate/"
REVISION = "181b6440821e1dd6beede7e34cab9b6baada601a"
FILES = {"REPORT.md", "calculate.py", "test_certificate.py", "witnesses.json",
         "integrity.py", "manifest.json"}
checks = 0


def require(condition, message):
    global checks
    if not condition:
        raise ValueError(message)
    checks += 1
    print("PASS " + message)


def git(*args, data=None):
    return subprocess.check_output(["git", "--no-pager", *args],
                                   input=data, cwd=ROOT)


def oid(data, path=None):
    args = ["hash-object", "--stdin"]
    args += ["--path", path] if path else ["--no-filters"]
    return git(*args, data=data).decode().strip()


def artifact(name, prepare):
    path = PREFIX + "correction-v2/" + name
    checkout = (HERE / name).read_bytes()
    if prepare:
        data = checkout.replace(b"\r\n", b"\n")
        require(oid(data) == oid(checkout, path), "proposed Git-clean bytes " + name)
    else:
        data = git("show", "HEAD:" + path)
        require(oid(data) == git("rev-parse", ":" + path).decode().strip(),
                "index equals committed blob " + name)
        require(oid(data) == oid(checkout, path), "checkout equals committed blob " + name)
    require(oid(data) == oid(data, path) ==
            oid(data.replace(b"\n", b"\r\n"), path),
            "LF/CRLF clean-filter portability " + name)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    args = parser.parse_args()
    require(git("rev-parse", "--verify", REVISION + "^{commit}").decode().strip()
            == REVISION, "historical certificate commit exists")
    require(subprocess.run(["git", "merge-base", "--is-ancestor", REVISION, "HEAD"],
                           cwd=ROOT).returncode == 0, "historical baseline ancestry")
    require({p.name for p in HERE.iterdir()} == FILES, "exact correction-v2 file set")
    contents = {name: artifact(name, args.prepare) for name in sorted(FILES)}
    manifest = json.loads(contents["manifest.json"])
    require(manifest["hash_scope"] == "raw Git blob content bytes",
            "raw Git blob SHA256 scope")
    require(manifest["old_revision"] == REVISION, "unchanged historical revision pin")
    require(set(manifest["files"]) == FILES - {"manifest.json"},
            "noncircular manifest files")
    for name, digest in manifest["files"].items():
        require(hashlib.sha256(contents[name]).hexdigest() == digest,
                "v2 blob SHA256 " + name)
    for name, digest in manifest["prior_files"].items():
        path = PREFIX + name
        committed = git("show", REVISION + ":" + path)
        require(hashlib.sha256(committed).hexdigest() == digest,
                "historical raw blob SHA256 " + name)
        require(oid((HERE.parent / name).read_bytes(), path) == oid(committed),
                "historical certificate checkout unchanged " + name)
        require(git("rev-parse", "HEAD:" + path) == git("rev-parse", ":" + path)
                == git("rev-parse", REVISION + ":" + path),
                "historical certificate HEAD/index unchanged " + name)
    source_metadata = json.loads(git("show", REVISION + ":" + PREFIX + "sources.json"))
    for item in source_metadata["sources"]:
        spec = item["revision"] + ":" + item["path"]
        data = git("show", spec)
        require(hashlib.sha256(data).hexdigest() == item["sha256"]
                and git("rev-parse", spec).decode().strip() == item["git_blob"],
                "pinned source blob/hash " + item["path"])
    w = json.loads(contents["witnesses.json"])
    require(w["precision_bits"] == 256 and w["bisections_per_root"] == 128,
            "immutable precision/root caps")
    require(w["N2"].startswith("CLOSED") and w["N4"].startswith("BLOCKED")
            and w["N5"].startswith("BLOCKED") and "Stage B" in w["N6"],
            "honest partial disposition and N6 boundary")
    require(w["disposition"] == "BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE",
            "combined BLOCKED disposition")
    for name in sorted(FILES):
        print(name, "raw Git blob SHA256", hashlib.sha256(contents[name]).hexdigest())
    print("%d integrity checks passed, 0 failed; %s" % (
        checks, "PREPUBLICATION ONLY" if args.prepare else "committed blob verification"))


if __name__ == "__main__":
    main()
