import ast,collections,hashlib,json,math,random,statistics,sys,time
from pathlib import Path
from learner import Learner,probability,quantized_weights
OUT=Path(__file__).resolve().parent;SOURCE=OUT.parent/"local-priority-lottery-v1"
sys.path.insert(0,str(SOURCE))
from arbiter import Request,choose
PLAN=json.loads((OUT/"plan.json").read_bytes())
original=json.loads((OUT/"results.json").read_bytes())
replay=json.loads((OUT/"replay-plan.json").read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((OUT/"learner.py").read_bytes())==original["learner_sha256"]
assert sha((OUT/"plan.json").read_bytes())==original["plan_sha256"]
assert sha((SOURCE/"arbiter.py").read_bytes())==original["arbiter_sha256"]
observations=original["plant_observations"];choices=original["heldout_choices"]
started=time.monotonic()
def budget():
 if time.monotonic()-started>replay["max_wall_seconds"]:raise RuntimeError("replay time cap")
# Compile only the original fit function. Importing study.py would execute its whole matrix.
tree=ast.parse((OUT/"study.py").read_bytes())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="fit")
exec(compile(ast.Module(body=[node],type_ignores=[]),str(OUT/"study.py"),"exec"),globals())
canonical=lambda o:json.dumps(o,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
rows=[]
for selected in replay["selected"]:
 index,case=next((i,c) for i,c in enumerate(PLAN["cases"]) if c["id"]==selected["case"])
 seed=selected["seed"];rng=random.Random(7000+index*100+seed)
 noise=[rng.gauss(0,PLAN["model"]["noise_sd"]) for _ in range(PLAN["observations_per_run"])]
 actual=fit(selected["arm"],case,seed,noise)
 expected=next(r for r in original["rows"] if r["case"]==case["id"] and r["arm"]==selected["arm"] and r["seed"]==seed)
 assert canonical(actual)==canonical(expected),"Training replay mismatch"
 rows.append(dict(**selected,exact_match=True,canonical_row_sha256=sha(canonical(actual))))
result=dict(status="PASS",checks=rows,cumulative_observations=observations,
 cumulative_choices=choices,extra_observations=observations-original["plant_observations"],
 extra_choices=choices-original["heldout_choices"],elapsed_seconds=time.monotonic()-started,
 original_results_sha256=sha((OUT/"results.json").read_bytes()),
 replay_plan_sha256=sha((OUT/"replay-plan.json").read_bytes()))
with (OUT/"replay-results.json").open("x",encoding="utf-8") as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
