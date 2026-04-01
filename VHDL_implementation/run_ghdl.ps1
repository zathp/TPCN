$ErrorActionPreference = 'Stop'

$ghdlCmd = $null
try {
	$ghdlCmd = (Get-Command ghdl -ErrorAction Stop).Source
} catch {
	$wingetPkg = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Directory -ErrorAction SilentlyContinue |
		Where-Object { $_.Name -like "ghdl.ghdl.ucrt64.mcode*" } |
		Select-Object -First 1

	$candidatePaths = @(
		"$env:LOCALAPPDATA\Microsoft\WinGet\Links\ghdl.exe",
		"$env:ProgramFiles\ghdl\bin\ghdl.exe",
		$(if ($wingetPkg) { Join-Path $wingetPkg.FullName "bin\ghdl.exe" })
	)
	foreach ($p in $candidatePaths) {
		if (Test-Path $p) {
			$ghdlCmd = $p
			break
		}
	}
}

if (-not $ghdlCmd) {
	throw "GHDL executable not found. Install GHDL or restart the shell so PATH updates are applied."
}

Write-Host "Analyzing VHDL files..."
& $ghdlCmd -a --std=08 .\tpcn_cell.vhd
& $ghdlCmd -a --std=08 .\tb_tpcn_cell.vhd

Write-Host "Elaborating testbench..."
& $ghdlCmd -e --std=08 tb_tpcn_cell

Write-Host "Running simulation..."
& $ghdlCmd -r --std=08 tb_tpcn_cell --stop-time=1us --vcd=tpcn_cell_tb.vcd

Write-Host "Simulation complete. Waveform: tpcn_cell_tb.vcd"
