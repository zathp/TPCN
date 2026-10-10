#!/usr/bin/env python3
"""Reproducible mathematical-witness certificate for Luna-63C Stage-A Lane W."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import gmpy2


ROOT = Path(__file__).resolve().parents[4]
LANE_DIR = Path(__file__).resolve().parent
FIXTURE_JSON = ROOT / "experiments" / "luna63c" / "fixture-freeze" / "fixtures.json"
FIXTURE_MD = ROOT / "experiments" / "luna63c" / "fixture-freeze" / "FIXTURE_FREEZE.md"
FIXTURE_PUBLICATION = "583148e2812b93d519a3dc2821944d08446497b7"
FIXTURE_PINS = {
    "fixtures.json": {
        "path": "experiments/luna63c/fixture-freeze/fixtures.json",
        "blob": "8c4f9d20dda217d71ef1bcbb4fdefd0e3507ed92",
        "sha256": "AF81F3390274B2D565F90CBF12C116C78F45C5DF65D6C28BA88194E9DF2F70FB",
    },
    "FIXTURE_FREEZE.md": {
        "path": "experiments/luna63c/fixture-freeze/FIXTURE_FREEZE.md",
        "blob": "fc3d883e72ec3062e07cc453927ee76cba4aa561",
        "sha256": "B3BB25D65A8344363DF17F2A6FF3085034FDC431605B6FBA729499D512BE667F",
    },
}
PRECISIONS = (256, 512)
ROOT_BISECTIONS_PER_PRECISION = 64
ROOT_BISECTIONS_MAX = 128
ROUNDING = {
    "lower": "MPFR_RNDD / gmpy2.RoundDown",
    "upper": "MPFR_RNDU / gmpy2.RoundUp",
}
C7_CASE_ROW_PLAN = {
    "C7.DUPLICATE_RECALL": 3,
    "C7.ALTERNATING_RECALL": 5,
    "C7.RESET_BEFORE_COMMIT": 2,
    "C7.RESET_AFTER_COMMIT": 2,
    "C7.STALE_TIMER": 2,
    "C7.REARM_BEFORE_QUIET": 1,
    "C7.EXPIRY_COALESCENCE_VALID": 2,
    "C7.EXPIRY_COALESCENCE_INVALID": 2,
    "C7.TIMESTAMP_INVALID": 8,
    "C7.OVERFLOW_17": 3,
    "C7.POST_ABORT_INGRESS": 1,
    "C7.OUTPUT_EXPIRY_COALESCENCE": 2,
    "C7.NEAR_CLOCK_LIMIT": 1,
    "C7.POSITIVE_SUB_ULP": 2,
}
C4_REQUIRED_ROW_IDS = [
    "C4.STORE_STATE",
    "C4.UP_ROOT",
    "C4.UP_ROOT_STATE",
    "C4.REARM_ROOT",
    "C4.REARM_STATE",
    "C4.QUIET",
    "C4.EXPIRY",
    "C4.TERMINAL",
]
C6_REQUIRED_ROW_IDS = [
    "C6.INITIAL",
    "C6.UP_ROOT",
    "C6.UP_STATE",
    "C6.REARM_ROOT",
    "C6.REARM_STATE",
    "C6.QUIET",
    "C6.QUIET_STATE",
    "C6.TERMINAL",
]


@dataclass(frozen=True)
class Interval:
    lo: Any
    hi: Any


def context(precision: int, rounding: int) -> Any:
    ctx = gmpy2.context()
    ctx.precision = precision
    ctx.round = rounding
    return ctx


def evaluate(precision: int, rounding: int, operation: Callable[[], Any]) -> Any:
    with gmpy2.context(context(precision, rounding)):
        return operation()


def mpfr_exact(value: Fraction | int, precision: int) -> Any:
    rational = Fraction(value)
    return evaluate(
        precision,
        gmpy2.RoundToNearest,
        lambda: gmpy2.mpfr(gmpy2.mpq(rational.numerator, rational.denominator)),
    )


def rational_interval(value: Fraction | int, precision: int) -> Interval:
    rational = Fraction(value)
    exact_q = gmpy2.mpq(rational.numerator, rational.denominator)
    lo = evaluate(precision, gmpy2.RoundDown, lambda: gmpy2.mpfr(exact_q))
    hi = evaluate(precision, gmpy2.RoundUp, lambda: gmpy2.mpfr(exact_q))
    return Interval(lo, hi)


def add(left: Interval, right: Interval, precision: int) -> Interval:
    return Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: left.lo + right.lo),
        evaluate(precision, gmpy2.RoundUp, lambda: left.hi + right.hi),
    )


def negate(value: Interval) -> Interval:
    precision = max(int(value.lo.precision), int(value.hi.precision))
    return Interval(
        evaluate(precision, gmpy2.RoundToNearest, lambda: -value.hi),
        evaluate(precision, gmpy2.RoundToNearest, lambda: -value.lo),
    )


def subtract(left: Interval, right: Interval, precision: int) -> Interval:
    return add(left, negate(right), precision)


def multiply(left: Interval, right: Interval, precision: int) -> Interval:
    lower_products = [
        evaluate(precision, gmpy2.RoundDown, lambda a=a, b=b: a * b)
        for a in (left.lo, left.hi)
        for b in (right.lo, right.hi)
    ]
    upper_products = [
        evaluate(precision, gmpy2.RoundUp, lambda a=a, b=b: a * b)
        for a in (left.lo, left.hi)
        for b in (right.lo, right.hi)
    ]
    return Interval(min(lower_products), max(upper_products))


def divide_positive(numerator: Interval, denominator: Interval, precision: int) -> Interval:
    if numerator.lo < 0 or denominator.lo <= 0:
        raise ValueError("positive interval division precondition failed")
    return Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: numerator.lo / denominator.hi),
        evaluate(precision, gmpy2.RoundUp, lambda: numerator.hi / denominator.lo),
    )


def exp_interval(value: Interval, precision: int) -> Interval:
    return Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: gmpy2.exp(value.lo)),
        evaluate(precision, gmpy2.RoundUp, lambda: gmpy2.exp(value.hi)),
    )


def log_positive(value: Interval, precision: int) -> Interval:
    if value.lo <= 0:
        raise ValueError("logarithm interval is not strictly positive")
    return Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: gmpy2.log(value.lo)),
        evaluate(precision, gmpy2.RoundUp, lambda: gmpy2.log(value.hi)),
    )


def sqrt_positive(value: Interval, precision: int) -> Interval:
    if value.lo < 0:
        raise ValueError("square-root interval is negative")
    return Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: gmpy2.sqrt(value.lo)),
        evaluate(precision, gmpy2.RoundUp, lambda: gmpy2.sqrt(value.hi)),
    )


def trig_point(function: Callable[[Any], Any], value: Fraction | int, precision: int) -> Interval:
    exact = mpfr_exact(Fraction(value), precision)
    return Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: function(exact)),
        evaluate(precision, gmpy2.RoundUp, lambda: function(exact)),
    )


def pi_interval(precision: int) -> Interval:
    return Interval(
        evaluate(precision, gmpy2.RoundDown, gmpy2.const_pi),
        evaluate(precision, gmpy2.RoundUp, gmpy2.const_pi),
    )


def constants(precision: int) -> dict[str, Interval]:
    pi = pi_interval(precision)
    minus_pi_over_four = Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: -pi.hi / 4),
        evaluate(precision, gmpy2.RoundUp, lambda: -pi.lo / 4),
    )
    exp_term = exp_interval(minus_pi_over_four, precision)
    root_two = sqrt_positive(rational_interval(2, precision), precision)
    g = divide_positive(exp_term, root_two, precision)
    two = rational_interval(2, precision)
    theta = multiply(two, g, precision)
    return {"pi": pi, "sqrt2": root_two, "g": g, "q": g, "theta": theta}


def quiet_time(magnitude: Fraction | int, q: Interval, precision: int) -> Interval:
    ratio = divide_positive(rational_interval(magnitude, precision), q, precision)
    return log_positive(ratio, precision)


def interval_contains_zero(value: Interval) -> bool:
    return value.lo <= 0 <= value.hi


def sign(value: Interval) -> int:
    if value.hi < 0:
        return -1
    if value.lo > 0:
        return 1
    if value.lo == 0 and value.hi == 0:
        return 0
    raise ArithmeticError("directed enclosure did not resolve a sign")


def exact_ratio(value: Any) -> dict[str, str]:
    numerator, denominator = value.as_integer_ratio()
    return {"numerator": str(numerator), "denominator": str(denominator)}


def serialize_interval(value: Interval) -> dict[str, Any]:
    return {"lower_exact": exact_ratio(value.lo), "upper_exact": exact_ratio(value.hi)}


def deserialize_interval(value: dict[str, Any], precision: int) -> Interval:
    def endpoint(item: dict[str, str]) -> Any:
        rational = Fraction(int(item["numerator"]), int(item["denominator"]))
        return mpfr_exact(rational, precision)

    return Interval(endpoint(value["lower_exact"]), endpoint(value["upper_exact"]))


def intervals_overlap(left: Interval, right: Interval) -> bool:
    return max(left.lo, right.lo) <= min(left.hi, right.hi)


def assert_precision_consistency(values: dict[int, Interval], label: str) -> None:
    if not intervals_overlap(values[256], values[512]):
        raise ArithmeticError(f"{label} 256/512-bit outward intervals do not overlap")


def interval_state(
    magnitude: Fraction | int, polarity: int, active_time: Fraction | int, precision: int
) -> dict[str, Interval]:
    exp_factor = exp_interval(
        negate(rational_interval(active_time, precision)), precision
    )
    sine = trig_point(gmpy2.sin, active_time, precision)
    cosine = trig_point(gmpy2.cos, active_time, precision)
    amplitude = multiply(rational_interval(magnitude, precision), exp_factor, precision)
    x = multiply(amplitude, cosine, precision)
    y = multiply(amplitude, sine, precision)
    if polarity < 0:
        x, y = negate(x), negate(y)
    return {"x": x, "y": y}


def state_at_quiet_boundary(q: Interval, quiet: Interval, precision: int) -> dict[str, Interval]:
    # For A=4 the quiet root lies strictly in (pi/2, pi), where sin and cos
    # are both decreasing; endpoint evaluation therefore encloses each range.
    sine = Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: gmpy2.sin(quiet.hi)),
        evaluate(precision, gmpy2.RoundUp, lambda: gmpy2.sin(quiet.lo)),
    )
    cosine = Interval(
        evaluate(precision, gmpy2.RoundDown, lambda: gmpy2.cos(quiet.hi)),
        evaluate(precision, gmpy2.RoundUp, lambda: gmpy2.cos(quiet.lo)),
    )
    return {
        "x": multiply(q, cosine, precision),
        "y": multiply(q, sine, precision),
    }


def interval_surface(
    active_time: Fraction,
    amplitude: Fraction,
    target: Interval,
    precision: int,
) -> Interval:
    radial = multiply(
        rational_interval(amplitude, precision),
        multiply(
            exp_interval(negate(rational_interval(active_time, precision)), precision),
            trig_point(gmpy2.sin, active_time, precision),
            precision,
        ),
        precision,
    )
    return subtract(radial, target, precision)


def bracket_root(
    *,
    target_name: str,
    target_factory: Callable[[int], Interval],
    left: Fraction,
    right: Fraction,
    increasing: bool,
) -> dict[str, Any]:
    lo = left
    hi = right
    records: dict[int, dict[str, Any]] = {}
    for precision in PRECISIONS:
        start_lo = lo
        start_hi = hi
        for _ in range(ROOT_BISECTIONS_PER_PRECISION):
            midpoint = (lo + hi) / 2
            value = interval_surface(
                midpoint,
                Fraction(4),
                target_factory(precision),
                precision,
            )
            direction = sign(value)
            if direction == 0:
                raise ArithmeticError(f"{target_name} midpoint is an exact root")
            if increasing:
                if direction < 0:
                    lo = midpoint
                else:
                    hi = midpoint
            else:
                if direction > 0:
                    lo = midpoint
                else:
                    hi = midpoint
        if hi <= lo:
            raise ArithmeticError(f"{target_name} root bracket collapsed")
        endpoint_values = {
            "left": interval_surface(lo, Fraction(4), target_factory(precision), precision),
            "right": interval_surface(hi, Fraction(4), target_factory(precision), precision),
        }
        wanted_left, wanted_right = ((-1, 1) if increasing else (1, -1))
        if sign(endpoint_values["left"]) != wanted_left:
            raise ArithmeticError(f"{target_name} left endpoint sign is not resolved")
        if sign(endpoint_values["right"]) != wanted_right:
            raise ArithmeticError(f"{target_name} right endpoint sign is not resolved")
        records[precision] = {
            "start_bracket": [fraction_text(start_lo), fraction_text(start_hi)],
            "bracket": [fraction_text(lo), fraction_text(hi)],
            "width": fraction_text(hi - lo),
            "iterations_this_precision": ROOT_BISECTIONS_PER_PRECISION,
            "endpoint_surface_enclosures": {
                "left": serialize_interval(endpoint_values["left"]),
                "right": serialize_interval(endpoint_values["right"]),
            },
        }
    bracket_256 = tuple(Fraction(item) for item in records[256]["bracket"])
    bracket_512 = tuple(Fraction(item) for item in records[512]["bracket"])
    if max(bracket_256[0], bracket_512[0]) > min(bracket_256[1], bracket_512[1]):
        raise ArithmeticError(f"{target_name} 256/512 root brackets do not overlap")
    return {
        "defining_equation": f"4*exp(-s)*sin(s) = {target_name}",
        "monotonicity": (
            "strictly increasing on the certified first-lobe bracket (0, pi/4)"
            if increasing
            else "strictly decreasing on the certified post-peak bracket (pi/4, pi)"
        ),
        "existence_and_uniqueness": "strict endpoint sign change plus strict monotonicity",
        "bisection_limit": ROOT_BISECTIONS_MAX,
        "bisections_total": sum(
            run["iterations_this_precision"] for run in records.values()
        ),
        "precision_runs": {
            str(precision): records[precision] for precision in PRECISIONS
        },
        "classification": "unique root; directional sign determined by monotone branch",
        "escalation_to_1024": "not required; both governed enclosures resolve and overlap",
    }


def independent_c6_root(
    *,
    target_name: str,
    target_factory: Callable[[int], Interval],
    left: Fraction,
    right: Fraction,
    increasing: bool,
) -> dict[str, Any]:
    """Separate C6 oracle root evaluator and bracket refinement implementation."""
    lower_s = left
    upper_s = right
    records: dict[int, dict[str, Any]] = {}
    for bits in PRECISIONS:
        initial = (lower_s, upper_s)
        for _ in range(ROOT_BISECTIONS_PER_PRECISION):
            midpoint = (lower_s + upper_s) / 2
            exact_midpoint = mpfr_exact(midpoint, bits)
            decay_down = evaluate(
                bits, gmpy2.RoundDown, lambda: gmpy2.exp(-exact_midpoint)
            )
            decay_up = evaluate(
                bits, gmpy2.RoundUp, lambda: gmpy2.exp(-exact_midpoint)
            )
            sine_down = evaluate(
                bits, gmpy2.RoundDown, lambda: gmpy2.sin(exact_midpoint)
            )
            sine_up = evaluate(
                bits, gmpy2.RoundUp, lambda: gmpy2.sin(exact_midpoint)
            )
            factor_lo = evaluate(
                bits,
                gmpy2.RoundDown,
                lambda: gmpy2.mpfr(4) * decay_down * sine_down,
            )
            factor_hi = evaluate(
                bits,
                gmpy2.RoundUp,
                lambda: gmpy2.mpfr(4) * decay_up * sine_up,
            )
            target = target_factory(bits)
            f_lo = evaluate(bits, gmpy2.RoundDown, lambda: factor_lo - target.hi)
            f_hi = evaluate(bits, gmpy2.RoundUp, lambda: factor_hi - target.lo)
            value = Interval(f_lo, f_hi)
            direction = sign(value)
            if increasing:
                if direction < 0:
                    lower_s = midpoint
                else:
                    upper_s = midpoint
            else:
                if direction > 0:
                    lower_s = midpoint
                else:
                    upper_s = midpoint
        endpoint_results: dict[str, Interval] = {}
        for label, endpoint in (("left", lower_s), ("right", upper_s)):
            exact_endpoint = mpfr_exact(endpoint, bits)
            dec_lo = evaluate(bits, gmpy2.RoundDown, lambda: gmpy2.exp(-exact_endpoint))
            dec_hi = evaluate(bits, gmpy2.RoundUp, lambda: gmpy2.exp(-exact_endpoint))
            sin_lo = evaluate(bits, gmpy2.RoundDown, lambda: gmpy2.sin(exact_endpoint))
            sin_hi = evaluate(bits, gmpy2.RoundUp, lambda: gmpy2.sin(exact_endpoint))
            product_lo = evaluate(
                bits,
                gmpy2.RoundDown,
                lambda: gmpy2.mpfr(4) * dec_lo * sin_lo,
            )
            product_hi = evaluate(
                bits,
                gmpy2.RoundUp,
                lambda: gmpy2.mpfr(4) * dec_hi * sin_hi,
            )
            target = target_factory(bits)
            endpoint_results[label] = Interval(
                evaluate(bits, gmpy2.RoundDown, lambda: product_lo - target.hi),
                evaluate(bits, gmpy2.RoundUp, lambda: product_hi - target.lo),
            )
        expected_left, expected_right = ((-1, 1) if increasing else (1, -1))
        if sign(endpoint_results["left"]) != expected_left:
            raise ArithmeticError("independent C6 left endpoint sign unresolved")
        if sign(endpoint_results["right"]) != expected_right:
            raise ArithmeticError("independent C6 right endpoint sign unresolved")
        records[bits] = {
            "start_bracket": [fraction_text(initial[0]), fraction_text(initial[1])],
            "bracket": [fraction_text(lower_s), fraction_text(upper_s)],
            "width": fraction_text(upper_s - lower_s),
            "iterations_this_precision": ROOT_BISECTIONS_PER_PRECISION,
            "endpoint_surface_enclosures": {
                "left": serialize_interval(endpoint_results["left"]),
                "right": serialize_interval(endpoint_results["right"]),
            },
        }
    return {
        "defining_equation": f"4*exp(-s)*sin(s) = {target_name}",
        "solver": "independent C6 scalar enclosure/bisection path; no C4 root result is an input",
        "monotonicity": (
            "strictly increasing on the certified first-lobe bracket (0, pi/4)"
            if increasing
            else "strictly decreasing on the certified post-peak bracket (pi/4, pi)"
        ),
        "existence_and_uniqueness": "strict endpoint sign change plus strict monotonicity",
        "bisection_limit": ROOT_BISECTIONS_MAX,
        "bisections_total": sum(
            run["iterations_this_precision"] for run in records.values()
        ),
        "precision_runs": {
            str(bits): records[bits] for bits in PRECISIONS
        },
        "classification": "unique independent reference root",
        "escalation_to_1024": "not required; both governed enclosures resolve and overlap",
    }


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact_float_fraction(value: float) -> Fraction:
    numerator, denominator = value.as_integer_ratio()
    return Fraction(numerator, denominator)


def positive_float_bits(value: float) -> int:
    bits = struct.unpack(">Q", struct.pack(">d", value))[0]
    if bits >> 63 or bits == 0 or bits >= 0x7FF0000000000000:
        raise ValueError("fixture neighbor conversion expected positive finite binary64")
    return bits


def float_from_positive_bits(bits: int) -> float:
    return struct.unpack(">d", struct.pack(">Q", bits))[0]


def q_neighbors(q_runs: dict[int, Interval]) -> dict[str, Any]:
    q = q_runs[512]
    midpoint = evaluate(
        512,
        gmpy2.RoundToNearest,
        lambda: (q.lo + q.hi) / 2,
    )
    center = float(midpoint)
    bits = positive_float_bits(center)
    center_fraction = exact_float_fraction(center)
    q_lower = q.lo.as_integer_ratio()
    q_upper = q.hi.as_integer_ratio()
    q_lo_fraction = Fraction(*q_lower)
    q_hi_fraction = Fraction(*q_upper)
    if center_fraction < q_lo_fraction:
        lower_bits, upper_bits = bits, bits + 1
    elif center_fraction > q_hi_fraction:
        lower_bits, upper_bits = bits - 1, bits
    else:
        raise ArithmeticError("binary64 candidate lies inside the 512-bit q enclosure")
    lower = float_from_positive_bits(lower_bits)
    upper = float_from_positive_bits(upper_bits)
    lower_exact = exact_float_fraction(lower)
    upper_exact = exact_float_fraction(upper)
    if not (lower_exact < q_lo_fraction and q_hi_fraction < upper_exact):
        raise ArithmeticError("q enclosure does not lie strictly between adjacent floats")
    if upper_bits - lower_bits != 1:
        raise ArithmeticError("q neighbors are not adjacent binary64 values")
    if not upper < 1.0:
        raise ArithmeticError("the fixture's q upper neighbor is not below one")
    return {
        "definition": "greatest finite binary64 < q and least finite binary64 > q",
        "lower_hex": lower.hex(),
        "lower_bits_hex": f"0x{lower_bits:016x}",
        "upper_hex": upper.hex(),
        "upper_bits_hex": f"0x{upper_bits:016x}",
        "adjacent_bits": True,
        "q_256_512_interval_strictly_between_neighbors": True,
        "upper_neighbor_strictly_less_than_one": True,
        "no_event_time_or_ordinal_materialized": True,
    }


def interval_from_serialized_root(root: dict[str, Any], precision: int) -> tuple[Fraction, Fraction]:
    bracket = root["precision_runs"][str(precision)]["bracket"]
    def parse(item: str) -> Fraction:
        numerator, denominator = item.split("/")
        return Fraction(int(numerator), int(denominator))
    return parse(bracket[0]), parse(bracket[1])


def root_state_enclosures(root: dict[str, Any], polarity: int) -> dict[str, Any]:
    runs: dict[str, Any] = {}
    for precision in PRECISIONS:
        left, right = interval_from_serialized_root(root, precision)
        # The upward root is in (0, pi/4); the re-arm root is in (pi/4, pi).
        # Each monotone branch has fixed signs for sin/cos over its tiny bracket.
        lower_t = rational_interval(right, precision)
        upper_t = rational_interval(left, precision)
        exp_lo = exp_interval(negate(lower_t), precision).lo
        exp_hi = exp_interval(negate(upper_t), precision).hi
        sin_left = trig_point(gmpy2.sin, left, precision)
        sin_right = trig_point(gmpy2.sin, right, precision)
        cos_left = trig_point(gmpy2.cos, left, precision)
        cos_right = trig_point(gmpy2.cos, right, precision)
        if left < Fraction(1):
            sine = Interval(sin_left.lo, sin_right.hi)
            cosine = Interval(cos_right.lo, cos_left.hi)
        else:
            sine = Interval(sin_right.lo, sin_left.hi)
            cosine = Interval(cos_right.lo, cos_left.hi)
        radial = multiply(
            rational_interval(4, precision),
            Interval(exp_lo, exp_hi),
            precision,
        )
        x = multiply(radial, cosine, precision)
        y = multiply(radial, sine, precision)
        if polarity < 0:
            x, y = negate(x), negate(y)
        runs[str(precision)] = {
            "x": serialize_interval(x),
            "y_surface": (
                "theta exactly at the upward root"
                if left < Fraction(1)
                else "q exactly at the downward re-arm root"
            ),
        }
    return runs


def host_identity() -> dict[str, Any]:
    import ctypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
    kernel.GetModuleHandleW.restype = ctypes.c_void_p
    kernel.GetModuleFileNameW.argtypes = [
        ctypes.c_void_p,
        ctypes.c_wchar_p,
        ctypes.c_uint,
    ]
    kernel.GetModuleFileNameW.restype = ctypes.c_uint
    loaded: dict[str, str] = {}
    for name in ("libmpfr-6.dll", "libgmp-10.dll"):
        module = kernel.GetModuleHandleW(name)
        buffer = ctypes.create_unicode_buffer(32768)
        length = kernel.GetModuleFileNameW(module, buffer, len(buffer)) if module else 0
        if not module or not length:
            raise RuntimeError(f"{name} is not loaded in the reference process")
        loaded[name] = buffer.value[:length]
    module_path = Path(gmpy2.__file__).resolve()
    extension_path = Path(sys.modules["gmpy2.gmpy2"].__file__).resolve()
    native_hashes = {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest().upper()
        for path in [extension_path, *(Path(path) for path in loaded.values())]
    }
    exp_smoke = exp_interval(rational_interval(1, 256), 256)
    pi_smoke = pi_interval(256)
    if not (exp_smoke.lo < exp_smoke.hi and pi_smoke.lo < pi_smoke.hi):
        raise RuntimeError("directed MPFR lower/upper rounding smoke test failed")
    return {
        "python": sys.version,
        "python_executable": str(Path(sys.executable).resolve()),
        "implementation": sys.implementation.name,
        "platform": sys.platform,
        "machine": os.environ.get("PROCESSOR_ARCHITECTURE", "unknown"),
        "binding": f"gmpy2 {gmpy2.version()}",
        "binding_package_module": str(module_path),
        "binding_extension": str(extension_path),
        "native_mpfr": gmpy2.mpfr_version(),
        "native_gmp": gmpy2.mp_version(),
        "loaded_native_paths": loaded,
        "loaded_binary_sha256": native_hashes,
        "rounding_constants": {
            "down": int(gmpy2.RoundDown),
            "up": int(gmpy2.RoundUp),
        },
        "outward_rounding_smoke_test": {
            "precision_bits": 256,
            "exp_1_lower_lt_upper": True,
            "pi_lower_lt_upper": True,
            "exp_1_interval": serialize_interval(exp_smoke),
            "pi_interval": serialize_interval(pi_smoke),
        },
        "profile_match": (
            gmpy2.mpfr_version() == "MPFR 4.2.2"
            and gmpy2.mp_version() == "GMP 6.3.0"
        ),
    }


def verify_source_pins() -> dict[str, Any]:
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", FIXTURE_PUBLICATION, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    ).returncode != 0:
        raise RuntimeError("immutable fixture publication is not an ancestor of HEAD")
    reports: dict[str, Any] = {}
    for name, pin in FIXTURE_PINS.items():
        head_blob = subprocess.run(
            ["git", "rev-parse", f"HEAD:{pin['path']}"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        ).stdout.strip()
        if head_blob != pin["blob"]:
            raise RuntimeError(f"{pin['path']} no longer matches pinned Git blob")
        canonical = subprocess.run(
            ["git", "cat-file", "blob", pin["blob"]],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
        canonical_hash = hashlib.sha256(canonical).hexdigest().upper()
        if canonical_hash != pin["sha256"]:
            raise RuntimeError(f"{pin['path']} canonical blob SHA256 mismatch")
        working_path = ROOT / Path(pin["path"])
        working_bytes = working_path.read_bytes()
        working_hash = hashlib.sha256(working_bytes).hexdigest().upper()
        normalized_hash = hashlib.sha256(
            working_bytes.replace(b"\r\n", b"\n")
        ).hexdigest().upper()
        if pin["path"].endswith("fixtures.json") and normalized_hash != pin["sha256"]:
            raise RuntimeError("fixture JSON checkout does not normalize to the pinned bytes")
        if pin["path"].endswith("FIXTURE_FREEZE.md") and working_hash != pin["sha256"]:
            raise RuntimeError("fixture-freeze Markdown raw checkout hash mismatch")
        reports[name] = {
            "path": pin["path"],
            "publication_commit": FIXTURE_PUBLICATION,
            "git_blob": pin["blob"],
            "canonical_blob_sha256": canonical_hash,
            "checkout_raw_sha256": working_hash,
            "checkout_lf_sha256": normalized_hash,
            "checkout_materialization_note": (
                "core.autocrlf=true; checkout CRLF bytes normalize to the pinned LF blob"
                if working_hash != canonical_hash
                else "checkout raw bytes equal the pinned canonical bytes"
            ),
        }
    return reports


def c7_case_map(fixtures: dict[str, Any]) -> dict[str, dict[str, Any]]:
    fixture = next(item for item in fixtures["fixtures"] if item["id"] == "C7")
    return {case["id"]: case for case in fixture["cases"]}


def row(
    row_id: str,
    fixture: str,
    subcase: str | None,
    checkpoint: str,
    claim: str,
    evidence_class: str,
    proof_refs: list[str],
    proof: str,
    *,
    n4_a: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "fixture": fixture,
        "subcase": subcase,
        "checkpoint": checkpoint,
        "owner": "W",
        "status": "CERTIFIED",
        "evidence_class": evidence_class,
        "claim": claim,
        "defining_function_or_identity": proof,
        "proof_refs": proof_refs,
        "n4_a_requirements": n4_a or ["N4-A1", "N4-A2", "N4-A5", "N4-A7"],
        "interval_method": (
            "Exact symbolic proof; no numerical interval required for this equality/classification."
            if evidence_class == "EXACT_SYMBOLIC"
            else "MPFR 4.2.2 / GMP 6.3.0; directed outward lower RNDD and upper RNDU at 256 and 512 bits; exact MPFR endpoints serialized as rational pairs."
        ),
    }


def make_evidence(fixtures: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    precision_constants = {
        precision: constants(precision) for precision in PRECISIONS
    }
    for name in ("pi", "sqrt2", "g", "q", "theta"):
        assert_precision_consistency(
            {precision: precision_constants[precision][name] for precision in PRECISIONS},
            name,
        )
    q_runs = {p: precision_constants[p]["q"] for p in PRECISIONS}
    theta_runs = {p: precision_constants[p]["theta"] for p in PRECISIONS}
    neighbors = q_neighbors(q_runs)
    q_below = Fraction.from_float(float.fromhex(neighbors["lower_hex"]))
    q_above = Fraction.from_float(float.fromhex(neighbors["upper_hex"]))
    if not (q_below < q_runs[256].lo and q_runs[512].hi < q_above):
        raise ArithmeticError("neighbor classifications are not separated by q intervals")

    quiet_runs: dict[str, dict[int, Interval]] = {}
    for label, magnitude in (("A1", Fraction(1)), ("A4", Fraction(4)), ("Q_ABOVE", q_above)):
        quiet_runs[label] = {
            precision: quiet_time(
                magnitude, precision_constants[precision]["q"], precision
            )
            for precision in PRECISIONS
        }
        assert_precision_consistency(quiet_runs[label], f"quiet_{label}")
    tq_runs = quiet_runs["A4"]
    life_runs = {
        precision: add(
            rational_interval(3, precision),
            tq_runs[precision],
            precision,
        )
        for precision in PRECISIONS
    }
    assert_precision_consistency(life_runs, "T_life")

    up_root = bracket_root(
        target_name="theta",
        target_factory=lambda p: precision_constants[p]["theta"],
        left=Fraction(0),
        right=Fraction(1, 2),
        increasing=True,
    )
    rearm_root = bracket_root(
        target_name="q",
        target_factory=lambda p: precision_constants[p]["q"],
        left=Fraction(1),
        right=Fraction(3),
        increasing=False,
    )
    root_states = {
        "up": root_state_enclosures(up_root, 1),
        "rearm": root_state_enclosures(rearm_root, 1),
        "up_negative_orientation": root_state_enclosures(up_root, -1),
    }

    # C6 is independently recomputed by fresh calls with its own root objects.
    c6_up = independent_c6_root(
        target_name="theta",
        target_factory=lambda p: precision_constants[p]["theta"],
        left=Fraction(0),
        right=Fraction(1, 4),
        increasing=True,
    )
    c6_rearm = independent_c6_root(
        target_name="q",
        target_factory=lambda p: precision_constants[p]["q"],
        left=Fraction(2),
        right=Fraction(3),
        increasing=False,
    )
    c6_quiet = {
        precision: quiet_time(
            Fraction(4), constants(precision)["q"], precision
        )
        for precision in PRECISIONS
    }
    assert_precision_consistency(c6_quiet, "C6 quiet root")
    quiet_boundary_states = {
        "C4": {
            str(precision): {
                coordinate: serialize_interval(value)
                for coordinate, value in state_at_quiet_boundary(
                    precision_constants[precision]["q"],
                    tq_runs[precision],
                    precision,
                ).items()
            }
            for precision in PRECISIONS
        },
        "C6": {
            str(precision): {
                coordinate: serialize_interval(value)
                for coordinate, value in state_at_quiet_boundary(
                    constants(precision)["q"],
                    c6_quiet[precision],
                    precision,
                ).items()
            }
            for precision in PRECISIONS
        },
    }
    for boundary, by_precision in quiet_boundary_states.items():
        for coordinate in ("x", "y"):
            parsed: dict[int, Interval] = {}
            for precision in PRECISIONS:
                serialized = by_precision[str(precision)][coordinate]
                parsed[precision] = deserialize_interval(serialized, precision)
            assert_precision_consistency(parsed, f"{boundary} quiet-state {coordinate}")
    c6_root_states = {
        "up": root_state_enclosures(c6_up, 1),
        "rearm": root_state_enclosures(c6_rearm, 1),
    }
    for precision in PRECISIONS:
        for label, primary, independent in (
            ("C6_up", up_root, c6_up),
            ("C6_rearm", rearm_root, c6_rearm),
        ):
            a = interval_from_serialized_root(primary, precision)
            b = interval_from_serialized_root(independent, precision)
            if max(a[0], b[0]) > min(a[1], b[1]):
                raise ArithmeticError(f"{label} independent enclosure disagrees")
        if not intervals_overlap(tq_runs[precision], c6_quiet[precision]):
            raise ArithmeticError("C6 quiet root does not overlap the C4 root")

    oracle_states: dict[str, Any] = {}
    for polarity_label, polarity in (("P", 1), ("N", -1)):
        oracle_states[polarity_label] = {}
        for time_label, active_time in (
            ("S0", Fraction(0)),
            ("S1_2", Fraction(1, 2)),
            ("S1", Fraction(1)),
            ("S2", Fraction(2)),
        ):
            oracle_states[polarity_label][time_label] = {
                str(precision): {
                    coordinate: serialize_interval(value)
                    for coordinate, value in interval_state(
                        Fraction(1), polarity, active_time, precision
                    ).items()
                }
                for precision in PRECISIONS
            }

    # MPFR-directed enclosures verify the qualitative subinterval claims.
    sq_a1 = quiet_runs["A1"]
    pi_256 = precision_constants[256]["pi"]
    pi_512 = precision_constants[512]["pi"]
    for precision, quiet in sq_a1.items():
        if not (quiet.lo > 1 and quiet.hi < 2):
            raise ArithmeticError("A=1 quiet root is not certified in (1,2)")
    for precision, quiet in tq_runs.items():
        if not (quiet.lo > 2 and quiet.hi < 3):
            raise ArithmeticError("A=4 quiet root is not certified in (2,3)")
        if not (life_runs[precision].lo > quiet.hi):
            raise ArithmeticError("finite lifetime does not strictly exceed quiet time")
    if not (q_runs[256].lo > 0 and q_runs[512].hi < 1):
        raise ArithmeticError("q is not certified in (0,1)")
    if not (pi_256.lo > 3 and pi_512.hi < 4):
        raise ArithmeticError("pi elementary bracket failed")
    q_above_quiet = quiet_runs["Q_ABOVE"]
    if not all(
        q_above_quiet[precision].lo > 0
        and q_above_quiet[precision].hi < tq_runs[precision].lo
        for precision in PRECISIONS
    ):
        raise ArithmeticError("positive upper-neighbor quiet delay is unresolved")
    if not all(
        exact_float_fraction(float.fromhex(neighbors["lower_hex"])) < q_runs[p].lo
        and q_runs[p].hi < exact_float_fraction(float.fromhex(neighbors["upper_hex"]))
        for p in PRECISIONS
    ):
        raise ArithmeticError("q neighbor relation disagrees at 256/512 bits")
    for polarity_label in ("P", "N"):
        for time_label in ("S0", "S1_2", "S1", "S2"):
            runs = oracle_states[polarity_label][time_label]
            for coordinate in ("x", "y"):
                assert_precision_consistency(
                    {
                        precision: deserialize_interval(
                            runs[str(precision)][coordinate], precision
                        )
                        for precision in PRECISIONS
                    },
                    f"A1 oracle {polarity_label}/{time_label}/{coordinate}",
                )
    for family, state_set in (
        ("A4", root_states),
        ("C6", c6_root_states),
    ):
        for root_name, runs in state_set.items():
            if root_name not in ("up", "rearm"):
                continue
            assert_precision_consistency(
                {
                    precision: deserialize_interval(
                        runs[str(precision)]["x"], precision
                    )
                    for precision in PRECISIONS
                },
                f"{family} {root_name} root-state x",
            )

    evidence: dict[str, Any] = {
        "environment": host_identity(),
        "source_pins": verify_source_pins(),
        "arithmetic_profile": {
            "native_profile": "MPFR C API 4.2.2 / GMP 6.3.0",
            "binding_used": f"gmpy2 {gmpy2.version()}",
            "binding_role": "Python binding to MPFR/GMP; only outward-rounded interval operations are used for numerical reference quantities.",
            "precisions_bits": list(PRECISIONS),
            "escalation_1024": "none required; all interval classifications resolved and 256/512 enclosures overlap",
            "root_bisection_cap": ROOT_BISECTIONS_MAX,
            "rounding": ROUNDING,
            "host_libm_used_for_reference_transcendentals": False,
            "active_time_or_event_clock_conversion_performed": False,
            "gmp_integer_active_time_accumulation_performed": False,
        },
        "constants": {
            name: {
                str(precision): serialize_interval(precision_constants[precision][name])
                for precision in PRECISIONS
            }
            for name in ("pi", "sqrt2", "g", "q", "theta")
        },
        "q_neighbor_inputs": neighbors,
        "quiet_times": {
            label: {
                str(precision): serialize_interval(quiet_runs[label][precision])
                for precision in PRECISIONS
            }
            for label in ("A1", "A4", "Q_ABOVE")
        },
        "T_q_A4": {
            str(precision): serialize_interval(tq_runs[precision])
            for precision in PRECISIONS
        },
        "T_life_A4": {
            "formula": "H + T_q + 1 = 3 + ln(4/q)",
            "identity": "3 + ln(4*sqrt(2)) + pi/4",
            "enclosures": {
                str(precision): serialize_interval(life_runs[precision])
                for precision in PRECISIONS
            },
        },
        "roots_A4": {"up": up_root, "rearm": rearm_root},
        "roots_C6_independent": {"up": c6_up, "rearm": c6_rearm},
        "root_state_enclosures_A4": root_states,
        "root_state_enclosures_C6_independent": c6_root_states,
        "quiet_times_C6_independent": {
            str(precision): serialize_interval(c6_quiet[precision])
            for precision in PRECISIONS
        },
        "quiet_boundary_states": quiet_boundary_states,
        "A1_oracle_states": oracle_states,
        "exact_symbolic_proofs": {
            "flow": "X(s)=p*A*exp(-s)*(cos(s),sin(s)); derived by exp(sM)=exp(-s)Rot(s), M=[[-1,-1],[1,-1]].",
            "radius": "x(s)^2+y(s)^2=A^2*exp(-2s); for s>=0 and A<=4 this is <=16.",
            "held": "R=0 gives s=0 identically, so X=(p*A,0) for every HOLD duration.",
            "quiet_A1": "ln(1/q)=pi/4+(ln 2)/2; directed interval lies strictly in (1,2).",
            "A1_s2_error": "candidate ideal terminal state is (0,0); independent unreset oracle norm is exp(-2). Strict margin exp(-2)<theta/4 follows from pi<22/7, e^(6/5)>73/25, (73/25)^2>8, and 2-pi/4>6/5.",
            "A1_s0_s_half_s1": "quiet is strictly after active time 1; the ideal state has not reset at 0, 1/2, or 1 and equals the independent semigroup state exactly. No candidate implementation comparison is made.",
            "A2_tangent": "At s=pi/4, 2*exp(-s)*sin(s)=theta exactly and derivative 2*exp(-s)*(cos(s)-sin(s))=0. The second derivative is strictly negative; later positive lobes are smaller by exp(-2*pi). No upward crossing.",
            "A2_tangent_state": "At s=pi/4 for A=2, X=(p*theta,p*theta) exactly; p*y=theta and d(p*y)/ds=0.",
            "A1_subthreshold": "For A=1 the maximum oriented output ordinate is g=q=theta/2<theta; no crossing.",
            "q_neighbor_subthreshold": "The upper binary64 neighbor of q is certified <1; its first-lobe maximum A*g<g=theta/2<theta, so it cannot cross.",
            "A4_up_crossing": "For A=4 the first-lobe peak is 4g=2theta>theta; strict monotonicity on (0,pi/4) gives exactly one upward root.",
            "A4_rearm": "For A=4, 4*exp(-s)*sin(s) strictly decreases on (pi/4,pi) from 4g to 0; exactly one downward q root.",
            "A4_quiet": "For A=4, r=4*exp(-s); first inward r=q occurs at ln(4/q), and derivative dr/ds=-r<0.",
            "A4_rearm_before_quiet": "The directed enclosures establish s_rearm<pi and s_quiet<pi; at s_quiet, p*y=q*sin(s_quiet)<q, while p*y>q at pi/4. Strict decrease after pi/4 therefore places the unique re-arm root before quiet.",
            "A4_quiet_before_expiry": "The exact lifetime is T_life=H+T_q+1=3+T_q, hence the A=4 quiet transition occurs exactly three TU before expiry in uninterrupted release from STORE.",
            "C5_hold_shift": "For H in {0,1,2}, HOLD adds no active time; corresponding mathematical event times are t_store+H+s_root. Root offsets and state formulas are identical; no binary64 bit-identity claim.",
            "C7_time_schedules": "All W claims are limited to the frozen real-time mathematical sources and conditional inequalities. Binary64 ceilings, input timestamps, scheduler order, and ordinals are not computed.",
        },
    }

    rows = build_rows(fixtures, evidence)
    return evidence, rows


def build_rows(fixtures: dict[str, Any], evidence: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    fixture_by_id = {fixture["id"]: fixture for fixture in fixtures["fixtures"]}
    exact = "EXACT_SYMBOLIC"
    numeric = "MPFR_OUTWARD_INTERVAL"

    rows.append(
        row(
            "C0.INITIAL",
            "C0",
            None,
            "C0.INITIAL",
            "Neutral state is a fixed point with no output, timer, or episode.",
            exact,
            ["flow", "radius"],
            "X0=(0,0); M*X0=0 and R=0 is identity.",
        )
    )
    for checkpoint in fixture_by_id["C1"]["checkpoints"]:
        rows.append(
            row(
                checkpoint["id"],
                "C1",
                None,
                checkpoint["id"],
                "RECALL changes only the gate; neutral state remains exactly (0,0).",
                exact,
                ["flow"],
                "X0=(0,0) is fixed for either R; no event surface crossing.",
            )
        )

    c2 = fixture_by_id["C2"]
    for case in c2["cases"]:
        polarities = case.get("instance_polarities", [])
        if not polarities:
            rows.append(
                row(
                    f"C2.{case['case_id']}.ZERO",
                    "C2",
                    case["case_id"],
                    f"{case['case_id']}.CLASSIFICATION",
                    "A=0 is quiet-at-entry; no logarithm, dynamic timer, or output.",
                    exact,
                    ["held"],
                    "A=0<=q and the fixture's atomic QUIET_ENTRY rule applies.",
                )
            )
            continue
        for designation in polarities:
            polarity_label, polarity_text = designation.split(":")
            case_id = case["case_id"]
            if case_id in ("AQ2", "AQ"):
                source_refs = ["constants"]
                proof_text = (
                    "A=q/2<q: exact strict inequality from q>0."
                    if case_id == "AQ2"
                    else "A=q exact symbolic equality: QUIET_ENTRY at STORE; no ln(A/q)."
                )
                claim = (
                    "Exact quiet-entry classification; no timer or output."
                    if case_id == "AQ2"
                    else "Exact-boundary quiet-entry classification; no logarithm, timer, or output."
                )
                evidence_class = exact
            elif case_id in ("Q_BELOW", "Q_ABOVE"):
                source_refs = ["q_neighbor_inputs", "constants", "q_neighbor_subthreshold"]
                relation = "A<q" if case_id == "Q_BELOW" else "A>q"
                proof_text = f"{relation} certified by exact binary64 dyadic import and the 256/512 q enclosure."
                claim = (
                    "Strict quiet-entry classification without logarithm, timer, or output."
                    if case_id == "Q_BELOW"
                    else "Strictly above q; positive quiet root exists, no output."
                )
                evidence_class = numeric
            elif case_id == "A1":
                source_refs = ["constants", "quiet_times.A1", "A1_subthreshold"]
                proof_text = "A=1>q and A*g=theta/2; quiet occurs after s=1 and before s=2."
                claim = "Subthreshold uninterrupted flow, no upward crossing, then quiet."
                evidence_class = numeric
            else:
                source_refs = ["constants.theta", "A2_tangent", "A2_tangent_state"]
                proof_text = "A=2 first-lobe maximum equals theta exactly; derivative is zero at s=pi/4."
                claim = "Exact tangent (not an upward crossing), then quiet; no output."
                evidence_class = exact
            rows.append(
                row(
                    f"C2.{case_id}.{polarity_label}.CASE",
                    "C2",
                    case_id,
                    f"{case_id}.{polarity_label}.CLASSIFICATION",
                    f"{claim} Orientation p={polarity_text}.",
                    evidence_class,
                    source_refs,
                    proof_text,
                    n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A5", "N4-A6", "N4-A7"],
                )
            )

    for checkpoint in c2["A1_checkpoints"]:
        polarity_label = "P" if checkpoint["polarity"] > 0 else "N"
        time_label = checkpoint["id"].rsplit(".", 1)[1]
        state = evidence["A1_oracle_states"][polarity_label][time_label]
        rows.append(
            {
                **row(
                    checkpoint["id"],
                    "C2",
                    "A1",
                    checkpoint["id"],
                    "Full two-coordinate independent flow-oracle state at exact active time "
                    f"s={checkpoint['active_time_TU']} TU; polarity p={checkpoint['polarity']}.",
                    numeric if checkpoint["active_time_TU"] not in ("0",) else exact,
                    ["A1_oracle_states", "quiet_times.A1", "A1_s2_error"],
                    "X_oracle=p*exp(-s)*(cos(s),sin(s)); q is owner-frozen and this checkpoint creates no event.",
                    n4_a=checkpoint["n4_a_requirements"],
                ),
                "active_time_TU": checkpoint["active_time_TU"],
                "polarity": checkpoint["polarity"],
                "oracle_state_enclosures": state,
                "candidate_comparison": "NOT PERFORMED — no Stage-B candidate evaluation in Lane W.",
                "candidate_ideal_lifecycle_state": (
                    ["0", "0"] if checkpoint["active_time_TU"] == "2" else "same exact flow state before quiet"
                ),
                "comparison_rule_reference": "strict L2 distance < theta/4; mathematical margin only at s=2",
            }
        )

    rows.append(
        row(
            "C2.A1.STRICT_MARGIN",
            "C2",
            "A1",
            "A1_S2_IDEAL_COMPARISON",
            "The exact ideal-model discrepancy at s=2 is exp(-2), strictly less than the owner-frozen later acceptance ceiling theta/4; this is not a candidate result.",
            exact,
            ["A1_s2_error", "constants.theta"],
            "At s=2 the ideal candidate has cleared to zero while the independent unreset oracle has norm exp(-2); the exact inequality proof is recorded in evidence.",
            n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A6", "N4-A7"],
        )
    )

    c3 = fixture_by_id["C3"]
    for checkpoint in c3["checkpoints"]:
        if checkpoint["id"] == "C3.AFTER_STORE":
            hold_values = ["STORE"]
        else:
            hold_values = c3["hold_durations_TU"]
        for hold in hold_values:
            row_id = "C3.AFTER_STORE" if hold == "STORE" else f"C3.DURING_HOLD@{hold}"
            rows.append(
                row(
                    row_id,
                    "C3",
                    f"HOLD_{hold}",
                    checkpoint["id"],
                    "Stored A=4 state remains exactly (4,0) during HOLD; the disk boundary is met but never exceeded.",
                    exact,
                    ["held", "radius"],
                    "R=0 implies s=0; x=4, y=0, x^2+y^2=16.",
                )
            )
    rows.append(
        row(
            "C3.EXPIRY_TIE.MATHEMATICAL",
            "C3",
            "EXPIRY_TIE",
            "C3.EXPIRY_TIE",
            "Held state is unchanged up to the exact STORE-origin lifetime; expiry is a terminal clear.",
            numeric,
            ["T_q_A4", "T_life_A4", "held"],
            "t_exp=t_store+T_life; T_life=3+ln(4/q)>0. No binary64 coalescence or timestamp is resolved here.",
            n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A6", "N4-A7"],
        )
    )

    rows.extend(
        [
            row("C4.STORE_STATE", "C4", "A4", "STORE", "Accepted mathematical load is X=(4,0), within the invariant disk.", exact, ["radius"], "A=4,p=+1; x^2+y^2=16."),
            row("C4.UP_ROOT", "C4", "A4", "C4.TIMER_CROSSING", "Exactly one first-lobe upward root exists and its derivative is positive.", numeric, ["roots_A4.up", "A4_up_crossing"], "F_theta(s)=4 exp(-s) sin(s)-theta; unique root in (0,1/2) subset (0,pi/4).", n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A5", "N4-A7"]),
            row("C4.UP_ROOT_STATE", "C4", "A4", "C4.OUTPUT_COMMIT", "At the mathematical upward root, y=theta exactly and the full-state x enclosure is supplied.", numeric, ["root_state_enclosures_A4.up"], "X(s*)=(4 exp(-s*)cos(s*), theta), p=+1; root bracket and directed state enclosure are in the proof table.", n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A5", "N4-A7"]),
            row("C4.REARM_ROOT", "C4", "A4", "C4.TIMER_REARM", "Exactly one downward re-arm root exists after the peak and before quiet.", numeric, ["roots_A4.rearm", "A4_rearm_before_quiet"], "F_q(s)=4 exp(-s) sin(s)-q; unique on (1,3) subset (pi/4,pi); derivative strictly negative."),
            row("C4.REARM_STATE", "C4", "A4", "C4.TIMER_REARM", "At downward re-arm, p*y=q exactly and the full-state x coordinate has an outward enclosure.", numeric, ["root_state_enclosures_A4.rearm"], "X(s_r)=(4 exp(-s_r)cos(s_r),q), with s_r enclosed by the bisection bracket."),
            row("C4.QUIET", "C4", "A4", "C4.TIMER_QUIET", "Quiet is the first inward radius-q crossing; pre-clear full state is enclosed, then terminal clear follows.", numeric, ["quiet_times.A4", "T_q_A4", "quiet_boundary_states.C4"], "r(s)=4 exp(-s); s_quiet=ln(4/q), dr/ds=-r<0; at the boundary X=q(cos(s_q),sin(s_q)); lifecycle then clears to (0,0).", n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A5", "N4-A6", "N4-A7"]),
            row("C4.EXPIRY", "C4", "A4", "C4.TIMER_EXPIRY", "Exact lifetime is finite and quiet occurs three active TU before expiry for the uninterrupted H=0 release.", numeric, ["T_q_A4", "T_life_A4", "A4_quiet_before_expiry"], "T_life=H+T_q+1=3+T_q; no ceiling, output-before-expiry conversion, or ordinal is asserted.", n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A6", "N4-A7"]),
            row("C4.TERMINAL", "C4", "A4", "QUIET", "Reviewed quiet terminal transition clears state to (0,0); no later first-lobe output is created.", exact, ["A4_quiet", "A4_up_crossing"], "One upward root then one downward q re-arm root; quiet at r=q commits terminal clear."),
        ]
    )

    for instance in fixture_by_id["C5"]["fresh_instances"]:
        name = instance["instance"]
        hold = Fraction(instance["hold_TU"])
        prefix = f"C5.{name}"
        rows.extend(
            [
                row(f"{prefix}.HOLD", "C5", name, "STORE/HOLD", f"During exact HOLD={instance['hold_TU']} TU, X=(4,0) and active time does not advance.", exact, ["held"], "R=0 identity flow; p=+1,A=4."),
                row(f"{prefix}.MATCHED_FLOW_STATE", "C5", name, "ACTIVE_FLOW", "After release, the full state at each exact active time is the same A=4 semigroup as C4, independent of the frozen HOLD duration.", exact, ["flow", "C5_hold_shift"], "X(s)=4*exp(-s)*(cos(s),sin(s)); absolute event-time shift by HOLD does not change active-time state."),
                row(f"{prefix}.UP_ROOT", "C5", name, "CROSSING", f"Active-time upward-root offset equals C4; absolute mathematical time is t_store+{fraction_text(hold)}+s_up.", numeric, ["roots_A4.up", "C5_hold_shift"], "HOLD contributes zero active time; exact absolute shift uses the fixture-frozen rational HOLD only.", n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A5", "N4-A7"]),
                row(f"{prefix}.REARM", "C5", name, "REARM", f"Active-time re-arm offset equals C4; absolute shift is exact HOLD={instance['hold_TU']} TU.", numeric, ["roots_A4.rearm", "C5_hold_shift"], "Same unique post-peak root; t_rearm=t_store+H+s_rearm."),
                row(f"{prefix}.QUIET_TERMINAL", "C5", name, "QUIET/TERMINAL", f"Quiet active-time root equals C4; lifecycle terminal state is (0,0), with real-time shift by HOLD={instance['hold_TU']} TU.", numeric, ["quiet_times.A4", "T_life_A4", "C5_hold_shift"], "s_quiet=ln(4/q); HOLD adds exactly H to absolute event time; no binary64 bit identity claim.", n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A6", "N4-A7"]),
                row(f"{prefix}.EXPIRY", "C5", name, "EXPIRY", "The absolute expiry remains fixed from STORE and uses the same exact T_life for all HOLD variants.", numeric, ["T_life_A4", "C5_hold_shift"], "t_exp=t_store+T_life; HOLD shifts release-derived roots, not the STORE-origin expiry."),
            ]
        )

    rows.extend(
        [
            row("C6.INITIAL", "C6", "A4", "INITIAL", "Independent oracle starts from X=(4,0),R=1 and remains in the exact invariant disk.", exact, ["radius", "flow"], "C6 recomputes the analytic semigroup independently of candidate propagation/lifecycle code."),
            row("C6.UP_ROOT", "C6", "A4", "ROOT_UP", "Independent fresh root solve certifies the unique upward crossing; interval overlaps C4 independently.", numeric, ["roots_C6_independent.up", "roots_A4.up"], "Separate C6 bisection with same mathematical function and no candidate-runtime code.", n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A5", "N4-A7"]),
            row("C6.UP_STATE", "C6", "A4", "ROOT_UP_STATE", "Independent root state has p*y=theta and certified x enclosure.", numeric, ["roots_C6_independent.up", "root_state_enclosures_C6_independent.up"], "X(s*)=(4 exp(-s*)cos(s*),theta) from independently bounded root."),
            row("C6.REARM_ROOT", "C6", "A4", "ROOT_REARM", "Independent fresh root solve certifies one downward q re-arm; enclosure overlaps C4.", numeric, ["roots_C6_independent.rearm", "roots_A4.rearm"], "Strictly decreasing branch after the first peak."),
            row("C6.REARM_STATE", "C6", "A4", "ROOT_REARM_STATE", "Independent re-arm state has p*y=q exactly and a full-state x enclosure.", numeric, ["roots_C6_independent.rearm", "root_state_enclosures_C6_independent.rearm"], "Independent root bracket and semigroup state at the downward q crossing."),
            row("C6.QUIET", "C6", "A4", "QUIET", "Independent oracle quiet time is ln(4/q), the first inward radius-q root.", numeric, ["quiet_times_C6_independent", "T_q_A4"], "Independently re-evaluated logarithmic radius root; no candidate timer/lifecycle implementation used."),
            row("C6.QUIET_STATE", "C6", "A4", "QUIET_STATE", "Independent quiet boundary state is enclosed at radius q before terminal clear.", numeric, ["quiet_boundary_states.C6", "quiet_times_C6_independent"], "X=q(cos(s_q),sin(s_q)) with s_q in (pi/2,pi); afterward terminal clear is (0,0)."),
            row("C6.TERMINAL", "C6", "A4", "TERMINAL", "Independent reference terminal classification is QUIET at s=ln(4/q), followed by clear.", exact, ["A4_quiet", "flow"], "r decreases strictly as exp(-s); q<4 and terminal condition is exact."),
        ]
    )

    c7 = c7_case_map(fixtures)
    c7_rows: dict[str, list[tuple[str, str, str, list[str], str]]] = {
        "C7.DUPLICATE_RECALL": [
            ("ZERO_ACTIVE", "Same-time duplicate RECALL has zero active duration; state remains (4,0).", exact, ["held"], "No elapsed time between equal input times."),
            ("CROSSING_SOURCE", "Any post-RECALL flow-boundary source is the same unique A=4 upward root.", numeric, ["roots_A4.up"], "C4 independent first-lobe mathematical source."),
            ("EXPIRY_SOURCE", "STORE-origin expiry duration is the exact finite T_life.", numeric, ["T_life_A4"], "T_life=3+ln(4/q); expiry remains tied to original STORE."),
        ],
        "C7.ALTERNATING_RECALL": [
            ("PAUSE_BELOW_ROOT", "Frozen pause condition 0<s_pause<s_up implies no crossing before RECALL_OFF.", numeric, ["roots_A4.up"], "First-lobe output ordinate is strictly increasing; every strict pre-root active time remains below theta."),
            ("UP_ROOT", "Resumed active-time trajectory has the same unique A=4 upward root.", numeric, ["roots_A4.up"], "Exact semigroup depends on accumulated active time, not held wall time."),
            ("REARM_ROOT", "Resumed trajectory has the same unique downward re-arm root.", numeric, ["roots_A4.rearm"], "Exact active-time root reused as a mathematical theorem; not a timer schedule."),
            ("QUIET_ROOT", "Resumed trajectory quiet root is ln(4/q), strictly before expiry under frozen release-by-H condition.", numeric, ["quiet_times.A4", "T_life_A4"], "T_life=H+T_q+1 and release starts by t_store+H."),
            ("EXPIRY_INVALIDATION", "Quiet precedes STORE-origin expiry by at least one TU for release no later than H.", exact, ["T_life_A4"], "Expiry absolute offset is H+T_q+1; quiet offset is release_start-t_store+T_q with release_start<=H."),
        ],
        "C7.RESET_BEFORE_COMMIT": [
            ("RESET_PRE_ROOT", "Frozen RESET time is after release begins but strictly before the up root, so the mathematical surface has not crossed.", numeric, ["roots_A4.up"], "First-lobe strict increase and the fixture's 0<s_reset<s_up relation."),
            ("NO_OUTPUT", "No output is mathematically committed before the certified upward root.", exact, ["A4_up_crossing"], "Output eligibility requires an upward h=0 crossing."),
        ],
        "C7.RESET_AFTER_COMMIT": [
            ("OUTPUT_ROOT", "The inherited C4 root is a unique upward root; output payload is exact +1 and is persistent by contract.", numeric, ["roots_A4.up", "root_state_enclosures_A4.up"], "Root commit occurs at mathematical t_root; processing/reset conversion is outside W."),
            ("REARM_SOURCE", "Reset is constrained before re-arm; the only mathematical re-arm source is the unique C4 q root.", numeric, ["roots_A4.rearm"], "No additional/replacement root or timer is introduced."),
        ],
        "C7.STALE_TIMER": [
            ("ORIGINAL_TIMER_SOURCE", "Stale crossing timer names the original unique A=4 upward-root source.", numeric, ["roots_A4.up"], "Cancellation/stale processing do not create a new mathematical root."),
            ("PAUSE_BELOW_ROOT", "Frozen positive pause below s_up remains below the output section.", numeric, ["roots_A4.up"], "Monotone rising branch before the root."),
        ],
        "C7.REARM_BEFORE_QUIET": [
            ("REARM_LT_QUIET", "Exact A=4 downward q root is strictly before first inward radius-q quiet root.", numeric, ["roots_A4.rearm", "quiet_times.A4", "A4_rearm_before_quiet"], "At s_quiet, p*y=q*sin(s_quiet)<q; post-peak ordinate decreases strictly."),
        ],
        "C7.EXPIRY_COALESCENCE_VALID": [
            ("HELD_STATE", "The fresh held A=4 state stays exactly (4,0) through mathematical expiry.", exact, ["held"], "R=0 identity flow."),
            ("EXPIRY_SOURCE", "Expiry mathematical source is t_store+T_life with T_life=3+ln(4/q).", numeric, ["T_life_A4"], "Distinct external time/shared ceiling and precedence are explicitly not evaluated."),
        ],
        "C7.EXPIRY_COALESCENCE_INVALID": [
            ("HELD_STATE", "The fresh held A=4 state stays exactly (4,0) through mathematical expiry.", exact, ["held"], "R=0 identity flow."),
            ("EXPIRY_SOURCE", "Expiry mathematical source is t_store+T_life with T_life=3+ln(4/q).", numeric, ["T_life_A4"], "Distinct external time/shared ceiling and precedence are explicitly not evaluated."),
        ],
        "C7.TIMESTAMP_INVALID": [],
        "C7.OVERFLOW_17": [
            ("OUTPUT_ROOT", "The accepted A=4 release has the same unique upward root as C4.", numeric, ["roots_A4.up"], "Overflow disposition does not change the previously committed root."),
            ("OUTPUT_TO_REARM_GAP", "The mathematical re-arm active-time root is strictly later than the upward root.", numeric, ["roots_A4.up", "roots_A4.rearm"], "Distinct roots on opposite sides of the first-lobe maximum; represented output/input/re-arm ordering is T/E."),
            ("QUIET_LIFETIME", "If release continues, quiet lies strictly before the STORE-origin expiry under the frozen start-by-H condition.", numeric, ["quiet_times.A4", "T_life_A4"], "Exact H+T_q+1 lifetime; attempt-17 time/order is outside W."),
        ],
        "C7.POST_ABORT_INGRESS": [
            ("NO_MATHEMATICAL_TRANSITION", "Closed ingress is rejected before component addressing; the mathematical state receives no new input.", exact, ["flow"], "Frozen post-abort ingress boundary; no continuous flow, root, or state update is part of this input."),
        ],
        "C7.OUTPUT_EXPIRY_COALESCENCE": [
            ("UP_ROOT_SOURCE", "Late release still references the unique A=4 upward root.", numeric, ["roots_A4.up"], "The mathematical root is separated from its eventual represented output time."),
            ("LIFETIME_SOURCE", "Expiry remains the exact STORE-origin t_store+T_life boundary.", numeric, ["T_life_A4"], "No assertion that a binary64 ceiling coalesces is made by W."),
        ],
        "C7.NEAR_CLOCK_LIMIT": [
            ("LIFETIME_SOURCE", "Both neighboring STORE-origin tests use the same finite exact T_life duration.", numeric, ["T_life_A4"], "The last in-domain binary64 STORE origin and successor remain T/E boundary calculations."),
        ],
        "C7.POSITIVE_SUB_ULP": [
            ("Q_ABOVE_CLASS", "The frozen least binary64 A>q is strictly above q; its logarithmic quiet delay is positive.", numeric, ["q_neighbor_inputs", "quiet_times.Q_ABOVE"], "Exact binary64 dyadic import and outward log interval; no event-time ULP or ceiling computed."),
            ("QUIET_BEFORE_EXPIRY", "The positive q-neighbor quiet delay is strictly less than the A=4 expiry-duration source.", numeric, ["quiet_times.Q_ABOVE", "T_life_A4"], "Directed intervals prove 0<ln(A/q)<T_life; strict-future represented mapping is reserved to T/E."),
        ],
    }
    if set(c7_rows) != set(c7):
        raise RuntimeError(
            f"C7 W row registry must reconcile exactly with frozen subcases; "
            f"unmapped={sorted(set(c7)-set(c7_rows))}, extra={sorted(set(c7_rows)-set(c7))}"
        )
    for case_id, assertions in c7_rows.items():
        case = c7[case_id]
        instances = case.get("instances")
        if isinstance(instances, list) and instances:
            for instance in instances:
                for suffix, claim, evidence_class, refs, proof in c7_rows[case_id]:
                    if case_id == "C7.TIMESTAMP_INVALID":
                        # Timestamp-invalid state assertions are covered separately below.
                        break
                if case_id == "C7.TIMESTAMP_INVALID":
                    rows.extend(
                        [
                            row(
                                f"{case_id}.{instance['id']}.STORE_STATE",
                                "C7",
                                f"{case_id}.{instance['id']}",
                                instance["events"][0],
                                "The accepted A=4 STORE leaves the held mathematical state exactly (4,0).",
                                exact,
                                ["held"],
                                "R=0 identity flow before invalid envelope handling.",
                            ),
                            row(
                                f"{case_id}.{instance['id']}.NO_SETTLEMENT",
                                "C7",
                                f"{case_id}.{instance['id']}",
                                instance["events"][-1],
                                "Invalid timestamp disposition causes no mathematical settlement/state transition.",
                                exact,
                                ["flow"],
                                "Timestamp-invalid packets are rejected before settlement by the frozen design contract.",
                            ),
                        ]
                    )
            continue
        for suffix, claim, evidence_class, refs, proof in assertions:
            rows.append(
                row(
                    f"{case_id}.{suffix}",
                    "C7",
                    case_id,
                    suffix,
                    claim,
                    evidence_class,
                    refs,
                    proof,
                    n4_a=["N4-A1", "N4-A2", "N4-A3", "N4-A4", "N4-A5", "N4-A6", "N4-A7"],
                )
            )
    return rows


def deferred_time_work(fixtures: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for fixture in fixtures["fixtures"]:
        if fixture["id"] in ("C0",):
            continue
        rows.append(
            {
                "row_id": f"{fixture['id']}.TIME_AND_ORDINAL_MATERIALIZATION",
                "fixture": fixture["id"],
                "owner": "T/E (not executed by authorization)",
                "status": "BLOCKED",
                "reason": "Binary64 event-time conversions, strict-future checks, schedule timestamps, and final ordinals are reserved to T/E; Lane W does not assign or materialize them.",
                "exact_values": None,
                "source": "published fixture inventory and N4-B1..N4-B7",
            }
        )
    rows.append(
        {
            "row_id": "C7.ALL_FROZEN_SCHEDULE_IDENTITIES",
            "fixture": "C7",
            "owner": "T/E (not executed by authorization)",
            "status": "BLOCKED",
            "reason": "All frozen C7 event times, binary64 ceilings, strict-future relations, schedule feasibility, and destination ordinals remain unmaterialized; only W mathematical source claims are certified.",
            "exact_values": None,
            "source": "fixtures.json C7 case event identities and N4-B1..N4-B7",
        }
    )
    return rows


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_certificate() -> dict[str, Any]:
    fixtures = json.loads(FIXTURE_JSON.read_text(encoding="utf-8"))
    evidence, rows = make_evidence(fixtures)
    fixture_by_id = {fixture["id"]: fixture for fixture in fixtures["fixtures"]}
    row_counts_by_fixture = {
        fixture_id: sum(item["fixture"] == fixture_id for item in rows)
        for fixture_id in [f"C{i}" for i in range(8)]
    }
    c2_case_rows = sum(
        1
        if not case.get("instance_polarities")
        else len(case["instance_polarities"])
        for case in fixture_by_id["C2"]["cases"]
    )
    coverage_plan = {
        "C0": {"source": "C0 checkpoint inventory", "expected_rows": len(fixture_by_id["C0"]["checkpoints"])},
        "C1": {"source": "C1 checkpoint inventory", "expected_rows": len(fixture_by_id["C1"]["checkpoints"])},
        "C2": {
            "source": "all seven frozen C2 cases expanded by polarity + eight A1 P/N checkpoints + exact strict-margin proof",
            "case_polarity_rows": c2_case_rows,
            "a1_checkpoint_rows": len(fixture_by_id["C2"]["A1_checkpoints"]),
            "strict_margin_rows": 1,
            "expected_rows": c2_case_rows + len(fixture_by_id["C2"]["A1_checkpoints"]) + 1,
        },
        "C3": {
            "source": "STORE state + each published HOLD duration + expiry mathematical source",
            "expected_rows": 1 + len(fixture_by_id["C3"]["hold_durations_TU"]) + 1,
        },
        "C4": {"source": "explicit Lane-W A4 state/root/re-arm/quiet/expiry/terminal row obligations", "expected_rows": len(C4_REQUIRED_ROW_IDS), "row_ids": C4_REQUIRED_ROW_IDS},
        "C5": {
            "source": "each of three frozen HOLD instances: HOLD, matched state, up root, re-arm, quiet terminal, expiry",
            "per_instance_rows": 6,
            "expected_rows": len(fixture_by_id["C5"]["fresh_instances"]) * 6,
        },
        "C6": {"source": "explicit independently solved ungated state/root/re-arm/quiet/terminal obligations", "expected_rows": len(C6_REQUIRED_ROW_IDS), "row_ids": C6_REQUIRED_ROW_IDS},
        "C7": {
            "source": "all fourteen frozen subcases, including four timestamp-invalid variants, by explicit Lane-W row map",
            "case_row_plan": C7_CASE_ROW_PLAN,
            "expected_rows": sum(C7_CASE_ROW_PLAN.values()),
        },
    }
    planned_total = sum(item["expected_rows"] for item in coverage_plan.values())
    matrix = {
        "format": "luna63c-stage-a-lane-w-coverage",
        "revision": 1,
        "disposition": "W COMPLETE — T/E conversion and ordinal work remains blocked and unrun",
        "scope": "Stage-A Lane W mathematical witnesses/N1 only; no C0-C7 experiment or Stage-B candidate comparison.",
        "source_inventory": {
            "fixture_ids": [fixture["id"] for fixture in fixtures["fixtures"]],
            "c2_case_count": len(next(f for f in fixtures["fixtures"] if f["id"] == "C2")["cases"]),
            "c2_a1_polarity_checkpoint_count": len(next(f for f in fixtures["fixtures"] if f["id"] == "C2")["A1_checkpoints"]),
            "c3_hold_duration_count": len(next(f for f in fixtures["fixtures"] if f["id"] == "C3")["hold_durations_TU"]),
            "c5_hold_instance_count": len(next(f for f in fixtures["fixtures"] if f["id"] == "C5")["fresh_instances"]),
            "c7_subcase_count": len(next(f for f in fixtures["fixtures"] if f["id"] == "C7")["cases"]),
            "c7_timestamp_invalid_instance_count": sum(
                len(case.get("instances", []))
                for case in next(f for f in fixtures["fixtures"] if f["id"] == "C7")["cases"]
                if case["id"] == "C7.TIMESTAMP_INVALID"
            ),
        },
        "reconciliation": {
            "row_count": len(rows),
            "certified_count": sum(item["status"] == "CERTIFIED" for item in rows),
            "blocked_count": sum(item["status"] == "BLOCKED" for item in rows),
            "w_required_count": sum(item["owner"] == "W" for item in rows),
            "t_e_deferred_count": len(deferred_time_work(fixtures)),
            "row_counts_by_fixture": row_counts_by_fixture,
            "coverage_plan": coverage_plan,
            "planned_total": planned_total,
            "c2_a1_rows_expected": 8,
            "c2_a1_rows_present": sum(item["fixture"] == "C2" and item["checkpoint"].startswith("C2.A1.") for item in rows),
            "c7_subcase_coverage": [
                case["id"]
                for case in next(f for f in fixtures["fixtures"] if f["id"] == "C7")["cases"]
            ],
            "c7_row_subcase_coverage": sorted(
                {item["subcase"] for item in rows if item["fixture"] == "C7"}
            ),
        },
        "rows": rows,
        "evidence": evidence,
        "deferred_not_w_lane": deferred_time_work(fixtures),
        "limitations": [
            "No candidate implementation was evaluated; the strict A=1 theta/4 rule is recorded and its exact ideal mathematical margin is proved, not tested against Stage B.",
            "No binary64 event timestamp, ceiling, schedule, ULP comparison, event ordinal, or timer schedule was materialized.",
            "The W artifact does not close N3, N4-B, Lane T, Lane E, Lane S/N5, Stage B, or the whole certificate.",
        ],
    }
    validate_certificate(matrix)
    return matrix


def validate_certificate(matrix: dict[str, Any]) -> None:
    rows = matrix["rows"]
    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise AssertionError("coverage row IDs are not unique")
    if any(item["status"] not in ("CERTIFIED", "BLOCKED") for item in rows):
        raise AssertionError("coverage rows require CERTIFIED or BLOCKED status")
    if any(item["owner"] != "W" for item in rows):
        raise AssertionError("non-W work leaked into W mathematical matrix")
    if any(not item["proof_refs"] or not item["defining_function_or_identity"] for item in rows):
        raise AssertionError("coverage row is missing proof/source evidence")
    if matrix["reconciliation"]["c2_a1_rows_present"] != 8:
        raise AssertionError("C2 A=1 must include P/N at all four frozen checkpoints")
    if len(matrix["reconciliation"]["c7_subcase_coverage"]) != 14:
        raise AssertionError("C7 must reconcile to all fourteen published subcases")
    c7_row_subcases = matrix["reconciliation"]["c7_row_subcase_coverage"]
    if any(
        not any(
            actual == required or actual.startswith(required + ".")
            for actual in c7_row_subcases
        )
        for required in matrix["reconciliation"]["c7_subcase_coverage"]
    ):
        missing_c7 = [
            required
            for required in matrix["reconciliation"]["c7_subcase_coverage"]
            if not any(
                actual == required or actual.startswith(required + ".")
                for actual in c7_row_subcases
            )
        ]
        raise AssertionError(
            f"frozen C7 subcases have no W mathematical-source row: {missing_c7}"
        )
    if matrix["reconciliation"]["row_count"] != len(rows):
        raise AssertionError("frozen-source row count does not reconcile")
    if matrix["reconciliation"]["row_count"] != matrix["reconciliation"]["planned_total"]:
        raise AssertionError("total W row count differs from frozen-source coverage plan")
    if matrix["reconciliation"]["row_counts_by_fixture"] != {
        "C0": 1,
        "C1": 2,
        "C2": 22,
        "C3": 5,
        "C4": 8,
        "C5": 18,
        "C6": 8,
        "C7": 36,
    }:
        raise AssertionError("fixture row counts do not reconcile to the frozen Lane-W plan")
    actual_c7_counts = {
        case_id: sum(
            item["fixture"] == "C7" and item["row_id"].startswith(case_id + ".")
            for item in rows
        )
        for case_id in C7_CASE_ROW_PLAN
    }
    if actual_c7_counts != C7_CASE_ROW_PLAN:
        raise AssertionError(f"C7 W case counts differ from plan: {actual_c7_counts}")
    actual_ids = {item["row_id"] for item in rows}
    if not set(C4_REQUIRED_ROW_IDS).issubset(actual_ids) or not set(C6_REQUIRED_ROW_IDS).issubset(actual_ids):
        raise AssertionError("C4/C6 required root/state/terminal rows are missing")
    if matrix["reconciliation"]["blocked_count"] != 0:
        raise AssertionError("a W-required row is blocked")
    if not matrix["evidence"]["environment"]["profile_match"]:
        raise AssertionError("actual native MPFR/GMP versions do not match the governed profile")
    if any(root["bisections_total"] > ROOT_BISECTIONS_MAX for root in (
        matrix["evidence"]["roots_A4"]["up"],
        matrix["evidence"]["roots_A4"]["rearm"],
        matrix["evidence"]["roots_C6_independent"]["up"],
        matrix["evidence"]["roots_C6_independent"]["rearm"],
    )):
        raise AssertionError("root bisection cap exceeded")


def make_manifest(matrix: dict[str, Any], raw: bytes) -> dict[str, Any]:
    return {
        "format": "luna63c-stage-a-lane-w-manifest",
        "revision": 1,
        "disposition": matrix["disposition"],
        "source_inventory": matrix["source_inventory"],
        "row_count": matrix["reconciliation"]["row_count"],
        "certified_count": matrix["reconciliation"]["certified_count"],
        "blocked_count": matrix["reconciliation"]["blocked_count"],
        "w_required_count": matrix["reconciliation"]["w_required_count"],
        "t_e_deferred_blocked_count": matrix["reconciliation"]["t_e_deferred_count"],
        "matrix_path": "experiments/luna63c/certificate/lane-w/coverage_matrix.json",
        "matrix_sha256": hashlib.sha256(raw).hexdigest().upper(),
        "certificate_program": "experiments/luna63c/certificate/lane-w/certificate.py",
        "certificate_program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper(),
        "fixture_raw_hashes": matrix["evidence"]["source_pins"],
        "actual_environment": matrix["evidence"]["environment"],
        "transcendental_method": "MPFR directed operations via gmpy2 C binding; host libm not used.",
    }


def write_certificate(matrix: dict[str, Any]) -> dict[str, Any]:
    matrix_path = LANE_DIR / "coverage_matrix.json"
    raw = canonical_json(matrix)
    matrix_path.write_bytes(raw)
    manifest = make_manifest(matrix, raw)
    manifest_path = LANE_DIR / "manifest.json"
    manifest_path.write_bytes(canonical_json(manifest))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic matrix and manifest")
    parser.add_argument("--check", action="store_true", help="verify checked-in matrix and manifest")
    args = parser.parse_args()
    matrix = build_certificate()
    if args.write:
        manifest = write_certificate(matrix)
        print(
            f"W rows={matrix['reconciliation']['row_count']} "
            f"certified={matrix['reconciliation']['certified_count']} "
            f"blocked={matrix['reconciliation']['blocked_count']} "
            f"matrix_sha256={manifest['matrix_sha256']}"
        )
    elif args.check:
        matrix_path = LANE_DIR / "coverage_matrix.json"
        manifest_path = LANE_DIR / "manifest.json"
        expected = canonical_json(matrix)
        if not matrix_path.is_file() or matrix_path.read_bytes() != expected:
            raise SystemExit("coverage_matrix.json differs from deterministic regeneration")
        expected_manifest = canonical_json(make_manifest(matrix, expected))
        if not manifest_path.is_file() or manifest_path.read_bytes() != expected_manifest:
            raise SystemExit("manifest differs from deterministic regeneration/hash inputs")
        print("Lane-W certificate regeneration and manifest checks passed.")
    else:
        print(json.dumps(matrix["reconciliation"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
