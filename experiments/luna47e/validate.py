"""Offline validation of documentary evidence; never executes TPCN or hardware."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
BASE = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
PRODUCTION = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
HANDOFF = "workflow/handoffs/luna-47e-hardware-realizability-20261006.md"
PRIMITIVES = {
    "leaky_integrator_wema", "programmable_resistance_conductance", "capacitor",
    "comparator_deadband", "rectification_absolute_value",
    "summation_subtraction_accumulation", "threshold_oscillator_bounded_output",
    "dac_digital_configuration",
}
VERDICTS = {"SUPPORTED", "PARTIALLY SUPPORTED", "NOT SUPPORTED", "BLOCKED"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def safe_relative(path: str) -> bool:
    if not isinstance(path, str) or "\\" in path:
        return False
    posix_path = PurePosixPath(path)
    windows_path = PureWindowsPath(path)
    return not (
        posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive
        or ".." in posix_path.parts or ".." in windows_path.parts
    )


def owned(path: str) -> bool:
    return safe_relative(path) and (
        path.startswith(("experiments/luna47e/", "artifacts/luna47e/"))
        or bool(re.fullmatch(r"tests/test_luna47e_[^/]+\.py", path))
        or path == HANDOFF
    )


def validate(matrix: dict) -> dict:
    require(matrix["schema"] == "LUNA47E-MATRIX-1", "Wrong matrix schema")
    require(matrix["authorization_revision"] == BASE, "Wrong authorization")
    require(matrix["production_evidence_baseline"] == PRODUCTION, "Wrong production baseline")
    require(matrix["verdict"] in VERDICTS, "Invalid verdict")
    owner = matrix["owner_access"]
    require(owner["status"] == "BLOCKED", "Owner access must remain blocked")
    require(all(owner[k] is None for k in ("region", "budget", "inventory", "supply_constraints")),
            "Owner constraints were not supplied")
    require(owned(matrix["criteria_path"]), "Criteria outside lane")
    require(sha(ROOT / matrix["criteria_path"]) == matrix["criteria_sha256"],
            "Criteria changed after declaration")
    cfg = matrix["configuration"]
    require(all(cfg[k] is False for k in ("hardware_execution", "purchase", "simulation")),
            "Unauthorized hardware/purchase/simulation claim")
    require(cfg["fixture_ids_used"] == [] and cfg["logical_time_to_seconds"] is None,
            "No physical fixture or time conversion authorized")
    sources = {}
    counts = {}
    for alias, path in matrix["source_catalogs"].items():
        require(owned(path), "Catalog outside lane")
        catalog = load(path)
        require(catalog["schema"] == "LUNA47E-SOURCES-1", "Wrong catalog schema")
        require(catalog["authorization_revision"] == BASE and
                catalog["source_baseline"] == PRODUCTION, "Catalog baseline mismatch")
        counts[alias] = len(catalog["sources"])
        for source in catalog["sources"]:
            identity = alias + ":" + source["id"]
            require(identity not in sources, "Duplicate source")
            require(urlparse(source["url"]).scheme == "https", "Non-HTTPS source")
            date = datetime.fromisoformat(source["retrieved_at_utc"])
            require(date.tzinfo is not None and date.date().isoformat() == "2026-10-07",
                    "Missing/wrong retrieval date")
            require(source["state"] in {"retrieved", "unavailable"}, "Invalid source state")
            if source["state"] == "retrieved":
                require(source["http_status"] == "200", "Retrieval without HTTP200")
                require(bool(re.fullmatch("[a-f0-9]{64}", source["raw_sha256"])),
                        "Invalid raw source hash")
                require(source["raw_bytes"] > 0, "Empty retrieved evidence")
            else:
                require(bool(source.get("error")) or source.get("http_status") != "200",
                        "Unexplained unavailable source")
            sources[identity] = source

    def check_refs(refs: list[str]) -> None:
        require(bool(refs), "Missing source references")
        require(all(ref in sources for ref in refs), "Unresolved source reference")

    components = {c["id"]: c for c in matrix["components"]}
    require(len(components) == len(matrix["components"]), "Duplicate component")
    independent = []
    for component in components.values():
        require(component["part_number"] and component["manufacturer"] and
                component["limits"] and component["configuration"] and
                component["package_accessories"] and component["spec_locators"],
                "Missing component bench detail")
        check_refs(component["source_refs"])
        require(component["availability"]["owner_access"] == "BLOCKED",
                "Component owner access cannot be asserted")
        retrieved = [sources[r] for r in component["source_refs"]
                     if sources[r]["state"] == "retrieved"]
        require(any(s["kind"].startswith("manufacturer") for s in retrieved),
                "No retrieved manufacturer capability source")
        availability = component["availability"]
        if availability["status"] == "independent_public_stock":
            stock = [s for s in retrieved if s["kind"] == "distributor"
                     and s.get("product", {}).get("mpn") == component["part_number"]]
            require(len(stock) == 1, "No unique exact-part independent offer")
            offer = stock[0]["product"]["offers"]
            require(offer["inventoryLevel"] == availability["stock_count"] > 0,
                    "Stock claim mismatch")
            require(offer["priceCurrency"] == "USD" and
                    offer["availability"].endswith("/InStock"), "Wrong offer currency/state")
            first = stock[0]["price_tiers"][0]
            require(first["ladder"] == availability["price_min_quantity"] and
                    first["usdPrice"] == availability["price_USD"], "Price/tier mismatch")
            independent.append(component["part_number"])
        else:
            require(availability["status"] == "manufacturer_orderable_only",
                    "Invalid availability evidence level")
            require(availability["stock_count"] is None and availability["lead_time"] is None,
                    "Unknown FPAA stock/lead-time must stay unknown")
    primitives = matrix["primitives"]
    require({p["id"] for p in primitives} == PRIMITIVES and len(primitives) == 8,
            "Required eight-family coverage mismatch")
    for primitive in primitives:
        require(primitive["verdict"] in VERDICTS and bool(primitive["gaps"]),
                "Invalid primitive classification/gaps")
        for realization in ("fpaa", "discrete"):
            mapping = primitive[realization]
            require(mapping["verdict"] in VERDICTS, "Invalid mapping verdict")
            require(mapping["components"] and
                    all(c in components for c in mapping["components"]),
                    "Unresolved component reference")
            if realization == "fpaa":
                require(mapping["verdict"] == "BLOCKED",
                        "FPAA independent purchase is unresolved")
                check_refs(mapping["source_refs"])
    for negative in matrix["negative_results"]:
        require(negative["verdict"] in VERDICTS, "Invalid negative classification")
        check_refs(negative["source_refs"])
    for context in matrix["retained_context"]:
        require(safe_relative(context["path"]), "Unsafe retained context path")
        require(sha(ROOT / context["path"]) == context["sha256"], "Retained evidence changed")
        baseline_bytes = subprocess.run(
            ["git", "show", PRODUCTION + ":" + context["path"]],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        require(hashlib.sha256(baseline_bytes).hexdigest() == context["git_blob_sha256"],
                "Retained context differs from production baseline")
        require((ROOT / context["path"]).read_bytes().replace(b"\r\n", b"\n") == baseline_bytes,
                "Checkout materialization differs beyond declared CRLF")
        require(context["preserved_verdict"] == "MIXED", "Retained result reinterpreted")
    calculations = {c["id"]: c for c in matrix["analytical_checks"]}
    require(math.isclose(calculations["rc_nominal"]["tau_s"], 100000 * 1e-7),
            "RC calculation mismatch")
    require(math.isclose(calculations["rc_nominal"]["tolerance_min_s"], .01*.99*.95) and
            math.isclose(calculations["rc_nominal"]["tolerance_max_s"], .01*1.01*1.05),
            "Tolerance calculation mismatch")
    require(calculations["dac_code"]["ideal_step_V"] == 2.5/4096,
            "DAC calculation mismatch")
    require(calculations["pot_step"]["nominal_step_ohm"] == 10000/256,
            "Resistance step mismatch")
    require(all(c["classification"] == "INFERRED" for c in calculations.values()),
            "Hand calculations are not measured hardware")
    return {"families": len(primitives), "components": len(components),
            "catalog_source_counts": counts, "independent_exact_part_offers": independent,
            "owner_access": "BLOCKED", "fpaa_independent_access": "BLOCKED",
            "verdict": matrix["verdict"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", help="New validation/provenance file in artifacts/luna47e")
    args = parser.parse_args()
    summary = validate(load("artifacts/luna47e/primitive-matrix.json"))
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=ROOT, check=True)
    diff = subprocess.run(["git", "diff", "--name-only", BASE], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.splitlines()
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                               cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    require(all(owned(p) for p in diff + untracked), "Diff exceeds lane ownership")
    summary.update({
        "schema": "LUNA47E-VALIDATION-1", "status": "PASS",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(),
        "head_at_validation": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                             capture_output=True, text=True, check=True).stdout.strip(),
        "authorization_revision": BASE, "production_evidence_baseline": PRODUCTION,
        "changed_paths": sorted(set(diff + untracked)),
        "validation_boundary": "Structural/source/stock/hash/hand-calculation checks only, no live or circuit equivalence checks.",
    })
    if args.record:
        path = (ROOT / args.record).resolve()
        require(path.is_relative_to((ROOT / "artifacts/luna47e").resolve()) and not path.exists(),
                "Record path must be new and lane-owned")
        inventory = list((ROOT / "artifacts/luna47e").glob("*.json"))
        inventory += list((ROOT / "experiments/luna47e").glob("*"))
        inventory += list((ROOT / "tests").glob("test_luna47e_*.py"))
        if (ROOT / HANDOFF).exists():
            inventory.append(ROOT / HANDOFF)
        summary["file_integrity"] = [
            {"path": p.relative_to(ROOT).as_posix(),
             "bytes": len(p.read_bytes().replace(b"\r\n", b"\n")), "sha256": sha(p)}
            for p in sorted(inventory) if p.is_file()
        ]
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
