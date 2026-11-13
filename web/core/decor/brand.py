"""`BrandMark` and `BrandShape`: the supplied artwork, inlined verbatim.

Inlined rather than referenced with `<img>` so shapes can be tinted and the
page makes no extra requests. Ids are namespaced per instance with `uid` (the
React site uses `useId`), which is what lets the same file appear more than
once without its clip paths fighting.
"""

from core.decor._markup import DECORATIVE, attrs
from core.decor.shapes import BRAND_MARK, DECOR_SHAPES
from core.svg import namespace_svg_ids, svg_inner_markup, svg_view_box

_MARK_VIEW_BOX = svg_view_box(BRAND_MARK)
_MARK_INNER = svg_inner_markup(BRAND_MARK)


def brand_mark(*, title: str, uid: str, class_name: str | None = None) -> str:
    """The official mark. Deliberately not redrawn or re-coloured.

    `title` is the accessible name and comes from the dictionary.
    """
    opening = attrs(
        ("viewBox", _MARK_VIEW_BOX),
        ("class", class_name),
        ("role", "img"),
        ("aria-label", title),
    )
    return f"<svg{opening}>{namespace_svg_ids(_MARK_INNER, uid)}</svg>"


def brand_shape(
    name: str, *, uid: str, color: str | None = None, class_name: str | None = None
) -> str:
    """One shape from the catalogue in `shapes.py`.

    `color` tints the shapes drawn with `currentColor` and is ignored by the
    multi-colour ones. An unknown name raises `KeyError`.
    """
    markup = DECOR_SHAPES[name]
    opening = attrs(
        ("viewBox", svg_view_box(markup)),
        ("class", class_name),
        # React serialises `style={{ color }}` as `color:<value>`, trimmed.
        ("style", f"color:{color.strip()}" if color else None),
        *DECORATIVE,
    )
    return f"<svg{opening}>{namespace_svg_ids(svg_inner_markup(markup), uid)}</svg>"
