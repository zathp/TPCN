# Attended RP-2 diagnostic O controller; RP-2B execution permission is separate.
# Interop and reader IL use Reflection.Emit Run-only: no compiler or disk assembly.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$RunId,
    [Parameter(Mandatory=$true)][string]$EvidenceLeaf,
    [Parameter(Mandatory=$true)][string]$ReviewedProbeHash,
    [Parameter(Mandatory=$true)][string]$ReviewedWrapperHash
)
Set-StrictMode -Version 2
$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\Patrick\Documents\ActiveCode\TPCN'
$Probe = Join-Path $Root 'scripts\luna65_phase2a_rp2_compatibility_probe.py'
$Image = 'C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe'
$ImageHash = '4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F'
$HostImage = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
$HostImageHash = '9785001B0DCF755EDDB8AF294A373C0B87B2498660F724E76C4D53F9C217C7A3'
$HostEngineVersion = '5.1.19041.6456'
$U = 'S-1-5-21-3301679920-2322392626-2066554248-1001'
$Nonce = 'L65-RP2A-SYNTHETIC-V1'
$XM = 'O:' + $U + 'D:P(D;;0x00060000;;;OW)S:(ML;;NWNR;;;ME)'
$TotalLimit = 1048576L
$PayloadLimit = 917504L
$FinalReserve = 131072L
$RecordLimit = 16384
$LowRecordLimit = 16384
$RemoteReservation = 393216L
$StopCode = [uint32]::Parse('E0650002',[Globalization.NumberStyles]::HexNumber)
$HostFiles = @{
    'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\mscorlib.dll'='CBBA0B14D43901FF3D92CC44EFE6A79149BFCAA3006C08CA05E186B2A75B54B5'
    'C:\WINDOWS\Microsoft.Net\assembly\GAC_MSIL\System.Management.Automation\v4.0_3.0.0.0__31bf3856ad364e35\System.Management.Automation.dll'='D0FBAA3BFB9380E2128015A9080A0403BAA3B593F20366BFEFD20A56F2195A9F'
    'C:\Users\Patrick\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1'='F2E63DE9AA2E2E9F2685A19AD4C082C5FF0CC4986F82CCFA33199FA52C91A425'
    'C:\Users\Patrick\.jabba\jabba.ps1'='39C0709A51E2E946FC96BE4E38B373F5DE39AAC54F1A248EABA03989A572E0A4'
    'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\machine.config'='68E0DC6FEF3FF0DF4284C47B935ACCF4315DFC8228FBA809CB181258C78CB5E1'
}
$HostAbsences = @(
    'C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1',
    'C:\Windows\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1',
    'C:\Users\Patrick\Documents\WindowsPowerShell\profile.ps1'
)
$HostTrees = @(
    @('C:\Windows\System32', $false, 3697, '407A2A6B40DB266BC34D5135A978256E2793816E90FFEF072CCC3D95AA2C4818'),
    @('C:\Windows\Microsoft.NET\Framework64\v4.0.30319', $true, 322, '5EA3204423F6059F775BBFCB501779B76672B516AC73550059B484A81173DEF8'),
    @('C:\Windows\Microsoft.NET\assembly\GAC_MSIL', $true, 414, 'C801D216D292E7E665E1F24D0B38752CC523E90DC4B278EC0933C3C6C06BEB7F'),
    @('C:\Windows\Microsoft.NET\assembly\GAC_64', $true, 53, 'F359CA53D9E16713C4ADD368309A416479D9F71DE8055B5FA043B5D610AEF341'),
    @('C:\Windows\assembly\NativeImages_v4.0.30319_64', $true, 802, 'BD11F74C01907C62FBB6DAD0A70B42BAF9FFD04C9F39544BCCF4131F3DFACF0B'),
    @('C:\Windows\System32\WindowsPowerShell\v1.0', $true, 396, '94A86CDF8D211C59074204D38F9807E8935DC1003F88C445F632641B1BBB7E3D', @('.dll','.ps1','.ps1xml','.psm1','.psd1','.config','.xml','.mshxml'))
)
$PythonBase = 'C:\Users\Patrick\AppData\Local\Programs\Python\Python311'
$PythonUser = 'C:\Users\Patrick\AppData\Roaming\Python\Python311\site-packages'
$PythonTreeRows = @(
    @(($PythonBase+'\Lib'),'site-packages',7008,'D5EA04080A3E9000761B076823B3AAEF0F8BDF009620D4F238B7BA5A3AD5ACD3'),
    @(($PythonBase+'\DLLs'),'',34,'1AD0A0100C7C6267A010467688F81AC41C4CD46EDC324FBFB52FBB51A953504E'),
    @(($PythonBase+'\Lib\site-packages\pytest'),'',4,'4EFE2CB65B5BEABE1AA8D55E80EAB668F7E7DF84B749A5A975910608C61F9241'),
    @(($PythonBase+'\Lib\site-packages\_pytest'),'',143,'A9E1E415449DA37D38A7B2234D8569362B0BFA78A28BC148B753450F270D1879'),
    @(($PythonBase+'\Lib\site-packages\pluggy'),'',16,'F56CF17FA5D42137192463469F89B39F06D505BA1D6B44074EB046C809858C45'),
    @(($PythonBase+'\Lib\site-packages\iniconfig'),'',8,'FDE164BD03F103E4A45B72935E5B6E54500DF815540C532D54C689CFD0539485'),
    @(($PythonBase+'\Lib\site-packages\packaging'),'',32,'A4B27C7FF9853C74BC6F70416255782C70A7F2D98BC222229843373A7C424B63'),
    @(($PythonBase+'\Lib\site-packages\_distutils_hack'),'',6,'053CD7DE1981E3BBB92EDEB9B7086DE5BEC92756241AC0FB11F99B1431864588'),
    @(($PythonUser+'\pygments'),'',674,'A34700D2D8C77C487B5A327B228CECCBEDA750ED277CA4A58599CBA53845AB04'),
    @(($PythonUser+'\colorama'),'',26,'9678523F53E349D2E0FAA5B695DAA7BD92D75139DCEC21146C5CBC52A4CD9EF6'),
    @(($PythonUser+'\pywin32_system32'),'',2,'554F89467F84A628F33C0211678ED1787DC1F2942EA2A0EC338C07DAF59B65E9')
)
$PythonFileRows = @(
    @(($PythonBase+'\Lib\site-packages\distutils-precedence.pth'),'2638CE9E2500E572A5E0DE7FAED6661EB569D1B696FCBA07B0DD223DA5F5D224'),
    @(($PythonBase+'\Lib\site-packages\_distutils_hack\__init__.py'),'4D27A48545B57DD137AE35376FCF326D2064271084A487960686F8704B94DE4A'),
    @(($PythonUser+'\pywin32.pth'),'D902584A2A0A5216CE12C712D1378FE07541D32C383D0CC5ABCD68412144FE4D'),
    @(($PythonUser+'\win32\lib\pywin32_bootstrap.py'),'FD31F27BC85A6B9C974670838B6EEFAFB32991BE4A9F840F96A4F5524DF3B3C3'),
    @(($PythonBase+'\Lib\site-packages\py.py'),'B71675B5D9845BA0814E9E88767F88DAC3B3CC0D3128DA028BD45EDBB523E871'),
    @(($PythonUser+'\typing_extensions.py'),'CC67BB3A7D7A4B91D597470F9689F7C22BFA334C98BDAC4399F946E6DAFAB6FD'),
    @(($PythonBase+'\python311.dll'),'A811C7516F531F1515D10743AE78004DD627EBA0DC2D3BC0D2E033B2722043CE'),
    @(($PythonBase+'\python3.dll'),'520169AA6CF49D7EE724D1178DE1BE0E809E4BDCF671E06F3D422A0DD5FD294A'),
    @(($PythonBase+'\vcruntime140.dll'),'A8F950B4357EC12CFCCDDC9094CCA56A3D5244B95E09EA6E9A746489F2D58736'),
    @(($PythonBase+'\vcruntime140_1.dll'),'E4B533A94E02C574780E4B333FCF0889F65ED00D39E32C0FBBDA2116F185873F')
)

function Assert-Hash([string]$Path, [string]$Expected) {
    if ($Expected -cnotmatch '^[A-F0-9]{64}$') { throw 'Hash grammar' }
    if ((Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash -cne $Expected) {
        throw ('Identity drift: ' + $Path)
    }
}
function Alert-Unresolved {
    [Console]::Error.WriteLine('RP2_UNKNOWN_FAIL_CLOSED: containment remains unresolved; an unconfirmed Low child/descendant may still be active. No retry or downstream progression is authorized.')
}
function Verify-HostTree($Spec) {
    $root=$Spec[0]
    $option=$(if($Spec[1]){[IO.SearchOption]::AllDirectories}else{[IO.SearchOption]::TopDirectoryOnly})
    if($Spec.Count -gt 4){
        $names=[string[]]@([IO.Directory]::EnumerateFiles($root,'*',$option)|Where-Object{[IO.Path]::GetExtension($_).ToLowerInvariant() -in $Spec[4]})
    }else{$names=[IO.Directory]::GetFiles($root,'*.dll',$option)}
    if($names.Count -ne $Spec[2] -or $names.Count -gt 4096){throw ('host closure count '+$root)}
    [Array]::Sort($names,[StringComparer]::OrdinalIgnoreCase)
    $sha=[Security.Cryptography.SHA256]::Create()
    try{
        foreach($full in $names){
            if([IO.File]::GetAttributes($full) -band [IO.FileAttributes]::ReparsePoint){throw 'host closure reparse'}
            $line=$full.Substring($root.Length+1).ToLowerInvariant()+'|'+(Get-Item -LiteralPath $full).Length+'|'+(Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash+"`n"
            $b=[Text.Encoding]::UTF8.GetBytes($line)
            [void]$sha.TransformBlock($b,0,$b.Length,$b,0)
        }
        [void]$sha.TransformFinalBlock((New-Object byte[] 0),0,0)
        if([BitConverter]::ToString($sha.Hash).Replace('-','') -cne $Spec[3]){throw ('host/DLL closure drift '+$root)}
    }finally{$sha.Dispose()}
}
function Walk-PythonTree([string]$Directory,[string]$Root,[string]$Skip,$State,[int]$Depth) {
            if($Depth -gt 32){throw 'closure depth cap'}
            $entries=[IO.Directory]::GetFileSystemEntries($Directory)
            if($entries.Count -gt 2048){throw 'closure directory fanout cap'}
            $map=@{};$keys=New-Object 'Collections.Generic.List[string]'
            foreach($full in $entries){
                if($Directory -ceq $Root -and [IO.Path]::GetFileName($full) -ceq $Skip){continue}
                $attributes=[IO.File]::GetAttributes($full)
                if($attributes -band [IO.FileAttributes]::ReparsePoint){throw ('closure reparse '+$full)}
                $isDir=[bool]($attributes -band [IO.FileAttributes]::Directory)
                $key=$full.ToLowerInvariant()+$(if($isDir){'\'}else{''})
                $keys.Add($key);$map[$key]=@($full,$isDir)
            }
            $sorted=$keys.ToArray();[Array]::Sort($sorted,[StringComparer]::OrdinalIgnoreCase)
            foreach($key in $sorted){
                $full=$map[$key][0]
                if($map[$key][1]){Walk-PythonTree $full $Root $Skip $State ($Depth+1);continue}
                if([IO.Path]::GetExtension($full).ToLowerInvariant() -notin @('.py','.pyc','.pyd','.dll','.pth','.json')){continue}
                $item=Get-Item -LiteralPath $full
                if($item.Length -gt 33554432 -or $State.Count -ge 10000){throw 'closure file/count cap'}
                $line=$full.Substring($Root.Length+1).ToLowerInvariant()+'|'+$item.Length+'|'+(Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash+"`n"
                $bytes=[Text.Encoding]::UTF8.GetBytes($line)
                [void]$State.SHA.TransformBlock($bytes,0,$bytes.Length,$bytes,0)
                $State.Count++
            }
        }
function Verify-PythonClosure {
            foreach($row in $PythonFileRows){Assert-Hash $row[0] $row[1]}
            foreach($row in $PythonTreeRows){
                $state=@{SHA=[Security.Cryptography.SHA256]::Create();Count=0}
                try{
                    Walk-PythonTree $row[0] $row[0] $row[1] $state 0
                    [void]$state.SHA.TransformFinalBlock((New-Object byte[] 0),0,0)
                    $hash=[BitConverter]::ToString($state.SHA.Hash).Replace('-','')
                    if($state.Count -ne $row[2] -or $hash -cne $row[3]){throw ('Python closure drift '+$row[0])}
                }finally{$state.SHA.Dispose()}
            }
            $search=@($Root,($Root+'\scripts'),$PythonBase,($PythonBase+'\Lib'),($PythonBase+'\DLLs'),($PythonBase+'\Lib\site-packages'),$PythonUser,($PythonUser+'\win32'),($PythonUser+'\win32\lib'),($PythonUser+'\Pythonwin'))
            foreach($p in $search){
                foreach($name in @('sitecustomize','sitecustomize.py','sitecustomize.pyc','sitecustomize.pyd','usercustomize','usercustomize.py','usercustomize.pyc','usercustomize.pyd')){
                    if(Test-Path -LiteralPath (Join-Path $p $name)){throw ('hook absence drift '+$p+'\'+$name)}
                }
            }
            foreach($name in @('python._pth','python311._pth','python311.zip','pyvenv.cfg')){
                if(Test-Path -LiteralPath (Join-Path $PythonBase $name)){throw ('path configuration drift '+$name)}
            }
            if(Test-Path -LiteralPath ($Root+'\~\Python\Python311\site-packages')){throw 'no-APPDATA effective user-site absence drift'}
            foreach($spec in @(@($PythonUser,'pywin32.pth'),@(($PythonBase+'\Lib\site-packages'),'distutils-precedence.pth'))){
                $pth=@([IO.Directory]::GetFiles($spec[0],'*.pth',[IO.SearchOption]::TopDirectoryOnly))
                if($pth.Count -ne 1 -or [IO.Path]::GetFileName($pth[0]) -cne $spec[1]){throw 'pth census drift'}
            }
            foreach($hive in @([Microsoft.Win32.Registry]::CurrentUser,[Microsoft.Win32.Registry]::LocalMachine)){
                foreach($name in @('Software\Python\PythonCore\3.11\PythonPath','Software\WOW6432Node\Python\PythonCore\3.11\PythonPath')){
                    $key=$hive.OpenSubKey($name,$false)
                    if($null -ne $key){$key.Dispose();throw ('Python registry-path absence drift '+$name)}
                }
            }
            $moduleNames=New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
            foreach($name in @('sys','os','json','ctypes','time','msvcrt','pytest','_pytest','pluggy','iniconfig','packaging','pygments','colorama','_distutils_hack','typing_extensions','pywin32_bootstrap','pywin32_system32','py','hashlib')){[void]$moduleNames.Add($name)}
            foreach($full in [IO.Directory]::GetFileSystemEntries($PythonBase+'\Lib')){
                if([IO.Path]::GetFileName($full) -in @('site-packages','__pycache__')){continue}
                $ext=[IO.Path]::GetExtension($full)
                if($ext -in @('','.py','.pyc')){[void]$moduleNames.Add([IO.Path]::GetFileNameWithoutExtension($full))}
            }
            foreach($p in @($Root,($Root+'\scripts'))){
                foreach($name in $moduleNames){foreach($suffix in @('','.py','.pyc','.pyd')){if(Test-Path -LiteralPath (Join-Path $p ($name+$suffix))){throw ('cwd/script shadow '+$name)}}}
                foreach($full in [IO.Directory]::GetFiles($p)){
                    if([IO.Path]::GetExtension($full) -in @('.dll','.pyd','.pth')){throw 'cwd native/startup shadow'}
                }
            }
            $dlls=@([IO.Directory]::GetFiles($PythonBase,'*.dll')|ForEach-Object{[IO.Path]::GetFileName($_)}|Sort-Object)
            if(($dlls -join '|') -cne 'python3.dll|python311.dll|vcruntime140.dll|vcruntime140_1.dll'){throw 'Python executable-directory DLL census'}
            $version=(Get-Item -LiteralPath $Image).VersionInfo
            if($version.FileVersion -notlike '3.11.4*' -or $version.OriginalFilename -ine 'python.exe'){throw 'interpreter resource identity'}
            $input=New-Object IO.FileStream($Image,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
            try{
                $header=New-Object byte[] 4096
                if($input.Read($header,0,4096) -ne 4096 -or $header[0] -ne 77 -or $header[1] -ne 90){throw 'PE DOS header'}
                $offset=[BitConverter]::ToInt32($header,60)
                if($offset -lt 64 -or $offset+26 -gt $header.Length -or [BitConverter]::ToUInt32($header,$offset) -ne 0x4550 -or [BitConverter]::ToUInt16($header,$offset+4) -ne 0x8664 -or [BitConverter]::ToUInt16($header,$offset+24) -ne 0x20B){throw 'AMD64 PE32+ image identity'}
            }finally{$input.Dispose()}
        }
function Quote-Arg([string]$Value) {
    if ($Value.Contains([string][char]0)) { throw 'NUL argv' }
    $b = New-Object Text.StringBuilder
    [void]$b.Append('"')
    $slashes = 0
    foreach ($ch in $Value.ToCharArray()) {
        if ($ch -eq '\') { $slashes++; continue }
        if ($ch -eq '"') { [void]$b.Append('\',($slashes*2+1)) }
        else { [void]$b.Append('\',$slashes) }
        [void]$b.Append($ch); $slashes=0
    }
    [void]$b.Append('\',($slashes*2)); [void]$b.Append('"')
    $b.ToString()
}
function Check-Api([bool]$OK,[string]$Stage) {
    $errorCode=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
    if (-not $OK) {
        $message=(New-Object ComponentModel.Win32Exception($errorCode)).Message
        throw (New-Object ComponentModel.Win32Exception($errorCode,($Stage+' error='+$errorCode+': '+$message)))
    }
}

function New-Interop {
    # P/Invoke signatures are emitted inside this existing attended host.
    $an=New-Object Reflection.AssemblyName('Luna65RP2_'+[Guid]::NewGuid().ToString('N'))
    $assembly=[AppDomain]::CurrentDomain.DefineDynamicAssembly($an,[Reflection.Emit.AssemblyBuilderAccess]::Run)
    $module=$assembly.DefineDynamicModule($an.Name)
    $type=$module.DefineType('RP2Native',[Reflection.TypeAttributes]'Public,Abstract,Sealed')
    $ip=[IntPtr]; $u32=[uint32]; $bool=[bool]; $void=[void]
    $ipr=$ip.MakeByRefType(); $ur=$u32.MakeByRefType(); $br=$bool.MakeByRefType()
    $size=[UIntPtr]; $sizer=$size.MakeByRefType(); $bytes=[byte[]]
    $api=@(
        @('kernel32.dll','GetTickCount64',[uint64],@()),
        @('kernel32.dll','GetCurrentProcess',$ip,@()),
        @('kernel32.dll','GetCurrentThread',$ip,@()),
        @('kernel32.dll','CloseHandle',$bool,@($ip)),
        @('kernel32.dll','GetHandleInformation',$bool,@($ip,$ur)),
        @('kernel32.dll','SetHandleInformation',$bool,@($ip,$u32,$u32)),
        @('kernel32.dll','CreatePipe',$bool,@($ipr,$ipr,$ip,$u32)),
        @('kernel32.dll','ReadFile',$bool,@($ip,$bytes,$u32,$ur,$ip)),
        @('kernel32.dll','CreateThread',$ip,@($ip,$size,$ip,$ip,$u32,$ur)),
        @('kernel32.dll','Sleep',$void,@($u32)),
        @('kernel32.dll','CancelSynchronousIo',$bool,@($ip)),
        @('kernel32.dll','WaitForSingleObject',$u32,@($ip,$u32)),
        @('kernel32.dll','ResumeThread',$u32,@($ip)),
        @('kernel32.dll','TerminateProcess',$bool,@($ip,$u32)),
        @('kernel32.dll','GetExitCodeProcess',$bool,@($ip,$ur)),
        @('kernel32.dll','GetProcessId',$u32,@($ip)),
        @('kernel32.dll','GetProcessTimes',$bool,@($ip,$ip,$ip,$ip,$ip)),
        @('kernel32.dll','QueryFullProcessImageNameW',$bool,@($ip,$u32,[Text.StringBuilder],$ur)),
        @('kernel32.dll','IsProcessInJob',$bool,@($ip,$ip,$br)),
        @('kernel32.dll','GetWindowsDirectoryW',$u32,@([Text.StringBuilder],$u32)),
        @('kernel32.dll','CreateDirectoryW',$bool,@([string],$ip)),
        @('kernel32.dll','InitializeProcThreadAttributeList',$bool,@($ip,$u32,$u32,$sizer)),
        @('kernel32.dll','UpdateProcThreadAttribute',$bool,@($ip,$u32,$size,$ip,$size,$ip,$ip)),
        @('kernel32.dll','DeleteProcThreadAttributeList',$void,@($ip)),
        @('kernel32.dll','CreateProcessW',$bool,@([string],[Text.StringBuilder],$ip,$ip,$bool,$u32,$ip,[string],$ip,$ip)),
        @('advapi32.dll','OpenProcessToken',$bool,@($ip,$u32,$ipr)),
        @('advapi32.dll','OpenThreadToken',$bool,@($ip,$u32,$bool,$ipr)),
        @('advapi32.dll','GetTokenInformation',$bool,@($ip,[int],$ip,$u32,$ur)),
        @('advapi32.dll','GetKernelObjectSecurity',$bool,@($ip,$u32,$bytes,$u32,$ur)),
        @('advapi32.dll','LookupPrivilegeNameW',$bool,@([string],$ip,[Text.StringBuilder],$ur)),
        @('advapi32.dll','GetLengthSid',$u32,@($ip)),
        @('advapi32.dll','ConvertStringSecurityDescriptorToSecurityDescriptorW',$bool,@([string],$u32,$ipr,$ur)),
        @('kernel32.dll','LocalFree',$ip,@($ip)),
        @('ntdll.dll','NtQueryObject',[int],@($ip,[int],$bytes,$u32,$ur))
    )
    $ctor=[Runtime.InteropServices.DllImportAttribute].GetConstructor(@([string]))
    $fields=[Reflection.FieldInfo[]]@(
        [Runtime.InteropServices.DllImportAttribute].GetField('SetLastError'),
        [Runtime.InteropServices.DllImportAttribute].GetField('CharSet'),
        [Runtime.InteropServices.DllImportAttribute].GetField('CallingConvention'),
        [Runtime.InteropServices.DllImportAttribute].GetField('ExactSpelling')
    )
    foreach($spec in $api) {
        $args=[Type[]]$spec[3]
        $method=$type.DefineMethod($spec[1],[Reflection.MethodAttributes]'Public,Static,PinvokeImpl',$spec[2],$args)
        if($spec[1] -eq 'ReadFile'){[void]$method.DefineParameter(2,[Reflection.ParameterAttributes]::Out,'buffer')}
        elseif($spec[1] -in @('GetKernelObjectSecurity','NtQueryObject')){[void]$method.DefineParameter(3,[Reflection.ParameterAttributes]::Out,'buffer')}
        $attr=New-Object Reflection.Emit.CustomAttributeBuilder($ctor,[object[]]@($spec[0]),$fields,[object[]]@($true,[Runtime.InteropServices.CharSet]::Unicode,[Runtime.InteropServices.CallingConvention]::Winapi,$true))
        $method.SetCustomAttribute($attr)
        $method.SetImplementationFlags([Reflection.MethodImplAttributes]::PreserveSig)
    }
    $native=$type.CreateType()
    # Windows native-thread callback; no PowerShell script runs on the worker.
    $d=$module.DefineType('RP2ThreadProc',[Reflection.TypeAttributes]'Public,Sealed',[MulticastDelegate])
    $dc=$d.DefineConstructor([Reflection.MethodAttributes]'Public,HideBySig,RTSpecialName',[Reflection.CallingConventions]::Standard,[Type[]]@([object],[IntPtr]))
    $dc.SetImplementationFlags([Reflection.MethodImplAttributes]'Runtime,Managed')
    $invoke=$d.DefineMethod('Invoke',[Reflection.MethodAttributes]'Public,HideBySig,NewSlot,Virtual',[uint32],[Type[]]@([IntPtr]))
    $invoke.SetImplementationFlags([Reflection.MethodImplAttributes]'Runtime,Managed')
    $unmanagedCtor=[Runtime.InteropServices.UnmanagedFunctionPointerAttribute].GetConstructor(@([Runtime.InteropServices.CallingConvention]))
    $unmanaged=New-Object Reflection.Emit.CustomAttributeBuilder($unmanagedCtor,[object[]]@([Runtime.InteropServices.CallingConvention]::Winapi))
    $d.SetCustomAttribute($unmanaged)
    $delegate=$d.CreateType()
    $r=$module.DefineType('RP2Reader',[Reflection.TypeAttributes]::Public)
    [void]$r.DefineDefaultConstructor([Reflection.MethodAttributes]::Public)
    $rf=@{}
    foreach($spec in @(@('Input',[IntPtr]),@('Buffer',[byte[]]),@('Count',[int]),@('EOF',[int]),@('Error',[int]),@('Stop',[int]),@('Ready',[int]),@('Pipeline',[System.Management.Automation.PowerShell]),@('Result',[object]),@('QueryException',[Exception]))) {
        $rf[$spec[0]]=$r.DefineField($spec[0],$spec[1],[Reflection.FieldAttributes]::Public)
    }
    $run=$r.DefineMethod('Run',[Reflection.MethodAttributes]'Public,Static',[uint32],[Type[]]@([IntPtr]))
    $il=$run.GetILGenerator()
    $state=$il.DeclareLocal($r); $count=$il.DeclareLocal([uint32]); $ok=$il.DeclareLocal([bool]); $error=$il.DeclareLocal([int])
    $loop=$il.DefineLabel(); $read=$il.DefineLabel(); $failed=$il.DefineLabel(); $eof=$il.DefineLabel(); $done=$il.DefineLabel()
    $ops=[Reflection.Emit.OpCodes]
    $il.Emit($ops::Ldarg_0)
    $il.Emit($ops::Call,[Runtime.InteropServices.GCHandle].GetMethod('FromIntPtr',[Type[]]@([IntPtr])))
    $gh=$il.DeclareLocal([Runtime.InteropServices.GCHandle]); $il.Emit($ops::Stloc,$gh)
    $il.Emit($ops::Ldloca,$gh); $il.Emit($ops::Call,[Runtime.InteropServices.GCHandle].GetProperty('Target').GetGetMethod())
    $il.Emit($ops::Castclass,$r); $il.Emit($ops::Stloc,$state)
    $il.Emit($ops::Ldloc,$state);$il.Emit($ops::Ldc_I4_1);$il.Emit($ops::Volatile);$il.Emit($ops::Stfld,$rf.Ready)
    $il.MarkLabel($loop)
    $il.Emit($ops::Ldloc,$state); $il.Emit($ops::Volatile); $il.Emit($ops::Ldfld,$rf.Stop); $il.Emit($ops::Brtrue,$done)
    $il.Emit($ops::Ldloc,$state); $il.Emit($ops::Volatile); $il.Emit($ops::Ldfld,$rf.Count); $il.Emit($ops::Brfalse,$read)
    $il.Emit($ops::Ldc_I4_1); $il.Emit($ops::Call,$native.GetMethod('Sleep')); $il.Emit($ops::Br,$loop)
    $il.MarkLabel($read)
    $il.Emit($ops::Ldloc,$state); $il.Emit($ops::Ldfld,$rf.Input)
    $il.Emit($ops::Ldloc,$state); $il.Emit($ops::Ldfld,$rf.Buffer)
    $il.Emit($ops::Ldc_I4,4096); $il.Emit($ops::Ldloca,$count)
    $il.Emit($ops::Ldsfld,[IntPtr].GetField('Zero')); $il.Emit($ops::Call,$native.GetMethod('ReadFile')); $il.Emit($ops::Stloc,$ok)
    $il.Emit($ops::Ldloc,$ok); $il.Emit($ops::Brfalse,$failed)
    $il.Emit($ops::Ldloc,$count); $il.Emit($ops::Brfalse,$eof)
    $il.Emit($ops::Ldloc,$state); $il.Emit($ops::Ldloc,$count); $il.Emit($ops::Conv_I4); $il.Emit($ops::Volatile); $il.Emit($ops::Stfld,$rf.Count)
    $il.Emit($ops::Br,$loop)
    $il.MarkLabel($failed)
    $il.Emit($ops::Call,[Runtime.InteropServices.Marshal].GetMethod('GetLastWin32Error')); $il.Emit($ops::Stloc,$error)
    $il.Emit($ops::Ldloc,$error); $il.Emit($ops::Ldc_I4,109); $il.Emit($ops::Beq,$eof)
    $il.Emit($ops::Ldloc,$state); $il.Emit($ops::Ldloc,$error); $il.Emit($ops::Volatile); $il.Emit($ops::Stfld,$rf.Error); $il.Emit($ops::Br,$done)
    $il.MarkLabel($eof)
    $il.Emit($ops::Ldloc,$state); $il.Emit($ops::Ldc_I4_1); $il.Emit($ops::Volatile); $il.Emit($ops::Stfld,$rf.EOF)
    $il.MarkLabel($done); $il.Emit($ops::Ldc_I4_0); $il.Emit($ops::Ret)
    $query=$r.DefineMethod('Query',[Reflection.MethodAttributes]'Public,Static',[uint32],[Type[]]@([IntPtr]))
    $qi=$query.GetILGenerator();$qs=$qi.DeclareLocal($r);$qg=$qi.DeclareLocal([Runtime.InteropServices.GCHandle]);$qe=$qi.DeclareLocal([Exception])
    $qi.Emit($ops::Ldarg_0);$qi.Emit($ops::Call,[Runtime.InteropServices.GCHandle].GetMethod('FromIntPtr',[Type[]]@([IntPtr])));$qi.Emit($ops::Stloc,$qg)
    $qi.Emit($ops::Ldloca,$qg);$qi.Emit($ops::Call,[Runtime.InteropServices.GCHandle].GetProperty('Target').GetGetMethod());$qi.Emit($ops::Castclass,$r);$qi.Emit($ops::Stloc,$qs)
    $qend=$qi.BeginExceptionBlock()
    $qi.Emit($ops::Ldloc,$qs);$qi.Emit($ops::Ldloc,$qs);$qi.Emit($ops::Ldfld,$rf.Pipeline)
    $invokePS=@([System.Management.Automation.PowerShell].GetMethods()|Where-Object{$_.Name -eq 'Invoke' -and -not $_.IsGenericMethod -and $_.GetParameters().Length -eq 0})
    if($invokePS.Count -ne 1){throw 'PowerShell Invoke ABI'}
    $qi.Emit($ops::Callvirt,$invokePS[0]);$qi.Emit($ops::Stfld,$rf.Result);$qi.Emit($ops::Leave,$qend)
    $qi.BeginCatchBlock([Exception]);$qi.Emit($ops::Stloc,$qe);$qi.Emit($ops::Ldloc,$qs);$qi.Emit($ops::Ldloc,$qe);$qi.Emit($ops::Stfld,$rf.QueryException);$qi.Emit($ops::Leave,$qend)
    $qi.EndExceptionBlock();$qi.Emit($ops::Ldc_I4_0);$qi.Emit($ops::Ret)
    $reader=$r.CreateType()
    return @{Native=$native;Reader=$reader;Delegate=$delegate;Assembly=$assembly}
}

function Alloc([int]$Count) {
    if($Count -lt 1 -or $Count -gt 65536){throw 'native allocation cap'}
    $p=[Runtime.InteropServices.Marshal]::AllocHGlobal($Count)
    $zero=New-Object byte[] $Count
    [Runtime.InteropServices.Marshal]::Copy($zero,0,$p,$Count)
    $script:Allocations.Add($p)
    return $p
}
function Free([IntPtr]$Pointer) {
    if($script:Allocations.Contains($Pointer)) {
        [Runtime.InteropServices.Marshal]::FreeHGlobal($Pointer)
        [void]$script:Allocations.Remove($Pointer)
    }
}
function Own([IntPtr]$Handle,[string]$Name) {
    if($Handle -eq [IntPtr]::Zero -or $Handle -eq [IntPtr](-1)){throw ('invalid handle: '+$Name)}
    if($script:Handles.ContainsKey($Handle.ToInt64())){throw 'duplicate handle ownership'}
    $script:Handles[$Handle.ToInt64()]=$Name
    return $Handle
}
function Close-Owned([IntPtr]$Handle) {
    if($script:Handles.ContainsKey($Handle.ToInt64())){
        Check-Api ($N::CloseHandle($Handle)) ('CloseHandle/'+$script:Handles[$Handle.ToInt64()])
        $script:Handles.Remove($Handle.ToInt64())
    }
}
function Rights([IntPtr]$Handle,[uint32]$Expected,[int]$Inherit) {
    $info=New-Object byte[] 56; [uint32]$length=0
    $status=$N::NtQueryObject($Handle,0,$info,56,[ref]$length)
    if($status -ne 0 -or $length -ne 56){throw ('NtQueryObject ABI/status '+$status+'/'+$length)}
    [uint32]$flags=0; Check-Api ($N::GetHandleInformation($Handle,[ref]$flags)) 'handle flags'
    $access=[BitConverter]::ToUInt32($info,4)
    if(($Expected -ne 0 -and $access -ne $Expected) -or $flags -ne $Inherit){throw 'handle rights/inheritance mismatch'}
    $typeInfo=New-Object byte[] 65536;[uint32]$typeLength=0
    $pin=[Runtime.InteropServices.GCHandle]::Alloc($typeInfo,[Runtime.InteropServices.GCHandleType]::Pinned)
    try{
        $typeStatus=$N::NtQueryObject($Handle,2,$typeInfo,65536,[ref]$typeLength)
        if($typeStatus -ne 0 -or $typeLength -lt 16 -or $typeLength -gt 65536){throw 'object type ABI/status'}
        $start=$pin.AddrOfPinnedObject().ToInt64();$pointer=[BitConverter]::ToInt64($typeInfo,8);$size=[BitConverter]::ToUInt16($typeInfo,0)
        if($size%2 -or $pointer -lt $start -or $pointer+$size -gt $start+65536){throw 'type UNICODE_STRING bounds'}
        $kind=[Text.Encoding]::Unicode.GetString($typeInfo,[int]($pointer-$start),$size)
    }finally{$pin.Free()}
    if($Expected -eq 0x20008 -and $kind -cne 'Token'){throw 'token handle object type'}
    return @{access=$access;flags=$flags;ntstatus=$status;length=$length;type=$kind;type_ntstatus=$typeStatus;type_length=$typeLength}
}
function Read-SD([IntPtr]$Handle) {
    [uint32]$length=0
    $ok=$N::GetKernelObjectSecurity($Handle,0x17,$null,0,[ref]$length)
    $errorCode=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
    if($ok -or $errorCode -ne 122 -or $length -eq 0 -or $length -gt 65536){throw ('SD size/error '+$length+'/'+$errorCode)}
    $raw=New-Object byte[] $length
    Check-Api ($N::GetKernelObjectSecurity($Handle,0x17,$raw,$length,[ref]$length)) 'SD readback'
    $sd=New-Object Security.AccessControl.RawSecurityDescriptor($raw,0)
    if($null -eq $sd.DiscretionaryAcl -or -not ($sd.ControlFlags -band 4) -or -not($sd.ControlFlags -band 0x8000)){throw 'NULL/absent DACL or non-self-relative SD'}
    $aces=@();$label='S-1-16-8192';$labelOrigin='OS-default-Medium';$labels=0
    foreach($aclName in @('DiscretionaryAcl','SystemAcl')) {
        if($null -eq $sd.$aclName){continue}
        foreach($ace in $sd.$aclName) {
            $ab=New-Object byte[] $ace.BinaryLength; $ace.GetBinaryForm($ab,0)
            $aceSid=$null;$mask=$null
            if($ab[0] -in @(0,1,17)){
                $aceSid=(New-Object Security.Principal.SecurityIdentifier($ab,8)).Value
                $mask=[BitConverter]::ToUInt32($ab,4)
            } elseif($ace -is [Security.AccessControl.KnownAce]) {
                $aceSid=$ace.SecurityIdentifier.Value; $mask=$ace.AccessMask
            } else {throw ('unsupported complete ACE decode '+$ab[0])}
            $aces+=@{acl=$aclName;type=[int]$ab[0];flags=[int]$ab[1];sid=$aceSid;mask=$mask;raw=[BitConverter]::ToString($ab).Replace('-','')}
            if($ab[0] -eq 17){$labels++;$label=$aceSid;$labelOrigin='explicit'}
        }
    }
    if($labels -gt 1){throw 'ambiguous label'}
    return @{raw=[BitConverter]::ToString($raw).Replace('-','');owner=$sd.Owner.Value;group=$(if($sd.Group){$sd.Group.Value}else{$null});control=[int]$sd.ControlFlags;aces=$aces;label=$label;label_origin=$labelOrigin}
}
function SD-Semantics($SD) {
    [ordered]@{owner=$SD.owner;group=$SD.group;control=$SD.control;aces=@($SD.aces|ForEach-Object{[ordered]@{acl=$_.acl;type=$_.type;flags=$_.flags;sid=$_.sid;mask=$_.mask}});label=$SD.label;label_origin=$SD.label_origin}|ConvertTo-Json -Depth 10 -Compress
}
function Token-Buffer([IntPtr]$Token,[int]$Kind) {
    [uint32]$length=0
    $ok=$N::GetTokenInformation($Token,$Kind,[IntPtr]::Zero,0,[ref]$length)
    $err=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
    if($ok -or $err -ne 122 -or $length -eq 0 -or $length -gt 65536){throw ('token size/error '+$Kind+'/'+$err+'/'+$length)}
    $p=Alloc $length
    $requestedLength=$length
    Check-Api ($N::GetTokenInformation($Token,$Kind,$p,$length,[ref]$length)) ('token query/'+$Kind)
    if($length -ne $requestedLength){throw ('token returned-length drift '+$Kind+'/'+$requestedLength+'/'+$length)}
    return @{Pointer=$p;Length=$length}
}
function Read-Sid([IntPtr]$Pointer,[IntPtr]$Start,[uint32]$Length) {
    if($Pointer -eq [IntPtr]::Zero -or $Pointer.ToInt64() -lt $Start.ToInt64() -or $Pointer.ToInt64()+8 -gt $Start.ToInt64()+$Length){throw 'SID pointer bounds'}
    $expected=8+4*[Runtime.InteropServices.Marshal]::ReadByte($Pointer,1)
    if([Runtime.InteropServices.Marshal]::ReadByte($Pointer) -ne 1 -or $expected -gt 68 -or $Pointer.ToInt64()+$expected -gt $Start.ToInt64()+$Length){throw 'SID header bounds'}
    $count=$N::GetLengthSid($Pointer)
    if($count -ne $expected){throw 'SID buffer length ABI'}
    $raw=New-Object byte[] $count
    [Runtime.InteropServices.Marshal]::Copy($Pointer,$raw,0,$count)
    return (New-Object Security.Principal.SecurityIdentifier($raw,0)).Value
}
function Read-Token([IntPtr]$Token) {
    $result=@{}
    foreach($spec in @(@('user',1),@('owner',4),@('integrity',25))){
        $b=Token-Buffer $Token $spec[1]
        try{
            $p=[Runtime.InteropServices.Marshal]::ReadIntPtr($b.Pointer)
            $result[$spec[0]]=Read-Sid $p $b.Pointer $b.Length
            if($spec[1] -ne 4){$result[$spec[0]+'_attributes']=[uint32][Runtime.InteropServices.Marshal]::ReadInt32($b.Pointer,8)}
        }finally{Free $b.Pointer}
    }
    foreach($spec in @(@('type',8),@('session',12),@('elevated',20),@('policy',27),@('appcontainer',29),@('ui_access',26))){
        $b=Token-Buffer $Token $spec[1]
        try{$result[$spec[0]]=[uint32][Runtime.InteropServices.Marshal]::ReadInt32($b.Pointer)}finally{Free $b.Pointer}
    }
    foreach($spec in @(@('groups',2),@('restricting',11))){
        $b=Token-Buffer $Token $spec[1]
        try{
            $count=[Runtime.InteropServices.Marshal]::ReadInt32($b.Pointer)
            if($count -lt 0 -or $count -gt 256 -or 8+16*$count -gt $b.Length){throw 'group census bounds'}
            $entries=@()
            for($i=0;$i -lt $count;$i++){
                $p=[Runtime.InteropServices.Marshal]::ReadIntPtr($b.Pointer,8+$i*16)
                $entries+=@{sid=(Read-Sid $p $b.Pointer $b.Length);attributes=[uint32][Runtime.InteropServices.Marshal]::ReadInt32($b.Pointer,16+$i*16)}
            }
            $result[$spec[0]]=$entries
        }finally{Free $b.Pointer}
    }
    $b=Token-Buffer $Token 3
    try{
        $count=[Runtime.InteropServices.Marshal]::ReadInt32($b.Pointer)
        if($count -lt 0 -or $count -gt 256 -or 4+12*$count -gt $b.Length){throw 'privilege census bounds'}
        $result.privileges=@()
        for($i=0;$i -lt $count;$i++){
            $p=[IntPtr]($b.Pointer.ToInt64()+4+12*$i)
            $name=New-Object Text.StringBuilder 256;[uint32]$size=256
            Check-Api ($N::LookupPrivilegeNameW($null,$p,$name,[ref]$size)) 'privilege LUID/name'
            $result.privileges+=@{low=[uint32][Runtime.InteropServices.Marshal]::ReadInt32($p);high=[Runtime.InteropServices.Marshal]::ReadInt32($p,4);name=$name.ToString();attributes=[uint32][Runtime.InteropServices.Marshal]::ReadInt32($p,8)}
        }
    }finally{Free $b.Pointer}
    $b=Token-Buffer $Token 6
    try{
        $p=[Runtime.InteropServices.Marshal]::ReadIntPtr($b.Pointer)
        if($p -eq [IntPtr]::Zero){$result.default_dacl=$null}
        else{
            if($p.ToInt64() -lt $b.Pointer.ToInt64() -or $p.ToInt64()+8 -gt $b.Pointer.ToInt64()+$b.Length){throw 'token default ACL pointer bounds'}
            $aclLength=[Runtime.InteropServices.Marshal]::ReadInt16($p,2)
            if($aclLength -lt 8 -or $p.ToInt64()+$aclLength -gt $b.Pointer.ToInt64()+$b.Length){throw 'token default ACL bounds'}
            $aclRaw=New-Object byte[] $aclLength;[Runtime.InteropServices.Marshal]::Copy($p,$aclRaw,0,$aclLength)
            $acl=New-Object Security.AccessControl.RawAcl($aclRaw,0)
            $result.default_dacl=@{raw=[BitConverter]::ToString($aclRaw).Replace('-','');count=$acl.Count}
        }
    }finally{Free $b.Pointer}
    return $result
}
function Admit-Medium($Fields) {
    if($Fields.user -cne $U -or $Fields.owner -cne $U -or $Fields.type -ne 1 -or $Fields.integrity -cne 'S-1-16-8192' -or $Fields.elevated -ne 0 -or $Fields.restricting.Count -ne 0 -or $Fields.appcontainer -ne 0 -or $Fields.ui_access -ne 0 -or ($Fields.user_attributes -band 0x10)){throw 'Medium account/type/IL/elevation/restrictions/AppContainer/UIAccess'}
    $forbidden=@('SeDebugPrivilege','SeAssignPrimaryTokenPrivilege','SeIncreaseQuotaPrivilege','SeTcbPrivilege','SeImpersonatePrivilege','SeBackupPrivilege','SeRestorePrivilege','SeTakeOwnershipPrivilege','SeLoadDriverPrivilege')
    $change=$false
    foreach($priv in $Fields.privileges){
        if($priv.name -in $forbidden){throw ('forbidden present privilege '+$priv.name)}
        if($priv.name -eq 'SeChangeNotifyPrivilege'){$change=[bool]($priv.attributes -band 2)}
        elseif($priv.attributes -band 2){throw ('enabled privilege '+$priv.name)}
    }
    if(-not $change){throw 'ChangeNotify not already enabled'}
}
function No-Impersonation {
    $token=[IntPtr]::Zero
    $ok=$N::OpenThreadToken($N::GetCurrentThread(),0x20008,$false,[ref]$token)
    $err=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
    if($ok){Check-Api ($N::CloseHandle($token)) 'rejected thread token close';throw 'thread token present'}
    if($err -ne 1008){throw ('thread-token query error '+$err)}
}
function New-XM-SA {
    $sd=[IntPtr]::Zero;[uint32]$length=0
    Check-Api ($N::ConvertStringSecurityDescriptorToSecurityDescriptorW($XM,1,[ref]$sd,[ref]$length)) 'X-M conversion'
    $script:LocalSDs.Add($sd)
    $sa=Alloc 24
    [Runtime.InteropServices.Marshal]::WriteInt32($sa,24)
    [Runtime.InteropServices.Marshal]::WriteIntPtr($sa,8,$sd)
    return $sa
}
function Start-Reader([IntPtr]$Input) {
    $reader=[Activator]::CreateInstance($Interop.Reader)
    $reader.Input=$Input;$reader.Buffer=New-Object byte[] 4096
    $pin=[Runtime.InteropServices.GCHandle]::Alloc($reader)
    $callback=[Delegate]::CreateDelegate($Interop.Delegate,$Interop.Reader.GetMethod('Run'))
    $pointer=[Runtime.InteropServices.Marshal]::GetFunctionPointerForDelegate($callback)
    $sa=New-XM-SA;[uint32]$tid=0
    $thread=$N::CreateThread($sa,[UIntPtr]::Zero,$pointer,[Runtime.InteropServices.GCHandle]::ToIntPtr($pin),4,[ref]$tid)
    $worker=@{State=$reader;Thread=$thread;Pin=$pin;Callback=$callback;Joined=$false;SD=$null}
    $script:Readers.Add($worker)
    if($thread -eq [IntPtr]::Zero){$err=[Runtime.InteropServices.Marshal]::GetLastWin32Error();$pin.Free();$worker.Joined=$true;throw ('reader CreateThread '+$err)}
    [void](Own $thread 'O native reader')
    [void](Rights $thread 0x1FFFFF 0)
    $sd=Read-SD $thread
    Admit-XM $sd
    $previous=$N::ResumeThread($thread)
    if($previous -eq 4294967295){throw ('reader ResumeThread error '+[Runtime.InteropServices.Marshal]::GetLastWin32Error())}
    if($previous -ne 1){throw ('reader ResumeThread '+$previous)}
    $worker.SD=$sd
    return $worker
}
function Start-TokenQuery([IntPtr]$Token) {
    # The deadline thread never enters GetTokenInformation for suspended P.
    # A retained native X-M thread invokes only hash-bound local query functions.
    Assert-Hash $PSCommandPath $ReviewedWrapperHash
    $tokens=$null;$errors=$null
    $ast=[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$tokens,[ref]$errors)
    if($errors.Count){throw 'own source parser error'}
    $wanted=@('Alloc','Free','Check-Api','Token-Buffer','Read-Sid','Read-Token','Read-SD','No-Impersonation')
    $definitions=@($ast.FindAll({param($node) $node -is [System.Management.Automation.Language.FunctionDefinitionAst]},$true)|Where-Object{$_.Name -in $wanted}|ForEach-Object{$_.Extent.Text})
    if($definitions.Count -ne $wanted.Count){throw 'query function closure'}
    $space=[System.Management.Automation.Runspaces.RunspaceFactory]::CreateRunspace()
    $space.ThreadOptions=[System.Management.Automation.Runspaces.PSThreadOptions]::UseCurrentThread
    $space.ApartmentState=[Threading.ApartmentState]::MTA
    $space.Open();$space.SessionStateProxy.SetVariable('N',$N);$space.SessionStateProxy.SetVariable('Token',$Token)
    $pipeline=[System.Management.Automation.PowerShell]::Create();$pipeline.Runspace=$space
    $body='$script:Allocations=New-Object ''Collections.Generic.List[IntPtr]'';'+($definitions -join "`n")+
          '; try { No-Impersonation; @{Fields=(Read-Token $Token);SD=(Read-SD $Token)} } finally { foreach($p in @($script:Allocations.ToArray())) { Free $p } }'
    [void]$pipeline.AddScript($body,$true)
    $state=[Activator]::CreateInstance($Interop.Reader);$state.Pipeline=$pipeline
    $pin=[Runtime.InteropServices.GCHandle]::Alloc($state)
    $callback=[Delegate]::CreateDelegate($Interop.Delegate,$Interop.Reader.GetMethod('Query'))
    $sa=New-XM-SA;[uint32]$tid=0
    $handle=$N::CreateThread($sa,[UIntPtr]::Zero,[Runtime.InteropServices.Marshal]::GetFunctionPointerForDelegate($callback),[Runtime.InteropServices.GCHandle]::ToIntPtr($pin),4,[ref]$tid)
    $worker=@{State=$state;Thread=$handle;Pin=$pin;Callback=$callback;Pipeline=$pipeline;Runspace=$space;Joined=$false}
    $script:QueryWorkers.Add($worker)
    if($handle -eq [IntPtr]::Zero){$err=[Runtime.InteropServices.Marshal]::GetLastWin32Error();$worker.Joined=$true;$pin.Free();$pipeline.Dispose();$space.Dispose();throw ('query CreateThread '+$err)}
    [void](Own $handle 'O token query worker')
    [void](Rights $handle 0x1FFFFF 0)
    $sd=Read-SD $handle
    Admit-XM $sd
    $previous=$N::ResumeThread($handle)
    if($previous -eq 4294967295){throw ('query ResumeThread error '+[Runtime.InteropServices.Marshal]::GetLastWin32Error())}
    if($previous -ne 1){throw ('query worker suspend count '+$previous)}
    return $worker
}
function Await-TokenQuery($Worker) {
    while($N::WaitForSingleObject($Worker.Thread,0) -eq 258){
        if($N::GetTickCount64() -ge $O0+15000){Stop-Exact;throw 'P admission token-query deadline'}
        $N::Sleep(25)
    }
    $wait=$N::WaitForSingleObject($Worker.Thread,0)
    if($wait -eq 4294967295){throw ('query-worker wait failed '+[Runtime.InteropServices.Marshal]::GetLastWin32Error())}
    if($wait -ne 0){throw ('query-worker unexpected wait '+$wait)}
    $Worker.Joined=$true
    if($null -ne $Worker.State.QueryException){throw $Worker.State.QueryException}
    if($Worker.Pipeline.HadErrors){
        $first=$Worker.Pipeline.Streams.Error[0]
        throw ('query-worker API/pipeline error: '+$first.Exception.ToString())
    }
    if($Worker.State.Result.Count -ne 1){throw 'query-worker result count'}
    return $Worker.State.Result[0].PSObject.BaseObject
}

function Admit-XM($SD) {
    $denies=@($SD.aces|Where-Object{$_.acl -eq 'DiscretionaryAcl'})
    $labels=@($SD.aces|Where-Object{$_.type -eq 17})
    if($SD.owner -cne $U -or $SD.label -cne 'S-1-16-8192' -or -not($SD.control -band 0x1000) -or $denies.Count -ne 1 -or $denies[0].type -ne 1 -or $denies[0].mask -ne 0x60000 -or $denies[0].sid -cne 'S-1-3-4' -or $denies[0].flags -ne 0 -or $labels.Count -ne 1 -or $labels[0].mask -ne 3){throw 'X-M exact descriptor mismatch'}
}

function Check-Route([string]$Path,[bool]$AllowMissingLeaf=$false) {
    $full=[IO.Path]::GetFullPath($Path)
    if($full -cne $Path -or $full.Substring(2).Contains(':')){throw 'noncanonical/alternate-stream evidence path'}
    $p=$full
    while($p){
        if([IO.File]::Exists($p) -or [IO.Directory]::Exists($p)){
            if([IO.File]::GetAttributes($p) -band [IO.FileAttributes]::ReparsePoint){throw ('reparse route '+$p)}
        }elseif(-not($AllowMissingLeaf -and $p -ceq $full)){throw ('missing evidence ancestor '+$p)}
        $parent=[IO.Path]::GetDirectoryName($p)
        if($parent -eq $p){break};$p=$parent
    }
}
function Charge([long]$Extra,[bool]$Final=$false) {
    if($Extra -lt 0){throw 'negative evidence charge'}
    $cap=$(if($Final){$TotalLimit}else{$PayloadLimit})
    $live=$script:DiskBytes+$script:MemoryBytes+$script:RemoteLiveReservation+$Extra
    if($live -gt $cap){$script:Overflow=$true;throw 'all-representation budget exceeded'}
    $script:Highwater=[Math]::Max($script:Highwater,$live)
}
function Retain-O([string]$Name,$Value) {
    $bytes=Json-Bytes $Value
    if($bytes.Length -gt $RecordLimit){throw 'retained O metadata record cap'}
    # Logical object projection, UTF-16 string and UTF-8 bytes are simultaneous.
    $script:RetainedRepresentations[$Name]=3L*$bytes.Length
    $sum=0L
    foreach($size in $script:RetainedRepresentations.Values){$sum+=$size}
    $script:RetainedBytes=$sum
    $script:MemoryBytes=$OMemoryBase+$sum+2L*$script:Line.Count
    Charge 0 ($Name -eq 'FINAL-P')
}
function Add-Failure($Value) {
    if($script:Failure.Count -ge 8){$script:OmittedFailures++;return}
    $bounded=@{}
    foreach($key in $Value.Keys){
        $item=$Value[$key]
        if($item -is [string] -and $item.Length -gt 512){$item=$item.Substring(0,480)+'[TRUNCATED; bounded diagnostic]'}
        $bounded[$key]=$item
    }
    $script:Failure+=,$bounded
}
function Write-Artifact([string]$Name,[byte[]]$Bytes,[bool]$Final=$false) {
    Check-Route $EvidenceLeaf
    Charge $Bytes.Length $Final
    if(-not $script:Files.ContainsKey($Name)){
        $path=Join-Path $EvidenceLeaf $Name
        $stream=New-Object IO.FileStream($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
        $script:Files[$Name]=@{Stream=$stream;Length=0L;Path=$path}
    }
    $file=$script:Files[$Name]
    $file.Stream.Write($Bytes,0,$Bytes.Length)
    $file.Length+=$Bytes.Length;$script:DiskBytes+=$Bytes.Length
    Check-Route $file.Path
}
function Json-Bytes($Value) {
    $text=ConvertTo-Json -InputObject $Value -Depth 30 -Compress
    return ,[Text.Encoding]::UTF8.GetBytes($text+"`n")
}
function Record-O([string]$Stage,$Data,[bool]$Final=$false) {
    $record=@{schema='L65-RP2-O-1';nonce=$Nonce;stage=$Stage;tick=$N::GetTickCount64();data=$Data}
    $bytes=Json-Bytes $record
    if($bytes.Length -gt 16384){throw 'O record cap'}
    Write-Artifact 'outer.jsonl' $bytes $Final
}
function Receive-Relay([byte[]]$Line) {
    if($Line.Length -gt $RecordLimit -or @($Line|Where-Object{$_ -gt 127}).Count -ne 0){throw 'relay ASCII/record cap'}
    $r=[Text.Encoding]::ASCII.GetString($Line)|ConvertFrom-Json
    if($r.schema -cne 'L65-RP2-RELAY-1' -or $r.nonce -cne $Nonce -or $r.sequence -ne $script:RelaySequence+1){throw 'relay schema/nonce/sequence'}
    $script:RelaySequence=$r.sequence
    if($r.tick -lt $script:O0 -or $r.tick -gt $N::GetTickCount64()){throw 'relay uptime epoch'}
    if($r.stage -eq 'P0'){
        if($null -ne $script:P0 -or $r.data.P0 -lt $script:O0 -or $r.data.P0 -ge $script:O0+20000 -or $r.data.O0 -ne $script:O0 -or $r.data.outer_allowance_ms -ne 20000 -or $r.data.source_hash -cne $ReviewedProbeHash -or $r.data.remote_representation_reservation -ne $RemoteReservation){throw 'P0/source metadata'}
        $script:P0=[uint64]$r.data.P0
        if($r.data.literal_bytes -ne 6583 -or $r.data.literal_sha256 -cne 'D9EC540BCEA9326C67A791DA6C59FC11357C00396B707EEB9FE278FCD08BF2A0'){throw 'frozen literal identity'}
    }elseif($null -eq $script:P0){throw 'missing first P0'}
    if($r.stage -eq 'BEFORE_LOW_ATTEMPT'){
        if($script:LowAttempted){throw 'second Low attempt'}
        $script:LowAttempted=$true;$script:LowCreateKnown=$false
    }
    if($r.stage -eq 'CREATE_RESULT'){
        if(-not $script:LowAttempted -or $script:LowCreateKnown){throw 'create result order'}
        $script:LowCreateKnown=$true;$script:LowCreated=[bool]$r.data.ok
        if($script:LowCreated){
            if($r.data.pid -le 0){throw 'Low create PID'}
            $script:LowPID=$r.data.pid
            foreach($name in @('stdout','stderr','ledger')){Write-Artifact ('low-'+$name+'.bin') ([byte[]]@())}
        }
    }
    if($r.stage -eq 'LOW_BYTES'){
        if($r.section -cne 'capture' -or $r.data.encoding -cne 'hex' -or $r.data.stream -cnotmatch '^(stdout|stderr|ledger)$' -or $r.data.length -lt 1 -or $r.data.length -gt 4096 -or $r.data.bytes.Length -ne $r.data.length*2 -or $r.data.bytes -cnotmatch '^[0-9a-f]+$'){throw 'capture encoding/length'}
        $raw=New-Object byte[] $r.data.length
        for($i=0;$i -lt $raw.Length;$i++){$raw[$i]=[Convert]::ToByte($r.data.bytes.Substring(2*$i,2),16)}
        Write-Artifact ('low-'+$r.data.stream+'.bin') $raw
        $script:LowSizes[$r.data.stream]+=$raw.Length
    }elseif($r.section -in @('U1','U2','U3')){
        Write-Artifact ($r.section+'.jsonl') ($Line+[byte]10)
        $script:SectionCounts[$r.section]++
        if($r.stage -like '*/complete'){$script:InventoryComplete[$r.stage]=$r.data.count}
    }
    if($r.stage -eq 'FINAL'){
        if($null -ne $script:FinalP){throw 'duplicate FINAL'}
        if($r.data.end_tick -gt [Math]::Min($script:P0+15000,$script:O0+20000)){throw 'P final deadline'}
        $script:FinalP=$r.data
        Retain-O 'FINAL-P' $script:FinalP
    }
}
function Validate-LowStreams {
    if(-not $LowCreated){return}
    foreach($name in @('stdout','stderr','ledger')){
        $path=Join-Path $EvidenceLeaf ('low-'+$name+'.bin')
        if(-not $Files.ContainsKey('low-'+$name+'.bin') -or $Files['low-'+$name+'.bin'].Length -ne $LowSizes[$name]){throw 'Low capture byte-length reconciliation'}
        $Files['low-'+$name+'.bin'].Stream.Flush()
        $input=New-Object IO.FileStream($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
        try{
            $line=New-Object 'Collections.Generic.List[byte]'
            $phases=@('READY','END');$count=0
            while($true){
                if($N::GetTickCount64() -ge $O0+20000){throw 'Low capture validation deadline'}
                $b=$input.ReadByte()
                if($b -lt 0){break}
                if($b -gt 127 -or $line.Count -gt $LowRecordLimit){throw 'Low capture ASCII/record cap'}
                if($b -ne 10){$line.Add([byte]$b);continue}
                if($count -ge 2){throw 'extra Low record'}
                $record=[Text.Encoding]::ASCII.GetString($line.ToArray())|ConvertFrom-Json
                $keys=@($record.PSObject.Properties.Name|Sort-Object)
                $expected=$(if($count -eq 0){'nonce|observation|phase|pid|schema|stream'}else{'nonce|phase|pid|schema|stream'})
                if(($keys -join '|') -cne $expected -or $record.schema -cne 'L65-RP2-LOW-1' -or $record.nonce -cne $Nonce -or $record.pid -ne $LowPID -or $record.stream -cne $name -or $record.phase -cne $phases[$count]){throw 'independent Low record grammar/order/identity'}
                $count++;$line.Clear()
            }
            if($count -ne 2 -or $line.Count -ne 0){throw 'missing/truncated Low records'}
        }finally{$input.Dispose()}
    }
}
function Drain-Medium {
    for($i=0;$i -lt $script:Readers.Count;$i++){
        $worker=$script:Readers[$i];$state=$worker.State
        if($state.Error -ne 0){throw ('O ReadFile error '+$state.Error)}
        [Threading.Thread]::MemoryBarrier()
        $count=$state.Count
        if($count -gt 0){
            if($count -gt 4096){throw 'reader count ABI'}
            $raw=New-Object byte[] $count;[Array]::Copy($state.Buffer,$raw,$count)
            $script:MemoryBytes=$OMemoryBase+$script:RetainedBytes+$count+2L*$script:Line.Count
            Charge 0
            Write-Artifact $(if($i -eq 0){'medium-stdout.bin'}else{'medium-stderr.bin'}) $raw
            if($i -eq 0){
                foreach($b in $raw){
                    if($b -eq 10){
                        $line=$script:Line.ToArray();$script:Line.Clear()
                        Receive-Relay $line
                    }else{
                        if($script:Line.Count -ge $RecordLimit){throw 'partial relay line cap'}
                        $script:Line.Add($b)
                    }
                }
            }else{$script:MediumDiagnosticBytes+=$count}
            [Threading.Thread]::MemoryBarrier()
            $state.Count=0
        }
        $script:MediumEOF[$i]=[bool]$state.EOF
    }
    $script:MemoryBytes=$OMemoryBase+$script:RetainedBytes+2L*$script:Line.Count
}
function Stop-Exact {
    if($script:StopRequested){return}
    $script:StopRequested=$true;$script:StopTick=$N::GetTickCount64()
    try{Record-O 'STOP_REQUESTED' @{handle=$script:PHandle.ToInt64();at_most_one=$true} $true}catch{Add-Failure @{stage='stop evidence';message=$_.Exception.Message}}
    $wait=$N::WaitForSingleObject($script:PHandle,0)
    if($wait -eq 258){
        $script:TerminationCalled=$true
        $ok=$N::TerminateProcess($script:PHandle,$StopCode)
        $err=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
        try{Record-O 'TerminateProcess-request' @{ok=$ok;error=$(if($ok){0}else{$err});not_cessation_proof=$true} $true}catch{Add-Failure @{stage='termination evidence';message=$_.Exception.Message}}
        if(-not $ok){Add-Failure @{stage='TerminateProcess';error=$err}}
    }elseif($wait -eq 4294967295){throw ('retained P wait failed '+[Runtime.InteropServices.Marshal]::GetLastWin32Error())}
    elseif($wait -ne 0){throw ('retained P unexpected wait '+$wait)}
}

$Handles=@{};$Allocations=New-Object 'Collections.Generic.List[IntPtr]'
$LocalSDs=New-Object 'Collections.Generic.List[IntPtr]'
$Readers=New-Object 'Collections.Generic.List[object]'
$QueryWorkers=New-Object 'Collections.Generic.List[object]'
$Files=@{};$DiskBytes=0L;$OMemoryBase=131072L;$MemoryBytes=$OMemoryBase;$Highwater=0L;$Overflow=$false
$RetainedRepresentations=@{};$RetainedBytes=0L;$OmittedFailures=0L
$RemoteLiveReservation=$RemoteReservation
$RelaySequence=0;$P0=$null;$O0=0L;$FinalP=$null
$LowAttempted=$false;$LowCreateKnown=$true;$LowCreated=$false;$LowPID=$null
$SectionCounts=@{U1=0;U2=0;U3=0};$InventoryComplete=@{}
$LowSizes=@{stdout=0L;stderr=0L;ledger=0L}
$Line=New-Object 'Collections.Generic.List[byte]'
$MediumEOF=@($false,$false);$MediumDiagnosticBytes=0L
$PHandle=[IntPtr]::Zero;$PThread=[IntPtr]::Zero
$StopRequested=$false;$TerminationCalled=$false;$StopTick=0L;$PResumed=$false
$MediumAttempted=$false;$MediumCreateKnown=$true;$MediumCreated=$false;$ResumeAttempted=$false
$PSignalled=$false;$PExit=$null;$LeafCreated=$false;$Failure=@()
$SourceToken=[IntPtr]::Zero;$AdmissionToken=[IntPtr]::Zero
$AttributeInitialized=$false
$Verdict='RP2_UNKNOWN_FAIL_CLOSED'

try {
    if($RunId -cnotmatch '^[A-Za-z0-9][A-Za-z0-9-]{0,63}$'){throw 'run ID grammar'}
    $expectedLeaf='C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp2-'+$RunId
    if($EvidenceLeaf -cne $expectedLeaf){throw 'unapproved evidence leaf route'}
    Assert-Hash $Probe $ReviewedProbeHash
    Assert-Hash $PSCommandPath $ReviewedWrapperHash
    Assert-Hash $Image $ImageHash
    Verify-PythonClosure
    Assert-Hash $HostImage $HostImageHash
    if($PSVersionTable.PSVersion.ToString() -cne $HostEngineVersion -or [IntPtr]::Size -ne 8 -or $PSHOME -ine 'C:\Windows\System32\WindowsPowerShell\v1.0'){throw 'attended host version/architecture/path'}
    foreach($p in $HostFiles.Keys){Assert-Hash $p $HostFiles[$p]}
    foreach($spec in $HostTrees){Verify-HostTree $spec}
    foreach($assembly in [AppDomain]::CurrentDomain.GetAssemblies()){
        if($assembly.IsDynamic){
            if($assembly.GetName().Name -cne 'Anonymously Hosted DynamicMethods Assembly'){throw ('unbound preexisting dynamic host assembly '+$assembly.FullName)}
            continue
        }
        $location=$assembly.Location
        if($location -and -not @($HostTrees|Where-Object{$location.StartsWith($_[0]+'\',[StringComparison]::OrdinalIgnoreCase)}).Count){throw ('host assembly outside frozen closure '+$location)}
    }
    foreach($p in $HostAbsences){if(Test-Path -LiteralPath $p){throw ('startup absence drift '+$p)}}
    Check-Route $EvidenceLeaf $true
    if(Test-Path -LiteralPath $EvidenceLeaf){throw 'evidence leaf not fresh'}
    $Interop=New-Interop;$N=$Interop.Native
    $observedHost=New-Object Text.StringBuilder 32768;[uint32]$hostLength=32768
    Check-Api ($N::QueryFullProcessImageNameW($N::GetCurrentProcess(),0,$observedHost,[ref]$hostLength)) 'actual attended host image'
    if($observedHost.ToString() -ine $HostImage){throw 'actual attended host image mismatch'}
    Assert-Hash $observedHost.ToString() $HostImageHash
    No-Impersonation
    $token=[IntPtr]::Zero
    Check-Api ($N::OpenProcessToken($N::GetCurrentProcess(),0x20008,[ref]$token)) 'O token open'
    $SourceToken=Own $token 'O primary token'
    [void](Rights $SourceToken 0x20008 0)
    $OFields=Read-Token $SourceToken;Admit-Medium $OFields
    $OSD=Read-SD $SourceToken
    Retain-O 'O-primary' @{Fields=$OFields;SD=$OSD}
    $systemroot=New-Object Text.StringBuilder 32768
    $rootLength=$N::GetWindowsDirectoryW($systemroot,32768)
    if($rootLength -eq 0 -or $rootLength -ge 32768 -or $systemroot.ToString() -ine 'C:\Windows'){throw 'SystemRoot binding'}
    Check-Api ($N::CreateDirectoryW($EvidenceLeaf,[IntPtr]::Zero)) 'atomic fresh evidence leaf'
    $LeafCreated=$true
    Check-Route $EvidenceLeaf
    foreach($artifact in @('medium-stdout.bin','medium-stderr.bin','U1.jsonl','U2.jsonl','U3.jsonl')){Write-Artifact $artifact ([byte[]]@())}
    Record-O 'preflight' @{run_id=$RunId;probe_hash=$ReviewedProbeHash;wrapper_hash=$ReviewedWrapperHash;image_hash=$ImageHash;host_hash=$HostImageHash;host_files=$HostFiles;host_DLL_manifests=$HostTrees;O_token=$OFields;O_token_SD=$OSD;scientific_isolation='no TPCN/neural/fixture/production claims'}
    $writes=New-Object 'Collections.Generic.List[IntPtr]'
    $reads=New-Object 'Collections.Generic.List[IntPtr]'
    $ordinarySA=Alloc 24
    [Runtime.InteropServices.Marshal]::WriteInt32($ordinarySA,24)
    for($i=0;$i -lt 2;$i++){
        $read=[IntPtr]::Zero;$write=[IntPtr]::Zero
        Check-Api ($N::CreatePipe([ref]$read,[ref]$write,$ordinarySA,4096)) 'ordinary Medium pipe'
        $reads.Add((Own $read 'Medium capture read'));$writes.Add((Own $write 'Medium capture write'))
        Check-Api ($N::SetHandleInformation($write,1,1)) 'Medium capture inherit write'
        $rs=Read-SD $read;$ws=Read-SD $write
        Retain-O 'last-Medium-pipe-SDs' @{read=$rs;write=$ws}
        if($rs.owner -cne $U -or $ws.owner -cne $U -or $rs.label -cne 'S-1-16-8192' -or $ws.label -cne 'S-1-16-8192'){throw 'ordinary Medium capture SD'}
        Record-O 'Medium-pipe' @{index=$i;read=$read.ToInt64();write=$write.ToInt64();read_rights=(Rights $read 0 0);write_rights=(Rights $write 0 1);read_SD=$rs;write_SD=$ws}
    }
    [UIntPtr]$attributeSize=[UIntPtr]::Zero
    $ok=$N::InitializeProcThreadAttributeList([IntPtr]::Zero,1,0,[ref]$attributeSize)
    $err=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
    if($ok -or $err -ne 122 -or $attributeSize.ToUInt64() -gt 65536){throw 'O attribute size ABI'}
    $attribute=Alloc ([int]$attributeSize.ToUInt64())
    Check-Api ($N::InitializeProcThreadAttributeList($attribute,1,0,[ref]$attributeSize)) 'O attributes'
    $AttributeInitialized=$true
    $handleList=Alloc 16
    for($i=0;$i -lt 2;$i++){[Runtime.InteropServices.Marshal]::WriteIntPtr($handleList,$i*8,$writes[$i])}
    Check-Api ($N::UpdateProcThreadAttribute($attribute,0,[UIntPtr]0x20002,$handleList,[UIntPtr]16,[IntPtr]::Zero,[IntPtr]::Zero)) 'O exact two HANDLE_LIST'
    $startup=Alloc 112
    [Runtime.InteropServices.Marshal]::WriteInt32($startup,112)
    [Runtime.InteropServices.Marshal]::WriteInt32($startup,60,0x100)
    [Runtime.InteropServices.Marshal]::WriteIntPtr($startup,88,$writes[0])
    [Runtime.InteropServices.Marshal]::WriteIntPtr($startup,96,$writes[1])
    [Runtime.InteropServices.Marshal]::WriteIntPtr($startup,104,$attribute)
    $pi=Alloc 24
    $environment='PYTHONDONTWRITEBYTECODE=1'+[char]0+'PYTHONHASHSEED=0'+[char]0+'SYSTEMROOT='+$systemroot.ToString()+[char]0+[char]0
    $envBytes=[Text.Encoding]::Unicode.GetBytes($environment)
    $env=Alloc $envBytes.Length;[Runtime.InteropServices.Marshal]::Copy($envBytes,0,$env,$envBytes.Length)
    $O0=$N::GetTickCount64()
    $argv=@($Image,'-B',$Probe,'--rp2',$Nonce,[string]$O0,'20000')
    $command=New-Object Text.StringBuilder(($argv|ForEach-Object{Quote-Arg $_}) -join ' ')
    $MediumAttempted=$true;$MediumCreateKnown=$false
    $created=$N::CreateProcessW($Image,$command,[IntPtr]::Zero,[IntPtr]::Zero,$true,0x8040C,$env,$Root,$startup,$pi)
    $createError=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
    $MediumCreateKnown=$true;$MediumCreated=$created
    if(-not $created){Record-O 'NO_MEDIUM_CREATED' @{error=$createError};throw ('CreateProcessW '+$createError)}
    $PHandle=Own ([Runtime.InteropServices.Marshal]::ReadIntPtr($pi,0)) 'P process'
    $PThread=Own ([Runtime.InteropServices.Marshal]::ReadIntPtr($pi,8)) 'P initial thread'
    $ObservedPID=$N::GetProcessId($PHandle)
    if($ObservedPID -eq 0){throw ('P retained PID query '+[Runtime.InteropServices.Marshal]::GetLastWin32Error())}
    if($ObservedPID -ne [Runtime.InteropServices.Marshal]::ReadInt32($pi,16)){throw 'creation-returned/retained P PID mismatch'}
    $processRights=Rights $PHandle 0x1FFFFF 0;$threadRights=Rights $PThread 0x1FFFFF 0
    if($processRights.type -cne 'Process' -or $threadRights.type -cne 'Thread'){throw 'P returned handle object types'}
    $processSD=Read-SD $PHandle;$threadSD=Read-SD $PThread
    Retain-O 'P-process-thread-SDs' @{process=$processSD;thread=$threadSD}
    if($processSD.owner -cne $U -or $threadSD.owner -cne $U -or $processSD.label -cne 'S-1-16-8192' -or $threadSD.label -cne 'S-1-16-8192'){throw 'ordinary P process/thread admission'}
    $token=[IntPtr]::Zero
    Check-Api ($N::OpenProcessToken($PHandle,0x20008,[ref]$token)) 'P admission token'
    $AdmissionToken=Own $token 'P admission token'
    [void](Rights $AdmissionToken 0x20008 0)
    $tokenQuery=Start-TokenQuery $AdmissionToken
    $admitted=Await-TokenQuery $tokenQuery
    $PFields=$admitted.Fields;Admit-Medium $PFields
    $PSD=$admitted.SD
    Retain-O 'P-admission' $admitted
    if($PFields.session -ne $OFields.session){throw 'O/P session mismatch'}
    $name=New-Object Text.StringBuilder 32768;[uint32]$length=32768
    Check-Api ($N::QueryFullProcessImageNameW($PHandle,0,$name,[ref]$length)) 'P image readback'
    if($name.ToString() -ine $Image){throw 'P image identity'}
    Assert-Hash $name.ToString() $ImageHash
    $times=@((Alloc 8),(Alloc 8),(Alloc 8),(Alloc 8))
    Check-Api ($N::GetProcessTimes($PHandle,$times[0],$times[1],$times[2],$times[3])) 'P creation identity'
    [bool]$ambient=$false;Check-Api ($N::IsProcessInJob($PHandle,[IntPtr]::Zero,[ref]$ambient)) 'P ambient job'
    Record-O 'P-admission' @{O0=$O0;P_pid=$ObservedPID;creation_filetime=[Runtime.InteropServices.Marshal]::ReadInt64($times[0]);image=$name.ToString();process_SD=$processSD;thread_SD=$threadSD;token=$PFields;token_SD=$PSD;ambient_job=$ambient;operational_process_mask=0x121401;operational_thread_mask=0x120042;argv=$argv;environment=@{PYTHONHASHSEED='0';PYTHONDONTWRITEBYTECODE='1';SYSTEMROOT=$systemroot.ToString()}}
    foreach($read in $reads){[void](Start-Reader $read)}
    foreach($worker in $Readers){
        while($worker.State.Ready -eq 0){
            if($N::GetTickCount64() -ge $O0+15000){throw 'O reader-ready deadline'}
            if($N::WaitForSingleObject($worker.Thread,0) -eq 0){throw 'O reader exited before readiness'}
            $N::Sleep(1)
        }
        if($worker.State.Error -ne 0){throw 'O reader readiness error'}
    }
    foreach($write in $writes){Close-Owned $write}
    $lastQuery=Start-TokenQuery $AdmissionToken
    $lastAdmitted=Await-TokenQuery $lastQuery
    Retain-O 'P-token-final-readback' $lastAdmitted
    $lastOFields=Read-Token $SourceToken
    $lastOSD=Read-SD $SourceToken
    Retain-O 'O-token-final-readback' @{Fields=$lastOFields;SD=$lastOSD}
    $OFinalRawEqual=$lastOSD.raw -ceq $OSD.raw
    $OFinalSemanticEqual=(SD-Semantics $lastOSD) -ceq (SD-Semantics $OSD)
    $PFinalRawEqual=$lastAdmitted.SD.raw -ceq $PSD.raw
    $PFinalSemanticEqual=(SD-Semantics $lastAdmitted.SD) -ceq (SD-Semantics $PSD)
    Record-O 'O-token-final-readback' @{fields=$lastOFields;SD=$lastOSD;raw_equal=$OFinalRawEqual;semantic_equal=$OFinalSemanticEqual}
    Record-O 'P-token-final-readback' @{fields=$lastAdmitted.Fields;SD=$lastAdmitted.SD;raw_equal=$PFinalRawEqual;semantic_equal=$PFinalSemanticEqual}
    if(-not $OFinalSemanticEqual -or -not $PFinalSemanticEqual){throw 'O/P token object SD drift'}
    Close-Owned $AdmissionToken;Close-Owned $SourceToken
    if($N::GetTickCount64() -ge $O0+15000){throw 'pre-resume O stop cutoff'}
    $ResumeAttempted=$true
    $previous=$N::ResumeThread($PThread)
    if($previous -eq 4294967295){throw ('P ResumeThread error '+[Runtime.InteropServices.Marshal]::GetLastWin32Error())}
    if($previous -ne 1){throw ('P ResumeThread result '+$previous)}
    $PResumed=$true;Close-Owned $PThread
    while($N::GetTickCount64() -lt $O0+20000){
        Drain-Medium
        $wait=$N::WaitForSingleObject($PHandle,0)
        if($wait -eq 0){$PSignalled=$true;break}
        if($wait -eq 4294967295){throw ('P wait failure '+[Runtime.InteropServices.Marshal]::GetLastWin32Error())}
        if($wait -ne 258){throw ('P unexpected wait '+$wait)}
        if($N::GetTickCount64() -ge $O0+15000){Stop-Exact;break}
        $N::Sleep(25)
    }
} catch {
    Add-Failure @{stage='O-controller';message=$_.Exception.Message;tick=$(if($O0 -gt 0){$N::GetTickCount64()}else{0})}
    $diagnostic=$_.Exception.ToString()
    if($diagnostic.Length -gt 1024){$diagnostic=$diagnostic.Substring(0,1024)+'[TRUNCATED]'}
    [Console]::Error.WriteLine('RP2 O-controller failure: '+$diagnostic)
} finally {
    if($PHandle -ne [IntPtr]::Zero){
        try {
            if(-not $PSignalled){Stop-Exact}
            $end=[Math]::Min($O0+20000,$(if($StopRequested){$StopTick+5000}else{$N::GetTickCount64()+5000}))
            while($N::GetTickCount64() -lt $end){
                try{Drain-Medium}catch{Add-Failure @{stage='drain';message=$_.Exception.Message}}
                $wait=$N::WaitForSingleObject($PHandle,0)
                if($wait -eq 0){$PSignalled=$true}
                elseif($wait -eq 4294967295){Add-Failure @{stage='wait';error=[Runtime.InteropServices.Marshal]::GetLastWin32Error()};break}
                if($PSignalled -and $MediumEOF[0] -and $MediumEOF[1]){break}
                $N::Sleep(25)
            }
            if($PSignalled){[uint32]$code=0;Check-Api ($N::GetExitCodeProcess($PHandle,[ref]$code)) 'P retained exit';$PExit=$code}
        }catch{Add-Failure @{stage='stop/wait';message=$_.Exception.Message}}
    }
    foreach($worker in $Readers){
        try{
            if($worker.Thread -eq [IntPtr]::Zero){continue}
            $worker.State.Stop=1
            if($N::WaitForSingleObject($worker.Thread,0) -ne 0){
                $ok=$N::CancelSynchronousIo($worker.Thread);$err=[Runtime.InteropServices.Marshal]::GetLastWin32Error()
                if(-not $ok -and $err -ne 1168){Add-Failure @{stage='CancelSynchronousIo';error=$err}}
                $remaining=[Math]::Max(0,$O0+20000-$N::GetTickCount64())
                $worker.Joined=$N::WaitForSingleObject($worker.Thread,[uint32][Math]::Min(100,$remaining)) -eq 0
            }else{$worker.Joined=$true}
            if($worker.Joined){$worker.Pin.Free();Close-Owned $worker.Thread}
        }catch{Add-Failure @{stage='reader cancellation';message=$_.Exception.Message}}
    }
    foreach($worker in $QueryWorkers){
        try{
            if($worker.Thread -eq [IntPtr]::Zero){continue}
            $worker.Joined=$N::WaitForSingleObject($worker.Thread,0) -eq 0
            if($worker.Joined){$worker.Pipeline.Dispose();$worker.Runspace.Dispose();$worker.Pin.Free();Close-Owned $worker.Thread}
        }catch{Add-Failure @{stage='query-worker closure';message=$_.Exception.Message}}
    }
    $outstanding=@($Readers|Where-Object{-not $_.Joined})+@($QueryWorkers|Where-Object{-not $_.Joined})
    if($PSignalled -and ((-not $ResumeAttempted) -or ($null -ne $FinalP -and $FinalP.cessation_confirmed))){$RemoteLiveReservation=0L}
    # Retain callbacks/buffers if a reader is unjoined; do not free live storage.
    if($outstanding.Count -eq 0){
        foreach($key in @($Handles.Keys)){try{Close-Owned ([IntPtr]$key)}catch{Add-Failure @{stage='handle closure';message=$_.Exception.Message}}}
        foreach($sd in $LocalSDs){if($N::LocalFree($sd) -ne [IntPtr]::Zero){Add-Failure @{stage='SD LocalFree';error=[Runtime.InteropServices.Marshal]::GetLastWin32Error()}}}
        if($AttributeInitialized){$N::DeleteProcThreadAttributeList($attribute)}
        foreach($p in @($Allocations.ToArray())){Free $p}
    }
    $lowComplete=$false
    if($null -ne $FinalP){
        $lowComplete=$FinalP.cessation_confirmed -and $FinalP.verdict -ne 'RP2_UNKNOWN_FAIL_CLOSED' -and $LowCreateKnown -and (($FinalP.Low_created -and $FinalP.Low_signalled -and $FinalP.job_zero -and @($FinalP.Low_EOF|Where-Object{-not $_}).Count -eq 0 -and $FinalP.Low_EOF.Count -eq 3 -and $FinalP.outstanding_workers.Count -eq 0 -and @($FinalP.owned_remaining.PSObject.Properties).Count -eq 0) -or (-not $FinalP.Low_created -and -not $LowCreated))
    }elseif(-not $ResumeAttempted){$lowComplete=$true}
    $outerComplete=$MediumCreateKnown -and (-not $MediumCreated -or $PSignalled) -and ($Readers.Count -eq 0 -or ($MediumEOF[0] -and $MediumEOF[1])) -and $outstanding.Count -eq 0 -and $Line.Count -eq 0 -and $Handles.Count -eq 0
    if($lowComplete -and $outerComplete -and $null -ne $FinalP -and $FinalP.verdict -eq 'RP2_PASS'){
        try{Validate-LowStreams}catch{Add-Failure @{stage='independent Low grammar';message=$_.Exception.Message}}
    }
    if(-not $lowComplete -or -not $outerComplete){$Verdict='RP2_UNKNOWN_FAIL_CLOSED';Alert-Unresolved}
    elseif($null -ne $FinalP -and $FinalP.verdict -eq 'RP2_CONTRACT_DEFECT'){$Verdict='RP2_CONTRACT_DEFECT'}
    elseif($Failure.Count -gt 0 -or $Overflow -or $MediumDiagnosticBytes -gt 0 -or ($null -ne $FinalP -and $FinalP.verdict -eq 'RP2_FAIL')){$Verdict='RP2_FAIL'}
    elseif($null -ne $FinalP -and $FinalP.verdict -eq 'RP2_PASS' -and $PExit -eq 0 -and $LowCreated -and $SectionCounts.U1 -gt 0 -and $SectionCounts.U2 -gt 0 -and $SectionCounts.U3 -gt 0 -and $InventoryComplete.ContainsKey('parent/complete') -and $InventoryComplete.ContainsKey('suspended/complete') -and $InventoryComplete.ContainsKey('READY/complete')){$Verdict='RP2_PASS'}
    else{$Verdict='RP2_PARTIAL'}
    if($LeafCreated){
        try{
            $lengths=@{}
            foreach($name in $Files.Keys){$Files[$name].Stream.Flush();$Files[$name].Stream.Dispose();$Files[$name].Stream=$null}
            $reconciled=0L
            foreach($name in $Files.Keys){
                $f=$Files[$name];Check-Route $f.Path
                $actual=(Get-Item -LiteralPath $f.Path).Length
                if($actual -ne $f.Length){throw 'artifact final length drift'}
                $reconciled+=$actual;$lengths[$name]=@{length=$actual;sha256=(Get-FileHash -LiteralPath $f.Path -Algorithm SHA256).Hash}
            }
            if($reconciled -ne $DiskBytes){throw 'aggregate artifact length drift'}
            $summary=@{schema='L65-RP2-FINAL-1';verdict=$Verdict;run_id=$RunId;O0=$O0;P0=$P0;Medium_attempted=$MediumAttempted;Medium_create_result_known=$MediumCreateKnown;Medium_created=$MediumCreated;Medium_resume_attempted=$ResumeAttempted;P_signalled=$PSignalled;P_exit=$PExit;P_observed_Low=$FinalP;O_independently_observes_Low=$false;Medium_EOF=$MediumEOF;operator_alert=$(if($Verdict -eq 'RP2_UNKNOWN_FAIL_CLOSED'){'Containment unresolved; an unconfirmed Low child/descendant may still be active; no retry/downstream progression.'}else{$null});errors=$Failure;terminate_calls=[int]$TerminationCalled;low_sizes=$LowSizes;files=$lengths;payload_bytes=$DiskBytes;remote_memory_reservation=$RemoteReservation;all_representation_highwater=$Highwater;final_reserve=$FinalReserve;limit=$TotalLimit;encoded_and_decoded_copies_counted=$true;scientific_claim='synthetic finite U1-U3 only; production venv/fixtures/supervisor not qualified'}
            $summary.omitted_bounded_diagnostics=$OmittedFailures
            $summary.O_retained_representation_bytes=$RetainedBytes
            $summary.O_fixed_transient_reservation=$OMemoryBase
            $summary.remote_memory_live_reservation=$RemoteLiveReservation
            $summary.remote_memory_released_only_after_retained_P_signal=$PSignalled
            $summary.remote_memory_release_also_requires_no_resume_or_P_observed_Low_cessation=$RemoteLiveReservation -eq 0
            $bytes=Json-Bytes $summary;$MemoryBytes=$OMemoryBase+$RetainedBytes+$bytes.Length*3
            for($i=0;$i -lt 4;$i++){
                Charge $bytes.Length $true
                $summary.all_representation_highwater=$Highwater
                $next=Json-Bytes $summary
                if($next.Length -eq $bytes.Length){$bytes=$next;break}
                $bytes=$next;$MemoryBytes=$OMemoryBase+$RetainedBytes+$bytes.Length*3
            }
            Write-Artifact 'report.json' $bytes $true
            $report=$Files['report.json'];$report.Stream.Flush();$report.Stream.Dispose();$report.Stream=$null
            $hash=(Get-FileHash -LiteralPath $report.Path -Algorithm SHA256).Hash
            [Console]::WriteLine($Verdict+' report.json bytes='+$report.Length+' sha256='+$hash+' highwater='+$Highwater)
        }catch{$Verdict='RP2_UNKNOWN_FAIL_CLOSED';Alert-Unresolved;[Console]::Error.WriteLine('Evidence finalization failed: '+$_.Exception.Message)}
        foreach($f in $Files.Values){if($null -ne $f.Stream){$f.Stream.Dispose()}}
    }
}
if($Verdict -eq 'RP2_PASS'){exit 0}
exit 3
