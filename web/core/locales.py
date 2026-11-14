"""Supported locales and how a request picks one.

Mirrors legacy-react/src/i18n/{locales,detectLocale}.ts. The React site
resolves the locale in the browser and remembers it in `localStorage`; here the
server resolves it and remembers it in a cookie (see `core.middleware`).
"""

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

# Same name as the React site's `LOCALE_STORAGE_KEY`, now a cookie.
LOCALE_COOKIE = "pyconlatam.locale"

# The query parameter an explicit language link carries.
LOCALE_PARAM = "lang"


def is_locale(value: str | None) -> TypeGuard[Locale]:
    return value in LOCALES


def from_query_string(request: HttpRequest) -> Locale | None:
    value = request.GET.get(LOCALE_PARAM)
    return value if is_locale(value) else None


def from_cookie(request: HttpRequest) -> Locale | None:
    value = request.COOKIES.get(LOCALE_COOKIE)
    return value if is_locale(value) else None


def _parse_accept_language(header: str) -> list[str]:
    """Return the language ranges of an `Accept-Language` header, most preferred
    first. Ranges with `q=0` (explicitly unwanted) and malformed q-values are
    dropped; equal weights keep their header order, like `navigator.languages`.
    """
    weighted: list[tuple[float, str]] = []
    for part in header.split(","):
        range_, _, params = part.strip().partition(";")
        range_ = range_.strip()
        if not range_:
            continue
        quality = 1.0
        for param in params.split(";"):
            name, _, value = param.strip().partition("=")
            if name.strip().lower() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0.0
        if quality > 0:
            weighted.append((quality, range_))
    weighted.sort(key=lambda item: item[0], reverse=True)
    return [range_ for _, range_ in weighted]


def from_accept_language(request: HttpRequest) -> Locale | None:
    for language in _parse_accept_language(request.headers.get("Accept-Language", "")):
        base = language.split("-")[0].lower()
        if is_locale(base):
            return base
    return None


def resolve_locale(request: HttpRequest) -> Locale:
    """Resolution order, as in the React site: explicit `?lang=` link >
    previous choice (cookie) > browser preference (`Accept-Language`) > Spanish.
    """
    return (
        from_query_string(request)
        or from_cookie(request)
        or from_accept_language(request)
        or DEFAULT_LOCALE
    )
