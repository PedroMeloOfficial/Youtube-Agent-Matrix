"""
GSAP-compatible easing curves (library module, no CLI).

The camera is designed in the same vocabulary as the animations (``power2.out``,
``expo.in``, ``power4.inOut`` …) so the two move as one system. Final Cut only
interpolates keyframes linearly or with its own presets, so the camera script samples
these curves densely and writes one keyframe per frame during a move: the curve that
plays is the curve that was designed.
"""

from __future__ import annotations

import math


def _power(p):
    def ease_in(t):
        return t ** (p + 1)
    return ease_in


def _expo_in(t):
    return 0.0 if t <= 0 else 2 ** (10 * (t - 1))


def _sine_in(t):
    return 1 - math.cos(t * math.pi / 2)


def _circ_in(t):
    return 1 - math.sqrt(max(0.0, 1 - t * t))


_IN = {"none": lambda t: t, "linear": lambda t: t,
       "power1": _power(1), "power2": _power(2), "power3": _power(3), "power4": _power(4),
       "quad": _power(1), "cubic": _power(2), "quart": _power(3), "quint": _power(4),
       "expo": _expo_in, "sine": _sine_in, "circ": _circ_in}


def ease(name: str, t: float) -> float:
    """Evaluate 'power2.out', 'expo.in', 'power4.inOut', 'none'… at t in [0, 1]."""
    t = min(1.0, max(0.0, t))
    base, _, kind = name.partition(".")
    f = _IN.get(base)
    if f is None:
        raise ValueError(f"Unknown ease {name!r}")
    if base in ("none", "linear"):
        return t
    kind = kind or "out"
    if kind == "in":
        return f(t)
    if kind == "out":
        return 1 - f(1 - t)
    if kind == "inOut":
        return f(2 * t) / 2 if t < 0.5 else 1 - f(2 - 2 * t) / 2
    raise ValueError(f"Unknown ease direction in {name!r}")


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t
