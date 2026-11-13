from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.content import EVENT
from core.locales import LOCALE_TAGS, LOCALES, OG_LOCALES, resolve_locale
from core.seo import event_json_ld


def index(request: HttpRequest) -> HttpResponse:
    locale = resolve_locale(request)
    context = {
        "locale": locale,
        "lang_tag": LOCALE_TAGS[locale],
        "og_locale": OG_LOCALES[locale],
        "og_locale_alternates": [OG_LOCALES[other] for other in LOCALES if other != locale],
        "event": EVENT,
        "locales": LOCALES,
        "json_ld": event_json_ld(locale),
    }
    return render(request, "landing/index.html", context)
