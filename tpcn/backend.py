"""Minimal ACP-0003 backend contract declarations.

These declarations describe compatibility; they do not implement or authorize
any backend, approximation, calibration, or hardware mapping.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from numbers import Real

from .execution_ir import IR_VERSION


class BackendIdentity(str, Enum):
    GPU_NATIVE = "gpu_native"
    GPU_FPGA_APPROXIMATION = "gpu_fpga_approximation"
    FPGA_NATIVE = "fpga_native"
    GPU_FPAA_APPROXIMATION = "gpu_fpaa_approximation"
    FPAA_NATIVE = "fpaa_native"


class EquivalenceLevel(str, Enum):
    E0_SEMANTIC = "E0"
    E1_NUMERICAL = "E1"
    E2_EVENT = "E2"
    E3_FUNCTIONAL = "E3"
    E4_STATISTICAL = "E4"


class EqualTimePolicy(str, Enum):
    SEQUENTIAL_DETERMINISTIC = "sequential_deterministic"
    COINCIDENT_WINDOW = "coincident_window"


class StatisticalRequirement(str, Enum):
    NONE = "none"
    REQUIRED = "required"


def _optional_tolerance(value: Real | None, name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number or None")
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative, or None")
    return result


@dataclass(frozen=True, slots=True)
class BackendCapabilities:
    identity: BackendIdentity
    supported_ir_version: str = IR_VERSION
    equivalence_levels: frozenset[EquivalenceLevel] = frozenset()
    equal_time_policies: frozenset[EqualTimePolicy] = frozenset({EqualTimePolicy.SEQUENTIAL_DETERMINISTIC})
    implemented: bool = False

    def __post_init__(self) -> None:
        if self.supported_ir_version != IR_VERSION:
            raise ValueError("backend capability must name the supported canonical IR version")
        if not isinstance(self.implemented, bool):
            raise TypeError("implemented must be a boolean")


@dataclass(frozen=True, slots=True)
class ApproximationContract:
    backend: BackendIdentity
    equivalence_levels: frozenset[EquivalenceLevel]
    equal_time_policy: EqualTimePolicy
    notes: str = ""
    supported_ir_version: str = IR_VERSION
    numeric_tolerance: float | None = None
    timing_tolerance: float | None = None
    statistical_requirement: StatisticalRequirement = StatisticalRequirement.NONE
    approximation_boundary: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if self.supported_ir_version != IR_VERSION:
            raise ValueError("approximation contract must name the supported canonical IR version")
        if not isinstance(self.notes, str):
            raise TypeError("notes must be a string")
        levels = frozenset(self.equivalence_levels)
        if not all(isinstance(level, EquivalenceLevel) for level in levels):
            raise TypeError("equivalence_levels must contain EquivalenceLevel values")
        object.__setattr__(self, "equivalence_levels", levels)
        if not isinstance(self.equal_time_policy, EqualTimePolicy):
            raise TypeError("equal_time_policy must be an EqualTimePolicy")
        if not isinstance(self.statistical_requirement, StatisticalRequirement):
            raise TypeError("statistical_requirement must be a StatisticalRequirement")
        object.__setattr__(
            self, "numeric_tolerance", _optional_tolerance(self.numeric_tolerance, "numeric_tolerance")
        )
        object.__setattr__(
            self, "timing_tolerance", _optional_tolerance(self.timing_tolerance, "timing_tolerance")
        )
        boundary = frozenset(self.approximation_boundary)
        if len(boundary) > 16:
            raise ValueError("approximation_boundary cannot contain more than 16 declarations")
        if any(not isinstance(item, str) or not item for item in boundary):
            raise ValueError("approximation_boundary must contain non-empty strings")
        object.__setattr__(self, "approximation_boundary", boundary)


@dataclass(frozen=True, slots=True)
class BackendMappingResult:
    backend: BackendIdentity
    ir_version: str
    mapped: bool
    diagnostics: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BackendDiagnostic:
    category: str
    message: str
    details: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class BackendRealizationState:
    """Opaque future backend formats; never part of canonical execution IR."""
    backend: BackendIdentity
    format_name: str
    scheduling_name: str


@dataclass(frozen=True, slots=True)
class CalibrationState:
    """Future physical calibration state, intentionally separate from IR."""
    backend: BackendIdentity
    characterized: bool = False


__all__ = [
    "ApproximationContract", "BackendCapabilities", "BackendDiagnostic",
    "BackendIdentity", "BackendMappingResult", "BackendRealizationState",
    "CalibrationState", "EqualTimePolicy", "EquivalenceLevel",
    "StatisticalRequirement",
]
