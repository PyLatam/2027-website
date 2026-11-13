"""Supported locales and how a request picks one."""

from typing import Literal, TypeGuard

from django.http import HttpRequest

Locale = Literal["es", "en"]

LOCALES: tuple[Locale, ...] = ("es", "en")

# Spanish is the primary language of the event and of the region.
DEFAULT_LOCALE: Locale = "es"

LOCALE_LABELS: dict[Locale, str] = {
    "es": "Español",
    "en": "English",
}

# BCP-47 tags for the `lang` attribute.
LOCALE_TAGS: dict[Locale, str] = {
    "es": "es-419",
    "en": "en",
}

# Open Graph locale identifiers.
OG_LOCALES: dict[Locale, str] = {
    "es": "es_419",
    "en": "en_US",
}


def is_locale(value: str | None) -> TypeGuard[Locale]:
    return value in LOCALES


def resolve_locale(request: HttpRequest) -> Locale:
    """Resolve the locale for a request: an explicit `?lang=` link, else Spanish.

    Phase 2 of the migration adds the remembered choice and `Accept-Language`.
    """
    value = request.GET.get("lang")
    return value if is_locale(value) else DEFAULT_LOCALE
