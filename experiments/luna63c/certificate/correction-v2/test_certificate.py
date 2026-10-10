"""Certificate arithmetic tests only; no runtime or scientific fixtures."""

from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import unittest

import calculate as c


class CertificateTests(unittest.TestCase):
    def test_outward_rational_and_products(self):
        for a in range(-4, 5):
            for b in range(1, 6):
                x = c.I.rational(a, b)
                self.assertLessEqual(F(x.lo, c.S), F(a, b))
                self.assertGreaterEqual(F(x.hi, c.S), F(a, b))
                for k in (-3, 0, 2):
                    y = x * c.I.rational(k, 7)
                    self.assertLessEqual(F(y.lo, c.S), F(a * k, b * 7))
                    self.assertGreaterEqual(F(y.hi, c.S), F(a * k, b * 7))

    def test_reciprocal_enclosure(self):
        x = c.I.rational(3, 7)
        y = x.reciprocal()
        self.assertLessEqual(F(y.lo, c.S), F(7, 3))
        self.assertGreaterEqual(F(y.hi, c.S), F(7, 3))

    def test_exact_zero_function_values_enclosed(self):
        e = c.exp_negative(c.I(0))
        s, co = c.trig(c.I(0)), c.trig(c.I(0), True)
        self.assertLessEqual(e.lo, c.S)
        self.assertGreaterEqual(e.hi, c.S)
        self.assertLessEqual(s.lo, 0)
        self.assertGreaterEqual(s.hi, 0)
        self.assertLessEqual(co.lo, c.S)
        self.assertGreaterEqual(co.hi, c.S)

    def test_positive_delay_below_one_ULP(self):
        # Arithmetic conversion lemma, NOT an executed C7 packet or timer.
        interval = c.I(c.S + (c.S >> 54))
        self.assertEqual(c.common_ceiling(interval)[1], "0x1.0000000000001p+0")
        self.assertEqual(c.binary64_ceiling(c.S)[1], "0x1.0000000000000p+0")

    def test_work_and_failure_caps(self):
        self.assertEqual(c.BITS, 256)
        with self.assertRaises(AssertionError):
            c.exp_negative(c.I.rational(7))
        # No common ceiling when a witness straddles a representable value.
        with self.assertRaises(AssertionError):
            c.common_ceiling(c.I(c.S - 1, c.S + 1))

    def test_remainders_are_below_fixed_quantum(self):
        from math import factorial
        exp_tail = F(6 ** 193, factorial(193)) / (1 - F(6, 194))
        sin_tail = F(6 ** 192, factorial(192))
        cos_tail = F(6 ** 191, factorial(191))
        for tail in (exp_tail, sin_tail, cos_tail, F(1, 257 * 5 ** 257),
                     F(2, 257 * 3 ** 257) / (1 - F(1, 9))):
            self.assertLess(tail, F(1, c.S))

    def test_conditional_binary64_A1_error_bound(self):
        # Conditional proof only: exact s, RN basic product, independently
        # correctly-rounded exp/sin/cos, no underflow, no state recurrence.
        u = F(1, 1 << 53)
        gamma3 = 3 * u / (1 - 3 * u)
        witness = json.loads((Path(__file__).parent / "witnesses.json").read_text())
        theta_lo = F(int(witness["constants"]["theta"]["lo_numerator"]), c.S)
        # Each coordinate error <= gamma3; squared norm <= 2*gamma3**2.
        self.assertLess(2 * gamma3 ** 2, theta_lo ** 2 / 16)
        self.assertGreater(theta_lo, F(1, 2))

    def test_sqrt2_integer_witness(self):
        lo = isqrt(2 * c.S * c.S)
        self.assertLess(lo * lo, 2 * c.S * c.S)
        self.assertGreater((lo + 1) * (lo + 1), 2 * c.S * c.S)

    def test_serialized_root_and_time_certificates(self):
        w = json.loads((Path(__file__).parent / "witnesses.json").read_text())
        self.assertEqual(w["bisections_per_root"], 128)
        self.assertEqual(w["q_neighbors"]["below_hex"], "0x1.4a226c87ef13fp-2")
        self.assertEqual(w["q_neighbors"]["above_hex"], "0x1.4a226c87ef140p-2")
        up = w["roots_A4"]["up_derivative"]
        rearm = w["roots_A4"]["rearm_derivative"]
        self.assertGreater(int(up["lo_numerator"]), 0)
        self.assertLess(int(rearm["hi_numerator"]), 0)
        self.assertIn("BLOCKED", w["disposition"])
        self.assertIn("Stage B", w["N6"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
