"""Fail-closed Windows supervisor boundary for the Luna-65 Phase 2A fixture.

This source implements the reviewed policy constants and Job Object
configuration/accounting primitives. It is not a qualified supervisor:
admission remains blocked until the unresolved containment, observer,
artifact-path, identity, and termination gates are independently closed.
"""

from __future__ import annotations

import ctypes
import enum
import os
import sys
import time
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Final


ROOT: Final = Path(__file__).resolve().parents[1]
PYTHON: Final = ROOT / ".venv" / "Scripts" / "python.exe"
FIXTURE: Final = Path("tests") / "test_luna65_capacity_direct.py"
EXPECTED_ARGUMENTS: Final = (
    "-m",
    "pytest",
    "-q",
    "-x",
    str(FIXTURE).replace("/", "\\"),
)
EXPECTED_COMMAND: Final = (
    str(PYTHON),
    *EXPECTED_ARGUMENTS,
)
EXPECTED_WORKING_DIRECTORY: Final = str(ROOT)
ALLOWED_ENVIRONMENT_NAMES: Final = frozenset(
    {
        "SystemRoot",
        "WINDIR",
        "SystemDrive",
        "PATH",
        "TEMP",
        "TMP",
        "PYTHONHASHSEED",
        "PYTHONDONTWRITEBYTECODE",
        "PYTHONNOUSERSITE",
        "PYTHONSAFEPATH",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD",
    }
)
FIXED_ENVIRONMENT_VALUES: Final = {
    "PYTHONHASHSEED": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONNOUSERSITE": "1",
    "PYTHONSAFEPATH": "1",
    "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
}

CPU_BUDGET_100NS: Final = 1_200_000_000
CPU_BUDGET_SECONDS: Final = 120
WALL_BUDGET_SECONDS: Final = 120
WALL_STOP_SECONDS: Final = 115
WATCHDOG_HEARTBEAT_MILLISECONDS: Final = 100
MONITOR_INTERVAL_MILLISECONDS: Final = 10
MAX_MONITOR_GAP_MILLISECONDS: Final = 100
JOB_MEMORY_LIMIT_BYTES: Final = 268_435_456
RETAINED_ARTIFACT_LIMIT_BYTES: Final = 1_048_576

JOB_OBJECT_LIMIT_JOB_MEMORY: Final = 0x00000200
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE: Final = 0x00002000
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION: Final = 9
JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION: Final = 1
CREATE_SUSPENDED: Final = 0x00000004
CREATE_UNICODE_ENVIRONMENT: Final = 0x00000400
EXTENDED_STARTUPINFO_PRESENT: Final = 0x00080000
WAIT_OBJECT_0: Final = 0
WAIT_TIMEOUT: Final = 258
INFINITE: Final = 0xFFFFFFFF

UNQUALIFIED_GATES: Final = (
    "restricted-token and deny-write ACL completeness",
    "hard retained-artifact boundary for all workload writes",
    "independent process-tree observer and event-loss signal",
    "Q03 escaped-child recovery and descendant cessation",
    "job commit limit equivalence to aggregate private commit",
    "watchdog heartbeat, crash recovery, and last-handle-close behavior",
    "post-budget termination observation limit",
)


class Failure(enum.StrEnum):
    CPU_BUDGET_EXCEEDED = "CPU_BUDGET_EXCEEDED"
    WALL_BUDGET_EXCEEDED = "WALL_BUDGET_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    ARTIFACT_LIMIT_EXCEEDED = "ARTIFACT_LIMIT_EXCEEDED"
    CONTROLLER_FAILURE = "CONTROLLER_FAILURE"
    PROCESS_CONTAINMENT_FAILURE = "PROCESS_CONTAINMENT_FAILURE"
    TERMINATION_UNCONFIRMED = "TERMINATION_UNCONFIRMED"
    EVIDENCE_INCOMPLETE = "EVIDENCE_INCOMPLETE"
    RESOURCE_MEASUREMENT_INCONCLUSIVE = "RESOURCE_MEASUREMENT_INCONCLUSIVE"


class AdmissionRejected(RuntimeError):
    """Raised when a Phase 2A workload cannot be admitted safely."""


class ControllerFailure(RuntimeError):
    """Raised when a required Windows observation or control operation fails."""


class _IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_uint64),
        ("WriteOperationCount", ctypes.c_uint64),
        ("OtherOperationCount", ctypes.c_uint64),
        ("ReadTransferCount", ctypes.c_uint64),
        ("WriteTransferCount", ctypes.c_uint64),
        ("OtherTransferCount", ctypes.c_uint64),
    ]


class _JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class _JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", _IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class _JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", ctypes.c_int64),
        ("TotalKernelTime", ctypes.c_int64),
        ("ThisPeriodTotalUserTime", ctypes.c_int64),
        ("ThisPeriodTotalKernelTime", ctypes.c_int64),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    ]


def _windows_kernel32() -> ctypes.WinDLL:
    if os.name != "nt":
        raise AdmissionRejected("Phase 2A supervisor is Windows-only")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    )
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.QueryPerformanceCounter.argtypes = (ctypes.POINTER(ctypes.c_int64),)
    kernel32.QueryPerformanceCounter.restype = wintypes.BOOL
    kernel32.QueryPerformanceFrequency.argtypes = (ctypes.POINTER(ctypes.c_int64),)
    kernel32.QueryPerformanceFrequency.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


def _last_error(operation: str) -> ControllerFailure:
    error = ctypes.get_last_error()
    return ControllerFailure(f"{operation} failed with Win32 error {error}")


def _qpc(kernel32: ctypes.WinDLL) -> int:
    value = ctypes.c_int64()
    if not kernel32.QueryPerformanceCounter(ctypes.byref(value)):
        raise _last_error("QueryPerformanceCounter")
    return value.value


def _qpc_frequency(kernel32: ctypes.WinDLL) -> int:
    value = ctypes.c_int64()
    if not kernel32.QueryPerformanceFrequency(ctypes.byref(value)):
        raise _last_error("QueryPerformanceFrequency")
    if value.value <= 0:
        raise ControllerFailure("QueryPerformanceFrequency returned a nonpositive value")
    return value.value


@dataclass(frozen=True)
class AccountingSample:
    qpc: int
    total_user_100ns: int
    total_kernel_100ns: int
    total_cpu_100ns: int
    active_processes: int

    @property
    def total_cpu_seconds(self) -> float:
        return self.total_cpu_100ns / 10_000_000


@dataclass(frozen=True)
class TerminationObservation:
    requested: bool
    request_qpc: int | None
    request_error: int | None
    job_signaled: bool
    active_processes: int | None
    observation_qpc: int


class WindowsJob:
    """Configured Job Object with checked read-back and explicit observations."""

    def __init__(self) -> None:
        self._kernel32 = _windows_kernel32()
        self._frequency = _qpc_frequency(self._kernel32)
        self.handle = self._kernel32.CreateJobObjectW(None, None)
        if not self.handle:
            raise _last_error("CreateJobObjectW")
        self._closed = False

    @property
    def qpc_frequency(self) -> int:
        return self._frequency

    def configure_and_verify(self) -> None:
        requested = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        requested.BasicLimitInformation.LimitFlags = (
            JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        requested.JobMemoryLimit = JOB_MEMORY_LIMIT_BYTES
        if not self._kernel32.SetInformationJobObject(
            self.handle,
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(requested),
            ctypes.sizeof(requested),
        ):
            raise _last_error("SetInformationJobObject")

        observed = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        returned = wintypes.DWORD()
        if not self._kernel32.QueryInformationJobObject(
            self.handle,
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(observed),
            ctypes.sizeof(observed),
            ctypes.byref(returned),
        ):
            raise _last_error("QueryInformationJobObject(extended limits)")
        expected_flags = JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if (
            observed.BasicLimitInformation.LimitFlags != expected_flags
            or observed.JobMemoryLimit != JOB_MEMORY_LIMIT_BYTES
        ):
            raise ControllerFailure(
                "effective Job Object limits do not exactly match the approved policy"
            )

    def accounting(self) -> AccountingSample:
        observed = _JOBOBJECT_BASIC_ACCOUNTING_INFORMATION()
        returned = wintypes.DWORD()
        if not self._kernel32.QueryInformationJobObject(
            self.handle,
            JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION,
            ctypes.byref(observed),
            ctypes.sizeof(observed),
            ctypes.byref(returned),
        ):
            raise _last_error("QueryInformationJobObject(accounting)")
        if observed.TotalUserTime < 0 or observed.TotalKernelTime < 0:
            raise ControllerFailure("Job Object CPU accounting regressed below zero")
        return AccountingSample(
            qpc=_qpc(self._kernel32),
            total_user_100ns=observed.TotalUserTime,
            total_kernel_100ns=observed.TotalKernelTime,
            total_cpu_100ns=observed.TotalUserTime + observed.TotalKernelTime,
            active_processes=observed.ActiveProcesses,
        )

    def terminate(self, exit_code: int = 1) -> tuple[int, int | None]:
        request_qpc = _qpc(self._kernel32)
        if self._kernel32.TerminateJobObject(self.handle, exit_code):
            return request_qpc, None
        return request_qpc, ctypes.get_last_error()

    def observe_termination(self, timeout_ms: int = 0) -> TerminationObservation:
        result = self._kernel32.WaitForSingleObject(self.handle, timeout_ms)
        if result == WAIT_TIMEOUT:
            signaled = False
        elif result == WAIT_OBJECT_0:
            signaled = True
        else:
            raise _last_error("WaitForSingleObject(job)")
        sample = self.accounting()
        return TerminationObservation(
            requested=False,
            request_qpc=None,
            request_error=None,
            job_signaled=signaled,
            active_processes=sample.active_processes,
            observation_qpc=sample.qpc,
        )

    def close(self) -> None:
        if self._closed:
            return
        if not self._kernel32.CloseHandle(self.handle):
            raise _last_error("CloseHandle(job)")
        self._closed = True

    def __enter__(self) -> WindowsJob:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()


class ResourceMonitor:
    """Monotonic QPC monitor for an already admitted job."""

    def __init__(self, job: WindowsJob, t0_qpc: int) -> None:
        self.job = job
        self.t0_qpc = t0_qpc
        self.frequency = job.qpc_frequency
        self.last_qpc: int | None = None
        self.first_failure: Failure | None = None
        self.failures: list[Failure] = []
        self.samples: list[AccountingSample] = []
        self.termination_observations: list[TerminationObservation] = []
        self.termination_requested = False
        self.deadline_escalated = False
        self.cpu_stop_requested = False

    def _record_failure(self, failure: Failure) -> None:
        if failure not in self.failures:
            self.failures.append(failure)
        if self.first_failure is None:
            self.first_failure = failure

    def sample(self) -> AccountingSample:
        try:
            current = self.job.accounting()
        except ControllerFailure:
            self._record_failure(Failure.RESOURCE_MEASUREMENT_INCONCLUSIVE)
            self._request_termination()
            raise
        elapsed_gap_ms = (
            None
            if self.last_qpc is None
            else (current.qpc - self.last_qpc) * 1000 / self.frequency
        )
        if self.last_qpc is not None and (
            current.qpc <= self.last_qpc
            or elapsed_gap_ms > MAX_MONITOR_GAP_MILLISECONDS
        ):
            self._record_failure(Failure.RESOURCE_MEASUREMENT_INCONCLUSIVE)
            self._request_termination()
            raise ControllerFailure("QPC is nonmonotonic or monitor gap exceeds 100 ms")
        if self.samples and current.total_cpu_100ns < self.samples[-1].total_cpu_100ns:
            self._record_failure(Failure.RESOURCE_MEASUREMENT_INCONCLUSIVE)
            self._request_termination()
            raise ControllerFailure("aggregate CPU counter regressed")
        self.last_qpc = current.qpc
        self.samples.append(current)
        if (
            current.total_cpu_100ns >= CPU_BUDGET_100NS
            and current.active_processes
            and not self.cpu_stop_requested
        ):
            self.cpu_stop_requested = True
            self._request_termination()
        if current.active_processes == 0 and current.total_cpu_100ns > CPU_BUDGET_100NS:
            self._record_failure(Failure.CPU_BUDGET_EXCEEDED)
        elapsed_seconds = (current.qpc - self.t0_qpc) / self.frequency
        if (
            elapsed_seconds >= WALL_STOP_SECONDS
            and current.active_processes
            and not self.termination_requested
        ):
            self._request_termination()
        if (
            elapsed_seconds >= WALL_BUDGET_SECONDS
            and current.active_processes
            and not self.deadline_escalated
        ):
            self._request_termination()
            self.deadline_escalated = True
        if elapsed_seconds > WALL_BUDGET_SECONDS:
            self._record_failure(Failure.WALL_BUDGET_EXCEEDED)
        return current

    def _request_termination(self) -> None:
        request_qpc, error = self.job.terminate()
        self.termination_requested = True
        observation = self.job.observe_termination()
        self.termination_observations.append(
            TerminationObservation(
                requested=True,
                request_qpc=request_qpc,
                request_error=error,
                job_signaled=observation.job_signaled,
                active_processes=observation.active_processes,
                observation_qpc=observation.observation_qpc,
            )
        )
        if error is not None:
            self._record_failure(Failure.CONTROLLER_FAILURE)
        if observation.job_signaled and observation.active_processes != 0:
            self._record_failure(Failure.RESOURCE_MEASUREMENT_INCONCLUSIVE)

    def run_until_inactive(self) -> tuple[AccountingSample, ...]:
        """Observe an admitted job; no post-budget duration is assumed."""
        while True:
            sample = self.sample()
            observation = self.job.observe_termination()
            self.termination_observations.append(observation)
            if observation.job_signaled and observation.active_processes == 0:
                if (observation.observation_qpc - self.t0_qpc) > (
                    WALL_BUDGET_SECONDS * self.frequency
                ):
                    self._record_failure(Failure.WALL_BUDGET_EXCEEDED)
                return tuple(self.samples)
            time.sleep(MONITOR_INTERVAL_MILLISECONDS / 1000)


class RetainedArtifactBudget:
    """Pre-write byte accounting for controller-owned retained artifacts."""

    ALLOCATIONS: Final = {
        "results.jsonl.gz": 786_432,
        "stdout.txt": 32_768,
        "stderr.txt": 32_768,
        "manifest.json": 16_384,
        "resource.json": 16_384,
        "failure.json": 8_192,
        "sha256.json": 8_192,
    }

    def __init__(self) -> None:
        self._retained: dict[str, int] = {}

    @property
    def total_retained_bytes(self) -> int:
        return sum(self._retained.values())

    def account_before_write(self, name: str, byte_count: int) -> None:
        if name not in self.ALLOCATIONS:
            raise AdmissionRejected(f"retained artifact is not allowlisted: {name}")
        if byte_count < 0:
            raise ValueError("byte_count must be nonnegative")
        next_file_size = self._retained.get(name, 0) + byte_count
        next_total = self.total_retained_bytes + byte_count
        if (
            next_file_size > self.ALLOCATIONS[name]
            or next_total > RETAINED_ARTIFACT_LIMIT_BYTES
        ):
            raise ControllerFailure(Failure.ARTIFACT_LIMIT_EXCEEDED.value)
        self._retained[name] = next_file_size


def _validate_exact_invocation(argv: list[str]) -> None:
    if tuple(argv) != EXPECTED_ARGUMENTS:
        raise AdmissionRejected("command differs from the exact Phase 2A allowlist")
    if str(PYTHON) != EXPECTED_COMMAND[0]:
        raise AdmissionRejected("Python executable differs from the pinned command")
    if os.path.normcase(os.path.abspath(os.getcwd())) != os.path.normcase(
        EXPECTED_WORKING_DIRECTORY
    ):
        raise AdmissionRejected("working directory differs from the Phase 2A contract")
    if not PYTHON.is_file():
        raise AdmissionRejected("pinned virtual-environment Python executable is absent")
    if not (ROOT / FIXTURE).is_file():
        raise AdmissionRejected("Phase 2A fixture is absent; workload admission refused")


def build_environment(profile: dict[str, str]) -> dict[str, str]:
    """Validate a complete reviewed allowlist; never inherit ambient variables."""
    if frozenset(profile) != ALLOWED_ENVIRONMENT_NAMES:
        raise AdmissionRejected("environment profile does not exactly match the allowlist")
    for name, expected in FIXED_ENVIRONMENT_VALUES.items():
        if profile[name] != expected:
            raise AdmissionRejected(f"environment override mismatch for {name}")
    for name in ("SystemRoot", "WINDIR", "SystemDrive", "PATH", "TEMP", "TMP"):
        if not profile[name]:
            raise AdmissionRejected(f"required environment value is missing: {name}")
    if os.path.normcase(profile["TEMP"]) != os.path.normcase(profile["TMP"]):
        raise AdmissionRejected("TEMP and TMP must use the same reviewed path")
    return dict(profile)


def _admission_blockers() -> tuple[str, ...]:
    return UNQUALIFIED_GATES


def run_phase2a(argv: list[str]) -> int:
    """Admission entry point; intentionally refuses while any gate is open."""
    _validate_exact_invocation(argv)
    blockers = _admission_blockers()
    if blockers:
        details = "\n".join(f"- {blocker}" for blocker in blockers)
        raise AdmissionRejected(
            "Phase 2A admission is blocked; no workload was started:\n" + details
        )
    raise AdmissionRejected(
        "No reviewed Phase 2A admission profile is configured; no workload was started"
    )


def main() -> int:
    """Never infer a workload command from the caller's arguments."""
    entry_kernel32 = _windows_kernel32()
    t0_qpc = _qpc(entry_kernel32)
    qpc_frequency = _qpc_frequency(entry_kernel32)
    if t0_qpc <= 0 or qpc_frequency <= 0:
        raise ControllerFailure("invalid T0 or QPC frequency")
    if len(sys.argv) < 2 or sys.argv[1] != "--phase2a":
        print(
            "Usage: luna65_phase2a_supervisor.py --phase2a "
            "<exact Phase 2A pytest arguments>",
            file=sys.stderr,
        )
        return 2
    try:
        return run_phase2a(sys.argv[2:])
    except (AdmissionRejected, ControllerFailure) as error:
        print(str(error), file=sys.stderr)
        return 3 if isinstance(error, AdmissionRejected) else 4


if __name__ == "__main__":
    raise SystemExit(main())
