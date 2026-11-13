"""The official artwork, loaded verbatim. Port of `shapes.ts` and the logo import.

The files in `core/assets/` are byte-for-byte copies of
`legacy-react/src/assets/` (a test checks their hashes). Never redraw one of
these by hand: to change a shape, replace its file.

Single-colour shapes were rewritten to `fill="currentColor"`, so they are
tinted with the CSS `color` property. Multi-colour shapes keep the brand
colours they shipped with.

To add a shape: drop the file in `core/assets/decor/` and add it below.
`sea-rock` and `dot-cluster` are not in the current scene; they are delivered
artwork kept discoverable, not dead code. (The scene draws its own `sea_rock`:
the supplied rock is cut for larger placements than the hero gives it.)
"""

from pathlib import Path
from typing import Literal, get_args

ASSETS = Path(__file__).resolve().parent.parent / "assets"

type DecorShapeName = Literal[
    "coral-branch",
    "coral-fan",
    "coral-staghorn",
    "dot-cluster",
    "leaf-frond-01",
    "leaf-frond-02",
    "leaf-frond-trio",
    "sea-rock",
]


def _read(relative: str) -> str:
    # Bytes, not `read_text`: universal newlines would rewrite `\r\n`.
    return (ASSETS / relative).read_bytes().decode("utf-8")


DECOR_SHAPES: dict[str, str] = {
    name: _read(f"decor/{name}.svg") for name in get_args(DecorShapeName.__value__)
}

BRAND_MARK = _read("pycon-latam-rd-mark.svg")
