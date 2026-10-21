"""Experimental external optimizer; no neuron/runtime dependencies."""
from dataclasses import dataclass
import math
import random

def clip(x,lo,hi):
    return max(lo,min(hi,x))

def probability(score):
    return 1.0/(1.0+math.exp(-score))

def quantized_weights(score):
    a=max(1,min(999,round(1000*probability(score))))
    return (a,1000-a)

def slope(n,sx,sy,sxx,sxy):
    denominator=sxx-sx*sx/n if n else 0.
    return None if denominator<=1e-12 else (sxy-sx*sy/n)/denominator

@dataclass
class Cycle:
    identity:int
    start:float
    period:float
    center:float
    amplitude:float
    sign:int
    sent:int=0
    received:int=0
    closed:bool=False
    sx:float=0.
    sy:float=0.
    sxx:float=0.
    sxy:float=0.

class Learner:
    def __init__(self,arm,settings,case,seed,limits):
        self.arm,self.settings,self.case,self.limits=arm,settings,case,limits
        self.center=settings["initial_center"]
        self.error=settings["initial_error_estimate"]
        self.last_feedback_time=None
        self.rng=random.Random(seed)
        self.orientation=1 if seed%2==0 else -1
        self.cycles={};self.next_identity=0;self.current=None
        self.updates=0;self.skipped=0;self.reversals=0
        self.max_gradient=0.;self.max_step=0.
        self._new_cycle(0.)

    def _new_cycle(self,start):
        s=self.settings
        amplitude=s["fixed_amplitude"]
        if self.arm in ("error_amplitude","error_time_oscillator"):
            amplitude=s["min_amplitude"]+(s["max_amplitude"]-s["min_amplitude"])*self.error/(self.error+s["error_scale"])
        if self.arm=="no_learning":amplitude=0.
        effective_tau=max(self.case["state_tau"],self.case["feedback_delay"],s["error_ema_tau"])
        period=s["period_multiplier"]*effective_tau if self.arm in ("time_scaled_frequency","error_time_oscillator") else s["fixed_period"]
        if self.arm=="paired_perturbation":period=s["paired_period"]
        if len(self.cycles)>=self.limits["max_live_cycles"]:raise RuntimeError("live cycle cap")
        sign=self.rng.choice((-1,1)) if self.arm=="paired_perturbation" else self.orientation
        c=Cycle(self.next_identity,start,period,self.center,amplitude,sign)
        self.cycles[c.identity]=c;self.current=c;self.next_identity+=1
        return c

    def probe(self,t):
        while t>=self.current.start+self.current.period:
            old=self.current
            old.closed=True;boundary=old.start+old.period
            self._complete(old)
            self._new_cycle(boundary)
        c=self.current
        phase=(t-c.start)/c.period
        carrier=(-1. if phase<.5 else 1.) if self.arm=="paired_perturbation" else (-1.+4.*phase if phase<.5 else 3.-4.*phase)
        trial=clip(c.center+c.sign*c.amplitude*carrier,*self.settings["center_bounds"])
        delta=trial-c.center
        c.sent+=1
        return trial,c.identity,delta

    def feedback(self,identity,delta,loss,t):
        if not math.isfinite(loss):raise RuntimeError("nonfinite loss")
        c=self.cycles.get(identity)
        if c is None or c.received>=c.sent:raise RuntimeError("unmatched or duplicate feedback")
        dt=0. if self.last_feedback_time is None else t-self.last_feedback_time
        if dt<0:raise RuntimeError("feedback time reversed")
        if self.last_feedback_time is None:alpha=1.
        else:alpha=1.-math.exp(-dt/self.settings["error_ema_tau"])
        self.error=(1.-alpha)*self.error+alpha*max(0.,loss)
        self.last_feedback_time=t
        c.received+=1;c.sx+=delta;c.sy+=loss;c.sxx+=delta*delta;c.sxy+=delta*loss
        self._complete(c)

    def _complete(self,c):
        if not c.closed or c.received!=c.sent:return
        g=slope(c.received,c.sx,c.sy,c.sxx,c.sxy)
        if self.arm!="no_learning" and g is not None:
            g=clip(g,-self.settings["max_abs_gradient"],self.settings["max_abs_gradient"])
            step=clip(-self.settings["learning_rate"]*g,-self.settings["max_center_step"],self.settings["max_center_step"])
            self.center=clip(self.center+step,*self.settings["center_bounds"])
            self.max_gradient=max(self.max_gradient,abs(g));self.max_step=max(self.max_step,abs(step))
            self.updates+=1
        else:self.skipped+=1
        self.reversals+=2
        del self.cycles[c.identity]

    def finish(self,t):
        self.current.closed=True
        self._complete(self.current)
