"""JavaScript number semantics, for SVG output identical to the React site.

Every number written into SVG goes through `js_str`, never through `str()` or
an f-string: Python prints `3.0` and `1e-07` where JavaScript prints `3` and
`1e-7`. The other helpers reproduce the two JS rounding rules the generators
rely on, which differ from Python's own (see the Phase 3 pitfalls in
docs/django-migration.md).
"""

import math
from decimal import ROUND_HALF_UP, Decimal

_CENTS = Decimal("0.01")


def js_str(value: float) -> str:
    """`String(value)` for a JS number (ECMAScript `Number::toString`)."""
    value = float(value)
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "Infinity" if value > 0 else "-Infinity"
    if value == 0:
        return "0"  # Also for -0, like JS.

    sign = "-" if value < 0 else ""
    # `repr` gives the shortest digit string that round-trips, as JS does.
    mantissa, _, exponent = repr(abs(value)).partition("e")
    whole, _, fraction = mantissa.partition(".")
    combined = whole + fraction
    stripped = combined.lstrip("0")
    digits = stripped.rstrip("0")
    k = len(digits)
    # The value is 0.<digits> × 10^n.
    n = len(whole) + int(exponent or 0) - (len(combined) - len(stripped))

    if k <= n <= 21:
        return sign + digits + "0" * (n - k)
    if 0 < n <= 21:
        return f"{sign}{digits[:n]}.{digits[n:]}"
    if -6 < n <= 0:
        return f"{sign}0.{'0' * -n}{digits}"
    e = n - 1
    e_str = f"e{'+' if e >= 0 else '-'}{abs(e)}"
    if k == 1:
        return sign + digits + e_str
    return f"{sign}{digits[0]}.{digits[1:]}{e_str}"


def js_round(value: float) -> float:
    """`Math.round`: the nearest integer, with halves rounded towards +∞.

    Python's `round` rounds halves to even, and `floor(x + 0.5)` is wrong for
    0.49999999999999994, so this compares against the floor instead.
    """
    value = float(value)
    if not math.isfinite(value) or value == 0:
        return value
    floor = math.floor(value)
    result = floor + 1 if value - floor >= 0.5 else floor
    if result == 0 and value < 0:
        return -0.0
    return float(result)


def js_fixed2(value: float) -> str:
    """`Number(value.toFixed(2)).toString()`.

    `toFixed` rounds the *exact* binary value and breaks exact ties away from
    zero (`0.125` → `0.13`, where Python's `f"{0.125:.2f}"` gives `0.12`).
    Passing the result back through `Number` turns `-0.00` into `0`.
    """
    value = float(value)
    if not math.isfinite(value) or abs(value) >= 1e21:
        return js_str(value)  # `toFixed` falls back to `ToString` here.
    fixed = Decimal(value).quantize(_CENTS, rounding=ROUND_HALF_UP)
    return js_str(float(fixed))


def js_hypot(x: float, y: float) -> float:
    """`Math.hypot(x, y)` as V8 computes it.

    V8 scales by the larger magnitude and sums with Kahan compensation, which
    can differ from Python's `math.hypot` in the last bit. Porting the same
    steps keeps the result bit-identical.
    """
    values = [abs(float(x)), abs(float(y))]
    if any(math.isinf(v) for v in values):
        return math.inf
    if any(math.isnan(v) for v in values):
        return math.nan
    largest = max(values)
    if largest == 0:
        return 0.0
    total = 0.0
    compensation = 0.0
    for v in values:
        n = v / largest
        summand = n * n - compensation
        preliminary = total + summand
        compensation = (preliminary - total) - summand
        total = preliminary
    return math.sqrt(total) * largest
