"""Isolated reference arbiter. No neural updates, training, routing or event removal."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import hmac
import json
import math
from numbers import Real
from typing import Iterable

VERSION = "local-priority-lottery-v1"
MAX_REQUESTS = 64
MAX_WEIGHT = (1 << 32) - 1
MAX_PRIORITY = (1 << 16) - 1
MAX_DRAWS = 8


class ArbitrationError(ValueError):
    pass


def _identifier(value, name):
    if not isinstance(value, str) or not 1 <= len(value) <= 128:
        raise ArbitrationError(name + " must contain 1..128 characters")
    return value


def _integer(value, name, maximum):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
        raise ArbitrationError(name + " is outside its integer range")
    return value


def _time(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ArbitrationError("time must be a real number")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ArbitrationError("time must be finite and nonnegative")
    return 0.0 if result == 0 else result


@dataclass(frozen=True, slots=True)
class Request:
    locality: str
    priority: int
    connection_id: str
    event_id: str
    timestamp: float
    weight: int

    def __post_init__(self):
        for name in ("locality", "connection_id", "event_id"):
            _identifier(getattr(self, name), name)
        _integer(self.priority, "priority", MAX_PRIORITY)
        _integer(self.weight, "weight", MAX_WEIGHT)
        object.__setattr__(self, "timestamp", _time(self.timestamp))


@dataclass(frozen=True, slots=True)
class Decision:
    version: str
    locality: str
    priority: int
    logical_timestamp: float
    decision_id: str
    model_id: str
    seed: int
    pool: tuple[Request, ...]
    effective_weights: tuple[int, ...]
    total_weight: int
    ticket: int
    sampler_attempts: int
    uniform_fallback: bool
    winner_event_id: str
    winner_connection_id: str

    @property
    def probabilities(self):
        """Exact numerator/denominator pairs; no floating normalization."""
        return tuple((r.connection_id, w, self.total_weight)
                     for r, w in zip(self.pool, self.effective_weights))


def _ticket(total, seed, context):
    # Rejection removes modulo bias. Both integer work and rejection attempts are bounded.
    domain = 1 << 64
    cutoff = domain - domain % total
    frame = json.dumps(context, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True).encode("utf-8")
    key = seed.to_bytes(8, "big")
    for attempt in range(MAX_DRAWS):
        digest = hmac.new(key, frame + b"\0" + bytes([attempt]), hashlib.sha256).digest()
        number = int.from_bytes(digest[:8], "big")
        if number < cutoff:
            return number % total, attempt + 1
    raise ArbitrationError("bounded random sampler exhausted; no fallback winner")


def choose(requests: Iterable[Request], *, locality: str, now: float,
           seed: int, decision_id: str, model_id: str) -> Decision | None:
    """Choose one head request from the oldest ready, local, equal-priority pool.

    The caller supplies at most one head per connection and commits service/removal.
    Repeating a decision_id is permitted for replay, not a new service transaction.
    """
    _identifier(locality, "locality")
    _identifier(decision_id, "decision_id")
    _identifier(model_id, "model_id")
    _integer(seed, "seed", (1 << 64) - 1)
    now = _time(now)
    bounded = []
    for request in requests:
        if len(bounded) == MAX_REQUESTS:
            raise ArbitrationError("request cap exceeded")
        if not isinstance(request, Request):
            raise ArbitrationError("expected Request")
        bounded.append(request)
    local = [r for r in bounded if r.locality == locality]
    if len({r.connection_id for r in local}) != len(local):
        raise ArbitrationError("provide exactly one head per local connection")
    if len({r.event_id for r in local}) != len(local):
        raise ArbitrationError("duplicate local event identity")
    ready = [r for r in local if r.timestamp <= now]
    if not ready:
        return None
    timestamp = min(r.timestamp for r in ready)
    chronological = [r for r in ready if r.timestamp == timestamp]
    priority = min(r.priority for r in chronological)  # Priority 0 is highest.
    pool = tuple(sorted((r for r in chronological if r.priority == priority),
                        key=lambda r: (r.connection_id, r.event_id)))
    raw = tuple(r.weight for r in pool)
    fallback = not any(raw)
    effective = (1,) * len(pool) if fallback else raw
    total = sum(effective)
    context = dict(version=VERSION, locality=locality,
                   timestamp_hex=timestamp.hex(), priority=priority, decision_id=decision_id)
    ticket, attempts = _ticket(total, seed, context)
    cumulative = 0
    for request, weight in zip(pool, effective):
        cumulative += weight
        if ticket < cumulative:
            return Decision(VERSION, locality, priority, timestamp, decision_id, model_id,
                            seed, pool, effective, total, ticket, attempts, fallback,
                            request.event_id, request.connection_id)
    raise ArbitrationError("invalid cumulative lottery state")
