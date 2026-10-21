from pathlib import Path
import csv,hashlib,json,statistics
out=Path(__file__).resolve().parent
r=json.loads((out/"results.json").read_bytes());p=json.loads((out/"plan.json").read_bytes())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert r["status"]=="COMPLETE" and len(r["rows"])==192
assert r["plan_sha256"]==sha(out/"plan.json") and r["learner_sha256"]==sha(out/"learner.py")
replay=json.loads((out/"replay-results.json").read_bytes())
assert replay["cumulative_observations"]<=p["limits"]["max_plant_observations"]
assert replay["cumulative_choices"]<=p["limits"]["max_heldout_choices"]
models=dict(schema="synthetic-local-priority-models-v1",status="experimental not deployed",
 training_plan_sha256=sha(out/"plan.json"),learner_sha256=sha(out/"learner.py"),
 study_sha256=sha(out/"study.py"),results_sha256=sha(out/"results.json"),models=[])
for row in r["rows"]:
 models["models"].append(dict(model_id=f'osc-v1:{row["case"]}:{row["arm"]}:seed{row["seed"]}',
  trained=row["arm"]!="no_learning",case=row["case"],arm=row["arm"],seed=row["seed"],
  locality="L0",priority=0,score=row["final_center"],weight_representation="uint32, exact sum1000",
  connections=[dict(connection_id="A",weight=row["quantized_weights"][0]),dict(connection_id="B",weight=row["quantized_weights"][1])],
  pending_feedback_at_freeze=row["pending_feedback"],learning_updates=row["updates"]))
with (out/"models.json").open("x",encoding="utf-8") as f:json.dump(models,f,indent=2)
with (out/"summary.csv").open("x",newline="",encoding="utf-8") as f:
 writer=csv.DictWriter(f,fieldnames=list(r["summaries"][0]))
 writer.writeheader();writer.writerows(r["summaries"])
lines=["# Oscillatory priority learning test — 21 October 2026","",
"## Result",
"The fixed experiment completed. The proposed error-amplitude/time-scaled oscillator learned on this synthetic task, but did not meet the predeclared criterion for improvement over paired perturbation and fixed-frequency oscillation. It had higher mean final error than both controls in all four cases.",
"",
"This tests one interpretation: sustained error increases the size of a bounded triangular score sweep; the reversal frequency is a fixed function of supplied local time constants. Error does not directly change frequency, and the frequency multiplier is not learned.",
"",
"## Overall mean final error",
"Lower is better; metric is squared difference between final frozen A-selection probability and the synthetic target service share. It is not classification accuracy.",
"",
"| Method | Mean final squared error |",
"|---|---:|"]
labels={"no_learning":"No learning","paired_perturbation":"Paired perturbation descent","fixed_oscillator":"Fixed-frequency oscillator",
"error_amplitude":"Error-driven amplitude only","time_scaled_frequency":"Time-scaled frequency only","error_time_oscillator":"Proposed combination"}
for arm in p["arms"]:lines.append(f'| {labels[arm]} | {r["overall_mean_final_error"][arm]:.8f} |')
lines+=["","## Per-case mean final error (8 seeds each)","",
"| Case | Paired descent | Fixed oscillator | Proposed combination |",
"|---|---:|---:|---:|"]
for case in p["cases"]:
 d={x["arm"]:x for x in r["summaries"] if x["case"]==case["id"]}
 lines.append("| "+case["id"]+" | "+" | ".join(f'{d[a]["mean_final_error"]:.8f}' for a in ("paired_perturbation","fixed_oscillator","error_time_oscillator"))+" |")
lines+=["","## What was implemented",
"- Scalar local priority score, bounded to[-4,4], converted through sigmoid and quantized to two positive integer connection weights summing to1000.",
"- Triangle-wave parameter drift and reversal around a frozen center within each cycle; ordinary control uses seeded two-sided block perturbations.",
"- Error-dependent amplitude bounded0.1..0.8; fixed-amplitude control0.4.",
"- Time-scaled period=8*max(state time constant, feedback delay, error-averaging time constant). Periods were32,64,128 and64 for fast/slow/delayed/target-shift cases.",
"- The center update uses the observed loss-versus-perturbation slope from completed, tagged cycles. Maximum center step0.2, common gain0.7; no analytic teacher gradient is supplied.",
"- Tagged delayed observations prevent loss from being assigned to the wrong probe cycle. Centers/amplitudes are held per cycle, with stale completed gradients applied to the current global center.",
"",
"## Task and evaluation boundaries",
"The synthetic response is a first-order low-pass response to a trial selection probability. The external target is a service share0.8, changing to0.2 halfway through the shift case. Squared response error plus shared seeded Gaussian measurement noise supplies the learning signal.",
"The teacher target is used only by the external loss/evaluation, not the runtime arbiter. This is a calibration surrogate; there is no dataset, learned neuronal representation, E1/E2 simulation, real classification task or local prediction-credit learner.",
"All methods use the same initial center/state,2048 observations, irregular observation intervals and matched noise per case/seed. Eight training seeds0..7; separate evaluation seeds10000..10007.",
"Final frozen weights were exercised through the actual unchanged local-priority-lottery-v1 arbiter:256 evaluation choices per model. All frequency sanity checks passed. These draws check that the learned weights are applied correctly; they do not demonstrate downstream task improvement.",
"",
"## Important tradeoff and limitations",
"Changing the oscillation period also changed the number of learning updates. In the delayed case, the proposed method made15 updates, the fixed oscillator63 and paired descent507. The proposed method therefore spent more of the fixed observation budget waiting for a full cycle.",
"Equal observation counts do not equal equal update counts, and a common gain is not an optimized per-method hyperparameter comparison. These are concrete confounds; the result rejects superiority of this exact configured candidate, not all error-driven oscillatory learning.",
"Error-amplitude-only and time-scaling-only controls also failed to improve the aggregate mean over the fixed oscillator here. No result was used to retune parameters or rerun the comparison.",
"Time constants/delay are supplied from the toy model, not estimated from neurons. Parameter clamps enforce bounds; they are not a convergence or network-stability proof. Delayed feedback still pending at the observation limit is recorded and was not flushed to gain extra learning.",
"",
"## Validation and budgets",
f'- {r["unit_tests"]["run"]} learner unit tests passed.',
"- Full fixed comparison:192 runs (6 arms*4 cases*8 seeds),393,216 synthetic observations and49,152 held-out arbiter choices.",
"- Additional exact replay checks: proposed method seed0 in fast/delayed/target-shift cases reproduced the complete per-run records, including trained scores, weights, checkpoints and evaluation counts.",
f'- Including those verification replays: {replay["cumulative_observations"]:,} observations <=400,000 and {replay["cumulative_choices"]:,} choices <=50,000.',
f'- Main execution approximately{r["elapsed_seconds"]:.3f}s; replay checks{replay["elapsed_seconds"]:.3f}s. These are diagnostics, not a performance benchmark.',
"- No neural workload, old qualification retry, production edit or arbiter source change occurred.",
"",
"## Next decisive experiment",
"Decouple the learned-center update cadence from the oscillation period: retain a slow probe wave but use a rolling, correctly tagged gradient estimate with a predeclared fixed update cadence. Compare update-matched controls and sweep frequency prospectively rather than select parameters from this outcome.",
"Only after a separate E1 rearm repair/readiness process should an actual event-ordering/classification experiment be attempted. This result does not clear R4 or Luna-72B.",
"",
"## Files",
"- plan.json: prospective settings, metrics, success criterion and limits.",
"- learner.py /test_learner.py /study.py: exact experimental implementation and tests.",
"- results.json /summary.csv: every original run, seed, checkpoint and aggregate.",
"- models.json: all192 model snapshots (160 trained,32 no-learning controls), not deployed.",
"- replay-plan.json /verify_replay.py /replay-results.json: supplementary integrity verification, excluded from the independent-run averages.",
"- manifest.json: retained file sizes and SHA-256, excluding itself.",
""]
with (out/"REPORT.md").open("x",encoding="utf-8") as f:f.write("\n".join(lines))
files=[dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f)) for f in sorted(out.iterdir()) if f.is_file()]
encoded=(json.dumps(dict(schema="oscillatory-priority-artifacts-v1",files=files,self_excluded=True),indent=2)+"\n").encode()
assert sum(f["bytes"] for f in files)+len(encoded)<=p["limits"]["max_result_bytes"]
with (out/"manifest.json").open("xb") as f:f.write(encoded)
print(json.dumps(dict(artifacts=len(files)+1,total_bytes=sum(f["bytes"] for f in files)+len(encoded),models=len(models["models"]),
 manifest_sha256=sha(out/"manifest.json")),indent=2))
