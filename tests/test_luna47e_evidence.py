"""Offline evidence checks and mutation controls; no production imports."""
import copy
import importlib.util
import hashlib
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "luna47e_validate", ROOT / "experiments/luna47e/validate.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
CAPTURE_SPEC = importlib.util.spec_from_file_location(
    "luna47e_capture", ROOT / "experiments/luna47e/capture_sources.py"
)
assert CAPTURE_SPEC and CAPTURE_SPEC.loader
capture_sources = importlib.util.module_from_spec(CAPTURE_SPEC)
CAPTURE_SPEC.loader.exec_module(capture_sources)


def matrix():
    return copy.deepcopy(validator.load("artifacts/luna47e/primitive-matrix.json"))


def test_retained_matrix_and_source_references():
    result = validator.validate(matrix())
    assert result["families"] == 8
    assert len(result["independent_exact_part_offers"]) == 8


@pytest.mark.parametrize("mutation", [
    "owner", "family", "part", "stock", "price", "ref", "criteria",
    "criteria_path", "catalog_path", "context_path", "baseline", "hardware",
    "fpaa", "calculation", "context",
])
def test_rejects_documentary_claim_mutations(mutation):
    m = matrix()
    if mutation == "owner":
        m["owner_access"]["region"] = "assumed US"
    elif mutation == "family":
        m["primitives"].pop()
    elif mutation == "part":
        m["components"][2]["part_number"] = "unverified-substitute"
    elif mutation == "stock":
        m["components"][2]["availability"]["stock_count"] += 1
    elif mutation == "price":
        m["components"][2]["availability"]["price_USD"] = 0.01
    elif mutation == "ref":
        m["components"][2]["source_refs"].append("r1:missing")
    elif mutation == "criteria":
        m["criteria_sha256"] = "0" * 64
    elif mutation == "criteria_path":
        m["criteria_path"] = "experiments/luna47e/../../artifacts/luna47a/evidence.json"
    elif mutation == "catalog_path":
        m["source_catalogs"]["r1"] = "artifacts/luna47e/../../artifacts/luna47a/evidence.json"
    elif mutation == "context_path":
        m["retained_context"][0]["path"] = "artifacts/luna47e/../../artifacts/luna47a/evidence.json"
    elif mutation == "baseline":
        m["production_evidence_baseline"] = "0" * 40
    elif mutation == "hardware":
        m["configuration"]["hardware_execution"] = True
    elif mutation == "fpaa":
        m["primitives"][0]["fpaa"]["verdict"] = "SUPPORTED"
    elif mutation == "calculation":
        m["analytical_checks"][0]["tau_s"] = 80
    elif mutation == "context":
        m["retained_context"][0]["sha256"] = "0" * 64
    with pytest.raises(ValueError):
        validator.validate(m)


@pytest.mark.parametrize("path", [
    "tpcn/neuron.py", "workflow/ARCHITECTURE_CONTRACT.md",
    "artifacts/luna47a/evidence.json", "tests/test_other.py",
    "artifacts/luna47e/../../artifacts/luna47a/evidence.json",
    "/artifacts/luna47e/evidence.json", r"artifacts\luna47e\..\luna47a\evidence.json",
    "C:/artifacts/luna47e/evidence.json",
])
def test_rejects_unowned_paths(path):
    assert not validator.owned(path)


def test_owned_paths():
    assert validator.owned("experiments/luna47e/validate.py")
    assert validator.owned("artifacts/luna47e/primitive-matrix.json")
    assert validator.owned("tests/test_luna47e_evidence.py")
    assert validator.owned(validator.HANDOFF)


def test_hashes_criteria_using_canonical_lf_bytes(tmp_path):
    criteria = ROOT / "experiments/luna47e/criteria.md"
    canonical = criteria.read_bytes().replace(b"\r\n", b"\n")
    assert validator.sha(criteria) == hashlib.sha256(canonical).hexdigest()
    windows_copy = tmp_path / "criteria.md"
    windows_copy.write_bytes(canonical.replace(b"\n", b"\r\n"))
    assert validator.sha(windows_copy) == hashlib.sha256(canonical).hexdigest()
    assert validator.validate(matrix())["families"] == 8


def test_capture_preserves_download_record_when_pdf_processing_fails(monkeypatch):
    raw = b"%PDF-1.4\nnot a parsed PDF"
    response = SimpleNamespace(
        returncode=0,
        stdout=raw + b"\nLUNA47E_HTTP:200:https://example.com/source.pdf",
        stderr=b"",
    )
    monkeypatch.setattr(capture_sources.subprocess, "run", lambda *args, **kwargs: response)

    class BrokenPdfReader:
        def __init__(self, _data):
            raise ValueError("cannot parse PDF")

    monkeypatch.setitem(sys.modules, "pypdf", SimpleNamespace(PdfReader=BrokenPdfReader))
    record = capture_sources.capture("pdf", "manufacturer_pdf", "https://example.com/source.pdf", False)

    assert record["http_status"] == "200"
    assert record["effective_url"] == "https://example.com/source.pdf"
    assert record["raw_bytes"] == len(raw)
    assert record["raw_sha256"] == hashlib.sha256(raw).hexdigest()
    assert record["state"] == "retrieved"
    assert record["processing_error"] == "cannot parse PDF"
