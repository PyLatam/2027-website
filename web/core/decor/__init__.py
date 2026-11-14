"""Presentational SVG shapes. Port of legacy-react/src/components/decor/.

Each function returns the markup React renders for the same props, as a plain
string. They know nothing about where they sit: placement belongs to the hero
templates, through `class_name`. No text, no state, no dictionary lookups;
copy such as the mark's accessible name is passed in.

Shapes with ids take a `uid` (React's `useId`); `core.templatetags.decor`
hands out one per instance and page.
"""

from core.decor.brand import brand_mark, brand_shape
from core.decor.circuit_traces import circuit_traces
from core.decor.palm_tree import palm_tree
from core.decor.sand_cove import sand_cove
from core.decor.sea_rock import sea_rock
from core.decor.shapes import DECOR_SHAPES, DecorShapeName
from core.decor.shoreline import shoreline

__all__ = [
    "DECOR_SHAPES",
    "DecorShapeName",
    "brand_mark",
    "brand_shape",
    "circuit_traces",
    "palm_tree",
    "sand_cove",
    "sea_rock",
    "shoreline",
]
