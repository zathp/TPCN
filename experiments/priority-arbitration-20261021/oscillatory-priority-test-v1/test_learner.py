import copy,json,math,unittest
from pathlib import Path
from learner import Learner,probability,quantized_weights,slope
P=json.loads(Path(__file__).with_name("plan.json").read_bytes())
def make(arm="error_time_oscillator",case=None):
 return Learner(arm,P["learner"],case or P["cases"][0],0,P["limits"])
class Tests(unittest.TestCase):
 def test_symmetric_quadratic_probe_slope_has_right_direction(self):
  xs=[-.4,.4];ys=[(x-1.)**2 for x in xs]
  self.assertAlmostEqual(slope(2,sum(xs),sum(ys),sum(x*x for x in xs),sum(x*y for x,y in zip(xs,ys))),-2.)
 def test_zero_variance_does_not_invent_gradient(self):
  self.assertIsNone(slope(2,0.,2.,0.,0.))
 def test_high_error_increases_bounded_exploration(self):
  low=make();low.error=0.;a=low._new_cycle(32.).amplitude
  high=make();high.error=1e6;b=high._new_cycle(32.).amplitude
  self.assertGreater(b,a);self.assertGreaterEqual(a,.1);self.assertLessEqual(b,.8)
 def test_frequency_tracks_slowest_declared_dynamics(self):
  fast=make();slow=make(case=P["cases"][1]);delayed=make(case=P["cases"][2])
  self.assertEqual((fast.current.period,slow.current.period,delayed.current.period),(32.,64.,128.))
 def test_fixed_frequency_is_a_control(self):
  self.assertEqual(make("fixed_oscillator",P["cases"][2]).current.period,32.)
 def test_triangle_drifts_and_reverses_without_center_update(self):
  m=make("fixed_oscillator");period=m.current.period
  values=[m.probe(t)[0] for t in [0.,period/4,period/2,3*period/4]]
  self.assertLess(values[0],values[1]);self.assertLess(values[1],values[2]);self.assertGreater(values[2],values[3])
  self.assertEqual(m.center,0.)
 def test_feedback_waits_for_closed_complete_cycle(self):
  m=make("fixed_oscillator")
  _,identity,d0=m.probe(0.);_,_,d1=m.probe(16.)
  m.feedback(identity,d0,(d0-1.)**2,1.)
  m.probe(32.)
  self.assertEqual(m.updates,0)
  m.feedback(identity,d1,(d1-1.)**2,33.)
  self.assertEqual(m.updates,1);self.assertGreater(m.center,0.)
  self.assertLessEqual(m.max_step,.2)
 def test_feedback_rejects_duplicate_finalized_cycle(self):
  m=make();_,i,d=m.probe(0.);m.feedback(i,d,1.,1.)
  with self.assertRaises(RuntimeError):m.feedback(i,d,1.,2.)
 def test_quantized_weights_are_positive_and_exact(self):
  for x in [-4.,0.,4.]:
   a,b=quantized_weights(x)
   self.assertEqual(a+b,1000);self.assertGreater(a,0);self.assertGreater(b,0)
 def test_no_learning_center_stays_fixed(self):
  m=make("no_learning")
  for t in range(100):
   trial,i,d=m.probe(float(t));m.feedback(i,d,.1,float(t))
  m.finish(100.)
  self.assertEqual(m.center,0.);self.assertEqual(m.updates,0)
 def test_irregular_event_times_advance_phase_analytically(self):
  m=make("fixed_oscillator")
  for t in [.1,.6,1.85]:
   value,_,_=m.probe(t)
   self.assertAlmostEqual(value,.4*(-1+4*t/32.))
if __name__=="__main__":unittest.main()
