"""Independent read-only evidence arithmetic; does not train or sample choices."""
from pathlib import Path
import hashlib
import csv
import itertools
import json
import math
import statistics

root = Path(__file__).resolve().parent
read = lambda name: json.loads((root / name).read_bytes())
digest = lambda name: hashlib.sha256((root / name).read_bytes()).hexdigest()
plan, result, verification = read('plan.json'), read('results.json'), read('verification.json')
assert result['status'] == 'COMPLETE'
assert digest('source-manifest.json') == '6cf75309fa99c3928c1e5dd2815a40060d02909994e0b955548be394c329b1eb'
for item in read('source-manifest.json')['files']:
    assert digest(item['path']) == item['sha256']
    assert (root / item['path']).stat().st_size == item['bytes']
assert result['source_manifest_sha256'] == digest('source-manifest.json')
assert result['plan_sha256'] == digest('plan.json')
assert result['arbiter_sha256'] == '3e9d66a258da0d76f08fb73a966a9c6d7da3af5ab538ea562ac9e534cf161534'
rows = result['rows']
keys = [(r['case'], r['seed'], r['arm']) for r in rows]
assert len(keys) == len(set(keys)) == 192
assert set(keys) == set(itertools.product([c['id'] for c in plan['cases']], plan['seeds'], plan['arms']))
times, t = [], 0.
for i in range(2048):
    t += plan['observation_intervals'][i % 5]
    times.append(t)
audit_count = 0
for row in rows:
    case = next(c for c in plan['cases'] if c['id'] == row['case'])
    probability = 1 / (1 + math.exp(-row['final_center']))
    assert row['final_probability'] == probability
    assert row['final_true_squared_error'] == (probability-case['target_after']) ** 2
    expected_weights = [max(1, min(999, round(1000 * probability))), 0]
    expected_weights[1] = 1000-expected_weights[0]
    assert row['quantized_weights'] == expected_weights
    fraction = expected_weights[0]/1000
    z = abs(row['heldout_A_count']-256*fraction)/math.sqrt(256*fraction*(1-fraction))
    assert z == row['heldout_z'] and z <= 6
    expected_pending = sum(completion+case['feedback_delay'] > times[-1] for completion in times)
    assert row['pending_feedback'] == expected_pending
    assert 0 <= row['max_pending'] <= 128
    audit = row['update_audit']
    expected = 0 if row['arm'] == 'no_learning' else 111
    assert row['opportunities'] == row['updates'] == len(audit) == expected
    assert row['skipped'] == 0
    assert row['max_gradient'] <= 2 and row['max_step'] <= .2
    previous_center = 0.
    for record, step in zip(audit, range(288, 2049, 16)):
        s, timestamp, count, first, last, variance, gradient, center = record
        expected_last = max(j for j in range(step) if times[j]+case['feedback_delay'] <= times[step-1])
        assert s == step and timestamp == times[step-1]
        assert count == 256 and first == expected_last-255 and last == expected_last
        assert math.isfinite(variance) and variance > 1e-12
        assert math.isfinite(gradient) and abs(gradient) <= 2
        delta = max(-.2, min(.2, -.7*gradient))
        expected_center = max(-4, min(4, previous_center+delta))
        assert center == expected_center
        previous_center = center
        audit_count += 1
    if audit:
        assert row['final_center'] == audit[-1][-1]
means = {a: statistics.mean(r['final_true_squared_error'] for r in rows if r['arm']==a) for a in plan['arms']}
by_case = {c['id']: {a: statistics.mean(r['final_true_squared_error'] for r in rows if r['case']==c['id'] and r['arm']==a) for a in plan['arms']} for c in plan['cases']}
assert means == result['overall_mean_final_error']
assert by_case == result['case_mean_final_error']
csvrows = list(csv.DictReader((root/'summary.csv').open(newline='', encoding='utf-8')))
assert len(csvrows) == 24
for entry in csvrows:
    matched = [r for r in rows if r['case']==entry['case'] and r['arm']==entry['arm']]
    errors = [r['final_true_squared_error'] for r in matched]
    assert int(entry['n']) == len(matched) == 8
    assert float(entry['mean_final_error']) == statistics.mean(errors)
    assert float(entry['sample_sd']) == statistics.stdev(errors)
    assert float(entry['mean_last_quarter_error']) == statistics.mean(r['last_quarter_true_squared_error'] for r in matched)
    assert int(entry['accepted_updates']) == matched[0]['updates']
report = (root/'REPORT.md').read_text(encoding='utf-8')
assert all(f'{v:.9f}' in report for v in means.values())
primary, controls = plan['primary_arm'], ['paired_perturbation', 'fixed_oscillator']
wins = sum(all(v[primary] < v[c] for c in controls) for v in by_case.values())
assert wins == result['primary_case_wins'] == 3
assert result['predeclared_improvement_criterion_met'] is False
assert not all(means[primary] < means[c] for c in controls)
assert result['plant_observations'] == 192*2048 == 393216
assert result['heldout_choices'] == 192*256 == 49152
assert verification['status'] == 'PASS' and verification['original_results_sha256'] == digest('results.json')
assert verification['cumulative_observations'] == 399360 <= plan['limits']['max_plant_observations']
assert verification['cumulative_choices'] == 49920 <= plan['limits']['max_heldout_choices']
for check in verification['checks']:
    row = next(r for r in rows if r['case']==check['case'] and r['arm']==primary and r['seed']==0)
    serialized = json.dumps(row, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    assert check['exact'] is True and check['row_sha256'] == hashlib.sha256(serialized).hexdigest()
assert {c['case'] for c in verification['checks']} == {'fast', 'delayed', 'target_shift'}
timing = read('verification-timing.json')
assert timing['exit_code'] == 0
elapsed = result['elapsed_seconds'] + timing['replay_command_seconds']
assert elapsed < 60
assert (root/'results.json').stat().st_size <= plan['limits']['max_result_bytes']
print(json.dumps(dict(status='PASS', reviewer='/root/luna0_update_matched_review',
    matrix_rows=len(rows), independently_checked_update_records=audit_count,
    primary_case_wins=wins, primary_improvement=False,
    result_sha256=digest('results.json'), observed_combined_seconds=elapsed,
    new_training_runs=0, new_arbiter_choices=0), indent=2))
