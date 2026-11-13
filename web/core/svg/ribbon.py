"""Tapered, variable-width bands. Port of legacy-react/src/lib/svg/ribbon.ts.

The arithmetic follows the TypeScript operation for operation (same order,
same `Math.hypot`), so the path strings are byte-identical.
"""

from collections.abc import Sequence
from typing import NamedTuple

from core.svg.numbers import js_fixed2, js_hypot

type SpinePoint = Sequence[float]
"""`(x, y, radius)`."""


class Point(NamedTuple):
    x: float
    y: float


def _f(n: float) -> str:
    return js_fixed2(n)


def smooth_path(points: Sequence[Point], is_closed: bool) -> str:
    """A smooth Catmull-Rom cubic Bézier path through `points`."""
    if not points:
        return ""
    if len(points) == 1:
        return f"M {_f(points[0].x)} {_f(points[0].y)}"
    if len(points) == 2:
        a, b = points
        return f"M {_f(a.x)} {_f(a.y)} L {_f(b.x)} {_f(b.y)}"

    n = len(points)
    parts = [f"M {_f(points[0].x)} {_f(points[0].y)}"]
    for i in range(n if is_closed else n - 1):
        p0 = points[(i - 1 + n) % n]
        p1 = points[i % n]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n]

        cp1x = p1.x + (p2.x - p0.x) / 6
        cp1y = p1.y + (p2.y - p0.y) / 6
        cp2x = p2.x - (p3.x - p1.x) / 6
        cp2y = p2.y - (p3.y - p1.y) / 6

        parts.append(f" C {_f(cp1x)} {_f(cp1y)}, {_f(cp2x)} {_f(cp2y)}, {_f(p2.x)} {_f(p2.y)}")
    return "".join(parts)


def ribbon_path(spine: Sequence[SpinePoint]) -> str:
    """A closed band around `spine`, offset by each point's radius."""
    if len(spine) < 2:
        return ""

    left: list[Point] = []
    right: list[Point] = []
    last = len(spine) - 1

    for i, (x, y, r) in enumerate(spine):
        if i == 0:
            next_x, next_y = spine[1][0], spine[1][1]
            dx = next_x - x
            dy = next_y - y
        elif i == last:
            prev_x, prev_y = spine[i - 1][0], spine[i - 1][1]
            dx = x - prev_x
            dy = y - prev_y
        else:
            prev_x, prev_y = spine[i - 1][0], spine[i - 1][1]
            next_x, next_y = spine[i + 1][0], spine[i + 1][1]
            dx = next_x - prev_x
            dy = next_y - prev_y

        length = js_hypot(dx, dy) or 1
        # Unit normal rotated 90 degrees CCW (-dy, dx).
        nx = -dy / length
        ny = dx / length

        left.append(Point(x + nx * r, y + ny * r))
        right.append(Point(x - nx * r, y - ny * r))

    # Left edge forwards, right edge backwards: one closed loop.
    return f"{smooth_path([*left, *reversed(right)], True)} Z"
