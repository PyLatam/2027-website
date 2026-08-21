export const LOCALES = ['es', 'en'] as const;

export type Locale = (typeof LOCALES)[number];

/** Spanish is the primary language of the event and of the region. */
export const DEFAULT_LOCALE: Locale = 'es';

export const LOCALE_LABELS: Record<Locale, string> = {
  es: 'Español',
  en: 'English',
};

/** BCP-47 tags used for the `lang` attribute and for Intl formatting. */
export const LOCALE_TAGS: Record<Locale, string> = {
  es: 'es-419',
  en: 'en',
};

export function isLocale(value: string | null | undefined): value is Locale {
  return value != null && (LOCALES as readonly string[]).includes(value);
}
