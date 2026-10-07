"""Validate publication ownership, immutable lane refs, evidence bytes and links."""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/luna47-review"
DOCS = [
    "workflow/docs/luna/LUNA_WORKFLOW.md",
    "workflow/ARCHITECTURE_CHANGELOG.md",
    "workflow/handoffs/luna-0-independent-review-luna47-20261006.md",
]
PINS = {
    "a": "eb56684eaa10dc9b765927ef8e883c7d56cb025b",
    "b": "41a0a28f6f85023b8933a47650f66628b0a9ceb0",
    "c": "609b2e5f8a7ae123f9b7f7da5c89378e29353624",
    "d": "deb01f07a0d6b315855d2fab57d558be303f95f3",
    "e": "4e413415a31853877333810d7093f415f93f72f7",
    "f": "8cddf9d5d3fc0ea6971dc54645e8033c290dc852",
    "g": "42698364392901de955ca04a770c975a1b0a94d2",
}


def git(*args: str, cwd: Path = ROOT) -> bytes:
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd)


def normalize_line_endings(data: bytes) -> bytes:
    normalized = data.replace(b"\r\n", b"\n")
    assert b"\r" not in normalized, "Python files may use LF or CRLF, not bare CR."
    return normalized


def validate() -> None:
    assert git("branch", "--show-current").decode().strip() == "copilot/luna47-independent-review"
    report: dict = {"schema": "LUNA47-REVIEW-PUBLICATION-1", "lanes": {}, "files": {}}
    for lane, pin in PINS.items():
        cwd = ROOT.parent / f"luna47{lane}"
        head = git("rev-parse", "HEAD", cwd=cwd).decode().strip()
        status = git("status", "--porcelain", cwd=cwd).decode()
        remote = git("ls-remote", "origin", f"refs/heads/copilot/luna47{lane}-investigation").decode().split()[0]
        assert head == pin == remote and not status, (lane, head, status, remote)
        report["lanes"][lane] = {"head": head, "remote": remote, "status": status}
    staged = git("diff", "--cached", "--name-only").decode().splitlines()
    assert staged, "Stage publication paths before running."
    assert all(p in DOCS or p.startswith("artifacts/luna47-review/") for p in staged), staged
    for path in staged:
        if path == "artifacts/luna47-review/publication-verification.json":
            continue
        p = ROOT / path
        assert "__pycache__" not in path
        raw = p.read_bytes()
        blob = git("show", f":{path}")
        if p.suffix in (".json", ".xml", ".log"):
            assert raw == blob, f"Raw evidence was altered by staging: {path}"
        elif p.suffix == ".py":
            assert normalize_line_endings(raw) == normalize_line_endings(blob), (
                f"Working Python differs from staged content beyond LF/CRLF: {path}")
        if p.suffix == ".json":
            json.loads(raw)
        elif p.suffix == ".xml":
            ET.fromstring(raw)
        elif p.suffix == ".py":
            ast.parse(blob.decode("utf-8"), filename=path)
        report["files"][path] = {
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "staged_sha256": hashlib.sha256(blob).hexdigest(),
            "bytes": len(raw),
        }
    for p in (OUT / "SYNTHESIS.md", ROOT / DOCS[-1]):
        for link in re.findall(r"\[[^]]*\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
            if "://" not in link and not link.startswith("#"):
                assert (p.parent / link.split("#")[0]).exists(), (str(p), link)
    raw_check = subprocess.run(
        ["git", "--no-pager", "diff", "--cached", "--check"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (OUT / "staged-whitespace-check.log").write_bytes(raw_check.stdout)
    report["raw_staged_whitespace_check"] = {
        "exit": raw_check.returncode, "output_path": "staged-whitespace-check.log",
        "output_sha256": hashlib.sha256(raw_check.stdout).hexdigest(),
        "policy": "Raw JSON/XML/logs preserve Windows CRLF and traceback whitespace; not a scientific waiver.",
    }
    scoped = [p for p in staged if not p.endswith((".log", ".xml", ".json"))]
    scoped_check = subprocess.run(
        ["git", "--no-pager", "diff", "--cached", "--check", "--", *scoped],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    report["source_docs_whitespace_check"] = {
        "exit": scoped_check.returncode, "output": scoped_check.stdout.decode()}
    assert scoped_check.returncode == 0, scoped_check.stdout.decode()
    report["status"] = "PASS - ownership, live lane parity/cleanliness, schemas, scripts and evidence bytes"
    report["self_hash_exclusion"] = "This generated report is excluded to avoid self-referential hashing."
    (OUT / "publication-verification.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report["status"])
    print("Raw whitespace exit:", raw_check.returncode,
          "; source/docs whitespace exit:", scoped_check.returncode)


if __name__ == "__main__":
    validate()
