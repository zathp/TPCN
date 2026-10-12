#requires -Version 5.1
# Luna-65 Phase 2A RP-1 read-only host inspection (candidate). Writes only to stdout/stderr.
param([Parameter(Mandatory = $true)][string]$RunId)
Set-StrictMode -Version 2
$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'Windows PowerShell 5.1 required' }
if ($RunId -notmatch '^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{7}$') { throw 'bad run id' }
$script:Sw = [Diagnostics.Stopwatch]::StartNew()
$script:Chars = 0
$script:Abort = $false
$script:Bad = 0
$WallBudgetMs = 27000
$CharCap = 4000000
$Repo = 'C:\Users\Patrick\Documents\ActiveCode\TPCN'
$BasePy = 'C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe'
$VenvPy = $Repo + '\.venv\Scripts\python.exe'
$EvParent = 'C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65'
function Emit([string]$s) {
    if ($script:Chars -ge $CharCap) { return }
    $marker = ' CAP_TRUNCATED'
    $room = $CharCap - $script:Chars - 2
    if ($s.Length -gt $room) {
        $keep = $room - $marker.Length
        if ($keep -lt 0) { $script:Chars = $CharCap; return }
        $s = $s.Substring(0, $keep) + $marker
    }
    $script:Chars += $s.Length + 2
    [Console]::Out.WriteLine($s)
}
function SecBegin([string]$id) { Emit ('BEGIN {0} t_ms={1}' -f $id, $script:Sw.ElapsedMilliseconds) }
function SecEnd([string]$id, [string]$st) { Emit ('END {0} status={1} t_ms={2}' -f $id, $st, $script:Sw.ElapsedMilliseconds) }
function TimeLeft { return ($WallBudgetMs - $script:Sw.ElapsedMilliseconds) }
function RunNative([string]$exe, [string]$argline, [int]$ms, [int]$maxLines) {
    if ($script:Abort) { Emit 'SKIPPED_ABORT_FAIL_CLOSED'; $script:Bad++; return 'ABORT' }
    if ((TimeLeft) -lt 1000) { Emit 'SKIPPED_BUDGET'; $script:Bad++; return 'BUDGET' }
    $psi = New-Object Diagnostics.ProcessStartInfo
    $psi.FileName = $exe; $psi.Arguments = $argline; $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true; $psi.CreateNoWindow = $true
    try { $p = [Diagnostics.Process]::Start($psi) } catch { Emit ('START_FAIL ' + $_.Exception.GetType().Name); $script:Bad++; return 'START_FAIL' }
    $o = $p.StandardOutput.ReadToEndAsync(); $e = $p.StandardError.ReadToEndAsync()
    $lim = [Math]::Min($ms, (TimeLeft))
    if (-not $p.WaitForExit($lim)) {
        $killErr = $null
        try { $p.Kill() } catch { $killErr = $_.Exception.GetType().Name }
        $gone = $false
        try { $gone = $p.WaitForExit(2000) } catch { }
        $script:Bad++
        if ($gone) { Emit 'TIMEOUT_KILLED_CONFIRMED'; return 'TIMEOUT' }
        $script:Abort = $true
        Emit ('KILL_UNCONFIRMED RP1_UNKNOWN_FAIL_CLOSED kill_error=' + $killErr)
        return 'KILL_UNCONFIRMED'
    }
    $p.WaitForExit()
    $n = 0
    foreach ($l in ($o.Result -split "`r?`n")) { $n++; if ($n -gt $maxLines) { Emit 'TRUNCATED_LINES'; break }; Emit $l }
    $en = 0
    foreach ($l in ($e.Result -split "`r?`n")) { if ($l -ne '') { $en++; if ($en -gt 20) { break }; Emit ('STDERR ' + $l) } }
    Emit ('EXIT ' + $p.ExitCode)
    if ($p.ExitCode -ne 0) { Emit 'EXIT_NONZERO'; $script:Bad++ }
    return ('EXIT_' + $p.ExitCode)
}
function Try-Section([string]$id, [scriptblock]$body) {
    SecBegin $id
    $st = 'OK'
    $ErrorActionPreference = 'Stop'
    try { $null = & $body } catch { Emit ('ERROR ' + $_.Exception.GetType().Name + ': ' + $_.Exception.Message); $st = 'ERROR'; $script:Bad++ }
    $ErrorActionPreference = 'Continue'
    SecEnd $id $st
}

Try-Section 'S00_header' {
    Emit 'schema=luna65-rp1-host-inspection-v1'
    Emit ('run_id=' + $RunId)
    Emit ('utc_start=' + [DateTime]::UtcNow.ToString('o'))
    Emit ('script_sha256=' + (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash)
    Emit ('ps_version=' + $PSVersionTable.PSVersion.ToString() + ' edition=' + $PSVersionTable.PSEdition)
    Emit ('process_64bit=' + [Environment]::Is64BitProcess + ' os_64bit=' + [Environment]::Is64BitOperatingSystem)
    Emit ('user=' + [Environment]::UserDomainName + '\' + [Environment]::UserName)
    Emit ('session_id=' + [Diagnostics.Process]::GetCurrentProcess().SessionId + ' interactive=' + [Environment]::UserInteractive)
    Emit ('cwd=' + (Get-Location).Path)
    Emit ((Get-ExecutionPolicy -List | Out-String).TrimEnd())
}

Try-Section 'S01_os' {
    $os = Get-CimInstance -ClassName Win32_OperatingSystem -OperationTimeoutSec 2
    Emit ('caption=' + $os.Caption + ' version=' + $os.Version + ' build=' + $os.BuildNumber + ' arch=' + $os.OSArchitecture)
    $cv = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    Emit ('edition_id=' + $cv.EditionID + ' product=' + $cv.ProductName + ' display=' + $cv.DisplayVersion + ' ubr=' + $cv.UBR)
    foreach ($f in 'kernel32.dll', 'ntdll.dll', 'advapi32.dll') {
        $fi = Get-Item -LiteralPath (Join-Path $env:SystemRoot ('System32\' + $f))
        Emit ($f + ' version=' + $fi.VersionInfo.FileVersion + ' sha256=' + (Get-FileHash -LiteralPath $fi.FullName -Algorithm SHA256).Hash)
    }
    Emit 'job_object_api=NOT_EVALUATED_BY_RP1 (documentation only; runtime availability is RP-2)'
}

Try-Section 'S02_token' {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $pr = New-Object Security.Principal.WindowsPrincipal($id)
    Emit ('is_administrator_role=' + $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) + ' auth=' + $id.AuthenticationType + ' impersonation=' + $id.ImpersonationLevel)
    $pol = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
    foreach ($n in 'EnableLUA', 'ConsentPromptBehaviorAdmin', 'FilterAdministratorToken') { $v = $null; if ($pol.PSObject.Properties.Name -contains $n) { $v = $pol.$n }; Emit ($n + '=' + $v) }
    RunNative (Join-Path $env:SystemRoot 'System32\whoami.exe') '/all /fo list' 5000 400
}

Try-Section 'S03_interpreter' {
    foreach ($py in $BasePy, $VenvPy) {
        Emit ('path=' + $py)
        if (-not (Test-Path -LiteralPath $py -PathType Leaf)) { Emit 'present=False'; continue }
        Emit ('present=True sha256=' + (Get-FileHash -LiteralPath $py -Algorithm SHA256).Hash + ' bytes=' + (Get-Item -LiteralPath $py).Length)
        RunNative $py '-I -B -c "import sys,platform;print(sys.version);print(sys.executable);print(sys.prefix);print(sys.base_prefix);print(platform.platform())"' 4000 20
    }
    $cfg = $Repo + '\.venv\pyvenv.cfg'
    if (Test-Path -LiteralPath $cfg -PathType Leaf) { Emit ('pyvenv_cfg_bytes=' + (Get-Item -LiteralPath $cfg).Length); Get-Content -LiteralPath $cfg -TotalCount 20 | ForEach-Object { Emit ('cfg ' + $_) } } else { Emit 'pyvenv_cfg=absent' }
}

Try-Section 'S04_repository_access' {
    Emit ('repo_exists=' + (Test-Path -LiteralPath $Repo -PathType Container))
    RunNative 'git.exe' ('--no-optional-locks -C "' + $Repo + '" rev-parse HEAD') 4000 5
    foreach ($p in $Repo, ($Repo + '\scripts'), ($Repo + '\.venv'), $EvParent) {
        $it = Get-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue
        if ($it) { Emit ('item path=' + $p + ' attributes=' + $it.Attributes + ' reparse=' + (($it.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) } else { Emit ('item path=' + $p + ' present=False') }
    }
}

Try-Section 'S05_acl_labels' {
    $icacls = Join-Path $env:SystemRoot 'System32\icacls.exe'
    foreach ($p in $Repo, ($Repo + '\scripts'), ($Repo + '\.venv\Scripts'), (Split-Path $BasePy), $EvParent, ($env:LOCALAPPDATA + '\TPCN')) {
        Emit ('ACL_TARGET ' + $p)
        if (Test-Path -LiteralPath $p) { RunNative $icacls ('"' + $p + '"') 4000 60 } else { Emit 'present=False' }
    }
}

Try-Section 'S06_low_label_sample' {
    $icacls = Join-Path $env:SystemRoot 'System32\icacls.exe'
    foreach ($p in ($env:USERPROFILE + '\*'), ($env:USERPROFILE + '\AppData\*'), ($env:USERPROFILE + '\AppData\LocalLow'), ($env:USERPROFILE + '\AppData\LocalLow\*'), ($env:LOCALAPPDATA + '\*'), $env:TEMP) {
        Emit ('LABEL_TARGET ' + $p)
        RunNative $icacls ('"' + $p + '"') 5000 300
    }
    Emit 'coverage=BOUNDED_SAMPLE_ONLY (not a complete Low-writable enumeration; registry AppDataLow not evaluated)'
}

Try-Section 'S07_network_policy' {
    RunNative (Join-Path $env:SystemRoot 'System32\netsh.exe') 'advfirewall show allprofiles' 5000 80
    Emit 'enforcement=NOT_ESTABLISHED (policy observation only)'
}

Try-Section 'S08_footer' {
    Emit ('utc_end=' + [DateTime]::UtcNow.ToString('o'))
    Emit ('elapsed_ms=' + $script:Sw.ElapsedMilliseconds + ' chars=' + $script:Chars)
    if ($script:Abort) { Emit 'RP1_UNKNOWN_FAIL_CLOSED' } elseif ($script:Bad -eq 0) { Emit 'RP1_COMPLETE' } else { Emit ('RP1_PARTIAL incomplete_observations=' + $script:Bad) }
}
