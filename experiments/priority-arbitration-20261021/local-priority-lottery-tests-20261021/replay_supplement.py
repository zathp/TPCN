from pathlib import Path
import hashlib,json,sys,time
OUT=Path(__file__).resolve().parent;SOURCE=OUT.parent/"local-priority-lottery-v1"
original=json.loads((OUT/"results.json").read_bytes())
plan=json.loads((OUT/"replay-plan.json").read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE/"arbiter.py")==original["source_sha256"]
sys.path.insert(0,str(SOURCE))
from arbiter import Request,choose
rows=[];calls=0;start=time.monotonic()
case=next(c for c in original["frequency"] if c["id"]==plan["case_id"])
for seed in plan["seeds"]:
 h=hashlib.sha256()
 for i in range(plan["draws_per_seed"]):
  assert calls<plan["max_calls"] and time.monotonic()-start<plan["max_wall_seconds"]
  d=choose([Request("L0",0,"1","event-1",1.,1),Request("L0",0,"0","event-0",1.,3)],
       locality="L0",now=1.,seed=seed,decision_id=f'weighted31:{i}',
       model_id="illustrative-fixed-weights-not-trained")
  h.update(bytes([int(d.winner_connection_id)]));calls+=1
 expected=next(s["stream_sha256"] for s in case["seeds"] if s["seed"]==seed)
 assert h.hexdigest()==expected
 rows.append(dict(seed=seed,stream_sha256=h.hexdigest(),exact_match=True))
result=dict(status="PASS",checks=len(rows),calls=calls,elapsed_seconds=time.monotonic()-start,
 original_results_sha256=sha(OUT/"results.json"),replay_plan_sha256=sha(OUT/"replay-plan.json"),
 source_sha256=sha(SOURCE/"arbiter.py"),streams=rows)
with (OUT/"replay-results.json").open("x",encoding="utf-8") as f:json.dump(result,f,indent=2)
print(json.dumps(dict(status="PASS",checks=len(rows),calls=calls,elapsed_seconds=result["elapsed_seconds"])))
