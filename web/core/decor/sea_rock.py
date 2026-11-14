"""The lone rock breaking the surface offshore. Port of `SeaRock.tsx`.

Drawn rather than taken from the official set: at the size it appears here
this reads better than the supplied `sea-rock` artwork, which is cut for
larger placements.
"""

from core.decor._markup import DECORATIVE, attrs, element
from core.svg import ribbon_path

OUTLINE = (
    "M3 86 C7 74 22 66 36 56 C48 48 54 30 66 26 C78 22 87 36 93 50 C99 64 103 78 102 88 "
    "C74 97 26 96 3 86 Z"
)

# Tapered currents wrapping the rock, built from the ribbon primitive.
CURRENTS = (
    ((40, 40, 0), (50, 34, 1.6), (60, 33, 1.8), (70, 37, 1.3), (78, 42, 0)),
    ((16, 66, 0), (28, 58, 1.7), (42, 55, 2), (56, 57, 1.7), (68, 62, 1.2), (76, 66, 0)),
    ((12, 82, 0), (26, 76, 1.6), (40, 74, 1.8), (54, 77, 1.6), (66, 82, 1.2), (74, 86, 0)),
)

_INNER = element(
    "path",
    ("d", OUTLINE),
    ("fill", "var(--c-ocean-500)"),
    ("stroke", "var(--c-paper)"),
    ("stroke-width", "5"),
    ("stroke-linejoin", "round"),
) + element(
    "g",
    ("fill", "var(--c-paper)"),
    children="".join(element("path", ("d", ribbon_path(spine))) for spine in CURRENTS),
)


def sea_rock(*, class_name: str | None = None) -> str:
    opening = attrs(("viewBox", "0 0 106 96"), ("class", class_name), *DECORATIVE)
    return f"<svg{opening}>{_INNER}</svg>"
