"""Template tags for the decor shapes in `core.decor`.

Usage: `{% load decor %}`, then for example
`{% brand_shape "coral-fan" color="var(--c-aqua-600)" class_name="…" %}`.
Placement is the template's job, through `class_name`; the shapes know nothing
about where they sit.

Shapes with ids get a fresh uid per instance, the job `useId` does in React,
so two copies of one file never share a clip path. The counter lives in the
root of `render_context`, which is shared by a page and every template it
includes and starts empty on each render, so ids are unique within a page and
stable across requests.
"""

from django import template
from django.utils.safestring import SafeString, mark_safe

from core import decor

register = template.Library()

_COUNTER = "core.decor.uid"


def _next_uid(context: template.Context) -> str:
    root = context.render_context.dicts[0]
    root[_COUNTER] = root.get(_COUNTER, 0) + 1
    return f"svg{root[_COUNTER]}"


def _safe(markup: str) -> SafeString:
    # `core.decor` escapes every attribute value it writes, and the only
    # unescaped content is the supplied artwork from `core/assets/`.
    return mark_safe(markup)  # noqa: S308


@register.simple_tag(takes_context=True)
def brand_mark(context: template.Context, title: str, class_name: str | None = None) -> str:
    return _safe(decor.brand_mark(title=title, uid=_next_uid(context), class_name=class_name))


@register.simple_tag(takes_context=True)
def brand_shape(
    context: template.Context, name: str, color: str | None = None, class_name: str | None = None
) -> str:
    return _safe(
        decor.brand_shape(name, uid=_next_uid(context), color=color, class_name=class_name)
    )


@register.simple_tag
def circuit_traces(class_name: str | None = None) -> str:
    return _safe(decor.circuit_traces(class_name=class_name))


@register.simple_tag
def palm_tree(
    trunk_color: str,
    crown_color: str,
    fronds: int = 7,
    flip: bool = False,
    class_name: str | None = None,
) -> str:
    return _safe(
        decor.palm_tree(
            trunk_color=trunk_color,
            crown_color=crown_color,
            fronds=fronds,
            flip=flip,
            class_name=class_name,
        )
    )


@register.simple_tag(takes_context=True)
def sand_cove(context: template.Context, seed: int = 21, class_name: str | None = None) -> str:
    return _safe(decor.sand_cove(uid=_next_uid(context), seed=seed, class_name=class_name))


@register.simple_tag
def sea_rock(class_name: str | None = None) -> str:
    return _safe(decor.sea_rock(class_name=class_name))


@register.simple_tag
def shoreline(class_name: str | None = None) -> str:
    return _safe(decor.shoreline(class_name=class_name))
