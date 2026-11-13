"""Framework-free SVG geometry. Port of legacy-react/src/lib/svg/.

Pure functions: numbers in, strings out. No Django, no templates, and no
`random` — anything random is seeded through `create_random`.
"""

from core.svg.canopy import CanopyBlob, canopy_blobs
from core.svg.markup import namespace_svg_ids, svg_inner_markup, svg_view_box
from core.svg.numbers import js_fixed2, js_hypot, js_round, js_str
from core.svg.prng import create_random
from core.svg.ribbon import SpinePoint, ribbon_path

__all__ = [
    "CanopyBlob",
    "SpinePoint",
    "canopy_blobs",
    "create_random",
    "js_fixed2",
    "js_hypot",
    "js_round",
    "js_str",
    "namespace_svg_ids",
    "ribbon_path",
    "svg_inner_markup",
    "svg_view_box",
]
