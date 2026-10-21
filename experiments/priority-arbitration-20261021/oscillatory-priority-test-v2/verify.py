"""Three exact training replays; preserves original results and charges cumulative budgets."""
import hashlib
import json
from pathlib import Path
from study import Budget, fit, load_plan, noise_for, sha

OUT = Path(__file__).resolve().parent


def main():
    plan = load_plan()
    result = json.loads((OUT / 'results.json').read_bytes())
    if result['status'] != 'COMPLETE':
        raise RuntimeError('original matrix incomplete')
    for entry in json.loads((OUT / 'source-manifest.json').read_bytes())['files']:
        if sha(OUT / entry['path']) != entry['sha256']:
            raise RuntimeError('source identity mismatch')
    budget = Budget(plan)
    budget.observations, budget.choices = result['plant_observations'], result['heldout_choices']
    checks = []
    for case_id in ('fast', 'delayed', 'target_shift'):
        index, case = next((i, c) for i, c in enumerate(plan['cases']) if c['id'] == case_id)
        actual = fit(plan, plan['primary_arm'], case, 0, noise_for(plan, index, 0), budget)
        expected = next(r for r in result['rows'] if r['case'] == case_id and r['arm'] == plan['primary_arm'] and r['seed'] == 0)
        # Serialization handles tuple/list differences without changing float values.
        canonical = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False)
        if canonical(actual) != canonical(expected):
            raise RuntimeError('exact training replay mismatch')
        checks.append(dict(case=case_id, arm=plan['primary_arm'], seed=0, exact=True,
                           row_sha256=hashlib.sha256(canonical(actual).encode()).hexdigest()))
    output = dict(status='PASS', checks=checks, cumulative_observations=budget.observations,
                  cumulative_choices=budget.choices, original_results_sha256=sha(OUT / 'results.json'))
    with (OUT / 'verification.json').open('x', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
