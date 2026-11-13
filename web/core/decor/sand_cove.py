"""The beach in the bottom-right corner. Port of `SandCove.tsx`.

Two different geometries are at work here, and mixing them up is what makes a
beach look wrong:

- `EDGE` is the *local* waterline. The foam follows it.
- The golden sand and the jungle behind it are **horizontal** bands. They are
  the far shore, so they run with the horizon, not with the local waterline.

Everything is clipped to the sand, so no dune and no crown can ever end up
floating on the water. The SVG keeps its native ratio so the generated canopy
crowns remain round.
"""

from core.decor._markup import DECORATIVE, attrs, element
from core.svg import CanopyBlob, canopy_blobs, js_str, ribbon_path

EDGE = (
    "M266 -14 C254 48 222 101 170 128 C235 108 306 108 330 130 C353 153 297 174 240 195 "
    "C190 214 176 235 205 253 C225 266 250 272 282 278"
)

SAND = f"{EDGE} L440 280 L440 -20 Z"

# The far shore, as two horizontal bands. Each fills *downwards* from a softly
# waving edge, so the jungle above it stays visible against the sky instead of
# being buried under a slab of sand.
DUNE = "M-20 142 C70 134 160 134 250 128 C325 122 382 112 440 116 V280 H-20 Z"
FORESHORE = "M-20 180 C80 178 170 174 260 166 C335 158 388 148 440 152 V280 H-20 Z"

LAND_TONGUE = "M126 150 C210 120 302 92 440 58 V156 H126 Z"
"""The pointed peninsula visible beneath the scalloped treeline."""

# Pale tapered ribbons that tighten as they enter the cove.
SURF = (
    (
        (0, 153, 0),
        (90, 148, 3),
        (190, 137, 5),
        (270, 134, 6),
        (315, 143, 5),
        (330, 155, 4),
        (302, 174, 6),
        (250, 194, 5),
        (205, 211, 4),
        (180, 229, 2),
        (193, 245, 0),
    ),
    (
        (0, 180, 0),
        (100, 172, 3),
        (205, 157, 5),
        (268, 164, 5),
        (292, 175, 4),
        (266, 193, 5),
        (218, 208, 4),
        (171, 223, 3),
        (148, 240, 2),
        (166, 257, 0),
    ),
    (
        (0, 210, 0),
        (88, 201, 3),
        (176, 181, 5),
        (222, 187, 5),
        (246, 198, 4),
        (226, 212, 5),
        (184, 225, 4),
        (142, 238, 3),
        (121, 253, 2),
        (137, 269, 0),
    ),
)

_SURF_PATHS = "".join(element("path", ("d", ribbon_path(spine))) for spine in SURF)


def _crowns(blobs: list[CanopyBlob]) -> str:
    return "".join(
        element("circle", ("cx", js_str(b.cx)), ("cy", js_str(b.cy)), ("r", js_str(b.r)))
        for b in blobs
    )


def sand_cove(*, uid: str, seed: int = 21, class_name: str | None = None) -> str:
    sand_clip = f"{uid}-sand"
    beach_clip = f"{uid}-beach"

    # Many small crowns, not a few big ones: the key art's treeline is a
    # scalloped edge, and large discs read as a mountain instead.
    back = canopy_blobs(
        seed=seed,
        count=28,
        start=(196, 126),
        end=(462, 26),
        min_radius=10,
        max_radius=26,
        scatter=22,
    )
    front = canopy_blobs(
        seed=seed + 101,
        count=26,
        start=(246, 116),
        end=(462, 6),
        min_radius=9,
        max_radius=24,
        scatter=20,
    )

    # Everything below the dune's edge goes in the beach clip. The waterline
    # runs the full height of the viewBox, but only its lower stretch is a
    # beach; a foam line drawn higher up floats in the sky.
    defs = element(
        "defs",
        children=element("clipPath", ("id", sand_clip), children=element("path", ("d", SAND)))
        + element("clipPath", ("id", beach_clip), children=element("path", ("d", DUNE))),
    )
    # The cove's nested surf is painted below the land.
    surf = element("g", ("data-surf", "true"), ("fill", "var(--c-foam-100)"), children=_SURF_PATHS)
    # Jungle first, against the sky, then the golden far shore over its base,
    # then the near sand.
    land = element(
        "g",
        ("clip-path", f"url(#{sand_clip})"),
        children=element("path", ("d", LAND_TONGUE), ("fill", "var(--c-jungle-500)"))
        + element("g", ("fill", "var(--c-aqua-400)"), children=_crowns(back))
        + element("g", ("fill", "var(--c-aqua-500)"), children=_crowns(front))
        + element("path", ("d", DUNE), ("fill", "var(--c-sand-400)"))
        + element("path", ("d", FORESHORE), ("fill", "var(--c-sand-200)")),
    )
    # The bright lip where the water meets the beach.
    waterline = element(
        "g",
        ("clip-path", f"url(#{beach_clip})"),
        children=element(
            "path",
            ("data-waterline", "true"),
            ("d", EDGE),
            ("fill", "none"),
            ("stroke", "var(--c-paper)"),
            ("stroke-width", "8"),
            ("stroke-linecap", "round"),
            ("vector-effect", "non-scaling-stroke"),
        ),
    )

    opening = attrs(
        ("viewBox", "0 0 420 270"),
        ("class", class_name),
        ("preserveAspectRatio", "xMaxYMax meet"),
        *DECORATIVE,
    )
    return f"<svg{opening}>{defs}{surf}{land}{waterline}</svg>"
