"""Single-attempt RP-2 diagnostic controller. RP-2B permission is separate.

U1-U3 are finite observations, not production containment qualifications.
O alone writes artifacts; this process owns the sole kill-on-close job.
"""

import ctypes as c
from ctypes import wintypes as w
import hashlib
import json
import os
import sys
import time


BASELINE = "f47c48a947e48867c629817fa1031cb93729e440"
ROOT = r"C:\Users\Patrick\Documents\ActiveCode\TPCN"
IMAGE = r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe"
IMAGE_SHA256 = "4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F"
USER = "S-1-5-21-3301679920-2322392626-2066554248-1001"
SOURCE_TOKEN_ACCESS = 0x2008B
QUERY_TOKEN_ACCESS = 0x20008
TOTAL_LIMIT = 1048576
PAYLOAD_LIMIT = 917504
FINAL_RESERVE = 131072
RECORD_LIMIT = 16384
TOKEN_LIMIT = 65536
ENUM_LIMIT = 256
NONCE = "L65-RP2A-SYNTHETIC-V1"
CONTRACTS = {
    "R1": ("F9913AC44C268291988F549A110B2EFCC4777139A2BB8BD0DA407DF020FABEFB",
           "8abb50dfef732da71cee94b1623c61b3f4f8e49e"),
    "candidate": ("4C4420998DE2B87745F8F7565B4CCA5B1CDBE7A619E9DE804D38BC1A5D07D9AE",
                  "97615eda16190c82e977cf71a7ba0439cad84e13"),
    "direct": ("374AB0328B62966EEA7C1E52E9E9E25BB40D973863177DEC4160D077E1C2A476",
               "66356a9328e6fc4dfc28e8b8eb2fdbbfc0cdf15d"),
    "older": ("E573ADA32D746E6766D21420C845FF6AA09B18107F05523A6F1BE8913EE3A313",
              "f61847d0c93f59b189142c5544caf9791e32bbe4"),
}

# These are inspected identities, not a complete or approved startup manifest.
INSPECTED_STARTUP = {
    r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\Lib\site-packages\distutils-precedence.pth":
        "2638CE9E2500E572A5E0DE7FAED6661EB569D1B696FCBA07B0DD223DA5F5D224",
    r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\Lib\site-packages\_distutils_hack\__init__.py":
        "4D27A48545B57DD137AE35376FCF326D2064271084A487960686F8704B94DE4A",
    r"C:\Users\Patrick\AppData\Roaming\Python\Python311\site-packages\pywin32.pth":
        "D902584A2A0A5216CE12C712D1378FE07541D32C383D0CC5ABCD68412144FE4D",
    r"C:\Users\Patrick\AppData\Roaming\Python\Python311\site-packages\win32\lib\pywin32_bootstrap.py":
        "FD31F27BC85A6B9C974670838B6EEFAFB32991BE4A9F840F96A4F5524DF3B3C3",
    r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\Lib\site-packages\py.py":
        "B71675B5D9845BA0814E9E88767F88DAC3B3CC0D3128DA028BD45EDBB523E871",
    r"C:\Users\Patrick\AppData\Roaming\Python\Python311\site-packages\typing_extensions.py":
        "CC67BB3A7D7A4B91D597470F9689F7C22BFA334C98BDAC4399F946E6DAFAB6FD",
    r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python311.dll":
        "A811C7516F531F1515D10743AE78004DD627EBA0DC2D3BC0D2E033B2722043CE",
    r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python3.dll":
        "520169AA6CF49D7EE724D1178DE1BE0E809E4BDCF671E06F3D422A0DD5FD294A",
    r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\vcruntime140.dll":
        "A8F950B4357EC12CFCCDDC9094CCA56A3D5244B95E09EA6E9A746489F2D58736",
    r"C:\Users\Patrick\AppData\Local\Programs\Python\Python311\vcruntime140_1.dll":
        "E4B533A94E02C574780E4B333FCF0889F65ED00D39E32C0FBBDA2116F185873F",
}
BASE = os.path.dirname(IMAGE)
USER_SITE = r"C:\Users\Patrick\AppData\Roaming\Python\Python311\site-packages"
# SHA256 of sorted UTF-8 relative-lowercase-path|length|uppercase-SHA256 LF
# entries, including bytecode. Conservative package closures, not imports.
TREE_MANIFEST = (
    (BASE + r"\Lib", "site-packages", 7008, "D5EA04080A3E9000761B076823B3AAEF0F8BDF009620D4F238B7BA5A3AD5ACD3"),
    (BASE + r"\DLLs", "", 34, "1AD0A0100C7C6267A010467688F81AC41C4CD46EDC324FBFB52FBB51A953504E"),
    (BASE + r"\Lib\site-packages\pytest", "", 4, "4EFE2CB65B5BEABE1AA8D55E80EAB668F7E7DF84B749A5A975910608C61F9241"),
    (BASE + r"\Lib\site-packages\_pytest", "", 143, "A9E1E415449DA37D38A7B2234D8569362B0BFA78A28BC148B753450F270D1879"),
    (BASE + r"\Lib\site-packages\pluggy", "", 16, "F56CF17FA5D42137192463469F89B39F06D505BA1D6B44074EB046C809858C45"),
    (BASE + r"\Lib\site-packages\iniconfig", "", 8, "FDE164BD03F103E4A45B72935E5B6E54500DF815540C532D54C689CFD0539485"),
    (BASE + r"\Lib\site-packages\packaging", "", 32, "A4B27C7FF9853C74BC6F70416255782C70A7F2D98BC222229843373A7C424B63"),
    (BASE + r"\Lib\site-packages\_distutils_hack", "", 6, "053CD7DE1981E3BBB92EDEB9B7086DE5BEC92756241AC0FB11F99B1431864588"),
    (USER_SITE + r"\pygments", "", 674, "A34700D2D8C77C487B5A327B228CECCBEDA750ED277CA4A58599CBA53845AB04"),
    (USER_SITE + r"\colorama", "", 26, "9678523F53E349D2E0FAA5B695DAA7BD92D75139DCEC21146C5CBC52A4CD9EF6"),
    (USER_SITE + r"\pywin32_system32", "", 2, "554F89467F84A628F33C0211678ED1787DC1F2942EA2A0EC338C07DAF59B65E9"),
)

# The nonce is a fixed literal identifier, not an execution run ID.
# Low receives no nonce argument or fifth environment variable.
SYNTHETIC_LITERAL = r'''
import sys, os, json, ctypes, ctypes.wintypes, time, msvcrt, pytest
C = ctypes
W = ctypes.wintypes
K = C.WinDLL("kernel32.dll", use_last_error=True)
A = C.WinDLL("advapi32.dll", use_last_error=True)
H = W.HANDLE
D = W.DWORD
P = C.c_void_p
def bind(lib, name, result, args):
    f = getattr(lib, name)
    f.restype = result
    f.argtypes = args
    return f
GetCurrentProcess = bind(K, "GetCurrentProcess", H, [])
GetStdHandle = bind(K, "GetStdHandle", H, [D])
GetConsoleWindow = bind(K, "GetConsoleWindow", H, [])
GetConsoleCP = bind(K, "GetConsoleCP", D, [])
GetConsoleMode = bind(K, "GetConsoleMode", W.BOOL, [H, C.POINTER(D)])
GetHandleInformation = bind(K, "GetHandleInformation", W.BOOL, [H, C.POINTER(D)])
WriteFile = bind(K, "WriteFile", W.BOOL, [H, P, D, C.POINTER(D), P])
CloseHandle = bind(K, "CloseHandle", W.BOOL, [H])
OpenProcessToken = bind(A, "OpenProcessToken", W.BOOL, [H, D, C.POINTER(H)])
GetTokenInformation = bind(A, "GetTokenInformation", W.BOOL, [H, C.c_int, P, D, C.POINTER(D)])
LookupPrivilegeName = bind(A, "LookupPrivilegeNameW", W.BOOL, [W.LPCWSTR, P, W.LPWSTR, C.POINTER(D)])
ConvertSidToStringSid = bind(A, "ConvertSidToStringSidW", W.BOOL, [P, C.POINTER(W.LPWSTR)])
LocalFree = bind(K, "LocalFree", P, [P])
class SIDATTR(C.Structure):
    _fields_ = [("sid", P), ("attributes", D)]
class LUID(C.Structure):
    _fields_ = [("low", D), ("high", W.LONG)]
class PRIV(C.Structure):
    _fields_ = [("luid", LUID), ("attributes", D)]
def query(token, kind):
    n = D()
    C.set_last_error(0)
    ok = GetTokenInformation(token, kind, None, 0, C.byref(n))
    error = C.get_last_error()
    if ok or error != 122 or n.value == 0 or n.value > 65536:
        raise RuntimeError(("token-size", kind, error, n.value))
    b = C.create_string_buffer(n.value)
    if not GetTokenInformation(token, kind, b, len(b), C.byref(n)):
        raise RuntimeError(("token-query", kind, C.get_last_error()))
    return b
def sid(value):
    out = W.LPWSTR()
    if not ConvertSidToStringSid(value, C.byref(out)):
        raise RuntimeError(("sid", C.get_last_error()))
    try:
        return out.value
    finally:
        if LocalFree(C.cast(out, P)):
            raise RuntimeError(("sid-free", C.get_last_error()))
def fields(token):
    result = {}
    for name, kind in (("user", 1), ("owner", 4), ("integrity", 25)):
        b = query(token, kind)
        if kind == 4:
            result[name] = sid(P.from_buffer(b).value)
        else:
            entry = SIDATTR.from_buffer(b)
            result[name] = sid(entry.sid)
            result[name + "_attributes"] = entry.attributes
    for name, kind in (("type", 8), ("session", 12), ("elevated", 20), ("policy", 27)):
        result[name] = D.from_buffer(query(token, kind)).value
    for name, kind in (("groups", 2), ("restricting", 11)):
        b = query(token, kind)
        count = D.from_buffer(b).value
        offset = (4 + C.alignment(SIDATTR) - 1) & ~(C.alignment(SIDATTR) - 1)
        if count > 256 or offset + count * C.sizeof(SIDATTR) > len(b):
            raise RuntimeError(("group-cap", name, count))
        result[name] = []
        for i in range(count):
            item = SIDATTR.from_buffer(b, offset + i * C.sizeof(SIDATTR))
            result[name].append([sid(item.sid), item.attributes])
    b = query(token, 3)
    count = D.from_buffer(b).value
    if count > 256 or 4 + count * C.sizeof(PRIV) > len(b):
        raise RuntimeError(("privilege-cap", count))
    result["privileges"] = []
    for i in range(count):
        item = PRIV.from_buffer(b, 4 + i * C.sizeof(PRIV))
        n = D(256)
        text = C.create_unicode_buffer(256)
        if not LookupPrivilegeName(None, C.byref(item.luid), text, C.byref(n)):
            raise RuntimeError(("privilege-name", C.get_last_error()))
        result["privileges"].append([item.luid.low, item.luid.high, text.value, item.attributes])
    return result
token = H()
if not OpenProcessToken(GetCurrentProcess(), 8, C.byref(token)):
    raise RuntimeError(("open-token", C.get_last_error()))
try:
    token_fields = fields(token)
    flags = D()
    if not GetHandleInformation(token, C.byref(flags)) or flags.value & 1:
        raise RuntimeError(("token-inherit", C.get_last_error(), flags.value))
finally:
    if not CloseHandle(token):
        raise RuntimeError(("close-token", C.get_last_error()))
ledger_text = os.environ["TPCN_LUNA65_LEDGER_HANDLE"]
if not ledger_text.isascii() or not ledger_text.isdecimal():
    raise RuntimeError("ledger-grammar")
ledger = int(ledger_text)
handles = [GetStdHandle(0xfffffff5), GetStdHandle(0xfffffff4), ledger]
stdin = GetStdHandle(0xfffffff6)
stdio = []
for h in [stdin] + handles:
    mode = D()
    C.set_last_error(0)
    ok = bool(GetConsoleMode(h, C.byref(mode)))
    error = C.get_last_error()
    stdio.append({"handle": h or 0, "console_mode_ok": ok, "console_mode": mode.value, "error": error})
modules = []
for name, module in sorted(tuple(sys.modules.items())):
    origin = getattr(getattr(module, "__spec__", None), "origin", None)
    modules.append([name, origin, getattr(module, "__file__", None)])
observation = {
    "pid": os.getpid(), "executable": sys.executable, "version": sys.version,
    "prefix": sys.prefix, "base_prefix": sys.base_prefix,
    "environment": dict(os.environ), "argv": sys.argv, "cwd": os.getcwd(),
    "sys_path": sys.path, "pytest_version": pytest.__version__, "modules": modules,
    "stdio": stdio, "console_window": GetConsoleWindow() or 0,
    "console_cp": GetConsoleCP(), "token": token_fields,
}
def emit(phase, stream, handle):
    record = {"schema": "L65-RP2-LOW-1", "nonce": "L65-RP2A-SYNTHETIC-V1",
              "phase": phase, "stream": stream, "pid": os.getpid()}
    if phase == "READY":
        record["observation"] = observation
    data = (json.dumps(record, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    if len(data) > 16384:
        raise RuntimeError(("record-cap", len(data)))
    buffer = C.create_string_buffer(data)
    written = D()
    if not WriteFile(handle, buffer, len(data), C.byref(written), None):
        raise RuntimeError(("write", stream, C.get_last_error()))
    if written.value != len(data):
        raise RuntimeError(("short-write", stream, written.value))
for name, h in zip(("stdout", "stderr", "ledger"), handles):
    emit("READY", name, h)
time.sleep(2)
for name, h in zip(("stdout", "stderr", "ledger"), handles):
    emit("END", name, h)
for h in handles:
    if not CloseHandle(h):
        raise RuntimeError(("close-stream", C.get_last_error()))
'''.lstrip()


class ContractError(RuntimeError):
    pass


class ContractDefect(ContractError):
    pass


class IncompleteObservation(ContractError):
    pass


class ApiError(RuntimeError):
    def __init__(self, stage, code):
        message = c.FormatError(code).strip() if isinstance(code, int) and code >= 0 else repr(code)
        super().__init__(stage, code, message)
        self.stage = stage
        self.code = code
        self.message = message


class BoundedErrors(list):
    def __init__(self):
        super().__init__()
        self.omitted = 0

    def append(self, entry):
        if len(self) == 8:
            self.omitted = min(0xFFFFFFFFFFFFFFFF, self.omitted + 1)
            return
        bounded = []
        for value in entry[:4]:
            if isinstance(value, str) and len(value) > 512:
                value = value[:480] + "[TRUNCATED; bounded diagnostic]"
            bounded.append(value)
        super().append(bounded)


class SIDATTR(c.Structure):
    _fields_ = [("sid", c.c_void_p), ("attributes", w.DWORD)]


class LUID(c.Structure):
    _fields_ = [("low", w.DWORD), ("high", w.LONG)]


class PRIV(c.Structure):
    _fields_ = [("luid", LUID), ("attributes", w.DWORD)]


class SECURITY_ATTRIBUTES(c.Structure):
    _fields_ = [("length", w.DWORD), ("descriptor", c.c_void_p), ("inherit", w.BOOL)]


class OBJECT_BASIC(c.Structure):
    _fields_ = [("attributes", w.ULONG), ("access", w.ULONG),
                ("handles", w.ULONG), ("pointers", w.ULONG), ("reserved", w.ULONG * 10)]

class STARTUPINFO(c.Structure):
    _fields_ = [("cb", w.DWORD), ("reserved", w.LPWSTR), ("desktop", w.LPWSTR),
                ("title", w.LPWSTR), ("x", w.DWORD), ("y", w.DWORD),
                ("cx", w.DWORD), ("cy", w.DWORD), ("chars_x", w.DWORD),
                ("chars_y", w.DWORD), ("fill", w.DWORD), ("flags", w.DWORD),
                ("show", w.WORD), ("reserved_size", w.WORD),
                ("reserved_data", c.c_void_p), ("stdin", w.HANDLE),
                ("stdout", w.HANDLE), ("stderr", w.HANDLE)]


class STARTUPINFOEX(c.Structure):
    _fields_ = [("startup", STARTUPINFO), ("attributes", c.c_void_p)]


class PROCESS_INFORMATION(c.Structure):
    _fields_ = [("process", w.HANDLE), ("thread", w.HANDLE),
                ("pid", w.DWORD), ("tid", w.DWORD)]


class JOB_BASIC(c.Structure):
    _fields_ = [("process_time", c.c_int64), ("job_time", c.c_int64),
                ("flags", w.DWORD), ("min_ws", c.c_size_t), ("max_ws", c.c_size_t),
                ("active", w.DWORD), ("affinity", c.c_size_t),
                ("priority", w.DWORD), ("scheduling", w.DWORD)]


class IO_COUNTERS(c.Structure):
    _fields_ = [(name, c.c_uint64) for name in
                ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]


class JOB_EXTENDED(c.Structure):
    _fields_ = [("basic", JOB_BASIC), ("io", IO_COUNTERS),
                ("process_memory", c.c_size_t), ("job_memory", c.c_size_t),
                ("peak_process_memory", c.c_size_t), ("peak_job_memory", c.c_size_t)]


class JOB_ACCOUNTING(c.Structure):
    _fields_ = [("user", c.c_int64), ("kernel", c.c_int64),
                ("period_user", c.c_int64), ("period_kernel", c.c_int64),
                ("faults", w.DWORD), ("total", w.DWORD),
                ("active", w.DWORD), ("terminated", w.DWORD)]


class MEMORY_COUNTERS(c.Structure):
    _fields_ = [("size", w.DWORD), ("faults", w.DWORD)] + [
        (name, c.c_size_t) for name in ("peak_ws", "ws", "peak_paged", "paged",
                                       "peak_nonpaged", "nonpaged", "pagefile",
                                       "peak_pagefile", "private")]

class PSS_HANDLE_ENTRY(c.Structure):
    # AMD64 SDK layout: the type-specific union occupies 48 bytes.
    _fields_ = [("handle", w.HANDLE), ("flags", w.DWORD), ("object_type", w.DWORD),
                ("capture_time", w.FILETIME), ("attributes", w.DWORD),
                ("reserved_access", w.DWORD), ("handle_count", w.DWORD),
                ("pointer_count", w.DWORD), ("paged", w.DWORD), ("nonpaged", w.DWORD),
                ("creation_time", w.FILETIME), ("type_name_length", w.WORD),
                ("type_name", w.LPWSTR), ("object_name_length", w.WORD),
                ("object_name", w.LPWSTR), ("type_specific", c.c_byte * 48)]


THREADPROC = c.WINFUNCTYPE(w.DWORD, c.c_void_p)


class Native:
    """Explicit x64 Windows ABI; constructors are never called during RP-2A."""

    def __init__(self):
        if (os.name != "nt" or c.sizeof(c.c_void_p) != 8 or c.sizeof(OBJECT_BASIC) != 56
                or c.sizeof(STARTUPINFOEX) != 112 or c.sizeof(PROCESS_INFORMATION) != 24
                or c.sizeof(JOB_EXTENDED) != 144 or c.sizeof(PSS_HANDLE_ENTRY) != 136
                or c.sizeof(MEMORY_COUNTERS) != 80):
            raise ContractError("Windows AMD64 / ObjectBasicInformation ABI")
        self.k = c.WinDLL("kernel32.dll", use_last_error=True)
        self.a = c.WinDLL("advapi32.dll", use_last_error=True)
        self.n = c.WinDLL("ntdll.dll")
        H, P, D, B = w.HANDLE, c.c_void_p, w.DWORD, w.BOOL
        HP, DP = c.POINTER(H), c.POINTER(D)
        specifications = (
            (self.k, "GetTickCount64", c.c_uint64, []),
            (self.k, "GetCurrentProcess", H, []),
            (self.k, "GetCurrentThread", H, []),
            (self.k, "GetHandleInformation", B, [H, DP]),
            (self.k, "SetHandleInformation", B, [H, D, D]),
            (self.k, "CloseHandle", B, [H]),
            (self.k, "LocalFree", P, [P]),
            (self.k, "DuplicateHandle", B, [H, H, H, HP, D, B, D]),
            (self.k, "CompareObjectHandles", B, [H, H]),
            (self.a, "GetKernelObjectSecurity", B, [H, D, P, D, DP]),
            (self.k, "WaitForSingleObject", D, [H, D]),
            (self.k, "TerminateProcess", B, [H, w.UINT]),
            (self.k, "TerminateJobObject", B, [H, w.UINT]),
            (self.k, "CancelSynchronousIo", B, [H]),
            (self.k, "GetExitCodeProcess", B, [H, DP]),
            (self.k, "GetProcessId", D, [H]),
            (self.k, "GetProcessTimes", B, [H, P, P, P, P]),
            (self.k, "K32GetProcessMemoryInfo", B, [H, P, D]),
            (self.k, "IsProcessInJob", B, [H, H, c.POINTER(B)]),
            (self.k, "CreatePipe", B, [HP, HP, P, D]),
            (self.k, "CreateEventW", H, [P, B, B, w.LPCWSTR]),
            (self.k, "CreateJobObjectW", H, [P, w.LPCWSTR]),
            (self.k, "SetInformationJobObject", B, [H, c.c_int, P, D]),
            (self.k, "QueryInformationJobObject", B, [H, c.c_int, P, D, DP]),
            (self.k, "CreateThread", H, [P, c.c_size_t, THREADPROC, P, D, DP]),
            (self.k, "ReadFile", B, [H, P, D, DP, P]),
            (self.k, "WriteFile", B, [H, P, D, DP, P]),
            (self.k, "GetStdHandle", H, [D]),
            (self.k, "ResumeThread", D, [H]),
            (self.k, "InitializeProcThreadAttributeList", B, [P, D, D, c.POINTER(c.c_size_t)]),
            (self.k, "UpdateProcThreadAttribute", B, [P, D, c.c_size_t, P, c.c_size_t, P, P]),
            (self.k, "DeleteProcThreadAttributeList", None, [P]),
            (self.k, "PssCaptureSnapshot", D, [H, D, D, HP]),
            (self.k, "PssFreeSnapshot", D, [H, H]),
            (self.k, "PssWalkMarkerCreate", D, [P, HP]),
            (self.k, "PssWalkMarkerFree", D, [H]),
            (self.k, "PssWalkSnapshot", D, [H, c.c_int, H, P, D]),
            (self.k, "QueryFullProcessImageNameW", B, [H, D, w.LPWSTR, DP]),
            (self.k, "OpenProcess", H, [D, B, D]),
            (self.k, "OpenThread", H, [D, B, D]),
            (self.a, "OpenProcessToken", B, [H, D, HP]),
            (self.a, "OpenThreadToken", B, [H, D, B, HP]),
            (self.a, "GetTokenInformation", B, [H, c.c_int, P, D, DP]),
            (self.a, "SetTokenInformation", B, [H, c.c_int, P, D]),
            (self.a, "CreateRestrictedToken", B, [H, D, D, P, D, P, D, P, HP]),
            (self.a, "CreateProcessAsUserW", B, [H, w.LPCWSTR, w.LPWSTR, P, P,
                                               B, D, P, w.LPCWSTR, P, P]),
            (self.a, "LookupPrivilegeNameW", B, [w.LPCWSTR, P, w.LPWSTR, DP]),
            (self.a, "ConvertSidToStringSidW", B, [P, c.POINTER(w.LPWSTR)]),
            (self.a, "ConvertStringSidToSidW", B, [w.LPCWSTR, c.POINTER(P)]),
            (self.a, "ConvertStringSecurityDescriptorToSecurityDescriptorW",
             B, [w.LPCWSTR, D, c.POINTER(P), DP]),
            (self.a, "IsValidSecurityDescriptor", B, [P]),
            (self.a, "GetSecurityDescriptorControl", B, [P, c.POINTER(w.WORD), DP]),
            (self.a, "GetSecurityDescriptorOwner", B, [P, c.POINTER(P), c.POINTER(B)]),
            (self.a, "GetSecurityDescriptorGroup", B, [P, c.POINTER(P), c.POINTER(B)]),
            (self.a, "GetSecurityDescriptorDacl", B, [P, c.POINTER(B), c.POINTER(P), c.POINTER(B)]),
            (self.a, "GetSecurityDescriptorSacl", B, [P, c.POINTER(B), c.POINTER(P), c.POINTER(B)]),
            (self.a, "GetAce", B, [P, D, c.POINTER(P)]),
            (self.n, "NtQueryObject", w.LONG, [H, c.c_int, P, w.ULONG, c.POINTER(w.ULONG)]),
        )
        for library, name, result, args in specifications:
            function = getattr(library, name)
            function.restype = result
            function.argtypes = args
            setattr(self, name, function)

    def check(self, value, stage):
        if not value:
            error = c.get_last_error()
            raise ApiError(stage, error)
        return value

    def rights(self, handle):
        info, length = OBJECT_BASIC(), w.ULONG()
        status = self.NtQueryObject(handle, 0, c.byref(info), 56, c.byref(length))
        if status != 0 or length.value != 56:
            raise ApiError("NtQueryObject/ABI", {"status": status, "length": length.value})
        flags = w.DWORD()
        self.check(self.GetHandleInformation(handle, c.byref(flags)), "GetHandleInformation")
        type_buffer, type_length = c.create_string_buffer(TOKEN_LIMIT), w.ULONG()
        type_status = self.NtQueryObject(handle, 2, type_buffer, len(type_buffer), c.byref(type_length))
        if type_status != 0 or not 16 <= type_length.value <= TOKEN_LIMIT:
            raise ApiError("NtQueryObject/type ABI", {"status": type_status, "length": type_length.value})
        string_length = w.WORD.from_buffer(type_buffer).value
        string_pointer = c.c_void_p.from_buffer(type_buffer, 8).value
        if (string_length % 2 or not string_pointer or string_pointer < c.addressof(type_buffer)
                or string_pointer + string_length > c.addressof(type_buffer) + len(type_buffer)):
            raise ContractError("object type UNICODE_STRING bounds")
        object_type = c.wstring_at(string_pointer, string_length // 2)
        return {"access": info.access, "object_attributes": info.attributes,
                "original_handle_flags": flags.value, "ntstatus": status, "length": length.value,
                "object_type": object_type, "type_ntstatus": type_status, "type_length": type_length.value}

    def sid(self, value, bounds):
        if not value:
            return None
        base, size = bounds
        if value < base or value + 8 > base + size:
            raise ContractError("SID pointer bounds")
        header = c.string_at(value, 8)
        required = 8 + 4 * header[1]
        if header[0] != 1 or required > 68 or value + required > base + size:
            raise ContractError("SID length/revision bounds")
        text = w.LPWSTR()
        self.check(self.ConvertSidToStringSidW(value, c.byref(text)), "ConvertSidToStringSidW")
        try:
            return text.value
        finally:
            if self.LocalFree(c.cast(text, c.c_void_p)):
                raise ApiError("LocalFree/SID", c.get_last_error())

    def token_buffer(self, token, kind):
        length = w.DWORD()
        c.set_last_error(0)
        ok = self.GetTokenInformation(token, kind, None, 0, c.byref(length))
        error = c.get_last_error()
        if ok or error != 122 or not 0 < length.value <= TOKEN_LIMIT:
            raise ApiError("GetTokenInformation/size", (kind, error, length.value))
        data = c.create_string_buffer(length.value)
        self.check(self.GetTokenInformation(token, kind, data, len(data), c.byref(length)),
                   "GetTokenInformation/data")
        if length.value != len(data):
            raise ContractError("token buffer returned-length drift")
        return data

    def token_fields(self, token):
        result = {}
        for name, kind in (("user", 1), ("owner", 4), ("integrity", 25)):
            data = self.token_buffer(token, kind)
            if kind == 4:
                result[name] = self.sid(c.c_void_p.from_buffer(data).value, (c.addressof(data), len(data)))
            else:
                item = SIDATTR.from_buffer(data)
                result[name] = self.sid(item.sid, (c.addressof(data), len(data)))
                result[name + "_attributes"] = item.attributes
        for name, kind in (("type", 8), ("session", 12), ("elevated", 20), ("policy", 27),
                           ("appcontainer", 29), ("ui_access", 26)):
            result[name] = w.DWORD.from_buffer(self.token_buffer(token, kind)).value
        for name, kind in (("groups", 2), ("restricting", 11)):
            data = self.token_buffer(token, kind)
            count = w.DWORD.from_buffer(data).value
            offset = (4 + c.alignment(SIDATTR) - 1) & ~(c.alignment(SIDATTR) - 1)
            if count > ENUM_LIMIT or offset + count * c.sizeof(SIDATTR) > len(data):
                raise ContractError(("group enumeration cap", name, count))
            result[name] = []
            for i in range(count):
                item = SIDATTR.from_buffer(data, offset + i * c.sizeof(SIDATTR))
                result[name].append([self.sid(item.sid, (c.addressof(data), len(data))), item.attributes])
        data = self.token_buffer(token, 3)
        count = w.DWORD.from_buffer(data).value
        if count > ENUM_LIMIT or 4 + count * c.sizeof(PRIV) > len(data):
            raise ContractError("privilege enumeration cap")
        result["privileges"] = []
        for i in range(count):
            item = PRIV.from_buffer(data, 4 + i * c.sizeof(PRIV))
            length = w.DWORD(256)
            text = c.create_unicode_buffer(256)
            self.check(self.LookupPrivilegeNameW(None, c.byref(item.luid), text, c.byref(length)),
                       "LookupPrivilegeNameW")
            result["privileges"].append([item.luid.low, item.luid.high, text.value, item.attributes])
        data = self.token_buffer(token, 6)
        acl = c.c_void_p.from_buffer(data).value
        result["default_dacl"] = self.acl(acl, (c.addressof(data), len(data))) if acl else None
        return result

    def acl(self, pointer, bounds):
        if not pointer:
            return None
        base, length = bounds
        if pointer < base or pointer + 8 > base + length:
            raise ContractError("ACL pointer bounds")
        header = c.string_at(pointer, 8)
        size = int.from_bytes(header[2:4], "little")
        count = int.from_bytes(header[4:6], "little")
        if size < 8 or size > TOKEN_LIMIT or count > ENUM_LIMIT or pointer + size > base + length:
            raise ContractError("ACL cap/size")
        entries = []
        for index in range(count):
            address = c.c_void_p()
            self.check(self.GetAce(pointer, index, c.byref(address)), "GetAce")
            head = c.string_at(address, 4)
            ace_size = int.from_bytes(head[2:4], "little")
            if ace_size < 8 or address.value < pointer or address.value + ace_size > pointer + size:
                raise ContractError("ACE bounds")
            raw = c.string_at(address, ace_size)
            kind = raw[0]
            # Ordinary allow/deny and mandatory label; unknown ACEs are explicit,
            # not discarded or interpreted with an incorrect SID offset.
            if kind not in (0, 1, 17):
                raise ContractError(("unsupported ACE decode", kind, raw.hex()))
            entries.append({"type": kind, "flags": raw[1],
                            "mask": int.from_bytes(raw[4:8], "little"),
                            "sid": self.sid(address.value + 8, (address.value, ace_size)), "raw": raw.hex()})
        return {"revision": header[0], "size": size, "count": count, "aces": entries}

    def descriptor(self, handle):
        length = w.DWORD()
        information = 0x17  # OWNER | GROUP | DACL | LABEL, never audit SACL.
        c.set_last_error(0)
        ok = self.GetKernelObjectSecurity(handle, information, None, 0, c.byref(length))
        error = c.get_last_error()
        if ok or error != 122 or not 0 < length.value <= TOKEN_LIMIT:
            raise ApiError("GetKernelObjectSecurity/size", (error, length.value))
        data = c.create_string_buffer(length.value)
        self.check(self.GetKernelObjectSecurity(handle, information, data, len(data), c.byref(length)),
                   "GetKernelObjectSecurity/data")
        self.check(self.IsValidSecurityDescriptor(data), "IsValidSecurityDescriptor")
        control, revision = w.WORD(), w.DWORD()
        self.check(self.GetSecurityDescriptorControl(data, c.byref(control), c.byref(revision)),
                   "GetSecurityDescriptorControl")
        result = {"raw": data.raw[:length.value].hex(), "control": control.value,
                  "revision": revision.value, "self_relative": bool(control.value & 0x8000),
                  "dacl_protected": bool(control.value & 0x1000)}
        for name, function in (("owner", self.GetSecurityDescriptorOwner),
                               ("group", self.GetSecurityDescriptorGroup)):
            pointer, defaulted = c.c_void_p(), w.BOOL()
            self.check(function(data, c.byref(pointer), c.byref(defaulted)), name)
            result[name] = self.sid(pointer.value, (c.addressof(data), len(data)))
            result[name + "_defaulted"] = bool(defaulted.value)
        for name, function in (("dacl", self.GetSecurityDescriptorDacl),
                               ("label_sacl", self.GetSecurityDescriptorSacl)):
            present, defaulted, pointer = w.BOOL(), w.BOOL(), c.c_void_p()
            self.check(function(data, c.byref(present), c.byref(pointer), c.byref(defaulted)), name)
            result[name + "_present"] = bool(present.value)
            result[name + "_defaulted"] = bool(defaulted.value)
            result[name] = self.acl(pointer.value, (c.addressof(data), len(data)))
        if not result["self_relative"] or not result["dacl_present"] or result["dacl"] is None:
            raise ContractError("unreadable/NULL/absent DACL")
        labels = result["label_sacl"]
        result["effective_label"] = "S-1-16-8192"
        result["label_origin"] = "OS-default-Medium"
        if labels:
            label_aces = [ace for ace in labels["aces"] if ace["type"] == 17]
            if len(label_aces) != 1:
                raise ContractError("ambiguous mandatory label")
            result["effective_label"] = label_aces[0]["sid"]
            result["label_origin"] = "explicit"
        return result

    def no_impersonation(self):
        token = w.HANDLE()
        c.set_last_error(0)
        ok = self.OpenThreadToken(self.GetCurrentThread(), QUERY_TOKEN_ACCESS, False, c.byref(token))
        error = c.get_last_error()
        if ok:
            self.check(self.CloseHandle(token), "CloseHandle/rejected thread token")
            raise ContractError("thread impersonation token present")
        if error != 1008:
            raise ApiError("OpenThreadToken/no-token", error)


def enforce_token(fields, low, source=None, literal_observation=False):
    if fields["user"] != USER or fields["owner"] != USER or fields["type"] != 1:
        raise ContractError("token account/owner/type")
    if fields["elevated"] or fields["restricting"]:
        raise ContractError("elevation/restricting SIDs")
    if fields["user_attributes"] & 0x10:
        raise ContractError("deny-only user")
    if not literal_observation and (fields["appcontainer"] or fields["ui_access"]):
        raise ContractError("AppContainer/UIAccess token")
    if fields["integrity"] != ("S-1-16-4096" if low else "S-1-16-8192"):
        raise ContractError("contained integrity")
    if low and fields["policy"] != 3:
        raise ContractError("mandatory policy is readback-only")
    forbidden = {"SeDebugPrivilege", "SeAssignPrimaryTokenPrivilege", "SeIncreaseQuotaPrivilege",
                 "SeTcbPrivilege", "SeImpersonatePrivilege", "SeBackupPrivilege", "SeRestorePrivilege",
                 "SeTakeOwnershipPrivilege", "SeLoadDriverPrivilege"}
    change = False
    for _, _, name, attributes in fields["privileges"]:
        if not low and name in forbidden:
            raise ContractError(("forbidden source privilege present", name))
        if name == "SeChangeNotifyPrivilege":
            change = bool(attributes & 2)
        elif attributes & 2:
            raise ContractError(("unexpected enabled privilege", name))
    if not change:
        raise ContractError("ChangeNotify must already be enabled; no repair")
    if source is not None:
        if source["session"] != fields["session"]:
            raise ContractError("session drift")
        original_privileges = {(low_part, high_part): name
                               for low_part, high_part, name, _ in source["privileges"]}
        for low_part, high_part, name, _ in fields["privileges"]:
            if original_privileges.get((low_part, high_part)) != name:
                raise ContractError(("added or renamed privilege", low_part, high_part, name))
        original = dict(source["groups"])
        if len(original) != len(source["groups"]) or len(dict(fields["groups"])) != len(fields["groups"]):
            raise ContractError("duplicate group SID census")
        # Setting contained IL replaces the integrity group SID, not an added
        # discretionary group or an unauthorized group-enabling operation.
        for old_sid, old_flags in list(original.items()):
            if old_flags & 0x20:
                del original[old_sid]
                original[fields["integrity"]] = old_flags
        allowed = {USER, "S-1-1-0", "S-1-5-32-545", "S-1-5-11"}
        for sid, flags in fields["groups"]:
            if sid not in original:
                raise ContractError(("added group", sid))
            if original[sid] & 0x10 and not flags & 0x10:
                raise ContractError(("deny-only group enabled", sid))
            if sid not in allowed and (not flags & 0x10 or flags & 6):
                raise ContractError(("group not disabled", sid))
            if sid in allowed and flags & 4 and not original[sid] & 4:
                raise ContractError(("source-disabled group enabled", sid))
        if {sid for sid, _ in fields["groups"]} != set(original):
            raise ContractError("group census changed")


def quote(argument):
    if "\0" in argument:
        raise ContractError("NUL command argument")
    result, backslashes = '"', 0
    for character in argument:
        if character == "\\":
            backslashes += 1
        elif character == '"':
            result += "\\" * (backslashes * 2 + 1) + '"'
            backslashes = 0
        else:
            result += "\\" * backslashes + character
            backslashes = 0
    return result + "\\" * (backslashes * 2) + '"'


def environment(ledger, systemroot):
    if not isinstance(ledger, int) or ledger <= 0:
        raise ContractError("ledger handle decimal grammar")
    values = {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
              "SYSTEMROOT": systemroot, "TPCN_LUNA65_LEDGER_HANDLE": str(ledger)}
    if any("\0" in value for value in values.values()):
        raise ContractError("environment NUL")
    return "\0".join(key + "=" + values[key] for key in sorted(values)) + "\0\0"


def source_digest(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest().upper()


XM = "O:" + USER + "D:P(D;;0x00060000;;;OW)S:(ML;;NWNR;;;ME)"
XL = "O:" + USER + "D:P(D;;0x00060000;;;OW)S:(ML;;NW;;;LW)"
PL = "O:" + USER + "D:P(D;;0x00060000;;;OW)(A;;0x0012019B;;;" + USER + ")S:(ML;;NW;;;LW)"
STOP_CODE = 0xE0650002
P_RETAINED_RESERVATION = 393216
LOW_RECORD_LIMIT = 16384
LOW_LOGICAL_RESERVATION = 3 * LOW_RECORD_LIMIT


class Descriptor:
    def __init__(self, n, text, inherit=False):
        self.n, self.pointer = n, c.c_void_p()
        length = w.DWORD()
        n.check(n.ConvertStringSecurityDescriptorToSecurityDescriptorW(
            text, 1, c.byref(self.pointer), c.byref(length)), "SDDL")
        self.attributes = SECURITY_ATTRIBUTES(c.sizeof(SECURITY_ATTRIBUTES),
                                               self.pointer, inherit)

    def close(self):
        if self.pointer.value:
            if self.n.LocalFree(self.pointer):
                raise ApiError("LocalFree/SDDL", c.get_last_error())
            self.pointer = c.c_void_p()


def semantic_sd(value):
    return {key: item for key, item in value.items() if key != "raw"}


def target_sd(n, handle, label, pipe=False):
    value = n.descriptor(handle)
    expected = [{"type": 1, "flags": 0, "mask": 0x60000, "sid": "S-1-3-4"}]
    if pipe:
        expected.append({"type": 0, "flags": 0, "mask": 0x12019B, "sid": USER})
    actual = [{key: ace[key] for key in ("type", "flags", "mask", "sid")}
              for ace in value["dacl"]["aces"]]
    labels = value["label_sacl"]
    if (value["owner"] != USER or not value["dacl_protected"] or actual != expected
            or value["label_origin"] != "explicit" or value["effective_label"] != label
            or not labels or labels["count"] != 1
            or labels["aces"][0]["mask"] != (3 if label == "S-1-16-8192" else 1)):
        raise ContractError(("descriptor target mismatch", value))
    return value


def tree_identity(path, skip, tick):
    digest, count = hashlib.sha256(), 0
    def walk(directory):
        nonlocal count
        items = []
        with os.scandir(directory) as scan:
            for entry in scan:
                tick()
                if directory == path and entry.name.casefold() == skip.casefold():
                    continue
                if entry.is_symlink() or entry.stat().st_file_attributes & 0x400:
                    raise ContractError(("reparse in closure", entry.path))
                items.append((entry.name.lower() + ("\\" if entry.is_dir() else ""), entry.path, entry.is_dir()))
                if len(items) > 2048:
                    raise ContractError("closure directory fanout cap")
        for _, full, is_dir in sorted(items):
            tick()
            if is_dir:
                walk(full)
                continue
            if os.path.splitext(full)[1].casefold() not in (".py", ".pyc", ".pyd", ".dll", ".pth", ".json"):
                continue
            if count >= 10000 or os.path.getsize(full) > 33554432:
                raise ContractError(("static closure cap", full))
            relative = os.path.relpath(full, path).lower()
            digest.update((relative + "|" + str(os.path.getsize(full)) + "|" +
                           source_digest(full) + "\n").encode("utf-8"))
            count += 1
    walk(path)
    return count, digest.hexdigest().upper()


def verify_closure(tick):
    if source_digest(IMAGE) != IMAGE_SHA256:
        raise ContractError("interpreter drift")
    for path, expected in INSPECTED_STARTUP.items():
        tick()
        if source_digest(path) != expected:
            raise ContractError(("startup drift", path))
    for path, skip, count, expected in TREE_MANIFEST:
        if tree_identity(path, skip, tick) != (count, expected):
            raise ContractError(("library closure drift", path))
    search = [ROOT, ROOT + r"\scripts", BASE, BASE + r"\Lib", BASE + r"\DLLs",
              USER_SITE, USER_SITE + r"\win32", USER_SITE + r"\win32\lib",
              USER_SITE + r"\Pythonwin", BASE + r"\Lib\site-packages"]
    effective_user_site = ROOT + r"\~\Python\Python311\site-packages"
    if os.path.lexists(effective_user_site):
        raise ContractError("no-APPDATA relative user-site absence drift")
    for path in search:
        for name in ("sitecustomize.py", "sitecustomize.pyc", "sitecustomize.pyd",
                     "usercustomize.py", "usercustomize.pyc", "usercustomize.pyd",
                     "sitecustomize", "usercustomize"):
            if os.path.lexists(os.path.join(path, name)):
                raise ContractError(("unapproved startup hook", path, name))
    for name in ("python._pth", "python311._pth", "pyvenv.cfg", "python311.zip"):
        if os.path.lexists(os.path.join(BASE, name)):
            raise ContractError(("unapproved path configuration", name))
    for root, expected in ((USER_SITE, ["pywin32.pth"]),
                           (BASE + r"\Lib\site-packages", ["distutils-precedence.pth"])):
        if sorted(name for name in os.listdir(root) if name.lower().endswith(".pth")) != expected:
            raise ContractError(("pth census drift", root))
    module_names = {"sys", "os", "json", "ctypes", "time", "msvcrt", "pytest", "_pytest",
                    "pluggy", "iniconfig", "packaging", "pygments", "colorama",
                    "_distutils_hack", "typing_extensions", "pywin32_bootstrap",
                    "pywin32_system32", "py", "hashlib"}
    for name in os.listdir(BASE + r"\Lib"):
        stem, extension = os.path.splitext(name)
        if extension in ("", ".py", ".pyc") and name not in ("site-packages", "__pycache__"):
            module_names.add(stem if extension else name)
    for root in (ROOT, ROOT + r"\scripts"):
        for name in module_names:
            for suffix in ("", ".py", ".pyc", ".pyd"):
                if os.path.lexists(os.path.join(root, name + suffix)):
                    raise ContractError(("cwd/script startup shadow", root, name + suffix))
        if any(name.lower().endswith((".dll", ".pyd", ".pth")) for name in os.listdir(root)):
            raise ContractError(("cwd native/startup shadow", root))
    return {"trees": TREE_MANIFEST, "startup": INSPECTED_STARTUP,
            "effective_Medium_path": [ROOT + r"\scripts", BASE + r"\python311.zip",
                                      BASE + r"\DLLs", BASE + r"\Lib", BASE,
                                      BASE + r"\Lib\site-packages"],
            "effective_Low_path": ["", BASE + r"\python311.zip", BASE + r"\DLLs",
                                   BASE + r"\Lib", BASE, BASE + r"\Lib\site-packages"],
            "inactive_user_site_supplement": USER_SITE,
            "relative_user_site_absent": effective_user_site,
            "hook_absence_search_roots": search, "imports_not_executed_by_preflight": True}


class Controller:
    def __init__(self, n, nonce, o0, p0):
        self.n, self.nonce, self.o0, self.p0 = n, nonce, o0, p0
        self.active_end = min(p0 + 10000, o0 + 20000)
        self.f = None
        self.sequence = 0
        self.sent = 0
        self.highwater = 0
        self.metadata_sizes = {}
        self.owned = {}
        self.workers = []
        self.references = []
        self.descriptors = []
        self.job = None
        self.pi = None
        self.attempted = False
        self.create_result_known = True
        self.resumed = False
        self.member = False
        self.errors = BoundedErrors()
        self.sections = {name: {"status": "NOT_REACHED", "reason": "entry"} for name in ("U1", "U2", "U3")}
        self.eofs = [False, False, False]
        self.ready = [None, None, None]
        self.ends = [None, None, None]
        self.lines = [bytearray(), bytearray(), bytearray()]
        self.exit_code = None
        self.root_signalled = False
        self.job_zero = False
        self.first_zero = None
        self.last_active = None
        self.descendant_unknown = False
        self.last_sample = 0
        self.contract_defect = False
        self.partial = False
        self.stop_reason = None
        self.output = n.GetStdHandle(0xFFFFFFF5)
        self.runtime_done = False
        self.systemroot = None
        self.source_fields = None
        self.child_token = None
        self.wall_pair = {"uptime_ms": n.GetTickCount64(), "wall_unix_ns": time.time_ns()}

    def retain_metadata(self, name, value):
        size = len(json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")) * 2
        next_total = sum(self.metadata_sizes.values()) - self.metadata_sizes.get(name, 0) + size
        if next_total + TOKEN_LIMIT + RECORD_LIMIT * 9 + LOW_LOGICAL_RESERVATION + 3 * 4096 > P_RETAINED_RESERVATION:
            raise IncompleteObservation("P retained metadata reservation exhausted")
        self.metadata_sizes[name] = size

    def reserve_parse(self, size):
        live = (TOKEN_LIMIT + LOW_LOGICAL_RESERVATION + sum(self.metadata_sizes.values())
                + sum(len(line) for line in self.lines) + 3 * RECORD_LIMIT
                + 3 * size + 3 * 4096)
        if live > P_RETAINED_RESERVATION:
            raise IncompleteObservation("P parse representation reservation exhausted")
        self.highwater = max(self.highwater, live)

    def tick(self, cleanup=False):
        now = self.n.GetTickCount64()
        end = self.cleanup_end() if cleanup else self.active_end
        if now >= end:
            raise ContractError(("deadline", now, end))
        return now

    def cleanup_end(self):
        return min((self.f if self.f is not None else self.active_end) + 5000,
                   self.p0 + 15000, self.o0 + 20000)

    def emit(self, section, stage, data):
        self.sequence += 1
        message = {"schema": "L65-RP2-RELAY-1", "nonce": self.nonce,
                   "sequence": self.sequence, "tick": self.n.GetTickCount64(),
                   "section": section, "stage": stage, "data": data}
        raw = (json.dumps(message, ensure_ascii=True, sort_keys=True,
                          separators=(",", ":")) + "\n").encode("ascii")
        reserve_stage = stage in {"NO_LOW_CREATED", "CLEANUP_BEGIN", "JOB_TERMINATION_REQUEST",
                                  "SUSPENDED_ROOT_TERMINATION_REQUEST", "FINAL"}
        sent_cap = PAYLOAD_LIMIT // 2 + (32768 if reserve_stage else 0)
        if len(raw) > RECORD_LIMIT or self.sent + len(raw) > sent_cap:
            raise ContractError("relay record/aggregate cap")
        self.highwater = max(self.highwater, TOKEN_LIMIT + LOW_LOGICAL_RESERVATION + sum(self.metadata_sizes.values()) +
                             len(raw) * 3 + sum(len(line) for line in self.lines)
                             + sum(worker.pending_size for worker in self.workers) + 3 * 4096)
        if self.highwater > P_RETAINED_RESERVATION:
            raise ContractError("P simultaneous representation reservation")
        length = w.DWORD()
        self.n.check(self.n.WriteFile(self.output, raw, len(raw), c.byref(length), None),
                     "WriteFile/relay")
        if length.value != len(raw):
            raise ContractError("relay short write")
        self.sent += len(raw)

    def own(self, handle, name):
        if not handle:
            raise ApiError(name, c.get_last_error())
        value = handle.value if isinstance(handle, w.HANDLE) else handle
        if value in self.owned:
            raise ContractError("duplicate ownership entry")
        self.owned[value] = name
        return value

    def close(self, handle):
        if handle in self.owned:
            self.n.check(self.n.CloseHandle(handle), "CloseHandle/" + self.owned[handle])
            del self.owned[handle]

    def cleanup_close(self, handle):
        try:
            self.close(handle)
        except Exception as error:
            self.errors.append(["cleanup close", getattr(error, "code", None), str(error)])

    def cleanup_emit(self, stage, data):
        try:
            self.emit("controller", stage, data)
        except Exception as error:
            self.errors.append(["cleanup evidence", stage, str(error)])

    def rights(self, handle, expected=None, inherit=False):
        value = self.n.rights(handle)
        if value["original_handle_flags"] != int(inherit):
            raise ContractError(("inheritance flag", handle, value))
        if expected is not None and value["access"] != expected:
            raise ContractError(("granted access", handle, value, expected))
        expected_type = {SOURCE_TOKEN_ACCESS: "Token", QUERY_TOKEN_ACCESS: "Token",
                         0x1F003F: "Job", 0x1F0003: "Event"}.get(expected)
        if expected_type is not None and value["object_type"] != expected_type:
            raise ContractError(("handle object type", value, expected_type))
        return value

    def token(self, process, access, name):
        token = w.HANDLE()
        self.n.check(self.n.OpenProcessToken(process, access, c.byref(token)), "OpenProcessToken/" + name)
        handle = self.own(token, name)
        self.rights(handle, access)
        fields, descriptor = self.n.token_fields(handle), self.n.descriptor(handle)
        self.retain_metadata(name, {"fields": fields, "sd": descriptor})
        self.emit("U1", name, {"fields": fields, "sd": descriptor, "rights": self.n.rights(handle)})
        return handle, fields, descriptor

    def drift(self, handle, before, name):
        after = self.n.descriptor(handle)
        self.emit("U1", name + "/SD-final", {"raw_equal": before["raw"] == after["raw"],
                                          "semantic_equal": semantic_sd(before) == semantic_sd(after),
                                          "sd": after})
        if semantic_sd(before) != semantic_sd(after):
            raise ContractError(("token object SD drift", name))

    def make_descriptor(self, text, inherit=False):
        value = Descriptor(self.n, text, inherit)
        self.descriptors.append(value)
        return value

    def restricted_token(self, source, fields):
        allowed = {USER, "S-1-1-0", "S-1-5-32-545", "S-1-5-11"}
        disabled = [sid for sid, _ in fields["groups"] if sid not in allowed]
        sid_pointers = []
        array = (SIDATTR * len(disabled))()
        try:
            for index, sid in enumerate(disabled):
                pointer = c.c_void_p()
                self.n.check(self.n.ConvertStringSidToSidW(sid, c.byref(pointer)), "disabled SID")
                sid_pointers.append(pointer)
                array[index] = SIDATTR(pointer, 0)
            result = w.HANDLE()
            self.n.check(self.n.CreateRestrictedToken(source, 1, len(array), array, 0, None,
                                                      0, None, c.byref(result)),
                         "CreateRestrictedToken/DISABLE_MAX_PRIVILEGE")
            handle = self.own(result, "derived token")
            before_flags = self.n.rights(handle)
            if before_flags["original_handle_flags"] & 1:
                self.n.check(self.n.SetHandleInformation(handle, 1, 0), "derived token noninherit")
            self.emit("U1", "derived-handle-inheritance", {"before": before_flags,
                      "inherit_cleared": bool(before_flags["original_handle_flags"] & 1),
                      "after": self.n.rights(handle)})
            self.rights(handle, SOURCE_TOKEN_ACCESS)
            low = c.c_void_p()
            self.n.check(self.n.ConvertStringSidToSidW("S-1-16-4096", c.byref(low)), "Low SID")
            sid_pointers.append(low)
            label = SIDATTR(low, 0x20)
            self.n.check(self.n.SetTokenInformation(handle, 25, c.byref(label),
                                                    c.sizeof(label) + 12), "SetTokenInformation/Low")
            derived, sd = self.n.token_fields(handle), self.n.descriptor(handle)
            self.retain_metadata("derived", {"fields": derived, "sd": sd})
            enforce_token(derived, True, fields)
            self.emit("U1", "derived", {"fields": derived, "sd": sd,
                                      "disabled_groups": disabled, "rights": self.n.rights(handle)})
            return handle, derived, sd
        finally:
            for pointer in sid_pointers:
                if self.n.LocalFree(pointer):
                    raise ApiError("LocalFree/group SID", c.get_last_error())

    def configure_job(self):
        attributes = self.make_descriptor(XM).attributes
        self.job = self.own(self.n.CreateJobObjectW(c.byref(attributes), None), "sole job")
        self.rights(self.job, 0x1F003F)
        target_sd(self.n, self.job, "S-1-16-8192")
        settings = JOB_EXTENDED()
        settings.basic.job_time = 50000000
        settings.basic.flags = 0x2000 | 0x200 | 0x8 | 0x4
        settings.basic.active = 8
        settings.job_memory = 67108864
        self.n.check(self.n.SetInformationJobObject(self.job, 9, c.byref(settings),
                                                   c.sizeof(settings)), "job limits")
        ui, action = w.DWORD(255), w.DWORD(0)
        for kind, value, name in ((4, ui, "UI-FF"), (7, action, "TERMINATE_AT_END_OF_JOB")):
            self.n.check(self.n.SetInformationJobObject(self.job, kind, c.byref(value),
                                                       c.sizeof(value)), "job/" + name)
            actual, length = w.DWORD(), w.DWORD()
            self.n.check(self.n.QueryInformationJobObject(self.job, kind, c.byref(actual), 4,
                                                         c.byref(length)), "job/readback/" + name)
            if length.value != 4 or actual.value != value.value:
                raise ContractError(("job readback", name, actual.value))
        actual, length = JOB_EXTENDED(), w.DWORD()
        self.n.check(self.n.QueryInformationJobObject(self.job, 9, c.byref(actual), c.sizeof(actual),
                                                     c.byref(length)), "job limits readback")
        if (length.value != c.sizeof(actual) or actual.basic.flags != settings.basic.flags
                or actual.basic.active != 8 or actual.job_memory != 67108864
                or actual.basic.job_time != 50000000):
            raise ContractError("effective job limits")
        self.emit("U2", "job-configured", {"flags": actual.basic.flags, "active_limit": 8,
                                         "memory": actual.job_memory, "user_time_100ns": actual.basic.job_time,
                                         "ui": 255, "end_action": 0})

    def job_observation(self):
        accounting, size = JOB_ACCOUNTING(), w.DWORD()
        self.n.check(self.n.QueryInformationJobObject(self.job, 1, c.byref(accounting),
                                                     c.sizeof(accounting), c.byref(size)), "job accounting")
        data = c.create_string_buffer(8 + 8 * 8)
        self.n.check(self.n.QueryInformationJobObject(self.job, 3, data, len(data),
                                                     c.byref(size)), "job member list")
        assigned, count = w.DWORD.from_buffer(data).value, w.DWORD.from_buffer(data, 4).value
        if count > 8 or assigned != count or accounting.active != count:
            raise ContractError("job list cap/inconsistent census")
        members = [c.c_size_t.from_buffer(data, 8 + index * 8).value for index in range(count)]
        if self.pi and any(pid != self.pi.pid for pid in members):
            self.descendant_unknown = True
            self.emit("U2", "unexpected-descendant", {"P_observed_pids": members,
                      "identity_cessation": "UNAVAILABLE: no descendant handle; no PID reopen"})
            raise ContractError("unexpected job descendant")
        now = self.n.GetTickCount64()
        if members:
            self.last_active = now
        elif self.first_zero is None:
            self.first_zero = now
        self.job_zero = not members
        if now - self.last_sample >= 250:
            times = [w.FILETIME() for _ in range(4)]
            self.n.check(self.n.GetProcessTimes(self.n.GetCurrentProcess(),
                         *(c.byref(value) for value in times)), "P CPU times")
            memory, limits = MEMORY_COUNTERS(), JOB_EXTENDED()
            memory.size = c.sizeof(memory)
            self.n.check(self.n.K32GetProcessMemoryInfo(self.n.GetCurrentProcess(),
                         c.byref(memory), c.sizeof(memory)), "P resource sample")
            self.n.check(self.n.QueryInformationJobObject(self.job, 9, c.byref(limits),
                         c.sizeof(limits), c.byref(size)), "job charge sample")
            self.emit("U2", "resources", {"tick": now, "P_user_100ns": times[3].dwLowDateTime +
                      (times[3].dwHighDateTime << 32), "P_kernel_100ns": times[2].dwLowDateTime +
                      (times[2].dwHighDateTime << 32), "P_private_bytes": memory.private,
                      "P_working_set": memory.ws, "P_memory_OS_bounded": False,
                      "job_peak_charge": limits.peak_job_memory, "job_user_100ns": accounting.user,
                      "job_kernel_100ns": accounting.kernel, "active": accounting.active})
            self.last_sample = now
        return {"pids": members, "user_100ns": accounting.user, "kernel_100ns": accounting.kernel,
                "active": accounting.active, "tick": now}

    def inventory(self, process, name, retain=False):
        snapshot, marker = w.HANDLE(), w.HANDLE()
        result, duplicates = [], []
        error = self.n.PssCaptureSnapshot(process, 0x4 | 0x10, 0, c.byref(snapshot))
        if error:
            raise ApiError("PssCaptureSnapshot/" + name, error)
        try:
            error = self.n.PssWalkMarkerCreate(None, c.byref(marker))
            if error:
                raise ApiError("PssWalkMarkerCreate/" + name, error)
            while True:
                self.tick()
                entry = PSS_HANDLE_ENTRY()
                error = self.n.PssWalkSnapshot(snapshot, 2, marker, c.byref(entry), c.sizeof(entry))
                if error == 259:
                    break
                if error:
                    raise ApiError("PssWalkSnapshot/" + name, error)
                if len(result) == ENUM_LIMIT:
                    raise ContractError(("complete inventory cap", name))
                # BASIC flag is required; reserved PSS access fields are never consumed.
                if not entry.flags & 1:
                    raise ContractError("PSS basic information missing")
                original = entry.handle
                if process == self.n.GetCurrentProcess() and original == self.job:
                    duplicate = self.job  # The sole job handle MUST NOT be duplicated.
                    must_close = False
                else:
                    value = w.HANDLE()
                    self.n.check(self.n.DuplicateHandle(process, original, self.n.GetCurrentProcess(),
                                                        c.byref(value), 0, False, 2),
                                 "DuplicateHandle/" + name)
                    duplicate = self.own(value, "inventory reference/" + name)
                    duplicates.append(duplicate)
                    if retain:
                        self.references.append(duplicate)
                    must_close = True
                rights = self.n.rights(duplicate)
                item = {"handle": original, "snapshot_flags": entry.flags,
                        "original_object_attributes": entry.attributes, "type": entry.object_type,
                        "rights": rights, "reference": duplicate}
                self.retain_metadata("inventory/" + name + "/" + str(len(result)), item)
                result.append(item)
                self.emit("U3", name + "/entry", {key: value for key, value in item.items()
                                                if key != "reference"})
                if not retain and must_close:
                    self.close(duplicate)
                    duplicates.remove(duplicate)
            self.emit("U3", name + "/complete", {"count": len(result), "cap": ENUM_LIMIT,
                                               "checkpoint_tick": self.n.GetTickCount64(),
                                               "transient_leaks_excluded": False})
            return result
        finally:
            if not retain:
                for handle in duplicates:
                    self.close(handle)
            if marker:
                error = self.n.PssWalkMarkerFree(marker)
                if error:
                    self.errors.append(["PssWalkMarkerFree", error])
            error = self.n.PssFreeSnapshot(self.n.GetCurrentProcess(), snapshot)
            if error:
                self.errors.append(["PssFreeSnapshot", error])

    def compare_inventory(self, child, parent, writes, runtime, suspended=None):
        found = set()
        suspended = suspended or []
        for item in child:
            matches = [old["handle"] for old in parent
                       if self.n.CompareObjectHandles(item["reference"], old["reference"])]
            allowed_matches = set(matches).intersection(writes)
            if matches and not allowed_matches:
                self_query = (runtime and item["rights"]["object_type"] == "Token"
                              and item["rights"]["access"] == 8
                              and not item["original_object_attributes"] & 2
                              and self.child_token is not None
                              and self.n.CompareObjectHandles(item["reference"], self.child_token)
                              and not any(self.n.CompareObjectHandles(item["reference"], old["reference"])
                                          for old in suspended))
                if self_query:
                    self.emit("U3", "runtime", {"handle": item["handle"], "parent_matches": matches,
                              "classification": "RUNTIME_SELF_TOKEN_QUERY_NOT_INHERITED",
                              "actual_child_primary_token_compared": True, "access": 8})
                    continue
                raise ContractError(("unintended inherited parent object", item["handle"], matches))
            if allowed_matches:
                if len(allowed_matches) != 1 or any(value not in writes for value in matches):
                    # Parent read/write ends can be distinct file objects of one pipe.
                    # Only exact object identity is accepted, never a pipe-name guess.
                    raise ContractError(("ambiguous inherited object", matches))
                original = next(iter(allowed_matches))
                if not runtime and item["handle"] != original:
                    raise ContractError("suspended inherited handle value")
                access = item["rights"]["access"]
                expected_access = next(old["rights"]["access"] for old in parent
                                       if old["handle"] == original)
                if not access & 2 or access & 1 or access != expected_access:
                    raise ContractError(("pipe write rights", item["handle"], access))
                if not item["original_object_attributes"] & 2:
                    raise ContractError("original inherited write flag missing")
                found.add(original)
                classification = "INHERITED_ALLOWED_WRITE"
            else:
                classification = ("RUNTIME_OPEN" if runtime and not any(
                    self.n.CompareObjectHandles(item["reference"], old["reference"])
                    for old in suspended) else "SUSPENDED_NONPARENT_OBJECT")
            self.emit("U3", "runtime" if runtime else "suspended", {
                "handle": item["handle"], "parent_matches": matches, "classification": classification})
        if found != set(writes):
            raise ContractError(("missing allowed writes", sorted(found), writes))

    def identity(self, process):
        length, text = w.DWORD(32768), c.create_unicode_buffer(32768)
        self.n.check(self.n.QueryFullProcessImageNameW(process, 0, text, c.byref(length)), "image")
        times = [w.FILETIME() for _ in range(4)]
        self.n.check(self.n.GetProcessTimes(process, *(c.byref(value) for value in times)), "creation time")
        pid = self.n.GetProcessId(process)
        if not pid:
            raise ApiError("GetProcessId", c.get_last_error())
        if self.pi is not None and pid != self.pi.pid:
            raise ContractError("retained Low process/PID mismatch")
        if os.path.normcase(text.value) != os.path.normcase(IMAGE) or source_digest(text.value) != IMAGE_SHA256:
            raise ContractError("Low image/hash drift")
        return {"pid": pid, "creation_filetime": times[0].dwLowDateTime + (times[0].dwHighDateTime << 32),
                "image": text.value, "image_hash": IMAGE_SHA256, "observer": "P retained handle"}

    def create(self, token, writes, systemroot):
        sizes = c.c_size_t()
        c.set_last_error(0)
        ok = self.n.InitializeProcThreadAttributeList(None, 2, 0, c.byref(sizes))
        error = c.get_last_error()
        if ok or error != 122 or not 0 < sizes.value <= TOKEN_LIMIT:
            raise ApiError("attribute list sizing", (error, sizes.value))
        attributes = c.create_string_buffer(sizes.value)
        self.n.check(self.n.InitializeProcThreadAttributeList(attributes, 2, 0, c.byref(sizes)),
                     "attribute list initialize")
        try:
            handles, jobs = (w.HANDLE * 3)(*writes), (w.HANDLE * 1)(self.job)
            for key, array in ((0x20002, handles), (0x2000D, jobs)):
                self.n.check(self.n.UpdateProcThreadAttribute(attributes, 0, key, array,
                                                             c.sizeof(array), None, None),
                             "attribute HANDLE_LIST/JOB_LIST")
            startup = STARTUPINFOEX()
            startup.startup.cb = c.sizeof(startup)
            startup.startup.flags = 0x100
            startup.startup.stdin = None
            startup.startup.stdout, startup.startup.stderr = writes[:2]
            startup.attributes = c.addressof(attributes)
            sd = self.make_descriptor(XL).attributes
            block_text = environment(writes[2], systemroot)
            block = c.create_unicode_buffer(block_text, len(block_text))
            command_text = " ".join(quote(value) for value in (IMAGE, "-B", "-c", SYNTHETIC_LITERAL))
            if len(command_text) >= 32767:
                raise ContractError("Windows argv length")
            command = c.create_unicode_buffer(command_text)
            self.emit("controller", "BEFORE_LOW_ATTEMPT", {"attempt": 1, "flags": 0x8040C,
                      "handles": writes, "job_handle_transferred": False,
                      "literal_sha256": hashlib.sha256(SYNTHETIC_LITERAL.encode("ascii")).hexdigest().upper()})
            self.tick()
            self.attempted, self.create_result_known = True, False
            information = PROCESS_INFORMATION()
            ok = self.n.CreateProcessAsUserW(token, IMAGE, command, c.byref(sd), c.byref(sd),
                                            True, 0x8040C, block, ROOT, c.byref(startup),
                                            c.byref(information))
            error = c.get_last_error()
            self.create_result_known = True
            if ok:
                self.pi = information
                self.own(information.process, "Low process")
                self.own(information.thread, "Low initial thread")
            self.emit("controller", "CREATE_RESULT", {"ok": bool(ok), "error": 0 if ok else error,
                      "pid": information.pid if ok else None, "suspended": bool(ok)})
            if not ok:
                self.emit("controller", "NO_LOW_CREATED", {"creation_return": False, "error": error})
                raise ApiError("CreateProcessAsUserW", error)
        finally:
            self.n.DeleteProcThreadAttributeList(attributes)

    def accept_line(self, index, raw, systemroot, source):
        if not raw.isascii() or len(raw) > LOW_RECORD_LIMIT:
            raise ContractError("Low record length/encoding")
        record = json.loads(raw)
        name = ("stdout", "stderr", "ledger")[index]
        if (record.get("schema") != "L65-RP2-LOW-1" or record.get("nonce") != NONCE
                or record.get("pid") != self.pi.pid or record.get("stream") != name):
            raise ContractError("Low schema/nonce/stream/PID")
        phase = record.get("phase")
        if phase == "READY" and self.ready[index] is None and self.ends[index] is None:
            observation = record["observation"]
            expected = {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
                        "SYSTEMROOT": systemroot, "TPCN_LUNA65_LEDGER_HANDLE": str(self.writes[2])}
            if (observation["environment"] != expected or observation["cwd"] != ROOT
                    or observation["argv"] != ["-c"] or observation["executable"] != IMAGE
                    or observation["prefix"] != BASE or observation["base_prefix"] != BASE
                    or not observation["version"].startswith("3.11.4 ")
                    or observation["pytest_version"] != "9.0.2"
                    or observation["sys_path"] != ["", BASE + r"\python311.zip", BASE + r"\DLLs",
                                                   BASE + r"\Lib", BASE, BASE + r"\Lib\site-packages"]
                    or observation["console_window"] or observation["console_cp"]
                    or observation["stdio"][0]["handle"] != 0
                    or [entry["handle"] for entry in observation["stdio"][1:]] != self.writes
                    or any(entry["console_mode_ok"] for entry in observation["stdio"])
                    or any(entry["error"] != 6 for entry in observation["stdio"])):
                raise ContractError("Low runtime/environment/console observation")
            enforce_token(observation["token"], True, source, literal_observation=True)
            allowed_roots = [item[0].casefold() + "\\" for item in TREE_MANIFEST[1:]]
            allowed_files = {item.casefold() for item in INSPECTED_STARTUP}
            for module_name, origin, filename in observation["modules"]:
                for path in (origin, filename):
                    if path is None or path in ("built-in", "frozen"):
                        continue
                    normalized = os.path.normcase(os.path.abspath(path))
                    stdlib = normalized.startswith((BASE + r"\Lib" + "\\").casefold()) and not normalized.startswith(
                        (BASE + r"\Lib\site-packages" + "\\").casefold())
                    if (normalized not in allowed_files and not stdlib
                            and not any(normalized.startswith(root) for root in allowed_roots)):
                        raise ContractError(("module outside frozen closure", module_name, path))
            self.ready[index] = {key: value for key, value in record.items() if key != "observation"}
        elif phase == "END" and self.ready[index] is not None and self.ends[index] is None:
            if set(record) != {"schema", "nonce", "phase", "stream", "pid"}:
                raise ContractError("END exact schema")
            self.ends[index] = record
        else:
            raise ContractError("duplicate/reordered/unknown Low phase")

    def drain(self, systemroot, source):
        for index, worker in enumerate(self.workers):
            if worker.error is not None:
                raise ApiError("Low native reader", worker.error)
            if worker.discarded:
                raise ContractError("Low reader overflow")
            while worker.pending:
                chunk = worker.pending.pop(0)
                self.emit("capture", "LOW_BYTES", {"stream": ("stdout", "stderr", "ledger")[index],
                                                  "encoding": "hex", "length": len(chunk), "bytes": chunk.hex()})
                self.lines[index].extend(chunk)
                if len(self.lines[index]) > LOW_RECORD_LIMIT + 4096:
                    raise ContractError("Low partial line cap")
                while b"\n" in self.lines[index]:
                    self.reserve_parse(self.lines[index].find(b"\n"))
                    line, _, rest = self.lines[index].partition(b"\n")
                    self.lines[index] = bytearray(rest)
                    self.accept_line(index, bytes(line), systemroot, source)
            self.eofs[index] = worker.eof
            if worker.eof and self.lines[index]:
                raise ContractError("truncated Low record at EOF")

    def run(self, systemroot):
        self.emit("controller", "P0", {"P0": self.p0, "O0": self.o0, "outer_allowance_ms": 20000,
                  "source_hash": source_digest(__file__), "baseline": BASELINE,
                  "remote_representation_reservation": P_RETAINED_RESERVATION,
                  "wall_uptime_pair": self.wall_pair, "OS_version": list(sys.getwindowsversion()),
                  "pointer_bits": c.sizeof(c.c_void_p) * 8,
                  "literal_bytes": len(SYNTHETIC_LITERAL.encode("ascii")),
                  "literal_sha256": hashlib.sha256(SYNTHETIC_LITERAL.encode("ascii")).hexdigest().upper()})
        expected_path = [ROOT + r"\scripts", BASE + r"\python311.zip", BASE + r"\DLLs",
                         BASE + r"\Lib", BASE, BASE + r"\Lib\site-packages"]
        if sys.path != expected_path or sys.executable != IMAGE or os.getcwd() != ROOT:
            raise ContractDefect("Medium effective startup/image/cwd drift")
        self.n.no_impersonation()
        source, source_fields, source_sd = self.token(self.n.GetCurrentProcess(), SOURCE_TOKEN_ACCESS, "source")
        self.systemroot, self.source_fields = systemroot, source_fields
        enforce_token(source_fields, False)
        self.sections["U1"] = {"status": "IN_PROGRESS"}
        self.emit("U2", "closure", verify_closure(self.tick))
        ambient = w.BOOL()
        self.n.check(self.n.IsProcessInJob(self.n.GetCurrentProcess(), None, c.byref(ambient)),
                     "ambient job")
        self.emit("U2", "ambient-job", {"member": bool(ambient.value), "no_breakaway": True})
        self.configure_job()
        derived, derived_fields, derived_sd = self.restricted_token(source, source_fields)
        self.reads, self.writes = [], []
        for name in ("stdout", "stderr", "ledger"):
            read, write = w.HANDLE(), w.HANDLE()
            sd = self.make_descriptor(PL).attributes
            self.n.check(self.n.CreatePipe(c.byref(read), c.byref(write), c.byref(sd), 4096),
                         "CreatePipe/" + name)
            self.reads.append(self.own(read, "Low " + name + " read"))
            self.writes.append(self.own(write, "Low " + name + " write"))
            target_sd(self.n, read, "S-1-16-4096", True)
            target_sd(self.n, write, "S-1-16-4096", True)
            self.n.check(self.n.SetHandleInformation(write, 1, 1), "allowlist write inheritance")
            self.rights(read)
            rights = self.rights(write, inherit=True)
            if not rights["access"] & 2 or rights["access"] & 1:
                raise ContractError("creation pipe write access")
        sentinel_sd = self.make_descriptor(XM, True).attributes
        sentinel = self.own(self.n.CreateEventW(c.byref(sentinel_sd), True, False, None), "sentinel")
        self.rights(sentinel, 0x1F0003, True)
        target_sd(self.n, sentinel, "S-1-16-8192")
        parent = self.bounded_inventory(self.n.GetCurrentProcess(), "parent", retain=True)
        self.sections["U3"] = {"status": "IN_PROGRESS", "parent_count": len(parent)}
        self.create(derived, self.writes, systemroot)
        self.rights(self.pi.process, 0x1FFFFF)
        self.rights(self.pi.thread, 0x1FFFFF)
        if (self.n.rights(self.pi.process)["object_type"] != "Process"
                or self.n.rights(self.pi.thread)["object_type"] != "Thread"):
            raise ContractError("creation-returned process/thread handle types")
        self.emit("U2", "Low-identity", self.identity(self.pi.process))
        for name, handle in (("process", self.pi.process), ("initial-thread", self.pi.thread)):
            self.emit("U1", "Low-" + name + "-SD", target_sd(self.n, handle, "S-1-16-4096"))
        member = w.BOOL()
        self.n.check(self.n.IsProcessInJob(self.pi.process, self.job, c.byref(member)), "Low membership")
        self.member = bool(member.value)
        if not self.member or self.job_observation()["pids"] != [self.pi.pid]:
            raise ContractError("creation-time sole-job admission")
        child_token, child_fields, child_sd = self.token(self.pi.process, QUERY_TOKEN_ACCESS, "child-suspended")
        self.child_token = child_token
        enforce_token(child_fields, True, source_fields)
        suspended = self.bounded_inventory(self.pi.process, "suspended", retain=True)
        self.compare_inventory(suspended, parent, self.writes, False)
        for read in self.reads:
            worker = NativeReader(self, read)
            self.workers.append(worker)
            worker.start()
        # Original writes close before resume. Noninheritable observation
        # duplicates exist only through the READY comparison and close before
        # any EOF assertion. They are explicitly accounted and inventoried.
        for write in self.writes:
            self.close(write)
        self.drift(source, source_sd, "source")
        self.drift(derived, derived_sd, "derived")
        self.drift(child_token, child_sd, "child-suspended")
        self.tick()
        previous = self.n.ResumeThread(self.pi.thread)
        if previous == 0xFFFFFFFF:
            raise ApiError("ResumeThread", c.get_last_error())
        if previous != 1:
            raise ContractError(("initial suspend count", previous))
        self.resumed = True
        runtime_done = False
        while True:
            self.tick()
            self.drain(systemroot, source_fields)
            if all(self.ready) and not runtime_done:
                if any(self.ends):
                    raise IncompleteObservation("READY checkpoint missed")
                token, fields, sd = self.token(self.pi.process, QUERY_TOKEN_ACCESS, "child-READY")
                same_token = bool(self.n.CompareObjectHandles(token, child_token))
                self.emit("U1", "child-READY/admitted-token-binding",
                          {"same_object": same_token, "admitted_reference": child_token,
                           "READY_reference": token})
                if not same_token:
                    raise ContractError("READY child token differs from admitted token object")
                enforce_token(fields, True, source_fields)
                self.drift(token, child_sd, "child-READY/admitted-SD")
                runtime = self.bounded_inventory(self.pi.process, "READY", retain=True)
                self.drain(systemroot, source_fields)
                if any(self.ends):
                    raise IncompleteObservation("END observed before READY checkpoint completed")
                self.compare_inventory(runtime, parent, self.writes, True, suspended)
                self.drift(child_token, child_sd, "child-suspended/after-runtime-comparison")
                self.drift(token, child_sd, "child-READY/after-runtime-comparison")
                self.close(token)
                self.close(child_token)
                runtime_done = True
                self.runtime_done = True
                for handle in list(self.references):
                    self.close(handle)
                self.references.clear()
                self.sections["U1"] = {"status": "COMPLETE"}
                self.sections["U3"] = {"status": "COMPLETE", "finite_checkpoints_only": True}
            state = self.job_observation()
            wait = self.n.WaitForSingleObject(self.pi.process, 0)
            if wait == 0xFFFFFFFF:
                raise ApiError("Low wait", c.get_last_error())
            if wait not in (0, 258):
                raise ApiError("Low unexpected wait", wait)
            if wait == 0:
                self.root_signalled = True
                exit_code = w.DWORD()
                self.n.check(self.n.GetExitCodeProcess(self.pi.process, c.byref(exit_code)), "Low exit code")
                self.exit_code = exit_code.value
                if self.f is None:
                    self.f = self.n.GetTickCount64()
                if state["active"] == 0:
                    break
                raise ContractError("root terminal outcome with outstanding job members")
            time.sleep(0.025)
        self.sections["U2"] = {"status": "COMPLETE" if all(self.ends) and runtime_done else "INCOMPLETE"}
        if self.exit_code != 0:
            raise ContractError("nonzero Low exit")

    def bounded_inventory(self, process, name, retain=False):
        state = {"result": None, "error": None}
        def action():
            try:
                state["result"] = self.inventory(process, name, retain)
            except Exception as error:
                state["error"] = error
        worker = NativeWorker(self, action)
        worker.start()
        while True:
            wait = self.n.WaitForSingleObject(worker.handle, 0)
            if wait == 0:
                break
            if wait == 0xFFFFFFFF:
                raise ApiError("inventory worker wait/" + name, c.get_last_error())
            if wait != 258:
                raise ApiError("inventory worker unexpected wait/" + name, wait)
            self.tick()
            time.sleep(0.025)
        worker.joined = True
        if state["error"] is not None:
            raise state["error"]
        if state["result"] is None:
            raise ContractError("inventory worker did not produce result")
        return state["result"]

    def cleanup(self):
        if self.f is None:
            self.f = self.n.GetTickCount64()
        if not self.pi and self.create_result_known:
            self.cleanup_emit("NO_LOW_CREATED", {"attempted": self.attempted,
                                                 "constructor_did_not_create_L": True})
        self.cleanup_emit("CLEANUP_BEGIN", {"F": self.f, "deadline": self.cleanup_end(),
                  "attempted": self.attempted, "create_result_known": self.create_result_known})
        if self.pi:
            if self.job and not self.job_zero:
                ok = self.n.TerminateJobObject(self.job, STOP_CODE)
                error = c.get_last_error()
                self.cleanup_emit("JOB_TERMINATION_REQUEST", {"ok": bool(ok), "error": 0 if ok else error})
                if not ok:
                    self.errors.append(["TerminateJobObject", error])
            if not self.member and not self.root_signalled:
                ok = self.n.TerminateProcess(self.pi.process, STOP_CODE)
                error = c.get_last_error()
                self.cleanup_emit("SUSPENDED_ROOT_TERMINATION_REQUEST",
                                  {"ok": bool(ok), "error": 0 if ok else error})
                if not ok:
                    self.errors.append(["TerminateProcess/suspended root", error])
        inventory_quiescent = True
        for worker in NativeWorker.instances(self):
            if isinstance(worker, NativeReader) or worker.handle is None or worker.joined:
                continue
            remaining = max(0, self.cleanup_end() - self.n.GetTickCount64())
            worker.joined = self.n.WaitForSingleObject(worker.handle, min(remaining, 100)) == 0
            inventory_quiescent = inventory_quiescent and worker.joined
        if inventory_quiescent:
            for handle in list(self.references):
                self.cleanup_close(handle)
            self.references.clear()
            for handle, name in list(self.owned.items()):
                if name.endswith(" write"):
                    self.cleanup_close(handle)
        while self.n.GetTickCount64() < self.cleanup_end():
            if self.pi:
                wait = self.n.WaitForSingleObject(self.pi.process, 0)
                if wait == 0:
                    self.root_signalled = True
                    code = w.DWORD()
                    if self.n.GetExitCodeProcess(self.pi.process, c.byref(code)):
                        self.exit_code = code.value
                    else:
                        self.errors.append(["GetExitCodeProcess/cleanup", c.get_last_error()])
                elif wait == 0xFFFFFFFF:
                    self.errors.append(["cleanup wait", c.get_last_error()])
                elif wait != 258:
                    self.errors.append(["cleanup unexpected wait", wait])
                if self.job:
                    try:
                        self.job_observation()
                    except (ApiError, ContractError) as error:
                        self.errors.append(["cleanup job query", str(error)])
            if self.workers:
                try:
                    self.drain(self.systemroot, self.source_fields)
                except (ApiError, ContractError, ValueError, KeyError) as error:
                    self.errors.append(["cleanup stream", str(error)])
                    for index, worker in enumerate(self.workers):
                        worker.discarded = min(0xFFFFFFFFFFFFFFFF,
                                               worker.discarded + worker.pending_size + len(self.lines[index]))
                        worker.pending.clear()
                        self.lines[index].clear()
                        self.eofs[index] = worker.eof
            if (not self.pi or self.root_signalled and self.job_zero) and (
                    not self.workers or all(self.eofs)):
                break
            time.sleep(0.025)
        for worker in NativeWorker.instances(self):
            if worker.handle is None:
                worker.joined = True
                continue
            if isinstance(worker, NativeReader):
                worker.stop_requested = True
            if self.n.WaitForSingleObject(worker.handle, 0) != 0:
                ok = self.n.CancelSynchronousIo(worker.handle)
                error = c.get_last_error()
                if not ok and error != 1168:
                    self.errors.append(["CancelSynchronousIo", error])
                remaining = max(0, self.cleanup_end() - self.n.GetTickCount64())
                worker.joined = self.n.WaitForSingleObject(worker.handle, min(remaining, 100)) == 0
            else:
                worker.joined = True
            if worker.joined:
                self.cleanup_close(worker.handle)
        outstanding = [worker.handle for worker in NativeWorker.instances(self) if not worker.joined]
        # Never invalidate memory/pipe/SD storage still referenced by a native worker.
        if not outstanding:
            for handle, name in list(self.owned.items()):
                if handle != self.job:
                    self.cleanup_close(handle)
            for descriptor in self.descriptors:
                try:
                    descriptor.close()
                except Exception as error:
                    self.errors.append(["descriptor closure", getattr(error, "code", None), str(error)])
        if self.job and not outstanding:
            self.cleanup_close(self.job)  # Last owned kernel object; never a duplicate.
            if self.job not in self.owned:
                self.job = None
        if self.pi and all(self.ready) and all(self.ends) and self.exit_code == 0 and self.runtime_done:
            self.sections["U2"] = {"status": "COMPLETE"}
        cessation = (not self.descendant_unknown and self.create_result_known and (not self.pi or
                     self.root_signalled and self.job_zero and all(self.eofs)) and not outstanding
                     and not self.owned and not any(sd.pointer.value for sd in self.descriptors))
        verdict = ("RP2_UNKNOWN_FAIL_CLOSED" if not cessation else
                   "RP2_CONTRACT_DEFECT" if self.contract_defect else
                   "RP2_PARTIAL" if self.partial and not self.errors else
                   "RP2_FAIL" if self.errors else
                   "RP2_PASS" if self.pi and all(value["status"] == "COMPLETE" for value in self.sections.values())
                   else "RP2_PARTIAL")
        self.emit("controller", "FINAL", {"verdict": verdict, "U1_U2_U3": self.sections,
                  "Low_created": bool(self.pi), "Low_signalled": self.root_signalled,
                  "cessation_confirmed": cessation, "descendant_cessation_unknown": self.descendant_unknown,
                  "Low_exit": self.exit_code, "job_zero": self.job_zero, "Low_EOF": self.eofs,
                  "Low_discarded_bytes": [worker.discarded for worker in self.workers],
                  "Low_reader_errors": [worker.error for worker in self.workers],
                  "outstanding_workers": outstanding, "owned_remaining": self.owned,
                  "job_close_deferred_for_live_workers": bool(self.job),
                  "first_zero": self.first_zero, "last_active": self.last_active,
                  "P_highwater": self.highwater, "P_payload_sent": self.sent,
                  "P_retained_metadata_bytes": sum(self.metadata_sizes.values()),
                  "errors": self.errors, "omitted_bounded_diagnostics": self.errors.omitted,
                  "observation_stop_reason": self.stop_reason,
                  "end_tick": self.n.GetTickCount64(),
                  "alert": ("Containment remains unresolved; an unconfirmed Low child/descendant may still be active. "
                            "No retry or downstream progression authorized.") if not cessation else None,
                  "scientific_claim": "synthetic finite U1-U3 only; no production/venv/supervisor qualification"})
        return 0 if verdict == "RP2_PASS" else 3


class NativeWorker:
    registry = []

    def __init__(self, controller, action):
        self.controller, self.action = controller, action
        self.handle = None
        self.joined = False
        self.running = False
        self.callback = THREADPROC(self.entry)
        self.error = None
        self.registry.append(self)

    @classmethod
    def instances(cls, controller):
        return [worker for worker in cls.registry if worker.controller is controller]

    def entry(self, unused):
        self.running = True
        try:
            self.action()
            return 0
        except Exception as error:
            if self.controller.f is None:
                self.controller.f = self.controller.n.GetTickCount64()
            self.error = [type(error).__name__, str(error)]
            return 1

    def start(self):
        owner = self.controller
        sd = owner.make_descriptor(XM).attributes
        tid = w.DWORD()
        self.handle = owner.own(owner.n.CreateThread(c.byref(sd), 0, self.callback, None,
                                                     0x4, c.byref(tid)), "native worker")
        owner.rights(self.handle, 0x1FFFFF)
        if owner.n.rights(self.handle)["object_type"] != "Thread":
            raise ContractError("native reader handle type")
        target_sd(owner.n, self.handle, "S-1-16-8192")
        previous = owner.n.ResumeThread(self.handle)
        if previous == 0xFFFFFFFF:
            raise ApiError("native worker resume", c.get_last_error())
        if previous != 1:
            raise ContractError(("native worker suspend count", previous))
        while not self.running:
            owner.tick()
            time.sleep(0.001)
        if self.error is not None:
            raise ApiError("native worker readiness", self.error)


class NativeReader(NativeWorker):
    def __init__(self, controller, read):
        self.read, self.pending = read, []
        self.discarded, self.eof = 0, False
        self.stop_requested = False
        super().__init__(controller, self.read_loop)

    @property
    def pending_size(self):
        return sum(map(len, tuple(self.pending)))

    def read_loop(self):
        buffer = c.create_string_buffer(4096)
        n = self.controller.n
        while True:
            while self.pending_size + len(buffer) > RECORD_LIMIT:
                if self.stop_requested:
                    return
                time.sleep(0.001)
            if self.stop_requested:
                return
            count = w.DWORD()
            ok = n.ReadFile(self.read, buffer, len(buffer), c.byref(count), None)
            error = c.get_last_error()
            if not ok:
                if error == 109:
                    self.eof = True
                    return
                raise ApiError("ReadFile", error)
            if not count.value:
                self.eof = True
                return
            if count.value > len(buffer):
                raise ContractError("native reader returned length")
            self.pending.append(buffer.raw[:count.value])


def main():
    epoch = c.WinDLL("kernel32.dll", use_last_error=True)
    epoch.GetTickCount64.restype, epoch.GetTickCount64.argtypes = c.c_uint64, []
    p0 = epoch.GetTickCount64()  # First entry epoch; never a Python stopwatch.
    n = Native()
    if (len(sys.argv) != 5 or sys.argv[1] != "--rp2"
            or sys.argv[2] != NONCE or not sys.argv[3].isascii()
            or not sys.argv[3].isdecimal() or sys.argv[4] != "20000"):
        raise ContractDefect("frozen Medium argv/deadline grammar")
    o0 = int(sys.argv[3])
    if str(o0) != sys.argv[3] or not 0 <= o0 <= p0 or p0 >= o0 + 20000:
        raise ContractDefect("future/expired/ambiguous O0")
    if set(os.environ) != {"PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "SYSTEMROOT"}:
        raise ContractDefect("Medium environment cardinality")
    if os.environ["PYTHONHASHSEED"] != "0" or os.environ["PYTHONDONTWRITEBYTECODE"] != "1":
        raise ContractDefect("Medium environment values")
    controller = Controller(n, NONCE, o0, p0)
    try:
        controller.run(os.environ["SYSTEMROOT"])
    except Exception as error:
        if controller.f is None:
            controller.f = n.GetTickCount64()
        controller.contract_defect = isinstance(error, ContractDefect)
        status = getattr(error, "code", None)
        unsupported = (isinstance(error, ApiError) and
                       (error.stage.startswith("Pss") and status in (50, 120)
                        or error.stage.startswith("NtQueryObject") and isinstance(status, dict)
                        and status.get("status", 0) & 0xFFFFFFFF in (0xC0000002, 0xC00000BB)))
        controller.partial = isinstance(error, IncompleteObservation) or unsupported
        controller.stop_reason = {"type": type(error).__name__,
                                  "stage": getattr(error, "stage", "controller"),
                                  "code": status, "message": str(error)[:512]}
        if not controller.partial:
            controller.errors.append([type(error).__name__, getattr(error, "stage", "controller"),
                                      getattr(error, "code", None), str(error)])
        for value in controller.sections.values():
            if value["status"] != "COMPLETE":
                value.update(status="INCOMPLETE", reason=str(error)[:512])
    try:
        return controller.cleanup()
    except Exception as error:
        # O cannot trust missing FINAL. Exit closes the sole job, a request only.
        sys.stderr.write("RP2_UNKNOWN_FAIL_CLOSED: cleanup/report failure: " + repr(error) +
                         "; containment remains unresolved; Low may survive; no downstream progression.\n")
        return 3


if __name__ == "__main__":
    sys.exit(main())
