"""Structured data (JSON-LD) built from the event facts."""

import json
from typing import Any

from django.utils.safestring import SafeString, mark_safe

from core.content import EVENT
from core.dictionary import translate
from core.locales import LOCALES, Locale

# Characters that could close the surrounding <script> element.
_SCRIPT_ESCAPES = {ord("<"): "\\u003C", ord(">"): "\\u003E", ord("&"): "\\u0026"}


def event_json_ld(locale: Locale) -> SafeString:
    """The schema.org `Event` node, safe to place inside a <script> element."""
    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": EVENT.name,
        "description": translate(locale, "meta.eventDescription"),
        "startDate": EVENT.dates.start,
        "endDate": EVENT.dates.end,
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "url": EVENT.canonical_url,
        "inLanguage": list(LOCALES),
        "location": {
            "@type": "Place",
            "name": EVENT.city,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": EVENT.city,
                "addressCountry": EVENT.country_code,
            },
        },
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2).translate(_SCRIPT_ESCAPES)
    return mark_safe(payload)  # noqa: S308 — escaped above.
