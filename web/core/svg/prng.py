"""Deterministic pseudo-random number generator (Mulberry32).

Port of legacy-react/src/lib/svg/random.ts (`createRandom`). Seeded so the
procedural artwork renders identically on every request and machine, and
identically to the React site. Python's `random` is a bug in a shape: it would
reshuffle the scene and could never match the JS sequence.

JS works on 32-bit integers here (`>>> 0`, `Math.imul`, `^`). Keeping every
intermediate as an unsigned 32-bit value gives the same bits: XOR, OR and
multiplication modulo 2^32 do not care whether the bits are read as signed.
"""

import math
from collections.abc import Callable

_MASK = 0xFFFFFFFF


def create_random(seed: float) -> Callable[[], float]:
    """Return a function producing floats in [0, 1), like `createRandom(seed)`."""
    # `Math.floor(seed) >>> 0`: ToUint32, so negative seeds wrap around.
    state = int(math.floor(seed)) & _MASK if math.isfinite(seed) else 0

    def next_value() -> float:
        nonlocal state
        state = (state + 0x6D2B79F5) & _MASK
        t = ((state ^ (state >> 15)) * (1 | state)) & _MASK
        t = ((t + (((t ^ (t >> 7)) * (61 | t)) & _MASK)) & _MASK) ^ t
        return ((t ^ (t >> 14)) & _MASK) / 4294967296

    return next_value
