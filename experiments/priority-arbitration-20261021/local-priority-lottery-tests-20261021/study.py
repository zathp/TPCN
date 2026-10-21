"""Bounded isolated arbiter validation; no neuron or training execution."""
import hashlib, io, json, math, sys, time, unittest
from collections import Counter, deque
from dataclasses import asdict
from pathlib import Path

OUT=Path(__file__).resolve().parent
SOURCE=OUT.parent/"local-priority-lottery-v1"
plan=json.loads((OUT/"plan.json").read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frozen=json.loads((SOURCE/"manifest.json").read_bytes())
for f in frozen["files"]:
 assert sha(SOURCE/f["path"])==f["sha256"],"Reference source/record drift"
sys.path.insert(0,str(SOURCE))
from arbiter import Request, choose
import test_arbiter

started=time.monotonic();calls=0
result=dict(schema="arbiter-isolated-results-v1",source_sha256=sha(SOURCE/"arbiter.py"),
 plan_sha256=sha(OUT/"plan.json"),status="RUNNING",checks=[],frequency=[],learning="NOT TRAINED",
 neural_execution=False,limits=plan["limits"])
def check(name,condition,detail=None):
 result["checks"].append(dict(name=name,passed=bool(condition),detail=detail))
 if not condition:raise AssertionError(name)
def select(requests,*,seed=0,decision_id="slot",now=1.,locality="L0"):
 global calls
 if calls>=plan["limits"]["max_study_arbiter_calls"]:raise RuntimeError("study call cap")
 if time.monotonic()-started>plan["limits"]["max_wall_seconds"]:raise RuntimeError("study wall cap")
 calls+=1
 return choose(requests,locality=locality,now=now,seed=seed,decision_id=decision_id,
               model_id="illustrative-fixed-weights-not-trained")
def request(i,w,**kw):
 return Request(kw.get("locality","L0"),kw.get("priority",0),str(i),
                kw.get("event",f"event-{i}"),kw.get("timestamp",1.),w)
def deviation(count,n,p):
 if p in (0,1):return 0. if count==n*p else float("inf")
 return abs(count-n*p)/math.sqrt(n*p*(1-p))

try:
 log=io.StringIO()
 suite=unittest.defaultTestLoader.loadTestsFromModule(test_arbiter)
 unit=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
 result["unit_tests"]=dict(run=unit.testsRun,failures=len(unit.failures),errors=len(unit.errors),output=log.getvalue())
 check("original_unit_suite",unit.wasSuccessful())
 for case in plan["cases"]:
  weights=case["weights"];effective=weights if any(weights) else [1]*len(weights)
  probabilities=[w/sum(effective) for w in effective]
  requests=[request(i,w) for i,w in enumerate(weights)]
  aggregate=[0]*len(weights);seed_rows=[];original_hashes={}
  for seed in plan["seed_set"]:
   counts=[0]*len(weights);gaps=[0]*len(weights);maxgaps=[0]*len(weights);stream=hashlib.sha256()
   for i in range(plan["draws_per_seed_per_case"]):
    d=select(requests,seed=seed,decision_id=f'{case["id"]}:{i}')
    winner=int(d.winner_connection_id);counts[winner]+=1;stream.update(bytes([winner]))
    for j in range(len(weights)):
     gaps[j]=0 if j==winner else gaps[j]+1;maxgaps[j]=max(maxgaps[j],gaps[j])
   z=[deviation(c,plan["draws_per_seed_per_case"],p) for c,p in zip(counts,probabilities)]
   check(f'{case["id"]}/seed{seed}/frequency',max(z)<=6.)
   seed_rows.append(dict(seed=seed,counts=counts,max_abs_z=max(z),max_consecutive_unselected=maxgaps,
                         stream_sha256=stream.hexdigest()))
   aggregate=[a+b for a,b in zip(aggregate,counts)]
   original_hashes[seed]=stream.hexdigest()
  n=plan["draws_per_seed_per_case"]*len(plan["seed_set"])
  z=[deviation(c,n,p) for c,p in zip(aggregate,probabilities)]
  check(case["id"]+"/aggregate_frequency",max(z)<=6.)
  result["frequency"].append(dict(id=case["id"],weights=weights,effective_weights=effective,
      probabilities=probabilities,draws=n,counts=aggregate,observed_fractions=[c/n for c in aggregate],
      max_abs_z=max(z),seeds=seed_rows))
  if case["id"]==plan["replay_case"]:
   for seed in plan["seed_set"]:
    replay=hashlib.sha256()
    for i in range(plan["draws_per_seed_per_case"]):
     d=select(list(reversed(requests)),seed=seed,decision_id=f'{case["id"]}:{i}')
     replay.update(bytes([int(d.winner_connection_id)]))
    check(f"full_stream_replay_seed{seed}",replay.hexdigest()==original_hashes[seed])
 # Finite backlog: caller commits service and exposes exactly one queue head per connection.
 queues={str(i):deque(request(i,[3,1,4,2,1,5,2,1][i],event=f"{i}:{j}") for j in range(8)) for i in range(8)}
 served=[];last={};max_service_gap={str(i):0 for i in range(8)}
 for slot in range(64):
  heads=[q[0] for q in queues.values() if q]
  d=select(heads,seed=5,decision_id=f"finite-burst:{slot}")
  item=queues[d.winner_connection_id].popleft()
  check(f"committed_head_{slot}",item.event_id==d.winner_event_id)
  gap=slot-last.get(item.connection_id,-1)-1
  max_service_gap[item.connection_id]=max(max_service_gap[item.connection_id],gap)
  last[item.connection_id]=slot;served.append(item.event_id)
 check("finite_burst_no_loss_or_duplication",len(set(served))==64 and not any(queues.values()))
 for i in range(8):
  check(f"connection{i}_fifo",[e for e in served if e.startswith(f"{i}:")]==[f"{i}:{j}" for j in range(8)])
 result["finite_burst"]=dict(serviced=64,unique=64,max_service_gap_slots=max_service_gap,
      caveat="Finite queue emptied; no general bounded-wait guarantee inferred")
 # Adversarial finite same-timestamp high-priority backlog.
 low=request("low",100,priority=1)
 low_served=0
 for slot in range(plan["priority_backlog"]["high_priority_heads"]):
  high=request("high",1,priority=0,event=f"high:{slot}")
  d=select([low,high],decision_id=f"priority-backlog:{slot}")
  low_served+=d.winner_event_id==low.event_id
 check("strict_priority_backlog_behavior",low_served==0)
 result["priority_backlog"]=dict(high_requests_serviced=256,low_requests_serviced=low_served,
      outcome="STARVATION RISK DEMONSTRATED under continued same-timestamp higher-priority backlog",
      caveat="Policy limitation, not a lottery probability or source-code failure")
 d=select([low],decision_id="after-high-drained")
 check("low_priority_served_after_high_backlog_drains",d.winner_event_id==low.event_id)
 old=request("older-low",1,priority=9,timestamp=.5)
 new=request("new-high",100,priority=0,timestamp=1.)
 check("chronology_overrides_newer_high_priority",select([old,new]).winner_event_id==old.event_id)
 for i in range(64):
  a=[request("A",3),request("B",1)]
  b=a+[request("outside",999,locality="L1"),request("lower",999,priority=9)]
  check(f"pool_isolation_{i}",select(a,decision_id=f"isolated:{i}")==select(b,decision_id=f"isolated:{i}"))
 result["status"]="PASS_WITH_KNOWN_PRIORITY_FAIRNESS_LIMITATION"
except Exception as error:
 result["status"]="FAIL"
 result["error"]=str(error)
finally:
 result["study_calls"]=calls;result["elapsed_seconds"]=time.monotonic()-started
 result["source_unchanged"]=sha(SOURCE/"arbiter.py")==result["source_sha256"]
 encoded=(json.dumps(result,indent=2,allow_nan=False)+"\n").encode()
 if len(encoded)>plan["limits"]["max_result_bytes"]:raise RuntimeError("result byte cap")
 with (OUT/"results.json").open("xb") as f:f.write(encoded)
 print(json.dumps(dict(status=result["status"],calls=calls,elapsed_seconds=result["elapsed_seconds"],
   checks=len(result["checks"]),frequency=[dict(id=c["id"],fractions=c["observed_fractions"]) for c in result["frequency"]],
   priority_backlog=result.get("priority_backlog"),source_unchanged=result["source_unchanged"]),indent=2))
sys.exit(0 if result["status"].startswith("PASS") else 1)
