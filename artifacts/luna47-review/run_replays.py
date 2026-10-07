"""Run published read-only verifiers, retaining raw stdout and status."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
COMMANDS = {
    "a": ["-m", "experiments.luna47a.run", "--verify"],
    "b": ["-m", "experiments.luna47b.diagnostic", "--replay"],
    "c": ["-m", "experiments.luna47c.evaluate", "--verify"],
    "d": ["-m", "experiments.luna47d.run", "--verify"],
    "e": ["experiments/luna47e/validate.py"],
    "f": ["experiments/luna47f/diagnostic.py", "--check"],
    "g": ["experiments/luna47g/simulate.py", "--verify"],
}
results = []
for letter, arguments in COMMANDS.items():
    cwd = ROOT.parent / f"luna47{letter}"
    env = dict(os.environ, PYTHONPATH=str(cwd), PYTHONHASHSEED="0",
               PYTHONDONTWRITEBYTECODE="1")
    start = time.monotonic()
    command = [sys.executable, *arguments]
    with (OUT / f"lane-{letter}-replay.log").open("wb") as log:
        log.write(f"cwd={cwd}\ncommand={command!r}\n".encode())
        log.flush()
        result = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    record = dict(lane=letter, command=command, cwd=str(cwd),
                  exit_code=result.returncode, seconds=time.monotonic()-start,
                  log_sha256=hashlib.sha256(
                      (OUT / f"lane-{letter}-replay.log").read_bytes()).hexdigest())
    results.append(record)
    print(json.dumps(record), flush=True)
(OUT / "replay-executions.json").write_text(
    json.dumps(results, indent=2)+"\n", encoding="utf-8")
