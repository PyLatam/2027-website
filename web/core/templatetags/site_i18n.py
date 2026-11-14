"""`{% t "key" %}`: look up a message for the current request's locale.

Usage: `{% load site_i18n %}` then `{% t "hero.lead" %}`, or with
placeholders `{% t "lang.switchTo" language="English" %}`. The locale comes
from the `locale` context variable that every view sets.
"""

from django import template

from core.dictionary import translate

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context: template.Context, key: str, **values: str) -> str:
    return translate(context["locale"], key, values)
