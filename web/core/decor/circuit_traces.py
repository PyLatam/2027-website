"""The faint PCB traces from the key art. Port of `CircuitTraces.tsx`.

The "tech" half of the tropical/tech pairing. Deliberately low-contrast: it is
texture, never content.
"""

from core.decor._markup import DECORATIVE, attrs, element
from core.svg import js_str

TRACES = (
    "M0 30 H60 L80 50 H140 L160 30 H240",
    "M20 90 H90 L110 70 H180 L200 90 H260",
    "M0 140 H50 L70 120 H130 L150 140 H230 L250 160",
    "M40 190 H110 L130 170 H210",
    "M110 0 V40 L130 60 V110",
    "M190 10 V60 L170 80 V130",
)

NODES = ((60, 30), (140, 50), (90, 90), (180, 70), (50, 140), (230, 140), (110, 40), (190, 60))

CHIPS = ((16, 46), (28, 46), (16, 58), (204, 104), (216, 104), (204, 116), (96, 158), (108, 158))


def _render() -> str:
    traces = "".join(element("path", ("d", d)) for d in TRACES)
    nodes = "".join(
        element("circle", ("cx", js_str(cx)), ("cy", js_str(cy)), ("r", "3.4")) for cx, cy in NODES
    )
    chips = "".join(
        element(
            "rect",
            ("x", js_str(x)),
            ("y", js_str(y)),
            ("width", "8"),
            ("height", "8"),
            ("rx", "1.5"),
        )
        for x, y in CHIPS
    )
    return (
        element(
            "g",
            ("fill", "none"),
            ("stroke", "currentColor"),
            ("stroke-width", "1.6"),
            ("stroke-linecap", "round"),
            ("stroke-linejoin", "round"),
            children=traces,
        )
        + element(
            "g",
            ("fill", "none"),
            ("stroke", "currentColor"),
            ("stroke-width", "1.6"),
            children=nodes,
        )
        + element("g", ("fill", "currentColor"), ("opacity", "0.65"), children=chips)
    )


_INNER = _render()


def circuit_traces(*, class_name: str | None = None) -> str:
    opening = attrs(("viewBox", "0 0 260 200"), ("class", class_name), *DECORATIVE)
    return f"<svg{opening}>{_INNER}</svg>"
