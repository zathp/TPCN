"""Read-only Stage A metadata/hash checker. No model/oracle/fixture execution."""

import hashlib
import json
from pathlib import Path
import subprocess


BASELINE = "73aaa50f97ceab322907875ae4dcf23e7541c3b5"
DESIGN = "3e7d31b9a527e908b21abee3766906084e7cd082"
HANDOFF = "a303ebb835b72fdd01c86df478431b8638aacbb4"
BLOCKED = "BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE"
DIRECTORY = Path(__file__).resolve().parent
ROOT = DIRECTORY.parents[2]
checks = 0


def require(condition, description):
    global checks
    if not condition:
        raise ValueError(description)
    checks += 1
    print("PASS " + description)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT)


def load(name):
    return json.loads((DIRECTORY / name).read_text(encoding="utf-8"))


def main():
    manifest = load("manifest.json")
    sources = load("sources.json")
    table = load("expected_outcomes.json")
    require(manifest["format"] == "luna63c-certificate-manifest"
            and manifest["version"] == 1, "manifest format/version")
    require(sources["format"] == "luna63c-certificate-sources"
            and sources["version"] == 1, "sources format/version")
    require(table["format"] == "luna63c-symbolic-expected-outcomes"
            and table["version"] == 1, "expectations format/version")
    require(all(x["baseline"] == BASELINE for x in (manifest, sources, table)),
            "all baseline pins")
    require(table["design_revision"] == DESIGN
            and table["handoff_revision"] == HANDOFF, "design/handoff pins")
    require(all(x["disposition"] == BLOCKED for x in (manifest, sources, table)),
            "all dispositions blocked")
    require(not table["mechanism_executed"] and not table["stage_b_eligible"],
            "no execution or Stage B eligibility")
    require(table["unresolved_gates"] == ["N1", "N2", "N3", "N4", "N5", "N6"],
            "unresolved gates retained")
    require(git("rev-parse", "--verify", BASELINE + "^{commit}").decode().strip()
            == BASELINE, "frozen baseline commit object exists")
    require(subprocess.run(
        ["git", "--no-pager", "merge-base", "--is-ancestor", BASELINE, "HEAD"],
        cwd=ROOT, check=False).returncode == 0,
        "frozen baseline is ancestor of HEAD")
    for item in sources["sources"]:
        spec = item["revision"] + ":" + item["path"]
        data = git("show", spec)
        require(hashlib.sha256(data).hexdigest() == item["sha256"],
                "source SHA256 " + item["path"])
        require(git("rev-parse", spec).decode().strip() == item["git_blob"],
                "source Git blob " + item["path"])
        require(data == git("show", BASELINE + ":" + item["path"]),
                "source equals integrated baseline " + item["path"])
    require(set(manifest["files"]) == {
        "CERTIFICATE.md", "expected_outcomes.json", "sources.json",
        "check_certificate.py"}, "exact noncircular manifest file set")
    require({p.name for p in DIRECTORY.iterdir()} ==
            set(manifest["files"]) | {"manifest.json"}, "certificate-only file set")
    for name, expected_hash in manifest["files"].items():
        data = (DIRECTORY / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected_hash,
                "artifact SHA256 " + name)
        unframed = data.replace(b"\r\n", b"")
        require(not data.startswith(b"\xef\xbb\xbf") and b"\r" not in unframed
                and b"\n" not in unframed and data.endswith(b"\r\n"),
                "UTF-8/CRLF/no-BOM framing " + name)
        data.decode("utf-8")
    require(table["bounds"] == {
        "within_budget_attempts": 16, "overflow_attempts": 1,
        "timer_records": 24, "output_records": 1, "unique_records": 42,
        "accepted_store": 1, "accepted_recall_including_duplicates": 8,
        "accepted_reset": 1, "live_flow_tokens": 1, "live_expiry_tokens": 1,
        "precision_min_bits": 256, "precision_max_bits": 1024,
        "bisections_per_root_max": 128,
        "identity_type": "unsigned 64-bit; no wrap; check before allocation"},
        "immutable work/record caps")
    require(16 + 1 + 24 + 1 == table["bounds"]["unique_records"],
            "42 arithmetic identity, not runtime enforcement")
    require(table["model"]["field"] == ["R*(-x-y)", "R*(x-y)"]
            and table["model"]["alpha"] == table["model"]["omega"] == "1 TU^-1"
            and table["model"]["g"] == "exp(-pi/4)/sqrt(2)"
            and table["model"]["theta"] == "2*g"
            and table["model"]["q"] == "g", "symbolic model identities")
    require(table["comparisons"]["A1_state"] ==
            "strict ||candidate-oracle||_2 < theta/4"
            and table["comparisons"]["candidate_operational_error_bound"] is None
            and table["root_identities"]["numeric_intervals_and_ceilings"] is None,
            "strict A1 rule and unresolved numerical claims")
    require([f["id"] for f in table["fixtures"]] ==
            ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"],
            "exact C0-C7 table names")
    require(all(f["execution"] == "NOT RUN" for f in table["fixtures"]),
            "all expectations unexecuted")
    require([c["A"] for c in table["fixtures"][2]["cases"]] ==
            ["0", "q/2", "q", "neighbor below q", "neighbor above q", "1", "2"],
            "C2 exact symbolic values and unresolved neighbors")
    require(table["fixtures"][3]["hold_durations_TU"] ==
            table["fixtures"][5]["hold_durations_TU"] == [0, 1, 2],
            "C3/C5 frozen HOLD durations")
    require(len(table["fixtures"][7]["cases"]) == 14,
            "C7 edge-case coverage count")
    require(table["future_replay"]["fresh_executions_min"] == 2
            and not table["future_replay"]["copied_artifacts_allowed"],
            "fresh future replay requirement")
    require("**Disposition: " + BLOCKED + ".**" in
            (DIRECTORY / "CERTIFICATE.md").read_text(encoding="utf-8"),
            "report blocked disposition")
    print("SELF-CONSISTENCY/HASH CHECKS: %d passed, 0 failed; "
          "scientific fixtures: 0 executed; numerical gates remain BLOCKED" % checks)
    print("manifest.json outer SHA256: " +
          hashlib.sha256((DIRECTORY / "manifest.json").read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
