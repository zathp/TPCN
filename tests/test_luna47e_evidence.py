"""Offline evidence checks and mutation controls; no production imports."""
import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "luna47e_validate", ROOT / "experiments/luna47e/validate.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def matrix():
    return copy.deepcopy(validator.load("artifacts/luna47e/primitive-matrix.json"))


def test_retained_matrix_and_source_references():
    result = validator.validate(matrix())
    assert result["families"] == 8
    assert len(result["independent_exact_part_offers"]) == 8


@pytest.mark.parametrize("mutation", [
    "owner", "family", "part", "stock", "price", "ref", "criteria",
    "baseline", "hardware", "fpaa", "calculation", "context",
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
])
def test_rejects_unowned_paths(path):
    assert not validator.owned(path)


def test_owned_paths():
    assert validator.owned("experiments/luna47e/validate.py")
    assert validator.owned("artifacts/luna47e/primitive-matrix.json")
    assert validator.owned("tests/test_luna47e_evidence.py")
    assert validator.owned(validator.HANDOFF)
