from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.locales import LOCALES, OG_LOCALES, Locale
from core.seo import event_json_ld


def index(request: HttpRequest) -> HttpResponse:
    # `core.middleware.LocaleMiddleware` resolved the locale; the shell context
    # (`locale`, `lang_tag`, `event`, switcher, footer) comes from
    # `core.context_processors.site`. Only head data specific to this page is here.
    locale: Locale = request.locale  # type: ignore[attr-defined]
    context = {
        "og_locale": OG_LOCALES[locale],
        "og_locale_alternates": [OG_LOCALES[other] for other in LOCALES if other != locale],
        "json_ld": event_json_ld(locale),
    }
    return render(request, "landing/index.html", context)
