"""All user-facing copy. Keys are flat and namespaced with dots.

The keys mirror legacy-react/src/i18n/dictionary.ts so the two sites can be
compared side by side. `ES` is the reference: a test fails if `EN` is missing a
key or has an extra one, so translations can never drift.
"""

import re
from collections.abc import Mapping

from core.locales import Locale

ES: dict[str, str] = {
    "meta.title": "PyCon Latam 2027 — Punta Cana, República Dominicana",
    "meta.description": (
        "PyCon Latam 2027 nos lleva a Punta Cana, República Dominicana del 26 al 29 de "
        "agosto de 2027. La conferencia de la comunidad Python de Latinoamérica."
    ),
    "meta.ogDescription": "Nos vemos en Punta Cana, República Dominicana. 26 – 29 de agosto, 2027.",
    "meta.eventDescription": (
        "PyCon Latam 2027 en Punta Cana, República Dominicana. 26 – 29 de agosto de 2027."
    ),
    "hero.eyebrow": "PyCon Latam 2027",
    "hero.lead": "Nos vemos en",
    "hero.city": "Punta Cana,",
    "hero.country": "República Dominicana",
    "hero.dates": "26 – 29 de agosto, 2027",
    "hero.aria": (
        "PyCon Latam 2027. Nos vemos en Punta Cana, República Dominicana del 26 al 29 de "
        "agosto de 2027."
    ),
    "venue.country": "República Dominicana",
    "logo.alt": "Logotipo de PyCon Latam RD, Punta Cana",
    "lang.legend": "Idioma",
    "lang.switchTo": "Cambiar idioma a {language}",
    "lang.short.es": "ES",
    "lang.short.en": "EN",
    "skip.toContent": "Saltar al contenido",
    "footer.rights": "Todos los derechos reservados.",
    "social.x": "X (Twitter) de PyCon Latam",
    "social.instagram": "Instagram de PyCon Latam",
    "social.linkedin": "LinkedIn de PyCon Latam",
    "social.facebook": "Facebook de PyCon Latam",
}

EN: dict[str, str] = {
    "meta.title": "PyCon Latam 2027 — Punta Cana, Dominican Republic",
    "meta.description": (
        "PyCon Latam 2027 takes us to Punta Cana, Dominican Republic from August 26 to 29, "
        "2027. The conference of the Latin American Python community."
    ),
    "meta.ogDescription": "See you in Punta Cana, Dominican Republic. August 26 – 29, 2027.",
    "meta.eventDescription": (
        "PyCon Latam 2027 in Punta Cana, Dominican Republic. August 26 – 29, 2027."
    ),
    "hero.eyebrow": "PyCon Latam 2027",
    "hero.lead": "See you in",
    "hero.city": "Punta Cana,",
    "hero.country": "Dominican Republic",
    "hero.dates": "August 26 – 29, 2027",
    "hero.aria": (
        "PyCon Latam 2027. See you in Punta Cana, Dominican Republic from August 26 to 29, 2027."
    ),
    "venue.country": "Dominican Republic",
    "logo.alt": "PyCon Latam RD logo, Punta Cana",
    "lang.legend": "Language",
    "lang.switchTo": "Switch language to {language}",
    "lang.short.es": "ES",
    "lang.short.en": "EN",
    "skip.toContent": "Skip to content",
    "footer.rights": "All rights reserved.",
    "social.x": "PyCon Latam on X (Twitter)",
    "social.instagram": "PyCon Latam on Instagram",
    "social.linkedin": "PyCon Latam on LinkedIn",
    "social.facebook": "PyCon Latam on Facebook",
}

DICTIONARIES: dict[Locale, dict[str, str]] = {"es": ES, "en": EN}

_PLACEHOLDER = re.compile(r"\{(\w+)\}")


def interpolate(template: str, values: Mapping[str, str] | None = None) -> str:
    """Replace `{placeholder}` tokens; unknown placeholders are left as-is."""
    values = values or {}
    return _PLACEHOLDER.sub(lambda m: values.get(m.group(1), m.group(0)), template)


def translate(locale: Locale, key: str, values: Mapping[str, str] | None = None) -> str:
    """Look up a message. A missing key raises, so a typo fails loudly."""
    return interpolate(DICTIONARIES[locale][key], values)
