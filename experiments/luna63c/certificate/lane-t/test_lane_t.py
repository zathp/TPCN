import json
import struct
import unittest
from fractions import Fraction as F

import convert as c


class LaneT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inv, cls.sch = c.generate()
        cls.rows = {r["event_id"]: r for r in cls.sch["rows"]}
        cls.wm, _ = c.load_w()

    def test_pins_and_files(self):
        c.verify_pins()
        self.assertEqual(c.sha(c.WMAT.read_bytes().replace(b"\r\n", b"\n")), c.PINS["w_matrix_sha256"])

    def test_counts(self):
        k = self.sch["counts"]
        self.assertEqual((k["events"], k["certified"], k["blocked"], k["observation_rows"]), (191, 9, 182, 15))
        self.assertEqual((k["c7_identities"], k["c7_certified"], k["c7_blocked"]), (119, 9, 110))
        self.assertEqual(self.sch["verdict"], "T BLOCKED \u2014 N3 NOT CLOSED")

    def test_unique_ids_and_exactly_one_status(self):
        ids = [r["event_id"] for r in self.sch["rows"]]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.sch["rows"]:
            self.assertIn(r["status"], ("CERTIFIED", "BLOCKED"))
            if r["status"] == "BLOCKED":
                self.assertTrue(r["blocked_reasons"])
                self.assertIsNone(r["final_ordinal"])
                self.assertIsNone(r["exact_time"])
            else:
                self.assertIsNotNone(r["final_ordinal"])

    def test_c7_per_case_counts(self):
        exp = {"DUPLICATE_RECALL": 5, "ALTERNATING_RECALL": 16, "RESET_BEFORE_COMMIT": 7, "RESET_AFTER_COMMIT": 11, "STALE_TIMER": 7,
               "REARM_BEFORE_QUIET": 12, "EXPIRY_COALESCENCE_VALID": 4, "EXPIRY_COALESCENCE_INVALID": 4, "TIMESTAMP_INVALID": 12,
               "OVERFLOW_17": 25, "POST_ABORT_INGRESS": 1, "OUTPUT_EXPIRY_COALESCENCE": 6, "NEAR_CLOCK_LIMIT": 3, "POSITIVE_SUB_ULP": 6}
        got = {}
        for r in self.sch["rows"]:
            if r["fixture"] == "C7":
                got[r["case"][3:]] = got.get(r["case"][3:], 0) + 1
        self.assertEqual(got, exp)
        self.assertEqual(sum(got.values()), 119)

    def test_w_refs_exist(self):
        _, w = c.load_w()
        for r in self.sch["rows"]:
            for ref in r["w_evidence"]:
                self.assertIn(ref, w)
                self.assertEqual(w[ref]["status"] if "status" in w[ref] else "CERTIFIED", "CERTIFIED")

    def test_grid_functions(self):
        self.assertEqual(c.ceil64(F(1) + F(1, 2 ** 60)), F(1) + F(1, 2 ** 52))
        self.assertEqual(c.floor64(F(1) + F(1, 2 ** 60)), F(1))
        self.assertEqual(c.ceil64(F(3, 2)), F(3, 2))
        self.assertEqual(c.ulp_exp(F(2) ** 19), -33)
        self.assertEqual(c.ulp_exp(F(2) ** 20 - F(1, 2 ** 33)), -33)

    def test_near_clock(self):
        nc = c.derive_near_clock(self.wm["evidence"])
        lo, hi = nc["T_life"]
        t, u = nc["t_star"], nc["ulp"]
        self.assertEqual(u, F(1, 2 ** 33))
        self.assertTrue(t + hi <= c.T_CLOCK < t + u + lo)
        self.assertEqual(nc["expiry1_ceiling"], c.T_CLOCK)
        self.assertEqual(self.rows["C7.NEAR_CLOCK_LIMIT.STORE_LAST_IN_DOMAIN_ORIGIN_1"]["binary64"]["hex"], "0x1.ffff4f6a5d2e4p+19")
        self.assertEqual(self.rows["C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1"]["binary64"]["hex"], "0x1.ffff4f6a5d2e5p+19")
        self.assertEqual(self.rows["C7.NEAR_CLOCK_LIMIT.TIMER_EXPIRY_CREATED_FOR_INSTANCE_1"]["due_binary64"]["hex"], float(2 ** 20).hex())

    def test_sub_ulp(self):
        nc = c.derive_near_clock(self.wm["evidence"])
        su = c.derive_sub_ulp(self.wm["evidence"], nc)
        self.assertTrue(0 < su["s_q"][0] and su["s_q"][1] < nc["ulp"] / 2 ** 20)
        self.assertEqual(su["ceiling"], nc["t_star"] + nc["ulp"])
        self.assertEqual(su["predecessor"], nc["t_star"])
        self.assertEqual(su["active_units"].denominator, 1)
        r = self.rows["C7.POSITIVE_SUB_ULP.TIMER_QUIET_1"]
        self.assertGreater(r["final_ordinal"], self.rows["C7.POSITIVE_SUB_ULP.TIMER_QUIET_CREATED_1"]["final_ordinal"])
        self.assertTrue(r["ceiling_proof"]["predecessor_is_cause_time"])
        self.assertEqual(r["ceiling_proof"]["exact_release_interval_units_2pow1041"], str(2 ** 1041))
        self.assertEqual(self.rows["C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_CREATED_1"]["due_binary64"]["hex"], float(2 ** 20).hex())

    def test_blocked_scope(self):
        for k in ("C7.OUTPUT_EXPIRY_COALESCENCE.TIMER_EXPIRY_1", "C7.EXPIRY_COALESCENCE_VALID.VALID_EXTERNAL_RECALL_1",
                  "C3.EXPIRY_TIE.RECALL", "C7.TIMESTAMP_INVALID.LATE.STORE_LATE", "C7.OVERFLOW_17.ATTEMPT",
                  "C7.POST_ABORT_INGRESS.CLOSED_EPISODE_INGRESS", "C4.STORE", "C6.ROOT_UP", "C1.RECALL_ON"):
            self.assertEqual(self.rows[k]["status"], "BLOCKED", k)

    def test_precedence_text_and_predecessors(self):
        r = self.rows["C7.REARM_BEFORE_QUIET.TIMER_QUIET_CREATED_1"]
        self.assertEqual(r["causal_predecessors"], ["C7.REARM_BEFORE_QUIET.TIMER_REARM_1"])
        self.assertIn("rearm strictly precedes quiet", " ".join(self.rows["C7.REARM_BEFORE_QUIET.TIMER_REARM_1"]["precedence_dependencies"]))

    def test_deterministic_and_committed(self):
        a, b = c.generate(), c.generate()
        self.assertEqual(c.canon(a[1]), c.canon(b[1]))
        c.check()


if __name__ == "__main__":
    unittest.main()
