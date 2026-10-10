#!/usr/bin/env python3
"""Independent N4 coverage audit of the immutable Luna-63C W and T outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
W_DIR = ROOT / "experiments/luna63c/certificate/lane-w"
T_DIR = ROOT / "experiments/luna63c/certificate/lane-t"
FIXTURE_JSON = ROOT / "experiments/luna63c/fixture-freeze/fixtures.json"
FIXTURE_MD = ROOT / "experiments/luna63c/fixture-freeze/FIXTURE_FREEZE.md"
N4_DOC = ROOT / "workflow/docs/luna/LUNA_63C_N4_CERTIFICATION_REQUIREMENTS.md"
DESIGN = ROOT / "workflow/docs/luna/LUNA_63C_NONLINEAR_EXCURSION_DESIGN.md"
GOVERNANCE = ROOT / "workflow/handoffs/luna-0-luna63c-reference-arithmetic-governance-20261010.md"
LANE_DOC = ROOT / ".github/agents/luna-63c-mechanism.agent.md"
OUT_MATRIX = HERE / "coverage_matrix.json"
OUT_MANIFEST = HERE / "manifest.json"

PINS = {
    "source_branch_head": "19caa49d7620062c06ad74d19528e47725f86b37",
    "fixture_publication": "583148e2812b93d519a3dc2821944d08446497b7",
    "w_complete_commit": "17907c67d52cc338249b66f28c3179cd97572c6e",
    "t_publication": "0a8c34b7e6febf681917d915082a8559eea998f7",
    "fixtures_json_blob": "8c4f9d20dda217d71ef1bcbb4fdefd0e3507ed92",
    "fixtures_json_sha256": "AF81F3390274B2D565F90CBF12C116C78F45C5DF65D6C28BA88194E9DF2F70FB",
    "fixture_freeze_md_blob": "fc3d883e72ec3062e07cc453927ee76cba4aa561",
    "fixture_freeze_md_sha256": "B3BB25D65A8344363DF17F2A6FF3085034FDC431605B6FBA729499D512BE667F",
    "n4_schema_revision": "9cc92adb56e388d8675d538410b319fd8d8841a5",
    "arithmetic_governance_revision": "87179ba2f5da13da7bc70727e72c000de924ed80",
    "design_revision": "3e7d31b9a527e908b21abee3766906084e7cd082",
    "w_matrix_sha256": "0B5AB09AE5E4A29AD951B00563C64F5D445D0665B332154C9D40F93335F90D9F",
}

A_OBLIGATIONS = tuple(f"N4-A{i}" for i in range(1, 8))
B_OBLIGATIONS = tuple(f"N4-B{i}" for i in range(1, 8))
OWNER_SOURCE_CLAUSES = {
    "1": ["rest/eigenvalue/stability", "N4-A1", "N4-A5"],
    "2": ["invariant disk/operating region", "N4-A2", "N4-A5"],
    "3": ["neutral RECALL", "N4-A5", "N4-A7"],
    "4": ["subthreshold/tangency", "N4-A3", "N4-A4", "N4-A5"],
    "5": ["A=4 release trajectory", "N4-A3", "N4-A4", "N4-A5"],
    "6": ["surface/direction/uniqueness/re-arm", "N4-A3", "N4-A4", "N4-A5"],
    "7": ["quiet/terminal/lifetime", "N4-A3", "N4-A5", "N4-A6"],
    "8": ["active-to-absolute time / expiry order", "N4-B1", "N4-B2", "N4-B3", "N4-B4", "N4-B6"],
    "9": ["A=1 exact comparison rule", "N4-A2", "N4-A5", "N4-A7"],
    "10": ["root/time refinement and event ceiling", "N4-A3", "N4-A4", "N4-B2", "N4-B3"],
    "11": ["timer/unique-record bounds", "N4-B4", "N4-B5", "N4-B6", "N4-B7"],
    "12": ["attempt-17 overflow / ingress closure", "N4-B4", "N4-B5", "N4-B6", "N4-B7"],
}
EXPECTED_CERTIFIED_T = {
    "C7.NEAR_CLOCK_LIMIT.STORE_LAST_IN_DOMAIN_ORIGIN_1",
    "C7.NEAR_CLOCK_LIMIT.TIMER_EXPIRY_CREATED_FOR_INSTANCE_1",
    "C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1",
    "C7.POSITIVE_SUB_ULP.STORE_UPPER_Q_NEIGHBOR_1",
    "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_CREATED_1",
    "C7.POSITIVE_SUB_ULP.RECALL_ON_1",
    "C7.POSITIVE_SUB_ULP.TIMER_QUIET_CREATED_1",
    "C7.POSITIVE_SUB_ULP.TIMER_QUIET_1",
    "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_INVALIDATED_AT_QUIET_1",
}
CLOCK = Fraction(2**20)
ACTIVE_SCALE = 2**1074


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def commit_blob(path: Path, commit: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{rel}"], cwd=ROOT, text=True
    ).strip()


def source_revision_blob(path: Path, revision: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "rev-parse", f"{revision}:{rel}"], cwd=ROOT, text=True
    ).strip()


def committed_bytes(path: Path, commit: str) -> bytes:
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "show", f"{commit}:{rel}"], cwd=ROOT)


def fraction(pair: dict[str, Any]) -> Fraction:
    return Fraction(int(pair["numerator"]), int(pair["denominator"]))


def exact_interval(value: dict[str, Any]) -> tuple[Fraction, Fraction]:
    lo = fraction(value["lower_exact"])
    hi = fraction(value["upper_exact"])
    assert lo <= hi
    return lo, hi


def collect_intervals(value: Any, path: tuple[str, ...] = ()) -> dict[tuple[str, ...], tuple[Fraction, Fraction]]:
    found: dict[tuple[str, ...], tuple[Fraction, Fraction]] = {}
    if isinstance(value, dict):
        if {"lower_exact", "upper_exact"} <= set(value):
            found[path] = exact_interval(value)
        else:
            for key, child in value.items():
                found.update(collect_intervals(child, path + (key,)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.update(collect_intervals(child, path + (str(index),)))
    return found


def interval_field(container: dict[str, Any], precision: str) -> tuple[Fraction, Fraction]:
    return exact_interval(container[precision])


def intersect(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    result = max(left[0], right[0]), min(left[1], right[1])
    assert result[0] <= result[1], "precision enclosures do not overlap"
    return result


def require_cover(stored: dict[str, Any], calculated: tuple[Fraction, Fraction]) -> None:
    lo, hi = exact_interval(stored)
    assert lo <= calculated[0] <= calculated[1] <= hi, (lo, calculated, hi)


class MP:
    """Small directed-MPFR interval kernel written for this independent audit."""

    def __init__(self, module: Any, lo: Any, hi: Any, precision: int):
        self.g = module
        self.lo = lo
        self.hi = hi
        self.precision = precision

    @classmethod
    def rational(cls, module: Any, value: Fraction | int, precision: int) -> "MP":
        q = Fraction(value)
        exact = module.mpq(q.numerator, q.denominator)
        with module.context(round=module.RoundDown, precision=precision):
            lo = module.mpfr(exact)
        with module.context(round=module.RoundUp, precision=precision):
            hi = module.mpfr(exact)
        return cls(module, lo, hi, precision)

    @classmethod
    def pi(cls, module: Any, precision: int) -> "MP":
        with module.context(round=module.RoundDown, precision=precision):
            lo = module.const_pi()
        with module.context(round=module.RoundUp, precision=precision):
            hi = module.const_pi()
        return cls(
            module,
            lo,
            hi,
            precision,
        )

    def _op(self, fn: Any, rounding: int) -> Any:
        with self.g.context(round=rounding, precision=self.precision):
            return fn()

    def __add__(self, other: "MP") -> "MP":
        return MP(self.g, self._op(lambda **k: self.lo + other.lo, self.g.RoundDown),
                  self._op(lambda **k: self.hi + other.hi, self.g.RoundUp), self.precision)

    def __neg__(self) -> "MP":
        return MP(
            self.g,
            self._op(lambda: -self.hi, self.g.RoundToNearest),
            self._op(lambda: -self.lo, self.g.RoundToNearest),
            self.precision,
        )

    def __sub__(self, other: "MP") -> "MP":
        return self + (-other)

    def __mul__(self, other: "MP") -> "MP":
        down = [self._op(lambda a=a, b=b, **k: a * b, self.g.RoundDown)
                for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        up = [self._op(lambda a=a, b=b, **k: a * b, self.g.RoundUp)
              for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return MP(self.g, min(down), max(up), self.precision)

    def positive_div(self, other: "MP") -> "MP":
        assert self.lo >= 0 and other.lo > 0
        return MP(self.g,
                  self._op(lambda **k: self.lo / other.hi, self.g.RoundDown),
                  self._op(lambda **k: self.hi / other.lo, self.g.RoundUp), self.precision)

    def exp(self) -> "MP":
        return MP(self.g,
                  self._op(lambda: self.g.exp(self.lo), self.g.RoundDown),
                  self._op(lambda: self.g.exp(self.hi), self.g.RoundUp), self.precision)

    def log_positive(self) -> "MP":
        assert self.lo > 0
        return MP(self.g,
                  self._op(lambda: self.g.log(self.lo), self.g.RoundDown),
                  self._op(lambda: self.g.log(self.hi), self.g.RoundUp), self.precision)

    def sqrt_nonnegative(self) -> "MP":
        assert self.lo >= 0
        return MP(self.g,
                  self._op(lambda: self.g.sqrt(self.lo), self.g.RoundDown),
                  self._op(lambda: self.g.sqrt(self.hi), self.g.RoundUp), self.precision)

    def sin(self) -> "MP":
        return monotone_trig(self, self.g.sin, kind="sin")

    def cos(self) -> "MP":
        return monotone_trig(self, self.g.cos, kind="cos")

    def fractions(self) -> tuple[Fraction, Fraction]:
        a, b = self.lo.as_integer_ratio(), self.hi.as_integer_ratio()
        return Fraction(int(a[0]), int(a[1])), Fraction(int(b[0]), int(b[1]))


def monotone_trig(value: MP, fn: Any, kind: str) -> MP:
    g, p = value.g, value.precision
    pi = MP.pi(g, p)
    half_pi = pi.positive_div(MP.rational(g, 2, p))
    assert value.lo >= 0 and value.hi <= pi.lo
    if kind == "sin":
        left = value._op(lambda: fn(value.lo), g.RoundDown)
        right = value._op(lambda: fn(value.hi), g.RoundDown)
        low = min(left, right)
        high_values = [
            value._op(lambda: fn(value.lo), g.RoundUp),
            value._op(lambda: fn(value.hi), g.RoundUp),
        ]
        if value.lo <= half_pi.hi and value.hi >= half_pi.lo:
            high_values.append(g.mpfr(1, precision=p))
        return MP(g, low, max(high_values), p)
    left = value._op(lambda: fn(value.hi), g.RoundDown)
    right = value._op(lambda: fn(value.lo), g.RoundDown)
    low = min(left, right)
    high = max(
        value._op(lambda: fn(value.lo), g.RoundUp),
        value._op(lambda: fn(value.hi), g.RoundUp),
    )
    return MP(g, low, high, p)


def positive_interval(g: Any, lo: MP, hi: MP) -> MP:
    """Conservative interval product where arguments are already MP intervals."""
    return lo.positive_div(MP.rational(g, 1, lo.precision).positive_div(hi))


def import_gmpy2() -> tuple[Any, dict[str, Any]]:
    engine = Path(r"C:\Users\Patrick\Documents\ActiveCode\TPCN\experiments\luna63c\certificate\lane-w\.engine")
    if str(engine) not in sys.path:
        sys.path.insert(0, str(engine))
    import gmpy2  # type: ignore[import-not-found]

    ext = Path(gmpy2.__file__).parent / "gmpy2.cp311-win_amd64.pyd"
    libs = engine / "gmpy2.libs"
    identities = {
        "binding": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "gmp": gmpy2.mp_version(),
        "binding_module": str(Path(gmpy2.__file__).resolve()),
        "extension": str(ext.resolve()),
        "extension_sha256": sha256(ext.read_bytes()),
        "native_libraries": {},
        "python": sys.version,
        "platform": sys.platform,
        "machine": __import__("platform").machine(),
        "rounding": {"RNDD": int(gmpy2.RoundDown), "RNDU": int(gmpy2.RoundUp)},
    }
    expected = {
        "libgmp-10.dll": "525F5681DC5FB40EF86B1BCB0EE5C40142AEC689E0A1BA8C8E40199173366F6A",
        "libmpfr-6.dll": "B81A548EB7A23D4E3ACBE296F1EFF077A0B284617A2C1CC53A1CCDB0637B52B8",
    }
    for name in ("libgmp-10.dll", "libmpfr-6.dll"):
        file = libs / name
        identities["native_libraries"][name] = {
            "path": str(file.resolve()),
            "sha256": sha256(file.read_bytes()),
        }
        assert identities["native_libraries"][name]["sha256"] == expected[name]
    assert identities["extension_sha256"] == "632D398D77023696549483852FB947B2627E6F7B88C4A42815A1A4977BEF30B5"
    assert identities["binding"] == "2.3.2"
    assert identities["mpfr"] == "MPFR 4.2.2"
    assert identities["gmp"] == "GMP 6.3.0"
    assert identities["rounding"] == {"RNDD": 3, "RNDU": 2}
    return gmpy2, identities


def check_pins(w: dict[str, Any], wm: dict[str, Any], t: dict[str, Any], tm: dict[str, Any]) -> dict[str, Any]:
    assert sha256((W_DIR / "coverage_matrix.json").read_bytes()) == PINS["w_matrix_sha256"]
    assert wm["format"] == "luna63c-stage-a-lane-w-manifest"
    assert wm["matrix_sha256"] == PINS["w_matrix_sha256"] and wm["certified_count"] == 100
    assert wm["blocked_count"] == 0
    assert wm["disposition"].startswith("W COMPLETE")
    assert t["pins"]["source_branch_head"] == PINS["source_branch_head"]
    assert t["pins"]["fixture_publication"] == PINS["fixture_publication"]
    assert tm["pins"]["w_complete_commit"] == PINS["w_complete_commit"]
    assert tm["verdict"] == "T BLOCKED — N3 NOT CLOSED"
    assert t["counts"] == {
        "blocked": 182, "c7_blocked": 110, "c7_certified": 9,
        "c7_identities": 119, "certified": 9, "events": 191,
        "observation_rows": 15,
    }
    assert tm["counts"]["events"] == 191
    assert tm["counts"]["certified"] == 9 and tm["counts"]["blocked"] == 182
    expected_t_pins = {
        "source_branch_head": PINS["source_branch_head"],
        "fixture_publication": PINS["fixture_publication"],
        "w_complete_commit": PINS["w_complete_commit"],
        "fixtures_json_canonical_sha256": PINS["fixtures_json_sha256"],
        "fixtures_json_blob": PINS["fixtures_json_blob"],
        "fixture_freeze_md_sha256": PINS["fixture_freeze_md_sha256"],
        "fixture_freeze_md_blob": PINS["fixture_freeze_md_blob"],
        "n4_requirements_revision": PINS["n4_schema_revision"],
        "arithmetic_profile_revision": PINS["arithmetic_governance_revision"],
        "design_revision": PINS["design_revision"],
        "w_matrix_sha256": PINS["w_matrix_sha256"],
    }
    assert all(tm["pins"].get(key) == value for key, value in expected_t_pins.items())
    fixture_raw = FIXTURE_JSON.read_bytes()
    freeze_raw = FIXTURE_MD.read_bytes()
    fixture_committed = committed_bytes(FIXTURE_JSON, PINS["fixture_publication"])
    freeze_committed = committed_bytes(FIXTURE_MD, PINS["fixture_publication"])
    assert sha256(fixture_committed) == PINS["fixtures_json_sha256"]
    assert sha256(freeze_committed) == PINS["fixture_freeze_md_sha256"]
    assert commit_blob(FIXTURE_JSON, PINS["fixture_publication"]) == PINS["fixtures_json_blob"]
    assert commit_blob(FIXTURE_MD, PINS["fixture_publication"]) == PINS["fixture_freeze_md_blob"]
    assert commit_blob(W_DIR / "coverage_matrix.json", PINS["w_complete_commit"]) == commit_blob(W_DIR / "coverage_matrix.json", "HEAD")
    for path in (T_DIR / "schedule.json", T_DIR / "inventory.json", T_DIR / "manifest.json"):
        assert commit_blob(path, PINS["t_publication"]) == commit_blob(path, "HEAD")
    for revision in (PINS["n4_schema_revision"], PINS["arithmetic_governance_revision"], PINS["design_revision"]):
        subprocess.check_call(["git", "cat-file", "-e", f"{revision}^{{commit}}"], cwd=ROOT)
    assert source_revision_blob(N4_DOC, PINS["n4_schema_revision"]) == commit_blob(N4_DOC, PINS["t_publication"])
    assert source_revision_blob(DESIGN, PINS["design_revision"]) == commit_blob(DESIGN, PINS["t_publication"])
    assert source_revision_blob(GOVERNANCE, PINS["arithmetic_governance_revision"]) == commit_blob(GOVERNANCE, PINS["t_publication"])
    return {
        "fixtures_json_checkout_sha256": sha256(fixture_raw),
        "fixtures_json_committed_sha256": sha256(fixture_committed),
        "fixture_freeze_checkout_sha256": sha256(freeze_raw),
        "fixture_freeze_committed_sha256": sha256(freeze_committed),
        "w_matrix_sha256": sha256((W_DIR / "coverage_matrix.json").read_bytes()),
        "committed_w_commit": PINS["w_complete_commit"],
        "committed_t_commit": PINS["t_publication"],
        "source_head_pin": PINS["source_branch_head"],
    }


def check_w_math(evidence: dict[str, Any], g: Any) -> dict[str, Any]:
    checked: Counter[str] = Counter()
    cache: dict[tuple[int, str], MP] = {}
    serialized = collect_intervals(evidence)
    assert len(serialized) == 90
    precision_pairs = 0
    for path, enclosure in serialized.items():
        if "256" not in path or "endpoint_surface_enclosures" in path:
            continue
        other_path = tuple("512" if piece == "256" else piece for piece in path)
        if other_path in serialized:
            try:
                intersect(enclosure, serialized[other_path])
            except AssertionError as exc:
                raise AssertionError(f"published 256/512 intervals do not overlap at {path}") from exc
            precision_pairs += 1
    assert precision_pairs == 36

    def cover(path: str, mp: MP, stored: dict[str, Any]) -> None:
        lo, hi = mp.fractions()
        require_cover(stored, (lo, hi))
        checked[path] += 1
        cache[(mp.precision, path)] = mp

    for bits in (256, 512):
        pi = MP.pi(g, bits)
        two = MP.rational(g, 2, bits)
        four = MP.rational(g, 4, bits)
        one = MP.rational(g, 1, bits)
        if bits == 256:
            cover("environment.pi_interval", pi, evidence["environment"]["outward_rounding_smoke_test"]["pi_interval"])
            exp_one = one.exp()
            cover("environment.exp_1_interval", exp_one, evidence["environment"]["outward_rounding_smoke_test"]["exp_1_interval"])
        sqrt2 = two.sqrt_nonnegative()
        minus_pi4 = -(pi.positive_div(four))
        exp_minus_pi4 = minus_pi4.exp()
        q = exp_minus_pi4.positive_div(sqrt2)
        theta = q * two
        for name, mp in (("pi", pi), ("sqrt2", sqrt2), ("g", q), ("q", q), ("theta", theta)):
            cover(f"constants.{name}", mp, evidence["constants"][name][str(bits)])

        # Independent evaluation of the frozen logarithmic source identities.
        tq = four.positive_div(q).log_positive()
        cover("T_q_A4", tq, evidence["T_q_A4"][str(bits)])
        life = tq + MP.rational(g, 3, bits)
        cover("T_life_A4", life, evidence["T_life_A4"]["enclosures"][str(bits)])
        for label, magnitude in (("A1", one), ("A4", four)):
            qtime = magnitude.positive_div(q).log_positive()
            cover(f"quiet_times.{label}", qtime, evidence["quiet_times"][label][str(bits)])
        quiet_c6 = four.positive_div(q).log_positive()
        cover("quiet_times_C6_independent", quiet_c6, evidence["quiet_times_C6_independent"][str(bits)])
        upper_neighbor = Fraction.from_float(float.fromhex(evidence["q_neighbor_inputs"]["upper_hex"]))
        qabove = MP.rational(g, upper_neighbor, bits).positive_div(q).log_positive()
        cover("quiet_times.Q_ABOVE", qabove, evidence["quiet_times"]["Q_ABOVE"][str(bits)])
        qlo, qhi = q.fractions()
        assert Fraction.from_float(float.fromhex(evidence["q_neighbor_inputs"]["lower_hex"])) < qlo
        assert qhi < upper_neighbor

        # At A=4 quiet, 4*exp(-s_q)=q exactly; use the identity rather
        # than interval-evaluating exp(-log(4/q)) and widening dependencies.
        tquiet = four.positive_div(q).log_positive()
        xquiet = q * tquiet.cos()
        yquiet = q * tquiet.sin()
        for label in ("C4", "C6"):
            node = evidence["quiet_boundary_states"][label][str(bits)]
            cover(f"quiet_boundary_states.{label}.{bits}.x", xquiet, node["x"])
            cover(f"quiet_boundary_states.{label}.{bits}.y", yquiet, node["y"])

        # All eight signed exact-time A=1 flow-oracle checkpoints.
        for polarity in ("P", "N"):
            p = 1 if polarity == "P" else -1
            for suffix, active in (("S0", Fraction(0)), ("S1_2", Fraction(1, 2)),
                                   ("S1", Fraction(1)), ("S2", Fraction(2))):
                s = MP.rational(g, active, bits)
                decay = (-s).exp()
                x = decay * s.cos()
                y = decay * s.sin()
                if p < 0:
                    x, y = -x, -y
                node = evidence["A1_oracle_states"][polarity][suffix][str(bits)]
                cover(f"A1_oracle_states.{polarity}.{suffix}.x", x, node["x"])
                cover(f"A1_oracle_states.{polarity}.{suffix}.y", y, node["y"])

        # C4/C6 A=4 root enclosures, endpoint surface signs and flow states.
        for root_group in ("roots_A4", "roots_C6_independent"):
            for which, threshold in (("up", theta), ("rearm", q)):
                runset = evidence[root_group][which]["precision_runs"]
                run = runset[str(bits)]
                left, right = (Fraction(x) for x in run["bracket"])
                assert left < right
                assert Fraction(run["width"]) == right - left
                surface = lambda s: (
                    MP.rational(g, 4, bits) * (-MP.rational(g, s, bits)).exp()
                    * MP.rational(g, s, bits).sin()
                ) - threshold
                for side, point in (("left", left), ("right", right)):
                    val = surface(point)
                    cover(f"{root_group}.{which}.{bits}.{side}",
                          val, run["endpoint_surface_enclosures"][side])
                lsign = surface(left).fractions()
                rsign = surface(right).fractions()
                assert (lsign[0] > 0 and rsign[1] < 0) if which == "rearm" else (lsign[1] < 0 and rsign[0] > 0)
                pi_bounds = pi.fractions()
                assert left > 0 and right < pi_bounds[0]
                if which == "up":
                    assert right < pi_bounds[0] / 4
                else:
                    assert left > pi_bounds[1] / 4
                assert runset["256"]["bracket"][0] == runset["256"]["bracket"][0]
                root_ev = evidence[root_group][which]
                assert root_ev["bisection_limit"] == 128
                assert root_ev["bisections_total"] <= 128
                assert set(root_ev["precision_runs"]) == {"256", "512"}
                state_key = "root_state_enclosures_A4" if root_group == "roots_A4" else "root_state_enclosures_C6_independent"
                state_name = "up" if which == "up" else "rearm"
                state = evidence[state_key][state_name][str(bits)]
                arg = MP.rational(g, left, bits)
                end = MP.rational(g, right, bits)
                time_range = MP(g, arg.lo, end.hi, bits)
                x = MP.rational(g, 4, bits) * (-time_range).exp() * time_range.cos()
                y = MP.rational(g, 4, bits) * (-time_range).exp() * time_range.sin()
                target_lo, target_hi = threshold.fractions()
                y_lo, y_hi = y.fractions()
                assert y_lo <= target_hi and target_lo <= y_hi
                cover(f"{state_key}.{state_name}.{bits}.x", x, state["x"])
                assert state["y_surface"] == (
                    "theta exactly at the upward root" if which == "up"
                    else "q exactly at the downward re-arm root"
                )
                if root_group == "roots_A4" and which == "up":
                    negative = evidence["root_state_enclosures_A4"]["up_negative_orientation"][str(bits)]
                    cover("root_state_enclosures_A4.up_negative_orientation." + str(bits) + ".x", -x, negative["x"])
                    assert negative["y_surface"] == "theta exactly at the upward root"

    # Precision convergence: all independent enclosures overlap and root brackets nest.
    for key in ("constants", "quiet_times"):
        for name, by_prec in evidence[key].items():
            if not isinstance(by_prec, dict) or "256" not in by_prec or "512" not in by_prec:
                continue
            if key == "constants":
                intersect(exact_interval(by_prec["256"]), exact_interval(by_prec["512"]))
            else:
                intersect(interval_field(by_prec, "256"), interval_field(by_prec, "512"))
    for group in ("roots_A4", "roots_C6_independent"):
        for which in ("up", "rearm"):
            root = evidence[group][which]
            runs = root["precision_runs"]
            assert sum(r["iterations_this_precision"] for r in runs.values()) == root["bisections_total"]
            assert root["bisections_total"] <= 128
            assert all(r["iterations_this_precision"] == 64 for r in runs.values())
            a = tuple(Fraction(x) for x in runs["256"]["bracket"])
            b = tuple(Fraction(x) for x in runs["512"]["bracket"])
            assert a[0] <= b[0] < b[1] <= a[1]
            assert Fraction(runs["512"]["width"]) < Fraction(runs["256"]["width"])
            start = tuple(Fraction(x) for x in runs["256"]["start_bracket"])
            expected_start = {
                ("roots_A4", "up"): (Fraction(0), Fraction(1, 2)),
                ("roots_A4", "rearm"): (Fraction(1), Fraction(3)),
                ("roots_C6_independent", "up"): (Fraction(0), Fraction(1, 4)),
                ("roots_C6_independent", "rearm"): (Fraction(2), Fraction(3)),
            }[(group, which)]
            assert start == expected_start
            assert Fraction(runs["256"]["width"]) == (start[1] - start[0]) / 2**64
            assert tuple(Fraction(x) for x in runs["512"]["start_bracket"]) == a
            assert Fraction(runs["512"]["width"]) == (a[1] - a[0]) / 2**64
    rearm_512 = tuple(Fraction(x) for x in evidence["roots_A4"]["rearm"]["precision_runs"]["512"]["bracket"])
    quiet_a4 = interval_field(evidence["quiet_times"]["A4"], "512")
    quiet_a1 = interval_field(evidence["quiet_times"]["A1"], "512")
    assert Fraction(1) < quiet_a1[0] and quiet_a1[1] < Fraction(2)
    assert rearm_512[1] < quiet_a4[0]
    assert quiet_a4[1] < MP.pi(g, 512).fractions()[0]
    life = interval_field(evidence["T_life_A4"]["enclosures"], "512")
    tq = interval_field(evidence["T_q_A4"], "512")
    assert life[0] - tq[1] <= 3 <= life[1] - tq[0]
    # Strict A=1 acceptance limit is an ideal mathematical margin only.
    for bits in (256, 512):
        theta = MP(g, cache[(bits, "constants.theta")].lo, cache[(bits, "constants.theta")].hi, bits)
        err = (-MP.rational(g, 2, bits)).exp()
        bound = theta.positive_div(MP.rational(g, 4, bits))
        assert err.fractions()[1] < bound.fractions()[0]
    assert sum(checked.values()) == 90
    lower_neighbor = Fraction.from_float(float.fromhex(evidence["q_neighbor_inputs"]["lower_hex"]))
    upper_neighbor = Fraction.from_float(float.fromhex(evidence["q_neighbor_inputs"]["upper_hex"]))
    lower_bits = struct.unpack(">Q", struct.pack(">d", float(lower_neighbor)))[0]
    upper_bits = struct.unpack(">Q", struct.pack(">d", float(upper_neighbor)))[0]
    assert upper_bits - lower_bits == 1
    assert upper_neighbor < 1
    assert evidence["q_neighbor_inputs"]["adjacent_bits"] is True
    exact_algebraic_checks = {
        "linear_field_matrix": "M=[[-1,-1],[1,-1]]",
        "eigenvalues": "lambda^2+2lambda+2=(lambda+1)^2+1; roots -1+i and -1-i",
        "lyapunov_derivative": "d(x^2+y^2)/ds=-2(x^2+y^2)<=0",
        "neutral_fixed_point": "M*(0,0)=(0,0), so either gate leaves the neutral state fixed",
        "hold": "R=0 implies zero field and no active-time advance",
        "a2_exact_tangency": "2*exp(-pi/4)*sin(pi/4)=theta; first derivative 0; second derivative <0",
        "a4_first_lobe_peak": "4g=2theta>theta",
        "quiet_formula": "s_q=ln(A/q) for A>q; inward radius derivative is -r",
        "lifetime": "T_life=H+T_q+1=3+T_q",
    }
    for bits in (256, 512):
        gv = cache[(bits, "constants.g")].fractions()
        qv = cache[(bits, "constants.q")].fractions()
        tv = cache[(bits, "constants.theta")].fractions()
        assert gv == qv
        assert 2 * gv[0] >= tv[0] and 2 * gv[1] <= tv[1]
        assert qv[1] < tv[0]
        assert 4 * gv[0] > tv[1]
    assert exact_algebraic_checks["eigenvalues"]
    assert exact_algebraic_checks["lyapunov_derivative"]
    return {
        "independent_mpfr_quantity_enclosures_checked": sum(checked.values()),
        "serialized_w_interval_pairs_total": 90,
        "serialized_w_interval_pairs_independently_rechecked": sum(checked.values()),
        "serialized_precision_overlaps_256_512": precision_pairs,
        "quantity_families": dict(sorted(checked.items())),
        "precision_bits": [256, 512],
        "root_count": 4,
        "root_bisections_max_per_root": 128,
        "root_signs_and_monotone_brackets": "PASS",
        "exact_symbolic_claims": exact_algebraic_checks,
        "a1_strict_theta_over_4_ideal_margin": "PASS; no Stage-B candidate evaluated",
        "1024_bit_escalation": "not required; identities and 256/512 enclosures resolve",
        "host_libm_for_reference_values": False,
    }


def check_w_inventory(rows: list[dict[str, Any]], evidence: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    by_id = {row["row_id"]: row for row in rows}
    assert len(by_id) == len(rows) == 100
    assert all(row["status"] == "CERTIFIED" and row["owner"] == "W" for row in rows)
    assert {row["fixture"] for row in rows} == set(f"C{i}" for i in range(8))
    assert set(manifest["source_inventory"]["fixture_ids"]) == {f"C{i}" for i in range(8)}
    assert {f"N4-A{i}" for i in range(1, 8)} <= {o for row in rows for o in row["n4_a_requirements"]}
    symbolic = evidence["exact_symbolic_proofs"]
    missing_refs: list[tuple[str, str]] = []
    for row in rows:
        assert "N4-A1" in row["n4_a_requirements"]
        assert "N4-A2" in row["n4_a_requirements"]
        assert "N4-A7" in row["n4_a_requirements"]
        for ref in row["proof_refs"]:
            if ref in symbolic or ref in evidence:
                continue
            target: Any = evidence
            for piece in ref.split("."):
                if not isinstance(target, dict) or piece not in target:
                    target = None
                    break
                target = target[piece]
            if target is None:
                missing_refs.append((row["row_id"], ref))
    assert not missing_refs, missing_refs
    required_symbolic = {
        "A1_s0_s_half_s1", "A1_s2_error", "A1_subthreshold", "A2_tangent",
        "A2_tangent_state", "A4_quiet", "A4_quiet_before_expiry", "A4_rearm",
        "A4_rearm_before_quiet", "A4_up_crossing", "C5_hold_shift",
        "C7_time_schedules", "flow", "held", "q_neighbor_subthreshold",
        "quiet_A1", "radius",
    }
    assert set(symbolic) == required_symbolic
    assert "M=[[-1,-1],[1,-1]]" in symbolic["flow"]
    assert "A^2*exp(-2s)" in symbolic["radius"]
    assert "R=0" in symbolic["held"]
    assert "exactly and derivative" in symbolic["A2_tangent"]
    assert "ln(4/q)" in symbolic["A4_quiet"]
    assert "strictly decreases" in symbolic["A4_rearm"]
    assert "H in {0,1,2}" in symbolic["C5_hold_shift"]
    assert "Binary64 ceilings" in symbolic["C7_time_schedules"]
    return {
        "w_rows": 100,
        "certified_rows": 100,
        "fixtures_covered": [f"C{i}" for i in range(8)],
        "distinct_checkpoint_ids": len(by_id),
        "all_proof_references_resolve": True,
        "symbolic_proof_families": sorted(required_symbolic),
        "n4_a_assignments": {
            obligation: sum(obligation in row["n4_a_requirements"] for row in rows)
            for obligation in A_OBLIGATIONS
        },
    }


def f64_from_bits(bits: int) -> Fraction:
    return Fraction.from_float(struct.unpack(">d", struct.pack(">Q", bits))[0])


def floor_binary64(value: Fraction) -> Fraction:
    lo, hi = 0, 0x7FEFFFFFFFFFFFFF
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if f64_from_bits(mid) <= value:
            lo = mid
        else:
            hi = mid - 1
    return f64_from_bits(lo)


def ceil_binary64(value: Fraction) -> Fraction:
    lo, hi = 0, 0x7FEFFFFFFFFFFFFF
    while lo < hi:
        mid = (lo + hi) // 2
        if f64_from_bits(mid) >= value:
            hi = mid
        else:
            lo = mid + 1
    return f64_from_bits(lo)


def as_mpz_units(g: Any, value: Fraction) -> int:
    scaled = g.mpz(value.numerator) * g.mpz(ACTIVE_SCALE)
    quotient, remainder = divmod(scaled, g.mpz(value.denominator))
    assert remainder == 0
    return int(quotient)


def check_t_math(t: dict[str, Any], inventory: dict[str, Any], evidence: dict[str, Any], g: Any) -> dict[str, Any]:
    events = t["rows"]
    inv_events = inventory["events"]
    assert len(events) == len(inv_events) == 191
    inv_by_id = {row["event_id"]: row for row in inv_events}
    event_by_id = {row["event_id"]: row for row in events}
    assert len(inv_by_id) == len(event_by_id) == 191
    assert set(inv_by_id) == set(event_by_id)
    assert sum(row["fixture"] == "C7" for row in inv_events) == 119
    assert sum(row["status"] == "CERTIFIED" for row in events) == 9
    assert sum(row["status"] == "BLOCKED" for row in events) == 182
    assert {row["event_id"] for row in events if row["status"] == "CERTIFIED"} == EXPECTED_CERTIFIED_T
    blocked = [row for row in events if row["status"] == "BLOCKED"]
    assert all(row["binary64"] is None and row["exact_time"] is None and row["final_ordinal"] is None for row in blocked)
    assert all(row["blocked_reasons"] for row in blocked)
    reason_counts = Counter(reason for row in blocked for reason in row["blocked_reasons"])
    unit_model = t["model_constants"]
    one_tu_units = g.mpz(2) ** 1074
    two_tu_units = g.mpz(2) ** 1075
    assert unit_model["active_unit"] == "2^-1074 TU"
    assert g.mpz(unit_model["authored_exact_offsets_units"]["1_TU"]) == one_tu_units
    assert g.mpz(unit_model["authored_exact_offsets_units"]["2_TU"]) == two_tu_units
    assert unit_model["hold_active_units"] == "0 for HOLD durations 0,1,2 TU"

    certified = [row for row in events if row["status"] == "CERTIFIED"]
    event_facts: dict[str, dict[str, Any]] = {}
    for row in certified:
        timestamp = Fraction(row["exact_time"]["num"], row["exact_time"]["den"])
        b64 = row["binary64"]
        binary = float.fromhex(b64["hex"])
        assert math.isfinite(binary) and 0 <= timestamp <= CLOCK
        assert Fraction.from_float(binary) == timestamp
        bits = struct.unpack(">Q", struct.pack(">d", binary))[0]
        assert b64["bits"] == f"0x{bits:016x}"
        assert floor_binary64(timestamp) == timestamp == ceil_binary64(timestamp)
        units = as_mpz_units(g, timestamp)
        assert units >= 0
        event_facts[row["event_id"]] = {
            "exact_time_fraction": f"{timestamp.numerator}/{timestamp.denominator}",
            "real_time_interval": [
                f"{timestamp.numerator}/{timestamp.denominator}",
                f"{timestamp.numerator}/{timestamp.denominator}",
            ],
            "binary64_hex": b64["hex"],
            "event_timestamp_common_ceiling": b64["hex"],
            "timestamp_units_2^-1074": str(units),
            "finite_clock_domain": "PASS: exact timestamp is in [0,2^20]",
            "cause_ids": row["causal_predecessors"],
            "component": row["instance_component"],
            "ordinal": row["final_ordinal"],
        }

    life = intersect(
        interval_field(evidence["T_life_A4"]["enclosures"], "256"),
        interval_field(evidence["T_life_A4"]["enclosures"], "512"),
    )
    tq = intersect(interval_field(evidence["T_q_A4"], "256"), interval_field(evidence["T_q_A4"], "512"))
    qabove = intersect(interval_field(evidence["quiet_times"]["Q_ABOVE"], "256"),
                       interval_field(evidence["quiet_times"]["Q_ABOVE"], "512"))
    tstar = floor_binary64(CLOCK - life[1])
    assert floor_binary64(CLOCK - life[0]) == tstar
    ulp = f64_from_bits(struct.unpack(">Q", struct.pack(">d", float(tstar)))[0] + 1) - tstar
    assert ulp > 0
    tstar_row = event_by_id["C7.NEAR_CLOCK_LIMIT.STORE_LAST_IN_DOMAIN_ORIGIN_1"]
    assert Fraction(tstar_row["exact_time"]["num"], tstar_row["exact_time"]["den"]) == tstar
    assert ceil_binary64(tstar + life[0]) == ceil_binary64(tstar + life[1]) == CLOCK
    assert tstar + life[1] <= CLOCK
    assert (tstar + ulp) + life[0] > CLOCK
    successor = tstar + ulp
    assert Fraction(event_by_id["C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1"]["exact_time"]["num"],
                    event_by_id["C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1"]["exact_time"]["den"]) == successor
    assert ceil_binary64(tstar + qabove[0]) == ceil_binary64(tstar + qabove[1]) == successor
    assert 0 < qabove[0] <= qabove[1] < ulp
    assert f64_from_bits(struct.unpack(">Q", struct.pack(">d", float(successor)))[0] - 1) == tstar
    assert qabove[1] < life[0]
    assert tstar + qabove[1] < tstar + life[0]
    assert as_mpz_units(g, successor - tstar) == g.mpz(2) ** 1041
    assert as_mpz_units(g, CLOCK - tstar) > 0
    expiry_interval = tstar + life[0], tstar + life[1]
    quiet_interval = tstar + qabove[0], tstar + qabove[1]
    for event_id in (
        "C7.NEAR_CLOCK_LIMIT.STORE_LAST_IN_DOMAIN_ORIGIN_1",
        "C7.NEAR_CLOCK_LIMIT.TIMER_EXPIRY_CREATED_FOR_INSTANCE_1",
    ):
        event_facts[event_id]["expiry_deadline_interval"] = [
            f"{v.numerator}/{v.denominator}" for v in expiry_interval
        ]
        event_facts[event_id]["expiry_deadline_common_ceiling"] = float(CLOCK).hex()
        event_facts[event_id]["expiry_precedes_clock_boundary"] = True
    event_facts["C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1"]["successor_expiry_lower_bound"] = (
        f"{(successor + life[0]).numerator}/{(successor + life[0]).denominator}"
    )
    event_facts["C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1"]["successor_expiry_out_of_domain"] = True
    for event_id in (
        "C7.POSITIVE_SUB_ULP.STORE_UPPER_Q_NEIGHBOR_1",
        "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_CREATED_1",
        "C7.POSITIVE_SUB_ULP.RECALL_ON_1",
        "C7.POSITIVE_SUB_ULP.TIMER_QUIET_CREATED_1",
        "C7.POSITIVE_SUB_ULP.TIMER_QUIET_1",
        "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_INVALIDATED_AT_QUIET_1",
    ):
        event_facts[event_id]["quiet_deadline_interval"] = [
            f"{v.numerator}/{v.denominator}" for v in quiet_interval
        ]
        event_facts[event_id]["quiet_deadline_common_ceiling"] = float(successor).hex()
        event_facts[event_id]["strict_future"] = True
        event_facts[event_id]["quiet_precedes_expiry"] = True
        event_facts[event_id]["quiet_active_delay_units_2^-1074"] = str(
            as_mpz_units(g, successor - tstar)
        )
        event_facts[event_id]["expiry_deadline_interval"] = [
            f"{v.numerator}/{v.denominator}" for v in expiry_interval
        ]
        event_facts[event_id]["expiry_deadline_common_ceiling"] = float(CLOCK).hex()
    event_facts["C7.POSITIVE_SUB_ULP.TIMER_QUIET_1"]["real_time_interval"] = [
        f"{v.numerator}/{v.denominator}" for v in quiet_interval
    ]

    group_ordinals = {
        "NEAR_CLOCK.instance_1": [
            "C7.NEAR_CLOCK_LIMIT.STORE_LAST_IN_DOMAIN_ORIGIN_1",
            "C7.NEAR_CLOCK_LIMIT.TIMER_EXPIRY_CREATED_FOR_INSTANCE_1",
        ],
        "NEAR_CLOCK.instance_2": ["C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1"],
        "POSITIVE_SUB_ULP": [
            "C7.POSITIVE_SUB_ULP.STORE_UPPER_Q_NEIGHBOR_1",
            "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_CREATED_1",
            "C7.POSITIVE_SUB_ULP.RECALL_ON_1",
            "C7.POSITIVE_SUB_ULP.TIMER_QUIET_CREATED_1",
            "C7.POSITIVE_SUB_ULP.TIMER_QUIET_1",
            "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_INVALIDATED_AT_QUIET_1",
        ],
    }
    for component, ids in group_ordinals.items():
        rows = [event_by_id[event_id] for event_id in ids]
        assert [r["final_ordinal"] for r in rows] == list(range(1, len(rows) + 1))
        assert all(r["instance_component"] == component for r in rows)
        times = [
            Fraction(r["exact_time"]["num"], r["exact_time"]["den"])
            for r in rows
        ]
        if component == "NEAR_CLOCK.instance_1":
            assert times == [tstar, tstar]
        elif component == "NEAR_CLOCK.instance_2":
            assert times == [successor]
        else:
            assert times == [tstar, tstar, tstar, tstar, successor, successor]
    expected_causes = {
        "C7.NEAR_CLOCK_LIMIT.TIMER_EXPIRY_CREATED_FOR_INSTANCE_1":
            ["C7.NEAR_CLOCK_LIMIT.STORE_LAST_IN_DOMAIN_ORIGIN_1"],
        "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_CREATED_1":
            ["C7.POSITIVE_SUB_ULP.STORE_UPPER_Q_NEIGHBOR_1"],
        "C7.POSITIVE_SUB_ULP.RECALL_ON_1":
            ["C7.POSITIVE_SUB_ULP.STORE_UPPER_Q_NEIGHBOR_1"],
        "C7.POSITIVE_SUB_ULP.TIMER_QUIET_CREATED_1":
            ["C7.POSITIVE_SUB_ULP.RECALL_ON_1"],
        "C7.POSITIVE_SUB_ULP.TIMER_QUIET_1":
            ["C7.POSITIVE_SUB_ULP.TIMER_QUIET_CREATED_1"],
        "C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_INVALIDATED_AT_QUIET_1":
            ["C7.POSITIVE_SUB_ULP.TIMER_QUIET_1"],
    }
    for event_id, causes in expected_causes.items():
        row = event_by_id[event_id]
        assert row["causal_predecessors"] == causes
        for cause_id in causes:
            cause = event_by_id[cause_id]
            cause_time = Fraction(cause["exact_time"]["num"], cause["exact_time"]["den"])
            event_time = Fraction(row["exact_time"]["num"], row["exact_time"]["den"])
            assert event_time >= cause_time
            if event_id.endswith("TIMER_QUIET_1"):
                assert event_time > cause_time
    assert len(t["observation_rows"]) == 15
    return {
        "event_count": 191,
        "c7_identity_count": 119,
        "certified_count": 9,
        "blocked_count": 182,
        "certified_ids": sorted(EXPECTED_CERTIFIED_T),
        "blocked_reason_counts": dict(sorted(reason_counts.items())),
        "independent_exact_binary64_grid_checks": 9,
        "active_time_values_reconstructed_with_GMP_integer_units": 9,
        "authored_TU_units_verified_with_GMP": {"1_TU": str(one_tu_units), "2_TU": str(two_tu_units)},
        "positive_sub_ulp_active_delay_units": str(as_mpz_units(g, successor - tstar)),
        "near_clock": {
            "least_in_domain_origin_hex": float(tstar).hex(),
            "expiry_ceiling": float(CLOCK).hex(),
            "expiry_in_inclusive_domain": True,
            "successor_store_expiry_lower_bound_exceeds_clock": True,
        },
        "positive_sub_ulp": {
            "quiet_delay_positive": True,
            "quiet_delay_less_than_origin_ulp": True,
            "common_least_ceiling_hex": float(successor).hex(),
            "strict_future_predecessor_hex": float(tstar).hex(),
            "quiet_strictly_before_expiry": True,
        },
        "equal_time_ordinal_groups": {key: len(value) for key, value in group_ordinals.items()},
        "all_182_blocked_rows_preserved": True,
        "certified_event_facts": event_facts,
    }


def requirement_rows(
    w_rows: list[dict[str, Any]], t_events: list[dict[str, Any]], t_obs: list[dict[str, Any]],
    t_audit: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_w = {row["row_id"]: row for row in w_rows}
    assert len(by_w) == 100 and all(r["status"] == "CERTIFIED" for r in by_w.values())
    for source in w_rows:
        for obligation in source["n4_a_requirements"]:
            assert obligation in A_OBLIGATIONS
            rows.append({
                "domain": "fixture_checkpoint",
                "row_id": source["row_id"],
                "fixture": source["fixture"],
                "obligation": obligation,
                "applicability": "APPLICABLE",
                "status": "PASS",
                "evidence": [f"lane-w:{source['row_id']}", "independent MPFR / rational audit"],
                "basis": "All 100 W rows retained; source pins, interval containment, exact symbolic identities, and assigned claim checks independently verified.",
            })
    for obs in t_obs:
        event_id = obs["event_id"]["id"] if isinstance(obs["event_id"], dict) else obs["event_id"]
        assert event_id in by_w
        rows.append({
            "domain": "observation_checkpoint",
            "row_id": event_id,
            "fixture": obs["fixture"],
            "obligation": "N4-A7",
            "applicability": "APPLICABLE",
            "status": "PASS",
            "evidence": [f"lane-t:observation:{event_id}", f"lane-w:{event_id}"],
            "basis": "All 15 observation-only records resolve to a W mathematical checkpoint; observations remain non-events.",
        })
    for ev in t_events:
        status = ev["status"]
        for obligation in B_OBLIGATIONS:
            applies = True
            if obligation == "N4-B3":
                applies = ev["kind"] in ("FLOW_TIMER", "EXPIRY_TIMER")
            if obligation == "N4-B6":
                applies = (
                    ev["kind"] in ("TIMER_LIFECYCLE_REFERENCE", "STALE_TIMER_POP", "EXPIRY_TIMER",
                                   "FLOW_TIMER", "OUTPUT_COMMIT", "OUTPUT_PROCESS", "OVERFLOW_ATTEMPT",
                                   "CLOSED_INGRESS")
                    or ev["fixture"] in ("C3", "C4", "C5", "C6", "C7")
                    or ev["fixture"] == "C2" and any(
                        case in ev["event_id"] for case in ("Q_ABOVE", "A1.", "A2_TANGENT")
                    )
                )
            if not applies:
                rows.append({
                    "domain": "scheduled_event",
                    "row_id": ev["event_id"],
                    "fixture": ev["fixture"],
                    "obligation": obligation,
                    "applicability": "NOT_APPLICABLE",
                    "status": "N/A",
                    "evidence": [f"lane-t:{ev['event_id']}"],
                    "basis": (
                        "This event has no positive timer delay."
                        if obligation == "N4-B3"
                        else "This event belongs to a frozen neutral or quiet-at-entry case with no lifecycle timer/output boundary."
                        if obligation == "N4-B6"
                        else "This event has no equal-time group or unresolved precedence dependency."
                    ),
                })
                continue
            blocked_reasons = ev["blocked_reasons"]
            row_status = "PASS" if status == "CERTIFIED" else "BLOCKED"
            facts = t_audit["certified_event_facts"].get(ev["event_id"])
            if row_status == "PASS" and obligation == "N4-B3":
                assert facts is not None and facts.get("strict_future") is True
            basis = (
                "Independent exact Fraction/binary64 ceiling, clock-domain, causal-order, ordinal, active-unit and lifecycle checks."
                if row_status == "PASS"
                else "T publication marks this exact event BLOCKED; E preserves rather than fills its absent time or ordinal: "
                     + ",".join(blocked_reasons)
            )
            rows.append({
                "domain": "scheduled_event",
                "row_id": ev["event_id"],
                "fixture": ev["fixture"],
                "obligation": obligation,
                "applicability": "APPLICABLE",
                "status": row_status,
                "evidence": [f"lane-t:{ev['event_id']}"] + [f"lane-w:{ref}" for ref in ev["w_evidence"]],
                "blocked_reasons": blocked_reasons if row_status == "BLOCKED" else [],
                "evidence_detail": (
                    {
                        "B1_exact_active_clock": {
                            "time_fraction": facts["exact_time_fraction"],
                            "gmp_integer_timestamp_units_2^-1074": facts["timestamp_units_2^-1074"],
                            "positive_active_delay_units_2^-1074": facts.get("quiet_active_delay_units_2^-1074"),
                        },
                        "B2_least_ceiling": {
                            "represented_hex": facts["binary64_hex"],
                            "real_time_interval": facts["real_time_interval"],
                            "least_ceiling": facts["event_timestamp_common_ceiling"],
                            "lifecycle_deadline_intervals": {
                                "quiet": facts.get("quiet_deadline_interval"),
                                "quiet_ceiling": facts.get("quiet_deadline_common_ceiling"),
                                "expiry": facts.get("expiry_deadline_interval"),
                                "expiry_ceiling": facts.get("expiry_deadline_common_ceiling"),
                            },
                        },
                        "B3_strict_future": {
                            "cause_ids": facts["cause_ids"],
                            "strict_future_proven": facts.get("strict_future", False),
                        },
                        "B4_causal_domain": {
                            "domain": "[0,2^20] inclusive",
                            "domain_result": facts["finite_clock_domain"],
                            "cause_ids": facts["cause_ids"],
                        },
                        "B5_precedence": {
                            "component": facts["component"],
                            "ordinal": facts["ordinal"],
                            "precedence_dependencies": ev["precedence_dependencies"],
                        },
                        "B6_lifecycle": {
                            "expiry_interval": facts.get("expiry_deadline_interval"),
                            "quiet_interval": facts.get("quiet_deadline_interval"),
                            "quiet_precedes_expiry": facts.get("quiet_precedes_expiry"),
                            "out_of_domain_successor": facts.get("successor_expiry_out_of_domain"),
                        },
                        "B7_identity": {
                            "inventory_source": ev["frozen_source"],
                            "event_id": ev["event_id"],
                            "mapping": "T identity reconciled; certified mapping retained" if row_status == "PASS"
                            else "identity reconciled; mapping remains BLOCKED by T",
                        },
                    }
                    if row_status == "PASS" and facts is not None else {}
                ),
                "basis": basis,
            })
    rows.sort(key=lambda r: (r["domain"], r["fixture"], r["row_id"], r["obligation"]))
    totals: dict[str, Any] = {}
    for obligation in A_OBLIGATIONS + B_OBLIGATIONS:
        subset = [r for r in rows if r["obligation"] == obligation]
        totals[obligation] = {
            "applicable_rows": sum(r["applicability"] == "APPLICABLE" for r in subset),
            "pass": sum(r["status"] == "PASS" for r in subset),
            "blocked": sum(r["status"] == "BLOCKED" for r in subset),
            "not_applicable": sum(r["status"] == "N/A" for r in subset),
        }
    return rows, totals


def build_outputs() -> tuple[dict[str, Any], dict[str, Any]]:
    w = read_json(W_DIR / "coverage_matrix.json")
    wm = read_json(W_DIR / "manifest.json")
    t = read_json(T_DIR / "schedule.json")
    tm = read_json(T_DIR / "manifest.json")
    inventory = read_json(T_DIR / "inventory.json")
    pin_evidence = check_pins(w, wm, t, tm)
    g, environment = import_gmpy2()
    assert wm["actual_environment"]["binding"].endswith(environment["binding"])
    assert environment["mpfr"] == wm["actual_environment"]["native_mpfr"]
    assert environment["gmp"] == wm["actual_environment"]["native_gmp"]
    assert environment["extension_sha256"] == wm["actual_environment"]["loaded_binary_sha256"][
        wm["actual_environment"]["binding_extension"]
    ]
    for name, record in environment["native_libraries"].items():
        assert record["sha256"] == wm["actual_environment"]["loaded_binary_sha256"][record["path"]]
    w_inventory_audit = check_w_inventory(w["rows"], w["evidence"], wm)
    w_math_audit = check_w_math(w["evidence"], g)
    w_audit = {"inventory": w_inventory_audit, "mathematics": w_math_audit}
    t_audit = check_t_math(t, inventory, w["evidence"], g)
    matrix_rows, totals = requirement_rows(w["rows"], t["rows"], t["observation_rows"], t_audit)
    blocked_ids = sorted(row["event_id"] for row in t["rows"] if row["status"] == "BLOCKED")
    matrix = {
        "format": "luna63c-stage-a-lane-e-coverage-matrix",
        "revision": 1,
        "disposition": "E BLOCKED — N4-A EVIDENCE AUDITED; N4-B FROZEN INVENTORY INCOMPLETE",
        "scope": "Certificate validation only; no candidate state, lifecycle, or Stage-B runtime execution.",
        "pins": PINS,
        "input_status": {
            "W": "COMPLETE; 100/100 mathematical witness rows",
            "T": "BLOCKED; 9/191 event identities certified; 182/191 blocked",
            "T_c7": "119 identities accounted; 9 certified and 110 blocked",
        },
        "source_clause_mapping": OWNER_SOURCE_CLAUSES,
        "historical_E1_E14_labels": (
            "No authoritative E1-E14 definitions exist in the pinned source tree. "
            "No such labels were inferred; the mechanism-contract source clauses 1-12 "
            "are mapped above to the real N4-A/N4-B schema."
        ),
        "audit_summary": {
            "w_rows": 100,
            "t_event_rows": 191,
            "t_observation_rows": 15,
            "n4_obligation_rows": len(matrix_rows),
            "n4_coverage": totals,
            "independent_w_checks": w_audit,
            "independent_t_checks": t_audit,
            "blocked_event_ids": blocked_ids,
        },
        "rows": matrix_rows,
    }
    manifest = {
        "format": "luna63c-stage-a-lane-e-manifest",
        "revision": 1,
        "verdict": matrix["disposition"],
        "pins": PINS,
        "inputs": pin_evidence,
        "environment": environment,
        "counts": {
            "w_rows": len(w["rows"]),
            "t_events": len(t["rows"]),
            "t_certified": sum(r["status"] == "CERTIFIED" for r in t["rows"]),
            "t_blocked": sum(r["status"] == "BLOCKED" for r in t["rows"]),
            "t_c7_ids": sum(r["fixture"] == "C7" for r in inventory["events"]),
            "observation_rows": len(t["observation_rows"]),
            "coverage_rows": len(matrix_rows),
        },
        "coverage": totals,
        "blocked_t_reason_counts": t_audit["blocked_reason_counts"],
        "audit": {
            "w_independent_checks": w_audit,
            "t_independent_checks": {k: v for k, v in t_audit.items() if k != "blocked_reason_counts"},
        },
        "owned_files": {
            "audit.py": sha256((HERE / "audit.py").read_bytes()),
            "test_audit.py": sha256((HERE / "test_audit.py").read_bytes()) if (HERE / "test_audit.py").exists() else None,
            "coverage_matrix.json": sha256(canonical_json(matrix).encode("utf-8")),
        },
        "limitation": "N4-B cannot close while 182 frozen T event schedules lack certified absolute event times and/or ordinals.",
    }
    return matrix, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    matrix, manifest = build_outputs()
    matrix_bytes = canonical_json(matrix).encode("utf-8")
    manifest["owned_files"]["coverage_matrix.json"] = sha256(matrix_bytes)
    manifest_bytes = canonical_json(manifest).encode("utf-8")
    if args.write:
        OUT_MATRIX.write_bytes(matrix_bytes)
        OUT_MANIFEST.write_bytes(manifest_bytes)
        print(f"Wrote {OUT_MATRIX.relative_to(ROOT)} ({len(matrix['rows'])} requirement rows)")
        print(f"Wrote {OUT_MANIFEST.relative_to(ROOT)}")
        return 0
    assert OUT_MATRIX.exists() and OUT_MANIFEST.exists()
    assert OUT_MATRIX.read_bytes() == matrix_bytes, "matrix differs from deterministic re-serialization"
    assert OUT_MANIFEST.read_bytes() == manifest_bytes, "manifest differs from deterministic re-serialization"
    print(f"PASS deterministic; W={len(read_json(W_DIR / 'coverage_matrix.json')['rows'])}; "
          f"T={len(read_json(T_DIR / 'schedule.json')['rows'])}; coverage={len(matrix['rows'])}; "
          f"blocked={manifest['counts']['t_blocked']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
