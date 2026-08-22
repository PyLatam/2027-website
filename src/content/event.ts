/**
 * Event facts — the single source of truth for everything the site states
 * about PyCon Latam 2027. UI components must read from here, never inline
 * a date, a city or a URL.
 *
 * Locale-dependent wording lives in `src/i18n/dictionary.ts` instead.
 */

export interface EventVenue {
  readonly city: string;
  /** Country name keyed by locale, resolved by the dictionary layer. */
  readonly countryKey: 'venue.country';
}

export interface EventDates {
  /** ISO-8601 date (YYYY-MM-DD). `null` until the committee announces it. */
  readonly start: string | null;
  readonly end: string | null;
  /** IANA time zone of the venue. */
  readonly timeZone: string;
}

export interface EventInfo {
  readonly name: string;
  readonly edition: number;
  readonly year: number;
  readonly venue: EventVenue;
  readonly dates: EventDates;
  readonly canonicalUrl: string;
  readonly social: {
    readonly x: string;
    readonly instagram: string;
    readonly linkedin: string;
    readonly facebook: string;
  };
}

export const EVENT: EventInfo = {
  name: 'PyCon Latam 2027',
  edition: 2027,
  year: 2027,
  venue: {
    city: 'Punta Cana',
    countryKey: 'venue.country',
  },
  dates: {
    start: '2027-08-26',
    end: '2027-08-29',
    timeZone: 'America/Santo_Domingo',
  },
  canonicalUrl: 'https://pylatam.github.io/2027-website/',
  social: {
    x: 'https://x.com/PyLatam',
    instagram: 'https://www.instagram.com/pyconlatam/',
    linkedin: 'https://www.linkedin.com/company/pylatam/',
    facebook: 'https://www.facebook.com/PyLatam/',
  },
} as const;
