<#
Luna-65 Phase 2A S1-B attended execution wrapper (Windows PowerShell 5.1).
Gate: L65-PHASE2A-S1B-EXECUTION-CONTRACT-V1, contract section 4 and 5.

Launches exactly one invocation of the frozen sizing generator under attended,
best-effort supervision. It does NOT create a Job Object, measure CPU or memory,
or establish whole-process-tree termination: taskkill /T /F is a best-effort
request. The 30 s CPU and 30 s wall budgets are the generator's own cooperative
guards. Same-user tampering is not excluded. Run only under an explicit owner
execution authorization that names the run id and the identities bound below.
Nothing in this file authorizes execution.

Usage (operator, attended):
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File <this file> -RunId <run-id>   -ExpectedVerifierSha256 <hex> -ExpectedWrapperSha256 <hex>
#>
param(
    [Parameter(Mandatory = $true)][string]$RunId,
    [Parameter(Mandatory = $true)]    [string]$ExpectedVerifierSha256,
        [Parameter(Mandatory = $true)][string]$ExpectedWrapperSha256
    )

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$Interpreter = 'C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe'
$InterpreterSha256 = '4fb049eeddd221e5470cd33177299dd13f85eba25beef7aced7a0890ad85181f'
$RepoRoot = 'C:\Users\Patrick\Documents\ActiveCode\TPCN'
$Generator = Join-Path $RepoRoot 'scripts\luna65_phase2a_ledger_sizing.py'
$GeneratorSha256 = 'dd2a3df5d51f234b9a90f8c58f69ed84cdd02dc5b9379b1d19a71cb15d719212'
$GeneratorBlob = '088d569c1787e08e3995d10d94aade8517093093'
$Contract = Join-Path $RepoRoot 'workflow\docs\luna\LUNA_65_PHASE2A_S1B_EXECUTION_CONTRACT.md'
$ContractBlob = 'b251e3d09d7e12d1008b34ec3e8c3dd2dbd6e3a2'
$Verifier = Join-Path $RepoRoot 'scripts\luna65_phase2a_ledger_sizing_verifier.py'
$EvidenceParent = 'C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\phase2a-sizing'
$WaitMs = 45000
$CleanupMs = 10000
$TextLimit = 4096
$WrapperJsonMax = 16384
$RetainedCap = 1048576
$MinFreeBytes = 2GB

function Get-Sha256Hex([string]$Path) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return (-join ($hasher.ComputeHash([IO.File]::ReadAllBytes($Path)) | ForEach-Object { $_.ToString('x2') })) }
    finally { $hasher.Dispose() }
}

function Get-GitBlobHex([string]$Path) {
    $bytes = [IO.File]::ReadAllBytes($Path)
    $body = New-Object IO.MemoryStream
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        if ($bytes[$i] -eq 13 -and ($i + 1) -lt $bytes.Length -and $bytes[$i + 1] -eq 10) { continue }
        $body.WriteByte($bytes[$i])
    }
    $header = [Text.Encoding]::ASCII.GetBytes('blob ' + $body.Length + [char]0)
    $all = New-Object IO.MemoryStream
    $all.Write($header, 0, $header.Length)
    $all.Write($body.ToArray(), 0, [int]$body.Length)
    $sha1 = [Security.Cryptography.SHA1]::Create()
    try { return (-join ($sha1.ComputeHash($all.ToArray()) | ForEach-Object { $_.ToString('x2') })) }
    finally { $sha1.Dispose() }
}

function Limit-Text([string]$Text, [int]$Limit) {
    if ($null -eq $Text) { return @('', $false) }
    if ($Text.Length -gt $Limit) { return @($Text.Substring(0, $Limit), $true) }
    return @($Text, $false)
}

function Get-Children([int]$ParentPid) {
    try {
        $rows = @(Get-CimInstance -ClassName Win32_Process -Filter ('ParentProcessId=' + $ParentPid) -OperationTimeoutSec 2)
        $entries = @()
        foreach ($row in ($rows | Select-Object -First 8)) {
            $name = [string]$row.Name
            if ($name.Length -gt 64) { $name = $name.Substring(0, 64) }
            $entries += , @{ pid = [int]$row.ProcessId; parent_pid = [int]$row.ParentProcessId; name = $name }
        }
        return @{ count = $rows.Count; truncated = ($rows.Count -gt 8); entries = $entries }
    }
    catch {
        return @{ count = -1; truncated = $false; entries = @() }
    }
}

function ConvertTo-CanonicalJson($Value) {
    if ($null -eq $Value) { return 'null' }
    if ($Value -is [bool]) { if ($Value) { return 'true' } else { return 'false' } }
    if ($Value -is [int] -or $Value -is [long]) { return ([string]$Value) }
    if ($Value -is [string]) {
        $sb = New-Object Text.StringBuilder
        [void]$sb.Append('"')
        foreach ($ch in $Value.ToCharArray()) {
            $c = [int]$ch
            if ($c -eq 34) { [void]$sb.Append('\"') }
            elseif ($c -eq 92) { [void]$sb.Append('\\') }
            elseif ($c -eq 10) { [void]$sb.Append('\n') }
            elseif ($c -eq 13) { [void]$sb.Append('\r') }
            elseif ($c -eq 9) { [void]$sb.Append('\t') }
            elseif ($c -eq 8) { [void]$sb.Append('\b') }
            elseif ($c -eq 12) { [void]$sb.Append('\f') }
            elseif ($c -lt 32 -or $c -gt 126) { [void]$sb.Append('\u' + $c.ToString('x4')) }
            else { [void]$sb.Append($ch) }
        }
        [void]$sb.Append('"')
        return $sb.ToString()
    }
    if ($Value -is [Collections.IDictionary]) {
        $keys = @($Value.Keys | ForEach-Object { [string]$_ })
        [Array]::Sort($keys, [StringComparer]::Ordinal)
        $parts = @()
        foreach ($k in $keys) { $parts += ((ConvertTo-CanonicalJson $k) + ':' + (ConvertTo-CanonicalJson $Value[$k])) }
        return '{' + ($parts -join ',') + '}'
    }
    if ($Value -is [Collections.IEnumerable]) {
        $parts = @()
        foreach ($item in $Value) { $parts += (ConvertTo-CanonicalJson $item) }
        return '[' + ($parts -join ',') + ']'
    }
    throw 'unsupported value type for canonical JSON'
}

function ConvertTo-CanonicalBytes($Value) {
    return ,((New-Object Text.UTF8Encoding($false)).GetBytes((ConvertTo-CanonicalJson $Value) + "`n"))
}

function Write-State([string]$Message) {
    Write-Host ('[' + [DateTime]::UtcNow.ToString('o') + '] ' + $Message)
}

# ---------------------------------------------------------------- preflight (no side effects)
$RunRoot = Join-Path $EvidenceParent $RunId
$WrapperDir = Join-Path $EvidenceParent ($RunId + '.wrapper')
$WrapperPath = $PSCommandPath
try {
    if ($RunId -notmatch '^\d{8}T\d{6}Z-[0-9a-f]{7}$') { throw 'run id must be <UTC yyyymmddThhmmssZ>-<7 hex>' }
    if ($ExpectedVerifierSha256 -notmatch '^[0-9a-fA-F]{64}$') { throw 'verifier SHA-256 must be 64 hex characters' }
    if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'Windows PowerShell 5.1 required' }
    if (@(Get-ChildItem Env: | Where-Object { $_.Name -like 'PYTHON*' -or $_.Name -like 'TPCN_*' }).Count -ne 0) { throw 'PYTHON* or TPCN_* environment variable present' }
    if ((Get-Sha256Hex $Interpreter) -ne $InterpreterSha256) { throw 'interpreter SHA-256 mismatch' }
    if ((Get-Sha256Hex $Generator) -ne $GeneratorSha256) { throw 'generator SHA-256 mismatch' }
    if ((Get-GitBlobHex $Generator) -ne $GeneratorBlob) { throw 'generator Git blob mismatch' }
    if ((Get-GitBlobHex $Contract) -ne $ContractBlob) { throw 'S1-B contract Git blob mismatch' }
    if ((Get-Sha256Hex $Verifier) -ne $ExpectedVerifierSha256.ToLowerInvariant()) { throw 'verifier SHA-256 mismatch' }
    if (-not [IO.Directory]::Exists($EvidenceParent)) { throw 'evidence parent must be pre-created' }
    if (@(Get-ChildItem -LiteralPath $EvidenceParent -Force).Count -ne 0) { throw 'evidence parent must be empty (single attempt)' }
    if ([IO.Directory]::Exists($RunRoot) -or [IO.File]::Exists($RunRoot)) { throw 'output directory must be absent' }
    if ([IO.Directory]::Exists($WrapperDir) -or [IO.File]::Exists($WrapperDir)) { throw 'wrapper directory must be absent' }
    if (([IO.DriveInfo]'C').AvailableFreeSpace -lt $MinFreeBytes) { throw 'less than 2 GiB free on C:' }
    if ($ExpectedWrapperSha256 -notmatch '^[0-9a-fA-F]{64}$') { throw 'wrapper SHA-256 must be 64 hex characters' }
    $WrapperSha256 = Get-Sha256Hex $WrapperPath
    if ($WrapperSha256 -ne $ExpectedWrapperSha256.ToLowerInvariant()) { throw 'wrapper SHA-256 mismatch' }
}
catch {
    Write-Host ('PREFLIGHT FAILED (no invocation consumed): ' + $_.Exception.Message)
    exit 20
}

Write-State ('Preflight passed. Run id ' + $RunId + '. Wrapper SHA-256 ' + $WrapperSha256)
Write-State 'Attended best-effort supervision: no Job Object, memory unmeasured, tree termination not guaranteed.'
$answer = Read-Host ('Type RUN ' + $RunId + ' to consume the single invocation')
if ($answer -ne ('RUN ' + $RunId)) {
    Write-Host 'Not confirmed (no invocation consumed).'
    exit 21
}

$ArgumentString = '-I -B "' + $Generator + '" --output-dir "' + $RunRoot + '"'
$S = [ordered]@{
    schema                       = 'luna65-s1b-wrapper-v1'
    run_id                       = $RunId
    invocation_count             = 1
    wrapper_sha256               = $WrapperSha256
    verifier_sha256              = $ExpectedVerifierSha256.ToLowerInvariant()
    generator_sha256             = $GeneratorSha256
    generator_blob               = $GeneratorBlob
    contract_blob                = $ContractBlob
    interpreter_path             = $Interpreter
    interpreter_sha256           = $InterpreterSha256
    powershell_version           = $PSVersionTable.PSVersion.ToString()
    arguments                    = $ArgumentString
    working_directory            = $RepoRoot
    wait_ms                      = $WaitMs
    cleanup_window_ms            = $CleanupMs
    pid                          = $null
    parent_pid                   = $null
    start_utc                    = ''
    exit_utc                     = $null
    process_start_time_utc       = ''
    exited_within_wait           = $false
    elapsed_ms_at_exit           = $null
    termination_requested        = $false
    termination_request_elapsed_ms = $null
    taskkill_exit_code           = $null
    cessation_confirmed          = $false
    cessation_elapsed_ms         = $null
    children_before_termination  = $null
    children_after_exit          = @{ count = -1; truncated = $false; entries = @() }
    exit_code                    = $null
    stdout                       = ''
    stdout_truncated             = $false
    stderr                       = ''
    stderr_truncated             = $false
    output_dir_total_bytes       = $null
    retained_upper_bound_bytes   = $null
    final_state                  = 'UNKNOWN_FAIL_CLOSED'
    failure_reason               = 'not completed'
}

# ---------------------------------------------------------------- single-invocation lock
$LockPath = Join-Path $WrapperDir 'invocation.lock'
$LockBytes = 0
$Process = $null
$StartTimeUtc = $null
$Stopwatch = $null
$OutTask = $null
$ErrTask = $null

function Request-Termination {
    $S.termination_requested = $true
    $S.termination_request_elapsed_ms = $Stopwatch.ElapsedMilliseconds
    $S.children_before_termination = Get-Children $S.pid
    Write-State ('Termination requested for PID ' + $S.pid + ' (taskkill /T /F, best effort)')
    $tk = Start-Process -FilePath (Join-Path $env:SystemRoot 'System32\taskkill.exe') -ArgumentList @('/PID', [string]$S.pid, '/T', '/F')     -WindowStyle Hidden -PassThru
        if ($tk.WaitForExit(5000)) { $S.taskkill_exit_code = $tk.ExitCode } else { $S.taskkill_exit_code = -1; Write-State 'taskkill did not return within 5000 ms; continuing fail-closed' }
    $remaining = [int][Math]::Max(0, $CleanupMs - ($Stopwatch.ElapsedMilliseconds - $S.termination_request_elapsed_ms))
    $gone = $Process.WaitForExit($remaining)
    $S.cessation_elapsed_ms = $Stopwatch.ElapsedMilliseconds
    $stillThere = @(Get-Process -Id $S.pid -ErrorAction SilentlyContinue | Where-Object { $_.StartTime.ToUniversalTime() -eq $StartTimeUtc })
    $left = $CleanupMs - ($Stopwatch.ElapsedMilliseconds - $S.termination_request_elapsed_ms)
    if ($left -ge 2000) { $S.children_after_exit = Get-Children $S.pid }
    else { $S.children_after_exit = @{ count = -1; truncated = $false; entries = @() }; Write-State 'cleanup deadline exhausted; post-exit child snapshot skipped (fail-closed)' }
    $S.cessation_confirmed = ($gone -and $stillThere.Count -eq 0 -and $S.children_after_exit['count'] -eq 0)
    Write-State ('Cessation confirmed: ' + $S.cessation_confirmed)
}

try {
    [void][IO.Directory]::CreateDirectory($WrapperDir)
    $lockBody = ConvertTo-CanonicalBytes @{ schema = 'luna65-s1b-lock-v1'; run_id = $RunId; utc = [DateTime]::UtcNow.ToString('o'); wrapper_sha256 = $WrapperSha256 }
    $lockStream = New-Object IO.FileStream($LockPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
    try { $lockStream.Write($lockBody, 0, $lockBody.Length) } finally { $lockStream.Dispose() }
    $LockBytes = $lockBody.Length
    Write-State 'Invocation lock created; invocation consumed. Zero retries.'

    # ------------------------------------------------------------ launch
    $psi = New-Object Diagnostics.ProcessStartInfo
    $psi.FileName = $Interpreter
    $psi.Arguments = $ArgumentString
    $psi.WorkingDirectory = $RepoRoot
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.StandardOutputEncoding = [Text.Encoding]::UTF8
    $psi.StandardErrorEncoding = [Text.Encoding]::UTF8

    $S.start_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ', [Globalization.CultureInfo]::InvariantCulture)
    $Stopwatch = [Diagnostics.Stopwatch]::StartNew()
    $Process = [Diagnostics.Process]::Start($psi)
    $S.pid = $Process.Id
    $StartTimeUtc = $Process.StartTime.ToUniversalTime()
    $S.process_start_time_utc = $StartTimeUtc.ToString('o')
    $OutTask = $Process.StandardOutput.ReadToEndAsync()
    $ErrTask = $Process.StandardError.ReadToEndAsync()
    $S.parent_pid = [int]$PID
    Write-State ('Started PID ' + $S.pid + '; waiting at most ' + $WaitMs + ' ms')

    # ------------------------------------------------------------ finite wait
    $exited = $Process.WaitForExit($WaitMs)
    if ($exited) {
        $S.exited_within_wait = $true
        $S.elapsed_ms_at_exit = $Stopwatch.ElapsedMilliseconds
        $S.exit_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ', [Globalization.CultureInfo]::InvariantCulture)
        $S.exit_code = $Process.ExitCode
        $S.children_after_exit = Get-Children $S.pid
        [void]([Threading.Tasks.Task]::WaitAll(@($OutTask, $ErrTask), 5000))
        $streamsDone = ($OutTask.IsCompleted -and $ErrTask.IsCompleted)
        if ($OutTask.IsCompleted) { $t = Limit-Text $OutTask.Result $TextLimit; $S.stdout = $t[0]; $S.stdout_truncated = $t[1] }
        if ($ErrTask.IsCompleted) { $t = Limit-Text $ErrTask.Result $TextLimit; $S.stderr = $t[0]; $S.stderr_truncated = $t[1] }
        $outTotal = [int64]0
        if ([IO.Directory]::Exists($RunRoot)) {
            foreach ($f in @(Get-ChildItem -LiteralPath $RunRoot -Recurse -Force -File)) { $outTotal += $f.Length }
        }
        $S.output_dir_total_bytes = $outTotal
        $S.retained_upper_bound_bytes = $outTotal + $LockBytes + $WrapperJsonMax
        if ($S.children_after_exit['count'] -ne 0) { $S.failure_reason = 'child process observed or unknown after exit' }
        elseif (-not $streamsDone) { $S.failure_reason = 'stdout/stderr capture incomplete' }
        elseif ($S.retained_upper_bound_bytes -gt $RetainedCap) { $S.failure_reason = 'retained evidence contract conflict: generator output plus wrapper artifacts exceed 1,048,576 bytes' }
        else { $S.final_state = 'COMPLETED'; $S.failure_reason = '' }
    }
    else {
        Write-State 'Outer wait expired.'
        Request-Termination
        $S.exit_code = if ($Process.HasExited) { $Process.ExitCode } else { $null }
        if ($ErrTask.IsCompleted) { $t = Limit-Text $ErrTask.Result $TextLimit; $S.stderr = $t[0]; $S.stderr_truncated = $t[1] }
        if ($OutTask.IsCompleted) { $t = Limit-Text $OutTask.Result $TextLimit; $S.stdout = $t[0]; $S.stdout_truncated = $t[1] }
        if ($S.cessation_confirmed) { $S.final_state = 'OUTER_TIMEOUT_TERMINATED'; $S.failure_reason = 'outer 45 s wait expired; process ceased after termination request' }
        else { $S.failure_reason = 'outer 45 s wait expired; cessation not confirmed' }
    }
}
catch {
    $S.final_state = 'UNKNOWN_FAIL_CLOSED'
    $reason = [string]$_.Exception.Message
    if ($reason.Length -gt 200) { $reason = $reason.Substring(0, 200) }
    $S.failure_reason = $reason
    Write-State ('Wrapper error: ' + $reason)
    try {
        if ($null -ne $Process -and -not $Process.HasExited -and -not $S.termination_requested) { Request-Termination }
    }
    catch { Write-State 'Best-effort termination after error also failed.' }
}

# ---------------------------------------------------------------- single bounded write of wrapper.json
function ConvertTo-Bytes($Table) { return ,(ConvertTo-CanonicalBytes $Table) }

$json = ConvertTo-Bytes $S
if ($json.Length -gt $WrapperJsonMax) {
    $S.children_before_termination = $null
    $S.children_after_exit = @{ count = $S.children_after_exit['count']; truncated = $true; entries = @() }
    $json = ConvertTo-Bytes $S
}
if ($json.Length -gt $WrapperJsonMax) {
    $s1 = Limit-Text $S.stdout 256; $s2 = Limit-Text $S.stderr 256
    $S.stdout = $s1[0]; $S.stdout_truncated = $true; $S.stderr = $s2[0]; $S.stderr_truncated = $true
    $json = ConvertTo-Bytes $S
}
if ($json.Length -gt $WrapperJsonMax) {
    $json = ConvertTo-Bytes ([ordered]@{ schema = 'luna65-s1b-wrapper-v1'; run_id = $RunId; final_state = 'UNKNOWN_FAIL_CLOSED'; failure_reason = 'wrapper log exceeded 16,384 bytes' })
}
try {
    $logStream = New-Object IO.FileStream((Join-Path $WrapperDir 'wrapper.json'), [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
    try { $logStream.Write($json, 0, $json.Length) } finally { $logStream.Dispose() }
}
catch {
    Write-Host ('WRAPPER LOG WRITE FAILED: ' + $_.Exception.Message)
    exit 30
}

Write-State ('Final state: ' + $S.final_state + '; exit code: ' + $S.exit_code)
if ($S.final_state -eq 'COMPLETED') {
    Write-State 'Next: run the independent verifier (read-only) per the execution authorization. No retry is permitted.'
    exit 0
}
Write-State 'Not completed. Evidence preserved. Do not retry under this authorization.'
exit 10
