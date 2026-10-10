"""Independent certificate calculation only: no candidate or event lifecycle."""

import hashlib
import json
from fractions import Fraction as F
from math import factorial, isqrt
from pathlib import Path
import struct

BITS = 256
S = 1 << BITS


def ceildiv(a, b):
    return -((-a) // b)


class I:
    """Endpoints are integers divided by 2**256; every operation rounds out."""

    def __init__(self, lo, hi=None):
        self.lo = lo
        self.hi = lo if hi is None else hi
        assert self.lo <= self.hi

    @staticmethod
    def rational(a, b=1):
        assert b > 0
        return I((a * S) // b, ceildiv(a * S, b))

    def __add__(self, other):
        return I(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        products = [a * b for a in (self.lo, self.hi)
                    for b in (other.lo, other.hi)]
        return I(min(products) // S, ceildiv(max(products), S))

    def divint(self, n):
        assert n > 0
        return I(self.lo // n, ceildiv(self.hi, n))

    def reciprocal(self):
        assert self.lo > 0
        return I((S * S) // self.hi, ceildiv(S * S, self.lo))

    def radius(self, a, b):
        r = ceildiv(a * S, b)
        return I(self.lo - r, self.hi + r)

    def pack(self):
        return {"lo_numerator": str(self.lo), "hi_numerator": str(self.hi),
                "denominator_power_of_two": BITS}


ONE = I.rational(1)


def atan_inverse(n):
    # Alternating arctan series, 128 terms; exact rational remainder <= next.
    total = sum((F((-1) ** k, (2 * k + 1) * n ** (2 * k + 1))
                 for k in range(128)), F(0))
    next_term = F(1, 257 * n ** 257)
    return I.rational(total.numerator, total.denominator).radius(
        next_term.numerator, next_term.denominator)


def ln2():
    # log(2)=2*atanh(1/3). Positive tail <=
    # 2*z**(2N+1)/((2N+1)*(1-z*z)), N=128.
    total = sum((F(2, (2 * k + 1) * 3 ** (2 * k + 1))
                 for k in range(128)), F(0))
    tail = F(2, 257 * 3 ** 257) / (1 - F(1, 9))
    base = I.rational(total.numerator, total.denominator)
    return I(base.lo, base.hi + ceildiv(tail.numerator * S, tail.denominator))


def exp_negative(x):
    assert 0 <= x.lo <= x.hi <= 6 * S
    term = ONE
    total = ONE
    for k in range(1, 193):
        term = (term * x).divint(k)
        total = total + term
    # Positive exp Taylor tail: next term upper with geometric ratio <=6/194.
    tail = F(6 ** 193, factorial(193)) / (1 - F(6, 194))
    enclosed = I(total.lo, total.hi +
                 ceildiv(tail.numerator * S, tail.denominator))
    return enclosed.reciprocal()


def trig(x, cosine=False):
    assert 0 <= x.lo <= x.hi <= 6 * S
    term = ONE if cosine else x
    total = term
    square = x * x
    for k in range(1, 96):
        a, b = (2 * k - 1, 2 * k) if cosine else (2 * k, 2 * k + 1)
        term = -(term * square).divint(a * b)
        total = total + term
    # Taylor's real Lagrange remainder |D**n sin/cos|<=1.
    degree = 190 if cosine else 191
    return total.radius(6 ** (degree + 1), factorial(degree + 1))


def section(s, target):
    return I.rational(4) * exp_negative(s) * trig(s) - target


def isolate(lo, hi, target, rising):
    sign_lo = section(I(lo), target)
    sign_hi = section(I(hi), target)
    assert (sign_lo.hi < 0 and sign_hi.lo > 0) if rising else (
        sign_lo.lo > 0 and sign_hi.hi < 0)
    for _ in range(128):
        mid = (lo + hi) // 2
        sign = section(I(mid), target)
        # Never guess a sign when intervals overlap zero.
        assert sign.hi < 0 or sign.lo > 0, "unresolved sign at work cap"
        if (sign.hi < 0) == rising:
            lo = mid
        else:
            hi = mid
    root = I(lo, hi)
    left, right = section(I(lo), target), section(I(hi), target)
    assert (left.hi < 0 and right.lo > 0) if rising else (
        left.lo > 0 and right.hi < 0)
    derivative = I.rational(4) * exp_negative(root) * (
        trig(root, True) - trig(root))
    assert derivative.lo > 0 if rising else derivative.hi < 0
    return root, derivative, left, right


def binary64_ceiling(n):
    """Exact integer upward conversion of n/2**256; positive normal range."""
    assert n > 0
    exponent = n.bit_length() - 1 - BITS
    assert -1022 <= exponent <= 1023
    shift = BITS + exponent - 52
    sig = ceildiv(n, 1 << shift) if shift >= 0 else n << (-shift)
    if sig == 1 << 53:
        sig >>= 1
        exponent += 1
    bits = ((exponent + 1023) << 52) | (sig - (1 << 52))
    # Float is for encoding/display only. Exact rational comparisons prove ceil.
    value = struct.unpack(">d", bits.to_bytes(8, "big"))[0]
    previous = struct.unpack(">d", (bits - 1).to_bytes(8, "big"))[0]
    assert F(*previous.as_integer_ratio()) < F(n, S) <= F(*value.as_integer_ratio())
    return bits, value.hex()


def common_ceiling(interval):
    low, high = binary64_ceiling(interval.lo), binary64_ceiling(interval.hi)
    assert low == high, "unresolved common ceiling"
    return low


def calculate():
    pi = I.rational(16) * atan_inverse(5) - I.rational(4) * atan_inverse(239)
    sqrt_lo = isqrt(2 * S * S)
    sqrt2 = I(sqrt_lo, sqrt_lo + 1)
    assert sqrt2.lo ** 2 < 2 * S * S < sqrt2.hi ** 2
    quarter_pi = pi.divint(4)
    q = exp_negative(quarter_pi) * sqrt2.reciprocal()
    theta = q + q
    log2 = ln2()
    quiet = I.rational(5) * log2.divint(2) + quarter_pi
    expiry = quiet + I.rational(3)
    assert 0 < expiry.lo <= expiry.hi < 6 * S < (1 << 20) * S
    # Fixed dyadic brackets within the analytic monotonicity intervals.
    assert S // 2 < quarter_pi.lo and quarter_pi.hi < S
    assert pi.lo > 3 * S
    up, dup, ul, ur = isolate(0, S // 2, theta, True)
    rearm, dre, rl, rr = isolate(S, 3 * S, q, False)
    assert up.hi < rearm.lo < rearm.hi < quiet.lo < quiet.hi < expiry.lo
    q_bits, q_above = common_ceiling(q)
    below = struct.unpack(">d", (q_bits - 1).to_bytes(8, "big"))[0]
    above = struct.unpack(">d", q_bits.to_bytes(8, "big"))[0]
    assert F(*below.as_integer_ratio()) < F(q.lo, S)
    assert F(q.hi, S) < F(*above.as_integer_ratio())
    # Bit adjacency is exact for these positive finite normal values.
    holds = {}
    for d in (0, 1, 2):
        times = [common_ceiling(r + I.rational(d))
                 for r in (up, rearm, quiet)]
        exp_time = common_ceiling(expiry)
        assert F(expiry.hi, S) < F(*float.fromhex(exp_time[1]).as_integer_ratio())
        assert times[0][0] < times[1][0] < times[2][0] < exp_time[0]
        assert F(*float.fromhex(times[0][1]).as_integer_ratio()) > d
        holds[str(d)] = {
            "origin_TU": d, "up": times[0][1], "rearm": times[1][1],
            "quiet": times[2][1], "expiry": exp_time[1],
            "mapping": "store_origin=0; absolute=hold+active_root",
            "certified_strict_order": True}
    checkpoints = {}
    for a, b in ((0, 1), (1, 2), (1, 1), (2, 1)):
        s = I.rational(a, b)
        decay = exp_negative(s)
        checkpoints[str(F(a, b))] = {
            "x": (decay * trig(s, True)).pack(),
            "y": (decay * trig(s)).pack()}
    return {
        "format": "luna63c-independent-interval-witnesses", "version": 2,
        "continuation_baseline": "181b6440821e1dd6beede7e34cab9b6baada601a",
        "precision_bits": BITS, "precision_escalations": 0,
        "bisections_per_root": 128,
        "constants": {k: v.pack() for k, v in
                      (("pi", pi), ("sqrt2", sqrt2), ("ln2", log2),
                       ("q", q), ("theta", theta), ("T_q", quiet),
                       ("T_life", expiry))},
        "roots_A4": {
            "up": up.pack(), "up_derivative": dup.pack(),
            "up_left_sign": ul.pack(), "up_right_sign": ur.pack(),
            "rearm": rearm.pack(), "rearm_derivative": dre.pack(),
            "rearm_left_sign": rl.pack(), "rearm_right_sign": rr.pack()},
        "q_neighbors": {"below_hex": below.hex(), "above_hex": q_above,
                        "strict_side_and_adjacency_proved": True},
        "restricted_absolute_certificates": holds,
        "A1_proposed_checkpoints_active_TU": checkpoints,
        "N1": "partial: constants and A4 roots certified; not all C7 mappings",
        "N2": "CLOSED: exact q strictly between adjacent binary64 neighbors",
        "N3": "partial: store_origin=0 holds0,1,2 only; full C7 unresolved",
        "N4": "BLOCKED: no certified candidate arithmetic implementation",
        "N5": "BLOCKED: no complete unambiguous numeric C7 freeze",
        "N6": "Stage B conformance only; not a Stage A blocker",
        "disposition": "BLOCKED — NUMERICAL CERTIFICATE INCOMPLETE"}


if __name__ == "__main__":
    result = calculate()
    encoded = (json.dumps(result, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True) + "\n").encode("utf-8")
    # No artifact write: parent-owned publication uses printed deterministic data.
    import sys
    if sys.argv[1:] == ["--check"]:
        expected = (Path(__file__).parent / "witnesses.json").read_bytes()
        assert expected.replace(b"\r\n", b"\n") == encoded
        print("PASS exact deterministic interval-witness recomputation")
        print("witnesses.json proposed raw Git blob SHA256:",
              hashlib.sha256(encoded).hexdigest())
    else:
        print(encoded.decode("utf-8"), end="")
