"""Per-request locale: resolve it once and remember an explicit choice."""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.cache import patch_vary_headers

from core.locales import LOCALE_COOKIE, from_query_string, resolve_locale

# One year: long enough to feel permanent, short enough to expire eventually.
LOCALE_COOKIE_MAX_AGE = 60 * 60 * 24 * 365


class LocaleMiddleware:
    """Sets `request.locale` and, when the visitor followed a `?lang=` link,
    stores that choice in a cookie, replacing the React site's `localStorage`.

    The response depends on the cookie and on `Accept-Language`, so it says so
    in `Vary`; otherwise a shared cache could serve one visitor's language to
    another.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.locale = resolve_locale(request)  # type: ignore[attr-defined]
        response = self.get_response(request)

        chosen = from_query_string(request)
        if chosen is not None and request.COOKIES.get(LOCALE_COOKIE) != chosen:
            response.set_cookie(
                LOCALE_COOKIE,
                chosen,
                max_age=LOCALE_COOKIE_MAX_AGE,
                secure=request.is_secure(),
                # Only the server reads it.
                httponly=True,
                samesite="Lax",
            )
        patch_vary_headers(response, ("Cookie", "Accept-Language"))
        return response
