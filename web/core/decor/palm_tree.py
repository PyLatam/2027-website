"""A coconut palm. Port of `PalmTree.tsx`.

A thin trunk with a small fan of drooping blades, both built from the ribbon
primitive, so the whole tree is two shapes.
"""

import math

from core.decor._markup import DECORATIVE, attrs, element
from core.svg import js_str, ribbon_path

CROWN_X, CROWN_Y = 86, 98
"""Where the trunk ends and the crown begins."""

# A thin, slightly leaning trunk. The key art draws its palms as delicate
# silhouettes: a thicker trunk with a denser crown turns into noise at the size
# these appear.
TRUNK = (
    (130, 340, 5.2),
    (124, 292, 4.4),
    (115, 242, 3.7),
    (104, 192, 3),
    (94, 146, 2.5),
    (88, 114, 2.1),
    (86, 100, 1.9),
)

# One drooping crown blade, drawn from the crown outward along +x. Broad rather
# than hairline: thin blades spread evenly around a point read as a pinwheel.
BLADE = ((0, 0, 3.5), (16, -11, 11), (35, -12, 10.5), (53, -3, 6.5), (68, 17, 0))

BLADE_PATH = ribbon_path(BLADE)
TRUNK_PATH = ribbon_path(TRUNK)


def palm_tree(
    *,
    trunk_color: str,
    crown_color: str,
    fronds: int = 7,
    flip: bool = False,
    class_name: str | None = None,
) -> str:
    """`flip` mirrors the tree, so a grove is not one tree repeated."""
    # Weighted to the upper half, with the outermost pair drooping: a real crown
    # is not an even circle.
    angles = [-180 + (index * 252) / max(fronds - 1, 1) for index in range(fronds)]

    blades = []
    for angle in angles:
        # A blade droops clockwise from the direction it points in. On the left
        # half of the crown that would arc *upwards*, so those blades are
        # mirrored; without this the crown reads as a pinwheel.
        points_left = math.cos((angle * math.pi) / 180) < 0
        transform = f"translate({CROWN_X} {CROWN_Y}) rotate({js_str(angle)})" + (
            " scale(1 -1)" if points_left else ""
        )
        blades.append(
            element("g", ("transform", transform), children=element("path", ("d", BLADE_PATH)))
        )

    crown = "".join(blades) + element(
        # Hides the point every blade radiates from.
        "circle",
        ("cx", js_str(CROWN_X)),
        ("cy", js_str(CROWN_Y)),
        ("r", "5.5"),
    )
    # Coconuts, tucked under the crown.
    coconuts = "".join(
        element("circle", ("cx", js_str(CROWN_X + dx)), ("cy", js_str(CROWN_Y + dy)), ("r", r))
        for dx, dy, r in ((-5, 8, "3.4"), (3, 10, "3.1"), (-1, 15, "2.8"))
    )
    tree = (
        element("path", ("d", TRUNK_PATH), ("fill", trunk_color))
        + element("g", ("fill", crown_color), children=crown)
        + element("g", ("fill", trunk_color), children=coconuts)
    )

    opening = attrs(("viewBox", "0 0 200 344"), ("class", class_name), *DECORATIVE)
    group = element(
        "g", ("transform", "translate(200 0) scale(-1 1)" if flip else None), children=tree
    )
    return f"<svg{opening}>{group}</svg>"
