"""Event facts: the single source of truth for everything the site states
about PyCon Latam 2027. Templates read from here and never inline a date, a
city or a URL.

Locale-dependent wording lives in `core.dictionary` instead.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EventDates:
    # ISO-8601 dates (YYYY-MM-DD). `None` until the committee announces them.
    start: str | None
    end: str | None
    # IANA time zone of the venue.
    time_zone: str


@dataclass(frozen=True, slots=True)
class EventSocial:
    x: str
    instagram: str
    linkedin: str
    facebook: str


@dataclass(frozen=True, slots=True)
class EventInfo:
    name: str
    year: int
    city: str
    country_code: str
    dates: EventDates
    canonical_url: str
    social: EventSocial


EVENT = EventInfo(
    name="PyCon Latam 2027",
    year=2027,
    city="Punta Cana",
    country_code="DO",
    dates=EventDates(
        start="2027-08-26",
        end="2027-08-29",
        time_zone="America/Santo_Domingo",
    ),
    canonical_url="https://2027.pylatam.org/",
    social=EventSocial(
        x="https://x.com/PyLatam",
        instagram="https://www.instagram.com/pyconlatam/",
        linkedin="https://www.linkedin.com/company/pylatam/",
        facebook="https://www.facebook.com/PyLatam/",
    ),
)
