"""One fixed external optimizer experiment; never imports TPCN/E1."""
import collections,hashlib,io,json,math,random,statistics,sys,time,unittest
from pathlib import Path
from learner import Learner,probability,quantized_weights
import test_learner

OUT=Path(__file__).resolve().parent
PLAN=json.loads((OUT/"plan.json").read_bytes())
SOURCE=OUT.parent/"local-priority-lottery-v1"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=json.loads((SOURCE/"manifest.json").read_bytes())
for f in original["files"]:assert sha(SOURCE/f["path"])==f["sha256"],"Arbiter source drift"
sys.path.insert(0,str(SOURCE))
from arbiter import Request,choose
source_hash=sha(SOURCE/"arbiter.py")
started=time.monotonic();observations=choices=0
result=dict(schema="oscillatory-priority-results-v1",status="RUNNING",
 plan_sha256=sha(OUT/"plan.json"),learner_sha256=sha(OUT/"learner.py"),
 arbiter_sha256=source_hash,rows=[],synthetic_only=True,neural_execution=False)
def budget():
 if time.monotonic()-started>PLAN["limits"]["max_wall_seconds"]:raise RuntimeError("wall cap")
def fit(arm,case,seed,noise):
 global observations,choices
 learner=Learner(arm,PLAN["learner"],case,seed,PLAN["limits"])
 pending=collections.deque();t=0.;state=PLAN["learner"]["initial_probability_state"]
 history=[];last_quarter=[];feedback_count=0;max_pending=0
 for i in range(PLAN["observations_per_run"]):
  budget()
  if observations>=PLAN["limits"]["max_plant_observations"]:raise RuntimeError("observation cap")
  trial,identity,delta=learner.probe(t)
  dt=PLAN["observation_intervals"][i%len(PLAN["observation_intervals"])]
  p=probability(trial)
  decay=math.exp(-dt/case["state_tau"])
  state=p+(state-p)*decay
  new_t=t+dt
  if not new_t>t or not 0<=state<=1:raise RuntimeError("invalid time/state")
  target=case["target_after"] if case["shift_step"] is not None and i>=case["shift_step"] else case["target_before"]
  loss=(state-target)**2+noise[i]
  if len(pending)>=PLAN["limits"]["max_pending_feedback"]:raise RuntimeError("feedback queue cap")
  pending.append((new_t+case["feedback_delay"],identity,delta,loss))
  observations+=1;t=new_t;max_pending=max(max_pending,len(pending))
  while pending and pending[0][0]<=t:
   due,identity,delta,loss=pending.popleft()
   learner.feedback(identity,delta,loss,due);feedback_count+=1
  if not -4<=learner.center<=4 or not math.isfinite(learner.center):raise RuntimeError("center bound")
  if i>=3*PLAN["observations_per_run"]//4:last_quarter.append((probability(learner.center)-target)**2)
  if (i+1)%PLAN["checkpoint_stride"]==0:
   history.append(dict(n=i+1,t=t,center=learner.center,error_estimate=learner.error,
       amplitude=learner.current.amplitude,period=learner.current.period,updates=learner.updates))
 learner.finish(t)
 weights=quantized_weights(learner.center);p_exact=weights[0]/sum(weights)
 selected=0
 for j in range(PLAN["heldout_decisions_per_model"]):
  budget()
  if choices>=PLAN["limits"]["max_heldout_choices"]:raise RuntimeError("choice cap")
  d=choose([Request("L0",0,"A","A",1.,weights[0]),Request("L0",0,"B","B",1.,weights[1])],
      locality="L0",now=1.,seed=seed+PLAN["heldout_seed_offset"],
      decision_id=f'evaluation:{case["id"]}:{j}',model_id=f'{arm}:{case["id"]}:{seed}')
  selected+=d.winner_connection_id=="A";choices+=1
 n=PLAN["heldout_decisions_per_model"]
 z=abs(selected-n*p_exact)/math.sqrt(n*p_exact*(1-p_exact))
 if z>6:raise RuntimeError("heldout arbitration frequency check")
 return dict(arm=arm,case=case["id"],seed=seed,final_center=learner.center,
     final_probability=probability(learner.center),quantized_weights=weights,
     target_final=case["target_after"],final_true_squared_error=(probability(learner.center)-case["target_after"])**2,
     last_quarter_true_squared_error=statistics.mean(last_quarter),
     heldout_fraction=selected/n,heldout_max_z=z,updates=learner.updates,
     completed_cycles=learner.updates+learner.skipped,pending_feedback=len(pending),
     live_cycles=len(learner.cycles),feedback_received=feedback_count,max_pending=max_pending,
     max_gradient=learner.max_gradient,max_center_step=learner.max_step,checkpoints=history)

try:
 log=io.StringIO();u=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_learner))
 result["unit_tests"]=dict(run=u.testsRun,failures=len(u.failures),errors=len(u.errors),output=log.getvalue())
 if not u.wasSuccessful():raise RuntimeError("learner unit validation failed; study not started")
 for index,case in enumerate(PLAN["cases"]):
  for seed in PLAN["seeds"]:
   rng=random.Random(7000+index*100+seed)
   noise=[rng.gauss(0,PLAN["model"]["noise_sd"]) for _ in range(PLAN["observations_per_run"])]
   for arm in PLAN["arms"]:
    result["rows"].append(fit(arm,case,seed,noise))
  print("Completed case "+case["id"],flush=True)
 summaries=[]
 for case in PLAN["cases"]:
  for arm in PLAN["arms"]:
   rows=[r for r in result["rows"] if r["case"]==case["id"] and r["arm"]==arm]
   values=[r["final_true_squared_error"] for r in rows]
   summaries.append(dict(case=case["id"],arm=arm,mean_final_error=statistics.mean(values),
      sample_sd=statistics.stdev(values),mean_last_quarter_error=statistics.mean(r["last_quarter_true_squared_error"] for r in rows),
      mean_updates=statistics.mean(r["updates"] for r in rows),
      improved_over_no_learning_seeds=sum(x<.09 for x in values),n=len(values)))
 comparisons=[]
 for case in PLAN["cases"]:
  lookup={r["arm"]:r["mean_final_error"] for r in summaries if r["case"]==case["id"]}
  wins=all(lookup["error_time_oscillator"]<lookup[b] for b in ("paired_perturbation","fixed_oscillator"))
  paired={}
  for b in ("paired_perturbation","fixed_oscillator"):
   paired[b]=sum(next(r["final_true_squared_error"] for r in result["rows"] if r["arm"]=="error_time_oscillator" and r["case"]==case["id"] and r["seed"]==s)
      <next(r["final_true_squared_error"] for r in result["rows"] if r["arm"]==b and r["case"]==case["id"] and r["seed"]==s) for s in PLAN["seeds"])
  comparisons.append(dict(case=case["id"],full_method_lower_than_both= wins,paired_seed_wins=paired))
 overall={a:statistics.mean(r["final_true_squared_error"] for r in result["rows"] if r["arm"]==a) for a in PLAN["arms"]}
 success=sum(c["full_method_lower_than_both"] for c in comparisons)>=3 and all(overall["error_time_oscillator"]<overall[b] for b in ("paired_perturbation","fixed_oscillator"))
 result.update(status="COMPLETE",summaries=summaries,comparisons=comparisons,
     overall_mean_final_error=overall,predeclared_improvement_criterion_met=success)
except Exception as error:
 result.update(status="STOPPED",reason=str(error))
finally:
 result.update(plant_observations=observations,heldout_choices=choices,elapsed_seconds=time.monotonic()-started,
               original_arbiter_unchanged=sha(SOURCE/"arbiter.py")==source_hash)
 encoded=(json.dumps(result,indent=2,allow_nan=False)+"\n").encode()
 if len(encoded)>PLAN["limits"]["max_result_bytes"]:raise RuntimeError("result byte cap")
 with (OUT/"results.json").open("xb") as f:f.write(encoded)
 print(json.dumps(dict(status=result["status"],unit_tests=result.get("unit_tests",{}).get("run"),
    plant_observations=observations,heldout_choices=choices,elapsed_seconds=result["elapsed_seconds"],
    criterion=result.get("predeclared_improvement_criterion_met"),
    overall=result.get("overall_mean_final_error"),comparisons=result.get("comparisons"),
    reason=result.get("reason")),indent=2))
sys.exit(0 if result["status"]=="COMPLETE" else 1)
