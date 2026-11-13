"""Context every page needs for the shell: locale, language switcher, footer."""

from dataclasses import dataclass

from django.http import HttpRequest

from core.content import EVENT
from core.locales import LOCALE_LABELS, LOCALE_PARAM, LOCALE_TAGS, LOCALES, Locale


@dataclass(frozen=True, slots=True)
class LanguageOption:
    code: Locale
    # Full language name, in its own language, for the accessible label.
    label: str
    short_key: str
    href: str
    active: bool


@dataclass(frozen=True, slots=True)
class SocialLink:
    label_key: str
    href: str
    # Template of the verbatim icon SVG.
    icon: str


def _social_links() -> tuple[SocialLink, ...]:
    # Same order as legacy-react/src/components/ui/Footer.tsx.
    return tuple(
        SocialLink(
            label_key=f"social.{network}",
            href=getattr(EVENT.social, network),
            icon=f"icons/{network}.svg",
        )
        for network in ("x", "instagram", "linkedin", "facebook")
    )


def site(request: HttpRequest) -> dict[str, object]:
    locale: Locale = request.locale  # type: ignore[attr-defined]
    return {
        "locale": locale,
        "lang_tag": LOCALE_TAGS[locale],
        "locales": LOCALES,
        "event": EVENT,
        "language_options": [
            LanguageOption(
                code=code,
                label=LOCALE_LABELS[code],
                short_key=f"lang.short.{code}",
                href=f"?{LOCALE_PARAM}={code}",
                active=code == locale,
            )
            for code in LOCALES
        ],
        "social_links": _social_links(),
    }
