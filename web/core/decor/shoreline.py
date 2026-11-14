"""The four broad water planes from the key art. Port of `Shoreline.tsx`.

Their shared crest-valley-rise rhythm matters more than small surface
details: it is what makes the lower edge read as one rolling Caribbean sea
instead of a stack of nearly horizontal stripes.
"""

from core.decor._markup import DECORATIVE, attrs, element

# Back to front.
BANDS = (
    (
        "M0 180 C150 170 225 72 360 22 C480 -18 565 92 690 154 C805 210 910 152 1044 90 "
        "C1168 34 1300 48 1440 72 V280 H0 Z",
        "var(--c-foam-200)",
    ),
    (
        "M0 220 C180 210 260 126 400 72 C525 24 610 148 735 210 C850 266 950 212 1080 150 "
        "C1200 94 1320 104 1440 122 V280 H0 Z",
        "var(--c-foam-300)",
    ),
    (
        "M0 258 C200 250 310 184 440 132 C560 86 650 210 775 264 C900 318 1000 264 1120 202 "
        "C1230 146 1340 154 1440 166 V280 H0 Z",
        "var(--c-ocean-200)",
    ),
    (
        "M0 282 C220 278 340 238 480 190 C600 150 690 252 820 292 C950 332 1050 302 1170 250 "
        "C1280 202 1365 204 1440 214 V280 H0 Z",
        "var(--c-ocean-300)",
    ),
)

# The same rhythm rebuilt for stacked layouts. Compressing the desktop geometry
# into a phone makes its tall first crest look like a pointed mountain, but
# flattening it into stripes is the opposite failure. These planes trade the
# single steep peak for two long, rolling swells, and keep every trough clear
# of the bottom edge so no sliver of page shows beneath the front band.
COMPACT_BANDS = (
    (
        "M0 118 C200 94 340 72 520 90 C700 108 830 156 1010 150 C1180 144 1320 110 1440 90 "
        "V280 H0 Z",
        "var(--c-foam-200)",
    ),
    (
        "M0 162 C190 140 350 120 540 138 C720 154 850 198 1030 194 C1200 190 1330 158 1440 138 "
        "V280 H0 Z",
        "var(--c-foam-300)",
    ),
    (
        "M0 204 C180 186 360 166 560 184 C740 200 870 234 1050 232 C1210 230 1340 204 1440 186 "
        "V280 H0 Z",
        "var(--c-ocean-200)",
    ),
    (
        "M0 244 C170 230 370 212 580 226 C760 238 890 256 1070 256 C1220 256 1350 238 1440 226 "
        "V280 H0 Z",
        "var(--c-ocean-300)",
    ),
)


def _bands(bands: tuple[tuple[str, str], ...]) -> str:
    return "".join(element("path", ("d", d), ("fill", fill)) for d, fill in bands)


_INNER = element("g", ("data-wide-bands", "true"), children=_bands(BANDS)) + element(
    "g", ("data-compact-bands", "true"), children=_bands(COMPACT_BANDS)
)


def shoreline(*, class_name: str | None = None) -> str:
    opening = attrs(
        ("class", class_name),
        ("viewBox", "0 0 1440 280"),
        ("preserveAspectRatio", "none"),
        *DECORATIVE,
    )
    return f"<svg{opening}>{_INNER}</svg>"
