"""Helpers for inlining SVG files. Port of legacy-react/src/lib/svg/markup.ts."""

import re

_VIEW_BOX = re.compile(r"""viewBox=["']([^"']+)["']""", re.IGNORECASE)
_OPEN_TAG = re.compile(r"^<svg[^>]*>", re.IGNORECASE)
_CLOSE_TAG = re.compile(r"</svg>\s*\Z", re.IGNORECASE)
# `re.ASCII` gives `\b` the JS meaning.
_ID = re.compile(r"""\bid=["']([^"']+)["']""", re.ASCII)


def svg_view_box(markup: str) -> str:
    """The `viewBox` of an SVG document, or `0 0 100 100`."""
    match = _VIEW_BOX.search(markup)
    return match.group(1) if match else "0 0 100 100"


def svg_inner_markup(markup: str) -> str:
    """The SVG document without its outer `<svg>` and `</svg>` tags."""
    return _CLOSE_TAG.sub("", _OPEN_TAG.sub("", markup, count=1), count=1).strip()


def namespace_svg_ids(markup: str, uid: str) -> str:
    """Suffix every `id` with `-<uid>`, along with `url(#…)` and `href="#…"`.

    This is what lets one file be inlined several times in a page without its
    clip paths fighting. Ids are escaped before going into a pattern; the
    TypeScript does not escape them, which makes no difference for the ids the
    supplied files use (letters, digits, `-` and `_`).
    """
    ids = dict.fromkeys(_ID.findall(markup))  # Unique, in document order.
    result = markup
    for id_ in ids:
        namespaced = f"{id_}-{uid}"
        escaped = re.escape(id_)
        # Replacements are functions so nothing in an id is read as `\1` etc.
        result = re.sub(
            rf"""\bid=["']{escaped}["']""",
            lambda _, ns=namespaced: f'id="{ns}"',
            result,
            flags=re.ASCII,
        )
        result = re.sub(rf"url\(#{escaped}\)", lambda _, ns=namespaced: f"url(#{ns})", result)
        result = re.sub(
            rf"""(href=["'])#{escaped}(["'])""",
            lambda m, ns=namespaced: f"{m.group(1)}#{ns}{m.group(2)}",
            result,
        )
    return result
