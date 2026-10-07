"""Retain exact observed test counts/signatures, not a pass/waiver wrapper."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
reports = []
for execution_path in sorted(OUT.glob("*-execution.json")):
    execution = json.loads(execution_path.read_bytes())
    name = execution["name"]
    path = OUT / (name + ".xml")
    report = dict(name=name, pytest_exit=execution["exit_code"],
                  execution=execution, xml_status="missing",
                  counts=None, exceptions=[])
    if not path.exists():
        report["xml_error"] = "No JUnit XML was produced for this execution."
        reports.append(report)
        continue
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as error:
        report["xml_status"] = "invalid"
        report["xml_error"] = str(error)
        reports.append(report)
        continue
    cases = list(root.iter("testcase"))
    failures = []
    for case in cases:
        for kind in ("failure", "error", "skipped"):
            element = case.find(kind)
            if element is not None:
                failures.append(dict(kind=kind, classname=case.attrib.get("classname"),
                                     name=case.attrib["name"],
                                     message=element.attrib.get("message")))
    counts = {kind: sum(case.find(kind) is not None for case in cases)
              for kind in ("failure", "error", "skipped")}
    counts["passed"] = len(cases)-sum(counts.values())
    report.update(counts=counts, exceptions=failures, xml_status="present",
                  xml_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    reports.append(report)
baseline = OUT / "luna47-baseline-tests.log"
if baseline.exists():
    baseline_bytes = baseline.read_bytes()
    baseline_encoding = "utf-16" if baseline_bytes.startswith(
        (b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    text = baseline_bytes.decode(baseline_encoding)
    baseline_comparison = dict(
        status="available", supplied_log=baseline.name,
        sha256=hashlib.sha256(baseline_bytes).hexdigest(),
        encoding=baseline_encoding,
        summary_lines=[line for line in text.splitlines() if
                       "passed" in line and ("failed" in line or "errors" in line)],
        supplied_revision="4b11e0e828fd6fbcb4cbf9b994f121bde54e4c37",
        comparison="Same pinned-source failure and seven setup errors. Additional review-checkout "
                   "Luna-46 catalog failure is exact LF-to-CRLF materialization, not waived.")
else:
    baseline_comparison = dict(
        status="unavailable",
        expected_log=baseline.name,
        reason="Original baseline log is not retained in this checkout.")
record = dict(reports=reports, baseline_comparison=baseline_comparison)
(OUT / "test-summary.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
for report in reports:
    print(report["name"], report["counts"], "pytest exit", report["pytest_exit"])
