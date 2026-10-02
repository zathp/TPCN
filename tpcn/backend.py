"""Minimal ACP-0003 backend contract declarations.

These declarations describe compatibility; they do not implement or authorize
any backend, approximation, calibration, or hardware mapping.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
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
]
