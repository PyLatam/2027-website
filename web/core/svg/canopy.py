"""Overlapping crowns along a line. Port of legacy-react/src/lib/svg/canopy.ts."""

from typing import NamedTuple

from core.svg.numbers import js_hypot, js_round
from core.svg.prng import create_random


class CanopyBlob(NamedTuple):
    cx: float
    cy: float
    r: float


def canopy_blobs(
    *,
    seed: float,
    count: int,
    start: tuple[float, float],
    end: tuple[float, float],
    min_radius: float,
    max_radius: float,
    scatter: float,
) -> list[CanopyBlob]:
    """Circles along `start` → `end` with seeded scatter (`canopyBlobs`).

    `start`/`end` are the TypeScript `from`/`to`; `from` is a Python keyword.
    """
    rand = create_random(seed)
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length = js_hypot(dx, dy) or 1
    nx = -dy / length
    ny = dx / length

    blobs: list[CanopyBlob] = []
    for i in range(count):
        t = i / (count - 1) if count > 1 else 0.5
        base_x = x1 + dx * t
        base_y = y1 + dy * t
        # The three draws happen in this order in JS too; keep it.
        offset_normal = (rand() - 0.5) * 2 * scatter
        offset_tangent = (rand() - 0.5) * (length / max(count, 1))
        cx = js_round((base_x + nx * offset_normal + (dx / length) * offset_tangent) * 10) / 10
        cy = js_round((base_y + ny * offset_normal + (dy / length) * offset_tangent) * 10) / 10
        r = js_round((min_radius + rand() * (max_radius - min_radius)) * 10) / 10
        blobs.append(CanopyBlob(cx, cy, r))
    return blobs
