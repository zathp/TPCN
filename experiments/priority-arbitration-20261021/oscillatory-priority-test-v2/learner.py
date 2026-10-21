"""Fixed-cadence external learner; tagged rolling, biased surrogate gradient."""
from collections import deque
from dataclasses import dataclass
import math
import random


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def probability(score):
    return 1 / (1 + math.exp(-score))


def quantized_weights(score):
    a = clip(round(1000 * probability(score)), 1, 999)
    return a, 1000 - a


def regression(samples):
    if len(samples) < 2:
        return None, 0.
    xs = [s.trial for s in samples]
    ys = [s.loss for s in samples]
    xm, ym = sum(xs) / len(xs), sum(ys) / len(ys)
    variance = sum((x - xm) ** 2 for x in xs)
    if variance <= 1e-12:
        return None, variance
    return sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / variance, variance


@dataclass(frozen=True)
class Probe:
    identity: int
    origin: float
    trial: float
    center: float


@dataclass(frozen=True)
class Sample:
    identity: int
    origin: float
    receipt: float
    trial: float
    center: float
    loss: float


class Learner:
    def __init__(self, arm, settings, case, seed, limits):
        self.arm, self.s, self.case, self.limits = arm, settings, case, limits
        self.center = settings['initial_center']
        self.error = settings['initial_error_estimate']
        self.orientation = 1 if seed % 2 == 0 else -1
        self.rng = random.Random(seed)
        self.paired_cycle, self.paired_sign = -1, 1
        self.period = settings['fixed_period']
        if arm.startswith('error_time_'):
            multiplier = int(arm.rsplit('_', 1)[1])
            self.period = multiplier * max(case['state_tau'], case['feedback_delay'], settings['error_ema_tau'])
        elif arm == 'paired_perturbation':
            self.period = settings['paired_period']
        self.pending = {}
        self.samples = deque(maxlen=settings['window_samples'])
        self.next_identity = 0
        self.last_probe_time = self.last_feedback_time = None
        self.last_step = 0
        self.updates = self.opportunities = self.skipped = 0
        self.max_gradient = self.max_step = 0.
        self.audit = []

    def amplitude(self):
        if self.arm == 'no_learning':
            return 0.
        if self.arm.startswith('error_time_'):
            return self.s['min_amplitude'] + (self.s['max_amplitude'] - self.s['min_amplitude']) * self.error / (self.error + self.s['error_scale'])
        return self.s['fixed_amplitude']

    def probe(self, t):
        if not math.isfinite(t) or t < 0 or (self.last_probe_time is not None and t <= self.last_probe_time):
            raise ValueError('probe time must strictly increase')
        if len(self.pending) >= self.limits['max_pending_feedback']:
            raise RuntimeError('pending cap')
        self.last_probe_time = t
        phase = (t % self.period) / self.period
        if self.arm == 'paired_perturbation':
            cycle = int(t // self.period)
            while self.paired_cycle < cycle:
                self.paired_sign = self.rng.choice((-1, 1))
                self.paired_cycle += 1
            carrier = self.paired_sign * (-1 if phase < .5 else 1)
        else:
            carrier = self.orientation * (-1 + 4 * phase if phase < .5 else 3 - 4 * phase)
        trial = clip(self.center + self.amplitude() * carrier, *self.s['center_bounds'])
        p = Probe(self.next_identity, t, trial, self.center)
        self.next_identity += 1
        self.pending[p.identity] = p
        return p

    def feedback(self, identity, loss, t):
        if not math.isfinite(loss) or not math.isfinite(t):
            raise ValueError('nonfinite feedback')
        p = self.pending.get(identity)
        if p is None or t < p.origin or (self.last_feedback_time is not None and t < self.last_feedback_time):
            raise ValueError('unmatched, duplicate, or reversed feedback')
        if identity != min(self.pending):
            raise ValueError('feedback must follow origin ID order')
        alpha = 1. if self.last_feedback_time is None else -math.expm1(-(t - self.last_feedback_time) / self.s['error_ema_tau'])
        self.error += alpha * (max(0., loss) - self.error)
        self.last_feedback_time = t
        del self.pending[identity]
        self.samples.append(Sample(identity, p.origin, t, p.trial, p.center, loss))

    def tick(self, step, t):
        if step != self.last_step + 1:
            raise ValueError('ticks must be consecutive')
        self.last_step = step
        if self.arm == 'no_learning' or step < self.s['first_update_step'] or step % self.s['update_stride']:
            return
        self.opportunities += 1
        g, variance = regression(self.samples)
        if g is None:
            self.skipped += 1
        else:
            g = clip(g, -self.s['max_abs_gradient'], self.s['max_abs_gradient'])
            delta = clip(-self.s['learning_rate'] * g, -self.s['max_center_step'], self.s['max_center_step'])
            self.center = clip(self.center + delta, *self.s['center_bounds'])
            self.max_gradient = max(self.max_gradient, abs(g))
            self.max_step = max(self.max_step, abs(delta))
            self.updates += 1
        if len(self.audit) >= self.limits['max_update_records']:
            raise RuntimeError('update audit cap')
        # Every update has a compact, auditable receipt window.
        self.audit.append([step, t, len(self.samples), self.samples[0].identity if self.samples else None,
                           self.samples[-1].identity if self.samples else None, variance, g, self.center])
