import itertools
import unittest
from unittest.mock import patch
from arbiter import (Request, choose, ArbitrationError, MAX_WEIGHT, MAX_REQUESTS,
                     MAX_DRAWS, _ticket)

def req(conn, weight, *, locality="L0", priority=0, timestamp=1.0, event=None):
    return Request(locality,priority,conn,event or "event-"+conn,timestamp,weight)

def select(requests, **kwargs):
    options=dict(locality="L0",now=1.,seed=17,decision_id="epoch0-slot0",model_id="example")
    options.update(kwargs)
    return choose(requests,**options)


class LotteryTests(unittest.TestCase):
    def test_equal_priority_normalizes_only_local_pool(self):
        result=select([req("A",3),req("B",1),req("C",99,priority=1),
                       req("D",MAX_WEIGHT,locality="L1")])
        self.assertEqual(result.probabilities,(("A",3,4),("B",1,4)))
        self.assertIn(result.winner_connection_id,("A","B"))

    def test_oldest_timestamp_precedes_priority(self):
        result=select([req("old",1,priority=5,timestamp=.5),
                       req("new",MAX_WEIGHT,priority=0)])
        self.assertEqual(result.winner_connection_id,"old")

    def test_all_input_orders_replay_exactly(self):
        requests=[req("A",3),req("B",1),req("outside",4,locality="L1")]
        original=select(requests)
        for order in itertools.permutations(requests):
            self.assertEqual(select(order),original)

    def test_outside_pool_changes_do_not_perturb_decision(self):
        base=[req("A",3),req("B",1)]
        self.assertEqual(select(base),select(base+[req("other",77,locality="L1")]))
        self.assertEqual(select(base),select(base+[req("low",77,priority=7)]))

    def test_zero_pool_uses_uniform_weights(self):
        decision=select([req("A",0),req("B",0)])
        self.assertTrue(decision.uniform_fallback)
        self.assertEqual(decision.probabilities,(("A",1,2),("B",1,2)))

    def test_zero_member_cannot_win_when_positive_weight_exists(self):
        for i in range(32):
            result=select([req("zero",0),req("positive",5)],decision_id=str(i))
            self.assertEqual(result.winner_connection_id,"positive")

    def test_no_ready_local_signal_returns_none(self):
        self.assertIsNone(select([req("future",1,timestamp=2.)]))
        self.assertIsNone(select([req("other",1,locality="L1")]))
        self.assertIsNone(select([]))

    def test_duplicate_heads_and_event_ids_are_rejected(self):
        with self.assertRaises(ArbitrationError):
            select([req("A",3),req("A",1,event="second")])
        with self.assertRaises(ArbitrationError):
            select([req("A",3,event="same"),req("B",1,event="same")])

    def test_requests_are_not_removed_or_modified(self):
        requests=[req("A",3),req("B",1)]
        before=tuple(requests)
        select(requests)
        self.assertEqual(tuple(requests),before)

    def test_weighted_distribution_fixed_seed_collection(self):
        # Finite, deterministic regression; no neural workloads or trained-benefit claim.
        count=0
        for i in range(4096):
            count+=select([req("A",3),req("B",1)],decision_id=f"draw-{i}").winner_connection_id=="A"
        self.assertGreater(count,4096*.70)
        self.assertLess(count,4096*.80)

    def test_sampler_rejects_modulo_bias_tail_and_stops_at_cap(self):
        class Tail:
            def digest(self): return b"\xff"*32
        with patch("arbiter.hmac.new",return_value=Tail()) as mocked:
            with self.assertRaises(ArbitrationError):_ticket(3,17,{"scope":"test"})
            self.assertEqual(mocked.call_count,MAX_DRAWS)

    def test_maximum_weight_sum_remains_exact(self):
        decision=select([req(str(i),MAX_WEIGHT) for i in range(MAX_REQUESTS)])
        self.assertEqual(decision.total_weight,MAX_REQUESTS*MAX_WEIGHT)
        self.assertTrue(0<=decision.ticket<decision.total_weight)

    def test_iterable_capacity_refuses_without_unbounded_materialization(self):
        def infinite():
            i=0
            while True:
                yield req(str(i),1);i+=1
        with self.assertRaises(ArbitrationError):select(infinite())

    def test_invalid_metadata_and_numbers_fail_explicitly(self):
        for value in (-1,True,1.5,MAX_WEIGHT+1):
            with self.subTest(weight=value),self.assertRaises(ArbitrationError):
                req("A",value)
        for t in (-1,float("inf"),float("nan"),True):
            with self.subTest(time=t),self.assertRaises(ArbitrationError):
                req("A",1,timestamp=t)
        with self.assertRaises(ArbitrationError):select([req("A",1)],seed=-1)
        with self.assertRaises(ArbitrationError):select([req("A",1)],decision_id="")
        with self.assertRaises(ArbitrationError):select([object()])

    def test_signed_zero_time_has_one_canonical_encoding(self):
        self.assertEqual(req("A",1,timestamp=-0.).timestamp.hex(),(0.).hex())


if __name__=="__main__":
    unittest.main()
