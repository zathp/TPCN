import copy
import json
import math
from pathlib import Path
import unittest
from learner import Learner, Sample, probability, quantized_weights, regression

PLAN = json.loads(Path(__file__).with_name('plan.json').read_text(encoding='utf-8-sig'))


def make(arm='error_time_8', case=None):
    return Learner(arm, PLAN['learner'], case or PLAN['cases'][0], 0, PLAN['limits'])


class Tests(unittest.TestCase):
    def test_regression_uses_absolute_trial_when_centers_differ(self):
        samples = [Sample(i, i, i, x, x - .1, 3 * x + 2) for i, x in enumerate([-1., 0., 1.])]
        self.assertAlmostEqual(regression(samples)[0], 3.)

    def test_zero_variance_returns_no_gradient(self):
        self.assertIsNone(regression([Sample(i, i, i, 1., 0., i) for i in range(3)])[0])

    def test_stored_trial_survives_center_change(self):
        m = make(); p = m.probe(0.); m.center = 2.
        m.feedback(p.identity, .1, 1.)
        self.assertEqual(m.samples[0].trial, p.trial)
        self.assertEqual(m.samples[0].center, 0.)

    def test_reject_duplicate_identity(self):
        m = make(); p = m.probe(0.); m.feedback(p.identity, .1, 1.)
        with self.assertRaises(ValueError): m.feedback(p.identity, .1, 2.)

    def test_reject_receipt_before_origin(self):
        m = make(); p = m.probe(2.)
        with self.assertRaises(ValueError): m.feedback(p.identity, .1, 1.)

    def test_reject_invalid_probe_time(self):
        for t in [-1., math.inf, math.nan]:
            with self.assertRaises(ValueError): make().probe(t)
        m = make(); m.probe(1.)
        with self.assertRaises(ValueError): m.probe(.5)

    def test_reject_feedback_order_and_nonfinite(self):
        m = make(); p = m.probe(0.); q = m.probe(1.)
        with self.assertRaises(ValueError): m.feedback(q.identity, .1, 2.)
        with self.assertRaises(ValueError): m.feedback(p.identity, math.nan, 2.)
        m.feedback(p.identity, .1, 2.)
        with self.assertRaises(ValueError): m.feedback(q.identity, .1, 1.5)

    def test_pending_cap(self):
        m = make()
        for i in range(128): m.probe(float(i))
        with self.assertRaises(RuntimeError): m.probe(128.)

    def test_receipt_window_is_bounded_and_latest(self):
        m = make()
        for i in range(300):
            p = m.probe(float(i)); m.feedback(p.identity, .1, i + .5)
        self.assertEqual(len(m.samples), 256)
        self.assertEqual((m.samples[0].identity, m.samples[-1].identity), (44, 299))

    def test_phase_tracks_physical_time_and_reverses(self):
        m = make('fixed_oscillator')
        values = [m.probe(t).trial for t in (0., 8., 16., 24.)]
        self.assertEqual(values, [-.4, 0., .4, 0.])

    def test_period_sweep_and_slowest_dynamic(self):
        self.assertEqual([make('error_time_' + str(k), PLAN['cases'][2]).period for k in (4, 8, 16)], [64, 128, 256])

    def test_error_only_uses_received_feedback(self):
        m = make(); original = m.amplitude(); p = m.probe(0.)
        self.assertEqual(m.amplitude(), original)
        m.feedback(p.identity, 100., 1.)
        self.assertGreater(m.amplitude(), original)
        self.assertLessEqual(m.amplitude(), .8)

    def test_update_schedule_equal_across_learning_arms(self):
        for arm in PLAN['arms']:
            m = make(arm)
            for i in range(2048):
                p = m.probe(float(i)); m.feedback(p.identity, (p.trial - 1.) ** 2, i + .5)
                m.tick(i + 1, i + .5)
            expected = 0 if arm == 'no_learning' else 111
            self.assertEqual(m.updates, expected)
            self.assertEqual(m.opportunities, expected)
            self.assertLessEqual(m.max_step, .2)
            self.assertTrue(-4 <= m.center <= 4)
            if expected: self.assertEqual([r[0] for r in m.audit], list(range(288, 2049, 16)))

    def test_no_update_before_first_tick_and_consecutive_ticks(self):
        m = make()
        for i in range(287): m.tick(i + 1, float(i))
        self.assertEqual(m.updates, 0)
        with self.assertRaises(ValueError): m.tick(289, 290.)

    def test_quantization_positive_exact(self):
        for score in (-4., 0., 4.):
            a, b = quantized_weights(score)
            self.assertEqual(a + b, 1000)
            self.assertGreater(min(a, b), 0)


if __name__ == '__main__':
    unittest.main()
