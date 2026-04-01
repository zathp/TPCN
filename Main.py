from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_vhdl(clean: bool, open_wave: bool) -> int:
	workdir = ROOT / "VHDL_implementation"
	script = workdir / "run_ghdl.ps1"
	vcd = workdir / "tpcn_cell_tb.vcd"

	if not script.exists():
		print(f"Missing VHDL runner script: {script}")
		return 2

	if clean:
		for artifact in (workdir / "work-obj08.cf", vcd):
			if artifact.exists():
				artifact.unlink()

	cmd = [
		"powershell",
		"-NoProfile",
		"-ExecutionPolicy",
		"Bypass",
		"-File",
		str(script),
	]

	print("Running VHDL simulation...")
	result = subprocess.run(cmd, cwd=workdir)

	if result.returncode == 0:
		print("VHDL simulation completed successfully.")
		if vcd.exists():
			print(f"Waveform generated: {vcd}")
			if open_wave:
				try:
					# Opens with OS-associated app (e.g., GTKWave if associated).
					vcd.resolve().open("rb").close()
					subprocess.run(["powershell", "-NoProfile", "-Command", f"Start-Process '{vcd}'"], check=False)
				except Exception as ex:  # pragma: no cover
					print(f"Could not open waveform automatically: {ex}")
	else:
		print(f"VHDL simulation failed with exit code {result.returncode}")

	return result.returncode


def run_baseline_3d(extra_args: list[str]) -> int:
	entry = ROOT / "TPCN_baseline_engine" / "Main_3d.py"
	if not entry.exists():
		print(f"Missing baseline entry script: {entry}")
		return 2

	cmd = [sys.executable, str(entry), *extra_args]
	print("Launching baseline 3D simulation...")
	return subprocess.run(cmd, cwd=entry.parent).returncode


def run_training(extra_args: list[str]) -> int:
	entry = ROOT / "train_tpcn.py"
	if not entry.exists():
		print(f"Missing training entry script: {entry}")
		return 2

	forward_args = extra_args[1:] if extra_args and extra_args[0] == "--" else extra_args
	cmd = [sys.executable, str(entry), *forward_args]
	print("Launching Python training loop...")
	return subprocess.run(cmd, cwd=ROOT).returncode


def run_distance_signal_copy_training(extra_args: list[str]) -> int:
	entry = ROOT / "train_signal_copy_distance.py"
	if not entry.exists():
		print(f"Missing distance-copy training entry script: {entry}")
		return 2

	forward_args = extra_args[1:] if extra_args and extra_args[0] == "--" else extra_args
	cmd = [sys.executable, str(entry), *forward_args]
	print("Launching distance signal-copy training loop...")
	return subprocess.run(cmd, cwd=ROOT).returncode


def run_signal_copy_pygame_gui(extra_args: list[str]) -> int:
	entry = ROOT / "gui_signal_copy_pygame.py"
	if not entry.exists():
		print(f"Missing pygame GUI script: {entry}")
		return 2

	forward_args = extra_args[1:] if extra_args and extra_args[0] == "--" else extra_args
	cmd = [sys.executable, str(entry), *forward_args]
	print("Launching distance signal-copy pygame GUI...")
	return subprocess.run(cmd, cwd=ROOT).returncode


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="TPCN project launcher (VHDL simulation + baseline engine)."
	)
	subparsers = parser.add_subparsers(dest="command")

	vhdl_parser = subparsers.add_parser("vhdl", help="Run VHDL simulation via GHDL")
	vhdl_parser.add_argument(
		"--clean",
		action="store_true",
		help="Remove previous simulation artifacts before running.",
	)
	vhdl_parser.add_argument(
		"--open-wave",
		action="store_true",
		help="Open generated VCD file with default associated app.",
	)

	baseline_parser = subparsers.add_parser(
		"baseline3d", help="Run baseline 3D engine entrypoint"
	)
	baseline_parser.add_argument(
		"args",
		nargs=argparse.REMAINDER,
		help="Optional arguments forwarded to TPCN_baseline_engine/Main_3d.py",
	)

	train_parser = subparsers.add_parser(
		"train", help="Run Python training loop (supports multi-GPU)"
	)
	train_parser.add_argument(
		"args",
		nargs=argparse.REMAINDER,
		help="Optional arguments forwarded to train_tpcn.py",
	)

	train_copy_parser = subparsers.add_parser(
		"traincopy", help="Run distance-constrained signal-copy training pipeline"
	)
	train_copy_parser.add_argument(
		"args",
		nargs=argparse.REMAINDER,
		help="Optional arguments forwarded to train_signal_copy_distance.py",
	)

	gui_copy_parser = subparsers.add_parser(
		"guicopy", help="Run realtime pygame visualization for signal-copy checkpoints"
	)
	gui_copy_parser.add_argument(
		"args",
		nargs=argparse.REMAINDER,
		help="Optional arguments forwarded to gui_signal_copy_pygame.py",
	)

	return parser


def main() -> int:
	parser = build_parser()
	args = parser.parse_args()

	if args.command is None:
		print("No command provided; defaulting to 'vhdl'.")
		return run_vhdl(clean=False, open_wave=False)

	if args.command == "vhdl":
		return run_vhdl(clean=args.clean, open_wave=args.open_wave)

	if args.command == "baseline3d":
		return run_baseline_3d(extra_args=args.args)

	if args.command == "train":
		return run_training(extra_args=args.args)

	if args.command == "traincopy":
		return run_distance_signal_copy_training(extra_args=args.args)

	if args.command == "guicopy":
		return run_signal_copy_pygame_gui(extra_args=args.args)

	parser.print_help()
	return 2


if __name__ == "__main__":
	raise SystemExit(main())
