"""Fixed prospective matrix. Imports have no execution or file-writing side effects."""
import collections
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import sys
import time

from learner import Learner, probability, quantized_weights

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent / 'local-priority-lottery-v1'
sys.path.insert(0, str(SOURCE))
from arbiter import Request, choose


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_plan():
    return json.loads((OUT / 'plan.json').read_text(encoding='utf-8-sig'))


class Budget:
    def __init__(self, plan):
        self.limits = plan['limits']
        self.started = time.monotonic()
        self.observations = self.choices = 0

    def charge(self, kind):
        if time.monotonic() - self.started > self.limits['max_wall_seconds']:
            raise RuntimeError('wall cap')
        name, limit = ('observations', 'max_plant_observations') if kind == 'observation' else ('choices', 'max_heldout_choices')
        if getattr(self, name) >= self.limits[limit]:
            raise RuntimeError(kind + ' cap')
        setattr(self, name, getattr(self, name) + 1)


def fit(plan, arm, case, seed, noise, budget):
    learner = Learner(arm, plan['learner'], case, seed, plan['limits'])
    pending = collections.deque()
    t, state = 0., .5
    last_quarter = []
    max_pending = 0
    for i in range(plan['observations_per_run']):
        budget.charge('observation')
        p = learner.probe(t)
        dt = plan['observation_intervals'][i % len(plan['observation_intervals'])]
        decay = math.exp(-dt / case['state_tau'])
        state = probability(p.trial) + (state - probability(p.trial)) * decay
        t += dt
        target = case['target_after'] if case['shift_step'] is not None and i >= case['shift_step'] else case['target_before']
        loss = (state - target) ** 2 + noise[i]
        pending.append((t + case['feedback_delay'], p.identity, loss))
        max_pending = max(max_pending, len(pending))
        if len(pending) > plan['limits']['max_pending_feedback']:
            raise RuntimeError('plant queue cap')
        while pending and pending[0][0] <= t:
            receipt, identity, measured_loss = pending.popleft()
            learner.feedback(identity, measured_loss, receipt)
        learner.tick(i + 1, t)
        if not math.isfinite(learner.center) or not -4 <= learner.center <= 4:
            raise RuntimeError('center bound')
        if i >= 3 * plan['observations_per_run'] // 4:
            last_quarter.append((probability(learner.center) - target) ** 2)
    weights = quantized_weights(learner.center)
    count = 0
    for j in range(plan['heldout_decisions_per_model']):
        budget.charge('choice')
        decision = choose([Request('L0', 0, 'A', 'A', 1., weights[0]), Request('L0', 0, 'B', 'B', 1., weights[1])],
                          locality='L0', now=1., seed=seed + plan['heldout_seed_offset'],
                          decision_id=f'evaluation:{case["id"]}:{j}', model_id=f'{arm}:{case["id"]}:{seed}')
        count += decision.winner_connection_id == 'A'
    n, fraction = plan['heldout_decisions_per_model'], weights[0] / 1000
    z = abs(count - n * fraction) / math.sqrt(n * fraction * (1 - fraction))
    if z > 6:
        raise RuntimeError('heldout frequency sanity check')
    expected = 0 if arm == 'no_learning' else 111
    if learner.opportunities != expected or learner.updates != expected or learner.skipped:
        raise RuntimeError('unequal accepted update budget')
    if len(learner.pending) != len(pending):
        raise RuntimeError('tag queue mismatch')
    return dict(arm=arm, case=case['id'], seed=seed, final_center=learner.center,
                final_probability=probability(learner.center), quantized_weights=weights,
                final_true_squared_error=(probability(learner.center) - case['target_after']) ** 2,
                last_quarter_true_squared_error=statistics.mean(last_quarter),
                heldout_A_count=count, heldout_z=z, opportunities=learner.opportunities,
                updates=learner.updates, skipped=learner.skipped, pending_feedback=len(pending),
                max_pending=max_pending, period=learner.period, max_gradient=learner.max_gradient,
                max_step=learner.max_step, update_audit=learner.audit)


def noise_for(plan, index, seed):
    rng = random.Random(7000 + index * 100 + seed)
    return [rng.gauss(0, plan['model']['noise_sd']) for _ in range(plan['observations_per_run'])]


def main():
    plan = load_plan()
    frozen = json.loads((OUT / 'source-manifest.json').read_bytes())
    for f in frozen['files']:
        if sha(OUT / f['path']) != f['sha256']:
            raise RuntimeError('frozen source mismatch: ' + f['path'])
    for f in json.loads((SOURCE / 'manifest.json').read_bytes())['files']:
        if sha(SOURCE / f['path']) != f['sha256']:
            raise RuntimeError('arbiter source drift')
    budget = Budget(plan)
    result = dict(schema='oscillatory-priority-results-v2', status='RUNNING', synthetic_only=True,
                  neural_execution=False, source_manifest_sha256=sha(OUT / 'source-manifest.json'),
                  plan_sha256=sha(OUT / 'plan.json'), arbiter_sha256=sha(SOURCE / 'arbiter.py'), rows=[])
    try:
        for index, case in enumerate(plan['cases']):
            for seed in plan['seeds']:
                noise = noise_for(plan, index, seed)
                for arm in plan['arms']:
                    result['rows'].append(fit(plan, arm, case, seed, noise, budget))
            print('Completed ' + case['id'], flush=True)
        overall = {a: statistics.mean(r['final_true_squared_error'] for r in result['rows'] if r['arm'] == a) for a in plan['arms']}
        by_case = {c['id']: {a: statistics.mean(r['final_true_squared_error'] for r in result['rows'] if r['case'] == c['id'] and r['arm'] == a) for a in plan['arms']} for c in plan['cases']}
        controls = ['paired_perturbation', 'fixed_oscillator']
        primary = plan['primary_arm']
        wins = sum(all(values[primary] < values[c] for c in controls) for values in by_case.values())
        result.update(status='COMPLETE', overall_mean_final_error=overall, case_mean_final_error=by_case,
                      primary_case_wins=wins, predeclared_improvement_criterion_met=wins >= 3 and all(overall[primary] < overall[c] for c in controls))
    except Exception as error:
        result.update(status='STOPPED', reason=str(error))
    result.update(plant_observations=budget.observations, heldout_choices=budget.choices,
                  elapsed_seconds=time.monotonic() - budget.started)
    data = (json.dumps(result, indent=None, allow_nan=False) + '\n').encode()
    if len(data) > plan['limits']['max_result_bytes']:
        raise RuntimeError('result byte cap')
    with (OUT / 'results.json').open('xb') as f:
        f.write(data)
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))
    return 0 if result['status'] == 'COMPLETE' else 1


if __name__ == '__main__':
    raise SystemExit(main())
