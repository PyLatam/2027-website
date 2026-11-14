"""Serialise elements exactly as `react-dom/server` does for these shapes.

React writes every non-void element with a closing tag (`<path …></path>`),
drops attributes whose value is `None`/`undefined`, and escapes attribute
values with the same five entities as `html.escape`.
"""

from html import escape


def attrs(*pairs: tuple[str, str | None]) -> str:
    """` name="value"` for each pair whose value is not `None`, in order."""
    return "".join(f' {name}="{escape(value)}"' for name, value in pairs if value is not None)


def element(tag: str, *pairs: tuple[str, str | None], children: str = "") -> str:
    return f"<{tag}{attrs(*pairs)}>{children}</{tag}>"


DECORATIVE: tuple[tuple[str, str | None], ...] = (("aria-hidden", "true"), ("focusable", "false"))
"""The attributes every decorative SVG ends with: hidden and never focusable."""
